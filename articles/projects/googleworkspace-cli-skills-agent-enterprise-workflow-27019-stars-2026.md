# Google Workspace CLI：让 AI Agent 操控 Gmail/Drive 的企业级工具

> **核心判断**：企业工作流的 Agent 自动化长期受困于"最后一个 mile"问题——AI Agent 能生成代码，但无法直接操作 Gmail/Drive/Calendar。Google Workspace CLI 通过 100+ SKILL.md 协议将这个 mile 缩短到零：让 AI Agent 用同一套接口操控 Google Workspace 的每一个服务，无需编写 OAuth 代码，无需维护 API 凭证，无需理解 REST 文档。
>
> 笔者认为，这比 MCP 协议的"数据层打通"更彻底——它是**行为层**的标准化，让非工程师也能通过自然语言驱动企业工具链。

---

## 一、核心命题

企业工作流自动化有一个隐藏的复杂度陷阱：**AI Agent 能生成代码，但无法直接操作 Gmail/Drive/Calendar**。要让它真正干活，你需要：

1. 写 OAuth 集成代码
2. 维护 API 凭证
3. 阅读 Google REST 文档
4. 处理分页、错误重试、权限边界

这套成本让"AI 自动化企业工作流"变成了一个需要后端工程师参与的项目，而不是业务人员用自然语言就能搞定的事。

**Google Workspace CLI（gws）把这个成本归零了。**

它用一行命令让 AI Agent 直接操控 Google Workspace 的每一个服务——Gmail、Drive、Calendar、Sheets、Docs、Chat、Admin——**内置 100+ SKILL.md 协议文件**，让 Agent 知道每个工具怎么用、什么场景用、什么权限边界。

---

## 二、为什么让笔者"哇"出来

### 1. 动态发现：Google 出新 API，gws 自动获得能力

大多数 CLI 工具是静态的——今天支持 Gmail，明天还是支持 Gmail，除非你升级版本。

gws 不一样。它从 Google Discovery Service 实时读取 API schema，在运行时动态构建命令表面。当 Google 添加新 API 端点或方法，gws **立即获得这些能力**，无需任何代码改动。

```
# 实时获得 Google 新增的 API 能力
gws drive files list --params '{"pageSize": 5}'
gws schema drive.files.list  # 内省任意方法的请求/响应 schema
```

这意味着 **gws 是一个与 Google API 同步进化的工具**——买一个，送无限。

### 2. SKILL.md 协议：让 AI Agent 真正理解"怎么做"

gws 附带 **100+ Agent Skills（SKILL.md 文件）**，每个支持的 API 一个，外加高层工作流助手和 50 个 Gmail/Drive/Docs/Calendar/Sheets 的配方。

```bash
# 一键安装所有 skills
npx skills add https://github.com/googleworkspace/cli

# 或按需安装
npx skills add https://github.com/googleworkspace/cli/tree/main/skills/gws-gmail
npx skills add https://github.com/googleworkspace/cli/tree/main/skills/gws-drive
```

这些 SKILL.md 不是普通的工具描述，而是**让 AI Agent 能自主决策的行为协议**：

- Gmail SKILL.md：教 Agent 理解"+send"是发邮件、"+reply"是回复线程、"+triage"是摘要未读邮件
- Drive SKILL.md：让 Agent 知道"file-announce"是把文件分享到 Chat space
- Calendar SKILL.md：让 Agent 理解"+agenda"使用 Google 账号时区，"+meeting-prep"准备会议议程

**这不是工具注册，是行为标准化。** MCP 打通数据层，SKILL.md 打通行为层——两者互补，缺一不可。

### 3. 企业级安全：Model Armor 集成

gws 集成了 Google Cloud Model Armor，在 API 响应到达 Agent 之前扫描提示注入：

```bash
gws gmail users messages get --params '...' \
 --sanitize "projects/P/locations/L/templates/T"
```

```
GOOGLE_WORKSPACE_CLI_SANITIZE_MODE=block  # 拦截模式
GOOGLE_WORKSPACE_CLI_SANITIZE_MODE=warn  # 警告模式
```

笔者认为，这是**企业 Agent 部署的必备防线**：prompt injection 通过外部内容（邮件、文档、聊天消息）注入是 Agent 安全中最难防守的向量，gws 在数据入口处就加上了一道过滤。

---

## 三、技术原理解析

### 架构：两阶段解析 + 动态构建

gws 使用两阶段解析策略：

```
阶段 1：读取 argv[1] 识别服务（如 drive、gmail）
阶段 2：获取服务的 Discovery Document（缓存 24h）
       → 构建 clap::Command 树
       → 重新解析剩余参数
阶段 3：认证 + 构建请求 + 发送
```

这套架构的结果是：**gws 的命令表面是 Google API 的忠实映射**，没有手工维护的滞后，没有版本不一致的问题。

### 认证层次：多种场景全覆盖

| 优先级 | 认证源 | 说明 |
|--------|--------|------|
| 1 | `GOOGLE_WORKSPACE_CLI_TOKEN` | 预获取的 Access Token（最高优先级）|
| 2 | `GOOGLE_WORKSPACE_CLI_CREDENTIALS_FILE` | OAuth 凭证 JSON（用户或服务账号）|
| 3 | `gws auth login` | 加密存储的凭证（AES-256-GCM）|
| 4 | `~/.config/gws/credentials.json` | 明文凭证（最低优先级）|

**凭证加密存储**（macOS Keychain 或 Linux libsecret），密钥在 OS Keyring 或 `~/.config/gws/.encryption_key`，从不写入磁盘。

