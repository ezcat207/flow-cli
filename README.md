# Flow CLI - Google Flow 自动化工具

自动化 Google Flow 图片生成的命令行工具。

## 🎯 功能

- ✅ 自动添加参考图到 Prompt
- ✅ 自动输入生成描述
- ✅ 自动提交生成请求
- ✅ 支持自定义配置
- ✅ 完整的错误处理

## 📦 安装

```bash
# 克隆仓库
git clone <repository-url>
cd flow-cli

# 安装依赖
pip install playwright
playwright install chromium
```

## 🚀 快速开始

### 1. 启动 Chrome

```bash
./scripts/start_chrome.sh
```

### 2. 登录并打开项目

在打开的 Chrome 中：
1. 登录 Google 账号
2. 访问你的 Flow 项目页面

### 3. 运行自动化

```bash
python3 scripts/flow_automation_final.py
```

## 📚 文档

- [完整教程](docs/FLOW_TUTORIAL.md) - 详细的操作教程
- [技能文档](docs/FLOW_SKILL.md) - 界面元素和选项详解
- [总结文档](docs/FLOW_AUTOMATION_SUMMARY.md) - 完整总结和经验

## ⚙️ 配置

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
├── docs/                  # 文档目录
│   ├── FLOW_TUTORIAL.md   # 完整教程
│   ├── FLOW_SKILL.md      # 技能文档
│   └── FLOW_AUTOMATION_SUMMARY.md  # 总结文档
├── scripts/               # 脚本目录
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

- [ ] 命令行界面 (CLI)
- [ ] 批量处理
- [ ] 结果自动下载
- [ ] 进度监控
- [ ] 配置文件支持

## 📝 版本历史

### v1.0.0 (2026-05-24)

- ✅ 基础自动化功能
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
