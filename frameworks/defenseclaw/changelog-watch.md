# DefenseClaw Changelog Watch

> 追踪 Cisco DefenseClaw 的版本变更和动态更新。

---

## 📋 追踪记录

### 2026-03-23 — Initial Release（RSAC 2026）

**版本**：Initial Release（GitHub repo 建立）
**来源**：RSAC 2026 / GitHub（cisco-ai-defense/defenseclaw）

**本轮变更**：

- 🚀 **Initial Release**：DefenseClaw 开源仓库正式建立（cisco-ai-defense/defenseclaw，127 stars）
- Skills Scanner：Agent 技能安全扫描工具
- MCP Scanner：MCP Server 完整性验证和监控
- A2A Scanner：Agent 间通信安全和身份验证（5 检测引擎：pattern matching / protocol validation / behavioral analysis / runtime testing / LLM analyzer）
- CodeGuard：动态生成代码的静态分析层
- AI Bill of Materials（AI BoM）：AI 资产持续清单生成

**其他来源记录**：

- Cisco 博客：https://blogs.cisco.com/ai/cisco-announces-defenseclaw
- ZDNet：https://www.zdnet.com/article/cisco-defenseclaw-to-govern-agentic-ai/
- Cisco 新闻：https://newsroom.cisco.com/c/r/newsroom/en/us/a/y2026/m03/cisco-reimagines-security-for-the-agentic-workforce.html
- A2A Scanner 独立博客：https://blogs.cisco.com/ai/securing-ai-agents-with-ciscos-open-source-a2a-scanner
- RSAC 2026 Innovation Sandbox 发布（3/23-27）

**状态**：🟡 跟踪中（GitHub repo 目前仅有 README.md 和 LICENSE，内容较简，暂无正式 Release Tag）

**备注**：

- GitHub repo 非常精简（仅 README + LICENSE），尚无正式 release tag 或完整代码
- 完整工具集（Skills Scanner / MCP Scanner / A2A Scanner / CodeGuard / AI BoM）的具体实现代码有待开源
- A2A Scanner 有独立博客详细介绍其 5 检测引擎架构
- 集成 NVIDIA OpenShell 运行时，提供沙箱执行环境
- 与 Cisco Duo Zero Trust Access 深度集成

---

*由 AgentKeeper 维护 | 每轮更新*
