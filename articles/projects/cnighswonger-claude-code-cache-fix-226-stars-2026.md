# claude-code-cache-fix：修复 Claude Code 成本增加 20 倍的 Prompt Cache Bug

> 项目来源：GitHub Trending · [cnighswonger/claude-code-cache-fix](https://github.com/cnighswonger/claude-code-cache-fix)（226 ⭐，2026-04-06）

## 让人想试的那个点

**你可能正在为 Claude Code 的 resumed sessions 支付 20 倍的费用，却不知道原因。** 这个工具帮你检测并修复这个问题——一个直接的、社区级的补丁，对应 Anthropic 官方 April 2026 postmortem 中记录的第二个改动（B。

---

## 背景：Anthropic 承认的 Bug

在 [Anthropic April 2026 postmortem](https://www.anthropic.com/engineering/april-23-postmortem) 中，官方记录了一个 prompt caching 优化 bug：

> "Instead of clearing thinking history once, it cleared it on every turn for the rest of the session."
> — Anthropic Engineering Blog

这个 bug 导致：每次请求都发送更多 uncached tokens → 成本增加可达 20 倍。

---

## 这个工具做了什么

claude-code-cache-fix 做了两件事：

1. **检测**：识别你的 Claude Code session 是否受这个 bug 影响
2. **修复**：提供补丁或配置建议来规避这个问题

```bash
# 安装后直接运行
npx claude-code-cache-fix
# 或
pip install claude-code-cache-fix
```

---

## 为什么值得关注

### 1. 社区响应的速度

这个项目在 Anthropic 官方 postmortem 发布后迅速出现——从 4月23日官方承认到 4月6日项目创建，只有两周时间。说明社区对 Claude Code 的依赖程度已经足够高，任何影响成本的问题都会立即引发响应。

### 2. 对 Max 计划用户影响最大

如果你是 Max 用户，这个 bug 会直接影响你的用量限额——每次请求的 token 消耗增加了 10-20 倍，限额消耗速度成比例增加。[claude-code-hidden-problem-analysis](https://github.com/ArkNill/claude-code-hidden-problem-analysis) 专门量化了这个问题。

### 3. 验证了官方透明度的价值

Anthropic 选择公开承认三个改动的问题，而不是掩盖。这个透明度的结果是：社区迅速开发了独立验证工具，形成了「官方分析 + 社区复现」的互补关系。

---

## 与本轮主题的关联

本轮 Article 分析了 Anthropic 质量退化事件，其中第二个改动（Prompt Caching Bug）是导致用户成本异常升高的直接原因。这个社区项目是对该改动的直接复现和修复建议。

---

## 引用来源

- [claude-code-cache-fix GitHub](https://github.com/cnighswonger/claude-code-cache-fix)
- [Anthropic April 23 Postmortem](https://www.anthropic.com/engineering/april-23-postmortem)