# Flow 自动化操作记录

## 目标
添加 Luna_on_mars.png 和 Wayne_on_earth.png 两个参考图，然后生成迪士尼场景

## 初始状态
- URL: https://labs.google/fx/tools/flow/project/4f24835c-c783-4646-96dc-a0b8c03c34fc
- 已登录，在项目页面

---

## 环境设置

**Chrome Profile:** `/tmp/flow_chrome_debug`
**调试端口:** 9222
**说明:** 此 profile 已登录 Google 账号，可重复使用

---

## 操作步骤

### 步骤 0: 导航到项目页面 ✅

**操作:**
```python
await page.goto("https://labs.google/fx/tools/flow/project/4f24835c-c783-4646-96dc-a0b8c03c34fc")
await page.wait_for_load_state('networkidle')
```

**结果:** 成功到达项目页面
**截图:** `/tmp/step0_project_page.png`

---

### 步骤 1: 添加第一个参考图 - Luna_on_mars.png ✅

**正确操作流程:**

```python
# 1. 点击输入框左下角的加号按钮
# 坐标约为 (170, 920) - 底部左侧
await page.mouse.click(170, 920)
await asyncio.sleep(3)

# 2. 媒体选择器打开后，点击 "Uploads" 标签
uploads_option = page.locator('text="Uploads"').first
await uploads_option.click()
await asyncio.sleep(2)

# 3. 在文件列表中点击 Luna_on_mars.png
luna_item = page.locator('text="Luna_on_mars.png"').first
await luna_item.click()
await asyncio.sleep(2)

# 4. 点击 "Add to Prompt" 按钮
add_btn = page.locator('button:has-text("Add to Prompt")').first
await add_btn.click()
await asyncio.sleep(2)
```

**关键发现:**
- ❌ 错误：点击顶部的 "Add Media" 按钮（那是用于创建新媒体的）
- ✅ 正确：点击**输入框旁边的加号按钮**（底部左侧）
- 加号按钮位置：输入框左下角，坐标约 (170, 920)
- 媒体选择器会弹出，显示多个标签（Uploads, Images, Characters 等）

**结果:**
- Luna_on_mars.png 成功添加到 Prompt
- 在输入区域显示缩略图

**截图:**
- `/tmp/media_picker_opened.png` - 媒体选择器界面
- `/tmp/uploads_list.png` - Uploads 文件列表
- `/tmp/luna_selected.png` - Luna 已选中
- `/tmp/luna_added_correct.png` - Luna 已添加

---

### 步骤 2: 添加第二个参考图 - Wayne_on_earth.png ✅

**操作:**

```python
# 5. 再次点击加号按钮
await page.mouse.click(170, 920)
await asyncio.sleep(3)

# 6. 点击 Uploads
uploads_option = page.locator('text="Uploads"').first
await uploads_option.click()
await asyncio.sleep(2)

# 7. 点击 Wayne_on_earth.png
wayne_item = page.locator('text="Wayne_on_earth.png"').first
await wayne_item.click()
await asyncio.sleep(2)

# 8. 点击 "Add to Prompt"
add_btn = page.locator('button:has-text("Add to Prompt")').first
await add_btn.click()
await asyncio.sleep(2)
```

**重要:**
- 每次只能添加一个参考图，需要重复打开媒体选择器
- 不支持多选

**结果:**
- Wayne_on_earth.png 成功添加到 Prompt
- 两个参考图都显示在输入区域

**截图:**
- `/tmp/wayne_selected.png` - Wayne 已选中
- `/tmp/both_refs_added_correct.png` - 两张参考图都已添加

---

## Appendix: 界面元素详细记录

### A. 主界面按钮（顶部工具栏）

从探索过程中发现的所有可见按钮：

| 索引 | 文本 | 用途 | 备注 |
|------|------|------|------|
| #0 | `arrow_back\nGo Back` | 返回上一页 | |
| #1 | `more_vert\nMore options` | 更多选项 | |
| #2 | `search\nSearch` | 搜索 | |
| #3 | `filter_list\nSort & Filter` | 排序和筛选 | |
| #4 | `add\nAdd Media` | 添加媒体 | **⚠️ 非添加参考图的按钮** |
| #5 | `help\nProduct Help` | 产品帮助 | |
| #6 | `settings_2\nView Settings` | 查看设置 | |
| #7 | `more_vert\nMore` | 更多 | |
| #8 | `PRO` | Pro 版本 | |

### B. 左侧边栏（导航）

| 索引 | 文本 | 用途 |
|------|------|------|
| #9 | `dashboard\nAll Media` | 所有媒体 |
| #10 | `image\nView images` | 查看图片 |
| #11 | `accessibility_new\nCharacters` | 角色 |
| #12 | `movie\nView scenes` | 查看场景 |
| #13 | `drive_folder_upload\nView uploaded media` | **查看上传的媒体（Uploads）** |
| #14 | `apps_spark_2\nTools` | 工具 |
| #15 | `delete\nView Trash` | 查看回收站 |
| #16 | `left_panel_close\nCollapse` | 收起侧边栏 |

