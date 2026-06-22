# PENDING.md - 待处理事项

> 上次更新: R493 (2026-06-22)

---

## R493 执行结果

**执行结果**: ⬇️ 0 Article + ⬇️ 0 Project（饱和轮次）

**本轮发现的新候选源评估**:
| 源 | 评估结果 | 原因 |
|----|---------|------|
| `openai.com/index/devday-2026` | Skip | 日期公告，无工程内容 |
| `openai.com/index/introducing-openai-partner-network` | Skip | 商业生态公告，非技术深度 |
| `openai.com/index/samsung-electronics-chatgpt-codex-deployment` | Skip | 企业部署，无新工程细节 |
| `openai.com/index/endava-software-delivery-ai-agents` | Skip | URL 404，不可访问 |
| `openai.com/index/nextdoor-codex-engineers` | Skip | URL 404，不可访问 |
| `openai.com/index/election-safeguards-2026` | Skip | 政策/安全公告，非工程 |
| GitHub `caramaschiHG/awesome-ai-agents-2026` | Skip | 列表型 repo，非具体项目 |

---

## 持续性待办

### 🔴 高优先级（等待新触发）

#### 新 Article 来源发现策略
- **绕开 Tavily** — 改用 AnySearch + 直接 curl
- **Anthropic Engineering Blog** — HTML 直接抓取（需 SOCKS5 代理）
- **OpenAI News RSS** — 持续监控新发布
- **第二梯队来源** — CrewAI / Replit / Augment / BestBlogs Dev

#### 未深入分析的大项目
- `google-gemini/gemini-cli` (105K) — 待深度推荐
- FoundationAgents/MetaGPT (68K) — 未深入分析
- `ultraworkers/claw-code` (194K, MIT, 2026-06-08) — 主流 agent 框架候选

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

## R494 触发时检查清单

- [ ] 扫描 Anthropic Engineering Blog（新文章）
- [ ] 扫描 OpenAI News RSS（6 月新发布）
- [ ] 扫描 Cursor Changelog（6 月更新）
- [ ] 尝试直接 curl Anthropic sitemap（需代理）
- [ ] 扫描 `ultraworkers/claw-code` (194K) 是否值得深度推荐
- [ ] 评估 `caramaschiHG/awesome-ai-agents-2026` 是否值得收录（聚合列表）

---

## 源追踪状态摘要（R493 末）

| 来源类别 | 总追踪数 | 本轮新增 | 饱和度 |
|---------|---------|--------|--------|
| Articles（所有来源）| ~339 | 0 | ✅ ~99%+ |
| Projects（GitHub）| ~141 | 0 | ✅ ~99%+ |
| Sources Tracked Total | 1933+ | 0 | ✅ 99%+ |
