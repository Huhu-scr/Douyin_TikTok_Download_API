# Railway 部署指南（省钱优化版）

## 🎯 部署概述

- **项目名称**: celebrated-flexibility
- **项目 ID**: fa8c12cd-feba-4287-99ff-5b9698f45be2
- **区域**: us-west1
- **配置**: 最低资源使用

---

## 💰 省钱策略

### 1. 使用最小资源配置
- ✅ 单实例运行
- ✅ 使用 Dockerfile（不额外安装依赖）
- ✅ 健康检查防止过度重启

### 2. 所有数据存储在 Cloudflare Worker
- ✅ Cookie 存储在 Worker KV（免费）
- ✅ 不使用 Railway 的数据库
- ✅ 不使用 Railway 的持久化存储

### 3. Railway 免费额度
- **$5 初始额度** + **$1/月**
- 预计可用 **3-6 个月**

---

## 🔧 配置环境变量

部署完成后，设置以下环境变量：

```bash
# 方法 1: 通过 CLI
railway variables set WORKER_COOKIE_URL=https://your-worker.workers.dev
railway variables set UPDATE_SECRET=your-secret-key-here

# 方法 2: 通过 Dashboard
# 访问 https://railway.com/project/fa8c12cd-feba-4287-99ff-5b9698f45be2
# 进入 Variables 标签，添加变量
```

**必需的环境变量**:

| 变量名 | 值 | 说明 |
|--------|-----|------|
| `WORKER_COOKIE_URL` | `https://your-worker.workers.dev` | Worker URL |
| `UPDATE_SECRET` | `your-secret-key` | Cookie 更新密钥 |
| `PORT` | `8000` | 端口（Railway 自动设置） |

---

## 🚀 部署命令

```bash
# 查看状态
railway status

# 查看日志
railway logs

# 查看构建日志
railway logs --build

# 重新部署
railway up

# 配置变量
railway variables set KEY=VALUE

# 查看变量
railway variables

# 获取服务 URL
railway domain
```

---

## 📊 监控资源使用

### 查看当前用量

```bash
# 通过 Dashboard 查看
# https://railway.com/account/usage
```

### 预估费用

**Railway 计费**:
- CPU: $0.000463/vCPU-min
- RAM: $0.000231/GB-min

**最低配置预估**（0.5 vCPU, 512 MB RAM）:
- 每小时: ~$0.02
- 每天: ~$0.48
- $5 可用约 **10 天持续运行**
- $6 可用约 **12 天**

**优化后（按需使用，非高峰期）**:
- $5 + $1/月 可用 **3-6 个月**

---

## 🔒 资源限制设置

Railway 会自动设置合理的资源限制，但你可以手动调整：

### 通过 Dashboard 设置

1. 访问项目: https://railway.com/project/fa8c12cd-feba-4287-99ff-5b9698f45be2
2. 选择服务
3. 进入 **Settings** 标签
4. 调整 **Resources**:
   - vCPU: **0.5** (最低)
   - Memory: **512 MB** (最低)

---

## 📝 架构设计（省钱版）

```
┌──────────────────────────────────────────┐
│   Cloudflare Worker (免费)               │
│                                           │
│   功能：                                  │
│   • Cookie 存储 (KV)                    │
│   • 保活 Cron (每 10 分钟)               │
│   • Cookie 管理 API                     │
│                                           │
│   成本: $0                               │
└──────────────────────────────────────────┘
                ↕️ HTTP
┌──────────────────────────────────────────┐
│   Railway Service ($5 + $1/月)          │
│                                           │
│   功能：                                  │
│   • FastAPI 服务                         │
│   • 视频解析 API                         │
│   • 从 Worker 读取 Cookie                │
│                                           │
│   配置：                                  │
│   • 0.5 vCPU (最低)                     │
│   • 512 MB RAM (最低)                   │
│   • 无数据库                             │
│   • 无持久化存储                         │
│                                           │
│   成本: ~$0.48/天 (持续运行)            │
│        或 ~$1/月 (按需使用)             │
└──────────────────────────────────────────┘
```

---

## ✅ 部署检查清单

### Railway 部署
- [x] 项目已创建
- [ ] 构建完成
- [ ] 服务运行中
- [ ] 配置环境变量
- [ ] 生成域名
- [ ] 测试 /health 接口

### Worker 部署
- [ ] 创建 KV Namespace
- [ ] 配置 wrangler.toml
- [ ] 设置 Secrets
- [ ] 部署 Worker
- [ ] 测试接口

### 集成测试
- [ ] 上传 Cookie 到 Worker
- [ ] 更新 Railway 环境变量
- [ ] 测试视频解析
- [ ] 验证保活功能

---

## 🔍 故障排查

### 构建失败

```bash
# 查看构建日志
railway logs --build
```

常见问题：
- Dockerfile 语法错误
- 依赖安装失败
- 内存不足

### 运行时错误

```bash
# 查看运行日志
railway logs
```

常见问题：
- 环境变量未设置
- Worker URL 无法访问
- 端口配置错误

### 服务无法访问

```bash
# 检查服务状态
railway status

# 生成公共域名
railway domain
```

---

## 🌐 获取服务 URL

```bash
# 生成域名
railway domain

# 输出类似：
# https://celebrated-flexibility-production.up.railway.app
```

---

## 💡 省钱技巧

### 1. 优化 Dockerfile

当前 Dockerfile 已经比较优化：
- ✅ 使用轻量级基础镜像
- ✅ 使用镜像源加速
- ✅ 清理缓存

### 2. 按需使用

- 不需要 24/7 运行
- 使用 Worker 保活机制
- 低流量时自动休眠

### 3. 监控使用量

定期检查：
```
https://railway.com/account/usage
```

当余额低于 $1 时，及时充值或暂停服务。

### 4. 不使用额外服务

- ❌ 不添加数据库
- ❌ 不使用持久化卷
- ❌ 不开启多副本
- ✅ 只运行单个服务

---

## 📚 相关文档

- **Railway Dashboard**: https://railway.com/project/fa8c12cd-feba-4287-99ff-5b9698f45be2
- **Worker 部署指南**: WORKER_DEPLOYMENT_GUIDE.md
- **API 文档**: API_DOCUMENTATION.md

---

生成时间: 2026-08-28
