# 🎯 Douyin_TikTok_Download_API - 完整 API 文档

## 📋 服务信息

- **服务名称**: Douyin_TikTok_Download_API
- **服务 URL**: https://celebrated-flexibility-production-2269.up.railway.app
- **项目 ID**: fa8c12cd-feba-4287-99ff-5b9698f45be2
- **部署环境**: Production
- **API 版本**: V4.1.2
- **鉴权状态**: ✅ 已启用

---

## 🔐 访问鉴权

**所有接口都需要携带访问密钥**，除了 `/api/health`（健康检查）。

### 密钥传递方式

```bash
# 方式 1: X-API-Key 请求头（推荐）
curl -H "X-API-Key: ak-your-key-here" "https://..."

# 方式 2: Authorization Bearer
curl -H "Authorization: Bearer ak-your-key-here" "https://..."

# 方式 3: 查询参数（浏览器场景）
https://...?key=ak-your-key-here
```

### 获取密钥

```bash
# 方式 1: 查看密钥文件
cat access_key.txt

# 方式 2: 使用生成脚本
python generate_access_key.py --show-only
```

### 错误响应

```json
// 401 - 缺少密钥
{"code":401,"detail":"Missing access key. 请通过请求头 X-API-Key、Authorization: Bearer <key> 或查询参数 ?key= 提供连接密钥。"}

// 403 - 密钥错误
{"code":403,"detail":"Invalid access key. 连接密钥无效。"}
```

---

## 🌐 基础 URL

```
https://celebrated-flexibility-production-2269.up.railway.app
```

---

## 📚 目录

