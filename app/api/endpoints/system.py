# ==============================================================================
# System endpoints for health check and configuration management
# ==============================================================================

from fastapi import APIRouter, HTTPException, Header
from typing import Optional
import os
import httpx
from datetime import datetime
import yaml

from crawlers.utils import cookie_provider

router = APIRouter()

# Load config - try multiple paths
config = None
config_paths = [
    os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'config.yaml'),
    os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))), 'config.yaml'),
    '/app/config.yaml'
]

for config_path in config_paths:
    if os.path.exists(config_path):
        with open(config_path, 'r', encoding='utf-8') as file:
            config = yaml.safe_load(file)
        break

# Fallback config if file not found
if config is None:
    config = {
        'API': {
            'Version': 'V4.1.2',
            'Update_Time': '2026/08/28',
            'Environment': 'Production',
            'Download_Switch': True
        },
        'Web': {
            'PyWebIO_Enable': True
        }
    }

WORKER_COOKIE_URL = os.getenv('WORKER_COOKIE_URL', '')


@router.get("/health", tags=["System"])
async def health_check():
    """
    健康检查接口 / Health Check Endpoint

    用于 Cloudflare Worker 保活 ping
    For Cloudflare Worker keep-alive ping
    """
    return {
        "status": "ok",
        "timestamp": datetime.now().isoformat(),
        "version": config['API']['Version'],
        "environment": config['API']['Environment']
    }


@router.get("/config/cookies", tags=["System"])
async def get_cookies_config():
    """
    获取 Cookie 配置（从 Worker 获取）
    Get Cookie configuration (from Worker)

    此接口从 Cloudflare Worker 获取最新的 Cookie
    This endpoint fetches latest cookies from Cloudflare Worker
    """
    if not cookie_provider.is_remote_enabled():
        raise HTTPException(
            status_code=500,
            detail="WORKER_COOKIE_URL / MEDIA_ACCESS_KEY not configured"
        )

    try:
        return await cookie_provider.refresh()
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error fetching cookies: {str(e)}"
        )


@router.post("/config/cookies/update", tags=["System"])
async def update_cookie(
    platform: str,
    cookie: str,
    authorization: Optional[str] = Header(None)
):
    """
    更新指定平台的 Cookie（仅供内部使用）
    Update cookie for specified platform (internal use only)

    平台: douyin, tiktok, bilibili
    Platforms: douyin, tiktok, bilibili
    """
    # 简单的认证检查
    secret = os.getenv('UPDATE_SECRET', 'change-me-in-production')
    if authorization != f"Bearer {secret}":
        raise HTTPException(status_code=401, detail="Unauthorized")

    if platform not in ['douyin', 'tiktok', 'bilibili']:
        raise HTTPException(
            status_code=400,
            detail="Invalid platform. Must be: douyin, tiktok, or bilibili"
        )

    if not cookie_provider.is_remote_enabled():
        raise HTTPException(
            status_code=500,
            detail="WORKER_COOKIE_URL / MEDIA_ACCESS_KEY not configured"
        )

    worker_token = os.getenv('WORKER_ADMIN_TOKEN', '')
    if not worker_token:
        raise HTTPException(
            status_code=500,
            detail="WORKER_ADMIN_TOKEN not configured (required to write cookies)"
        )

    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.put(
                cookie_provider.cookie_write_endpoint(platform),
                headers={'Authorization': f'Bearer {worker_token}'},
                json={'cookie': cookie}
            )
            if response.status_code == 200:
                await cookie_provider.refresh()
                return {"status": "success", "message": f"{platform} cookie updated"}
            else:
                raise HTTPException(
                    status_code=response.status_code,
                    detail=f"Failed to update cookie: {response.text}"
                )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error updating cookie: {str(e)}"
        )


@router.get("/status", tags=["System"])
async def get_status():
    """
    获取系统状态信息
    Get system status information
    """
    return {
        "api_version": config['API']['Version'],
        "update_time": config['API']['Update_Time'],
        "environment": config['API']['Environment'],
        "worker_configured": bool(WORKER_COOKIE_URL),
        "worker_url": WORKER_COOKIE_URL if WORKER_COOKIE_URL else "Not configured",
        "download_enabled": config['API']['Download_Switch'],
        "web_enabled": config['Web']['PyWebIO_Enable']
    }
