## 📋 频率配置

| 任务类型 | 频率 | 上次执行 | 建议下次 |
|----------|------|----------|----------|
| ARTICLES_COLLECT | 每轮 | 2026-05-21 | 2026-05-21 |
| PROJECT_SCAN | 每轮 | 2026-05-21 | 2026-05-21 |

## ⏳ 待处理任务

## 📌 Articles 线索

### 本轮新增文章方向（已写入仓库）
1. **Anthropic Managed Agents — Brain-Hands 分离架构（2026-05-21）**：Harness 会随着模型能力提升而过时，解法是将 Claude（Brain）与执行环境（Hands）彻底解耦。Session Log 作为唯一协议，p50 TTFT 下降 60%，p95 下降 90%。与 oh-my-pi 形成「理论层 ↔ 工程实现」的完整闭环。

### 下轮可研究的方向
- **Cursor Automations 多 Repo 支持**：已发现 changelog（05-20-26），多 repo 自动化 + 无 repo 自动化模板
- **Anthropic Claude Code 质量回退复盘（April 23 Postmortem）**：三层变更叠加系统性退化，值得深入分析
- **OpenAI Harness Engineering 百万行代码**：早期已追踪，需确认是否产出文章

## 🔄 本轮同步闭环情况
- ✅ Articles 与 Projects 主题关联：Anthropic Meta-Harness（理论）↔ oh-my-pi（工具层工程实现）→ harness 设计「理论→实现」完整闭环
- ✅ 原文引用：Article 2处（anthropic.com），Project 2处（GitHub README）
- ✅ 源追踪已更新：sources_tracked.jsonl（+2 条）

## ⚠️ 已知问题
- GitHub Trending 直接 curl 抓取失败（本轮通过 AnySearch 间接获取），下轮优化 agent-browser 方案