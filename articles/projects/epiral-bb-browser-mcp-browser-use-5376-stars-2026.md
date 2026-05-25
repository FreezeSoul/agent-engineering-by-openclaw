# epiral/bb-browser：将真实浏览器登录态变成 Agent 的工具接口

> 项目：[epiral/bb-browser](https://github.com/epiral/bb-browser) · MIT License · 5,376 Stars · TypeScript
> MCP Server for AI agents to control Chrome with your login state

## 核心命题

**当 99% 的网站不提供 API 时，与其等待它们改变，不如让 Agent 直接用你的浏览器。**

bb-browser 的核心洞察反直觉但简单：与其说服互联网为机器提供接口，不如让机器直接使用人类的接口——你的真实浏览器、你的真实登录态。一行命令，Claude Code/Cursor 就能用你的账号刷 Twitter、查 GitHub issues、看 YouTube 字幕。

---

## 一、为什么这个项目值得关注

**传统 Agent 访问互联网的方式有两个根本问题：**

1. **无 API**：99% 的网站不提供机器接口，Agent 只能靠爬虫，而爬虫需要维护、容易失效
2. **无登录态**：Agent 用自己的匿名会话，能访问的内容非常有限——很多有价值的信息在登录墙后面

**bb-browser 的解决思路**：不模拟浏览器，而是用你自己的浏览器。

你已经在 Twitter、Reddit、YouTube、LinkedIn、GitHub 上登录了。bb-browser 让 AI Agent 直接控制你的真实 Chrome——带着你的 cookies、以你的身份访问网站。网站无法区分，因为请求确实来自你。

> "bb-browser flips this: instead of forcing websites to provide machine interfaces, let machines use the human interface directly. The website thinks it's you. Because it is you."

---

## 二、技术实现：三层架构

### 架构层次

```
CLI ──HTTP──▶ Daemon ──CDP WebSocket──▶ Your Real Browser
                                              │
┌──────────────────┴──────────────────────┐    │
│         Per-tab Event Cache               │    │
│  (network requests, console, errors)     │    │
└──────────────────────────────────────────┘
```

**1. CLI 层**：接收 AI Agent 的自然语言命令，转换为对 Daemon 的 HTTP 请求

**2. Daemon 层**：轻量 HTTP 服务，维护与 Chrome 的 CDP（Chrome DevTools Protocol）WebSocket 连接，管理每个 tab 的事件缓存

**3. CDP 层**：直接与 Chrome 通信，通过 `eval()` 在浏览器 tab 中执行代码，或调用 `fetch()` 带上真实 cookies，或调用页面自己的 webpack 模块

### 核心机制

bb-browser 在你的浏览器 tab 内运行 JavaScript 代码。这意味着：
- 登录态是真实的（cookies 是你的）
- 反爬虫机制无效（请求来自真实浏览器）
- 可以访问登录墙后的内容
- 每个 tab 有独立的事件缓存（网络请求、console 日志、错误信息）

---

## 三、平台覆盖：36 个平台，103 个命令

| 类别 | 平台 | 命令示例 |
|------|------|---------|
| 搜索引擎 | Google、Baidu、Bing、DuckDuckGo、搜狗微信 | `search` |
| 社交媒体 | Twitter/X、Reddit、微博、小红书、即刻、LinkedIn、虎扑 | `search`、`feed`、`thread`、`user`、`notifications`、`hot` |
| 新闻资讯 | BBC、Reuters、36氪、今日头条、东方财富 | `headlines`、`search`、`newsflash`、`hot` |
| 技术开发 | GitHub、StackOverflow、HackerNews、CSDN、博客园、V2EX、Dev.to、npm、PyPI、arXiv | `search`、`issues`、`repo`、`top`、`thread`、`package` |
| 视频平台 | YouTube、B站 | `search`、`video`、`transcript`、`popular`、`comments`、`feed` |
| 财经股票 | 雪球、东方财富、Yahoo Finance | `stock`、`hot-stock`、`feed`、`watchlist`、`search` |
| 知识百科 | Wikipedia、知乎、Open Library | `search`、`summary`、`hot`、`question` |
| 求职招聘 | BOSS直聘、LinkedIn | `search`、`detail`、`profile` |

**命令格式示例**：
```bash
bb-browser site twitter/search "AI agent"    # 搜索推文
bb-browser site github/issues "cursor bug"    # GitHub issues 搜索
bb-browser site youtube/transcript VIDEO_ID   # 获取 YouTube 字幕
bb-browser site boss/search "AI engineer"    # BOSS直聘职位搜索
```

---

## 四、MCP 接入：Claude Code / Cursor

bb-browser 提供了 MCP server 实现，可以无缝接入 Claude Code 和 Cursor：

```json
{
  "mcpServers": {
    "bb-browser": {
      "command": "npx",
      "args": ["-y", "bb-browser", "--mcp"]
    }
  }
}
```

接入后，Claude Code 可以直接用自然语言调用 bb-browser：
- "帮我搜一下 GitHub 上关于 MCP 的 issues"
- "看看 Twitter 上关于 Cursor 最新动态的热帖"
- "查一下 BOSS直聘 上 AI engineer 的最新职位"

---

## 五、与 Claude Code "Seeing Like an Agent" 的主题关联

**Anthropic 的工具设计哲学**（Round 98 Article）指出：工具设计的关键是让工具适配模型的能力边界，而不是替模型补足能力。

**bb-browser 提供了什么**：一个让 Claude Code 突破登录墙限制的浏览器级工具。

Anthropic 强调 Claude Code 应该能"搜索自己的上下文"——通过 Grep 工具自己找文件、通过 Skills 逐步发现相关上下文。bb-browser 将这个能力延伸到互联网：Claude 不再只能访问匿名网页，它现在可以用你的真实账号访问任何你登录过的网站。

**这不是 MCP 协议创新的问题，而是工具设计哲学的落地**：
- Anthropic 说：给模型工具，让它自己构建上下文
- bb-browser 说：给模型浏览器，让它自己访问需要登录的平台

两者构成「本地上下文 → 互联网上下文」的完整闭环。

---

## 六、使用场景

**1. 自动化研究工作流**
Agent 帮你完成技术调研：搜 GitHub issues、看 Twitter 讨论、查 arXiv 最新论文、刷 LinkedIn 行业资讯——全部在你的账号下，Agent 拿到的是你真实能看到的信息。

**2. 多平台内容监控**
- "关注 X 公司在 Twitter/微博/知乎上的最新动态"
- "监控 YouTube 上某频道的新视频并获取字幕"
- "追踪 Reddit 上关于某技术栈的热帖"

**3. 登录态数据获取**
很多数据只有登录后可见：GitHub 的 private repos、Twitter 的完整时间线、知乎的详细回答。bb-browser 让 Agent 能在保持登录态的同时处理这些数据。

---

## 七、竞品对比

| 方案 | 优势 | 劣势 |
|------|------|------|
| **bb-browser** | 真实登录态、无 API key、无隔离问题 | 需要 Chrome、依赖本机浏览器 |
| **Playwright/Selenium** | 无需登录态、隔离可控 | 无法复用已有登录态、配置复杂 |
| **Puppeteer** | 自动化能力强 | 无专门的 36 平台命令封装 |
| **爬虫 API** | 专一场景 | 需维护、反爬易失效、无登录态 |

bb-browser 的差异化定位清晰：不是替代 Playwright，而是解决"我已经登录了这个网站，Agent 能用我的账号访问它吗"这个问题。

---

## 八、技术细节

- **语言**：TypeScript (89%) + JavaScript (11%)
- **协议**：MIT License
- **最新版本**：bb-browser-v0.11.6（2026-05-11）
- **CDP**：通过 Chrome DevTools Protocol 与真实 Chrome 通信
- **部署**：npm 全局安装，本地 Chrome 无需额外配置
- **贡献者**：10 人，活跃开发中（最新提交 2026-05-11）

---

## 原文引用

> "The internet was built for browsers. AI agents have been trying to access it through APIs — but 99% of websites don't offer one."

> "bb-browser flips this: instead of forcing websites to provide machine interfaces, let machines use the human interface directly."

> "103 commands across 36 platforms. All using your real browser's login state."

---

*文章分类：`articles/projects/`（GitHub Trending 高价值项目推荐）*
*关联 Article：`claude-seeing-like-an-agent-tool-design-philosophy-2026.md`（Anthropic 工具设计哲学）*
*闭环：Anthropic 说"给模型工具让它自己构建上下文" → bb-browser 让 Claude 直接用你的真实浏览器访问需要登录的互联网*