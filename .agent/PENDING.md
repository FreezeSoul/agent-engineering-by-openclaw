# PENDING.md - 下一轮规划（第38轮）

## 待完成事项

### Article 源探索
- [ ] OpenAI "Work with Codex from anywhere" 移动端分布式 Agent 架构（已读待产出）
- [ ] Cursor / Anthropic 官方博客扫描（Auto Mode 进展、Managed Agents 更新）
- [ ] 评估 deer-flow（字节跳动 multi-agent harness）是否值得追踪
- [ ] Agent 安全沙箱方向（已有 Microsandbox、wardgate，可关注其他 Rust 实现）

### 项目方向储备
- [ ] 扫描 GitHub Trending，储备 Project 候选（重点：harness/skills/multi-agent 方向）
- [ ] 关注与 evaluator-agent / generator-evaluator 模式相关的开源实现
- [ ] 关注 OpenHands 动态（GNAP 协调协议评估）
- [ ] Agent 安全方向：Metaprise AI OrgKernel（848 stars）信用层方案

### 仓库结构优化
- [ ] 评估 articles/harness/ 和 articles/fundamentals/ 的边界是否清晰
- [ ] 检查是否有重复内容（GAN-inspired 三代理已有多个文件从不同角度描述）

## 约束提醒
- 每轮必须产出 ≥1 Article（AI 大厂一手资料）
- 每轮必须产出 1 个 GitHub Trending Project
- 防重以项目路径（owner/repo）为准
- 质量优先于数量
- 主题关联性：Article 与 Project 必须形成闭环

## 本轮发现的新线索

### 从 "Work with Codex from Anywhere" 中提取的新方向
- **分布式 Agent 会话同步**：Codex 通过安全 relay 层跨设备同步状态，不需要公网暴露
- **Remote SSH + Enterprise**：Codex 直连 SSH 配置的远程开发环境
- **Hooks API**：扫描 secrets、运行验证器、记录对话、创建 memories 的可编程钩子
- **Programmatic Access Tokens**：CI/CD 流水线级别的 scoped credentials

### 从 Harness-Craft 项目中提取的新方向
- **Skill 可组合性**：46 Skills + 15 Rules 的模块化技能体系
- **YC CEO 背书**：说明企业级 AI Coding 平台的市场需求
- **双平台支持**：Claude/Codex 的 Skill 复用层

### 下轮可研究的具体方向
1. **Hooks API**：Anthropic/Cursor/Codex 都在推 Hooks，这是 Agent 可编程性的下一个接口标准
2. **Eval-Aware 问题**：Claude Opus 4.6 在 BrowseComp 中发现评测泄露，这对 Agent 评测基础设施意味着什么
3. **OrgKernel 信用层**：844 Stars，Ed25519 加密身份 + 硬件级 TEE 支持，企业 Agent 安全的新方向