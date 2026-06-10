# Anthropic 安全工程指南：当 AI 加速进攻时，防御者必须做什么

> Anthropic 在 2026 年 4 月 10 日发布的 "Preparing your security program for AI-accelerated offense"，是一份**面向防御者的工程化安全运营手册**——它在三个层面区别于一般安全建议：①按控制措施的"持续有效性"重排优先级；②承认攻击者将"无限耐心"，因此偏爱硬边界而非摩擦；③把 AI 自动化明确嵌入到每一条建议的执行路径中。

---

## 核心断言：漏洞到利用的时间窗正在从"月"压缩到"小时"

Anthropic 在文章开篇给出了一个被低估的时序判断：

> "Frontier AI models are compressing the timeline between vulnerability and exploit from months to hours."

并预测：**24 个月内，海量潜藏在代码中多年的 bug 会被 AI 模型发现并被链成可用 exploit。** 公开的、低于 Mythos 级别的模型**已经**能够发现传统审查多年漏掉的严重漏洞。

这个判断的工程含义不在于"威胁很严重"——而在于：**所有依赖"延迟反应"的安全控制都将失效**。安全工程必须从"检测→响应"的串行模型，迁移到"先假设被攻破→持续验证→自动化处置"的并行模型。

---

## 七条工程化建议：按"控制持续性"重排优先级

Anthropic 的 7 段建议**不是平铺的检查清单**，而是按"在 AI 加速进攻下哪些控制持续有效、哪些控制会快速退化"重新排序的工程优先级。

### 1. 关闭补丁滞后（patch gap）

AI 模型极其擅长**反向工程已公开的补丁到工作 exploit**。KEV 目录里的漏洞一旦可达就是紧急事件，EPSS 概率排序让剩余 CVE 变成可管理队列。

> **工程动作**：互联网暴露系统 **24 小时内**打补丁；启用云/OS 厂商原生自动化补丁；CI 中跑依赖清单扫描，自动用 KEV+EPSS 注释。

### 2. 准备"10 倍"的漏洞报告量

未来两年内，Vulnerability Management 流程将承受数量级增长。**电子表格 + 周会**的处理模式注定失败。

> **工程动作**：用前沿模型做**自动 triage**（去重、估算暴露面、起草修复工单）；用 LLM 查 lockfile 发现**功能重复的依赖**（多个 HTTP 客户端、多个 JSON 解析器是攻击面浪费）；对 OpenSSF Scorecard 低分的小依赖用 **AI vendoring**——让 LLM 写等价实现替换它。

### 3. 在代码交付前发现 bug

默认假设：到达生产的 bug 终将被发现，所以**安全测试必须发生在生产之前**。

> **工程动作**：CI 中加 SAST + AI 辅助 code review，**高置信度发现直接 block merge**；用 **OWASP ASVS** 三级严谨度定义"通过"；用 **SLSA** 分级保护构建管线（攻击者若能注入 commit→deploy 之间的代码，根本不需要找漏洞）；新代码默认选 Rust/Go，旧的 C/C++ 不强求重写。

### 4. 主动扫描已有代码中的未知漏洞

外部依赖的 KEV 解决了"已知漏洞"，但**自己的代码库里有"从未被前沿模型审视过"的未知漏洞**。Anthropic 明确建议：

> "Pick one internet-facing service with few current owners and scan its input handling and auth logic."

这是**最容易被低估的一条**——因为它的反馈是"找到问题"而非"消除问题"，但这是防御者相对于攻击者的最大时间差。

### 5. 为"已经被突破"设计（Design for breach）

这是整篇文章最核心的反直觉断言：

> "Mitigations whose value comes from friction—making an attack tedious—rather than a hard barrier (extra pivot hops, rate limits, non-standard ports, SMS-based MFA) are much less effective against an adversary that can grind through those tedious steps."

