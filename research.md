# DMXAPI 搜索模型选型指南

> 传统大语言模型的知识截止于训练日期，无法获取实时信息。**搜索增强模型**（Search-Augmented LLM）通过在推理过程中主动检索互联网内容，让 AI 具备了"联网能力"——不仅能回答实时问题，还能给出带引用来源的可溯源答案。
>
> DMXAPI 平台目前提供了多款搜索增强模型，覆盖海外搜索与国内搜索两大类。本文档帮助你根据自身场景，快速选择最合适的模型。

---

## 一、模型速览

### 海外搜索模型（Perplexity Sonar 系列）

| 模型 ID                                | 一句话定位                    | 上下文窗口 | 速度                | 成本     |
| -------------------------------------- | ----------------------------- | ---------- | ------------------- | -------- |
| `perplexity-sonar-ssvip`               | 轻量快速，日常问答首选        | 128K       | ⚡ 极快（~1200 t/s） | 💰 低     |
| `perplexity-sonar-pro-ssvip`           | 深度搜索，专业调研主力        | 200K       | ⚡ 快（~88 t/s）     | 💰💰 中    |
| `perplexity-sonar-pro-search-ssvip`    | 多步搜索推理，自主研究工作流  | 200K       | 🔄 中等              | 💰💰 中    |
| `perplexity-sonar-reasoning-pro-ssvip` | 链式推理 + 搜索，复杂分析利器 | 128K       | 🔄 中等              | 💰💰💰 较高 |
| `perplexity-deep-research-ssvip`       | 深度调研，自动生成长篇报告    | 128K       | 🐢 较慢（多步骤）    | 💰💰💰 较高 |

### 国内搜索模型（通义千问系列 & DeepSeek）

| 模型 ID                     | 一句话定位                     | 速度   | 成本     |
| --------------------------- | ------------------------------ | ------ | -------- |
| `qwen-flash-search`         | 极速搜索，简单问题秒回         | ⚡ 极快 | 💰 极低   |
| `qwen-plus-search`          | 均衡搜索，中等复杂度任务       | ⚡ 快   | 💰 低     |
| `qwen3-max-search`          | 高质量搜索，复杂中文任务       | 🔄 中等 | 💰💰 中    |
| `qwen-deep-research`        | 深度调研，拆解复杂问题生成报告 | 🐢 较慢 | 💰💰💰 较高 |
| `DMXAPI-DeepSeek-R1-search` | 推理增强搜索，逻辑分析场景     | 🔄 中等 | 💰💰 中    |

---

## 二、海外搜索模型详解（Perplexity Sonar 系列）

Perplexity Sonar 是目前业内最成熟的搜索增强 LLM API 系列，所有模型均支持**实时网络检索**与**引用溯源**，兼容 OpenAI API 格式。

### 2.1 `perplexity-sonar-ssvip` — 轻量日常款

**基础架构**：基于 Llama 3.3 70B 微调，由 Cerebras 推理加速，输出速度可达 ~1200 tokens/秒。

**核心优势**：

- 速度最快、成本最低，适合高频调用
- SimpleQA 基准 F-score 达 0.773，事实准确性超过 GPT-4o Mini
- 支持引用来源和自定义搜索域名

**最佳场景**：

- ✅ 快速事实查询："XXX 公司最新一季财报营收是多少？"
- ✅ 新闻摘要："今天 AI 领域有什么重要新闻？"
- ✅ 产品/概念速查："对比 React 19 和 Vue 3.5 的主要差异"
- ✅ 嵌入应用的实时问答组件（chatbot、客服等）

**不适合**：

- ❌ 需要多角度深入分析的研究问题
- ❌ 需要严密逻辑链条的推理任务

---

### 2.2 `perplexity-sonar-pro-ssvip` — 深度搜索主力款

**核心优势**：

- 200K 上下文窗口，可处理更长更复杂的对话
- 平均引用数量是 Sonar 基础版的 **2 倍**
- SimpleQA 基准 F-score 达 **0.858**，事实准确性领先
- 支持 High / Medium / Low 三档搜索深度

