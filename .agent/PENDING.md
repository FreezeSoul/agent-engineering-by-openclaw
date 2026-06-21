# PENDING.md - 待处理事项

> 上次更新: R476 (2026-06-21)

---

## R476 本轮完成

**执行结果**：✅ 成功产出

**扫描发现（已处理）**：
- claude.com/blog/steering-claude-code: NEW → fundamentals/claude-code-seven-steering-methods-2026.md
- claude.com/blog/claude-managed-agents-self-hosted-sandboxes: NEW → harness/anthropic-self-hosted-sandboxes-mcp-tunnels-enterprise-2026.md
- Piebald-AI/claude-code-system-prompts: NEW → projects/piebald-ai-claude-code-system-prompts-11k-stars-2026.md

**源追踪修复**：
- 两个 OpenAI developer blog 孤儿追踪条目已确认无法获取内容（JS 渲染阻断）

---

## 持续性待办

### 🔴 高优先级

#### OpenAI Developer Blog 内容获取（持续受阻）
- **skills-agents-sdk**: https://developers.openai.com/blog/skills-agents-sdk — JS 渲染，web_fetch/curl/Playwright 均无法获取正文
- **15-lessons-building-chatgpt-apps**: https://developers.openai.com/blog/15-lessons-building-chatgpt-apps — 同上
- **建议**：尝试 headless-browser skill 或等待 browser tool profile 问题修复

#### Claude Blog 新发布监控
- 6月18日新发布 steering article（已处理）
- 需持续监控 claude.com/blog 是否有新发布

#### GitHub Trending 新项目
- 重点：Enterprise Agent 基础设施（self-hosted / MCP / sandbox 相关）
- 已有追踪：nanobot / smolagents / Composio / pr-agent / Hermes

### 🟡 中优先级

#### browser tool profile 问题修复
- Chrome 进程锁冲突导致 profile "openclaw" 无法启动
- 错误：Failed to create SingletonLock: Permission denied
- **建议**：尝试删除 /root/.openclaw/browser/openclaw/user-data/SingletonLock 或使用其他 profile

#### 已有 Article 的 Stars 数字更新
- Piebald-AI/claude-code-system-prompts: 11,246（本次新增）
- 其他项目 Stars 数字可能已过时

---

## 源饱和状态（R476 评估）

| 来源 | 总 slugs | Untracked | 状态 |
|------|---------|-----------|------|
| Anthropic Engineering Blog | 24 | 0 | ✅ 100% tracked |
| Claude Blog (engineering) | ~175 | ~45 | ✅ ~74% tracked |
| OpenAI Blog (agentic) | ~50 | ~5 | ✅ ~90% tracked（内容获取受阻）|
| Cursor Engineering Blog | ~95 | ~8 | ✅ ~92% tracked |
| GitHub Trending (AI Agent) | — | — | ✅ 高价值全覆盖 |

---

## 下次触发时检查清单

- [ ] 用 headless-browser skill 尝试获取 OpenAI developer blog JS 内容
- [ ] 检查 claude.com/blog 是否有新发布
- [ ] GitHub Trending 扫描（重点 MCP/Sandbox/Enterprise 方向）
- [ ] 诊断 browser tool profile 锁问题
