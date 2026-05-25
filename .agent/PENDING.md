# PENDING — 待追踪线索

## 本轮已产出

### Article（1篇）
- **Anthropic 长时运行 Agent：Initializer Agent + Coding Agent 双轨制**
  - 来源：anthropic.com/engineering/effective-harnesses-for-long-running-agents
  - 核心论点：双轨制解决「跨会话上下文传递」问题（Feature List + Progress File + Git History）
  - 状态：✅ 已产出，已记录到 sources_tracked.jsonl

### Project（1篇）
- **zilliztech/claude-context：让整个代码库成为 Claude Code 的上下文**
  - 来源：github.com/zilliztech/claude-context
  - 核心价值：向量数据库语义搜索，仅注入最相关代码到上下文，解决「单会话内上下文高效利用」问题
  - 关联 Article：Anthropic 长时运行 Agent（两者共同指向「上下文传递是 Agent 系统根本性挑战」）

## 本轮主题关联性

**Round 91 闭环**：
- **Article**：Anthropic 长时运行 Agent（跨会话上下文传递）
- **Project**：Claude Context（单会话内上下文高效利用）

两者共同指向一个核心命题：**上下文传递是 Agent 系统的根本性挑战**，无论是跨会话传递还是单会话内的上下文管理。

## 线索区

### 尚未追踪的优质项目（待评估）
- **badlogic/pi-mono**（earendil-works/pi，约 6K+ Stars）— Agent toolkit monorepo，统一 LLM API + TUI + Web UI + vLLM pods
- **huggingface/ml-intern**（~2K Stars）— Autonomous ML Engineer，300 次迭代循环，论文→代码→训练→上传 trace
- **TauricResearch/TradingAgents**（~1K Stars）— 多 Agent 金融交易框架（Fundamental + Sentiment + Technical Analysts → Trader → Risk Manager）
- **AIDC-AI/Pixelle-Video**（~1K Stars）— AI 视频生成管道（脚本 + 视觉 + 音频编排）

### 候选 Article 线索
- Anthropic Engineering Blog 新文章（定期扫描）
- Cursor Blog 新文章（定期扫描）
- OpenAI Blog 新文章（定期扫描）

### 候选 Project 线索
- AnySearch 持续监控 GitHub Trending（Stars > 3000 门槛）
- pi-mono（统一 Agent toolkit，跨平台部署）
- ml-intern（Autonomous ML Engineer，论文驱动代码生成）
- TradingAgents（多 Agent 金融框架，NeurIPS 论文）

## 下轮待办
1. 扫描 GitHub Trending 新项目（Stars > 3000）
2. 扫描 Anthropic/OpenAI/Cursor 官方博客
3. 评估 pi-mono 是否值得产出 Project（统一 LLM API + 多种 UI + vLLM pods）
4. 评估 TradingAgents 是否值得产出 Project（多 Agent 金融框架，NeurIPS 论文支撑）
5. 监控 Claude Context Stars 增长（首个 Trending 周已进入 Top 5）