**最佳场景**：

- ✅ 专业文献调研："总结 2024-2025 年大模型 RLHF 训练的主流方法及各自优缺点"
- ✅ 多角度市场分析："分析东南亚电商市场 2025 年竞争格局"
- ✅ 需要大量引用支撑的写作："撰写一份关于碳中和政策的综述，要求注明出处"
- ✅ 多轮深度追问对话

**不适合**：

- ❌ 简单事实查询（用 Sonar 基础版更经济）
- ❌ 需要复杂逻辑推理的数学/代码分析

---

### 2.3 `perplexity-sonar-pro-search-ssvip` — 多步搜索推理款

**核心优势**：

- 在 Sonar Pro 基础上增加了**自主多步推理**能力
- 不仅是单次"查询+综合"，而是能规划并执行整个研究工作流
- 自动拆分复杂问题为子查询，逐步检索和整合

**最佳场景**：

- ✅ 复杂的比较研究："对比三种主流向量数据库在十亿级数据下的性能、成本和生态"
- ✅ 需要交叉验证的问题："某药物的 III 期临床试验结果如何？不同研究之间是否一致？"
- ✅ 多维度行业洞察："从技术、政策、市场三个维度分析自动驾驶行业现状"

---

### 2.4 `perplexity-sonar-reasoning-pro-ssvip` — 推理分析款

**基础架构**：基于 DeepSeek R1，融合链式推理（Chain-of-Thought）与实时搜索。

**核心优势**：

- **2025 年 Search Arena 评测排名第一**，与 Gemini 2.5 Pro Grounding 并列榜首
- 在正面对决中，53% 的情况下胜过 Gemini 2.5 Pro Grounding
- 先"想清楚"再"搜准确"——推理能力确保搜索方向正确，搜索结果反哺推理深度

**最佳场景**：

- ✅ 复杂逻辑分析："分析美联储加息对亚太新兴市场资本流动的传导机制"
- ✅ 法律条文解读："结合最新判例，分析 GDPR 第 17 条'被遗忘权'的实际执行边界"
- ✅ 技术方案评估："对比 gRPC 与 GraphQL 在微服务架构中的适用场景，结合最新社区实践"
- ✅ 科研假设评估："基于现有文献，评估 XX 疗法对 YY 疾病的疗效证据强度"

**不适合**：

- ❌ 简单查询（杀鸡用牛刀，成本偏高）
- ❌ 对延迟极度敏感的场景

---

### 2.5 `perplexity-deep-research-ssvip` — 深度调研报告款

**核心优势**：

- 可自主发起**数百次搜索**，多步骤综合信息
- 自动拆解复杂课题 → 检索 → 阅读 → 评估 → 优化方法 → 生成报告
- 将数小时的人工研究压缩至数分钟
- 输出为带完整引用的长篇专业报告

**最佳场景**：

- ✅ 学术文献综述："综述 2023-2025 年 Transformer 架构优化的主要研究方向"
- ✅ 行业研究报告："生成一份关于全球 AI 芯片市场的竞争格局分析报告"
- ✅ 竞品深度分析："全面对比 Notion、Obsidian、Logseq 的功能、定价和用户生态"
- ✅ 政策影响评估："分析欧盟 AI 法案对中国出海企业的合规影响"

**注意事项**：

- ⚠️ 单次请求耗时较长（数分钟级别），不适合实时交互
- ⚠️ 搜索费用单独计算（$5/1000 次搜索），一次调研可能触发数十至上百次搜索
- ⚠️ 适合异步任务、后台生成，而非即时对话

---

## 三、国内搜索模型详解

当你的搜索目标主要是中文内容、国内网站、或需要访问国内特有的信息源时，国内搜索模型通常效果更好。

### 3.1 `qwen-flash-search` — 极速中文搜索

**最佳场景**：

- ✅ 中文新闻快讯："今天 A 股市场有哪些重大消息？"
- ✅ 国内产品/服务速查："微信最新版本更新了什么功能？"
- ✅ 简单中文知识问答
- ✅ 对延迟敏感、需要极快响应的嵌入式场景

