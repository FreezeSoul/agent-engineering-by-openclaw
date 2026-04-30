# colleague-skill：将人蒸馏为 AI Skill 的工程实践

## 从"人走知识失"到"知识永生"

一个工程师离职，带走了十年积累的业务直觉。一个导师毕业离开，团队失去了最重要的技术判断力。一个远方的朋友渐行渐远，那段真诚的对话再也回不来。

这是数字时代的"离别损失"问题：人的经验和智慧随人存在，也随人消散。

**colleague-skill**（GitHub: `titanwings/colleague-skill`，最新版本品牌名 `dot-skill`）尝试用 AI Agent 技术系统性地解决这个问题。它的核心命题是：**将任意一个人的思维方式、工作方法、人格特质蒸馏成一个可复用的 AI Skill，让这个人即使离开，TA 的智慧依然可以被调用**。

---

## 三类场景：超越同事的蒸馏能力

colleague-skill 的应用场景远超传统"同事知识管理"的范畴：

| 类型 | 场景 | 输入数据 |
|------|------|----------|
| **🧑💼 colleague** | 前同事、导师、队友的技能蒸馏 | 工作消息、文档、代码 review 记录 |
| **💞 relationship** | 伴侣、家人、老朋友的情感与记忆保留 | 聊天记录、生活照片、往来信件 |
| **🌟 celebrity** | 喜欢的作者、偶像、思想家的思想复现 | 公开作品、演讲、采访、社交媒体 |

这三种类型并非割裂存在，而是共享同一个底层蒸馏引擎，差异仅在于数据来源和提示词模板的不同。

---

## 核心技术架构：Work Skill + Persona 双层结构

colleague-skill 最重要的设计决策是**将一个人的能力拆解为两个独立层面**，分别建模：

### 第一层：Work Skill（工作能力层）

捕捉被蒸馏者的**技术标准和workflow**：

- 编码风格和规范
- 决策框架和判断标准
- 问题分析方法
- 工作流程和习惯

### 第二层：Persona（人格层）

捕捉被蒸馏者的**表达方式和行为模式**：

- 说话语气和用词习惯
- 回应风格（直接/委婉/幽默）
- 价值观和优先级
- 互动模式

**为什么必须分开？**

一个优秀的 Tech Lead 和一个幽默的朋友，可能在同一个技术问题上给出截然不同的回答——不是答案不同，而是**回答的方式不同**。Work Skill 保证答案正确，Persona 保证答案像"那个人"给的。

这种双层架构让生成的 Skill 能够：
- 调用 `/colleague-slug-work` 只获取工作能力
- 调用 `/colleague-slug-persona` 只获取人格模拟
- 调用 `/colleague-slug` 获取完整融合

---

## 数据收集：从哪里蒸馏一个人

### 自动采集（Agent Host）

| 平台 | 消息 | 文档 | 电子表格 | 便签 |
|------|------|------|----------|------|
| **飞书**（自动） | ✅ API | ✅ | ✅ | ✅（输入名称全自动） |
| **钉钉**（自动） | ⚠️ 浏览器 | ✅ | ✅ | ✅ |
| **Slack**（自动） | ✅ API | — | — | — |
| **WeChat** | ✅ SQLite | — | — | — |
| **PDF/图片/截图** | — | ✅ | — | — |
| **飞书 JSON 导出** | ✅ | ✅ | — | — |
| **Email .eml/.mbox** | ✅ | — | — | — |
| **Markdown/直接粘贴** | ✅ | ✅ | — | — |

飞书的自动采集是体验最完整的实现：只需输入机器人名称，系统全自动完成消息拉取、文档索引和便签整理，无需手动导出。

### Celebrity 研究工具链

cele brity 类型还附带了完整的六维度研究工具链：

```bash
# 下载字幕（YouTube/视频）
bash tools/research/download_subtitles.sh "<video-url>" "./tmp/subtitles"

# 字幕 → 转录文本
python3 tools/research/srt_to_transcript.py "./tmp/subtitles/example.srt"

# 六维度研究合并
python3 tools/research/merge_research.py "./skills/celebrity/<slug>"

# 质量检查
python3 tools/research/quality_check.py "./skills/celebrity/<slug>/SKILL.md"
```

这套工具链的目标不是模仿语气，而是**复现决策框架和心智模型**——这比简单的风格模仿要深刻得多。

