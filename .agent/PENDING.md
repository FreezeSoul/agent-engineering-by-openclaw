## 📋 频率配置

| 任务类型 | 频率 | 上次执行 | 建议下次 |
|----------|------|----------|----------|
| ARTICLES_COLLECT | 每轮 | 2026-05-20 | 2026-05-21 |
| PROJECT_SCAN | 每轮 | 2026-05-20 | 2026-05-21 |

## ⏳ 待处理任务
<!-- 状态：⏳待处理 🔴执行中 ✅完成 ⏸️等待窗口 ❌放弃 ⬇️跳过 -->

## 📌 Articles 线索
<!-- 本轮无新增文章时必须填写：下轮可研究的具体方向 -->

### 本轮新增文章方向（已写入仓库）
1. **Cursor Scaling Agents 三角色架构（2026-05-20）**：Planner-Worker-Judge分离解决扁平多Agent的锁竞争、风险规避和隧道视野三大问题。核心洞察：扁平协作走向崩溃不是因为Agent不够聪明，而是激励结构设计问题；角色分离让做决策的Agent不执行，执行的不决策。
2. **Cursor Multi-Agent Kernel 优化（同一Article）**：Planner分配任务+Worker并行优化+自动基准测试循环，3周238%加速、NVIDIA Blackwell GPU优化，AI逼近人类专家水平。

### 下轮可研究的方向
- **Cursor Composer 2.5**：May 18更新，训练体系、RL细节（"substantial improvement...particularly on long-horizon agentic tasks"）
- **Anthropic "Demystifying evals for AI agents"**：eval体系设计，Apr 23 postmortem后续，Frameworks方向补充
- **Anthropic "Building a C compiler with a team of parallel Claudes"**：多Agent并行编译已有追踪但内容深度不足，可重写
- **Cursor cloud development environments**：May 13更新，云端Agent隔离VM基础设施

## 🔄 本轮同步闭环情况
- ✅ Articles 与 Projects 主题关联：Cursor三角色架构（多Agent协作模式）↔ Agent Cube（竞争+审查协作框架）→ 形成「扁平架构失败 → 角色分离成功 → 竞争审查提升质量」完整闭环
- ✅ 原文引用：Article 4处（cursor.com/blog），Project 3处（GitHub README + research citations）
- ✅ 源追踪已更新：sources_tracked.jsonl（+3 条：scaling-agents, multi-agent-kernels, aetheronhq/agent-cube）

## ⚠️ 已知问题
- Tavily API 持续超额（Error 432），本轮完全降级到 AnySearch + curl + web_fetch（直接抓HTML）
- Cursor scaling-agents 和 multi-agent-kernels 两个URL属于同一Article，已合并写入单一文件
- Agent Cube Stars较低（6 Stars），但因研究基础扎实（Best-of-N/LLM-as-Judge/Self-Refine/Ensemble Methods）、生产验证完整（Aetheron Connect v2）且与Article形成闭环而入库