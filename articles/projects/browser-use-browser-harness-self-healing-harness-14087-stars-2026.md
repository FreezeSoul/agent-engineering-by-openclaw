# browser-use/browser-harness: Self-Healing Browser Harness for Coding Agents

## 核心命题

browser-harness 解决了一个让所有Coding Agent难堪的问题：**当浏览器任务需要未定义的工具时，Agent 只能报错或放弃**。它的解法是让 Agent 自己在执行过程中写缺失的帮助函数——每跑一次，harness 就自我进化一次。这不是普通的浏览器自动化，这是 **会自我进化的 Harness Engineering 教科书案例**。

![GitHub](screenshots/browser-use-browser-harness-2026-05-31.png)

## 一、为什么这个项目值得关注

### 1. 自愈机制：Agent 写代码，Harness 变强

传统的浏览器自动化框架需要开发者预先定义所有可能用到的工具。browser-harness 反其道而行：

```
agent: wants to upload a file
│
agent-workspace/agent_helpers.py → helper missing
│
agent writes it                         agent_helpers.py
                                                    + custom helper
✓ file uploaded
```

当 Agent 遇到缺失的帮助函数时，它不是报错退出，而是**直接在 `agent_helpers.py` 里写一个新的**。这个文件是 agent 可编辑的空间，也是 harness 的进化存储。每次运行都在积累新的能力。

笔者认为，这种「运行时自愈」的设计，比预定义工具集的方式更接近真实人类工程师的工作方式——遇到问题，当场解决，顺便把解决方案固化下来。

### 2. 极简架构：1000行代码，4个核心文件

| 文件 | 作用 |
|------|------|
| `install.md` | 首次安装和浏览器引导 |
| `SKILL.md` | 日常使用指南 |
| `src/browser_harness/` | 核心包（受保护） |
| `agent-workspace/agent_helpers.py` | Agent 可编辑的帮助函数 |
| `agent-workspace/domain-skills/` | 可复用的站点技能 |

整个 harness ~1000 行代码，却实现了完整的自愈循环。架构清晰度值得所有 Harness Engineering 学习。

### 3. CDP 直连：无中间层，只有 Agent 和浏览器

```text
Agent ←→ (WebSocket) ←→ Chrome CDP ←→ Real Browser
```

一个 WebSocket 连接 Chrome 的远程调试端口，没有任何额外的自动化框架在中间。Agent 直接与浏览器对话，写入自己的 helpers。这个设计让 browser-harness 成为了真正的「薄 harness」——它只提供连接，不提供智能，所有智能都由 Agent 自行生成。

### 4. 自我进化：每跑一次，能力多一分

这个项目的核心理念是：**Harness 改进不是靠开发者，而是靠 Agent 在每次执行中自动完成**。当 agent 遇到并修复一个问题时，这个修复就被固化在 `agent_helpers.py` 里，成为 harness 的一部分。

这不是传统意义上的「框架更新」，而是**让 Agent 成为 harness 的共同开发者**。

## 二、技术原理：从问题到解法

### 问题：现有浏览器自动化框架的局限性

现有的浏览器自动化框架（如 Playwright、Puppeteer）需要开发者预先定义好所有可能用到的操作。当 Agent 遇到一个框架未覆盖的场景时，只能：

1. 报错退出
2. 用低级 `executeScript` 硬撑
3. 等待框架维护者更新

这对需要长时间运行、需要处理多样化任务的 Agent 来说，是致命的。

### 解法：开放写入权限，让 Agent 自我扩展

browser-harness 的解法是把 `agent_helpers.py` 作为 Agent 可写的空间。当 Agent 发现缺少某个帮助函数时，它可以直接写一个：

```python
# agent_helpers.py — Agent writes these
async def upload_file_to_form(page, file_path, selector):
    """Upload file using a file input selector"""
    file_input = await page.query_selector(selector)
    await file_input.set_input_files(file_path)

async def fill_dynamic_form(page, fields):
    """Fill form fields dynamically based on page structure"""
    for field in fields:
        el = await page.query_selector(field['selector'])
        await el.fill(field['value'])
```

这些函数在首次运行时由 Agent 写出来，之后就成为 harness 的一部分。这是一个**边执行边进化的工程机制**，完全符合 Harness Engineering 的核心理念。

