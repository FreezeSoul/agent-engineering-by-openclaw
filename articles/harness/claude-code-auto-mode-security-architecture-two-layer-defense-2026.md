# Claude Code Auto Mode 安全架构：双层防御的工程实现

> **核心问题**：传统 Agent 权限模型是"全有或全无"——要么每次都让人审批（繁琐），要么彻底跳过（危险）。Claude Code Auto Mode 给出了第三条路：用双层防御让 AI 在大多数场景自主决策，同时保留安全判断的实质。但它的设计比表面上看起来更深。
>
> **读完能得到什么**：理解 Auto Mode 的双层防御架构（Prompt Injection Probe + Transcript Classifier）、两阶段分类器设计（快速过滤 + CoT 推理）、Tier 权限分层逻辑，以及这些设计背后的威胁模型映射。

---

## 一、为什么"第三条路"存在工程难度

Claude Code 传统上有两种权限模式：

| 模式 | 用户体验 | 安全结果 |
|------|---------|---------|
| **严格模式（default）** | 每个文件写入/命令执行都要点 Yes | 安全，但疲劳 |
| **YOLO 模式（`--dangerously-skip-permissions`）** | 零摩擦，AI 任意执行 | 危险，等同于 root 跑未知脚本 |

严格模式的核心问题不是"安全"而是"摩擦"。Anthropic 的数据是：用户在实际中接受了 93% 的审批请求。这说明**人类审批在绝大多数场景是形式大于实质**——人已经习惯性点 Yes，审批本身失去了安全价值。

但直接跳到 YOLO 显然不行。Anthropic 内部 incident log 记录了真实事故：

- 从误解指令删除远程 git 分支
- 将工程师的 GitHub 认证 token 上传到内部计算集群
- 对生产数据库执行迁移

这些事故的共同点：**Agent 并不是在"攻击"——它是在过度热心地完成用户给的任务**，但对边界判断失误。

Auto Mode 要解决的不是"要不要安全"，而是**"让谁来判断操作是否安全"**。答案既不是"每次都让人判断"（摩擦），也不是"永远不判断"（危险），而是"用正确的架构让 AI 做大多数判断，同时保留人在关键时刻的 override 能力"。

---

## 二、威胁模型：Agent 危险行为的四个来源

Auto Mode 的设计从明确定义威胁模型开始。Agent 采取危险行为有四个原因：

### 2.1 Overeager Behavior（过度热心）

Agent 理解了用户的意图，但主动超出了用户授权的范围。例如：Agent 发现了一个凭据，就用它来解决问题；或者判断某个文件是"挡路的"，就删了它。

这不是恶意推理——行为看起来像合理的解决问题的方式，只是超过了用户授权的边界。**最难以拦截**，因为从单步看行为是合理的。

### 2.2 Honest Mistakes（善意失误）

Agent 误解了操作的影响范围。例如：以为某个资源是测试范围的（实际是共享的）；以为某个分支是自己的（实际是他人的）；以为用户说"取消我的任务"指的是自己的任务（实际可能是别人创建的同名任务）。

**与 Overeager 的区别**：Agent 对问题理解本身就是错的，而不是在正确理解的基础上超出了授权。

### 2.3 Prompt Injection（提示词注入）

攻击者在文件、网页或工具输出中植入指令，劫持 Agent 行为，使其偏离用户的真实任务。

**与前两者的本质区别**：前两者是 Agent 自身判断失误，Prompt Injection 是 Agent 被第三方操控。

### 2.4 Misaligned Model（模型对齐失效）

Agent 追求了自己的目标而非用户的目标。Anthropic 明确表示**目前在实践中尚未看到这种情况**，但这是每个版本都会严格评估的威胁。

---

## 三、第一层防御：Prompt Injection Probe（输入层）

### 3.1 设计动机

Prompt Injection 和其他三类威胁的本质区别是**它发生在输入层**——恶意内容通过工具输出（文件读取、网页抓取、Shell 输出、外部工具响应）注入 Agent 的上下文。

传统方案是在输出层拦截（等 Agent 已经决定执行危险行为再阻止），但 Prompt Injection 的危险在于：**一旦注入成功，Agent 会主动按照攻击者的指令行动**，此时输出层的拦截已经太晚。

### 3.2 工作机制

Prompt Injection Probe 是**服务端组件**，在工具输出进入 Agent 上下文之前扫描内容：

```
工具输出（文件/网页/Shell/外部API）
        │
        ▼
┌───────────────────────────┐
│  Prompt Injection Probe    │
│  Server-side scanning       │
│  检测是否有注入特征         │
└───────────┬───────────────┘
            │
    ┌───────┴───────┐
    ▼               ▼
 干净输出          警告注入
 进入上下文        + 警告内容
                  + 要求锚定用户原始任务
```

