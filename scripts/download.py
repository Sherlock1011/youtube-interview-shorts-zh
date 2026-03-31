#!/usr/bin/env python3
"""
download.py — 使用 yt-dlp 下载 YouTube 视频、英文字幕和缩略图。

用法：
    python youtube/download.py <URL> --output <output_dir>

依赖：
    pip install yt-dlp

行为：
    - 下载最佳质量视频（MP4）
    - 下载英文字幕（.en.srt，优先手动字幕，回退到自动生成）
    - 下载缩略图（.jpg）
    - 使用浏览器 cookies（--cookies-from-browser chrome）
    - 输出文件名：original.mp4, original.en.srt, original.jpg
"""

import sys
import subprocess
import argparse
import shutil
import os


def check_ytdlp():
    if not shutil.which("yt-dlp"):
        print("错误：未找到 yt-dlp，请先安装：", file=sys.stderr)
        print("  pip install yt-dlp", file=sys.stderr)
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        description="下载 YouTube 视频、英文字幕和缩略图"
    )
    parser.add_argument("url", help="YouTube 视频 URL")
    parser.add_argument(
        "--output", "-o", required=True, help="输出目录"
    )
    parser.add_argument(
        "--cookies-from-browser",
        default="chrome",
        help="从浏览器读取 cookies（默认 chrome，可选 firefox/edge/safari）",
    )
    args = parser.parse_args()

    check_ytdlp()

    os.makedirs(args.output, exist_ok=True)

    output_template = os.path.join(args.output, "original.%(ext)s")

    cmd = [
        "yt-dlp",
        args.url,
        "--cookies-from-browser", args.cookies_from_browser,
        # 视频格式：最佳质量 MP4
        "--format", "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best",
        "--merge-output-format", "mp4",
        # 字幕：英文（优先手动，回退自动生成）
        "--write-subs",
        "--write-auto-subs",
        "--sub-langs", "en",
        "--sub-format", "srt",
        "--convert-subs", "srt",
        # 缩略图
        "--write-thumbnail",
        "--convert-thumbnails", "jpg",
        # 输出文件名
        "--output", output_template,
    ]

    print(f"下载：{args.url}", file=sys.stderr)
    print(f"输出到：{args.output}", file=sys.stderr)
    print(f"使用 cookies：{args.cookies_from_browser}", file=sys.stderr)

    result = subprocess.run(cmd)

    if result.returncode != 0:
        print("\n下载失败。可能原因：", file=sys.stderr)
        print("  1. cookies 已过期，请刷新浏览器登录状态", file=sys.stderr)
        print("  2. 视频不可用或需要会员", file=sys.stderr)
        print(f"  3. 尝试其他浏览器：--cookies-from-browser firefox", file=sys.stderr)
        sys.exit(result.returncode)

    print("\n下载完成。检查输出文件：", file=sys.stderr)
    for f in os.listdir(args.output):
        print(f"  {f}", file=sys.stderr)


if __name__ == "__main__":
    main()
