# Cookie 提供者：从 Cloudflare Worker 拉取 Cookie，不在本地持久化
#
# 设计要点：
#   1. Railway 容器不存储 Cookie，全部由 Worker KV 托管
#   2. 内存缓存 + TTL，避免每个请求都打 Worker
#   3. Worker 不可用时回退到 config.yaml 中的静态 Cookie，保证可用性

import asyncio
import os
import time

import httpx

# 环境变量配置
# 沿用仓库既有命名（system.py / load_cookies.py 同名），避免多套变量并存。
# WORKER_COOKIE_URL 既可填站点根，也可填完整的 /admin/api/media/cookies 端点。
WORKER_COOKIE_URL = os.getenv("WORKER_COOKIE_URL", "").rstrip("/")
MEDIA_ACCESS_KEY = os.getenv("MEDIA_ACCESS_KEY", "")
COOKIE_TTL = int(os.getenv("COOKIE_TTL", "60"))

_COOKIES_PATH = "/admin/api/media/cookies"


def _cookies_endpoint() -> str:
    if WORKER_COOKIE_URL.endswith(_COOKIES_PATH):
        return WORKER_COOKIE_URL
    return f"{WORKER_COOKIE_URL}{_COOKIES_PATH}"

_cache = {}
_cache_at = 0.0
_lock = asyncio.Lock()


def is_remote_enabled() -> bool:
    return bool(WORKER_COOKIE_URL and MEDIA_ACCESS_KEY)


async def _fetch_remote() -> dict:
    url = _cookies_endpoint()
    async with httpx.AsyncClient(timeout=10.0) as client:
        response = await client.get(url, headers={"X-Upstream-Key": MEDIA_ACCESS_KEY})
        response.raise_for_status()
        payload = response.json()

    if not payload.get("success"):
        raise ValueError(f"Worker returned failure: {payload.get('error')}")

    data = payload.get("data") or {}
    return {
        "douyin": data.get("douyin") or "",
        "tiktok": data.get("tiktok") or "",
    }


async def get_cookie(platform: str, fallback: str = "") -> str:
    """获取指定平台的 Cookie。

    platform: "douyin" 或 "tiktok"
    fallback: Worker 不可用时使用的兜底 Cookie（通常来自 config.yaml）
    """
    global _cache, _cache_at

    if not is_remote_enabled():
        return fallback

    now = time.monotonic()
    if _cache and now - _cache_at < COOKIE_TTL:
        return _cache.get(platform) or fallback

    async with _lock:
        # 双重检查：可能已被其他协程刷新
        now = time.monotonic()
        if _cache and now - _cache_at < COOKIE_TTL:
            return _cache.get(platform) or fallback

        try:
            _cache = await _fetch_remote()
            _cache_at = now
            print(f"[cookie_provider] Synced from Worker, "
                  f"douyin={len(_cache['douyin'])} tiktok={len(_cache['tiktok'])}")
        except Exception as error:
            print(f"[cookie_provider] Sync failed ({error}), using fallback")
            # 保留旧缓存（若有），否则回退到静态配置
            return _cache.get(platform) or fallback

    return _cache.get(platform) or fallback


async def refresh() -> dict:
    """强制刷新缓存，返回各平台 Cookie 长度。"""
    global _cache, _cache_at

    if not is_remote_enabled():
        return {"enabled": False}

    async with _lock:
        _cache = await _fetch_remote()
        _cache_at = time.monotonic()

    return {
        "enabled": True,
        "douyin": len(_cache["douyin"]),
        "tiktok": len(_cache["tiktok"]),
    }
