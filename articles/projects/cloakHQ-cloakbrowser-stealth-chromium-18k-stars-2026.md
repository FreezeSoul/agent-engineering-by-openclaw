# CloakBrowser：当反爬虫检测遇见 Agent 场景的工程最优解

> **核心命题**：CloakBrowser 通过 58 个 C++ 层面的 fingerprint 补丁，把 Chromium 变成一个「看起来完全像普通用户浏览器」的 stealth browser——不是注入 JS，不是打配置补丁，而是**在源码级别重写指纹特征**。对于需要长时间运行、频繁访问目标网站的 AI Agent，这可能是目前最容易集成、效果最可靠的 anti-bot bypass 方案。

---

## 为什么这个项目值得关注

CloakBrowser 的核心差异化在于它的实现路径：**不绕路，直接改 Chromium 源码**。

市面上大多数 stealth browser 方案都是：
- 配置层面打补丁（容易失效）
- JS 注入层（容易被检测）
- Selenium / Playwright 的 `stealth` 模式（同样容易被检测）

CloakBrowser 的做法是直接编译修改过的 Chromium，二进制层面就与正常 Chrome 无异。这让它在 Cloudflare Turnstile、FingerprintJS、BrowserScan 等 30+ 主流检测系统的测试中都能通过。

**一个细节能说明问题**：项目自称 `humanize=True` 标志可以让鼠标曲线、键盘时序、滚动模式都模拟真实人类行为。这不是简单的随机延迟，而是行为模式的概率建模。

---

## 核心能力

### 58 个源码级 Fingerprint 补丁

覆盖：canvas、WebGL、audio、fonts、GPU、screen、WebRTC、network timing、automation signals、CDP input behavior。

每个补丁都在 C++ 编译层面生效，所以检测工具看到的不是「被修改的浏览器」，而是「真实的浏览器」。

### 3 行代码，30 秒接入

```python
from cloakbrowser import launch
browser = launch()
page = browser.new_page()
page.goto("https://protected-site.com")  # no more blocks
```

从 Playwright 迁移过来只需要改一行 import 语句。Python 和 JavaScript（Node.js）都有原生支持，Puppeteer 也没问题。

### Auto-updating Binary

首次安装自动下载 stealth Chromium 二进制（~200MB），后续在后台检查更新，始终保持最新版本。

---

## 技术原理简析

笔者认为 CloakBrowser 的技术护城河有两条：

**护城河一：CDP Input Behavior 补丁**。主流检测系统（包括 Cloudflare）会检测自动化工具注入的鼠标事件时序特征——真实用户的鼠标移动有微小的加减速曲线，而自动化工具的点击是线性位移。CloakBrowser 的补丁让这些事件在二进制层面就符合真实用户的特征分布。

**护城河二：WebRTC leak 封闭**。WebRTC 会在 `media.peerconnection.enabled` 开启时暴露真实 IP，即使使用了 HTTP 代理。这是一个常见的 IP leak 路径，CloakBrowser 在 C++ 层封闭了这个漏洞。

---

## 与 Agent 场景的关联

本文配对文章（Anthropic Claude Code Sandboxing）讨论的是 Agent 的 filesystem + network 隔离问题。CloakBrowser 在另一个维度提供了补充：**当 Agent 需要访问部署了严格 anti-bot 系统的网站时，如何不被检测和封锁**。

两者共同指向一个趋势：**工程级 Agent 的每个环节都需要「看起来像正常用户」的能力**——安全隔离是基础，「行为伪装」决定了 Agent 能否真正完成任务。

---

## 适用场景

| 场景 | 推荐程度 | 说明 |
|------|---------|------|
| AI Agent 批量访问目标网站 | ⭐⭐⭐⭐⭐ | 核心场景，反-bot 能力直接影响任务成功率 |
| 爬虫项目 | ⭐⭐⭐⭐ | 相比其他方案，检测通过率显著更高 |
| 自动化测试（需绕过反爬）| ⭐⭐⭐⭐ | 同上 |
| 普通浏览自动化 | ⭐⭐ | 杀鸡用牛刀，普通 Playwright 足够 |

---

## 引用来源

项目 README 自述：
> "Not a patched config. Not a JS injection. A real Chromium binary with fingerprints modified at the C++ source level. Antibot systems score it as a normal browser — because it *is* a normal browser."

---
- GitHub：[CloakHQ/CloakBrowser](https://github.com/CloakHQ/CloakBrowser)（18,562 Stars，MIT License）
- PyPI：`pip install cloakbrowser`
- npm：`npm install cloakbrowser`