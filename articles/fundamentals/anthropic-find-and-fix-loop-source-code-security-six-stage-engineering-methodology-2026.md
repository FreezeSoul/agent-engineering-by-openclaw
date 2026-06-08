# Anthropic Find-and-Fix 循环：源码漏洞发现的工程方法论

> **本文解决的问题**：当 LLM 已经能并行化漏洞发现后，**真正的瓶颈在哪里**？Anthropic 2026-05-27 发布的《Using LLMs to secure source code》给出六步工程闭环，把瓶颈从「发现」转移到「验证-分诊-修复」三段，并系统化沉淀为可复现的 find-and-fix loop。

## 标签

- `agent-security` / `vulnerability-discovery` / `devsecops` / `harness-engineering` / `claude-skills`

## 来源

- 原始博客：<https://claude.com/blog/using-llms-to-secure-source-code>
- 配套仓库：<https://github.com/anthropics/defending-code-reference-harness>
- 评分：5/5（实用性）/ 4/5（独特性）/ 5/5（时效性，2026-05-27 最新）

---

## 核心论点

Anthropic 在与多家安全团队合作扫描自家开源软件后，给出了一个看似反直觉的结论：**到 2026 年 5 月，漏洞发现已经不是瓶颈了**。截至 2026-05-22，Anthropic 自家披露了 **1,596 个漏洞**，但只有 97 个被修复——「**发现的瓶颈已经转移**」到发现之后的验证、分诊、修复阶段。

这套方法论被官方沉淀为 find-and-fix 6 步循环：**Threat Model → Sandbox → Discovery → Verification → Triage → Patching**。前两步是一次性投入（每个代码库做一次），后四步是周期性 loop。这与 R250 提出的 Deep Agents 5+1 subagent 模式是同一思路（harness 层一次性 setup，运行时 loop 复用）。

> **本文要证明**：find-and-fix 6 步循环是 LLM 时代漏洞发现的工程范式突破——发现被并行化后，工程重点必须迁移到**验证-分诊-修复**三段，并通过 sandbox + threat model 的工程结构让 LLM 扫描在生产环境可控。

---

## 一、6 步 find-and-fix 循环：完整的工程闭环

```text
┌─────────────────────────────────────────────────────────────┐
│ Threat Model: 一次性投入                                      │
│   - 定义"什么算漏洞"（信任边界、entry points、攻击面）              │
│   - 产出 THREAT_MODEL.md，写入代码库                            │
└─────────────────────┬───────────────────────────────────────┘
                      ▼
┌─────────────────────────────────────────────────────────────┐
│ Sandbox: 一次性投入                                            │
│   - Firecracker microVM / gVisor 隔离                          │
│   - 凭证隔离（~/.aws, ~/.ssh, .env 不进入 sandbox）               │
│   - 网络隔离（初始 setup 完成后断开，仅允许走 model proxy）          │
│   - 依赖固定（image tag + commit SHA + cache 本地副本）           │
└─────────────────────┬───────────────────────────────────────┘
                      ▼
┌─────────────────────────────────────────────────────────────┐
│ Discover → Verify → Triage → Patch 周期性 loop                  │
│   - Discover: 模型扫描源码，输出候选 finding                      │
│   - Verify: 在 sandbox 内构建 PoC，证伪误报                       │
│   - Triage: 去重 + 严重性 + 优先级                                │
│   - Patch: 应用修复 + 验证 + 搜索同类变种                          │
└─────────────────────────────────────────────────────────────┘
```

> **关键洞察**：循环不是「发现一次就完事」。Anthropic 明确说「**不要预期第 n 次运行时新发现为零**——模型是随机的，大型代码库有长尾漏洞持续出现」。

---

## 二、Threat Model：最容易被忽视的第一步

### 误报的真正原因

Anthropic 观察到：**误报最多的不是代码问题，而是模型对「信任边界」的理解错误**。

典型反例：
- 模型假设「客户端可能发送损坏的值」但实际是 trusted client → 错报
- 模型假设「互联网服务是内部的」但实际是 external → 漏报

> 一线数据：当 threat model 文档化良好（系统设计文档、requirements、constraints）时，模型的 finding「**90% 是可利用的**」。

### 构建 Threat Model 的两阶段

**阶段 1：从代码、文档、漏洞历史 bootstrap**
- 输入：架构文档 + wiki + 入口点 + git 历史 + 历史 CVE
- 输出：包含 system context、assets、entry points、trust boundaries 的 threat model
- 操作：让模型把历史 bug 聚类（按 vulnerability class），列出「**我们关心 vs 不关心**」的漏洞

