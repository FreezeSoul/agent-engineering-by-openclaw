# LangChain 欧盟宏观经济研究 Agent：Deep Agents × LangSmith × You.com Finance API 的完整生产案例

> **一句话总结**：当 Deep Agents 接管欧盟 27 国 GDP 异常分析，**单次运行 $2.20 / 45 分钟 / 13 节报告 / 每个发现追溯到原始来源**——这就是「可解释 AI 在金融领域的工程范式」。

## 标签

- `deep-agents` / `langsmith` / `financial-research` / `subagent-orchestration` / `you-com-finance` / `case-study`

## 来源

- 原始博客：[Financial AI that Investigates Macro Trends: EU Economic Analysis with You.com and LangChain](https://www.langchain.com/blog/financial-ai-that-investigates-macro-trends-eu-economic-analysis-with-you-com-and-langchain)（Srimanth Tangedipalli, Karan Singh, Saurabh Sharma, Akhil Pothana，2026-05-20，18 min）
- 完整代码与报告：[GitHub Repository](https://github.com/langchain-ai/deepagents/tree/main/examples)
- 评分：4.5/5（实用性 ⭐⭐⭐⭐⭐ / 独特性 ⭐⭐⭐⭐ / 时效性 ⭐⭐⭐⭐）

---

## 为什么这件事重要

大多数人以为「AI 投顾」就是把 LLM 接到彭博终端——但 LangChain 这次和 You.com 的合作展示了一个**完全不同的范式**：

> **AI 投顾的核心不是"更快地分析数据"，而是"让分析过程可审计"**。当监管要求每个数字都能追到出处时，传统的 RAG 方案（直接给 LLM 一堆文档）是不够的——你需要一个**对每个数据点都有完整决策链**的 agent 系统。

这个案例的核心数据点（2025 GDP 全 EU-27 真实数据）：

| 维度 | 数字 |
|------|------|
| 覆盖国家 | 27 个 EU 成员国 |
| 运行成本 | $2.20 / 每次完整分析 |
| 运行时长 | ~45 分钟 |
| 输出结构 | 13 节标准报告 |
| 数据精度 | 87.29% FinSearchComp 公开基准 |
| 异常识别 | 爱尔兰 +12.3%（药品出口假象）vs 德国（汽车+建筑业崩盘）|
| 引用方式 | 每个发现 [[n]] 编号回溯到原始来源 |

这不是一个 demo——这是**生产级金融研究 agent 的完整参考实现**。

## 核心洞察

> **金融 AI 的真正难题不是"能不能用 LLM 分析财报"，而是"如何让 LLM 的分析结果通过合规审查"**。LangChain 的解法是：**让 LangSmith 捕获 agent 执行的每一步决策，包括每个 tool call、每个中间结果、每个引用源**——审计员可以从最终报告的任何一个数字反向追溯到「这是哪条 You.com API 在什么时间点返回的」。

这是「**白盒可解释性**」在金融领域的一次完整工程示范。

## 副观点 1：Deep Agents 的"5+1 Subagent"架构是研究型任务的标准范式

这个案例展示的子智能体结构**不是任意设计的**——它对应着宏观经济研究本身的层次：

```
1. landscape-scanner（总览扫描）
   ↓ 发现异常
2. country-investigator × N（每个异常国家一个实例，并行）
   ↓ 深入调查
3. sector-attributor（行业归因）
4. policy-tracker（政策追踪）
5. report-writer（最终报告生成）
+ 1 个 general-purpose subagent（兜底）
```

**关键工程取舍**：
- **Fan-out 模式**：country-investigator 不是循环生成，而是**对每个异常国家 spawn 一个独立实例**——失败隔离、并发执行、结果聚合都由 Deep Agents 处理
- **上下文隔离**：每个 subagent 只接收它需要的 context（避免 context pollution）
- **工具范围**：每个 subagent 只有一个工具——`you_finance_research`——这种「**窄工具 + 强推理**」的组合优于「宽工具 + 弱推理」

```python
@tool(parse_docstring=True)
async def you_finance_research(
    input: str,
    research_effort: Literal["deep", "exhaustive"] = "deep",
) -> str:
    """Research financial and macroeconomic topics with cited sources."""
    # Finance Research API 本身就是一个 multi-step agent
    # 这里把它包装为 Deep Agents 的 tool
    body = {"input": input, "research_effort": research_effort}
    headers = {
        "Content-Type": "application/json",
        "X-API-Key": os.environ["YDC_API_KEY"],
    }
    async with httpx.AsyncClient(timeout=HTTP_API_TIMEOUT) as client:
        response = await client.post(HTTP_ENDPOINT, headers=headers, json=body)
        data = response.json()
        output = data.get("output", {})
        content = output.get("content", "")
        sources = output.get("sources", [])
        result = content
        if sources:
            result += "\n\n### Sources\n"
            for i, src in enumerate(sources, 1):
                title = src.get("title", "Untitled")
                url = src.get("url", "")
                result += f"[[{i}]] {title}: {url}\n"
        return result
```

**两个值得注意的设计**：
1. **`research_effort` 是 budget 控制的关键**：focused query 拿满 budget 得到定量答案，overloaded query 分到薄 budget 只得定性答案。Agent 的 system prompt 必须知道这一点。
2. **`read=None` timeout 是 deliberate**：复杂查询可能要好几分钟，不能因为 timeout 杀死关键任务。

## 副观点 2：You.com Finance Research API 的"Agent-as-Tool"模式

这个案例展示了一种**正在快速普及的范式**：

> **把一个 multi-step research agent 包装成一个单一 tool**——这个 tool 接收复杂查询、运行多步推理、返回带 [[n]] 引用标签的答案。然后上层 agent 把这个 tool 当作"超级研究助理"使用。

```
[Deep Agents Layer]
   ↓ 调用 you_finance_research (LangChain tool)
[You.com Finance Research API Layer]
   ├── 数据检索（World Bank / IMF / OECD / Eurostat / FRED）
   ├── 私有数据（S&P Global 等授权数据）
   ├── 多分支并行验证
   └── 返回带 [[n]] 标签的答案
```

**这种分层的优势**：
- **职责清晰**：上层 agent 负责 orchestration / planning / reporting；下层 agent 负责 deep research / data retrieval / citation
- **成本可控**：每个 tool call 是 discrete unit cost，不会因为 deep dive 失控
- **可替换**：可以通过 MCP 直接调用 You.com 的 hosted server（`https://api.you.com/mcp?tools=you-finance`），用 `langchain-mcp-adapters` 替换直接 HTTP 调用

**LangSmith 的"trace-as-audit-trail"是这个模式成立的前提**：

> 监管要求每个数据点可追溯 → agent 必须记录每个 tool call、每个 response、每个中间结果 → LangSmith 把这些**全部 capture 为可检索 trace** → 审计员从最终报告反向追溯到原始数据

## 副观点 3：Budget 模型决定 Agent 怎么写 Prompt

You.com Finance API 的 budget 模型给了我们一个**对所有 agent 架构都适用的教训**：

| Query 形态 | Budget 分配 | 结果质量 | 适用场景 |
|-----------|-----------|---------|---------|
| Focused（一个实体 + 一个分析问题）| 满 | 丰富、定量 | 深度分析 |
| Overloaded（多实体 + 多维度）| 分摊 | 薄、定性 | ❌ 应该拆分 |
| Data-retrieval（多实体 + 简单数据点）| 单价低 | 完整数据 | ✅ 可以批量 |

**这意味着 agent 的 prompt 工程必须理解下层 API 的 budget 模型**——盲目「一个 call 解决所有问题」会得到最差的结果。

**正确的模式**（在这个案例中体现）：
- **单点深挖**：一个国家、一个分析维度 → 一次 focused call → 详细定量结果
- **批量扫描**：所有国家、单一数据点 → 一次 overloaded call → 完整 GDP 表
- **避免**：所有国家、所有维度 → 一次 call → 薄定性输出

## 副观点 4：LangSmith Deployment 让 Local Dev = Production

这个案例有个**容易被忽视但工程上极重要**的细节：

> **同一个 agent 在本地开发环境和生产环境无需任何代码改动**——LangSmith Deployment 处理 scaling、persistent storage（StoreBackend）、environment management。

这是「**agent 工程化**」和「**agent demo**」的本质区别：

| 维度 | Demo Agent | 生产 Agent（这个案例）|
|------|------------|---------------------|
| 状态持久化 | 内存 dict | StoreBackend（pluggable）|
| 部署方式 | `python main.py` | LangSmith Deployment 自动 scaling |
| 上下文管理 | 手动管理 | Backends + Skills + File system |
| 工具安全 | 直接调用 | Scoped per subagent |
| 观测性 | print debugging | LangSmith trace + JSON export + MCP 查询 |

**最大的工程价值**：把"研究型 agent 部署到生产"从 1 个月的工程量压缩到 1 天——因为 LangSmith 接管了 scaling / persistence / observability 这三个传统上最耗时的工作。

## 核心发现的具体证据

这个案例最大的价值是**展示了真实数据**——不是合成数据，而是 2025 年 EU-27 GDP 实际数据：

### 爱尔兰 +12.3%：药品出口假象

```
Agent 输出：
- Ireland 12.3% GDP growth → 表面繁荣
- 深入调查：pharma-led export surge 前置到 US 关税前
- 工业部门单独贡献 +6.55pp
- Modified GNI 显示实际增长更温和

Agent 做了什么：
1. 调用 landscape-scanner 发现爱尔兰异常
2. Spawn country-investigator（爱尔兰专用）
3. country-investigator 调用 you_finance_research 询问"爱尔兰 12.3% 的产业归因"
4. 调用 sector-attributor 验证制药业贡献
5. 调用 policy-tracker 检查关税时间线
6. report-writer 整合所有发现
```

### 德国：不是周期性而是结构性

```
Agent 区分了"周期性收缩" vs "结构性收缩"：
- 汽车业暴露（中国竞争）
- 建筑业崩盘（高利率滞后）
- 这不是「暂时的」，是「结构性问题」
```

### 共同主线

```
滞后国家共同主线：
- 暴露于 US 关税
- 中国制造业竞争
- 建筑业高利率滞后

跑赢国家共同主线：
- 实际工资复苏（西班牙、波兰）
- EU 基金拨付（保加利亚、克罗地亚）
```

**所有这些发现的 citation 都通过 LangSmith trace 完整保留**——任何审计员都可以从「爱尔兰制药出口」这个发现追到 `you_finance_research` 的某一次具体 API call。

## 为什么这个案例是 2026 年 Agent 工程化的范式

我们过去一年看了太多"AI 投顾"、"AI 研究员"的 demo——绝大多数是**用 LLM 总结新闻**的薄包装。LangChain 这个案例展示的**是另一回事**：

| 维度 | 普通 AI 投顾 Demo | 这个案例 |
|------|-----------------|---------|
| 数据源 | 公开网页摘要 | 授权私有数据（S&P Global）+ 公开数据（World Bank / IMF / OECD）|
| 分析深度 | 表面总结 | 27 国 × 多维度 deep dive |
| 可解释性 | "AI 这样说的" | 每个数字 [[n]] 引用回源 |
| 成本 | 不透明 | $2.20 / 45 分钟 |
| 部署 | 一次性脚本 | LangSmith Deployment 托管 |
| 审计 | 不可能 | 完整 trace 可追溯 |

**这是 2026 年 5 月的 production-grade financial research agent**——不是 research paper，不是 demo，是**正在 LangSmith 平台上运行的真实工作流**。

## 对 Agent 工程师的具体启示

1. **不要试图用单个 agent 做完整研究任务**——这个案例的 5+1 subagent 架构对应研究任务的**自然层次**
2. **把 multi-step research API 包装为单一 tool**——Agent-as-Tool 是构建大型 agent 系统的标准模式
3. **理解下层 API 的 budget 模型**——Agent 的 prompt 工程必须考虑 cost / latency / quality 的 trade-off
4. **可观测性不是 optional**——金融 / 医疗 / 法律领域的 agent 必须有完整 trace，否则无法过合规
5. **local dev = production** 是工程化的分水岭——LangSmith Deployment / Vellum / Lindy 都在朝这个方向演进

## 关联阅读

- **langchain-ai/deepagents**（23,434 Stars）——本案例使用的 harness 实现
- **LangSmith Engine** ——本案例使用的观测/部署平台
- **You.com Finance Research API** ——本案例使用的下层研究 agent
- **OpenAI self-improving tax agents with Codex** ——类似的「agent 用生产数据自我改进」案例

---

*本文是「Deep Agents × LangSmith」系列在金融领域的具体案例分析，展示了 subagent 编排 + 工具抽象 + 可观测性 三者如何组合成 production-grade 系统。*
