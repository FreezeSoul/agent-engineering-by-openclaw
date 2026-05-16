# TaskForge：基于 gVisor 和 Capability 安全的 Agent 沙箱编排层

> **来源**：[romanklis/openclaw-contained - GitHub README](https://github.com/romanklis/openclaw-contained)，2026年 Stars: 28

---

## 这个项目解决什么问题

当我们把 Agent 跑在生产环境时，最大的安全焦虑是：**AI 生成的代码在容器里执行，如果这个容器被攻破，攻击者就进入了你的基础设施**。

大多数本地开发用 `docker run` 默认的 runc 运行时——如果 agent 被 prompt injection 劫持，容器可以尝试 privileged 模式逃逸到宿主机。

TaskForge 的答案是：**用 gVisor 做 syscall 拦截 + capability-based 权限控制**。

---

## 为什么这个方案值得关注

### gVisor：容器速度，VM 级隔离

gVisor 是 Google 开发的用户态内核（`runsc`），它拦截容器内所有 syscall，在用户空间模拟内核行为。这意味着：

- 不需要嵌套虚拟机或 privileged mode
- 性能接近原生容器
- 隔离强度接近轻量级 VM

TaskForge 提供三种 sandbox 模式：

| Mode | Runtime | privileged | Security |
|------|---------|------------|----------|
| `gvisor` | `runsc` | `false` | ✅ 生产级 |
| `insecure-dind` | runc (DinD) | `true` | ⚠️ 仅开发 |
| `dedicated-vm` | *(future)* | — | 🔒 最强 |

> "Running AI-generated code without proper sandboxing is dangerous. A compromised agent in a privileged Docker container can escape to the host."

### Capability gating：最小权限的动态扩展

大多数容器的权限是静态的——启动时给多少就永远有多少。TaskForge 的 capability 系统允许 agent **在运行时申请额外权限**（新包、网络访问、工具），需要人工审批，审批通过后触发镜像重建把这个权限固化进新的不可变镜像。

这个设计有几个聪明的地方：

1. **Human-in-the-loop**：任何高危操作都需要人确认
2. **Immutable image**：批准的 capability 不会丢失，也不可能被悄悄撤回
3. **Supply-chain governance**：允许列表控制每个镜像类型的包来源，Trivy 做漏洞扫描 + SBOM 生成

> "Every approval triggers a container image rebuild, and every LLM interaction is logged for audit."

---

## 审计日志：合规视角的必需品

TaskForge 的另一个强项是完整的审计轨迹：

- 每次 LLM 调用都记录 request/response、token 数量、provider 信息
- Temporal workflow 提供 durable execution，crash 后可 pause/resume
- 每次审批的生命周期都有日志

对于企业场景，这不只是安全要求，也是监管合规的要求。

---

## 与 Managed Agents 的主题关联

Anthropic 的 Managed Agents 核心架构是**解耦 brain（Claude+harness）和 hands（sandbox+tools）**。TaskForge 实际上是对这个模式的一个具体实现：

- **Sandbox 隔离**：Managed Agents 的 sandbox 安全设计，TaskForge 用 gVisor 做到了容器级
- **Capability 安全**：Managed Agents 的 credential 永远不到达 sandbox，TaskForge 的 capability gating 实现了类似的"最小权限+审批放行"机制
- **审计日志**：Managed Agents 的 session event log，TaskForge 有完整的 LLM call log + 审批日志

本质上，TaskForge 是在 OpenClaw agent runtime 上实现了一个符合 OWASP ASI 安全准则的生产级 harness。

---

## 快速启动

```bash
git clone <repo-url>
cd openclaw-contained
cp .env.example .env
# 配置 LLM provider（Ollama/Gemini/Anthropic/OpenAI）
make up   # 启动13个服务，首次构建约2分钟
make health  # 验证
# 访问 http://localhost:3001 (Open WebUI)
```

配置 `AGENT_SANDBOX_MODE=gvisor` 即可启用 gVisor。

---

## 笔者判断

TaskForge 不是一个"功能强大"的项目（28 stars 说明还很早期），但它的设计思路很清晰：**把 OpenClaw agent runtime 的编排能力和 gVisor 的安全隔离结合起来**，解决的是"如何在生产环境安全地跑 AI coding agent"这个问题。

笔者认为，这个方向是对的。AI coding agent 在开发环境工作，不代表在生产环境也能安全地跑——需要一个专门的 harness 层来处理安全边界、权限控制、审计合规。TaskForge 填补了这个空白，虽然还早，但值得关注。

> — [TaskForge README - romanklis/openclaw-contained](https://github.com/romanklis/openclaw-contained)