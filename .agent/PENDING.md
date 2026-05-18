# PENDING.md - 下一轮规划（第63轮）

## 待完成事项

### 信息源扫描方向
- [ ] **Anthropic Engineering Blog**：直接 web_fetch（绕开 Tavily 限额），最新文章如 5月份更新
- [ ] **Cursor Composer 2 + Terminal-Bench 2.0**：Harbor Framework 关联项目
- [ ] **Agent 安全方向**：IronClaw vs Greywall vs microsandbox 多方案对比

### 项目方向储备
- [ ] **harbor-framework/harbor**：Terminal-Bench 2.0 官方 Harness，1985 Stars，需评估
- [ ] **nearai/ironclaw**：WASM 沙箱方案，12,283 Stars，与 OpenAI Codex 沙箱形成 Windows/跨平台对比
- [ ] **CloakHQ/CloakBrowser**：反检测浏览器，14,661 Stars，Browser Agent 场景

### 仓库结构优化
- [ ] 评估 articles/ai-coding/ 目录是否需要独立 README 索引
- [ ] 评估 articles/projects/ 的防重索引是否完整

## 约束提醒
- 每轮必须产出 ≥1 Article（AI 大厂一手资料）
- 每轮必须产出 1 个 GitHub Trending Project
- 防重以项目路径（owner/repo）为准
- 质量优先于数量
- 主题关联性：Article 与 Project 必须形成闭环

## 本轮发现的新线索

### Agent 环境自举与工程原则的互补
- **本轮发现**：Cursor Autoinstall 揭示了"用旧模型配置新模型训练环境"的自举飞轮；12-factor-agents 提出了构建生产级 LLM 软件的 12 条设计原则
- **核心判断**：两者共同回答了"如何构建真正达到生产质量的 Agent 软件"这个问题——Autoinstall 解决环境自动化，12-factor-agents 解决架构设计原则
- **关联性**：两者形成"环境自举 → 工程原则"的完整 Agent 质量保障双维度闭环

### 下轮可研究的具体方向
1. **Agent 安全沙箱多方案对比**：OpenAI Codex Windows ACL/Token → IronClaw WASM → Greywall container-free → microsandbox microvm
2. **Cursor Terminal-Bench 2.0**：Harbor Framework 作为官方 harness 的实现分析
3. **Agent Skills 生态**：mattpocock/skills（85,764⭐）的大规模采用背后的工程原因

## 源追踪状态
- cursor.com/blog/bootstrapping-composer-with-autoinstall ✅ 本轮已追踪
- github.com/humanlayer/12-factor-agents ✅ 本轮已追踪