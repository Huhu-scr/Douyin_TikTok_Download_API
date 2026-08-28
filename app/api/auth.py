# ==============================================================================
# Access key authentication
# 所有请求必须携带连接密钥，格式为 ak- 加 32 位十六进制字符
# ==============================================================================

import os
import re
import secrets
import yaml
from typing import Optional

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse

KEY_PATTERN = re.compile(r'^ak-[0-9a-f]{32}$')

# 请求中携带密钥的位置 / Where the key can be provided
HEADER_NAME = 'X-API-Key'
QUERY_NAME = 'key'
COOKIE_NAME = 'api_access_key'

# 无需鉴权的路径 / Paths that skip authentication
# Railway 平台健康检查无法自定义请求头，因此必须放行
DEFAULT_EXEMPT_PATHS = ('/api/health',)


def _load_config() -> dict:
    config_paths = [
        os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'config.yaml'),
        '/app/config.yaml',
    ]
    for path in config_paths:
        if os.path.exists(path):
            with open(path, 'r', encoding='utf-8') as file:
                return yaml.safe_load(file) or {}
    return {}


def _read_key_file(path: str) -> Optional[str]:
    if not path:
        return None
    if not os.path.isabs(path):
        base = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        path = os.path.join(base, path)
    if not os.path.exists(path):
        return None
    with open(path, 'r', encoding='utf-8') as file:
        return file.read().strip() or None


def load_access_key() -> Optional[str]:
    """
    按优先级读取密钥：环境变量 > 密钥文件 > config.yaml
    Resolve the access key: environment variable > key file > config.yaml
    """
    auth_config = _load_config().get('Auth') or {}

    key = os.getenv('API_ACCESS_KEY', '').strip()
    if not key:
        key_file = os.getenv('API_ACCESS_KEY_FILE', '') or auth_config.get('Access_Key_File', '')
        key = _read_key_file(key_file) or ''
    if not key:
        key = str(auth_config.get('Access_Key') or '').strip()

    return key or None


def is_auth_enabled() -> bool:
    override = os.getenv('API_AUTH_ENABLE', '').strip().lower()
    if override in ('1', 'true', 'yes'):
        return True
    if override in ('0', 'false', 'no'):
        return False
    auth_config = _load_config().get('Auth') or {}
    return bool(auth_config.get('Enable', False))


def generate_access_key() -> str:
    """生成一个符合格式要求的密钥 / Generate a key in the required format"""
    return f'ak-{secrets.token_hex(16)}'


def extract_key(request: Request) -> Optional[str]:
    """从请求头、查询参数或 Cookie 中取出密钥"""
    key = request.headers.get(HEADER_NAME)
    if key:
        return key.strip()

    authorization = request.headers.get('Authorization', '')
    if authorization.lower().startswith('bearer '):
        return authorization[7:].strip()

    key = request.query_params.get(QUERY_NAME)
    if key:
        return key.strip()

    return request.cookies.get(COOKIE_NAME)


class AccessKeyMiddleware(BaseHTTPMiddleware):
    """
    校验每个 HTTP 请求的连接密钥。
    浏览器通过 ?key=ak-... 首次访问后会写入 Cookie，便于 /docs 等页面继续加载资源。

    注意：该中间件只作用于 HTTP 请求，PyWebIO 的 WebSocket 连接不经过此处，
    但其入口页面仍受保护。
    """

    def __init__(self, app, exempt_paths: tuple = DEFAULT_EXEMPT_PATHS):
        super().__init__(app)
        self.exempt_paths = exempt_paths
        self.access_key = load_access_key()

    async def dispatch(self, request: Request, call_next):
        path = request.url.path

        if path in self.exempt_paths:
            return await call_next(request)

        if not self.access_key:
            return JSONResponse(
                status_code=503,
                content={
                    'code': 503,
                    'detail': 'Access key is not configured on the server. '
                              '服务端未配置连接密钥，已拒绝全部请求。',
                },
            )

        provided = extract_key(request)
        if not provided:
            return JSONResponse(
                status_code=401,
                content={
                    'code': 401,
                    'detail': f'Missing access key. 请通过请求头 {HEADER_NAME}、'
                              f'Authorization: Bearer <key> 或查询参数 ?{QUERY_NAME}= 提供连接密钥。',
                },
            )

        if not KEY_PATTERN.match(provided) or not secrets.compare_digest(provided, self.access_key):
            return JSONResponse(
                status_code=403,
                content={'code': 403, 'detail': 'Invalid access key. 连接密钥无效。'},
            )

        response = await call_next(request)

        # 浏览器场景：用查询参数通过校验后写入 Cookie，后续同源请求自动携带
        if request.query_params.get(QUERY_NAME) and request.cookies.get(COOKIE_NAME) != provided:
            response.set_cookie(
                COOKIE_NAME,
                provided,
                httponly=True,
                samesite='lax',
                secure=request.url.scheme == 'https',
                max_age=60 * 60 * 24 * 30,
            )

        return response
