# Flow CLI 项目现状

## ✅ 已完成的工作

### 1. 完整的项目框架
```
flow-cli/
├── src/flow_cli/
│   ├── __init__.py          ✅ 包初始化
│   ├── auth.py              ✅ Playwright 认证框架
│   ├── client.py            ✅ API 客户端框架
│   ├── cli.py               ✅ 完整 CLI 命令
│   ├── config.py            ✅ 配置管理
│   ├── models.py            ✅ 数据模型
│   ├── capture.py           ✅ API 捕获工具
│   └── mcp_server.py        ✅ MCP Server 支持
├── tests/                   ✅ 单元测试
├── docs/                    ✅ 完整文档
└── pyproject.toml           ✅ 项目配置
```

### 2. 核心发现

**真实 Flow API**:
- 端点: `https://aisandbox-pa.googleapis.com/v1/projects/{projectId}/flowMedia:batchGenerateImages`
- 认证: OAuth Bearer token + reCAPTCHA
- 架构: 需要 Chrome Extension 桥梁

**与 NotebookLM 的区别**:
| 特性 | NotebookLM | Flow |
|------|-----------|------|
| 认证 | Cookies | OAuth + reCAPTCHA |
| 实现 | 简单 | 需要 Extension |
| 难度 | ⭐ | ⭐⭐⭐⭐⭐ |

### 3. 开源项目发现

**flow-proxy** - 图片生成 (TypeScript):
- https://github.com/liorium/flow-proxy
- 完整的 Chrome Extension
- 已可用！

**flowkit** - 视频生成 (Python):
- https://github.com/crisng95/flowkit
- 完整视频生成流程
- 已可用！

## ⚠️ 当前状态

### 我创建的框架
- ✅ **CLI 接口**: 完整的 Typer 命令行
- ✅ **数据模型**: Pydantic 验证
- ✅ **配置管理**: 多 profile 支持
- ✅ **MCP Server**: Claude 集成
- ⚠️ **API 客户端**: 端点是占位符，需要更新
- ❌ **Chrome Extension**: 还未实现

### 缺少的部分（需要实现）
1. **Chrome Extension** (JavaScript):
   - 获取 OAuth token
   - 解决 reCAPTCHA
   - WebSocket 通信

2. **WebSocket 服务器** (Python):
   - 接收 Extension 的 tokens
   - 管理会话

3. **真实 API 集成**:
   - 更新 `client.py` 使用真实端点
   - 添加 OAuth 认证
   - 添加 reCAPTCHA 处理

## 🎯 三个使用选项

### 选项 1: 直接使用现有开源项目（推荐）⭐⭐⭐⭐⭐

**立即可用，无需开发**

```bash
# 图片生成
npm install -g flow-proxy
flow-proxy generate "a beautiful sunset"

# 视频生成
git clone https://github.com/crisng95/flowkit
cd flowkit && python main.py
```

**优点**:
- ✅ 5-10 分钟设置
- ✅ 社区维护
- ✅ 已验证可用

**缺点**:
- ❌ 不是纯 Python
- ❌ 两个独立工具

---

### 选项 2: 创建 Python 封装器 ⭐⭐⭐

**基于我的框架，封装现有工具**

```python
# src/flow_cli/cli.py (更新后)
import subprocess
import shutil

@app.command("image")
def generate_image(prompt: str):
    """Generate image via flow-proxy"""
    if not shutil.which('flow-proxy'):
        console.print("[red]flow-proxy not installed![/red]")
        console.print("Run: npm install -g flow-proxy")
        return

    subprocess.run(['flow-proxy', 'generate', prompt])

@app.command("video")
def generate_video(prompt: str):
    """Generate video via flowkit"""
    flowkit_path = Path.home() / 'flowkit' / 'main.py'
    if not flowkit_path.exists():
        console.print("[red]flowkit not found![/red]")
        console.print("Run: git clone https://github.com/crisng95/flowkit ~/flowkit")
        return

    subprocess.run(['python', str(flowkit_path), '--prompt', prompt])
```

**优点**:
- ✅ 统一接口
- ✅ 1-2 小时实现
- ✅ 复用现有工具

**缺点**:
- ❌ 依赖外部工具（npm + git）

**实现步骤**:
1. 更新 `cli.py` 添加封装函数
2. 添加依赖检查
3. 创建安装脚本
4. 测试

---

### 选项 3: 完全从零实现 ⭐⭐⭐⭐⭐

**基于我的框架，添加 Extension + WebSocket**

**需要实现**:
1. **Chrome Extension** (参考 flow-proxy):
   ```javascript
   // extension/content.js
   async function getOAuthToken() {
     // 从 labs.google 页面提取 token
   }

   async function solveRecaptcha() {
     // 自动解决 reCAPTCHA
   }

   // 通过 WebSocket 发送给本地服务器
   ws.send({oauth: token, recaptcha: captchaToken});
   ```

