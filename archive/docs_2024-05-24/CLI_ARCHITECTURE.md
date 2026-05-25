# Flow CLI 架构文档

## 概述

Flow CLI 是一个用于自动化 Google Flow 图片生成的命令行工具。它将原始的自动化脚本封装成了一个完整的 CLI 应用。

## 架构设计

### 模块结构

```
flow_cli/
├── __init__.py        # 包版本和初始化
├── cli.py             # CLI 主入口和命令解析
├── automation.py      # 自动化核心逻辑
├── config.py          # 配置管理
└── chrome.py          # Chrome 进程管理
```

### 组件职责

#### 1. cli.py - CLI 接口层

**职责:**
- 命令行参数解析（使用 argparse）
- 命令分发（generate, config, start-chrome, stop-chrome）
- 用户交互和输出格式化
- 错误处理和异常捕获

**主要函数:**
- `main()` - CLI 入口点
- `cmd_generate()` - 处理 generate 命令
- `cmd_config()` - 处理 config 命令
- `cmd_start_chrome()` - 处理 start-chrome 命令
- `cmd_stop_chrome()` - 处理 stop-chrome 命令

**设计模式:**
- Command Pattern（命令模式）
- 每个命令对应一个处理函数
- 清晰的输入验证和错误处理

#### 2. automation.py - 自动化引擎

**职责:**
- 连接到 Chrome（CDP 协议）
- 操作 Flow 页面元素
- 执行完整的生成流程
- 截图和状态验证

**核心类:**

```python
class FlowAutomation:
    async def connect()                      # 连接到 Chrome
    async def add_reference_image(name)      # 添加单张参考图
    async def add_reference_images(images)   # 添加多张参考图
    async def input_prompt(prompt)           # 输入生成 Prompt
    async def submit_generation(screenshot)  # 提交生成请求
    async def generate(images, prompt, ...)  # 完整流程
    async def close()                        # 关闭连接
```

**设计模式:**
- Facade Pattern（外观模式）
- 封装复杂的 Playwright 操作
- 提供简洁的高层 API

#### 3. config.py - 配置管理

**职责:**
- 读写配置文件
- 提供默认配置
- 配置验证和访问

**核心类:**

```python
class Config:
    def __init__(config_path)        # 初始化并加载配置
    def save()                       # 保存配置到文件
    def get(key, default)            # 获取配置值
    def set(key, value)              # 设置配置值
    def get_project_url()            # 专用 getter
    def set_project_url(url)         # 专用 setter
    # ... 其他配置项的 getter/setter
```

**配置存储:**
- 位置: `~/.config/flow-cli/config.json`
- 格式: JSON
- 自动创建父目录

**默认配置:**

```json
{
  "cdp_url": "http://127.0.0.1:9222",
  "chrome_profile": "/tmp/flow_chrome_debug",
  "project_url": "",
  "screenshot_dir": "/tmp"
}
```

#### 4. chrome.py - Chrome 管理

**职责:**
- 跨平台 Chrome 路径检测
- 启动 Chrome 进程（带调试端口）
- 停止 Chrome 进程

**核心函数:**

```python
def get_chrome_path()                    # 获取 Chrome 路径（跨平台）
def start_chrome(port, profile) -> bool  # 启动 Chrome
def stop_chrome() -> bool                # 停止 Chrome
```

**平台支持:**
- macOS: `/Applications/Google Chrome.app/Contents/MacOS/Google Chrome`
- Linux: `/usr/bin/google-chrome` 或 `/usr/bin/chromium`
- Windows: `C:\Program Files\Google\Chrome\Application\chrome.exe`

## 数据流

### 生成流程

```
用户命令
  ↓
flow generate -i img1.png -i img2.png -p "prompt"
  ↓
cli.py (参数解析)
  ↓
cmd_generate(args)
  ↓
Config (读取配置)
  ↓
FlowAutomation (初始化)
  ↓
automation.connect() (连接 Chrome)
  ↓
automation.add_reference_images() (添加图片)
  │
  ├─ 打开媒体选择器
  ├─ 选择文件
  └─ 点击 "Add to Prompt"
  ↓
automation.input_prompt() (输入 Prompt)
  ↓
automation.submit_generation() (提交)
  │
  ├─ 点击 Create 按钮
  └─ 保存截图
  ↓
automation.close() (关闭连接)
  ↓
输出结果给用户
```

### 配置管理流程

```
用户命令
  ↓
flow config --set-project URL
  ↓
cli.py (参数解析)
  ↓
cmd_config(args)
  ↓
Config (加载现有配置)
  ↓
config.set_project_url(URL)
  ↓
config.save()
  ↓
写入 ~/.config/flow-cli/config.json
  ↓
输出确认信息
```

## 依赖关系

```
cli.py
  ├─ automation.py
  │   └─ playwright (Playwright 库)
  ├─ config.py
  │   └─ json (标准库)
  └─ chrome.py
      └─ subprocess (标准库)
```

## 错误处理策略

### 分层错误处理

1. **自动化层** (automation.py)
   - 捕获 Playwright 异常
   - 超时处理
   - 元素定位失败

