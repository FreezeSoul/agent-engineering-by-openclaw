# EvalView：AI Agent 的行为回归门卫

**T - Target 用户画像**：
- 正在将 AI Agent 集成到生产系统的工程师/SRE
- 团队规模 1-10 人，没有专职 AI 测试团队
- 已有基础的 Agent 跑起来，但担心「上线后不知道什么时候悄悄变差了」

**R - Result 核心成果**：
- 从「健康检查通过 → 功能正常」升级到「健康检查通过 → 行为未退化」
- 将「provider 变更」和「系统回归」区分开来，避免误报导致的空焦虑
- 实际价值：避免在 model upgrade 后收到用户投诉才知道出了问题

---

## 定位破题（Positioning）

**一句话定义**：像 Playwright 一样做 Agent 的行为回归测试，但测的不是 UI，而是 tool calls 和 multi-turn 对话轨迹。

**场景锚定**：当你需要回答「这个 model/prompt/config 变更有没有影响现有 Agent 行为」时，EvalView 是你 CI/CD 里的那道 gate。

**差异化标签**：`silent regression detector` — 专门抓「返回 200 但答案错了」这类传统测试漏掉的坑。

---

## 体验式介绍（Sensation）

想象你刚升级了 Claude 3.7，CI 显示绿色，一切正常。三天后用户反馈「客服 Agent 开始跳过核保步骤了」。你回查日志发现：tool calling 顺序变了，但返回格式完全正确，HTTP 200。

EvalView 解决的就是这个：

```
✓ login-flow PASSED
⚠ refund-request TOOLS_CHANGED
 - lookup_order → check_policy → process_refund
 + lookup_order → check_policy → process_refund → escalate_to_human
✗ billing-dispute REGRESSION -30 pts
Score: 85 → 55 Output similarity: 35%
```

**这就是你 CI 里缺失的那层防护**。不是测「Agent 跑不跑得起来」，而是测「跑起来之后做的事对不对」。

---

## 拆解验证（Evidence）

### 技术深度

EvalView 的核心设计是 **snapshot behavior → diff → classify** 三步循环：

1. **Snapshot**：用 `evalview snapshot` 记录当前 Agent 的行为基准（tool calls 顺序、多轮对话轨迹、输出指纹）
2. **Diff**：用 `evalview check` 检测变更后的行为偏差
3. **Classify**：将偏差归类为 `TOOLS_CHANGED`（可能是 prompt 调整）、`REGRESSION`（真的变差了）、`improved`（正向变化）

> "Traditional tests tell you if your agent is up. EvalView tells you if it still behaves correctly."
> — [EvalView README](https://github.com/hidai25/eval-view)

**关键工程决策**：detector + classifier 的分离设计。检测是确定性的（diff），分类是带置信度的（LLM judgment）。这样既能避免过度依赖 LLM 做 binary decision，又能保留 LLM 在复杂场景下的判断能力。

### 分级 Verdict 机制

四档输出：SAFE_TO_SHIP / SHIP_WITH_QUARANTINE / INVESTIGATE / BLOCK_RELEASE

```python
VERDICT: 🛑 BLOCK RELEASE

 • 1 regression: billing-dispute
 • 1 test changed behavior: refund-request
 • Cost up 14% vs baseline

Likely cause & next actions:
 1. Rerun statistically to distinguish flake from real drift
 2. Review tool descriptions for: escalate_to_human
```

这个设计让「要不要发版」的决策清晰化，而不是只有 pass/fail 两个极端。

### 多框架兼容

> "Works with LangGraph, CrewAI, OpenAI, Anthropic."
> — [EvalView README](https://github.com/hidai25/eval-view)

支持主流 Agent 框架，这意味着不需要为了用 EvalView 而换掉现有技术栈。

### Model Drift Detection

**这可能是最有价值的功能**：不用跑完整的 Agent 测试，直接测 model 本身的行为一致性。

```bash
evalview model-check --model claude-opus-4-5-20251101
# 第一次运行保存 baseline
# 下周运行检测是否有任何变化
```

这解决了一个实际问题：Anthropic 发布 Claude 更新时，你不知道你的 Agent 会不会受影响。EvalView 的 canary suite 可以提前告诉你。

### 社区健康度

GitHub 上有明确的 CI 状态 badge 和 contributors 活跃度，虽然没有公布具体 star 数量（从搜索结果看相对小众），但 issues 和 PR 的响应速度表明这是一个有维护者活跃更新的项目。

---

## 行动引导（Threshold）

### 快速上手（3 步）

```bash
pip install evalview
evalview init   # 自动检测 Agent 类型，配置 starter suite
evalview snapshot  # 保存当前行为基准
evalview check    # 变更后检测回归
```

### 适合的贡献场景

- 发现 bug → 提 issue + 附上 replay trace
- 有新的 Agent 框架集成需求 → 提 PR
- 觉得 verdict 分类不准 → 提供 case 给 maintainer

### 路线图价值

如果你的团队正在做 Agent 上生产，EvalView 是值得 watch 的项目——随着 Agent 在生产环境中的普及，行为回归测试会成为标配，而 EvalView 可能是这个领域最专注的工具。

---

## 关联性说明

**为何与「Anthropic Long-Running Agent Harness」形成关联？**

Anthropic 的双组件架构（Initializer Agent + Coding Agent）本质上在 Session 级别建立了一种隐性的质量保障机制——每个 Coding Agent 结束前必须留下「clean state」和「描述性 commit」，这让下一个 Agent 能快速定位问题。

EvalView 提供的则是**独立于 Agent 内部逻辑的显式行为验证层**：即使 Harness 设计再好，外部依赖（model 版本、API provider 配置）变化仍然可能导致行为漂移。EvalView 的 snapshot + diff + classify 循环，提供了一层与具体实现无关的防御机制。

两者形成互补：**Harness 设计保证 Agent 实现的可维护性，EvalView 保证 Agent 行为的一致性**。

---

**引用来源**

- [EvalView GitHub Repository](https://github.com/hidai25/eval-view)（项目 README，含核心功能描述）
- [EvalView PyPI Package](https://pypi.org/project/evalview/)（安装方式）
- [Operating Model 文档](https://github.com/hidai25/eval-view/blob/main/docs/OPERATING_MODEL.md)（实际工作流参考）