---

### 3.2 `qwen-plus-search` — 均衡中文搜索

**最佳场景**：

- ✅ 中等复杂度的中文调研任务
- ✅ 国内行业信息查询
- ✅ 中文内容摘要与整理
- ✅ 性价比与质量的均衡之选

---

### 3.3 `qwen3-max-search` — 高质量中文搜索

**最佳场景**：

- ✅ 复杂中文问题的深度搜索
- ✅ 需要高质量中文理解和生成的调研
- ✅ 中文学术和专业领域的搜索任务
- ✅ 对中文输出质量要求较高的场景

---

### 3.4 `qwen-deep-research` — 中文深度调研

**最佳场景**：

- ✅ 国内市场/政策深度研究
- ✅ 需要综合多个中文信息源的复杂课题
- ✅ 中文行业分析报告生成

---

### 3.5 `DMXAPI-DeepSeek-R1-search` — 推理增强搜索

**基础架构**：基于 DeepSeek R1 的推理能力，结合搜索增强。

**最佳场景**：

- ✅ 需要逻辑推理的中文搜索："根据最新财报数据，推断 XX 公司下季度的增长趋势"
- ✅ 技术问题诊断："搜索并分析 XXX 框架这个报错的根本原因和解决方案"
- ✅ 数据驱动的分析任务

---

## 四、场景速查表

根据你的实际需求，快速找到最合适的模型：

| 使用场景                               | 推荐模型                               | 备选模型                            |
| -------------------------------------- | -------------------------------------- | ----------------------------------- |
| **日常快速问答**（今天天气、最新新闻） | `perplexity-sonar-ssvip`               | `qwen-flash-search`                 |
| **中文新闻/国内信息查询**              | `qwen-flash-search`                    | `qwen-plus-search`                  |
| **产品对比、技术选型速查**             | `perplexity-sonar-ssvip`               | `perplexity-sonar-pro-ssvip`        |
| **专业文献调研**（需要引用）           | `perplexity-sonar-pro-ssvip`           | `perplexity-sonar-pro-search-ssvip` |
| **复杂逻辑分析**（金融、法律）         | `perplexity-sonar-reasoning-pro-ssvip` | `DMXAPI-DeepSeek-R1-search`         |
| **学术综述 / 行业报告生成**            | `perplexity-deep-research-ssvip`       | `qwen-deep-research`                |
| **国内市场/政策研究**                  | `qwen-deep-research`                   | `qwen3-max-search`                  |
| **编程问题实时搜索**                   | `perplexity-sonar-ssvip`               | `DMXAPI-DeepSeek-R1-search`         |
| **多维度竞品分析**                     | `perplexity-deep-research-ssvip`       | `perplexity-sonar-pro-search-ssvip` |
| **数据驱动的推理分析**                 | `perplexity-sonar-reasoning-pro-ssvip` | `DMXAPI-DeepSeek-R1-search`         |
| **嵌入应用 / Chatbot**                 | `perplexity-sonar-ssvip`               | `qwen-flash-search`                 |
| **中文学术/专业领域**                  | `qwen3-max-search`                     | `qwen-deep-research`                |

---

## 五、选型决策流程

按照以下问题逐步缩小选择范围：

```
你的搜索目标主要是中文/国内内容吗？
│
├── 是 ──→ 需要深度调研还是快速问答？
│          │
│          ├── 快速问答 ──→ qwen-flash-search / qwen-plus-search
│          ├── 中等深度 ──→ qwen3-max-search
│          ├── 深度调研 ──→ qwen-deep-research
│          └── 需要推理 ──→ DMXAPI-DeepSeek-R1-search
│
└── 否（英文/海外内容为主） ──→ 任务复杂度如何？
                                │
                                ├── 简单问答 ──→ perplexity-sonar-ssvip
                                ├── 专业搜索 ──→ perplexity-sonar-pro-ssvip
                                ├── 多步研究 ──→ perplexity-sonar-pro-search-ssvip
                                ├── 复杂推理 ──→ perplexity-sonar-reasoning-pro-ssvip
                                └── 报告生成 ──→ perplexity-deep-research-ssvip
```

