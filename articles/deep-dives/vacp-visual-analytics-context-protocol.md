# VACP: Visual Analytics Context Protocol — 让可视化应用成为 Agent 的原生伙伴

> **本质**：将可视化分析（VA）应用改造为 Agent 可直接理解和操作的「原生接口」，而非依赖计算机视觉或 DOM 解析

## 一、基本概念

### 问题：现有 Agent 方案在可视化场景中的困境

当前 AI Agent 处理可视化分析任务时，依赖两种落后方案：

| 方案 | 原理 | 致命缺陷 |
|------|------|---------|
| **Computer Vision** | 用视觉模型「看」图表 | 消耗大量 token；无法理解交互语义；精度低 |
| **Raw DOM 访问** | 直接爬取网页 DOM | Token 开销极高；语义丢失；DOM 结构一变就失效 |

这两种方案的本质问题：**把 Agent 当作「盲人用户」，让它通过间接方式感知界面**。VACP（Visual Analytics Context Protocol）的核心洞察是：可视化应用天然具有丰富的结构化信息（数据模型、交互元素、可视化状态），问题在于这些信息没有以 Agent 可理解的方式暴露出来。

### VACP 定义

> VACP：Visual Analytics Context Protocol，一个将可视化分析应用改造为「Agent 原生接口」的协议框架，通过显式暴露应用状态、可用交互和直接执行机制，使 Agent 能够像人类用户一样理解和操作可视化界面。

VACP 不是另起炉灶的协议，而是对现有通用协议（如 MCP）的**领域专用扩展**——类似于 HTTP、WebSocket 是在 TCP 之上构建的应用层协议，VACP 是在 MCP 之上构建的可视化分析专用层。

---

## 二、核心技术机制

### 2.1 三层信息暴露模型

VACP 要求 VA 应用显式暴露以下三层信息：

**Layer 1 — Application State（应用状态层）**
- 数据模型：底层数据集的结构和内容
- 可视化状态：当前绑定的数据字段、聚合方式、过滤条件
- 坐标系统：视觉编码映射（颜色→类别、大小→数值等）

**Layer 2 — Available Interactions（可用交互层）**
- 交互原语：哪些操作是可用的（选择、过滤、缩放、排序等）
- 参数约束：每个交互接受的参数范围和类型
- 语义标签：交互的领域含义（而非仅技术参数）

**Layer 3 — Execution Mechanism（执行机制层）**
- 直接 API：Agent 可直接调用执行操作的接口（无需模拟点击）
- 响应格式：操作结果的标准化返回
- 事务语义：操作是否可撤销、批提交还是即时生效

### 2.2 形式化规范

论文贡献了 AI Agent 在 VA 界面中的**需求形式化规范**，定义了 Agent 理解 VA 界面所需的知识表示：

```
Agent-VA Interface = {
  DataModel:      Schema + Instance
  VisualEncoding:  {channel → data_field} 映射规则
  InteractionSet:  {action → {parameters, preconditions, effects}}
  ExecutionAPI:   {method → {input, output, side_effects}}
}
```

### 2.3 库实现

VACP 以库的形式实现，兼容主流可视化框架：

- **可视化语法层**：Vega-Lite、Observable Plot、Matplotlib 等
- **Web 框架层**：React（通过自定义 Hooks）、Vue、Svelte 等
- **BI 工具层**：支持对商业智能工具的可观测层扩展

这意味着现有可视化应用可以在**不重写核心逻辑的情况下**通过添加 VACP 层变成「Agent 可读」。

---

## 三、与其他概念的关系

### VACP vs 标准 MCP

MCP 是通用协议，定义了 Agent 与外部系统交互的标准方式（工具调用、资源订阅、提示注入等）。VACP 将 MCP 的通用原语**特化到可视化分析领域**：

| MCP 原语 | VACP 扩展 |
|---------|----------|
| `tools/list` | 映射为 VA 交互原语集合 |
| `tools/call` | 直接调用 VA 操作（而非模拟点击）|
| `resources/read` | 读取数据模型和可视化状态 |
| `resources/subscribe` | 订阅可视化状态变更事件 |

### 演进路径定位

