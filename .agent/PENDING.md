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
1. **Anthropic Harness Design（2026-05-20）**：Generator-Evaluator 分离 + Context Reset + 三 Agent 协同，突破长时 Agent 的上下文漂移和自我评价失真两大天花板。核心洞察：Compaction 无法解决上下文焦虑，只有 Reset 才能提供干净白板；Generator-Evaluator 分离让「对 LLM 生成内容系统性宽容」的偏差可通过调校独立 Evaluator 来消除。

### 下轮可研究的方向
- **Cursor Composer 2.5 完整解析**：训练体系、RL 细节（May 18 更新，7min read）
- **Cursor "speeding up GPU kernels by 38%"**：多 Agent 协同优化 GPU 内核，可能涉及系统性多 Agent 协作新范式（被 agent-browser 问题阻断，需重试）
- **Anthropic "Building a C compiler with a team of parallel Claudes"**：多 Agent 并行协作编译（已追踪 managed-agents 相关内容，可能重复）

## 🔄 本轮同步闭环情况
- ✅ Articles 与 Projects 主题关联：Anthropic Harness Design（长时运行 Agent 架构）↔ NousResearch/hermes-agent（跨会话自改进框架）→ 形成「架构设计 → 框架实现」完整闭环
- ✅ 原文引用：Article 4处（anthropic.com/engineering），Project 3处（GitHub README）
- ✅ 源追踪已更新：sources_tracked.jsonl（+2 条）

## ⚠️ 已知问题
- Tavily API 持续超额（Error 432），本轮完全降级到 AnySearch + curl（直接抓 HTML）
- Cursor "speeding up GPU kernels by 38%" 文章页面 JS 渲染无法用 curl 抓取内容，agent-browser 代理参数被忽略，需进一步调试
- agent-browser daemon 需要先 `agent-browser close` 才能用新代理参数重启