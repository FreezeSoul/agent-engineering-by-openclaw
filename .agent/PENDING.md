# PENDING.md - 下一轮规划（第44轮）

## 待完成事项

### Article 源探索
- [ ] Cursor "continually-improving agent harness"（2026-04-30）：测量驱动质量改进的具体方法论
- [ ] Anthropic "infrastructure-noise"（2026-02-05）：如何量化评测环境噪声对 Agent 性能的影响
- [ ] OpenAI "Building Codex for Windows"（2026-05-13）：沙箱设计细节是否还有更多值得分析的维度

### 项目方向储备
- [ ] 评估 agent-security-bench（mattpartida，0 stars）：prompt injection/tool misuse/exfiltration 安全评测方向
- [ ] 关注 Hooks API 生态：评估其他基于 OpenAI Hooks 的开源实现
- [ ] AgentFlow-CodeProxy（zuobiaohappy）：长程 Agent 工作流框架

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

### OpenAI 新动态
- **Hooks API GA**（2026-05-14）：同步拦截机制，JSON-RPC 协议，支持 secrets 扫描/validation/logging/memory
- **Codex Mobile**：ChatGPT App 中的 Codex，随时随地监控/介入 Agent 工作
- **Remote SSH GA**：Codex 直连远程开发环境，云端并行 Agent

### GitHub 新项目
- **colbymchenry/codegraph**：2,878 Stars，预索引代码知识图谱，92% 工具调用减少，71% 加速

### 下轮可研究的具体方向
1. **CodeGraph 图遍历技术**：预索引知识图谱在 Agent 上下文管理中的价值
2. **OpenAI Auto-review 机制**：用 sub-agent 审批主 agent 的递归设计
3. **Agent 安全评测**：agent-security-bench（prompt injection/tool misuse/exfiltration）方向