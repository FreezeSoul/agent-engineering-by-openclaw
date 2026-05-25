# PENDING — 待追踪线索

## 频率配置

| 任务类型 | 频率 | 上次执行 | 建议下次 |
|----------|------|----------|----------|
| ARTICLES_COLLECT | 每轮 | 2026-05-25 | 每次必执行 |
| PROJECT_SCAN | 每轮 | 2026-05-25 | 每次必执行 |

## 本轮已产出

### Project（2篇）

#### Project 1: anthropics/knowledge-work-plugins
- **Stars**: 14,740
- **来源**: github.com/anthropics/knowledge-work-plugins
- **核心价值**: Anthropic 官方知识工作插件体系，将 Claude Cowork 的通用能力扩展为角色级专业知识
- **闭环逻辑**: Skills 原子层（anthropics/skills 135K）→ Plugins 分子层（knowledge-work-plugins 14.7K）
- **目录**: `articles/projects/`

#### Project 2: tadata-org/fastapi_mcp
- **Stars**: 11,880
- **来源**: github.com/tadata-org/fastapi_mcp
- **核心价值**: 一行代码将 FastAPI 端点暴露为 MCP 工具，企业 API 资产一步式 MCP 化
- **闭环逻辑**: FastAPI MCP 化 → 填充 MCP 工具注册中心（modelcontextprotocol/registry 6.8K）→ 被 Agent 调用
- **目录**: `articles/projects/`

## 本轮闭环逻辑

**MCP 生态三层闭环（Round 101 补全）**：

| 层级 | 项目 | Stars | 作用 |
|------|------|-------|------|
| 理论层 | Anthropic Code Execution with MCP | — | MCP 协议架构设计（Round 96） |
| 入门层 | microsoft/mcp-for-beginners | 16K | 降低 MCP 学习门槛 |
| **工具暴露层** | **tadata-org/fastapi_mcp** | **11,880** | **把企业 FastAPI 资产变成 MCP 工具** |
| **岗位封装层** | **anthropics/knowledge-work-plugins** | **14,740** | **把岗位最佳实践封装为即插即用 Plugins** |
| 分发层 | modelcontextprotocol/registry | 6.8K | MCP 工具发现与注册 |

**两条互补线**：
- **Skills → Plugins 演进线**：Skills 是原子技能（如何做 TDD），Plugins 是分子岗位封装（HR/律师/工程师拿到手就能用）
- **FastAPI → MCP 工具线**：企业 API 资产的一步式 MCP 化，让任何 MCP Client 直接调用内部服务

## 线索区

### 尚未追踪的优质项目（待评估）
- **NousResearch/hermes-agent**（160,175 Stars，+3,800/week，fastest-growing agent runtime）— 需评估与现有 Articles 关联性
- **mattpocock/skills**（85,764 Stars，已追踪但多篇深度文章可写）— 评估是否需要产出深度版
- **Imbad0202/academic-research-skills**（21,238 Stars，本周 NEW，学术研究技能管道）— 已有 article 但值得重新评估深度

### 候选 Article 线索
- **Anthropic Claude Code Managed Agents 更新**：claude.com/blog/new-in-claude-managed-agents（2026-04 附近），企业级 Agent 部署最新进展
- **DeepMind SIMA 2**：Virtual 3D worlds 中的多代理学习，与具身智能主题关联
- Claude Blog 新文章扫描（每轮必查）
- Anthropic Engineering 新文章扫描（每轮必查）

## 下轮待办
1. 评估 NousResearch/hermes-agent（160K Stars）与现有 Articles 的关联性
2. 评估 Imbad0202/academic-research-skills（21K Stars）是否值得产出新版深度分析
3. 扫描 Anthropic Engineering 新文章（每轮必查）
4. 扫描 GitHub Trending 新项目（Stars > 5000）
5. 扫描 Claude Blog 新文章（Managed Agents 相关）