# Claude Opus 4.7 使用指南

Claude Opus 4.7 是 Anthropic 推出的旗舰模型，在编程、复杂推理和长时间 Agent 任务上表现尤为突出。相比 Opus 4.6，Opus 4.7 新增了 `xhigh` 思考力度等级，并对 `effort` 参数的响应更加精确，适合需要深度思考和多步骤工具调用的场景。


## 新功能

### 高分辨率图片支持

Opus 4.7 是首个支持高分辨率图片的 Claude 模型：

- 图片分辨率上限从 1568px / 1.15MP 提升至 **2576px / 3.75MP**
- 模型输出的坐标与实际像素 **1:1 对应**，无需任何缩放换算
- 自动生效，无需额外 beta header

:::warning
高分辨率图片最多消耗约 **3 倍**图片 Token（单张上限约 4784 tokens，旧模型约 1600 tokens）。若不需要高分辨率细节，建议在发送前降采样以控制成本。
:::

### Task Budgets（beta）

Opus 4.7 新增 `task_budget` 参数，用于给整个 Agent 循环设置总 Token 预算。模型会感知剩余预算，并在预算耗尽前主动收尾任务。

**与 `max_tokens` 的区别：**
- `task_budget`：模型可见，建议性上限，作用于完整 Agent 循环（含思考、工具调用、输出）
- `max_tokens`：模型不可见，硬限制，仅作用于单次请求的生成 Token 数

```python
import anthropic

client = anthropic.Anthropic(
    api_key="YOUR_DMXAPI_KEY",
    base_url="https://www.dmxapi.cn",
)

response = client.beta.messages.create(
    model="claude-opus-4-7",
    max_tokens=128000,
    output_config={
        "effort": "high",
        "task_budget": {"type": "tokens", "total": 128000},
    },
    messages=[
        {"role": "user", "content": "审查代码库并提出重构方案。"}
    ],
    betas=["task-budgets-2026-03-13"],
)
```

:::tip
Task Budgets 适用于需要控制 Agent 总开销的场景（如代码审查、自动化工作流）。质量优先的开放式任务建议不设置。最小值为 20k tokens。
:::

---

## Breaking changes（从 Opus 4.6 迁移）

以下变更在 Opus 4.7 上会直接返回 **400 错误**，迁移前必须处理。

**1. 扩展思考参数移除**

`thinking: {type: "enabled", budget_tokens: N}` 已不支持，调用直接报 400。改用自适应思考配合 effort 参数：

```python
# 旧写法（Opus 4.6）
thinking={"type": "enabled", "budget_tokens": 32000}

# 新写法（Opus 4.7）
thinking={"type": "adaptive"},
output_config={"effort": "high"},  # 或 xhigh / max / medium / low
```

:::warning
Opus 4.7 **默认不启用思考**，不传 `thinking` 字段等同于不思考。需要思考时必须显式设置 `thinking: {type: "adaptive"}`。
:::

**2. 采样参数移除**

`temperature`、`top_p`、`top_k` 设为任何非默认值均返回 400。请从请求中直接移除这三个参数，通过 Prompt 引导模型行为代替。

**3. Prefill 移除**

在 assistant 消息开头预填内容返回 400。改用结构化输出、system prompt 指令或 `output_config.format`。

---

以下两项不报错，但属于**静默行为变化**，可能影响现有产品。

**4. 思考内容默认不返回**

思考块（thinking block）仍出现在响应流，但 `thinking` 字段默认为空（Opus 4.6 默认返回摘要）。需要展示思考过程时，显式设置：

```python
thinking = {
    "type": "adaptive",
    "display": "summarized",
}
```

**5. 新分词器，Token 消耗增加**

Opus 4.7 使用了全新分词器，同样文本最多比 4.6 多消耗 **35%** 的 Token。建议：
- 更新 `max_tokens`，留出更多余量
- 重新校准成本预算
- 不要依赖客户端 Token 估算，改用 `/v1/messages/count_tokens` 接口核验

---

## effort 参数说明

Opus 4.7 支持通过 `effort` 参数控制模型在响应时投入的 Token 量，在回答质量与速度/成本之间灵活权衡。`effort` 会影响文本回复、工具调用和扩展思考的全部 Token 消耗。

### 可用等级

| 等级 | 说明 | 适用场景 |
|------|------|---------|
| `low` | 高效模式，Token 消耗最少 | 简短、明确的任务；子 Agent 调用 |
| `medium` | 均衡模式，适度降低成本 | 对成本敏感、对质量要求一般的工作流 |
| `high` | 默认等级，高质量输出 | 复杂推理、高质量代码生成、Agent 任务 |
| `xhigh` | 扩展模式，深度探索 | **编程和 Agent 任务的推荐起点**；反复工具调用、深度搜索等长时间任务 |
| `max` | 最高能力，无 Token 限制 | 真正前沿级问题；大多数任务不建议使用 |

:::tip
**Opus 4.7 的推荐起点是 `xhigh`**，用于编程和 Agent 场景。`high` 适合大多数智能敏感任务。仅当 `xhigh` 的评测结果仍有明显提升空间时，才升级到 `max`。

在 `xhigh` 或 `max` 等级下，建议将 `max_tokens` 设置为 64000 以上，为模型留足思考和工具调用的空间。
:::

:::info
若在低 `effort` 下遇到复杂问题推理较浅的情况，应提高 `effort`，而非通过 Prompt 绕过。如必须保持低 `effort`，可在提示词中加入："这项任务涉及多步推理。请仔细思考后再作答。"
:::

## effort 与扩展思考

Opus 4.7 使用**自适应思考**（`thinking: {type: "adaptive"}`），`effort` 是控制思考深度的推荐方式：

- `high` / `xhigh` / `max` 等级下，模型几乎总会进行深度思考
- `low` / `medium` 等级下，简单问题可能跳过思考直接回答
- Opus 4.7 **不再支持**手动指定 `budget_tokens` 的扩展思考方式，请改用 `effort` 控制

## effort 对工具调用的影响

| effort 等级 | 工具调用行为 |
|------------|------------|
| 低（`low` / `medium`）| 合并操作，减少调用次数，直接行动，响应简洁 |
| 高（`high` / `xhigh` / `max`）| 更多工具调用，先解释计划再行动，提供详细摘要 |

## 使用建议

| 场景 | 推荐 effort | max_tokens 参考 |
|------|------------|----------------|
| 编程、Agent、复杂工具调用 | `xhigh` | 64000+ |
| 复杂推理、代码审查 | `high` | 16000+ |
| 常规工作流、翻译、摘要 | `medium` | 4096 |
| 高频分类、简单问答 | `low` | 1024 |
| 真正前沿级难题 | `max` | 64000+ |



<p align="center">
  <small>© 2026 DMXAPI Claude Opus 4.7 使用指南</small>
</p>
