# PENDING.md - 下一轮规划（第45轮）

## 待完成事项

### Article 源探索
- [ ] Cursor "continually-improving agent harness"（2026-04-30）：测量驱动质量改进的具体方法论
- [ ] Anthropic "infrastructure-noise"（2026-02-05）：如何量化评测环境噪声对 Agent 性能的影响
- [ ] OpenAI "Building Codex for Windows"（2026-05-13）：沙箱设计细节是否还有更多值得分析的维度
- [ ] Cursor 3.3 Explore subagent 配置更新：从设置控制 Explore subagent 模型选择或禁用

### 项目方向储备
- [ ] 评估 agent-security-bench（mattpartida，0 stars）：prompt injection/tool misuse/exfiltration 安全评测方向
- [ ] 关注 Hooks API 生态：评估其他基于 OpenAI Hooks 的开源实现
- [ ] AgentFlow-CodeProxy（zuobiaohappy）：长程 Agent 工作流框架
- [ ] 评估 HKUDS/CLI-Anything（35,244 Stars）：CLI 包装器自动生成，18+ 应用支持

### 仓库结构优化
- [ ] 评估 articles/harness/ 和 articles/orchestration/ 的边界是否清晰
- [ ] 考虑将「多 Agent 并行开发」主题归类到 orchestration 而非 fundamentals

## 约束提醒
- 每轮必须产出 ≥1 Article（AI 大厂一手资料）
- 每轮必须产出 1 个 GitHub Trending Project
- 防重以项目路径（owner/repo）为准
- 质量优先于数量
- 主题关联性：Article 与 Project 必须形成闭环

## 本轮发现的新线索

### Cursor 3.3 更新（2026-05-07）
- **Build in Parallel**：用 LLM 理解任务依赖，async subagent 并行执行，依赖感知的调度
- **Split PRs**：用 chat context 识别逻辑切片，自动拆分为独立 PR（除非有依赖）
- **PR Review**：端到端代码审查体验，Reviews/Commits/Changes 三标签
- **Explore subagent 控制**：从设置选择模型或禁用

### GitHub Trending 新项目
- **colbymchenry/codegraph**：2,955 Stars，预索引代码知识图谱，92% 工具调用减少（52→3）+ 71% 加速

### 下轮可研究的具体方向
1. **CodeGraph 图遍历技术**：预索引知识图谱在 Agent 上下文管理中的价值
2. **OpenAI Auto-review 机制**：用 sub-agent 审批主 agent 的递归设计
3. **Agent 安全评测**：agent-security-bench（prompt injection/tool misuse/exfiltration）方向
4. **CLI-Anything 七阶段自动生成**：HKUDS 的 CLI 包装器自动生成方法论