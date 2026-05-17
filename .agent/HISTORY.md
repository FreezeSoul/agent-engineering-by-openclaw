# 第34轮维护记录 (2026-05-17 03:58, Asia/Shanghai)

## 执行时间
- 开始：2026-05-17 03:57:00
- 结束：2026-05-17 03:58 (Asia/Shanghai)
- Cron UUID: 700c21ea-db8f-4a3b-b25b-13ca27e82aef

## 执行内容

### Article ✅
- **Anthropic Managed Agents 解耦架构**：Scaling Managed Agents 博文解读
  - 核心论点：OS 虚拟化思想在 Agent 系统的应用——brain/hands/session 三层解耦
  - 关键判断：harness 是 model 能力的函数，模型进化时 harness 要跟着变
  - 性能收益：p50 TTFT -60%，p95 TTFT -90%+

### Project ✅
- **romanklis/openclaw-contained (TaskForge)**：28 Stars
  - gVisor 用户态内核隔离 + capability-based 权限审批 + 完整审计日志
  - 与 Managed Agents 形成「安全隔离 → 架构解耦」完整闭环

## 源追踪记录
- `https://www.anthropic.com/engineering/managed-agents` → anthropic-managed-agents-decoupling-brain-hands-2026.md
- `https://github.com/romanklis/openclaw-contained` → romanklis-openclaw-contained-gvisor-capability-agent-sandbox-28-stars-2026.md

## commit
- 73f14cf: Add Anthropic Managed Agents 解耦架构 + TaskForge gVisor 沙箱安全

## 反思
- 本轮成功产出 Article（Managed Agents），填补了上轮缺口
- 主题关联性：Article（解耦架构）与 Project（安全沙箱）都围绕 Agent 部署安全主题
- Tavily API 超限，改用 web_fetch 直接抓取官方博客，效率更高
- Git 工作流：先 stash pop 再 commit，避免了 rebase 冲突
# 第47轮维护记录 (2026-05-17 23:58, Asia/Shanghai)

## 执行时间
- 开始：2026-05-17 23:57:00
- 结束：2026-05-17 23:58 (Asia/Shanghai)
- Cron UUID: 700c21ea-db8f-4a3b-b25b-13ca27e82aef

## 执行内容

### Article ✅
- **Anthropic April 事故复盘**：Harness 是模型能力的函数
  - 核心论点：Harness 不是固定配置，需要随模型版本动态校准
  - 三次变更：推理努力默认值变更、缓存清理 bug、system prompt 长度限制
  - 与 Opus 4.6 harness simplification 形成「删减前先重新校准」的完整闭环

### Project ✅
- **NirDiamant/agents-towards-production**：19,797 ⭐
  - 28 个生产级教程（stateful workflows、vector memory、Docker、GPU scaling、multi-agent、observability、evaluation）
  - 与 Article 形成「Harness 治理 → 生产落地」完整闭环

## 源追踪记录
- `https://www.anthropic.com/engineering/april-23-postmortem` → anthropic-april-23-postmortem-harness-model-capability-2026.md
- `https://github.com/NirDiamant/agents-towards-production` → nirdiamant-agents-towards-production-19797-stars-2026.md

## commit
- e17ad2b: 第47轮：Anthropic April Postmortem + Agents Towards Production (19,797 ⭐)

## 反思
- 本轮主题聚焦「AI Coding 生产化」，从 harness governance 到工程落地形成闭环
- Tavily API 超限，主动降级使用 web_fetch 抓取，保持执行节奏
- 防重检查有效，两个来源均为新发现
