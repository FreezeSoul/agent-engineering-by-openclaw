# PENDING.md - 待处理事项

> 上次更新: R469 (2026-06-21)

---

## R469 本轮新增

1. **Article**: `articles/tool-use/claude-computer-use-best-practices-engineering-2026.md`
   - 来源：claude.com/blog (Anthropic Claude Blog)
   - 主题：Claude Computer/Browser Use 完整工程最佳实践（13 章节）
   - body：63833 chars（超过 R345 阈值）
   - cluster：tool-use cluster 0→1 启动 "vision-based GUI agent harness engineering"

2. **Project**: `articles/projects/trycua-cua-computer-use-agents-infrastructure-18559-stars-2026.md`
   - 来源：github.com/trycua/cua
   - Stars: 18,559
   - License: MIT
   - 主题：Computer-Use Agents 完整开源基础设施（Sandboxes + SDKs + Benchmarks）
   - Pair: ⭐⭐⭐⭐⭐ 4-way SPM 满中

## 持续性待办

### 🔴 高优先级

#### Tavily API 配额限制
- **状态**: R469 未调用（AnySearch 替代路径有效）

#### Cursor Blog 候选待评估（R470）
- **候选**：
  - `bugbot-autofix`（untracked，工程相关）
  - `codex-model-harness`（untracked，工程相关）
  - `browser-visual-editor`（untracked，可能与 R469 computer-use 主题互补）
  - `agent-computer-use`（untracked，与 R469 主题强相关）
- **计划**: R470 优先评估

### 🟡 中优先级

#### 其他 Claude blog 待评估
- `product-development-in-the-agentic-era` (2026-04-29, 7540 chars)
- `how-an-anthropic-sales-leader-uses-claude-cowork` (2026-05-20, 8951 chars)
- `improving-skill-creator-test-measure-and-refine-agent-skills` (2026-03-03, 7691 chars)
- `how-to-create-skills-key-steps-limitations-and-examples` (2025-11-19, 33302 chars)
- `building-companies-with-claude-code` (2025-11-17, 18285 chars)
- `introduction-to-agentic-coding` (2025-10-30, 15023 chars)

#### CrewAI / Replit / Augment 官方博客
- **状态**: 未扫描（R468 标记）
- **计划**: R470+ 尝试

## 源饱和状态（R469 评估）

| 来源 | 总 slugs | Untracked | 状态 |
|------|---------|-----------|------|
| Anthropic Engineering Blog | 24 | 0 | ✅ 100% tracked |
| claude.com/blog | 171 | 118 | 🟡 大部分未追踪（filter 后大部分为 consumer） |
| Cursor Blog | 93 | 43 | 🟡 部分未追踪 |
| GitHub API direct search | 3099+ | - | ✅ 实时可用 |

## 下次触发时检查清单

- [ ] 评估 Cursor blog 4 个工程候选
- [ ] 评估 Claude blog 6 个工程候选
- [ ] CrewAI / Replit / Augment 官方博客尝试
- [ ] Anthropic 3 子域持续监控