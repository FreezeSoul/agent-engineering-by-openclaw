# Bernstein：每一个调度决策都有迹可查的多 Agent 编排

> 本项目推荐：[sipyourdrink-ltd/bernstein](https://github.com/sipyourdrink-ltd/bernstein)，542 Stars，MIT License，Python 3.12+。

---

## 核心命题

Bernstein 解决了一个具体而痛苦的问题：**每月花 $400 运行三个并行 coding agent，得到的是非确定性的合并结果**。

它的解法是：不依赖 LLM 做调度，而是用纯 Python 写一个确定性调度器，所有调度决策都写入 HMAC 签名审计链，每一个文件写入都记录完整的血缘关系。

这不是一个"让 Agent 更聪明"的项目，而是一个"让 Agent 的行为可审计、可重现、可追究"的项目。

---

## 为什么值得关注

### 1. HMAC-SHA256 审计链：让调度决策不可篡改

每个调度决策（哪个 agent 运行、哪个文件被修改、哪个模型被调用）都会写入一条记录，用 RFC 2104 HMAC-SHA256 签名。

```bash
$ bernstein lineage verify <run_id>
[audit] ✓ HMAC signature valid
[lineage] src/auth/middleware.py
  produced-by: claude-sonnet (run-abc123)
  inputs: [src/auth/base.py, tests/test_auth.py]
  prompt-sha: 4a7f2e...
  model: sonnet-4.6
  cost: $0.12
```

这意味着：当出现问题时，你有一份完整的、无法篡改的行动记录。不是"Agent 做了什么"，而是"**为什么**做了这个决策，**基于什么输入**"。

笔者认为，比起那些"用 LLM 反思来保证质量"的方案，这种基于加密签名的审计链更适合需要合规性审查的团队。

### 2. 凭证隔离：不在客户端 repo 中留下凭证

> "credentials stay in your env, not the client's; agents you spawn are whichever CLI tool the client already trusts"

Bernstein 的设计是：**operator 的凭证留在 operator 的环境中**，通过 per-session zero-trust JWT 传递授权，Bernstein 的 agent token 存在 `.sdd/runtime/agent_tokens/` 中。Agent 进程从不直接持有凭证。

这与 Anthropic 在 *Scaling Managed Agents* 中描述的"Auth in vault"模式高度一致：凭证不在 Agent 可达范围内，Agent只能通过授权代理访问外部服务。

### 3. 确定性调度器：零 LLM 在协调回路中

Bernstein 用一个 LLM 调用来分解目标（goal decomposition），之后所有的调度决策——在哪个 git worktree 中运行哪个 agent、什么时候重试、什么时候合并——都是纯 Python。

```python
# Bernstein调度器示意（非实际代码）
for task in decomposed_tasks:
    worktree = create_worktree(task.id)
    agent = select_agent(task, budget)
    result = agent.run(worktree, task.prompt)
    if result.test_gates_pass():
        merge_queue.add(task)
    else:
        retry_schedule.append(task)
```

这意味着：**你可以 replay 昨天的计划，得到昨天的任务图**。这是任何 LLM-based orchestrator 都无法保证的属性。

### 4. 44 个 CLI Agent 适配器：最大的 Agent 覆盖范围

Bernstein 支持44 个 CLI agent 适配器，包括：

| Agent | 模型 | 安装方式 |
|-------|------|---------|
| Claude Code | Opus 4, Sonnet 4.6, Haiku 4.5 | `npm install -g @anthropic-ai/claude-code` |
| Codex CLI | GPT-5, GPT-5 mini | `npm install -g @openai/codex` |
| GitHub Copilot CLI | Copilot-managed | `npm install -g @github/copilot` |
| Gemini CLI | Gemini 2.5 Pro/Flash | `npm install -g @google/gemini-cli` |
| ... | ... | ... |

支持 local 模型（Ollama + Aider）、 sovereign/on-prem LLM（CLM gateway）、以及任何带 `--prompt` 接口的通用 CLI agent。

### 5. Git Worktree 并行化：真正的隔离执行

每个 agent 运行在独立的 git worktree 中，Bernstein 的 merge queue 序列化合并顺序，避免竞态条件：

```
[manager] decomposed into 4 tasks
[agent-1] claude-sonnet: src/auth/middleware.py  (done, 2m 14s)
[agent-2] codex:         tests/test_auth.py      (done, 1m 58s)
[agent-3] gemini-cli:     src/auth/routes.py     (done, 3m 02s)
[agent-4] aider: docs/auth.md (done, 1m 41s)
[verify]  all gates pass. merging to main.
```

---

## 关键设计对比

| 维度 | Bernstein | 典型 LLM Orchestrator |
|------|-----------|---------------------|
| **调度确定性** | 纯 Python，可 replay | LLM 调度，非确定性 |
| **审计粒度** | 每步 HMAC 签名 | 无结构化审计 |
| **凭证管理** | per-session JWT + vault | 环境变量/共享 |
| **Agent 隔离** | git worktree | 共享进程/容器 |
| **血缘追踪** | 每文件完整 lineage | 无 |
| **部署模式** | on-prem only | SaaS 为主 |

---

## 适用场景

**Bernstein 的目标用户**（满足两条以上说明你可能需要它）：

- 工程团队同时运行 ≥3 个 CLI coding agent 并行任务
- 需要合规性审查的 workflow（HMAC 签名审计链）
- 需要 Agent 决策过程可完整回放
- 每月在 coding agent 上的支出超过 $1k，需要确定性结果
- 需要 air-gap 部署（不依赖外部 SaaS）

**不适合的场景**：

- 只需要一个 pair-programmer 对话的场景
- prototype 阶段，merge gate 过度的场景
- 非 coding 任务（研究、写作、数据分析 pipeline）
- 需要厂商 SLA 支持的企业场景

---

## 原文关键引用

> "Why the scheduler is plain Python: Most agent orchestrators use an LLM to decide who does what. That is non-deterministic and burns tokens on scheduling instead of code."

> "I wrote bernstein because I was paying $400/month in claude bills running three coding agents in parallel and getting nondeterministic merges."

> "Credentials stay in your env, not the client's; agents you spawn are whichever CLI tool the client already trusts."

---

## 快速开始

```bash
# 安装（30 秒）
pipx install bernstein
bernstein init
bernstein run -g "fix the failing test in tests/test_foo.py"

# 带审计日志的运行
bernstein run -g "Add JWT auth" --audit

# 验证血缘
bernstein lineage verify <run_id>
```

---

## 与本文档其他内容的关联

- **本文配对 Article**：[Anthropic Scaling Managed Agents：大脑与手的分离](./anthropic-scaling-managed-agents-brain-hands-2026.md) — Anthropic 提出的 Brain/Hands/Session 三元解耦架构，Bernstein 在工程层面实现了相同的解耦原则（Session 外部化 + 凭证隔离 + 确定性调度）

---

*项目最后更新：2026-06 | License: Apache 2.0 | 维护者：solo open source（GitHub Sponsors 赞助）*