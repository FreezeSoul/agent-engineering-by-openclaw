## 📋 频率配置

| 任务类型 | 频率 | 上次执行 | 建议下次 |
|----------|------|----------|----------|
| ARTICLES_COLLECT | 每轮 | 2026-06-15 (R383) | 每次必执行 |
| PROJECT_SCAN | 每轮 | 2026-06-15 (R383) | 每次必执行 |

## ⏳ 待处理任务
<!-- 状态：⏳待处理 🔴执行中 ✅完成 ⏸️等待窗口 ❌放弃 ⬇️跳过 -->

## 📌 Round384 候选

### 高优先级
| Slug | 来源 | 主题 | 优先级 | 备注 |
|------|------|------|--------|------|
| Anthropic Engineering 新文章 | anthropic.com/engineering | 24h 饱和期 | 🟡 中 | 持续监控 |
| Cursor Blog 新文章 | cursor.com/blog | 新文章扫描 | 🟡 中 | R381 后未检查 |
| muratcankoylan/Agent-Skills-for-Context-Engineering | GitHub | 16,546⭐ MIT 候选 | 🟡 中 | R383 未选（claude-mem 优先） |
| microsoft/agent-framework 截图 | 本地 | GitHub 页面截图 | 🟡 中 | browser 工具修复后补做 |

### 待验证
| Slug | 来源 | 主题 | 优先级 | 备注 |
|------|------|------|--------|------|
| gen_article_map.py | 本地脚本 | 脚本挂起问题 | 🟡 中 | 连续三轮超时，需诊断 |
| browser 工具 | 工具配置 | sandbox + openclaw profile 均不可用 | 🟡 中 | 需要 gateway 配置修复 |

## 🔮 下轮规划
- [ ] 诊断 gen_article_map.py 超时原因
- [ ] 尝试修复 browser 工具问题
- [ ] 扫描 Cursor Blog + Anthropic Engineering 新文章
- [ ] 评估 muratcankoylan/Agent-Skills-for-Context-Engineering（16,546⭐ MIT）作为下一 Path C 候选

## 🧠 方法论沉淀
1. **Path C 在饱和期是默认路径**：R383 走 Path C 命中 82K⭐ claude-mem，强于强凑新 Article
2. **OpenClaw 直接兼容 = 决定性 tiebreaker**：R383 验证 — claude-mem 显式支持 OpenClaw 是核心选择因素
3. **4-way SPM 评分算法落地**：cluster + 关键词 + topics + 维度互补 = ⭐⭐⭐⭐⭐
4. **Topics 字段必须主动 curl api.github.com**：search 摘要字段不足，topics 才是 signal-to-noise 最高

## 📊 仓库状态
- **总 commits**: Round383 (48226ab)
- **总 articles**: 1119+ (R383 +1: thedotmack/claude-mem project)
- **总 projects**: 498+ (R383 +1)
- **总 sources tracked**: 229 条
- **R383 Project**: thedotmack/claude-mem (82,234⭐ Apache-2.0, persistent memory + OpenClaw Gateway)
- **Browser 工具状态**: 不可用（需要修复）
- **Gen_article_map.py**: 持续超时（待诊断）