### 辅助命令：超越 Discovery 的手工优化

除了自动生成的 Discovery 方法，gws 还提供手工制作的辅助命令（以 `+` 前缀区分）：

| 服务 | 命令 | 功能 |
|------|------|------|
| gmail | `+send` | 发送邮件 |
| gmail | `+reply` | 自动处理线程回复 |
| gmail | `+triage` | 未读收件箱摘要（发件人、主题、日期）|
| gmail | `+watch` | 监控新邮件并流式推送 NDJSON |
| sheets | `+append` | 追加行到电子表格 |
| calendar | `+agenda` | 显示今日日程（使用账号时区）|
| workflow | `+standup-report` | 晨会摘要（今日会议 + 待办任务）|
| workflow | `+meeting-prep` | 会议准备：议程、参会人、关联文档 |
| modelarmor | `+sanitize-prompt` | 通过 Model Armor 模板清理用户提示 |

**时间感知辅助命令**（`+agenda`、`+standup-report`、`+weekly-digest`）自动使用 Google 账号时区，支持 `--timezone` 覆盖。

---

## 四、竞品对比

| 维度 | gws | googleapis/google-api-python-client | 其他 Google CLI |
|------|-----|-------------------------------------|----------------|
| **命令来源** | 动态 Discovery | 手工维护 | 静态编译 |
| **Agent Skills** | 100+ SKILL.md | 无 | 无 |
| **输出格式** | 结构化 JSON | 杂糅 | 文本 |
| **Model Armor** | 原生集成 | 无 | 无 |
| **多账号支持** | 是 | 否 | 否 |
| **许可** | Apache-2.0 | Apache-2.0 | 各异 |

笔者认为，gws 的差异化不是"更好的 API 包装"，而是**第一个将企业工具链的 Agent 化当作产品目标而非技术副产品的项目**。100+ SKILL.md 协议文件是最直接的证明——这不是工具，是**行为标准库**。

---

## 五、使用场景

### 场景 1：AI Agent 处理 Gmail 工作流

```bash
# Agent 自动分类邮件并发送汇总
gws gmail +triage  # 未读邮件摘要
gws gmail +send --to team@example.com --subject "Daily Summary" --body "..."

# 监控特定发件人的邮件
gws gmail +watch | jq -r '.from == "boss@company.com"'
```

### 场景 2：Agent 驱动 Google Sheets 报告

```bash
# 读取数据
gws sheets +read --spreadsheet SPREADSHEET_ID --range Sheet1!A1:C10

# 追加新数据
gws sheets +append --spreadsheet SPREADSHEET_ID --values "Alice,95"
```

### 场景 3：会议自动化准备

```bash
# 晨会摘要
gws workflow +standup-report

# 下一个会议准备
gws workflow +meeting-prep
```

### 场景 4：Drive 文件自动归档

```bash
# 上传文件
gws drive +upload ./report.pdf --name "Q1 Report"

# 通知到 Chat space
gws workflow +file-announce --file-id FILE_ID --space SPACES_ID
```

---

## 六、落地指引

### 安装

```bash
# npm（跨平台）
npm install -g @googleworkspace/cli

# Homebrew（macOS/Linux）
brew install googleworkspace-cli

# GitHub Releases（预编译二进制）
curl -fsSL https://github.com/googleworkspace/cli/releases/latest/download/gws-macos-arm64.tar.gz | tar -xz
```

### 认证

```bash
# 最快方式（需要 gcloud CLI）
gws auth setup

# 手动 OAuth（无 gcloud）
# 1. 在 Google Cloud Console 创建 OAuth App
# 2. 下载 client_secret.json 到 ~/.config/gws/client_secret.json
# 3. 添加测试用户（必须！）
# 4. 运行 gws auth login
```

### OpenClaw 集成

```bash
# 一键安装所有 skills 到 OpenClaw
npx skills add https://github.com/googleworkspace/cli

# 或复制特定 skills
cp -r skills/gws-* ~/.openclaw/skills/
```

### Model Armor 安全配置

```bash
# 在 .env 中配置
export GOOGLE_WORKSPACE_CLI_SANITIZE_TEMPLATE="projects/P/locations/L/templates/T"
export GOOGLE_WORKSPACE_CLI_SANITIZE_MODE="block"  # 拦截模式
```

---

## 七、笔者观点

Google Workspace CLI 的价值不是"又一个 Google API 包装工具"，而是**第一个将企业工具链 Agent 化作为核心产品目标的项目**。

100+ SKILL.md 协议文件是最直接的证据：这不是技术演示，是**行为标准库**——每个 skill 都是一个让 AI Agent 能自主决策的工作流单元。

在 SKILL.md 协议生态中，gws 的定位是 **"企业工具链 SKILL.md 库最完整的实现"**。从 R357 的"非工程师 Agent 构建"视角看，这是让业务人员用自然语言驱动企业工具链的关键拼图——不是 MCP 的数据层打通，是行为层的标准化。

---

## 八、项目信息

| 项目 | 值 |
|------|------|
| **Stars** | 27,019 ⭐（持续增长）|
| **License** | Apache-2.0 |
| **语言** | Rust + Node.js |
| **GitHub** | https://github.com/googleworkspace/cli |
| **Agent Skills** | 100+ SKILL.md 文件 |
| **最新版本** | v0.x（活跃开发中）|

> 🔴 **注意**：这不是 Google 官方产品（"This is not an officially supported Google product"），但由 Google Workspace 团队维护，质量有保障。