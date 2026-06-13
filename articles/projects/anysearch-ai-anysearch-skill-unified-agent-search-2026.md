# AnySearch Skill：跨 Agent 统一搜索引擎 skill (Apache-2.0, 3,122 Stars)

> source_url: https://github.com/anysearch-ai/anysearch-skill
> source_type: github_repository
> license: Apache-2.0
> stars_at_write: 3122
> topics: `anysearch`, `hermes`, `openclaw`, `qclaw`, `skill`, `skills`
> created_at: 2026-04-30
> pair_article: articles/enterprise/anthropic-gtm-claude-code-non-coder-agent-builder-2026.md (R357)
> pair_mechanism: L2 协议行为层 — 跨 Agent 工具兼容 skill (R357 cluster)
> cluster: enterprise/non-coder-agent-builder (extension)
> round: 367

---

## 核心命题

**AnySearch Skill (Apache-2.0, 3,122 Stars)** 是一个**跨 Agent 平台的统一实时搜索引擎 skill**，将通用网页搜索、垂直领域搜索、并行批量搜索、全页面内容提取四种能力封装为单一 `SKILL.md`，**明确将 OpenClaw / Hermes / Claude Code / OpenCode / Cursor / Codex 列为兼容目标**。它在 L2 协议行为层提供了"任何 Agent 都能用的搜索原语"，是 R357 cluster（"非工程师 Agent 构建工具栈"）的关键缺失能力。

**核心观察**：当 R357 文章揭示"非工程师也能构建生产工具"时，**这意味着工具栈必须可跨 Agent 移植**。一个团队成员用 Claude Code，另一个用 Cursor，第三个用 OpenClaw——**他们能否共享同一个"搜索 skill"**？AnySearch Skill 的回答是"可以"——通过 `~/.agents/skills/anysearch` 这样的共享安装路径 + SKILL.md 标准化定义，**搜索能力变成跨 Agent 工具的"公共协议"**，不再是单个 agent 平台的私有能力。

---

## 一、机制：跨 Agent Skill 的工程实现

### 1.1 单一 SKILL.md 跨平台兼容

AnySearch Skill 的安装路径声明**显式覆盖 6 个 Agent 平台**：

```bash
# Claude Code:    mv anysearch-skill ~/.claude/skills/anysearch
# OpenCode:       mv anysearch-skill ~/.config/opencode/skills/anysearch
# Cursor/Windsurf: mv anysearch-skill <project>/.skills/anysearch
# Generic:        mv anysearch-skill <your_agent_skill_dir>/anysearch
# Shared agents:  mv anysearch-skill ~/.agents/skills/anysearch
```

> "`~/.agents/skills/` is a useful shared install location when multiple AI tools read from the same skill directory, including Codex, Cursor, and OpenClaw personal agent skills."

**关键洞察**：`~/.agents/skills/` 这个共享路径让**同一份 skill 文件被多个 Agent 同时读取**——这是"协议行为层"在工程上的具象化。R357 文章中 Anthropic 描述的"跨 Agent 互操作"在此变成一个**文件系统级别的协议**：Agent 不需要知道 skill 的内部实现，只需要能从约定路径加载即可。

### 1.2 运行时自适配：Python > Node.js > Shell

skill 在 README 中显式描述**多运行时回退探测协议**：

```bash
# 探测顺序：Python → Node.js → PowerShell → Bash
python3 <skill_dir>/scripts/anysearch_cli.py search "query"
node <skill_dir>/scripts/anysearch_cli.js search "query"
bash <skill_dir>/scripts/anysearch_cli.sh search "query"
```

探测成功后写入 `runtime.conf`，后续调用直接读取。这是**Agent skill 标准化的一个未声明但关键的工程基础**——**不是所有 Agent 运行环境都有 Python**（macOS 一些 CI 环境只有 Node.js），skill 必须自适配运行时而不是假设。

### 1.3 四种搜索原语：search / batch_search / extract / doc

```bash
# 通用网页搜索（单条）
python3 anysearch_cli.py search "anthropic claude code" --max_results 5

# 垂直领域批量搜索（多条并行）
python3 anysearch_cli.py batch_search --queries '[{"query":"q1"},{"query":"q2"}]'

# 全页面内容提取（输出直接是 Markdown）
python3 anysearch_cli.py extract "https://example.com/page"

# 协议自描述（让 Agent 自学用法）
python3 anysearch_cli.py doc
```