### C. 底部创建区域

| 索引 | 文本 | 用途 |
|------|------|------|
| #17 | `add_2\nCreate` | 创建按钮 |
| #18 | `Agent` | Agent 相关 |
| #19 | 模型选择 | 如 `🍌 Nano Banana 2` |
| #20 | `arrow_forward\nCreate` | 创建（另一个入口）|

### D. "Add Media" 菜单选项

点击顶部 "Add Media" (#4) 后出现的菜单：

| 索引 | 文本 | 用途 | 备注 |
|------|------|------|------|
| #21 | `upload\nUpload media` | 上传媒体 | 上传新文件 |
| #22 | `folder\nCreate Collection` | 创建集合 | |
| #23 | `account_circle\nCreate Character` | 创建角色 | |
| #24 | `play_movies\nCreate Scene` | 创建场景 | |

### E. 媒体选择器（加号按钮弹出）

**触发方式:** 点击输入框左下角的加号按钮（坐标约 170, 920）

**可用标签:**
- **Uploads** - 已上传的文件（我们使用的）
- Images - 图片库
- Characters - 角色库
- Scenes - 场景库
- Collections - 集合
- （可能还有其他）

**操作流程:**
1. 选择标签（如 Uploads）
2. 点击文件名选中
3. 点击 "Add to Prompt" 按钮添加

### F. Uploads 页面发现的文件

从探索过程中看到的上传文件：

1. `Luna_on_mars.png` - Luna 角色在火星场景 ✅ 已使用
2. `Wayne_on_earth.png` - Wayne 角色在地球场景 ✅ 已使用
3. `Wayne_on_mars.jpeg` - Wayne 角色在火星场景
4. `Wayne_with_mech.png` - Wayne 与机甲
5. `Luna` (character reference) - Luna 角色参考图
6. `Kirin Mech` - Kirin 机甲
7. `Wayne` (character reference) - Wayne 角色参考图

### G. 关键坐标位置

| 元素 | 坐标 | 说明 |
|------|------|------|
| 加号按钮（添加参考图）| (170, 920) | 输入框左下角 |
| Uploads 卡片 #1 | (244, 76) | 左上角第一张 |
| Uploads 卡片 #2 | (718, 76) | 右上角 |
| Uploads 卡片 #3 | (244, 433) | 左下角 |
| Uploads 卡片 #4 | (660, 433) | 右下角 |

### H. 选择器策略总结

**稳定的选择器:**
- 文本选择器：`page.locator('text="Uploads"').first`
- 按钮索引：`page.locator('button').nth(13)` （但可能变化）
- 坐标点击：`page.mouse.click(x, y)` （屏幕分辨率固定时可靠）

**不稳定的选择器:**
- CSS 选择器（如 `#__next > div > ...`）- DOM 结构可能变化
- 按钮索引 - 页面状态变化时索引会改变

**推荐策略:**
1. 优先使用文本选择器（最稳定）
2. 关键位置使用坐标（需要固定分辨率）
3. 避免复杂的 CSS 选择器

---

## 总结与学习

### 成功的关键点

1. ✅ **正确的入口点:** 使用输入框旁的加号按钮，而不是顶部的 "Add Media"
2. ✅ **Chrome Profile 重用:** 使用 `/tmp/flow_chrome_debug` 可以保留登录状态
3. ✅ **CDP 连接方式:** `--remote-debugging-port=9222` 稳定可靠
4. ✅ **文本选择器:** `text="Uploads"` 比复杂 CSS 选择器更稳定
5. ✅ **分步操作:** 每次只添加一个参考图，不支持批量添加

### 遇到的陷阱

1. ❌ 点错了 "Add Media" 按钮（那是创建新媒体的）
2. ❌ 使用系统 profile 时调试端口打不开
3. ❌ 按钮索引在页面状态变化时会改变
4. ❌ 假设可以多选（实际每次只能选一个）

### 可复用的代码模式

```python
# 启动 Chrome
/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome \
  --remote-debugging-port=9222 \
  --user-data-dir="/tmp/flow_chrome_debug"

# 连接
browser = await p.chromium.connect_over_cdp("http://127.0.0.1:9222")
context = browser.contexts[0]
page = context.pages[0]

# 添加参考图（可复用流程）
await page.mouse.click(170, 920)  # 点击加号
await page.locator('text="Uploads"').first.click()  # 选择 Uploads
await page.locator('text="filename.png"').first.click()  # 选择文件
await page.locator('button:has-text("Add to Prompt")').first.click()  # 添加
```
