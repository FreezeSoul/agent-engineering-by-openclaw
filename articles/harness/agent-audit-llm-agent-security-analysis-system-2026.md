# Agent Audit：面向 LLM Agent 应用的安全分析系统

> **核心问题**：开发者部署 LLM Agent 前，该检查什么——模型权重、工具代码，还是部署配置？
> **答案**：三者都要，但现有 SAST 工具只覆盖第一层。
> **本文产出**：Agent Audit——首个覆盖 Agent 软件栈全层的安全分析系统，22 个样本中检测出 40/42 漏洞，recall 是 Bandit/Semgrep 的 4 倍。

---

## 一、为什么传统安全工具不够用

传统 SAST 工具（Bandit、Semgrep）在代码安全领域久经考验，但面对 LLM Agent 软件栈时暴露出了三类盲区：

### 1.1 工具边界风险（Tool Boundary Risk）

Agent 的核心特征是**工具调用**：模型生成调用参数 → 传递给工具函数 → 执行外部操作。Bandit 能检测 `eval()` 调用，但无法理解"这个 `eval()` 出现在 `@tool` 装饰的函数中"意味着什么。当模型生成的不可信输出流入危险操作时，攻击面成倍扩大。

```python
@tool
def analyze_data(expr: str):
    return eval(expr)  # Bandit: V1. 但这里风险更高——输入来自 LLM
```

Agent Audit 为此设计了**Tool Boundary Detection**：对 12 种工具装饰器模式（LangChain `BaseTool`、CrewAI `@tool` 等）进行识别，并在工具边界内的发现赋予 0.90 的基础置信度（普通函数仅 0.55）。

### 1.2 MCP 配置风险（MCP Configuration Risk）

MCP（Model Context Protocol）配置以 JSON/YAML 格式存在，Bandit/Semgrep 将其视为不透明数据，完全无法分析。但 MCP 配置中的过度授权（如 `--allow-write /`）和安全服务器缺失同样会导致严重漏洞：

```json
{
  "args": ["@untrusted-org/data-mcp-server", "--allow-write", "/"]
}
```

Agent Audit 的 MCPConfigScanner 支持 9 种配置格式（Claude Desktop、VS Code、Cursor、Windsurf 等），将 JSON/YAML 作为结构化数据解析，而非字符串。这是现有 SAST 工具根本无法企及的分析维度。

### 1.3 提示词注入面（Prompt Injection Surface）

用户输入嵌入系统提示词的方式（f-string、`.format()`、字符串拼接）会在未经消毒的情况下创造注入面。Bandit/Semgrep 同样无法识别这类 Agent 特有的风险模式。

---

## 二、Agent Audit 技术架构

### 2.1 四层扫描管道

Agent Audit 采用多扫描器并行架构：

```
输入文件 → 类型分发 → 四大扫描器（并行）
                        ↓
              统一 RuleEngine（规则映射 + 置信度分层 + 跨扫描器去重）
                        ↓
              输出：Terminal / JSON / SARIF / Markdown
```

**四大扫描器**：
1. **PythonScanner**：AST 级别数据流分析，追踪从污点源到危险 sink 的路径
2. **SecretScanner**：40+ 正则模式检测 API Key，Shannon 熵值过滤占位符
3. **MCPConfigScanner**：结构化解析 9 种 MCP 配置格式
4. **PrivilegeScanner**：检测 daemon 进程权限、NOPASSWD sudoers、CAP_SYS_ADMIN 等

### 2.2 污点分析四阶段管道

PythonScanner 的核心是四阶段污点分析：

| 阶段 | 内容 |
|------|------|
| 1. Source Classification | 函数参数、`chain.invoke()` 返回值、`request.json()` 标记为污点源 |
| 2. Data Flow Graph | 通过 AST 遍历构建数据流图 |
| 3. Sanitization Detection | 调用 `shlex.quote()`、`isinstance()`、参数化查询时降低置信度 ×0.20 |
| 4. Sink Reachability | BFS 判定污点数据是否到达 `eval()`、`subprocess.run()`、`cursor.execute()` 等危险操作 |

