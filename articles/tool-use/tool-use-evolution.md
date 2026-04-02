# Tool Use 演进：从 Function Calling 到 MCP 生态

> **本质**：Tool Use 是 Agent 感知和操控世界的触角。从最初的硬编码工具调用，到结构化 Function Calling，再到协议级 MCP 生态，工具调用的标准化程度决定了 Agent 能力的边界。

---

## 一、演进阶段总览

```
Hardcoded Functions（硬编码函数）
    ↓ 结构化抽象
Function Calling / Tool Schema（结构化工具）
    ↓ 协议标准化
MCP (Model Context Protocol)（标准化协议）
    ↓ 扩展到Agent间通信
Tool Mesh / Agent Communication（工具网格）
```

---

## 二、Stage 1：硬编码函数调用

最早的 LLM 工具调用是硬编码的——开发者直接在代码中定义函数，LLM 通过文本生成函数名，代码执行调用。

```python
def run_command(cmd: str) -> str:
    """执行 shell 命令"""
    return subprocess.run(cmd, shell=True, capture_output=True)

def read_file(path: str) -> str:
    """读取文件内容"""
    with open(path) as f:
        return f.read()

# LLM 输出需要被解析
if "shell" in response:
    result = run_command(parse_command(response))
```

**问题**：
- 每个工具都需要硬编码解析逻辑
- LLM 容易生成无法执行的函数调用
- 工具描述不统一，LLM 难以理解可用工具

---

## 三、Stage 2：Function Calling / Tool Schema

OpenAI 2023 年推出 Function Calling，将工具定义标准化为结构化 Schema，LLM 输出直接匹配函数签名。

**标准 Tool Schema 格式**：
```json
{
  "type": "function",
  "function": {
    "name": "get_weather",
    "description": "获取指定城市的天气",
    "parameters": {
      "type": "object",
      "properties": {
        "location": {
          "type": "string",
          "description": "城市名，如 北京、Shanghai"
        },
        "unit": {
          "type": "string",
          "enum": ["celsius", "fahrenheit"]
        }
      },
      "required": ["location"]
    }
  }
}
```

**优势**：
- 结构化输出，减少解析错误
- 工具描述作为上下文帮助 LLM 选择正确工具
- 支持多工具并行调用

**代表框架**：
- OpenAI Assistants API（Tools + Function Calling）
- LangChain Tool Calling
- 元工具（Tool Callers）

---

## 四、Stage 3：MCP（Model Context Protocol）

> 详见：[MCP: Model Context Protocol](articles/concepts/mcp-model-context-protocol.md)

MCP 将工具调用的标准化推向了协议层，不仅定义了工具 Schema，还定义了：
- 工具发现机制（Resources）
- 提示模板（Prompts）
- 工具调用生命周期
- 安全权限模型

**MCP 的关键创新**：
```json
// MCP Tool 定义（JSON-RPC 2.0）
{
  "jsonrpc": "2.0",
  "method": "tools/list",
  "params": {},
  "id": 1
}

// MCP Tool Call
{
  "jsonrpc": "2.0",
  "method": "tools/call",
  "params": {
    "name": "filesystem_read",
    "arguments": { "path": "/data/input.txt" }
  },
  "id": 2
}
```

**为什么 MCP 重要**：
1. **一次实现，多 Agent 复用**：开发者只需实现一次 MCP Server，任何兼容 MCP 的 Agent 都可以使用
2. **安全权限模型**：MCP 内置了工具权限管理，解决了 Tool Use 的安全问题
3. **工具发现**：Agent 可以动态发现可用的工具，无需硬编码

---

## 五、Stage 4：从工具调用到工具网格（Tool Mesh）

当前演进方向：**工具不是孤立的，而是形成可编排的网格**。

### 5.1 工具编排（Tool Orchestration）

单个 Agent 需要按顺序或并行调用多个工具：

```python
# 伪代码：工具编排
tools = [search, fetch, parse, summarize]

# 顺序执行
for tool in tools:
    result = await tool.execute(context)
    context.update(result)

# 并行执行
results = await asyncio.gather(*[t.execute(context) for t in tools])
```

### 5.2 工具路由（Tool Routing）

根据任务类型动态选择最合适的工具：

```python
def route(task: str, tools: List[Tool]) -> Tool:
    if "search" in task:
        return search_tools[task.type]
    elif "code" in task:
        return code_tools[task.type]
    elif "file" in task:
        return file_tools[task.type]
```

### 5.3 工具组合（Tool Composition）

多个简单工具组合成复杂工具：

```python
# 组合搜索 + 读取 + 解析
complex_tool = compose(
    web_search,      # 第一步：搜索
    fetch_content,    # 第二步：获取内容
    extract_info      # 第三步：提取信息
)
```

---

## 六、Tool Use 的安全风险

工具调用是 Agent 系统最常见的攻击面：

| 攻击类型 | 描述 | 防御手段 |
|---------|------|---------|
| **权限升级** | Agent 获得了超出预期的工具访问权限 | MCP 权限模型、最小权限原则 |
| **Prompt 注入** | 恶意输入让 Agent 调用不该调用的工具 | 输入验证、权限隔离 |
| **工具劫持** | 恶意工具替代正常工具 | 代码签名、工具校验 |
| **组合爆炸** | 工具A调工具B，工具B再调工具A，死循环 | 调用深度限制、循环检测 |
| **工具误用** | Agent 正确调用工具但参数错误导致事故 | 参数校验、干运行（dry-run） |

> 详见：[The MCP Security Survival Guide](articles/community/mcp-security-survival-guide-tds.md)

---

## 七、Tool Use 与 MCP 的未来

**当前趋势**（基于 2026 年 MCP 路线图）：

1. **Agent 间工具共享**：MCP 从工具调用扩展为 Agent 间通信协议
2. **动态工具发现**：Agent 在运行时动态发现和评估可用工具
3. **工具版本管理**：工具 API 演进时，Agent 自动适配而非重新配置
4. **工具安全标准化**：OWASP 正在制定 Agent 工具安全标准（ASI 系列）

---

## 八、关键概念关联

```
Function Calling / Tool Schema
    ↓
MCP（标准化协议层）
    ↓
Tool Mesh（工具网格）
    ↓
Multi-Agent Tool Sharing（多 Agent 工具共享）
    ↓
A2A + MCP（Agent 间通信 + 工具共享）
```

- MCP 与 A2A 的关系：MCP 负责 Agent 与工具的接口，A2A 负责 Agent 与 Agent 的通信
- Tool Use 是 Harness Engineering 的核心组成部分：工具是 Agent 行为的边界

---

## 参考文献

- OpenAI Function Calling 文档
- MCP 官方规范：modelcontextprotocol.io
- [MCP Security Survival Guide](articles/community/mcp-security-survival-guide-tds.md)
- [MCP Real Faults Taxonomy](articles/community/mcp-real-faults-taxonomy-arxiv.md)
