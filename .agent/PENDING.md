## 📋 频率配置

| 任务类型 | 频率 | 上次执行 | 建议下次 |
|----------|------|----------|----------|
| ARTICLES_COLLECT | 每轮 | 2026-05-19 | 2026-05-20 |
| PROJECT_SCAN | 每轮 | 2026-05-19 | 2026-05-20 |

## ⏳ 待处理任务
<!-- 状态：⏳待处理 🔴执行中 ✅完成 ⏸️等待窗口 ❌放弃 ⬇️跳过 -->

## 📌 Articles 线索
<!-- 本轮无新增文章时必须填写：下轮可研究的具体方向 -->

### 本轮新增文章方向（已写入仓库）
1. **Anthropic 基础设施噪声与 Benchmark 有效性** — 资源配比差异导致 6pp 分数差异，低于 3pp 的 Leaderboard 差距不值得信赖
2. **SWE-Smith 训练数据规模化** — 50k 实例 × 128 repos，与基础设施噪声研究形成「数据规模 → 评测公平性」对话

### 下轮可研究的方向
- AnySearch 发现的新方向：SwarmRelay（E2E 加密 A2A 消息）、ACP（Agent Control Protocol over WebSocket）
- OpenAI Responses API WebSocket mode 深入分析（40% 延迟降低的技术实现）
- Cursor Composer 2.5 的新能力

## 🔄 本轮同步闭环情况
- ✅ Articles 与 Projects 主题关联：基础设施噪声（Anthropic）→ SWE-Smith（训练数据规模）形成评测「数据+环境」完整闭环
- ✅ 原文引用：Article 5+ 处，Project 4 处
- ✅ 源追踪已更新：sources_tracked.jsonl

## ⚠️ 已知问题
- Tavily API 今日配额耗尽（432 限制），全程使用 AnySearch
- AnySearch 无需 API Key，匿名模式可用，效率高于 Tavily
- agent-browser snapshot 超时，优先使用 AnySearch + web_fetch