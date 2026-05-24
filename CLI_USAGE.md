# Flow CLI 使用指南

## 命令概览

```bash
flow --help              # 显示帮助
flow generate            # 生成图片
flow config              # 配置管理
flow start-chrome        # 启动 Chrome
flow stop-chrome         # 停止 Chrome
```

## 详细用法

### 1. generate - 生成图片

#### 基础用法

```bash
flow generate -i 图片1.png -i 图片2.png -p "生成描述"
```

#### 参数说明

- `-i, --image` - 参考图文件名（必需，可多次使用）
- `-p, --prompt` - 生成描述 Prompt（必需）
- `--project` - 项目 URL（可选，覆盖配置）
- `--no-screenshot` - 不保存截图（可选）

#### 示例

```bash
# 基础示例
flow generate \
  -i Luna_on_mars.png \
  -i Wayne_on_earth.png \
  -p "他们在中国杭州玩"

# 使用不同的项目
flow generate \
  -i image1.png \
  -i image2.png \
  -p "A beautiful sunset" \
  --project https://labs.google/fx/tools/flow/project/OTHER_PROJECT_ID

# 不保存截图
flow generate \
  -i photo.png \
  -p "Professional headshot" \
  --no-screenshot

# 添加更多参考图
flow generate \
  -i ref1.png \
  -i ref2.png \
  -i ref3.png \
  -i ref4.png \
  -p "Group photo at Disney"
```

### 2. config - 配置管理

#### 查看配置

```bash
flow config --show
```

输出示例：
```
======================================================================
Flow CLI 配置
======================================================================

配置文件: /Users/username/.config/flow-cli/config.json

CDP URL:        http://127.0.0.1:9222
项目 URL:       https://labs.google/fx/tools/flow/project/4f24835c-...
Chrome Profile: /tmp/flow_chrome_debug
截图目录:       /tmp
```

#### 设置项目 URL

```bash
flow config --set-project https://labs.google/fx/tools/flow/project/YOUR_PROJECT_ID
```

#### 设置截图目录

```bash
flow config --set-screenshot-dir ~/Pictures/flow-screenshots

# 或使用绝对路径
flow config --set-screenshot-dir /Users/username/Desktop/screenshots
```

#### 设置 CDP URL（高级）

```bash
# 通常不需要修改，除非使用自定义端口
flow config --set-cdp-url http://127.0.0.1:9223
```

### 3. start-chrome - 启动 Chrome

#### 基础用法

```bash
flow start-chrome
```

#### 参数说明

- `--port` - 调试端口（默认: 9222）
- `--profile` - Chrome profile 目录（默认: /tmp/flow_chrome_debug）

#### 示例

```bash
# 使用默认设置
flow start-chrome

# 使用自定义端口
flow start-chrome --port 9223

# 使用自定义 profile
flow start-chrome --profile /tmp/my_chrome_profile

# 组合使用
flow start-chrome --port 9223 --profile /tmp/custom_profile
```

启动后，Chrome 会自动打开。你需要：
1. 登录 Google 账号
2. 访问你的 Flow 项目页面

### 4. stop-chrome - 停止 Chrome

```bash
flow stop-chrome
```

会关闭所有 Chrome 实例。

## 完整工作流程

### 第一次使用

```bash
# 1. 安装
pip install -e .
playwright install chromium

# 2. 配置项目
flow config --set-project https://labs.google/fx/tools/flow/project/YOUR_PROJECT_ID

# 3. 设置截图目录（可选）
flow config --set-screenshot-dir ~/Pictures/flow

# 4. 验证配置
flow config --show

# 5. 启动 Chrome
flow start-chrome

# 6. 在 Chrome 中登录并打开项目

# 7. 生成图片
flow generate -i image1.png -i image2.png -p "Your prompt"
```

### 日常使用

```bash
# 1. 启动 Chrome（如果还没运行）
flow start-chrome

# 2. 生成图片
flow generate -i photo1.png -i photo2.png -p "生成描述"

# 3. 完成后关闭 Chrome（可选）
flow stop-chrome
```

## 提示和技巧

### 1. 保持 Chrome 运行

Chrome 可以一直保持运行状态，无需每次都重启：

```bash
# 启动一次
flow start-chrome

# 然后可以多次生成
flow generate -i img1.png -p "prompt 1"
flow generate -i img2.png -p "prompt 2"
flow generate -i img3.png -p "prompt 3"
```

### 2. 多项目管理

