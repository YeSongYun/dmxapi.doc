# OpenAI Responses API 文件分析

本页演示通过 DMXAPI 兼容代理把公开 PDF 文件 URL 传给 `gpt-5.6-sol`，并让模型读取文件内容。

## 接口地址

| 接口 | 请求方式 | URL |
|------|---------|-----|
| 分析文件 | POST | `https://www.dmxapi.cn/v1/responses` |

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
payload = {
    "model": "gpt-5.6-sol",
    "input": [
        {
            "role": "user",
            "content": [
                {
                    "type": "input_file",
                    "file_url": "https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf",
                },
                {
                    "type": "input_text",
                    "text": "只回复这份文档的标题。",
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
    timeout=180,
)
response.raise_for_status()
result = response.json()
print(json.dumps(result, indent=2, ensure_ascii=False))
```

## 返回示例

```json
{
  "id": "resp_example_gpt56_file_001",
  "object": "response",
  "status": "completed",
  "model": "gpt-5.6-sol",
  "output": [
    {
      "id": "msg_example_gpt56_file_001",
      "type": "message",
      "status": "completed",
      "role": "assistant",
      "content": [
        {
          "type": "output_text",
          "text": "Dummy PDF file",
          "annotations": []
        }
      ]
    }
  ]
}
```

## 注意事项

- 文件 URL 必须能被服务端直接访问，且响应内容应与声明的文件类型一致。
- 大文件会增加处理时间与 token 消耗；生产环境应限制文件大小、来源和类型。
- 本页公开 PDF、标题提取提示词和返回结构均已通过 DMXAPI 实测；模型措辞可能略有差异。

<p align="center">
  <small>© 2026 DMXAPI OpenAI Responses API 文件分析</small>
</p>
