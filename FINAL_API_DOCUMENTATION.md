# 🎉 Railway 部署成功！完整 API 文档

## ✅ 部署状态：成功运行

### 服务信息
- **状态**: ✅ 正常运行
- **服务名称**: Douyin_TikTok_Download_API
- **服务 URL**: `https://celebrated-flexibility-production-2269.up.railway.app`
- **API 版本**: V4.1.2
- **部署时间**: 2026-08-28
- **健康检查**: ✅ 通过
- **鉴权状态**: ✅ 已启用

### 🔐 访问密钥（重要）

**所有接口都需要携带访问密钥**，除了 `/api/health`（健康检查）。

#### 三种传递方式

```bash
# 方式 1: X-API-Key 请求头（推荐）
curl -H "X-API-Key: ak-your-key-here" "https://celebrated-flexibility-production-2269.up.railway.app/api/status"

# 方式 2: Authorization Bearer
curl -H "Authorization: Bearer ak-your-key-here" "https://celebrated-flexibility-production-2269.up.railway.app/api/status"

# 方式 3: 查询参数（浏览器场景，会自动写入 Cookie）
https://celebrated-flexibility-production-2269.up.railway.app/docs?key=ak-your-key-here
```

#### 获取密钥

密钥存储在项目根目录的 `access_key.txt` 文件中（该文件已被 `.gitignore` 排除，不会提交到仓库）。

```bash
# 查看密钥
cat access_key.txt

# 或使用生成脚本
python generate_access_key.py --show-only
```

#### 错误响应

```bash
# 缺少密钥 → 401
{"code":401,"detail":"Missing access key. 请通过请求头 X-API-Key、Authorization: Bearer <key> 或查询参数 ?key= 提供连接密钥。"}

# 密钥错误 → 403
{"code":403,"detail":"Invalid access key. 连接密钥无效。"}
```

### 快速测试

```bash
# 设置密钥（替换为你的实际密钥）
export API_KEY="ak-your-key-here"

# 健康检查 - 无需密钥 ✅
curl https://celebrated-flexibility-production-2269.up.railway.app/api/health
# 响应: {"status":"ok","timestamp":"2026-08-28T...","version":"V4.1.2","environment":"Demo"}

# 系统状态 - 需要密钥 ✅
curl -H "X-API-Key: $API_KEY" https://celebrated-flexibility-production-2269.up.railway.app/api/status
# 响应: {"api_version":"V4.1.2","worker_configured":false,...}
```

---

## 📚 完整 API 文档

### 基础 URL
```
https://celebrated-flexibility-production-2269.up.railway.app
```

### 交互式文档
- **Swagger UI**: https://celebrated-flexibility-production-2269.up.railway.app/docs
- **ReDoc**: https://celebrated-flexibility-production-2269.up.railway.app/redoc

---

## 🔧 核心 API 接口

### 1️⃣ 系统接口

#### 健康检查
```http
GET /api/health
```
**响应**:
```json
{
  "status": "ok",
  "timestamp": "2026-08-28T10:15:49.312465",
  "version": "V4.1.2",
  "environment": "Demo"
}
```

#### 系统状态
```http
GET /api/status
```
**响应**:
```json
{
  "api_version": "V4.1.2",
  "update_time": "2025/03/16",
  "environment": "Demo",
  "worker_configured": false,
  "worker_url": "Not configured",
  "download_enabled": true,
  "web_enabled": true
}
```

---

### 2️⃣ 混合解析接口（推荐）

#### 解析视频（支持抖音/TikTok/Bilibili）
```http
GET /api/hybrid/video_data?url={video_url}&minimal=false
```

**示例**:
```bash
# 设置密钥
export API_KEY="ak-your-key-here"

# 解析抖音视频
curl -H "X-API-Key: $API_KEY" "https://celebrated-flexibility-production-2269.up.railway.app/api/hybrid/video_data?url=https://v.douyin.com/iFhnojQT/"

# 解析 TikTok 视频
curl -H "X-API-Key: $API_KEY" "https://celebrated-flexibility-production-2269.up.railway.app/api/hybrid/video_data?url=https://vm.tiktok.com/xxx/"

# 解析 Bilibili 视频
curl -H "X-API-Key: $API_KEY" "https://celebrated-flexibility-production-2269.up.railway.app/api/hybrid/video_data?url=https://www.bilibili.com/video/BVxxx/"
```

---

### 3️⃣ 抖音接口

#### 获取单个视频
```http
GET /api/douyin/web/fetch_one_video?aweme_id={video_id}
```

#### 获取用户作品
```http
GET /api/douyin/web/fetch_user_post_videos?sec_user_id={user_id}&max_cursor=0&count=20
```

