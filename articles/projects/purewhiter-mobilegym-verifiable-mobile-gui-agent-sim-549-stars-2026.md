# Purewhiter/mobilegym：让手机 GUI Agent拥有可验证的训练场

## TRIP 四要素

- **T（Target）**：研究手机 GUI Agent 的团队（学术或工业），当前被卡在「真实设备不可控 +模拟器不可信」的两难：真实手机状态黑盒、ADB/accessibility tree拿不到余额/订单/聊天记录，verifier只能依赖 VLM随机判定（实测10.2%误判率）；模拟器没有真实后端，无法重置/克隆/并行，GRPO 等 group-RL跑不起来
- **R（Result）**：通过 MobileGym 提供**完全可编程状态的浏览器托管 Android模拟环境**——28 个仿真 App +416 个参数化任务模板 +确定性 sub-millisecond判分器，单服务器256 个并行实例，95.1% Sim-to-Real迁移率（Qwen3-VL-4B GRPO训练 +42.8 pt模拟增益 →真实设备 +40.7 pt）
- **I（Insight）**：手机 GUI Agent研究的真正瓶颈不是模型能力，而是**评测与训练的可靠性**。MobileGym 把整个环境建模为「结构化 JSON snapshot」，judges 直接读取状态而非 VLM字符串匹配——从根上消除了「评测噪声」对模型排名的污染；同时让「clone state into hundreds of parallel instances」成为可能，group-RL 从「理论上可行」变为「工程上可跑」
- **P（Proof）**：arXiv2605.26114论文支撑；Apache2.0（代码）+ CC BY-NC4.0（数据）；GitHub549 stars（24 天增长）；MobileGym-Bench256 个测试任务 leaderboard 上 Gemini3.1 Pro58.8% / Doubao-Seed-2.0-Pro52.0% / Qwen3-VL-4B GRPO 后从基线22.1 →64.9 SR

---

## P-SET骨架

### P - Positioning（定位破题）

**一句话定义**：把「手机 GUI Agent 的训练与评测」从依赖真实设备的不可能三角，转化为**浏览器里一键启动的、完全可编程状态的、确定性判分的并行仿真平台**。

**场景锚定**：你想训练一个能在「抖音商城」下单的手机 Agent——但你不能在真机上跑10000 个 episode训练（钱真的会被扣掉）；传统 Android模拟器又没有真实后端，每次 reset 都是同样的初始状态，无法做 GRPO。MobileGym 的解法是：**把整个 App状态建模为 JSON**，judge读 JSON，trainer改 JSON，256 个 instance各自独立——这是从「GUI Agent 的 ImageNet」走向「GUI Agent 的 RL Gym」的工程突破。

**差异化标签**：**唯一同时支持「可验证评测」+「可并行 RL训练」+「Sim-to-Real验证」三合一的手机 GUI Agent平台**；UI-Venus / UI-TARS / GUI-Owl / AutoGLM 等主流开源 GUI Agent 都已在 MobileGym-Bench 上提交成绩

### S - Sensation（体验式介绍）

当你想用 MobileGym训练一个手机 Agent 时：

```bash
#1. 安装（Node.js ≥22 + Python ≥3.11）
pip install mobilegym
npm install -g @mobilegym/runtime

#2.启动模拟器（浏览器里直接看到28 个仿真 App）
mobilegym boot --parallel256

#3. 用自然语言跟 Agent 对话
mobilegym agent \
 --model qwen3-vl-4b \
 --task "在抖音商城搜索'无线耳机'并按价格升序加购前3 个" \
 --judge deterministic # 不是 VLM，是 JSON状态对比

#4.跑 benchmark（256 个测试任务，全跑完 ~6 分钟）
mobilegym bench --suite mobilegym-bench --parallel256
```

这就是 MobileGym 的核心价值——**把手机 GUI Agent 的开发循环从「等真机」变成「等 GPU」**，评测不再是 VLM噪声，训练不再是转账风险。

### E - Evidence（拆解验证）

**核心数据**（来自 README + arXiv2605.26114）：

|维度 | MobileGym |真实设备方案 |传统 Android模拟器 |
|------|-----------|-------------|------------------|
|状态可读性 | ✅ JSON snapshot，可 diff | ❌ 黑盒（ADB 只暴露 UI） | ❌状态黑盒 |
|状态可写性 | ✅ Reset/Inject/Clone/Snapshot | ❌真实数据库不可重置 | ⚠️ 部分 reset |
|副作用 | ✅沙箱无副作用 | ❌ 转账/解绑不可逆 | ⚠️ 部分 |
|评测判分 | ✅确定性 sub-millisecond | ❌ VLM误判率10.2% | ❌ VLM误判率高 |
| 并行度 | ✅256 instances / 单 server | ❌1 device =1 instance | ⚠️几实例 |
| 单实例资源 | ✅ ~400 MB RAM, ~3 s cold start | N/A | GB 级 |
| Sim-to-Real | ✅95.1%迁移率 | N/A | 通常30-50% |

**关键 Sim-to-Real案例**（Qwen3-VL-4B, GRPO,10 steps,1 node）：

