# PENDING.md - 下一轮规划（第59轮）

## 待完成事项

### 信息源扫描方向
- [ ] **Multi-agent orchestration 安全问题**：当多个 Agent 并行工作时，安全边界如何设计
- [ ] **Shannon "AGPL vs Commercial"**：Lite vs Pro 功能边界与选型建议
- [ ] **AI Coding 安全主题延伸**：OWASP Agentic Top 10 相关项目
- [ ] **Cursor cloud-agent development environments**：云端开发环境，可能是下一个大主题
- [ ] **AI Coding 安全：Skill Registry 安全验证**：Agent Skills 注册表与 Snyk 扫描联动

### 项目方向储备
- [ ] **K-Dense-AI/scientific-agent-skills**：135 个科研 Agent Skills，Trending 发现
- [ ] **NirDiamant/agents-towards-production**：Trending 发现，需评估
- [ ] **muratcankoylan/Agent-Skills-for-Context-Engineering**：15,733 stars，已发现未追踪
- [ ] **microsoft/ai-agents-for-beginners**：微软 AI Agents 入门课程，多语言支持

### 仓库结构优化
- [ ] 评估 articles/evaluation/ 和 articles/projects/ 的边界是否清晰
- [ ] 评估是否需要在 evaluation/ 增加 Harbor 相关内容的更多链接

## 约束提醒
- 每轮必须产出 ≥1 Article（AI 大厂一手资料）
- 每轮必须产出 1 个 GitHub Trending Project
- 防重以项目路径（owner/repo）为准
- 质量优先于数量
- 主题关联性：Article 与 Project 必须形成闭环

## 本轮发现的新线索

### Cursor Harness 持续改进主题
- **本轮发现**：Cursor 官方博客 "Continually improving our agent harness" → 测量驱动工程实践 → Keep Rate + 异常检测 + 自动化问题发现
- **核心判断**：Cursor 的 harness 改进方法论代表了 AI Coding Agent 工程化的一个重要方向——从「直觉驱动」到「测量驱动」。通过 Keep Rate（代码留存率）和「未知错误 = Bug」的原则，把 agent 质量控制变成了可量化的工程问题。
- **Article → Project 关联性**：Skill Registry（Tech Leads Club Agent Skills）→ 输入安全验证；Harness Monitoring（Cursor）→ 输出质量控制。两者形成「输入-输出」安全闭环。

### 下轮可研究的具体方向
1. **AI Coding Agent 安全的系统性框架**：输入安全（Skill Registry）+ 输出质量（Harness Monitoring）+ 运行时隔离（Sandbox）
2. **Multi-agent 场景下的 Harness 角色变化**：Cursor 提出的「harness 作为编排核心」观点
3. **OpenAI Codex Windows Sandbox**：与 Cursor Cloud Agent Development Environments 的企业安全对比

## 源追踪状态
- cursor.com/blog/continually-improving-agent-harness ✅ 本轮已追踪
- github.com/tech-leads-club/agent-skills ✅ 本轮已追踪