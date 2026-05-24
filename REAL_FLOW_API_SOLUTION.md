# Flow CLI 真实 API 解决方案

## 核心发现 🔍

经过调研，我找到了 Flow API 的真实实现方式：

### 真实 API 端点
```
https://aisandbox-pa.googleapis.com/v1/projects/{projectId}/flowMedia:batchGenerateImages
```

### 为什么简单的 cookie 认证不够

**NotebookLM** (简单):
```
浏览器登录 → cookies → 直接调 API ✅
```

**Flow** (复杂):
```
浏览器登录 → OAuth token + reCAPTCHA → 需要 Chrome Extension → 调 API ⚠️
```

## 已有的开源实现

好消息！社区已经有完整的实现了：

### 1. [flow-proxy](https://github.com/liorium/flow-proxy) - 图片生成 🖼️

```bash
# 安装
npm install -g flow-proxy

# 使用
flow-proxy generate "a beautiful mountain landscape"
```

**特点**:
- ✅ 完整的 Chrome Extension
- ✅ 自动处理 OAuth 和 reCAPTCHA
- ✅ 支持 Imagen 3.5
- ✅ Token 持续 30 天

### 2. [flowkit](https://github.com/crisng95/flowkit) - 视频生成 🎬

```bash
# 克隆
git clone https://github.com/crisng95/flowkit
cd flowkit

# 安装 Chrome Extension
# (见项目 README)

# 使用
python main.py --prompt "drone shot of futuristic city"
```

**特点**:
- ✅ 完整视频生成流程
- ✅ 多场景拼接
- ✅ TTS 旁白
- ✅ Python + FastAPI

## 三种使用方案

### 方案 A: 直接使用现有项目（最简单）⭐⭐⭐⭐⭐

**图片生成**:
```bash
npm install -g flow-proxy
flow-proxy generate "your prompt"
```

**视频生成**:
```bash
git clone https://github.com/crisng95/flowkit
cd flowkit && python main.py
```

**优点**:
- ✅ 开箱即用
- ✅ 社区维护
- ✅ 无需开发

**缺点**:
- ❌ 两个不同的工具（图片/视频分开）

### 方案 B: 基于现有项目创建统一 CLI ⭐⭐⭐

创建一个 Python CLI 包装 flow-proxy 和 flowkit:

```python
# flow_cli/wrapper.py
import subprocess

def generate_image(prompt):
    """调用 flow-proxy"""
    subprocess.run(['flow-proxy', 'generate', prompt])

def generate_video(prompt):
    """调用 flowkit"""
    subprocess.run(['python', 'flowkit/main.py', '--prompt', prompt])
```

**优点**:
- ✅ 统一接口
- ✅ 复用现有实现
- ✅ 快速实现

**缺点**:
- ❌ 依赖外部工具
- ❌ 需要 npm + Python

### 方案 C: 完全从零实现 ⭐

参考 flow-proxy 创建纯 Python 实现:

```
flow-cli/
├── cli/              # Python CLI (Typer)
├── extension/        # Chrome Extension
│   ├── manifest.json
│   ├── content.js   # OAuth + reCAPTCHA
│   └── background.js
├── server/          # WebSocket (FastAPI)
└── docs/
```

**优点**:
- ✅ 完全 Python
- ✅ 可自定义
- ✅ 学习价值高

**缺点**:
- ❌ 开发时间长（1-2 周）
- ❌ 需要维护 Extension
- ❌ 复杂度高

## 推荐方案：混合方案

结合现有项目 + Python 封装：

### Step 1: 安装现有工具

```bash
# 图片生成
npm install -g flow-proxy

# 视频生成
git clone https://github.com/crisng95/flowkit ~/flowkit
```

### Step 2: 创建 Python CLI 封装

```python
# src/flow_cli/cli.py

@app.command("image")
def generate_image(prompt: str):
    """Generate image using flow-proxy"""
    subprocess.run(['flow-proxy', 'generate', prompt])

@app.command("video")
def generate_video(prompt: str):
    """Generate video using flowkit"""
    subprocess.run([
        'python',
        os.path.expanduser('~/flowkit/main.py'),
        '--prompt', prompt
    ])
```