#### 获取用户信息
```http
GET /api/douyin/web/fetch_user_info?sec_user_id={user_id}
```

#### 获取直播流
```http
GET /api/douyin/web/fetch_user_live_videos?web_rid={room_id}
```

---

### 4️⃣ TikTok 接口

#### 获取单个视频
```http
GET /api/tiktok/web/fetch_one_video?aweme_id={video_id}
```

#### 获取用户作品
```http
GET /api/tiktok/web/fetch_user_post_videos?sec_user_id={user_id}&max_cursor=0&count=20
```

#### 获取用户信息
```http
GET /api/tiktok/web/fetch_user_info?sec_user_id={user_id}
```

---

### 5️⃣ Bilibili 接口

#### 获取视频详情
```http
GET /api/bilibili/web/fetch_video_info?bvid={bv_id}
```

#### 获取视频流
```http
GET /api/bilibili/web/fetch_video_stream?bvid={bv_id}&cid={cid}
```

#### 获取用户作品
```http
GET /api/bilibili/web/fetch_user_post_videos?mid={user_id}&pn=1&ps=20
```

---

### 6️⃣ 下载接口

#### 无水印下载
```http
GET /api/download?url={video_url}&prefix=true&with_watermark=false
```

**示例**:
```bash
# 设置密钥
export API_KEY="ak-your-key-here"

# 下载抖音视频
curl -H "X-API-Key: $API_KEY" -o video.mp4 "https://celebrated-flexibility-production-2269.up.railway.app/api/download?url=https://v.douyin.com/xxx"

# 下载 TikTok 视频
curl -H "X-API-Key: $API_KEY" -o video.mp4 "https://celebrated-flexibility-production-2269.up.railway.app/api/download?url=https://vm.tiktok.com/xxx"
```

---

### 7️⃣ iOS 快捷指令

#### 获取快捷指令信息
```http
GET /api/ios/shortcut_info
```

---

### 8️⃣ Cookie 管理接口

#### 获取 Cookie 配置
```http
GET /api/config/cookies
```
**当前状态**: ⚠️ 需要配置 Worker（见下方配置步骤）

#### 更新 Cookie
```http
POST /api/config/cookies/update?platform={platform}
Authorization: Bearer {your_secret}
Content-Type: text/plain

{cookie_content}
```

---

## ⚙️ 下一步：配置 Cloudflare Worker

### 为什么需要 Worker？

Worker 用于：
1. **存储 Cookie**（KV 存储，免费）
2. **保活服务**（Cron 每 10 分钟 ping）
3. **Cookie 管理**（统一管理接口）

### Worker 部署步骤

#### 步骤 1: 创建 KV Namespace

```bash
cd D:\cloudflareworker\want_to_study_api\Douyin_TikTok_Download_API
wrangler kv:namespace create COOKIES
```

输出示例：
```
{ binding = "COOKIES", id = "abc123def456..." }
```

#### 步骤 2: 更新 wrangler.toml

编辑 `wrangler.toml`，替换 KV ID：
```toml
[[kv_namespaces]]
binding = "COOKIES"
id = "你的KV_ID"  # ← 替换这里
```

#### 步骤 3: 设置 Secrets

```bash
# 设置更新密钥（自己创建一个强密码）
wrangler secret put UPDATE_SECRET
# 输入: your-strong-secret-key-123

# 设置 Railway URL
wrangler secret put RENDER_URL
# 输入: https://celebrated-flexibility-production-2269.up.railway.app
```

#### 步骤 4: 部署 Worker

```bash
wrangler deploy
```

成功后会显示 Worker URL，例如：
```
https://douyin-api-manager.你的子域.workers.dev
```

#### 步骤 5: 更新 Railway 环境变量

```bash
# 方法 1: CLI
cd D:\cloudflareworker\want_to_study_api\Douyin_TikTok_Download_API
railway variables set WORKER_COOKIE_URL=https://你的worker.workers.dev --service celebrated-flexibility
railway variables set UPDATE_SECRET=your-strong-secret-key-123 --service celebrated-flexibility

# 方法 2: Dashboard
# 访问 https://railway.com/project/fa8c12cd-feba-4287-99ff-5b9698f45be2
# Variables 标签 → 添加变量
```

---

## 🍪 配置 Cookie

### 步骤 1: 获取 Cookie

#### 抖音 Cookie
1. 浏览器访问 https://www.douyin.com/
2. 登录你的账号
3. F12 开发者工具 → Network 标签
4. 刷新页面，选择任意请求
5. Headers → Request Headers → 复制 Cookie 值

#### TikTok Cookie
同样方式从 https://www.tiktok.com/ 获取

