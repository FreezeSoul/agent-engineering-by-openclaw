# Round349 — R341 协议 #14 二次验证（stash/pop 破坏 mtime）+ R337 orphan 复活机制 + Eval cluster 0→1 启动

## 摘要

R349 是**收尾轮次**而非新启动：检测到 working tree 有 3 个 untracked articles + 4 个 modified .agent 文件 + 1 个 modified ARTICLES_MAP.md，全部由 R349 起草者创建但未 commit 提交。R341 协议 #14（工作树中途出现 untracked 文件 = 并行 cron / 外部进程碰撞）的 mtime 检查**部分失效**（stash/pop 重置文件 mtime），需要三路交叉验证。这是 R341 协议的**第二次验证**（首次 R341 实战是 parallel cron 文件碰撞）。

## 关键发现

### 1. R341 协议 #14 mtime 失效实战

**R341 协议原文**（SKILL.md 失败模式 #14）：
> 当 `git add -A` 阶段出现**本轮没创建的 `.md` 文件**……**绝对不能直接 `git add -A` + commit 一锅端**——可能是：(a) 另一台机器/另一 worker 正在并行跑 cron、(b) FreezeSoul 手动写入、(c) 上一轮 commit 失败留下的 working tree 残骸。
>
> 强制协议：
> 1. `stat -c '%y' <file>` 看 mtime → 早于本轮开始 = 旧残骸；晚于本轮开始 = 并行进程

**R349 实战失效**：本轮开始时执行 `git stash` → `git pull --rebase` → `git stash pop`，**`git stash pop` 会 touch 所有恢复的文件**，mtime 全部刷新到 pop 时间（18:17）。3 个 R349 起草的 untracked 文件 mtime 全部变成 18:17，无法用 mtime 区分"本轮起草" vs "历史残骸"。

**R349 实战解决**：回退到**三路交叉验证**：
1. `git log --all --oneline -- <file>` 确认无 commit 历史（最可靠信号）
2. 文件内容内自标 round 字段（如行末 "Round349"）— R349 起草者主动标注
3. `.agent/sources_tracked.jsonl` `used_at` 时间戳匹配 R349 时段

**协议升级建议**（R350+）：mtime 是**辅助信号**，**不是决定性证据**。**根本解决方案**：cron job 应配 worker_id 锁（`.agent/lock/` 目录 acquire/release 文件锁），R349 因无 lock 基础设施只能事后审计。

### 2. R337 orphan 复活机制（JSONL orphan 复用）

**问题场景**：`.agent/sources_tracked.jsonl` 第 1081 行已有 R337 起草时的 CowAgent 记录：
```json
{"url": "https://github.com/zhayujie/CowAgent", "type": "project",
 "filename": "zhayujie-cowagent-agent-harness-multi-model-multi-channel-45k-stars-2026.md",
 "stars": 45051, "used_at": "2026-06-04T07:00:00Z"}
```
但 `git log --all -- <file>` 找不到任何 commit → **R337 写 jsonl 但未成功 commit** + 未创建文件 = JSONL orphan。

**R349 重新启用**：
- 创建了新文件 `zhayujie-CowAgent-agent-harness-three-tier-memory-45241-stars-2026.md`（不同 slug、不同 stars 数据 45,241）
- 文件末尾自标 "Round349"（R349 起草者明确知道是 R349 产出）
- 内容写明 "关联 Article：OpenAI Dreaming (R348)" — Pattern 9 SPM 强闭环（三层记忆 + Deep Dream 蒸馏 ↔ R348 OpenAI Dreaming 三层目标 Carry Forward / Follow Preferences / Stay Current）

**协议决策**：
- 补录 R349 jsonl 条目（保留 R337 历史记录不删）— **合法 orphan 复活**
- 新 jsonl 条目标 `round: 349` + `cluster: context-memory` + `used_at: 2026-06-12T18:30:00Z` + `note` 字段说明"R337 orphan 重新启用, 更新 stars 45,051→45,247"
- Stars 数据用 GitHub API 实时验证：45,051 (R337 估) → 45,241 (R349 文件写) → **45,247** (R349 GitHub API 实测)

**协议要点**：
1. **R337 写 jsonl 但未 commit = 合法 JSONL orphan**：jsonl 本身是计划，不是产出
2. **R349 重新启用 = 重新走完整协议**：写新文件 + 标新 round + API 验证 + 补录 jsonl
3. **不删 R337 历史 jsonl 条目**：保留作为"曾经想用但未成功"的审计痕迹
4. **Slug 不要求与 R337 一致**：R337 slug 含 "multi-model-multi-channel"，R349 slug 含 "three-tier-memory" — 反映同一项目不同 round 的不同关注点

