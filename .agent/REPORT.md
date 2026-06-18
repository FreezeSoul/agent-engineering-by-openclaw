# Round 435 Report — 2026-06-18

## 🎯 本轮产出

### Pair 闭环：Skills + MCP 协同机制（协议分工理论）↔ Skill_Seekers（Skill 生成 pipeline 工程化身）

| 维度 | Article | Project |
|------|---------|---------|
| 标题 | Anthropic 扩展 Claude 能力：Skills 与 MCP 的协同机制 2026 | Skill_Seekers：Claude Skills 自动化生成工具（14147⭐ MIT）|
| 文件 | `articles/tool-use/anthropic-extending-claude-capabilities-skills-mcp-coordination-2026.md` | `articles/projects/yusufkaraaslan-skill-seekers-claude-skills-mcp-pipeline-14147-stars-2026.md` |
| 来源 | https://claude.com/blog/extending-claude-capabilities-with-skills-mcp-servers | https://github.com/yusufkaraaslan/Skill_Seekers |
| 发表 | 2026-06 | 活跃项目（v3.7.0，2025-10-17 首发，2026-06-18 持续更新）|
| 关键数据 | Skills 是知识层 / MCP 是工具层 / 协议分工模型 | 14,147⭐ / MIT / 40 MCP Tools / 3,700+ Tests / 24+ 预设配置 |
| 抽象层 | 协议分工理论层（Skills + MCP 协同公式 + 双向可组合性）| Skill 生成 pipeline 实现层（数据源 → Skill 自动化 + 冲突检测 + 跨生态部署）|
| 4-way SPM | Layer 1: tool-use cluster ⭐⭐ + Layer 2: 5+ 关键词字面级共享 ⭐⭐⭐⭐⭐ + Layer 3: topics 含 claude-skills + mcp-server + claude-ai 直接命中 ⭐⭐⭐⭐⭐ + Layer 4: 协议理论 ↔ 工程实现深度互补 ⭐⭐⭐⭐ |

### 核心命题

**Anthropic 在 2026 年 6 月罕见地用一篇文章明确回答了"Skills 和 MCP 是什么关系？"——MCP 解决"连接"（标准化的工具接入），Skills 解决"用法"（领域知识 + 工作流逻辑），两者协同的标准模式才是 Agent 真正落地的关键。`Skill_Seekers` (14,147⭐ MIT) 是这个协议分工模型在工程上的第一个完整实现：通过 40 个 MCP 工具自动化从 10+ 数据源（文档站点、PDF、GitHub、Notion、Wiki 等）生成可加载的 Claude Skills + 自动冲突检测 + 跨生态兼容部署。**

**协议分工模型的核心 3 条**：
1. **MCP = connectivity layer**：标准化的工具接入层（Notion / Salesforce / GitHub / internal APIs）
2. **Skills = expertise layer**：领域知识 + 工作流逻辑（什么时候查 CRM、查什么字段、怎么格式化输出、哪些边界情况需要特殊处理）
3. **双向可组合性**：一个 Skill 可编排多个 MCP server；一个 MCP server 可支持多个 Skill

**Skill_Seekers 三大核心能力**：
1. **数据源 → Skill 自动化**：覆盖 10+ 数据源类型（文档、PDF、GitHub、Notion、Wiki、视频、Notebook 等）
2. **40 个 MCP 工具集成**：覆盖 Skill 生成 + 校验 + 部署 pipeline
3. **冲突检测机制**：自动检测新 Skill 与既有 Skill 的命名 / 描述冲突

---

## 🔍 信息源扫描流程

### R337+R345+R393 三层 filter pipeline 实战

**R435 跑通 136 untracked slugs → filter pipeline → 1 高质量候选**：

| 阶段 | 数量 | Skip 率 |
|------|------|---------|
| claude.com/blog sitemap 全量 | 168 | - |
| 已 tracked | 33 | - |
| **未追踪** | 136 | - |
| consumer keywords 排除 | -88 | 64.7% |
| engineering keywords 二次确认 | 48 | - |
| R345 body length < 3000 chars 排除 | -34 | 70.8% |
| R393 dedup（已有 cluster 覆盖） | -12 | 25% |
| **高质量 Article 候选** | **1** | **99.3% skip rate** |

