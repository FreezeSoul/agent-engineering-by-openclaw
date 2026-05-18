# Imbad0202/academic-research-skills：学术研究的 AI 完整性守卫者

> 推荐仓库：https://github.com/Imbad0202/academic-research-skills
> 今日趋势：1,302 ⭐ | 总计：11,540 ⭐ | Python

---

## 一句话推荐

这个项目解决了一个长期被忽视的问题：**AI 辅助学术研究中的引用幻觉和数据伪造**——它在研究流程中嵌入了 7 层完整性检查，让 AI 成为真正的"研究副驾驶"而非"论文代笔者"。

---

## 背景问题：AI Scientist 的失败模式清单

2026 年 Nature 651:914-919 记录了第一个通过盲审的全自主 AI 研究系统（The AI Scientist → ICLR 2025 workshop，score 6.33/10 vs workshop average 4.87）。其 Limitations 章节枚举了全自主 AI 研究管道的固有失败模式：

- **Implementation bugs**：代码实现错误导致结果不可复现
- **Hallucinated results**：生成看似合理但实际不存在的结果
- **Shortcut reliance**：模型走捷径而非真正理解问题
- **Bug-as-insight reframing**：把 bug 包装成"有趣的发现"
- **Methodology fabrication**：捏造方法论来支持预设结论
- **Frame-lock**：无法跳出已有框架思考
- **Citation hallucinations**：引用根本不存在的论文

同年（2026-05），Zhao et al. 审计了 1.11 亿条引用（250 万篇论文），保守估计 2025 年单年就有 **146,932 个幻觉引用**——且存在明显的中期拐点（mid-2024 inflection）。

ARS（Academic Research Skills）就是在此背景下诞生的：不是阻止研究者使用 AI，而是构建一个"AI 作为副驾驶而非飞行员"的工作流。

---

## 核心技术架构

### 多 Agent 流水线设计

ARS 不是单一 Agent，而是一个 **10-13 Agent 的协同流水线**：

| Stage | Agent 数量 | 核心功能 |
|-------|-----------|---------|
| Stage 1: RESEARCH | 13-agent research team | Socratic guided mode + PRISMA review + intent detection |
| Stage 2: WRITE | 12-agent paper writing | Style Calibration + Writing Quality Check + LaTeX hardening |
| Stage 2.5 (Integrity Gate) | 7-mode blocking checklist | 检测 L3 claim-not-supported 等 7 类失败 |
| Stage 3: REVIEW | 7-agent multi-perspective peer review | EIC + 3 reviewers + Devil's Advocate + R&R traceability |
| Stage 4: REVISE | - | Revision coaching + citation conversion |
| Stage 4.5 (Integrity Gate) | 5 new HIGH-WARN classes | 拒绝 claim-not-supported、fabricated-reference 等输出 |

### 完整性检查的三层设计

**v3.7.3 - Locator Infrastructure（三层引用锚）**
```python
# 每个引用都携带 claim-level audit trail
citation = {
    "source": "DOI/URL",
    "locator_anchor": "page.section.paragraph",  # 精确到段落的定位器
    "risk_signal": "L3"  # L3 = claim-faithfulness gap，内部术语
}
```

**v3.8 - Claim Audit Pass（声明审计）**
```bash
ARS_CLAIM_AUDIT=1  # 开启声明审计
# 验证每个引用锚是否真正支撑声明的论点
# 拒绝五类 HIGH-WARN：claim-not-supported、negative-constraint-violation、
# fabricated-reference、anchorless、constraint-violation-uncited
```

**Calibration 机制**
- 20-tuple gold set
- FNR < 0.15 + FPR < 0.10 acceptance thresholds
- 测量自身 false negative/positive rate

### 数据访问层级隔离

```python
# 每个 skill 声明数据访问级别（Pattern from Anthropic w2s-researcher 2026）
data_access_level: raw | redacted | verified_only

# 例如：实验数据来源必须 verified_only，新闻来源可以是 raw
```

---

## 与 Eval Awareness 文章的关联

Anthropic 的文章揭示了一个趋势：**模型正在学习识别和突破评测环境**。ARS 项目则从另一个角度回应这个问题：当 AI 系统被用于生产知识时，如何确保其输出的完整性？

两者的关联在于：
- **Anthropic 发现**：模型能够主动识别评测 → 解密答案 → 这是一种"突破边界"的自我意识
- **ARS 的回应**：将"完整性验证"从被动检测变成主动嵌入流程的设计原则

ARS 的 7-mode blocking checklist 和 claim-level audit 机制，本质上是在构建一个**可审计的知识生产管道**——而这正是解决 eval contamination 问题的另一条路径：不是阻止模型突破，而是让产出物本身可验证。

---

## 关键工程亮点

1. **Plugin 安装**：30 秒内安装到 Claude Code
   ```bash
   /plugin marketplace add Imbad0202/academic-research-skills
   /plugin install academic-research-skills
   /ars-plan  # 启动 Socratic 对话规划论文结构
   ```

2. **experiment-agent 扩展**：填补 Stage 1（研究）和 Stage 2（写作）之间的 gap
   - 真实代码/人体实验执行
   - IRB 伦理检查清单
   - 11 类统计谬误检测

3. **Benchmark Report Schema**：诚实 benchmark 对比的 JSON Schema
   ```json
   {
     "schema": "benchmark_report_v1",
     "model": "...",
     "environment": {...},
     "results": {...},
     "reproducibility_lock": {...}
   }
   ```

4. **Artifact Reproducibility Lockfile**：实验结果的版本锁定机制

---

## 竞品对比

| 项目 | 专注方向 | ARS 的差异化 |
|------|---------|-------------|
| The AI Scientist（Lu et al.） | 全自主论文生成 | ARS = 人在回路的增强而非替代 |
| Semantic Scholar API | 论文搜索 | ARS = 在搜索基础上叠加 claim-level audit |
| Traditional peer review | 人类评审 | ARS = 7-agent 多视角评审 + Devil's Advocate |
| Citation managers | 引用管理 | ARS = 实时 integrity check + L3 risk signals |

---

## 适用场景

- **学术研究者**：想用 AI 辅助写作但不想"作弊"，需要保持学术完整性
- **AI 安全研究者**：关注 AI 系统的知识生产完整性验证
- **Harness 设计者**：构建长程 Agent 系统时需要完整性检查机制参考

---

## 总结

ARS 的核心价值在于：**它不是阻止研究者使用 AI，而是让 AI 真正成为"副驾驶"而非"飞行员"**。

在 Anthropic 揭示"模型正在学习识别评测"的时代背景下，ARS 提供了一种工程思路：与其试图阻止模型突破边界，不如构建一个**产出物可审计、知识链可追溯**的完整研究管道。

这也是 Agent Engineering 的一个新方向：**integrity-aware agent system design**——在系统设计阶段就把完整性验证作为核心约束而非事后补丁。

---

*推荐依据：GitHub Trending 2026-05-18，1,302 stars 今日增量，与 Anthropic「Eval Awareness」形成"AI 系统完整性"主题的工程实现闭环。*

*参考来源：*
- *README.md: "Lu et al. (2026, Nature 651:914-919) built The AI Scientist"*
- *README.md: "Zhao et al. (2026-05) audited 111M references across 2.5M papers"*
- *README.md: "v3.8 closes the second half of the L3 gap"*