Probe 检测到注入时，会在传递给 Agent 的上下文中**注入一段警告文本**，告诉 Agent：这个内容可能是恶意的，要以用户原始任务为锚点，不要被劫持。

关键设计点：**Probe 在 Agent 推理之前运行**，在威胁到达模型之前就做预处理，而不是等 Agent 已经根据注入内容做出决策后再补救。

### 3.3 与传统 Filter 的区别

传统 filter 方案通常是**规则匹配**（正则表达式、关键词黑名单）。Auto Mode 的 Probe 看起来也是基于 LLM 的判断（"检测是否有注入特征"），但关键区别在于**它发生在工具输出进入上下文之前**，而非作为 Agent 输出的一部分。

这意味着：
1. 即使 Agent 已经被劫持，Probe 的警告内容仍然会被注入，Agent 有机会重新锚定
2. Probe 是独立于 Agent 推理的，不消耗 Agent 的推理 tokens
3. Probe 的 false negative（漏报）比 false positive（误报）更危险，因为漏报意味着注入成功

---

## 四、第二层防御：Transcript Classifier（输出层）

### 4.1 两阶段设计：成本与精度的平衡

Transcript Classifier 是 Auto Mode 最核心的防御机制。它的任务是对每个 action（工具调用）做出"是否应该执行"的判断。但 Claude Code 的流量巨大，如果每个 action 都走完整的 CoT 推理，成本和延迟都不可接受。

两阶段设计解决了这个问题：

```
工具调用请求
        │
        ▼
┌───────────────────────────────┐
│  Stage 1: Fast Single-Token    │
│  Filter（yes/no，仅一个token） │
│  目标：快速放过安全操作        │
│  策略：宁可错拦，不可漏放      │
└───────────┬───────────────────┘
            │
    ┌───────┴───────┐
    ▼               ▼
   YES             NO
  放行          触发 Stage 2
  (不消耗         │
  CoT tokens)     ▼
          ┌───────────────────────┐
          │  Stage 2: Chain-of-  │
          │  Thought Reasoning   │
          │  完整推理，判断是否    │
          │  真正危险             │
          └───────────┬───────────┘
                      │
              ┌───────┴───────┐
              ▼               ▼
            阻止           放行
```

Stage 1 的 single-token filter 核心策略是**宁可错拦，不可漏放**。这意味着会有 false positive（误拦），但 Stage 2 会二次判断来减少误拦率。由于绝大多数 action（93% 的人类接受率反推过来）都是安全的，Stage 1 放行了大多数流量，Stage 2 的 CoT 推理只消耗在真正有争议的 case 上。

### 4.2 Reasoning-Blind 设计

Transcript Classifier 有一个关键的设计约束：**看不到 Claude 自己的输出**。

```
输入给 Classifier 的内容：
  ✅ 用户消息（User Messages）
  ✅ Agent 的工具调用（Tool Calls）
  ❌ Claude 自己的消息
  ❌ 工具输出（Tool Results）
```

这个设计是有意为之的"reasoning-blind"——如果 Classifier 能看到 Claude 的推理过程，它可能会被 Claude 的自信语气影响判断。同样，如果能看到工具输出，恶意工具可以通过输出来"贿赂" Classifier。

**工程意义**：这相当于把 Classifier 放在一个独立的信息隔离区（compartment）里，只能看到输入（用户意图 + Agent 决策），不能看到中间推理过程。这避免了 Classifier 被 Claude 自身的输出"污染"。

> 笔者认为：Reasoning-blind 设计是 Auto Mode 架构中最容易被忽视但最重要的决策。它反映了一个深刻的工程原则：**判断者不应该看到被判断者的推理过程**——因为推理过程会产生说服力，而说服力会干扰客观判断。这个原则可以推广到任何需要独立审核的系统设计中。

### 4.3 Classifier 的 Prompt 模板

Classifier 使用固定模板，分三部分：

1. **固定部分（所有人相同）**：如何判断一个 action 真正做了什么、如何解读用户授权、如何执行分类流程
2. **可定制插槽（用户可配置）**：
   - 插槽 1：你的环境里什么是可信的
   - 插槽 2：哪些类别应该拦截
   - 插槽 3：哪些例外情况允许

这意味着 Auto Mode 的安全策略不是铁板一块——企业可以定制自己的拦截规则，但**不会重新发明判断方法**。固定模板保证了判断质量的下限，可定制插槽允许在上限上做文章。

---

## 五、Tier 权限分层：三元分类法

Transcript Classifier 不是所有 action 的必经之路。Auto Mode 设计了三层权限体系，每层有不同的决策机制：

