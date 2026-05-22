# OpenAI Codex Windows 沙箱：为什么现有工具都不够用，以及最终方案的设计逻辑

> 本文深入分析 OpenAI 工程团队为 Codex 构建 Windows 沙箱的技术决策过程，涵盖三个被否决的原生方案、无权限沙箱的原型局限，以及最终「降权沙箱 + 独立用户 + 防火墙」的工程实现。

---

## 核心命题

**Codex 在 Windows 上的沙箱问题，本质上是一个「操作系统原生隔离能力不足」与「AI Agent 开放工作流」之间的结构性矛盾。** macOS 有 Seatbelt、Linux 有 seccomp/bubblewrap，而 Windows 没有开箱即用的对应方案——这不是 OpenAI 的技术短板，而是整个 Windows 生态在沙箱基础设施上的历史欠账。

---

## 一、问题背景：为什么 Windows 沙箱难做

Codex 是一个运行在开发者笔记本上的编码 Agent，通过 CLI、IDE 插件或桌面应用与用户交互。它以用户权限运行，理论上可以做用户能做的任何事——读取文件、运行命令、写代码、创建 Git 分支。这种「高权限 + 开放工作流」的组合，让安全边界变得异常复杂。

当 Codex 需要在 Windows 上实现沙箱时，面临的不是「如何实现」，而是「如何不借助管理员权限，在用户态实现真正有效的隔离」。这不是一个纯粹的安全问题，而是一个**安全与用户体验的工程权衡问题**。

> **真正的问题是**：沙箱不能要求用户都是管理员，否则大多数开发者根本无法使用 Codex。

---

## 二、三个被否决的原生 Windows 方案

OpenAI 团队系统性地评估了 Windows 原生提供的三种隔离手段，全部否决。

### 2.1 AppContainer：形状不匹配

**What**：Windows 原生沙箱，基于能力的隔离模型，专为「预先知道需要哪些权限」的应用设计。

**Why not**：AppContainer 的隔离粒度是「一个固定范围的小型应用」，而 Codex 驱动的是「开放式开发者工作流」——Shell、Git、Python、包管理器、构建工具，以及 Agent 决定使用的任何二进制文件。AppContainer 能提供强隔离，但隔离的形状与「让 Agent 像开发者一样工作」的需求完全不匹配。

用 AppContainer 做沙箱，相当于用专门为 ATM 设计的安全壳去保护一台通用开发工作站。

### 2.2 Windows Sandbox：产品形态不兼容

**What**：微软提供的轻量级Disposable VM，每次启动提供干净的 Windows 环境，关闭后所有更改消失。

**Why not**：Codex 需要**直接在用户的实际代码库上工作**——不是在独立的虚拟机里配置一套新环境，再建立 host/guest 桥接。更致命的是，Windows Sandbox 甚至不在 Windows Home SKU 上提供，产品覆盖直接缺了一大块。

这和 AppContainer 的问题本质相同：沙箱的边界是 VM/容器级别，但 Codex 需要的是进程级别的隔离，粒度不对。

### 2.3 Mandatory Integrity Control（MIC）：语义污染不可接受

**What**：Windows 的完整性级别机制（Low/Medium/High），低完整性进程默认不能写入中等完整性的对象。

**Why not**：MIC 的问题不是它不能工作，而是它对文件系统的语义修改范围过大。把工作区标记为低完整性，不只是「让 Codex 可以写入」，而是「所有低完整性进程都可以写入」。这将用户真实的代码仓库变成了一个低完整性的公共 sink，信任模型发生了根本性改变——而且难以界定边界和撤回。

**笔者的判断**：MIC 在理论上优雅，但「修改系统信任模型」这件事在多租户开发机器上的风险远超收益。当一个安全机制本身需要改变系统的安全假设时，它就已经输了。

---

## 三、无权限原型：SIDs + Write-Restricted Token 的文件隔离

在否决了所有原生方案后，OpenAI 决定自己实现沙箱。第一个原型的核心设计基于两个 Windows 概念：

### 3.1 合成 SID：给沙箱一个独立身份

SID（Security Identifier）是 Windows 权限系统的基石。Windows 允许创建**不对应真实用户的合成 SID**，但这些 SID 可以像普通 SID 一样写在 ACL 中。这给了沙箱一个关键能力：创建一个 `sandbox-write` 合成 SID，专门用于控制 Codex 的写入权限，且不影响机器上任何其他安全主体。

### 3.2 Write-Restricted Token：双重检查机制

Windows 的写限制令牌（Write-Restricted Token）在普通身份检查之上增加了一层额外检查：写操作要成功，**必须同时满足**——正常用户身份允许，且令牌的限制 SID 列表中至少有一个 SID 也被允许。

