# wshobson/agents: Multi-Harness Agentic Plugin Marketplace

## 核心命题

如果 browser-harness 是「让 Agent 自己写工具」，那 wshobson/agents 就是「让 Agent 自己选工具包」。这个项目做了一件事：**把 83 个插件、191 个 Agent、155 个 Skills、102 个命令，打包成跨 5 个主流 Coding Harness（Claude Code / Codex / Cursor / OpenCode / Gemini CLI）的通用市场**。不是翻译，不是适配，而是让每个 harness 拿到原生格式的工件。

![GitHub](screenshots/wshobson-agents-multi-harness-marketplace-2026-05-31.png)

## 一、为什么这个项目值得关注

### 1. 一源多 harness：每个平台拿到的都是「原生货」

传统插件市场的问题：用 Claude Code 写的插件，换到 Cursor 就得重写——要么功能阉割，要么体验降级。

wshobson/agents 的解法是 **「一个源头，五套原生产出」**：

```
plugins/python-development/
├── .claude-plugin/plugin.json    → Claude Code 原生
├── agents/                       → Codex 原生
├── commands/                     → Cursor 原生
└── skills/                       → OpenCode/Gemini 原生
```

这不是「翻译」，而是每个 harness 都从同一套源码生成自己平台的原生格式。这需要理解每个 harness 的插件系统，才能做到真正的 idiomatic 产出。

### 2. 规模：83 插件 + 191 Agent + 155 Skills + 102 命令

| 类型 | 数量 | 说明 |
|------|------|------|
| **Plugins** | 83 | 单插件 = 可独立安装的最小单元 |
| **Agents** | 191 | 领域专家（架构/语言/infra/安全/数据/ML/文档/商业/SEO）|
| **Skills** | 155 | 模块化知识包，按需渐进加载 |
| **Commands** | 102 | 斜杠命令（脚手架/安全扫描/测试生成/infra配置）|
| **Orchestrators** | 16 | 多 Agent 协调工作流 |

这是一个**完整的 Agent 工具生态**，不是点工具，而是一个能覆盖整个软件工程生命周期的工具矩阵。

### 3. 三层模型策略：让合适的模型做合适的事

| 层级 | 模型 | 职责 |
|------|------|------|
| Tier 1 | Opus 4.7 | 架构决策、安全审查、生产级代码审查 |
| Tier 2 | inherit | 用户自选（后端/前端/AI/ML/专业领域）|
| Tier 3 | Sonnet | 文档、测试、调试、API 参考 |
| Tier 4 | Haiku | 快速运营任务、SEO、部署、内容 |

这个分层策略的洞见在于：**不是所有任务都需要最强的模型**，但现有的 Agent 框架往往把模型选择权完全交给用户或硬编码。wshobson/agents 把模型路由作为插件系统的一部分，让每个插件可以声明自己的模型偏好。

### 4. 跨平台支持：5 个主流 Coding Harness 全覆盖

```
✅ Claude Code — 原生插件格式
✅ Codex CLI — 通过 npx codex-marketplace
✅ Cursor — 通过 /plugin install
✅ OpenCode — 通过 make generate + symlink
✅ Gemini CLI — 通过 make generate + extensions install
✅ GitHub Copilot — 通过 committed registries
```

这是目前覆盖最广的 Coding Agent 插件市场。如果你在多个平台间切换，这个市场可以作为统一的工具来源。

## 二、技术原理：从插件到多平台原生工件

### 核心机制：每个 harness 有自己的生成器

```bash
make generate HARNESS=gemini   # 为 Gemini CLI 生成原生格式
make generate HARNESS=opencode  # 为 OpenCode 生成原生格式
```

每个 harness 都有自己的生成逻辑，理解该平台的数据结构、加载方式、权限模型，然后从 `plugins/` 源码生成对应的工件。这个生成过程是 idempotent 的——可以反复运行，每次都产出一致的平台原生包。

### 插件结构示例

