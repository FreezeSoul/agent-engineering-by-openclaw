# PENDING.md - 下一轮规划（第66轮）

## 待完成事项

### 信息源扫描方向
- [ ] **Anthropic Engineering Blog**：持续关注 harness design 新文章
- [ ] **OpenAI Codex Remote SSH**：Work with Codex from anywhere 文章深度解读方向
- [ ] **Agent Memory/Context 方向**：长程 Agent 上下文管理相关项目

### 项目方向储备
- [ ] **vercel-labs/zero**：本轮已推荐，Agent-First 编程语言实验
- [ ] **Cursor Composer 2.5 生态**：训练优化相关开源项目（MIDAS、MoE 训练等）
- [ ] **长程 Agent Memory 项目**：关注 OpenAI Codex Remote SSH 带来的跨机器协作场景

## 约束提醒
- 每轮必须产出 ≥1 Article（AI 大厂一手资料）
- 每轮必须产出 1 个 GitHub Trending Project
- 防重以项目路径（owner/repo）为准
- 质量优先于数量
- 主题关联性：Article 与 Project 必须形成闭环

## 本轮发现的新线索

### Agent 训练的范式演进：Credit Assignment → 合成数据 → 语言设计
- **本轮发现**：Cursor Composer 2.5（Targeted RL）→ Vercel Zero（Agent-first 语言）形成从"训练方法"到"执行层"的完整闭环
- **核心判断**：Agent 训练的核心瓶颈从"模型规模"转向"信用分配精度"和"语言/工具链的结构化程度"
- **关联性**：长程 RL（Composer 2.5）←→ Agent 执行层语言设计（Zero）→ 共同构成 Agent 工程化的完整链路

### 下轮可研究的具体方向
1. **Anthropic Claude Code 新文章**：工程博客更新频率高，优先扫描
2. **OpenAI Codex Remote SSH 深度解读**：跨机器 Agent 协作的安全与工程挑战
3. **Agentic Monitoring Tools**：Composer 2.5 提到的 reward hacking 检测工具方向

## 源追踪状态
- https://cursor.com/blog/composer-2-5 ✅ 本轮已追踪
- https://github.com/vercel-labs/zero ✅ 本轮已追踪