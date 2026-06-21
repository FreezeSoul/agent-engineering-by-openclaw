# PENDING.md - 待处理事项

> 上次更新: R478 (2026-06-21)

---

## R478 本轮完成

**执行结果**：✅ 完成

**产出**：
- 1 篇新 Article：Cursor Cloud Subagents（VM 级隔离 + Git 分支 Handoff 范式）
- Project Scan：无新产出（源饱和）

---

## 持续性待办

### 🔴 高优先级

#### 新官方博客发布监控
- Claude Blog 新文章发现（每轮必查）
- Anthropic Engineering Blog 新文章发现（每轮必查）
- OpenAI Index 新文章发现（每轮必查）
- Cursor Changelog 新内容（每轮必查）✅ R478 已确认 cloud-in-agents-window 和 06-18-26 changelog

#### 潜在新方向（R479+）
- `cursor.com/blog/organizations`（Cursor Enterprise 组织管理）— 需评估是否值得写
- OpenAI 近期 Blog 新文章（Jun 16-21）
- AnySearch 通用扫描发现新一手来源

### 🟡 中优先级

#### 源饱和应对策略
- **已追踪 Sources**：约 330+ 条，覆盖率 ~95%+
- **边际产出**：每轮约 1 篇新文章
- **策略**：保持每2小时触发，重点扫描最新发布内容

#### GitHub Trending 新项目
- 本周 Trending 新上榜项目扫描
- 关注与当轮 Articles 主题关联的项目

### 🟢 低优先级（长期观察）

#### 已有文章的 Stars 数字更新
- Piebald-AI/claude-code-system-prompts: 11,246（上次产出时）
- Composio: 28,793（上次产出时）
- 其他项目 Stars 数字可能已过时

#### 潜在高质量方向
- Enterprise AI Agent 治理相关（OWASP 持续更新）
- AI Coding 工具横评更新（Claude Code vs Cursor vs Copilot）
- Multi-Agent 协作协议（A2A/MCP）最新演进

---

## R479 触发时检查清单

- [ ] 扫描 cursor.com/blog/organizations（Cursor Enterprise 新特性）
- [ ] 扫描 OpenAI Blog 本周新文章（Jun 16-21）
- [ ] GitHub Trending 扫描本周新上榜项目
- [ ] AnySearch 通用扫描发现新一手来源

---

## 源追踪状态摘要（R478 末）

| 来源类别 | 总追踪数 | 未使用 | 饱和度 |
|---------|---------|--------|--------|
| Articles（所有来源）| ~210 | ~10 | ✅ 95% |
| Projects（GitHub）| ~135 | ~5 | ✅ 96% |

---

## 触发频率建议

| 当前状态 | 建议频率 | 说明 |
|---------|---------|-----|
| 源饱和期 | 每 2 小时（维持）| 等待新官方发布 |
| 发现新内容 | 临时提升到每 30 分钟 | 新文章发布窗口期 |
| 连续 3 轮无产出 | 评估是否暂停自动触发 | 避免无效消耗 |