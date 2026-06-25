# anthropics/knowledge-work-plugins：Anthropic 开源的 11 个企业级 Agent 技能包（21.9K Stars）

> 核心判断：这不是一个代码库，这是一个**企业 Agent 落地的方法论实体化**——Anthropic 把「如何用 AI 做好一个岗位」拆解成了可安装、可定制、可部署的技能包。

---

## 解决什么问题

企业引入 AI Agent 时，最常遇到的阻力不是技术，是**流程适配**：

- AI 不知道你们公司的 Jira 项目叫什么、Slack 频道在哪里、CRM 里怎么区分客户阶段
- 通用 AI 助手很强，但放在具体岗位上，价值出不来

Knowledge Work Plugins 是 Anthropic 给出的答案：**把「某个岗位该怎么做」封装成插件，让 AI 上岗即上手**。

---

## 核心内容：11 个生产级 Agent 技能包

Anthropic 开源了 11 个针对知识工作者的插件：

| 插件 | 解决什么问题 | 典型连接器 |
|------|-------------|-----------|
| **productivity** | 任务、日历、每日工作流，让 AI 知道你当前在做什么 | Slack, Notion, Asana, Linear, Jira, Monday, Microsoft 365 |
| **sales** | 潜客研究、销售管线、跟进邮件、竞争情报 | Slack, HubSpot, Close, Clay, ZoomInfo, Notion, Jira |
| **customer-support** | 工单处理、响应草稿、升级流程、知识库沉淀 | Slack, Intercom, HubSpot, Guru, Jira, Notion |
| **product-management** | 需求文档、路线图规划、用户研究综合、竞品追踪 | Slack, Linear, Asana, Monday, Jira, Notion, Figma, Amplitude |
| **marketing** | 内容草稿、活动规划、品牌一致性检查、效果分析 | Slack, Canva, Figma, HubSpot, Amplitude, Notion, Ahrefs |
| **legal** | 合同审查、NDA 处理、合规检查、会议准备 | Slack, Box, Egnyte, Jira, Microsoft 365 |
| **finance** | 分录处理、账务核对、财务报表生成、差异分析 | Snowflake, Databricks, BigQuery, Slack, Microsoft 365 |
| **data** | SQL 查询、可视化、统计分析、仪表板验证 | Snowflake, Databricks, BigQuery, Definite, Hex, Amplitude |
| **enterprise-search** | 跨工具统一搜索，一次查询覆盖邮件、文档、聊天、Wiki | Slack, Notion, Guru, Jira, Asana, Microsoft 365 |
| **bio-research** | 临床前研究工具连接（文献检索、基因组分析、靶点优先级）| PubMed, BioRxiv, ClinicalTrials.gov, ChEMBL, Benchling |
| **cowork-plugin-management** | 创建和定制新插件的工具 | — |

每个插件都包含三类组件：

- **Skills**（`.md` 文件）：AI 自动调用的领域知识和工作流定义
- **Commands**（`/sales:call-prep` 等）：用户显式触发的命令
- **Connectors**（`.mcp.json`）：连接外部工具的配置

---

## 技术架构：纯声明式的插件定义

这是 Knowledge Work Plugins 最值得注意的设计选择：**所有插件都是 Markdown + JSON，没有代码，没有构建步骤**。

```bash
plugin-name/
├── .claude-plugin/plugin.json   # 插件清单
├── .mcp.json                    # MCP 服务连接配置
├── commands/                    # 斜杠命令定义
└── skills/                      # Agent 技能（SKILL.md 文件）
```

plugin.json 定义插件的元数据：

```json
{
  "name": "finance",
  "description": "Prep journal entries, reconcile accounts...",
  "author": { "name": "Anthropic" },
  "category": "enterprise",
  "connectors": ["snowflake", "bigquery", "slack"]
}
```

MCP.json 定义工具连接：

```json
{
  "mcpServers": {
    "snowflake": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-snowflake"]
    }
  }
}
```

这意味着：**企业定制成本极低**——不需要写代码，只需要修改 JSON 配置文件和 Markdown 文件，就可以把一个「通用销售助手」变成「你们公司的销售助手」。

---

## 真正价值：工作流定义而非工具集成

大多数企业 AI 集成的思路是**工具优先**——给 AI 开放 API 访问就算完成。Knowledge Work Plugins 的思路是**工作流优先**：

> 举一个细节：`/data:write-query` 的设计，不只是「连接了 Snowflake」，而是：
> 
> 1. 写 SQL 查询
> 2. 验证结果正确性
> 3. 重新审视分析方法
> 4. 在 Hex 或 Amplitude 中构建可视化
> 5. **将结论写入 Jira ticket，获得团队确认后才算完成**

这不是一个工具，这是一个**完整的工作流定义**。AI 不是你的数据库浏览器，AI 是你的初级分析师。

---

## 与 Advisor Strategy 的关联

这个组合非常有意思：

- **Knowledge Work Plugins** = 角色级垂直 Agent 定义（每个岗位怎么工作的知识封装）
- **Advisor Strategy** = 模型级的按需升级能力（Executor 遇到复杂问题时调用 Opus）

如果再加上 **Skill 系统**（Anthropic 的 Skill Creator 生态），Anthropic 实际上在构建一个三层体系：

| 层级 | 作用 | 技术形态 |
|------|------|---------|
| **Skill** | 持久的能力定义和持续改进 | SKILL.md，一次编写，持续生效 |
| **Role Plugin** | 特定岗位的工作流封装 | Markdown + JSON，可定制 |
| **Advisor** | 推理过程中的按需升级 | API 原生支持，运行时调用 |

这三层组合在一起，就是一个**完整的 Agent 企业落地框架**。

---

## 上手指南

```bash
# 1. 添加 Anthropic 插件市场
claude plugin marketplace add anthropics/knowledge-work-plugins

# 2. 安装特定插件
claude plugin install sales@knowledge-work-plugins

# 3. 配置连接器（编辑 .mcp.json）
# 指向你公司的 Slack/Jira/HubSpot 实例

# 4. 开始使用
/sales:call-prep @潜在客户
/data:write-query "过去30天转化率分析"
```

---

**引用来源**：

> "Cowork lets you set the goal and Claude delivers finished, professional work. Plugins let you go further: tell Claude how you like work done, which tools and data to pull from, how to handle critical workflows."
> — Anthropic, [Knowledge Work Plugins README](https://github.com/anthropics/knowledge-work-plugins)
