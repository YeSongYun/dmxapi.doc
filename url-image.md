# OpenAI Chat Completions 网络图片分析

本页演示通过 DMXAPI 兼容代理调用 `gpt-5.6-sol`，使用 Chat Completions 的 `image_url` 内容项分析公网图片。该请求形状已通过 DMXAPI 实测。

## 接口地址

| 接口 | 请求方式 | URL |
|------|---------|-----|
| 分析网络图片 | POST | `https://www.dmxapi.cn/v1/chat/completions` |

:::warning API 密钥安全
示例令牌为不可用占位符。请妥善保管真实 DMXAPI 令牌，不要提交到公开仓库或日志。
:::

## 模型名称

- `gpt-5.6-sol`

## Python 调用示例

```python
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
        {
            "role": "user",
            "content": [
                {"type": "text", "text": "请简要描述这张图片。"},
                {
                    "type": "image_url",
                    "image_url": {
                        "url": "https://www.w3.org/Icons/w3c_home.png"
                    },
                },
            ],
        }
    ],
    "reasoning_effort": "none",
    "max_completion_tokens": 512,
}

response = requests.post(url, headers=headers, json=payload, timeout=120)
response.raise_for_status()
result = response.json()
print(json.dumps(result, indent=2, ensure_ascii=False))
print(result["choices"][0]["message"]["content"])
```

## 返回示例

```json
{
  "id": "chatcmpl_example_gpt56_image_url_001",
  "object": "chat.completion",
  "created": 1787270400,
  "model": "gpt-5.6-sol-2026-07-09",
  "choices": [
    {
      "index": 0,
      "message": {
        "role": "assistant",
        "content": "图片中是蓝色的 W3C 标志。"
      },
      "finish_reason": "stop"
    }
  ]
}
```

## 注意事项

- `image_url.url` 必须是模型服务可访问的公网图片直链。
- GPT-5.6 支持图片输入、文本输出；本页不涉及图片生成。
- 对票据、证件等重要内容的模型识别结果应由业务系统再次核验。

<p align="center">
  <small>© 2026 DMXAPI OpenAI 网络图片分析</small>
</p>
