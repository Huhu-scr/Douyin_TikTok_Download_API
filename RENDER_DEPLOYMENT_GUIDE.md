# Render 部署指南

## 📋 部署步骤

### 前提条件
- ✅ GitHub 账号已有 fork: https://github.com/Huhu-scr/Douyin_TikTok_Download_API
- ✅ Render 账号: https://render.com
- ⚠️ **需要绑定支付信息**（即使使用免费计划）

---

## 🚀 通过 Render Dashboard 部署

### 步骤 1: 登录 Render

访问: https://dashboard.render.com/

### 步骤 2: 创建新服务

1. 点击 **"New +"** 按钮
2. 选择 **"Web Service"**

### 步骤 3: 连接 GitHub 仓库

1. 选择 **"Build and deploy from a Git repository"**
2. 点击 **"Connect GitHub"**（如果还未连接）
3. 找到并选择仓库: **Huhu-scr/Douyin_TikTok_Download_API**
4. 点击 **"Connect"**

### 步骤 4: 配置服务

填写以下信息：

#### 基本设置
- **Name**: `douyin-tiktok-api`（或你喜欢的名字）
- **Region**: `Oregon (US West)`（推荐，或选择其他区域）
- **Branch**: `main`
- **Runtime**: `Docker`

#### 实例类型
- **Instance Type**: `Free`

#### 环境变量（Environment Variables）

点击 **"Add Environment Variable"** 添加：

```
WORKER_COOKIE_URL = https://your-worker.workers.dev
UPDATE_SECRET = your-strong-secret-key-here
```

**注意**: 
- `WORKER_COOKIE_URL` 先留空或填占位符，等部署 Worker 后再更新
- `UPDATE_SECRET` 生成一个强密码，比如：`generateRandomString123!@#`

#### 高级设置（Advanced）

- **Health Check Path**: `/health`
- **Auto-Deploy**: `Yes`（推荐）

### 步骤 5: 创建服务

点击 **"Create Web Service"** 按钮

---

## ⏳ 部署过程

### 1. 构建阶段
- Render 会自动检测 Dockerfile
- 构建 Docker 镜像（大约 5-10 分钟）
- 显示构建日志

### 2. 部署阶段
- 启动容器
- 运行健康检查
- 分配 URL

### 3. 完成

部署成功后，你会得到一个 URL：
```
https://douyin-tiktok-api.onrender.com
```

---

## ✅ 验证部署

### 测试健康检查

```bash
curl https://your-app.onrender.com/health
```

**预期响应**:
```json
{
  "status": "ok",
  "timestamp": "2026-08-28T...",
  "version": "V4.1.2",
  "environment": "Demo"
}
```

### 测试系统状态

```bash
curl https://your-app.onrender.com/status
```

### 访问 API 文档

打开浏览器访问：
```
https://your-app.onrender.com/docs
```

---

## 🔧 部署后配置

### 1. 更新环境变量

等 Cloudflare Worker 部署完成后：

1. 进入 Render Dashboard
2. 选择你的服务
3. 进入 **"Environment"** 标签
4. 更新 `WORKER_COOKIE_URL` 为实际的 Worker URL
5. 点击 **"Save Changes"**
6. 服务会自动重新部署

### 2. 设置自定义域名（可选）

1. 进入 **"Settings"** 标签
2. 找到 **"Custom Domain"** 部分
3. 添加你的域名
4. 按照提示配置 DNS

---

## 📊 监控和管理

### 查看日志

1. 进入 Render Dashboard
2. 选择你的服务
3. 点击 **"Logs"** 标签
4. 查看实时日志

### 手动部署

1. 进入 **"Manual Deploy"** 
2. 选择分支
3. 点击 **"Deploy"**

### 重启服务

在服务页面点击 **"Manual Deploy"** → **"Clear build cache & deploy**

---

## ⚠️ 常见问题

### 1. 服务一直显示 "Deploying"

**原因**: 构建时间较长或网络问题

**解决**:
- 查看构建日志
- 等待 10-15 分钟
- 如果超过 30 分钟，可能需要重新部署

### 2. 健康检查失败

**原因**: 
- `/health` 端点不可访问
- 应用启动失败

**解决**:
- 检查日志中的错误信息
- 确认 `start.sh` 有执行权限
- 验证 Docker 镜像构建成功

### 3. Cookie 相关错误

**原因**: 
- `WORKER_COOKIE_URL` 未配置
- Worker 尚未部署
- Cookie 已过期

**解决**:
- 启动时的 Cookie 加载失败不会阻止服务启动
- 日志中会显示警告但服务继续运行
- 部署 Worker 后服务会正常获取 Cookie

### 4. 服务自动休眠

**原因**: Render 免费版 15 分钟无活动会休眠

**解决**:
- 部署 Cloudflare Worker 保活脚本
- Worker 每 10 分钟 ping `/health` 接口
- 可有效防止休眠

---

## 📝 下一步

1. ✅ 服务已部署到 Render
2. ⏳ 接下来部署 Cloudflare Worker
3. ⏳ 配置 Worker KV 存储 Cookie
4. ⏳ 设置 Worker Cron 保活任务

---

## 🔗 相关链接

- **Render Dashboard**: https://dashboard.render.com/
- **你的 GitHub Repo**: https://github.com/Huhu-scr/Douyin_TikTok_Download_API
- **API 文档**: 查看 API_DOCUMENTATION.md
- **Render 文档**: https://render.com/docs

---

## 💡 提示

1. **免费计划限制**:
   - 750 小时/月（单个服务可运行全月）
   - 512 MB RAM
   - 0.1 vCPU
   - 自动休眠（15 分钟无活动）

2. **建议**:
   - 使用 Worker 保活可避免大部分休眠
   - 定期检查服务状态
   - 监控日志查看问题

3. **成本**:
   - 完全免费（Render Free + Cloudflare Free）
   - 无需信用卡用于计费
   - 绑定信用卡仅为验证身份

---

生成时间: 2026-08-28
