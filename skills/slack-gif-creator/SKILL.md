---
name: slack-gif-creator
description: 用于创建优化用于Slack的动画GIF的知识和工具。提供约束条件、验证工具和动画概念。当用户请求为Slack创建动画GIF时使用，例如"为我创建一个X做Y的GIF用于Slack"。
license: Complete terms in LICENSE.txt
---

# Slack GIF 创建工具包

提供用于创建优化用于Slack的动画GIF的工具和知识。

## Slack 要求

**尺寸：**
- 表情GIF：128x128（推荐）
- 消息GIF：480x480

**参数：**
- 帧率：10-30（越低文件越小）
- 颜色数：48-128（越少文件越小）
- 持续时间：表情GIF保持在3秒以内

## 核心工作流程

```python
from core.gif_builder import GIFBuilder
from PIL import Image, ImageDraw

# 1. 创建构建器
builder = GIFBuilder(width=128, height=128, fps=10)

# 2. 生成帧
for i in range(12):
    frame = Image.new('RGB', (128, 128), (240, 248, 255))
    draw = ImageDraw.Draw(frame)

    # 使用PIL图元绘制动画
    # （圆形、多边形、线条等）

    builder.add_frame(frame)

# 3. 保存并优化
builder.save('output.gif', num_colors=48, optimize_for_emoji=True)
```

## 绘制图形

### 处理用户上传的图片
如果用户上传了图片，考虑他们是否想要：
- **直接使用**（例如"制作这个的动画"、"把这个分成帧"）
- **作为参考**（例如"制作一个类似的"）

使用PIL加载和处理图片：
```python
from PIL import Image

uploaded = Image.open('file.png')
# 直接使用，或仅作为颜色/风格的参考
```

### 从零开始绘制
从零开始绘制图形时，使用PIL ImageDraw图元：

```python
from PIL import ImageDraw

draw = ImageDraw.Draw(frame)

# 圆形/椭圆
draw.ellipse([x1, y1, x2, y2], fill=(r, g, b), outline=(r, g, b), width=3)

# 星星、三角形、任意多边形
points = [(x1, y1), (x2, y2), (x3, y3), ...]
draw.polygon(points, fill=(r, g, b), outline=(r, g, b), width=3)

# 线条
draw.line([(x1, y1), (x2, y2)], fill=(r, g, b), width=5)

# 矩形
draw.rectangle([x1, y1, x2, y2], fill=(r, g, b), outline=(r, g, b), width=3)
```

**不要使用：** 表情字体（在不同平台上不可靠）或假设此技能中预置有图形。

### 让图形更好看

图形应该看起来精致且有创意，而不是基础的。以下是方法：

**使用更粗的线条** - 始终为轮廓和线条设置`width=2`或更高。细线条（width=1）看起来不流畅且不专业。

**添加视觉深度**：
- 为背景使用渐变（`create_gradient_background`）
- 多层叠加形状以增加复杂度（例如：内部带有小星星的星星）

**让形状更有趣**：
- 不要只画普通的圆形 - 添加高光环、圆环或图案
- 星星可以有光晕（在后面绘制较大的半透明版本）
- 组合多个形状（星星+闪光点，圆环+光环）

**注意颜色搭配**：
- 使用鲜艳、互补的颜色
- 添加对比度（浅色形状上的深色轮廓，深色形状上的浅色轮廓）
- 考虑整体构图

**对于复杂形状**（心形、雪花等）：
- 使用多边形和椭圆的组合
- 仔细计算点以保持对称性
- 添加细节（心形可以有高光线，雪花可以有复杂的分支）

要有创意且注重细节！一个好的Slack GIF应该看起来精致，而不是像占位符图形。

## 可用工具

### GIFBuilder (`core.gif_builder`)
组装帧并优化用于Slack：
```python
builder = GIFBuilder(width=128, height=128, fps=10)
builder.add_frame(frame)  # 添加PIL图像
builder.add_frames(frames)  # 添加帧列表
builder.save('out.gif', num_colors=48, optimize_for_emoji=True, remove_duplicates=True)
```

