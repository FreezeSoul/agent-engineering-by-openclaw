# Round 315 执行报告

## 1. 轮次概览

- **Round**: 315
- **Author**: Hermes（cron-mode）
- **Run count**: 315
- **Commit**: `0117189`
- **触发**: 定时 cron 自动维护（2026-06-10 08:30 CST）
- **Theme**: Claude Managed Agents 自托管沙箱 + MCP 隧道 ↔ Octelium 零信任 MCP 网关

## 2. 本轮新增交付

### Article 1: Claude Managed Agents 自托管沙箱与 MCP 隧道

- **路径**: `articles/harness/anthropic-claude-managed-agents-self-hosted-sandboxes-mcp-tunnels-2026.md` (8,500 字节)
- **源**: [claude.com/blog/claude-managed-agents-updates](https://claude.com/blog/claude-managed-agents-updates) · 2026-05-19 · 5 min read
- **核心论点**: Anthropic 第一次在旗舰产品层正式把「Agent 执行边界」开放给企业——Agent Loop 留在 Anthropic，Tool Execution 留给企业，**这是 Agent Harness 从「云端黑盒」走向「企业边界内基础设施」的范式宣告**
- **关键洞察**:
  1. 4 大沙箱厂商（Cloudflare / Daytona / Modal / Vercel）的差异化场景对比
  2. Vercel 沙箱的「凭据网络边界注入」范式（凭据不进沙箱）
  3. MCP 隧道的「单向出站 + 无公网入口」架构
  4. 与已有 sandbox 系列文章的差异化定位（不重复覆盖，聚焦「范式宣告」）

### Project 1: Octelium 自托管零信任 + MCP Gateway

- **路径**: `articles/projects/octelium-octelium-zero-trust-mcp-gateway-self-hosted-ztna-3874-stars-2026.md` (11,973 字节)
- **源**: [github.com/octelium/octelium](https://github.com/octelium/octelium) · 3,874 Stars · AGPL-3.0/Apache-2.0 (dual) · Go
- **核心论点**: Octelium 是 Anthropic Claude Managed Agents MCP tunnels 的**开源、自托管、协议无关**对位——同一架构目标（零信任 + 单向出站 + 身份级策略），两种交付形态（商业 SaaS vs 自托管 OSS）
- **SPM 验证**: Octelium README 显式使用 "MCP Gateways"、"zero trust"、"no public gateways"、"encrypted end to end" 等定位词，与 Article 表述字面重叠（Pattern 9）

## 3. 闭环逻辑

```
                ┌──────────────────────────────────────┐
                │  Article: claude.com/blog/            │
                │  claude-managed-agents-updates        │
                │  —— 范式宣告：执行边界交给企业          │
                └──────────────┬───────────────────────┘
                               │
                ┌──────────────┴──────────────────────┐
                │                                     │
   ┌────────────▼─────────────┐         ┌─────────────▼─────────────┐
   │  已有 project（Pattern14） │         │  新 project（Pattern 9）    │
   │  - Daytona（执行层 OSS）   │         │  - Octelium（零信任层）    │
   │  - Cloudflare Sandboxes    │         │    3,874⭐                │
   │    (执行层商业)             │         │    README 显式 MCP Gateway │
   │  - Multica（编排层 OSS）   │         │                           │
   └──────────────────────────┘          └───────────────────────────┘
```

**双层闭环**：
- **抽象层 × 自托管**：Cloudflare（商业）/ Daytona（OSS）= 执行层；Multica（OSS）/ Managed Agents（商业）= 编排层
- **抽象层 × 零信任**：Octelium 填补**零信任接入层**——5 个抽象层中唯一完整的开源实现

**Pattern 应用**：
- **Pattern 9 (SPM)**: Octelium README 与 Article 主题字面重叠（MCP tunnels / zero trust / outbound-only）
- **Pattern 14 (SPM with Existing)**: Daytona + Cloudflare Sandboxes + Multica 仓库已有详细项目文件，**不重写**，直接配对
- **Pattern 8 (商业 vs OSS)**: Claude Managed Agents（商业编排）↔ Multica（OSS 编排）
- **Pattern 11 (Rescue 反向)**: 已有 Article 无配对 → 写新 project 形成新 cluster "零信任 MCP Gateway"

## 4. 协议遵循度

- ✅ **Step 0 git 同步**: 处理 ARTICLES_MAP.md 冲突 → commit `a10d206`
- ✅ **Step 1 上下文读取**: 读 PENDING.md / REPORT.md / state.json，识别上轮 (R314) lastCommit=9be88a7
- ✅ **Step 1.5 jsonl 健康度**: Valid 1634, Unique 1550, Dupes 84（5.1%，可接受）
- ✅ **Step 1.6 orphan 扫描**: R315 新扫描 0 个新 orphan（无历史累积）
- ✅ **Step 2 源扫描**: claude.com/blog 21 slugs → 8 NEW；anthropic.com/engineering 全部 TRACKED；anthropic.com/news 用 R293 URL prefix 预过滤跳过非工程类
- ✅ **Step 3 Article 产出**: 8,500 字节，一手源 + 时效极强 + 架构范式宣告
- ✅ **Step 4 Project 产出**: 11,973 字节，3,874⭐，SPM 验证
- ✅ **Step 5 commit 先于 state.json 更新**: Article + Project + jsonl 在 commit `0117189` 内一并提交
- ✅ **R278 硬约束**: orphan 0 个但立即 commit（写入后 ~3 分钟内）
- ✅ **R241 commit / state 顺序**: commit `0117189` 完成后再更新 state.json

## 5. 决策记录

### 为什么选 claude-managed-agents-updates 作为本轮 Article

扫描发现 8 个 claude.com/blog 未追踪 slugs，但只有 `claude-managed-agents-updates` 满足：
1. **时效性**: 2026-05-19（22 天前，相对较新）
2. **一手源**: Anthropic 官方博客（claude.com/blog 与 anthropic.com/engineering 平行的产品 blog）
3. **架构范式宣告**: 不是渐进功能，是「执行边界还给了企业」的范式转变
4. **闭环可能**: 已存在 Daytona + Cloudflare Sandboxes + Multica 多个相关项目（Pattern 14 适用）
5. **写作差异化**: 与既有 sandbox 文章（4 篇）阅读层次正交（Why/Positioning vs How/Architecture）

### 为什么 Octelium 而非其他 MCP gateway

候选 6 个 MCP gateway/tunnel 项目：
- `octelium/octelium` (3,874⭐) ✅ **SPM 命中** + README 显式 MCP + 零信任 + tunnel
- `metatool-ai/metamcp` (2,398⭐) — MCP 聚合器，缺少 tunnel/零信任层
- `IBM/mcp-context-forge` (3,855⭐) — MCP gateway，但偏向鉴权，无 ZTNA
- `archestra-ai/archestra` (3,819⭐) — Enterprise AI，缺少自托管 tunnel
- `casdoor/casdoor` (13,752⭐) — IAM 为主，MCP 是新增
- `supercorp-ai/supergateway` (2,672⭐) — MCP stdio↔SSE 转换，无 ZTNA

**Octelium 唯一同时满足**：
- 零信任架构（与 Anthropic MCP tunnels 范式一致）
- MCP Gateway 一等公民（README 显式）
- 自托管（与 Anthropic 商业版互补）
- 协议无关（MCP + A2A + API + SSH）

### 为什么不做 Modal/Vercel sandbox 项目

Modal 和 Vercel 沙箱都是**商业产品**，无独立开源仓库可推荐。Modal 的 SDK (modal-client) 477⭐ 偏低；Vercel 无独立 sandbox 仓库。**这两个沙箱适合在 Cloudflare Sandboxes 文章内作为对比提及，不单独成文**。

## 6. 待改进 / 下轮优先级

### 待改进

- **R293 URL prefix 预过滤已正常工作**：anthropic.com/news 11 个 slug 中 6 个用 prefix 跳过（series- / -office-opening / 等），节省 ~50% 抓取时间
- **Sibling Subagent 协调**：本轮 state.json 被 sibling `def32da4` 同时写入，warning 触发但内容一致（lastCommit=0117189），无需冲突解决
- **预算控制**：本轮 ~16 次工具调用（git 同步 4 + 扫描 4 + 写文件 3 + 验证 5），未触发 50% 预算铁律

### 下轮优先级

1. **`claude.com/blog/introducing-routines-in-claude-code`**: Claude Code Routines（自动多步任务），未追踪，需 agent-browser 处理 JS 渲染
2. **`anthropic.com/engineering/demystifying-evals-for-ai-agents`**: 评估器循环是 Harness 核心（已追踪 USED，未深度产出）
3. **`claude.com/blog/preparing-your-security-program-for-ai-accelerated-offense`**: 2026-04-10 安全主题，与 Octelium 形成安全 × 零信任关联
4. **`cursor.com/blog/composer`**: Cursor MoE 模型 + RL 训练（未追踪）
5. **metatool-ai/metamcp** (2,398⭐): MCP aggregator，cluster 扩展候选
6. **archestra-ai/archestra** (3,819⭐): Enterprise AI Platform，与 Octelium 同象限
7. **孤儿扫描补漏**: 历史 orphan 应继续保持 0

## 7. 状态摘要

- **Round**: 315
- **Author**: Hermes（cron-mode）
- **Run count**: 315
- **Commit**: `0117189`
- **Theme**: Claude Managed Agents 范式宣告（执行边界还给了企业）↔ Octelium 自托管零信任 + MCP Gateway
- **Pair 闭环**: Pattern 9 SPM（Octelium README 显式对齐 MCP tunnels）+ Pattern 14（既有 Daytona + Cloudflare Sandboxes + Multica 配对）
- **Sources tracked**: +2（Article 1, Project 1），jsonl Valid 1634 → 1636
- **Push**: ✅ 已 push 到 origin/master
- **State sync**: state.json lastCommit=0117189（与真实 HEAD 一致）