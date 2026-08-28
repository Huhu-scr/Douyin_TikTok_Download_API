// ==============================================================================
// Cloudflare Worker for Douyin_TikTok_Download_API
// Functions:
// 1. Keep-alive Cron (ping Render every 10 minutes)
// 2. Cookie storage in KV
// 3. Cookie management API
// ==============================================================================

export default {
  // ========== HTTP 请求处理 ==========
  async fetch(request, env) {
    const url = new URL(request.url)
    const path = url.pathname

    // CORS 头
    const corsHeaders = {
      'Access-Control-Allow-Origin': '*',
      'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
      'Access-Control-Allow-Headers': 'Content-Type, Authorization',
    }

    // 处理 OPTIONS 请求
    if (request.method === 'OPTIONS') {
      return new Response(null, { headers: corsHeaders })
    }

    // ========== 健康检查 ==========
    if (path === '/health') {
      return new Response(JSON.stringify({
        status: 'ok',
        timestamp: new Date().toISOString(),
        worker: 'douyin-api-manager'
      }), {
        headers: { ...corsHeaders, 'Content-Type': 'application/json' }
      })
    }

    // ========== 获取单个 Cookie ==========
    // GET /cookie/:platform
    const getCookieMatch = path.match(/^\/cookie\/(douyin|tiktok|bilibili)$/)
    if (getCookieMatch && request.method === 'GET') {
      const platform = getCookieMatch[1]
      const cookie = await env.COOKIES.get(`${platform}_cookie`)

      return new Response(cookie || '', {
        headers: { ...corsHeaders, 'Content-Type': 'text/plain' }
      })
    }

    // ========== 更新单个 Cookie ==========
    // POST /cookie/:platform
    if (getCookieMatch && request.method === 'POST') {
      const platform = getCookieMatch[1]

      // 简单认证
      const authHeader = request.headers.get('Authorization')
      const SECRET = env.UPDATE_SECRET || 'change-me-in-production'

      if (authHeader !== `Bearer ${SECRET}`) {
        return new Response('Unauthorized', {
          status: 401,
          headers: corsHeaders
        })
      }

      const cookie = await request.text()
      await env.COOKIES.put(`${platform}_cookie`, cookie)

      // 记录更新时间
      await env.COOKIES.put(
        `${platform}_cookie_updated_at`,
        new Date().toISOString()
      )

      return new Response(JSON.stringify({
        status: 'success',
        message: `${platform} cookie updated`,
        timestamp: new Date().toISOString()
      }), {
        headers: { ...corsHeaders, 'Content-Type': 'application/json' }
      })
    }

    // ========== 获取所有配置 ==========
    // GET /config
    if (path === '/config' && request.method === 'GET') {
      const douyin = await env.COOKIES.get('douyin_cookie')
      const tiktok = await env.COOKIES.get('tiktok_cookie')
      const bilibili = await env.COOKIES.get('bilibili_cookie')

      // 获取更新时间
      const douyinUpdated = await env.COOKIES.get('douyin_cookie_updated_at')
      const tiktokUpdated = await env.COOKIES.get('tiktok_cookie_updated_at')
      const bilibiliUpdated = await env.COOKIES.get('bilibili_cookie_updated_at')

      return new Response(JSON.stringify({
        douyin_cookie: douyin || '',
        tiktok_cookie: tiktok || '',
        bilibili_cookie: bilibili || '',
        metadata: {
          douyin_updated_at: douyinUpdated || 'never',
          tiktok_updated_at: tiktokUpdated || 'never',
          bilibili_updated_at: bilibiliUpdated || 'never'
        }
      }), {
        headers: { ...corsHeaders, 'Content-Type': 'application/json' }
      })
    }

    // ========== 获取状态信息 ==========
    // GET /status
    if (path === '/status' && request.method === 'GET') {
      const lastKeepalive = await env.COOKIES.get('last_keepalive')
      const renderUrl = env.RENDER_URL || 'Not configured'

      return new Response(JSON.stringify({
        worker: 'douyin-api-manager',
        version: '1.0.0',
        render_url: renderUrl,
        last_keepalive: lastKeepalive || 'never',
        kv_configured: !!env.COOKIES,
        timestamp: new Date().toISOString()
      }), {
        headers: { ...corsHeaders, 'Content-Type': 'application/json' }
      })
    }

    // ========== 默认响应 ==========
    return new Response(JSON.stringify({
      message: 'Douyin_TikTok_Download_API Worker',
      version: '1.0.0',
      endpoints: {
        health: 'GET /health',
        config: 'GET /config',
        status: 'GET /status',
        getCookie: 'GET /cookie/{platform}',
        updateCookie: 'POST /cookie/{platform}',
      },
      platforms: ['douyin', 'tiktok', 'bilibili']
    }), {
      headers: { ...corsHeaders, 'Content-Type': 'application/json' }
    })
  },

  // ========== 定时任务：保活 Render ==========
  async scheduled(event, env, ctx) {
    const renderUrl = env.RENDER_URL || ''

    if (!renderUrl) {
      console.log('⚠️  RENDER_URL not configured, skipping keepalive')
      return
    }

    console.log(`🔄 Starting keepalive ping to: ${renderUrl}`)

    try {
      const response = await fetch(`${renderUrl}/health`, {
        method: 'GET',
        headers: {
          'User-Agent': 'CF-Worker-KeepAlive/1.0',
          'X-Keepalive-Source': 'cloudflare-worker'
        }
      })

      const status = response.status
      console.log(`✅ Keepalive ping successful: HTTP ${status}`)

      // 记录最后一次保活时间
      await env.COOKIES.put('last_keepalive', new Date().toISOString())

      // 可选：记录响应内容（用于调试）
      if (status === 200) {
        const data = await response.json()
        console.log(`   Server version: ${data.version}`)
        console.log(`   Server status: ${data.status}`)
      }

    } catch (error) {
      console.error(`❌ Keepalive ping failed: ${error.message}`)

      // 记录失败
      const failures = parseInt(await env.COOKIES.get('keepalive_failures') || '0')
      await env.COOKIES.put('keepalive_failures', String(failures + 1))

      // 如果连续失败超过 3 次，可以发送告警（需要配置告警服务）
      if (failures >= 3) {
        console.error(`⚠️  Warning: ${failures} consecutive keepalive failures`)
      }
    }
  }
}
