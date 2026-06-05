# LiveKit Agents: Realtime Voice AI Agent Framework

## 基本信息

| 字段 | 值 |
|------|-----|
| **Repo** | livekit/agents |
| **Stars** | 10.7k |
| **Contributors** | 382 |
| **语言** | Python |
| **License** | Apache 2.0 |
| **分类** | 基础设施 / Agent Framework |
| **发现日期** | 2026-06-05 |

## 一句话定位

**开源 WebRTC 框架，用于构建实时、多模态语音 AI Agent，支持电话呼入/呼出、MCP 集成和自托管部署。**

## 核心功能

### 1. 实时多模态交互

- **语音优先**：内置 VAD（Voice Activity Detection）、STT、LLM、TTS 完整pipeline
- **视频支持**：AI Avatar 集成（Tavus、Bithuman、LemonSlice）
- **语义打断检测**：Transformer 模型判断用户是否说完了，减少误打断

### 2. 灵活的模型集成

```
# 支持多种组合方式
AgentSession(
    vad=silero.VAD.load(),
    stt="deepgram/nova-3",      # 多种 STT 选项
    llm="openai/gpt-4.1-mini",  # 任何 LLM
    tts="cartesia/sonic-3"      # 多种 TTS 选项
)
```

LiveKit 提供统一的 Inference API，可以混用不同提供商的 STT/LLM/TTS。

### 3. MCP 原生支持

一行代码接入 MCP Server：

```python
# 官方提供 LiveKit Docs MCP Server
# 给 AI coding assistant 接入最新文档和代码搜索
```

### 4. 电话集成（Telephony）

- 呼入：用户打电话给 Agent
- 呼出：Agent 主动打电话给用户
- 与 SIP 协议深度集成

### 5. 任务调度与分发

```python
# 内置 dispatch APIs 连接终端用户到 Agent
@server.rtc_session()
async def entrypoint(ctx: JobContext):
    session = AgentSession(...)
    await session.start(agent=agent, room=ctx.room)
```

### 6. 自托管部署

- **LiveKit Server**：生产级 WebRTC 服务器，GitHub star 30k+
- 完全开源，可跑在自己的服务器上
- 官方推荐的生产架构：

```
用户端 (Web/Mobile)
    ↓ WebRTC
LiveKit Server (自托管)
    ↓
LiveKit Agents (你的 Agent Logic)
    ↓
STT/LLM/TTS Provider
```

## 工程亮点

### 亮点 1：WebRTC 原生

LiveKit 本身是业界领先的 WebRTC 服务器（30k+ stars），Agents 框架继承了这一能力：
- 低延迟实时通信
- 穿越 NAT/Symmetric NAT
- 媒体录制和回放
- 多人多 Agent 场景

### 亮点 2：技能与文档双轨制

官方为 AI coding assistant 提供了两个工具：

| 工具 | 作用 | 使用方式 |
|------|------|---------|
| **LiveKit Docs MCP Server** | 提供最新 API 文档、代码搜索、示例 | MCP 协议接入 |
| **LiveKit Agent Skill** | 架构指导和最佳实践 | `npx skills add livekit/agent-skills` |

两者配合：Skill 教「怎么设计」，MCP 提供「怎么实现」。

### 亮点 3：多 Agent 协作示例

```python
class IntroAgent(Agent):
    async def on_enter(self):
        # 收集用户信息
        self.session.generate_reply(instructions="greet the user and gather information")

    @function_tool
    async def information_gathered(self, context, name, location):
        # 交接给 StoryAgent
        story_agent = StoryAgent(name, location)
        return story_agent, "Let's start the story!"
```

支持 Agent 之间通过 function tool 进行交接（handoff）。

## 与同类对比

| 框架 | 实时性 | 电话集成 | MCP | 自托管 | Stars |
|------|--------|---------|-----|--------|-------|
| **LiveKit Agents** | ✅ WebRTC原生 | ✅ SIP/电话 | ✅ | ✅ | 10.7k |
| **OpenAI Realtime API** | ✅ | ❌ | ❌ | ❌ | - |
| **Letta** | ❌ | ❌ | ❌ | ✅ | 17.5k |
| **CrewAI** | ❌ | ❌ | ✅ | ✅ | 37.6k |

**定位差异**：LiveKit Agents 专注于**实时语音/视频**场景，而不是通用 Agent 编排。

## 应用场景

1. **客服机器人**：电话呼入 + AI 对话 + 知识库检索
2. **AI Avatar**：视频会议中的虚拟主播
3. **语音助手**：智能家居、车内语音交互
4. **远程面试助手**：实时转录 + 智能问答
5. **多语言同传**：实时语音翻译

## 技术栈

```
Python Agents Framework
    ├── VAD: Silero
    ├── STT: Deepgram (nova-3)
    ├── LLM: OpenAI / Anthropic / 任意
    ├── TTS: Cartesia (sonic-3)
    └── WebRTC: LiveKit Server
```

## 关键数据

| 指标 | 值 |
|------|-----|
| Stars | 10.7k |
| Contributors | 382 |
| Python 版本 | 3.9+ |
| 安装大小 | 轻量（插件化） |

## 链接

- GitHub: https://github.com/livekit/agents
- 文档: https://docs.livekit.io/agents/
- MCP Server: https://docs.livekit.io/mcp
- Agent Skill: https://github.com/livekit/agent-skills

## 点评

LiveKit Agents 代表了**实时语音 AI Agent**这一细分方向的工程化成熟度。相比通用的 Agent 框架（LangChain/CrewAI），它解决的是更具体的问题：如何在真实的实时通信场景中部署 AI Agent？

WebRTC 原生 + 电话集成 + MCP 支持这三个特性，让它在「需要与人实时对话」的场景下有明显优势。而 Apache 2.0 许可证 + 自托管部署能力，则让它在企业市场有吸引力。

值得关注的趋势：随着 GPT-4o 级别的实时语音 API 成熟，**实时多模态 Agent** 会成为新战场。LiveKit Agents 提前在这个方向上建立了完整的开源方案。