# Zeabur 部署指南

## 📋 概述

Zeabur 是一个完全免费、无需信用卡的部署平台，支持 Docker 和 GitHub 自动部署。

**优势**：
- ✅ 完全免费，永久可用
- ✅ 无需信用卡或支付信息
- ✅ 支持 Docker 部署
- ✅ 中文友好界面
- ✅ 自动 HTTPS 证书

---

## 🚀 方式一：通过 Dashboard 部署（推荐新手）

### 步骤 1: 注册 Zeabur

1. 访问 https://zeabur.com/
2. 点击 **"Sign in with GitHub"**
3. 授权 GitHub 访问

### 步骤 2: 创建项目

1. 点击 **"Create Project"**
2. 输入项目名称：`douyin-tiktok-api`
3. 选择区域：`ap-east` (香港) 或 `us-west` (美国西部)

### 步骤 3: 添加服务

1. 点击 **"Add Service"**
2. 选择 **"Git"**
3. 连接你的 GitHub 仓库：`Huhu-scr/Douyin_TikTok_Download_API`
4. 选择分支：`main`

### 步骤 4: 配置服务

Zeabur 会自动检测 Dockerfile 并配置。

**添加环境变量**：
1. 点击服务卡片
2. 进入 **"Variables"** 标签
3. 添加以下变量：
   ```
   WORKER_COOKIE_URL = https://your-worker.workers.dev
   UPDATE_SECRET = your-secret-key-here
   ```

### 步骤 5: 部署

1. Zeabur 自动开始构建
2. 等待 5-10 分钟
3. 部署完成后会显示 URL

### 步骤 6: 绑定域名（可选）

1. 点击 **"Networking"** 标签
2. 点击 **"Generate Domain"** 生成免费域名
3. 或添加自定义域名

---

## 💻 方式二：通过 CLI 部署（推荐开发者）

### 步骤 1: 安装和登录

```bash
# 使用 npx（无需安装）
npx zeabur auth login

# 或全局安装
npm install -g zeabur
zeabur auth login
```

浏览器会自动打开，登录你的 Zeabur 账号。

### 步骤 2: 创建项目

```bash
# 交互式创建
npx zeabur project create

# 或非交互式
npx zeabur project create --name douyin-tiktok-api --region ap-east
```

### 步骤 3: 设置项目上下文

```bash
# 列出所有项目
npx zeabur project ls

# 设置当前项目（交互式选择）
npx zeabur context set project

# 或指定项目名称
npx zeabur context set project --name douyin-tiktok-api
```

### 步骤 4: 部署服务

```bash
# 在项目目录下运行
cd Douyin_TikTok_Download_API

# 部署（Zeabur 会自动检测 Dockerfile）
npx zeabur deploy
```

**部署过程**：
1. CLI 检测到 Dockerfile
2. 推送代码到 Zeabur
3. 自动构建 Docker 镜像
4. 部署并生成 URL

### 步骤 5: 配置环境变量

```bash
# 通过 Dashboard 添加环境变量更方便
# 或使用 CLI（如果支持）

# 访问 Dashboard 配置：
# https://dash.zeabur.com
```

### 步骤 6: 查看服务状态

```bash
# 列出服务
npx zeabur service ls

# 查看部署状态
npx zeabur deployment get

# 查看运行日志
npx zeabur deployment log -t=runtime

# 查看构建日志
npx zeabur deployment log -t=build
```

### 步骤 7: 重启服务

```bash
npx zeabur service restart
```

---

## 🔧 配置说明

### 环境变量

在 Zeabur Dashboard 中添加：

| 变量名 | 值 | 说明 |
|--------|-----|------|
| `WORKER_COOKIE_URL` | `https://your-worker.workers.dev` | Worker URL（先部署 Worker） |
| `UPDATE_SECRET` | `your-secret-key` | Cookie 更新密钥 |

### 域名

Zeabur 提供：
- ✅ 免费 `.zeabur.app` 子域名
- ✅ 自动 HTTPS 证书
- ✅ 支持自定义域名

---

## 📊 免费额度

Zeabur 免费计划：
- **CPU**: 0.25 vCPU（共享）
- **内存**: 256 MB
- **存储**: 1 GB
- **带宽**: 无限制
- **服务数量**: 无限制
- **构建时长**: 无限制

**对比 Render 免费版**：
- Zeabur: 256 MB RAM, 0.25 vCPU
- Render: 512 MB RAM, 0.1 vCPU

