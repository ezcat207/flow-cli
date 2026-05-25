# Flow 视频生成 Skill

自动化 Google Flow 视频生成的完整流程。

## 使用场景

当用户要求生成视频时使用，例如：
- "生成一个 Luna 和 Wayne 在西湖划船的视频"
- "用这两张图片生成视频"
- "创建视频，首帧是岸边，尾帧是跳船"

## 前置条件

1. Chrome 已启动（调试端口 9222）
2. 已登录 Google 账号
3. 已打开 Flow 项目页面
4. 已有可用的图片作为首尾帧

## 完整流程（必须按顺序）

### 为什么顺序很重要？

**必须严格按照以下顺序操作，否则会失败：**

1. **先进入 Video Frames 模式** → 界面才会正确初始化
2. **先选择首尾帧** → 再添加角色，否则界面状态会混乱
3. **角色在 prompt 之前** → 这是 Flow 的 UI 设计要求
4. **Prompt 必须单行** → 换行会触发提前提交

### 步骤 1: 打开 Nano Banana

**操作：** 点击右下角的 "Nano Banana 2" 按钮

**为什么：** 这是打开创建界面的唯一入口

**选择器：**
```python
nano_btn = page.locator('button:has-text("Nano Banana")').first
```

### 步骤 2: 切换到 Video 模式

**操作：** 点击 "Video" 标签

**为什么：** 必须先切换到 Video，才能看到 Frames 选项

**选择器：**
```python
video_tab = page.locator('button[role="tab"]:has-text("Video")').first
```

### 步骤 3: 切换到 Frames 模式

**操作：** 点击 "Frames" 标签

**为什么：** Frames 模式才能选择首尾帧生成视频

**选择器：**
```python
frames_tab = page.locator('button[role="tab"]:has-text("Frames")').first
```

**与 Ingredients 的区别：**
- Frames: 使用首尾帧生成视频（推荐）
- Ingredients: 使用其他参考素材

### 步骤 4: 选择 Start 帧（首帧）

**操作：**
1. 点击 "Start" 按钮
2. 在图片列表中选择首帧图片
3. 点击 "Add to Prompt"（或自动添加）

**为什么：** 首帧定义视频的开始画面

**选择器：**
```python
start_btn = page.locator('text=Start').first
image = page.locator('text="图片名称"').nth(索引)
add_btn = page.locator('button:has-text("Add to Prompt")').first
```

### 步骤 5: 选择 End 帧（尾帧）

**操作：**
1. 点击 "End" 按钮
2. 在图片列表中选择尾帧图片
3. 按 Escape 关闭对话框

**为什么：** 尾帧定义视频的结束画面

**选择器：**
```python
end_btn = page.locator('text=End').first
option = page.locator('[role="option"]').nth(索引)
```

### 步骤 6: @ 添加角色

**操作：**
1. 在输入框输入 `@`
2. 点击 "Characters" 标签
3. 选择角色（luna, wayne）
4. 第一个角色点击 "Add to Prompt"
5. 第二个角色自动添加

**为什么必须在 prompt 之前：**
- Flow 的 UI 设计要求角色必须先添加
- 角色信息需要先初始化才能正确处理 prompt

**为什么用 @ 方式（Character 模式）：**
- Character 模式包含**声音 + 外观 + 个性**
- 视频生成需要声音数据
- Upload 模式（加号）只有外观，不适合视频

**选择器：**
```python
# 输入 @
page.keyboard.type('@')

# 点击 Characters 标签
characters_tab = page.locator('button[role="tab"]:has-text("Characters")').first

# 选择角色
character_option = page.locator('[role="option"]').filter(has_text="luna").first

# 点击 Add to Prompt（仅第一个角色）
add_btn = page.locator('button:has-text("Add to Prompt")').first
```

### 步骤 7: 输入运动描述 Prompt

**操作：**
1. 在输入框输入运动描述（**单行，无换行！**）
2. 等待 5 秒确保输入完成
3. 验证内容
4. 再等待 3 秒作为最后确认

**⚠️ 为什么必须单行：**
- **换行键会触发提前提交！**
- 每次按 Enter，Flow 会立即提交当前内容
- 导致生成大量不完整的"废片"
- 最终只有最后一行被正确生成

**为什么要等待 5+3 秒：**
- `keyboard.type()` 是异步的，需要时间完成
- 等待 5 秒确保所有字符都输入完成
- 再等待 3 秒作为双重保险
- 这是从多次失败中总结的经验

