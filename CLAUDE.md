# Flow CLI - 项目记忆文档

## 项目概述

Flow CLI 是一个用于自动化 Google Flow 图片生成的工具。当前以**脚本方式**为主，CLI 工具尚在开发中。

**当前状态：**
- ✅ 脚本方式：稳定可用（推荐）
- 🚧 CLI 方式：开发中，存在已知问题

## 快速开始（推荐方式）

### 1. 启动 Chrome

```bash
./scripts/start_chrome.sh
```

### 2. 在 Chrome 中
1. 登录 Google 账号
2. 访问你的 Flow 项目页面

### 3. 运行脚本

```bash
python3 scripts/flow_automation_final.py
```

**就这么简单！** 脚本会自动：
- 添加参考图（Luna_on_mars.png, Wayne_on_earth.png）
- 输入生成描述
- 提交生成请求

## 项目结构

```
flow-cli/
├── CLAUDE.md              ← 你在这里（项目记忆）
├── README.md              ← 项目说明
├── CLI_USAGE.md           ← CLI 使用指南（未完善）
├── INSTALL.md             ← 安装说明
│
├── scripts/               ← ⭐ 主要工作方式
│   ├── start_chrome.sh    ← Chrome 启动脚本
│   ├── flow_automation_at_method.py  ← @ 方式脚本（最新，推荐）⭐
│   └── flow_automation_final.py  ← 加号方式脚本（原始方法）
│
├── flow_cli/              ← 🚧 CLI 工具（开发中）
│   ├── cli.py             ← CLI 入口
│   ├── automation.py      ← 自动化逻辑
│   ├── config.py          ← 配置管理
│   └── chrome.py          ← Chrome 管理
│
├── docs/                  ← 📚 文档
│   ├── FLOW_TUTORIAL.md   ← 完整教程
│   ├── FLOW_SKILL.md      ← 界面元素和操作详解 ⭐
│   ├── FLOW_AUTOMATION_SUMMARY.md  ← 总结
│   └── CLI_ARCHITECTURE.md  ← CLI 架构（未来）
│
└── archive/               ← 失败尝试的记录
    ├── README.md          ← 失败原因分析
    └── [旧脚本...]
```

## 核心文件说明

### 1. 脚本方式（当前主要使用）

#### `scripts/flow_automation_at_method.py` ⭐ 最新推荐
- **功能：** 使用 @ 方式添加角色
- **方法：** 在输入框输入 `@角色名` 选择角色
- **配置：** 修改脚本头部的配置
  ```python
  PROJECT_URL = "你的项目URL"
  CHARACTERS = ["luna", "wayne"]  # 角色名称列表
  PROMPT = "生成描述"
  ```
- **运行：** `python3 scripts/flow_automation_at_method.py`
- **状态：** ✅ 稳定，**推荐使用**
- **优势：**
  - 更简单：不需要点击加号按钮
  - 更稳定：不会出现添加第二张图失败的问题
  - 支持搜索：可以快速找到角色

#### `scripts/flow_automation_final.py` (原始方法)
- **功能：** 使用加号按钮打开媒体选择器
- **方法：** 点击坐标 (230, 327) 打开媒体选择器
- **配置：** 修改脚本头部的配置
  ```python
  PROJECT_URL = "你的项目URL"
  REFERENCE_IMAGES = ["图片1.png", "图片2.png"]
  PROMPT = "生成描述"
  ```
- **运行：** `python3 scripts/flow_automation_final.py`
- **状态：** ⚠️ 存在问题：添加第二张图时可能失败
- **建议：** 使用新的 @ 方式脚本

#### `scripts/start_chrome.sh`
- **功能：** 启动 Chrome（调试模式）
- **运行：** `./scripts/start_chrome.sh`
- **参数：**
  - 端口：9222
  - Profile：/tmp/flow_chrome_debug

### 2. CLI 方式（开发中）

#### `flow_cli/` 包
- **状态：** 🚧 未完成，存在已知问题
- **问题：** 添加第二张参考图时会失败
- **待修复：** 添加图片的逻辑需要调整

#### 已知问题
```
问题：添加参考图失败
现象：第一张图片成功，第二张失败
原因：界面状态切换导致选择器失效
影响：CLI 命令 `flow generate` 无法正常工作
```