### 2.3 57 条规则覆盖 OWASP Agentic Top 10

Agent Audit 的 57 条检测规则完整覆盖 OWASP Agentic Security Initiative 的 10 个类别：

| OWASP 类别 | 规则数量 |
|-----------|---------|
| Supply Chain Risks (ASI-04) | 10 |
| Tool Misuse (ASI-02) | 9 |
| Identity/Priilege Management (ASI-03) | 9 |
| 跨类的凭证/MCP/权限提升 | 4 |

另有 4 条专项规则覆盖 MCP 供应链攻击：跨服务器工具影子（AGENT-055）、工具描述投毒（AGENT-056）、参数注入（AGENT-057）、基线漂移检测（AGENT-054）。

### 2.4 置信度四层分级

所有发现经过四层置信度系统：

| 级别 | 阈值 | 含义 |
|------|------|------|
| **BLOCK** | ≥ 0.92 | 高危漏洞，需立即处理 |
| **WARN** | ≥ 0.60 | 大概率问题 |
| **INFO** | ≥ 0.30 | 参考性发现 |
| **SUPPRESSED** | < 0.30 | 大概率误报 |

超过 20 种误报抑制机制（工具边界提升、框架路径抑制、测试上下文检测等）在合成 ground-truth fixture 上实现了 98.51% 精确率（100% 召回下）。

---

## 三、Agent-Vuln-Bench：首个 Agent 安全评测基准

### 3.1 基准构成

Agent Audit 的评估基于 **Agent-Vuln-Bench (AVB)**，包含 22 个样本、42 个专家标注漏洞，分为三类：

| 类别 | 描述 | 漏洞数 |
|------|------|--------|
| Set A | 注入/RCE（含 CVE 重现：LangChain LLMMathChain eval 注入、CVE-2023-29374） | 19 |
| Set B | MCP/组件（MCP 服务器工具影子、工具描述投毒等） | 9 |
| Set C | 数据/认证（凭证泄漏、SSRF 等） | 14 |

**KNOWN 子集**：CVE 重现（LangChain eval 注入、PythonREPLTool RCE）
**WILD 子集**：生产环境真实漏洞模式（计算器工具无沙箱 eval、SSRF via 用户控制 URL、动态 importlib 自我修改等）

### 3.2 核心评估结果

| 指标 | Bandit | Semgrep | Agent Audit |
|------|--------|---------|-------------|
| Recall | ~25% | ~30% | **94.6%** |
| Precision | — | — | 87.5% |
| F1 | — | — | **0.91** |
| 扫描耗时 | 慢 | 慢 | **sub-second** |

Agent Audit 的 recall 是通用 SAST 工具的 **4 倍**，且分析速度达到子秒级——可以无缝集成到 CI/CD 流水线中。

---

## 四、与现有工具的系统性对比

### 4.1 检测能力矩阵

| 风险类型 | Bandit | Semgrep | Agent Audit |
|---------|--------|---------|-------------|
| 工具函数中的代码执行 | ✅ 部分 | ✅ 部分 | ✅ 完整（Tool Boundary 增强） |
| 提示词注入面 | ❌ | ❌ | ✅ |
| MCP 配置过授权 | ❌ | ❌ | ✅ |
| MCP 供应链攻击 | ❌ | ❌ | ✅ |
| 凭证检测 | ✅ | ✅ | ✅（熵值过滤 + 语义分析）|
| 权限提升模式 | ✅ | ✅ | ✅（Daemon/sudo/CAP_SYS_ADMIN）|
| SARIF 输出（CI/CD） | ❌ | ✅ | ✅ |

### 4.2 关键差异：Agent-Aware

