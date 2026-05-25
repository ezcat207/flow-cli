# 旧版脚本 - 坐标方式

这些脚本使用了**坐标点击**方式，已被更好的方法替代。

## 为什么被归档？

1. **坐标方式不稳定**
   - 页面缩放（zoom in/out）会失效
   - 窗口大小改变会失效
   - 页面布局变化会失效

2. **新方法更好**
   - 使用 `get_by_role()` 等语义选择器
   - 基于元素的角色和文本，不依赖位置
   - 更稳定、更易维护

## 归档的脚本

1. **flow_automation_final.py** - 加号方式生成图片（使用坐标 230, 327）
2. **flow_video_ingredients.py** - Ingredients 视频（使用坐标）
3. **flow_video_generation.py** - Frames 视频（使用坐标）

## 推荐使用

**新版脚本（无坐标）：**
- `scripts/flow_automation_at_method.py` - 图片生成（@ 方式）
- `scripts/flow_video_at_method.py` - 视频生成（@ 方式）

归档日期：2024-05-24