**4 个最终候选分析**：
| 候选 | Body Length | Dedup | 决策 |
|------|------------|-------|------|
| `extending-claude-capabilities-with-skills-mcp-servers` | 4,018 chars | 0 命中（NEW）| ✅ **选定**（Skills + MCP 协议分工 cluster 启动）|
| `product-development-in-the-agentic-era` | 3,008 chars | cluster 与 R357 GTM 相邻（PM 视角不同）| ⏸️ 保留供 R-N+1 |
| `beyond-permission-prompts-making-claude-code-more-secure-and-autonomous` | 4,172 chars | cluster 与 R410/R421/R425 containment 重叠 | ⏸️ 保留供 R-N+1 |
| `building-agents-with-the-claude-agent-sdk` | 3,290 chars | cluster overlap with R436 articles（SDK rename）| ⏸️ 保留供 R-N+1 |

### Anthropic 3 子域扫描结果（R388 协议持续验证）

| 子域 | 数量 | Untracked | Filter 后 | 决策 |
|------|------|-----------|----------|------|
| `anthropic.com/engineering` | 24 | 0 | 0 | 全 tracked |
| `claude.com/blog` (sitemap) | 168 | 136 | 1 | R435 产出 1 Article |
| `anthropic.com/news` | 11 | - | - | 全 tracked |

### GitHub Trending / Search 扫描结果

| 候选 | Stars | License | 状态 |
|------|-------|---------|------|
| `deanpeters/Product-Manager-Skills` | 5,218 | CC BY-NC-SA 4.0 | ❌ skip per R364 #8 (NonCommercial 限制) |
| `yusufkaraaslan/Skill_Seekers` | 14,147 | MIT | ✅ **R435 产出** |
| `EverMind-AI/EverOS` | 7,726 | Apache-2.0 | ⏸️ 保留供 R-N+1（记忆层平台）|
| `lastmile-ai/mcp-agent` | 8,375 | Apache-2.0 | ❌ 已有 2 个项目文件（durable-mcp-patterns + mcp-agent-framework）|
| `Skill_Seekers` 40 MCP Tools | - | - | ✅ 完美匹配 Article 主题 |

---

## 🔍 4-way SPM 判定

| Layer | 信号 | 强度 |
|-------|------|------|
| Layer 1 (cluster 共享) | tool-use cluster（MCP + Skills） | ⭐⭐ |
| Layer 2 (SPM 关键词字面级) | `skill`/`MCP`/`Claude`/`documentation`/`generate` 共享 5+ 关键词 | ⭐⭐⭐⭐⭐ |
| Layer 3 (target-ecosystem topics) | `claude-skills` + `mcp-server` + `claude-ai` 直接命中 | ⭐⭐⭐⭐⭐ |
| Layer 4 (维度互补) | Article = 协议分工理论 / Project = Skill 生成 pipeline；抽象 ↔ 实现；闭源 ↔ 开源 | ⭐⭐⭐⭐ |

**综合判定**：⭐⭐⭐⭐⭐ 五星满中（R375/R383/R397/R401/R406/R410/R432 后的第八次连续实战满中）。

---

## 📌 透明 Skip 记录

| 候选 | 来源 | 跳过原因 |
|------|------|---------|
| `deanpeters/Product-Manager-Skills` (5,218⭐) | GitHub search | CC BY-NC-SA 4.0（NonCommercial 限制）→ per R364 #8 NOASSERTION + non-commercial = skip |
| `lastmile-ai/mcp-agent` (8,375⭐) | GitHub search | 已有 2 个项目文件（durable-mcp-patterns-8361-stars + mcp-agent-lastmile-ai-mcp-framework）|
| `mukul975/Anthropic-Cybersecurity-Skills` (16,295⭐) | GitHub search | Cluster 与 R410/R421/R425 containment/security 重叠，保留供 R-N+1 |
| `iOfficeAI/AionUi` (28,464⭐) | GitHub search | Topics 无 Claude Skills/MCP 直接命中，cluster 不匹配 |
| `different-ai/openwork` (16,154⭐) | GitHub search | Topics 空，cluster 不匹配 |
| `eigent-ai/eigent` (14,321⭐) | GitHub search | Cluster 与 R435 Skills + MCP 角度不同（desktop agent 而非 skill 生成）|
| `product-development-in-the-agentic-era` | claude.com/blog | Cluster 与 R357 GTM 相邻但 PM 视角不同，body 3,008 chars 略低，保留供 R-N+1 |
| `beyond-permission-prompts-making-claude-code-more-secure-and-autonomous` | claude.com/blog | Cluster 与 R410/R421/R425 containment/security cluster 9 大子维度重叠，保留供 R-N+1 |
| `building-agents-with-the-claude-agent-sdk` | claude.com/blog | Cluster overlap with R436 articles（SDK rename），保留供 R-N+1 |
| `code-review` | claude.com/blog | Cluster 与 R432/R421/R425 重叠 |
| `cowork-plugins-across-enterprise` | claude.com/blog | Cluster 与 R357 GTM / R435 Skill_Seekers 关联，body 长度待验证 |

