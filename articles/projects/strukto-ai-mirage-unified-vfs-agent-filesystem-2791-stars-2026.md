# Mirage：用一个文件系统统一所有后端

> 仓库：[strukto-ai/mirage](https://github.com/strukto-ai/mirage)  
> Stars：2,791（持续增长）  
> 语言：TypeScript + Python  
> License：Apache 2.0  
> 发布时间：2026-05-06

---

## 核心命题

Mirage 解决了一个根本问题：当一个 Agent 需要同时操作 S3、MongoDB、Slack、Github 和 Gmail 时，它实际上在面对 **N 个 SDK + M 个 MCP 协议**。Mirage 的答案是：**用一个统一虚拟文件系统（Virtual Filesystem）代替所有这些，Agent 用同一套 bash 工具操作一切。**

笔者认为，这个项目的设计哲学比它的功能列表更有价值——它选择了一条最难但最正确的路径：**不发明新词汇，而是复用 LLM 最熟悉的词汇（Unix/bash）作为统一接口**。

---

## 解决的问题

在没有 Mirage 的世界里，一个 Agent 操作多个后端服务是这样的：

```
操作 S3 → 调 AWS SDK
操作 Gmail → 调 Gmail API  
操作 GitHub → 调 GitHub API
操作 Slack → 调 Slack API
操作 Redis → 调 redis-py
```

每个 SDK 有不同的认证方式、不同的数据结构、不同的错误处理。Agent 需要理解所有这些细节才能有效工作。

Mirage 把这个变成：

```
ls /s3/bucket-name/
cat /gmail/inbox/unread/...
cp /github/repos/... /local/
echo "message" | write /slack/channels/engineering
```

**同一个 bash 工具链，操作所有后端。**

---

## 技术架构

### 核心设计：单一根目录，多服务并排挂载

```
/                     # Mirage 虚拟根
  /ram/               # 内存盘
  /disk/              # 本地磁盘
  /redis/             # Redis
  /s3/bucket/         # S3 / R2 / OCI / Supabase / GCS
  /gmail/inbox/       # Gmail
  /gdrive/            # Google Drive / Docs / Sheets / Slides
  /github/repos/      # GitHub
  /linear/            # Linear
  /notion/            # Notion
  /slack/channels/    # Slack
  /mongodb/           # MongoDB
  /ssh/               # SSH
```

所有路径都是虚拟的，实际数据来自对应的后端服务。

### Agent 为什么用 bash

> 原文引用：「Any LLM that already knows bash can use Mirage out of the box, with zero new vocabulary.」

Unix/bash 是现代 LLM 训练数据中最密集的语料之一。LLM 对 `ls`、`cat`、`cp`、`echo`、`grep` 的语义有精确的内在理解。Mirage 复用这套词汇，而不是发明新的 API DSL。

> 原文引用：「Pipelines compose across services as naturally as on a local disk, the exact corpus modern LLMs are most heavily trained on.」

### 跨服务 Pipeline 示例

```bash
# 从 S3 读取数据 → 处理 → 写入 Notion
cat /s3/data-export/reports/q1.csv | python3 analyze.py > /notion/analytics/quarterly.md

# 监控 Slack 某频道消息 → 触发 GitHub Issue
tail -f /slack/channels/incidents | grep ERROR | while read line; do
  echo "$line" > /github/repos/infra/issues/new.txt
done

# Gmail 附件 → S3 备份
cp /gmail/inbox/attachments/*.zip /s3/backup/emails/
```

每个管道步骤的语法完全相同，Agent 不需要理解后端差异。

---

## 框架集成

Mirage 不是又一个独立运行的 Agent 框架，它**插入现有框架作为沙箱或工具层**：

| 框架 | 集成方式 |
|------|---------|
| OpenAI Agents SDK | `mirageTools(ws)` 暴露 workspace 为工具集 |
| Vercel AI SDK | 同上，Node 或浏览器 |
| LangChain | 适配器 |
| Pydantic AI | 适配器 |
| CAMEL | 适配器 |
| OpenHands | 适配器 |
| Mastra | 适配器 |

> 原文引用：「Your agent runs against the same mount tree it would in bash, so swapping the model or runtime never changes the surface.」

这意味着 Mirage 是模型/运行时无关的——同一个 mount tree，换任何模型都能工作。

---

## SDK 与工具

### Python SDK

```python
from mirage import Workspace

ws = Workspace()
ws.mount("s3", bucket="my-data")
ws.mount("gmail", credentials_file="gmail-creds.json")

# Agent 直接操作
ws.cat("/s3/reports/sales.csv")
ws.write("/gmail/drafts/intro.txt", content)
```

### TypeScript SDK

```typescript
import { Workspace } from "@strukto-ai/mirage";

const ws = new Workspace();
await ws.mount("github", { repo: "my-org/my-repo" });
await ws.write("/github/README.md", "# Hello");
```

### CLI + Daemon

```bash
# 启动 Mirage daemon
mirage daemon

# 在任意 Agent 中使用
export MIRAGE_SOCKET=/tmp/mirage.sock
ls /github/my-org/my-repo/
```

---

## 关键工程决策

### 决策 1：模拟环境，不是翻译层

大多数集成方案是「API 翻译层」——把 GitHub API 翻译成类似的文件操作。Mirage 不做翻译，它**模拟完整的文件系统语义**，包括：
- 目录树结构
- 文件读写语义
- 权限模型（rwx）
- 管道组合

这样做的问题是实现复杂，但收益是 LLM 的行为可预测——文件系统语义是标准化的，不需要学习新规则。

### 决策 2：挂载粒度可配置

不是所有数据都需要挂载。用户可以：
- 只挂载需要的几个服务
- 控制每个挂载的权限（如只读 S3，可写 GitHub）
- 克隆 snapshot 并版本化 workspace

### 决策 3：认证与权限

每个挂载服务需要各自的凭证文件。Mirage 不统一管理认证——它让每个服务保持自己的安全模型，只在访问层提供统一的虚拟化接口。

---

## 与 OpenAI 数据 Agent 的互补关系

在[上一篇文章](../orchestration/openai-in-house-data-agent-5-layer-memory-2026.md)中，OpenAI 的数据 Agent 解决了「如何让 Agent 理解跨服务的业务语义」问题。它依赖五层上下文记忆，包括 Slack/Notion 的检索。

Mirage 从不同方向解决同一个问题：**如果每个服务都呈现为文件系统，那么跨服务的操作自然变成管道组合，而不需要理解每个服务的 API 细节。**

两者结合的理想图景：
- **Mirage** 提供统一的虚拟文件系统接口
- **OpenAI 的 Layer 4/5（Institutional Knowledge + Memory）** 提供语义层上下文
- **Agent** 用 bash 操作一切，同时保留跨服务的业务语义理解

---

## 适用场景

✅ **适合**：需要跨多个服务操作的 Agent；减少 Agent 需要学习的 API 数量；让非技术用户通过自然语言操作复杂数据管道

❌ **不适合**：需要实时事务一致性的场景（如金融操作）；需要细粒度 API 控制的高频交易；挂载服务数量超过 20+ 的复杂场景（路径管理可能变复杂）

---

**执行流程**：
1. **理解任务**：本轮有两个高质量线索——OpenAI data agent（五层上下文+自调试）与 Mirage（统一VFS）
2. **规划**：Article 来自一手来源（openai.com/index），Project 来自 AnySearch 发现，Mirage 2.8K Stars 未被以独特角度写过
3. **执行**：调用 `write` 两次，分别产出 article 和 project markdown
4. **返回**：两篇文档均写入仓库目录
5. **整理**：Article → orchestration/（五层上下文主题），Project → projects/（统一VFS工具链）

**调用工具**：
- `write`: 2次（Article + Project）
- `exec`: 多次（搜索、防重检查）