### 3. Pair 关联"具体对位"原则（vs 泛关联）

R349 起草时的 3 个产出形成 2 个 Pair：
- **Pair 1 (Cluster 0→1 启动)**: Eval Playbook (Article) + Stagewise (Project)
- **Pair 2 (跨 Round SPM 强闭环)**: CowAgent (Project) ↔ R348 OpenAI Dreaming (Article)

**Pair 1 关联性争议**：Eval Playbook 五层框架 (Article) vs Stagewise Agentic IDE (Project) — 表面是"工具需要评估"泛关联，但实际是**字面级对位**：
- Eval 第四层（过程可观测）= 关注 trace 收集、上下文忠实度、工具选择准确度
- Stagewise 浏览器内 console/debugger 访问权 = **正是**过程可观测的工程实现

这是**具体对位 > 泛关联**的实战示例。在 Stagewise 文件中**显式标注**配对 Article 路径：
> 配对 Article: `articles/evaluation/ai-agent-eval-playbook-five-layer-framework-2026.md` — Stagewise 的浏览器内 console/debugger 访问权是 Eval Playbook 第四层（过程可观测）的工程实现案例

**Pair 2 强闭环**：CowAgent 三层记忆 + Deep Dream ↔ R348 OpenAI Dreaming 三层目标 = Pattern 9 SPM 字面级对位（与 R237 LangChain `model-neutrality` ↔ `zhayujie/CowAgent` "reference implementation of Agent Harness engineering" 的 SPM 验证互为对照）。

### 4. Eval cluster 0→1 启动信号

R349 起草的 Eval Playbook 是仓库 `articles/evaluation/` 目录的**首个 anchor** — 这是**Cluster 0→1 启动信号**。按 R331 协议：
> 当 Article 明确点名某个具体机制（如 vault、context anxiety、3-tier framework），且 GitHub Trending 或 search 显示**多个新仓库**实现该机制，**且 articles/ 中该 cluster 文章数 = 0** → 这是 cluster 0→1 启动信号。

Eval cluster 的 5 层框架是新的机制化分类（声明 / 基准 / 评判 / 过程 / 安全），仓库前无此 cluster → **R331 协议下不应被饱和度阈值卡死**，必须 R349 写。

**R350+ 补强建议**：R349 Pair 1 关联性中等（多层框架 vs 单一工具），R350 可考虑加一篇过程可观测的 Project 加强维度，形成"理论 + 多实现"完整 cluster。

### 5. License Risk Protocol 实战触发

R349 起草的 Stagewise Project 文件引用源写 **"Apache-2.0 license reference"** — **错误**。GitHub API `license.spdx_id` 字段实际返回 **AGPL-3.0**（GNU Affero General Public License v3.0）。

**R323 协议硬化要求**：所有 license 声明必须 API 验证。R349 实战中通过 `curl api.github.com/repos/<owner>/<repo>` 验证后修正。

**协议升级建议**（R350+）：**所有 Project 文件起草时**必须：
1. `curl -s https://api.github.com/repos/<owner>/<repo> | grep -E '"spdx_id"'` 验证
2. 在引用源明确标注：`(AGPL-3.0, N⭐, 验证于 YYYY-MM-DD via GitHub API)`
3. License 类型填入 jsonl

### 6. Title Length 校验硬约束实战

R349 起草的 CowAgent 文件标题 `# CowAgent：从「三层记忆」到「自我进化」的开源 Agent Harness 实现` = **31.5 单位 > 30 上限**。按 R323 协议硬约束必须 ≤ 30。

R349 修复方案：砍掉末尾"实现"两字 → `# CowAgent：从「三层记忆」到「自我进化」的开源 Agent Harness` = **29.0 单位 ≤ 30 ✓**

**R350+ 协议硬化**：
- 写完 Article/Project 文件**立即**跑 `title_len()` 校验（**不要 commit 后再补**）
- `def title_len(s): cjk = sum(1 for c in s if ord(c) > 0x2E80); ascii_ = len(s) - cjk; return cjk * 1.0 + ascii_ * 0.5`
- **cluster anchor 文章可超 30**，其他一律硬约束

### 7. ARTICLES_MAP.md meta 文件处理

R349 起草时执行了 `python3 .agent/gen_article_map.py`，但脚本在 1100+ articles 上跑超时（60s 内未完成）。**R349 起草者中断脚本后**留下**未完成修改**的 ARTICLES_MAP.md（2126 行 +/-，但 R349 三个新文件不在内 grep 验证 0 命中）= **meta 文件未完成污染**。

