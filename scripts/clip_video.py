#!/usr/bin/env python3
"""
clip_video.py — 从源视频精确切取一段并重新编码为 MP4。

用法：
    python scripts/clip_video.py \\
        --input original.mp4 \\
        --start <start_seconds> \\
        --end <end_seconds> \\
        --output clip.mp4

依赖：ffmpeg（系统已安装）

行为：
    - 使用 -ss / -to 精确定位（输入端 seek + 输出端截断）
    - 重新编码（libx264 + aac），确保帧精度
    - 视频保持原始分辨率和帧率
"""

import sys
import subprocess
import argparse
import shutil


def check_ffmpeg():
    if not shutil.which("ffmpeg"):
        print("错误：未找到 ffmpeg，请先安装。", file=sys.stderr)
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(description="精确切取视频片段并重新编码")
    parser.add_argument("--input", "-i", required=True, help="输入视频文件")
    parser.add_argument("--start", "-s", required=True, type=float, help="开始时间（秒）")
    parser.add_argument("--end", "-e", required=True, type=float, help="结束时间（秒）")
    parser.add_argument("--output", "-o", required=True, help="输出 MP4 文件")
    args = parser.parse_args()

    check_ffmpeg()

    duration = args.end - args.start
    if duration <= 0:
        print(f"错误：结束时间必须大于开始时间（{args.start}s → {args.end}s）", file=sys.stderr)
        sys.exit(1)

    cmd = [
        "ffmpeg",
        "-y",                        # 覆盖输出文件
        "-ss", str(args.start),      # 输入端 seek（快速）
        "-i", args.input,
        "-t", str(duration),         # 持续时长
        "-c:v", "libx264",
        "-preset", "fast",
        "-crf", "18",
        "-c:a", "aac",
        "-b:a", "128k",
        "-movflags", "+faststart",
        args.output,
    ]

    print(f"切片：{args.start}s → {args.end}s ({duration:.1f}s)", file=sys.stderr)
    result = subprocess.run(cmd, capture_output=True, text=True)

    if result.returncode != 0:
        print("ffmpeg 错误：", file=sys.stderr)
        print(result.stderr, file=sys.stderr)
        sys.exit(result.returncode)

    print(f"已输出：{args.output}", file=sys.stderr)


if __name__ == "__main__":
    main()