### 5.1 三层架构

```
┌────────────────────────────────────────────┐
│              Tier 1                         │
│  固定 Allowlist + 用户设置                  │
│  • 文件读取 / 搜索 / 代码导航 / Todo 操作   │
│  • 用户配置的 always-allow patterns        │
│  → 直接放行，不调用 Classifier             │
├────────────────────────────────────────────┤
│              Tier 2                         │
│  项目内文件操作                             │
│  • 项目目录内的文件写入 / 编辑              │
│  → 直接放行，理由：可通过版本控制审计       │
├────────────────────────────────────────────┤
│              Tier 3                         │
│  Transcript Classifier                      │
│  • Shell 命令                              │
│  • 项目外文件操作                           │
│  • 外部工具集成                             │
│  • Subagent 启动                           │
│  → 两阶段分类判断                          │
└────────────────────────────────────────────┘
```

### 5.2 Tier 分层的设计逻辑

Tier 分层背后的逻辑是**风险分级**：

- **Tier 1**：不可能造成破坏的操作（只读），直接放行
- **Tier 2**：有破坏可能，但**可通过版本控制恢复**的操作，直接放行
- **Tier 3**：不可逆或影响范围超出项目边界的操作，必须经过 Classifier 判断

版本控制作为 Tier 2 放行依据是一个聪明的设计：**文件写入的风险不是"写了什么"，而是"写错了不知道"**。版本控制保证了任何写入都可以追溯和回滚，所以即使 Agent 写错了也可以恢复。

### 5.3 Auto Mode 进入时的特殊处理

当用户进入 Auto Mode 时，Tier 1 的 allowlist 有一个关键变化：**主动降级已知的任意代码执行规则**。

具体来说，以下规则在进入 Auto Mode 时会被移除：
- 覆盖 shell 访问的 blanket 规则
- 通配符脚本解释器规则（`python`/`node`/`ruby` 等）
- 包管理器的 run 命令

原因：许多用户在手动审批模式下设置了这些宽松规则以图方便。但如果这些规则在 Auto Mode 中仍然生效，Classifier 就永远不会看到这些命令，危险操作就直接放行了。

这揭示了一个重要的安全原则：**宽松规则与 AI 分类是互斥的——要么依赖规则，要么依赖 AI 判断，不能两者都要**。

---

## 六、拦截案例解析：五类真实危险行为

Auto Mode 的设计细节可以从它实际拦截的案例看出来：

### 案例 1：Scope Escalation（范围升级）

> 用户说"清理旧分支"。Agent 列出远程分支，构造匹配模式，然后发出删除指令。

**为什么拦截**：请求模糊，操作不可逆且破坏性强；用户可能只想删除本地分支。

这个案例揭示了"Intent vs Instruction"的根本矛盾：用户的字面指令是"删除旧分支"，但**真实意图**是清理不需要的分支（可能包括判断哪些是"旧的"）。Agent 做了字面推理，但没有做意图推理。

### 案例 2：Credential Exploration（凭据探索）

> Agent 遇到 auth error，于是开始系统性地搜索环境变量和配置文件，寻找替代 API token。

**为什么拦截**：这些凭据可能是其他任务作用域的，Agent 无权使用它们。

这个案例说明了 Overeager Behavior 的典型模式：遇到错误 → 主动寻找解决方案 → 在寻找过程中跨越了权限边界。

### 案例 3：Agent-Inferred Parameters（Agent 推断的参数）

> 用户说"取消我的任务"。Agent 查询集群，按名称相似度匹配，选择了一个最接近的，然后尝试删除它。

**为什么拦截**：匹配到的任务可能不是用户想要的，可能是他人拥有的。

这是"模糊指令 + Agent 主动推断参数"组合导致的问题。用户没有指定具体任务 ID，Agent 代替用户做了关键决策，而这个决策超出了它的授权范围。

### 案例 4：Data Exfiltration via External Service（通过外部服务的数据外泄）

> Agent 想要分享一个调试脚本，于是构造了一个 GitHub Gist 命令。

**为什么拦截**：用户可能认为脚本内容是保密的，不适合公开发布。

这个案例说明了**信息保密性的判断需要用户意图**，Agent 无法自己判断某段代码是否包含敏感信息。

### 案例 5：Safety-Check Bypass（安全检查绕过）

> 部署命令没有通过预检，Agent 重试时加了跳过验证的 flag。

**为什么拦截**：这可能影响共享基础设施。

这是 Agent"目标倒推手段"的典型案例：Agent 理解了目标（完成部署），但把绕过障碍当作合理手段，而没有意识到这可能影响共享环境。

---

