# OpenAI Chat Completions 本地图片分析

本页演示将本地图片编码为 Base64 数据 URI，再通过 DMXAPI 兼容代理的 Chat Completions 接口交给 `gpt-5.6-sol` 分析。该请求形状已通过 DMXAPI 实测。

## 接口地址

| 接口 | 请求方式 | URL |
|------|---------|-----|
| 分析本地图片 | POST | `https://www.dmxapi.cn/v1/chat/completions` |

:::warning API 密钥安全
示例中的令牌为不可用占位符。请妥善保管真实 DMXAPI 令牌，不要在客户端或日志中泄露。
:::

## 模型名称

- `gpt-5.6-sol`

## Python 调用示例

```python
import base64
import json
import mimetypes
from pathlib import Path

import requests


def encode_image(image_path: str) -> str:
    path = Path(image_path)
    mime_type = mimetypes.guess_type(path.name)[0] or "image/png"
    encoded = base64.b64encode(path.read_bytes()).decode("ascii")
    return f"data:{mime_type};base64,{encoded}"


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
                {
                    "type": "text",
                    "text": "图片顶部红框中的中文标题是什么？只回复标题。",
                },
                {
                    "type": "image_url",
                    "image_url": {
                        "url": encode_image("C:/path/to/example.png")
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
  "id": "chatcmpl_example_gpt56_base64_image_001",
  "object": "chat.completion",
  "created": 1787270400,
  "model": "gpt-5.6-sol-2026-07-09",
  "choices": [
    {
      "index": 0,
      "message": {
        "role": "assistant",
        "content": "推理强度控制"
      },
      "finish_reason": "stop"
    }
  ]
}
```

## 注意事项

- Base64 会增加请求体积；大图应关注上传时间、输入 token 与超时设置。
- 本页示例图片应包含“推理强度控制”标题；确定性问题便于验证模型确实读取了图片内容。
- 数据 URI 的 MIME 类型应与实际图片格式一致。
- 本地路径仅由客户端读取，不会作为路径字符串直接发送给模型。
- 二次验收中，仅替换为 `deepseek-v4-flash-0731` 会返回 HTTP 400、错误码 10305；该模型不适用于本页图片输入。

<p align="center">
  <small>© 2026 DMXAPI OpenAI 本地图片分析</small>
</p>
