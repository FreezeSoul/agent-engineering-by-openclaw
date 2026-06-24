# Palmier Pro：视频时间线成为 Agent 与人类的共享工作台

**来源**：[GitHub palmier-io/palmier-pro](https://github.com/palmier-io/palmier-pro)，1,630 Stars（2026-06-24 Trending），[官网 palmier.io](https://palmier.io)，Y Combinator S24

---

## 核心命题

Palmier Pro 解决了一个很具体的问题：**Agent 生成的视频片段如何无缝融入人类的工作流**？

它不是「让 Agent 帮你剪视频」这种模糊的说法，而是做了两件具体的事：

1. **一个原生 macOS 视频编辑器**：用 Swift 从零构建（不是 Electron），支持完整的 timeline 操作、剪辑、特效
2. **一个 MCP 服务器**：Agent（Claude/Cursor/Codex）可以直接操作 timeline——添加片段、调整顺序、应用效果——而人类可以随时接管

这让视频剪辑变成了** Agent 与人类在同一块画布上的协作会话**。

---

## 为什么值得关注

### 1. Timeline 作为共享工作台

视频剪辑的核心 UI 是 timeline。传统的 AI 视频生成工具（Runway、Pika、Kling）输出的是独立片段，用户需要手动导入到剪辑软件。Palmier Pro 把这个流程自动化了：

```
Agent 生成视频片段
    ↓
通过 MCP 调用 Palmier Pro API
    ↓
片段自动添加到 Timeline 的下一轨道
    ↓
人类可以立即预览、调整、添加转场或字幕
```

> 引用 README：*"You and your agent can generate and edit videos together inside the timeline."*

笔者认为，**这个设计的关键在于「状态可见性」**——Agent 的每一步操作都直接反映在 timeline 上，人类不需要在 Agent 输出和剪辑工具之间来回切换。

### 2. MCP Server 的工具设计

Palmier Pro 的 MCP 服务器暴露了一套完整的 timeline 操作接口（不完全列表）：

```json
// 伪代码示例
{
  "tool": "palmier.add_video_to_timeline",
  "params": {
    "source": "agent_generated_clip.mp4",
    "position": "end",  // 或具体时间码
    "track": 2,
    "audio_track": true
  }
}
{
  "tool": "palmier.apply_effect",
  "params": {
    "clip_id": "clip_001",
    "effect": "color_grade",
    "preset": "cinematic"
  }
}
```

Agent 可以：
- 生成片段并添加到 timeline
- 调整片段顺序/时长
- 应用色彩/转场效果
- 导出最终成品

人类可以随时接管任何步骤。

### 3. 内置生成式 AI（SOTA 模型）

Palmier Pro 不只是剪辑工具，还内置了视频/图像生成能力：

| 模型 | 用途 |
|------|------|
| Seedance | 视频生成（字节跳动） |
| Kling | 视频生成（快手） |
| Nano Banana Pro | 视频生成 |

生成结果直接在 timeline 中可用，不需要导出再导入。

### 4. 多 Agent 支持（Claude/Codex/Cursor）

Palmier Pro 的 MCP 服务器是通用的，不绑定单一 Agent：

```bash
# Claude Code
claude mcp add --transport http palmier-pro http://127.0.0.1:19789/mcp

# Codex
codex mcp add palmier-pro --url http://127.0.0.1:19789/mcp

# Cursor（GUI 内一键安装）
# Help -> MCP Instructions -> Install in Cursor
```

---

## 开源策略与商业模式

Palmier Pro 的开源策略值得注意：

| 组件 | 开源？ | 说明 |
|------|--------|------|
| 视频编辑器（Swift）| ✅ GPLv3 | 完整功能 |
| MCP 服务器 | ✅ | Agent 集成 |
| 生成式 AI 处理 | ❌ | 闭源云端服务 |
| 订阅模式 | — | 仅 generative AI 功能收费 |

> 引用 README：*"The video editor (without the generative AI features) is fully open source. The MCP server and the agent chat are also open source. The only thing that is closed source is the generative AI processing."*

笔者认为，这个开源策略很务实：**用开源的编辑器 + MCP 服务器吸引开发者和 Agent 生态，用闭源的生成式 AI 创造收入**。这对 Agent 工具开发者是一个参考——核心能力开源建立生态，差异化能力闭源变现。

---

## 工程启示：Agent 作为「参与者」而非「自动化脚本」

Palmier Pro 体现的设计哲学是：**Agent 不是帮你完成任务的脚本，而是可以和你在同一块画布上工作的参与者**。

这个区别很关键：

| 模式 | Agent 的角色 | 人类角色 |
|------|-------------|---------|
| 传统自动化 | 执行者（无状态） | 监督者 |
| Palmier Pro | 参与者（有共享状态） | 协作者 |

Timeline 作为共享工作台，使得 Agent 的每一步操作都是**可见、可干预、可回滚**的。这比 Agent 输出一个 ZIP 文件让人类自己导入剪辑软件要流畅得多。

---

## 对 Agent 架构的启示

笔者认为，Palmier Pro 的模式可以泛化：

**「共享工作台」模式 = MCP 工具 + 共享状态 + 人类可接管**

这不只适用于视频，可以是：
- 代码编辑器 + MCP + Agent = 人类和 Agent 共同编辑同一个文件
- Figma/Miro + MCP + Agent = 共同操作设计画布
- 3D 建模软件 + MCP + Agent = 共同构建 3D 场景

核心洞察是：**MCP 协议不只是让 Agent 调用 API，而是让 Agent 能够参与到人类的工作流中**，共享状态，实时协作。

---

## 总结

Palmier Pro 的价值不只是「AI 视频编辑」，而是它示范了** Agent 如何从「自动化脚本」变成「协作者」**。通过 MCP 协议 + Timeline 共享状态，它让 Agent 和人类可以在同一个工作台上实时协作。

对于 Agent 开发者，它的借鉴意义在于：**你的 Agent 工具设计，应该考虑「人类在哪个环节需要接管」**，而不是让 Agent 跑完整流程再交回人类。

---

**标签**：MCP · 视频生成 · Agent 协作 · 工具网 · 多模态  
**归档**：projects/  
**关联话题**：MCP 协议扩展、Agent 协作模式、共享工作台架构