2. **CLI 层** (cli.py)
   - 参数验证
   - 配置缺失
   - 用户友好的错误消息

3. **Chrome 管理层** (chrome.py)
   - 进程启动失败
   - 权限错误
   - 路径不存在

### 错误处理示例

```python
# automation.py
try:
    await file_item.click()
except TimeoutError:
    print(f"❌ 未找到文件: {image_name}")
    raise

# cli.py
try:
    asyncio.run(_run_generate(...))
except KeyboardInterrupt:
    print("\n中断执行")
    return 130
except Exception as e:
    print(f"❌ 错误: {e}")
    traceback.print_exc()
    return 1
```

## 扩展性设计

### 1. 添加新命令

在 `cli.py` 中：

```python
# 1. 添加 subparser
upload_parser = subparsers.add_parser('upload', help='上传文件')
upload_parser.add_argument('-f', '--file', required=True)

# 2. 添加命令处理
elif args.command == 'upload':
    return cmd_upload(args)

# 3. 实现命令函数
def cmd_upload(args):
    # 实现逻辑
    pass
```

### 2. 添加新配置项

在 `config.py` 中：

```python
# 1. 更新默认配置
def _default_config(self) -> dict:
    return {
        # ... 现有配置
        "new_setting": "default_value"
    }

# 2. 添加 getter/setter
def get_new_setting(self) -> str:
    return self.data.get("new_setting", "default_value")

def set_new_setting(self, value: str):
    self.data["new_setting"] = value
```

### 3. 添加新自动化功能

在 `automation.py` 中：

```python
class FlowAutomation:
    async def new_feature(self, ...):
        """新功能的实现"""
        # 使用 self.page 操作页面
        # 使用 self.screenshot_dir 保存截图
        pass
```

## 性能考虑

### 1. 连接复用

Chrome 可以保持运行，避免重复启动：

```python
# 用户可以这样使用
flow start-chrome  # 启动一次

flow generate ...  # 多次生成，复用连接
flow generate ...
flow generate ...
```

### 2. 配置缓存

Config 对象在单次命令执行中只加载一次：

```python
config = Config()  # 只读取一次文件
project_url = config.get_project_url()
cdp_url = config.get_cdp_url()
```

### 3. 异步操作

使用 Playwright 的异步 API：

```python
async def add_reference_images(self, images):
    for img in images:
        await self.add_reference_image(img)  # 异步等待
```

## 测试策略

### 单元测试（未来）

```python
# tests/test_config.py
def test_config_default():
    config = Config()
    assert config.get_cdp_url() == "http://127.0.0.1:9222"

# tests/test_chrome.py
def test_get_chrome_path():
    path = get_chrome_path()
    assert path is not None
```

### 集成测试（未来）

```python
# tests/test_cli.py
async def test_generate():
    automation = FlowAutomation(...)
    await automation.connect()
    await automation.generate(["test.png"], "test prompt")
```

## 部署和分发

### 1. 开发模式

```bash
pip install -e .
```

- 代码改动立即生效
- 适合开发调试

### 2. 正式安装

```bash
pip install .
```

- 安装固定版本
- 适合生产使用

### 3. PyPI 发布（未来）

```bash
python -m build
twine upload dist/*
```

- 可通过 `pip install flow-cli` 安装
- 版本管理

## 维护和更新

### 版本管理

在 `flow_cli/__init__.py`:

```python
__version__ = "0.1.0"
```

在 `pyproject.toml`:

```toml
[project]
version = "0.1.0"
```

### 更新流程

1. 修改代码
2. 更新版本号
3. 更新 CHANGELOG
4. 提交 Git
5. 创建 Tag
6. 发布（如果需要）

## 安全考虑

### 1. 配置文件权限

```python
# 确保配置文件只有用户可读写
os.chmod(config_path, 0o600)
```

### 2. Chrome Profile 隔离

使用独立的测试 profile，不影响系统 Chrome：

```python
chrome_profile = "/tmp/flow_chrome_debug"
```

### 3. 输入验证

```python
# 验证 URL 格式
if not project_url.startswith("https://labs.google/fx/tools/flow/"):
    print("❌ 无效的项目 URL")
    return 1
```

## 未来改进

### 短期（1-2 周）

- [ ] 环境变量支持
- [ ] 批量生成
- [ ] 进度条显示
- [ ] 更详细的日志

### 中期（1-2 月）

- [ ] 交互式配置向导
- [ ] 结果自动下载
- [ ] 多项目管理
- [ ] Shell 自动补全

### 长期（3-6 月）

- [ ] Web 界面
- [ ] 插件系统
- [ ] API 服务
- [ ] 云端同步

## 总结

Flow CLI 采用了清晰的分层架构：

1. **CLI 层** - 用户交互
2. **业务逻辑层** - 自动化引擎
3. **配置层** - 持久化配置
4. **系统层** - Chrome 管理

这种设计使得每个模块职责单一、易于测试和扩展。

---

**创建日期:** 2026-05-24  
**版本:** v0.1.0  
**作者:** Flow CLI Team
