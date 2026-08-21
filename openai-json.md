# OpenAI Chat Completions 结构化 JSON 输出

本页使用 OpenAI Python SDK 的结构化输出解析功能，通过 DMXAPI 兼容代理调用 `gpt-5.6-sol`，并将结果校验为 Pydantic 模型。

## 接口地址

| 接口 | 请求方式 | URL |
|------|---------|-----|
| 创建结构化聊天补全 | POST | `https://www.dmxapi.cn/v1/chat/completions` |

:::warning API 密钥安全
请使用自己的 DMXAPI 令牌替换占位符。不要把真实令牌写进公开仓库或日志。
:::

## 模型名称

- `gpt-5.6-sol`

## Python 示例代码

```python
import json

from openai import OpenAI
from pydantic import BaseModel


class ProductInfo(BaseModel):
    product_name: str
    price: float
    description: str


client = OpenAI(
    api_key="sk-***************************************",
    base_url="https://www.dmxapi.cn/v1",
)

completion = client.beta.chat.completions.parse(
    model="gpt-5.6-sol",
    messages=[
        {
            "role": "system",
            "content": "从用户描述中提取产品名称、价格和简短描述。",
        },
        {
            "role": "user",
            "content": "一台 75 寸电视，价格 4999 元，适合客厅观影。",
        },
    ],
    reasoning_effort="none",
    max_completion_tokens=512,
    response_format=ProductInfo,
)

parsed = completion.choices[0].message.parsed
if parsed is None:
    raise ValueError("模型未返回符合 ProductInfo 的结构化结果。")

print(json.dumps(parsed.model_dump(), indent=2, ensure_ascii=False))
```

## 返回示例

```json
{
  "product_name": "75 寸电视",
  "price": 4999.0,
  "description": "适合客厅观影的大屏电视。"
}
```

## 注意事项

- 本页使用 SDK 的 `response_format=ProductInfo` 生成并校验结构化输出。
- DMXAPI 已实测 `gpt-5.6-sol` 可完成该 `client.beta.chat.completions.parse(...)` 调用。
- 生产环境仍应处理拒答、解析为空、超时和 HTTP 错误。

<p align="center">
  <small>© 2026 DMXAPI OpenAI 结构化 JSON 输出</small>
</p>
