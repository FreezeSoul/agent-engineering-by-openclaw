# google/agents-cli：把任意 Coding Agent 变成 Google Cloud Agent 专家

> GitHub: 3,119 Stars | License: Apache-2.0 | 官方 Google 仓库

## 核心命题

google/agents-cli 解决了一个现实问题：当你用 Claude Code、Codex 或 Gemini CLI 这样的 coding agent 在 Google Cloud 上构建和部署 agent 时，你需要学习一大套 Google Cloud CLI（gcloud、kubectl、docker 等）才能正确完成任务。agents-cli 把这些 CLI 和最佳实践封装成 skills，让你的 coding agent 直接学会用它们——你只需要用自然语言描述需求，agent 会调用正确的工具。

**笔者的判断**：比起让开发者自己学一套 Google Cloud 工具链，让 coding agent 学这套工具链是更合理的分工——前者是一次性成本，后者是可复用的能力积累。agents-cli 的本质是把 Google Cloud 的运维知识转化为 agent 可调用的 skill，而不是让人类重新培训。

---

## 核心能力

### Skill 体系（6 个核心 Skill）

agents-cli 把 Google Cloud agent 开发经验封装成 6 个可组合的 skill：

| Skill | 能力 |
|-------|------|
| `google-agents-cli-workflow` | 开发生命周期、代码保留规则、模型选择 |
| `google-agents-cli-adk-code` | ADK Python API — agents、tools、orchestration、callbacks、state |
| `google-agents-cli-scaffold` | 项目脚手架 — 创建、增强、升级 |
| `google-agents-cli-eval` | 评估方法论 — metrics、datasets、LLM-as-judge、adaptive rubrics |
| `google-agents-cli-deploy` | 部署 — Agent Runtime、Cloud Run、GKE、CI/CD、secrets |
| `google-agents-cli-observability` | 可观测性 — Cloud Trace、logging、第三方集成 |

每个 skill 都可以被任意 coding agent 通过 `npx skills add google/agents-cli` 安装。

### CLI 命令体系

```
agents-cli setup           # 安装 CLI + skills 到 coding agents
agents-cli scaffold <name> # 创建新的 agent 项目
agents-cli scaffold enhance # 为现有项目添加部署/CI/CD/RAG
agents-cli run "prompt"    # 用单次 prompt 运行 agent
agents-cli eval generate   # 在评估数据集上运行 agent，生成 traces
agents-cli eval grade      # 对 traces 进行评分
agents-cli eval dataset synthesize # 综合生成多轮评估场景
agents-cli eval compare    # 对比两个评估结果文件
agents-cli eval analyze    # 聚类 grade 结果中的失败模式
agents-cli eval metric list # 列出可用 metrics
agents-cli eval optimize   # 使用评估数据自动调优 agent prompts
agents-cli deploy          # 部署到 Google Cloud
agents-cli infra single-project # 配置单项目基础设施
agents-cli infra cicd      # 设置 CI/CD pipeline + staging/prod 基础设施
```

### 多 Agent 兼容

官方声明兼容：
- **Gemini CLI**（Google 自家）
- **Claude Code**（Anthropic）
- **Codex**（OpenAI）
- **任何其他 coding agent**

这意味着 agents-cli 的 skill 层是**框架无关的**，不绑定任何特定 coding agent。

---

## 与 Google ADK 的关系

Google ADK（Agent Development Kit）是 Google 的官方 agent 框架。agents-cli 不是 ADK 的替代品，而是 ADK 的**工程效率层**：

> "ADK is an agent framework. agents-cli gives your coding agent the skills and tools to build, evaluate, and deploy ADK agents end-to-end."

这意味着：
- **ADK**：定义如何写一个 agent（Python API、tool 定义、orchestration 逻辑）
- **agents-cli**：定义如何把 agent 从想法变成生产级部署（scaffold、eval、deploy、observability）

两者组合覆盖了「写 agent」到「运行 agent in production」的完整生命周期。

---

## 本地开发无需 Google Cloud

值得注意的设计决策：**本地开发（create、run、eval）完全不需要 Google Cloud 账号**，只需要 AI Studio API key 就能用 Gemini 运行 ADK agent 本地开发。

这降低了实验门槛，让开发者在接触云部署之前先验证 agent 逻辑。

---

## 与 Coinbase Agent-First 转型的关联

Coinbase 案例（R550 Article）揭示了企业 Agent-first 转型的一个核心需求：**需要完整的工具链支撑 agent 从开发到部署的全生命周期**。

agents-cli 恰好填补了这个需求：
- Coinbase 需要「工程师定义目标、agent 执行」的模式 → 需要 `eval grade` 评估 agent 输出质量
- Coinbase 需要「living docs 作为评估框架」→ agents-cli 的 `eval dataset synthesize` 支持多轮场景生成
- Coinbase 需要 5-7 个并行 agent → agents-cli 的 scaffold/enhance 支持多 agent 项目管理

**结论**：agents-cli 是企业级 Agent-first 工程转型的工具链基础设施，与 Coinbase 案例形成「实践层-工具层」闭环。

---

## License 与使用

License: **Apache-2.0**（无限制条款，可商用）

安装方式：
```bash
# 一键安装 CLI + skills
uvx google-agents-cli setup

# 单独安装 skills（coding agent 会自动使用）
npx skills add google/agents-cli
```

前置依赖：Python 3.11+、uv、Node.js

---

*来源：https://github.com/google/agents-cli，Stars: 3,119（2026-06-26），Apache-2.0*