### 自愈循环的技术实现

```
1. Agent 执行任务 → 需要 upload_file
2. 检查 agent_helpers.py → 没有这个函数
3. Agent 分析需求 → 写一个新的 upload_file_to_form()
4. 执行成功 → 函数固化到 agent_helpers.py
5. 下次运行 → upload_file 已有定义
```

## 三、与 Agent Engineering 的主题关联

### Harness Engineering 的教科书实现

browser-harness 是 Harness Engineering 领域的教科书级案例。根据 SKILL 中对 Harness 的定义：

> Harness = 环境配置 + 状态管理 + 验证机制 + 控制机制，让 Agent 能在长任务中稳定工作

browser-harness 在每一个维度都做得极致：

| 维度 | browser-harness 实现 |
|------|---------------------|
| **环境配置** | CDP 直连 Chrome，零中间层 |
| **状态管理** | agent_helpers.py 固化每次运行的状态 |
| **验证机制** | Agent 执行成功 = 验证通过 |
| **控制机制** | Agent 可编辑 helpers，控制权在 Agent |

### 对比现有 Harness 项目

| 项目 | Stars | 特点 | 定位 |
|------|-------|------|------|
| **browser-harness** | 14,087 | 自愈式进化，CDP直连 | 浏览器专用 |
| **ECC** | 199K | Skills+Instincts+Memory完整系统 | 全栈 Harness |
| **hive** | 10,408 | 多Agent编排 | 生产级 Harness |
| **revfactory/harness** | 4,202 | Team-Architecture Factory | 企业级 Harness |

browser-harness 是其中**最小、最专注、最独特的自愈机制实现**。它的价值不在于功能丰富，而在于它揭示了一个核心洞见：**让 Agent 自己写 harness，harness 才会真正进化**。

## 四、适合谁用

✅ **需要处理复杂浏览器任务的 Coding Agent 用户**  
✅ **正在研究 Harness Engineering 想要看实战案例的开发者**  
✅ **需要让 Agent 处理需要未知工具的动态任务场景**  
❌ **只需要简单固定操作的浏览器自动化场景**（用 Playwright 就好）  
❌ **生产级需要完整维护和监控的企业场景**

## 五、快速上手

### 安装

```bash
# Clone repo
gh repo clone browser-use/browser-harness
cd browser-harness

# 读取安装指南
cat install.md
```

### 连接浏览器

1. 打开 Chrome，访问 `chrome://inspect/#remote-debugging`
2. 勾选 "Allow remote debugging"
3. Chrome 弹出时点击 "Allow"

### 启动 Agent

```bash
# 告诉 Claude Code 或 Codex 设置这个 harness
Set up https://github.com/browser-use/browser-harness for me.
Read \`install.md\` and follow the steps to install browser-harness and connect it to my browser.
```

### 观察自愈过程

当你给 Agent 一个需要未知工具的浏览器任务时，观察：

1. Agent 发现缺失帮助函数
2. Agent 自己写一个新的
3. 任务成功执行
4. agent_helpers.py 多了一个新函数

## 六、笔者判断

browser-harness 是一个**思路极简但洞见极深**的项目。它没有试图做一个功能完备的浏览器自动化框架，而是抓住了 Harness Engineering 的核心：**好的 harness 不是给 Agent 一套工具，而是给 Agent 写工具的能力**。

当大多数 Harness 项目在比拼「预定义了多少工具」时，browser-harness 在做一件完全相反的事：**让工具在被需要时由 Agent 自行生成**。这个思路如果扩展到其他领域（比如文件操作、代码执行、网络请求），可能会催生出真正能适应任何任务的通用型 Agent Harness。

笔者认为，这是 2026 年最值得研究的 Harness Engineering 案例之一，尤其适合正在构建自己的 Agent 框架或研究 Harness 自愈机制的工程师。

---

**关联文章**：
- [Anthropic: Effective harnesses for long-running agents](articles/harness/anthropic-effective-harnesses-long-running-agents.md)（Harness Engineering 核心理论）
- [Awesome Harness Engineering](articles/projects/ai-boost-awesome-harness-engineering-2026.md)（Harness Engineering 知识地图）

**Stars**: 14,087 | **Language**: Python | **GitHub**: [browser-use/browser-harness](https://github.com/browser-use/browser-harness)