#!/usr/bin/env python3
"""
验证器 - 检查GIF是否符合Slack的要求。

这些验证器帮助确保您的GIF满足Slack的尺寸和维度限制。
"""

from pathlib import Path


def validate_gif(
    gif_path: str | Path, is_emoji: bool = True, verbose: bool = True
) -> tuple[bool, dict]:
    """
    验证GIF是否符合Slack要求（尺寸、大小、帧数）。

    参数:
        gif_path: GIF文件路径
        is_emoji: 对于表情符号为True（推荐128x128），对于消息GIF为False
        verbose: 打印验证详情

    返回:
        元组（通过验证: bool，结果: dict，包含所有详情）
    """
    from PIL import Image

    gif_path = Path(gif_path)

    if not gif_path.exists():
        return False, {"error": f"文件未找到: {gif_path}"}

    # 获取文件大小
    size_bytes = gif_path.stat().st_size
    size_kb = size_bytes / 1024
    size_mb = size_kb / 1024

    # 获取尺寸和帧信息
    try:
        with Image.open(gif_path) as img:
            width, height = img.size

            # 统计帧数
            frame_count = 0
            try:
                while True:
                    img.seek(frame_count)  # 定位到指定帧
                    frame_count += 1       # 增加帧计数
            except EOFError:
                pass  # 到达文件末尾

            # 获取持续时间
            try:
                duration_ms = img.info.get("duration", 100)  # 获取帧持续时间（毫秒）
                total_duration = (duration_ms * frame_count) / 1000  # 计算总持续时间（秒）
                fps = frame_count / total_duration if total_duration > 0 else 0  # 计算帧率
            except:
                total_duration = None
                fps = None

    except Exception as e:
        return False, {"error": f"读取GIF失败: {e}"}

    # 验证尺寸
    if is_emoji:
        optimal = width == height == 128  # 最优尺寸：128x128
        acceptable = width == height and 64 <= width <= 128  # 可接受尺寸：正方形且边长在64-128之间
        dim_pass = acceptable  # 尺寸是否通过
    else:
        aspect_ratio = (
            max(width, height) / min(width, height)
            if min(width, height) > 0
            else float("inf")
        )  # 计算宽高比
        dim_pass = aspect_ratio <= 2.0 and 320 <= min(width, height) <= 640  # 消息GIF的尺寸要求

    results = {
        "file": str(gif_path),
        "passes": dim_pass,
        "width": width,
        "height": height,
        "size_kb": size_kb,
        "size_mb": size_mb,
        "frame_count": frame_count,
        "duration_seconds": total_duration,
        "fps": fps,
        "is_emoji": is_emoji,
        "optimal": optimal if is_emoji else None,
    }

    # 如果verbose为True则打印信息
    if verbose:
        print(f"\n正在验证 {gif_path.name}:")
        print(
            f"  尺寸: {width}x{height}"
            + (
                f" ({'最优' if optimal else '可接受'})"
                if is_emoji and acceptable
                else ""
            )
        )
        print(
            f"  大小: {size_kb:.1f} KB"
            + (f" ({size_mb:.2f} MB)" if size_mb >= 1.0 else "")
        )
        print(
            f"  帧数: {frame_count}"
            + (f" @ {fps:.1f} fps ({total_duration:.1f}秒)" if fps else "")
        )

        if not dim_pass:
            print(
                f"  注意: {'表情符号应为128x128' if is_emoji else 'Slack的尺寸不寻常'}"
            )

        if size_mb > 5.0:
            print(f"  注意: 文件较大 - 建议减少帧数/颜色数")

    return dim_pass, results


def is_slack_ready(
    gif_path: str | Path, is_emoji: bool = True, verbose: bool = True
) -> bool:
    """
    快速检查GIF是否已准备好用于Slack。

    参数:
        gif_path: GIF文件路径
        is_emoji: 对于表情符号GIF为True，对于消息GIF为False
        verbose: 打印反馈信息

    返回:
        如果尺寸可接受则返回True
    """
    passes, _ = validate_gif(gif_path, is_emoji, verbose)  # 调用验证函数
    return passes  # 返回验证结果
