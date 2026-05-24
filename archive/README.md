# Archive - 失败的尝试

这个目录包含了在开发过程中失败的尝试和方案。记录失败原因以便将来参考。

## 失败方案列表

### 1. 使用顶部 "Add Media" 按钮

**文件:** `wrong_add_media_approach.md`

**尝试内容:**
- 点击顶部工具栏的 "Add Media" 按钮
- 期望打开媒体选择器添加参考图

**失败原因:**
- ❌ "Add Media" 按钮是用来**创建/上传**新媒体的
- ❌ 不是添加参考图到 Prompt 的入口
- ❌ 点击后显示的是上传菜单，不是文件选择器

**正确方案:**
- ✅ 使用输入框左侧的加号按钮（坐标约 230, 327）

---

### 2. 使用系统 Chrome Profile

**文件:** `system_profile_attempt.py`

**尝试内容:**
```bash
--user-data-dir="$HOME/Library/Application Support/Google/Chrome"
```

**失败原因:**
- ❌ 系统 profile 启动时，调试端口无法打开
- ❌ `lsof -i :9222` 显示端口未监听
- ❌ ProcessSingleton 锁文件冲突

**错误信息:**
```
playwright._impl._errors.Error: BrowserType.connect_over_cdp: 
connect ECONNREFUSED ::1:9222
```

**正确方案:**
- ✅ 使用独立的测试 profile 目录
- ✅ `--user-data-dir="/tmp/flow_chrome_debug"`

---

### 3. 使用 Playwright Chrome for Testing

**文件:** `playwright_chrome_testing.py`

**尝试内容:**
```python
context = await p.chromium.launch_persistent_context(
    profile_dir,
    headless=False
)
```

**失败原因:**
- ❌ macOS 上遇到 SIGTRAP 错误
- ❌ 即使使用全新 profile 也会崩溃
- ❌ Playwright 的 Chrome for Testing 版本不稳定

**错误信息:**
```
signal=SIGTRAP
```

**正确方案:**
- ✅ 使用系统 Chrome + CDP 连接
- ✅ `executable_path="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"`

---

### 4. 通过侧边栏 Uploads 访问文件

**文件:** `sidebar_uploads_approach.py`

**尝试内容:**
- 点击左侧边栏的 "Uploads" 按钮
- 期望打开文件列表选择器

**失败原因:**
- ❌ 侧边栏 Uploads 打开的是**图片卡片网格视图**
- ❌ 不是文件列表视图
- ❌ 无法直接通过文件名选择

**看到的内容:**
```
┌────────┐  ┌────────┐  ┌────────┐
│ [图]   │  │ [图]   │  │ [图]   │
│ Luna   │  │ Kirin  │  │ Wayne  │
└────────┘  └────────┘  └────────┘
```

**正确方案:**
- ✅ 使用加号按钮打开的媒体选择器
- ✅ 媒体选择器显示的是文件列表（带文件名）

---

### 5. 使用复杂的 CSS 选择器

**文件:** `css_selector_approach.py`

**尝试内容:**
```python
selector = "#__next > div > div:nth-of-type(5) > div > div > div > div > div:nth-of-type(2) > div > div > button"
await page.click(selector)
```

**失败原因:**
- ❌ DOM 结构经常变化
- ❌ 选择器在页面更新后失效
- ❌ 不同页面状态下选择器不同

**错误信息:**
```
Timeout: element not found
```

**正确方案:**
- ✅ 使用文本选择器: `page.locator('text="Uploads"')`
- ✅ 使用坐标点击: `page.mouse.click(x, y)`
- ✅ 使用语义选择器: `button:has(i:text("arrow_forward"))`

---

### 6. 假设可以批量添加参考图

**文件:** `batch_add_attempt.py`

**尝试内容:**
- 在媒体选择器中选择多个文件
- 期望一次性添加所有参考图

