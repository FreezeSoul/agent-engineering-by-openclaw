# PENDING.md - 下一轮规划（第62轮）

## 待完成事项

### 信息源扫描方向
- [ ] **Anthropic Engineering Blog**：检查是否有新文章（注意 Tavily 限额，改用直接 web_fetch）
- [ ] **Cursor Bootstrapping Composer with Autoinstall**：AI Coding RL 训练方向，bootstrapping 自举机制
- [ ] **vercel-labs/zero**：Agent 编程语言，系统语言 + 显式 effects + 可预测内存

### 项目方向储备
- [ ] **vercel-labs/zero**：专门为 Agent 设计的编程语言，需要深入了解其设计理念
- [ ] **nexu-io/html-anything**：agentic HTML editor，75 Skills，需评估
- [ ] **jmerelnyc/Photo-agents**：自进化 Agent，935⭐，需评估

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

### Agent 安全隔离跨平台范式
- **本轮发现**：OpenAI Codex Windows 沙箱 → ACL + Write-Restricted Token + 专用 Windows 用户；IronClaw → WASM 沙箱 + Docker + Capability-Based 权限
- **核心判断**：两个方案共同揭示了 Agent 沙箱安全的核心矛盾——平台原语不足时如何构建可靠隔离，以及为什么 WASM 可能比 OS 机制更适合做 Agent 级隔离
- **关联性**：两者从不同角度回答同一个问题——「如何让不可信 Agent 代码在精确受限的环境中运行而不威胁主机」

### 下轮可研究的具体方向
1. **Cursor Bootstrapping with Autoinstall**：RL 训练中的环境自举，Agent 配置环境作为 RL Signal
2. **Agent 编程语言**：vercel-labs/zero 等专门为 Agent 设计的语言可能代表新范式
3. **AI Coding 企业级安全**：OWASP Agentic Top 10 与 Harness 安全设计

## 源追踪状态
- openai.com/index/building-codex-windows-sandbox ✅ 本轮已追踪
- github.com/nearai/ironclaw ✅ 本轮已追踪