-模拟环境 SR：22.1 →64.9（**+42.8 pt**）
-真实 Redmi Note12 Turbo SR：23.5 →64.2（**+40.7 pt**，保留95.1%）

**Leaderboard（MobileGym-Bench,256 test tasks）**：

| Model | Overall SR | L1 | L2 | L3 | L4 |
|-------|-----------|----|----|----|----|
| Gemini3.1 Pro |58.8% |97.5 |83.6 |63.3 |21.9 |
| Doubao-Seed-2.0-Pro |52.0% |100.0 |93.2 |48.2 |6.2 |
| Qwen3.6-Plus |45.7% |100.0 |78.1 |44.6 |3.8 |
| AutoGLM-Phone-9B |20.0% |86.2 |33.6 |9.6 |1.9 |
| UI-Venus-1.5-8B |15.4% |85.0 |21.9 |6.0 |1.9 |
| GUI-Owl-1.5-8B |15.1% |76.2 |26.0 |6.0 |1.2 |

L4（最难层级）所有模型 SR 都低于25%——表明当前手机 GUI Agent 在「复杂多步 +跨 App +状态依赖」任务上仍有巨大提升空间。

### T - Transformation（行动召唤）

**适用读者**：

1. **手机 GUI Agent 研究者**（学术 +工业）：如果你被「真机评测贵 +模拟器训练假」困住，MobileGym提供了**第一个同时支持确定性评测 + 并行 RL训练**的平台。优先用它做 GRPO / PPO训练，性价比远超 SWE-bench / WebArena。
2. **AI Coding工具厂商**（Cursor / Claude Code / Copilot团队）：手机是 Agent 的下一个战场——如果你的工具未来要支持「帮用户订外卖 /退订 / 转账」，需要先在 MobileGym-Bench 上评估「自家 GUI Agent 在 L3/L4任务上的真实能力」。
3. **LLM团队**（Qwen / Doubao / GLM / UI-TARS团队）：如果你在做多模态 Agent 模型，MobileGym-Bench已成为事实标准的手机 GUI评测榜——上榜成绩直接影响论文/产品的可信度。

**何时不要用**：

- ❌ 仅做桌面/Web GUI Agent（请用 OSWorld / WebArena）
- ❌ 不需要可验证评测（直接跑真机更快）
- ❌任务完全 stateless（不需要 reset/clone，模拟器足够）

**一句话总结**：MobileGym 让「手机 GUI Agent 的研究」从「VLM噪声评测 + 真机不可逆训练」的双重诅咒中解脱——**第一个把手机 GUI Agent变成「像 SWE-bench一样可量化、像 RL Gym一样可并行训练」的工程平台**。

---

##闭环配对

### Cluster归属

**新建 Cluster：`AI Agent Eval — Verifiable Mobile/Desktop GUI Benchmark`**

- 当前文章数：0（本文是 cluster起点）
-邻近 cluster：`Eval / Sandbox / Harness`（强交叉）
-关键差异化：手机 GUI评测填补了「桌面 SWE-bench」与「Web WebArena」之间的空白地带

### 与已有仓库内容的关联

- **articles/projects/inclusionai-ui-venus-precise-gui-grounding-native-ui-agent-2026.md**（UI-Venus,1008 stars）—— Model层的 GUI grounding专用模型
- **articles/evaluation/agent-evaluation-tools-2026.md**（Agent评测工具综述）
- **articles/harness/langsmith-sandboxes-every-agent-needs-a-computer-philosophy-2026.md**（Sandbox哲学）
- **articles/harness/openai-codex-windows-sandbox-deep-dive-2026.md**（Windows Sandbox架构）

###闭环逻辑（Pattern12: Eval × Model）

|维度 | UI-Venus（已收录） | MobileGym（本文） |
|------|-------------------|------------------|
|抽象层 | Model layer（专用 VLM grounding） | Eval/Runtime layer（仿真平台） |
|能力 | 从截图精准定位 UI元素 |评测 +训练手机 Agent |
|解决的问题 | GUI grounding误差 |评测噪声 +训练不可逆 |
|互补关系 | 给 Agent更好的「眼睛」 | 给 Agent更好的「训练场 +考试」 |

**一句话**：UI-Venus 让 Agent「看得准」，MobileGym 让 Agent「练得好 +评得对」——两条路各有最佳实践，但只有两者结合才能产出可信的手机 GUI Agent。

---

## 来源

- **GitHub**：[github.com/Purewhiter/mobilegym](https://github.com/Purewhiter/mobilegym)（549 stars, Apache2.0）
- **arXiv**：[arxiv.org/abs/2605.26114](https://arxiv.org/abs/2605.26114)（2026-05论文）
- **Project Site**：[mobilegym.dev](https://mobilegym.dev)
- **评分**：5/5（实用性：5/5，唯一手机 GUI评测平台；独特性：5/5，Sim-to-Real验证 +确定性判分双首创；时效性：5/5，24 天新发布即被 Gemini/Qwen 等顶尖模型采用）

---

*Round283 |2026-06-07 | Hermes Agent*
