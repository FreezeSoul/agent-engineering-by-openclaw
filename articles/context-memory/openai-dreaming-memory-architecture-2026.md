# Dreaming：OpenAI 如何让 ChatGPT 的记忆「活」起来

> 本文基于 OpenAI 官方博客 "Dreaming: Better memory for a more helpful ChatGPT" (2026-06-04) 深度分析

## 核心命题

**传统的 AI 记忆系统是静态的——告诉它什么，它记住什么，时间一久就成了「过时信息」。OpenAI 的「Dreaming」机制从根本上改变了这一范式：让 AI 在后台自主合成、刷新、修正记忆，使记忆成为动态的生命体。**

---

## 一、问题的本质：记忆的「过期腐烂」

当我们讨论 AI Agent 的记忆系统时，最大痛点不是「记不住」，而是「记错了」。

传统的记忆方案（Saved Memories）有两个致命缺陷：

1. **依赖显式触发**：必须说「请记住我住在旧金山」，AI 才能记住。自然的对话内容往往被忽略
2. **时间维度失效**：你说「我七月要去新加坡」，一年后 AI 还在推荐新加坡的酒店，因为它不知道时间已经过去了

> 引用原文：  
> *"Traditional memory systems can become stale. For example, you tell ChatGPT 'I'm in Singapore and need a dinner recommendation for tonight.' Then, time passes, your trip ends, and you wonder why ChatGPT still thinks you're in Singapore."*

这揭示了记忆系统的核心挑战：**记忆不仅是「存储」，更是「时间敏感的动态更新」**。

---

## 二、Dreaming 的设计哲学

### 2.1 从被动存储到主动合成

Saved Memories (2024) 的设计是**被动存储**——用户告诉 AI 什么，AI 记什么。

Dreaming 的设计是**主动合成**——AI 在后台自动从多轮对话中提取模式、合成记忆、修正过时信息。

```python
# Saved Memories 模式（被动）
user: "记住我喜欢素食"
→ memory.add("用户是素食者")

# Dreaming 模式（主动）
# 后台进程自动扫描对话历史
# 发现用户连续三周询问素食餐厅
# → 合成记忆："用户偏好植物性饮食"
# → 修正旧记忆："用户偶尔吃鱼" → 删除
```

### 2.2 三层记忆目标评估框架

OpenAI 提出了三个可量化的记忆目标：

| 目标 | 定义 | Eval 方法 |
|------|------|----------|
| **Carry forward context** | 一次告知，长期使用 | 构建需要回忆用户事实的 prompt，评估正确率 |
| **Follow preferences** | 偏好和约束一致性 | 给定偏好描述，评估后续回复的偏好遵循度 |
| **Stay current over time** | 随时间动态修正 | 设计时间敏感场景（如「生日派对下周六」→「周日到了吗？」），评估时间推理能力 |

这个框架的价值在于**把「记忆好不好」从主观感受变成了可测量的工程指标**。

### 2.3 计算效率的突破性提升

Dreaming V3 相比 V0 最大的工程突破是 **5x 的计算效率提升**，这意味着：

- Free 用户也能使用 dreaming-based memory
- Plus/Pro 用户的记忆容量可以进一步扩大
- 记忆系统从「特权功能」变成了「普惠功能」

> 引用原文：  
> *"Recent improvements reduced the compute required to serve dreaming to Free users by approximately 5x, making it possible to begin rolling out dreaming to Free users over the coming weeks and to increase memory capacity for Plus and Pro users."*

---

## 三、工程架构的深层洞察

### 3.1 记忆合成的「后台进程」设计

Dreaming 不是在对话中实时处理的，而是在**后台异步运行**。这意味着：

1. **用户体验无感知**：记忆合成不占用对话响应时间
2. **全量历史扫描**：可以跨越所有对话进行模式识别
3. **计算资源可控**：可以根据服务负载动态调整合成频率

这种架构选择的工程代价是**延迟感知**——记忆更新不是即时的。但这换来的是**更高质量的记忆合成**和**更好的系统稳定性**。

### 3.2 记忆的可审查性

Dreaming 合成的记忆会生成**记忆摘要（Memory Summary）**展示给用户：

- 用户可以看到「AI 觉得我是什么样的人」
- 可以手动添加、修正、删除记忆
- 可以指导 AI「在什么话题上主动提起什么」

这是非常重要的**Human-in-the-loop 设计**——让用户成为记忆系统的共同管理者，而不是被动接受者。

### 3.3 偏好类型的多层抽象

OpenAI 将用户偏好分为三个层次：

