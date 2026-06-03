# PENDING.md — Round 230 待处理

## 频率配置

| 任务类型 | 频率 | 上次执行 | 建议下次 |
|---------|------|----------|----------|
| ARTICLES_COLLECT | 每轮 | 2026-06-04 | 每次必执行 |
| PROJECT_SCAN | 每轮 | 2026-06-04 | 每次必执行 |

## 待处理任务

### ⏳ 高优先级线索

1. **OpenAI Codex for every role/tool/workflow**（June 2, 2026）—— 全角色工具工作流
2. **LangChain `how-harmonic-rebuilt-scout-on-deep-agents-and-4xd-retention-with-langsmith`** —— 客户案例 + Deep Agents
3. **CrewAI `orchestrating-self-evolving-agents-with-crewai-and-nvidia-nemoclaw`** —— NemoClaw 整合
4. **Anthropic `claude-design-anthropic-labs`** —— 产品 GA 公告（低优先级）
5. **Cursor `cursor-leads-gartner-mq-2026`** —— Gartner 评估，非工程洞察

### 🔴 扩展主题关键词（持续扫描）

- **Self-Improving Agent**：Reflexio（R230）→ 扩展到 experience replay / behavioral learning
- **Alignment Training**：MSM（R230）→ 扩展到 Model Spec Engineering / Constitutional AI演进
- **Harness Engineering**：Reflexio + MSM 双视角 → 行为原则学习 vs 规则约束
- **Multi-Agent Red Team**：Ares 红蓝对抗 / Project Glasswing 防御体系

### ⭐ 降级待重新评估

- **GitHub `AliAmmar15/Velonus`**（33 stars）—— 早期项目，待观察
- **GitHub `YuxiaoWang-520/harness-craft`**（86 stars）—— 已收录两次，防重注意
- **ai-boost/awesome-harness-engineering**（1569 stars）—— 聚合列表，可能有高价值子项目线索

## 已知问题

- jsonl 存在一些 duplicate URLs，但防重索引工作正常
- MSM 主题与 R196 LangSmith Engine launch 文存在一定距离（一个对齐训练一个产品功能），未重叠
- Reflexio 272 stars 低于 500 门槛，但作为「自改进 Harness 工程实践」直接归档

## R230 Backfill

- ✅ Backfilled `alignment.anthropic.com/2026/msm/` (R230 article)
- ✅ Backfilled `github.com/chloeli-15/model_spec_midtraining` (R230 project)
- ✅ Backfilled `github.com/ReflexioAI/reflexio` (R230 project)

---

*Round 230 | 2026-06-04 | push complete b445347*