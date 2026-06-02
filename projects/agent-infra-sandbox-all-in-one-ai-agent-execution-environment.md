# agent-infra/sandbox：All-in-One Agent 执行沙箱

**推荐理由**：`agent-infra/sandbox` 将 Browser、Shell、File System、MCP 和 VSCode Server 集成到一个 Docker 容器中，为 AI Agent 提供完整的「计算机级」执行环境。与 LangSmith Sandboxes（硬件虚拟化微VM）形成互补——一个侧重隔离安全，一个侧重功能集成。

**关联 Article**：LangSmith Sandboxes 架构模式

---

## 基本信息

| 指标 | 数值 |
|------|------|
| GitHub | `agent-infra/sandbox` |
| Stars | 4,891 |
| 语言 | Go + Dockerfile |
| 主题 | agent, all-in-one, browser, filesystem, mcp, sandbox, shell |

## 核心能力

`sandbox` 将多类执行环境统一封装，为 Agent 提供一站式工作环境：

- **Browser**：让 Agent 控制浏览器，执行 Web 操作
- **Shell**：让 Agent 执行命令行操作
- **File System**：让 Agent 读写文件
- **MCP Server**：让 Agent 通过 MCP 协议调用外部工具
- **VSCode Server**：让 Agent 使用代码编辑环境

```
Agent → sandbox (Docker) → Browser + Shell + FS + MCP + VSCode
```

## 与 LangSmith Sandboxes 的互补性

| 维度 | LangSmith Sandboxes | agent-infra/sandbox |
|------|---------------------|----------------------|
| 隔离级别 | 硬件虚拟化微VM（更强隔离） | Docker 容器（共享内核） |
| 功能范围 | 代码执行为主 | Browser + Shell + FS + MCP + VSCode |
| 集成方式 | LangSmith 平台深度集成 | 独立 Docker 镜像 |
| 适用场景 | 企业级安全隔离执行 | 多功能开发/测试环境 |
| 部署 | 云服务（托管） | 自部署 |

**两者互补**：安全敏感场景用 LangSmith Sandboxes，多功能开发/测试场景用 `agent-infra/sandbox`。

## 技术架构

`sandbox` 通过单个 Docker 容器提供所有能力：

```bash
docker run -d agent-infra/sandbox
# 容器内包含：Chromium + Node.js + VSCode Server + MCP Server
```

Agent 通过标准协议与 sandbox 通信，无需感知底层差异。

## 使用场景

- **开发调试**：本地开发 Agent 时需要多种执行能力
- **测试环境**：为 Agent 创建隔离但功能完整的测试环境
- **多框架兼容**：同一 sandbox 可服务于不同 Agent 框架（LangGraph、 CrewAI、AutoGen）
- **MCP 生态**：与 MCP 工具生态无缝集成

## 为什么值得推荐

1. **一站式**：无需为 Agent 配置多个独立服务，一个容器搞定所有执行需求
2. **MCP 原生**：MCP 协议支持让工具扩展标准化
3. **轻量级**：相比 LangSmith Sandboxes 的企业级硬件虚拟化，更轻量易部署
4. **活跃生态**：4,891 Stars，GitHub Agent 基础设施领域的成熟项目

---

**引用来源**：
- GitHub: `https://github.com/agent-infra/sandbox`