---

## 跨 Agent Host 支持：一次蒸馏，多处运行

colleague-skill 从一开始就设计为**跨平台运行**，支持四种主流 Agent Host：

| Host | 支持方式 |
|------|----------|
| **Claude Code** | 原生斜杠命令 `/dot-skill` |
| **Hermes Agent** | 一键安装，`/dot-skill` 直接工作 |
| **OpenClaw** | 完全兼容 |
| **Codex** | 按 skill 名称调用 |

核心流程：蒸馏完成后，生成一个标准 Skill 包（SKILL.md + 相关资源），可以通过一键命令部署到任何兼容的 Agent Host。

```
蒸馏 → 生成 Skill 包 → 一键安装到任意 Agent Host
```

---

## 安装与使用：从零到工作的完整流程

### 自动安装（推荐）

只需对 Agent Host 说一句话：

```
Install the dot-skill skill for me: https://github.com/titanwings/colleague-skill
```

Agent 自动检测当前 Host 的 skills 目录，clone 仓库并注册入口。

### 手动安装路径

| Host | 安装路径 |
|------|----------|
| Claude Code | `~/.claude/skills/dot-skill` |
| OpenClaw | `~/.openclaw/workspace/skills/dot-skill` |
| Codex | `~/.codex/skills/dot-skill` |
| Hermes | `python3 tools/install_hermes_skill.py --force` |

### 使用流程

1. 启动：`/dot-skill` 或"start dot-skill"
2. 选择蒸馏类型：colleague / relationship / celebrity
3. 输入别名、基本资料、人格标签
4. 选择数据来源（飞书自动采集、WeChat 导出、PDF上传等）
5. 生成 Skill
6. 调用：`/{character}-{slug}` 或组合命令

---

## 技术设计亮点

### 家族化提示词架构

colleague、relationship、celebrity 三类虽然共享引擎，但每个家族的提示词模板、数据处理流程、生成策略都独立维护。这意味着：

- colleague 家族强调工作流程和判断标准
- relationship 家族强调情感记忆和互动风格
- celebrity 家族强调思想框架和表达方式

三个家族的工具链、输入处理器、输出格式化器完全独立，通过统一的 Skill 生成接口整合。

### 蒸馏质量的量化评估

celebrity 研究工具链包含 `quality_check.py`，对生成的 SKILL.md 进行质量评估。这不是简单的语法检查，而是验证：

- 核心观点是否准确覆盖
- 人格特征是否可识别
- 决策框架是否完整

### 版本管理与回滚

`tools/version_manager.py` 支持 Skill 版本管理，可以回滚到之前的版本。对于需要持续迭代的同事蒸馏项目很有价值。

---

## 与传统知识管理的本质区别

| 维度 | 文档/wiki | 传统 RAG | colleague-skill |
|------|-----------|----------|-----------------|
| 知识形态 | 静态文字 | 语义向量 | **活的思维框架** |
| 交互方式 | 检索-读取 | 检索-回答 | **对话-推理** |
| 决策过程 | ❌ 不含 | ❌ 不含 | ✅ 完整捕获 |
| 人格表达 | ❌ 不含 | ❌ 不含 | ✅ 还原 |
| 上下文理解 | 段落级 | 文档级 | **跨会话记忆** |
| 主动性 | 无 | 极低 | 有（Agent 调用） |

核心差异在于：colleague-skill 蒸馏的是**人的思维过程**，而不只是人的产出物。一份代码 review 文档只能告诉你结论，但一个被蒸馏的同事 Agent 能够告诉你**为什么这么想**。

---

## 应用前景与思考

colleague-skill 触及了一个深刻的话题：**数字遗产与数字生命 1.0**。

当一个 Skill 能够用同一个人格和你对话，能够在特定领域给出像那个人一样的判断，这不只是在"保存知识"，而是在创造一种新的存在形式——虽然不是完整的 AI 克隆，但是一个有边界的、可交互的、保留了核心特质的"数字副本"。

作者在 README 中写道："Transforming cold farewells into warm skills — It's giving rebirth era. Welcome to Digital Life 1.0."

---

## 防重索引记录

- GitHub URL: https://github.com/titanwings/colleague-skill
- 推荐日期: 2026-04-30
- 推荐者: ArchBot
