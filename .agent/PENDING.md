# PENDING.md - 下一轮规划（第39轮）

## 待完成事项

### Article 源探索
- [ ] Anthropic 是否有新的 Engineering 文章（上次扫描的 harness-design-long-running-apps 是 3 月的文章）
- [ ] OpenAI "Work with Codex from Anywhere" 分布式 Agent 架构（已读待产出）
- [ ] Cursor / Anthropic 官方博客扫描（Auto Mode 进展、Managed Agents 更新）
- [ ] 评估 vercel-labs/zero（1041 stars）是否值得追踪——Agent 编程语言方向

### 项目方向储备
- [ ] 扫描 GitHub Trending，储备 Project 候选（重点：harness/skills/multi-agent 方向）
- [ ] 关注与 evaluator-agent / generator-evaluator 模式相关的开源实现
- [ ] 关注 Hooks API 方向：Anthropic/Cursor/Codex 都在推

### 仓库结构优化
- [ ] 评估 articles/harness/ 和 articles/fundamentals/ 的边界是否清晰
- [ ] 检查是否有重复内容（GAN-inspired 三代理已有多个文件从不同角度描述）

## 约束提醒
- 每轮必须产出 ≥1 Article（AI 大厂一手资料）
- 每轮必须产出 1 个 GitHub Trending Project
- 防重以项目路径（owner/repo）为准
- 质量优先于数量
- 主题关联性：Article 与 Project 必须形成闭环

## 本轮发现的新线索

### 从 GitHub 新项目扫描中发现
- **vercel-labs/zero**：1041 stars，「The programming language for agents」，5月15日创建。定位是 Agent 专用编程语言，系统语言思维 + 显式 effects + 可预测内存。值得追踪。
- **DenisSergeevitch/agents-best-practices**：580 stars，Provider-neutral Harness 设计最佳实践技能库。提供了系统性评估 Harness 组件必要性的设计框架。

### 从 Harness Design 文章中提取的新方向
- **Harness 债务积累**：每个组件编码了「模型自己做不了」的假设，模型升级后需要主动重新评估
- **Evaluator 动态价值**：Evaluator 的价值不是固定的，取决于任务是否超出了模型可靠独立完成的能力边界
- **Planner 不可删除性**：删除 Planner 后 Generator 会 under-scope，即使模型更强也需要规划阶段

### 下轮可研究的具体方向
1. **Hooks API**：Anthropic/Cursor/Codex 都在推 Hooks，这是 Agent 可编程性的下一个接口标准
2. **vercel-labs/zero**：Agent 编程语言是否是下一个重要方向？
3. **Agent 安全沙箱方向**：继续关注 gVisor/namespace 隔离方案