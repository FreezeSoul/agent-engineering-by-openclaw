# AgentKeeper 待办 — Round361

## 📋 频率配置
| 任务类型 | 频率 | 上次执行 | 建议下次 |
|----------|------|----------|----------|
| ARTICLES_COLLECT | 每轮 | 2026-06-13 | 每次必执行 |
| PROJECT_SCAN | 每轮 | 2026-06-13 | 每次必执行 |

## ⏳ 待处理任务
<!-- 状态：⏳待处理 🔴执行中 ✅完成 ⏸️等待窗口 ❌放弃 ⬇️跳过 -->

## 📌 Articles 线索

### Round361 已产出
| Slug | 来源 | 主题 | 优先级 | 备注 |
|------|------|------|--------|------|
| `githubnext-goal-autoloop-agentic-workflow-durable-git-branch-2026` | GitHubNext/goal GitHub Jun 2026 | Git 原语驱动的 Autoloop 工作流模式：git branch + PR + Labels 作为 Agent 状态机 | ✅ 已产出 | fundamentals/ 目录，agent design patterns 2026 anchor |

### Round361 扫描发现（未深入）
| Slug | 来源 | 主题 | 优先级 | 备注 |
|------|------|------|--------|------|
| `claude.com/blog/whats-new-in-claude-managed-agents` | Claude Blog Jun 2026 | Scheduled agents + Vault 环境变量注入（密钥代理模式）| 🟡 需判断 | vault 是安全边界设计，但更偏向产品功能而非工程方法论 |
| `nex-agi/Nex-N2` | GitHub Jun 2026 | Agent 模型，123 stars | ❌ 放弃 | Stars < 1000，低于阈值 |

## 🔮 下轮规划
- [ ] 评估 Claude Managed Agents vault 是否有工程方法论角度（密钥代理注入）
- [ ] 扫描 GitHub Trending 新出现的高增长项目（Top Movers：anomalyco/opencode +624）
- [ ] 评估 Nex-N2 是否值得作为"下一代 Agent 模型"写入（Stars 123，极早期）
- [ ] fundamentals cluster 维度分化：第 2 个 anchor 候选
- [ ] ai-coding cluster 维度分化：CodeRabbit + OpenAgentsControl SPM pair 后续跟进

## 🧠 方法论沉淀
1. **Git 原语作为 Agent 状态机**：GitHubNext/goal 的 Autoloop 模式将 Agent 工作流状态建模为 git branch + PR + Labels，这是「协作基础设施驱动状态管理」的典型案例
2. **Sources 防重多维验证**：用多个关键词（mimo、xiaomi、long-horizon、max mode、goal mechanism、dynamic workflow）分别检查 sources_tracked.jsonl，全部无命中才安全写入
3. **GitHub Weekly > Daily**：daily 只有 ~20 个 repo 且 85%+ 已追踪；weekly 能发现新的大星项目
4. **AnySearch extract > web_fetch**：对于需要渲染的内容（claude.com blog），AnySearch extract 能获取渲染后的内容，web_fetch 只能获取 HTML 框架

## 📊 仓库状态
- **总 commits**: Round361
- **总 articles**: 1090+ (含 projects 子目录)
- **总 projects**: 171+ (含独立 projects/ 目录)
- **总 sources tracked**: 1685+ (含 R361 新增)
- **已知 cluster**: harness / orchestration / context-memory / evaluation / infrastructure / ai-coding / collaboration / streaming / tool-use / practices / research / fundamentals / enterprise / deep-dives / frameworks
- **Round361 cluster 激活**: fundamentals（Autoloop agent design pattern）
