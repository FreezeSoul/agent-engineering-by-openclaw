# LangChain / LangGraph / LangSmith Changelog Watch

> 本文件追踪 LangChain 生态的重大更新。每日检查 GitHub Releases 和官方博客，有重大版本更新时追加。

---

## 2026-03-23｜LangSmith Fleet 发布（Agent Builder 重命名）

**版本**：无版本号（产品重命名）
**性质**：🟡 Minor 产品重构
**来源**：[LangChain Blog](https://blog.langchain.com/introducing-langsmith-fleet/) | [LangChain Changelog](https://changelog.langchain.com/announcements/agent-builder-is-now-langsmith-fleet)

### 变更内容

LangChain 宣布将 **Agent Builder** 重命名为 **LangSmith Fleet**，定位为企业级 AI Agent 构建与管理平台。

**核心变化**：
- **产品定位升级**：从单一 Agent 构建工具 → 企业多 Agent 协作治理平台
- **新增企业能力**：权限管理（Permissions）、凭证管理（Credentials）、多 Agent  Oversight
- **无代码入口**：提供模板化方式，非技术用户也可构建 Agent
- **名称变更**：产品 UI、文档、官网均已更新为新名称
- **兼容性**：所有现有 Agent、配置、集成保持兼容，无 Breaking Changes

**为什么重要**：
这是 LangChain 从"开发者框架"向"企业平台"战略延伸的明确信号。Fleet 的权限和凭证管理能力，直接对应 RSAC 2026 期间 Agentic AI 安全讨论中的"身份治理"需求。

**版本判断**：Minor（产品更名 + 功能扩展，无破坏性变更）

---

## 2026-03｜LangChain × NVIDIA 企业级 Agent 平台

**版本**：战略合作（无具体版本号）
**性质**：🟡 生态系统
**来源**：[LangChain 官方新闻](https://blog.langchain.com/nvidia-enterprise/)

LangChain 与 NVIDIA 联合发布企业 Agentic AI 平台，在 RSAC 2026 期间（3月23-26日）宣布：

- **目标**：结合 LangChain 的 Agent 开发框架 + NVIDIA AI 基础设施，实现企业级生产部署
- **覆盖**：构建、部署、监控全生命周期
- **NVIDIA 能力**：NIM 微服务、CUDA 加速、企业级安全

**版本判断**：Minor（合作公告，非代码版本更新）

---

## 2026-03｜LangGraph Deep Agents SDK 更新

**版本**：Deep Agents SDK（独立包）
**性质**：🟢 Patch / 特性更新
**来源**：[LangChain Blog - Autonomous Context Compression](https://blog.langchain.com/autonomous-context-compression/)

### 值得关注的更新

- **Autonomous Context Compression**：Deep Agents SDK 新增功能，允许模型自主压缩自身上下文窗口，减少 token 消耗
- **Open SWE 发布**：基于 Deep Agents + LangGraph 的开源代码 Agent 框架，专为内部编码任务设计
- **LangSmith CLI & Skills**：AI 编码 Agent（Codex、Claude Code、Deep Agents CLI）的 LangSmith 生态集成技能包

**版本判断**：Patch（工具增强，不影响主框架）

---

## 2026-03｜LangChain v1.x 稳定版

**版本**：LangChain 1.x（主版本）
**性质**：🔴 Major 架构更新
**来源**：[LangChain Release Notes](https://github.com/langchain-ai/langchain/releases)

### 关键里程碑

LangChain 1.0 正式发布（与 LangGraph 1.0 GA 同步），代表框架从"实验性"到"生产就绪"的跨越：

- **API 稳定性承诺**：语义化版本控制，Breaking Changes 需 Major 版本升级
- **LangChain Core**：核心接口稳定，第三方集成需明确兼容性声明
- **LangChain Expression Language (LCEL)**：链式调用统一语法
- **生产级 Tracing**：LangSmith 深度集成，支持结构化日志

**版本判断**：Major（生产就绪，API 稳定承诺）

> ⚠️ **注意**：LangChain 1.0 GA 是 2025 年 10 月的重大里程碑，建议回顾官方 Release Notes 确认历史版本完整性。

---

## 历史版本速查

| 时间 | 版本 | 关键变化 |
|------|------|---------|
| 2025-10 | LangChain 1.0 GA + LangGraph 1.0 GA | 生产就绪，API 稳定 |
| 2025-Q4 | LangSmith Agent Builder | 企业级 Agent 构建 |
| 2026-03 | Agent Builder → LangSmith Fleet | 重命名 + 企业治理 |
| 2026-03 | Deep Agents SDK | Autonomous Context Compression |

---

## 下次检查计划

- 每日检查 LangChain Blog 和 GitHub Releases
- 关注 LangChain 1.x 的 Breaking Changes 公告
- 监控 NVIDIA 合作平台正式发布

---

*本文件由 AgentKeeper 自动维护 | 追踪频率：每日*
