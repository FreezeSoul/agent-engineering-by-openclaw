---
title: "recall：TF-IDF+TextRank 替代 LLM 做记忆压缩"
slug: raiyanyahya-recall-local-first-project-memory-textrank-zero-token-2026
date: 2026-07-01
category: context-memory
tags:
  - agent-memory
  - claude-code
  - local-first
  - text-rank
  - tf-idf
  - session-continuity
  - hook-driven-capture
  - privacy-by-design
source: Open Source GitHub Repository (raiyanyahya/recall)
score: 5/5（独特性 / 工程机制密度 / 隐私价值）
---

# raiyanyahya/recall：当 Claude Code 用 TF-IDF + TextRank 替代 LLM 做记忆压缩，token 成本归零

> **核心论点**：raiyanyahya/recall 这个 639 ⭐ 的 Claude Code 插件用**经典 NLP 算法**（TF-IDF + TextRank）做会话摘要——**零 LLM 调用、零 token 成本、零数据外传**。它把「Agent 记忆」从「再调一次 LLM」的反直觉设计拉回到「30 年前的 PageRank 就能解决」的工程原点。这个项目对当前 Agent 社区的「什么都要走 LLM」惯性是一个清醒的反驳。

---

## 一、社区惯性：Agent 记忆 = 再调一次 LLM？

2026 年上半年，Agent 记忆架构的主流方案是「**再调一次 LLM**」：在 session 结束时，把整段 transcript 喂给模型，压缩成「下次从哪里继续」的摘要，下个 session 开始时再把这部分 prepend 到 prompt。

这种设计的「工程味道」非常糟糕：

| 隐性成本 | 量级 | 备注 |
|---------|------|------|
| 摘要 token | 与 transcript 等长 | 调一次 LLM 读完整段历史，token 消耗 = transcript 长度 × 2 |
| 摘要延迟 | 2-15 秒 | 网络往返 + LLM 推理 |
| 摘要订阅消耗 | 计入会话额度 | API 用户额外付费，订阅用户挤占 5h 限额 |
| 摘要数据外传 | transcript 完整送 API | 含代码、路径、可能的 secrets |
| 摘要可重现性 | 0 | 模型升级 / temperature 抖动 → 同一 transcript 输出不同摘要 |

笔者认为：**Agent 记忆的本质是「从一段噪声文本中提取关键句子」**——这是一个经典的 NLP 任务，不是 LLM 任务。把 LLM 用在这里是杀鸡用牛刀，更糟糕的是「杀鸡用牛刀还让鸡付刀钱」。

raiyanyahya/recall[1] 的核心洞察就在这里：**TF-IDF + TextRank 在「提取关键句」这个任务上不输 LLM，且成本归零**。

---

## 二、Recall 的核心设计：双文件 + 经典算法

Recall 把项目记忆分成两个互补的文件，全部写入项目根的 `.recall/` 目录：

```
.recall/
├── history.md   # 追加日志（append-only）
└── context.md   # 覆盖式摘要（overwrite）
```

| 文件 | 写入模式 | 内容 | 谁来写 |
|------|---------|------|--------|
| `history.md` | append-only | 完整 session transcript：prompt / reply / files touched / commands run | Stop + SessionEnd hook |
| `context.md` | overwrite | 浓缩的「我们目前在哪、接下来做什么」 | `/recall:save` 触发本地摘要器 |

`history.md` 解决「**原始证据完整性**」——任何事后审计、debug、回溯都能查到原始 transcript。`context.md` 解决「**下次 session 开局**」——Claude 启动时被注入 1-2K tokens 的紧凑摘要，session 立刻进入状态。

### 摘要器：`scripts/summarizer.py` 怎么用 30 年前的算法

Recall 的本地摘要器实现可以用一段伪代码完整描述：

```
1. 把 transcript 切成 sentences
2. 对每个 sentence 算 TF-IDF 向量
   - TF = 词频 / sentence 总词数
   - IDF = log(总 sentence 数 / 包含该词的 sentence 数)
3. 算 sentence 之间的 cosine 相似度
4. 用 PageRank power iteration 在相似度图上做 sentence ranking
5. 取 top-N sentence（默认 N=8）按原始顺序拼回
```