### 3. 文档（技能知识库）

#### `docs/FLOW_SKILL.md` ⭐ 重要
- **内容：** Flow 界面的所有元素和操作
- **包括：**
  - 按钮位置和功能
  - 选择器策略
  - 操作流程
  - 常见问题
- **用途：** 作为操作参考和问题排查指南

#### `docs/FLOW_TUTORIAL.md`
- **内容：** 完整的操作教程
- **适合：** 第一次使用的人

#### `archive/README.md`
- **内容：** 7 种失败尝试的记录
- **价值：** 避免重复犯错

## 当前工作流程

### 方式一：脚本方式（推荐）

#### 方式 1A：@ 方式（最新，推荐） ⭐

```bash
# 1. 启动 Chrome
./scripts/start_chrome.sh

# 2. 在 Chrome 中登录并打开项目

# 3. 编辑配置（可选）
# 修改 scripts/flow_automation_at_method.py 中的：
#   - PROJECT_URL
#   - CHARACTERS = ["luna", "wayne"]
#   - PROMPT

# 4. 运行
python3 scripts/flow_automation_at_method.py
```

**优势：**
- ✅ 更简单：直接 @角色名
- ✅ 更稳定：不需要处理媒体选择器
- ✅ 支持搜索：可以快速找到角色

#### 方式 1B：加号方式（原始方法）

```bash
# 运行原始脚本
python3 scripts/flow_automation_final.py
```

**问题：** 添加第二张参考图时可能失败

### 方式二：CLI 方式（未完成，不推荐）

```bash
# 安装
pip install -e .

# 配置
flow config --set-project URL

# 启动 Chrome
flow start-chrome

# 生成（会失败）
flow generate -i img1.png -i img2.png -p "prompt"
```

**注意：** CLI 方式目前有 bug，请使用脚本方式。

## 技术细节

### 工作原理

1. **连接方式：** CDP (Chrome DevTools Protocol)
2. **浏览器：** 系统 Chrome + 独立 profile
3. **自动化：** Playwright (Python)
4. **页面定位：**
   - 坐标点击：加号按钮 (230, 327)
   - 文本选择器：文件名、按钮文本
   - 图标选择器：`button:has(i:text("arrow_forward"))`

### 关键坐标

```python
加号按钮（打开媒体选择器）: (230, 327)
```

### 关键选择器

#### @ 方式（推荐）
```python
输入框: page.locator('[contenteditable="true"]').first
角色选项: page.locator('[role="option"]').filter(has_text="角色名").first
Create 按钮: page.locator('button:has(i:text("arrow_forward"))').first
```

#### 加号方式（原始）
```python
加号按钮坐标: (230, 327)
文件名: page.locator('text=/文件名/i').first
Add to Prompt 按钮: page.locator('button:has-text("Add to Prompt")').first
Create 按钮: page.locator('button:has(i:text("arrow_forward"))').first
输入框: page.locator('[contenteditable="true"]').first
```

## 已知问题和限制

### 问题 1：CLI 添加第二张图失败

**现象：**
```
✅ 第一张图片添加成功
❌ 第二张图片选择成功，但点击 "Add to Prompt" 失败
✅ 但最终两个角色都在对话框中（结果正确）
```

**原因：**
- 添加第一张图后，界面自动切换
- "Add to Prompt" 按钮消失或位置改变
- 需要调整添加逻辑

**临时解决方案：**
- 使用脚本方式
- 手动在 Chrome 中添加图片

### 问题 2：页面定位不稳定

**现象：**
- 有时找不到文件名
- 有时找不到按钮

**原因：**
- Flow 界面可能有多个视图
- 需要确保在正确的页面

**解决方案：**
- 确保访问正确的项目 URL
- 等待页面加载完成
- 使用更稳定的选择器

## 成功案例

### 最近成功生成

#### 使用 @ 方式（2026-05-24）⭐
**角色：** luna, wayne
**Prompt：** "在东京迪士尼乐园玩耍，温馨欢乐，日式卡通风格"
**结果：** ✅ 完全自动化成功！

**方法：**
1. 运行 `python3 scripts/flow_automation_at_method.py`
2. 脚本自动完成所有步骤
3. 生成成功！

