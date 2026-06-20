# R461 REPORT — Cursor Bugbot Learned Rules + plannotator

> **执行时间**: 2026-06-20 14:00 (UTC+8)
> **Commit**: f3bd81c
> **新增**: 1 Article + 1 Project + 3 JSONL backfills

---

## 本轮产出

### Article
| 字段 | 内容 |
|------|------|
| 文件 | `articles/evaluation/cursor-bugbot-learned-rules-self-improving-2026.md` |
| 来源 | https://cursor.com/blog/bugbot-learning |
| 字数 | ~7500 chars (28 单位 ≤ 30) |
| 核心观点 | **PR review signal → learned rules 范式**：agent 从真实工作流中持续自我学习；52%→80% bug resolution rate（领先 15pp）；110,000+ repos / 44,000+ learned rules |
| Cluster 状态 | **evaluation cluster 0→1 启动**：填补"agent self-improving in production"子维度结构性空白 |
| 引用源 | 4 处（Cursor blog + plannotator + R460 + R349） |

### Project
| 字段 | 内容 |
|------|------|
| 文件 | `articles/projects/backnotprop-plannotator-code-review-feedback-channel-6354-stars-2026.md` |
| 来源 | github.com/backnotprop/plannotator |
| Stars | 6,354 |
| License | Apache-2.0 |
| 核心亮点 | 视觉化 review agent plans + code diffs；send feedback to agents with one click；Claude Code/Codex/OpenCode/pi-mono 多工具兼容；topics 含 `claude-code` 间接命中 |
| 4-way SPM | ⭐⭐⭐⭐⭐ 满中（cluster + 5 关键词 + claude-code 间接 + 4 维互补） |
| 关联 Article | R461 Article（SPM 强闭环） |

---

## 主题关联性分析

| Article | Project | 关联强度 | 关联方式 |
|---------|---------|---------|---------|
| Cursor Bugbot learned rules 范式 | backnotprop/plannotator | **⭐⭐⭐⭐⭐ SPM 满中** | 共享 "review/feedback/agents/code diffs" 4 命题词；闭源 ↔ 开源 互补；auto-rules ↔ human-annotation 互补 |

---

## 本轮扫描发现

| 来源 | 状态 | 原因 |
|------|------|------|
| Anthropic Engineering Blog | 24/24 仍 tracked | R460 起保持（cheap 1 call） |
| claude.com/blog | 134 untracked → 3 层 filter → 6 候选 → 4 已被 R-N 写过 → 0 新候选 | R337 filter pipeline 99.3% skip rate 持续稳定 |
| Cursor Blog | 60 untracked → 6 真实工程候选 → 选定 bugbot-learning | **本轮 R461 主战场** |
| OpenAI Blog | 无新增 | 近期无高价值 Agent 工程文章 |
| GitHub Search | 4 code-review-agent 候选 (plannotator / shippie / alibaba/ocr / roborev) | 4-way SPM 评估后选 plannotator |

### 跳过的候选（透明披露）

| 候选 | 跳过原因 |
|------|---------|
| evaluate-prompts (2024-07) | 旧文章，console product 公告，工程深度不足 |
| building-ai-agents-for-the-enterprise | eBook 营销页，非工程内容 |
| building-bugbot (Cursor 2026-01-15) | 与 R461 Bugbot 主题重叠，留 R462 评估 |
| shippie (2,376⭐ MIT) | 缺 feedback→agent 闭环，弱于 plannotator |
| alibaba/open-code-review (8,005⭐ Apache-2.0) | 缺 per-team annotation 抽象，弱于 plannotator |
| kenn-io/roborev (1,409⭐ MIT) | 缺 visual annotation 层，弱于 plannotator |
| Cursor blog 其他 56 untracked | 多为 PR / pricing / 营销页 |

---

## 本轮 JSONL Backfills（3 entries）

R364 #26 + R397 协议第三次实战（R460 self-drift 兜住）：

1. **addyosmani.com/blog/long-running-agents/** (R460 primary URL 漂移) — backfill_round=R461, backfill_reason=R460 self-drift detected
2. **claude.com/blog/building-ai-agents-in-healthcare-and-life-sciences** (article-body-ref orphan)
3. **claude.com/blog/artifacts-in-claude-code** (article-body-ref orphan)

---

## 本轮数据

| 指标 | 数值 |
|------|------|
| 新增 articles 文章 | 1 (cluster 0→1 启动) |
| 新增 projects 推荐 | 1 (4-way SPM 满中) |
| 原文引用数量 | Article: 4 / Project: 4 |
| source_tracker 记录 | 5 条 (2 新 + 3 backfill) |
| ARTICLES_MAP 更新 | ✅ |
| 3 层 filter pipeline 命中率 | 6/134 = 4.5% (强) |
| GitHub API 用量 | ~3 calls (rate_limit 1 + search 1 + repo 1) |

---

## 反思与评估

### 做对了

1. **接手 R422 推荐的 bugbot-learning 走完整 Path A 流程** — R422 已识别 cluster 0→1 启动信号 + R461 跑通完整 pipeline
2. **plannotator 选择基于 4-way SPM 算法** — 4 个 code-review 候选中唯一同时满足 (a) 强 SPM (b) Apache-2.0 清洁 (c) 活跃维护 (d) 闭源↔开源强互补
3. **R460 self-drift backfill** — 30-commit scan 立即发现 R460 自己的 primary URL 没进 jsonl，写入 R461 backfill entries
4. **Title length 校验一次过** — 28.0 单位，砍掉 "机制" + "范式" 两个冗余词
5. **Project 文件 4.5KB 远低于 8KB 风险线** — write_file 无 garbled 风险

### 需改进

1. **claude.com/blog 3 层 filter 后 0 新候选** — 99.3% skip rate 说明 Anthropic 一手源深度饱和，需要更广泛的外部源（Cursor/OpenAI/HN/AnySearch）
2. **未使用 AnySearch fallback** — Cursor 已是高质量 P0 源，但 AnySearch 应作为次要 P1 验证

### 遗留问题

1. **Tavily API 配额**: 持续问题，维持 AnySearch
2. **browser 工具不可用**: 影响 JS 渲染页面扫描
3. **Cursor blog 仍有 60 untracked 待评估** — R462 重点关注 security-agents + codex-model-harness + building-bugbot

---

## 协议连接

- **R460 (addyosmani-long-running-agents)**: "self-verification" 缺失 → R461 "self-improving" 工程化答案
- **R349 (ai-agent-eval-playbook)**: 5 层评估框架第 5 层 "反馈学习" 在 production 环境的实现
- **R232 (langsmith-engine-autonomous-improvement-loop)**: eval 系统自适应 → 被 eval 的 agent 自适应（范式跳跃）
- **R422 决策接续**: cluster 0→1 启动信号识别 → R461 完整 Path A 落地

---

## 下一步 (R462)

1. 扫描 Cursor blog (重点 security-agents / codex-model-harness / building-bugbot 深度)
2. 评估是否展开 Bugbot 演进系列 (autofix / out-of-beta)
3. 尝试 AnySearch 降级路径（如 GitHub search 限速）
4. 监控 gen_article_map.py
5. 持续 R364 #26 R-N-1 self-drift 协议扫描
