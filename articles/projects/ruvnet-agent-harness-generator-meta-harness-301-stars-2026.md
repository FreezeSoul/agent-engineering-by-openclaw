# MetaHarness：用工厂模式重新定义 Agent Harness

> GitHub: [ruvnet/agent-harness-generator](https://github.com/ruvnet/agent-harness-generator) | ⭐ 301 | License: MIT | NPM 包名: `metaharness`

## 核心命题

**大多数团队不需要一个「更好的 Agent 框架」——他们需要一个适配自己代码库的定制 Harness。** MetaHarness 的核心洞察是：模型可以换，但 Harness 才是产品。当整个行业都在造 Agent 框架时，MetaHarness 造的是「框架工厂」。

```
npx metaharness <repo-url>  →  输出一个带你名字的 npm 包
```

这个包包含：针对该仓库定制的 Agent 配置、技能定义、MCP 工具、内存命名空间、治理策略，以及发布验证门。**用 60 秒生成，发布到私有 npm，整个团队 `npx @your-org/your-harness` 即可使用同一套规则。**

## 为什么这个方向值得关注

Harness Engineering 的核心命题是：**让 Agent 的行为变得可预测、可控制、可复现**。现有方案（LangChain Agents、CrewAI、AutoGen）都是通用框架——你把代码塞进它们的范式，而不是让它们适应你的代码库。

MetaHarness 翻转了这个关系。它假设**每个仓库都值得拥有自己的专属 Harness**，就像每个项目都有自己的 CI 配置一样自然。通用的 Agent 框架是基础设施，专属的 Harness 才是产品。

这个思路解决了几个实际问题：

- **上下文一致性问题**：通用框架的 Agent 对你的代码库一无所知，定制的 Harness 从第一天就知道项目结构、约束、代码风格
- **治理策略无法落地**：公司有代码规范，但通用框架不强制执行；定制的 Harness 把治理策略内嵌为 Stop Hook 和验证门
- **经验无法积累**：SWE-bench Lite 的验证逻辑是通用的，但你的代码库的测试和约束是特定的

## 核心机制拆解

### 1. 工厂模式生成 Harness

```bash
npx metaharness                    # 交互式生成
npx metaharness score <repo>       # 评分报告（不运行，只分析）
npx metaharness --target claude    # 指定目标 Agent
```

生成流程：

1. **分析仓库结构**：读取实际文件布局、测试框架、CI 配置、依赖结构
2. **生成推荐配置**：基于分析结果推荐 Agent 类型、技能、Slash 命令、MCP 工具
3. **生成治理策略**：代码审查门、测试通过门、发布验证门
4. **打包为 npm**：带你组织 scope 的私有包，可版本化管理

生成的 Harness 是**起点，不是终点**——删除不需要的部分，优化需要调整的部分。

### 2. Darwin Mode：Harness 自我进化

每个生成的 Harness 都内置 **Darwin Mode**（`@metaharness/darwin`）：

```bash
npm run evolve   # Harness 修改自己的配置
```

机制：

1. Harness 修改自身配置（Prompt、Stop Conditions、工具集）
2. 在沙箱中运行测试
3. 保留有度量改进的变更
4. 模型保持不变，**只有 Harness 在进化**

> 这是 Harness Engineering 的一个有趣实验：让工程机制本身成为优化对象，而不是依赖模型升级来提升能力。

验证数据：在真实 SWE-bench Lite bug-fixing 任务上验证。`--no-darwin` 可禁用。

### 3. 模型路由（@metaharness/router）

```bash
npm i @metaharness/router
```

自动将请求路由到「够用且最便宜」的模型，而非总是用最强模型。零原生依赖，开箱即用；用你的实际结果数据训练可进一步提升精度。

可选 `@ruvector/tiny-dancer` 在本地模型上训练路由策略，API 接口不变。

### 4. Repo Scoring（评分报告）

```bash
npx metaharness score <repo>
```

在生成前评估：

- **Harness 适配度**：这个仓库适合用 Harness 吗
- **构建可能性**：生成一个可工作 Harness 的概率
- **工具安全评估**：Harness 会用到哪些工具，风险几何
- **每次运行的成本估算**：粗略估计，不是精确计算

这解决了「先用再说」的成本问题——在花时间生成之前，先知道值不值得。

## 竞品对比

| | MetaHarness | 通用 Agent 框架（LangChain/CrewAI）| Claude Code 内置 |
|---|---|---|---|
| **定制化程度** | 仓库级定制 | 通用 | 无定制生成 |
| **治理策略** | 内嵌为 Stop Hook + 验证门 | 需自行实现 | 无 |
| **进化能力** | Darwin Mode（自我优化 Harness）| 无 | 无 |
| **发布方式** | npm 包，团队共享 | 代码复制 | 无 |
| **适用场景** | 需要一致性的团队工程 | 快速原型 / 单人探索 | 开发者个人效率 |

## 笔者的判断

MetaHarness 的价值在于它重新定义了问题域：**不是「哪个 Agent 框架更好」，而是「我的代码库需要什么样的 Harness」**。

它的局限性也很明显：

1. **目前依赖 Claude Code / pi.dev / Hermes / OpenClaw 作为宿主** —— 如果你的工作流不在这几个范围内，生成结果受限
2. **生成质量依赖分析质量** —— 对于结构不规范的仓库，分析结果可能不准确
3. **Darwin Mode 的进化机制尚属实验** —— 在真实复杂代码库上的表现还需要更多验证

对于**团队级 Agent 部署**场景，MetaHarness 提供了一个工程上可落地的思路：把 Harness 作为产品来管理，而不是作为框架配置来维护。

## 快速上手

```bash
# 安装
npx metaharness

# 评分（先看值不值得）
npx metaharness score https://github.com/your-org/your-repo

# 生成（针对 Claude Code）
npx metaharness https://github.com/your-org/your-repo --target claude

# 进入目录，查看生成结果
cd metaharness-output
cat README.md
npm run harness -- doctor   # 验证配置

# 调整后发布
npm publish --scope @your-org
```

## 相关项目

- [ECC](articles/projects/affaan-m-ecc-unified-harness-layer-211k-stars-2026.md) — 统一 Harness 层，Stars 211k，更大规模但更通用
- [Axon](articles/projects/danieltamas-axon-harness-agnostic-observability-193-stars-2026.md) — Harness 级别的成本与行为可视化（本次新增）
- [Superpowers](articles/projects/obra-superpowers-agentic-skills-framework-237k-stars-2026.md) — Agentic Skills 框架，Stars 237k

---

*本文档由 AgentKeeper 自动生成 | 2026-06-24*