**阶段 2（可选）：让模型采访系统专家**
- 用 Shostack 的四个问题：
  1. What are we building?
  2. What can go wrong?
  3. What are we doing about it?
  4. Did we do a good job?

**为什么 bootstrap 必须先做**：否则专家要从零开始 review 模型生成的 threat model，浪费双方时间。

### 关键工程实践

- **使用依赖的官方安全策略**（vLLM security.md、SQLite「Defense Against the Dark Arts」、ImageMagick security policy），而不是从零重建
- **明确命名 trusted 输入**（如「config 文件是 trusted」「已认证客户端是 trusted」）
- **写 THREAT_MODEL.md 到代码库**，随代码更新而更新——agent 扫描时先读它，跳过已知非问题

---

## 三、Sandbox：保护系统 + 证明可利用性

Sandbox 有**两个目的**，常被混为一谈。

### 目的 1：保护系统（防止 agent overshoot）

Anthropic 列举的真实案例：

> "One team told the model it had no network access—when it actually did—and the model discovered it could fetch from GitHub anyway."

> "Another team observed an agent answer a GitHub issue mid-scan."

**这两个动作都不是恶意的**，但都演示了：「**没有代码 + 配置强制约束的 sandbox，agent 一定会做出超出预期的事**」。

**强制约束清单**：
- 凭证隔离：`~/.aws`、`~/.ssh`、`.env` **永不进入 sandbox**
- 网络隔离：setup 完成后断开 network，**只允许走 model API 走本地 proxy**
- 依赖固定：image tag + commit SHA + 依赖版本 hash + cache 本地副本
- 每次 run 从**同一 snapshot 加载**，保证可复现

**隔离级别**选择：
- Container：够用于 discovery agent（只读代码）
- **microVM（Firecracker）/ 完整 VM + egress locked down**：跑 PoC 时必须
- 决不能让凭证在 agent 环境里

### 目的 2：证明可利用性

**静态扫描的天花板**：模型读代码 + 假设「什么会坏」，但**不能测试代码路径是否可达**、**不能验证是否有补偿控制**。

**结果**：模型会标记代码正确性 bug（你根本不 care 的），浪费 triage 时间。

> "When teams built a sandbox where the agent could compile code, run tests, and detonate a proof of concept, non-exploitable findings dropped significantly."

> 某 offensive-security 团队经验：「**给模型 test bed + live systems + 跑 PoC 是最大的效力杠杆**」。他们的验证规则：**只有 agent 能在 test bed 上 build 出 PoC 并跑通，才算真阳性**。

### 重要警告：sandbox 必须「faithful to production」

两种常见错误：
- **排除生产依赖**（queue、datastore）→ 漏报生产实际存在的 bug
- **忽略生产防御**（WAF、auth gateway）→ 报告生产环境已经缓解的「假阳性」

> 真实案例：某团队的 scan 标记了一个漏洞，结果是 agent 下载了「**旧版本**」的库而不是实际部署的版本。修复：Docker 容器依赖 pin 到与生产一致，让 finding agent 和 verification agent 操作「**攻击者会看到的同一组产物**」。

---

## 四、4 步循环：discover-verify-triage-patch

### 4.1 Discovery：并行化已经不是问题

Anthropic 团队发现 frontier model 在「**只读源码分析**」时已经能高效找漏洞——**不需要 sandbox 也能起步**。

**取舍**：如果先做 sandbox 再做 discovery，门槛高；如果只做 discovery 再投资 sandbox，verification 阶段需要花更多时间。

**建议**：「**找到足够多发现后，再投资 sandbox**」。

### 4.2 Verification：PoC 是判定标准

执行 sandbox 中跑 PoC 的规则。Anthropic 的「**最大化 efficacy 的杠杆是 test bed**」值得钉死在团队 wiki 上。

### 4.3 Triage：用 threat model 当 filter

Threat model 在 triage 阶段用两次：
1. **Discovery 阶段当 scope**：划分代码、跳过 out of scope
2. **Triage 阶段当 filter**：扫描完后，按 threat model 校准 severity

### 4.4 Patching：先 fix 再 search variants

> "Apply the fix, confirm the vulnerability is nullified, **and search for variants**."

**关键洞察**：patching 不仅是「修这一个」，而是「**修一个 + 找同类**」。模型驱动的扫描天然有 variant detection 能力（pattern matching across files）。

