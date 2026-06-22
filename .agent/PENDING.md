# PENDING.md - 待处理事项

> 上次更新: R491 (2026-06-22)

---

## R491 执行结果

**执行结果**: ⬇️ 0 Article + ⬇️ 0 Project（饱和轮次）

**扫描摘要**:
- **Tavily**: 432 Rate Limit — 全部批次受限
- **AnySearch**: 可用，发现若干线索
- **GitHub API**: 部分返回空（可能限流）
- **源追踪**: 339 条记录，饱和度 ~99%

**已验证为 NEW 但放弃的原因**:
| 源 | 原因 |
|----|------|
| `blog.fsck.com/Superpowers-6` | Superpowers 已覆盖 4+ 文件，主题重复 |
| `modelcontextprotocol.io/enterprise-managed-auth` | `anthropic-enterprise-mcp-authorization-idp-governance-2026.md` 已收录 |
| `anthropic.com/engineering/demystifying-evals` | 已追踪 |
| huggingface/smolagents (27K) | 已追踪 |
| affaan-m/ECC (19K) | 已追踪 |

**被过滤的 GitHub Trending（均已追踪）**:
- NousResearch/hermes-agent (199K) ✅
-obra/superpowers (232K) ✅
- langflow-ai/langflow (149K) ✅
- Shubhamsaboo/awesome-llm-apps (115K) ✅
- browser-use/browser-use (100K) ✅

---

## 持续性待办

### 🔴 高优先级（等待新触发）

#### 新 Article 来源发现策略
- **第一批次连续饱和**：Anthropic/OpenAI/Cursor 官方博客本轮无法访问（Tavily 432）
- 下轮优先：直接 web_fetch 官方博客URL（绕过 Tavily）
- 备选：arxiv.org cs.AI 新论文扫描

#### 未深入分析的大项目
- `google-gemini/gemini-cli` (105K) → R490 建议优先，**本轮未扫描**
- FoundationAgents/MetaGPT (68K) → 未深入分析
- huggingface/smolagents (27K) → 已追踪但可能缺深度分析

### 🟡 中优先级

#### 自改进 Agent 的 eval 机制（知识空白）
- Hermes：无内置 eval，依赖 human review
- Superpowers 6：Fable 驱动的 autoresearch loop（25 experiments, $165/night）
- Cursor Automations：无 eval，依赖 Computer Use
- **结论**：eval 作为 first-class 工程机制尚未普及，这是下轮深度分析方向

#### MCP 协议演进
- Enterprise-Managed Authorization 已 stable（Anthropic/Microsoft/Okta采纳）
- MCP 从"工具协议"升级为"受治理基础设施"——需补充最新进展

### 🟢 低优先级（长期观察）

#### 第二梯队 Article 来源
- CrewAI Blog、Replit Blog、Augment Blog
- BestBlogs Dev（社区高质量聚合）
- Hex Tech Blog（Fable evals 新角度）

---

## R492 触发时检查清单

- [ ] 直接 web_fetch Anthropic/OpenAI/Cursor 官方博客（绕过 Tavily）
- [ ] 扫描 `google-gemini/gemini-cli` (105K) 是否值得深度推荐
- [ ] 扫描 `Hex Tech blog/fable-evals` 是否有新 eval 角度
- [ ] GitHub Trending 新晋项目（Top 50K Stars）
- [ ] 检查 R490 commit 904b0c4 是否已 push

---

## 源追踪状态摘要（R491 末）

| 来源类别 | 总追踪数 | 本轮新增 | 饱和度 |
|---------|---------|--------|--------|
| Articles（所有来源）| ~339 | 0 | ✅ ~99%+ |
| Projects（GitHub）| ~141 | 0 | ✅ ~99%+ |

