---
title: "cc-connect：跨 13 个 IM 的本地 AI Agent 桥接（12.9K Stars）"
date: 2026-06-24
tags: [cc-connect, Claude Code, Codex, Slack, Feishu, DingTalk, Multi-Agent, IM-Bridge, Harness]
description: cc-connect 把本地 AI Coding Agent（Claude Code / Cursor / Codex / Gemini CLI）桥接到 13 个 IM 平台，multi-bot relay + 完整 chat 控制 + 多项目架构 = Claude Tag 模式的工程实现。
---

# chenhg5/cc-connect：让本地 AI Coding Agent 跨 13 个 IM 平台协作（12.9K Stars）

> GitHub：[chenhg5/cc-connect](https://github.com/chenhg5/cc-connect)  
> Stars：**12,900+** | License：MIT | 最新版：v1.3.3 stable  
> 维护：chenhg5（中国开发者，Trendshift 收录）

## 核心亮点

**cc-connect 是一个本地代理，把 10+ AI Coding Agent 桥接到 13 个 IM 平台（Slack / Feishu / DingTalk / Telegram / Discord / WeChat Work / LINE / QQ / Matrix 等）。** 当 Claude Tag 在 Slack 内部署了「常驻 @Claude」时，cc-connect 已经把这个模式**开源 + 跨平台 + 多 agent**地工程化。

**与 Claude Tag 的关系**：Claude Tag 是 Anthropic 的**官方垂直方案**（Slack-only，Opus 4.8 only，企业控制）；cc-connect 是**社区横向方案**（13 平台、10+ agent、本地部署、MIT 协议）。两者解决同一类问题（Agent 进 IM 协作），但 cc-connect 把「桥接」从单一服务变成**通用能力**。

---

## 一、平台覆盖（13 个 IM）

| IM 平台 | Text | Markdown | Streaming | 文件/图片 | 语音 | DM | Group |
|--------|:----:|:--------:|:---------:|:--------:|:----:|:--:|:-----:|
| Feishu (Lark) | ✅ | ✅ | ✅ | ✅ | ⚠️ | ✅ | ✅ |
| DingTalk | ✅ | ✅ | ✅ | ✅ | ⚠️ | ✅ | ✅ |
| Slack | ✅ | ✅ | ✅ | ✅ | ⚠️ | ✅ | ✅ |
| Telegram | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Discord | ✅ | ✅ | ✅ | ✅ | ⚠️ | ✅ | ✅ |
| WeChat Work (WeCom) | ✅ | ⚠️ | ✅ | ✅ | ⚠️ | ✅ | ✅ |
| LINE | ✅ | ✅ | ✅ | ⚠️ | ❌ | ✅ | ✅ |
| WPS Xiezuo (金山协作) | ✅ | ✅ | ✅ | ❌ | ❌ | ✅ | ✅ |
| Weibo | ✅ | ❌ | ✅ | ❌ | ❌ | ✅ | ❌ |
| Weixin (personal) | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| QQ / QQ Bot | ✅ | ✅ | ✅ | ✅ | ⚠️ | ✅ | ✅ |
| Matrix | ✅ | ⚠️ | ✅ | ✅ | ❌ | ✅ | ✅ |

**大多数平台零公网 IP 需求**（用长连接 / WebSocket 风格），这在企业内网部署是巨大优势。

---

## 二、Agent 覆盖（10+ Coding Agent）

### 2.1 官方 first-class 支持

- **Claude Code**（Anthropic）— Opus 1M-context, append_system_prompt, PermissionRequest hooks
- **Codex**（OpenAI）— request_user_input app-server events
- **Cursor Agent** — Composer mode
- **Devin CLI**（Cognition）
- **GitHub Copilot CLI**
- **Google Antigravity**（`agy`）
- **Gemini CLI**
- **Kimi CLI**（Moonshot）
- **Qoder CLI**
- **OpenCode**
- **iFlow CLI**
- **Pi**
- 任何支持 [Agent Client Protocol (ACP)](https://agentclientprotocol.com/get-started/agents) 的 agent

### 2.2 关键差异：agent 间可以协作

> *"Multi-Bot Relay — Bind multiple bots in a group chat and let them communicate with each other. Ask Claude, get insights from Gemini — all in one conversation."*

这是**真正的 multi-agent 协作**，不是「单 agent 多模型」——不同 agent 在同一 group chat 中**互相对话**，形成**collaborative reasoning**。Claude 写代码 → Gemini review → Cursor 优化测试 → 都在同一个 Slack 线程里可见。

这与 Anthropic Claude Tag 的「一个 channel 一个 Claude」是同源思路，但 cc-connect 把「多 agent」做了**显式扩展**。

---

## 三、Chat 端完整控制（Claude Tag 模式的开源实现）

### 3.1 Slash Commands

| Command | 功能 |
|---------|------|
| `/model` | 切换 agent 模型（如 Sonnet → Opus） |
| `/reasoning` | 调 reasoning effort（low/medium/high） |
| `/mode` | 切换 permission mode（accept-edits / plan / bypass-permissions） |
| `/dir <path>` | 切换工作目录 |
| `/memory` | 读写 agent 指令文件 |
| `/timer` | 一次性延迟任务 |
| `/cancel` | 中断当前 turn |
| `/ps` | 进程状态 |
| `/permit` | 授权 IM 发送者 |

### 3.2 与 Claude Tag 4 大特性的对应

| Claude Tag | cc-connect |
|------------|-----------|
| Multiplayer | ✅ Multi-Bot Relay（多 agent 多人） |
| Learns Over Time | ✅ `/memory` 持久化 |
| Takes Initiative (Ambient) | ✅ `cron` 调度 + scheduled tasks |
| Works Asynchronously | ✅ 长任务 streaming + 跨 turn 持续 |

**关键差异**：Claude Tag 的 ambient 是**单一 Claude 主动**；cc-connect 的 ambient 是**多 agent 协同主动**（如每天 6am 总结 GitHub trending）。

---

## 四、生产级工程特性

### 4.1 Multi-Project 架构

> *"One process, multiple projects, each with its own agent + platform combo."*

单进程管理多项目（每个项目独立的 agent + IM 配对），比 Claude Tag 的「one channel one identity」更细粒度。

### 4.2 Long-Running Turn Hardening

> *"new `max_turn_time_mins` wall-clock cap with soft-stop + force-kill + auto-resume so a long bash / test command can no longer lock a session indefinitely"*（#1091）

这是从「demo-grade」到「production-grade」的关键工程细节——长 bash/test 命令超时机制：soft stop（礼貌取消）→ force kill（强制）→ auto resume（自动续期）。

### 4.3 OS-User Isolation

> *"run_as_user — switch OS user per project, so each agent runs in an isolated OS account"*

每个项目可以指定**不同的 OS user** 运行。这是**安全 + multi-tenant** 的工程实现层——和 Claude Tag 的「channel-scoped identity」是同源思路，但放到 OS 级别。

### 4.4 Provider 生态

NekoCode、VisionCoder、AIHubMix、MiniMax M3 presets——表明**该项目的用户已经形成「多 provider 路由」的工作流**，与单一官方 provider 相比有显著的成本/可用性优势。

---

## 五、v1.3.3 stable（2026-06 关键更新）

- **3 个新 agent first-class**：Devin CLI / Google Antigravity / GitHub Copilot CLI
- **Slack Assistant API** 支持（直接对标 Claude Tag 的核心 API）
- **QQ Bot inline keyboards** + **Feishu audio/video native media**
- **DingTalk @mentions / richText / image / file inbound** 完整支持
- **Provider resume regression suite**（codex / opencode / kimi 的 provider 恢复测试）
- **≈ 235 PRs since v1.3.2**，community-driven evolution 信号强

---

## 六、Install（3 种方式）

### 6.1 npm（最简）
```bash
npm install -g cc-connect
```

### 6.2 Homebrew
```bash
brew install cc-connect
```

### 6.3 AI Agent 自动安装（最炫）
> *"Send this to Claude Code or any AI coding agent, and it will handle the entire installation and configuration for you."*

```bash
Follow https://raw.githubusercontent.com/chenhg5/cc-connect/refs/heads/main/INSTALL.md to install and configure cc-connect.
```

**「meta-bootstrap」**：让 Claude Code 自己安装 cc-connect——这是 AI agent **自动部署 AI agent 协作基础设施** 的范本。

---

## 七、关联性：与 Claude Tag 的「正交」关系

| 维度 | Claude Tag | cc-connect |
|------|-----------|-----------|
| 来源 | Anthropic 官方 | 社区开源 |
| 平台 | Slack only | 13 个 IM |
| Agent | Claude Opus 4.8 only | 10+ coding agents |
| 部署 | 云托管（企业控制） | 本地 + 自托管 |
| 协议 | 闭源 | MIT |
| Multi-agent | ❌ 单一 Claude per channel | ✅ Multi-Bot Relay |
| 社区驱动 | ❌ | ✅ 235 PRs / 12.9K stars |

**两者是「vertical 官方方案」vs「horizontal 社区方案」的关系**——Claude Tag 设定了 Slack 内部署的标准，cc-connect 把这个标准**复用到 13 个平台 + 10 个 agent**。

对企业用户：
- **需要数据完全控制** → cc-connect（本地部署 + MIT）
- **想要 Anthropic 官方支持 + 最简配置** → Claude Tag（Enterprise / Team）
- **多 agent 协作** → 两者结合（Claude Tag + cc-connect 把其他 agent 接入）

---

## 八、总结

cc-connect 的工程价值在于：**它把「AI agent 进 IM 协作」从一个单点产品（Claude Tag）变成可复用的基础设施**。

三个数字值得关注：
- **12.9K stars** — 表明「IM 内部署 AI agent」是真实需求
- **13 平台 × 10 agent = 130 组合** — 表明「多对多桥接」是产品形态而非单点
- **235 PRs / 单版本** — 表明 community-driven 演化速度比官方单点方案快

如果 Claude Tag 是「**AI 同事成为 Slack 居民**」的官方范式，cc-connect 就是「**AI 同事成为全球 IM 居民**」的开源范式。两者不冲突——一个是企业的官方答案，一个是社区的开源答案。
