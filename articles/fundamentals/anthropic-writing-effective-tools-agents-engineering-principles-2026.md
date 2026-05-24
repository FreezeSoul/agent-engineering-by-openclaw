# Anthropic 工件具设计原则：让 Agent 高效使用工具的工程实践

## 核心论点

Anthropic 在《Writing effective tools for AI agents》中揭示了工具设计的核心悖论：**对 Agent 最"人体工学"的工具，往往对人类也直觉直觉**。通过渐进式披露（Progressive Disclosure）和精确的上下文管理，工具可以从"信息生产者"进化为"可协作伙伴"。

## 关键发现

### 1. 工具的本质：确定性系统与非确定性 Agent 之间的契约

传统软件是确定性系统——`getWeather("NYC")` 每次以完全相同的方式获取纽约市天气。但 Agent 是非确定性系统——相同的起始条件可能产生不同的响应。这意味着为 Agent 编写工具本质上是重写软件契约：

> "Tools are a new kind of software which reflects a contract between deterministic systems and non-deterministic agents."

关键洞察：工具的"人体工学"程度与 Agent 的执行效率直接相关，而对 Agent 友好的工具往往也对人类直觉友好。

### 2. 渐进式披露三层架构

Anthropic 展示了工具设计的核心原则——渐进式披露：

| 层级 | 内容 | 加载时机 |
|------|------|----------|
| **系统提示层** | 工具名称和描述 | Agent 启动时预加载 |
| **上下文层** | 完整 SKILL.md 内容 | Agent 判断相关时加载 |
| **按需层** | 额外链接文件 | Agent 探索时发现 |

这种架构与 Agent Skills 的设计完全一致——如 Skill 目录包含 `SKILL.md` + 额外文件（`reference.md`、`forms.md`），Agent 只在需要时才深入下一层。

### 3. 评估驱动的工具优化

Anthropic 强调用 Agent 协助改进工具的飞轮：

```
构建原型 → 运行评估 → 分析结果 → Agent 协作改进 → 重复
```

评估任务应该是：
- **强任务**：多工具调用（可能需要数十次调用），基于真实数据和场景
- **弱任务**：单一查询，过于简化的沙箱环境

例如强评估任务：
> "Customer ID 9182 reported they were charged three times for a single purchase attempt. Find all relevant log entries and determine if any other customers were affected."

### 4. 工具选择的根本原则

Anthropic 指出了一个常见错误：**仅因为现有 API 存在就包装工具**。

核心权衡：
- LLM Agent 有有限的"上下文"（能同时处理的信息量有限）
- 计算机内存便宜且充足
- 传统软件可以逐条处理列表（如搜索通讯录），但如果 Agent 工具返回所有联系人并逐条阅读，则是浪费上下文空间

正确的设计模式：
```python
# 差：返回所有联系人，Agent 逐条扫描
get_all_contacts() → 浪费上下文

# 好：Agent 精确获取所需信息
search_contacts(query="John") → 精准返回结果
```

### 5. 工具描述的工程细节

Anthropic 发现 Claude 常常产生微妙的偏差——如在网络搜索工具的查询参数后无意义地追加"2025"，偏见搜索结果。这通过改进工具描述得到了纠正，展示了**精确描述 > 隐式约定**的工程原则。

## 核心工程原则总结

1. **少即是多**：不必实现所有可能的工具，选择针对高频、高价值工作流的精选工具
2. **精确优于通用**：工具应精确返回所需信息，而非返回全部让 Agent 过滤
3. **描述驱动**：工具的描述和规格是 Agent 理解其用途的主要信号
4. **渐进式加载**：不要一次性加载所有上下文，让 Agent 按需发现
5. **评估闭环**：用真实任务评估工具，用 Agent 协助改进工具

## 实践启示

对于 AI Coding 工具链（如 Cursor、Claude Code）：

- **工具命名**应清晰表达功能边界（Namespacing）
- **返回内容**应只包含 Agent 当前任务所需信息
- **描述文本**应包含使用示例和成功条件
- **评估框架**应基于真实工作流，而非简化测试用例

这种思维方式与 MCP（Model Context Protocol）的设计理念一脉相承——工具体系本质上是一套 Agent 与确定性系统之间的契约规范。

## 来源

- [Writing effective tools for AI agents](https://www.anthropic.com/engineering/writing-tools-for-agents)（Anthropic Engineering Blog）