# anthropics/claude-plugins-official：Claude Code 官方插件市场（31K Stars）

> 核心判断：Anthropic 正在把 Claude Code 打造成一个**插件化平台**，而这个仓库是官方维护的质量标杆——不是所有插件都值得信任，但这个仓库里的，Anthropic 替用户做了一次筛选。

---

## 解决什么问题

Claude Code 本身是一个强大的 Agent，但它的能力边界由内置工具集决定。插件系统允许第三方扩展 Claude Code 的能力——新增 MCP 服务器、新增 Skill、新增 Agent 行为定义。

问题是：**第三方插件的质量参差不齐，安全风险不透明**。

claude-plugins-official 是 Anthropic 官方的回应：

> "Make sure you trust a plugin before installing, updating, or using it. Anthropic does not control what MCP servers, files, or other software are included in plugins."

这个仓库的定位是：**Anthropic 认证过的插件目录**，有官方维护的 quality gates。

---

## 目录结构：两类插件的治理模型

```
/plugins               # Anthropic 内部开发和维护
/external_plugins/     # 第三方插件，通过审核流程准入
```

**Internal Plugins**（`/plugins`）：
- Anthropic 团队成员开发和维护
- 直接反映 Claude Code 最新的能力和方向
- 有完整的测试和质量保证

**External Plugins**（`/external_plugins`）：
- 第三方合作伙伴和社区提交
- 需要通过 Anthropic 的 quality + security 审核
- 审核通过后才会在 marketplace 中展示

这个**两层治理模型**很有意思：Anthropic 没有把插件生态完全放手给社区，而是维护了一个官方认证体系。这与 WordPress 插件生态有点类似——社区可以开发，但需要通过审核才能进入官方目录。

---

## Skill-Bundle 插件：npm 风格的 Skill 分发

仓库里有一个值得注意的技术创新：**Skill-Bundle 插件**。

当一个插件的源码仓库本身包含 Skill 文件（`SKILL.md`），但没有 `.claude-plugin/plugin.json` 清单文件时，marketplace entry 可以直接声明这些 skills：

```json
{
  "name": "example-bundle",
  "description": "Brief description of the bundled skills.",
  "author": { "name": "Author Name" },
  "category": "development",
  "source": {
    "source": "git-subdir",
    "url": "https://github.com/example-org/sdk.git",
    "path": "packages/agent-skills",
    "ref": "main",
    "sha": "<commit sha>"
  },
  "strict": false,
  "skills": ["./skill-a", "./skill-b", "./skill-c"],
  "homepage": "https://github.com/example-org/sdk"
}
```

**这本质上是 Skill 的 CDN 机制**：Skill 作者不需要把自己的 SKILL.md 文件提交到 Claude Code 官方仓库，只需要维护自己项目里的 SKILL.md，然后在 plugin.json 里声明路径引用即可。

这与 npm 的模块分发逻辑非常相似——你不需要把所有依赖打包进项目，只需要声明「我依赖这个版本的那个包」。SKILL.md 就是那个「包」，plugin.json 就是 package.json。

---

## 安装方式

```bash
# 从官方 marketplace 安装
/claude plugin install {plugin-name}@claude-plugins-official

# 或者通过 Discover 命令浏览
/plugin > Discover
```

---

## 战略意义

claude-plugins-official 加上 knowledge-work-plugins，代表 Anthropic 的**平台化战略**：

- **claude-plugins-official**：开发者生态 + 工具扩展
- **knowledge-work-plugins**：企业级垂直场景封装
- **Advisor Strategy**：运行时智能升级机制
- **Skill Creator**：技能创作和分发基础设施

这四条线合在一起，构成了一个**完整的 Agent 平台架构**——而且是官方在推动的。

---

**引用来源**：

> "Make sure you trust a plugin before installing, updating, or using it. Anthropic does not control what MCP servers, files, or other software are included in plugins and cannot verify that they will work as intended." — Anthropic, [Claude Code Plugins Directory README](https://github.com/anthropics/claude-plugins-official)

> "When a plugin's source repository ships skills (SKILL.md files) without a .claude-plugin/plugin.json manifest, the marketplace entry can declare the skills directly." — Anthropic, [Claude Code Plugins Directory README](https://github.com/anthropics/claude-plugins-official)
