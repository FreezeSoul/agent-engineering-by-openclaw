# Odysseus：自托管 AI Workspace，隐私优先的本地 Agent 平台

## 推荐理由

**Odysseus（7,100 Stars）是一个功能完整的自托管 AI Workspace——集成 Chat/Agent/Deep Research/Memory/Email/Calendar 等模块，支持本地模型（vLLM/llama.cpp/Ollama）和 MCP 协议。它代表了「隐私优先 + 功能完整」的自托管 AI 平台在 2026 年的成熟形态。**

---

## 核心能力

### 多模态 Chat 与 Agent

Odysseus 支持与任何本地模型或 API 对话（vLLM · llama.cpp · Ollama · OpenRouter · OpenAI）。其 Agent 模式基于 [opencode](https://github.com/anomalyco/opencode) 构建，配备了工具集：MCP · web · files · shell · skills · memory。

### Cookbook：硬件感知模型推荐

内置的 Cookbook 模块扫描用户硬件，推荐适合的模型并支持一键下载和服务化。built on [llmfit](https://github.com/AlexsJones/llmfit)，提供 VRAM 感知评分、GGUF/AWQ/FP8 格式支持。

### Deep Research

多步骤研究工作流：从多个来源收集、阅读并综合成可视化报告。adapted from [Tongyi DeepResearch](https://github.com/Alibaba-NLP/DeepResearch)。

### Memory / Skills 持久化

基于 ChromaDB + fastembed (ONNX) 的向量 + 关键词混合检索，支持导入/导出。Agent 在长期使用中持续学习和适应用户偏好。

### Productivity Suite（Email/Calendar/Notes/Tasks）

- **Email**：IMAP/SMTP 收件箱 + AI 分拣（紧急提醒、自动标签、自动摘要、自动回复草稿、垃圾邮件过滤）
- **Calendar**：CalDAV 同步（Radicale/Nextcloud/Apple/Fastmail）
- **Notes & Tasks**：带提醒的速记清单、cron 风格定时任务（ntfy/browser/email 渠道通知）

### 响应式 Mobile 支持

PWA 可安装，支持移动端触控手势。

## 技术栈

- **前端**：JavaScript（自称 jank but fun）
- **Agent 引擎**：opencode
- **向量存储**：ChromaDB + fastembed (ONNX)
- **本地推理**：vLLM、llama.cpp、Ollama
- **协议**：MCP（Model Context Protocol）、IMAP/SMTP、CalDAV

## Stars 轨迹

| 日期 | Stars |
|------|-------|
| 2026-05-31 | 7,079 |
| 2026-06-01 | 7,100 |

5 天增长约 2,100 Stars（42%），处于快速成长期。

## 与现有 Article 的关联

| 已有关于 | 本文补充 |
|---------|---------|
| [anthropic-context-engineering-llm-attention-budget-2026](./context-memory/anthropic-context-engineering-llm-attention-budget-2026.md) | Odysseus 的 Memory/Skills 模块是 Context Engineering 的工程实践 |
| [Mirage: Unified Virtual Filesystem](./projects/strukto-ai-mirage-virtual-filesystem-agent-2591-stars-2026.md) | Odysseus 的文件/工具整合思路与 Mirage 的 VFS 抽象互补 |
| [Hugging Face smolagents](./projects/huggingface-smolagents-barebones-code-agent-27k-stars-2026.md) | 两者都强调轻量化和本地优先，但 Odysseus 更侧重平台完整性 |

## 适用场景

- **隐私敏感开发者**：不希望数据上云的独立开发者
- **本地模型爱好者**：已经在运行 vLLM/ollama，想获得 ChatGPT/Claude 级别的聚合体验
- **全栈生产力用户**：需要 AI + Email + Calendar + Notes 一体化工作流的个人用户

---

**GitHub**：https://github.com/pewdiepie-archdaemon/odysseus  
**Stars**：7,100（2026-06-01）  
**语言**：JavaScript  
**License**：需查看 README（自托管项目通常有各自许可）