### Step 3: 使用统一接口

```bash
# 现在可以用一个命令
flow generate image "sunset"
flow generate video "drone shot"
```

## 快速开始（最简单的方法）

### 图片生成（5 分钟设置）

1. **安装 flow-proxy**:
   ```bash
   npm install -g flow-proxy
   ```

2. **安装 Chrome Extension**:
   - 访问 flow-proxy GitHub
   - 下载 extension
   - 在 Chrome 中加载 unpacked extension

3. **登录 Flow**:
   ```bash
   # 打开 Flow 并登录
   open https://labs.google/fx/tools/flow
   ```

4. **生成图片**:
   ```bash
   flow-proxy generate "a serene mountain landscape at sunset"
   ```

### 视频生成（10 分钟设置）

1. **克隆 flowkit**:
   ```bash
   git clone https://github.com/crisng95/flowkit
   cd flowkit
   ```

2. **安装依赖**:
   ```bash
   pip install -r requirements.txt
   ```

3. **安装 Chrome Extension**:
   - 按照 flowkit README 安装 extension

4. **运行**:
   ```bash
   python main.py --prompt "drone shot of futuristic city"
   ```

## 技术细节

### Flow API 请求格式

```javascript
// 图片生成
POST https://aisandbox-pa.googleapis.com/v1/projects/{projectId}/flowMedia:batchGenerateImages

Headers:
  Authorization: Bearer {oauth_token}
  X-Recaptcha-Token: {recaptcha_token}

Body:
{
  "prompt": "a beautiful sunset",
  "aspectRatio": "16:9",
  "model": "imagen4"
}
```

### 认证流程

```
1. 用户访问 labs.google/fx/tools/flow
2. Chrome Extension 提取 OAuth token
3. Extension 解决 reCAPTCHA 挑战
4. Extension 通过 WebSocket 发送 tokens
5. CLI 接收 tokens 并调用 API
```

### 为什么需要 Chrome Extension

```
Flow API 安全措施:
1. ✅ OAuth token (不是简单 cookie)
2. ✅ reCAPTCHA v3 (防自动化)
3. ✅ 项目 ID (从会话提取)
4. ✅ 实时 token 刷新

Chrome Extension 的作用:
→ 在真实浏览器环境中
→ 自动获取 OAuth token
→ 自动解决 reCAPTCHA
→ 保持会话活跃
```

## 下一步行动

### 如果你想快速使用 Flow CLI:

```bash
# 1. 安装 flow-proxy (图片)
npm install -g flow-proxy

# 2. 安装 extension 并生成图片
flow-proxy generate "your prompt"

# 完成！🎉
```

### 如果你想开发完整的 Python CLI:

1. Fork flow-proxy 了解 Chrome Extension 实现
2. 创建 Python WebSocket 服务器 (FastAPI)
3. 移植 Extension 到项目中
4. 创建统一的 CLI 接口 (Typer)
5. 添加 MCP Server 支持

预计开发时间: 1-2 周

## 总结

| 需求 | 推荐方案 | 时间 |
|------|---------|------|
| 只想生成图片 | flow-proxy | 5分钟 |
| 只想生成视频 | flowkit | 10分钟 |
| 想要统一 CLI | Python 封装器 | 1小时 |
| 想要完整项目 | 从零实现 | 1-2周 |

## Resources

- 📦 [flow-proxy](https://github.com/liorium/flow-proxy) - 图片生成 (TypeScript)
- 🎬 [flowkit](https://github.com/crisng95/flowkit) - 视频生成 (Python)
- 📝 [NotebookLM CLI](https://github.com/jacob-bd/notebooklm-cli) - 简单认证示例
- 🔧 [API Reverse Engineering](https://www.plaidnox.com/blog/demystifying-api-reverse-engineering-tools-techniques-for-2026)

---

**结论**: Flow CLI 需要 Chrome Extension + OAuth + reCAPTCHA，比 NotebookLM 复杂得多。推荐直接使用现有的开源项目（flow-proxy + flowkit），或创建一个 Python 封装器统一接口。
