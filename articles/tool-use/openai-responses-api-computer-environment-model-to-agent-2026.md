# 从模型到 Agent：OpenAI Responses API 的 Computer Environment 工程解析

**核心论点**：模型本身只是"建议者"，真正的 Agent 能力来自 computer environment 提供的那一层执行环——shell tool、filesystem、database、network 访问加上 context compaction，构成了从"能说"到"能做"的关键一跳。

---

## 一、问题：模型为何不能自己执行？

传统的模型调用范式是：**模型输出 → 开发者解析 → 手动执行**。这意味着模型只能"建议"，不能"行动"。

OpenAI 在工程实践中发现了几个具体问题：

> "A few practical problems emerge when you try to build agents: where to put intermediate files, how to avoid pasting large tables into a prompt, how to give the workflow network access without creating a security headache, and how to handle timeouts and retries without building a workflow system yourself."
>
> — OpenAI Engineering Blog, "From model to agent"

这四个问题精确地描述了从模型到 Agent 的工程 Gap：

| 问题 | 本质 | 常见错误做法 |
|------|------|------------|
| 中间文件放哪？ | 状态管理 | 往 prompt 里塞 Base64 |
| 大表格怎么处理？ | 上下文溢出 | 分片截断，丢失完整性 |
| 网络访问怎么做？ | 安全边界 | 直接给容器越权访问 |
| 超时重试谁处理？ | 可靠性工程 | 开发者自己写 harness |

笔者的判断是：**这四个问题不是"用更好的 Prompt"能解决的**，它们需要的是一层基础设施——computer environment。

---

## 二、Computer Environment 的五层架构

OpenAI 的 Responses API 通过 hosted container workspace 提供了一套完整的 computer environment，分为五层：

### 2.1 Shell Tool：让模型"能做"的第一步

Shell tool 是整个系统的执行接口。与 Code Interpreter（只能跑 Python）不同，shell tool 提供的是完整的 Unix 命令行环境：

```bash
# 模型可以执行的典型操作
grep -r "function" ./src/           # 搜索代码
curl -X POST https://api.example.com/data  # 调用外部 API
awk '{sum+=$2} END {print sum}' data.csv   # 数据处理
```

模型在训练阶段学会的是"propose 工具调用"，而 shell tool 让这个 propose 变成了真实可执行的命令。**这是模型到 Agent 最关键的一跳**：模型不只是输出文本，而是输出可执行的 shell 命令。

> "When we say 'using a tool', we mean the model actually only proposes a tool call. It can't execute the call on its own."
> — OpenAI Engineering Blog

笔者认为，这个设计洞察非常重要：**工具执行和工具选择必须解耦**。模型负责"判断用什么"，执行层负责"真的做"。这比让模型直接拥有执行权限更安全、更可控。

### 2.2 Agent Loop 编排：Responses API 作为 Orchestrator

单个 shell 命令没用，真正的 Agent 能力来自循环：

```
模型 propose → API 执行 → 结果回流 → 模型 propose → ...
```

Responses API 的编排机制：
1. 模型决定下一步 action（shell 命令或最终答案）
2. 若选择 shell，API 将命令转发给 container runtime
3. Container streaming 输出 → API 实时回流给模型
4. 模型在下一轮 context 中看到输出，决定后续动作
5. 循环直到模型输出不含 shell 命令

**并发执行**是另一个重要特性：

```python
# 模型可以在单轮中提出多个 shell 命令
# Responses API 并发执行，返回 multiplexed 结果
{
  "commands": ["ls -la", "git status", "curl api/data"],
  "concurrent": true  # 三个 session 并行
}
```

笔者认为，**并发是 agent loop 效率的关键**。如果每个命令必须串行执行，agent 的速度会被最慢的命令拖累。OpenAI 在这里的设计是正确的。

**Output Cap**：另一个工程细节是 output boundedness。模型可以为每个命令指定输出上限，API 保证首尾内容保留，中间截断。这防止了大文件扫描等场景把 context 撑爆。

> "The model specifies an output cap per command. The Responses API enforces that cap and returns a bounded result that preserves both the beginning and end of the output, while marking omitted content."
> — OpenAI Engineering Blog

