# ==============================================================================
# System endpoints for health check and configuration management
# ==============================================================================

from fastapi import APIRouter, HTTPException, Header
from typing import Optional
import os
import httpx
from datetime import datetime
import yaml

router = APIRouter()

# Load config
config_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'config.yaml')
with open(config_path, 'r', encoding='utf-8') as file:
    config = yaml.safe_load(file)

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
    if not WORKER_COOKIE_URL:
        raise HTTPException(
            status_code=500,
            detail="WORKER_COOKIE_URL not configured"
        )

    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(f'{WORKER_COOKIE_URL}/config')
            if response.status_code == 200:
                return response.json()
            else:
                raise HTTPException(
                    status_code=response.status_code,
                    detail=f"Failed to fetch cookies from worker: {response.text}"
                )
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

    if not WORKER_COOKIE_URL:
        raise HTTPException(
            status_code=500,
            detail="WORKER_COOKIE_URL not configured"
        )

    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.post(
                f'{WORKER_COOKIE_URL}/cookie/{platform}',
                headers={'Authorization': authorization},
                content=cookie
            )
            if response.status_code == 200:
                return {"status": "success", "message": f"{platform} cookie updated"}
            else:
                raise HTTPException(
                    status_code=response.status_code,
                    detail=f"Failed to update cookie: {response.text}"
                )
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
