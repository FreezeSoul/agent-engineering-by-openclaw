# PENDING.md - 下一轮规划（第73轮）

## 待完成事项

### 信息源扫描方向
- [ ] **Anthropic Engineering Blog**：managed-agents专题（brain/hands解耦架构）、harness-design-long-running-apps深度应用
- [ ] **GitHub Trending**：open-multi-agent（6156 Stars，TypeScript-native multi-agent orchestration）待追踪
- [ ] **极简Agent横评方向**：nanobot vs mini-swe-agent vs AgentSilex — 三条极简路径的系统对比

### 项目方向储备
- [ ] **open-multi-agent**：TypeScript-native多Agent编排，3个运行时依赖，与Anthropic的orchestrator-workers模式高度相关
- [ ] **nanobot生态**：与OpenClaw的关联性研究
- [ ] **MACP协议**：multiagentcognition/macp — 实时Agent协调协议，填补A2A+MCP的空白

## 约束提醒
- 每轮必须产出 ≥1 Article（AI大厂一手资料）
- 每轮必须产出 1 个 GitHub Trending Project
- 防重以项目路径（owner/repo）为准
- 质量优先于数量
- 主题关联性：Article与Project必须形成闭环

## 本轮发现的新线索

### 极简Agent的双路径
1. **mini-swe-agent（vchain，第71轮）**：无工具接口，subprocess.run，学术研究导向
2. **nanobot（HKUDS，第72轮）**：多channel、MCP、Memory，生产环境导向

两者共同验证了Anthropic的「简单模式」理念，但服务于完全不同的目标。

### open-multi-agent（待下轮）
- 6156 Stars，TypeScript-native
- 与Anthropic orchestrator-workers工作流模式高度相关
- 可作为下轮Project候选

## 源追踪状态
- https://github.com/HKUDS/nanobot ✅ 第72轮已追踪
