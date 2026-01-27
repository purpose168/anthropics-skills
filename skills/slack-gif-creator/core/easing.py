#!/usr/bin/env python3
"""
缓动函数库 - 用于平滑动画的定时函数。

提供各种缓动函数以实现自然运动和时序效果。
所有函数接收一个值t（0.0到1.0）并返回缓动后的值（0.0到1.0）。
"""

import math


def linear(t: float) -> float:
    """线性插值（无缓动效果）。"""
    return t


def ease_in_quad(t: float) -> float:
    """二次缓入（开始缓慢，加速前进）。"""
    return t * t


def ease_out_quad(t: float) -> float:
    """二次缓出（开始快速，减速停止）。"""
    return t * (2 - t)


def ease_in_out_quad(t: float) -> float:
    """二次缓入缓出（开始和结束都缓慢）。"""
    if t < 0.5:
        return 2 * t * t
    return -1 + (4 - 2 * t) * t


def ease_in_cubic(t: float) -> float:
    """三次缓入（开始缓慢）。"""
    return t * t * t


def ease_out_cubic(t: float) -> float:
    """三次缓出（开始快速）。"""
    return (t - 1) * (t - 1) * (t - 1) + 1


def ease_in_out_cubic(t: float) -> float:
    """三次缓入缓出。"""
    if t < 0.5:
        return 4 * t * t * t
    return (t - 1) * (2 * t - 2) * (2 * t - 2) + 1


def ease_in_bounce(t: float) -> float:
    """弹跳缓入（弹跳式开始）。"""
    return 1 - ease_out_bounce(1 - t)


def ease_out_bounce(t: float) -> float:
    """弹跳缓出（弹跳式结束）。"""
    if t < 1 / 2.75:
        return 7.5625 * t * t
    elif t < 2 / 2.75:
        t -= 1.5 / 2.75
        return 7.5625 * t * t + 0.75
    elif t < 2.5 / 2.75:
        t -= 2.25 / 2.75
        return 7.5625 * t * t + 0.9375
    else:
        t -= 2.625 / 2.75
        return 7.5625 * t * t + 0.984375


def ease_in_out_bounce(t: float) -> float:
    """弹跳缓入缓出。"""
    if t < 0.5:
        return ease_in_bounce(t * 2) * 0.5
    return ease_out_bounce(t * 2 - 1) * 0.5 + 0.5


def ease_in_elastic(t: float) -> float:
    """弹性缓入（弹簧效果）。"""
    if t == 0 or t == 1:
        return t
    return -math.pow(2, 10 * (t - 1)) * math.sin((t - 1.1) * 5 * math.pi)


def ease_out_elastic(t: float) -> float:
    """弹性缓出（弹簧效果）。"""
    if t == 0 or t == 1:
        return t
    return math.pow(2, -10 * t) * math.sin((t - 0.1) * 5 * math.pi) + 1


def ease_in_out_elastic(t: float) -> float:
    """弹性缓入缓出。"""
    if t == 0 or t == 1:
        return t
    t = t * 2 - 1
    if t < 0:
        return -0.5 * math.pow(2, 10 * t) * math.sin((t - 0.1) * 5 * math.pi)
    return math.pow(2, -10 * t) * math.sin((t - 0.1) * 5 * math.pi) * 0.5 + 1


# 便捷映射表
EASING_FUNCTIONS = {
    "linear": linear,
    "ease_in": ease_in_quad,
    "ease_out": ease_out_quad,
    "ease_in_out": ease_in_out_quad,
    "bounce_in": ease_in_bounce,
    "bounce_out": ease_out_bounce,
    "bounce": ease_in_out_bounce,
    "elastic_in": ease_in_elastic,
    "elastic_out": ease_out_elastic,
    "elastic": ease_in_out_elastic,
}


def get_easing(name: str = "linear"):
    """根据名称获取缓动函数。"""
    return EASING_FUNCTIONS.get(name, linear)


def interpolate(start: float, end: float, t: float, easing: str = "linear") -> float:
    """
    在两个值之间进行带缓动的插值。

    参数:
        start: 起始值
        end: 结束值
        t: 进度（0.0到1.0）
        easing: 缓动函数名称

    返回:
        插值后的值
    """
    ease_func = get_easing(easing)  # 获取对应的缓动函数
    eased_t = ease_func(t)          # 应用缓动函数
    return start + (end - start) * eased_t  # 计算最终值


def ease_back_in(t: float) -> float:
    """回退缓入（在向前运动之前先轻微向后过冲）。"""
    c1 = 1.70158
    c3 = c1 + 1
    return c3 * t * t * t - c1 * t * t


def ease_back_out(t: float) -> float:
    """回退缓出（向前过冲然后回弹稳定）。"""
    c1 = 1.70158
    c3 = c1 + 1
    return 1 + c3 * pow(t - 1, 3) + c1 * pow(t - 1, 2)


def ease_back_in_out(t: float) -> float:
    """回退缓入缓出（两端都过冲）。"""
    c1 = 1.70158
    c2 = c1 * 1.525
    if t < 0.5:
        return (pow(2 * t, 2) * ((c2 + 1) * 2 * t - c2)) / 2
    return (pow(2 * t - 2, 2) * ((c2 + 1) * (t * 2 - 2) + c2) + 2) / 2


def apply_squash_stretch(
    base_scale: tuple[float, float], intensity: float, direction: str = "vertical"
) -> tuple[float, float]:
    """
    计算挤压和拉伸比例以实现更动态的动画效果。

    参数:
        base_scale: (width_scale, height_scale) 基础缩放比例
        intensity: 挤压/拉伸强度（0.0-1.0）
        direction: 'vertical'（垂直）、'horizontal'（水平）或'both'（两者）

    返回:
        应用挤压/拉伸后的(width_scale, height_scale)
    """
    width_scale, height_scale = base_scale

    if direction == "vertical":
        # 垂直方向压缩，水平方向扩展（保持体积感）
        height_scale *= 1 - intensity * 0.5
        width_scale *= 1 + intensity * 0.5
    elif direction == "horizontal":
        # 水平方向压缩，垂直方向扩展
        width_scale *= 1 - intensity * 0.5
        height_scale *= 1 + intensity * 0.5
    elif direction == "both":
        # 整体挤压（两个方向都压缩）
        width_scale *= 1 - intensity * 0.3
        height_scale *= 1 - intensity * 0.3

    return (width_scale, height_scale)


def calculate_arc_motion(
    start: tuple[float, float], end: tuple[float, float], height: float, t: float
) -> tuple[float, float]:
    """
    计算抛物线弧线路径上的位置（自然运动路径）。

    参数:
        start: (x, y) 起始位置
        end: (x, y) 结束位置
        height: 中点处的弧高（正值为向上）
        t: 进度（0.0-1.0）

    返回:
        弧线路径上的(x, y)位置
    """
    x1, y1 = start
    x2, y2 = end

    # 线性插值计算x坐标
    x = x1 + (x2 - x1) * t

    # 抛物线插值计算y坐标
    # y = start + progress * (end - start) + arc_offset
    # 弧线偏移量在t=0.5处达到峰值
    arc_offset = 4 * height * t * (1 - t)
    y = y1 + (y2 - y1) * t - arc_offset

    return (x, y)


# 将新的缓动函数添加到便捷映射表中
EASING_FUNCTIONS.update(
    {
        "back_in": ease_back_in,
        "back_out": ease_back_out,
        "back_in_out": ease_back_in_out,
        "anticipate": ease_back_in,  # 别名：预演
        "overshoot": ease_back_out,  # 别名：过冲
    }
)
