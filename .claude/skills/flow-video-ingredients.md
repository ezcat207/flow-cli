# Flow 视频生成 Skill - Ingredients 模式

使用参考图 + 动作描述生成视频（区别于 Frames 模式）

## 使用场景

当用户要求使用参考图生成视频时使用，例如：
- "用这张图生成视频，让他们跳舞"
- "基于这个场景生成视频"
- "Luna 和 Wayne 在跳舞的视频"

## 前置条件

1. Chrome 已启动（调试端口 9222）
2. 已登录 Google 账号
3. 已打开 Flow 项目页面
4. 已有可用的图片作为参考

## Ingredients vs Frames 模式

| 特性 | Ingredients 模式 | Frames 模式 |
|------|-----------------|-------------|
| **输入** | 参考图 + 动作描述 | 首帧 + 尾帧 |
| **适用场景** | 单一参考，AI 生成动作 | 明确起止画面 |
| **控制程度** | 较低（AI 发挥） | 较高（定义起止）|
| **脚本** | `flow_video_ingredients.py` | `flow_video_generation.py` |

## 完整流程

### 步骤 1: 确保在 Video 模式

**操作：** 检查是否已在 Video 模式，如果不在则切换

**关键点：**
- 如果能看到 Video 标签页 → 已在 Video 模式，跳过此步
- 如果找不到 Nano Banana 按钮 → 说明已在某个模式下，继续即可

**选择器：**
```python
# 检查是否在 Video 模式
video_tab = page.locator('button[role="tab"]:has-text("Video")')
count = await video_tab.count()

if count > 0:
    # 已在 Video 模式
    pass
else:
    # 需要切换
    nano_btn = page.locator('button:has-text("Nano Banana")').first
    await nano_btn.click()

    video_tab = page.locator('button[role="tab"]:has-text("Video")').first
    await video_tab.click()
```

### 步骤 2: 打开媒体选择器

**操作：** 点击加号按钮

**选择器：**
```python
await page.mouse.click(230, 327)  # 加号按钮坐标
await asyncio.sleep(3)
```

### 步骤 3: 切换到 Images 标签

**操作：** 在媒体选择器中点击 Images 标签

**为什么：** 确保只显示图片，不显示视频等其他媒体

**选择器：**
```python
images_tab = page.locator('button[role="tab"]:has-text("Images")').first
await images_tab.click()
```

### 步骤 4: 选择参考图片

**操作：** 点击目标图片

**🔑 关键发现：** 在 Ingredients 模式下，**点击图片即自动添加到 prompt**，不需要额外点击 "Add to Prompt" 按钮！

**与其他模式的区别：**
- 图片生成（Upload 模式）：需要点击 "Add to Prompt"
- Frames 视频模式：需要点击 "Add to Prompt"
- **Ingredients 视频模式**：点击即添加 ✨

**选择器：**
```python
# 方式1: 使用 role="option"（推荐）
target = page.locator('[role="option"]:has-text("Luna Wayne at West Lake")').first
await target.click()

# 方式2: 直接文本匹配（备选）
target = page.locator('text="Luna Wayne at West Lake"').first
await target.click()
```

### 步骤 5: 输入动作描述

**操作：** 在输入框输入动作描述

**⚠️ 超级重要：必须明确说明每个角色是什么动物！**

**为什么：** Flow 从图片上可能无法准确识别动物种类，必须在 prompt 中明确说明

**正确示例：**
```
✅ "Luna 是一只白色兔子，Wayne 是一只猫，他们在西湖岸边欢快地跳舞"
✅ "兔子 Luna 和猫 Wayne 在跳舞"
```

**错误示例：**
```
❌ "Luna 和 Wayne 在跳舞"  （没说是什么动物）
❌ "他们在跳舞"  （完全没有角色信息）
```

**⚠️ 物种准确性：**
- Luna = 白色兔子 ✅
- Wayne = 猫 ✅（不是狗！）

**选择器：**
```python
input_box = page.locator('[contenteditable="true"]').first
await input_box.click()
await page.keyboard.type(MOTION_PROMPT, delay=30)
```

### 步骤 6: 提交生成

**操作：** 按回车键提交

**选择器：**
```python
await page.keyboard.press('Enter')
```

## 运行脚本

```bash
python3 scripts/flow_video_ingredients.py
```

## 配置说明

在脚本中修改：

```python
# 参考图片名称
REFERENCE_IMAGE = "Luna Wayne at West Lake"

# 动作描述（单行！明确动物种类！）
MOTION_PROMPT = "Luna 是一只白色兔子，Wayne 是一只猫，他们在西湖岸边欢快地跳舞"
```

## 常见问题

### Q: 为什么不需要点击 "Add to Prompt"？

**A:** 这是 Ingredients 模式的特性。在这个模式下，点击图片会立即添加到 prompt 区域，媒体选择器自动关闭。这与其他模式（图片生成、Frames 视频）不同。

### Q: 为什么必须说明动物种类？

**A:** Flow 的 AI 可能无法准确从图片中识别角色是什么动物。如果不明确说明：
- 可能生成错误的动物
- 动作可能不符合该动物的特征
- 视频结果不可预测

### Q: Wayne 是什么动物？

**A:** Wayne 是一只**猫**，不是狗！虽然图片中可能看起来像柯基，但角色设定是猫。

### Q: 找不到 Nano Banana 按钮怎么办？

**A:** 说明已经在某个创建模式下了（可能是 Video 模式）。检查是否能看到 Video 标签页，如果能看到，直接跳过步骤1继续即可。

### Q: 点击图片后没反应？

**A:**
1. 确保点击的是 Images 标签下的内容，不是 Videos
2. 等待 2-3 秒让界面响应
3. 检查是否真的在 Video 模式（不是图片生成模式）

## 故障排查

### 问题：找不到图片

**原因：** 可能在错误的标签页

**解决：**
1. 确认已点击 "Images" 标签
2. 使用搜索功能（如果有）
3. 检查图片名称拼写

### 问题：提交后没有生成

**原因：** Prompt 为空或格式错误

**解决：**
1. 检查输入框是否有内容
2. 确保 prompt 是单行（不能有换行）
3. 验证是否包含动物种类信息

## 成功案例

### 西湖跳舞视频

**配置：**
- 参考图: "Luna Wayne at West Lake"
- Prompt: "Luna 是一只白色兔子，Wayne 是一只猫，他们在西湖岸边欢快地跳舞"

**结果：** ✅ 成功生成

## 关键经验总结

1. **点击即添加** - Ingredients 模式特有，无需 "Add to Prompt" 按钮
2. **明确物种** - 必须在 prompt 中说明每个角色是什么动物
3. **单行 prompt** - 不能有换行
4. **Wayne 是猫** - 不是狗，记住这点
5. **检查模式** - 确保在 Video 模式，不要混淆其他模式

## 参考脚本

完整脚本位置：
```
scripts/flow_video_ingredients.py
```

查看源码了解详细实现。