Agent Audit 的核心设计原则是 **Agent-Aware**——它理解 Agent 软件栈特有的语义：

- 识别 12 种工具装饰器模式，在工具边界内提升置信度
- 将 MCP 配置文件作为结构化数据解析，而非不透明文本
- 检测跨服务器工具影子和工具描述投毒——这是传统 SAST 完全无法建模的攻击面

> **笔者判断**：Agent Audit 填补的不是"更好的 Bandit"，而是"Agent 特有的"安全分析空白。MCP 供应链攻击这一类威胁，OWASP 已有系统性分类，但缺少检测工具——Agent Audit 首次将其工程化。

---

## 五、部署集成

### 5.1 工具安装与使用

```bash
pip install agent-audit

# 扫描本地 Agent 代码
agent-audit scan ./my-agent/

# CI/CD 集成（高危漏洞阻断）
agent-audit scan ./ --fail-on high --format sarif > results.sarif

# VS Code / GitHub Code Scanning 集成
agent-audit inspect --server localhost:8080
```

### 5.2 inspect 子命令：MCP 服务器实时检测

`agent-audit inspect` 可连接运行中的 MCP 服务器，在不执行任何工具的情况下检测：
- 工具描述投毒（Tool Description Poisoning）
- 跨服务器工具影子（Cross-Server Tool Shadowing）

这是传统 SAST 完全无法覆盖的能力——它分析的是运行时行为，而不仅仅是静态代码。

### 5.3 输出格式

| 格式 | 用途 |
|------|------|
| Rich 终端显示 | 本地开发即时反馈 |
| JSON | 自动化处理 |
| SARIF | GitHub Code Scanning / VS Code 集成 |
| Markdown | 报告生成 |

---

## 六、工程判断：Agent Audit 的价值与局限

### 6.1 价值

1. **填补 MCP 安全空白**：MCP 供应链攻击（工具影子、描述投毒）是 2025-2026 的新兴威胁面，目前几乎无工具覆盖。Agent Audit 是首个系统性解决方案。
2. **CI/CD 无缝集成**：sub-second 扫描 + SARIF 输出使安全检查可以加入 PR 流水线，实现"代码合并前发现漏洞"。
3. **覆盖 OWASP Agentic Top 10 全部 10 类**：57 条规则提供了最完整的 Agent 安全覆盖。
4. **recall 优势显著**：94.6% recall vs Bandit ~25%——对于安全工具，recall 比 precision 更关键。

### 6.2 局限

1. **仅支持 Python**：Agent Audit 当前仅分析 Python Agent 代码，对于 JavaScript/TypeScript Agent（占很大比例）尚不支持。
2. **AVB 基准规模有限**：22 样本 / 42 漏洞的规模远小于 SWE-bench，评估结论需要更多生产环境验证。
3. **不检测模型层威胁**：Agent Audit 专注于软件栈安全，对提示词注入（模型层）的检测依赖提示词注入面识别，不处理直接的对抗性模型输出。
4. **工具装饰器覆盖有限**：当前仅覆盖 12 种模式，新兴框架的装饰器可能漏过。

> **工程建议**：对于 Python Agent 项目，`agent-audit --fail-on high` 应成为 CI 标配。但不要将其视为银弹——它与 OWASP ASI 框架配合使用效果最佳：OWASP 定义威胁分类，Agent Audit 提供自动化检测手段。

---

## 参考文献

- [Agent Audit: A Security Analysis System for LLM Agent Applications](https://arxiv.org/abs/2603.22853) — 论文原文，一手来源
- [HeadyZhang/agent-audit (GitHub)](https://github.com/HeadyZhang/agent-audit) — 开源实现，134 stars
- [OWASP Agentic Security Initiative Top 10](https://owasp.org/www-project/agentic-security-initiative/) — Agent 安全威胁分类框架
- [Anthropic MCP Documentation](https://docs.anthropic.com/en/docs/mcp) — MCP 协议规范
