# AutoHarness：让每个 Agent 都能从"demo-ready"走向生产可靠

> 来源：[aiming-lab/AutoHarness](https://github.com/aiming-lab/AutoHarness)，2026-04-01 发布  
> 标签：`projects` `harness` `governance` `open-source` `multi-agent`

---

## TRIP 四要素

**T-Target**：正在构建或部署 AI Agent 的工程师，尤其是经历过 agent 从 demo 跑通到生产落地的人——那些被 context 爆炸、token 成本失控、prompt injection 攻击、审计缺失折磨过的人。

**R-Result**：用 2 行代码为任何 LLM Client 添加完整的 governance layer：6 步 pipeline 阻止 `rm -rf /`，token budget 防止成本爆炸，layered validation 防御 prompt injection，JSONL audit log 满足合规要求，multi-agent profiles 实现角色权限隔离。

**I-Insight**：核心洞察是"Agent = Model + Harness"——模型负责推理，harness 负责治理。Demo 阶段靠模型就能跑通，但生产级别 reliability 必须在 harness 层解决。AutoHarness 把这层治理从隐式变显式，从手工变自动化。

**P-Proof**：2026-04-01 发布 v0.1.0，GitHub 257 stars，958 tests passing。支持 Python，多语言 README（中文/日文/韩文/西班牙文/法文/德文/葡萄牙文/俄文），说明项目在发布后迅速获得国际社区关注。

---

## P-SET 骨架

### P（Position）——15秒判断"和我有关"

你想把一个 AI Agent 部署到生产环境，却被这些问题卡住：
- Agent 动不动就"token 爆炸"，成本失控
- 没有任何审计日志，出问题无法追溯
- 不同 Agent 需要不同权限，但全用同一套配置
- Prompt injection 攻击完全没有防御

如果你有以上任何一个问题，AutoHarness 就是你正在找的东西。

---

### S（Story）——体验式介绍

想象你给团队里每个 Agent 都装上了一个"治理层"——在模型真正执行任何操作之前，先经过 6 步检查：

```
1. Parse & Validate   → 格式正确吗？
2. Risk Classify     → 有危险操作吗？
3. Permission Check  → 这个角色有权限吗？
4. Execute           → 执行
5. Output Sanitize   → 输出干净吗？
6. Audit Log         → 记录每一步
```

不加 harness 层，你的 Agent 收到 `"rm -rf /"` 会直接执行。加了 AutoHarness，这一步会被 block、log、解释原因。

**实际代码（2行接入）**：

```python
from openai import OpenAI
from autoharness import AutoHarness

client = AutoHarness.wrap(OpenAI())
# That's it. Your agent just had its aha moment.
```

这就是项目 tagline 的含义：从"demo-ready"到真正 reliable，harness 是关键。

---

### E（Evidence）——技术深度与竞品对比

**AutoHarness 的三层 Pipeline Mode**：

| Mode | Pipeline Steps | Hooks | Multi-Agent | 适用场景 |
|------|--------------|-------|-------------|---------|
| Core | 6-step | Secret scanner + path guard + output sanitizer | 单 Agent | 轻量级治理，最小 overhead |
| Standard | 8-step | + Risk classifier + pre-hooks | Basic profiles | 生产级 Agent |
| Enhanced ⚠️ | 14-step | + Turn governor + alias resolution + failure hooks | Fork/Swarm/Background | 最大治理强度 |

⚠️ Enhanced 是默认模式。用户开箱即得最强治理，改用 Core 降低 overhead。

**与 Cursor Harness 的互补关系**：

- **Cursor** 是闭源商业产品内部的 harness 实践，针对 coding agent 场景，有完整的 measurement infrastructure（CursorBench + A/B testing + Keep Rate tracking）
- **AutoHarness** 是开源 harness 框架，通用设计，覆盖治理（pipeline/权限/安全），但不包含 measurement 和 evaluation 体系

两者代表 harness 工程的不同维度：Cursor 展示"如何迭代"，AutoHarness 提供"用什么构建"。

**项目技术规格**：
- Python 包：`pip install -e .` 本地安装
- 配置文件：`constitution.yaml`（YAML 格式，声明式配置）
- AgentLoop：`AgentLoop(model="gpt-5.4", constitution="constitution.yaml")` 完整 agent 循环封装
- Token 预算和成本追踪：per-call cost attribution with model-aware pricing
- 多 Agent profiles：角色权限隔离

---

### T（Action）——3步上手

**Step 1：安装**
```bash
git clone https://github.com/aiming-lab/AutoHarness.git
cd AutoHarness && pip install -e .
```

**Step 2：用 2 行代码接入现有 Client**
```python
from openai import OpenAI
from autoharness import AutoHarness
client = AutoHarness.wrap(OpenAI())
```

**Step 3：配置 constitution（可选）**
```yaml
# constitution.yaml
mode: standard  # core / standard / enhanced
risk_threshold: high
```

**贡献入口**：
- GitHub Issues：报告 bug 或请求 feature
- PR：欢迎贡献，尤其是 Enhanced mode 的 hooks 扩展

**Roadmap**（根据 v0.1.0 release note）：
- v0.1.0: 三层 pipeline modes，6-step governance，risk pattern matching，YAML constitution，trace diagnostics，session persistence
- 预期：更多 provider 支持（不限于 OpenAI）、更细粒度的 policy engine、可观测性集成

---

## 自检清单

| 检查项 | 状态 |
|--------|------|
| TRIP×4 完成 | ✅ T（生产部署工程师）、R（2行接入+6步治理）、I（模型+治理分离）、P（257 stars + 958 tests） |
| P-SET×4 完成 | ✅ P（问题驱动）、S（6步pipeline体验）、E（竞品对比+技术规格）、T（3步上手+贡献入口） |
| 通用×3 | ✅ 中文输出、来源一手（GitHub README）、时效新（2026-04发布） |
| 与 Articles 主题关联 | ✅ Articles 分析 Cursor harness 工程方法论（evaluation + iteration），Projects 推荐 AutoHarness（治理框架实现） |
| GitHub Trending 筛选 | ✅ 257 stars（本轮最高相关度），2026-04 创建（非老旧项目） |