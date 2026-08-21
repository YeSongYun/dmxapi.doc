# OpenAI Responses API 网络图片分析

本页演示通过 DMXAPI 兼容代理向 `gpt-5.6-sol` 传入公开图片 URL，并获取图片分析结果。

## 接口地址

| 接口 | 请求方式 | URL |
|------|---------|-----|
| 分析网络图片 | POST | `https://www.dmxapi.cn/v1/responses` |

:::warning API 密钥安全
示例令牌为不可用占位符。请妥善保管真实 DMXAPI 令牌，不要在公开代码或日志中泄露。
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
payload = {
    "model": "gpt-5.6-sol",
    "input": [
        {
            "role": "user",
            "content": [
                {"type": "input_text", "text": "请简要描述这张图片。"},
                {
                    "type": "input_image",
                    "image_url": "https://www.w3.org/Icons/w3c_home.png",
                },
            ],
        }
    ],
    "reasoning": {"effort": "none"},
    "max_output_tokens": 512,
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
  "id": "resp_example_gpt56_url_image_001",
  "object": "response",
  "status": "completed",
  "model": "gpt-5.6-sol",
  "output": [
    {
      "id": "msg_example_gpt56_url_image_001",
      "type": "message",
      "status": "completed",
      "role": "assistant",
      "content": [
        {
          "type": "output_text",
          "text": "图片中是蓝色的 W3C 标志。",
          "annotations": []
        }
      ]
    }
  ]
}
```

## 注意事项

- 图片 URL 必须能被服务端公开访问，不能依赖本地登录态或临时浏览器会话。
- 生产环境应校验 URL 来源、文件类型和大小，避免服务端请求伪造风险。
- 本页已使用同一请求结构通过 DMXAPI 实测；图片内容不同会产生不同回答。

<p align="center">
  <small>© 2026 DMXAPI OpenAI Responses API 网络图片分析</small>
</p>
