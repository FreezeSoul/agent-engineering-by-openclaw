# HyperFrames：让 AI Agent 用 HTML 写出视频的开源框架

**GitHub**: https://github.com/heygen-com/hyperframes  
**Stars**: 31,341 ⭐  
**Language**: TypeScript (87.3%), JavaScript (11.4%)  
**License**: Apache 2.0  
**Cluster**: `tool-use/video-generation`

---

## 核心命题

HyperFrames 解决了一个根本问题：AI Agent 生成的视频通常是"黑箱输出"——你无法控制渲染过程，不知道发生了什么，只能接受最终结果。

它的解法反直觉：**让 Agent 写 HTML，而不是生成视频**。

> "Write HTML. Render video. Built for agents."

---

## 架构设计：HTML 作为视频的声明式描述

HyperFrames 的核心洞察是：HTML 是一种**声明式、确定性、可调试**的媒体描述语言。

传统的 AI 视频生成是"黑箱渲染"：
1. 输入 Prompt
2. 模型生成视频（过程不可见）
3. 输出 MP4（无法编辑中间状态）

HyperFrames 的流程是"透明渲染"：
1. Agent 编写 HTML + CSS + JS（确定性文本）
2. HyperFrames 执行浏览器渲染引擎
3. 输出确定性 MP4（逐帧可验证）

```
AI Agent → 编写 HTML/CSS/JS → HyperFrames 渲染引擎 → 确定性 MP4
```

这意味着：Agent 写的代码**本身就是视频**，而不是"生成视频的指令"。

---

## 19 个 Skills：让 Agent 学会视频制作的工作流

HyperFrames 不是一个单一工具，而是一个**技能体系**。它提供了 19 个可加载的 Skills，每个 Skill 对应一个特定视频制作场景：

| Skill | 适用场景 |
|-------|---------|
| `/hyperframes` | 入口 Skill，自动路由到合适的子 Skill |
| `/product-launch-video` | 产品发布视频（从 URL 或简介生成） |
| `/faceless-explainer` | 无人物解说视频（AI 生成所有视觉元素） |
| `/pr-to-video` | GitHub PR → 变更说明视频 |
| `/talking-head-recut` | 人物视频 + 设计图形叠加 |
| `/motion-graphics` | 动态图形（logo sting、lower-third 等） |
| `/music-to-video` | 音乐 → 节拍同步视频 |

这些 Skills 的设计哲学是：**让 Agent 理解视频制作的工作流，而不只是执行单一任务**。

Agent 学会了：先规划 → 写 HTML → 调试 seekable animations → 添媒体 → lint → 预览 → 渲染。

---

## 为什么对 AI Coding 有意义

传统的 AI Coding 输出的是**代码产物**——文本文件，可审查、可修改、可版本控制。

但用户需要的往往不是代码，而是**代码的最终效果**。HyperFrames 让 Agent 能直接交付"视频"这种最终产物，同时保留"代码即产物"的可审计性。

一个具体的场景：你想让 Agent 为你的开源项目制作一个 product demo 视频。传统路径：
1. Agent 写代码
2. 人录制屏幕
3. 人工剪辑

HyperFrames 路径：
1. `px skills add heygen-com/hyperframes`
2. `Using /hyperframes, create a 10-second product intro with a fade-in title...`
3. Agent 生成 HTML → 渲染 MP4

**关键区别**：整个过程是**可复现、可调试、可修改**的，因为中间产物是 HTML 代码。

---

## 技术细节：seekable animations

HyperFrames 视频的核心是 **seekable animations**——可在任意时间点精确定位的动画。这需要：

- 确定性渲染（同样的 HTML + 时间输入 → 同样的输出）
- 逐帧控制（pauseAt()、playAt() 等精确时间操作）
- 无音频依赖的时序（音频单独轨道，同步绑定）

这与传统的"关键帧动画"不同——seekable animations 是**基于时间的函数式描述**，而非关键帧插值。

---

## 多 Agent 协作场景

HyperFrames 的 Skills 设计天然支持多 Agent 协作：

1. **规划 Agent**：决定视频结构和内容
2. **代码 Agent**：编写 HTML/CSS/JS
3. **审核 Agent**：lint + 预览验证
4. **渲染 Agent**：执行最终 MP4 渲染

每个 Agent 的输出都是下一个 Agent 的输入，整个流程是**声明式管道**而非线性执行。

---

## 竞品对比

| 方案 | 控制力 | 可审计性 | 多 Agent 支持 |
|------|--------|----------|--------------|
| **HyperFrames** | ✅ 完整（HTML 即代码）| ✅ 完整（源码可查）| ✅ 原生 |
| **Remotion** | ✅ 完整（React）| ✅ 完整 | ❌ 需自行集成 |
| **Runway/Pika** | ❌ 黑箱 | ❌ 无源码 | ❌ 不适用 |
| **ffmpeg + AI** | ⚠️ 脚本控制 | ⚠️ 可审计但复杂 | ⚠️ 需自行编排 |

---

## 引用来源

> "HyperFrames is an open-source framework for turning HTML, CSS, media, and seekable animations into deterministic MP4 videos. Use it locally with the CLI, from AI coding agents with skills, or as the rendering core behind hosted authoring workflows."

> "The skills teach agents the HyperFrames production loop: plan the video, write valid HTML, wire seekable animations, add media, lint, preview, and render. They work with Claude Code, Cursor, Gemini CLI, Codex, and other coding agents that support skills."

> "Write HTML. Render video. Built for agents." — [HyperFrames README](https://github.com/heygen-com/hyperframes)

---

## 结论

HyperFrames 代表了一种**AI Coding 产物扩展**的思路：不让 Agent 生成黑箱输出，而是让 Agent 生成**声明式描述语言**（HTML），再通过确定性渲染得到最终产物。

这个思路的价值在于：保留了代码的可审计性，同时交付了用户真正需要的媒体格式。对于需要交付视频内容的 AI Coding 场景，这是一个值得关注的工具。

**安装**：`px skills add heygen-com/hyperframes`  
**文档**：[hyperframes.heygen.com](https://hyperframes.heygen.com/)
