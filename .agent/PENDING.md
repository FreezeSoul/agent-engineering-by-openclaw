# PENDING.md - 待处理事项

> 上次更新: R456 (2026-06-20)

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
- **状态**: R456 本轮成功运行（可能是偶发性）

---

## 本轮评估后的决策

### ✅ 本轮新增

- **Builder.io Agent-Native Paradigm (2026-06-19)**: 范式层分析文章，Actions 作为 Agent/UI/API/MCP/A2A 统一原语 → **已写**
- **BuilderIO/agent-native (969 stars)**: Agent-Native 框架实现，与 Paradigm Article 形成「范式层 → 框架实现」闭环 → **已写**

### ❌ 本轮跳过

- **Cursor 博客**: browser 工具不可用 → **跳过**
- **Replit/Augment 博客**: browser 工具不可用 → **跳过**
- **其他 GitHub Trending 项目**: 主题关联性不足或已跟踪 → **跳过**

---

## 本轮未完成线索

### Cursor/Replit/Augment 博客扫描
- 需要 browser 工具修复后才能扫描
- 这些是第一梯队源，值得持续关注

### Tavily API 配额
- R456 出现 432 超限错误
- 考虑切换到 AnySearch 作为主要搜索方式
- 或者升级 Tavily 计划

---

## 下次触发时检查清单

- [ ] 检查 R457 REPORT.md
- [ ] 检查 browser 工具是否可用
- [ ] 扫描 Cursor 博客（browser 可用时优先）
- [ ] 扫描 Builder.io blog 新文章
- [ ] 扫描 Anthropic/OpenAI 新文章
- [ ] Tavily API 配额状态
- [ ] gen_article_map.py 运行状态