---

## 六、实用建议

### 1. 成本控制策略

- **日常高频场景**优先使用 `sonar-ssvip` 或 `qwen-flash-search`，成本最低
- **Deep Research 类模型**按需使用，单次调用成本较高，适合高价值任务
- Sonar Pro 支持 High / Medium / Low 三档搜索模式，可根据问题复杂度灵活切换搜索深度以控制成本

### 2. 质量优化技巧

- **明确搜索意图**：在 prompt 中说清楚你要搜什么、搜索范围、时间范围。例如："搜索 2025 年之后发表的关于 XX 的论文"
- **要求引用来源**：在 prompt 中明确要求"请列出信息来源链接"，搜索模型会返回更规范的引用
- **利用 system prompt 约束输出格式**：例如要求以表格形式对比、以要点形式列出结论

### 3. 海外 vs 国内搜索的选择

- 搜索**英文内容、国际学术论文、海外市场信息** → Perplexity Sonar 系列
- 搜索**中文内容、国内政策法规、A 股/国内市场信息** → 通义千问搜索系列
- **中英文混合需求** → 可先用 Sonar 搜索海外信息，再用国内模型补充中文资料

### 4. API 调用注意事项

- 所有搜索模型均兼容 **OpenAI API 格式**，切换模型只需修改 `model` 参数
- Deep Research 类模型响应时间较长，建议使用**流式输出**（streaming）以获得更好的用户体验
- 搜索模型的输出通常包含 `citations` 字段，记得在前端展示引用来源以提升可信度

---

## 七、常见问答

**Q：Sonar 基础版和 Sonar Pro 该怎么选？**

> 如果你的问题用一句话就能说清楚（如"XX 是什么"、"最新价格是多少"），用 Sonar 基础版。如果你的问题需要多角度、多来源的深入回答（如"对比分析"、"综述"），用 Sonar Pro。

**Q：Sonar Reasoning Pro 和普通 Sonar Pro 有什么区别？**

> Reasoning Pro 会在搜索前先进行链式推理（Chain-of-Thought），"想清楚要搜什么"再去搜，因此在需要逻辑分析的复杂问题上表现更好。普通 Sonar Pro 更侧重于"搜得广、搜得准"。

**Q：Deep Research 适合实时对话吗？**

> 不适合。Deep Research 会自主发起数十到数百次搜索，耗时数分钟，更适合后台异步生成报告，而非即时交互。

**Q：国内搜索模型能搜索英文内容吗？**

> 可以，但 Perplexity Sonar 系列对英文网页的覆盖和检索质量更优。建议英文内容优先用 Sonar 系列。

**Q：在 Claude Code 等工具中调用搜索模型有什么建议？**

> 推荐使用 `perplexity-sonar-ssvip` 作为默认搜索模型，响应快、输出稳定。如需深度分析，切换到 `sonar-reasoning-pro-ssvip`。避免在需要快速交互的工作流中使用 Deep Research 类模型。

---

*本文档基于 2026 年 2 月各模型的公开信息整理，模型能力和定价可能随时更新，请以 DMXAPI 平台实际显示为准。*

*参考资料：*

- *[Perplexity Sonar 官方介绍](https://www.perplexity.ai/hub/blog/meet-new-sonar)*
- *[Perplexity Sonar 性能与定价](https://www.perplexity.ai/hub/blog/new-sonar-search-modes-outperform-openai-in-cost-and-performance)*
- *[Perplexity Search Arena 评测](https://www.perplexity.ai/hub/blog/perplexity-sonar-dominates-new-search-arena-evolution)*
- *[Perplexity API 平台](https://sonar.perplexity.ai/)*
- *[Sonar Deep Research 文档](https://docs.perplexity.ai/getting-started/models/models/sonar-deep-research)*
- *[通义千问 API 文档](https://www.alibabacloud.com/help/en/model-studio/models)*