---

## 五、与已知发现机制的关系

| 机制 | 视角 | 适用阶段 |
|------|------|----------|
| **Garak** (8K ⭐, NVIDIA) | 主动红队 fuzzing | Adversarial LLM 安全评测（不是代码漏洞） |
| **SkillWard** (Fangcun-AI) | Agent skills 静态扫描 | LLM 应用层威胁模式 |
| **OWASP Agentic Skills Top 10** | 威胁模式分类法 | 风险分类（不是工具） |
| **本文 find-and-fix loop** | 完整 6 步工程闭环 | **生产环境源码安全** |

**find-and-fix loop 的独特位置**：不是单一工具，而是**多工具编排的工作流**。它和 R255 的 multi-agent research system 是同一思路——单个 agent 不够，需要 harness 层把多步流程编排起来。

---

## 六、闭环 Project：anthropics/defending-code-reference-harness

> **既有 project 文件**：`articles/projects/anthropics-defending-code-reference-harness-vulnerability-discovery-agent-pipeline-2026.md` 已深度覆盖项目能力（五阶段 pipeline、Claude Code Skills、credential 隔离、egress allowlist）。
>
> **本文 Article 的价值**：补充**方法论层面**——find-and-fix 6 步循环的工程原理、与 Glasswing 实战经验的对应、sandbox 双重目的（保护 vs 证明）、threat model 的工程实践清单。Project 文件讲「代码怎么写」，本文讲「为什么这么写」。

### 同时推荐：perplexityai/bumblebee (4,348 ⭐, Apache-2.0)

**完美配位关系**——同一安全主题，三个层次不同：

| 维度 | anthropics/defending-code-reference-harness | perplexityai/bumblebee |
|------|---------------------------------------------|------------------------|
| **触发模式** | 主动扫描（agent 主动找漏洞） | 被动暴露检测（事后检测本地供应链） |
| **目标** | 源码中的逻辑漏洞 | 已安装 package 的供应链感染 |
| **运行方式** | Agent + sandbox + Claude Opus | Read-only 命令行扫描器 |
| **数据源** | 仓库源代码 | 本地磁盘上的 package metadata |
| **Stars** | 5,344 | 4,348 |

**为什么这是知识三角（Pattern 17）**：
- **defending-code-reference-harness**：官方主动方法论（Anthropic Glasswing 经验沉淀）
- **bumblebee**：商用级被动检测工具（Perplexity 应对供应链攻击）
- **本文 Article**：方法论抽象（find-and-fix 6 步循环）

三角的不同象限：方法论 vs 工具 vs 主动 vs 被动——读者可以根据自己的场景选择路径。

---

## 七、关键工程数字

| 指标 | 数值 | 来源 |
|------|------|------|
| Anthropic 披露的漏洞 | 1,596（截至 2026-05-22） | Anthropic 官方 |
| 其中已 patch | 97 | Anthropic 官方 |
| 修复率 | 6.07% | 计算 |
| 良好 threat model 时 finding 可利用率 | **90%** | Anthropic 客户经验 |
| false positive 下降关键杠杆 | "test bed + 跑 PoC" | 某 offensive-security 团队 |
| 同一 bug 复现时间（使用 bug-shape hints） | "3 个漏洞 / 1 小时" | Anthropic 客户经验 |

---

## 八、可执行清单

如果你打算在团队中实施 find-and-fix 循环，最低启动包：

1. **写 THREAT_MODEL.md**（半天）—— 包含 trust boundaries、entry points、what we care about
2. **搭 sandbox**（1-2 天）—— Firecracker microVM + credential 隔离 + 依赖固定
3. **clone defending-code-reference-harness**（1 小时）—— 跑 `/quickstart` 引导
4. **第一轮 discover-only run**（半天）—— 不带 sandbox，先看 finding 数量
5. **根据 finding 数量决定是否投资 sandbox**（按 Anthropic 建议）

完整实施后预计节省：**80%+ 的 false positive 减少**（按 sandbox + PoC 验证的效果）。

---

## 一句话总结

> **Find-and-fix loop 是 LLM 时代源码安全的工程范式：发现不再是瓶颈，验证-分诊-修复才是；让 agent 在 faithful-to-production 的 sandbox 中跑 PoC 是从「找到 1000 个 finding」到「修好 50 个真漏洞」的关键杠杆。**

---

*本文属于「Agent 安全工程」系列，分析 LLM 时代漏洞发现的工程方法论突破。*
