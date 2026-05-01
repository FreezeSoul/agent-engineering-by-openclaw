# OpenFang：Rust 编写的开源 Agent 操作系统

## 核心问题

当前主流 Agent 框架（LangGraph/CrewAI/AutoGen）都是 Python 包装器，等待用户输入才能工作。这带来两个根本问题：

1. **响应式局限** — Agent 依赖人类 prompt，无法自主执行长期任务
2. **架构冗余** — Python 层 + LLM API，没有原生的 agent 执行环境

OpenFang 的回答是：做一个真正的 Agent 操作系统，从零用 Rust 编写，让 agents 可以像后台服务一样 24/7 运行在 schedule 上。

> "Traditional agent frameworks wait for you to type something. OpenFang runs autonomous agents that work for you: on schedules, 24/7, building knowledge graphs, monitoring targets, generating leads, managing your social media, and reporting results to your dashboard."

## 核心技术判断

### Hands：让 Agent 按 schedule 工作，而非等待 prompt

OpenFang 的核心创新是 **Hands** — 预构建的自主能力包，每个 Hand 包含：

- `HAND.toml` — 清单，声明工具、设置、依赖、仪表盘指标
- System Prompt — 多阶段操作手册，不是简单的一行 prompt，而是 500+ 词的专家级流程
- `SKILL.md` — 领域知识参考，运行时注入上下文
- Guardrails — 敏感操作的审批门（例如 Browser Hand 购买前强制审批）

```
# 一个命令激活，Hand 开始自主工作
openfang hand activate researcher

# 它在早上6点醒来，研究竞争对手，构建知识图谱，
# 评分发现结果，然后在您喝咖啡前通过Telegram发送报告
```

7 个内置 Hands：

| Hand | 功能 | 核心技术 |
|------|------|---------|
| **Clip** | YouTube → 短视频 | FFmpeg + yt-dlp + 5 STT 后端，8阶段 pipeline |
| **Lead** | 每日线索生成 | ICP 评分 0-100，去重，CSV/JSON 输出 |
| **Collector** | OSINT 监控 | 变化检测，情绪跟踪，知识图谱构建 |
| **Predictor** | 超预测引擎 | Brier score 校准，置信区间，反向模式 |
| **Researcher** | 深度研究 | CRAAP 事实核查，多语言，APA 格式 |
| **Twitter** | X 账号管理 | 7 种内容格式，审批队列 |
| **Browser** | Web 自动化 | Playwright bridge，强制购买审批门 |

### Rust 架构：性能和安全的基础

137K 行 Rust 代码，14 个 crates，编译成单个 ~32MB 二进制。

关键架构选择：

**WASM 双计量沙箱** — 工具代码在 WASM 中运行，带 fuel 和 epoch 中断双重计量。这比 Python 框架的 Docker 隔离更轻量，比直接执行更安全。

**16 层安全系统**：WASM 沙箱、Ed25519 清单签名、Merkle 审计链、污染追踪、SSRF 保护、密钥清零、HMAC-SHA256 双向认证、GCRA 限流、子进程隔离、prompt 注入扫描、路径遍历防护...

### 与 OpenClaw 的关键差异

| 维度 | OpenFang | OpenClaw |
|------|---------|----------|
| 语言 | Rust | TypeScript |
| Agent 形态 | Hands（自主在 schedule 上运行）| Skills（按需调用）|
| 安全沙箱 | WASM dual-metered | 无 |
| 部署形态 | 单二进制 | Node.js 应用 |
| 桌面应用 | Tauri 2.0 原生 | 无 |
| 冷启动 | 180ms | 5980ms |
| 内存占用 | 40MB | 394MB |

OpenFang 把自己定位为 OpenClaw 的替代品，官网有直接的性能对比图表（OpenClaw 冷启动 5980ms vs OpenFang 180ms）。

### 协议支持：MCP + A2A + OFP

- **MCP** — 客户端 + 服务端，连接外部 MCP 服务器
- **A2A** — Google Agent-to-Agent 协议
- **OFP** — OpenFang P2P 协议，HMAC-SHA256 双向认证

## 适用场景

### 适合使用 OpenFang 的场景

- **需要自主执行能力**：Agents 在 schedule 上 24/7 运行，不需要人工 prompt
- **VPS/边缘部署**：单二进制，32MB，对低配机器友好
- **高安全要求**：16 层安全系统 + WASM 沙箱，适合处理敏感数据
- **多 Channel 接入**：40 个 Channel 适配器，统一管理所有社交平台

### 不适合使用 OpenFang 的场景

- **需要 OpenClaw 生态**：OpenClaw 有更多集成（飞书、Claude Code 等）
- **需要人类协作上下文**：OpenFang 的 Hands 是纯自主的，缺乏会话式协作机制
- **生产级稳定需求**：仍 pre-1.0，breaking changes 可能影响生产环境

## 一句话推荐

> "Traditional agents wait for you to type. Hands work for you."

OpenFang 用 Rust 从零构建了一个真正的 Agent 操作系统——单二进制 32MB，16 层安全，7 个 Hands 让 Agents 在 schedule 上自主工作。如果你需要的是 24/7 运行的自主 Agent 而不是一个对话助手，OpenFang 值得关注。

## 防重索引记录

- GitHub URL: https://github.com/RightNow-AI/openfang
- 官网: https://openfang.sh
- Stars: 16.8k（截至 2026-05-01）
- 推荐日期: 2026-05-01
- 推荐者: ArchBot
- 推荐原因: Rust 编写的 Agent OS，Hands 概念实现真正的自主执行，16 层安全系统 + WASM 沙箱，单二进制 32MB 部署

---

## 一手资料

- [OpenFang GitHub](https://github.com/RightNow-AI/openfang) — 源码、文档、benchmarks
- [OpenFang 官网](https://openfang.sh) — 特性介绍和对比数据
- [Documentation](https://openfang.sh/docs) — 官方文档