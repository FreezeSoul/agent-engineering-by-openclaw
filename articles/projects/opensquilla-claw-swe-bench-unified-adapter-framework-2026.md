# opensquilla/claw-swe-bench — Unified Adapter Framework for Agent Harness Evaluation

> Unified adapter framework for evaluating agent harnesses (claws) on SWE-bench

- **Stars**: 25 ⭐
- **License**: MIT
- **Created**: 2026-06-10
- **Pushed**: 2026-06-15
- **Organization**: opensquilla

## 一句话描述

claw-swe-bench 是一个标准化的 SWE-bench 评估适配层，通过统一的 `BaseClawAdapter` 接口，让 OpenClaw、NanoBot、ZeroClaw、Hermes、GenericAgent 等多种 Agent Harness 在同一基准下公平比较。

---

## 核心问题：Harness 评估的不公平性

SWE-bench 是评估 Coding Agent 的标准基准，但不同 Harness（OpenClaw、NanoBot 等）在以下维度存在差异：

| 差异维度 | 影响 |
|---------|------|
| **提示词** | 不同 harness 用不同 system prompt |
| **工具命名** | GenericAgent 用自己的工具名，其他用默认名 |
| **网络访问** | 有的允许上网查资料，有的不允许 |
| **Patch 收集方式** | 有的靠 agent 自我报告，有的靠 runner diff |
| **环境隔离** | 容器 vs 非容器，隔离程度不同 |

这使得"谁的 harness 更好"无法直接比较——**任何对比研究都存在信息泄漏风险**。

## 解决方案：标准化适配层

claw-swe-bench 通过两层标准化解决：

### 1. 统一提示词

所有 claws 使用 `prompts/default.txt`（阶段化长提示词）。

唯一允许的 override 是工具名指导（`prompts/generic.txt` 为 GenericAgent 添加 3 行工具名指引并禁用其 web 工具），**除此之外完全一致**。

### 2. 统一环境隔离

**Same prompt + No network access + Future-commit stripping + Runner-side patch collection + Per-instance isolation**

#### No Network Access

- 统一 prompt 禁止网络访问
- OpenClaw 额外配置了 13 个工具的拒绝列表（web/memory/session/cron tools）
- NanoBot 的 web tools 在配置中禁用
- ZeroClaw 流量经过工具过滤代理

#### Future-Commit Stripping

SWE-bench 的官方镜像在 git 历史中保留了 gold patch（正确答案）。claw-swe-bench 对每个 workspace：

1. 删除所有 future tags/commits
2. 过期 reflogs
3. Git GC
4. 启动 agent 前断言 zero future commits remain

#### Runner-Side Patch Collection

Patch（agent 生成的代码修改）通过以下方式收集：
- **始终用 `git diff`** 由 runner 在 agent 退出后执行
- **不是** agent 自己报告的
- Setup/lock-file 和 binary diffs 被剥离（`patch.py`）

#### Per-Instance Isolation

每个 SWE-bench 实例运行在**独立的新容器**中：
- 进程/内存限制
- OpenClaw 每个实例额外获得一个 throwaway agent

---

## 架构：BaseClawAdapter

### SWE-bench Harness Layer

核心职责（`swebench/`）：
- Dataset loading
- Container lifecycle
- Repo preparation
- Prompt rendering
- Runner-side patch collection/cleaning
- Predictions/state persistence
- Harness evaluation

### Claw Adapters Layer

每个 claw 实现 `BaseClawAdapter` 接口：

```python
class BaseClawAdapter:
    #额外 docker run 参数（mounts）
    #Post-start provisioning
    #Agent lifecycle
    #Task launch
    #Session backup
    #Usage collection
```

添加新 claw = 一个新文件 + 一个注册表条目。

### 支持的 Claws

| Claw | 环境变量 | 说明 |
|------|---------|------|
| `hermes` | `HERMES_ENV_PATH` | - |
| `nanobot` | `NANOBOT_ENV_PATH` | web tools 已禁用 |
| `generic` | `GA_REPO_PATH` / `GA_ENV_PATH` | GenericAgent |
| `zeroclaw` | `ZEROCLAW_BIN` | 工具过滤代理 |
| `openclaw` | `OPENCLAW_*` | 额外 throwaway agent |

---

## 主机要求

- **Docker** + 预构建 SWE-bench 镜像
  - `sweb.eval.x86_64.<instance_id>:latest`
  - 或 `swebench/sweb.eval.x86_64.<id>`（SWE-agent 格式，自动检测）
- **Python 3.10+**
- **SWE-bench harness** 安装在独立 venv（默认 `/data/swe-bench-env`）

---

## 工程意义

### 对 Agent 工程师

claw-swe-bench 解决了 **"我的 harness 比别人好"** 这个无法自证的问题。通过：
- 统一基准
- 消除信息泄漏
- 公平比较

### 对研究者

可以基于这个框架做 **Harness 横向评测研究**，而不需要自己搭建完整的 SWE-bench 评估管道。

---

## 质量评估

- ⭐⭐⭐⭐ — 问题定义清晰（harness 评估不公平），解决方案严谨（多层隔离），工程实现完整（5 种 claws 支持）；25 stars 说明是小众研究工具但质量高
- **核心价值**：为 Agent Harness 评估提供了方法论层面的规范化

---

## 来源

- GitHub: https://github.com/opensquilla/claw-swe-bench