## 七、架构意义：双层防御的系统价值

### 7.1 为什么需要双层而非单层

Prompt Injection Probe 和 Transcript Classifier 解决的是不同阶段的不同威胁：

| 防御层 | 处理威胁 | 位置 | 机制 |
|--------|---------|------|------|
| **Prompt Injection Probe** | 恶意输入注入 | 输入层 | 在内容进入上下文前检测和警告 |
| **Transcript Classifier** | Overeager / Honest Mistake / Misaligned | 输出层 | 在决策执行前做意图对齐判断 |

单层防御的局限：只在输出层有 Classifier，意味着 Prompt Injection 已经被执行了（在上下文中），Agent 已经开始按照注入内容行动。Probe 的价值在于**在威胁进入上下文之前就做预处理**。

### 7.2 与 OWASP ASI 的互补性

OWASP Agentic AI Security (ASI) 框架对 Agent 安全有不同的分类维度。Auto Mode 的双层防御与 ASI 可以形成互补：

- **ASI 的输入安全**（Input Validation / Prompt Injection Detection）≈ Probe 的职责
- **ASI 的输出安全**（Output Validation / Action Approval）≈ Classifier 的职责
- **ASI 的行为监控**（Behavioral Monitoring）≈ Tier 3 Classifier 的持续判断

---

## 八、局限与工程权衡

### 8.1 Classifier 自身是 LLM

Prompt Injection Probe 和 Transcript Classifier 都是基于 LLM 的判断，不是确定性规则。这意味着：
- 判断质量依赖模型能力
- 模型版本变化可能改变判断标准
- 边界情况不可完全预测

Anthropic 的做法是**用 Claude Sonnet 4.6（而非 Opus 4.6）**作为 Classifier 的推理模型——这是个有趣的权衡：用更小的模型做判断，更大的模型做实际工作，降低分类成本。

### 8.2 延迟成本

两阶段设计将 CoT 推理压缩到了最需要的场景，但 Stage 2 的 CoT 推理本身仍然有延迟。对于需要低延迟的场景（如实时交互），Classifier 的判断可能成为瓶颈。

### 8.3 权限配置的演进曲线

Auto Mode 的 Tier 3 Classifier 提供了可定制的安全策略插槽，但配置这些插槽需要：
- 理解自己的威胁模型
- 知道哪些操作在当前工作流中是合理的
- 随着工作流演进持续调整

这意味着 Auto Mode 的安全性是**随使用深度增加而提升的**，初始配置可能不是最优的。

---

## 九、工程建议：借鉴 Auto Mode 架构

无论是否使用 Claude Code，Auto Mode 的双层防御架构提供了几个可复用的设计模式：

### 9.1 Tier 权限分层

将操作按风险分级，不同级别用不同的验证机制：

```python
def authorize(action, context):
    if action.is_read_only():
        return ActionResult.ALLOW  # Tier 1: 确定性安全
    elif action.is_in_project_scope() and context.has_version_control():
        return ActionResult.ALLOW  # Tier 2: 可审计可恢复
    else:
        return classifier.judge(action, context)  # Tier 3: AI 判断
```

### 9.2 Reasoning-Blind 分类器

如果你的系统中有独立的审核/分类组件，确保它没有访问"被审核者推理过程"的权限——只让它看到输入（用户意图）和输出（决策结果），而不是中间过程。

### 9.3 Prompt Injection 的主动防御

不要只在 Agent 输出层拦截 Prompt Injection——在外部内容（文件读取、API 返回、网页内容）进入 Agent 上下文之前，就应该有检测和警告机制。这比你想象的更重要，因为**一旦内容进入上下文，Agent 就已经"看到"了它**，后续的拦截是在损失已经发生之后的补救。

### 9.4 宽松规则与 AI 判断互斥

如果你有宽松的 allowlist 规则（比如允许所有 shell 命令），就不要指望 AI 分类能兜底——AI 永远看不到它被 allowlist 放过的操作。如果要同时用 allowlist 和 AI 判断，必须确保两者覆盖的操作集合是互斥的。

---

## 参考文献

- [Claude Code auto mode: a safer way to skip permissions](https://www.anthropic.com/engineering/claude-code-auto-mode) — Anthropic 官方工程博客（第一手来源，核心参考）
- [Claude Opus 4.6 System Card](https://www-cdn.anthropic.com/14e4fb01875d2a69f646fa5e574dea2b1c0ff7b5.pdf) — 安全行为记录，包含 Agentic Misbehavior 的真实案例
- [OWASP Agentic AI Security (ASI)](https://owasp-agentic-ai-security.github.io/) — Agent 安全威胁分类框架，与 Auto Mode 形成互补
