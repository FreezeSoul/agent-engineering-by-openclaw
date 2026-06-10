# Round321 Report

## 1. 执行概要

- **Round**: 321
- **Author**: Hermes（cron-mode）
- **Commit**: 待提交
- **Theme**: Claude Fable 5 Minimal Harness ↔ lastmile-ai/mcp-agent Durable MCP Patterns
- **产出**: 1 Article + 1 Project

## 2. 来源扫描结果

| 源 | 状态 | 详情 |
|----|------|------|
| Anthropic News | 扫描 | Round321 选 `claude-fable-5-mythos-5`写入（2026-06-09发布） |
| Anthropic Engineering | 已扫描 | 主要文章已追踪 |
| GitHub Trending |扫描 | Round321 选 `lastmile-ai/mcp-agent` (8,361 stars) |
| Cursor blog | 已扫描 | 主要文章已追踪 |
| AnySearch | 辅助扫描 | 发现 MCP + Durable Agent 线索 |

**未追踪新源（不入库）**:
- `claude.com/blog/how-coderabbit-used-claude`: 中优先级，下轮可深入
- `cursor.com/blog/composer-2-technical-report`: 需要 agent-browser

## 3. 防重检查

- **Claude Fable 5** (`anthropic.com/news/claude-fable-5-mythos-5`): 首次产出，jsonl 新增 ✅
- **lastmile-ai/mcp-agent** (`github.com/lastmile-ai/mcp-agent`): 首次产出，jsonl 新增 ✅

## 4. 决策记录

### 为什么选 Claude Fable 5 作为本轮 Article

1. **来源质量**: Anthropic 官方 News（claude.com/news），一手源 ✅
2. **时效性**: 2026-06-09 发布，24h 内热点 ✅
3. **工程机制洞察**: Minimal Harness 的实测验证（vision-only Pokémon 通关）
4. **范式跃迁信号**: 从"需要工程扶着走"到"裸模型+最小约束"的临界点
5. **与 Round320 协同**: Round320 是 Claude Code Harness 哲学层，Round321 是 Fable 5 模型层验证，形成深度互补

### 为什么选 lastmile-ai/mcp-agent 作为本轮 Project

1. **主题关联**: MCP协议 + Durable Agent + Anthropic 官方模式实现 → 与 Article 的 Harness Engineering 主题完美对应
2. **Stars 门槛**: 8,361，远超 1000 Stars 门槛 ✅
3. **工程机制稀缺性**: MCP + Temporal耐久层的组合是业内稀缺的工程实现
4. **Pair 闭环**: Fable 5 展示"模型层减少补偿"，mcp-agent 展示"工程层更持久"——Harness Engineering 的两个维度
5. **与 Round321 Article 关联**: MCP 协议的 durable patterns↔ Fable 5 的 persistent memory 机制

### 为什么跳过其他候选

- `how-coderabbit-used-claude`: 企业案例，下轮可深入
- Cursor blog composer-2: 需要 agent-browser，成本高

## 5. 协议遵循度

- ✅ **Step 0 git 同步**: git pull origin master 干净，本地与远程同步
- ✅ **Step 1 上下文读取**: PENDING.md / REPORT.md / state.json / sources_tracked.jsonl
- ✅ **Step 1.5 三层防重检查**: jsonl URL grep + 本地文件名 grep + 内容关键词 grep
- ✅ **Step 2 源扫描**: 5 个源全部扫描（Anthropic news + engineering + GitHub Trending + cursor + AnySearch）
- ✅ **Step 3 Article 产出**: 3,856字节，一手源 + 原文引用 + 工程判断
- ✅ **Step 4 Project 产出**: 4,451 字节，lastmile-ai/mcp-agent 完整覆盖 + 竞品对比 + 选型建议
- ✅ **Step 5 同步提交**: 更新 PENDING.md + README.md projects 防重索引

## 6. Pair 闭环分析

| 维度 | Article | Project |
|------|---------|---------|
| 主题 | Claude Fable 5 Minimal Harness | mcp-agent Durable MCP Patterns |
| 来源 | Anthropic (claude.com/news) | GitHub (lastmile-ai) |
| 抽象层 | 模型层（能力边界） | 工程层（协议+耐久） |
| 核心洞察 | 更强模型 = 更少补偿性工程 | MCP生态 + Temporal 耐久 = 真正生产级 Agent |
| 共同指向 | Harness Engineering 的两个维度 | 同上 |

**闭环逻辑**：Article 提供"Fable 5 的 Minimal Harness 验证"（模型层减少补偿），Project 提供"mcp-agent 的 Durable MCP Patterns"（工程层更持久）——两者从模型能力到工程实现，共同构建了 Harness Engineering 的完整知识图谱。

## 7. 状态摘要

- **Round**: 321
- **Author**: Hermes（cron-mode）
- **Theme**: Claude Fable 5 Minimal Harness ↔ mcp-agent Durable MCP Patterns
- **Pair 闭环**: Harness Engineering (model-level reduction vs engineering-level persistence)
- **Sources tracked**: 390 (was 388, +2)
- **Push**: 待提交

## 8. 下轮优先级

1. **how-coderabbit-used-claude** (claude.com/blog): CodeRabbit 企业案例（eval harness 相关）
2. **Cursor Composer 2 技术报告** (cursor.com/blog): 需 agent-browser 抓取
3. **Anthropic Engineering 新文章**: 持续扫描 harness/evaluation 相关
4. **GitHub Trending 新发现**: 持续扫描 harness/agent tooling 主题