# Flow CLI - Google Flow 自动化工具

自动化 Google Flow 图片和视频生成的 Python 脚本集合。

## ✨ 特点

- ✅ **完全自动化** - 从添加角色到生成提交
- ✅ **稳定可靠** - 使用语义选择器，不依赖坐标
- ✅ **支持缩放** - 页面 zoom 不影响
- ✅ **图片 + 视频** - 两种模式都支持

## 🚀 快速开始

### 1. 启动 Chrome

```bash
./scripts/start_chrome.sh
```

### 2. 在浏览器中

- 登录 Google 账号
- 打开你的 Flow 项目页面

### 3. 生成图片

```bash
python3 scripts/flow_automation_at_method.py
```

### 4. 生成视频

```bash
python3 scripts/flow_video_at_method.py
```

## 📜 核心脚本

| 脚本 | 功能 | 状态 |
|------|------|------|
| `flow_automation_at_method.py` | 图片生成（@ 方式） | ✅ 稳定 |
| `flow_video_at_method.py` | 视频生成（@ 方式） | ✅ 稳定 |
| `download_video.py` | 下载生成内容 | ✅ 可用 |
| `start_chrome.sh` | 启动 Chrome（调试模式） | ✅ 必需 |

## ⚙️ 配置

### 图片生成配置

编辑 `scripts/flow_automation_at_method.py`:

```python
CHARACTERS = ["luna", "wayne"]
PROMPT = "Luna 是一只白色兔子，Wayne 是一只猫，他们在北京长城玩，中国风"
```

### 视频生成配置

编辑 `scripts/flow_video_at_method.py`:

```python
CHARACTERS = ["luna", "wayne"]
MOTION_PROMPT = "Luna 是兔子，Wayne 是猫，他们在海边奔跑，日式动漫风格"
```

## ⚠️ 重要注意事项

### 1. 必须明确说明角色物种

**Luna** = 白色兔子 🐰
**Wayne** = 猫 🐱（不是狗！）

Flow 无法准确识别角色物种，必须在 Prompt 中明确说明：

```python
# ✅ 正确
PROMPT = "Luna 是兔子，Wayne 是猫，他们在玩"

# ❌ 错误
PROMPT = "Luna 和 Wayne 在玩"  # 没说是什么动物
```

### 2. Prompt 必须单行

```python
# ✅ 正确
PROMPT = "Luna 是兔子，Wayne 是猫，在大峡谷玩，日式风格"

# ❌ 错误 - 换行会导致提前提交
PROMPT = """Luna 是兔子
Wayne 是猫
在大峡谷玩"""
```

### 3. 不要使用坐标方式

旧版脚本使用坐标点击（已归档）：
- ❌ 页面缩放会失效
- ❌ 窗口大小改变会失效
- ❌ 非常不稳定

新版脚本使用语义选择器：
- ✅ `get_by_role()`
- ✅ 基于元素角色和文本
- ✅ 稳定可靠

## 📚 文档

- **完整 Skill 文档**: `.claude/skills/flow-automation-complete.md`
- **项目记忆**: `CLAUDE.md`
- **界面参考**: `docs/FLOW_SKILL.md`

## 🔧 技术栈

- **Python** - 脚本语言
- **Playwright** - 浏览器自动化
- **CDP** - Chrome DevTools Protocol
- **端口** - 9222

## 📁 项目结构

```
flow-cli/
├── scripts/                    # 核心脚本
│   ├── flow_automation_at_method.py    # 图片生成 ⭐
│   ├── flow_video_at_method.py         # 视频生成 ⭐
│   ├── download_video.py               # 下载工具
│   └── start_chrome.sh                 # Chrome 启动
├── downloads/                  # 下载目录
├── docs/                       # 文档
│   └── FLOW_SKILL.md          # 界面参考
├── .claude/skills/            # Skill 文档
│   └── flow-automation-complete.md    # 完整指南 ⭐
└── archive/                    # 归档（旧版本）
```

## 💡 使用示例

### 生成图片：东方明珠塔

```python
# 编辑 flow_automation_at_method.py
CHARACTERS = ["luna", "wayne"]
PROMPT = "Luna 是白兔，Wayne 是猫，他们在上海东方明珠塔下玩，现代都市风"
```

```bash
python3 scripts/flow_automation_at_method.py
```

### 生成视频：大峡谷探险

```python
# 编辑 flow_video_at_method.py
CHARACTERS = ["luna", "wayne"]
MOTION_PROMPT = "Luna 是兔子，Wayne 是猫，在大峡谷探险，日式动漫风格"
```

```bash
python3 scripts/flow_video_at_method.py
# 等待约 2 分钟
python3 scripts/download_video.py
```

## 🐛 故障排查

### Chrome 连接失败

```bash
# 检查端口
lsof -i :9222

# 重启 Chrome
killall "Google Chrome"
./scripts/start_chrome.sh
```

### 找不到角色

1. 确保已在 Flow 中创建 Character（luna, wayne）
2. 检查角色名称拼写
3. 查看截图：`/tmp/*.png`

### 生成结果不对

1. 检查 Prompt 是否明确说明了物种
2. 确保 Prompt 是单行（无换行）
3. 等待时间是否充足

## 📝 更新日志

### 2024-05-24 - v2.0
- ✅ 移除所有坐标方式
- ✅ 使用 `get_by_role()` 语义选择器
- ✅ 归档旧脚本
- ✅ 创建完整 Skill 文档
- ⚠️ 强调必须说明角色物种

## 🤝 贡献

欢迎提交 Issues 和 Pull Requests！

## 📄 License

MIT

## 👥 作者

Claude + User

---

**⭐ Star this repo if you find it useful!**
