#!/usr/bin/env python3
# ==============================================================================
# Cookie loader from Cloudflare Worker
# This script runs on startup to fetch cookies from Worker KV
# ==============================================================================

import os
import httpx
import yaml
import asyncio

async def load_cookies_from_worker():
    """从 Worker 获取 Cookie 并更新配置文件"""
    worker_url = os.getenv('WORKER_COOKIE_URL', '')

    if not worker_url:
        print("⚠️  WORKER_COOKIE_URL not configured, skipping cookie update")
        return False

    print(f"🔄 Fetching cookies from Worker: {worker_url}")

    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(f'{worker_url}/config')

            if response.status_code == 200:
                cookies = response.json()
                print("✅ Cookies fetched successfully:")
                print(f"   - Douyin: {'✓' if cookies.get('douyin_cookie') else '✗'}")
                print(f"   - TikTok: {'✓' if cookies.get('tiktok_cookie') else '✗'}")
                print(f"   - Bilibili: {'✓' if cookies.get('bilibili_cookie') else '✗'}")

                # 设置为环境变量供运行时使用
                if cookies.get('douyin_cookie'):
                    os.environ['DOUYIN_COOKIE'] = cookies['douyin_cookie']
                if cookies.get('tiktok_cookie'):
                    os.environ['TIKTOK_COOKIE'] = cookies['tiktok_cookie']
                if cookies.get('bilibili_cookie'):
                    os.environ['BILIBILI_COOKIE'] = cookies['bilibili_cookie']

                return True
            else:
                print(f"❌ Failed to fetch cookies: HTTP {response.status_code}")
                return False

    except Exception as e:
        print(f"❌ Error fetching cookies from worker: {str(e)}")
        return False

if __name__ == "__main__":
    asyncio.run(load_cookies_from_worker())
