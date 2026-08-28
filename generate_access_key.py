# ==============================================================================
# 生成连接密钥 / Generate the API access key
#
# 用法 / Usage:
#   python generate_access_key.py            # 生成并写入 access_key.txt
#   python generate_access_key.py --show     # 生成、写入并在终端显示
#   python generate_access_key.py --show-only  # 只显示已有密钥，不重新生成
#
# 密钥格式 / Format: ak- + 32 hex chars
# 文件 access_key.txt 已加入 .gitignore，不会被提交。
# ==============================================================================

import os
import re
import secrets
import stat
import sys

# 该脚本刻意不导入 app 包，以便在未安装项目依赖的机器上也能生成密钥
KEY_PATTERN = re.compile(r'^ak-[0-9a-f]{32}$')

KEY_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'access_key.txt')


def generate_access_key() -> str:
    return f'ak-{secrets.token_hex(16)}'


def read_existing() -> str:
    if not os.path.exists(KEY_FILE):
        return ''
    with open(KEY_FILE, 'r', encoding='utf-8') as file:
        return file.read().strip()


def write_key(key: str) -> None:
    with open(KEY_FILE, 'w', encoding='utf-8') as file:
        file.write(key + '\n')
    try:
        # 仅当前用户可读写 / Owner read-write only
        os.chmod(KEY_FILE, stat.S_IRUSR | stat.S_IWUSR)
    except OSError:
        pass


def main() -> int:
    args = sys.argv[1:]
    show = '--show' in args
    show_only = '--show-only' in args

    if show_only:
        key = read_existing()
        if not key:
            print(f'No key file found at {KEY_FILE}. Run without --show-only to create one.')
            return 1
        if not KEY_PATTERN.match(key):
            print(f'Key in {KEY_FILE} does not match the required format ak-<32 hex>.')
            return 1
        print(key)
        return 0

    existing = read_existing()
    if existing and '--force' not in args:
        print(f'A key already exists at {KEY_FILE}.')
        print('Use --show-only to print it, or --force to overwrite.')
        return 1

    key = generate_access_key()
    write_key(key)

    print(f'Access key written to: {KEY_FILE}')
    print(f'Length check: {len(key)} chars, format valid: {bool(KEY_PATTERN.match(key))}')
    if show:
        print(f'Key: {key}')
    else:
        print('Key not printed. Run with --show-only to display it, '
              'or open the file directly.')
    print('\nRemember to set the same value on your deployment platform:')
    print('  railway variables --set "API_ACCESS_KEY=<your key>" --service <service>')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