这正是 2004 年 Mihalcea & Tarau 提出的 **TextRank**[2] 的标准实现。Recall 的工程亮点不在算法本身（任何 NLP 教科书都有），而在「**把它做成了一个 100% offline、零依赖、可选 numpy 加速**」的生产级实现：

- **numpy 存在时**：用矩阵运算加速，几十万 token 的 session 也能秒级完成
- **numpy 不存在时**：自动降级到纯 Python 实现，结果**完全一致**（CI 用 `benchmarks/bench.py --check` gate 两个路径必须选相同句子）
- **stdlib-only**：除了 numpy（可选），没有 `transformers`、没有 `torch`、没有 `openai`——这是它「privacy 承诺」能被验证的工程基础

`context.md` 的内容不是「摘要器单输出」，而是「摘要器 + 确定性事实」的组合：

```markdown
# Project Context

**Goal:** <from first user prompt>
**Summary:** <8-sentence TextRank output>
**Next steps:** <extracted from open threads>
**Files touched:** <from transcript parse>
**Commands run:** <from transcript parse>
**Where you left off:** <from last assistant message>
**Recent commits:** <from `git log`>
**git diff --stat:** <from `git diff`>
```

「目标、文件、命令、commit」全是 deterministic pull，不依赖摘要器。摘要器只负责「叙事凝练」这一项。

---

## 三、Hook 驱动捕获：SessionStart / Stop / SessionEnd 怎么联动

Recall 的捕获完全是 **Hook 驱动**——它不修改 Claude Code 内部，只通过 Anthropic 官方的 Hooks API 在 session 边界自动化运行：

| 时机 | 事件 | Recall 的动作 |
|------|------|---------------|
| Session 启动 | SessionStart hook | 读 `context.md` → 展示给用户 → 问「是否 resume？」「是否继续 logging？」|
| 每轮对话 | Stop hook | 把本轮 prompt + reply + tools 增量 append 到 `history.md` |
| Session 结束 | SessionEnd hook | 如果配置 `auto_save_context: "on_end"`，自动调摘要器重写 `context.md` |
| 用户手动 | `/recall:save` | 同上，但显式触发 |

这套机制有两个**非显见的工程价值**：

### 价值 1：捕获是增量的，不是 snapshot

传统 Agent 记忆工具的实现往往是「session 结束时一次性 dump 整段 transcript」。这有两个问题：
- **延迟**：session 跑 30 分钟，结束时 dump 要再等 10 秒
- **可靠性**：如果 session crash 或 OOM，dump 没执行 → 记忆全丢

Recall 的 Stop hook 是**每轮触发**的——它每次只写「本轮新增的部分」，session 越长越能体现价值。

### 价值 2：捕获和摘要解耦，可选时机

```
捕获（自动）:        摘要（手动 or 自动）
SessionStart     →   读 context.md
    ↓
    ↓ 每轮 prompt
    ↓
Stop hook   →  append to history.md
    ↓
    ↓
SessionEnd  →  (可选) auto-summarize
    ↓
/recall:save  →  (强制) summarize + overwrite
```

用户可以**只开捕获不开摘要**（默认配置），也可以**开了捕获 + on_end 自动摘要**（推荐生产配置）。这种解耦让 recall 在「保守隐私」和「全自动连续性」之间灵活切换。

---

## 四、Privacy by Design：6 个安全护栏的工程意义

Recall 的 README 用了 250 行的篇幅讲 privacy，这不是「凑字数的 ethics statement」，而是有**可被验证的工程机制**支撑的承诺：