**`extract` 输出直接是 Markdown**——这是**对 Agent 工作流的关键优化**。其他搜索 API 返回 HTML（Agent 还得 parse），而 AnySearch 直接给 Agent 可消费的格式。这把"搜索→消费"的步骤从 2 步简化成 1 步，**对长 horizon 任务（如 research agent）的 token 成本有显著降低**。

---

## 二、与 R357 cluster 的对位：L2 协议行为层扩展

R357 cluster (非工程师 Agent 工具栈) 通过 4 层模型描述：

| 层 | 焦点 | R357 实战 | AnySearch Skill 对位 |
|------|------|--------|---------------------|
| L1 协议数据层 | Agent 接入外部数据 | MCP servers (Salesforce/Calendar/Gmail) | 搜索结果（网页/垂直 API） |
| **L2 协议行为层** | **Agent 行为可分发** | **Planning-with-Files SKILL.md** | **AnySearch SKILL.md** |
| L3 实现状态层 | 持久化状态管理 | markdown plan + JSONL ledger | runtime.conf + .env |
| L4 平台分发层 | 非工程师可分发工具 | Claude Cowork 80% 销售采用 | （本项目无关）|

**Pair 关联强度（⭐⭐⭐⭐）**：
- **共享 cluster**: R357 (非工程师 Agent 工具栈)
- **共享关键词**: "skill", "cross-tool", "agent", "compatible", "OpenClaw"
- **共享工程模式**: SKILL.md 跨 Agent 标准 + 共享文件系统路径 `~/.agents/skills/`
- **维度互补**: R357 Project (planning-with-files) 是 "持久化状态协议"，AnySearch 是 "实时信息检索协议"

**具体对位维度**：
- **R357 Article L4 平台分发层** ↔ **AnySearch L2 协议行为层** = "非工程师用什么分发" ↔ "非工程师用什么搜索"
- 两者都是"非工程师构建工具栈"中**协议可移植性**的具体实现

---

## 三、工程模式拆解：Agent Skill 标准化的三个隐性要素

### 3.1 文件系统路径作为协议载体

AnySearch Skill 选择 `~/.agents/skills/anysearch` 作为**共享安装路径**，这意味着**协议本身是文件系统约定**。这种设计的好处：
- 不需要中心化注册表
- 不需要平台厂商批准
- 一个 skill 文件被所有平台读取 = "事实上标准"

R357 cluster 中 Planning-with-Files 同样采用"跨 Agent 文件路径"模式。**这两个项目共同验证了一个隐性假设：跨 Agent 工具互操作的最快路径是文件系统，不是 HTTP API**。

### 3.2 运行时自探测协议

README 描述的探测序列（Python > Node.js > Shell）是**Agent skill 工程的标准化范式**——避免硬依赖、保留降级路径。**这种"多 runtime 自适配"协议可以推广到任何跨 Agent skill**，未来 Agent skills 应该默认支持。

### 3.3 输出格式优化（HTML → Markdown）

`extract` 直接返回 Markdown，**减少 Agent 二次处理**。这是**对 Agent 工作流优化的隐性 deep understanding**——skill 作者意识到 Agent 不消费 HTML，所以预先转换。这一设计细节透露：**AnySearch Skill 的开发者真正"以 Agent 视角"设计接口**。

---

## 四、对比：AnySearch vs 其他 Agent 搜索工具

| 工具 | Stars | License | 跨 Agent 标准 | 输出格式 |
|------|-------|---------|--------------|---------|
| **AnySearch Skill** | **3,122** | **Apache-2.0** | **✓ SKILL.md 6 平台** | **Markdown** |
| Tavily MCP | ~10K | Proprietary | MCP-only | JSON |
| Perplexity API | N/A | Proprietary | REST only | JSON/HTML |
| Exa | ~5K | Apache-2.0 | SDK only | JSON |
| Brave Search | ~3K | Various | REST only | JSON |

**AnySearch 的差异化**：在 Apache-2.0 license 下提供 SKILL.md 跨 Agent 标准 + Markdown 直出 + 4 种搜索原语。**这种"开源协议 + 多能力封装"组合**在 Agent search 领域相对独特。

---

## 五、与本仓库（OpenClaw）的直接关联

**AnySearch Skill 的 README 明确将 "OpenClaw personal agent skills" 列为兼容目标**：