#### Bilibili Cookie
同样方式从 https://www.bilibili.com/ 获取

### 步骤 2: 上传 Cookie 到 Worker

```bash
# 抖音
curl -X POST "https://你的worker.workers.dev/cookie/douyin" \
  -H "Authorization: Bearer your-strong-secret-key-123" \
  -H "Content-Type: text/plain" \
  --data "你复制的抖音Cookie"

# TikTok
curl -X POST "https://你的worker.workers.dev/cookie/tiktok" \
  -H "Authorization: Bearer your-strong-secret-key-123" \
  -H "Content-Type: text/plain" \
  --data "你复制的TikTok Cookie"

# Bilibili
curl -X POST "https://你的worker.workers.dev/cookie/bilibili" \
  -H "Authorization: Bearer your-strong-secret-key-123" \
  -H "Content-Type: text/plain" \
  --data "你复制的Bilibili Cookie"
```

### 步骤 3: 验证配置

```bash
# 检查 Railway 能否获取 Cookie
curl https://celebrated-flexibility-production-2269.up.railway.app/api/config/cookies

# 预期响应（配置成功后）：
# {
#   "douyin_cookie": "your_cookie...",
#   "tiktok_cookie": "your_cookie...",
#   "bilibili_cookie": "your_cookie..."
# }
```

---

## 📊 完整架构图

```
┌───────────────────────────────────────────────┐
│          用户 / User                          │
│                                               │
│  • 发送视频链接                               │
│  • 下载无水印视频                             │
└───────────────┬───────────────────────────────┘
                │
                ↓
┌───────────────────────────────────────────────┐
│   Railway FastAPI Service (已部署 ✅)         │
│   https://celebrated-flexibility...           │
│                                               │
│   功能：                                      │
│   • 视频解析 API                              │
│   • 无水印下载                                │
│   • 用户信息查询                              │
│   • 从 Worker 读取 Cookie                     │
│                                               │
│   配置：                                      │
│   • 0.5 vCPU, 512 MB RAM                     │
│   • 无数据库（省钱）                          │
│   • 成本: ~$1/月                             │
└───────────────┬───────────────────────────────┘
                │ HTTP
                ↓
┌───────────────────────────────────────────────┐
│   Cloudflare Worker (待部署 ⏳)               │
│   https://你的worker.workers.dev              │
│                                               │
│   功能：                                      │
│   • Cookie 存储 (KV)                         │
│   • Cron 保活 (每 10 分钟 ping Railway)      │
│   • Cookie 管理 API                          │
│                                               │
│   配置：                                      │
│   • 完全免费                                  │
│   • 成本: $0/月                              │
└───────────────────────────────────────────────┘
```

---

## 💰 成本分析

### Railway 费用
- **初始额度**: $5
- **每月赠送**: $1
- **预计使用**: 按需使用约 3-6 个月

### 最低配置建议
在 Railway Dashboard 设置：
- vCPU: 0.5（最低）
- Memory: 512 MB（最低）

### Cloudflare 费用
- Worker: 免费（10 万请求/天）
- KV: 免费（100K 读取/天，1K 写入/天）
- Cron: 免费

**总成本**: $1/月 ✅

---

## 🧪 完整测试脚本

```bash
# 设置基础 URL 和密钥
API_URL="https://celebrated-flexibility-production-2269.up.railway.app"
API_KEY="ak-your-key-here"  # 替换为你的实际密钥

# 1. 健康检查（无需密钥）
echo "=== 健康检查 ==="
curl -s "$API_URL/api/health" | jq
echo ""

# 2. 系统状态（需要密钥）
echo "=== 系统状态 ==="
curl -s -H "X-API-Key: $API_KEY" "$API_URL/api/status" | jq
echo ""

# 3. 解析抖音视频（需要有效链接和密钥）
echo "=== 解析抖音视频 ==="
curl -s -H "X-API-Key: $API_KEY" "$API_URL/api/hybrid/video_data?url=https://v.douyin.com/iFhnojQT/" | jq '.code, .message'
echo ""

# 4. Cookie 配置状态（需要密钥）
echo "=== Cookie 配置 ==="
curl -s -H "X-API-Key: $API_KEY" "$API_URL/api/config/cookies"
echo ""

# 5. 访问 API 文档（浏览器访问，密钥通过查询参数传递）
echo "=== API 文档 ==="
echo "Swagger UI: $API_URL/docs?key=$API_KEY"
echo "ReDoc: $API_URL/redoc?key=$API_KEY"
```

---

## 📋 快速命令参考

### Railway 管理