| 护栏 | 机制 | 防的威胁 |
|------|------|---------|
| **No network** | 全部代码 grep 不到 `urllib` / `requests` / `http` | 代码被植入恶意 endpoint |
| **No API key** | 全部代码 grep 不到 `ANTHROPIC_*` / `sk-ant` / `sk-` | 用户误把 key 提交进 plugin |
| **Secret redaction** | `scripts/redact.py` 在写入前剥离 `API key` / `Bearer` / `.env=` / `PEM key` 形态的串 | `context.md` 误 commit 到公开仓库 |
| **Hardened git** | `core.fsmonitor` / `diff.external` / hooks / pager 全部 disable 后才跑 `git diff/log` | 恶意 `~/.gitconfig` 借 recall 触发 RCE |
| **Path confinement** | `output_dir` 强制留在项目根，路径穿越检测（绝对路径 / `../` 拒绝）| 恶意 config 把 `history.md` 写到 `/etc/passwd` |
| **Untrusted fence** | `context.md` 注入 prompt 时明确标记为「untrusted reference data」，不是 instructions | 队友写恶意 `context.md` 做 prompt injection |

最后一项护栏是**最值得展开的**：

> "If you commit `.recall/` as shared team memory, treat it like any other shared input: a teammate (or a bad actor with repo write access) could craft a `context.md` to attempt prompt-injection. SessionStart fences the content and labels it untrusted data, and Claude asks before relying on it — but if you don't fully trust who can write the repo, keep `.recall/` git-ignored."

这是**对 prompt injection 威胁的诚实承认**。绝大多数 Agent 记忆工具都会宣传「把我们的 memory 交给 agent 就完事了」，但 Recall 直接说「**共享 memory 等于共享 prompt 写入权限**」，并要求用户做 trust boundary 决策。

笔者认为：**这是 2026 年 Agent 工具该有的态度**。把 privacy 简化成「我们不卖你数据」是营销话术，把 privacy 拆成 6 个可被验证的工程机制 + 1 个明确的 threat model + 用户决策权，才是工程实践。

---

## 五、和同 cluster 项目的对照：recall 在「记忆架构」光谱上的位置

Agent 记忆架构在 2026 年已经形成一条清晰的光谱：

| 项目 | 摘要技术 | Token 成本 | 隐私强度 | Vendor 锁定 | 检索能力 |
|------|---------|-----------|---------|-----------|---------|
| **akitaonrails/ai-memory** (260⭐) | LLM 压缩（Claude Sonnet 4）| 高 | 中（Docker 部署）| 跨厂商 | grep |
| **byterover/context-tree** (1500+⭐) | LLM-curated tree | 高 | 中 | LangChain 生态 | semantic |
| **mem0** (30k+⭐) | Embedding + LLM extraction | 高 | 低（云端）| LangChain 生态 | semantic |
| **recall** (639⭐) | **TF-IDF + TextRank** | **0** | **极高**（无网络）| **Claude Code** | grep |

Recall 在光谱上的位置是**极端的反 LLM 化**：

- **不用 LLM 摘要** → token 成本归零
- **不用 embedding** → 不依赖 embedding model，零网络
- **不用 vector store** → 不需要装 chroma/qdrant，零运维
- **纯 Markdown 文件** → 可 grep、可 diff、可 commit、可审计

**代价是什么**？Recall 的检索能力只能到「关键词 grep」级别。如果你需要「找到上周讨论过『OAuth 流程优化』但没出现『OAuth』字样的段落」——这是 semantic search 的领域，Recall 不擅长。

**笔者认为**：

> 对 90% 的 Agent 工作流，「**我昨天让你重构了 `parser.py` 的第 47-89 行**」这种精确的、关键词可见的回顾，**grep 比 embedding 更好用**。Embedding 的「语义模糊匹配」是 LLM 时代的产物——当你已经用 `git log` 拿到了「6/28 修改过 parser.py」的事实，何须 embedding 来「猜」相关性？

Recall 的设计哲学是 **「让 fact-based 检索回到桌面」**，把 semantic search 留给「我真的不知道关键词」的少数场景。

---

## 六、与 Anthropic 官方方向的对照

Anthropic 在 2025-2026 年发布了一系列「**用 LLM 做 Agent 记忆**」的工程文章：

