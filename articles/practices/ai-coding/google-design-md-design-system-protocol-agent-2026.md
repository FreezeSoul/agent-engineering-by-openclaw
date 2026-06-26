# Google design.md: 让编码 Agent 读懂设计系统的工程协议

**核心命题**：Google Labs 发布的 design.md 是目前最完整的「让 AI Agent 理解视觉设计系统」的协议规范。它用 YAML + Markdown 双层格式解决了 AI 编码中设计系统上下文丢失的根本问题——Tokens 提供精确值，Prose 解释为什么，Agent 两者结合才能生成符合设计意图的代码。

---

## 一、为什么现有的 Design-to-Code 方案在 Agent 场景失效

在传统的设计-开发流程中，设计师通过 Figma/Sketch 导出的设计稿交给工程师，工程师手动翻译成代码。这个流程有几个关键特征：

1. **人类理解弥补信息损失**：设计师的意图通过视觉隐喻传达，工程师用经验填补缺失的上下文
2. **上下文是隐性的**：为什么这个按钮用 `#B8422E` 而不是其他红色？设计师可能说不清，工程师也不会问
3. **修改成本高**：一旦设计系统更新，需要人工同步代码，人工审查是否遗漏

对于 AI 编码 Agent，这三个特征全部变成了阻塞问题。Agent 没有「经验」可以调用，没有「不会问」的自觉，更不会「主动审查」遗漏。

现有解决方案的问题：

| 方案 | 核心问题 |
|------|---------|
| Figma API + 设计 token 导出 | 需要额外的工程对接，Agent 无法直接消费 |
| 设计系统文档（Storybook）| 人类可读但机器解析成本高，版本同步滞后 |
| 直接在 Prompt 里塞设计规则 | 上下文窗口爆炸，规则之间冲突无法检测 |
| 让 Agent「看」设计稿截图 | 只能获得像素级信息，无法理解设计意图和约束 |

**真正的问题不是「Agent 不知道设计稿长什么样」，而是「Agent 不知道设计系统为什么这样设计，以及在什么情况下可以例外」。**

---

## 二、design.md 的核心设计：双层结构

Google Labs 的 design.md 用一个文件同时解决了「值是什么」和「为什么这样值」两个问题。

```markdown
---
name: Heritage
colors:
  primary: "#1A1C1E"
  secondary: "#6C7278"
  tertiary: "#B8422E"
  neutral: "#F7F5F2"
typography:
  h1:
    fontFamily: Public Sans
    fontSize: 3rem
  body-md:
    fontFamily: Public Sans
    fontSize: 1rem
  label-caps:
    fontFamily: Space Grotesk
    fontSize: 0.75rem
rounded:
  sm: 4px
  md: 8px
spacing:
  sm: 8px
  md: 16px
---

## Overview

Architectural Minimalism meets Journalistic Gravitas. The UI evokes a
premium matte finish — a high-end broadsheet or contemporary gallery.
```

**YAML 层（Tokens）**：机器可解析的精确值，Agent 直接引用不会出错

**Markdown 层（Prose）**：人类可读的设计意图解释，Agent 理解边界和例外

关键洞察：**Tokens 是规范，Prose 是元规范**。Tokens 告诉 Agent 值是什么，Prose 告诉 Agent 在什么上下文中使用哪个值，以及为什么。

---

## 三、Token 引用的工程价值：打破硬编码循环

design.md 最聪明的设计是 Token 引用机制——组件属性可以引用 Token 而不是硬编码值：

```yaml
components:
  button-primary:
    backgroundColor: "{colors.tertiary}"
    textColor: "{colors.on-tertiary}"
    rounded: "{rounded.sm}"
    padding: 12px
  button-primary-hover:
    backgroundColor: "{colors.tertiary-container}"
```

这个设计解决了一个实际问题：当设计系统更新主色时，硬编码的 `#B8422E` 需要手动全部替换，而 Token 引用只需要改一处。

对于 Agent 来说，这还有额外的工程价值：

1. **一致性保证**：Agent 引用 `{colors.tertiary}` 生成的颜色，必然与系统其他组件一致
2. **变更可追踪**：设计系统更新后，Agent 可以通过 `diff` 命令检测哪些组件受影响
3. **WCAG 可验证**：`lint` 命令自动检查对比度是否满足 WCAG AA/AAA

笔者认为，这个 Token 引用机制比 Figma 的变量系统更接近代码工程师的直觉——它本质上是一个只读的、发布后的设计系统快照。

---

## 四、命令行工具：lint / diff / export

design.md 附带三个核心命令，覆盖了设计系统变更的生命周期：

### 4.1 lint：自动化设计规则检查

```bash
npx @google/design.md lint DESIGN.md
```

输出结构化 JSON：

```json
{
  "findings": [
    {
      "severity": "warning",
      "path": "components.button-primary",
      "message": "textColor (#ffffff) on backgroundColor (#1A1C1E) has contrast ratio 15.42:1 — passes WCAG AA."
    }
  ],
  "summary": { "errors": 0, "warnings": 1, "info": 1 }
}
```

这个命令的价值在于：它把设计规则检查自动化了。在没有这个工具之前，设计系统规范通常只存在于设计师的脑海里或者 Figma 的样式面板里，工程师无法自动化验证自己生成的代码是否符合规范。

### 4.2 diff：设计系统版本变更检测

