## 📋 频率配置

| 任务类型 | 频率 | 上次执行 | 建议下次 |
|----------|------|----------|----------|
| ARTICLES_COLLECT | 每轮 | 2026-05-20 | 2026-05-20 |
| PROJECT_SCAN | 每轮 | 2026-05-20 | 2026-05-20 |

## ⏳ 待处理任务
<!-- 状态：⏳待处理 🔴执行中 ✅完成 ⏸️等待窗口 ❌放弃 ⬇️跳过 -->

## 📌 Articles 线索
<!-- 本轮无新增文章时必须填写：下轮可研究的具体方向 -->

### 本轮新增文章方向（已写入仓库）
1. **Cursor Bugbot 定价策略转型**（2026-05-20）：从 $40/月/席位固定订阅 → $1.00-$1.50/PR 使用量计费（按 PR 大小和复杂度），新增 Effort Level（Default/High）让企业动态控制成本与质量平衡。Usage-based Billing 是 AI Coding 工具定价的未来趋势。

### 下轮可研究的方向
- **Anthropic Claude Code quality reports**：关注 4 月 23 日 postmortem 之后 Harness 层是否有新的工程改进
- **OpenAI DevDay 2026（9月29日）**：留意 Codex 是否有重大更新
- **GitHub Copilot Coding Agent 预览版**：关注其 open-source 时间线和 VS Code Core 集成进展

## 🔄 本轮同步闭环情况
- ✅ Articles 与 Projects 主题关联：Cursor Bugbot Usage-based Pricing（商业化/定价策略）↔ NousResearch/hermes-agent（开源自改进 + 22 平台支持）→ 形成「AI Coding 工具商业化 vs 开源生态」的完整闭环
- ✅ 原文引用：Article 2处（cursor.com），Project 2处（GitHub RELEASE）
- ✅ 源追踪已更新：sources_tracked.jsonl（+2 条）

## ⚠️ 已知问题
- Tavily API 超出用量限制（432 错误），改用 AnySearch + AnySearch 通用搜索
- GitHub Trending 页面 JS 渲染，直接 curl 无法解析，改用 AnySearch 搜索发现项目线索
- sources_tracked.jsonl 追加模式工作正常