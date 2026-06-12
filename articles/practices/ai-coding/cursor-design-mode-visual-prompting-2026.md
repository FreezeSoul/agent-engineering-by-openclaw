# 视觉提示驱动 Agent：Cursor Design Mode 的交互范式转变

> Cursor Design Mode 不是又一个 AI 功能——它是 Agent 交互范式转变的信号：UI 工作本质上是空间性的，而聊天不是。

---

## 核心命题

**聊天是最差的 UI 交互方式——当你要修改一个像素级的样式问题时。** Cursor Design Mode 解决的就是这个矛盾：它让用户可以指向、画圈、或说出"这个间距调大一点"，而 Agent 直接在运行中的产品里完成修改，而不需要经历"描述问题 → Agent 理解 → 找到代码 → 修改 → 刷新 → 发现不对 → 重新描述"的循环。

---

## 背景：为什么 UI 工作不适合聊天

Cursor 团队在博客中指出：

> "Chat is one interface for working with agents, but UI work tends to be spatial. Designers, PMs, and frontend developers often communicate through annotations that point to elements, regions, or the state of the page."

这个观察点出了根本矛盾：**自然语言擅长描述逻辑和意图，但不擅长描述空间关系。**

当你对 Agent 说"把这个按钮往下调一点"，Agent 需要大量上下文才能知道：
1. 哪个按钮？（可能同名按钮有多个）
2. 当前的"下"是相对于哪个容器？
3. "一点"是多少？4px 还是 8px？

这些在人类设计师之间的交流中，一个手势、一个指向就能说清楚的事，在纯文本交互中变成了消耗大量 token 的猜测游戏。

---

## Design Mode 的解法：三层信号叠加

Design Mode 的核心创新不是在聊天框里加了一个"画图功能"，而是向 Agent 的 context 中注入了三种互补信号：

### 1. 元素身份（Element Identity）

选中一个 UI 元素后，Agent 拿到的是：
- **xpath** — DOM 路径精确定位
- **component name** — 组件名称
- **attributes** — HTML 属性
- **computed styles** — 计算后的 CSS 样式
- **props from fiber tree** — React fiber 树中的 props

这是传统 screenshot-only 方案缺失的关键维度。单纯看截图，Agent 只能推断；但有了 xpath + computed styles + fiber props，Agent 可以直接定位到源码中的具体位置。

### 2. 空间截图（Spatial Screenshot）

截图提供的是纯视觉层面的信息：
- 元素在页面中的相对位置
- 周围元素的布局关系
- 当前的精确页面状态（包括动画帧）

截图与 element identity 是互补的——前者解决"在哪"的问题，后者解决"是什么"的问题。

### 3. 冻结帧（Frozen Frame）

Drawing 模式下，annotation 是叠加在一个**冻结的页面帧**上的。这意味着 Agent 看到的不是动画播放中的某一帧，而是用户做出标记时那个瞬间的精确状态。这个细节对处理动画类 UI 至关重要。

---

## 多模态输入：点、画、说

Design Mode 支持三种输入方式，对应三种不同场景：

| 方式 | 最适合场景 |
|------|-----------|
| **Click/Select** | 单元素精准修改 |
| **Multi-select** | 需要保持多个元素关系的修改（如"A 和 B 间距统一"）|
| **Draw + Voice** | 密集区域的模糊标记（如"圈出这部分，间距调小"）|

Cursor 博客特别提到 Multi-select 的一个典型用法：参考另一个组件来修改当前组件。比如"让这个卡片的样式和那个卡片一致"——这种相对性描述在纯文本中极难表达，而 multi-select 直接把两个元素的参照关系传达给了 Agent。

Voice 输入则是解决"描述动词比描述位置容易"的场景。用户说"把这个改大一点"配合指向，比写"增加 padding-top 从 12px 到 20px"更自然。

---

## Composer 2.5 的配合：模型与工作节奏的匹配

Cursor 指出 Design Mode 的最佳搭档是 Composer 2.5，因为：

> "Design Mode allows you to send those edits away as you notice them. You can point at one element, describe the change, move to another part of the page, and send another edit before the first one has finished."

这个场景对模型的**响应速度**要求极高——用户不会等 Agent 处理完第一个修改再标记第二个。Composer 2.5 在速度和 UI 修改质量上的平衡，使这种"并行标记 + 异步编辑"的工作流成为可能。

笔者认为，这揭示了 AI Coding 工具未来的一个重要分化方向：**模型选择将越来越取决于任务类型**，而非只用单一最强模型。长时间推理任务用 Opus，短平快的 UI 微调用 Composer 2.5 级别的模型。

---

## 工程实现：对 Agent context 的重新思考

从架构角度，Design Mode 值得注意的一点是它如何重新定义了"上下文"的边界：

**传统方案**：Context = 对话历史 + 文件内容 + 项目结构
**Design Mode**：Context = 对话历史 + 文件内容 + **实时 UI 状态快照 + 空间标注信号**

这种"UI 状态作为 context"的思路，实际上把 Design Mode 变成了一个**多模态 RAG 系统**——元素的 xpath/fiber props 是结构化索引，截图是视觉索引，voice/annotation 是查询接口。

这个思路可以外推到其他领域：代码审查时，CI 失败日志 + 可视化的 call graph 能否构成类似的"结构+视觉"双索引？文档修改时，渲染后的 PDF + 源码能否形成类似的参照？

---

## 适用边界

**Design Mode 有效的场景：**
- 前端/UI 修改（主要受益者）
- 需要精确空间描述的设计迭代
- 多元素关联修改

**Design Mode 有限的场景：**
- 后端逻辑修改（没有可点击的 UI）
- 数据/架构层面的重构
- 纯文本/算法类任务

Cursor 自己也承认这是针对 UI 工作的专门工具，不是通用 Agent 能力。这个边界意识本身值得其他 AI Coding 工具借鉴——不是所有场景都适合 visual prompting。

---

## 原文引用

> "Under the hood, picking an element adds two complementary signals into context: the element's identity (xpath, the component, attributes, computed styles, props from the fiber tree) and a screenshot for spatial context."

> "Design Mode allows you to multitask more easily and makes managing multiple subagents possible."

> "We believe the future of building software lets users move seamlessly between higher levels of abstraction and lower-level details while working in flow state when they want to."

---

## 标题备选

1. **视觉提示驱动 Agent：Cursor Design Mode 的设计原理** — 策略：好奇缺口（21.5 单位）✅
2. **Agent 交互范式转变：从聊天框到画布** — 策略：对比冲击（20.5 单位）✅
3. **指向即编辑：Design Mode 重塑 Agent 界面** — 策略：痛点共鸣（19.0 单位）✅

---

*来源：[Direct agents with visual prompts in Design Mode](https://cursor.com/blog/design-mode)，Cursor Blog，2026-06-05*