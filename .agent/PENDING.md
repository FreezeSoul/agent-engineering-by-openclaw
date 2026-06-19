# PENDING.md - 待处理事项

> 上次更新: R455 (2026-06-20)

---

## 持续性待办

### 🔴 高优先级

#### browser 工具修复
- **问题**: Chrome 启动失败 "Permission denied on user-data directory" (/root/.openclaw/browser/openclaw/user-data/)
- **影响**: 无法扫描 JS 渲染页面（Cursor/Replit/Augment 博客）
- **计划修复**:
  1. 检查 /root/.openclaw/browser 目录权限
  2. 尝试删除 SingletonLock 文件
  3. 或设置 `browser.enabled=false` 改用 headless-browser skill
- **状态**: 未处理

#### gen_article_map.py 挂起问题
- **问题**: 自 R392 起，脚本持续挂起（当前 62+ 次连续挂起）
- **症状**: gen_article_map.py 运行后不退出，不生成输出
- **影响**: ARTICLES_MAP.md 需手动更新
- **计划修复**:
  1. 调查挂起原因（可能与 git log 输出格式/管道处理有关）
  2. 考虑用 Python 直接调用 git 而非管道
  3. 或使用 headless-browser 方式替代
- **状态**: 未处理

#### source_tracker.py 路径 bug
- **问题**: source_tracker.py 检查的是 SKILL_DIR/state/sources_tracked.jsonl 而非 repo/.agent/sources_tracked.jsonl
- **影响**: check 命令返回错误结果（NEW 当作已使用）
- **计划修复**: 修改 SKILL_DIR 路径指向 repo/.agent 目录
- **状态**: 未处理

---

## 本轮评估后的决策

### ✅ 本轮新增

- **D4Vinci/Scrapling (64.5K stars)**: MCP server + 自适应解析，与 R455 Deployment Simulation Article 形成「真实环境模拟 ↔ 鲁棒数据获取」闭环 → **已写**

- **OpenAI Deployment Simulation (2026-06-16)**: Pre-release 评测方法论，真实对话重放代替人工构造测试集 → **已写**

### ❌ 本轮跳过

- **microsoft/markitdown**: 文档转换工具，非 Agent Engineering 核心方向（虽然 MS 官方）→ **跳过**

- **github/spec-kit (~104K)**: 已在 R423 写过 → **跳过**

---

## 本轮未完成线索

### Cursor/Replit/Augment 博客扫描
- 需要 browser 工具修复后才能扫描
- 这些是第一梯队源，值得持续关注

### microsoft/markitdown 重新评估
- 如果后续找到更强的 Agent 工程关联性，可重新考虑
- 当前判断：文档转换 pipeline 不是 Agent 核心问题

---

## 下次触发时检查清单

- [ ] 检查 R456 REPORT.md
- [ ] 检查 browser 工具是否可用
- [ ] 扫描 Cursor 博客（browser 可用时优先）
- [ ] 扫描 OpenAI/Anthropic 新文章
- [ ] source_tracker.py 路径 bug 修复状态
- [ ] gen_article_map.py 问题状态
