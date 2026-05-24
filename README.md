# Flow CLI - Google Flow 自动化工具

自动化 Google Flow 图片生成的命令行工具。

## 🎯 功能

- ✅ **命令行界面** - 简单易用的 CLI 工具
- ✅ **配置管理** - 支持配置文件和命令行参数
- ✅ **Chrome 管理** - 一键启动/停止 Chrome
- ✅ **自动添加参考图** - 支持多张图片
- ✅ **自动输入描述** - 自定义生成 Prompt
- ✅ **自动提交生成** - 完整的自动化流程
- ✅ **截图保存** - 自动保存生成结果
- ✅ **错误处理** - 完善的错误提示

## 📋 快速参考

```bash
# 安装
pip install -e .

# 配置
flow config --set-project <PROJECT_URL>

# 启动
flow start-chrome

# 生成
flow generate -i image1.png -i image2.png -p "prompt"

# 查看帮助
flow --help
```

详细用法见：[CLI 使用指南](CLI_USAGE.md)

## 📦 安装

### 方式1: CLI 工具安装（推荐）

```bash
# 克隆仓库
git clone <repository-url>
cd flow-cli

# 开发模式安装
pip install -e .

# 安装 Playwright
playwright install chromium
```

详细安装说明见：[INSTALL.md](INSTALL.md)

### 方式2: 直接运行脚本

```bash
# 安装依赖
pip install playwright
playwright install chromium

# 使用脚本
./scripts/start_chrome.sh
python3 scripts/flow_automation_final.py
```

## 🚀 快速开始

### 使用 CLI（推荐）

```bash
# 1. 配置项目
flow config --set-project https://labs.google/fx/tools/flow/project/YOUR_PROJECT_ID

# 2. 启动 Chrome
flow start-chrome

# 3. 在 Chrome 中登录 Google 账号并打开 Flow 项目

# 4. 生成图片
flow generate \
  -i Luna_on_mars.png \
  -i Wayne_on_earth.png \
  -p "他们在中国杭州玩"
```

### 使用脚本

```bash
# 1. 启动 Chrome
./scripts/start_chrome.sh

# 2. 登录并打开项目（在 Chrome 中）

# 3. 运行自动化
python3 scripts/flow_automation_final.py
```

## 📚 文档

- [CLI 使用指南](CLI_USAGE.md) - **CLI 工具完整使用说明** ⭐
- [安装指南](INSTALL.md) - 详细的安装步骤
- [完整教程](docs/FLOW_TUTORIAL.md) - 详细的操作教程
- [技能文档](docs/FLOW_SKILL.md) - 界面元素和选项详解
- [总结文档](docs/FLOW_AUTOMATION_SUMMARY.md) - 完整总结和经验

## ⚙️ 配置

### CLI 配置

```bash
# 查看当前配置
flow config --show

# 设置项目 URL
flow config --set-project https://labs.google/fx/tools/flow/project/YOUR_PROJECT_ID

# 设置截图保存目录
flow config --set-screenshot-dir ~/Pictures/flow-screenshots

# 设置 CDP URL（通常不需要修改）
flow config --set-cdp-url http://127.0.0.1:9222
```

配置文件位置：`~/.config/flow-cli/config.json`

### 脚本配置

编辑 `scripts/flow_automation_final.py` 中的配置：

```python
# 项目 URL
PROJECT_URL = "https://labs.google/fx/tools/flow/project/YOUR_PROJECT_ID"

# 参考图文件名
REFERENCE_IMAGES = [
    "your_image1.png",
    "your_image2.png"
]

# 生成 Prompt
PROMPT = "你的自定义 prompt"
```

## 📁 项目结构

```
flow-cli/
├── README.md              # 项目说明
├── INSTALL.md             # 安装指南
├── pyproject.toml         # Python 项目配置
├── setup.py               # 安装脚本
├── flow_cli/              # CLI 工具包
│   ├── __init__.py        # 包初始化
│   ├── cli.py             # CLI 主入口
│   ├── automation.py      # 自动化核心逻辑
│   ├── config.py          # 配置管理
│   └── chrome.py          # Chrome 管理工具
├── docs/                  # 文档目录
│   ├── FLOW_TUTORIAL.md   # 完整教程
│   ├── FLOW_SKILL.md      # 技能文档
│   └── FLOW_AUTOMATION_SUMMARY.md  # 总结文档
├── scripts/               # 脚本目录（向后兼容）
│   ├── start_chrome.sh    # Chrome 启动脚本
│   └── flow_automation_final.py  # 主自动化脚本
└── archive/               # 历史尝试（失败的方案）
    ├── README.md          # 失败原因说明
    └── [旧脚本...]
```

## 🎓 学到的经验

### 成功的关键

1. **正确的入口点**
   - ✅ 使用输入框旁的加号按钮
   - ❌ 不是顶部的 "Add Media" 按钮

2. **稳定的选择器**
   - ✅ 文本选择器和坐标点击
   - ❌ 复杂的 CSS 选择器

3. **Chrome Profile 管理**
   - ✅ 使用独立的测试 profile
   - ❌ 使用系统 profile（调试端口打不开）

## ⚠️ 常见问题

### Q: 找不到文件名？

**A:** 确保：
1. 媒体选择器已打开
2. 在 Uploads 分类中
3. 文件已上传

### Q: Create 按钮不可点击？

**A:** 检查：
1. Prompt 是否已输入
2. 按钮状态 (aria-disabled)
3. 是否是正确的按钮（带箭头的）

### Q: Chrome 连接失败？

**A:** 确认：
1. Chrome 已启动
2. 使用了 `--remote-debugging-port=9222`
3. 使用了独立的 profile 目录

更多问题见：[故障排除](docs/FLOW_TUTORIAL.md#故障排除)

## 📊 性能

- 总耗时: ~20-30秒
  - Chrome 连接: <1秒
  - 添加参考图: ~10秒
  - 输入 Prompt: ~2秒
  - 提交生成: ~3秒

## 🚧 下一步计划

- [x] 命令行界面 (CLI) ✅
- [x] 配置文件支持 ✅
- [ ] 批量处理
- [ ] 结果自动下载
- [ ] 进度监控
- [ ] 交互式图片选择
- [ ] 支持从文件读取配置

## 📝 版本历史

### v0.1.0 (2026-05-24)

- ✅ CLI 工具
- ✅ 配置管理
- ✅ Chrome 启动/停止
- ✅ 自动添加参考图
- ✅ 自动输入 Prompt
- ✅ 自动提交生成
- ✅ 完整文档

### v1.0.0 (2026-05-24)

- ✅ 基础自动化脚本
- ✅ 参考图添加
- ✅ Prompt 输入
- ✅ 生成提交
- ✅ 完整文档

## 📄 许可

MIT License

## 🙏 致谢

基于 Google Flow 和 Playwright 构建。

---

**环境要求:**
- macOS (tested)
- Chrome 148+
- Python 3.13+
- Playwright

**创建日期:** 2026-05-24
