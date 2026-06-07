# Azure/azure-dev：微软官方的 AI 应用部署开发 CLI

## TRIP 四要素

- **T（Target）**：使用 Azure 生态开发 AI 应用的团队——需要统一代码-构建-部署-监控工作流，不想在 azd CLI、Azure Portal、ARM Template 之间来回切换
- **R（Result）**：一个开发者 CLI，将 Azure 资源管理的复杂操作抽象为 `code / build / deploy / monitor` 四个阶段的简单命令，March 2026 更新新增 `azd ai agent` 命令族支持本地 AI Agent 开发
- **I（Insight）**：**Azure生态的「git」**——azd 的设计理念是让 Azure 资源管理变得像 git 一样直观，通过 `azd init` → `azd up` → `azd deploy` 的流程覆盖 AI 应用的生命周期管理
- **P（Proof）**：微软官方维护；被 Azure 官方文档推荐为 AI 应用开发的标准工具；March 2026 更新新增 AI Agent 本地开发和 GitHub Copilot 集成

---

## P-SET 骨架

### P - Positioning（定位破题）

**一句话定义**：微软官方的 Azure 资源管理和 AI Agent部署 CLI，通过统一的工作流抽象简化云原生 AI应用的开发和部署。

**场景锚定**：当你需要把一个 AI Agent 部署到 Azure Container Apps + Azure AI Foundry 时，传统方案需要在 Azure Portal、ARM Template、az CLI 之间来回切换。azd 把这些操作统一成：

```bash
azd init      # 初始化项目
azd up # 创建资源并部署
azd deploy # 增量部署
azd monitor   # 监控
```

**差异化标签**：**Azure 生态唯一的官方「端到端」部署 CLI**——不是解决某个具体问题，而是覆盖整个开发部署生命周期。

### S - Sensation（体验式介绍）

azd 给你的是什么体验？

**AI Agent 开发**（March 2026 新功能）：

```bash
# 本地启动 Agent
azd ai agent run

# 向 Agent 发送消息
azd ai agent invoke --message "帮我查询今天的天气"

# 监控 Agent 状态
azd ai agent monitor
```

**GitHub Copilot 集成**：

```bash
azd init --copilot
# 启动 GitHub Copilot Agent 进行 AI 辅助脚手架生成
# 在修改文件前请求 MCP server 工具授权
```

这就是 azd 的核心价值——**把 Azure AI 应用开发的复杂度封装成简单的命令**。

### E - Evidence（拆解验证）

**命令族概览**：

| 阶段 | 命令 | 功能 |
|------|------|------|
| 代码 | `azd init` | 初始化项目，配置 azure.yaml |
| 构建 | `azd build` | 构建 Docker镜像 |
| 部署 | `azd deploy` | 部署到 Azure Container Apps |
| 监控 | `azd monitor` | 实时日志和指标 |
| AI Agent | `azd ai agent run/invoke/show/monitor` | 本地 AI Agent 开发 |

**March 2026 更新**（版本 1.23.7 ~ 1.23.13）：
- AI agent extension：本地运行、调用、监控 Agent
- GitHub Copilot 集成：AI 辅助项目初始化
- Container App Jobs 支持
- 本地预检验证
- 远程构建回退机制

**技术栈**：Go 语言编写，支持 Go1.26+

> "A developer CLI for working with Azure resources to build and deploy AI applications. Commands map to key workflow stages: code, build, deploy, and monitor." — [GitHub README](https://github.com/Azure/azure-dev)

### T - Threshold（行动引导）

**快速上手**：

```bash
# 安装
# macOS
brew install azure-dev-cli

# Linux
curl -fsSL https://aka.ms/install-azd.sh | bash

# Windows
winget install microsoft.azd
```

**项目初始化**：

```bash
azd init --template https://github.com/azure-samples/openai-chat-app
cd my-project
azd up
```

**AI Agent 开发**：

```bash
azd ai agent run
# 本地启动 Agent
# 通过 azd ai agent invoke 与 Agent 交互
```

**vs nanobot**：azd 解决的是「如何把 Agent 部署到 Azure」，nanobot 解决的是「如何在本地跑一个 Agent」。两者是互补关系——**azd 管部署，nanobot 管运行**。

---

## 关联主题

本文是 [azure-developer-cli-azd-local-agent-development-loop-2026.md](../practices/azure-developer-cli-azd-local-agent-development-loop-2026.md) 的配套项目推荐。两者共同指向一个主题：**本地 AI Agent 开发与执行的工程化实践**。

- azd：解决 Azure 环境下的本地开发循环和部署问题
- nanobot：解决任意环境下的本地 Agent 运行问题

**适用场景互补**：

| 场景 | azd | nanobot |
|------|-----|--------|
| Azure 部署 | ✅ | ❌ |
| 本地开发调试 | ✅ | ✅ |
| 多渠道接入 | ❌ | ✅ |
| 超轻量级 | ❌ | ✅ |
| 企业级管控 | ✅ | ❌ |

---

## 参考链接

- [Azure/azure-dev GitHub](https://github.com/Azure/azure-dev)
- [Azure Developer CLI (azd) – March 2026](https://devblogs.microsoft.com/azure-sdk/azure-developer-cli-azd-march-2026/)
- [azd 官方文档](https://learn.microsoft.com/azure/developer/azure-developer-cli/)