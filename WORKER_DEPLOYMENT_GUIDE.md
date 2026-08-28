# Cloudflare Worker 部署指南

## 📋 概述

这个 Worker 提供以下功能：
1. **保活任务**: 每 10 分钟 ping Render 服务，防止休眠
2. **Cookie 存储**: 使用 KV 存储抖音、TikTok、Bilibili 的 Cookie
3. **Cookie API**: 提供 Cookie 的读取和更新接口

---

## 🚀 部署步骤

### 前提条件

1. **Cloudflare 账号**: https://dash.cloudflare.com/
2. **Wrangler CLI**: Cloudflare 的命令行工具

---

### 步骤 1: 安装 Wrangler CLI

```bash
# 使用 npm 安装
npm install -g wrangler

# 验证安装
wrangler --version
```

---

### 步骤 2: 登录 Cloudflare

```bash
wrangler login
```

这会打开浏览器，登录你的 Cloudflare 账号并授权。

---

### 步骤 3: 创建 KV Namespace

```bash
# 创建 KV namespace（用于存储 Cookie）
wrangler kv:namespace create COOKIES

# 会输出类似这样的内容：
# 🌀 Creating namespace with title "douyin-api-manager-COOKIES"
# ✨ Success!
# Add the following to your configuration file in your kv_namespaces array:
# { binding = "COOKIES", id = "abc123def456..." }
```

**记下输出的 ID**，更新 `wrangler.toml` 文件：

```toml
[[kv_namespaces]]
binding = "COOKIES"
id = "abc123def456..."  # 替换为你的 KV namespace ID
```

---

### 步骤 4: 设置环境变量（Secrets）

```bash
# 设置更新密钥（用于保护 Cookie 更新接口）
wrangler secret put UPDATE_SECRET
# 输入: 一个强密码，例如: MySecretKey123!@#

# 设置 Render 服务 URL（用于保活 ping）
wrangler secret put RENDER_URL
# 输入: https://your-app.onrender.com
```

**注意**: 
- `UPDATE_SECRET`: 用于认证 Cookie 更新请求
- `RENDER_URL`: 你的 Render 服务地址（部署后获得）

---

### 步骤 5: 部署 Worker

```bash
# 部署到 Cloudflare
wrangler deploy
```

**输出示例**:
```
⛅️ wrangler 3.x.x
-------------------
Uploaded douyin-api-manager (x.xx sec)
Published douyin-api-manager (x.xx sec)
  https://douyin-api-manager.your-subdomain.workers.dev
Current Deployment ID: abc-123-def
```

**记下你的 Worker URL**: `https://douyin-api-manager.your-subdomain.workers.dev`

---

## ✅ 验证部署

### 1. 测试健康检查

```bash
curl https://douyin-api-manager.your-subdomain.workers.dev/health
```

**预期响应**:
```json
{
  "status": "ok",
  "timestamp": "2026-08-28T...",
  "worker": "douyin-api-manager"
}
```

### 2. 测试状态接口

```bash
curl https://douyin-api-manager.your-subdomain.workers.dev/status
```

**预期响应**:
```json
{
  "worker": "douyin-api-manager",
  "version": "1.0.0",
  "render_url": "https://your-app.onrender.com",
  "last_keepalive": "never",
  "kv_configured": true,
  "timestamp": "2026-08-28T..."
}
```

### 3. 测试配置接口

```bash
curl https://douyin-api-manager.your-subdomain.workers.dev/config
```

**预期响应** (首次为空):
```json
{
  "douyin_cookie": "",
  "tiktok_cookie": "",
  "bilibili_cookie": "",
  "metadata": {
    "douyin_updated_at": "never",
    "tiktok_updated_at": "never",
    "bilibili_updated_at": "never"
  }
}
```

---

## 🔧 初始化 Cookie

### 获取 Cookie

#### 抖音 Cookie:
1. 打开浏览器访问 https://www.douyin.com/
2. 登录你的账号
3. 打开开发者工具（F12）
4. 切换到 Network 标签
5. 刷新页面，选择任意请求
6. 在 Headers 中找到 `Cookie`，复制完整内容

#### TikTok Cookie:
1. 打开浏览器访问 https://www.tiktok.com/
2. 登录你的账号
3. 同样方式获取 Cookie

#### Bilibili Cookie:
1. 打开浏览器访问 https://www.bilibili.com/
2. 登录你的账号
3. 同样方式获取 Cookie

---

### 上传 Cookie 到 Worker

```bash
# 上传抖音 Cookie
curl -X POST https://douyin-api-manager.your-subdomain.workers.dev/cookie/douyin \
  -H "Authorization: Bearer MySecretKey123!@#" \
  -H "Content-Type: text/plain" \
  --data "你的抖音Cookie内容"

# 上传 TikTok Cookie
curl -X POST https://douyin-api-manager.your-subdomain.workers.dev/cookie/tiktok \
  -H "Authorization: Bearer MySecretKey123!@#" \
  -H "Content-Type: text/plain" \
  --data "你的TikTok Cookie内容"

# 上传 Bilibili Cookie
curl -X POST https://douyin-api-manager.your-subdomain.workers.dev/cookie/bilibili \
  -H "Authorization: Bearer MySecretKey123!@#" \
  -H "Content-Type: text/plain" \
  --data "你的Bilibili Cookie内容"
```

**成功响应**:
```json
{
  "status": "success",
  "message": "douyin cookie updated",
  "timestamp": "2026-08-28T..."
}
```

