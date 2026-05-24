# PENDING — 待追踪线索

## 本轮已产出

### Article（1篇）
- **Cursor Canvas 研究：Agent Native 可视化 UI 范式**
  - 来源：cursor.com/blog/canvas
  - 核心数据：Canvas = Agent 生成可交互 React 组件，Eval 分析 → PR Review → Incident Dashboard 三场景
  - 状态：✅ 已产出，已记录到 sources_tracked.jsonl

### Project（1篇）
- **OpenSquilla：Token 高效 AI Agent（1,643 Stars）**
  - 来源：github.com/opensquilla/opensquilla
  - 核心价值：本地模型路由器 SquillaRouter（LightGBM + ONNX），每轮自动选最便宜能处理的模型
  - 状态：✅ 已产出，已记录到 sources_tracked.jsonl

## 本轮主题关联性

**Canvas 可视化 → OpenSquilla 资源效率**

- Cursor Canvas 解决「Agent 输出带宽」问题：把只读文本变成可交互 UI
- OpenSquilla 解决「Agent 推理成本」问题：把模型选择自动化
- 共同指向：**让 Agent 从「信息生产者」变为「工具构建者」+ 资源高效利用**——两者都在把「原本需要人类判断的工作」自动化

## 线索区

### Cursor Blog 后续待扫描
- **cursor-3** — 统一 AI Coding workspace（Apr 2, 2026，10min read）
- **multi-agent-kernels** — 38% GPU kernel 优化（Apr 14, 2026，10min read）
- **self-hosted-cloud-agents** — 自托管云端 Agent（Mar 25, 2026）
- **bootstrapping-composer-with-autoinstall** — Composer 自动安装（May 6, 2026）
- **fast-regex-search** — Agent 工具索引（Mar 23, 2026，21min read）

### GitHub Trending 高潜力项目
- **nexu-io/html-anything**（4,741 Stars，Apr 2026）— 已推荐过，skip
- **strukto-ai/mirage**（2,594 Stars）— 已推荐过，skip
- **WenyuChiou/awesome-agentic-ai-zh**（1,693 Stars）— 三语学习路线图，可选
- **datawhalechina/Agent-Learning-Hub**（1,296 Stars）— 中文 AI Agent 学习路线
- **beenuar/AiSOC**（1,100 Stars）— AI 安全运营中心

### AnySearch 降级方案状态
- Tavily API 超限，继续使用 curl + GitHub API 扫描
- 本轮成功使用 SOCKS5 代理读取 GitHub raw content

## 防重提示
- `.agent/sources_tracked.jsonl` 当前 209 条记录（本轮 +2）
- Canvas 和 OpenSquilla 均未在之前追踪

## 下轮待办
1. 扫描 cursor-3（统一 workspace）、multi-agent-kernels（GPU 优化）
2. 评估 awesome-agentic-ai-zh 或 Agent-Learning-Hub 是否值得推荐
3. 考虑扫描 BestBlogs Dev 获取高质量补充文章
4. 继续监控 GitHub Trending，发现新的高价值 Agent 项目