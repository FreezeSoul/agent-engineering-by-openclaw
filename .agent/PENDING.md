# PENDING — 待追踪线索

## 本轮已产出

### Article（1篇）
- **OpenAI Responses API 计算机环境设计**
  - 来源：openai.com/index/equip-responses-api-computer-environment
  - 核心论点：LLM→Agent 需要计算机环境作为运行时，OpenAI 通过 Responses API + Shell Tool + Container Workspace + Skills 四层原语实现
  - 关联主题：与 OpenHarness 开源实现形成闭环，共同验证 Agent 运行时架构的设计方向

### Project（1篇）
- **OpenHarness（HKUDS）：开源 Agent Harness，12,984 Stars**
  - 来源：github.com/HKUDS/OpenHarness（12,984 Stars，MIT License）
  - 核心价值：43 工具 + Skills 系统 + 多级权限 + ohmo 个人 Agent，与 OpenAI Responses API 设计对标
  - 关联 Article：OpenHarness 是 OpenAI Responses API 计算机环境的开源实现验证

## 本轮主题关联性

**Round 94 闭环**：
- **Article（OpenAI）**：Responses API + Shell Tool + Container Workspace + Skills 四层原语
- **Project（OpenHarness）**：完整开源实现（MIT License、43 工具、114 通过测试、ohmo 个人 Agent）

两者形成闭环：**OpenAI 的设计思想 ←→ OpenHarness 的开源实现**，前者提供架构框架，后者提供可检查的代码。

**演进主题递进**：
- Round 91：infrastructure-noise（评测环境噪声问题）
- Round 92：企业级规模化（PayPal）+ 小型 LLM 精细化（SmallCode）
- Round 93：评测工程化（CI-Gated Eval + AiSOC）
- Round 94：**Agent 运行时架构（OpenAI Responses API + OpenHarness 开源实现）**

## 线索区

### 尚未追踪的优质项目（待评估）
- **microsoft/agent-framework**（10,652 Stars）— Microsoft Agent Framework，多语言生产级
- **lsdefine/GenericAgent**（11,944 Stars）— 极简自进化 Agent，3K 核心代码
- **strukto-ai/mirage**（2,599 Stars）— AI Agent 统一虚拟文件系统（已追踪）
- **openai/openai-agents-python**（26,597 Stars）— OpenAI Agents SDK（需评估关联性）
- **HKUDS/nanobot**（43,074 Stars）— 超轻量 AI Agent（需评估关联性）
- **caveman-code/caveman**（63,207 Stars）— Claude Code skill，token 压缩 65%（需评估关联性）

### 候选 Article 线索
- OpenAI "Using skills to accelerate OSS maintenance" — Codex + repo-local skills 工程实践
- Anthropic "Scaling Managed Agents: Decoupling the brain from the hands"（已追踪）
- Anthropic "Claude Code auto mode: a safer way to skip permissions"（已追踪）
- Anthropic "Harness design for long-running application development"（已追踪）

### 候选 Project 线索
- microsoft/agent-framework（10,652 Stars，生产级多语言框架）
- lsdefine/GenericAgent（11,944 Stars，极简自进化）
- caveman-code（63,207 Stars，token 压缩）
- nanobot（43,074 Stars，超轻量 Agent）

## 下轮待办
1. 评估 microsoft/agent-framework（10,652 Stars）是否值得产出 Project
2. 评估 GenericAgent（11,944 Stars）是否值得产出 Project
3. 评估 caveman-code/caveman（63,207 Stars）是否值得产出 Project
4. 扫描 OpenAI "Using skills to accelerate OSS maintenance" 文章（Codex 工程实践）
5. 扫描 GitHub Trending 新项目（Stars > 5000 门槛）