性能相近，但 Zeabur **无需信用卡**！

---

## ✅ 验证部署

### 测试健康检查

```bash
curl https://your-app.zeabur.app/health
```

**预期响应**：
```json
{
  "status": "ok",
  "timestamp": "2026-08-28T...",
  "version": "V4.1.2",
  "environment": "Demo"
}
```

### 访问 API 文档

```
https://your-app.zeabur.app/docs
```

### 测试视频解析

```bash
curl "https://your-app.zeabur.app/api/hybrid/video_data?url=https://v.douyin.com/xxx"
```

---

## 🔄 更新服务

### 自动部署

连接 GitHub 后，每次 push 代码到 `main` 分支，Zeabur 会自动重新部署。

### 手动触发

```bash
# CLI 触发重新部署
npx zeabur service restart

# 或在 Dashboard 中点击 "Redeploy"
```

---

## 📝 CLI 常用命令

### 项目管理

```bash
# 列出所有项目
npx zeabur project ls

# 创建项目
npx zeabur project create --name my-project

# 设置项目上下文
npx zeabur context set project
```

### 服务管理

```bash
# 列出服务
npx zeabur service ls

# 重启服务
npx zeabur service restart

# 查看服务详情
npx zeabur service get
```

### 部署管理

```bash
# 部署当前目录
npx zeabur deploy

# 查看部署状态
npx zeabur deployment get

# 查看日志
npx zeabur deployment log -t=runtime
npx zeabur deployment log -t=build
```

### 工作区管理

```bash
# 列出工作区
npx zeabur workspace list

# 切换工作区
npx zeabur workspace switch <team-name>

# 返回个人工作区
npx zeabur workspace clear
```

---

## 🔍 故障排查

### 问题 1: 构建失败

**查看构建日志**：
```bash
npx zeabur deployment log -t=build
```

**常见原因**：
- Dockerfile 语法错误
- 依赖安装失败
- 内存不足（256 MB 限制）

### 问题 2: 服务无法访问

**检查**：
1. 服务状态是否为 "Running"
2. 端口配置是否正确（应该监听 `0.0.0.0`）
3. 健康检查是否通过

**查看运行日志**：
```bash
npx zeabur deployment log -t=runtime
```

### 问题 3: 内存不足

Zeabur 免费版只有 256 MB RAM。

**优化方案**：
1. 精简依赖
2. 优化 Dockerfile
3. 减少内存占用

---

## 🆚 Zeabur vs Render

| 特性 | Zeabur | Render |
|------|--------|--------|
| **信用卡** | ❌ 不需要 | ⚠️ 必须绑定 |
| **RAM** | 256 MB | 512 MB |
| **CPU** | 0.25 vCPU | 0.1 vCPU |
| **休眠** | ❌ 不休眠 | ✅ 15分钟休眠 |
| **冷启动** | 快速 | 30-90秒 |
| **中文支持** | ✅ 完善 | ❌ 英文 |
| **部署速度** | 快 | 慢 |

**结论**：Zeabur 更适合无信用卡的免费部署！

---

## 🎯 完整部署流程

### 快速开始（5 分钟）

```bash
# 1. 登录
npx zeabur auth login

# 2. 进入项目目录
cd Douyin_TikTok_Download_API

# 3. 部署
npx zeabur deploy

# 4. 等待完成
# Zeabur 会显示你的服务 URL

# 5. 测试
curl https://your-app.zeabur.app/health
```

### 配置环境变量

1. 访问 https://dash.zeabur.com
2. 选择你的项目和服务
3. 进入 "Variables" 标签
4. 添加环境变量
5. 保存后自动重启

---

## 📚 相关资源

- **Zeabur 官网**: https://zeabur.com/
- **Zeabur Dashboard**: https://dash.zeabur.com/
- **Zeabur 文档**: https://zeabur.com/docs
- **Zeabur CLI GitHub**: https://github.com/zeabur/cli
- **Zeabur 模板市场**: https://zeabur.com/templates

---

## 💡 提示

1. **区域选择**：
   - 中国用户：`ap-east` (香港)
   - 其他地区：`us-west` (美国)

2. **性能优化**：
   - 使用轻量级基础镜像
   - 精简依赖
   - 启用多阶段构建

3. **监控**：
   - 定期查看日志
   - 监控资源使用
   - 及时更新 Cookie

---

生成时间: 2026-08-28
