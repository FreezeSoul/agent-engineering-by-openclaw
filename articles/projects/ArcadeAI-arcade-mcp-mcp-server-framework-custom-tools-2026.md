# Arcade-mcp：把自定义工具装进 MCP 框架的工程实践

> ⭐ **915 stars** | 🔗 [ArcadeAI/arcade-mcp](https://github.com/ArcadeAI/arcade-mcp) | 🏷️ MCP Framework / Custom Tools | 📅 **2026 新发现**

## 核心命题

Cursor SDK June 2026 用内置 MCP 服务器 `custom-user-tools` 把"函数定义"直接变成"Agent 工具"，让自定义能力零成本接入 Agent 工具链。**Arcade-mcp** 做了同一件事的另一面：让你用 Python 写一个 MCP 服务器，把任何自定义能力暴露给任何支持 MCP 的 Agent。

> 引用 README：*"MCP Server Framework and Tool Development library for building custom capabilities into agents."*

两者是同一枚硬币的两面——Cursor SDK 是"如何在 Cursor 里暴露自定义工具"，Arcade-mcp 是"如何把你的服务变成一个标准 MCP 服务器，让所有 Agent 都能用"。

---

## 为什么值得关注

### 1. MCP 协议层的事实标准位置

MCP 正在成为 Agent 工具扩展的事实协议。Cursor SDK 的 `custom-user-tools`、Claude Code 的 tool use、Copilot 的插件系统——都在向 MCP 靠拢。Arcade-mcp 让你不需要理解 MCP 协议的每一个细节，只需要关注"我要暴露什么能力"。

### 2. 三行代码启动一个 MCP 服务器

```python
from arcade import Arcade

@Arcade.tool()
def query_database(sql: str) -> str:
    """Query the analytics database"""
    return db.execute(sql)

Arcade.run()
```

> 引用 README：*"Build an MCP server in minutes, not days. Define tools, resources and prompts as Python decorators."*

笔者认为，这个开发体验的压缩是 Arcade-mcp 最大的价值——从"写 stdio 服务器 + 调试通信"到"装饰器 + run()"。

### 3. 工具继承与层级化组织

和 Cursor SDK 的工具继承类似，Arcade-mcp 支持 MCP 服务器之间的组合：

```
arcade-mcp 主服务器
  ├── 内置 tools（query_database, file_search）
  ├── 组合子服务器（sub-servers）
  │     ├── GitHub MCP
  │     ├── Slack MCP
  │     └── Database MCP
  └── 动态工具注册
```

### 4. 支持的 Agent 生态

| Agent | 支持状态 |
|-------|---------|
| Claude (via Claude Code) | ✅ 官方支持 |
| Cursor | ✅ 通过 custom-user-tools |
| GitHub Copilot | ✅ MCP 协议兼容 |
| 其他 MCP Client | ✅ 通用 MCP 协议 |

---

## 与 Cursor SDK Custom Tools 的互补关系

| 维度 | Cursor SDK (`custom-user-tools`) | Arcade-mcp |
|------|----------------------------------|------------|
| **入口** | 函数定义 → 传入 `local.customTools` | 装饰器 → Python 文件运行 |
| **暴露方式** | 内置 MCP 服务器（Agent 内部） | 独立 MCP 服务器（跨 Agent） |
| **工具继承** | 父 Agent → 子 Subagent | MCP 服务器组合 |
| **适用场景** | Cursor SDK 内部扩展 | 通用 MCP 服务开发 |
| **协议层** | SDK 内部实现 | 标准 MCP 协议 |

笔者认为，两者组合使用效果最好：用 Arcade-mcp 开发和调试你的 MCP 工具服务，然后用 Cursor SDK 的 `custom-user-tools` 在 Cursor 环境中直接使用它们。

---

## 适用边界

**适合**：
- 需要把内部服务/数据库暴露给多个 Agent 的场景
- MCP 工具的快速原型和测试
- 跨团队的 MCP 工具服务复用

**不适合**：
- 简单的单工具需求（直接用 Cursor SDK 的 `custom-userTools` 更轻量）
- 需要复杂认证和权限管理的生产级 MCP 服务（用官方 MCP Python SDK）

---

## 快速上手

```bash
pip install arcade-mcp

# 创建工具文件
cat > tools.py << 'EOF'
from arcade import Arcade, tool

@Arcade.tool()
def analyze_pr(pr_url: str) -> dict:
    """Analyze a GitHub PR for code quality and security"""
    return {"score": 85, "issues": []]

Arcade.run()
EOF

# 启动服务（其他 Agent 通过 MCP 协议连接）
python tools.py
```

---

## 相关引用

> *"Build an MCP server in minutes, not days. Define tools, resources and prompts as Python decorators."* — Arcade-mcp README

> *"MCP Server Framework and Tool Development library for building custom capabilities into agents."* — GitHub Description

---

## 关联文章

本文与 **Cursor SDK Custom Tools + Nested Subagents** 文章形成互补闭环：

- **文章**解答了"Cursor SDK 如何在内部暴露自定义工具"
- **项目**解答了"如何把你的服务变成标准 MCP 服务器，让任何 Agent 都能用"

两者共同指向同一个核心工程模式：**工具即 MCP 服务，MCP 服务即工具**。