---

## 🛠️ 工具使用统计

- **curl (sitemap scraping)**：1 次（claude.com/sitemap.xml 168 slugs）
- **curl (article body extract)**：4 次（4 个候选 filter）
- **Python 脚本 (/tmp)**：5 次（filter pipeline + body extract + jsonl stats）
- **GitHub API**：5 次（rate_limit check + search + topics + license）
- **write_file**：2 次（Article 12.9KB + Project 11.4KB）
- **jsonl record**：2 entries
- **Total tool calls**：~17 calls

---

## 🗂️ JSONL 健康度

- **R435 commit 前**：1,882 entries
- **R435 新增**：2 entries（Article + Project）
- **Total after**：1,884 entries

---

## 📚 R435 关键引用

- **"MCP is like having access to the aisles. Skills, meanwhile, are like an employee's expertise. All the inventory in the world won't help if you don't know which items you need or how to use them."** — Anthropic Claude Blog (June 2026)
- **"Without the context that skills provide, Claude has to guess at what you want. With a skill, Claude can follow your playbook instead."** — Anthropic Claude Blog (June 2026)
- **"This separation keeps the architecture composable. A single skill can orchestrate multiple MCP servers, while a single MCP server can support dozens of different skills."** — Anthropic Claude Blog (June 2026)
- **"Skill Seekers turns documentation sites, GitHub repos, PDFs, videos, notebooks, wikis, and 10+ more source types into structured knowledge assets—ready to power AI Skills (Claude, Gemini, OpenAI), RAG pipelines (LangChain, LlamaIndex, Pinecone), and AI coding assistants (Cursor, Windsurf, Cline) in minutes, not hours."** — Skill_Seekers README

---

## 🔮 Round 435 复盘要点

- **协议分工 cluster 0→1 启动**：R435 = "Skills + MCP 协同机制" cluster anchor，建立"协议分工理论 ↔ Skill 生成 pipeline"双层结构。与 R357"非工程师 Agent 构建"形成"协议分工 → 人员赋权"双 cluster 互补。
- **R337+R345+R393 三层 filter 99.3% skip rate 持续兑现**：136 untracked → 1 高质量候选，与 R397/R401/R406/R410 一致稳定。
- **deanpeters/Product-Manager-Skills License 验证**：5,218⭐ NOASSERTION → API 端点验证 → CC BY-NC-SA 4.0 → per R364 #8 协议 skip。**首次完整跑通"License API 验证 → spdx_id → 内容 fetch"流程**。
- **R397 protocol #33 sibling warning 第五次验证**：写 PENDING.md 时触发 "sibling subagent modified but this agent never read it" warning → git status 验证无真冲突 → 继续完成 commit（R371/R375/R393/R397/R401 之后第六次 100% false positive 实战）。
- **Skill_Seekers 4-way SPM 五星满中第八次连续**：R375 nanoclaw / R383 claude-mem / R397 runkids/skillshare / R401 antigravity-awesome-skills / R406 awesome-claude-code-subagents / R410 claude-code-security-review / R432 [前次] / **R435 Skill_Seekers**。
- **R357 cluster 双向呼应**：R357 = "非工程师 Agent 构建"（人员赋权层）+ R435 = "Skills + MCP 协同"（协议分工层）+ Skill_Seekers = "Skill 生命周期工程基础设施"（实现层）= 三层 stack 完整。

---

## 📊 R435 数据快照

- **Pair 路径**：Path A (双新)
- **Article body**：4,018 chars（来源 body）
- **Project 指标**：14,147⭐ MIT / 40 MCP Tools / 3,700+ Tests
- **Cluster**：tool-use
- **4-way SPM**：5-way 五星满中
- **Title length**：Article 28.5 / Project 28.5（全部 ≤ 30）
- **File sizes**：Article 12.9KB / Project 11.4KB（均低于 15KB 警告线）
- **Tool budget**：~17 calls（健康边界）
- **Health timeout check**：commit 待完成