2. **WebSocket 服务器**:
   ```python
   # src/flow_cli/ws_server.py
   class TokenServer:
       async def wait_for_tokens(self):
           """等待 Extension 发送 tokens"""
           async with websockets.serve(...):
               # 接收并返回 tokens
   ```

3. **更新 API 客户端**:
   ```python
   # src/flow_cli/client.py
   async def generate_image(self, request):
       # 1. 启动 WebSocket 服务器
       server = TokenServer()

       # 2. 等待 Extension 发送 tokens
       tokens = await server.wait_for_tokens()

       # 3. 调用真实 API
       response = await httpx.post(
           'https://aisandbox-pa.googleapis.com/v1/projects/{projectId}/flowMedia:batchGenerateImages',
           headers={
               'Authorization': f'Bearer {tokens.oauth}',
               'X-Recaptcha-Token': tokens.recaptcha
           },
           json={'prompt': request.prompt}
       )
   ```

**优点**:
- ✅ 完全 Python
- ✅ 可自定义
- ✅ 学习价值

**缺点**:
- ❌ 1-2 周开发时间
- ❌ 需要维护 Extension
- ❌ 高复杂度

**实现步骤**:
1. Fork flow-proxy，研究 Extension 实现
2. 创建 `extension/` 目录，移植 JavaScript 代码
3. 实现 `ws_server.py` (FastAPI + WebSockets)
4. 更新 `client.py` 使用真实端点
5. 添加完整错误处理
6. 编写测试

**预计时间**: 1-2 周全职开发

## 📝 完整文档

我已经创建了以下文档：

1. **REAL_FLOW_API_SOLUTION.md** - 完整解决方案和三个选项
2. **WHY_DIFFERENT_FROM_NOTEBOOKLM.md** - 技术对比详解
3. **HOW_TO_CAPTURE_API.md** - 如何捕获 API 端点
4. **API_RESEARCH.md** - API 调研文档
5. **README.md** - 项目说明
6. **QUICKSTART.md** - 快速开始
7. **EXAMPLES.md** - 使用示例
8. **SETUP.md** - 开发设置

## 🚀 推荐行动

### 如果你只想立即使用 Flow (5分钟):

```bash
# 安装 flow-proxy
npm install -g flow-proxy

# 生成图片
flow-proxy generate "a serene mountain landscape at sunset"
```

### 如果你想要统一的 Python CLI (1小时):

1. 安装依赖工具:
   ```bash
   npm install -g flow-proxy
   git clone https://github.com/crisng95/flowkit ~/flowkit
   ```

2. 更新我创建的 `cli.py`，添加封装函数

3. 使用:
   ```bash
   flow generate image "sunset"
   flow generate video "drone shot"
   ```

### 如果你想要完整的纯 Python 实现 (1-2周):

1. 研究 flow-proxy 的 Chrome Extension
2. 在我的框架基础上添加:
   - `extension/` (Chrome Extension)
   - `ws_server.py` (WebSocket)
   - 更新 `client.py` (真实 API)
3. 测试和发布

## 📊 项目价值

### 我创建的框架价值
- ✅ 完整的 CLI 架构（可复用）
- ✅ 良好的代码结构（可扩展）
- ✅ 丰富的文档（可学习）
- ✅ MCP Server 支持（可集成 Claude）

### 学习价值
- 理解 API 反向工程
- 学习 OAuth 认证流程
- 掌握 Chrome Extension 开发
- 理解 WebSocket 通信
- 实践完整的 CLI 开发

## 🎓 技术栈总结

**当前实现**:
- Python 3.10+
- Typer (CLI)
- Playwright (浏览器自动化)
- Pydantic (数据验证)
- httpx (HTTP 客户端)

**需要添加**（选项 3）:
- JavaScript (Chrome Extension)
- FastAPI (WebSocket 服务器)
- websockets (通信)
- OAuth 2.0 (认证)

## 🔗 相关资源

- [flow-proxy](https://github.com/liorium/flow-proxy) - 图片生成（可用）
- [flowkit](https://github.com/crisng95/flowkit) - 视频生成（可用）
- [NotebookLM CLI](https://github.com/jacob-bd/notebooklm-cli) - 参考项目
- [Google Flow](https://labs.google/fx/tools/flow) - 官方网站

## 结论

✅ **框架完成**: 我已经创建了一个完整的 Python CLI 框架
⚠️ **需要 Extension**: Flow API 需要 Chrome Extension，比 NotebookLM 复杂
🎯 **推荐方案**: 直接使用 flow-proxy (5分钟) 或创建封装器 (1小时)
🚀 **下一步**: 选择一个选项并开始实现！