**对抗"无限耐心攻击者"，必须用硬边界替代摩擦**：
- **零信任架构**：每个服务间请求都要认证授权（CISA Zero Trust Maturity Model）
- **硬件绑定凭证**：FIDO2/passkey + 已认证设备身份
- **短时 token 替代长生命周期密钥**
- **服务间身份隔离**：被攻破的 build server 不应能 query 生产数据库

### 6. 缩减并清点暴露面

两条原则：①你无法防御你不知道的系统；②暴露面越小，被攻击的可能性越低。

> **工程动作**：维护**互联网暴露资产清单**（API endpoints、host、service）；定期用 AI 跑**自动外网侦察 + 链路化攻击尝试**（autonomous external red-teaming）；定期退役无主服务。

### 7. 缩短 IR（事件响应）时间

Exploit 可能数小时内出现，**IR 流程以"天"为单位就是太慢**。

> **工程动作**：把"模型前置在告警队列"作为第一道工序（triage agent 用 SIEM 只读访问做首轮分类）；优先度量 **dwell time + coverage**（这是 AI 自动化最能改进的两个指标）；演练"**同一周 5 个并发 incident**"——单 CVE 演练已不足以验证能力；把检测覆盖率对照 **MITRE ATT&CK**——优先覆盖 lateral movement 和 credential access。

---

## 工程视角：这份指南"反共识"在哪里

Anthropic 明确点出几条与流行安全文化的冲突：

| 流行观点 | Anthropic 立场 |
|---------|---------------|
| "更多密码策略 = 更安全" | ❌ 长生命周期密钥是 AI 辅助代码分析**第一批被发现的目标** |
| "MFA 加上 SMS 就够了" | ❌ 短信 MFA 属"摩擦类"控制，对无限耐心攻击者无效；用 FIDO2/passkey |
| "补丁 SLA 是周" | ❌ 互联网暴露系统 24 小时内打补丁 |
| "安全团队用电子表格跟踪" | ❌ 漏洞量将增长 10 倍，必须 AI 自动化 triage |
| "CTF 演练就够" | ❌ 单一 CVE 演练不够，要演练"同一周 5 个并发 incident" |

这些都是**已被验证持续有效的控制 vs 在 AI 加速进攻下退化的控制**——Anthropic 按这个维度重排了优先级。

---

## 对 AI Agent 工程的直接含义

这份指南不只面向传统安全团队，对**部署 AI Agent 的工程团队**也直接相关：

1. **Agent 本身是新的攻击面**——它有 broad tool access 和自主决策能力，URL safety / prompt injection / tool poisoning 都是 Agent-specific 风险
2. **传统访问控制不能阻止 Agent 误用合法权限**——零信任的"每请求认证授权"对 Agent 必须延伸
3. **Memory poisoning 是 Agent 特有的新攻击类型**——传统安全扫描工具几乎不覆盖
4. **Red-team 必须按 Agent 行为建模**——而不是按传统 API 攻击面

Anthropic 同期发布的 *Zero Trust for AI agents*（May 27, 2026）正是把这份指南延伸到 Agent 系统的具体框架。

---

## 原文引用

> "AI models are very effective at recognizing the signatures of known, already-patched vulnerabilities in unpatched systems. Reversing a patch into a working exploit is exactly the kind of mechanical analysis at which these models excel."

> "Mitigations whose value comes from friction—making an attack tedious—rather than a hard barrier (extra pivot hops, rate limits, non-standard ports, SMS-based MFA) are much less effective against an adversary that can grind through those tedious steps."

> "You should run the version where five incidents hit in the same week."

---

## 相关阅读

- 原文：[Preparing your security program for AI-accelerated offense](https://claude.com/blog/preparing-your-security-program-for-ai-accelerated-offense)（Anthropic 官方博客，2026-04-10）
- 配套框架：[Zero Trust for AI agents](https://claude.com/blog/zero-trust-for-ai-agents)（2026-05-27）
- 关联项目：[Anthropic Threat Intelligence](https://www.anthropic.com/news/project-glasswing)（Project Glasswing）