---

### 验证 Cookie 已保存

```bash
curl https://douyin-api-manager.your-subdomain.workers.dev/config
```

现在应该能看到 Cookie 内容了。

---

## 🔄 更新 Render 环境变量

现在 Worker 已部署，需要更新 Render 服务的环境变量：

### 方法 1: 通过 Render Dashboard

1. 登录 https://dashboard.render.com/
2. 选择你的服务 `douyin-tiktok-api`
3. 进入 **Environment** 标签
4. 更新 `WORKER_COOKIE_URL`:
   ```
   https://douyin-api-manager.your-subdomain.workers.dev
   ```
5. 点击 **Save Changes**
6. 服务会自动重新部署

### 方法 2: 通过 Render CLI

```bash
# 如果支持 CLI 更新环境变量
render env set WORKER_COOKIE_URL="https://douyin-api-manager.your-subdomain.workers.dev" \
  --service douyin-tiktok-api
```

---

## 🔍 监控和管理

### 查看 Worker 日志

```bash
# 实时查看日志
wrangler tail
```

### 查看 KV 内容

```bash
# 列出所有 key
wrangler kv:key list --namespace-id=YOUR_KV_NAMESPACE_ID

# 获取特定 key 的值
wrangler kv:key get "douyin_cookie" --namespace-id=YOUR_KV_NAMESPACE_ID
```

### 查看 Cron 触发历史

登录 Cloudflare Dashboard:
1. 进入 Workers & Pages
2. 选择你的 Worker
3. 查看 **Triggers** 标签
4. 查看 **Cron Triggers** 执行历史

---

## 🧪 测试保活功能

### 手动触发保活

虽然 Cron 会自动运行，但你可以测试：

1. 等待 Render 服务完全启动（约 2-3 分钟）
2. 查看 Worker 日志：
   ```bash
   wrangler tail
   ```
3. 等待下一个 10 分钟的整数倍（如 15:00, 15:10, 15:20）
4. 在日志中应该能看到保活 ping 的输出

### 验证 Render 没有休眠

1. 15 分钟内不访问 Render 服务
2. 之后访问 Render 服务应该**立即响应**（无冷启动）
3. 如果响应很快（<2秒），说明保活成功

---

## 📊 性能和配额

### Cloudflare Workers 免费计划

- **请求数**: 100,000 请求/天
- **CPU 时间**: 10ms/请求
- **KV 读取**: 100,000 次/天
- **KV 写入**: 1,000 次/天
- **KV 存储**: 1 GB

### 本项目预估使用量

- **Cron 触发**: 144 次/天（每 10 分钟）
- **KV 读取**: ~200-500 次/天
- **KV 写入**: ~3-10 次/天（Cookie 更新）
- **外部请求**: 0（Render 不调用 Worker，只有 Worker 调用 Render）

**结论**: 完全在免费额度内 ✅

---

## 🔧 故障排查

### 问题 1: Worker 部署失败

**检查**:
```bash
wrangler deploy --dry-run
```

**常见原因**:
- `wrangler.toml` 配置错误
- KV namespace ID 未设置
- 语法错误

### 问题 2: KV 读写失败

**检查 KV namespace**:
```bash
wrangler kv:namespace list
```

**验证绑定**:
- 确认 `wrangler.toml` 中的 binding 名称为 `COOKIES`
- 确认 namespace ID 正确

### 问题 3: Cron 没有触发

**检查 Cron 配置**:
1. 登录 Cloudflare Dashboard
2. Workers & Pages → 选择 Worker
3. Triggers → Cron Triggers
4. 查看 "Upcoming" 和 "Past Invocations"

**验证**:
- Cron 表达式: `*/10 * * * *`
- 时区: UTC

### 问题 4: 保活失败

**检查 RENDER_URL**:
```bash
# 查看当前 secrets
wrangler secret list

# 如果需要重新设置
wrangler secret put RENDER_URL
```

**验证**:
- URL 格式正确（https://）
- Render 服务已启动
- `/health` 端点可访问

---

## 🔄 更新 Worker

### 修改代码后重新部署

```bash
# 编辑 worker.js
# 然后重新部署
wrangler deploy
```

### 回滚到之前版本

```bash
# 查看部署历史
wrangler deployments list

# 回滚到特定版本
wrangler rollback [deployment-id]
```

---

## 🔐 安全建议

1. **保护 UPDATE_SECRET**:
   - 使用强密码
   - 不要提交到 Git
   - 定期更换

2. **Cookie 安全**:
   - 不要分享你的 Cookie
   - 定期更新 Cookie
   - 监控异常访问

3. **访问控制**:
   - Cookie 更新接口需要认证
   - 考虑添加 IP 白名单（可选）

---

## 📝 下一步

1. ✅ Worker 已部署
2. ✅ Cookie 已初始化
3. ✅ Cron 保活已配置
4. ⏳ 等待 Render 服务部署完成
5. ⏳ 更新 Render 环境变量
6. ⏳ 测试完整流程

---

## 🔗 相关链接

- **Cloudflare Dashboard**: https://dash.cloudflare.com/
- **Workers 文档**: https://developers.cloudflare.com/workers/
- **KV 文档**: https://developers.cloudflare.com/kv/
- **Wrangler 文档**: https://developers.cloudflare.com/workers/wrangler/

---

生成时间: 2026-08-28
