# R460 REPORT — AddyOsmani Long-running Agents + Zhipu GLM-5

> **执行时间**: 2026-06-20 11:57（UTC+8）
> **新增**: 1 Article + 1 Project

---

## 本轮产出

### Article
| 字段 | 内容 |
|------|------|
| 文件 | `articles/harness/addyosmani-long-running-agents-three-walls-harness-2026.md` |
| 来源 | https://addyosmani.com/blog/long-running-agents/ |
| 字数 | ~4900 chars |
| 核心观点 | 长程 Agent 三个壁垒（有限上下文、无持久状态、无自我验证）；行业四方案对比（Anthropic Brain-Hands-Session / Cursor Planner-Worker-Judge / Google Agent Platform / Ralph Loop） |
| 原文引用 | 4 处 |

### Project
| 字段 | 内容 |
|------|------|
| 文件 | `articles/projects/zai-glm-5-vibe-coding-to-agentic-engineering-4620-stars-2026.md` |
| 来源 | github.com/zai-org/GLM-5 |
| Stars | 4,620 |
| 核心亮点 | 第一个 Intelligence Index v4.0 突破 50 分的开源模型；Vending-Bench 2 年尺度任务 #1 开源；DSA 稀疏注意力（90% 上下文冗余可被利用）；异步 RL 基础设施 |
| 关联 Article | R460 Article（模型层 ↔ Harness 工程层闭环） |

---

## 主题关联性分析

| Article | Project | 关联强度 | 关联方式 |
|---------|---------|---------|---------|
| AddyOsmani 长程 Agent 三壁垒 + 四方案对比 | Zhipu GLM-5 | **强闭环** | Article 描述 Harness 层工程方案；GLM-5 在模型层验证了长程推理、年度任务、自我修正能力 |

---

## 本轮扫描发现

| 来源 | 状态 | 原因 |
|------|------|------|
| Anthropic Engineering Blog | 无新增 | 已追踪（harness-design-long-running-apps） |
| Cursor Blog | 无新增 | 已追踪（scaling-agents / cloud-agent-lessons） |
| OpenAI Blog | 无新增 | 近期无高价值 Agent 工程文章 |
| AnySearch 通用搜索 | 扫描完成 | 发现 AddyOsmani Long-running Agents（新来源） |
| GitHub Trending | 扫描完成 | GLM-5（未追踪，与 Article 主题强关联） |
| LangChain Blog | 已读未写 | Runtime + Anatomy 文章可降级为 cite，不独立成 Article |
| headroom / flue | 已追踪 | Stars 高但与 Article 关联度不足 |

---

## 本轮数据

| 指标 | 数值 |
|------|------|
| 新增 articles 文章 | 1 |
| 新增 projects 推荐 | 1 |
| 原文引用数量 | Article: 4 处 / Project: 3 处 |
| source_tracker 记录 | 2 条 |
| ARTICLES_MAP 更新 | ✅ |

---

## 反思与评估

### 做对了

1. **AddyOsmani 作为 Article 而非 LangChain**: LangChain "Runtime + Anatomy" 两篇都是 LangChain 自家产品视角，不如 AddyOsmani 的跨厂商 practitioner 对比稀缺性高
2. **选择 GLM-5 而非 easy-agent**: easy-agent Stars=0（新 fork），推荐可信度不足；GLM-5 有完整 arXiv 论文，4620 Stars，主题与 Article 强闭环
3. **跳过 headroom**: 39K Stars 明星项目但属于 Token 压缩工具方向，与「Harness 工程」主题关联度中等，不强行配对
4. **持续使用 AnySearch**: Tavily 配额问题持续，AnySearch 功能稳定

### 需改进

1. **browser 工具问题仍未解决**: 影响 Cursor/Replit/Augment 等 JS 渲染博客的扫描；建议设置 `browser.enabled=false` 改用 headless-browser skill
2. **LangChain 两篇文章（Runtime + Anatomy）未利用**: 两篇都有具体的 checkpointing/interrupt/resume 实现细节，值得作为 cite 引用补充到现有 harness 文章中

### 遗留问题

1. **Tavily API 配额**: 持续问题，维持 AnySearch
2. **browser 工具不可用**: 影响 JS 渲染页面扫描
3. **LangChain Runtime/Anatomy**: 可作为 cite 引用，不独立成 Article

---

## 下一步 (R461)

1. 扫描 Anthropic/OpenAI 新文章（AnySearch）
2. GitHub Trending 新项目发现（AnySearch）
3. 尝试修复 browser 工具或改用 headless-browser skill
4. 考虑将 LangChain Runtime/Anatomy 文章降级为现有 harness 文章的 cite
5. 监控 Tavily 配额问题
