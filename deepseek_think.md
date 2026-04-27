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

---

## 示例

```bash
curl https://www.dmxapi.cn/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $DMXAPI_KEY" \
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
