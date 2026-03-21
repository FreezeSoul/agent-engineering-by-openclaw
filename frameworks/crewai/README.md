# CrewAI

> 角色扮演式多Agent协作框架，强调任务分解与角色扮演。

---

## 核心概念

CrewAI 通过**角色扮演**的方式组织多个 Agent 协作，核心理念是「每个 Agent 都有明确的职责」。

### 三大核心

1. **Agent（角色）**
   - 定义：角色名称、角色目标、 backstory（背景故事）
   - 可绑定 LLM 和 Tools
   - 支持层级式 Agent（Agent 管理者）

2. **Task（任务）**
   - 具体的工作单元
   - 描述、期望输出、分配给哪个 Agent
   - 支持前置依赖任务

3. **Crew（团队）**
   - Agent 集合
   - 定义执行顺序（sequential / hierarchical）
   - 配置任务流程和输出格式

### 两种执行模式

- **Sequential（顺序）**：任务按定义顺序依次执行
- **Hierarchical（层级）**：一个 Manager Agent 负责分配任务给其他 Agent

---

## 适用场景

- 需要多角度分析的任务（如市场调研）
- 角色分工明确的业务流程
- 需要「研究员 + 审核员 + 决策者」协作的场景

---

## 学习资源

- [CrewAI Blog](https://crewai.com/blog)
- [CrewAI GitHub](https://github.com/crewAI)

---

## 优势

✅ 多 Agent 协作开箱即用
✅ 角色设计直观，易于理解
✅ 支持 hierarchical 模式
✅ 文档相对完善

## 劣势

⚠️ 状态管理依赖外部
⚠️ 复杂工作流需要自行设计
⚠️ 框架相对较新，生态还在成长

---

*最后更新：2026-03-21*
