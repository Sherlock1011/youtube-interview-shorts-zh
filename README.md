# 🎬 YouTube Interview → Chinese Shorts

> 一键将 YouTube 长访谈切割成多个带中文硬字幕的短视频片段

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)

**让 AI 帮你完成从长视频到短视频的全流程：** 智能选片 → 精准切割 → 字幕翻译 → 标题生成 → 硬字幕烧录

---

## ✨ 特性

- 🤖 **AI 驱动的智能选片** — 自动识别访谈中的精彩片段（反常识、有观点、情感锐利）
- 🎯 **精准时间戳定位** — 确保每个片段都是完整的思想表达
- 🌏 **中文字幕翻译** — 自然口语化翻译,保留专有名词和数字
- 📝 **短视频标题生成** — 适合抖音/快手/视频号的吸睛标题
- 🔥 **硬字幕烧录** — 首帧标题叠加 + 全程中文字幕
- 🔧 **跨平台支持** — Claude Code 和 Codex 双平台 skill

---

## 🚀 快速开始

### 前置要求

- Python 3.8+
- ffmpeg
- yt-dlp
- Claude Code 或 Codex

### 安装步骤

**1. 克隆仓库**

```bash
git clone https://github.com/your-username/youtube-interview-shorts-zh.git
cd youtube-interview-shorts-zh
```

**2. 安装 Python 依赖**

```bash
pip install yt-dlp
```

**3. 安装 Skill 到 AI 平台**

<details>
<summary><b>Claude Code 用户</b></summary>

```bash
mkdir -p ~/.claude/skills/youtube-interview-shorts-zh
cp claude/SKILL.md ~/.claude/skills/youtube-interview-shorts-zh/SKILL.md
cp -r references ~/.claude/skills/youtube-interview-shorts-zh/references
```

</details>

<details>
<summary><b>Codex 用户</b></summary>

```bash
mkdir -p ~/.agents/skills/youtube-interview-shorts-zh
cp codex/SKILL.md ~/.agents/skills/youtube-interview-shorts-zh/SKILL.md
```

</details>

**4. 准备工作区**

在你的项目目录下:

```bash
# 创建目录
mkdir -p ./scripts ./youtube

# 复制脚本
cp youtube-interview-shorts-zh/scripts/*.py ./scripts/
cp youtube-interview-shorts-zh/scripts/download.py ./youtube/

# 准备中文字体(自行下载)
# 将字体文件放到 ./youtube/ZITI.ttf
```

---

## 📖 使用方法

在你的工作区目录下,向 AI 发送:

```
/youtube-interview-shorts-zh https://www.youtube.com/watch?v=XXXX
```

### 工作流程

```mermaid
graph LR
    A[输入 YouTube URL] --> B[下载视频+字幕]
    B --> C[AI 分析转录]
    C --> D[生成 10-15 个候选片段]
    D --> E[用户选择片段]
    E --> F[切片+翻译+烧录]
    F --> G[输出带中文字幕的短视频]
```

### 示例输出

AI 会展示候选片段供你选择:

```
---
**[01] 为什么大多数人永远不会成功**
⏱ 03:12 → 05:47 (2分35秒)

嘉宾指出大多数人失败不是因为能力不足,而是因为从未真正承诺过一件事。
他用亲身经历说明,专注力才是区分成败的关键变量。
---

**[02] 如何在30天内掌握一项新技能**
⏱ 12:34 → 14:20 (1分46秒)

分享了一个反直觉的学习方法:不是每天练习1小时,而是集中3天高强度训练。
这种方法让他在一个月内学会了弹吉他。
---
```

你选择要导出的片段 ID (如 `01 03 07`),AI 会自动完成剩余工作。

---
## 📁 项目结构

```
youtube-interview-shorts-zh/
├── claude/                   # Claude Code 版 Skill
│   └── SKILL.md
├── codex/                    # Codex 版 Skill
│   └── SKILL.md
├── references/               # 引用文档
│   ├── clip-schema.md        # JSON 结构定义
│   └── analysis-prompt.md    # AI 分析提示词
├── scripts/                  # 核心脚本
│   ├── download.py           # YouTube 下载器
│   ├── srt_to_json.py        # 字幕解析
│   ├── window_srt.py         # 字幕窗口提取
│   ├── clip_video.py         # 视频切片
│   └── burn_subtitles.py     # 字幕烧录
└── README.md
```

---

## 🎯 选片规则

AI 会根据以下标准智能选择片段：

### ✅ 优先选择
- 有明确立场、反常识的观点
- 情感锐利、有激励性的内容
- 适合引用、有记忆点的金句
- 首 3 秒内有强钩子
- 20 秒 ~ 3 分钟时长

### ❌ 自动排除
- 暖场、介绍、闲聊
- 赞助商推广
- 严重依赖前文或画面的片段
- 不完整的句子或思想

---

## 🛠️ 技术栈

| 组件 | 技术 |
|------|------|
| 视频下载 | yt-dlp |
| 视频处理 | ffmpeg |
| 字幕解析 | Python (SRT) |
| AI 分析 | Claude Code / Codex |
| 字幕翻译 | AI (自然语言处理) |

---

## 💡 常见问题

<details>
<summary><b>Q: 下载失败提示 cookies 过期？</b></summary>

下载器依赖浏览器 cookies。解决方法：
1. 在浏览器中重新登录 YouTube
2. 或尝试其他浏览器：`--cookies-from-browser firefox`

</details>

<details>
<summary><b>Q: 视频没有英文字幕？</b></summary>

Skill 会自动尝试下载自动生成字幕。如果仍然失败：
- 检查视频是否有字幕（YouTube 播放器中查看）
- 部分私有视频可能无法下载字幕

</details>

<details>
<summary><b>Q: 想要竖屏短视频格式？</b></summary>

当前版本输出横屏画面。竖屏裁剪功能计划在后续版本添加。

</details>

<details>
<summary><b>Q: 可以处理中文访谈吗？</b></summary>

当前版本专为英文访谈设计（英文字幕 → 中文翻译）。
中文访谈支持需要修改 Skill 中的字幕语言设置。

</details>

---
## 🙏 致谢

- [洛克AI](http://xhslink.com/o/601eK0akjJd) - 提供youtube快速剪辑短视频skill思路

---

## 📮 联系方式

如有问题或建议，欢迎：
- 提交 [Issue](https://github.com/your-username/youtube-interview-shorts-zh/issues)

---

<p align="center">
  Made with ❤️ by <a href="https://github.com/your-username">Your Name</a>
</p>
