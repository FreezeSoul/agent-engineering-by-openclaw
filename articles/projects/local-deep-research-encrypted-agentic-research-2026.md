# Local Deep Research：加密隐私 + 多源研究的本地化 Agent 实践

## TRIP 四要素

| 要素 | 内容 |
|------|------|
| **T - Target** | 需要深度研究能力但对数据隐私有强需求的用户（研究人员、开发者、分析师），特别是在离线环境或需要处理私有文档的场景 |
| **R - Result** | 研究任务从「多平台切换手动搜集」变成「一键自动深度研究 + 引用溯源」；SimpleQA ~95% 准确率；完全本地运行，零数据外传 |
| **I - Insight** | 通过 SQLCipher AES-256 加密隔离每个用户的数据库，实现真正的零知识隐私；LangGraph Agent Strategy 让 LLM 自适应选择搜索源而非固定管道 |
| **P - Proof** | 4,706 Stars、447 Forks、Docker Hub 活跃部署、20+ 研究策略、OpenSSF 安全评分 |

---

## P - Positioning（定位破题）

**一句话定义**：本地运行的 AI 驱动深度研究助手，支持多 LLM 和多搜索引擎，可构建加密知识库。

**场景锚定**：当你需要做学术研究、市场调研、技术调研时，通常需要在 Google Scholar、arXiv、PubMed、Wikipedia 之间来回切换，手动整理引用。而 Local Deep Research 把这个过程自动化了。

**差异化标签**：`privacy-first` + `agentic research` + `local-encrypted knowledge base`

---

## S - Sensation（体验式介绍）

使用 Local Deep Research 时，你的体验是这样的：

**第一步**：你问一个复杂问题，比如「过去三年 RISC-V 在数据中心的市场渗透率变化」

**第二步**：LDR 自动决定搜索哪些来源——它可能会选择 arXiv 找学术论文、Wikipedia 找历史数据、SerpAPI 抓取新闻报道。如果你的本地知识库里有相关文档，它也会一并检索。

**第三步**：研究结果以结构化报告形式呈现，每个论点都有原始来源的引用，点击即可溯源。

**关键体验点**：
- 你可以选择 `langgraph-agent` 策略，这是 Cursor Composer Self-Summarization 文章中提到的「模型自主决定搜索策略」理念的工程实现——LLM 自适应选择 specialized engines（arXiv、PubMed、Semantic Scholar 等）
- 每次研究找到的优质来源会自动下载到你的加密知识库，日积月累形成你自己的研究资产
- 完全本地运行意味着即使处理竞品分析等敏感内容，数据也不会离开你的机器

---

## E - Evidence（拆解验证）

### 技术深度

**多 LLM 支持**：Ollama、Google、Anthropic、OpenAI 等主流提供商，以及 Qwen 3.6 等本地模型。这意味着你可以在离线环境用量化后的 Qwen 跑出一个 SimpleQA ~95% 准确率的研究助手。

**20+ 研究策略**：包括 Quick Summary（30 秒到 3 分钟）、Detailed Research（综合分析）、Report Generation（专业报告）、Document Analysis（私有文档检索）等。

**LangGraph Agent Strategy**：
> "An autonomous agentic research mode where the LLM decides what to search, which specialized engines to use (arXiv, PubMed, Semantic Scholar, etc.), and when to synthesize. Early results are promising — it adaptively switches between search engines based on what it finds and collects significantly more sources than pipeline-based strategies."
> — [GitHub README](https://github.com/LearningCircuit/local-deep-research)

这与 Cursor Composer Self-Summarization 的「compaction-in-the-loop」思路形成对照：两者都在让模型学会更智能地管理信息流——Cursor 压缩 context，LDR 扩展搜索源的自适应选择。

**加密架构**：
> "Each user gets their own isolated SQLCipher database encrypted with AES-256 (Signal-level security). No password recovery means true zero-knowledge—even server admins can't read your data."
> — [GitHub README](https://github.com/LearningCircuit/local-deep-research)

### 安全体系

LDR 拥有我见过的最完整的安全扫描矩阵：

| 类别 | 工具 |
|------|------|
| 静态分析 | CodeQL、Semgrep、DevSkim、Bearer |
| 依赖/密钥扫描 | Gitleaks、OSV-Scanner、npm-audit、Retire.js |
| 容器安全 | Container Security、Dockle、Hadolint、Checkov |
| 工作流/运行时安全 | Zizmor、OWASP ZAP、Security Tests |
| Supply Chain | Docker 镜像 Cosign 签名 + SLSA provenance + SBOM |

> "Docker images are signed with Cosign, include SLSA provenance attestations, and attach SBOMs."
> — [GitHub README](https://github.com/LearningCircuit/local-deep-research)

### 社区健康度

| 指标 | 数值 |
|------|------|
| GitHub Stars | 4,706 |
| Forks | 447 |
| PyPI Downloads | 高活跃度 |
| Docker Pulls | 活跃部署 |
| 贡献者 | 持续增长 |
| 提交频率 | 月活跃 |

---

## T - Threshold（行动引导）

### 快速上手（Docker Compose）

```bash
# CPU-only（全平台）
curl -O https://raw.githubusercontent.com/LearningCircuit/local-deep-research/main/docker-compose.yml && docker compose up -d

# NVIDIA GPU（Linux）
curl -O https://raw.githubusercontent.com/LearningCircuit/local-deep-research/main/docker-compose.yml && \
curl -O https://raw.githubusercontent.com/LearningCircuit/local-deep-research/main/docker-compose.gpu.override.yml && \
docker compose -f docker-compose.yml -f docker-compose.gpu.override.yml up -d

# 访问
open http://localhost:5000  # 约30秒后启动
```

### 或 pip 安装

```bash
pip install local-deep-research
```

### 适合贡献的场景

- **研究策略开发**：20+ 策略还有扩展空间，可以为特定领域（金融、医疗、法律）定制研究管道
- **LangGraph Agent 优化**：当前是早期阶段，自适应搜索源选择有改进空间
- **知识库体验**：构建更丰富的本地文档分析能力
- **安全加固**：虽然已有业界最完整的安全扫描矩阵，但 in-memory credentials 的处理仍有优化空间（当前依赖 session-scoped lifetime 和 core dump exclusion）

---

## 关联主题

**关联 Articles**：本文与「Cursor Composer Self-Summarization：Compaction-in-the-Loop 强化学习」形成技术对照——两者都在处理长上下文场景下的信息管理问题，但角度互补：

| 维度 | Cursor Composer | Local Deep Research |
|------|----------------|-------------------|
| 问题域 | Agent context window 内的信息压缩 | 多源研究的信息获取与整合 |
| 核心创新 | 训练模型学会「压缩什么」 | 让 LLM 学会「搜索什么」 |
| 技术路线 | RL + compaction-in-the-loop | LangGraph Agent Strategy + 多引擎编排 |
| 隐私设计 | N/A（云端模型） | SQLCipher AES-256 本地加密 |

> 两者共同指向一个趋势：**未来的 Agent 系统需要让模型学会主动管理信息流，而不是依赖固定的工程流程**。

---

**引用来源**：

1. [LearningCircuit/local-deep-research - GitHub](https://github.com/LearningCircuit/local-deep-research)
2. [Local Deep Research Wiki](https://github.com/LearningCircuit/local-deep-research/wiki)
3. [LDR Benchmarks on Hugging Face](https://huggingface.co/datasets/local-deep-research/ldr-benchmarks)