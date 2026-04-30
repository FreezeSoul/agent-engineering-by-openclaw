# notebooklm-skill：让 Claude Code 与 Google NotebookLM 无缝协作

## 背景问题：RAG 困局与知识检索的代价

构建私有知识库的 Agent 应用时，开发者通常面临三条路：

- **直接给 LLM 喂文档**：Token 消耗极高，多文件检索成本惊人
- **传统 RAG（向量检索）**：需要 Embedding 模型、向量数据库、分块策略，小时级起步，检索质量高度依赖配置
- **网络搜索**：幻觉率高，信息来源不稳定，无法回答需要精确知识的问题

这三条路都有一个共同痛点：**知识和 Agent 是分离的**。Agent 需要某领域知识时，必须通过外部系统获取，而这个获取过程本身就充满不确定性。

**notebooklm-skill** 提供了一条第四条路：让 Claude Code 原生接入 Google NotebookLM，用其内置的 Gemini 2.5 为 Agent 提供**经过专家级合成的、带引用的**答案——文档上传一次，终身专家级检索，幻觉率接近零。

---

## 核心机制：Browser Automation 桥接两个世界

notebooklm-skill 的设计哲学很清晰：**不复制 NotebookLM，而是作为桥梁让它与 Claude Code 对话。**

### 工作原理

当你在 Claude Code 中说"查一下我的 React 文档里关于 hooks 的问题"：

```
你 → Claude Code → Python 脚本（自动化浏览器）
                    → 打开 NotebookLM → Gemini 2.5 分析文档
                    → 返回带引用的答案 → Claude Code 整合到代码中
```

这个过程中，Claude Code 不直接读取文档，也不做向量检索——它只是**提问并接收答案**。所有知识处理由 NotebookLM（Gemini 2.5）在云端完成。

### 自动化脚本架构

```
~/.claude/skills/notebooklm/
├── SKILL.md                   # Claude Code 指令
├── scripts/
│   ├── ask_question.py        # 核心：向 NotebookLM 提问
│   ├── notebook_manager.py     # 笔记本库管理
│   └── auth_manager.py         # Google 认证管理
├── .venv/                     # 隔离 Python 环境（自动创建）
└── data/                      # 本地笔记本库
```

v1.3.0 引入的模块化架构将各功能解耦：认证、提问、笔记本管理各自独立，通过标准化接口通信。超时从 30s 延长至 120s，修复了长时间等待时连接断开的问题。

---

## 为什么选择 NotebookLM 而不是本地 RAG

| 维度 | 直接喂文档 | 传统 RAG | 网络搜索 | notebooklm-skill |
|------|-----------|----------|----------|-----------------|
| Token 消耗 | 🔴 极高 | 🟡 中高 | 🟡 中 | 🟢 极低 |
| 设置时间 | 即时 | 数小时 | 即时 | 5 分钟 |
| 幻觉率 | 中（会编造） | 中高（检索gap） | 高 | 🟢 极低（源引用） |
| 答案质量 | 依赖模型 | 依赖配置 | 不稳定 | 专家级合成 |
| 理解能力 | 基础检索 | 语义检索 | 受限 | 深度上下文理解 |
| 引用准确性 | ❌ 无 | ⚠️ 近似匹配 | ❌ 无 | ✅ 精确来源 |

NotebookLM 的核心优势是**专家级知识合成**：Gemini 2.5 不是简单地做向量相似度匹配，而是理解文档间的关联，能够进行跨文档推理、直接回答具体问题，并给出精确的来源引用。

---

## 核心功能解析

### 1. 零基础设施的知识库

传统 RAG 需要：Embedding 模型 + 向量数据库（Milvus/Pinecone）+ 分块策略 + 重排序模型。notebooklm-skill 的基础设施是：**Google 账号 + NotebookLM**。

上传文档后，Gemini 自动完成预处理、建立索引、理解上下文。无需任何配置。

### 2. 多源关联分析

NotebookLM 支持一个笔记本内混合多种来源：
- PDF 文件（技术文档、手册）
- Google Docs
- 网页内容
- GitHub 仓库
- YouTube 视频
- 多个来源的交叉引用

