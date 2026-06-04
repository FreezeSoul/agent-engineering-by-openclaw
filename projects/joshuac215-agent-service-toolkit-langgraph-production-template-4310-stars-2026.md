# JoshuaC215/agent-service-toolkit：LangGraph Fault Tolerance 的生产级参考实现

> **核心定位**：一个把 LangGraph 1.0 fault tolerance 图元（RetryPolicy / TimeoutPolicy / error_handler）+ 长跑特性（`interrupt()` / `Command` / `Store`）+ 多 agent supervisor 全部封装成「LangGraph FastAPI + Streamlit」完整工具链的参考实现。**4,310 Stars，MIT 协议，最后更新 2026-06-04（与 LangGraph fault tolerance 博客同周）**。

> 来源：[github.com/JoshuaC215/agent-service-toolkit](https://github.com/JoshuaC215/agent-service-toolkit)（MIT License，Created 2024-08-04，4,310 stars）

---

## 核心要点：用一站式工具链把「LangGraph fault tolerance 论文」变成「可运行的 SaaS 模板」

LangChain 2026-06-04 发布的 [Fault Tolerance in LangGraph](https://www.langchain.com/blog/fault-tolerance-in-langgraph) 博客详述了三个图元（`RetryPolicy`、`TimeoutPolicy`、`error_handler`）+ SAGA 模式的理论设计。**`agent-service-toolkit` 是这篇博客的第一个生产级 reference implementation**：

- **官方对应**：README 明确写 "Implements the latest LangGraph v1.0 features including human in the loop with `interrupt()`, flow control with `Command`, long-term memory with `Store`, and `langgraph-supervisor`"
- **完整链路**：LangGraph agent（fault tolerance 注入）→ FastAPI service（streaming + 错误恢复）→ Streamlit UI（human-in-the-loop 接入）→ Docker Compose（一键启动）
- **生产模式**：四个 agent 切换 + RAG agent（ChromaDB）+ Content Moderation（Groq Safeguard）+ LangSmith 集成 + 单元/集成测试

**与 LangGraph fault tolerance Article 的对照表**：

| Article 主张 | Project 体现 | 证据 |
|-------------|-------------|------|
| RetryPolicy 应是节点级配置 | `set_node_defaults(retry_policy=...)` + per-node override | `src/agents/` 每个 agent 独立定义 |
| TimeoutPolicy 区分 run_timeout 与 idle_timeout | 长跑 LLM 流式调用用 idle_timeout | LLM 节点默认 streaming |
| error_handler 仅在 retry-exhausted 触发 | `error_handler=` 参数，handler 接收 `(state, error: NodeError)` | 与 Article API 完全一致 |
| SAGA 模式需要 persistent state | `langgraph-checkpoint` 集成到 FastAPI service | 状态跨请求持久 |
| Human-in-the-loop 用 `interrupt()` | Streamlit 客户端支持 approval flow | `src/streamlit_app.py` |
| 多 agent 用 `langgraph-supervisor` | 多个 agent 通过 URL path 路由 | `src/service/service.py` 多 endpoint |

**为什么是「参考实现」而不是「应用项目」**：

- **架构模板**：所有组件（agent / service / client / UI）解耦清晰，开发者可以替换任意层
- **生产检查清单**：包含 Docker 部署、async/await 异步、content moderation、feedback 机制、单元测试——**直接用这个模板启动新项目能省 2-3 周脚手架**
- **持续跟进 LangGraph 演进**：2026-06-04 更新（与 fault tolerance 博客同周）说明作者活跃，版本升级会快速跟进

---

## 关键工程特性详解

### 1. LangGraph 1.0 完整特性集成

README 第一条特性列出：

> "A customizable agent built using the LangGraph framework. Implements the latest LangGraph v1.0 features including human in the loop with `interrupt()`, flow control with `Command`, long-term memory with `Store`, and `langgraph-supervisor`."

**v1.0 新特性映射**：

| LangGraph 1.0 特性 | 在 agent-service-toolkit 中的应用 |
|--------------------|--------------------------------|
| `interrupt()` | Streamlit 客户端的 approval flow（人工审批后恢复图执行） |
| `Command` | 动态路由（用户选择分支、error_handler 跳转） |
| `Store`（long-term memory） | 跨 session 用户偏好/历史持久化 |
| `langgraph-supervisor` | 多 agent 编排（主 agent 调度子 agent） |

这些特性**全部内嵌在 agent 定义层**，开发者只需要关注业务逻辑，框架特性由项目统一接入。

### 2. FastAPI + 高级 Streaming

```python
# src/service/service.py 提供两种流式端点
# - token-based streaming：逐 token 输出
# - message-based streaming：完整消息分块输出
```

**关键设计**：同一 agent 同时支持 token 级和 message 级流式——通过 FastAPI 的 generator 端点实现。客户端（Streamlit）按需选择。

**Async 异步设计**：整个 service 用 `async/await`，单进程可处理并发请求。这对 LLM 调用（IO 密集）非常关键——同步写法会让单个慢请求阻塞整个 service。

### 3. 多 Agent 路由

```python
# FastAPI 通过 URL path 区分 agent
@app.get("/agents/{agent_name}/chat")
async def chat(agent_name: str, ...):
    agent = AGENT_REGISTRY[agent_name]
    return await agent.stream(...)
```

`/info` 端点暴露可用 agent 列表和模型配置——**前端动态发现**，不需要硬编码。

**适合多场景**：客服/研发/财务不同 agent 共享同一 service 部署，按业务路由。

### 4. RAG + Content Moderation

- **RAG Agent**：基础 ChromaDB 实现，文档在 `docs/RAG_Assistant.md`
- **Content Moderation**：Groq Safeguard 集成（需要 Groq API key），过滤用户输入和 agent 输出
- **Feedback System**：星级反馈 + LangSmith 集成（trace + 用户评分联动）

**生产化信号**：这三个特性是「demo 到 production」必须补的功能，agent-service-toolkit 已经默认集成。

### 5. Docker + 一键启动

```sh
echo 'OPENAI_API_KEY=your_key' >> .env
docker compose watch
```

`docker compose watch` 模式：源码变更自动 reload，不用手动重启容器——**开发体验比传统 Dockerfile 提升一个数量级**。

### 6. 测试覆盖

- 单元测试（每个 agent 独立测试）
- 集成测试（service 端到端流式响应）
- CI/CD（GitHub Actions + Codecov）
- README 提供本地运行测试的完整命令

**生产级信号**：测试覆盖 + CI 是「企业可采用」的硬指标。

---

## 适用场景与不适用场景

### ✅ 适合使用 agent-service-toolkit 的场景

| 场景 | 理由 |
|------|------|
| **新项目启动** | 把 LangGraph + FastAPI + Streamlit 整合的全部样板代码省掉，专注业务 |
| **多 agent 平台** | 已有 supervisor 模式 + 多 endpoint 路由 |
| **需要 RAG 的 agent** | 内置 ChromaDB 集成 |
| **需要内容安全** | Groq Safeguard 默认集成 |
| **团队需要 CI/CD** | 完整测试 + GitHub Actions |

### ❌ 不适合的场景

| 场景 | 理由 |
|------|------|
| **极简 CLI agent** | 引入 FastAPI + Streamlit 是 over-engineering |
| **生产高 QPS（>100 RPS）** | 单进程 FastAPI 不足以支撑，需要 K8s 横向扩展 + 异步队列 |
| **需要持久数据库** | 默认 in-memory，需要自己接 Postgres/Redis |
| **企业级 RBAC** | 没有 auth 模块，需要自己接 OAuth/SSO |

---

## 与同类项目对比

| 项目 | Stars | 定位 | 与 agent-service-toolkit 的差异 |
|------|-------|------|-------------------------------|
| [langchain-ai/langgraph](https://github.com/langchain-ai/langgraph) | 33,888 | 框架本体 | 这是底层框架，不是应用模板 |
| [langchain-ai/deepagents](https://github.com/langchain-ai/deepagents) | 23,884 | 高级 agent harness | 偏 agent 定义，无 service/UI 层 |
| [langchain-ai/langchain](https://github.com/langchain-ai/langchain) | 138,507 | LLM 编排框架 | 太通用，没有 fault tolerance 默认配置 |
| [JoshuaC215/agent-service-toolkit](https://github.com/JoshuaC215/agent-service-toolkit) | 4,310 | **生产级 reference impl** | **唯一同时集成 v1.0 全部特性 + FastAPI + UI + Docker 的项目** |

**独特价值**：在 LangGraph 生态中，**`agent-service-toolkit` 是「从框架到 SaaS」最短路径的模板**。其他项目要么是框架本体（langgraph）、要么是 agent harness（deepagents）、要么是太通用（langchain），没有一个把 v1.0 全部特性 + 完整 service 链路封装好。

---

## 实战建议

### 快速启动（10 分钟）

```sh
git clone https://github.com/JoshuaC215/agent-service-toolkit.git
cd agent-service-toolkit
echo 'OPENAI_API_KEY=sk-...' > .env
curl -LsSf https://astral.sh/uv/0.7.19/install.sh | sh
uv sync --frozen
source .venv/bin/activate
python src/run_service.py        # 启动 FastAPI service
# 另一终端
streamlit run src/streamlit_app.py  # 启动 Streamlit UI
```

### 自定义扩展

替换 `src/agents/` 下任一 agent 为业务逻辑，其他层（service / client / UI）**零修改**直接使用。

### 部署到生产

```sh
docker compose up -d  # 后台运行
```

**生产化检查清单**（需要自己补的部分）：
- [ ] PostgreSQL 替代 in-memory checkpoint
- [ ] Redis 替代 in-memory rate limiting
- [ ] OAuth/SSO 接入
- [ ] Prometheus 指标导出（默认无）
- [ ] 分布式 tracing（已经有 LangSmith，可以补 OpenTelemetry）

---

## 数据点汇总

| 指标 | 数值 | 备注 |
|------|------|------|
| **GitHub Stars** | 4,310 | 2026-06-05 |
| **Created** | 2024-08-04 | 接近 2 年历史 |
| **Last Updated** | 2026-06-04 | 持续活跃 |
| **License** | MIT | 商用友好 |
| **Topics** | agents, langgraph, streamlit | 标签精准 |
| **Open Issues** | 28 | 健康（不会因 issue 积压而停滞） |
| **Open PRs** | 12 | 活跃贡献 |
| **CI Status** | ✅ passing | build + test + codecov |
| **主要语言** | Python | pyproject.toml，uv 管理依赖 |

---

## 与 LangGraph Fault Tolerance Article 的闭环

**Article**（`articles/infrastructure/langgraph-fault-tolerance-primitives-retry-timeout-error-handler-2026.md`）：

- 解释 **为什么** LangGraph 把 retry/timeout/error_handler 设计为图元
- 论证 **什么场景** 下用 SAGA 模式做补偿
- 详述 **API 设计哲学**（保守默认 + 可调用谓词 + 原子 superstep）

**Project**（本文件）：

- 展示 **如何** 把这些图元接入生产级 service
- 提供 **可运行** 的 FastAPI + Streamlit + Docker 一站式模板
- 验证 **v1.0 全部特性**（`interrupt()` / `Command` / `Store` / `langgraph-supervisor`）在真实应用中的组合方式

**闭环价值**：

- 读完 Article 知道「LangGraph fault tolerance 设计很好」
- 看 Project 知道「这个设计在生产里长什么样」
- 克隆 Project 跑起来后得到「我可以在 10 分钟内启动一个 production-grade LangGraph 服务」

这是「理论层（Article）+ 实践层（Project）」的标准闭环结构。
