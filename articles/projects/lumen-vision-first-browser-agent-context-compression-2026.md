# Lumen：视觉优先的浏览器 Agent 与上下文压缩工程实践

## 🔍 项目概览

**GitHub**: [omxyz/lumen](https://github.com/omxyz/lumen)  
**定位**: 视觉优先的浏览器 Agent，采用 screenshot → model → action 的纯视觉感知循环  
**核心差异化**: 无 DOM 解析、无选择器依赖，通过两层上下文压缩实现长时任务稳定运行

---

## 🎯 目标用户

| 维度 | 描述 |
|------|------|
| **用户类型** | 需要自动化浏览器操作场景的 Agent 开发者和研究人员 |
| **水平要求** | 有 Node.js 开发经验，了解浏览器自动化基础概念 |
| **典型场景** | Web 任务自动化、跨站点数据采集、登录态页面操作、需要长期运行的多步骤浏览器流程 |

---

## 💡 核心价值

> 在 WebVoyager 基准测试中，Lumen 达到 **25/25 (100%)** 成功率，而同期对比的 Stagehand 仅为 19/25 (76%)。

Lumen 的核心价值不在于"更聪明"，而在于**更稳定**——通过视觉优先架构和两层上下文压缩，即使面对 100+ token 消耗的复杂任务，也能保持可靠的执行轨迹。

---

## 🔬 技术架构

### 视觉感知循环

```
┌──────────────────────────────────────┐
│           PerceptionLoop             │
│                                        │
│  ┌────────┐   ┌────────┐   ┌────────────────┐   ┌────────┐
│  │ Chrome │──▶│Screenshot│──▶│History Manager │──▶│ Build  │
│  │  (CDP) │   │         │   │                │   │Context │
│  └────────┘   └─────────┘   │  tier-1: compress│   │+ state │
│                              │  tier-2: summarize│   │+ KB    │
│                              └────────┬────────┘   │+ nudge │
│                                        │             └────┬───┘
│                                        ▼                  │
│                              ┌─────────────────┐          │
│                              │   Action Router │◀─────────┤
│                              │   click/type/scroll/goto   │
│                              └────────┬──────────────────┘
└──────────────────────────────────────┘
```

核心流程：
1. **Screenshot** — 通过 CDP 捕获浏览器视口截图
2. **History Manager** — 当上下文超过阈值时执行两层压缩
3. **Build Context** — 组装系统提示（含持久状态、SiteKB 导航规则、stuck nudges）
4. **Action Router** — 将模型输出的动作调度到 Chrome（click/type/scroll/goto/terminate）

### 两层上下文压缩（这是本文的核心技术亮点）

> "History compression — tier-1 screenshot compression + tier-2 LLM summarization at 80% context utilization."

Lumen 的压缩不是单一策略，而是**双层递进**：

| 层级 | 触发条件 | 压缩方式 | 目标 |
|------|---------|---------|------|
| **Tier-1** | 上下文使用率 > 60% | 丢弃旧截图，保留文本历史 | 快速缓解，保留关键决策链 |
| **Tier-2** | 上下文使用率 > 80% | LLM summarization 生成摘要 | 深度压缩，将长轨迹凝练为高密度信息块 |

这个设计直接对应 Anthropic 提出的 **attention budget** 概念——当 token 消耗触及 budget 边界时，系统有明确的降级策略，而不是等到溢出才被动压缩。

### 视觉优先 vs DOM 解析

Lumen 的架构假设：视觉理解比 DOM 解析更鲁棒。

```
视觉优先优势：
├─ 不依赖页面结构变化（DOM 随时可能变）
├─ 不需要维护复杂的选择器（选择器脆弱易碎）
├─ 跨站点泛化能力强（不绑定特定网站结构）
└─ 与人眼工作方式一致（人不会读 DOM，而是看页面）
```

对比传统方案（如 Playwright/Puppeteer 的 DOM 交互）：
- **传统方案**：精确但脆弱，页面改版即失效
- **Lumen**：粗粒度但鲁棒，适应页面变化

### 验证门控（Termination Gate）

当模型调用 `task_complete` 时，Lumen 不会立即退出，而是通过 **ModelVerifier** 检查截图确认任务真正完成：

```javascript
import { Agent, UrlMatchesGate, ModelVerifier, AnthropicAdapter } from "@omxyz/lumen";

// URL 模式匹配
verifier: new UrlMatchesGate(/\/confirmation\?order=\d+/)

// 模型验证（使用小模型判断）
verifier: new ModelVerifier(
  new AnthropicAdapter("claude-haiku-4-5-20251001"),
  "Complete the checkout flow",
)
```

> 这是防止"模型误判任务完成"的关键安全机制——在真实环境中，模型经常因为看到类似 UI 就判断任务完成，而不检查实际结果。

### Session 持久化与恢复

```javascript
// 保存
const snapshot = await agent.serialize();
fs.writeFileSync("session.json", JSON.stringify(snapshot));

// 恢复
const data = JSON.parse(fs.readFileSync("session.json", "utf8"));
const agent2 = Agent.resume(data, { model: "anthropic/claude-sonnet-4-6", browser: { type: "local" } });
```

结合 `writeState` 持久化结构化 JSON，即使经过上下文压缩，Agent 仍能保留关键状态信息。

---

## 📊 性能对比

| 指标 | Lumen | browser-use | Stagehand |
|------|-------|-------------|-----------|
| **成功率** | **25/25 (100%)** | 25/25 (100%) | 19/25 (76%) |
| **平均步数** | 14.4 | 8.8 | 23.1 |
| **平均耗时** | 77.8s | 109.8s | 207.8s |
| **平均 Token** | 104K | N/A | 200K |

> 注：所有框架统一使用 Claude Sonnet 4.6 作为 Agent 模型

---

## 🔗 与 Cursor Self-Summarization 的关联

这是本文推荐 Lumen 的核心原因——**Cursor 的训练侧方案与 Lumen 的工程侧方案形成完美互补**：

| 维度 | Cursor Composer (训练侧) | Lumen (工程侧) |
|------|------------------------|----------------|
| **压缩时机** | 预定义的 token 触发点（固定长度） | 80% utilization 阈值触发 |
| **压缩方式** | RL 训练让模型学会自我总结 | tier-2 LLM summarization |
| **压缩粒度** | 模型"学会"保留什么 | 工程规则决定保留什么 |
| **上下文保持** | 通过训练内化 | 通过 session state 外化 |
| **适用场景** | 长期任务（数百个 action） | 中期任务（数十个 action） |

**关键洞察**：Cursor 的 self-summarization 是"让模型自己决定保留什么"（训练产物），Lumen 的 tier-2 compression 是"通过工程规则决定保留什么"（系统设计）。两者并不矛盾——未来的浏览器 Agent 完全可能同时具备：训练出来的 summarization 能力 + 可配置的系统压缩阈值。

---

## ⚠️ 已知局限

1. **步数偏高**：平均 14.4 步 vs browser-use 的 8.8 步，说明视觉循环的采样密度更高但效率略低
2. **Token 消耗不透明**：browser-use 未报告 Token 消耗，无法完整对比上下文压缩效率
3. **纯本地 Chrome**：依赖本地 Chrome 实例，生产环境需要额外配置 CDP 端点
4. **npm ESM-only**：不支持 CJS，对旧项目迁移有门槛

---

## 🚀 快速上手

```bash
npm install @omxyz/lumen
```

```javascript
import { Agent } from "@omxyz/lumen";

// 最简使用
const result = await Agent.run({
  model: "anthropic/claude-sonnet-4-6",
  browser: { type: "local" },
  instruction: "Go to news.ycombinator.com and tell me the title of the top story.",
});

console.log(result.result);
```

```javascript
// 带验证器（推荐用于生产）
import { Agent, ModelVerifier, AnthropicAdapter } from "@omxyz/lumen";

const agent = new Agent({
  model: "anthropic/claude-sonnet-4-6",
  browser: { type: "local" },
  verifier: new ModelVerifier(
    new AnthropicAdapter("claude-haiku-4-5-20251001"),
    "Verify the checkout flow completed",
  ),
});
```

---

## 📚 技术引用

> "History compression — tier-1 screenshot compression + tier-2 LLM summarization at 80% context utilization."
> — [Lumen README](https://github.com/omxyz/lumen)

> "Vision-only loop — screenshot → model → action(s) → screenshot. No DOM scraping, no selectors."
> — [Lumen README](https://github.com/omxyz/lumen)

> "Lumen runs with SiteKB (domain-specific navigation tips) and ModelVerifier (termination gate) enabled."
> — [Lumen README](https://github.com/omxyz/lumen)

---

**关联文章**: [Cursor Composer Self-Summarization: 长时任务的训练侧压缩方案](../deep-dives/cursor-composer-self-summarization-long-horizon-2026.md) — 训练让模型学会自我压缩；本文 Lumen 是工程侧的压缩实践

**适用场景**：需要稳定执行多步骤浏览器任务的开发者；研究上下文压缩工程的实践者；需要处理登录态/反爬/长流程 Web 任务的 Agent 框架构建者