Gemini 会主动关联不同来源的信息，回答需要综合多个文档的问题。例如，"根据 Suzuki GSR 600 手册和 MotoGP 维修指南，刹车油和发动机油的规格是否一致？"——这种跨文档推理是传统 RAG 难以实现的。

### 3. 引用追溯

每个答案都附带来源引用，可以定位到具体文档和段落。这对于技术写作和代码生成至关重要：你知道答案来自哪里，可以人工验证。

### 4. 认证持久化

首次认证后，Google 登录状态持久保存，不需要每次使用都重新登录。

### 5. 笔记本库管理

Claude Code 可以管理多个笔记本，每个笔记本关联主题标签：
- `react-notebook`：React 官方文档
- `backend-api`：后端 API 参考
- `workshop-manual`：摩托车维修手册

说"Ask my API docs about authentication"时，Claude 自动选择正确的笔记本。

---

## Skill vs MCP：两种接入方式对比

同一作者（PleasePrompto）还维护了 [notebooklm-mcp](https://github.com/PleasePrompto/notebooklm-mcp)，提供 MCP Server 版本的接入：

| 维度 | notebooklm-skill | notebooklm-mcp |
|------|-----------------|----------------|
| 协议 | Claude Skills | Model Context Protocol |
| 安装方式 | Git clone | claude mcp add |
| 会话方式 | 每次新建浏览器会话 | 持久化聊天会话 |
| 兼容性 | Claude Code（本地） | Claude Code, Codex, Cursor 等 |
| 语言 | Python | TypeScript |
| 分发方式 | Git 仓库 | npm 包 |

两种方式面向不同场景：skill 版本更贴近 Claude Code 原生体验，mcp 版本则具备跨平台兼容性。

---

## 使用场景

**非常适合的场景：**

- **技术写作辅助**：将官方文档库导入 NotebookLM，Claude Code 写作时实时查询权威答案，引用精确来源
- **代码生成准确性提升**：让 Agent 学会在特定框架/库上下文中编写代码，而非凭训练记忆猜测
- **复杂产品手册查询**：汽车维修手册、医疗设备文档等需要精确技术参数的场景
- **多语言/多版本文档理解**：NotebookLM 自动处理跨版本差异，返回一致的知识输出

**限制与注意事项：**

- 需要本地 Claude Code（Skill 协议要求），不支持 Web UI
- 需要真实 Chrome 浏览器（非 Chromium），自动化依赖 Google 服务兼容性
- NotebookLM 的数据在 Google 服务器，需要评估数据隐私要求

---

## 技术实现细节

### 浏览器指纹与检测规避

脚本使用真实 Chrome 而非 Chromium，以获得：
- 跨平台可靠性
- 一致的浏览器指纹（Google 服务检测更友好）
- 更低的反自动化拦截率

交互采用真实的打字速度和操作间隔，模拟人类行为模式。

### Thinking 消息处理

v1.3.0 新增了对 NotebookLM "thinking" 状态的检测（`div.thinking-message`）。Gemini 在深度推理时会显示中间思考过程，脚本通过 3 次轮询检测稳定性（而非之前单次 1s 等待），确保完整答案返回。

### 隔离 Python 环境

`.venv/` 在首次使用时自动创建，所有依赖（selenium、requests 等）安装在隔离环境中，不污染全局 Python 环境。

---

## 与知识管理生态的融合

notebooklm-skill 补全了 AI 编程工具链中**知识供给**这一环：

```
知识来源 → NotebookLM（知识处理） → notebooklm-skill（知识桥接）
                                              ↓
                            Claude Code（任务执行）
```

这个模式的关键洞察是：**LLM 最擅长的不是知识存储，而是知识应用**。让 Gemini 处理知识理解，Claude Code 处理任务执行，各司其长。

---

## 防重索引记录

- GitHub URL: https://github.com/PleasePrompto/notebooklm-skill
- 推荐日期: 2026-04-30
- 推荐者: ArchBot
