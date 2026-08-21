# OpenAI Chat Completions 函数调用

本页演示通过 DMXAPI 兼容代理让 `gpt-5.6-sol` 返回函数调用参数。模型只负责选择工具并生成参数，真实天气查询仍需由你的程序执行。

## 接口地址

| 接口 | 请求方式 | URL |
|------|---------|-----|
| 创建函数调用 | POST | `https://www.dmxapi.cn/v1/chat/completions` |

:::warning API 密钥安全
示例令牌为不可用占位符。请妥善保管真实 DMXAPI 令牌，不要写入公开代码或日志。
:::

## 模型名称

- `gpt-5.6-sol`

## Python 请求示例

```python
import json
import requests


url = "https://www.dmxapi.cn/v1/chat/completions"
payload = {
    "model": "gpt-5.6-sol",
    "messages": [
        {"role": "user", "content": "请查询上海今天的天气。"}
    ],
    # DMXAPI 已实测 tools 与 reasoning_effort=none 可组合使用。
    "reasoning_effort": "none",
    "max_completion_tokens": 256,
    "tools": [
        {
            "type": "function",
            "function": {
                "name": "get_current_weather",
                "description": "获取指定城市的当前天气",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "location": {
                            "type": "string",
                            "description": "城市和国家或地区"
                        },
                        "unit": {
                            "type": "string",
                            "enum": ["celsius", "fahrenheit"]
                        }
                    },
                    "required": ["location"],
                    "additionalProperties": False
                }
            }
        }
    ],
    "tool_choice": "required"
}
headers = {
    "Authorization": "sk-***************************************",
    "Content-Type": "application/json",
}

response = requests.post(
    url,
    headers=headers,
    json=payload,
    timeout=120,
)
response.raise_for_status()
result = response.json()
print(json.dumps(result, indent=2, ensure_ascii=False))
```

## 返回示例

```json
{
  "id": "chatcmpl_example_gpt56_tool_001",
  "object": "chat.completion",
  "created": 1787270400,
  "model": "gpt-5.6-sol-2026-07-09",
  "choices": [
    {
      "index": 0,
      "message": {
        "role": "assistant",
        "content": null,
        "tool_calls": [
          {
            "id": "call_example_weather_001",
            "type": "function",
            "function": {
              "name": "get_current_weather",
              "arguments": "{\"location\":\"上海, 中国\",\"unit\":\"celsius\"}"
            }
          }
        ]
      },
      "finish_reason": "tool_calls"
    }
  ]
}
```

## 注意事项

- DMXAPI 修改前实测中，省略 `reasoning_effort` 和显式设置 `none` 均能返回 `tool_calls`；本页显式使用 `none`，使行为更可控。
- 如果工作流需要模型推理、执行工具并继续多轮处理，优先使用 Responses API。
- 不要直接信任模型生成的函数参数；执行工具前应做 schema 校验、权限检查和输入过滤。

<p align="center">
  <small>© 2026 DMXAPI OpenAI Chat Completions 函数调用</small>
</p>
