# Flow Automation Skill

**自动化 Google Flow 图片和视频生成**

通过 Playwright 浏览器自动化实现 Google Flow 的完整操作流程。

## 功能

- ✅ 创建新项目
- ✅ 自动生成图片（Imagen 4, Nano Banana 2/Pro）
- ✅ 自动生成视频（Veo）
- ✅ 配置生成参数（宽高比、数量、模型）
- ✅ 等待并检测生成结果

## 为什么需要浏览器自动化？

Flow **没有公开 API**，所有操作都需要通过浏览器界面完成，并且需要：
- OAuth 认证
- reCAPTCHA 验证
- 项目会话管理

因此必须使用 **Playwright 浏览器自动化**，无法直接调用 HTTP API。

## ⚠️ 重要：添加多个参考图的正确流程

**每个参考图都必须分别添加，不能在一次 Media 库打开中添加多个！**

正确流程：
```
第一个参考图：
1. 打开 Media 库
2. 点击 Uploads 标签
3. 点击选中第一张图片
4. 点击 "Add to Prompt"
5. 关闭 Media 库（按 Escape）

第二个参考图：
1. 重新打开 Media 库
2. 点击 Uploads 标签
3. 点击选中第二张图片
4. 点击 "Add to Prompt"
5. 关闭 Media 库（按 Escape）
```

**错误做法**：在一次 Media 库打开中尝试添加多个图片 ❌

## 使用方法

### 1. 生成图片

```python
from flow_automation import FlowAutomation

async def generate_image():
    flow = FlowAutomation()

    # 启动浏览器并登录（使用已保存的会话）
    await flow.start()

    # 创建新项目
    project_id = await flow.create_project()

    # 生成图片
    images = await flow.generate_image(
        prompt="A cute orange kitten playing with yarn",
        model="banana2",  # 或 "imagen4", "banana-pro"
        aspect_ratio="16:9",  # 或 "1:1", "4:3", "9:16", "3:4"
        count=2  # 生成2张
    )

    print(f"生成了 {len(images)} 张图片")

    await flow.close()
```

### 2. 生成视频

```python
async def generate_video():
    flow = FlowAutomation()
    await flow.start()

    project_id = await flow.create_project()

    # 生成视频
    videos = await flow.generate_video(
        prompt="A drone shot flying over a futuristic city at sunset",
        duration=5,  # 秒
        aspect_ratio="16:9"
    )

    print(f"生成了 {len(videos)} 个视频")

    await flow.close()
```

### 3. CLI 命令

```bash
# 生成图片
python flow_automation.py image "A cute cat" --model banana2 --ratio 16:9 --count 2

# 生成视频
python flow_automation.py video "Drone shot of city" --duration 5

# 使用已有项目
python flow_automation.py image "A cat" --project-id abc-123-def
```

## 关键选择器（Key Selectors）

通过实际测试确认的精确选择器：

### 1. New Project 按钮
```python
'button:has-text("New project")'
```

### 2. 输入框容器
```python
'#__next > div > div:nth-of-type(5) > div > div > div > div'
```

### 3. 可编辑输入框
```python
'[contenteditable="true"]'
```

### 4. Create 按钮（关键！）
```python
'#__next > div > div:nth-of-type(5) > div > div > div > div > div:nth-of-type(2) > div:nth-of-type(2) > button:nth-of-type(2)'
```
**注意**：这个是真正触发生成的按钮，`aria-disabled` 必须是 `"false"` 才能点击。

### 5. 配置菜单按钮
```python
'button:has-text("Nano Banana")'  # 或 'button:has-text("Video")'
```

### 6. Image/Video 类型选择
```python
'button:has-text("Image")'  # 图片
'button:has-text("Video")'  # 视频
```

### 7. 生成的图片
```python
'img[alt="Generated image"]'
```

## 完整流程

### 图片生成流程

```
1. 导航到 Flow 主页
   → https://labs.google/fx/tools/flow

2. 点击 "New project" 按钮
   → 进入新项目页面，获取 project_id

3. （可选）配置生成选项
   → 点击 "Nano Banana 2" 按钮
   → 选择 "Image"
   → 选择宽高比（16:9, 1:1, etc.）
   → 选择生成数量（1x, x2, x3, x4）

4. 定位输入框容器并点击
   → 使用选择器定位输入区域
   → 点击激活

5. 在可编辑元素中输入 prompt
   → 找到 [contenteditable="true"] 元素
   → 使用 .fill() 输入文本

6. 点击 Create 按钮
   → 使用精确选择器
   → 确保 aria-disabled="false"
   → 点击触发生成

7. 等待生成完成
   → 等待 1-2 分钟
   → 检测 img[alt="Generated image"] 出现

8. 提取结果
   → 获取图片 src URL
   → 下载或返回结果
```

### 视频生成流程

```
1-2. 同图片流程

3. 配置为视频模式
   → 点击配置按钮
   → 选择 "Video"
   → 选择宽高比

4-6. 输入 prompt 并生成（同图片）

7. 等待视频生成
   → 视频生成时间更长（3-5 分钟）
   → 检测视频元素出现

8. 提取视频结果
```

## 技术要点

### 1. 浏览器会话持久化

使用 `launch_persistent_context` 保存登录状态：

```python
context = await p.chromium.launch_persistent_context(
    '/tmp/flow_browser_profile',  # 会话保存目录
    headless=False,
    args=['--start-maximized']
)
```

### 2. 等待策略

```python
# 等待网络空闲
await page.wait_for_load_state('networkidle')

# 等待元素可见
await element.is_visible(timeout=5000)

# 固定延时（给 UI 渲染时间）
await asyncio.sleep(2)
```

### 3. 元素定位优先级

```python
# 1. 精确 CSS 选择器（最可靠）
page.locator('#__next > div > ...')

# 2. 文本匹配
page.locator('button:has-text("Create")')

# 3. 属性匹配
page.locator('[contenteditable="true"]')

# 4. 容器内查找
container.locator('textarea').first
```

### 4. 错误处理

```python
try:
    element = page.locator('button').first
    if await element.is_visible(timeout=5000):
        await element.click()
except Exception as e:
    # 截图调试
    await page.screenshot(path='/tmp/error.png')
    raise
```

## 已知限制

1. **需要用户首次登录**：第一次使用需要手动在浏览器中登录 Google 账号
2. **会话过期**：登录会话可能过期，需要重新登录
3. **生成时间不固定**：图片 30-120 秒，视频 3-5 分钟
4. **选择器可能变化**：Google 更新 UI 后选择器可能失效
5. **无法并发**：同一个浏览器配置只能运行一个实例

## 调试技巧

### 1. 截图调试
```python
await page.screenshot(path='/tmp/debug.png', full_page=True)
```

### 2. 慢速执行
```python
context = await p.chromium.launch_persistent_context(
    user_data_dir,
    slow_mo=1000  # 每步操作延迟 1 秒
)
```

### 3. 打印元素信息
```python
elements = page.locator('button')
count = await elements.count()
for i in range(count):
    el = elements.nth(i)
    text = await el.inner_text()
    visible = await el.is_visible()
    print(f"Button {i}: {text}, visible={visible}")
```

### 4. 获取页面 HTML
```python
content = await page.content()
print(content[:1000])
```

## 示例项目

参考 `/Volumes/Lexar/oneweekoneproject/001cli/flow-cli/` 中的完整实现。

## 相关资源

- [Playwright 文档](https://playwright.dev/python/)
- [flow-proxy](https://github.com/liorium/flow-proxy) - 参考实现
- [Google Flow](https://labs.google/fx/tools/flow)
