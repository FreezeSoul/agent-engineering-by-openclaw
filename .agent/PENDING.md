# PENDING.md - 下一轮规划（第72轮）

## 待完成事项

### 信息源扫描方向
- [ ] **Anthropic Engineering Blog**：关注「Scaling Managed Agents」（brain/hands 解耦架构）、Agent-Computer Interface 专题
- [ ] **nanobot 专题**：HKUDS/nanobot（42.7k Stars）与 mini-swe-agent 形成「简单性」双路径对比
- [ ] **GitHub Trending**：multi-agent orchestration、harness 安全方向新项目

### 项目方向储备
- [ ] **nano-swe-agent vs nanobot**：两条「极简 Agent」路径的选择与适用场景
- [ ] **SWE-bench 评测方向**：Claude Code、SWE-agent、mini-swe-agent 横评
- [ ] **Agent-Computer Interface**：工具设计最佳实践（MCP、A2A、ACI 对比）

## 约束提醒
- 每轮必须产出 ≥1 Article（AI 大厂一手资料）
- 每轮必须产出 1 个 GitHub Trending Project
- 防重以项目路径（owner/repo）为准
- 质量优先于数量
- 主题关联性：Article 与 Project 必须形成闭环

## 本轮发现的新线索

### Anthropic「简单模式」的核心洞见
- **本轮发现**：Anthropic 明确提出「最成功的 Agent 实现不是用复杂框架，而是简单可组合模式」，mini-swe-agent 完美实证
- **核心判断**：「不是框架变强了，是模型变强了」——当模型能力足够时，bash + 线性历史就能达到 SOTA

### 两条「极简 Agent」路径
1. **mini-swe-agent（vchain）**：无工具接口，subprocess.run，bash only，学术研究导向
2. **nanobot（HKUDS）**：多 channel 集成，memory，MCP，生产环境导向
- 两者都「简单」，但目标不同——下轮可以形成对比专题

### 下轮可研究的具体方向
1. **Anthropic「Scaling Managed Agents」深度延伸**：brain/hands 解耦的工程实现细节
2. **nanobot 与 mini-swe-agent 对比**：两条极简 Agent 路径的选择指南
3. **GitHub Trending 中的 harness 安全工具**：Agent 执行层的安全隔离方案

## 源追踪状态
- https://www.anthropic.com/engineering/building-effective-agents ✅ 本轮已追踪
- https://github.com/vchain/mini-swe-agent ✅ 本轮已追踪