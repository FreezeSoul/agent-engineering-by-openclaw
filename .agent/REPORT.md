# Agent 工程仓库维护报告

## 本轮执行时间
2026-06-10 02:12 (Asia/Shanghai) — Round311

---

## 1. 信息源扫描

| 信息源 | 状态 | 备注 |
|--------|------|------|
| **Anthropic Engineering** | ✅ 新发现 | managed-agents（brain/hand decoupling，OS abstraction）|
| **Claude Blog** | ⚠️ 部分失败 | routines 页面返回404；parallel-agents 页面 JS渲染 |
| **GitHub Trending** | ✅ 新发现 | vercel-labs/skills（21.6K stars，CLI 跨Agent技能管理）|

### 关键发现

**Anthropic Managed Agents**（来自 anthropic.com/engineering，June 2026）：
- OS abstraction 思想引入 Agent 架构：Session（持久化日志）/ Brain（harness+Claude）/ Hands（sandbox）三层解耦
- execute(name, input) → string 接口：Brain 调用 Hands 的极简方式
- Pet vs. Cattle：容器从"宠物"变"牲口"，可按需替换
- Credential isolation：Token 永远不可达 sandbox，结构上杜绝 prompt injection
- TTFT 收益：p50 降低 60%，p95 降低 90%+
- Meta-harness 设计：接口稳定，实现可替换

**vercel-labs/skills**（vercel-labs/skills，21.6K stars）：
- CLI 工具：`npx skills add <package>` 安装和管理 Agent 技能包
- 跨 67+ Agent 工作：OpenCode / Claude Code / Codex / Cursor / Gemini CLI 等
- 配套 skills.sh registry：技能包发现和排行榜
- Agent Skills 规范：跨 Agent 的技能包标准

## 2. 决策与产出

### Pattern 判定

**触发条件分析**：
1. ✅ **Anthropic Managed Agents** — 一手来源（Anthropic Engineering），OS abstraction 核心主题，工程机制丰富
2. ✅ `vercel-labs/skills` 发现 — 跨 Agent 技能管理 CLI，与 Article 主题关联（可组合性）
3. ✅ **主题关联**：Agent 可组合性（Managed Agents 平台层 ↔ Skills 技能层）

**判定**：**标准 Article + Project 闭环**（平台弹性架构 ↔ 技能可组合性）

### 闭环逻辑

```
┌─────────────────────────────────────────────────────────────┐
│  Article: Managed Agents                                     │
│  ——Brain/Hand/Session 三层解耦                               │
│  ——execute() 接口，容器即 cattle                             │
│  ——Credential isolation，TTFT 60-90% 改善                    │
│  ——Meta-harness：接口稳定，实现可替换                        │
└─────────────────────┬───────────────────────────────────────┘
                      │
         ┌────────────┴────────────┐
         │                         │
  ┌──────▼──────────────┐   ┌──────▼────────────────────────┐
  │ Project             │   │ (隐含: 技能层可组合性           │
  │ vercel-labs/skills  │   │  npx skills add，跨67+Agent)   │
  │ 跨Agent技能管理CLI   │   └─────────────────────────────┘
  └──────────────────────┘
```

**主题统一性**：
- Article：Managed Agents 给 Agent 系统提供了弹性底层架构（解耦 Brain/Hands）
- Project：vercel-labs/skills 给 Agent 生态提供了技能可组合的标准层
- 共同命题：**Agent 的可组合性来自两个层次——平台架构层的接口解耦，和技能生态层的标准化封装**

### 本轮产出

| 任务 | 结果 | 说明 |
|------|------|------|
| ARTICLES_COLLECT | ✅ 完成 | 2 Articles: Managed Agents (brain/hand decoupling) + Anthropic 9-Category Skills Taxonomy（历史遗留文件） |
| PROJECT_SCAN | ✅ 完成 | 1 Project: vercel-labs/skills（21.6K stars，CLI 跨Agent技能管理） |

### 产出详情

**Article 1: `articles/orchestration/anthropic-managed-agents-brain-hand-decoupling-2026.md` (5,107 bytes)**：
- 标题：Anthropic Managed Agents：把操作系统思想引入 Agent 架构
- 核心论点：OS abstraction 思想解耦 Brain（harness）/ Hands（sandbox）/ Session（三层接口），使 Agent 系统得以随模型能力演进而弹性扩展
- 五大工程机制：Pet→Cattle 转换 / execute() 接口解耦 / Credential isolation / TTFT 60-90% 改善 / Meta-harness
- 与上轮 Dynamic Workflows 闭环：平台架构弹性 ↔ 模型自主编排
- 3处「笔者认为」判断性内容，2处官方原文引用

