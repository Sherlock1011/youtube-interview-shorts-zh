# Clip Schema Reference

`selected_clips.json` 的完整结构定义。

## 顶层结构

```json
{
  "source_url": "https://www.youtube.com/watch?v=XXXX",
  "video_slug": "video-slug",
  "clips": [ ... ]
}
```

## 单条 Clip 对象

```json
{
  "id": "01",
  "start": "00:03:12,400",
  "end": "00:05:47,800",
  "start_seconds": 192.4,
  "end_seconds": 347.8,
  "duration_seconds": 155.4,
  "working_title": "为什么大多数人永远不会成功",
  "summary": "嘉宾指出大多数人失败不是因为能力不足，而是因为从未真正承诺过一件事。他用亲身经历说明，专注力才是区分成败的关键变量。",
  "quality_signals": ["opinionated", "counterintuitive", "strong_opening"],
  "selected": false
}
```

## 字段说明

| 字段 | 类型 | 说明 |
|------|------|------|
| `id` | string | 两位数字，如 `"01"`、`"12"` |
| `start` | string | SRT 格式时间戳 `HH:MM:SS,mmm` |
| `end` | string | SRT 格式时间戳 `HH:MM:SS,mmm` |
| `start_seconds` | number | 浮点秒数，用于脚本参数 |
| `end_seconds` | number | 浮点秒数，用于脚本参数 |
| `duration_seconds` | number | `end_seconds - start_seconds` |
| `working_title` | string | 工作标题，可供用户审核参考 |
| `summary` | string | 恰好两句话：第一句说内容，第二句说价值 |
| `quality_signals` | array | 见下方枚举值 |
| `selected` | boolean | 用户确认后设为 `true` |

## quality_signals 枚举值

- `informative` — 有信息量
- `opinionated` — 有明确立场
- `counterintuitive` — 反常识
- `motivating` — 有激励性
- `memorable` — 有记忆点
- `emotionally_sharp` — 情感锐利
- `quotable` — 适合引用

## 约束

- `duration_seconds` 应在 20 ~ 180 秒之间
- `summary` 必须恰好两句，不多不少
- `end` 时间戳必须落在说话人完成完整句子之后
- clip 之间不应大量重叠（除非必要）
- 1 小时视频目标产出 10 ~ 15 条候选
