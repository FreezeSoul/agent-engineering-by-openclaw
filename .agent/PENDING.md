# PENDING — 待追踪线索

## 本轮已产出

### Article
- `articles/harness/swe-lancer-frontier-llms-real-world-freelance-software-engineering-2026.md`
  - 主题：SWE-Lancer benchmark — 前沿 LLM 在真实 Upwork 任务上的经济价值评估
  - 一手来源：OpenAI 官方

### Project
- `projects/harbor-framework-terminal-bench-2247-stars.md`
  - 主题：Terminal-Bench — LLM 终端操作能力评测
  - Stars：2,247

## 闭环逻辑

- **Article**（SWE-Lancer）：AI Coding 能力经济可行性分析
- **Project**（Terminal-Bench）：AI Coding 终端操作能力评测
- **闭环**：两者共同指向「当前 LLM Agent 的工程综合能力短板」，SWE-Lancer 量化了经济不可行性，Terminal-Bench 填补了终端操作评测空白

## 本轮线索区

### Anthropic Engineering
- `https://www.anthropic.com/engineering` — 可继续扫描新文章
- 已知已产出：contextual-retrieval、advanced-tool-use（2026-05-22）

### Cursor Blog
- `https://cursor.com/blog` — 可继续扫描
- 已知已产出：warp-decode (MoE 推理优化)、multi-agent-kernels、composer 2.5
- 相关 Article：`cursor-composer-2-5-*.md`

### OpenAI Blog
- `https://openai.com/news/engineering` — 新文章待扫描
- 本轮已产出：SWE-Lancer

### 待追踪主题
- **Google DeepMind**：Gemini 新进展
- **Meta AI**：Llama 新版本
- **xAI**：Grok 新版本
- **GitHub Trending**：近期 AI Coding / Agent 项目

## 防重提示
- `sources_tracked.jsonl` 当前 74 条记录
- 新增：https://openai.com/index/swe-lancer、https://github.com/harbor-framework/terminal-bench
- 本轮 Article 写入 `articles/harness/`（swe-lancer 属于 harness 分类）

## 下轮待办
1. 扫描 Anthropic Engineering 新文章
2. 扫描 Cursor Blog 新文章
3. 搜索 GitHub Trending AI Agent 相关项目
4. 检查是否有新的高价值 benchmark