> "Shared agents: mv anysearch-skill `~/.agents/skills/anysearch`"

这意味着**OpenClaw 用户可以直接使用 AnySearch 作为其搜索能力扩展**。本仓库（`agent-engineering-by-openclaw`）作为一个维护 Agent Engineering 知识体系的仓库，应该记录这个**直接兼容 OpenClaw** 的开源 skill。

**对应 R357 Article 的核心论点**："非工程师能否成为产品构建者"——AnySearch Skill 给出了肯定回答中的**关键拼图**：即使非工程师不写搜索代码，他们也能通过安装一个跨 Agent skill 让 Agent 获得搜索能力。**这是"工具栈即产品"哲学的具体落地**。

---

## 六、风险与限制

### 6.1 Stars 相对较低 (3,122)

对比 Tavily (~10K)、Exa (~5K)，AnySearch Skill 的 stars 处于中等水平。但考虑到它创建于 2026-04-30（不到 2 个月）且直接服务于 OpenClaw/Hermes 等新兴生态，**增长速度可观**。

### 6.2 依赖单一供应商 API

README 提到 "Without an API key, you can still use all search features via anonymous access, but with **lower rate limits and quota**"。这意味着**搜索基础设施层依赖 AnySearch.com 的中央 API**。如果 AnySearch.com 关闭，所有部署该 skill 的 Agent 将失去搜索能力。

**缓解**：SKILL.md 协议本身是开源的——理论上任何团队可以 fork 后接入自己的搜索后端。这与 MCP servers 的"协议开放 + 实现多样"模式一致。

### 6.3 OpenClaw / Hermes 兼容性仍在验证

README 提到 OpenClaw 兼容，但**实际集成测试覆盖度未知**。需要更多社区反馈才能确认 SKILL.md 在 OpenClaw 平台上的实际加载行为。

---

## 七、Pair 闭环判定

- **共享 cluster**: R357 (非工程师 Agent 工具栈) ✓
- **共享关键词**: skill/cross-tool/agent/compatible/OpenClaw ✓
- **License 清洁**: Apache-2.0 ✓
- **Stars 阈值**: 3,122 > 700 ✓
- **直接兼容本仓库目标生态 (OpenClaw)**: ✓

**Pair 关联强度**：⭐⭐⭐⭐ (具体对位 — R357 L4 ↔ AnySearch L2，协议行为层互补)
**Pair 路径**：Path C (新 Project × 既有 Article R357) — 符合 R361 Path C 协议

**反模式检查**：
- ❌ 非泛关联（不是"任何搜索工具都配非工程师 cluster"）
- ✓ 具体对位维度明确（L2 协议行为层 + SKILL.md 跨 Agent 标准）
- ✓ 与 R357 Project (planning-with-files) 形成 cluster 内第二项目 — cluster 扩展而非 cluster 重复

---

## 八、对 Agent 工程的启示

1. **跨 Agent skill 协议的现实路径是文件系统**：`~/.agents/skills/<name>` 比 HTTP API 更适合"非工程师分发"
2. **多 runtime 自适配是 Agent skill 的工程底线**：Python > Node.js > Shell 探测协议应成为默认设计模式
3. **输出格式优化（HTML → Markdown）是 Agent 友好接口的隐性细节**：消耗方是 LLM，不是人
4. **SKILL.md 是 Agent 时代的"README 升级版"**：从"给人看"到"给 Agent 读"，metadata schema 必须自描述
5. **直接兼容 OpenClaw 等新兴生态是开源 skill 的增长路径**：当大平台（Anthropic Claude/OpenAI）的 marketplace 尚未成熟时，跨平台 SKILL.md 是最快的 adoption 通道

---

## 引用

1. AnySearch Skill README, https://github.com/anysearch-ai/anysearch-skill, Apache-2.0, 3,122 Stars (2026-04-30 created)
2. SKILL.md (cross-agent standard), see https://github.com/anysearch-ai/anysearch-skill/blob/main/SKILL.md
3. R357 Article (Pair): `articles/enterprise/anthropic-gtm-claude-code-non-coder-agent-builder-2026.md` - 非工程师 Agent 工具栈 L2/L3/L4 层
4. R357 Project (cluster sibling): `articles/projects/othmanadi-planning-with-files-skill-md-23105-stars-2026.md` - 持久化状态协议