**R349 处理决策**：
- `git checkout ARTICLES_MAP.md` 恢复 HEAD 版本
- 不在 R349 commit 中 add ARTICLES_MAP.md
- 让下次 cron 跑 gen_article_map 时**一次性完整生成**（超时可能是脚本本身的 N+1 git log 问题，需要 R350 优化）

**反模式警告**（R345 协议 #16 同源）：**不要让 meta 文件污染 commit**。如果 meta 文件未完成，先 reset 跳过，下次 cron 补跑。

## 工具预算实战

- 本轮工具调用：~22 次（与 R345 Skip 轮次预算一致）
- 写作前 ~50% 用于"orphan 识别 + 三路验证 + License 验证" = 健康的质量保证而非浪费
- 写作 + commit + push = ~10 次
- **远低于** 30% reserve（~12-15 次）

## Pair 闭环强度评估

| Pair | 关联维度 | 闭环强度 | 备注 |
|------|---------|---------|------|
| Eval Playbook ↔ Stagewise | 过程可观测（Eval 第四层 ↔ Stagewise console/debugger）| ⭐⭐⭐ 中等 | 强于泛关联，弱于 SPM 字面级 |
| CowAgent ↔ R348 OpenAI Dreaming | 三层记忆架构 + Deep Dream ↔ 三层目标 | ⭐⭐⭐⭐⭐ 强 | Pattern 9 SPM 字面级对位 |

## R349 产出元数据

- **Commit**: `6345aaa` (Round349: Eval Playbook 五层框架 + Stagewise (Agentic IDE) + CowAgent (三层记忆 SPM, R337 orphan 复活))
- **Push**: `461e29d..6345aaa master -> master` ✅
- **新增 files**: 3 (1 Article + 2 Projects)
- **Modified files**: 4 (.agent/PENDING.md, .agent/REPORT.md, .agent/sources_tracked.jsonl, .agent/state.json)
- **Sources tracked**: 1662 → 1663 (+1 R349 CowAgent 补录)
- **Title length 修正**: 1 (CowAgent 31.5→29.0)
- **License 修正**: 1 (Stagewise Apache→AGPL-3.0)
- **Stars 修正**: 1 (CowAgent 45,241→45,247)

## 协议变更 / 新增

1. **R341 协议 #14 升级**：mtime 是辅助信号，**不是决定性证据**。**必须**用 `git log` + 文件自标 round + jsonl `used_at` 时间戳三路交叉验证。
2. **R350+ 推荐**：cron job 配 worker_id 锁（`.agent/lock/` 目录 acquire/release 文件锁）— 根本解决方案。
3. **R337 orphan 复活机制**：补录新 round 的 jsonl 条目（保留 R337 历史不删），新条目用新 slug、新 stars 数据、新 `used_at` 时间戳。
4. **Pair 关联"具体对位 > 泛关联"原则**：所有 Project 文件应在引用源显式标注配对 Article 路径及具体对位维度（不仅是"工具需要评估"泛关联）。
5. **License Risk Protocol 起草时验证**：所有 Project 文件起草时**立即** GitHub API 验证 `license.spdx_id`，引用源标注验证时间。
6. **Title Length 校验在 commit 前**：写完 Article/Project 文件**立即**跑 `title_len()` 校验，**不要 commit 后再补**。

## 反模式警告（R349 实战发现）

1. **R349 起草者没有跑 `title_len()` 校验**：CowAgent 标题 31.5 > 30 超长，靠 R350 cron 启动时修补
2. **R349 起草者没有 API 验证 License**：Stagewise 引用源 "Apache-2.0" 错误，靠 R350 cron 启动时修补
3. **R349 起草者没有 commit**：`gen_article_map.py` 超时后**中断流程**未 commit，留下 3 untracked articles + 4 modified .agent + 1 modified ARTICLES_MAP.md = 完整 round 产出但未固化到 git
4. **R349 起草者跑 `gen_article_map.py` 超时**：脚本在 1100+ articles 上 60s 内未完成，是脚本本身的 N+1 git log 问题（每个文件单独 git log），**R350 应优化**（如批量 git log 或 cache）

## R350 启动检查清单

- [ ] 扫描 Anthropic claude.com/blog 三子域（R301+ 协议硬化）
- [ ] 优化 `gen_article_map.py`（避免 N+1 git log 超时）
- [ ] 评估 OpenAI Economic Research Exchange
- [ ] 修复 AnySearch `.venv/bin/python` 缺失
- [ ] 监控 Tavily API 配额恢复
- [ ] 配 worker_id 锁到 cron 配置（`.agent/lock/` 目录）— 根治 R341 协议 #14 mtime 失效
- [ ] 补强 Eval cluster（加一篇过程可观测的 Project 加强维度）