**失败原因:**
- ❌ Flow 界面**不支持多选**
- ❌ 每次只能选择一个文件
- ❌ 必须重复打开选择器添加每个文件

**正确方案:**
- ✅ 循环添加每个参考图
- ✅ 每次添加后重新打开选择器

---

### 7. 使用按钮索引定位

**文件:** `button_index_approach.py`

**尝试内容:**
```python
add_media_btn = page.locator('button').nth(4)
await add_media_btn.click()
```

**失败原因:**
- ❌ 按钮索引在不同页面状态下会变化
- ❌ 对话框打开/关闭会改变按钮数量
- ❌ 不稳定，容易点错按钮

**遇到的问题:**
- 有时点击了 Agent 按钮而不是 Create
- 索引 #19 vs #23 容易混淆

**正确方案:**
- ✅ 使用图标特征选择: `button:has(i:text("arrow_forward"))`
- ✅ 使用属性过滤: `button[aria-disabled="false"]`

---

## 失败模式总结

### 选择器失败模式

| 失败类型 | 示例 | 原因 |
|---------|------|------|
| CSS 路径 | `#__next > div > ...` | DOM 结构变化 |
| 按钮索引 | `.nth(4)` | 索引不稳定 |
| 假设的文本 | `text="filename.png"` | 文本不在 DOM 中 |

### 环境失败模式

| 失败类型 | 示例 | 原因 |
|---------|------|------|
| Profile 冲突 | 系统 profile | ProcessSingleton 锁 |
| 浏览器版本 | Chrome for Testing | SIGTRAP 错误 |
| 端口冲突 | 9222 不可用 | 另一个实例占用 |

### 交互失败模式

| 失败类型 | 示例 | 原因 |
|---------|------|------|
| 点错按钮 | Add Media vs 加号 | 理解错误 |
| 批量操作 | 多选文件 | UI 不支持 |
| 视图混淆 | 卡片 vs 列表 | 入口不同 |

---

## 经验教训

### 1. 先手动操作，再自动化

❌ **错误做法:**
- 直接写脚本
- 凭假设编码
- 跳过验证步骤

✅ **正确做法:**
- 手动执行一遍完整流程
- 记录每个步骤
- 截图验证状态
- 然后转化为代码

### 2. 使用稳定的选择器

❌ **不稳定:**
- CSS 路径选择器
- 元素索引
- 假设的结构

✅ **稳定:**
- 文本内容
- 语义属性 (aria-label)
- 图标特征
- 坐标（固定分辨率）

### 3. 环境隔离很重要

❌ **问题:**
- 使用系统配置
- 共享资源
- 依赖特定状态

✅ **解决:**
- 独立的 profile
- 清理启动状态
- 可重复的环境

### 4. 充分的等待和验证

❌ **问题:**
- 等待时间不足
- 不验证中间状态
- 假设操作成功

✅ **解决:**
- 合理的等待时间
- 每步后截图
- 验证预期状态

---

## 调试技巧

### 1. 截图调试法

```python
# 每个关键步骤后截图
await page.screenshot(path=f'/tmp/step_{i}.png')
print(f"📸 已截图: step_{i}.png")
```

### 2. 元素检查法

```python
# 检查元素是否存在/可见
is_visible = await element.is_visible(timeout=2000)
print(f"元素可见: {is_visible}")

# 检查元素属性
aria_disabled = await element.get_attribute('aria-disabled')
print(f"禁用状态: {aria_disabled}")
```

### 3. 文本提取法

```python
# 提取页面文本帮助理解状态
page_text = await page.locator('body').inner_text()
lines = page_text.split('\n')[:20]
for line in lines:
    print(f"  {line.strip()}")
```

### 4. 坐标定位法

```python
# 先截图，然后在图片上标注坐标
box = await element.bounding_box()
if box:
    print(f"元素位置: ({int(box['x'])}, {int(box['y'])})")
```

---

**创建日期:** 2026-05-24
**作者:** 基于实际失败经验总结
