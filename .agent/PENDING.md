# PENDING.md - 待处理事项

> 上次更新: R454 (2026-06-20)

---

## 持续性待办

### 🔴 高优先级

#### gen_article_map.py 挂起问题
- **问题**: 自 R392 起，脚本持续挂起（当前 62 次连续挂起）
- **症状**: gen_article_map.py 运行后不退出，不生成输出
- **影响**: 无法执行 "30-commit scan" 和 "New repositories since R_" 扫描
- **计划修复**:
  1. 调查挂起原因（可能与 git log 输出格式/管道处理有关）
  2. 考虑用 Python 直接调用 git 而非管道
  3. 或使用 headless-browser 方式替代
- **状态**: 未处理

#### 源饱和应对策略
- **问题**: 所有一级源（Anthropic/OpenAI/Cursor/CrewAI/Replit/Augment）已饱和
- **影响**: 连续 R453、R454 均为 SKIP
- **计划**:
  1. 用 browser 工具扫描 Cursor/Replit/Augment 博客（JS 渲染）
  2. 评估是否需要扩展一级源列表
  3. 考虑工具类项目的纳入标准
- **状态**: 未处理

---

## 本轮评估后的决策

### ✅ 可关闭

- **heygen-com/hyperframes 评估**: 28.5K stars，但视频渲染工具，非 Agent Engineering 核心方向 → **关闭，不纳入**

### ❌ 本轮关闭但需重新审视

- **Addy Osmani "Long-running Agents"**: 不在 SKILL 一级源列表 → **关闭，但 SKILL 规则可能需要审视**（Addy Osmani 是 Google 前工程师，独立工程视角，内容深度超过大多数企业博客）
- **CrewAI "How to build Agents Where Data Already Lives"**: 评估为浅（企业定位）→ **关闭，但可重新评估**

---

## 探索性想法

### 源扩展可能性
当前一级源列表：
- Anthropic ✅
- OpenAI ✅
- Cursor ✅ (需 browser)
- CrewAI ✅
- Replit ✅ (需 browser)
- Augment ✅ (需 browser)
- GitHub (trending) ✅

可能扩展方向：
- Microsoft (Azure AI, Semantic Kernel)
- Google (Agent Development Kit, Gemini for Developers)
- Meta (Llama 相关生态)
- Hugging Face (SmolAgents)
- LangChain (langgraph)
- Multi-agent 相关框架（AutoGen, Mastra, PydanticAI）

**注意**: 扩展需符合 SKILL 的工程视角和质量门槛

### hyperframes 重新考虑
- 28.5K stars，Apache 2.0，活跃维护（每周更新）
- Claude Code skill 集成
- Deterministic rendering pipeline
- **反对纳入**: 非 Agent Engineering 核心问题
- **支持纳入**: 28.5K stars 说明被广泛使用，且 Claude Code skill 是真实的 Agent 集成案例
- **建议**: 等待 FSIO 决策

---

## 下次触发时检查清单

- [ ] 检查 R454 REPORT.md
- [ ] 检查一级源是否有新文章
- [ ] 尝试用 browser 工具扫描 Cursor 博客
- [ ] gen_article_map.py 问题状态
- [ ] hyperframes 决策状态
