# 使用官方 Python 3.11 的轻量版镜像
FROM python:3.11-slim

LABEL maintainer="Evil0ctal"

# 设置非交互模式，避免 Docker 构建时的交互问题
ENV DEBIAN_FRONTEND=noninteractive

# 设置工作目录
WORKDIR /app

# 复制应用代码到容器
COPY . /app

# 使用 Aliyun 镜像源加速 pip
RUN pip install -i https://mirrors.aliyun.com/pypi/simple/ -U pip \
    && pip config set global.index-url https://mirrors.aliyun.com/pypi/simple/

# 安装依赖
RUN pip install --no-cache-dir -r requirements.txt

# 暴露端口
EXPOSE 8000

# 直接使用 Python 启动，避免 shell 脚本问题
# 如果设置了 WORKER_COOKIE_URL，先加载 Cookie
CMD python load_cookies.py 2>/dev/null || true && python start.py
