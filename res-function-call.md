# OpenAI Responses API 函数调用

本页演示通过 DMXAPI 兼容代理让 `gpt-5.6-sol` 生成函数调用。模型只返回函数名和参数，真实天气查询仍需由你的程序执行。

## 接口地址

| 接口 | 请求方式 | URL |
|------|---------|-----|
| 创建函数调用 | POST | `https://www.dmxapi.cn/v1/responses` |

:::warning API 密钥安全
示例令牌为不可用占位符。请妥善保管真实 DMXAPI 令牌，不要写入公开代码或日志。
:::

## 模型名称

- `gpt-5.6-sol`

## Python 请求示例

```python
import json
import requests


url = "https://www.dmxapi.cn/v1/responses"
headers = {
    "Authorization": "sk-***************************************",
    "Content-Type": "application/json",
}
tools = [
    {
        "type": "function",
        "name": "get_current_weather",
        "description": "获取指定城市的当前天气",
        "parameters": {
            "type": "object",
            "properties": {
                "location": {
                    "type": "string",
                    "description": "城市和国家或地区",
                },
                "unit": {
                    "type": "string",
                    "enum": ["celsius", "fahrenheit"],
                },
            },
            "required": ["location", "unit"],
            "additionalProperties": False,
        },
        "strict": True,
    }
]
payload = {
    "model": "gpt-5.6-sol",
    "input": "请查询北京今天的天气。",
    "tools": tools,
    "tool_choice": "required",
    "reasoning": {"effort": "none"},
    "max_output_tokens": 256,
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
  "id": "resp_example_gpt56_tool_001",
  "object": "response",
  "status": "completed",
  "model": "gpt-5.6-sol",
  "output": [
    {
      "id": "fc_example_weather_001",
      "type": "function_call",
      "status": "completed",
      "name": "get_current_weather",
      "arguments": "{\"location\":\"北京, 中国\",\"unit\":\"celsius\"}",
      "call_id": "call_example_weather_001"
    }
  ],
  "tool_choice": "required"
}
```

## 注意事项

- `arguments` 是 JSON 字符串；反序列化后仍需按 schema、权限和业务规则再次校验。
- 收到 `function_call` 后，由应用执行真实工具，再把结果作为后续输入提交给模型。
- 本页包含 `strict: true` 的完整载荷已通过 DMXAPI 定点实测，并成功返回 `function_call`。

<p align="center">
  <small>© 2026 DMXAPI OpenAI Responses API 函数调用</small>
</p>
