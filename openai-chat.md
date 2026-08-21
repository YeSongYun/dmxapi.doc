# OpenAI Chat Completions 非流式调用

本页演示通过 DMXAPI 兼容代理的 Chat Completions 接口调用 `gpt-5.6-sol`，分别提供 OpenAI Python SDK 与 `requests` 写法。

## 接口地址

| 接口 | 请求方式 | URL |
|------|---------|-----|
| 创建聊天补全 | POST | `https://www.dmxapi.cn/v1/chat/completions` |

:::warning API 密钥安全
请使用自己的 DMXAPI 令牌替换占位符，并通过服务端环境变量管理真实令牌；不要泄露令牌。
:::

## 模型名称

- `gpt-5.6-sol`

## 调用示例

::: code-group

```python [SDK]
import json

from openai import OpenAI


client = OpenAI(
    api_key="sk-***************************************",
    base_url="https://www.dmxapi.cn/v1",
)

response = client.chat.completions.create(
    model="gpt-5.6-sol",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "请简单介绍鲁迅。"},
    ],
    reasoning_effort="none",
    max_completion_tokens=256,
)

print(json.dumps(response.model_dump(), indent=2, ensure_ascii=False))
```

```python [requests]
import json

import requests


url = "https://www.dmxapi.cn/v1/chat/completions"
headers = {
    "Authorization": "sk-***************************************",
    "Content-Type": "application/json",
}
payload = {
    "model": "gpt-5.6-sol",
    "messages": [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "请简单介绍鲁迅。"},
    ],
    "reasoning_effort": "none",
    "max_completion_tokens": 256,
}

response = requests.post(url, headers=headers, json=payload, timeout=120)
response.raise_for_status()
print(json.dumps(response.json(), indent=2, ensure_ascii=False))
```

:::

## 返回示例

```json
{
  "id": "chatcmpl_example_gpt56_nonstream_001",
  "object": "chat.completion",
  "created": 1787270400,
  "model": "gpt-5.6-sol-2026-07-09",
  "choices": [
    {
      "index": 0,
      "message": {
        "role": "assistant",
        "content": "鲁迅，原名周树人，是中国现代文学的重要作家，代表作包括《狂人日记》《阿Q正传》等。"
      },
      "finish_reason": "stop"
    }
  ]
}
```

## 注意事项

- GPT-5.6 官方默认推理强度为 `medium`；本页使用 `none` 作为普通问答的低延迟示例。
- Chat Completions 的推理字段是 `reasoning_effort`；Responses API 使用嵌套的 `reasoning.effort`。
- DMXAPI 实测的 Chat Completions 响应模型名为版本化快照 `gpt-5.6-sol-2026-07-09`。

<p align="center">
  <small>© 2026 DMXAPI OpenAI Chat Completions 非流式调用</small>
</p>
