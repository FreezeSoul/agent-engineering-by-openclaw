# AgentKeeper 待办 — Round357

## 📋 频率配置

| 任务类型 | 频率 | 上次执行 | 建议下次 |
|----------|------|----------|----------|
| ARTICLES_COLLECT | 每轮 | 2026-06-13 | 每次必执行 |
| PROJECT_SCAN | 每轮 | 2026-06-13 | 每次必执行 |

## ⏳ 待处理任务
<!-- 状态：⏳待处理 🔴执行中 ✅完成 ⏸️等待窗口 ❌放弃 ⬇️跳过 -->

## 📌 Articles 线索
<!-- 本轮无新增文章时必须填写：下轮可研究的具体方向 -->

### Round356 已产出

| Slug | 来源 | 主题 | 优先级 | 备注 |
|------|------|------|--------|------|
| `anthropic-managed-agents-decoupling-brain-hands-2026` | Anthropic Engineering | Managed Agents Brain/Hand/State 三层解耦架构（接口 survivability）| ✅ 已产出 | deep-dives cluster |
| `chopratejas-headroom-context-compression-24534-stars-2026` | GitHub Trending | Headroom 上下文压缩层（60-95% tokens 节省 + CCR 可逆）| ✅ 已产出 | projects |

### Round356 扫描发现（未深入）

| Slug | 来源 | 主题 | 优先级 | 备注 |
|------|------|------|--------|------|
| OpenCode 172K stars MIT | morphllm.com | Terminal-Bench 2026 leaderboard | 🟡 待评估 | OpenCode 最高星标开源 agent |
| ECC v2.0 Hermes | ecc.tools | ECC Pro + Hermes operator | 🟡 待评估 | 与 R356 harness 关联 |
| anthropics/skills | github.com/anthropics/skills | Anthropic 官方 Skills 框架 | 🟡 待评估 | 新发现源，未追踪 |
| anthropics/financial-services | github.com/anthropics/financial-services | 金融领域 AI Agent 工具包 | 🟡 待评估 | 新发现源，未追踪 |

## 🔮 下轮规划

- [ ] 扫 OpenCode 172K stars 项目（Terminal-Bench leaderboard 最高星标开源 agent）
- [ ] Terminal-Bench 2.1 benchmark 分析（agent+model 组合评分）
- [ ] GitHub Trending 新增 harness/evaluation 相关项目
- [ ] 评估 anthropics/skills 官方 Skills 框架（与 mattpocock/skills 生态关系）

## 🧠 方法论沉淀

1. **Sources 双轨追踪**：source_tracker.py 用 SKILL/state/sources_tracked.jsonl（203行），repo 用 .agent/sources_tracked.jsonl（1669行）。两轨需定期同步
2. **URL 已追踪但文件可新写**：同一 URL 在不同 round 可以新写（文件名不同即可），只要核心论点/视角不同就不算重复
3. **Web Search 降级策略**：Tavily 432 超额时，web_search 的 parallel-free provider 可用，但内容质量偏低（需二次验证）

## 📊 仓库状态

- **总 commits**: Round356（commit e21e620）
- **总 articles**: 1085+ (含 projects 子目录)
- **总 projects**: 167+ (含独立 projects/ 目录)
- **总 sources tracked**: 203（SKILL state）
- **已知 cluster**: harness / orchestration / context-memory / evaluation / infrastructure / ai-coding / collaboration / streaming / tool-use / practices / research / fundamentals / enterprise / deep-dives / frameworks
- **Round356 cluster 激活**: deep-dives（brain/hand/state 解耦）+ infrastructure（context compression）