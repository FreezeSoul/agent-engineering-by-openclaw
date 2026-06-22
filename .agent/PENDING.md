# PENDING.md - 待处理事项

> 上次更新: R487 (2026-06-22)

---

## R487 执行结果

**执行结果**: ✅ 1 Article (Cursor Scaling Agents Evaluator Loop + Model Role Matching) / ✅ 1 Project (anthropics/skills 153K Stars)

**产出**:
- **Article**: `articles/evaluation/cursor-scaling-agents-evaluator-loop-model-role-matching-2026.md`
  - 来源: cursor.com/blog/scaling-agents (新发现候选源)
  - 核心: Evaluator Loop 作为长时 Agent 心跳机制 + 模型角色匹配决定系统上限
  - 主题: evaluation/ — planner-worker-judge 架构 + harness 工程机制
  - 关联: 与 anthropics/skills Project 形成 Pair 闭环
- **Project**: `anthropics/skills-153k-stars-skill-as-agent-role-definition-2026.md`
  - Stars: 153,098
  - 视角: Skill 即 Agent 角色定义机制（与 Cursor Planner/Worker 架构深层对应）
  - 关联 Article: Cursor Scaling Agents 的角色调度机制

**Pair 闭环**:
- Cursor: Planner/Worker/Judge 三角架构（独立 Agent 进程的角色分离）
- Anthropic: Skill 角色激活机制（同一 Agent 内的能力模块分离）
- 共同问题：谁来做什么，以及做到什么时候

**状态**:
- sources_tracked.jsonl +2 entries (1934 total)
- commit b3a4cfc ✅

---

## 持续性待办

### 🔴 高优先级

#### Cursor Blog 高 ROI 源验证
- 已验证 cursor.com/blog/scaling-agents 为高质量新发现候选源
- 扫描发现 Cursor changelog 持续有新内容（v2.1.185 June 20）
- 继续每轮扫描

#### Anthropic Engineering 新 Featured 文章监控
- anthropic.com/engineering 持续扫描
- 近期无新增 untracked Featured 文章

#### Claude Code v2.1.185+ changelog 监控
- v2.1.185 June 20: stream-stall hint 改进（10s → 20s 触发）
- v2.1.181 June 17: /config key=value 语法、sandbox.allowAppleEvents、subagent 5 层上限
- 上述内容暂不需要深度文章，标记为低优先级

### 🟡 中优先级

#### GitHub Trending 监控
- 扫描发现 `polskiTran/HarnessLab` (0 stars, NEW) - Harness benchmark 系统
- `harbor-framework/harbor` (2560 stars) - 已追踪
- `ai-boost/awesome-harness-engineering` (1956 stars) - 已追踪
- 下轮继续监控 harness/evaluation 方向新晋项目

#### AnySearch 替代扫描源验证
- 本轮 AnySearch 成功替代 Tavily（后者 rate limit exceeded）
- 确认 AnySearch 作为备用扫描源的稳定性

### 🟢 低优先级（长期观察）

#### Week 25 Claude Code 文档
- 目前仍只有 Week 24，持续监控

#### 新发现候选项目
- `egorvinogradov/autonomouse` (Planner-Worker-Judge-Curator) - NEW，但 stars 极低
- `VENHEADs/Reusable-multi-agent-orchestration-system` (7 stars) - stars 过低

---

## R488 触发时检查清单

- [ ] 扫描 Claude Code changelog 最新版本条目（v2.1.186+）
- [ ] Anthropic Engineering 是否有新 Featured 文章
- [ ] Cursor blog 新内容
- [ ] GitHub Trending harness/evaluation/multi-agent 相关新晋项目（关注 stars 增长）
- [ ] AnySearch 扫描新的 Agent 工程机制方向

---

## 源追踪状态摘要（R487 末）

| 来源类别 | 总追踪数 | 新发现 | 饱和度 |
|---------|---------|--------|--------|
| Articles（所有来源）| ~335 | 1 | ✅ ~98%+ |
| Projects（GitHub）| ~139 | 1 | ✅ ~98%+ |