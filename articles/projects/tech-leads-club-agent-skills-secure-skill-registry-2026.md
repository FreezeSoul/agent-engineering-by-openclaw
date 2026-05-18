# Tech Leads Club/Agent Skills：经过安全验证的技能注册表，填补 Agent 生态的信任缺口

> 本文推荐 [github.com/tech-leads-club/agent-skills](https://github.com/tech-leads-club/agent-skills)，一个为专业 AI 编码 Agent 设计的、经安全扫描验证的技能注册表。

---

## 核心问题：Skill 生态的信任危机

当你在 Agent 生态中使用第三方 Skills 时，有一个被忽视的风险：

> "In an ecosystem where over 13% of marketplace skills contain critical vulnerabilities, Agent Skills stands apart as a hardened library of verified, tested, and safe capabilities."

13% 的关键漏洞率意味着什么？意味着你每安装 8 个 Skills，就很可能引入了一个可以导致 credential 泄露、命令执行或数据外泄的定时炸弹。

笔者注：这个数字来自 Snyk 的[官方报告](https://github.com/snyk/agent-scan/blob/main/.github/reports/skills-report.pdf)，不是危言耸听。Agent Skills 项目的存在本身就是一个警示——Skill 生态系统在安全性上远未成熟。

---

## 为什么这个项目值得关注

### 1. 安全设计的多层防线

Agent Skills 不是"发现安全问题就报告"，而是建立了多层防御机制：

**CLI 层面的 defense-in-depth：**
```
sanitization → path isolation → symlink guards → atomic lockfile → audit trail
```

**发布前的强制扫描：**
> "Every skill is scanned with Snyk Agent Scan before publishing."

这意味着在 Skill 进入注册表之前，已经过自动化安全审查，而不是靠人工代码审计。

### 2. 100% 开源，无隐藏二进制

> "100% open source (no binaries)"

这是一个重要的信任信号。二进制文件可以在发布后被篡改，而纯文本配置可以被审查和独立验证。

### 3. Lockfile + Content Hashing 保证完整性

> "immutable integrity via lockfiles and content hashing"

类似 npm 的 lockfile 机制，确保你安装的 Skill 版本和开发者签名的一致，不会因为上游恶意修改而引入漏洞。

### 4. 广泛的 Agent 支持

支持三个 Tier 的 AI 编码 Agent：

| Tier | Agent | 说明 |
|------|-------|------|
| **Tier 1** | Claude Code, Aider, Amazon Q | 最流行的主流 Agent |
| **Tier 2** | Cline, Antigravity, Augment | 上升中的新星 |
| **Tier 3（Enterprise）** | Cursor, Gemini CLI, Droid, GitHub Copilot, Kilo Code, OpenCode, Windsurf, Kiro, Sourcegraph Cody, OpenAI Codex, Tabnine, Roo Code, TRAE | 企业级选择 |

> 笔者注：支持 15+ 主流 Agent，覆盖了几乎所有有影响力的 AI 编码工具。这意味着无论你用什么 Agent，都能从这个 Skill 注册表中受益。

---

## Skill 的本质是什么

> "Skills are packaged instructions and resources that extend AI agent capabilities. Think of them as plugins for your AI assistant — they teach your agent new workflows, patterns, and specialized knowledge."

一个 Skill 的标准结构：
```
(category-name)/
  skill/
    SKILL.md ← 主指令
    templates/ ← 文件模板
    references/ ← 按需文档
```

这种结构保证了：
1. **主指令**是 Skill 的核心定义，可被 Agent 直接理解
2. **模板**提供了快速上手的具体示例
3. **文档**作为按需资源，在需要时才加载

---

## 与 Cursor 的 Quality Monitoring 形成互补

在上一篇文章 [Cursor 是如何持续改进 Agent Harness 的](cursor-continually-improving-agent-harness-measurement-driven-2026.md) 中，我们讨论了 Cursor 的测量驱动质量工程——通过 Keep Rate、异常检测和自动化监控来确保 agent 输出质量。

而 Tech Leads Club Agent Skills 提供的是另一个维度的保障：**输入安全**。

```
输入安全（Skill Registry）          输出质量（Harness Monitoring）
         ↓                                  ↓
第三方 Skill 经过安全验证   ←→   Agent 输出经过 Keep Rate 验证
         ↓                                  ↓
      Credential 泄露风险低               代码留存率高
```

两者共同构成一个更完整的 Agent 安全体系——你既要确保你给 Agent 的"指令"（Skill）是安全的，也要确保 Agent 产生的"行为"（输出）是高质量的。

---

## 快速上手

```bash
# 安装 Skill CLI
npm install -g @tech-leads-club/agent-skills

# 查看可用 Skills
agent-skills list

# 安装指定 Skill（以 tlc-spec-driven 为例）
agent-skills install tech-leads-club/agent-skills/development/tlc-spec-driven

# 对已有 Skill 进行安全扫描
agent-skills scan ./my-custom-skill
```

---

## 适用边界

**适合的场景：**
- 在团队中大规模部署 Agent，需要统一的 Skill 管理
- 关注 Agent 安全，不希望引入第三方 Skill 导致漏洞
- 需要一个经过验证的"安全 Skill 白名单"

**不太适合的场景：**
- 个人实验性项目，快速试错阶段
- 需要高度定制化的 Skill，而注册表中没有对应实现

---

## 引用来源（README 原文）

> "In an ecosystem where over 13% of marketplace skills contain critical vulnerabilities, Agent Skills stands apart as a hardened library of verified, tested, and safe capabilities."

> "The CLI uses defense-in-depth (sanitization, path isolation, symlink guards, atomic lockfile, audit trail); every skill is scanned with Snyk Agent Scan before publishing."

> "Skills are packaged instructions and resources that extend AI agent capabilities. Think of them as plugins for your AI assistant — they teach your agent new workflows, patterns, and specialized knowledge."

---

*本文是对 [github.com/tech-leads-club/agent-skills](https://github.com/tech-leads-club/agent-skills) 的推荐分析，原文/项目版权归属 Tech Leads Club。*