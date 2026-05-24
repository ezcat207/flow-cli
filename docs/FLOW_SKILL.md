# Google Flow 自动化技能文档

## 📚 目录

1. [界面结构](#界面结构)
2. [主要功能区域](#主要功能区域)
3. [媒体选择器详解](#媒体选择器详解)
4. [按钮和操作](#按钮和操作)
5. [完整操作流程](#完整操作流程)
6. [常见问题](#常见问题)

---

## 界面结构

### 主界面布局

```
┌─────────────────────────────────────────────────────────────┐
│ ← [返回] [更多选项] [搜索] [筛选] [+添加媒体] [帮助] [设置] │ 顶部工具栏
├──────────┬──────────────────────────────────────────────────┤
│          │                                                  │
│ 侧边栏   │              主内容区域                           │
│          │         (显示生成的图片网格)                       │
│ - All    │                                                  │
│ - Images │                                                  │
│ - Chars  │                                                  │
│ - Scenes │                                                  │
│ - Upload │                                                  │
│ - Tools  │                                                  │
│          │                                                  │
├──────────┴──────────────────────────────────────────────────┤
│ [+] [输入框: What do you want to create?] [Agent] [Create→] │ 底部创建区
└─────────────────────────────────────────────────────────────┘
```

### 关键区域坐标（参考值）

| 区域 | 坐标 (x, y) | 说明 |
|------|-------------|------|
| 加号按钮 | (230, 327) | 打开媒体选择器 |
| 输入框区域 | (400, 920) | Prompt 输入 |
| Create 按钮 | (右下角) | 带箭头的提交按钮 |

---

## 主要功能区域

### 1. 顶部工具栏

#### 左侧按钮组

| 按钮 | 图标 | 文本 | 功能 |
|------|------|------|------|
| #0 | `arrow_back` | Go Back | 返回上一页 |
| #1 | `more_vert` | More options | 更多选项菜单 |
| #2 | `search` | Search | 搜索功能 |
| #3 | `filter_list` | Sort & Filter | 排序和筛选 |

#### 右侧按钮组

| 按钮 | 图标 | 文本 | 功能 |
|------|------|------|------|
| #4 | `add` | Add Media | 创建/上传媒体（❌ 不是添加参考图的入口）|
| #5 | `help` | Product Help | 产品帮助文档 |
| #6 | `settings_2` | View Settings | 查看和修改设置 |
| #7 | `more_vert` | More | 更多操作 |
| #8 | - | PRO | Pro 版本标识 |

### 2. 左侧边栏导航

| 索引 | 图标 | 文本 | 功能 | 用途 |
|------|------|------|------|------|
| #9 | `dashboard` | All Media | 所有媒体 | 显示所有类型的媒体 |
| #10 | `image` | Images | 图片 | 只显示图片类型 |
| #11 | `accessibility_new` | Characters | 角色 | 角色库管理 |
| #12 | `movie` | Scenes | 场景 | 场景库管理 |
| #13 | `drive_folder_upload` | Uploads | 上传文件 | **用户上传的文件** |
| #14 | `apps_spark_2` | Tools | 工具 | Flow 工具集 |
| #15 | `delete` | Trash | 回收站 | 已删除的项目 |
| #16 | `left_panel_close` | Collapse | 收起 | 隐藏侧边栏 |

### 3. 底部创建区域

#### 左侧

| 元素 | 类型 | 功能 | 重要程度 |
|------|------|------|----------|
| **加号按钮 (+)** | 按钮 | **打开媒体选择器** | ⭐⭐⭐⭐⭐ |
| Agent 按钮 | 按钮 | 打开 Agent 设置 | ⭐⭐ |

#### 中间

| 元素 | 类型 | Placeholder | 功能 |
|------|------|------------|------|
| **输入框** | contenteditable | "What do you want to create?" | **输入生成 Prompt** |

#### 右侧

| 元素 | 类型 | 图标 | 功能 | 重要程度 |
|------|------|------|------|----------|
| 模型选择器 | 下拉菜单 | 🍌 Nano Banana 2 | 选择生成模型 | ⭐⭐⭐ |
| **Create 按钮** | 按钮 | `arrow_forward` | **提交生成请求** | ⭐⭐⭐⭐⭐ |

---

## 媒体选择器详解

### 打开方式

**正确方式:** 点击输入框左侧的加号按钮 (坐标约 230, 327)

❌ **错误方式:** 点击顶部的 "Add Media" 按钮（那是用来上传新文件的）

### 媒体选择器界面结构

```
┌─────────────────────────────────────────────────────────────┐
│  媒体选择器                                          [X 关闭]  │
├─────────────┬───────────────────────────────────────────────┤
│             │                                               │
│ 分类列表     │           文件列表 / 预览区域                  │
│             │                                               │
│ □ All       │  ┌─────────────────────────────────────────┐ │
│ □ Images    │  │ Luna_on_mars.png         [缩略图]       │ │
│ □ Videos    │  │ Wayne_on_earth.png       [缩略图]       │ │
│ □ Voices    │  │ Wayne_with_mech.png      [缩略图]       │ │
│ □ Characters│  │ Wayne_on_mars.jpeg       [缩略图]       │ │
│ □ Avatar    │  │ ...                                     │ │
│ ▣ Uploads   │  └─────────────────────────────────────────┘ │
│             │                                               │
│             │          [预览区域 - 选中文件的大图]            │
│             │                                               │
├─────────────┴───────────────────────────────────────────────┤
│                    [Add to Prompt 按钮]                      │
└─────────────────────────────────────────────────────────────┘
```

### 分类选项详解

#### All (全部)
- **功能:** 显示所有类型的媒体
- **内容:** 混合显示图片、视频、角色、场景等
- **使用场景:** 不确定文件在哪个分类时

#### Images (图片)
- **功能:** 只显示图片类型的媒体
- **内容:** 所有图片格式文件 (.png, .jpg, .jpeg, .webp 等)
- **使用场景:** 快速查找图片素材

#### Videos (视频)
- **功能:** 显示视频文件
- **内容:** 视频格式文件 (.mp4, .mov 等)
- **使用场景:** 添加视频参考

#### Voices (语音)
- **功能:** 语音文件库
- **内容:** 音频文件
- **使用场景:** 为生成内容添加语音

#### Characters (角色)
- **功能:** 角色库
- **内容:** 已创建或上传的角色参考图
- **使用场景:** 选择角色参考

#### Avatar (头像)
- **功能:** 头像库
- **内容:** 头像资源
- **使用场景:** 角色头像选择

#### **Uploads (上传) ⭐⭐⭐⭐⭐**
- **功能:** 用户上传的所有文件
- **内容:** 所有通过 "Upload media" 上传的文件
- **使用场景:** **添加自己上传的参考图**
- **重要性:** 本项目主要使用此分类

### 文件列表显示方式

#### 列表视图（默认）
```
[文件名]           [缩略图]    [日期]
Luna_on_mars.png    [图]      May 23
Wayne_on_earth.png  [图]      May 23
```

#### 网格视图（某些分类）
```
┌────────┐  ┌────────┐  ┌────────┐
│ [图]   │  │ [图]   │  │ [图]   │
│ Luna   │  │ Wayne  │  │ Kirin  │
└────────┘  └────────┘  └────────┘
```

### Search Asset 功能 🔍

**位置:** 媒体选择器顶部

**使用方法:**
```python
# 1. 打开媒体选择器
await page.mouse.click(230, 327)

# 2. 点击搜索框
search_box = page.locator('[placeholder*="Search"]').first
await search_box.click()

# 3. 输入搜索关键词
await search_box.fill("Luna")

# 4. 等待搜索结果
await asyncio.sleep(1)

# 5. 从结果中选择文件
file = page.locator('text="Luna_on_mars.png"').first
await file.click()
```

**搜索支持:**
- 文件名搜索
- 标签搜索
- 内容搜索（AI 识别）

**示例搜索词:**
- `Luna` - 查找包含 Luna 的所有文件
- `mars` - 查找火星相关的文件
- `earth` - 查找地球相关的文件

### 操作按钮

#### Add to Prompt (添加到 Prompt)
- **位置:** 媒体选择器底部（大按钮）
- **样式:** 蓝色背景，全宽按钮
- **文本:** "Add to Prompt"
- **功能:** 将选中的文件添加为参考图
- **行为:** 点击后自动关闭媒体选择器

#### 取消/关闭
- **位置:** 右上角 X 按钮，或按 ESC 键
- **功能:** 关闭媒体选择器而不添加

---

## 按钮和操作

### "Add Media" 下拉菜单（顶部按钮 #4）

**打开方式:** 点击顶部的 "Add Media" 按钮

**菜单选项:**

| 索引 | 图标 | 文本 | 功能 | 使用场景 |
|------|------|------|------|----------|
| #21 | `upload` | Upload media | 上传新文件 | 上传本地图片/视频 |
| #22 | `folder` | Create Collection | 创建集合 | 组织媒体文件 |
| #23 | `account_circle` | Create Character | 创建角色 | 新建角色定义 |
| #24 | `play_movies` | Create Scene | 创建场景 | 新建场景设定 |

**注意:**
- ❌ 这**不是**添加参考图到 Prompt 的入口
- ✅ 这是用来**创建/上传**新媒体的
- 如果需要上传新文件到 Uploads，使用此菜单的 "Upload media"

### Create 按钮（底部右侧）

#### 两个 Create 按钮的区别

| 按钮 | 索引 | 图标 | 功能 | 使用场景 |
|------|------|------|------|----------|
| Create #1 | #17 | `add_2` | 打开创建菜单 | ❌ 不是提交按钮 |
| **Create #2** | #23 | `arrow_forward` | **提交生成请求** | ✅ **这是正确的提交按钮** |

**正确的提交按钮特征:**
- 带有 `arrow_forward` (→) 图标
- 位于输入框右下角
- 通常在输入 Prompt 后才可点击（非灰色状态）

**选择器代码:**
```python
# 正确的选择器
create_btn = page.locator('button:has(i:text("arrow_forward"))').first
await create_btn.click()

# 或者使用 aria-disabled 属性筛选
create_btn = page.locator('button[aria-disabled="false"]:has(i:text("arrow_forward"))').first
```

---

## 完整操作流程

### 流程 1: 从零开始生成图片

```
1. 启动环境
   ├─ 启动 Chrome (CDP: 9222)
   ├─ 登录 Google 账号
   └─ 打开 Flow 项目页面

2. 添加参考图 #1
   ├─ 点击加号按钮 (230, 327)
   ├─ 选择 "Uploads" 分类
   ├─ 点击文件 "Luna_on_mars.png"
   └─ 点击 "Add to Prompt"

3. 添加参考图 #2
   ├─ 再次点击加号按钮
   ├─ 选择 "Uploads" 分类
   ├─ 点击文件 "Wayne_on_earth.png"
   └─ 点击 "Add to Prompt"

4. 输入 Prompt
   ├─ 点击输入框
   └─ 输入: "他们在中国杭州玩"

5. 提交生成
   └─ 点击 Create 按钮 (arrow_forward)

6. 等待结果
   ├─ 顶部显示生成进度 (10%, 20%, ...)
   └─ 完成后图片出现在网格中
```

### 流程 2: 使用搜索功能

```
1. 打开媒体选择器
   └─ 点击加号按钮

2. 使用搜索
   ├─ 点击搜索框
   ├─ 输入关键词 (如 "Luna")
   └─ 等待搜索结果

3. 从结果中选择
   ├─ 点击搜索结果中的文件
   └─ 点击 "Add to Prompt"

4. 继续后续步骤
   └─ (同流程 1 的步骤 4-6)
```

### 流程 3: 上传新文件并使用

```
1. 上传新文件
   ├─ 点击顶部 "Add Media" 按钮
   ├─ 选择 "Upload media"
   ├─ 选择本地文件
   └─ 等待上传完成

2. 添加刚上传的文件
   ├─ 点击加号按钮
   ├─ 选择 "Uploads" 分类
   ├─ 找到刚上传的文件
   └─ 点击 "Add to Prompt"

3. 继续生成流程
   └─ (同流程 1 的步骤 4-6)
```

---

## 常见问题

### Q1: 找不到文件名文本

**问题:** `page.locator('text="filename.png"')` 超时

**原因:**
- 媒体选择器未打开
- 在错误的分类中（如在 Images 而不是 Uploads）
- 文件名拼写错误

**解决方案:**
```python
# 1. 确保媒体选择器已打开
await page.mouse.click(230, 327)
await asyncio.sleep(2)

# 2. 确保在 Uploads 分类
await page.locator('text="Uploads"').first.click()
await asyncio.sleep(1)

# 3. 使用正则表达式模糊匹配
file = page.locator('text=/Luna.*mars/i').first
await file.click()

# 4. 或者先截图调试
await page.screenshot(path='/tmp/debug.png')
```

### Q2: 点击 Create 后没有反应

**问题:** 点击 Create 按钮后没有开始生成

**原因:**
- 点击了错误的 Create 按钮（#17 而不是 #23）
- 按钮处于禁用状态 (aria-disabled="true")
- Prompt 未输入

**解决方案:**
```python
# 1. 确保使用正确的按钮（带箭头的）
create_btn = page.locator('button:has(i:text("arrow_forward"))').first

# 2. 检查按钮状态
is_disabled = await create_btn.get_attribute('aria-disabled')
if is_disabled == 'true':
    print("按钮被禁用，请检查是否已输入 Prompt")

# 3. 确保 Prompt 已输入
input_box = page.locator('[contenteditable="true"]').first
await input_box.fill("你的 prompt")
await asyncio.sleep(1)

# 4. 然后再点击
await create_btn.click()
```

### Q3: 媒体选择器显示卡片视图而不是列表

**问题:** 打开后显示的是图片卡片网格，而不是文件名列表

**原因:**
- 误点了侧边栏的 "Uploads" 而不是加号按钮
- 或者点击了顶部的 "Add Media"

**解决方案:**
```python
# 1. 按 ESC 返回主界面
await page.keyboard.press('Escape')
await asyncio.sleep(1)

# 2. 确保点击的是输入框旁边的加号
await page.mouse.click(230, 327)  # 使用坐标点击
await asyncio.sleep(2)

# 3. 应该会看到左侧分类列表
# 如果还是不对，截图查看状态
await page.screenshot(path='/tmp/check_picker.png')
```

### Q4: 参考图没有添加成功

**问题:** 点击 "Add to Prompt" 后，输入框区域没有显示缩略图

**原因:**
- 点击了错误的按钮
- 媒体选择器意外关闭
- 文件未正确选中

**解决方案:**
```python
# 1. 点击文件后，等待选中状态
file = page.locator('text=/Luna.*mars/i').first
await file.click()
await asyncio.sleep(1)

# 2. 截图确认文件已选中（右侧应显示预览）
await page.screenshot(path='/tmp/file_selected.png')

# 3. 确保点击的是底部的大按钮
add_btn = page.locator('button:has-text("Add to Prompt")').first
# 检查按钮是否可见
is_visible = await add_btn.is_visible()
if not is_visible:
    print("Add to Prompt 按钮不可见")

# 4. 点击并等待
await add_btn.click()
await asyncio.sleep(2)

# 5. 验证是否添加成功（检查输入框区域是否有缩略图）
await page.screenshot(path='/tmp/after_add.png')
```

### Q5: Chrome 调试端口连接失败

**问题:** `connect ECONNREFUSED 127.0.0.1:9222`

**原因:**
- Chrome 未启动
- Chrome 启动时未使用 `--remote-debugging-port=9222`
- 使用了系统 profile（调试端口无法打开）

**解决方案:**
```bash
# 1. 完全关闭 Chrome
killall "Google Chrome"
sleep 2

# 2. 使用正确的命令重新启动
/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome \
  --remote-debugging-port=9222 \
  --user-data-dir="/tmp/flow_chrome_debug" &

# 3. 等待 5 秒让 Chrome 启动
sleep 5

# 4. 验证端口是否打开
curl http://127.0.0.1:9222/json/version

# 5. 然后运行脚本
python3 flow_automation_final.py
```

---

## 附录

### A. 选择器速查表

| 目标元素 | 推荐选择器 | 备选方案 |
|----------|-----------|----------|
| 加号按钮 | `page.mouse.click(230, 327)` | `page.locator('button:has-text("+")').first` |
| Uploads 分类 | `page.locator('text="Uploads"').first` | - |
| 文件列表项 | `page.locator('text=/filename/i').first` | `page.locator('text="exact_filename.png"')` |
| Add to Prompt | `page.locator('button:has-text("Add to Prompt")').first` | - |
| 输入框 | `page.locator('[contenteditable="true"]').first` | `page.locator('textarea').first` |
| Create 按钮 | `page.locator('button:has(i:text("arrow_forward"))').first` | `page.locator('button[aria-disabled="false"]:has-text("Create")').filter(has=page.locator('i:text("arrow_forward")'))` |

### B. 等待时间参考

| 操作 | 推荐等待时间 | 说明 |
|------|-------------|------|
| 点击加号 | 2-3秒 | 等待媒体选择器打开 |
| 切换分类 | 1-2秒 | 等待文件列表加载 |
| 选择文件 | 1秒 | 等待预览加载 |
| Add to Prompt | 2秒 | 等待添加完成并关闭 |
| 输入 Prompt | 1秒 | 等待输入稳定 |
| 点击 Create | 3秒 | 等待生成请求提交 |
| 页面导航 | 3-5秒 | 等待 networkidle |

### C. 调试检查清单

运行脚本前检查：

- [ ] Chrome 进程运行中
- [ ] 端口 9222 可访问 (`curl http://127.0.0.1:9222/json/version`)
- [ ] Google 账号已登录
- [ ] 在 Flow 项目页面
- [ ] 参考图已上传到 Uploads
- [ ] Playwright 和依赖已安装

遇到问题时：

1. [ ] 在每个关键步骤后截图
2. [ ] 检查选择器是否正确
3. [ ] 验证元素是否可见/可点击
4. [ ] 增加等待时间
5. [ ] 查看浏览器控制台错误

---

**文档版本:** 1.0
**更新日期:** 2026-05-24
**适用版本:** Google Flow (May 2026)