### 2.3 Context Compaction：让长任务不崩溃

长任务是 agent 的典型场景，但 context window 是有限的。OpenAI 的解法是**服务端压缩**（server-side compaction）：

```python
# 工作机制
original_context = [用户请求, 10轮tool调用, 中间结果...]
↓ 模型生成压缩表示
compacted = "用户在处理订单流程，已完成：身份验证✓、库存查询✓、支付接口✓"
next_context = [compacted_item, 高价值片段, 新请求]
```

关键设计点：
- **触发阈值可配置**：开发者设置 context 剩余多少时触发压缩
- **模型原生训练**：压缩逻辑不是规则引擎，是模型自己学会的
- **加密传输**：压缩结果 token-efficient 且模型无法反向解读原始内容
- **Codex 自举**：OpenAI 让 Codex 自己用 compaction 系统，两套 Codex instance 互相调查 bug

> "When one Codex instance hit a compaction error, we'd spin up a second instance to investigate. The result was that Codex got a native, effective compaction system just by working on the problem."
> — OpenAI Engineering Blog

笔者认为这段描述非常有意思——Codex 作为自己的测试者，这本身就是一种 harness 工程的体现。

### 2.4 Container Context：三层资源抽象

Container 不仅是"执行环境"，还是"工作区状态"的载体，提供三层资源：

#### Filesystem

模型看到的是一个有组织的文件系统，而不是把所有文件内容塞进 prompt：

```bash
# 错误做法：把所有输入塞进 prompt
prompt = "data.csv 内容如下：\n" + open('data.csv').read()

# 正确做法：文件驻留在 container，模型用 shell 命令按需访问
# 模型执行：cat data.csv | head -20
# 模型执行：wc -l data.csv
```

> "A common anti-pattern is packing all input directly into prompt context. As inputs grow, overfilling the prompt becomes expensive and hard for the model to navigate. A better pattern is to stage resources in the container file system and let the model decide what to open, parse, or transform with shell commands."
> — OpenAI Engineering Blog

#### Database（SQLite）

结构化数据放 SQLite，模型按需 SQL 查询：

```sql
-- 模型分析："哪些产品本季度销售额下降？"
SELECT product_name, revenue_q2, revenue_q1, (revenue_q2-revenue_q1) as delta
FROM sales
WHERE delta < 0
ORDER BY delta ASC;
```

这比把整个 spreadsheet 塞进 prompt 要**快、便宜、可扩展**。

#### Network Access（Egress Proxy）

这是最敏感的部分——agent 需要网络访问，但不能是裸奔。OpenAI 用 **sidecar egress proxy** 解决：

```
Container → Egress Proxy（policy layer）→ 外部网络
              ↓
         allowlist + secret injection
         (模型只看到 placeholder)
```

Secret injection 的设计很巧妙：**模型和 container 只能看到占位符**（如 `{{SECRET_API_KEY}}`），真实密钥在 egress 层根据目标域名动态注入。这比把密钥放在 environment variable 然后祈祷模型不泄漏要安全得多。

### 2.5 Agent Skills：可复用工作流的标准化

重复性任务的 Agent 每次都要重新学习工作流，Skills 就是来解决这个问题的：

```yaml
# SKILL.md 结构
name: "invoice-processor"
description: "从邮件提取发票数据并录入系统"
resources:
  - api_spec.yaml
  - ui_template.json
scripts:
  - extract_invoice.sh
  - validate_data.py
  - submit_to_erp.py
```

Skill 的加载流程：

```
开发者上传 skill bundle（版本化管理）
                    ↓
Responses API 在模型推理前：
  1. 获取 skill metadata（名称、描述）
  2. 下载 bundle → 解压到 container
  3. 将 skill 路径和 metadata 加入 model context
                    ↓
模型在需要时：
  - shell 命令探索 skill 文件（ls, cat）
  - 读取 instructions
  - 执行 skill scripts
```

> "Agents have to rediscover the workflow each run—replanning, reissuing commands, and relearning conventions—leading to inconsistent results and wasted execution."
> — OpenAI Engineering Blog

笔者认为这句话点出了 skills 的核心价值：**把 workflow 从"每次重新发现"变成"按需复用"**。这是 Agent 工程化的关键一步。

