#!/usr/bin/env python3
"""
burn_subtitles.py — 将中文 SRT 字幕烧录进视频，并可在第一秒叠加标题。

用法：
    python scripts/burn_subtitles.py \\
        --input clip.mp4 \\
        --srt clip.zh.srt \\
        --font ./youtube/ZITI.ttf \\
        --output clip.hardsub.mp4 \\
        [--title "标题文字"] \\
        [--font-size 48] \\
        [--outline 3]

依赖：ffmpeg（系统已安装，需支持 libass）

行为：
    - 使用 ffmpeg subtitles filter 烧录字幕（硬字幕）
    - 若指定 --title，在视频第一秒居中叠加标题文字
      - 字号：--font-size（默认 48）
      - 描边：--outline（默认 3）
      - 字体：--font 指定的 TTF 文件
    - 重新编码输出为 MP4（libx264 + aac）
"""

import sys
import subprocess
import argparse
import shutil
import os


def check_ffmpeg():
    if not shutil.which("ffmpeg"):
        print("错误：未找到 ffmpeg，请先安装。", file=sys.stderr)
        sys.exit(1)


def escape_filter_path(path: str) -> str:
    """转义 ffmpeg filter 中的路径（冒号和反斜杠需转义）。"""
    path = os.path.abspath(path)
    path = path.replace("\\", "/")
    path = path.replace(":", "\\:")
    return path


def build_drawtext_filter(title: str, font_path: str, font_size: int, outline: int) -> str:
    """构建 drawtext filter 字符串，标题在第一秒居中显示。"""
    # 转义标题中的特殊字符
    title_escaped = (
        title
        .replace("\\", "\\\\")
        .replace("'", "\\'")
        .replace(":", "\\:")
    )
    font_escaped = escape_filter_path(font_path)

    return (
        f"drawtext="
        f"fontfile='{font_escaped}':"
        f"text='{title_escaped}':"
        f"fontsize={font_size}:"
        f"fontcolor=white:"
        f"borderw={outline}:"
        f"bordercolor=black:"
        f"x=(w-text_w)/2:"
        f"y=(h-text_h)/2:"
        f"enable='between(t,0,1)'"
    )


def main():
    parser = argparse.ArgumentParser(description="烧录中文字幕并叠加标题")
    parser.add_argument("--input", "-i", required=True, help="输入视频文件")
    parser.add_argument("--srt", required=True, help="中文 SRT 字幕文件")
    parser.add_argument("--font", required=True, help="字体文件路径（TTF）")
    parser.add_argument("--output", "-o", required=True, help="输出视频文件")
    parser.add_argument("--title", default="", help="叠加在第一秒的标题文字（可选）")
    parser.add_argument("--font-size", type=int, default=48, help="字幕/标题字号（默认 48）")
    parser.add_argument("--outline", type=int, default=3, help="描边宽度（默认 3）")
    args = parser.parse_args()

    check_ffmpeg()

    for path in [args.input, args.srt, args.font]:
        if not os.path.exists(path):
            print(f"错误：文件不存在：{path}", file=sys.stderr)
            sys.exit(1)

    srt_path_escaped = escape_filter_path(args.srt)
    font_path_escaped = escape_filter_path(args.font)

    # 构建字幕 filter
    subtitle_filter = (
        f"subtitles='{srt_path_escaped}':"
        f"force_style='FontName={os.path.basename(args.font).replace('.ttf','').replace('.TTF','')},"
        f"FontSize={args.font_size},"
        f"PrimaryColour=&H00FFFFFF,"
        f"OutlineColour=&H00000000,"
        f"Outline={args.outline},"
        f"Alignment=2'"
        f":fontsdir='{os.path.dirname(os.path.abspath(args.font))}'"
    )

    # 组合 filter chain
    if args.title:
        drawtext = build_drawtext_filter(
            args.title, args.font, args.font_size, args.outline
        )
        vf = f"{subtitle_filter},{drawtext}"
    else:
        vf = subtitle_filter

    cmd = [
        "ffmpeg",
        "-y",
        "-i", args.input,
        "-vf", vf,
        "-c:v", "libx264",
        "-preset", "fast",
        "-crf", "18",
        "-c:a", "aac",
        "-b:a", "128k",
        "-movflags", "+faststart",
        args.output,
    ]

    print(f"烧录字幕：{args.srt}", file=sys.stderr)
    if args.title:
        print(f"叠加标题（第1秒）：{args.title}", file=sys.stderr)

    result = subprocess.run(cmd, capture_output=True, text=True)

    if result.returncode != 0:
        print("ffmpeg 错误：", file=sys.stderr)
        print(result.stderr, file=sys.stderr)
        sys.exit(result.returncode)

    print(f"已输出：{args.output}", file=sys.stderr)


if __name__ == "__main__":
    main()
