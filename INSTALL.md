# Flow CLI 安装指南

## 安装方式

### 方式1: 开发模式安装（推荐用于测试）

```bash
cd flow-cli
pip install -e .
```

这样安装后可以直接修改代码，改动会立即生效。

### 方式2: 正式安装

```bash
cd flow-cli
pip install .
```

### 方式3: 从 GitHub 安装

```bash
pip install git+https://github.com/yourusername/flow-cli.git
```

## 安装 Playwright

```bash
playwright install chromium
```

## 验证安装

```bash
flow --help
```

应该看到 Flow CLI 的帮助信息。

## 初始配置

### 1. 设置项目 URL

```bash
flow config --set-project https://labs.google/fx/tools/flow/project/YOUR_PROJECT_ID
```

### 2. 查看配置

```bash
flow config --show
```

### 3. 启动 Chrome

```bash
flow start-chrome
```

然后在 Chrome 中：
1. 登录 Google 账号
2. 访问你的 Flow 项目

### 4. 测试生成

```bash
flow generate \
  -i Luna_on_mars.png \
  -i Wayne_on_earth.png \
  -p "他们在中国杭州玩"
```

## 升级

### 开发模式

如果使用 `-e` 安装，代码改动会自动生效，无需重新安装。

### 正式安装

```bash
cd flow-cli
git pull
pip install --upgrade .
```

## 卸载

```bash
pip uninstall flow-cli
```

## 常见问题

### Q: 找不到 flow 命令

**A:** 确保 pip 的 bin 目录在 PATH 中：

```bash
# macOS/Linux
export PATH="$HOME/.local/bin:$PATH"

# 或者使用 pipx (推荐)
pipx install -e .
```

### Q: Playwright 连接失败

**A:** 确认 Chrome 已启动：

```bash
flow start-chrome
```

然后检查端口：

```bash
lsof -i :9222
```

### Q: 模块导入错误

**A:** 重新安装：

```bash
pip uninstall flow-cli
pip install -e .
```

## 配置文件位置

配置文件保存在：

```
~/.config/flow-cli/config.json
```

可以手动编辑这个文件。

## 依赖要求

- Python 3.10+
- Playwright 1.40.0+
- Google Chrome (系统安装)
- macOS / Linux / Windows