VACP 处于 **Stage 3（MCP）× Stage 6（Tool Use）** 的交叉地带：
- **Stage 3**：作为 MCP 协议的领域专用扩展
- **Stage 6**：将 VA 工具从「视觉感知对象」升级为「结构化可操作接口」

### 核心演进链

```
MCP（通用工具协议）
  → VACP/MCP-Transport（领域专用扩展）
    → Agent 与 VA 系统的深度集成
```

---

## 四、实验评估

### 评估方法

论文设计了三类代表性 VA 任务的对照实验：
1. **界面解释任务**：Agent 理解当前可视化显示的内容
2. **操作执行任务**：Agent 完成特定的数据操作（筛选、聚合、切换图表类型等）
3. **端到端分析任务**：Agent 自主完成一个完整的可视化分析流程

### 关键结果

| 指标 | VACP-enabled Agent | CV-based Agent | DOM-based Agent |
|------|--------------------|----------------|-----------------|
| 任务成功率 | **最高** | 较低 | 低 |
| Token 消耗 | **最低** | 高 | 极高 |
| 延迟 | **最低** | 高 | 高 |

> 核心数据：VACP-enabled agents 在**不损失精度的情况下**，token 消耗和延迟均显著低于 CV/DOM 方案。

### 为什么 token 消耗更低？

CV 方案需要将每个可视化帧编码为 token（一张图表可能消耗 1000+ tokens），DOM 方案需要遍历整个 DOM 树。VACP 通过直接读取**结构化的应用状态**，将 token 开销从「整张图表」降低到「关键状态字段」。

---

## 五、局限性与未来方向

### 当前局限性

1. **实现覆盖有限**：库目前仅支持主流 Web 可视化框架，企业级 BI 工具（Tableau、PowerBI）的插件生态尚未建立
2. **离线场景缺失**：VACP 假设 VA 应用在线可用，不适合离线文件（.ipynb、离线 HTML）
3. **安全模型未讨论**：协议暴露了丰富的应用内部状态，商业场景下的权限控制需要额外设计
4. **学术评估 vs 工业规模**：论文评测规模有限，生产环境中的大规模部署效果尚待验证

### 未来演进方向

- **BI 工具官方支持**：与 Tableau、PowerBI 官方合作，将 VACP 纳入插件 SDK
- **多 Agent 协作扩展**：单一 VACP 接口 → 多 Agent 分工协作（一个 Agent 操作图表、一个 Agent 分析数据）
- **离线 VACP**：支持 PDF/静态 HTML 中的可视化上下文提取
- **安全层**：在 VACP 之上构建权限控制和数据脱敏机制

---

## 六、参考文献

- **本篇论文**：Stähle, T., Gyarmati, P.F., Spinner, T., Sevastjanova, R., Moritz, D., & El-Assady, M. (2026). *VACP: Visual Analytics Context Protocol*. arXiv:2603.29322. https://arxiv.org/abs/2603.29322

---

## 附：快速上手

> VACP 库目前可通过 GitHub 获取（论文未提供明确 URL，建议通过 arXiv 论文链接获取源代码链接）

```python
# VACP 概念示例（伪代码）
from vacp import VAContextProtocol

# 初始化 VACP 代理
vacp = VAContextProtocol(chart_app)

# 获取应用状态（Agent 可读格式）
state = vacp.get_state()
print(state["data_model"])     # {"fields": ["sales", "region", "date"]}
print(state["visual_encoding"]) # {"x": "date", "y": "sales", "color": "region"}

# 获取可用交互
interactions = vacp.get_interactions()
print(interactions[0]) # {"type": "filter", "field": "region", "values": ["APAC", "EMEA"]}

# Agent 直接执行操作（无需模拟点击）
result = vacp.execute("filter", {"field": "region", "values": ["APAC"]})
```

---

*本文属于 Stage 3（MCP）× Stage 6（Tool Use）交叉领域，与 [MCP Ecosystem 2026](mcp-ecosystem-2026-state-of-the-standard.md) 互为补充：后者关注 MCP 生态全景，VACP 关注 MCP 的可视化分析垂直场景扩展。*
