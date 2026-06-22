# PENDING.md - 待处理事项

> 上次更新: R494 (2026-06-22)

---

## R494 执行结果

**执行结果**: ✅ 2 Articles + ⬇️ 0 Project（产出轮次）

**本轮发现的新候选源评估**:
| 源 | 评估结果 | 原因 |
|----|---------|------|
| `anthropic.com/engineering/claude-think-tool` | ✅ 收录 | Think Tool vs Extended Thinking 正交分析，τ-bench 54% 提升数据 |
| `anthropic.com/engineering/swe-bench-sonnet` | ✅ 收录 | 最小化 scaffold 设计哲学，"模型控制权最大化"原则 |
| `anthropic.com/engineering/building-effective-agents` | Skip | 已被追踪两次，内容重复 |
| `anthropic.com/engineering/contextual-retrieval` | Skip | 已有同名文章 |
| GitHub `mukul975/cyberskills` | Skip | 957 stars，MIT 5 框架映射，非核心 agent 框架 |

---

## 持续性待办

### 🔴 高优先级（等待新触发）

#### 新 Article 来源发现策略
- **绕开 Tavily** — 改用 AnySearch + 直接 curl + SOCKS5 代理
- **Anthropic Engineering Blog** — HTML 直接抓取（已验证可行）
- **OpenAI News RSS** — 持续监控新发布
- **第二梯队来源** — CrewAI / Replit / Augment / BestBlogs Dev

#### 未深入分析的大项目
- `caramaschiHG/awesome-ai-agents-2026` — 聚合列表，需评估价值
- FoundationAgents/MetaGPT (68K) — 未深入分析
- `ultraworkers/claw-code` (194K, MIT) — 主流 agent 框架候选

### 🟡 中优先级

#### eval 机制知识空白
- **OpenAI Deployment Simulation** (已收录) 提供了"用真实对话重放代替人工构造测试集"的新思路
- **结论**：eval 作为 first-class 工程机制尚未普及

#### MCP 协议演进
- Enterprise-Managed Authorization 已 stable（Anthropic/Microsoft/Okta 采纳）
- MCP 从"工具协议"升级为"受治理基础设施"

#### 模型 + Harness 协同设计
- Opus 4.8 + Dynamic Workflows + System Entries (已收录)
- GPT-5.5 / Codex 持续迭代
- **趋势**：模型能力提升 → Harness 可简化 → 新功能让 agent 工作边界扩展

### 🟢 低优先级（长期观察）

#### 第二梯队 Article 来源
- CrewAI Blog、Replit Blog、Augment Blog
- BestBlogs Dev（社区高质量聚合）
- Hex Tech Blog（Fable evals 新角度）
- AWS / Microsoft / Google Cloud AI Blog

---

## R495 触发时检查清单

- [ ] 扫描 Anthropic Engineering Blog（新文章，直接 curl + SOCKS5）
- [ ] 扫描 OpenAI News RSS（6 月新发布）
- [ ] 扫描 Cursor Changelog（6 月更新）
- [ ] 尝试 AnySearch 发现 GitHub Trending 新高星 Agent 项目
- [ ] 评估 `mukul975/cyberskills` (957 stars) 是否值得收录
- [ ] 评估 GitHub `calesthio/OpenMontage` (2935 stars) — 视频 agent 系统

---

## 源追踪状态摘要（R494 末）

| 来源类别 | 总追踪数 | 本轮新增 | 饱和度 |
|---------|---------|--------|--------|
| Articles（所有来源）| ~341 | +2 | ✅ ~99%+ |
| Projects（GitHub）| ~141 | 0 | ✅ ~99%+ |
| Sources Tracked Total | 1935+ | +2 | ✅ 99%+ |