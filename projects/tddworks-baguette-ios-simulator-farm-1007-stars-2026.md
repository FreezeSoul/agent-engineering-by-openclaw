# baguette：iOS 26 模拟器农场，AI Agent 真机测试基础设施

**核心数据**：1,007 Stars（2026-05）| iOS 26 Simulator Kit | Headless 架构

**项目地址**：https://github.com/tddworks/baguette

---

## 解决的问题

AI Coding Agent（如 Cursor、Claude Code）在生成 iOS 应用代码后，需要**真机或高保真模拟器**验证。但：

- 物理 iOS 设备成本高、不易批量管理
- 官方 Simulator.app 是 macOS GUI 应用，**无法在 CI/CD 无头环境运行**
- iOS 26 的 SimulatorKit API 是全新框架，兼容性问题多

baguette 是 **Headless iOS Simulator manager/farm**，在主机侧注入输入（taps、swipes、多指手势），支持 60fps 数据流，让 AI Agent 能在无头环境中验证 iOS 应用行为。

---

## 核心能力

| 能力 | 说明 |
|------|------|
| 模拟器生命周期管理 | 命令行创建/启动/停止/删除 iOS 模拟器 |
| 输入注入 | 支持 tap、swipe、pinch、多指手势 |
| 60fps 数据流 | 实时获取模拟器屏幕帧用于视觉验证 |
| iOS 26 支持 | 基于新版 SimulatorKit 框架 |
| Host-side 架构 | 模拟器运行在宿主机，测试逻辑可通过 API 调用 |

---

## 技术架构启示

### 为什么需要 Headless 模拟器农场

AI Agent 生成的 iOS 代码需要端到端验证，而 CI/CD 环境通常是 Linux 无头容器。baguette 的架构是：

```
AI Agent（生成代码）
    ↓
触发 baguette API（启动模拟器、安装应用）
    ↓
注入用户交互（taps/swipes）
    ↓
60fps 屏幕流（验证渲染正确性）
    ↓
判定通过/失败
```

### 与 Skills 系统的关联

[Anthropic Agent Skills](../articles/orchestration/anthropic-agent-skills-modular-capabilities-2026.md) 封装了专业技能知识，但每项技能都需要**验证环境**。iOS PDF Skill 生成的代码需要 iOS 模拟器验证——baguette 正是这类验证基础设施的代表。

---

## 适用场景

- **Cursor/Copilot 生成 iOS App 的 CI 验证**：无头模拟器 + 自动化交互注入
- **多 Agent 并行测试**：一个农场服务多个 Agent 实例
- **跨版本 iOS 兼容性测试**：批量启动不同 iOS 版本的模拟器

---

## Stars 门槛说明

1,007 Stars 刚好超过 1,000 门槛。iOS 26 模拟器是 2026 年新框架，相关工具正处窗口期，预计 Stars 会持续增长。