1. [系统接口](#系统接口)
2. [混合解析接口](#混合解析接口)
3. [抖音接口](#抖音接口)
4. [TikTok 接口](#tiktok-接口)
5. [Bilibili 接口](#bilibili-接口)
6. [下载接口](#下载接口)
7. [iOS 快捷指令](#ios-快捷指令)
8. [Worker 集成](#worker-集成)
9. [完整示例](#完整示例)

---

## 🔧 系统接口

### 1. 健康检查（保活接口）

用于 Cloudflare Worker 定时 ping，防止服务休眠。**该接口无需密钥**。

**请求**：
```http
GET /api/health
```

**响应**：
```json
{
  "status": "ok",
  "timestamp": "2026-08-28T17:30:00.000Z",
  "version": "V4.1.2",
  "environment": "Production"
}
```

**使用场景**：
- Worker Cron 每 10 分钟调用
- 监控服务健康状态
- 防止 Railway 休眠

---

### 2. 系统状态

获取服务的详细状态信息。**需要密钥**。

**请求**：
```http
GET /api/status
X-API-Key: ak-your-key-here
```

**响应**：
```json
{
  "api_version": "V4.1.2",
  "update_time": "2026/08/28",
  "environment": "Production",
  "worker_configured": true,
  "worker_url": "https://your-worker.workers.dev",
  "download_enabled": true,
  "web_enabled": true
}
```

---

### 3. 获取 Cookie 配置

从 Cloudflare Worker KV 获取所有平台的 Cookie。

**请求**：
```http
GET /config/cookies
```

**响应**：
```json
{
  "douyin_cookie": "your_douyin_cookie_here",
  "tiktok_cookie": "your_tiktok_cookie_here",
  "bilibili_cookie": "your_bilibili_cookie_here"
}
```

**错误响应**：
```json
{
  "detail": "WORKER_COOKIE_URL not configured"
}
```

---

### 4. 更新 Cookie（内部接口）

更新指定平台的 Cookie。

**请求**：
```http
POST /config/cookies/update?platform={platform}
Authorization: Bearer {your_secret}
Content-Type: text/plain

{cookie_string}
```

**参数**：
- `platform`: `douyin` | `tiktok` | `bilibili`
- `Authorization`: Bearer token（环境变量 `UPDATE_SECRET`）

**响应**：
```json
{
  "status": "success",
  "message": "douyin cookie updated"
}
```

**示例**：
```bash
curl -X POST "https://your-app.railway.app/config/cookies/update?platform=douyin" \
  -H "Authorization: Bearer your-secret-key" \
  -H "Content-Type: text/plain" \
  --data "your_douyin_cookie"
```

---

## 🎬 混合解析接口

### 解析视频数据（通用）

自动识别抖音、TikTok、Bilibili 链接并解析。

**请求**：
```http
GET /api/hybrid/video_data?url={video_url}&minimal=false
```

**参数**：
- `url` (required): 视频链接
- `minimal` (optional): 是否返回最小化数据，默认 `false`

**支持的链接格式**：

| 平台 | 短链接 | 完整链接 |
|------|--------|----------|
| 抖音 | `https://v.douyin.com/xxx` | `https://www.douyin.com/video/123456` |
| TikTok | `https://vm.tiktok.com/xxx` | `https://www.tiktok.com/@user/video/123456` |
| Bilibili | - | `https://www.bilibili.com/video/BVxxx` |

**响应示例**（抖音）：
```json
{
  "code": 200,
  "message": "success",
  "data": {
    "aweme_id": "7398765432100000000",
    "title": "视频标题",
    "author": {
      "nickname": "作者昵称",
      "uid": "MS4wLjABAAAA...",
      "sec_uid": "MS4wLjABAAAA...",
      "avatar": "https://..."
    },
    "video": {
      "play_addr": "https://...",
      "cover": "https://...",
      "duration": 15000,
      "width": 1080,
      "height": 1920
    },
    "statistics": {
      "digg_count": 10000,
      "comment_count": 500,
      "share_count": 200,
      "play_count": 50000
    },
    "create_time": 1724832000
  }
}
```

**错误响应**：
```json
{
  "code": 400,
  "message": "Invalid URL format"
}
```

---

## 🎵 抖音接口

### 1. 获取单个视频数据

**请求**：
```http
GET /api/douyin/web/fetch_one_video?aweme_id={video_id}
```

**参数**：
- `aweme_id` (required): 视频 ID

**示例**：
```bash
curl "https://your-app.railway.app/api/douyin/web/fetch_one_video?aweme_id=7398765432100000000"
```

---

### 2. 获取用户主页作品

**请求**：
```http
GET /api/douyin/web/fetch_user_post_videos?sec_user_id={user_id}&max_cursor=0&count=20
```

**参数**：
- `sec_user_id` (required): 用户 ID
- `max_cursor` (optional): 分页游标，默认 `0`
- `count` (optional): 每页数量，默认 `20`

**响应**：
```json
{
  "code": 200,
  "message": "success",
  "data": {
    "videos": [
      {
        "aweme_id": "...",
        "title": "...",
        ...
      }
    ],
    "has_more": true,
    "max_cursor": 20
  }
}
```

---

### 3. 获取用户信息

**请求**：
```http
GET /api/douyin/web/fetch_user_info?sec_user_id={user_id}
```

**参数**：
- `sec_user_id` (required): 用户 ID

---

### 4. 获取直播流

**请求**：
```http
GET /api/douyin/web/fetch_user_live_videos?web_rid={room_id}
```

**参数**：
- `web_rid` (required): 直播间 ID

---

## 🌍 TikTok 接口

### 1. 获取单个视频数据

**请求**：
```http
GET /api/tiktok/web/fetch_one_video?aweme_id={video_id}
```

**参数**：
- `aweme_id` (required): 视频 ID

---

### 2. 获取用户主页作品

**请求**：
```http
GET /api/tiktok/web/fetch_user_post_videos?sec_user_id={user_id}&max_cursor=0&count=20
```

---

### 3. 获取用户信息

**请求**：
```http
GET /api/tiktok/web/fetch_user_info?sec_user_id={user_id}
```

---

## 📺 Bilibili 接口

### 1. 获取视频详情

**请求**：
```http
GET /api/bilibili/web/fetch_video_info?bvid={bv_id}
```

**参数**：
- `bvid` (required): BV 号，例如 `BV1xx411c7mD`

---

### 2. 获取视频流地址

**请求**：
```http
GET /api/bilibili/web/fetch_video_stream?bvid={bv_id}&cid={cid}
```

**参数**：
- `bvid` (required): BV 号
- `cid` (required): 视频分 P 的 CID

---

### 3. 获取用户作品

**请求**：
```http
GET /api/bilibili/web/fetch_user_post_videos?mid={user_id}&pn=1&ps=20
```

**参数**：
- `mid` (required): 用户 UID
- `pn` (optional): 页码，默认 `1`
- `ps` (optional): 每页数量，默认 `20`

---

## 📥 下载接口

### 无水印下载

**请求**：
```http
GET /api/download?url={video_url}&prefix=true&with_watermark=false
```

**参数**：
- `url` (required): 视频链接
- `prefix` (optional): 是否添加文件名前缀，默认 `true`
- `with_watermark` (optional): 是否带水印，默认 `false`

**响应**：
- 直接返回视频文件流
- Content-Type: `video/mp4`
- Content-Disposition: `attachment; filename="..."`

**示例**：
```bash
curl -o video.mp4 "https://your-app.railway.app/api/download?url=https://v.douyin.com/xxx"
```

---

## 📱 iOS 快捷指令

### 获取快捷指令信息

**请求**：
```http
GET /api/ios/shortcut_info
```

**响应**：
```json
{
  "version": "7.0",
  "update_time": "2024/07/05",
  "link": "https://www.icloud.com/shortcuts/...",
  "link_en": "https://www.icloud.com/shortcuts/...",
  "update_note": "重构了快捷指令以兼容TikHub API。",
  "update_note_en": "Refactored the shortcut to be compatible with the TikHub API."
}
```

---

## 🔗 Worker 集成

### Worker 架构

```
┌────────────────────────────────────────┐
│   Cloudflare Worker (免费)             │
│                                         │
│   接口：                                │
│   • GET /health                        │
│   • GET /config                        │
│   • GET /cookie/{platform}             │
│   • POST /cookie/{platform}            │
│                                         │
│   Cron: 每 10 分钟 ping Railway       │
└────────────────────────────────────────┘
              ↕️ HTTP
┌────────────────────────────────────────┐
│   Railway Service                      │
│                                         │
│   接口：                                │
│   • GET /health                        │
│   • GET /status                        │
│   • GET /config/cookies                │
│   • POST /config/cookies/update        │
│   • GET /api/hybrid/video_data         │
│   • ... 其他所有 API                   │
└────────────────────────────────────────┘
```

### Worker 接口

#### 1. Worker 健康检查

**请求**：
```http
GET https://your-worker.workers.dev/health
```

**响应**：
```json
{
  "status": "ok",
  "timestamp": "2026-08-28T...",
  "worker": "douyin-api-manager"
}
```

---

#### 2. 获取所有 Cookie

**请求**：
```http
GET https://your-worker.workers.dev/config
```

**响应**：
```json
{
  "douyin_cookie": "...",
  "tiktok_cookie": "...",
  "bilibili_cookie": "...",
  "metadata": {
    "douyin_updated_at": "2026-08-28T...",
    "tiktok_updated_at": "never",
    "bilibili_updated_at": "never"
  }
}
```

---

#### 3. 更新 Cookie

**请求**：
```http
POST https://your-worker.workers.dev/cookie/douyin
Authorization: Bearer {your_secret}
Content-Type: text/plain

{cookie_content}
```

**响应**：
```json
{
  "status": "success",
  "message": "douyin cookie updated",
  "timestamp": "2026-08-28T..."
}
```

---

## 💡 完整示例

### 示例 1: 解析抖音视频

```bash
# 1. 使用混合接口（推荐）
curl "https://your-app.railway.app/api/hybrid/video_data?url=https://v.douyin.com/iFhnojQT/"

# 2. 响应
{
  "code": 200,
  "message": "success",
  "data": {
    "aweme_id": "7398765432100000000",
    "title": "这是一个测试视频",
    "video": {
      "play_addr": "https://aweme.snssdk.com/aweme/v1/play/?video_id=...",
      "download_addr": "https://aweme.snssdk.com/aweme/v1/play/?video_id=..."
    }
  }
}
```

---

### 示例 2: 下载无水印视频

```bash
# 直接下载
curl -o video.mp4 "https://your-app.railway.app/api/download?url=https://v.douyin.com/iFhnojQT/"
```

---

### 示例 3: 通过 Worker 管理 Cookie

```bash
# 1. 上传抖音 Cookie 到 Worker
curl -X POST "https://your-worker.workers.dev/cookie/douyin" \
  -H "Authorization: Bearer your-secret-key" \
  -H "Content-Type: text/plain" \
  --data "your_douyin_cookie_here"

# 2. Railway 自动从 Worker 获取 Cookie
# 每次启动时自动加载，或通过接口手动获取
curl "https://your-app.railway.app/config/cookies"
```

---

### 示例 4: Worker 保活

```javascript
// Worker Cron Trigger (每 10 分钟)
export default {
  async scheduled(event, env, ctx) {
    await fetch('https://your-app.railway.app/health')
  }
}
```

---

## 🔐 认证和安全

### 环境变量

| 变量名 | 必需 | 说明 |
|--------|------|------|
| `WORKER_COOKIE_URL` | 是 | Worker URL |
| `UPDATE_SECRET` | 是 | Cookie 更新密钥 |
| `PORT` | 否 | 端口（Railway 自动设置） |

### Cookie 管理

1. **获取 Cookie**：
   - 浏览器登录平台
   - F12 开发者工具
   - Network → 选择请求 → Headers → Cookie

2. **上传到 Worker**：
   ```bash
   curl -X POST "https://worker.workers.dev/cookie/douyin" \
     -H "Authorization: Bearer your-secret" \
     --data "cookie_content"
   ```

3. **Railway 自动加载**：
   - 启动时自动从 Worker 获取
   - 或手动调用 `/config/cookies`

---

## 📊 响应代码

| 代码 | 说明 |
|------|------|
| 200 | 成功 |
| 400 | 请求参数错误 |
| 401 | 未授权（Cookie 更新接口） |
| 404 | 资源不存在 |
| 500 | 服务器内部错误 |

---

## 🔍 错误处理

### 常见错误

1. **Cookie 失效**：
```json
{
  "code": 403,
  "message": "Cookie expired or invalid"
}
```
**解决**：更新 Cookie

2. **视频不存在**：
```json
{
  "code": 404,
  "message": "Video not found"
}
```

3. **Worker 未配置**：
```json
{
  "detail": "WORKER_COOKIE_URL not configured"
}
```
**解决**：设置环境变量

---

## 🚀 快速测试

### 测试命令

```bash
# 1. 健康检查
curl https://your-app.railway.app/health

# 2. 系统状态
curl https://your-app.railway.app/status

# 3. 解析抖音视频
curl "https://your-app.railway.app/api/hybrid/video_data?url=https://v.douyin.com/iFhnojQT/"

# 4. API 文档
open https://your-app.railway.app/docs
```

---

## 📚 交互式文档

部署完成后，访问以下 URL 获取交互式 API 文档：

- **Swagger UI**: `https://your-app.railway.app/docs`
- **ReDoc**: `https://your-app.railway.app/redoc`

---

## 💰 成本优化

### Railway 使用建议

1. **最小化资源**：
   - 使用 0.5 vCPU
   - 使用 512 MB RAM

2. **数据存储**：
   - ✅ Cookie 存在 Worker KV（免费）
   - ❌ 不使用 Railway 数据库

3. **监控用量**：
   ```
   https://railway.com/account/usage
   ```

---

## 🔗 相关链接

- **Railway Dashboard**: https://railway.com/project/fa8c12cd-feba-4287-99ff-5b9698f45be2
- **GitHub 仓库**: https://github.com/Huhu-scr/Douyin_TikTok_Download_API
- **原项目**: https://github.com/Evil0ctal/Douyin_TikTok_Download_API

---

## 📄 许可证

Apache-2.0 License

---

**生成时间**: 2026-08-28
**文档版本**: 1.0.0
