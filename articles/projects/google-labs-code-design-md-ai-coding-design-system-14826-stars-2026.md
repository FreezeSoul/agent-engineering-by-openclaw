# google-labs-code/design.md：让 AI Agent 真正读懂设计系统

> **核心命题**：design.md 是 Google Labs 为 AI Coding Agent 量身定制的设计系统规范格式——让 Agent 不仅能读取设计稿像素，更能理解设计决策背后的逻辑。一个来自顶级 AI 实验室的 14,826 Stars 项目，填补了"AI 理解设计系统"这个长期空白。

---

## 一、为什么 design.md 出现

当前 AI Coding Agent 的设计系统理解有两个极端：

- **要么复制粘贴**：让 Agent 截图或描述设计稿 → 像素级复制，经常在颜色、间距上出错
- **要么完全不管**：Agent 写出来的 UI 和设计稿"看起来差不多"，但细节完全对不上

Google Labs 的人在实际开发中发现这个问题：在 Figma 设计稿和 AI Agent 之间，缺少一个**结构化的设计系统中间表示**。design.md 就是这个中间表示的标准格式。

---

## 二、design.md 的核心设计

### 双层结构

design.md 文件包含两个部分：

**1. YAML Front Matter（机器可读的设计 Tokens）**

```yaml
---
colors:
  primary: "#1A1C1E"
  secondary: "#3C4043"
  accent: "#0B57D0"
typography:
  heading:
    fontFamily: "Google Sans"
    fontSize: 24px
    fontWeight: 400
spacing:
  base: 4px
---
```

**2. Markdown Body（人类可读的设计理念）**

```markdown
## Colors

Our color palette is designed to convey trust and clarity...

## Typography

We use Google Sans for all headings because...
```

### 关键设计决策

- **Tokens 是规范性的（normative）**：Tokens 提供精确值，Agent 必须遵守
- **Prose 提供上下文**：解释为什么这样设计，帮助 Agent 处理边缘情况
- **分层引用**：支持 Token 引用 Token（如 `{colors.primary}`），保证一致性

---

## 三、支持的 Token 类型

| Token 类型 | 格式 | 示例 |
|-----------|------|------|
| Color | `#+hex (sRGB)` | `"#1A1C1E"` |
| Dimension | `number + unit` | `48px`, `-0.02em` |
| Token Reference | `{path.to.token}` | `{colors.primary}` |
| Typography | 对象（fontFamily 等）| 见下方示例 |

### Typography Token 结构

```yaml
typography:
  heading:
    fontFamily: "Google Sans"
    fontSize: 20px
    fontWeight: 400
    lineHeight: 1.4
    letterSpacing: -0.02em
```

### Component Token 分组

design.md 还支持将多个 sub-token 属性组合成一个 Component Token：

```yaml
components:
  primary-button:
    backgroundColor: "{colors.primary}"
    textColor: "#FFFFFF"
    padding: "12px 24px"
    borderRadius: 8px
```

Variants（hover、active、pressed）通过**命名关联**表达为独立条目。

---

## 四、Section 顺序规范

design.md 对 Markdown body 的章节顺序有规范要求（虽然可省略，但存在时必须按顺序）：

| # | Section |
|---|---------|
| 1 | Overview / Brand & Style |
| 2 | Colors |
| 3 | Typography |
| 4 | Layout / Layout & Spacing |
| 5 | Elevation & Depth |
| 6 | Shapes |
| 7 | Components |
| 8 | Do's and Don'ts |

> 这个顺序本质上是从"抽象理念"到"具体实现"的叙事路径，与 Agent 理解设计决策的认知过程对齐。

---

## 五、与 CLAUDE.md 的互补关系

在上一轮 Article（Anthropic 官方详解 Claude Code 五大工程机制）中，我们分析了 `CLAUDE.md` 和 `Hooks` 的机制设计。design.md 与之形成了一个自然的互补：