**正确格式：**
```python
# ✅ 正确 - 单行
PROMPT = "Luna 和 Wayne 从岸边走向船，跳上船，船摇晃，镜头跟随，背景稳定"

# ❌ 错误 - 多行会提前提交
PROMPT = """Luna 和 Wayne 从岸边走向船
跳上船
船摇晃"""
```

**输入代码：**
```python
await page.keyboard.type(PROMPT, delay=20)  # 每字符延迟 20ms
await asyncio.sleep(5)  # 等待输入完成
# 验证
input_text = await input_box.inner_text()
await asyncio.sleep(3)  # 最后确认
```

### 步骤 8: 提交生成

**操作：** 点击带箭头的 Create 按钮

**选择器：**
```python
create_btn = page.locator('button:has(i:text("arrow_forward"))').first
```

## 运行脚本

```bash
python3 scripts/flow_video_generation.py
```

## 配置说明

在脚本中修改以下配置：

```python
# 首尾帧选择
START_FRAME_KEYWORD = "Luna Wayne at West Lake"  # 岸边场景
START_FRAME_INDEX = 1  # 选择第几个（0-based）

END_FRAME_KEYWORD = "Luna Wayne jumping"  # 跳船场景
END_FRAME_INDEX = 0  # 选择第几个（0-based）

# 角色
CHARACTERS = ["luna", "wayne"]

# 运动描述（单行！）
MOTION_PROMPT = "你的描述，用逗号分隔，不要换行"
```

## 常见问题

### Q: 为什么必须先切换到 Video Frames 再添加角色？

**A:** 因为 Flow 的界面初始化顺序要求如此。如果先添加角色再切换模式，界面状态会混乱，导致后续操作失败。

### Q: 为什么 Prompt 不能有换行？

**A:** 换行键在 Flow 的输入框中会触发提交动作。每次换行都会提交当前内容，导致：
- 生成多个不完整的图片/视频
- 只有最后一行能正确生成
- 浪费配额和时间

### Q: 为什么要等待 5+3 秒？

**A:** `keyboard.type()` 是异步的，输入需要时间：
- 100 个字符 × 20ms/字符 = 2000ms
- 加上网络延迟和界面渲染
- 5 秒是安全的等待时间
- 3 秒是额外保险

### Q: 第二个角色为什么自动添加？

**A:** Flow 的 UI 设计：
- 第一个角色需要点击 "Add to Prompt"
- 之后的角色选择后自动添加
- 不需要再点击按钮

### Q: Character 和 Upload 有什么区别？

**A:**
- **Character (@方式)**: 包含声音+外观+个性，适合视频
- **Upload (加号方式)**: 只有图片外观，适合图片生成

## 故障排查

### 问题：找不到 Frames 按钮

**原因：** 没有先点击 Nano Banana 或没有切换到 Video 模式

**解决：** 严格按照顺序：Nano Banana → Video → Frames

### 问题：生成了很多废片

**原因：** Prompt 有换行

**解决：**
1. 检查 prompt 字符串是否包含 `\n`
2. 改用单行格式，用逗号分隔
3. 确保没有使用三引号字符串 `"""`

### 问题：第二个角色添加失败

**原因：** 尝试点击 "Add to Prompt" 但按钮已消失

**解决：** 第二个角色选择后直接等待，不要点击按钮

### 问题：提交按钮被禁用

**原因：** 上一个生成还在进行中

**解决：** 等待上一个生成完成，或刷新页面重新开始

## 成功案例

### 西湖划船视频

**配置：**
- Start: Luna Wayne at West Lake (岸边场景)
- End: Luna Wayne jumping onto boat (跳船场景)
- Characters: luna, wayne
- Prompt: "Luna 和 Wayne 从西湖岸边走向游船，轻快地跳上船，船在湖面轻轻摇晃，镜头平滑跟随他们的动作从岸边推进到船上，背景西湖美景和远山保持稳定，日式平面风格明亮温暖"

**结果：** ✅ 成功生成 8 秒视频

## 关键经验总结

1. **顺序不能变** - Nano Banana → Video → Frames → Start → End → Characters → Prompt
2. **绝对禁止换行** - Prompt 必须单行
3. **等待很重要** - 输入后等 5+3 秒
4. **用 Character 模式** - 视频需要声音数据
5. **第二个角色自动加** - 不要手动点击

## 参考脚本

完整脚本位置：
```
scripts/flow_video_generation.py
```

查看源码了解详细实现。