#### 使用加号方式（2026-05-24）
**参考图：** Luna_on_mars.png, Wayne_on_earth.png
**Prompt：** "他们两个在上海玩，四格漫画，日式平面风格，温馨欢乐的氛围"
**结果：** ⚠️ 部分自动化

**方法：**
1. 运行脚本添加第一张图
2. 脚本在第二张图时报错
3. 手动继续：输入 Prompt + 点击生成
4. 成功！

## 下一步计划

### 短期（1-2 天）

1. **修复 CLI 添加图片逻辑**
   - 调查正确的添加流程
   - 处理界面状态切换
   - 添加重试机制

2. **改进脚本**
   - 添加错误恢复
   - 支持批量生成
   - 添加进度显示

### 中期（1 周）

1. **完善 CLI**
   - 修复所有已知问题
   - 添加测试
   - 完善文档

2. **增强功能**
   - 支持更多图片
   - 自动下载结果
   - 配置文件支持

### 长期（1 月）

1. **稳定性**
   - 处理各种边缘情况
   - 添加完整的错误处理
   - 性能优化

2. **易用性**
   - 交互式配置
   - 更好的进度反馈
   - Shell 自动补全

## 重要提醒

### ⚠️ 使用前必读

1. **Chrome Profile 隔离**
   - 必须使用独立 profile（`/tmp/flow_chrome_debug`）
   - 不能使用系统 Chrome profile
   - 原因：调试端口冲突

2. **登录要求**
   - 需要在 Chrome 中登录 Google 账号
   - 需要访问 Flow 项目页面
   - 脚本不会自动登录

3. **文件上传**
   - 参考图必须先上传到 Flow 的 Uploads
   - 脚本只是选择已有文件，不会上传
   - 文件名必须完全匹配（区分大小写）

4. **调试端口**
   - 默认端口：9222
   - 如果被占用，需要修改
   - 检查：`lsof -i :9222`

### ✅ 最佳实践

1. **每次使用前**
   ```bash
   # 检查 Chrome 是否运行
   lsof -i :9222

   # 如果需要，重启 Chrome
   killall "Google Chrome"
   ./scripts/start_chrome.sh
   ```

2. **修改配置时**
   - 直接编辑 `scripts/flow_automation_final.py`
   - 不需要重启 Chrome
   - 不需要重新登录

3. **出错时**
   - 查看截图：`/tmp/*.png`
   - 检查 Chrome 是否在正确页面
   - 尝试手动操作确认流程

## 故障排查

### Chrome 连接失败

```bash
# 检查端口
lsof -i :9222

# 重启 Chrome
killall "Google Chrome"
./scripts/start_chrome.sh
```

### 找不到文件

1. 确认文件已上传到 Flow
2. 检查文件名是否完全匹配
3. 查看截图确认当前页面

### 按钮点击失败

1. 检查是否在正确页面
2. 等待时间是否足够
3. 尝试增加 `await asyncio.sleep()` 时间

## 参考资料

- **FLOW_TUTORIAL.md** - 完整教程
- **FLOW_SKILL.md** - 界面元素参考 ⭐
- **archive/README.md** - 失败案例学习
- **CLI_ARCHITECTURE.md** - CLI 设计文档

## 联系和支持

- **问题反馈：** GitHub Issues
- **文档更新：** 直接编辑此文件
- **最后更新：** 2026-05-24

---

## 更新日志

### 2026-05-24 晚上
- ✅ 发现并实现 @ 方式添加角色
- ✅ 创建 flow_automation_at_method.py
- ✅ 完全自动化成功
- ✅ 更新文档

### 2026-05-24 下午
- ✅ 创建项目
- ✅ 脚本方式基本可用
- ✅ 完整文档
- 🚧 CLI 开发中
- ❌ CLI 存在添加图片 bug

### 待办事项
- [x] 找到更好的添加角色方式 ✅ @ 方式
- [ ] 将 @ 方式集成到 CLI
- [ ] 添加自动化测试
- [ ] 完善错误处理
- [ ] 支持批量生成
- [ ] 结果自动下载

---

**记住：**
- 当前使用**脚本方式**最稳定
- CLI 还在开发中，不推荐生产使用
- 遇到问题查看 `docs/FLOW_SKILL.md`
- 失败案例在 `archive/README.md`
