---
name: youtube-interview-shorts-zh
description: Use when the user invokes /youtube-interview-shorts-zh with a YouTube URL to convert a long interview or podcast into multiple short clips with Chinese hard subtitles.
---

# YouTube Interview → Chinese Shorts

将一段 YouTube 访谈/播客切割成多个带中文硬字幕的短视频片段。

## 前置检查

按以下顺序检查，遇到问题先询问用户再继续：

**第一步：检查目录是否存在**

检查 `./youtube/` 和 `./scripts/` 是否存在。若任一不存在，询问用户：

> 「未找到 `./youtube/` 或 `./scripts/` 目录。是否自动创建？（创建后你仍需手动放入所需文件）」

- 用户同意 → 执行 `mkdir -p ./youtube ./scripts`，告知已创建，继续第二步
- 用户拒绝 → 停止，提示用户手动准备工作区后再调用

**第二步：检查必要文件**

目录存在后，验证以下文件，任意缺失立即报告并停止：

- `./youtube/download.py`
- `./youtube/ZITI.ttf`
- `./scripts/srt_to_json.py`
- `./scripts/window_srt.py`
- `./scripts/clip_video.py`
- `./scripts/burn_subtitles.py`
- `ffmpeg` 可用（`ffmpeg -version`）

## 工作区布局（约定）

```
work/<video-slug>/
  source/
    original.mp4
    original.en.srt
    original.jpg        # 可选缩略图
  analysis/
    transcript.json
    selected_clips.json
    candidate-review.txt
    clip-packaging.txt
  clips/
    <id>-<slug>/
      clip.mp4
      clip.en.srt
      clip.zh.srt
      clip.hardsub.mp4
      metadata.txt
```

## 主流程

按以下顺序执行 8 个步骤：

1. **创建工作目录** — 从 URL 提取 video-slug，创建 `work/<video-slug>/source/`、`analysis/`、`clips/`
2. **下载源文件** — 运行 `python ./youtube/download.py <URL> --output work/<video-slug>/source/`，识别 `.mp4`、`.en.srt`（必须）、`.jpg`（可选）
3. **转换字幕为 JSON** — 运行 `python ./scripts/srt_to_json.py <srt_path> > analysis/transcript.json`
4. **分析转录（Stage 1）** — 使用下方 Stage 1 提示词分析 `transcript.json`，1 小时视频目标 10~15 个候选（宁多勿少）
5. **写候选列表** — 结果写入 `analysis/selected_clips.json`（结构见下方 Clip Schema）
6. **呈现候选给用户（Stage 2）** — 每个片段展示：时间戳、时长、标题、两句摘要，询问用户选哪些 clip ids
7. **导出选中 clips** — 对每个 clip 依次执行：切片 → 提取字幕窗口 → 翻译中文 → 生成标题描述 → 烧录字幕
8. **返回产物路径** — 列出所有 `clip.hardsub.mp4` 和 `metadata.txt` 路径

## 导出命令

对每个选中的 clip：

```bash
# 切片
python ./scripts/clip_video.py \
  --input work/<slug>/source/original.mp4 \
  --start <start_seconds> --end <end_seconds> \
  --output work/<slug>/clips/<id>-<slug>/clip.mp4

# 提取字幕窗口
python ./scripts/window_srt.py \
  --input work/<slug>/source/original.en.srt \
  --start <start_seconds> --end <end_seconds> \
  --output work/<slug>/clips/<id>-<slug>/clip.en.srt

# 烧录中文字幕（翻译后）+ 标题叠加
python ./scripts/burn_subtitles.py \
  --input work/<slug>/clips/<id>-<slug>/clip.mp4 \
  --srt work/<slug>/clips/<id>-<slug>/clip.zh.srt \
  --title "<屏幕叠加标题约12字>" \
  --font ./youtube/ZITI.ttf \
  --font-size 48 --outline 3 \
  --output work/<slug>/clips/<id>-<slug>/clip.hardsub.mp4
```

标题叠加：居中、视频第一秒、约 12 个中文字。

## Clip Schema（selected_clips.json）

```json
{
  "source_url": "https://www.youtube.com/watch?v=XXXX",
  "video_slug": "video-slug",
  "clips": [
    {
      "id": "01",
      "start": "00:03:12,400",
      "end": "00:05:47,800",
      "start_seconds": 192.4,
      "end_seconds": 347.8,
      "duration_seconds": 155.4,
      "working_title": "为什么大多数人永远不会成功",
      "summary": "嘉宾指出大多数人失败不是因为能力不足，而是从未真正承诺过一件事。他用亲身经历说明，专注力才是区分成败的关键变量。",
      "quality_signals": ["opinionated", "counterintuitive"],
      "selected": false
    }
  ]
}
```

- `duration_seconds` 应在 20 ~ 180 秒之间
- `summary` 恰好两句
- `end` 必须落在说话人完成完整句子之后

## 分析提示词

### Stage 1：候选选取

```
你是一位专业的短视频剪辑编辑。以下是一段访谈的英文字幕（JSON格式）。

找出适合剪辑成独立短视频的片段，标准：
- 可独立理解，不依赖大量前文
- 至少具备：有观点、反常识、有激励性、情感鲜明、适合引用之一
- 时长 20 秒到 3 分钟，开头 3 秒内有强钩子，以完整思想结尾

排除：暖场、赞助商推广、严重依赖前文或画面的片段

1 小时视频目标 10~15 个候选，宁多勿少。
以 JSON 格式输出，遵循上方 Clip Schema。

字幕内容：
{TRANSCRIPT_JSON}
```

### Stage 2：用户审核格式

每个 clip 输出以下格式，用 `---` 分隔：

```
**[01] 为什么大多数人永远不会成功**
⏱ 03:12 → 05:47（2分35秒）

嘉宾指出大多数人失败不是因为能力不足，而是从未真正承诺过一件事。他用亲身经历说明，专注力才是区分成败的关键变量。
```

结尾询问：请输入要导出的 clip id（如 `01 03 07`），或输入「全部」自动选最强片段。

### Stage 3：中文字幕翻译

```
将以下英文 SRT 翻译成简体中文。
- 保留所有时间戳不变
- 自然口语中文，不逐字直译
- 保留专有名词、数字、产品名、引用短语
- 保留字幕条目数量（宁多勿少）

{SRT_CONTENT}
```

### Stage 4：标题与描述生成

```
为以下短视频生成标题和描述：
发言人：{SPEAKER}，节目：{SHOW}，话题：{TOPIC}，核心内容：{SUMMARY}

输出：
1. 完整标题（短视频平台风格，可反问/反常识，忠实原意）
2. 屏幕叠加标题（约 12 个中文字）
3. 描述（140 中文字以内，含发言人、节目名、话题、核心观点）
```

## 选片规则

**优先：** 有立场、反常识、激励性、情感锐利、可引用的片段
**排除：** 暖场、赞助、依赖前文/画面的片段

## 翻译规则

- 忠实原意，改写为自然口语中文
- 保留时间戳结构，保留条目数量
- 保留专有名词、数字、引用

## 错误契约

| 阻断原因 | 报告内容 |
|----------|----------|
| 下载失败 | cookies 是否过期、具体错误 |
| 无英文字幕 | 文件名列表，确认 `.en.srt` 不存在 |
| ffmpeg 缺失 | `which ffmpeg` 输出 |
| 转录质量差 | 不可信段落示例 |
| 脚本缺失 | 缺失的文件路径 |
