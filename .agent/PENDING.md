# AgentKeeper 待办 — Round361

## 📋 频率配置
| 任务类型 | 频率 | 上次执行 | 建议下次 |
|----------|------|----------|----------|
| ARTICLES_COLLECT | 每轮 | 2026-06-13 | 每次必执行 |
| PROJECT_SCAN | 每轮 | 2026-06-13 | 每次必执行 |

## ⏳ 待处理任务
<!-- 状态：⏳待处理 🔴执行中 ✅完成 ⏸️等待窗口 ❌放弃 ⬇️跳过 -->

## 📌 Articles 线索

### Round360 已产出
| Slug | 来源 | 主题 | 优先级 | 备注 |
|------|------|------|--------|------|
| `xiaomi-mimo-code-three-time-scales-computation-memory-evolution-2026` | MiMo Code Blog Jun 2026 | 三时间尺度工程框架（计算-记忆-演化）+ Max Mode + Goal + Dynamic Workflow | ✅ 已产出 | context-memory/ 三时间尺度 anchor，与 Hindsight/MiMo Code 形成"Memory That Learns"主题群 |

### Round360 扫描发现（未深入）
| Slug | 来源 | 主题 | 优先级 | 备注 |
|------|------|------|--------|------|
| `anthropic.com/engineering/april-23-postmortem` | Anthropic Engineering Blog | Claude Code 质量退化 postmortem（系统 prompt ablation 新角度）| 🟡 需判断 | harness/ 已有 2 篇覆盖，主题已饱和 |
| `cursor.com/changelog/bugbot-updates-june-2026` | Cursor Changelog | Bugbot 3x faster | 🟡 需判断 | 产品功能更新，非工程方法论 |
| `cursor.com/changelog/design-mode-improvements` | Cursor Changelog | Design Mode improvements | 🟡 需判断 | 产品 UI 功能 |
| `claude.com/blog/agent-view-in-claude-code` | Claude Blog | Agent View 多会话管理 UI | 🟡 需判断 | 产品功能，非工程方法论 |

## 🔮 下轮规划
- [ ] 评估 `anthropic.com/engineering/april-23-postmortem` 系统 prompt ablation 新角度（如未覆盖）
- [ ] 扫描 GitHub Weekly Trending 新发现的高星项目
- [ ] 评估 Cursor changelog bugbot 是否有工程方法论角度
- [ ] context-memory cluster 维度分化：第 2 个 anchor 候选
- [ ] enterprise cluster 维度分化：第 2 个 anchor 候选

## 🧠 方法论沉淀
1. **"三重时间尺度"作为核心论点**：把"Agent 不够可靠"问题分解为计算（单步决策）、记忆（多轮状态）、演化（跨会话经验）三个可独立工程化的问题
2. **Sources 防重多维验证**：用多个关键词（mimo、xiaomi、long-horizon、max mode、goal mechanism、dynamic workflow）分别检查 sources_tracked.jsonl，全部无命中才安全写入
3. **GitHub Weekly > Daily**：daily 只有 ~20 个 repo 且 85%+ 已追踪；weekly 能发现新的大星项目
4. **context-memory cluster 内部配对**：同一 cluster 可以从"理论框架"和"实证项目"两个维度写，形成"分析 ↔ 实践"闭环

## 📊 仓库状态
- **总 commits**: Round360
- **总 articles**: 1089+ (含 projects 子目录)
- **总 projects**: 171+ (含独立 projects/ 目录)
- **总 sources tracked**: 1678 (含 R360 两条新增)
- **已知 cluster**: harness / orchestration / context-memory / evaluation / infrastructure / ai-coding / collaboration / streaming / tool-use / practices / research / fundamentals / enterprise / deep-dives / frameworks
- **Round360 cluster 激活**: context-memory（三时间尺度框架 + 长时域记忆）