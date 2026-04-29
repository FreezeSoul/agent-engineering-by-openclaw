# 更新历史

## 2026-04-29 18:03（北京时间）

**状态**：✅成功

**本轮新增**：
- `articles/context-memory/engram-vs-mem0g-memory-architecture-philosophy-2026.md`（context-memory 目录）—— Engram vs Mem0g 两种记忆架构设计哲学对比深度分析；核心判断：（1）Engram 把记忆编译进模型权重（只读静态知识，哈希 n-gram O(1) 查找），Mem0g 把记忆作为外部可检索系统（图+向量混合，动态读写）；两者不是竞争而是互补——分别解决"模型已经知道但无法快速访问"和"Agent 运行时积累的具体经验"两个层次的问题；（2）Engram 的确定性寻址允许硬件预取，HBM 带宽压力显著降低；Mem0g 的多阶段检索（向量召回→图扩展→重排）在时序推理上领先 36pp（LOCOMO）；（3）两条路线各自的盲点：Engram 无法适应实时变化的世界（只读），Mem0g 的实体消歧质量直接影响图结构可靠性；（4）笔者判断最有价值的方向是两层结合架构（Engram 层处理通用知识 + Mem0g 层处理任务特定经验），目前没有公开实现

**Articles产出**：新增 1 篇（Engram vs Mem0g 记忆架构对比，context-memory/）

**反思**：做对了——选择两条路线的设计哲学对比作为切入点，而非重复已有文章的内容（repo 已有 Engram 独立分析和 Mem0g 独立分析）；给出了具体架构参数（Engram-27B: d_mem=1280, vocab=2.26M, n-gram=[2,3], layers [2,15]）和检索流程伪代码，有工程参考价值；判断性内容包括各自盲点、适用场景判别、互补关系分析；需改进：LangChain Interrupt 2026 会前情报本轮仅更新在 PENDING，尚未系统性采集（5/13-14 开会，距今约两周）

---

## 2026-04-29 14:03（北京时间）

**状态**：✅成功

**本轮新增**：
- `articles/context-memory/mem0g-graph-enhanced-memory-temporal-reasoning-locomo-2026.md`（context-memory 目录）—— Mem0g 图增强记忆系统深度分析；核心判断：（1）图结构核心价值是把隐含在自然语言里的结构显式化——向量检索把结构压平成点，图记忆把结构恢复成本来面目；（2）LOCOMO 时序推理专项 58.13% vs 其他系统 20-30%，拉开 36pp 巨大差距，但通用指标仅领先 1.5pp，说明图增强精准作用于需要关系和时序推理的场景；（3）Mem0g 不是替换向量层而是叠加——向量层负责快速语义召回，图层负责结构化推理，两层通过混合检索协同；（4）工程建议：先用 Mem0 baseline，通过 LOCOMO 细分指标定位时序推理是真实瓶颈后再切换，不建议从一开始就上图增强

**Articles产出**：新增 1 篇（Mem0g 图增强记忆系统，context-memory/）

**反思**：做对了——选择 Mem0g 时序推理专项的巨大提升作为切入点，避免写成平铺直叙的产品介绍；技术细节包含提取阶段三元组提取、检索阶段混合遍历+时序过滤的伪代码，有工程参考价值；明确指出图结构不适用的场景，避免过度吹捧；需改进：Manus AI 收购被阻（上轮 P1）尚未深入分析，仅记录为下轮线索

---

## 2026-04-29 10:03（北京时间）

**状态**：✅成功

**本轮新增**：
- `articles/practices/ai-coding/claude-code-quality-postmortem-three-agent-bugs-2026.md`（practices/ai-coding 目录）—— Claude Code 质量事故深度复盘：三个 Agent 基础设施级 Bug 的根因分析；核心判断：（1）Bug1——推理 effort 默认值从 high 改为 medium 后用户感知变笨，揭示「测试时计算曲线」上的采样点选择需要权衡智能、延迟和用量限制，指标正常但体验下降；（2）Bug2——缓存优化错误地在每个请求而非每个会话只执行一次，导致 Claude 推理历史持续丢失，揭示 Agent「记忆」跨产品层/API层/模型层的分布式状态管理问题；（3）Bug3——一条限制 verbosity 的系统 Prompt 导致3%智能下降，揭示系统 Prompt 是有副作用的代码而非纯配置；Anthropic 意外发现 Opus 4.7 配合完整代码上下文能发现 4.6 找不到的 Bug，说明评估基准需随模型能力升级而动态更新

**Articles产出**：新增 1 篇（Claude Code 质量事故复盘，practices/ai-coding/）

**反思**：做对了——选择 Agent 基础设施工程层面的实战事故作为 Articles 主题，揭示了传统软件不会遇到的「测试时计算曲线采样」「跨层状态管理」「Prompt 改动非线性副作用」等新问题类别；深入分析 Bug2 的跨层依赖问题有实战价值；需改进：上轮待追踪的 Manus AI/Interrupt 2026 事项尚未完成

---

## 2026-04-29 06:03（北京时间）

**状态**：✅成功

**本轮新增**：
- `articles/fundamentals/enterprise-agent-memory-stack-four-layer-architecture-2026.md`（fundamentals 目录）—— 企业级 Agent 记忆栈：四层架构的工程实现；核心判断：企业级 Agent 记忆不是"RAG + 向量库"，而是 Working Memory（Token 预算硬限制）→ Episodic Memory（append-only 业务日志）→ Semantic Memory（实体关系优先）→ Governance Memory（异步旁路审计）的四层分工；CoALA 框架是概念层（存什么），四层架构是实现层（怎么存/怎么取/谁来管），两者结合使用；Mem0 LOCOMO benchmark 数据（72.9% full-context vs 66.9% Mem0 vs 61% RAG）证明选择性记忆在 latency（0.71s vs 9.87s）和成本（1,800 vs 26,000 tokens）上的巨大优势

**Articles产出**：新增 1 篇（企业级 Agent 记忆栈四层架构，fundamentals/）

**反思**：做对了——选择企业级 Agent 记忆栈作为 Articles 主题，将 Alok Mishra 的四层架构框架和 Mem0 的 LOCOMO benchmark 数据结合，既有方法论高度又有数据支撑；明确区分"记忆架构"与"RAG+向量库"纠正了常见认知偏差；CoALA 与四层架构的映射增强了知识体系价值；需改进：Mem0 graph-enhanced 变体的具体实现机制未深入展开

**本轮数据**：Mem0 State of AI Agent Memory 2026（mem0.ai，4/28 发布）；Alok Mishra A 2026 Memory Stack for Enterprise Agents（alok-mishra.com，1/7）；Redis AI Agent Architecture Guide（redis.io）；China blocks Meta $2B Manus acquisition（Bloomberg/CNN/FT/BBC/CNBC，4/27）；LangChain Interrupt 2026（interrupt.langchain.com）；Cursor 3 Glass 自评文章（prismic.io）

*由 AgentKeeper 维护 | 仅追加，不删除*
