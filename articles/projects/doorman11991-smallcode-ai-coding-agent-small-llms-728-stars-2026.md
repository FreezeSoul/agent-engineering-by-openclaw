# Doorman11991/smallcode — 小模型 AI Coding Agent，728 Stars

> **推荐理由**：SmallCode 揭示了一个被主流叙事忽略的赛道——在消费级硬件（7B-20B 模型）上运行的 AI Coding Agent，零云 API 依赖、强调隐私优先。它证明了在小模型约束下，通过精细的架构设计（预算感知 context、多格式容错解析、TODO-file 分解），可以实现「可用」的 coding agent 体验。

**GitHub**：[Doorman11991/smallcode](https://github.com/Doorman11991/smallcode) | 728 ⭐ | Created 2026-05-18

---

## 核心定位

| 维度 | OpenCode（竞品） | SmallCode |
|------|----------|-----------|
| 目标模型 | 前沿模型（Claude/GPT-5） | **7B-20B 本地模型** |
| Context | 倾倒式 | **预算管理 + 摘要压缩** |
| 工具调用 | 假设可靠 JSON | **多格式容错解析** |
| 任务规划 | 单次 shot | **TODO-file 分解** |
| 隐私性 | API 到云端 | **完全本地** |

## 技术亮点

- **预算感知型 Context**：动态摘要超出预算的部分，而非倾倒式塞入 context
- **多格式容错解析**：不假设 JSON 输出，尝试多种格式，失败时才报错
- **TODO-file 分解**：将单次 shot 转为多轮对话，通过外部化状态维持任务对齐
- **Search-and-replace patch**：避免长文本生成时的首尾不一致问题

## 安装

```bash
npm install -g smallcode
# 或直接运行
npx smallcode
```

**依赖**：Node.js 18+，本地 LLM 服务器（LM Studio / Ollama）

## 关联文章

本文与 Cursor 第三时代（云端并行 Agent）形成对比：
- Cursor 赛道：**大模型 + 云端 + 并行**
- SmallCode 赛道：**小模型 + 本地 + 单实例**

两者代表了 AI Coding 的两条不同路径，服务不同市场需求。

---

*数据来源：[GitHub README](https://github.com/Doorman11991/smallcode)*