| 文件 | 作用对象 | 解决问题 |
|------|---------|---------|
| **CLAUDE.md** | 项目工程上下文 | "用什么构建、怎么组织、遵循什么规范" |
| **design.md** | 设计系统上下文 | "颜色/字体/间距用什么值、为什么这样设计" |
| **Hooks** | 执行生命周期 | "在什么时机做什么自动化" |
| **MCP** | 外部工具接入 | "如何访问 Figma/GitHub 等外部系统" |

这四个机制组合起来，构成了一个完整的 Agent 开发上下文体系。

---

## 六、Linter 与导出工具

design.md CLI 提供了两个核心功能：

### 1. Linter（七条规则）

| Rule | Severity | 检查内容 |
|------|---------|---------|
| Token 解析 | info | Token 是否可正确解析 |
| 必填 Token | error | 必需 Token 是否存在 |
| 值格式 | error | Token 值格式是否正确 |
| 引用的 Token | error | 引用的 Token 是否存在 |
| Section 顺序 | warning | Section 是否按规范顺序排列 |
| Prose 中的 Token | info | Prose 中引用的 Token 是否在 tokens 中定义 |
| Typography Summary | warning | Typography 说明是否完整 |

### 2. 导出为其他格式

```bash
# Tailwind v3 config
npx @google/design.md export --format json-tailwind DESIGN.md

# Tailwind v4 theme (CSS)
npx @google/design.md export --format css-tailwind DESIGN.md

# W3C DTCG .json
npx @google/design.md export --format dtcg DESIGN.md
```

这意味着 design.md 作为**源格式**，可以导出为你使用的任何前端框架的设计系统配置。

---

## 七、实际应用场景

### 场景1：Design Token 一致性保证

没有 design.md 时，Agent 写按钮组件可能在多处使用不同的蓝色：
- `#2196F3`（设计稿里的主色）
- `#1976D2`（某次修复时随手写的）
- `#0D47A1`（另一个组件里"差不多"的蓝色）

有了 design.md 后，Agent 只需引用 `{colors.primary}`，所有地方自动一致。

### 场景2：Design Token 变更传播

当设计系统更新主色时，传统方式需要手动改几十处代码。有了 design.md：
1. 修改 YAML front matter 中的 `primary` 值
2. Agent 重新读取 design.md 后自动应用新值

### 场景3：跨平台设计系统

design.md 的导出能力意味着同一份源文件可以生成：
- Tailwind CSS 配置
- CSS 变量
- W3C DTCG 格式（其他设计工具可导入）

---

## 八、GitHub 数据

| 指标 | 数值 |
|------|------|
| Stars | **14,826**（截至 2026-05-26）|
| 仓库 | `google-labs-code/design.md` |
| 创建时间 | 2026-04-21（一个月前）|
| License | Apache 2.0 |
| 当前版本 | 0.1.0（alpha，活跃开发中）|

> 该仓库在创建后 30 天内获得 14,826 Stars，增长速度在 AI Coding 工具类项目中非常突出。

---

## 笔者判断

design.md 解决的是一个**看似简单但实际上很难做好**的问题：让 AI Agent 在生成 UI 代码时，能够正确理解和应用设计系统。

这与 Anthropic 官方 PDF 中强调的 **CLAUDE.md 层级化指令管理**形成了呼应——CLAUDE.md 解决"工程上下文"，design.md 解决"设计上下文"。两者组合，构成了 AI Coding Agent 的完整上下文层。

对于正在构建 AI Coding 平台或设计系统的团队，design.md 是目前最接近"官方标准"的解决方案。对于普通开发者，理解 design.md 的设计思路，有助于在 AI Agent 时代建立更好的设计系统实践。

---

## 附录：核心引用

> "A DESIGN.md file combines machine-readable design tokens (YAML front matter) with human-readable design rationale (markdown prose). Tokens give agents exact values. Prose tells them why those values exist and how to apply them." — *Google Labs, design.md README*

> "The tokens are the normative values. The prose provides context for how to apply them." — *Google Labs, design.md README*

---

*来源：[github.com/google-labs-code/design.md](https://github.com/google-labs-code/design.md)，Google Labs，2026年4月21日*