```bash
# 进入项目目录
cd D:\cloudflareworker\want_to_study_api\Douyin_TikTok_Download_API

# 查看状态
railway status

# 查看日志
railway logs --service celebrated-flexibility

# 查看实时日志
railway logs --service celebrated-flexibility -f

# 设置环境变量
railway variables set KEY=VALUE --service celebrated-flexibility

# 查看所有变量
railway variables --service celebrated-flexibility

# 重新部署
railway up --service celebrated-flexibility

# 查看用量
open https://railway.com/account/usage
```

### Worker 管理

```bash
# 部署 Worker
wrangler deploy

# 查看 Worker 日志
wrangler tail

# 测试 Worker 本地
wrangler dev

# 查看 KV 数据
wrangler kv:key list --namespace-id=你的KV_ID

# 获取 KV 值
wrangler kv:key get "douyin_cookie" --namespace-id=你的KV_ID
```

---

## 🔗 重要链接

### Railway
- **Dashboard**: https://railway.com/project/fa8c12cd-feba-4287-99ff-5b9698f45be2
- **服务 URL**: https://celebrated-flexibility-production-2269.up.railway.app
- **API 文档**: https://celebrated-flexibility-production-2269.up.railway.app/docs
- **用量监控**: https://railway.com/account/usage

### GitHub
- **你的仓库**: https://github.com/Huhu-scr/Douyin_TikTok_Download_API
- **原项目**: https://github.com/Evil0ctal/Douyin_TikTok_Download_API

### 本地文档
- `COMPLETE_API_DOCUMENTATION.md` - 完整 API 参考
- `RAILWAY_DEPLOYMENT_GUIDE.md` - Railway 部署指南
- `WORKER_DEPLOYMENT_GUIDE.md` - Worker 部署指南
- `DEPLOYMENT_COMPLETE.md` - 部署总结

---

## ✅ 完成检查清单

### Railway 部署
- [x] 项目创建成功
- [x] Dockerfile 优化完成
- [x] 端口配置修复
- [x] 健康检查路径修复
- [x] 服务成功运行
- [x] API 可正常访问
- [x] 健康检查通过
- [ ] 配置 Worker URL
- [ ] 配置 UPDATE_SECRET

### Worker 部署
- [ ] 创建 KV Namespace
- [ ] 更新 wrangler.toml
- [ ] 设置 UPDATE_SECRET
- [ ] 设置 RENDER_URL
- [ ] 部署 Worker
- [ ] 配置 Cron 保活
- [ ] 测试 Worker 接口

### Cookie 配置
- [ ] 获取抖音 Cookie
- [ ] 获取 TikTok Cookie
- [ ] 获取 Bilibili Cookie
- [ ] 上传 Cookie 到 Worker
- [ ] 验证 Railway 可获取

### 最终测试
- [ ] 测试保活功能
- [ ] 测试视频解析
- [ ] 测试下载功能
- [ ] 验证完整流程

---

## 🎓 使用建议

### 1. Cookie 有效期管理
- Cookie 通常 30-90 天过期
- 定期检查并更新
- 设置提醒

### 2. 监控资源使用
- 每周检查 Railway 用量
- 余额低于 $1 时充值
- 优化不必要的请求

### 3. 保活策略
- Worker Cron 每 10 分钟 ping
- 防止 Railway 休眠
- 确保即时响应

### 4. 安全建议
- UPDATE_SECRET 使用强密码
- 不要在代码中硬编码密钥
- 定期更换密码

---

## 🆘 常见问题

### Q: API 返回 Cookie 错误怎么办？
**A**: Cookie 可能已过期，重新获取并上传。

### Q: Railway 额度用完了怎么办？
**A**: 访问 https://railway.com/account/billing 充值，最低 $5。

### Q: Worker 部署失败怎么办？
**A**: 检查 wrangler.toml 配置，确保 KV ID 正确。

### Q: 视频解析失败怎么办？
**A**: 
1. 检查视频链接是否有效
2. 确认 Cookie 已配置
3. 查看 Railway 日志

### Q: 如何降低成本？
**A**:
1. 使用最低配置（0.5 vCPU, 512 MB RAM）
2. 所有数据存 Worker KV
3. 避免不必要的请求

---

## 🎉 恭喜！

你已经成功部署了一个完整的抖音/TikTok/Bilibili 视频解析 API 服务！

**下一步**：
1. 部署 Cloudflare Worker
2. 上传 Cookie
3. 开始使用 API

**需要帮助？**
- 查看详细文档
- 访问 GitHub Issues
- 或者直接问我！

---

**部署完成时间**: 2026-08-28  
**文档版本**: 1.0.0  
**状态**: ✅ Railway 部署成功，Worker 待部署
