# Douyin_TikTok_Download_API - 完整 API 文档

## 🌐 部署信息

- **Render 服务**: https://your-app.onrender.com
- **API 文档**: https://your-app.onrender.com/docs
- **ReDoc 文档**: https://your-app.onrender.com/redoc

---

## 📋 目录

1. [系统接口 (System APIs)](#系统接口)
2. [混合解析接口 (Hybrid APIs)](#混合解析接口)
3. [抖音接口 (Douyin APIs)](#抖音接口)
4. [TikTok 接口 (TikTok APIs)](#tiktok-接口)
5. [Bilibili 接口 (Bilibili APIs)](#bilibili-接口)
6. [下载接口 (Download APIs)](#下载接口)
7. [Cloudflare Worker 集成](#cloudflare-worker-集成)

---

## 系统接口

### 1. 健康检查（保活接口）

**用途**: 供 Cloudflare Worker 定时 ping，防止 Render 休眠

```http
GET /health
```

**响应示例**:
```json
{
  "status": "ok",
  "timestamp": "2026-08-28T15:30:00",
  "version": "V4.1.2",
  "environment": "Production"
}
```

**Worker 定时任务使用**:
```javascript
// 每 10 分钟调用一次
await fetch('https://your-app.onrender.com/health')
```

---

### 2. 获取系统状态

```http
GET /status
```

**响应示例**:
```json
{
  "api_version": "V4.1.2",
  "update_time": "2025/03/16",
  "environment": "Production",
  "worker_configured": true,
  "worker_url": "https://your-worker.workers.dev",
  "download_enabled": true,
  "web_enabled": true
}
```

---

### 3. 获取 Cookie 配置（从 Worker）

```http
GET /config/cookies
```

**响应示例**:
```json
{
  "douyin_cookie": "your_douyin_cookie_here",
  "tiktok_cookie": "your_tiktok_cookie_here",
  "bilibili_cookie": "your_bilibili_cookie_here"
}
```

**说明**: 此接口从 Cloudflare Worker KV 获取最新的 Cookie

---

### 4. 更新 Cookie（内部接口）

```http
POST /config/cookies/update?platform={platform}
Authorization: Bearer {your_secret}
Content-Type: text/plain

{cookie_string}
```

**参数**:
- `platform`: douyin | tiktok | bilibili
- `Authorization`: Bearer token (在环境变量 `UPDATE_SECRET` 中配置)

**响应示例**:
```json
{
  "status": "success",
  "message": "douyin cookie updated"
}
```

---

## 混合解析接口

### 解析视频数据（支持抖音/TikTok/Bilibili）

```http
GET /api/hybrid/video_data?url={video_url}&minimal=false
```

**参数**:
- `url`: 视频链接
- `minimal`: 是否返回最小化数据 (默认: false)

**支持的链接格式**:
- 抖音短链接: `https://v.douyin.com/xxx`
- 抖音完整链接: `https://www.douyin.com/video/123456`
- TikTok 短链接: `https://www.tiktok.com/t/xxx`
- TikTok 完整链接: `https://www.tiktok.com/@user/video/123456`
- Bilibili: `https://www.bilibili.com/video/BVxxx`

**响应示例**:
```json
{
  "code": 200,
  "message": "success",
  "data": {
    "aweme_id": "7123456789",
    "video_url": "https://...",
    "title": "视频标题",
    "author": "作者名",
    ...
  }
}
```

---

## 抖音接口

### 1. 获取视频数据

```http
GET /api/douyin/web/fetch_one_video?aweme_id={video_id}
```

### 2. 获取用户主页作品

```http
GET /api/douyin/web/fetch_user_post_videos?sec_user_id={user_id}&max_cursor=0&count=20
```

### 3. 获取用户信息

```http
GET /api/douyin/web/fetch_user_info?sec_user_id={user_id}
```

### 4. 获取直播流

```http
GET /api/douyin/web/fetch_user_live_videos?web_rid={room_id}
```

---

## TikTok 接口

### 1. 获取视频数据

```http
GET /api/tiktok/web/fetch_one_video?aweme_id={video_id}
```

### 2. 获取用户主页作品

```http
GET /api/tiktok/web/fetch_user_post_videos?sec_user_id={user_id}&max_cursor=0&count=20
```

### 3. 获取用户信息

```http
GET /api/tiktok/web/fetch_user_info?sec_user_id={user_id}
```

---

## Bilibili 接口

### 1. 获取视频详情

```http
GET /api/bilibili/web/fetch_video_info?bvid={bv_id}
```

### 2. 获取视频流地址

```http
GET /api/bilibili/web/fetch_video_stream?bvid={bv_id}&cid={cid}
```

### 3. 获取用户作品

```http
GET /api/bilibili/web/fetch_user_post_videos?mid={user_id}&pn=1&ps=20
```

---

## 下载接口

### 无水印下载（抖音/TikTok 混合）

```http
GET /api/download?url={video_url}&prefix=true&with_watermark=false
```

**参数**:
- `url`: 视频链接
- `prefix`: 是否添加文件前缀 (默认: true)
- `with_watermark`: 是否带水印 (默认: false)

**响应**: 直接返回视频文件流

---

## Cloudflare Worker 集成

### Worker 架构

```
┌─────────────────────────────────────┐
│   Cloudflare Worker (免费)          │
│  ┌────────────────────────────┐    │
│  │ 1. Cron: 每10分钟保活      │    │
│  │ 2. KV: 存储 Cookie          │    │
│  │ 3. API: 提供 Cookie 接口    │    │
│  └────────────────────────────┘    │
└─────────────────────────────────────┘
              ↕️
        HTTP 请求交互
              ↕️
┌─────────────────────────────────────┐
│   Render Service (免费)              │
│  ┌────────────────────────────┐    │
│  │ FastAPI + 爬虫逻辑         │    │
│  │ 启动时从 Worker 获取 Cookie │    │
│  └────────────────────────────┘    │
└─────────────────────────────────────┘
```

### Worker 需要提供的接口

#### 1. 保活接口（Cron Trigger）

```javascript
// wrangler.toml
[triggers]
crons = ["*/10 * * * *"]  # 每 10 分钟

// worker.js
async scheduled(event, env, ctx) {
  await fetch('https://your-app.onrender.com/health')
}
```

#### 2. Cookie 存储接口

```javascript
// GET /config - 获取所有 Cookie
export default {
  async fetch(request, env) {
    if (request.url.includes('/config')) {
      const douyin = await env.COOKIES.get('douyin_cookie')
      const tiktok = await env.COOKIES.get('tiktok_cookie')
      const bilibili = await env.COOKIES.get('bilibili_cookie')
      
      return new Response(JSON.stringify({
        douyin_cookie: douyin || '',
        tiktok_cookie: tiktok || '',
        bilibili_cookie: bilibili || ''
      }), {
        headers: { 'Content-Type': 'application/json' }
      })
    }
  }
}
```

#### 3. Cookie 更新接口

```javascript
// POST /cookie/{platform}
if (request.method === 'POST' && request.url.includes('/cookie/')) {
  const platform = request.url.split('/cookie/')[1]
  const cookie = await request.text()
  
  await env.COOKIES.put(`${platform}_cookie`, cookie)
  
  return new Response('Cookie updated')
}
```

### Worker KV 配置

```toml
[[kv_namespaces]]
binding = "COOKIES"
id = "your_kv_namespace_id"
```

### 环境变量配置

#### Render 环境变量

```bash
WORKER_COOKIE_URL=https://your-worker.workers.dev
UPDATE_SECRET=your-secret-key-here
```

#### Worker 环境变量

```bash
RENDER_URL=https://your-app.onrender.com
UPDATE_SECRET=your-secret-key-here
```

---

## 🚀 部署步骤

### 1. 部署到 Render

```bash
# 使用 Render CLI
render services create \
  --name douyin-tiktok-api \
  --type web \
  --repo https://github.com/Huhu-scr/Douyin_TikTok_Download_API \
  --plan free \
  --region oregon \
  --runtime docker
```

或使用 `render.yaml` 自动部署。

### 2. 配置环境变量

在 Render Dashboard 中设置：
- `WORKER_COOKIE_URL`: https://your-worker.workers.dev
- `UPDATE_SECRET`: 生成一个强密码

### 3. 部署 Cloudflare Worker

```bash
wrangler deploy
```

### 4. 初始化 Cookie

```bash
# 设置抖音 Cookie
curl -X POST https://your-worker.workers.dev/cookie/douyin \
  -H "Authorization: Bearer your-secret-key" \
  -H "Content-Type: text/plain" \
  --data "your_douyin_cookie"

# 设置 TikTok Cookie
curl -X POST https://your-worker.workers.dev/cookie/tiktok \
  -H "Authorization: Bearer your-secret-key" \
  -H "Content-Type: text/plain" \
  --data "your_tiktok_cookie"
```

---

## 📝 注意事项

1. **Cookie 管理**
   - Cookie 需要定期更新（建议每周检查）
   - 通过浏览器开发者工具获取 Cookie
   - 使用已登录账号的 Cookie 效果更好

2. **保活机制**
   - Worker Cron 每 10 分钟 ping `/health`
   - Render 免费版 15 分钟无活动会休眠
   - 保活可有效防止休眠

3. **限制和配额**
   - Render 免费版：750 小时/月
   - Cloudflare Workers：100,000 请求/天（免费）
   - Workers KV：100,000 读取/天（免费）

4. **性能优化**
   - Render 免费版 CPU：0.1 vCPU
   - 内存：512 MB
   - 响应时间：2-5 秒（冷启动 30-90 秒）

---

## 🔗 相关链接

- **原项目**: https://github.com/Evil0ctal/Douyin_TikTok_Download_API
- **Render 文档**: https://render.com/docs
- **Cloudflare Workers 文档**: https://developers.cloudflare.com/workers/
- **在线演示**: https://douyin.wtf

---

## 📄 许可证

Apache-2.0 License

---

生成时间: 2026-08-28
