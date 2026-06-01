# JuliusBrussee/caveman：让 AI Agent 用「洞穴语言」燃烧一半的 Token

> **核心命题**：caveman 是一个 Claude Code skill，它让 AI 用洞穴人风格说话——结果是把输出 Token 砍掉 65-75%，同时保持 100% 技术准确性。这个项目的成功揭示了一个重要的工程原理：**LLM 的输出噪音远大于输入噪音，减少废话不等于降低质量**。

---

## 一句话概括

caveman 通过「语言压缩」而不是「模型降级」来降低 AI 编程成本——同样的模型、同样的任务、Token 消耗砍半。

**GitHub**: https://github.com/JuliusBrussee/caveman  
**Stars**: 63,207 | **Forks**: 3,546 | **语言**: JavaScript (63%), Python (28%)  
**License**: MIT  
**最新版本**: v1.8.2 (2026-05-12)

---

## 核心机制：洞穴人风格的工程原理

### 四档语言压缩模式

| 模式 | 风格 | Token 节省 | 适用场景 |
|------|------|-----------|---------|
| **lite** | 去掉语气词 | ~40% | 快速任务，不需要完整句子 |
| **full（默认）** | 洞穴人说话 | ~65% | 生产编码，完整表达 |
| **ultra** | 电报风格 | ~75% | 超长任务，最大化压缩 |
| **wenyan** | 文言中文 | ~70%+ | 中文项目，古文爱好者 |

### Full 模式示例

传统 Agent 输出：
> "I've analyzed the codebase and found that the issue is in the authentication middleware. The problem appears to be that the token validation is not correctly handling the edge case where the token has expired but the refresh token is also missing. Let me walk through the potential solutions and then implement the most appropriate fix for this scenario."

caveman 输出：
> "issue in auth middleware. token validation no handle edge case where token expired but refresh token missing too. let me try fix."

技术准确性：✅ 完全相同  
Token 节省：~60%

**README 原文引用**：
> "🪨 why use many token when few token do trick — A Claude Code skill (also Codex, Gemini, Cursor, Windsurf, Cline, Copilot, 30+ more) that makes agent talk like caveman — cuts ~75% of output tokens, keeps full technical accuracy. Brain still big. Mouth small."

---

## 为什么这个方向有效：三个工程原理

### 原理 1：LLM 输出噪音远大于输入噪音

当你让模型「解释清楚」和「写得简洁」时，模型在「解释」模式下会生成大量连接词、缓冲句、语气词——这些在大多数编程场景下完全不影响输出质量。

**笔者的判断**：这不是让模型变笨，而是让模型「别假装礼貌」。编程 Agent 的输出是给机器看的，不需要人类社交语言。

### 原理 2：Token 成本不对称性

- **输入 Token**：模型可以参考历史上下文、一次性发送大量信息，边际成本低
- **输出 Token**：每个 Token 都要完整计算生成，边际成本高

caveman 专攻输出端——减少 65% 的输出 Token = 直接降低 65% 的 API 成本，而不是降级模型或减少上下文。

### 原理 3：Token 预算是一种隐式 Harness

当 Agent 的 Token 预算紧张时，它被迫更直接地表达——这个压力反而让输出更清晰。caveman 把这个「被迫」变成了默认行为，而不是等模型遇到预算墙才被迫压缩。

---

## 技术实现：不是一个普通 Prompt

caveman 是一个**安装即用的 Claude Code skill**，而不是简单的 prompt 模板：

```bash
# 安装
npx caveman install

# 切换模式
caveman lite    # 轻量模式
caveman full    # 默认洞穴人模式  
caveman ultra   # 极端压缩
caveman wenyan  # 文言中文
caveman off     # 恢复正常
```

**技术细节**：
- 30+ AI 编程工具兼容：Claude Code、Codex、Gemini、Cursor、Windsurf、Cline、Copilot 等
- Skill 系统：Claude Code 的 `/caveman` 命令直接激活
- 一行开关：不需要改代码或配置，一句话切换风格

---

## 适用场景与不适用场景

### ✅ 强烈推荐

- **长时间运行的编码任务**：每次循环节省 65% Token，累积效果显著
- **大规模代码库修改**：多轮编辑、多文件修改，Token 节省放大
- **成本敏感的团队**：不需要换模型或减少上下文，零代价节省

### ⚠️ 不适合

- **需要完整解释的场景**：代码审查报告、文档写作，输出不只是代码
- **多 Agent 协作**：如果其他 Agent 需要解析 caveman 的输出，语言压缩可能造成沟通障碍
- **中文正式文档**：caveman 的压缩风格影响可读性

---

## 与其他 Token 优化方案的对比

| 方案 | 原理 | Token 节省 | 代价 |
|------|------|-----------|------|
| **caveman** | 输出语言压缩 | 65-75% | 风格改变（可接受）|
| **模型降级** | 换更小的模型 | 30-50% | 质量下降 |
| **上下文裁剪** | 减少历史信息 | 20-40% | 可能丢失重要上下文 |
| **MCP 工具化** | 外部工具替代生成 | 变化大 | 需要额外集成工作 |

**笔者的判断**：caveman 是目前成本最低、质量损失最小的 Token 优化方案——不需要换模型、不需要改架构，一行命令切换。对于预算敏感的生产项目，这个节省比例是惊人的。

---

## 背后的工程哲学

caveman 的成功暗示了一个更大的趋势：**AI Coding 的效率瓶颈不在模型能力，而在通信开销**。

当 Agent 输出 100 个 Token，其中 60 个是「礼貌性的废话」时，这 60 个 Token 的成本完全由你承担，但没有贡献任何技术价值。caveman 揭示了一个简单的事实：

> **「说得少」和「说得好」不矛盾——在大多数编程任务中，它们甚至是同一件事。**

---

## 快速上手

```bash
# 试用 Claude Code
npx caveman install

# 下一次 Claude Code 对话中，Agent 自动使用洞穴人风格
# 或者手动激活
/caveman
```

或者直接访问：https://getcaveman.dev

---

*数据来源：[JuliusBrussee/caveman](https://github.com/JuliusBrussee/caveman)，63K Stars，MIT License，2026 年 4 月发布。*