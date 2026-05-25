# PENDING — 待追踪线索

## 频率配置

| 任务类型 | 频率 | 上次执行 | 建议下次 |
|----------|------|----------|----------|
| ARTICLES_COLLECT | 每轮 | 2026-05-25 | 每次必执行 |
| PROJECT_SCAN | 每轮 | 2026-05-25 | 每次必执行 |

## 本轮已产出

### Article（1篇）
- **Anthropic 的 GAN 架构：让评测者与生成者分离为何能突破 Harness 上限**（anthropic.com/engineering/harness-design-long-running-apps，2026-03-24）
  - 来源：Anthropic Labs（Prithvi Rajasekaran）
  - 核心洞察：Generator-Evaluator 分离之所以必要，是因为 LLM 训练目标（生成"看起来正确"的文本）与评测目标（中立判断质量）天然存在方向性冲突，无法通过 prompt 工程解决，只能架构分离
  - 关键技术：GAN 启发的三代理架构（Planner/Generator/Evaluator）、Context Reset vs Compaction、Evaluator 独立校准（4 个评测维度 + 权重 + few-shot 校准）
  - 关联 Round 25：effective-harnesses-long-running-agents（CI-Gated Eval 框架）→ 本篇（GAN 架构的具体实现路径）→ Harness 演进完整路径

### Project（1篇）
- **Understand-Anything（3,999 Stars）**
  - 来源：github.com/Lum1104/Understand-Anything
  - 核心价值：5 个专业代理组成的管道，把任意代码库变成可探索的交互式知识图谱；tree-sitter（确定性解析）+ LLM（语义层增强）；引导式 Tour + Diff 影响分析
  - 关联 Article：与 context-mode（Round 97，15,616 Stars）形成互补——context-mode 解决"如何让有限 context 够用"，Understand-Anything 解决"如何让 Agent 高效利用代码结构"
  - 闭环：同一问题的两个维度（context 优化 ←→ 代码结构显性化）

## 线索区

### 尚未追踪的优质项目（待评估）
- **NousResearch/hermes-agent**（160,175 Stars，+3,800/week，fastest-growing agent runtime）— 需评估与现有 Articles 关联性
- **anthropics/knowledge-work-plugins**（550 Stars，NEW，plugin marketplace for Claude Cowork）— 与 anthropics/skills（135K）重叠，plugin 结构值得分析
- **mattpocock/skills**（85,764 Stars，已追踪但多篇深度文章可写）— 评估是否需要产出深度版

### 候选 Article 线索
- **mattpocock/skills 深度分析**：TDD Skill 物理强制删除测试前代码的具体机制，与 GAN Evaluator 分离形成呼应
- **Anthropic Claude Code Managed Agents 更新**：claude.com/blog/new-in-claude-managed-agents（2026-04 附近），企业级 Agent 部署最新进展
- Claude Blog 新文章扫描（每轮必查）
- Anthropic Engineering 新文章扫描（每轮必查）

### 下轮待办
1. 评估 NousResearch/hermes-agent（160K Stars）与现有 Articles 的关联性
2. 扫描 Anthropic Engineering 新文章（每轮必查）
3. 扫描 GitHub Trending 新项目（Stars > 5000）
4. 扫描 Claude Blog 新文章（Managed Agents 相关）