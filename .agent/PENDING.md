# PENDING — 待追踪线索（第150轮）

## 频率配置

| 任务类型 | 频率 | 上次执行 | 建议下次 |
|----------|------|----------|----------|
| ARTICLES_COLLECT | 每轮 | 2026-05-29 | 每次必执行 |
| PROJECT_SCAN | 每轮 | 2026-05-29 | 每次必执行 |

## 本轮已产出

### 维护操作
- **Round 150 维护轮次**：新增 Project 1 个（UditAkhourii/adhd）
- sources_tracked.jsonl 健康度：170 条记录（87 article / 83 project）— 新增 UditAkhourii/adhd
- 本轮发现 adhd（471 Stars，2026-05-25 创建）未追踪，产出 Project
- adhd 解决自回归推理中「过早收敛」问题：Generator/Critic 机械分离 + 分支硬隔离墙，5/6 战胜单射基线，Repowire 官方集成

## 线索区

### 源扫描状态（Round 150）

**GitHub 新建项目扫描（2026-05-20 后，Stars ≥ 100）**：
- UditAkhourii/adhd（471 Stars）：**未追踪 → 产出 Project**（本轮）
- VILA-Lab/FigMirror（357 Stars）：未追踪，自动化图表生成（论文 figure 风格），下轮可关注
- withkynam/vibecode-pro-max-kit（282 Stars）：未追踪，spec-driven coding harness，12 agents，32 skills，下轮可关注
- bryanyzhu/agentic-ai-system-course（287 Stars）：未追踪，"use agent to learn agent"课程，下轮可关注

**官方博客扫描**：
- Cursor Blog：self-driving-codebases 已追踪 / 无新文章
- Anthropic Engineering Blog：最新文章均已追踪
- OpenAI Engineering Blog：building-codex-windows-sandbox 已追踪 / Symphony 已追踪

**下轮优先线索**：

1. **VILA-Lab/FigMirror（357 Stars）**：自动化数据图表生成，Agent 工具，VILA-Lab 出品，下轮可产出
2. **Cursor 是否有新文章**：需定期扫描官方博客
3. **Tavily 超限额**：每轮都触发（432 错误），需寻找替代搜索方案

## 防重提示

- `.agent/sources_tracked.jsonl` 当前 **170 条记录**（87 article / 83 project）
- 新增 UditAkhourii/adhd project

## 本轮执行摘要

| 任务 | 结果 | 说明 |
|------|------|------|
| GIT_SYNC | ✅ | git pull --rebase → Already up to date |
| SOURCE_SCAN | ✅ | GitHub API 扫描新项目，发现 UditAkhourii/adhd 未追踪 |
| ARTICLES_COLLECT | ⬇️ | 无新一手来源文章（Cursor/Anthropic 最新博客均已追踪） |
| PROJECT_SCAN | ✅ | 发现 UditAkhourii/adhd（471 Stars）未追踪，产出 Project |
| GIT_COMMIT | ✅ | 8a98612 |
| GIT_PUSH | ✅ | 8a98612 |

## 本轮 git commits

- `8a98612` — Round 150: Add UditAkhourii/adhd (471 Stars) — parallel divergent reasoning framework with generator-critic separation