这允许精确的 ACL 控制：把 `sandbox-write` SID 的写权限授予工作目录和配置文件中的 `writable_roots`，同时明确拒绝它访问 `.git`、`.codex`、`.agents` 等只读区域。

**这个方案有效解决了文件写入控制**，且完全不需要管理员权限——ACL 写在文件系统上，普通用户就能设置。

### 3.3 网络隔离：环境变量投毒（ Advisory Only ）

文件问题解决了，但网络隔离更棘手。没有管理员权限就无法使用 Windows 防火墙，OpenAI 退而求其次，在沙箱进程的环境变量层面做「投毒」：

```bash
HTTPS_PROXY=http://127.0.0.1:9      # 让代理感知流量走不通的代理
ALL_PROXY=http://127.0.0.1:9
GIT_HTTPS_PROXY=http://127.0.0.1:9
GIT_SSH_COMMAND=cmd /c exit 1        # 让 Git over SSH 直接失败
```

在 PATH 前面插入 stub 脚本，让 `ssh`/`scp` 直接被拦截。

**这套机制能 catch 常规开发工具的流量，但只是 advisory**——任何进程都可以忽略环境变量、直接打开 socket，或绕过 PATH。OpenAI 自己也承认，这不是为对抗性代码设计的。

### 3.4 原型的问题：ACL 变更成本 + 网络隔离是硬伤

| 问题 | 影响 |
|------|------|
| ACL 应用耗时长 | 取决于工作区目录拓扑，大仓库代价高 |
| 语义难以动态修改 | macOS 可以改 .sbpl 文件热更新，Windows 改 ACL 是缓慢且侵入的操作 |
| 网络保护是 advisory | 好意代码可能绕过，恶意代码完全可以绕过 |

前三个问题是「自定义沙箱 + 开放工作流的固有代价」，但**网络隔离是硬伤**——不是设计权衡，而是安全失效。

---

## 四、重设计：Elevated Sandbox——以用户换防火墙

### 4.1 关键洞察：防火墙规则需要独立安全主体

为什么环境变量投毒不够？恶意代码可以不认 `HTTPS_PROXY`，直接用 `socket()` 发起网络连接。

要用 Windows 防火墙精确限制沙箱进程的网络访问，Windows 防火墙规则只能按「Windows 用户」或「可执行文件路径」匹配——但这里有两个致命限制：

1. **无法按 Token 身份匹配**：Windows 防火墙不认识 restricted token 中的合成 SID
2. **按路径匹配太粗**：可以阻止 `codex.exe` 的网络访问，但无法阻止 Agent 启动的 `git.exe`/`python.exe`

要真正按「沙箱进程树」限制网络，需要让沙箱命令以**独立的 Windows 用户**身份运行。这样就能用防火墙阻止 `CodexSandboxOffline` 用户的所有出站流量。

### 4.2 独立用户：CodexSandboxOffline + CodexSandboxOnline

升级后的设计创建两个本地 Windows 账户：

- `CodexSandboxOffline`：被防火墙规则阻止所有出站网络——用于需要完全隔离的命令
- `CodexSandboxOnline`：网络不受限——用于需要访问 API 的场景

但独立用户带来新问题：**读取权限**。Windows 默认不允许用户读取其他用户的配置目录（如 `C:\Users\<username>`）。沙箱用户需要能够读取工作区的文件，这些文件属于主用户账户。

解决方案：为沙箱用户在常用目录上添加读 ACL，这是一个**最佳努力且异步执行**的操作（因为对每个目录应用 ACL 代价高昂），不阻塞沙箱启动。

### 4.3 两段式进程创建：codex-command-runner.exe 的引入

在 Windows 上，从另一个用户账户的进程创建一个受限 Token 并启动子进程，有一个权限墙——`CreateProcessAsUserW()` 不允许从用户态跨边界调用。这意味着 codex.exe 无法在自己进程中创建受限 Token 并以沙箱用户身份启动子进程。

**OpenAI 的解法**：引入 `codex-command-runner.exe`，一个职责唯一的二进制文件，专门负责 mint 受限 Token 并启动最终命令。

```
codex.exe                          codex-command-runner.exe
（真实用户进程）                    （沙箱用户进程）
     │                                   │
     └──CreateProcessWithLogonW()────►  │
                                        │
                              OpenProcessToken()
                              GetTokenInformation()
                              CreateRestrictedToken()
                              CreateProcessAsUserW()
                                        │
                                   最终命令
```

两段式设计的精髓：**Token 创建和受限 Token mint 发生在沙箱用户侧**，而不是跨越用户边界。这绕过了 `CreateProcessAsUserW()` 的权限墙。

### 4.4 Setup Binary 的必要性

Elevated Sandbox 在启动前需要执行一系列设置操作：