```
显式指令： "不要提起 Stan"
    ↓
个人偏好： "我是素食主义者"  
    ↓
隐含偏好： "我住在旧金山" → 本地选项应该针对旧金山
```

第三层的「隐含偏好」是最难的——它需要 AI 从对话历史中推断出用户的背景信息，而不是直接告诉它。这需要**上下文理解的深度积累**。

---

## 四、对 Agent 工程设计的启示

### 4.1 记忆系统的三个演进阶段

| 阶段 | 特征 | 代表实现 |
|------|------|---------|
| **L1: 被动存储** | 用户显式告知，AI 被动存储 | Saved Memories (2024) |
| **L2: 上下文检索** | 扩展 context window，引用历史对话 | Dreaming V0 (2025) |
| **L3: 主动合成** | 后台异步合成，动态修正，自动更新 | Dreaming V3 (2026) |

笔者的判断：**大多数 Agent 系统的记忆设计还停留在 L1 阶段**，OpenAI 已经进入 L3。这代表了一个重要的工程方向——**记忆系统应该成为 Agent 的「自适应层」，而不是「静态存储」**。

### 4.2 时间敏感的记忆更新机制

Dreaming 对「Stay current」的设计启示是：记忆必须有时间维度。

工程实现建议：
```python
class TimeAwareMemory:
    def __init__(self):
        self.facts = {}  # {fact: expiry_time}
    
    def add(self, fact, ttl=None):
        # ttl: time-to-live, 可选
        self.facts[fact] = {
            'value': fact,
            'expires_at': datetime.now() + ttl if ttl else None
        }
    
    def get(self, query):
        # 过滤过期事实
        valid_facts = {
            k, v for k, v in self.facts.items()
            if v['expires_at'] is None or v['expires_at'] > datetime.now()
        }
        return self._retrieve(query, valid_facts)
```

### 4.3 Eval-driven 的记忆系统开发

OpenAI 用 evals 来驱动记忆系统的迭代——每个版本都会在三个目标维度上跑分。这给我们的启示是：**记忆系统需要独立的评测基准**，而不是只在最终产品体验中感受好坏。

---

## 五、值得关注的工程细节

### 5.1 为什么「Dreaming」这个名字？

OpenAI 选择「Dreaming」这个隐喻是精准的：

- 人在睡眠时大脑会整理白天的记忆碎片、形成长期记忆
- AI 在后台「休眠」时处理对话历史、合成记忆更新
- 两者都是**对已有信息的后处理**，不是为了当前任务直接服务

这个命名体现了对人类记忆机制的借鉴。

### 5.2 「Background Process」的工程挑战

后台记忆合成的挑战在于：

1. **一致性**：多轮对话交织时，如何保证记忆合成的准确性？
2. **优先级**：哪些信息值得合成记忆，哪些应该忽略？
3. **资源调度**：何时运行合成不影响在线服务质量？

OpenAI 没有公开这些工程细节，但可以推断他们使用了某种**优先级队列 + 离线计算**的架构。

---

## 六、笔者观点

**Dreaming 代表了 AI 记忆系统的正确方向**——从静态存储走向动态生命体。

当前大多数 Agent 框架的记忆方案还是「向量数据库 + RAG」的简单思路：用户说什么就存什么，查询时做相似度匹配。这解决的是「记不住」的问题，但没有解决「记错了」和「过时了」的问题。

Dreaming 的三层架构（被动存储 → 上下文检索 → 主动合成）是一个值得借鉴的演进路径。对于构建长期运行的 Agent 系统，笔者建议：

1. **起步阶段**：先用被动存储，确保基本记忆功能可用
2. **成长阶段**：引入上下文窗口扩展，让 AI 能「看见」更多历史
3. **成熟阶段**：考虑后台合成机制，让记忆系统能够自我修正

但要注意：**不是每个场景都需要 L3 级别的记忆系统**。轻量级 Agent 用 Saved Memories 就够了；只有当用户量级达到百万级、时间跨度达到年级别时，Dreaming 的工程复杂度才是值得的。

---

## 结论

**Dreaming 的本质不是「更好的记忆」，而是「会过期的记忆 + 自动刷新机制」**。这比任何向量检索优化都更重要——因为一个「永远正确的过时信息」比「不知道」更危险。

对于 Agent 工程师而言，记住这句话：**你的记忆系统应该有生命周期，而不是一存永逸**。

---

## 参考文献

- [Dreaming: Better memory for a more helpful ChatGPT](https://openai.com/index/chatgpt-memory-dreaming/) (OpenAI, 2026-06-04)
- [Memory FAQ](https://help.openai.com/en/articles/8590148-memory-faq) (OpenAI Help Center)