```bash
npx @google/design.md diff DESIGN.md DESIGN-v2.md
```

输出：

```json
{
  "tokens": {
    "colors": { "added": ["accent"], "removed": [], "modified": ["tertiary"] },
    "typography": { "added": [], "removed": [], "modified": [] }
  },
  "regression": false
}
```

这个功能对于多 Agent 协作场景尤其有价值：当一个 Agent 修改了 DESIGN.md，其他 Agent 可以通过 `diff` 快速了解变更范围，而不是重新解析整个文件。

### 4.3 export：多格式导出

```bash
npx @google/design.md export --format css-tailwind DESIGN.md > theme.css
npx @google/design.md export --format dtcg DESIGN.md > tokens.json
npx @google/design.md export --format json-tailwind DESIGN.md > tailwind.theme.json
```

这解决了「设计系统和前端框架的格式鸿沟」问题。Tailwind CSS、DTCG (Design Token Community Group) 等格式各有适用场景，design.md 作为中间格式，一次定义，多格式导出。

---

## 五、与现有方案的对比

| 维度 | design.md | Figma Variables | Style Dictionary | Storybook |
|------|-----------|-----------------|------------------|-----------|
| **机器可读性** | ✅ 原生 JSON/YAML | ⚠️ 需要 API | ✅ JSON | ❌ HTML |
| **人类可读性** | ✅ Markdown | ❌ Figma UI | ⚠️ JSON | ✅ React |
| **Agent 直接消费** | ✅ | ❌ | ✅ | ❌ |
| **WCAG 验证** | ✅ 内置 | ❌ | ❌ | ❌ |
| **diff 版本对比** | ✅ | ❌ | ⚠️ 手动 | ❌ |
| **多格式导出** | ✅ Tailwind/DTCG | ❌ | ✅ | ❌ |
| **设计意图记录** | ✅ Prose 层 | ❌ | ❌ | ⚠️ 注释 |
| **依赖 Figma** | ❌ | ✅ | ❌ | ❌ |

笔者认为，design.md 的核心优势不是功能上的，而是**定位上的**：它明确面向 AI Agent 设计，把「设计系统文档」这个人类工具翻译成了 Agent 可以精确消费的协议。

Figma Variables 是给设计师用的，Style Dictionary 是给前端工程师用的，design.md 是给 AI Agent 用的。这个定位差异决定了它的最佳应用场景。

---

## 六、适用边界与已知局限

design.md 不是银弹，它有明确的适用边界：

**适用场景**：
- 已有明确设计系统定义的中大型团队
- 需要多个 Agent 协作生成 UI 的场景
- 需要设计变更可追踪、可验证的场景

**不适用场景**：
- 快速原型阶段（设计系统尚未定义完整）
- 单一 Agent 简单任务（维护成本 > 收益）
- 设计系统和代码已经深度耦合的历史项目（迁移成本高）

**当前局限**：
1. **组件变体表达能力有限**：Variants（hover/active/pressed）用分离的组件条目表达，没有变体数组直观
2. **无 Figma 同步机制**：design.md 和 Figma 是两个独立的数据源，需要手动或通过额外工具同步
3. **生态尚未成熟**：npm 包在 2026 年中才发布，部分平台的安装存在 Registry 配置问题

---

## 七、如何集成到现有 Agent 工作流

把 design.md 融入 Agent 工作流有两种路径：

### 路径 A：项目初始化阶段（推荐）

```
1. 设计团队定义 DESIGN.md
2. Agent 通过 lint 验证 DESIGN.md 格式正确
3. Agent 通过 export 生成框架级样式文件
4. 后续所有 UI 生成任务引用 DESIGN.md
```

这种路径适合从零开始的项目，design.md 作为设计系统共识文档，Agent 和人类工程师共同遵守。

### 路径 B：存量项目接入

```
1. 从 Figma/Sketch 提取设计 Token，手动或通过工具转换
2. 创建 DESIGN.md 并 lint 验证
3. 在 Agent 的 system prompt 中加入 `Read DESIGN.md before writing UI code`
4. 定期 diff 检测设计系统变更
```

这种路径适合已有设计系统但尚未结构化的团队，接入成本比路径 A 高，但长期收益显著。

---

## 八、结论

Google design.md 解决的不是「设计系统怎么管理」的问题，而是「AI Agent 怎么消费设计系统」的问题。这两个问题看起来相似，但解决方案的约束条件完全不同——后者要求机器可解析、变更可追踪、规则可验证。

笔者认为，design.md 代表了一个更大的趋势：**AI Agent 时代的工程实践需要把「人类默契」翻译成「机器可读协议」**。设计系统的 Token 化只是其中一个领域，随着 Agent 进入生产环境，我们会看到更多类似的「人类工具 → Agent 协议」的转换。

这不是 design.md 本身有多复杂——它的代码量可能不超过 2000 行——而是因为它抓住了问题的本质：Agent 需要的是规范，不是描述。

---

**关联阅读**：
- [Google design.md 官方 Spec](https://github.com/google-labs-code/design.md/blob/main/docs/spec.md)
- [Orca - AI 编码 Agent 的多 Agent 并行执行环境](/projects/stablyai-orca-multi-agent-ide-331-stars-2026.md)

---

*来源：[github.com/google-labs-code/design.md](https://github.com/google-labs-code/design.md)，2026-06-25 GitHub Trending，619+ stars，MIT License*