1. 创建合成 SID
2. 创建沙箱用户（Online + Offline）
3. 用 DPAPI 加密存储用户凭据
4. 创建/验证防火墙规则
5. 异步为沙箱用户添加读 ACL

这些操作与沙箱运行时职责完全不同。OpenAI 将 setup 逻辑封装为独立二进制，理由：

- **UAC 边界分离**：只在需要时跨 UAC 提示符
- **平台解耦**：不让 Windows 专用 setup 代码污染其他平台的 codex.exe
- **生命周期解耦**：将长时间运行的设置与主进程生命周期分离
- **路径统一**：在一个地方处理沙箱的不同 setup 路径

---

## 五、设计权衡的深层逻辑

### 5.1 「无权限」与「有效安全」之间的不可调和

OpenAI 的探索过程揭示了一个重要工程真相：**在 Windows 上，无管理员权限和强网络隔离是不可兼得的**。

- 无管理员权限 → 无法使用 Windows Firewall → 无法强制网络隔离
- 无网络隔离 → 环境变量投毒是唯一选择 → Advisory Only

这不是 OpenAI 做得不够，而是操作系统层面的能力缺口。选择「接受环境变量投毒」是一种务实的工程妥协；选择「要求管理员权限」是权衡后的安全升级。

### 5.2 macOS/Linux 为何没有这个问题

| 平台 | 进程隔离机制 | 沙箱配置 |
|------|------------|---------|
| macOS | Seatbelt（.sbpl 配置）| 配置文件热更新，无需改 ACL |
| Linux | seccomp/bubblewrap | BPF 程序精确控制，无需用户账户 |

这两个平台都提供了**无需管理员权限即可限制进程网络访问的内核级机制**。Windows 缺了这一层。

### 5.3 为什么不让 Agent 自己控制网络

从 Agent 的能力设计角度，另一个思路浮出水面：与其在 OS 层面做网络隔离，是否可以让 Agent 自身控制何时可以联网——通过工具权限系统实现「需要联网才给你网络工具」？

这确实是可行的路径（Anthropic 的 Claude Code Auto Mode 也走了类似方向，通过 Classifier 分层控制权限）。但这不是 OpenAI 这篇文章的讨论范围。值得注意的是，两个方向本质上是互补的：OS 层面的沙箱提供深层防御，Agent 权限控制提供细粒度策略。

---

## 六、工程启示

### 6.1 沙箱设计不是安全策略，是工程哲学

Codex Windows 沙箱的设计过程，本质上是在回答一个哲学问题：**「防御深度」和「用户摩擦」之间的最优解在哪里？**

过度严格的沙箱 → 用户体验差 → 大家开 Full Access  
过度宽松的沙箱 → 安全风险 → 事故  

OpenAI 最终选择了「Elevated Sandbox（需要管理员设置一次，但运行时无需提权）」，这是一个务实的折中：**setup 时的一次性成本，换取运行时的持续安全保护**。

### 6.2 两段式进程创建是 Windows 跨用户沙箱的标准范式

`codex-command-runner.exe` 的两段式设计（`CreateProcessWithLogonW()` → 独立进程 → `CreateRestrictedToken()`）揭示了 Windows 进程安全的深层约束：Token 创建和 Token 限制不能在同一个用户侧跨边界操作，必须在目标用户侧内部完成。

如果你的 Agent 需要在 Windows 上实现类似的沙箱机制，这个模式是绕不过去的工程路径。

### 6.3 平台能力决定安全上限

这个案例最重要的提醒：**Agent 的安全边界，由底层操作系统提供的能力决定**。当平台能力不足时，再好的安全设计也会遇到天花板。

这也是为什么 Anthropic 和 OpenAI 都在不同场合强调「平台级沙箱基础设施」的重要性——这不是单个 Agent 的问题，而是整个 AI Coding 生态需要行业共同解决的基础设施问题。

---

## 引用来源

> "Codex runs with the permissions of a real user by default, meaning it can do everything the user can do. This is powerful and potentially dangerous."
> — David Wiesen, OpenAI Codex Engineering

> "Windows doesn't currently provide this type of capability out of the box."
> — OpenAI Engineering Blog

> "To apply a firewall rule specifically to our sandboxed commands, we needed to run them as a separate principal, not as the 'real' user."
> — OpenAI Engineering Blog

> "We encapsulated the setup logic in its own binary partly to cross the UAC boundary only when needed."
> — OpenAI Engineering Blog

> "The network suppression story was different, though... We felt that this aspect was enough to consider investing in a better sandbox mode."
> — OpenAI Engineering Blog

---

**Tags**：#沙箱设计 #Windows安全 #Codex #HarnessEngineering #安全架构

**相关演进路径**：Harness Engineering → OS-Level Isolation → Platform Security