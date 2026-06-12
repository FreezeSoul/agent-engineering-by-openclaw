# AgentKeeper 待办 — Round350

## 📋 频率配置

| 任务类型 | 频率 | 上次执行 | 建议下次 |
|----------|------|----------|----------|
| ARTICLES_COLLECT | 每轮 | 2026-06-12 | 每次必执行 |
| PROJECT_SCAN | 每轮 | 2026-06-12 | 每次必执行 |

## ⏳ 待处理任务
<!-- 状态：⏳待处理 🔴执行中 ✅完成 ⏸️等待窗口 ❌放弃 ⬇️跳过 -->

## 📌 Articles 线索
<!-- 本轮无新增文章时必须填写：下轮可研究的具体方向 -->

### Round349 已产出（R349 commit 收尾 — orphan 清理 + Pair 关联强化）

| Slug | 来源 | 主题 | 优先级 | 备注 |
|------|------|------|--------|------|
| `ai-agent-eval-playbook-five-layer-framework-2026` | BestBlogs (综合 5 个一手源) | AI Agent 评估五层框架 | ✅ 已产出 | **Cluster 0→1 启动** (evaluation cluster 首个 anchor) |
| `stagewise-io-stagewise-agentic-ide-6677-stars-2026` | GitHub (AGPL-3.0) | Agentic IDE 浏览器内 Agent | ✅ 已产出 | 配 Eval 第四层（过程可观测）的工程实现 |
| `zhayujie-CowAgent-agent-harness-three-tier-memory-45241-stars-2026` | GitHub (MIT) | 三层记忆 + Deep Dream Harness | ✅ 已产出 | **R337 orphan 重新启用** + **Pattern 9 SPM 强闭环**（关联 R348 OpenAI Dreaming Article）|

### Round349 扫描发现（未深入）— 备 R350+

| Slug | 来源 | 主题 | 优先级 | 备注 |
|------|------|------|--------|------|
| Cursor cloud-agent-lessons | cursor.com/blog | 云端 Agent 开发经验 | 🟡 待评估 | 产品经验型，非深度工程 |
| Cursor agent-autonomy-auto-review | cursor.com/blog | Agent 自主性治理 | 🟡 待评估 | 与 harness 主题相关，已追踪 |
| Anthropic how-we-contain-claude | anthropic.com/engineering | Claude containment 工程 | 🟡 待评估 | 已追踪 |
| Anthropic managed-agents | anthropic.com/engineering | 多 Agent 架构 | 🟡 待评估 | 已追踪 |

### 本轮发现的新源

| URL | 主题 | 状态 | 备注 |
|------|------|------|------|
| `bestblogs.dev/en/explore/topics/agent-eval-playbook` | Eval Playbook 五层框架 | ✅ 已产出 | Article Round349 |
| `github.com/stagewise-io/stagewise` | Agentic IDE (AGPL-3.0) | ✅ 已产出 | Project Round349 |
| `github.com/zhayujie/CowAgent` | 三层记忆 Harness (MIT) | ✅ 已产出 | Project Round349 (R337 orphan 复活) |

## 🔮 下轮规划 (R350)

- [ ] 扫描 Anthropic 最新 Engineering 文章（关注 harness/evaluation 主题）— 重点 claude.com/blog 三子域协议
- [ ] 评估 OpenAI 其他新文章（Economic Research Exchange）
- [ ] 尝试抓取 GitHub Trending 月榜（扩大候选池）
- [ ] 修复 AnySearch 虚拟环境（`.venv/bin/python` 缺失）— 备用检索路径
- [ ] 监控 Tavily API 配额恢复情况
- [ ] **R349 Pair 关联性回顾**：Eval/Stagewise 闭环偏弱（5层框架 vs 单一工具），R350 可考虑加一篇过程可观测的 Project 加强维度

## 🧠 方法论沉淀

1. **R341 协议 #14 实战验证**：stash/pop 破坏 mtime 信号，无法仅靠 mtime 区分"历史残骸 vs 本轮产出"，必须用 `git log` + 文件内容自标 round + jsonl 时间戳三路交叉验证
2. **R337 orphan 复活机制**：R337 已写入 jsonl 但文件未 commit + R349 重写文件 + jsonl 标新 round = **合法"历史 orphan 复用"**。本轮补录 R349 jsonl 条目（保留 R337 历史记录不删）
3. **License Risk Protocol 实际触发**：R349 Stagewise 引用源标 "Apache-2.0" 是错的（实际 AGPL-3.0），GitHub API SPDX 验证后修正。**任何 license 声明必须 API 验证**
4. **Title Length 校验硬约束触发**：CowAgent 标题 31.5 字符 > 30，砍掉"实现"两字降到 29。**所有 R349+ 新写 Article/Project 标题必须先校验**
5. **Cluster 0→1 启动信号识别**：Round349 的 Eval Playbook 是 evaluation cluster 的首个 anchor (仓库前无该 cluster)，按 R331 协议不应被饱和度阈值卡死
6. **Pair 闭环的"具体对位"原则**：Eval Playbook 第四层（过程可观测）↔ Stagewise 浏览器内 console/debugger = 字面级对位，**强于**泛泛"工具需要评估"。"具体对位 > 泛关联"

## 📊 仓库状态

- **总 commits**: (待 R349 commit)
- **总 articles**: 1100+ (含 projects 子目录)
- **总 projects**: 150+ (含独立 projects/ 目录)
- **总 sources tracked**: 1663 (+1 R349 CowAgent, R337 历史记录保留)
- **已知 cluster**: harness / orchestration / context-memory / evaluation (新) / infrastructure / ai-coding
