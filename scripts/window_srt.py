#!/usr/bin/env python3
"""
window_srt.py — 提取与指定时间窗口重叠的字幕条目，并将时间戳归零。

用法：
    python scripts/window_srt.py \\
        --input original.en.srt \\
        --start <start_seconds> \\
        --end <end_seconds> \\
        --output clip.en.srt

行为：
    - 选取与 [start, end] 窗口有任意重叠的字幕条目
    - 将所有时间戳减去 start_seconds，使新 SRT 从 00:00:00,000 开始
    - 截断超出窗口末尾的条目结束时间
    - 重新编号，从 1 开始
"""

import sys
import re
import argparse


def timestamp_to_seconds(ts: str) -> float:
    match = re.match(r"(\d+):(\d+):(\d+)[,.](\d+)", ts.strip())
    if not match:
        raise ValueError(f"无法解析时间戳：{ts!r}")
    h, m, s, ms = match.groups()
    return int(h) * 3600 + int(m) * 60 + int(s) + int(ms) / 1000


def seconds_to_timestamp(seconds: float) -> str:
    seconds = max(0.0, seconds)
    ms = round((seconds % 1) * 1000)
    total_s = int(seconds)
    s = total_s % 60
    m = (total_s // 60) % 60
    h = total_s // 3600
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def parse_srt(content: str) -> list:
    records = []
    blocks = re.split(r"\n\s*\n", content.strip())
    for block in blocks:
        lines = block.strip().splitlines()
        if len(lines) < 3:
            continue
        try:
            index = int(lines[0].strip())
        except ValueError:
            continue
        ts_match = re.match(r"([\d:,]+)\s+-->\s+([\d:,]+)", lines[1].strip())
        if not ts_match:
            continue
        start_ts, end_ts = ts_match.group(1), ts_match.group(2)
        text = "\n".join(lines[2:]).strip()
        records.append({
            "index": index,
            "start_seconds": timestamp_to_seconds(start_ts),
            "end_seconds": timestamp_to_seconds(end_ts),
            "text": text,
        })
    return records


def main():
    parser = argparse.ArgumentParser(
        description="提取字幕窗口并将时间戳归零"
    )
    parser.add_argument("--input", "-i", required=True, help="输入 SRT 文件")
    parser.add_argument("--start", "-s", required=True, type=float, help="窗口开始（秒）")
    parser.add_argument("--end", "-e", required=True, type=float, help="窗口结束（秒）")
    parser.add_argument("--output", "-o", required=True, help="输出 SRT 文件")
    args = parser.parse_args()

    with open(args.input, encoding="utf-8-sig") as f:
        content = f.read()

    records = parse_srt(content)

    # 筛选与窗口重叠的条目
    windowed = [
        r for r in records
        if r["start_seconds"] < args.end and r["end_seconds"] > args.start
    ]

    if not windowed:
        print(f"警告：在 {args.start}s ~ {args.end}s 范围内未找到字幕", file=sys.stderr)

    # 生成归零后的 SRT
    lines = []
    for new_index, r in enumerate(windowed, start=1):
        shifted_start = r["start_seconds"] - args.start
        shifted_end = min(r["end_seconds"], args.end) - args.start
        lines.append(str(new_index))
        lines.append(
            f"{seconds_to_timestamp(shifted_start)} --> {seconds_to_timestamp(shifted_end)}"
        )
        lines.append(r["text"])
        lines.append("")

    with open(args.output, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print(f"已写入 {len(windowed)} 条字幕到 {args.output}", file=sys.stderr)


if __name__ == "__main__":
    main()
