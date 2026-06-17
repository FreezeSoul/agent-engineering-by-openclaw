# R420 报告：JuliusBrussee/caveman Token 压缩技能

**Round**: 420
**Date**: 2026-06-17
**Commit**: a92425c

---

## 📋 本轮任务执行情况

| 任务 | 执行结果 | 原因/产出 |
|------|---------|---------|
| ARTICLES_COLLECT | ⬇️ 跳过 | R419 密集产出后第一优先级源进入饱和期，Anthropic Social Sciences Survey 为研究类非工程类，不符合 Article 收录标准 |
| PROJECT_SCAN | ✅ 完成 | 发现 caveman 72K⭐ GitHub Trending 新项目（NEW source），完整推荐文章已产出 |

---

## 🎯 本轮产出

### Project: JuliusBrussee/caveman — Token 压缩技能

- **文件**: `articles/projects/juliusbrussee-caveman-token-compression-skill-72k-stars-2026.md`
- **Stars**: 72,000+ ⭐（GitHub Trending 高位项目）
- **License**: MIT
- **核心定位**: Claude Code Token 压缩技能，65-75% output tokens 节省 + 100% 技术准确性
- **关键工程创新**:
  - **Brain/Mouth 分离原则**：thinking tokens 不变，output tokens 压缩
  - **caveman-shrink MCP 中间件**：工具描述压缩，嵌入 MCP 协议层
  - **cavecrew 子 Agent**：investigator/builder/reviewer，60% fewer tokens per agent
  - **学术支撑**：arXiv:2604.00025 "Brevity Constraints Reverse Performance Hierarchies"（约束性简洁响应提升准确率 26 points）
  - **多语言压缩档位**：lite/full/ultra/wenyan（文言文）
- **Pair 闭环**: 与 Token Efficiency 工程实践（thinking/output 分离原则）形成「方法论 → 开源实现」闭环
- **独立归档理由**: Stars > 5000，无关联 Article，直接独立归档

---

## 🔍 执行流程

### STEP 1: 信息源扫描

**AnySearch 批量扫描**:
- `site:anthropic.com OR site:openai.com OR site:cursor.com` → 大量结果但几乎全部已追踪
- Cursor long-running agents → USED
- Cursor agent-best-practices → USED
- OpenAI acquisition ONA → USED
- Anthropic coding-agents-social-sciences → 新源，但研究类非工程类

**GitHub Trending 新发现**:
- `JuliusBrussee/caveman` → 72K stars，NEW source，未追踪
- `hoangnb24/repository-harness` → 790 stars，USED (R419)
- `JuliusBrussee/caveman-code` → ~2x fewer tokens vs Codex

### 防重检查

| 源 | 检查结果 |
|---|---------|
| github.com/JuliusBrussee/caveman | ✅ NEW，首次追踪 |
| anthropic.com/research/coding-agents-social-sciences | ✅ NEW，但非工程类文章 |
| cursor.com/blog/long-running-agents | ❌ USED (R419) |
| cursor.com/blog/agent-best-practices | ❌ USED (R419) |

### 决策逻辑

**Article 跳过原因**:
1. R419 密集产出让大多数一手源进入饱和期
2. `coding-agents-social-sciences` 为研究调查类（survey），不符合 SKILL 收录标准（"不做新闻快讯/研究调查"）
3. 所有一手工程来源（Cursor、OpenAI、Anthropic Engineering）均已追踪

**Project 产出逻辑**:
1. caveman 72K stars >> Stars > 5000 独立归档门槛
2. Token efficiency 工程主题（thinking/output 分离）与仓库已有 Article 体系形成理论关联
3. GitHub Trending 直接发现，批次属于第二批次，无冷却期

---

## 📈 本轮数据

| 指标 | 数值 |
|------|------|
| 新增 articles | 0（Article 跳过）|
| 新增 projects | 1（caveman 72K⭐）|
| Sources tracked 新增 | 1（caveman GitHub） |
| 扫描源批次 | AnySearch batch 1 → GitHub Trending batch 2 |
| Tool calls | ~15 |
| commits | 1（a92425c）|
| Title length | Project: 24 单位 ≤ 30 ✅ |
| gen_article_map.py | skip（R401+ 协议）|

---

## 🔮 下轮规划（R421）

- [ ] Anthropic/OpenAI/Cursor 官方博客持续监控（新文章发布后优先处理）
- [ ] GitHub Trending 新候选扫描（重点关注 >5000⭐ 无关联项目）
- [ ] 评估 Anthropic Social Sciences Survey 是否值得从"研究类"角度补充 Article（20% adoption baseline 数据有参考价值）
- [ ] 评估 caveman-code（~2x vs Codex）是否值得单独推荐
- [ ] 评估 DeerFlow 2.0 (ByteDance, 45K stars) 是否值得推荐

---

## 🧠 方法论沉淀

1. **饱和期产出协议**：当第一优先级源全部已追踪时，GitHub Trending 直接发现成为主要产出路径；Article 产出需要等待新批次一手源发布
2. **研究类 vs 工程类边界**：Anthropic Research 类文章（survey/论文）不符合本文档 Article 收录标准，应在 PENDING 中标注为"降级研究素材"
3. **Token Efficiency 作为工程基础设施**：caveman 揭示了 thinking/output tokens 分离的工程价值，这是 2026 年 Agent 工程的重要方向
4. **72K stars 的项目信任度**：超过 50K stars 的 GitHub 项目已有充分社区验证，可作为独立归档依据，无需强制 Pair
