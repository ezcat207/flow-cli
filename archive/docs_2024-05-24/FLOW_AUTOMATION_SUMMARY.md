# Flow 自动化完整总结

## 🎯 最终成功的工作流程

### 前置准备

```bash
# 1. 启动 Chrome 带调试端口
/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome \
  --remote-debugging-port=9222 \
  --user-data-dir="/tmp/flow_chrome_debug" &

# 2. 在浏览器中登录 Google 账号

# 3. 打开 Flow 项目页面
# https://labs.google/fx/tools/flow/project/{PROJECT_ID}
```

### 操作步骤

1. **添加第一张参考图 (Luna_on_mars.png)**
   - 点击输入框旁的加号按钮（坐标约 230, 327）
   - 在左侧文件列表中点击 "Luna_on_mars.png"
   - 点击底部的 "Add to Prompt" 按钮

2. **添加第二张参考图 (Wayne_on_earth.png)**
   - 再次点击加号按钮打开媒体选择器
   - 在左侧文件列表中点击 "Wayne_on_earth.png"
   - 点击底部的 "Add to Prompt" 按钮

3. **输入生成 Prompt**
   - 在输入框中输入: "他们在中国杭州玩"
   - （此 prompt 可以随时修改）

4. **提交生成**
   - 点击右下角带箭头的 Create 按钮
   - 系统开始生成图片（显示进度百分比）

## 📝 关键发现

### 成功的要点

1. ✅ **Chrome Profile 重用**
   - 使用独立的 profile 目录: `/tmp/flow_chrome_debug`
   - 登录状态会保存，下次无需重新登录

2. ✅ **正确的加号按钮**
   - **不是**顶部的 "Add Media" 按钮
   - **是**输入框旁边的加号按钮（约坐标 230, 327）
   - 点击后会打开文件列表选择器

3. ✅ **文件选择方式**
   - 左侧显示文件名列表（不是卡片视图）
   - 直接点击文件名进行选择
   - 底部有大的 "Add to Prompt" 按钮

4. ✅ **必须分两次添加**
   - 每次只能添加一张参考图
   - 添加后媒体选择器自动关闭
   - 需要再次点击加号添加下一张

5. ✅ **正确的提交按钮**
   - 带 `arrow_forward` 图标的 Create 按钮
   - 位于输入框右下角区域

### 错误的尝试（避免）

1. ❌ 点击顶部的 "Add Media" 按钮
   - 那是用来创建/上传新媒体的
   - 不是添加参考图的入口

2. ❌ 使用系统 Chrome Profile
   - 系统 profile 启动时调试端口无法打开
   - 必须使用独立的测试 profile

3. ❌ 使用复杂的 CSS 选择器
   - 页面结构可能变化
   - 文本选择器和坐标点击更稳定

4. ❌ 假设可以批量添加
   - 界面不支持多选
   - 必须逐个添加

## 🔧 技术细节

### CDP 连接

```python
from playwright.async_api import async_playwright

async with async_playwright() as p:
    browser = await p.chromium.connect_over_cdp("http://127.0.0.1:9222")
    context = browser.contexts[0]
    page = context.pages[0]  # 或通过 URL 筛选
```

### 文件选择器定位

```python
# 打开媒体选择器（加号按钮）
await page.mouse.click(230, 327)
await asyncio.sleep(2)

# 选择文件（使用正则匹配文件名）
file_item = page.locator('text=/Luna.*mars/i').first
await file_item.click()

# 添加到 Prompt
add_btn = page.locator('button:has-text("Add to Prompt")').first
await add_btn.click()
```

### 提交生成

```python
# 输入 Prompt
input_box = page.locator('[contenteditable="true"]').first
await input_box.fill("你的 prompt")

# 点击 Create 按钮（带箭头）
create_btn = page.locator('button:has(i:text("arrow_forward"))').first
await create_btn.click()
```

## 📦 可复用脚本

完整脚本已保存在: `/tmp/flow_automation_final.py`

### 使用方法

```bash
# 1. 启动 Chrome（如果还没启动）
/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome \
  --remote-debugging-port=9222 \
  --user-data-dir="/tmp/flow_chrome_debug" &

# 2. 登录并打开项目页面

# 3. 运行脚本
python3 /tmp/flow_automation_final.py
```

### 自定义配置

编辑脚本中的配置部分：

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

## 📊 性能数据

- Chrome 启动时间: ~3-5秒
- CDP 连接时间: <1秒
- 单张图片添加: ~5秒
- Prompt 输入: ~2秒
- 提交响应: ~3秒
- **总耗时: ~20-30秒**

## 🎓 学到的经验

### 调试技巧

1. **截图是最好的调试工具**
   - 每个关键步骤都截图
   - 对比截图vs预期状态

2. **逐步执行 > 一次性执行**
   - 先手动执行一遍流程
   - 记录每步的元素和状态
   - 再转化为自动化脚本

3. **选择器优先级**
   - 文本选择器（最稳定）
   - 坐标点击（需固定分辨率）
   - CSS 选择器（最不稳定）

### 自动化原则

1. **状态重置很重要**
   - 每次执行前按几次 Escape
   - 确保从已知的干净状态开始

2. **等待时间要充足**
   - 网络请求: 2-3秒
   - 动画效果: 1-2秒
   - 复杂操作: 3-5秒

3. **错误处理**
   - 使用 try-except 捕获异常
   - 提供有意义的错误提示
   - 失败时截图保存现场

## 🚀 下一步可能的优化

1. **参数化**
   - 通过命令行参数传入文件名和 prompt
   - 支持配置文件

2. **结果等待**
   - 轮询检查生成进度
   - 生成完成后自动下载

3. **批量处理**
   - 支持多组参考图+prompt
   - 批量生成多张图片

4. **CLI 工具**
   - 打包成独立的命令行工具
   - 提供友好的交互界面

## ✅ 验证清单

每次运行前检查：

- [ ] Chrome 已启动并开启调试端口 (9222)
- [ ] 已登录 Google 账号
- [ ] 在 Flow 项目页面
- [ ] 参考图文件已上传到 Uploads
- [ ] Playwright 已安装 (`pip install playwright`)
- [ ] Playwright 浏览器已安装 (`playwright install chromium`)

---

**创建时间:** 2026-05-24
**Chrome Profile:** `/tmp/flow_chrome_debug`
**项目 ID:** `4f24835c-c783-4646-96dc-a0b8c03c34fc`
