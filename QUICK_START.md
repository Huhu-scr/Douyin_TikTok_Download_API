# 🎯 快速部署指南

本项目支持多种免费部署方式，选择适合你的平台：

## 📋 部署平台对比

| 平台 | 信用卡 | RAM | CPU | 休眠 | 推荐度 |
|------|--------|-----|-----|------|--------|
| **Zeabur** | ❌ 不需要 | 256 MB | 0.25 vCPU | ❌ 不休眠 | ⭐⭐⭐⭐⭐ |
| **Railway** | ❌ 不需要 | 自定义 | 自定义 | ❌ 不休眠 | ⭐⭐⭐⭐ |
| **Render** | ⚠️ 需要 | 512 MB | 0.1 vCPU | ✅ 15分钟 | ⭐⭐⭐ |
| **Cloudflare Workers** | ❌ 不需要 | - | - | ❌ 不休眠 | ⭐⭐ (仅保活) |

---

## 🚀 推荐方案

### 方案 A: Zeabur（最简单，无需信用卡）

**适合人群**: 所有用户，尤其是没有信用卡的用户

**特点**:
- ✅ 完全免费，永久可用
- ✅ 无需信用卡或支付信息
- ✅ 中文界面，操作简单
- ✅ 支持 Docker 和 GitHub 自动部署

**部署步骤**: 查看 [ZEABUR_DEPLOYMENT_GUIDE.md](./ZEABUR_DEPLOYMENT_GUIDE.md)

**快速开始**:
```bash
# 1. 登录
npx zeabur auth login

# 2. 部署
cd Douyin_TikTok_Download_API
npx zeabur deploy
```

---

### 方案 B: Railway + Worker（最佳性能）

**适合人群**: 需要更好性能的用户

**特点**:
- ✅ $5 免费额度（约 500 小时）
- ✅ 无需信用卡
- ✅ 更高配置（可自定义）
- ⚠️ 额度用完需充值

**部署步骤**: 
1. 注册 https://railway.app/
2. 连接 GitHub 仓库
3. 自动部署

---

### 方案 C: Render + Worker（需要信用卡）

**适合人群**: 有信用卡的用户

**特点**:
- ✅ 永久免费
- ⚠️ 需要绑定信用卡（不扣费）
- ⚠️ 会自动休眠（需 Worker 保活）

**部署步骤**: 查看 [RENDER_DEPLOYMENT_GUIDE.md](./RENDER_DEPLOYMENT_GUIDE.md)

---

## 🛠️ Cloudflare Worker（保活和 Cookie 管理）

**所有方案都建议配合 Worker 使用**:
- 保活功能（防止休眠）
- Cookie 集中管理
- 完全免费

**部署步骤**: 查看 [WORKER_DEPLOYMENT_GUIDE.md](./WORKER_DEPLOYMENT_GUIDE.md)

---

## 📚 完整文档

- **DEPLOYMENT_SUMMARY.md** - 部署总览和检查清单
- **API_DOCUMENTATION.md** - 完整 API 文档
- **ZEABUR_DEPLOYMENT_GUIDE.md** - Zeabur 部署详细步骤 ⭐推荐
- **RENDER_DEPLOYMENT_GUIDE.md** - Render 部署详细步骤
- **WORKER_DEPLOYMENT_GUIDE.md** - Worker 部署详细步骤

---

## 🎯 新增功能

本 Fork 版本添加了以下功能：

### 系统接口
- `GET /health` - 健康检查（保活）
- `GET /status` - 系统状态
- `GET /config/cookies` - 获取 Cookie 配置
- `POST /config/cookies/update` - 更新 Cookie

### Worker 集成
- 自动从 Worker KV 加载 Cookie
- 定时保活机制
- Cookie 集中管理

### 部署支持
- 支持 Zeabur、Railway、Render
- Docker 优化
- 详细部署文档

---

## 🚀 快速开始

### 1. Fork 本仓库

点击右上角 **Fork** 按钮

### 2. 选择部署平台

根据你的情况选择：
- 无信用卡 → **Zeabur**
- 追求性能 → **Railway**
- 有信用卡 → **Render**

### 3. 部署 Cloudflare Worker

所有平台都建议配置 Worker：
```bash
wrangler deploy
```

### 4. 测试

访问你的服务：
```
https://your-app.zeabur.app/docs
```

---

## 📊 架构图

```
┌──────────────────────────────────────────┐
│   Cloudflare Worker (免费)               │
│   • Cron: 每 10 分钟保活                │
│   • KV: Cookie 存储                     │
│   • API: Cookie 管理                    │
└──────────────────────────────────────────┘
                ↕️
┌──────────────────────────────────────────┐
│   Zeabur/Railway/Render (免费)           │
│   • FastAPI 服务                         │
│   • 抖音/TikTok/Bilibili 爬虫          │
│   • 完整 API                            │
└──────────────────────────────────────────┘
```

---

## 💡 注意事项

1. **Cookie 管理**: 需要定期更新 Cookie（建议每周）
2. **保活机制**: Worker 可防止服务休眠
3. **性能**: 免费版性能有限，适合个人使用
4. **成本**: 完全免费（无需信用卡）

---

## 🔗 原项目

本项目基于 [Evil0ctal/Douyin_TikTok_Download_API](https://github.com/Evil0ctal/Douyin_TikTok_Download_API) 并添加了部署支持和 Worker 集成。

---

## 📄 许可证

Apache-2.0 License

---

**最后更新**: 2026-08-28
**Fork 维护者**: Huhu-scr
