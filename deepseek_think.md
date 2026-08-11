# DeepSeek 思考参数说明

思考功能允许 DeepSeek 模型在给出最终答案前，先输出一段思维链内容（`reasoning_content`），以提升最终答案的准确性。思维链内容与最终回答（`content`）同级返回。

> ⚠️ 思考模式不支持 `temperature`、`top_p`、`presence_penalty`、`frequency_penalty` 参数。为兼容已有软件，设置这些参数不会报错，但不会生效。

---

## 支持的模型

| 模型 | 说明 |
|------|------|
| `deepseek-v4-pro` | 主推思考模型，支持 `reasoning_effort` 参数 |
| `deepseek-v4-flash` | 默认非思考模式，可通过参数开启思考 |

---

## 参数说明

DeepSeek 思考功能通过两个维度控制：**思考开关**和**思考强度**。

| 功能 | OpenAI 格式 | Anthropic 格式 |
|------|-------------|----------------|
| 思考模式开关 <sup>(1)</sup> | `{"thinking": {"type": "enabled/disabled"}}` （通过 `extra_body` 传入） | 无 |
| 思考强度控制 <sup>(2)(3)</sup> | `reasoning_effort: "high/max"` （顶层参数） | `{"output_config": {"effort": "high/max"}}` |

> (1) 默认思考开关为 `enabled`
>
> (2) 普通请求默认 effort 为 `high`；复杂 Agent 类请求（如 Claude Code、OpenCode）会自动设置为 `max`
>
> (3) 出于兼容考虑，`low`、`medium` 会映射为 `high`，`xhigh` 会映射为 `max`

### 另一种思考开关写法：`enable_thinking`

除上表的 `thinking.type` 外，DMXAPI 上的 DeepSeek 系列还接受顶层布尔参数 `enable_thinking`（对齐百炼 / DashScope 风格），二者指向同一能力：

| 写法 | 开启思考 | 关闭思考 |
|------|---------|---------|
| `thinking: {"type": "enabled/disabled"}` | 可靠生效 | 可靠生效（推荐） |
| `enable_thinking: true/false` | 可靠生效 | 仅 `deepseek-v4-flash` 生效，`deepseek-v4-pro` 上被忽略 |

> 开启思考时两种写法等效；**关闭思考建议统一使用 `thinking: {"type": "disabled"}`**。请勿同时传入两者。基于 `enable_thinking` 的完整示例代码（含流式、token 用量解析）见 [DeepSeek 推理开关](/thinking-deepseek)。

### 各模型默认思考状态

| 模型 | 默认状态 |
|------|---------|
| `deepseek-v4-pro` | 默认思考，不传参数即输出 `reasoning_content` |
| `deepseek-v4-flash` | 默认不思考，需显式开启 |

> 两个模型默认行为相反，请始终显式传入思考开关，不要依赖默认值。

---

## CURL示例

```bash
curl https://www.dmxapi.cn/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer 你的DMXAPI密钥" \
  -d '{
    "model": "deepseek-v4-pro",
    "messages": [
      {
        "role": "user",
        "content": "9.11 和 9.8，哪个更大？"
      }
    ],
    "reasoning_effort": "high",
    "thinking": {
      "type": "enabled"
    }
  }'
```

---

## 多轮对话说明

- **未进行工具调用时**：上一轮的 `reasoning_content` 无需拼接到下一轮，传入会被自动忽略。
- **进行了工具调用时**：该轮产生的 `reasoning_content` 必须完整回传给 API，否则返回 400 报错。

---

## 注意事项

- 使用工具调用时，必须将每轮产生的 `reasoning_content` 完整回传给 API
- 对于简单问题，建议将 `thinking` 设为 `disabled`，以节省 token 并加快响应

---

© 2025 DMXAPI DeepSeek thinking
