# PENDING.md - 下一轮规划（第37轮）

## 待完成事项

### Article 源探索
- [ ] Anthropic engineering 页面新文章扫描（Harness design for long-running apps 已读完，待产出）
- [ ] OpenAI blog 最新工程文章（Codex Windows sandbox 已产出，注意防重）
- [ ] Cursor changelog 新功能深度分析
- [ ] 评估 deer-flow（字节跳动 multi-agent harness）是否值得追踪

### 项目方向储备
- [ ] 继续扫描 GitHub Trending，储备 Project 候选
- [ ] 关注与 evaluator-agent / generator-evaluator 模式相关的开源实现
- [ ] 关注 OpenHands 动态（GNAP 协调协议评估）
- [ ] Agent 安全沙箱方向（已有 Microsandbox，可关注其他 Rust 实现）

### 仓库结构优化
- [ ] 评估是否需要在 articles/ 下增加新的分类维度（如 "infrastructure" 或 "environments"）
- [ ] 整理现有 article 的 URL 去重检查

## 约束提醒
- 每轮必须产出 ≥1 Article（AI 大厂一手资料）
- 每轮必须产出 1 个 GitHub Trending Project
- 防重以项目路径（owner/repo）为准
- 质量优先于数量
- 主题关联性：Article 与 Project 必须形成闭环

## 本轮发现的新线索

### 从 Anthropic Harness Design 文章中提取的新方向
- **Evaluator Agent 模式**：分离 generator 和 evaluator，解决 self-evaluation 偏差问题
- **Context Reset vs Compaction**：reset 提供 clean slate，compaction 保留连续性，各有取舍
- **Planner-Generator-Evaluator 三角色架构**：完整的长任务 harness 设计模式
- **GAN-inspired 架构**：将设计评估的 grader criteria 应用到代码 QA

### 从 Codex Windows Sandbox 文章中提取的新方向
- **Write-restricted token + synthetic SID**：Windows 下的精细化权限控制
- **Elevated vs Unelevated 沙箱**：安全与易用性的权衡取舍
- **MIC 完整性级别标签的陷阱**：改变 trust model 的风险
- **Platform constraints 反向驱动架构**：没有标准方案时的工程突围