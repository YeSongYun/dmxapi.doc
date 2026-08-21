# OpenAI Responses API 本地图片分析

本页演示将本地图片编码为 Base64 Data URL，再通过 DMXAPI 兼容代理交给 `gpt-5.6-sol` 分析。

## 接口地址

| 接口 | 请求方式 | URL |
|------|---------|-----|
| 分析本地图片 | POST | `https://www.dmxapi.cn/v1/responses` |

:::warning API 密钥安全
示例令牌为不可用占位符。请妥善保管真实 DMXAPI 令牌，不要写入公开仓库或日志。
:::

## 模型名称

- `gpt-5.6-sol`

## Python 请求示例

```python
import base64
import json
import mimetypes
from pathlib import Path

import requests


image_path = Path("C:/path/to/example.png")
mime_type = mimetypes.guess_type(image_path.name)[0] or "image/png"
image_base64 = base64.b64encode(image_path.read_bytes()).decode("ascii")
image_data_url = f"data:{mime_type};base64,{image_base64}"

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
                {"type": "input_image", "image_url": image_data_url},
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
  "id": "resp_example_gpt56_base64_image_001",
  "object": "response",
  "status": "completed",
  "model": "gpt-5.6-sol",
  "output": [
    {
      "id": "msg_example_gpt56_base64_image_001",
      "type": "message",
      "status": "completed",
      "role": "assistant",
      "content": [
        {
          "type": "output_text",
          "text": "图片中包含一组清晰可见的图形和文字元素。",
          "annotations": []
        }
      ]
    }
  ]
}
```

## 注意事项

- Data URL 格式必须是 `data:<MIME>;base64,<内容>`。
- Base64 会增加请求体积；大文件应优先使用可访问的 URL 或文件上传方案。
- 不要读取不受信任的任意文件路径，生产环境应限制格式、大小和来源。

<p align="center">
  <small>© 2026 DMXAPI OpenAI Responses API 本地图片分析</small>
</p>