### 验证器 (`core.validators`)
检查GIF是否符合Slack要求：
```python
from core.validators import validate_gif, is_slack_ready

# 详细验证
passes, info = validate_gif('my.gif', is_emoji=True, verbose=True)

# 快速检查
if is_slack_ready('my.gif'):
    print("就绪！")
```

### 缓动函数 (`core.easing`)
实现平滑运动而非线性运动：
```python
from core.easing import interpolate

# 进度从0.0到1.0
t = i / (num_frames - 1)

# 应用缓动
y = interpolate(start=0, end=400, t=t, easing='ease_out')

# 可用选项：linear、ease_in、ease_out、ease_in_out、
#          bounce_out、elastic_out、back_out
```

### 帧辅助函数 (`core.frame_composer`)
满足常见需求的便捷函数：
```python
from core.frame_composer import (
    create_blank_frame,          # 纯色背景
    create_gradient_background,  # 垂直渐变
    draw_circle,                 # 圆形辅助函数
    draw_text,                   # 简单文本渲染
    draw_star                    # 五角星
)
```

## 动画概念

### 震动/振动
使用振荡偏移对象位置：
- 将`math.sin()`或`math.cos()`与帧索引结合使用
- 添加小的随机变化以获得自然感
- 应用于x和/或y位置

### 脉冲/心跳
有节奏地缩放对象大小：
- 使用`math.sin(t * frequency * 2 * math.pi)`实现平滑脉冲
- 对于心跳：两次快速脉冲然后暂停（调整正弦波）
- 在基础大小的0.8到1.2之间缩放

### 弹跳
对象下落并弹起：
- 使用带有`easing='bounce_out'`的`interpolate()`实现落地效果
- 对下落使用`easing='ease_in'`（加速）
- 通过每帧增加y速度来模拟重力

### 旋转
围绕中心旋转对象：
- PIL：`image.rotate(angle, resample=Image.BICUBIC)`
- 对于摇摆：使用正弦波计算角度而非线性增加

### 淡入/淡出
逐渐出现或消失：
- 创建RGBA图像，调整alpha通道
- 或使用`Image.blend(image1, image2, alpha)`
- 淡入：alpha从0到1
- 淡出：alpha从1到0

### 滑动
将对象从屏幕外移动到位置：
- 起始位置：框架边界之外
- 结束位置：目标位置
- 使用带有`easing='ease_out'`的`interpolate()`实现平滑停止
- 对于过冲：使用`easing='back_out'`

### 缩放
缩放和定位以实现缩放效果：
- 放大：从0.1缩放到2.0，裁剪中心
- 缩小：从2.0缩放到1.0
- 可以添加运动模糊以增强戏剧性（PIL滤镜）

### 爆炸/粒子爆发
创建向外辐射的粒子：
- 生成具有随机角度和速度的粒子
- 更新每个粒子：`x += vx`，`y += vy`
- 添加重力：`vy += gravity_constant`
- 粒子随时间淡出（减少alpha）

## 优化策略

仅当被要求减小文件大小时，实施以下几种方法：

1. **减少帧数** - 更低的帧率（10而不是20）或更短持续时间
2. **减少颜色数** - `num_colors=48`而不是128
3. **更小尺寸** - 128x128而不是480x480
4. **移除重复帧** - 在save()中使用`remove_duplicates=True`
5. **表情模式** - `optimize_for_emoji=True`自动优化

```python
# 表情的最大程度优化
builder.save(
    'emoji.gif',
    num_colors=48,
    optimize_for_emoji=True,
    remove_duplicates=True
)
```

## 设计理念

此技能提供：
- **知识**：Slack的要求和动画概念
- **工具**：GIFBuilder、验证器、缓动函数
- **灵活性**：使用PIL图元创建动画逻辑

它不提供：
- 僵化的动画模板或预制函数
- 表情字体渲染（在不同平台上不可靠）
- 技能内置的预制图形库

**关于用户上传的说明**：此技能不包含预置图形，但如果用户上传了图片，使用PIL加载并处理它 - 根据他们的请求判断是要直接使用还是仅作为参考。

要有创意！组合各种概念（弹跳+旋转、脉冲+滑动等）并充分利用PIL的功能。

## 依赖项

```bash
pip install pillow imageio numpy
```
