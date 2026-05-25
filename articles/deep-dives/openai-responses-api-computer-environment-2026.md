# 从模型到 Agent：OpenAI Responses API 的计算机环境设计

> **核心论点**：LLM 本身只提供"训练智能"，真正的 Agent 能力来自于赋予它一个可持久运行、可执行命令、可管理状态的计算环境。OpenAI 通过 Responses API + Shell Tool + Container Workspace + Skills 这四层原语，将这个设计清晰地表达了出来。

---

## 一、为什么模型到 Agent 的转变需要新的运行时

从模型到 Agent 的转变，本质上是**从"访问训练知识"到"访问计算能力"的跨越**。

通过 Prompt，模型只能访问它在训练过程中学到的东西。但当你给模型一个计算机环境时，它可以执行真实世界的操作——运行服务、向 API 请求数据、生成有用的产物（电子表格、报告等）。

OpenAI 在其博客中指出：

> "By prompting models, you can only access trained intelligence. However, giving the model a computer environment can achieve a much wider range of use cases, like running services, requesting data from APIs, or generating more useful artifacts like spreadsheets or reports."

问题是：开发者不应该自己构建这个执行环境。OpenAI 替开发者把必要的组件构建好了——Responses API 被赋予了计算机环境，可以可靠地执行真实世界的任务。

**关键洞察**：这不是在模型外面包一层工具，而是**让模型的"推理能力"与"执行能力"在一个设计好的环境里协同工作**。

---

## 二、四层原语：Responses API 计算机环境的架构设计

OpenAI 的计算机环境由四个核心原语构成，它们分层协作，形成完整的 Agent 运行时：

### 1. Responses API — 编排层

Responses API 是开发者与 OpenAI 模型交互的接口。当它与自定义工具结合时，可以协调各种工具的调用。

关键设计点：

- 当模型需要使用工具时，控制权交回给客户端
- 客户端需要自己维护工具执行的 harness（这是合理的，因为不同场景的 harness 需求差异很大）
- 但这个 API 也可以在工具之间编排，只要在用户 prompt 中提及使用工具且选择的模型是 GPT-5.2 或更高版本

### 2. Shell Tool — 执行层

Shell Tool 提供可执行的动作。模型负责推理和规划，然后 Shell Tool 负责在隔离环境中运行命令。

这是 Agent 与普通模型调用的核心区别：**模型可以驱动真实世界的行动，而不只是返回文本**。

### 3. Hosted Container Workspace — 持久化运行时上下文

Hosted Container 提供了一个**持久化的运行时上下文**，包含：

- **文件系统**：用于输入和输出
- **可选的结构化存储（如 SQLite）**：用于状态持久化
- **受限的网络访问**：安全边界

模型在文件中读写，在数据库中查询状态，这些操作都发生在有边界的执行环境中。

### 4. Skills — 可组合的工作流复用单元

这是最有趣的一层。

Shell 命令很强大，但很多任务是**相同的多步模式的重复**。Agent 每次运行时都必须重新发现工作流——重新规划、重新发出命令、重新学习约定——导致结果不一致和执行浪费。

Skills 将这些模式打包成**可组合的构建块**。具体来说：

> "A skill is a folder bundle that includes 'SKILL.md' (containing metadata and instructions) plus any supporting resources, such as API specs and UI assets."

OpenAI 提供 API 来管理 Skills：
- 开发者上传技能文件夹作为版本包
- 之后可以通过 Skill ID 引用
- 在发送 prompt 之前，系统加载 Skill 并将其包含在模型上下文中

**这个序列是确定性的**：选择 Skill → 加载 SKILL.md → 注入上下文 → 模型推理。

---

## 三、Compaction：让 Agent 长时间运行的核心机制

上下文窗口是有限的。当 Agent 运行很长时间时，上下文会被填满，导致模型无法继续。

OpenAI 的解决方案是 **Compaction**（压缩）：

> "Compaction allows an agent to run for a long time with the context it needs."

原理大概是：将历史交互压缩为高层摘要，保留关键信息的同时释放上下文空间。这类似于"把对话的精华提取出来"，让模型始终有足够的上下文来继续工作。

这是一个**工程问题**，而不是模型问题。模型不需要"记住"每一次交互，它需要的是"能够做出正确决策所需的上下文"。

---

## 四、安全设计：秘密值与隔离执行

安全是计算机环境设计的核心部分。

OpenAI 的设计哲学：

> "The model only sees placeholders, while secret values stay outside model context and only applied for approved destinations — risk of leakage while still enabling authenticated external calls."

这意味着：

1. **模型永远不直接看到密钥**：它们以占位符的形式存在
2. **密钥只在批准的目的地应用**：防止泄漏
3. **仍然启用经过认证的外部调用**：安全不等于封闭

---

## 五、端到端工作流示例

把这四层原语放在一起，一个 prompt 可以展开为端到端的工作流：

```
发现正确的 Skill → 获取数据 → 转换为本地结构化状态 → 高效查询 → 生成持久化产物
```

在这个流程中：
- **Responses API** 提供编排
- **Shell Tool** 提供可执行的动作
- **Hosted Container** 提供持久的运行时上下文
- **Skills** 层叠可复用的工作流逻辑
- **Compaction** 让 Agent 可以长时间运行

---

## 六、我的判断

### 为什么这个架构设计值得关注

1. **分层清晰**：四层原语各有明确的职责边界，不混淆
2. **工程化思维**：不是喊口号，而是把"模型能力"、"执行环境"、"工作流复用"、"安全边界"当作系统设计问题来处理
3. **Compaction 作为一等公民**：把上下文管理当作核心工程问题，而不是"让模型自己处理"

### 尚未解决的问题

- **Skills 的版本管理策略**：随着 Skill 数量增长，如何处理依赖和兼容？
- **跨 Skill 的状态共享**：多个 Skill 在同一个 Workspace 中协作时，如何管理共享状态？
- **Compaction 的算法细节**：OpenAI 没有公开 compaction 的具体实现，这可能是一个有价值的实现方向

---

## 参考来源

- [From model to agent: Equipping the Responses API with a computer environment | OpenAI](https://openai.com/index/equip-responses-api-computer-environment/)（2026年3月11日）