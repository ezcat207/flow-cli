# Flow 自动化完整指南

Google Flow 图片和视频自动化生成的完整 Skill 文档

## 目录

1. [快速开始](#快速开始)
2. [核心脚本](#核心脚本)
3. [角色说明](#角色说明)
4. [最佳实践](#最佳实践)
5. [常见问题](#常见问题)
6. [技术细节](#技术细节)

---

## 快速开始

### 前置条件

1. **启动 Chrome**（调试模式）
   ```bash
   ./scripts/start_chrome.sh
   ```

2. **在浏览器中**
   - 登录 Google 账号
   - 打开你的 Flow 项目页面

### 生成图片

```bash
python3 scripts/flow_automation_at_method.py
```

**修改配置：**
```python
CHARACTERS = ["luna", "wayne"]
PROMPT = "Luna 是一只白色兔子，Wayne 是一只猫，他们在北京长城开心地玩耍，中国风格"
```

### 生成视频

```bash
python3 scripts/flow_video_at_method.py
```

**修改配置：**
```python
CHARACTERS = ["luna", "wayne"]
MOTION_PROMPT = "Luna 是一只白色兔子，Wayne 是一只猫，他们在海边奔跑玩耍，日式动漫风格"
```

---

## 核心脚本

### 1. 图片生成 - @ 方式 ⭐ 推荐

**脚本：** `scripts/flow_automation_at_method.py`

**功能：**
- 使用 @ 方式添加 Character 角色
- 输入生成描述
- 自动提交

**特点：**
- ✅ 最稳定的方法
- ✅ 使用语义选择器（`get_by_role`）
- ✅ 不依赖坐标
- ✅ 支持缩放和窗口调整

**流程：**
1. 确保在 Image 模式
2. 输入 `@` 触发角色选择
3. 点击 Characters 标签
4. 选择角色（luna, wayne）
5. 输入 Prompt
6. 提交生成

### 2. 视频生成 - @ 方式 ⭐ 推荐

**脚本：** `scripts/flow_video_at_method.py`

**功能：**
- 在 Video 模式下使用 @ 方式添加角色
- 输入运动描述
- 生成视频

**特点：**
- ✅ 和图片生成同样稳定
- ✅ 无需参考图
- ✅ 直接用角色 + 描述生成

**流程：**
1. 切换到 Video 模式
2. 输入 `@` 触发角色选择
3. 点击 Characters 标签
4. 选择角色
5. 输入运动描述
6. 提交生成

### 3. 下载生成内容

**脚本：** `scripts/download_video.py`

**功能：**
- 下载最新生成的图片/视频
- 保存到 `downloads/` 目录

**使用：**
```bash
# 等待生成完成（图片约 30 秒，视频约 2 分钟）
python3 scripts/download_video.py
```

**下载位置：** `flow-cli/downloads/`

---

## 角色说明

### ⚠️ 重要：必须明确说明角色物种

**Flow 的 AI 无法准确从图片识别角色物种，必须在 Prompt 中明确说明！**

### 角色列表

| 角色名 | 物种 | 描述 |
|--------|------|------|
| **Luna** | 🐰 兔子 | 白色兔子 |
| **Wayne** | 🐱 猫 | 猫（不是狗！） |

### Prompt 模板

**图片生成：**
```
Luna 是一只白色兔子，Wayne 是一只猫，他们在[地点][动作]，[风格]
```

**视频生成：**
```
Luna 是一只白色兔子，Wayne 是一只猫，他们[动作描述]，背景是[场景]，[风格]
```

### 示例

✅ **正确：**
- "Luna 是一只白色兔子，Wayne 是一只猫，他们在大峡谷探险，日式动漫风格"
- "白兔 Luna 和猫 Wayne 在海边奔跑，温暖明亮"

❌ **错误：**
- "Luna 和 Wayne 在玩" （没说是什么动物）
- "他们在大峡谷" （完全没有角色信息）

---

## 最佳实践

### 1. Prompt 编写

**必须遵守：**
- ✅ **单行** - 不能有换行符（`\n`）
- ✅ **明确物种** - 必须说明角色是什么动物
- ✅ **具体场景** - 描述清楚地点和动作
- ✅ **风格指定** - 日式、中国风、写实等

**换行会导致提前提交！**
```python
# ❌ 错误
PROMPT = """Luna 和 Wayne
在大峡谷
玩耍"""

# ✅ 正确
PROMPT = "Luna 是兔子，Wayne 是猫，他们在大峡谷玩耍，日式风格"
```

### 2. 选择器策略

**优先级：**
1. **get_by_role()** - 最推荐
   ```python
   page.get_by_role("button", name="Characters")
   page.get_by_role("option").get_by_text("luna")
   ```

2. **locator() 语义选择器** - 次选
   ```python
   page.locator('button[role="tab"]:has-text("Characters")')
   page.locator('[role="option"]').filter(has_text="luna")
   ```

3. **❌ 坐标点击** - 避免使用
   ```python
   # 不要这样做！
   await page.mouse.click(230, 327)
   ```

**为什么避免坐标？**
- 页面缩放失效
- 窗口大小改变失效
- 页面布局变化失效

### 3. 等待时间

**推荐等待：**
- 输入 `@` 后：2 秒
- 点击标签后：2 秒
- 选择角色后：2-3 秒
- 输入 Prompt 后：5 秒（确保完整输入）
- 提交后：3 秒

### 4. 错误处理

**遇到问题时：**
1. 先按几次 `Escape` 清理对话框
2. 检查是否在正确的模式（Image/Video）
3. 查看截图：`/tmp/*.png`
4. 检查 Prompt 是否单行

---

## 常见问题

### Q1: 为什么必须说明角色物种？

**A:** Flow 的 AI 无法准确识别图片中的角色是什么动物。如果不明确说明：
- Luna 可能被识别为狗、猫或其他动物
- Wayne 可能被识别为狗（实际是猫）
- 生成结果不符合预期

**解决：** 在 Prompt 中明确写 "Luna 是兔子，Wayne 是猫"

### Q2: Wayne 是什么动物？

**A:** Wayne 是**猫**，不是狗！

虽然外观可能像柯基，但角色设定是猫。必须在 Prompt 中说明。

### Q3: 为什么 Prompt 不能换行？

**A:** Flow 的输入框中，每次按 Enter 键都会触发提交。如果 Prompt 有多行：
- 第一行提交生成
- 第二行提交生成
- 第三行提交生成
- 结果生成了多个不完整的内容

**解决：** 使用单行，用逗号分隔。

### Q4: 坐标方式为什么不稳定？

**A:** 坐标点击依赖固定的像素位置：
- 用户缩放页面（Ctrl +/-）→ 坐标错位
- 窗口大小改变 → 坐标错位
- Flow 更新界面布局 → 坐标错位

**解决：** 使用 `get_by_role()` 等语义选择器。

### Q5: 如何检查当前在什么模式？

**方法 1：** 查找特定按钮
```python
# Image 模式：有 Nano Banana 按钮
nano_btn = page.get_by_role("button", name=re.compile("Nano Banana"))

# Video 模式：有 Video 标签
video_tab = page.locator('button[role="tab"]:has-text("Video")')
```

**方法 2：** 尝试操作，失败则切换模式

### Q6: 生成完成后如何下载？

**图片：** 约 30 秒生成完成
**视频：** 约 2 分钟生成完成

**下载：**
```bash
python3 scripts/download_video.py
```

文件保存在 `flow-cli/downloads/`

---

## 技术细节

### 工作原理

1. **连接方式：** CDP (Chrome DevTools Protocol)
2. **浏览器：** 系统 Chrome + 独立 profile
3. **自动化：** Playwright (Python)
4. **端口：** 9222

### 关键坐标（已弃用）

~~`(230, 327)` - 加号按钮（不再使用）~~

### 关键选择器

**@ 方式添加角色：**
```python
# 输入框
input_box = page.locator('[contenteditable="true"]').first

# Characters 标签（必须点击）
characters_tab = page.get_by_role("tab", name=re.compile("Characters"))

# 角色选项
character = page.get_by_role("option").get_by_text("luna")

# Add to Prompt 按钮
add_btn = page.locator('button:has-text("Add to Prompt")').first

# 提交按钮（按回车更可靠）
await page.keyboard.press('Enter')
```

### 两种模式对比

| 模式 | 入口 | 适用 | 稳定性 |
|------|------|------|--------|
| **@ 方式** | 输入 `@` | 图片 + 视频 | ⭐⭐⭐⭐⭐ |
| 加号方式 | 坐标点击 | 仅图片 | ⭐⭐（已弃用）|

### 已知限制

1. **第二个角色自动添加** - 不需要点 "Add to Prompt"
2. **必须先点 Characters 标签** - 否则会在 All Media 中选错
3. **必须单行 Prompt** - 换行会提前提交
4. **必须明确物种** - AI 无法准确识别

### Chrome Profile

**位置：** `/tmp/flow_chrome_debug`

**为什么独立 profile？**
- 系统 Chrome 无法同时开启调试端口
- 登录状态保持在独立 profile 中
- 避免干扰日常浏览

---

## 更新日志

### 2024-05-24 - 完全移除坐标方式
- ✅ 创建新的图片和视频生成脚本（@ 方式）
- ✅ 使用 `get_by_role()` 语义选择器
- ✅ 归档旧的坐标方式脚本
- ✅ 创建完整 Skill 文档
- 📝 强调必须说明角色物种

### 2024-05-24 - Ingredients 视频完成
- ✅ 完成 Ingredients 模式（参考图方式）
- 🔑 发现：点击图片自动添加，无需按钮

### 2024-05-24 - Frames 视频完成
- ✅ 完成 Frames 模式（首尾帧方式）
- 🔑 发现：必须先进入 Video Frames 模式

---

## 分享给其他 AI

这个 Skill 文档可以分享给其他 AI 助手使用。关键要点：

1. **使用 `get_by_role()`** - 不要用坐标
2. **@ 方式添加角色** - 输入 `@` 触发选择器
3. **必须说明物种** - "Luna 是兔子，Wayne 是猫"
4. **单行 Prompt** - 不能有换行
5. **等待充分** - 每步操作后等待 2-5 秒

**测试方法：**
```bash
# 1. 启动 Chrome
./scripts/start_chrome.sh

# 2. 生成图片
python3 scripts/flow_automation_at_method.py

# 3. 生成视频
python3 scripts/flow_video_at_method.py
```

---

**维护者：** Claude + User
**最后更新：** 2024-05-24
**文档版本：** 2.0
