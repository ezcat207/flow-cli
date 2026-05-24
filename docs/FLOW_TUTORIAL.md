# Google Flow 完整操作教程

## 📑 快速导航

- [环境准备](#环境准备)
- [教程 1: 基础图片生成](#教程-1-基础图片生成)
- [教程 2: 使用搜索功能](#教程-2-使用搜索功能)
- [教程 3: 上传并使用新文件](#教程-3-上传并使用新文件)
- [自动化脚本使用](#自动化脚本使用)
- [故障排除](#故障排除)

---

## 环境准备

### 步骤 1: 启动 Chrome 浏览器

```bash
# 完全关闭现有 Chrome 进程
killall "Google Chrome"
sleep 2

# 启动带调试端口的 Chrome
/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome \
  --remote-debugging-port=9222 \
  --user-data-dir="/tmp/flow_chrome_debug" &

# 等待 Chrome 启动
sleep 5

# 验证调试端口
curl http://127.0.0.1:9222/json/version
```

**期望输出:**
```json
{
   "Browser": "Chrome/148.x.x.x",
   "Protocol-Version": "1.3",
   ...
}
```

### 步骤 2: 登录 Google 账号

1. 在打开的 Chrome 窗口中，访问 Google.com
2. 点击右上角的"登录"按钮
3. 输入 Google 账号和密码
4. 完成登录验证

### 步骤 3: 打开 Flow 项目

1. 访问：`https://labs.google/fx/tools/flow`
2. 选择或创建一个项目
3. 进入项目页面

**验证:** 地址栏 URL 应为: `https://labs.google/fx/tools/flow/project/{PROJECT_ID}`

---

## 教程 1: 基础图片生成

### 目标
使用两张参考图（Luna_on_mars.png 和 Wayne_on_earth.png）生成一张新图片

### 前置条件
- ✅ Chrome 已启动并登录
- ✅ 在 Flow 项目页面
- ✅ 参考图已上传到 Uploads

---

### 步骤 1.1: 添加第一张参考图

#### 操作点位: 加号按钮

**位置:** 输入框左侧
**坐标:** 约 (230, 327)
**外观:** 圆形按钮，"+" 图标

**点击后会遇到的内容:**

弹出媒体选择器对话框：

```
┌─ 媒体选择器 ─────────────────────┐
│                                  │
│  [搜索框: Search assets]          │
│                                  │
│  左侧分类列表     │   右侧内容区    │
│  ────────────   │   ──────────  │
│  ○ All          │                │
│  ○ Images       │   文件列表      │
│  ○ Videos       │   或           │
│  ○ Voices       │   预览图       │
│  ○ Characters   │                │
│  ○ Avatar       │                │
│  ● Uploads      │                │
│                                  │
│     [Add to Prompt 按钮]          │
└──────────────────────────────────┘
```

**可选操作:**
1. 直接在列表中找文件
2. 使用搜索功能
3. 切换不同分类
4. 关闭对话框 (ESC 或 X)

---

#### 操作点位: Uploads 分类

**位置:** 左侧分类列表中
**外观:** 带文件夹上传图标
**文本:** "Uploads"

**点击后会遇到的内容:**

右侧显示所有已上传的文件：

**文件列表示例:**
```
┌─────────────────────────────────┐
│ □ Luna_on_mars.png      [缩略图] │
│ □ Wayne_on_earth.png    [缩略图] │
│ □ Wayne_with_mech.png   [缩略图] │
│ □ Wayne_on_mars.jpeg    [缩略图] │
│ □ Kirin_mech.png        [缩略图] │
│ ...                              │
└─────────────────────────────────┘
```

**可用操作:**
- 点击文件名选中
- 滚动查看更多
- 使用搜索过滤

---

#### 操作点位: Luna_on_mars.png 文件

**位置:** Uploads 文件列表中
**外观:** 文件名 + 缩略图
**状态:** 未选中 / 选中（高亮）

**点击后会遇到的内容:**

1. 文件项背景变色（选中状态）
2. 右侧显示大图预览
3. 底部 "Add to Prompt" 按钮变为可用状态

**预览区域显示:**
```
┌─────────────────────────┐
│                         │
│    [Luna 大图预览]       │
│                         │
│  文件名: Luna_on_mars.png│
│  尺寸: 1024x1024        │
│  大小: 2.3 MB           │
│  日期: May 23, 2026     │
└─────────────────────────┘
```

**可用操作:**
- 点击其他文件切换选择
- 点击 "Add to Prompt" 添加
- 点击 X 或 ESC 取消

---

#### 操作点位: Add to Prompt 按钮

**位置:** 媒体选择器底部
**外观:** 蓝色大按钮，全宽
**文本:** "Add to Prompt"
**状态:** 禁用（灰色）/ 启用（蓝色）

**点击后会遇到的内容:**

1. 媒体选择器自动关闭
2. 回到主界面
3. 输入框区域**显示添加的图片缩略图**
4. 输入框左侧有小的预览图标

**主界面变化:**
```
[之前]
┌────────────────────────────────────┐
│ [+] [What do you want to create?]  │
└────────────────────────────────────┘

[之后]
┌────────────────────────────────────┐
│ [小缩略图]                          │
│ [Luna_on_mars.png]                 │
│ [+] [What do you want to create?]  │
└────────────────────────────────────┘
```

---

### 步骤 1.2: 添加第二张参考图

**重复步骤 1.1，但选择 Wayne_on_earth.png**

#### 关键差异:

1. **再次点击加号按钮**
   - 上次的参考图仍然保留
   - 可以继续添加更多

2. **选择 Wayne_on_earth.png**
   - 在同样的 Uploads 列表中
   - 可能需要滚动查找

3. **添加后的状态**
   ```
   [现在有两个参考图]
   ┌────────────────────────────────────┐
   │ [Luna缩略图] [Wayne缩略图]          │
   │ [Luna_on_mars.png] [Wayne_on_earth.png] │
   │ [+] [What do you want to create?]  │
   └────────────────────────────────────┘
   ```

---

### 步骤 1.3: 输入生成 Prompt

#### 操作点位: 输入框

**位置:** 底部中央区域
**外观:** 大文本框
**Placeholder:** "What do you want to create?"
**类型:** contenteditable div

**点击后会遇到的内容:**

1. 输入框获得焦点（蓝色边框）
2. 光标出现
3. Placeholder 文字消失
4. 可以开始输入

**输入示例:**
```
他们在中国杭州玩
```

**其他可用 Prompt 示例:**
- "Luna and Wayne at Disneyland, sunny day, high quality"
- "两只可爱的动物在公园里玩耍，迪士尼风格"
- "cute animals having fun, Disney style, vibrant colors"

**注意事项:**
- 支持中文和英文
- 可以混合使用
- 长度建议 10-100 字
- 描述越详细，生成结果越精确

---

### 步骤 1.4: 提交生成请求

#### 操作点位: Create 按钮 (带箭头)

**位置:** 输入框右下角
**外观:** 圆形按钮，带 → (arrow_forward) 图标
**文本:** "Create" (隐藏文本，辅助功能)
**状态:**
- 灰色 (aria-disabled="true") - 不可点击
- 蓝色 (aria-disabled="false") - 可点击

**点击前需要满足:**
- ✅ 至少输入了一些 Prompt 文字
- （可选）添加了参考图

**点击后会遇到的内容:**

#### 立即变化:
1. 输入框内容清空
2. Create 按钮变灰（禁用）
3. 顶部出现生成进度卡片

#### 生成进度显示:
```
┌─────────────────────────┐
│  [进度条]                │
│  10%                    │
│  [模糊的预览图]          │
└─────────────────────────┘
```

#### 进度阶段:
- **0-10%:** 初始化
- **10-30%:** 理解 Prompt
- **30-60%:** 生成基础图像
- **60-90%:** 细化细节
- **90-100%:** 最终处理

#### 完成后:
```
┌─────────────────────────┐
│                         │
│   [完整的生成图片]       │
│                         │
│  May 24, 11:28 PM      │
└─────────────────────────┘
```

**可用操作:**
- 点击图片查看大图
- 下载图片
- 编辑/再生成
- 删除

---

### 步骤 1.5: 查看生成结果

#### 操作点位: 生成的图片卡片

**位置:** 主内容区域顶部
**外观:** 图片卡片，带时间戳

**点击后会遇到的内容:**

打开图片详情视图：

```
┌─────────────────────────────────────┐
│  [← 返回]  [标题]  [下载] [更多]     │
├─────────────────────────────────────┤
│                                     │
│         [大图显示]                   │
│                                     │
├─────────────────────────────────────┤
│ Prompt: 他们在中国杭州玩               │
│                                     │
│ 参考图:                              │
│  - Luna_on_mars.png                 │
│  - Wayne_on_earth.png               │
│                                     │
│ 模型: Nano Banana 2                  │
│ 时间: May 24, 2026 11:28 PM        │
└─────────────────────────────────────┘
```

**可用操作:**
- ← 返回列表
- 下载 (Download 按钮)
- 分享 (Share 按钮)
- 编辑 (Edit 按钮) - 重新生成
- 删除 (Delete 按钮)
- 收藏 (Favorite 按钮)
- 查看历史 (History 按钮)

---

## 教程 2: 使用搜索功能

### 目标
通过搜索快速找到需要的参考图

### 步骤 2.1: 打开媒体选择器并使用搜索

#### 操作点位: 搜索框

**位置:** 媒体选择器顶部
**Placeholder:** "Search assets"
**功能:** 搜索文件名、标签、内容

**使用方法:**

1. **打开媒体选择器**
   ```
   点击加号按钮 (230, 327)
   ```

2. **点击搜索框**
   ```
   ┌─ 媒体选择器 ────────────────┐
   │ [🔍 Search assets______]    │ ← 点击这里
   │                             │
   │  分类列表  │  文件列表       │
   └─────────────────────────────┘
   ```

3. **输入搜索关键词**

   **示例 1: 搜索文件名**
   ```
   输入: Luna
   结果:
     - Luna_on_mars.png
     - Luna_character.png
     - Luna_reference.png
   ```

   **示例 2: 搜索场景**
   ```
   输入: mars
   结果:
     - Luna_on_mars.png
     - Wayne_on_mars.jpeg
     - Mars_landscape.png
   ```

   **示例 3: 搜索格式**
   ```
   输入: .png
   结果: 所有 PNG 格式文件
   ```

4. **从搜索结果中选择**
   - 点击想要的文件
   - 右侧显示预览
   - 点击 "Add to Prompt"

**搜索技巧:**
- 使用部分文件名
- 搜索标签或关键词
- 使用文件格式过滤 (.png, .jpg)
- 清空搜索框查看全部

---

## 教程 3: 上传并使用新文件

### 目标
上传本地图片并在生成中使用

### 步骤 3.1: 上传新文件

#### 操作点位: Add Media 按钮

**位置:** 顶部工具栏右侧
**图标:** `add` (加号)
**文本:** "Add Media"
**注意:** ⚠️ 这**不是**输入框旁的加号

**点击后会遇到的内容:**

下拉菜单出现：

```
┌─────────────────────────┐
│ 📤 Upload media         │ ← 选择这个
│ 📁 Create Collection    │
│ 👤 Create Character     │
│ 🎬 Create Scene         │
└─────────────────────────┘
```

#### 菜单选项详解:

| 选项 | 功能 | 使用场景 |
|------|------|----------|
| **Upload media** | 上传文件 | 上传本地图片/视频 |
| Create Collection | 创建集合 | 组织现有媒体 |
| Create Character | 创建角色 | 定义新角色 |
| Create Scene | 创建场景 | 定义新场景设定 |

---

#### 操作点位: Upload media

**点击后会遇到的内容:**

系统文件选择器打开：

```
┌─ 选择文件 ────────────────┐
│                           │
│  [文件浏览器]              │
│                           │
│  我的文件/                 │
│    Downloads/             │
│      image1.png           │
│      image2.jpg           │
│                           │
│  [取消]  [打开]           │
└───────────────────────────┘
```

**支持的文件格式:**
- 图片: .png, .jpg, .jpeg, .webp, .gif
- 视频: .mp4, .mov, .avi
- 其他: 根据 Flow 版本可能有所不同

**选择文件后:**

1. 上传进度显示
   ```
   ┌──────────────────────┐
   │ Uploading...         │
   │ [========>    ] 75%  │
   └──────────────────────┘
   ```

2. 上传完成
   ```
   ┌──────────────────────┐
   │ ✅ Upload complete   │
   │ image1.png           │
   └──────────────────────┘
   ```

3. 文件自动添加到 Uploads 分类

---

### 步骤 3.2: 使用刚上传的文件

1. **点击加号按钮** 打开媒体选择器
2. **选择 Uploads** 分类
3. **找到刚上传的文件** (通常在列表顶部)
4. **点击文件** 选中
5. **点击 Add to Prompt** 添加
6. **继续输入 Prompt 并生成**

---

## 自动化脚本使用

### 方式 1: 使用提供的脚本

```bash
# 1. 确保 Chrome 已启动
/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome \
  --remote-debugging-port=9222 \
  --user-data-dir="/tmp/flow_chrome_debug" &

# 2. 等待并登录

# 3. 运行脚本
python3 /tmp/flow_automation_final.py
```

### 方式 2: 自定义脚本

编辑 `/tmp/flow_automation_final.py`：

```python
# === 配置部分 ===

# 修改项目 URL
PROJECT_URL = "https://labs.google/fx/tools/flow/project/YOUR_PROJECT_ID"

# 修改参考图文件名
REFERENCE_IMAGES = [
    "your_image1.png",
    "your_image2.png",
    "your_image3.png"  # 可以添加更多
]

# 修改 Prompt
PROMPT = "你的自定义生成描述"
```

保存后运行：
```bash
python3 /tmp/flow_automation_final.py
```

---

## 故障排除

### 问题 1: 找不到加号按钮

**症状:** 脚本报错找不到加号按钮

**检查:**
```python
# 截图查看界面状态
await page.screenshot(path='/tmp/debug_interface.png')
```

**可能原因:**
1. 页面未完全加载
2. 界面布局变化
3. 坐标不准确

**解决方案:**
```python
# 方法 1: 增加等待时间
await asyncio.sleep(3)

# 方法 2: 使用选择器而不是坐标
plus_btn = page.locator('button[aria-label*="add"]').first
await plus_btn.click()

# 方法 3: 手动调整坐标
await page.mouse.click(250, 330)  # 微调坐标
```

---

### 问题 2: 文件列表为空

**症状:** 打开 Uploads 后看不到任何文件

**检查:**
1. 确认文件已上传
2. 查看是否在正确的分类
3. 尝试刷新页面

**解决方案:**
```python
# 1. 切换到 Uploads 分类
await page.locator('text="Uploads"').first.click()
await asyncio.sleep(2)

# 2. 如果还是没有，尝试使用搜索
search_box = page.locator('[placeholder*="Search"]').first
await search_box.fill("你的文件名")
await asyncio.sleep(1)

# 3. 如果还是找不到，先上传文件
# 使用 Add Media > Upload media
```

---

### 问题 3: Create 按钮不可点击

**症状:** Create 按钮是灰色的，点击无效

**检查:**
```python
# 检查按钮状态
create_btn = page.locator('button:has(i:text("arrow_forward"))').first
is_disabled = await create_btn.get_attribute('aria-disabled')
print(f"按钮状态: {is_disabled}")  # true = 禁用, false = 可用
```

**可能原因:**
1. 未输入 Prompt
2. Prompt 太短
3. 系统限制（如配额用完）

**解决方案:**
```python
# 1. 确保 Prompt 已输入
input_box = page.locator('[contenteditable="true"]').first
await input_box.click()
await asyncio.sleep(0.5)
await input_box.fill("你的 Prompt 内容")
await asyncio.sleep(1)

# 2. 再次检查按钮状态
is_disabled = await create_btn.get_attribute('aria-disabled')
if is_disabled == 'true':
    # 截图查看问题
    await page.screenshot(path='/tmp/create_disabled.png')
    print("Create 按钮仍然禁用，请检查截图")
else:
    # 可以点击了
    await create_btn.click()
```

---

### 问题 4: 生成失败或无响应

**症状:** 点击 Create 后没有进度显示

**检查流程:**

1. **检查网络连接**
   ```bash
   ping google.com
   ```

2. **检查账号状态**
   - 是否还登录？
   - 配额是否用完？

3. **检查浏览器控制台**
   ```python
   # 在脚本中添加控制台日志监听
   page.on("console", lambda msg: print(f"Console: {msg.text}"))
   page.on("pageerror", lambda err: print(f"Error: {err}"))
   ```

4. **手动测试**
   - 在浏览器中手动执行一次流程
   - 确认功能正常

**解决方案:**
- 刷新页面重试
- 重新登录账号
- 联系 Flow 支持

---

## 快速参考

### 常用坐标

| 元素 | 坐标 (x, y) |
|------|-------------|
| 加号按钮 | (230, 327) |
| 输入框 | (400, 920) |

### 常用选择器

| 元素 | 选择器 |
|------|--------|
| Uploads 分类 | `text="Uploads"` |
| 文件列表项 | `text=/filename/i` |
| Add to Prompt | `button:has-text("Add to Prompt")` |
| 输入框 | `[contenteditable="true"]` |
| Create 按钮 | `button:has(i:text("arrow_forward"))` |

### 常用等待时间

| 操作 | 等待时间 |
|------|----------|
| 点击加号 | 2秒 |
| 切换分类 | 1秒 |
| 选择文件 | 1秒 |
| Add to Prompt | 2秒 |
| 输入 Prompt | 1秒 |
| 点击 Create | 3秒 |

---

**教程版本:** 1.0
**创建日期:** 2026-05-24
**作者:** AI Assistant
**测试环境:** macOS, Chrome 148.x, Google Flow (May 2026)
