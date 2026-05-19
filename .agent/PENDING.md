# PENDING.md - 下一轮规划（第71轮）

## 待完成事项

### 信息源扫描方向
- [ ] **Anthropic Engineering Blog**：关注「Scaling Managed Agents」文章（解耦 brain/hands 架构深度解析）
- [ ] **Cursor Blog**：追踪 Composer 2.5 的长程 RL 细节、Cloud Agent Development Environments 的工程实现
- [ ] **OpenAI Blog**：Parameter Golf 后续分析，以及 Codex Windows Sandbox 的工程细节补充

### 项目方向储备
- [ ] **AI Coding Agent 评测方向**：SWE-bench、ClawProBench 等 benchmark 框架深入研究
- [ ] **多 Agent 编排方向**：A2A 协议、multi-agent orchestration 相关开源项目
- [ ] **Agent Security**：Agent-Threat-Rules 等安全检测工具的深度分析

## 约束提醒
- 每轮必须产出 ≥1 Article（AI 大厂一手资料）
- 每轮必须产出 1 个 GitHub Trending Project
- 防重以项目路径（owner/repo）为准
- 质量优先于数量
- 主题关联性：Article 与 Project 必须形成闭环

## 本轮发现的新线索

### Windows Agent 沙箱的双轨范式
- **本轮发现**：OpenAI Codex Windows Sandbox（Elevated/Unelevated 双模式 + 四层进程架构）与 Aembit Agentic AI Security Starter Kit（输入层检测）形成纵深防御的两个维度
- **核心判断**：两者不是竞争关系，而是互补——沙箱解决「执行层的边界」，Starter Kit 解决「输入层的安全」

### 下轮可研究的具体方向
1. **Anthropic「Scaling Managed Agents」深度延伸**：brain/hands 解耦的工程实现细节
2. **Cursor Cloud Agent Development Environments**：multi-repo 环境的 Dockerfile 配置与治理
3. **GitHub Trending 中的安全工具**：MCP Firewall、OPA-based Agent Policy 等新兴方向

## 源追踪状态
- https://openai.com/index/building-codex-windows-sandbox/ ✅ 本轮已追踪
- https://github.com/aembit/agentic-ai-security-starter-kit ✅ 本轮已追踪