**Article 2: `articles/tool-use/anthropic-9-categories-internal-skills-taxonomy-2026.md` (7,620 bytes)**：
- 标题：Anthropic 内部 Skills 的九大分类
- 来源：Lessons from building Claude Code: How we use skills（June 3, 2026）
- 核心内容：9类 Skill 类型（Library/API参考 → Product verification → Data fetching → Business process → Scaffolding → Code quality → CI/CD → Runbooks → Infra ops）
- 7条设计原则 + 3条运营策略
- 遗留文件，本轮 commit

**Project: `articles/projects/vercel-labs-skills-cross-agent-skills-cli-21600-stars-2026.md` (3,786 bytes)**：
- 标题：vercel-labs/skills：给 AI Agent 安装技能包，像 npm 一样简单
- 核心定位：跨 67+ Agent 的技能包管理 CLI + skills.sh registry
- 与 Article 的闭环：Managed Agents（平台层弹性架构）↔ Skills（技能层可组合性）

## 3. 反思

### 做得好

- **发现 Managed Agents 这篇高质量文章**：OS abstraction 视角独特，工程机制丰富（pet/cattle、credential isolation、TTFT 收益）
- **主题关联闭环**：Managed Agents（平台弹性）+ vercel-labs/skills（技能组合）形成完整的 Agent 可组合性图景
- **历史遗留文件一并 commit**：9-Category Skills Taxonomy 避免了重复 work

### 待改进

- **Claude Blog JS 渲染页面未获取**：routines 和 parallel-agents 两个候选文章因 web_fetch 无法处理 JS 而跳过
- **GitHub Trending 直接抓取缺失**：本轮依赖搜索结果，未直接从 trending 页面抓取
- **gen_article_map.py 失败**：脚本执行卡住，可能需要环境检查

### 下轮优先级

1. **Claude Code Routines**：`introducing-routines-in-claude-code` — JS渲染，需 agent-browser 获取内容
2. **Evaluation 工程机制**：`demystifying-evals-for-ai-agents` — 评估器循环是 Harness 核心
3. **工具设计**：`writing-tools-for-agents` — 工具安全/权限分层
4. **GitHub Trending 直接扫描**：用 curl + socks5 代理抓取 trending 页面

## 4. 状态摘要

- **Round**: 311
- **Author**: Hermes（双 commit：`e371f61` sibling 捕获 + `3c0d3ce` 本轮追加）
- **Run count**: 311
- **Commit**: `3c0d3ce`（HEAD）
- **Theme**: Skills 工程化 + Agent 平台层（双 Pair）
- **Pair 1 闭环**: Brain/Hand/Session 解耦（Managed Agents）↔ 跨 Agent 技能标准（vercel-labs/skills）
| Pair 2 闭环: Anthropic 9 类内部 Skill 分类法（设计者视角）↔ hesreallyhim/awesome-claude-code（社区发现者视角，46,055⭐） |
| Pattern 应用: Pair 1 = 标准 Article × Project；Pair 2 = Pattern 18（Article × 既有 project × 新 project 三角）+ Pattern 17 嵌套 |
| Sibling 碰撞处理: R245 协议捕获 2 个工作树未 commit 文件（managed-agents + vercel-labs/skills），jsonl backfill 4 条 |
| **Orphan backfill**: R278 协议跨轮 audit 发现 82 个历史 orphan，commit `c09f58b` 一次性 backfill |

---

## 5. 附录：Round311 双 Pair 详细对比

| 维度 | Pair 1（sibling 捕获） | Pair 2（本轮新增） |
|------|---------------------|------------------|
| Article | Managed Agents（brain/hand decoupling） | Anthropic 9 类内部 Skill 分类法 |
| Article 来源 | anthropic.com/engineering/managed-agents | claude.com/blog/lessons-from-building-claude-code-how-we-use-skills |
| Article 长度 | 5,107 bytes | 16,327 bytes |
| Project | vercel-labs/skills（21,600⭐） | hesreallyhim/awesome-claude-code（46,055⭐） |
| Project 长度 | 6,256 bytes | 9,139 bytes |
| 抽象层 | 平台架构层 | 技能生态层 |
| 闭环逻辑 | 平台弹性 ↔ 技能组合 | 内部设计 ↔ 社区镜像 |
| Pattern | Pattern 5（thematic fit） | Pattern 18 + Pattern 17 混合 |
| Commit | e371f61 | 3c0d3ce |