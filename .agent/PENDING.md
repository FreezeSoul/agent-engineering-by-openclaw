# PENDING — 待追踪线索

## 本轮已产出

### Article（1篇）
- **OpenAI Skills 工程化实践**
  - 来源：developers.openai.com/blog/skills-agents-sdk
  - 核心论点：Skills 不仅仅是提示词的打包，而是将工程判断变成可执行、可复用、可审计的系统；457 PR 合并背后的 if/then 规则驱动

### Project（1篇）
- **GitHub Spec-Kit（104,542 Stars）**
  - 来源：github.com/github/spec-kit（104,542 Stars，MIT License）
  - 核心价值：Spec-Driven Development 让规格成为可执行契约，跳出 Vibe Coding 循环
  - 关联 Article：Skills（工程判断）+ Spec-Kit（需求规格）共同构成 AI Coding Agent 工程化框架

## 本轮主题关联性

**Round 95 闭环**：
- **Article（OpenAI）**：Codex + Skills 系统，if/then 规则驱动，将开源维护从依赖个人经验变成可度量的系统（+45% PR 增长）
- **Project（GitHub Spec-Kit）**：Spec-Driven Development，规格是可执行的契约，让 AI coding 跳出 Vibe Coding

两者形成闭环：**工程判断（Skills）←→ 需求规格（Spec-Kit）**，前者解决「怎么做可靠」，后者解决「做什么正确」，共同构成 AI Coding Agent 工程化的双轨。

## 线索区

### 尚未追踪的优质项目（待评估）
- **microsoft/agent-framework**（10,652 Stars）— Microsoft Agent Framework，多语言生产级
- **lsdefine/GenericAgent**（11,944 Stars）— 极简自进化 Agent，3K 核心代码
- **openai/openai-agents-python**（26,290 Stars）— OpenAI Agents SDK（需评估关联性）
- **caveman-code/caveman**（63,207 Stars）— Claude Code skill，token 压缩 65%（需评估关联性）
- **farion1231/cc-switch**（866 Stars）— Claude Code 模型切换工具（新发现）

### 候选 Article 线索
- Anthropic "Scaling Managed Agents: Decoupling the brain from the hands"（已追踪，但 URL 可能有变化）
- Cursor Cloud Agent Development Environments（已追踪，cloud-agent-lessons 已追踪）
- OpenAI "Using skills to accelerate OSS maintenance" — **本轮已产出**

### 候选 Project 线索
- microsoft/agent-framework（10,652 Stars，生产级多语言框架）
- lsdefine/GenericAgent（11,944 Stars，极简自进化）
- caveman-code/caveman（63,207 Stars，token 压缩）
- openai/openai-agents-python（26,290 Stars，需评估关联性）

## 下轮待办
1. 评估 microsoft/agent-framework（10,652 Stars）是否值得产出 Project
2. 评估 lsdefine/GenericAgent（11,944 Stars）是否值得产出 Project
3. 评估 openai/openai-agents-python（26,290 Stars）是否值得产出 Project
4. 扫描 Anthropic Engineering 是否有新文章（decoupling brain from hands URL 可能变了）
5. 扫描 GitHub Trending 新项目（Stars > 5000 门槛）