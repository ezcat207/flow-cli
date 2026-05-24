# 为什么 Flow CLI 和 NotebookLM CLI 实现方式不同

## TL;DR

**NotebookLM CLI**: 只需 cookies → 可以直接调用 API ✅
**Flow CLI**: 需要 Chrome Extension + OAuth token + reCAPTCHA → 更复杂 ⚠️

## 详细对比

### NotebookLM CLI 的实现

```
用户 → Playwright → Google 登录 → 获取 cookies → 直接调用 API
```

**认证方式**:
```python
# 1. 打开浏览器登录
browser = await playwright.chromium.launch()
page = await browser.new_page()
await page.goto('https://notebooklm.google.com')
# 等待用户登录

# 2. 获取 cookies
cookies = await context.cookies()

# 3. 直接用 cookies 调用 API
httpx.get(url, cookies=cookies)  # 就这么简单！
```

**为什么可行**:
- NotebookLM API 只需要 session cookies
- 没有 reCAPTCHA 保护
- 认证机制相对简单

### Flow CLI 的真实实现（基于社区项目）

```
用户 → Chrome Extension → OAuth token + reCAPTCHA → Flow API
        ↑                    ↓
        └─ WebSocket ────────┘
     (localhost:3847/9222)
```

**真实端点**:
```
https://aisandbox-pa.googleapis.com/v1/projects/{projectId}/flowMedia:batchGenerateImages
```

**认证方式**（flow-proxy 项目）:
```javascript
// Chrome Extension (content script)
// 1. 从 labs.google 页面获取 OAuth token
const token = await getOAuthToken();

// 2. 自动解决 reCAPTCHA
const recaptchaToken = await solveRecaptcha();

// 3. 通过 WebSocket 发送给本地服务器
ws.send({
  type: 'token',
  oauth: token,
  recaptcha: recaptchaToken
});

// 本地服务器 (Node.js/Python)
// 4. 接收 tokens 并调用 API
const response = await fetch(apiUrl, {
  headers: {
    'Authorization': `Bearer ${oauthToken}`,
    'X-Recaptcha-Token': recaptchaToken
  }
});
```

**为什么更复杂**:
1. **OAuth Token**: 不是简单的 cookie，需要特殊的 bearer token
2. **reCAPTCHA**: 每次请求都需要验证（防止自动化）
3. **项目 ID**: 需要从 labs.google 会话中提取
4. **Chrome Extension**: 必须在真实浏览器环境中运行

## 现有的开源实现

### 1. [flow-proxy](https://github.com/liorium/flow-proxy) - 图片生成

**架构**:
```
CLI (TypeScript) ← WebSocket → Chrome Extension
                                    ↓
                            labs.google tab
                              (OAuth + reCAPTCHA)
```

**特点**:
- 本地服务器 port 3847
- Chrome extension 自动处理认证
- Token 持续 ~30 天
- 支持 Imagen 3.5

### 2. [flowkit](https://github.com/crisng95/flowkit) - 视频生成

**架构**:
```
Python Agent (FastAPI) ← WebSocket → Chrome Extension
     port 8100             (port 9222)
```

**特点**:
- 完整视频生成流程
- 支持多场景拼接
- 自动添加 TTS 旁白
- Reference images 保持一致性

## 实现 Flow CLI 的正确方法

基于我们的发现，有三种方法：

### 方法 1: 使用现有项目（推荐）

直接集成 flow-proxy 或 flowkit:

```bash
# 使用 flow-proxy
npm install -g flow-proxy
flow-proxy generate "a beautiful sunset"

# 使用 flowkit
git clone https://github.com/crisng95/flowkit
cd flowkit && python main.py
```

### 方法 2: 创建类似的架构

创建一个包含 Chrome Extension 的完整解决方案:

```
flow-cli/
├── cli/              # Python CLI
├── extension/        # Chrome Extension
│   ├── manifest.json
│   ├── content.js    # 获取 token + 解决 reCAPTCHA
│   └── background.js
└── server/           # WebSocket 服务器
```

**工作流程**:
1. 用户安装 Chrome Extension
2. 用户访问 labs.google/fx/tools/flow 并登录
3. CLI 启动本地 WebSocket 服务器
4. Extension 发送 OAuth token 到服务器
5. CLI 调用真实 API

### 方法 3: 简化版（仅文档/工具）

提供工具帮助用户手动获取 token:

```bash
# 1. 用户在浏览器 DevTools 中获取 token
flow auth capture  # 打开浏览器并显示如何获取 token

# 2. 用户复制 token
flow auth set --token "ya29.xxx..."

# 3. 使用 CLI
flow generate image "sunset"
```

## 为什么我的初始实现不够

我最初创建的 Flow CLI:
```python
# ❌ 这不够
cookies = extract_cookies_from_browser()
httpx.post(api_url, cookies=cookies)
```

**缺少的部分**:
1. ❌ 没有 OAuth Bearer token
2. ❌ 没有 reCAPTCHA 处理
3. ❌ 没有项目 ID 提取
4. ❌ 没有 Chrome Extension 桥梁

**需要的完整实现**:
```python
# ✅ 正确的方式
class FlowClient:
    def __init__(self):
        # 启动 WebSocket 服务器
        self.ws_server = WebSocketServer(port=3847)

        # 等待 Extension 发送 token
        self.oauth_token = await self.ws_server.wait_for_token()

        # 每次请求都需要新的 reCAPTCHA
        self.recaptcha_token = await self.ws_server.request_recaptcha()

    async def generate_image(self, prompt):
        response = await httpx.post(
            'https://aisandbox-pa.googleapis.com/v1/projects/{projectId}/flowMedia:batchGenerateImages',
            headers={
                'Authorization': f'Bearer {self.oauth_token}',
                'X-Recaptcha-Token': self.recaptcha_token
            },
            json={'prompt': prompt}
        )
```

## 推荐方案

### 短期：使用现有项目

直接使用 **flow-proxy** (图片) 或 **flowkit** (视频):

```bash
# 图片生成
npm install -g flow-proxy
flow-proxy generate "a serene mountain landscape"

# 视频生成
git clone https://github.com/crisng95/flowkit
cd flowkit
# 按照 README 安装 Chrome Extension
python main.py --prompt "drone shot of city"
```

### 长期：创建完整的 Python CLI

参考 flow-proxy 的架构，创建一个 Python 版本:

1. **创建 Chrome Extension** (manifest v3)
2. **Python WebSocket 服务器** (FastAPI/asyncio)
3. **CLI 接口** (Typer)
4. **自动化流程** (一键启动)

## 关键要点

| 特性 | NotebookLM CLI | Flow CLI |
|------|---------------|----------|
| 认证 | Cookies | OAuth + reCAPTCHA |
| 浏览器 | 一次性登录 | 持续运行 Extension |
| 实现难度 | 简单 ⭐ | 复杂 ⭐⭐⭐⭐ |
| 现有项目 | ✅ 已完成 | ✅ 已有但更复杂 |
| API 文档 | 社区已记录 | 社区已记录 + 需要 Extension |

## Sources

- [flow-proxy GitHub](https://github.com/liorium/flow-proxy) - 图片生成实现
- [flowkit GitHub](https://github.com/crisng95/flowkit) - 视频生成实现
- [NotebookLM CLI GitHub](https://github.com/jacob-bd/notebooklm-cli) - 简单 cookie 认证
- [API Reverse Engineering Guide](https://www.plaidnox.com/blog/demystifying-api-reverse-engineering-tools-techniques-for-2026)
