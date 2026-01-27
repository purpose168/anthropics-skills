#!/usr/bin/env python3
"""
帧组合器 - 将视觉元素组合成帧的工具函数库。

提供用于绘制形状、文本、表情符号以及将元素合成以创建动画帧的函数。
"""

from typing import Optional

import numpy as np
from PIL import Image, ImageDraw, ImageFont


def create_blank_frame(
    width: int, height: int, color: tuple[int, int, int] = (255, 255, 255)
) -> Image.Image:
    """
    创建具有纯色背景的空白帧。

    参数:
        width: 帧宽度
        height: 帧高度
        color: RGB颜色元组（默认：白色）

    返回:
        PIL图像
    """
    return Image.new("RGB", (width, height), color)


def draw_circle(
    frame: Image.Image,
    center: tuple[int, int],
    radius: int,
    fill_color: Optional[tuple[int, int, int]] = None,
    outline_color: Optional[tuple[int, int, int]] = None,
    outline_width: int = 1,
) -> Image.Image:
    """
    在帧上绘制圆形。

    参数:
        frame: 要绘制的PIL图像
        center: (x, y) 中心位置
        radius: 圆形半径
        fill_color: RGB填充颜色（None表示不填充）
        outline_color: RGB轮廓颜色（None表示无轮廓）
        outline_width: 轮廓宽度（像素）

    返回:
        修改后的帧
    """
    draw = ImageDraw.Draw(frame)
    x, y = center
    bbox = [x - radius, y - radius, x + radius, y + radius]  # 计算边界框
    draw.ellipse(bbox, fill=fill_color, outline=outline_color, width=outline_width)  # 绘制椭圆
    return frame


def draw_text(
    frame: Image.Image,
    text: str,
    position: tuple[int, int],
    color: tuple[int, int, int] = (0, 0, 0),
    centered: bool = False,
) -> Image.Image:
    """
    在帧上绘制文本。

    参数:
        frame: 要绘制的PIL图像
        text: 要绘制的文本
        position: (x, y) 位置（除非centered=True，否则为左上角）
        color: RGB文本颜色
        centered: 如果为True，则将文本居中于位置

    返回:
        修改后的帧
    """
    draw = ImageDraw.Draw(frame)

    # 使用Pillow的默认字体
    # 如果需要为表情符号更改字体，请在此处添加额外的逻辑
    font = ImageFont.load_default()

    if centered:
        bbox = draw.textbbox((0, 0), text, font=font)  # 获取文本边界框
        text_width = bbox[2] - bbox[0]                 # 计算文本宽度
        text_height = bbox[3] - bbox[1]                # 计算文本高度
        x = position[0] - text_width // 2              # 计算居中x坐标
        y = position[1] - text_height // 2             # 计算居中y坐标
        position = (x, y)                              # 更新位置

    draw.text(position, text, fill=color, font=font)  # 绘制文本
    return frame


def create_gradient_background(
    width: int,
    height: int,
    top_color: tuple[int, int, int],
    bottom_color: tuple[int, int, int],
) -> Image.Image:
    """
    创建垂直渐变背景。

    参数:
        width: 帧宽度
        height: 帧高度
        top_color: 顶部的RGB颜色
        bottom_color: 底部的RGB颜色

    返回:
        具有渐变效果的PIL图像
    """
    frame = Image.new("RGB", (width, height))
    draw = ImageDraw.Draw(frame)

    # 计算每行的颜色步长
    r1, g1, b1 = top_color
    r2, g2, b2 = bottom_color

    for y in range(height):
        # 插值计算颜色
        ratio = y / height
        r = int(r1 * (1 - ratio) + r2 * ratio)
        g = int(g1 * (1 - ratio) + g2 * ratio)
        b = int(b1 * (1 - ratio) + b2 * ratio)

        # 绘制水平线条
        draw.line([(0, y), (width, y)], fill=(r, g, b))

    return frame


def draw_star(
    frame: Image.Image,
    center: tuple[int, int],
    size: int,
    fill_color: tuple[int, int, int],
    outline_color: Optional[tuple[int, int, int]] = None,
    outline_width: int = 1,
) -> Image.Image:
    """
    绘制五角星。

    参数:
        frame: 要绘制的PIL图像
        center: (x, y) 中心位置
        size: 星星尺寸（外半径）
        fill_color: RGB填充颜色
        outline_color: RGB轮廓颜色（None表示无轮廓）
        outline_width: 轮廓宽度

    返回:
        修改后的帧
    """
    import math

    draw = ImageDraw.Draw(frame)
    x, y = center

    # 计算星星的顶点
    points = []
    for i in range(10):
        angle = (i * 36 - 90) * math.pi / 180  # 每36度一个点，从顶部开始
        radius = size if i % 2 == 0 else size * 0.4  # 在外径和内径之间交替
        px = x + radius * math.cos(angle)  # 计算x坐标
        py = y + radius * math.sin(angle)  # 计算y坐标
        points.append((px, py))

    # 绘制星星
    draw.polygon(points, fill=fill_color, outline=outline_color, width=outline_width)

    return frame
