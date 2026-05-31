# juanjuandog/FinSight-AI：股票研究 Agent 的弹性工程架构

> AI 股票研究 Agent，以弹性工程为核心 —— Redis Lua single-flight、pgvector RAG、版本化报告、可信溯源、RAG 评估。

**Stars**：769 | **Fork**：25 | **Language**：Java (72.6%) + JavaScript + Python | **License**：MIT

---

## 核心命题

FinSight-AI 做了一件很多金融 AI 项目没做的事：**把 Agent 当成基础设施来设计，而不是当成玩具来演示**。它展示了一个生产级股票研究 Agent 应该长什么样——不是单次问答，而是多阶段可恢复的工作流，配合幂等性控制、失败恢复、版本化报告、和 RAG 评估的完整闭环。

笔者认为，这才是 AI Agent 在垂直领域落地的正确姿势：**先有弹性，再谈智能**。

---

## 关键架构

### 工作流弹性设计

FinSight 把股票研究分解为五个可独立恢复的阶段：

| 阶段 | 关键机制 |
|------|---------|
| Data ingestion | 文档解析、格式化 |
| Metric recalculation | 指标重新计算 |
| Document indexing | 向量化索引构建 |
| Intelligence build | 情报构建 |
| AI report generation | 报告生成 |

每个阶段都有**状态机 + 重试 + 死信状态 + 超时接管调度器**。任何一个阶段失败后，下一次触发会从断点恢复，而不是从头重来。

### 并发控制（Redis Lua single-flight）

```lua
-- Redis Lua single-flight lease伪代码
local key = KEYS[1]
local holder = redis.call('GET', key)
if holder then
    return holder -- 已有人持有，直接返回
end
redis.call('SET', key, requester_id, 'NX', 'EX', ttl)
return nil  -- 获得锁
```

这是金融场景的标配：同一标的的并发请求只需要一次真实查询，其他请求等待结果复用。**fencing token** 进一步防止惊群效应。

### 可信缓存（Trustworthy AI Cache）

```
contextHash + dataSnapshotHash → reportVersion → Redis/PostgreSQL backed reuse
```

缓存失效不再依赖时间窗口，而是依赖**数据快照哈希**。当底层数据变了，缓存自然失效；当数据没变，报告版本直接复用。这是 CRAG（Corrective RAG）的工程实现。

### RAG 与评估

| 维度 | 实现 |
|------|------|
| **Hit Rate** | RAG 命中率评估 |
| **Evidence Coverage** | 证据覆盖率 |
| **Answer Coverage** | 答案覆盖率 |
| **Hallucination Risk** | 幻觉风险检测 |
| **Conclusion Consistency** | 结论一致性 |
| **Confidence Calibration** | 置信度校准 |

这六维评估框架来自学术 RAG 评估实践，工程化进了工作流里。

---

## 技术栈

- **Spring Boot**：API + Dashboard
- **PostgreSQL**：JSONB 存储 + 全文搜索 + pgvector 向量检索
- **Redis**：缓存 + single-flight lease + fencing token
- **RabbitMQ**：任务队列
- **pgvector**：向量嵌入存储，支持混合检索（BM25 + dense vector）

---

## 竞品对比

| 维度 | FinSight-AI | 通用 RAG Agent |
|------|------------|----------------|
| **工作流恢复** | 状态机 + 阶段级 checkpoint | 通常无 |
| **并发控制** | Redis Lua single-flight | 通常无 |
| **缓存失效** | 数据快照哈希驱动 | TTL驱动 |
| **评估** | 六维 RAG 评估 | 通常无 |
| **领域深度** | 股票研究专用 | 通用 |

笔者认为 FinSight-AI 的真正价值在于**把工程弹性放在了模型智能之前**。很多 Agent 项目强调模型多强、上下文多长，但生产环境里真正让你崩溃的是并发、缓存失效、和任务中断。FinSight 先解决了这些问题，再谈 AI 报告生成。

---

## 适用场景

- **量化研究团队**：需要自动化新闻/研报/公告的结构化提取 + 生成
- **投资机构**：多数据源的证据溯源报告，监管合规
- **RAG 系统工程师**：六维 RAG 评估框架可直接复用

---

## 引用

> *"FinSight turns filings, financial reports, research notes, market data, and company events into source-grounded answers and versioned AI research reports."*

— [GitHub README](https://github.com/juanjuandog/FinSight-AI)

---

##资源

- GitHub：https://github.com/juanjuandog/FinSight-AI
- Stars：769（2026-05）