---

## 三、整体系统视图

```
┌─────────────────────────────────────────────────────────────────┐
│                     Developer Prompt                            │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                     Responses API                               │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────┐  │
│  │ Orchestrator │  │  Compaction  │  │   Skill Loader       │  │
│  └──────────────┘  └──────────────┘  └──────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
                              │
         ┌────────────────────┼────────────────────┐
         ▼                    ▼                    ▼
┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐
│   Shell Tool    │  │  Shell Tool     │  │  Shell Tool     │
│   (Session 1)   │  │  (Session 2)    │  │  (Session 3)    │
│   ls -la        │  │  git status     │  │  curl api/data  │
└────────┬────────┘  └────────┬────────┘  └────────┬────────┘
         │                    │                    │
         └────────────────────┼────────────────────┘
                              ▼
              ┌───────────────────────────────┐
              │   Hosted Container Workspace  │
              │  ┌─────────┐  ┌────────────┐  │
              │  │Filesystem│  │  SQLite    │  │
              │  │         │  │  Database  │  │
              │  └─────────┘  └────────────┘  │
              │         │                     │
              │         ▼                     │
              │  ┌─────────────────────────┐  │
              │  │   Egress Proxy          │  │
              │  │   (allowlist + secrets) │  │
              │  └─────────────────────────┘  │
              └───────────────────────────────┘
```

**笔者的核心判断**：这个架构的精妙之处在于**每一层都是可选的、可组合的**。你可以只用 shell tool 做简单任务，也可以加上 skills 做复杂 workflow，再加上 compaction 做长程任务。层次之间是**正交的设计**，不是捆绑销售。

---

## 四、与传统 Agent 框架的关键区别

| 维度 | 传统 Agent 框架（如 LangChain Agent）| OpenAI Responses API |
|------|--------------------------------------|---------------------|
| **执行环境** | 开发者自己搭 harness | 平台原生提供 |
| **Tool 定义** | Python function + schema | Shell command + output cap |
| **Context 管理** | 开发者手动处理 | 服务端 compaction 原生支持 |
| **网络访问** | 开发者自己管安全 | Egress proxy + secret injection |
| **Workflow 复用** | 无标准格式 | Skill bundle（SKILL.md 格式）|
| **长任务支持** | 依赖模型 context window | Compaction + checkpoint 机制 |

笔者认为，OpenAI 的核心优势在于**把 harness 工程做成了平台能力**，而不是让每个开发者自己造轮子。这也是为什么"用 OpenAI 的 Responses API"比自己用 GPT-4 API 搭 Agent 系统在工程上更靠谱的原因。

---

## 五、工程的本质：为什么这个架构值得研究？

回到本文的核心论点：**Computer Environment 是从模型到 Agent 的那一层缺失的基础设施**。

很多人以为把模型加一个 function calling 能力就是 Agent 了。但 function calling 只是"建议用什么工具"，真正的 Agent 还需要：

1. **执行层**：工具能被真的执行（shell tool）
2. **状态层**：执行结果能持久化、能按需查询（filesystem + database）
3. **安全层**：网络访问能被管控（egress proxy）
4. **长程层**：长任务不因 context 溢出而崩溃（compaction）
5. **复用层**：好用的 workflow 能被封装（skills）

这五层缺少任何一层，Agent 都只能在"玩具场景"下工作，无法进入生产环境。

OpenAI Responses API 的价值，不是他们"发明"了这五层，而是他们**第一次把这五层做成了统一平台体验**，让开发者不需要自己拼凑 harness。

---

## 附：三个备选标题

1. **从模型到 Agent：OpenAI Responses API 的执行环设计** — 策略：好奇心缺口（直接点出核心转变）
2. **OpenAI 的 Computer Environment：Agent 工程的基础设施解法** — 策略：数据冲击（"基础设施"这个词暗示工程严肃性）
3. **为什么你的 Agent 只能"说"不能"做"？** — 策略：痛点共鸣（反问句引发共鸣）

---

*来源：[OpenAI Engineering Blog - From model to agent: Equipping the Responses API with a computer environment](https://openai.com/index/equip-responses-api-computer-environment/)*