```
plugins/python-development/
├── .claude-plugin/plugin.json  # Claude Code 格式
├── agents/                     # 多 harness 兼容的 Agent 定义
│   ├── python-pro/             # 高级 Python 工程
│   ├── django-pro/             # Django 专家
│   └── fastapi-pro/            # FastAPI 专家
├── commands/
│   └── scaffold/                # 脚手架命令
└── skills/
    ├── async/                  # 异步编程技能
    ├── testing/                # 测试技能
    ├── packaging/              # 打包技能
    └── ...（16个专业技能）
```

### 安装体验

```bash
# Claude Code
/plugin marketplace add wshobson/agents
/plugin install python-development

# Codex CLI
npx codex-marketplace add wshobson/agents

# Gemini CLI
gh repo clone wshobson/agents ~/agents && cd ~/agents
make generate HARNESS=gemini && gemini extensions install .
```

## 三、与 Agent Engineering 的主题关联

### 多 Agent 编排：16 个 Orchestrators

wshobson/agents 提供了 16 个多 Agent 协调工作流：

- **full-stack** — 全栈开发协调
- **security** — 安全扫描协调
- **ML** — 机器学习协调
- **incident-response** — 事故响应协调

每个 orchestrator 都是一个多 Agent 系统，定义了 Agent 之间的协作模式和通信方式。这与 SKILL 中「Orchestration」主题直接对应。

### Skills 系统：按需加载的模块化知识

155 个 Skills 构成了一个完整的知识体系，Agent 在需要时加载，不需要时不占用 context。这个设计完全符合 SKILL 中「Skill Registry」主题的核心理念：

> 一个 Skill 就是一个可复用的能力单元，Agent 在遇到对应任务时自动激活。

### 三层模型路由：Agent 级别的模型选择

这个项目把模型选择从「框架配置」提升到了「插件元数据」层面。每个插件可以声明自己需要的模型层级，这让工具本身携带了智能选择的「基因」。

## 四、适合谁用

✅ **在多个 Coding Harness 间工作的工程师**（Claude Code + Cursor + Codex 等）  
✅ **想要一个统一工具市场而不是每个平台单独配置的团队**  
✅ **需要领域专家 Agent（安全/ML/架构/数据）的场景**  
✅ **正在构建插件系统需要参考设计模式的框架开发者**  
❌ **只用单一平台、不需要跨平台工具的开发者**（用平台自己的市场就好）

## 五、快速上手

### 添加市场（Claude Code）

```bash
/plugin marketplace add wshobson/agents
```

### 安装插件

```bash
/plugin install python-development    # Python 全栈开发
/plugin install security-scanner      # 安全扫描
/plugin install ml-pipeline           # ML 管道
```

### 查看所有可用插件

```bash
# 详见文档
docs/plugins.md
docs/agents.md
docs/agent-skills.md
docs/commands.md
```

## 六、笔者判断

wshobson/agents 是一个**工程量极大的跨平台工具市场**，它的价值不在于「有多少插件」，而在于它解决了 **「同一套工具如何在多个 Agent 平台原生工作」** 这个真正困难的问题。

ECC（199K Stars）是一个完整的 Harness 系统，而 wshobson/agents 更像是一个 **Harness 的插件商店**——它假设你已经有一个 Harness，然后在上面提供一个统一的高质量工具矩阵。

笔者认为，如果你在构建多平台支持的 Agent 系统，或者需要在团队内共享 Agent 工具，这个项目的架构设计（源码 → 多平台原生生成的生成器模式）值得深入研究。它展示了一种优雅的「插件」思路：**工具本身不需要知道目标平台，实现者和平台之间有一层生成器解耦**。

---

**关联文章**：
- [affaan-m/ECC: Agent Harness Performance System](articles/projects/affaan-m-ECC-harness-performance-optimization-190k-stars-2026.md)（完整 Harness 系统参考）
- [Awesome Harness Engineering](articles/projects/ai-boost-awesome-harness-engineering-2026.md)（Harness Engineering 知识地图）

**Stars**: 36,167 | **Language**: Python | **GitHub**: [wshobson/agents](https://github.com/wshobson/agents)