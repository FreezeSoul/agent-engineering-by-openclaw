# 从 65 TPS 到 1000 TPS：OpenAI WebSocket Mode 如何消除 Agent 循环的瓶颈

> 当推理速度提升 15 倍之后，API 开销反而成了 Agent 性能的新敌人。

2025 年 11 月之前，OpenAI 的 Responses API 面临一个结构性悖论：旗舰模型（GPT-5、GPT-5.2）推理速度约为 65 tokens/s，API 服务端开销可以"隐藏"在 GPU 推理时间之后。但到了 2026 年，GPT-5.3-Codex-Spark 通过 Cerebras 专用硬件将推理速度提升至 1000 TPS（峰值 4000 TPS）时，API 开销从隐藏变成了主角——用户不是在等 GPU，而是在等 CPU 处理 API 请求。

这不是某个环节的性能问题，而是整个交互模式的结构性问题。

## 问题根源：每个请求都在重复"重建巴别塔"

在 HTTP 模式下，Responses API 将每个 Codex 请求视为独立的对话。即使对话内容 99% 未变，API 仍需执行以下操作：

1. **重新解析完整对话历史** — tokenization 和网络调用
2. **重新验证所有历史请求** — 安全分类器每次都跑一遍
3. **重新路由模型请求** — 即使结果完全可预测
4. **重新建立网络连接** — 每个请求都是新的 HTTP 握手

当推理只需 1ms 时，这些"隐藏成本"可能只占 10%；但当推理只需 0.1ms 时，这些成本占据了 90%。这不是优化级别的问题，而是架构级别的重新设计。

## 解决方案：持久连接 + 状态缓存

OpenAI 的设计思路非常清晰：既然对话状态在多次请求间高度稳定，那就**只在连接生命周期内缓存一次**，而不是每个请求都重建。

### 核心技术决策：选择 WebSocket

团队评估了 WebSocket 和 gRPC bidirectional streaming 两种方案，最终选择 WebSocket 的理由是：

> "WebSocket 作为简单的消息传输协议，用户无需改变 Responses API 的输入输出形状。它对开发者友好，且与现有架构适配最小。"

这体现了 OpenAI 的 API 设计哲学：**让新协议适应旧接口，而非让开发者适应新协议**。

### 关键技术实现

#### 1. 连接级缓存（Connection-scoped In-memory Cache）

当 WebSocket 连接建立后，服务器维护一个连接作用域内的内存缓存，存储：

- 前一个 response 对象
- 历史输入/输出 items
- 工具定义和命名空间
- 可复用的采样 artifacts（如已渲染的 token）

```python
# 服务端伪代码（概念模型）
class WebSocketConnection:
    def __init__(self):
        self.cache = ResponseStateCache()  # 连接级缓存
    
    def handle_response_create(self, request):
        if request.previous_response_id:
            # 从缓存获取，而不是重建
            state = self.cache.get(request.previous_response_id)
        else:
            state = self.cache.create_new()
        
        # 优化后的安全分类器只检查新输入
        security_result = self.fast_classifier.check(request.new_input_only)
```

#### 2. 增量安全验证（Incremental Safety Validation）

传统模式下，安全分类器需要处理完整对话历史。在 WebSocket 模式下，分类器**只检查新输入**，因为历史状态已在缓存中验证过。

```python
# 优化对比
# HTTP 模式：每次都验证完整历史
security.check(full_conversation_history)

# WebSocket 模式：只验证新增部分
security.check(new_input_only)  # 历史已在缓存中验证
```

#### 3. 异步 Token 渲染缓存（In-memory Token Rendering Cache）

已渲染的 token 在内存中追加，无需每次重新 tokenize。这在长对话场景下收益尤为明显。

### 架构对比

| 维度 | HTTP 轮询模式 | WebSocket 持久连接 |
|------|-------------|-----------------|
| 连接建立 | 每个请求独立握手 | 一次建立，长期复用 |
| 状态管理 | 每个请求独立解析 | 连接级内存缓存 |
| 安全验证 | 每次全量历史 | 仅新增输入 |
| Token 渲染 | 每次完整解析 | 增量追加缓存 |
| 网络开销 | 高（重复握手+全量传输）| 低（增量传输+复用）|
| 适用场景 | 低频/短对话 | 高频/长对话 Agent |

## 性能数据：40% 延迟改善，覆盖整个生态

WebSocket mode 带来了实打实的性能提升：

- **OpenAI Codex**：主要 traffic 已切换到 WebSocket，延迟显著改善
- **Vercel AI SDK**：集成后延迟降低 **40%**
- **Cline**：多文件工作流 **39%** 加速
- **Cursor**：OpenAI 模型最高 **30%** 加速
- **GPT-5.3-Codex-Spark**：达到 1000 TPS 设计目标，峰值 4000 TPS

这些数字来自真实生产环境的 alpha 测试反馈，团队在两个月内完成了从原型到生产部署的全流程。

## 开发者体验：API 形状不变，行为自动优化

WebSocket mode 最重要的设计决策之一是**不改变 API 形状**：

```python
# 开发者无需改变 API 调用方式
response = client.responses.create(
    model="gpt-5.3-codex-spark",
    previous_response_id=previous_response.id,  # 相同参数
    input="继续修复这个 bug"
)

# 底层自动使用 WebSocket 持久连接
# - 第一次：建立连接，缓存状态
# - 后续：复用缓存，增量传输
```

这意味着现有的 Codex/Cline/Cursor 集成**无需任何代码修改**，只要更新到新版本 SDK 就能自动获得性能提升。

## 深层含义：传输层正在成为 Agent 性能的关键战场

WebSocket mode 的发布揭示了一个重要趋势：**随着模型推理速度越来越快，传输层正在成为 Agent 性能的新瓶颈**。

这个规律不局限于 OpenAI：

- 当 GPU 推理从 100ms 优化到 10ms，API 开销从 10% 变成 90%
- 当模型响应时间从秒级降到毫秒级，网络延迟和序列化开销成为主角
- 持久连接、增量更新、状态缓存这些 Web 应用优化的经典技术，正在被引入 AI Agent 领域

笔者认为，这代表了 Agent 架构演进的一个新阶段：**从模型能力驱动，到系统效率驱动**。

## 工程启示录

1. **架构匹配是关键**：当推理速度提升 15 倍时，原有架构已不再适用，需要重新设计传输层
2. **协议设计优先于性能调优**：选择 WebSocket 而非 gRPC，是因为它保留了 API 兼容性，这体现了"协议服务于接口"的工程哲学
3. **增量优化比全量重写更安全**：在已有系统上叠加缓存层，而非推翻重来，降低了升级风险
4. **SDK 升级应该是透明的**：WebSocket mode 能在 SDK 版本更新后自动生效，这意味着架构团队在设计时已经将向后兼容作为核心约束

---

**引用来源**：
- [Speeding up agentic workflows with WebSockets in the Responses API](https://openai.com/index/speeding-up-agentic-workflows-with-websockets/) — OpenAI Engineering Blog, April 22, 2026
- [Responses API Documentation](https://developers.openai.com/api/docs/models/gpt-5.3-codex) — OpenAI Developers

**相关技术**：[持久连接](/articles/orchestration/agent-stateful-continuation-transport-layer-architecture-2026.md) | [A2A 协议](/articles/orchestration/a2a-protocol-one-year-production-retrospective-2026.md)