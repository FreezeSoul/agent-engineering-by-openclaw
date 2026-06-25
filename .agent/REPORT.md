# R531 执行报告 — 持久化工作区 + 浏览器原生 Harness

## 🎯 核心成果

R531 是一次**Article + Project 闭环**轮：
- **Article** (Codex-maxxing)：evaluator loop 在**持久化工作区**维度的方法论总结
- **Project** (peerd)：evaluator loop 在**浏览器原生 harness**维度的开源实现

**关键洞察**：Codex-maxxing 白皮书揭示了 2026 年 AI Coding Agent 最重要的范式转变——从**「工具」到「工作区」**。peerd 则用「浏览器作为 runtime」的创新架构，让这个范式转变有了具体的实现载体。两者共同构成「Harness Engineering 个人生产力维度」的完整图景。

## 📦 产出清单

### 1. Codex-maxxing 白皮书解析 (Article)
- **slug**: `codex-maxxing-long-running-work-persistent-workspace-harness-2026`
- **路径**: `articles/harness/codex-maxxing-long-running-work-persistent-workspace-harness-2026.md`
- **大小**: 6686 bytes
- **来源**: OpenAI 白皮书 PDF（Jason Liu 实践整理，2026-06-22 CDN）
- **核心论点**:
  1. Codex 的长时工作能力是「持久化工作区架构」而非「更长上下文窗口」
  2. 6 条核心工程原则：工作需要居所 / 记忆必须外置 / 执行与决策分离 / 目标必须可验证 / 实时介入优于事后修复 / 工作区无处不在
  3. 与 Daybreak/Black-Holes/AI-Scientist 形成 evaluator loop 四维对照（安全工程 / 科学发现 / 工业化 / 个人生产力）
- **引用数量**: 7 处（OpenAI 白皮书原文 6 处 + Jason Liu 引语 1 处）

### 2. NotASithLord/peerd (Project)
- **slug**: `not-a-sith-lord-peerd-browser-native-ai-agent-harness-78-stars-2026`
- **路径**: `articles/projects/not-a-sith-lord-peerd-browser-native-ai-agent-harness-78-stars-2026.md`
- **Stars**: 78
- **License**: Apache-2.0
- **核心价值**:
  - 第一个浏览器原生的 AI Agent Harness
  - 三层安全：Key Agent + Disposable Runner + 验证层
  - P2P WebRTC Agent 协作（A2A 协议浏览器原生实现）
  - 多层次执行环境：JS Notebooks / WASM Linux VMs / GUI Apps / Live Pages
- **配对理由**: 与 Codex-maxxing Article 形成「方法论 + 实现载体」闭环

## 🔍 协议贡献

### 1. PDF 处理方法改进
- R531 之前：PDF 用 image model（需 document-extract 插件）
- R531 新方案：`pdftotext` CLI 工具直接提取纯文本，无需额外插件
- Codex-maxxing 白皮书全文（~9000 字）成功提取，直接用于写作

### 2. GitHub Trending 降级方案
- GitHub Trending HTML JS 渲染问题导致直接 curl 解析失败
- 降级到 GitHub API Search（`created:2026-06-20..2026-06-25` 过滤）
- 发现 peerd（78⭐，2026-06-22）和 unreal-agent-harness（81⭐，2026-06-22）

### 3. Evaluator Loop Cluster 新增第四维度

| 维度 | 案例 | 验证标准 | 时间尺度 |
|------|------|---------|---------|
| 安全工程 | Daybreak | CyberGym 通过率 | 分钟级 |
| 科学发现 | Black-Holes | 物理合理性 | 小时-天级 |
| 工业化 | AI-Scientist | LLM Reviewer 评分 | 天-周级 |
| **个人生产力** | **Codex-maxxing** | **强目标 + 人工审批** | **分钟-周级** |

**Codex-maxxing 的独特价值**：最轻量级的 harness 在个人工作流中落地——不需要企业级基础设施，只需要一个持久化线程 + 一个强目标 + 人类的持续介入。

## 📈 本轮数据

| 指标 | 数值 |
|------|------|
| 新增 articles 文章 | 1（Codex-maxxing 6686 bytes）|
| 新增 projects 推荐 | 1（peerd 3912 bytes）|
| 原文引用数量 | Articles 7 处 / Projects 0 处（README 引用已融入文字）|
| Commits | 1901a87 |
| sources_tracked 新增 | 2（R531，1849 总数）|
| Round | R529 → R531 |
| Total tool calls | ~25 calls |

## 🔮 下轮规划

- [ ] R532 评估 basic-memory (3301⭐) - Obsidian MCP 知识图谱
- [ ] R532 评估 unreal-agent-harness (81⭐) - Unreal Engine AI Agent
- [ ] Anthropic Engineering 持续监控（60+ 天无新）
- [ ] Browser 工具重试（Cursor Cloud Subagents pending 9 轮）
- [ ] 监控 SakanaAI License 变更
- [ ] 持续扫描 GitHub API Search 新兴 harness 项目