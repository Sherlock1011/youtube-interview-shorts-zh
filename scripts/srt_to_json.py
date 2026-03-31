#!/usr/bin/env python3
"""
srt_to_json.py — 将 SRT 字幕文件解析为 JSON 记录。

用法：
    python scripts/srt_to_json.py <input.srt> [--output output.json]
    python scripts/srt_to_json.py <input.srt> > output.json

每条记录包含：
    index         字幕序号（int）
    start         开始时间戳（SRT格式 HH:MM:SS,mmm）
    end           结束时间戳（SRT格式 HH:MM:SS,mmm）
    start_seconds 开始时间（浮点秒数）
    end_seconds   结束时间（浮点秒数）
    text          字幕文本
"""

import sys
import json
import re
import argparse


def timestamp_to_seconds(ts: str) -> float:
    """将 SRT 时间戳 HH:MM:SS,mmm 转换为浮点秒数。"""
    match = re.match(r"(\d+):(\d+):(\d+)[,.](\d+)", ts.strip())
    if not match:
        raise ValueError(f"无法解析时间戳：{ts!r}")
    h, m, s, ms = match.groups()
    return int(h) * 3600 + int(m) * 60 + int(s) + int(ms) / 1000


def parse_srt(content: str) -> list:
    """解析 SRT 文件内容，返回字幕记录列表。"""
    records = []
    # 按空行分割字幕块
    blocks = re.split(r"\n\s*\n", content.strip())

    for block in blocks:
        lines = block.strip().splitlines()
        if len(lines) < 3:
            continue

        # 第一行：序号
        try:
            index = int(lines[0].strip())
        except ValueError:
            continue

        # 第二行：时间戳
        timestamp_line = lines[1].strip()
        ts_match = re.match(
            r"([\d:,]+)\s+-->\s+([\d:,]+)", timestamp_line
        )
        if not ts_match:
            continue

        start_ts = ts_match.group(1)
        end_ts = ts_match.group(2)

        # 剩余行：字幕文本
        text = "\n".join(lines[2:]).strip()

        records.append({
            "index": index,
            "start": start_ts,
            "end": end_ts,
            "start_seconds": timestamp_to_seconds(start_ts),
            "end_seconds": timestamp_to_seconds(end_ts),
            "text": text,
        })

    return records


def main():
    parser = argparse.ArgumentParser(
        description="将 SRT 字幕文件解析为 JSON 记录"
    )
    parser.add_argument("input", help="输入 SRT 文件路径")
    parser.add_argument(
        "--output", "-o", help="输出 JSON 文件路径（默认输出到 stdout）"
    )
    args = parser.parse_args()

    with open(args.input, encoding="utf-8-sig") as f:
        content = f.read()

    records = parse_srt(content)

    output = json.dumps(records, ensure_ascii=False, indent=2)

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(output)
        print(f"已写入 {len(records)} 条记录到 {args.output}", file=sys.stderr)
    else:
        print(output)


if __name__ == "__main__":
    main()
