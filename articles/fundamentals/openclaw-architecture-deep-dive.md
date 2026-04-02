# OpenClaw Architecture Deep Dive: Gateway/Channel/LLM 三层设计

> 来源：eastondev
> 评分：4.5/5（实践 4 / 独特 4 / 质量 5）
> 关联 FSIO 文章：OpenClaw + AI Gateway 的架构设计

## 核心洞察

作者花了3天完整梳理 OpenClaw 源码，发现设计非常巧妙：

> "Gateway manages sessions, Channel handles routing, LLM manages interfaces—the three-layer architecture is crystal clear."

## 三层架构

### Gateway Layer：会话管理中心

**职责**：
- 用户会话的完整生命周期管理
- 消息队列和调度（优先级策略）
- 认证和权限控制
- WebSocket 长连接维护

**Session 对象包含**：
```javascript
conversationHistory  // 对话历史
context             // 上下文变量
state               // 当前状态
channelInfo         // 来源平台信息
```

**关键设计**：per-channel-peer isolation——同一用户在 WhatsApp 和 Telegram 上的 Session 独立，不互相污染。

**消息调度队列**：
- 并发控制：最多同时处理 N 个请求
- 错误重试：指数退避（1s → 2s → 4s）

### Channel Layer：平台适配器

**职责**：
- 不同平台消息格式适配（WhatsApp/Telegram 格式不同）
- 路由规则（私信还是群聊、是否@机器人）
- 事件处理（接收/发送/错误）

**最巧妙的设计**：增加新平台？只改 Channel 层，其他层不动。

### LLM Layer：模型接口

**职责**：
- 统一 Provider 接口（Claude/GPT/本地模型调用方式一致）
- Tool calling（Function Calling）
- 流式响应处理
- MCP Server 集成

## 完整消息流程

```
用户发送消息
    ↓
Channel Layer：接收 webhook，标准化为内部格式
    ↓
路由决策：检查 DM/群聊、@mention、用户权限
    ↓
Gateway：找到（或创建）用户 Session，加入队列
    ↓
LLM：根据配置选择 Provider（如 Anthropic），发送对话上下文
    ↓
响应返回：LLM → Gateway → Channel → 用户
```

## 为什么三层设计

**单层设计**在小规模下没问题，但 OpenClaw 需要：
- 多平台（WhatsApp、Telegram、Gmail...）
- 多模型（Claude、GPT、本地模型...）
- 数百到数千用户会话管理

没有分层的话，改一处可能影响所有功能——完全不可维护。

## 扩展实践

### 自定义 Channel（Discord 集成）

只需关注 Channel 层，按照适配器模式实现即可。

### 自定义 Provider（Kimi 集成）

只需关注 LLM 层，实现统一的 Provider 接口。

## 一句话总结

> OpenClaw 三层架构解析：Gateway 管会话、Channel 管适配、LLM 管接口——想加新平台只动 Channel，想换模型只动 LLM，Gateway 完全不用碰。

## 原文

https://eastondev.com/blog/en/posts/ai/20260205-openclaw-architecture-guide/

## 标签

#community #OpenClaw #architecture #gateway #channel #llm
