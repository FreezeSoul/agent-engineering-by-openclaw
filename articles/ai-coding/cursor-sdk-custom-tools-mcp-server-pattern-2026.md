# Cursor SDK Custom Tools + Nested Subagents：让自定义函数成为 Agent 一等公民的工程力学

> 📅 **June 4, 2026** | 来源：[Cursor Changelog - SDK Updates Jun 2026](https://cursor.com/changelog/sdk-updates-jun-2026) | 🔴 第一批次

## 核心命题

Cursor SDK June 2026 这次更新解决了一个长期困扰 Agent SDK 开发者的工程问题：**如何让自定义函数和原生工具在 Agent 眼中毫无差别**。

答案是**内置 MCP 服务器 `custom-user-tools`**——你只需传一个函数定义，SDK 自动把它暴露成标准 MCP 工具，天然继承完整权限链路。同样的设计逻辑扩展到了 Nested Subagents：子 Agent 派生的子 Agent，自动继承父级工具集，无需任何显式配置。

这不是功能堆砌，而是一套**以工具为中心**的 Agent 扩展架构。

---

## 一、Custom Tools：内置 MCP 服务器的工程逻辑

### 旧范式的痛苦

在这次更新之前，如果你想在 Cursor SDK 里暴露一个自定义能力，流程是这样的：

```
1. 写一个 stdio 或 HTTP MCP 服务器
2. 把服务器接入 Agent（wire it in）
3. 调试服务器和 Agent 之间的通信
```

笔者认为，这套流程对于"只需要一个函数"的场景来说，成本极高。每一个自定义工具都要维护一个独立进程，对于快速原型和轻量集成来说是严重的工程负担。

### 新范式：函数定义即工具

```typescript
// Agent.create() 时传入
const agent = await Agent.create({
  local: {
    customTools: [
      {
        name: 'query_database',
        description: 'Query the analytics database',
        inputSchema: {
          type: 'object',
          properties: {
            sql: { type: 'string' }
          },
          required: ['sql']
        },
        handler: async ({ sql }) => {
          return await db.query(sql);
        }
      }
    ]
  }
});
```

SDK 内部做了什么？它把这个函数定义注册到一个内置的 MCP 服务器 `custom-user-tools`，模型调用这个工具时，走的是**和任何其他 MCP 工具完全相同的路径和权限门**。

> 引用原文：*"You can now hand the local agent your own tools by passing function definitions through `local.customTools`. The SDK exposes them to the agent through a built-in MCP server called `custom-user-tools`, so the model calls your code through the same path and the same permission gate as any other MCP tool."*

### 工具继承：子 Agent 无需重新注册

Custom tools 还有一个关键特性：**一旦在父级定义，自动向下渗透到所有子 Agent**。

> 引用原文：*"Custom tools are also visible to every subagent of a parent agent, so a tool you define once is available throughout the whole run."*

这意味着你不需要在每个子 Agent 的配置里重复注册工具，工具继承是自动的。

笔者认为，这个设计解决了一个实际的工程问题：多 Agent 协作场景中，工具集合的一致性维护。以前每个子 Agent 都需要知道有哪些工具可用，现在只需要在根 Agent 定义一次，继承链路自动完成。

---

## 二、Auto-review：自然语言指令驱动的权限分类器

### 问题背景

Local SDK Agent 在 headless 模式下运行时，默认没有人工干预环节——工具调用直接执行。对于需要安全边界的生产环境，这显然不可接受。

传统解法是"要么全放行，要么全拦截"。Cursor SDK 的 auto-review 引入了一个更细粒度的分类器。

### 工作机制

```typescript
const agent = await Agent.create({
  local: {
    autoReview: {
      // 路由本地工具调用经过 auto-review 而非直接执行
    }
  }
});
```

`permissions.json` 中的配置：

```json
{
  "autoRun": {
    "allow_instructions": [
      "Read-only inspections of build artifacts under ./dist are fine."
    ],
    "block_instructions": [
      "Always pause delete operations so I get a chance to review them."
    ]
  }
}
```

分类器读取 `allow_instructions` 和 `block_instructions` 的自然语言描述，判断当前工具调用应该自动执行还是暂停等待审查。

> 引用原文：*"A classifier decides which calls run automatically and which to hold back, rather than bypassing review entirely."*

笔者认为，这个设计的聪明之处在于**用自然语言描述策略，而不是写规则代码**。对于非安全背景的开发者，这意味着他们可以用"不要让我看到删除操作"这样的自然语言来配置安全边界，而不需要理解具体的权限模型。

### 与 MCP 权限门的互补关系

Custom tools 通过 `custom-user-tools` 内置 MCP 服务器暴露，天然经过 MCP 权限门。Auto-review 则是在**调用链路**上增加了一层运行时分类。两者是正交的：

- MCP 权限门：控制"这个工具能不能被调用"
- Auto-review 分类器：控制"这个调用在当前上下文中是否合适"

---

## 三、Nested Subagents：层级委托的执行模型

### 核心机制

Subagents 现在可以派生自己的 subagents，形成任意深度的树状结构：

```
Root Agent
  └── Reviewer Subagent
        └── Test-writer Subagent
              └── Bug-reporter Subagent
                    └── ...
```

每一层保留自己的 prompt 和 model 配置，互不干扰。

> 引用原文：*"A reviewer subagent can delegate to a test-writer, which can delegate further, with each level keeping its own prompt and model."*

### 关键实现细节

**无需开启任何开关**：子 Agent 派生功能是自动的，因为 subagent session 在注册时会携带需要的 executor 信息。

```typescript
// 每个 subagent 都知道如何调用 Task
const subagent = await agent.spawnSubagent({
  prompt: 'Review the PR for security issues',
  model: 'composer-2.5'
});

// subagent 内部可以继续派生
await subagent.spawnSubagent({
  prompt: 'Write tests for the reported vulnerabilities',
  model: 'composer-2.5'
});
```

### 工具继承的层级叠加

结合 Custom Tools 的继承机制，整个工具体系形成了一个**从根到叶**的树状渗透：

- 根 Agent 定义 `query_database`
- Reviewer Subagent 可以使用 `query_database`
- Test-writer Subagent 也可以使用 `query_database`
- Bug-reporter Subagent 同样可以使用 `query_database`

笔者认为，这种层级叠加的工具继承，使得复杂任务的 Agent 分解变得自然：你可以在根 Agent 定义所有基础工具，然后在不同层级的 subagent 中使用它们，而不需要每层都重新注册。

---

## 四、Pluggable Storage：LocalAgentStore 接口的可组合性

### 从 SQLite 到 JSONL

```typescript
// 切换存储后端
import { JsonlLocalAgentStore } from '@cursor/sdk';

// JSONL 模式：追加写入，可读可 diff，可 check in 到 version control
const agent = await Agent.create({
  local: {
    store: new JsonlLocalAgentStore('./agent-runs/')
  }
});
```

> 引用原文：*"Both SqliteLocalAgentStore and JsonlLocalAgentStore are exported directly."*

### 自定义存储接口

如果默认实现都不满足需求，可以实现 `LocalAgentStore` 接口：

```typescript
interface LocalAgentStore {
  saveRun(run: Run): Promise<void>;
  loadRun(runId: string): Promise<Run>;
  listRuns(filter?: RunFilter): Promise<Run[]>;
}
```

笔者认为，这个接口设计的价值在于**把 Agent State 的存储选择权交给开发者**。内存存储适合 CI ephemeral 环境，Postgres 适合和业务数据放在一起，JSONL 适合需要版本控制可审计的场景。

---

## 五、可靠性工程：Run Correlation 与 Safe Checkpoints

### requestId 贯穿全链路

```typescript
const result = await agent.send('Analyze this PR');
// result.run.requestId 可以关联到 backend logs / analytics / support
console.log(result.run.requestId);
```

> 引用原文：*"Every send() now carries a platform-generated requestId, exposed on Run and RunResult and persisted across the in-memory, SQLite, and JSONL stores."*

### 可靠的 wait()

```typescript
const run = await agent.send('Run the full test suite');
await run.wait(); // 现在会等到 terminal result 写入后才 resolve
```

> 引用原文：*"Hydration keeps refreshing until the run reaches a final state, so automation reads a complete result."*

### Safe Checkpoints on Dispose

```typescript
agent.dispose(); // 不再在有 checkpoint blob 残留时清空目录
```

> 引用原文：*"Disposing a local agent no longer removes checkpoint data when a root reference is missing but checkpoint blobs still exist."*

---

## 六、工程意义总结

| 维度 | 旧范式 | 新范式 |
|------|--------|--------|
| **自定义工具暴露** | 独立 stdio/HTTP MCP 服务器 | 函数定义 + 内置 MCP 服务器 `custom-user-tools` |
| **工具继承** | 每个子 Agent 单独注册 | 父级定义 → 全链路渗透 |
| **权限控制** | 全放行或全拦截 | 自然语言指令驱动的分类器 |
| **Subagent 嵌套** | 深度受限 | 任意深度，每层独立 prompt/model |
| **状态存储** | SQLite 单一实现 | SQLite / JSONL / 自定义接口 |

笔者认为，Cursor SDK 这次更新的主线不是"加了什么功能"，而是**把扩展机制统一到了 MCP 协议层**。Custom tools 通过 MCP 服务器暴露，Auto-review 分类器决定调用是否执行，工具继承通过 MCP 链路自动渗透。这使得整个扩展体系有了一致的permission gate，而不是散乱的各自为战。

---

## 附录：关键原文引用

1. *"You can now hand the local agent your own tools by passing function definitions through `local.customTools`, on `Agent.create()` or per `send()`. The SDK exposes them to the agent through a built-in MCP server called `custom-user-tools`, so the model calls your code through the same path and the same permission gate as any other MCP tool."*

2. *"Custom tools are also visible to every subagent of a parent agent, so a tool you define once is available throughout the whole run."*

3. *"A classifier decides which calls run automatically and which to hold back, rather than bypassing review entirely. You steer that classifier with natural-language instructions in `permissions.json`."*

4. *"Subagents can now spawn their own subagents, and so on. A reviewer subagent can delegate to a test-writer, which can delegate further, with each level keeping its own prompt and model."*

5. *"Both SqliteLocalAgentStore and JsonlLocalAgentStore are exported directly. If neither default fits your setup, implement the public LocalAgentStore interface and pass it through `local.store`."*

6. *"Every send() now carries a platform-generated requestId, exposed on Run and RunResult and persisted across the in-memory, SQLite, and JSONL stores."*