为不同项目创建配置文件：

```bash
# 项目 A
flow config --set-project https://labs.google/fx/tools/flow/project/PROJECT_A_ID
flow generate -i imageA.png -p "Project A prompt"

# 项目 B（使用 --project 覆盖）
flow generate \
  -i imageB.png \
  -p "Project B prompt" \
  --project https://labs.google/fx/tools/flow/project/PROJECT_B_ID
```

### 3. 截图管理

设置有意义的截图目录：

```bash
# 按项目组织截图
flow config --set-screenshot-dir ~/Pictures/flow/project-disney

# 按日期组织
flow config --set-screenshot-dir ~/Pictures/flow/$(date +%Y-%m-%d)
```

### 4. 快速测试

测试配置是否正确：

```bash
# 1. 检查配置
flow config --show

# 2. 检查 Chrome 是否运行
lsof -i :9222

# 3. 快速生成（使用简单的参考图）
flow generate -i test.png -p "test prompt" --no-screenshot
```

### 5. 错误排查

```bash
# Chrome 连接失败？
lsof -i :9222  # 检查端口是否打开

# 找不到文件？
# 确保文件已上传到 Flow 的 Uploads

# 配置丢失？
cat ~/.config/flow-cli/config.json  # 查看配置文件
```

## 进阶用法

### 脚本集成

在 shell 脚本中使用：

```bash
#!/bin/bash
# generate_batch.sh

IMAGES=(
  "person1.png"
  "person2.png"
  "person3.png"
)

PROMPTS=(
  "At the beach"
  "In the mountains"
  "At a cafe"
)

for i in "${!IMAGES[@]}"; do
  echo "Generating image $((i+1))/${#IMAGES[@]}..."
  flow generate \
    -i "${IMAGES[$i]}" \
    -p "${PROMPTS[$i]}" \
    --no-screenshot

  sleep 5  # 等待生成完成
done
```

### Python 集成

作为 Python 库使用：

```python
import asyncio
from flow_cli.automation import FlowAutomation
from flow_cli.config import Config

async def main():
    config = Config()

    automation = FlowAutomation(
        cdp_url=config.get_cdp_url(),
        project_url=config.get_project_url(),
        screenshot_dir=config.get_screenshot_dir()
    )

    try:
        await automation.connect()
        await automation.generate(
            images=["image1.png", "image2.png"],
            prompt="My custom prompt",
            screenshot=True
        )
    finally:
        await automation.close()

asyncio.run(main())
```

## 环境变量

可以通过环境变量覆盖配置：

```bash
# 设置环境变量
export FLOW_CDP_URL="http://127.0.0.1:9223"
export FLOW_PROJECT_URL="https://labs.google/fx/tools/flow/project/YOUR_ID"
export FLOW_SCREENSHOT_DIR="~/Pictures/flow"

# 然后运行命令（会优先使用环境变量）
flow generate -i image.png -p "prompt"
```

注：当前版本尚未实现环境变量支持，这是未来的功能。

## 常见错误和解决方案

### 1. `playwright._impl._errors.Error: connect ECONNREFUSED`

**原因:** Chrome 未启动或端口不正确

**解决:**
```bash
flow start-chrome
lsof -i :9222  # 确认端口已打开
```

### 2. `FileNotFoundError: [Errno 2] No such file or directory`

**原因:** Chrome 可执行文件路径不正确

**解决:**
- macOS: 确认 Chrome 安装在 `/Applications/Google Chrome.app`
- Linux: 检查 `/usr/bin/google-chrome` 或 `/usr/bin/chromium`
- Windows: 检查 `C:\Program Files\Google\Chrome\Application\chrome.exe`

### 3. `Timeout: element not found`

**原因:** 文件名不匹配或文件未上传

**解决:**
- 确认文件名完全匹配（区分大小写）
- 确认文件已上传到 Flow 的 Uploads
- 确认已登录 Google 账号
- 确认已打开正确的项目页面

### 4. `未设置项目 URL`

**原因:** 配置文件中没有项目 URL

**解决:**
```bash
flow config --set-project https://labs.google/fx/tools/flow/project/YOUR_ID
```

## 获取帮助

```bash
# 查看总体帮助
flow --help

# 查看特定命令的帮助
flow generate --help
flow config --help
flow start-chrome --help
```

## 卸载

```bash
pip uninstall flow-cli
rm -rf ~/.config/flow-cli  # 删除配置文件（可选）
```
