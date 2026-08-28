#!/bin/sh

echo "🚀 Starting Douyin_TikTok_Download_API..."

# Load cookies from Worker (if configured)
if [ -n "$WORKER_COOKIE_URL" ]; then
    echo "📥 Loading cookies from Cloudflare Worker..."
    python3 load_cookies.py
else
    echo "⚠️  WORKER_COOKIE_URL not set, skipping cookie loading"
fi

# Starting the Python application directly using python3
echo "🌐 Starting FastAPI server..."
python3 start.py