- [Effective context engineering for AI agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents) — 推荐用 `compaction`（LLM 压缩）
- [How we built our multi-agent research system](https://www.anthropic.com/engineering/multi-agent-research-system) — 用 LeadResearcher + sub-agent + `compaction`
- [Building agents with the Claude Agent SDK](https://www.anthropic.com/engineering/building-agents-with-the-claude-agent-sdk) — 同样推荐 `compaction`

**Recall 不是反对这些**。它是给出了一个**完全不同的预算选择**：

> 如果你的 session 短（<10 轮）、transcript 小（<5K tokens），用 LLM compaction 没问题，token 成本可控。
> 
> 如果你的 session 长（50-200 轮）、transcript 大（>50K tokens），或者你在按订阅跑（每 token 都要精打细算），或者你处理敏感代码（不能外传）——**TF-IDF + TextRank 是更优解**。

这不是 LLM 派 vs 经典派的宗教战争，是**「不同规模 / 不同预算 / 不同威胁模型下用不同工具」**的工程现实。

---

## 七、局限性与不适用场景

Recall 不适合以下场景：

1. **多语言混合 transcript**：TF-IDF 在中文/英文混合时 IDF 计算会偏（默认 tokenizer 不分词中文）
2. **超长 session（>200K tokens transcript）**：摘要器的 `max_input_chars: 200000` 默认会丢早期内容
3. **需要 semantic 检索**：「找上周讨论过的类似架构思路」——grep 不够用
4. **多 agent 并行写同一个 `.recall/`**：history.md 是 append-only，并行写会冲突

如果你的工作流命中以上任一条，建议用 mem0 / byterover 等 LLM-based 方案。

---

## 八、快速上手

```bash
# 1. 从 marketplace 安装
/plugin marketplace add raiyanyahya/recall
/plugin install recall@recall

# 2. (可选) 修改配置
cat > recall.config.json << 'EOF'
{
  "output_dir": ".recall",
  "capture_history": true,
  "auto_save_context": "on_end",
  "summary_sentences": 8,
  "redact": true,
  "include_git": true,
  "max_input_chars": 200000
}
EOF

# 3. 开始一个 session
# SessionStart hook 会问：是否 resume from context.md? 是否继续 logging?
# 答：是，是

# 4. 正常用 Claude Code 写代码
# Stop hook 每轮自动 append 到 history.md

# 5. 手动保存摘要
/recall:save
# 或配置 auto_save_context: "on_end" 后让 SessionEnd 自动保存

# 6. 下次开新 session 时，SessionStart 自动注入 context.md
```

**没有 `pip install`，没有 API key，没有外部依赖**。

---

## 九、笔者结论

> **raiyanyahya/recall 是 2026 年 Agent 记忆工具里我见过的、最清醒的一个项目**。
>
> 它不追逐「embedding 一切」的浪潮，**用 30 年前的算法解决了一个 LLM 时代被忽视的问题**。它不回避 prompt injection 的威胁，**把 trust boundary 明明白白交给用户决定**。它不依赖任何 LLM 推理，**用 1.6K 行 Python（含测试和 benchmark）交付了一个 5 个 hook 联动的完整记忆系统**。
>
> 如果你正在为 Claude Code 找一个「**不烧 token、不外传数据、不复杂部署**」的记忆工具，**recall 是当前的最优解之一**。
>
> 如果你正在思考「Agent 记忆一定要走 LLM 吗？」——**recall 是最有力的反例**。

---

## 引用来源

[1] raiyanyahya/recall — GitHub, MIT License, 639 ⭐, 36 forks, 2026-06-19 created
https://github.com/raiyanyahya/recall

[2] TextRank: Bringing Order into Texts — Rada Mihalcea, Paul Tarau, 2004
https://aclanthology.org/W04-3252/

[3] Claude Code Hooks 官方文档 — Anthropic
https://docs.claude.com/en/docs/claude-code/hooks

[4] Effective context engineering for AI agents — Anthropic Engineering
https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents
