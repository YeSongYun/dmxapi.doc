# GPT-5.6 Sol 推理摘要

本页演示通过 DMXAPI 兼容代理请求 `gpt-5.6-sol` 的推理摘要。`reasoning.summary` 返回的是模型生成的摘要，不是完整、逐字的内部思维链。

## 接口地址

| 接口 | 请求方式 | URL |
|------|---------|-----|
| 创建带推理摘要的响应 | POST | `https://www.dmxapi.cn/v1/responses` |

:::warning API 密钥安全
示例令牌为不可用占位符。请妥善保管真实 DMXAPI 令牌，不要在公开仓库或日志中泄露。
:::

## 模型与参数

- 模型：`gpt-5.6-sol`
- 推理强度：`none`、`low`、`medium`、`high`、`xhigh`、`max`
- 默认推理强度：`medium`
- 推理摘要：`reasoning.summary` 设置为 `auto`

## 请求示例

::: code-group

```python [SDK]
from openai import OpenAI


client = OpenAI(
    api_key="sk-***************************************",
    base_url="https://www.dmxapi.cn/v1",
)

response = client.responses.create(
    model="gpt-5.6-sol",
    input="比较归并排序和快速排序，并说明各自更适合的场景。",
    reasoning={"effort": "low", "summary": "auto"},
    max_output_tokens=512,
)

for item in response.output:
    if item.type == "reasoning":
        for summary in item.summary:
            print("【推理摘要】", summary.text)
    elif item.type == "message":
        for content in item.content:
            if content.type == "output_text":
                print("【最终回答】", content.text)
```

```python [requests]
import requests


url = "https://www.dmxapi.cn/v1/responses"
headers = {
    "Authorization": "sk-***************************************",
    "Content-Type": "application/json",
}
payload = {
    "model": "gpt-5.6-sol",
    "input": "比较归并排序和快速排序，并说明各自更适合的场景。",
    "reasoning": {"effort": "low", "summary": "auto"},
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

for item in result.get("output", []):
    if item.get("type") == "reasoning":
        for summary in item.get("summary", []):
            print("【推理摘要】", summary.get("text", ""))
    elif item.get("type") == "message":
        for content in item.get("content", []):
            if content.get("type") == "output_text":
                print("【最终回答】", content.get("text", ""))
```

```shell [cURL]
curl -X POST https://www.dmxapi.cn/v1/responses \
  -H "Content-Type: application/json" \
  -H "Authorization: sk-***************************************" \
  --json '{
    "model": "gpt-5.6-sol",
    "input": "比较归并排序和快速排序，并说明各自更适合的场景。",
    "reasoning": {"effort": "low", "summary": "auto"},
    "max_output_tokens": 512
  }'
```

:::

## 返回示例

```json
{
  "id": "resp_example_gpt56_reasoning_001",
  "object": "response",
  "status": "completed",
  "model": "gpt-5.6-sol",
  "output": [
    {
      "id": "rs_example_gpt56_reasoning_001",
      "type": "reasoning",
      "summary": [
        {
          "type": "summary_text",
          "text": "比较两种算法的时间复杂度、稳定性、额外空间与典型使用场景。"
        }
      ]
    },
    {
      "id": "msg_example_gpt56_reasoning_001",
      "type": "message",
      "status": "completed",
      "role": "assistant",
      "content": [
        {
          "type": "output_text",
          "text": "归并排序稳定且最坏时间复杂度为 O(n log n)，适合外部排序和要求稳定性的场景；快速排序通常原地且平均性能优秀，适合内存中的通用排序。",
          "annotations": []
        }
      ]
    }
  ]
}
```

## 注意事项

- 即使设置 `summary: auto`，返回的 `summary` 仍可能为空；代码必须兼容该情况。
- DMXAPI 实测中，较复杂请求在 `low`、`medium` 和 `high` 下均能返回推理项，但摘要是否出现会随请求和调用而变化。
- 推理 token 会计入输出用量；应根据准确性、延迟和成本选择强度。
- OpenAI 上游模型说明与最新模型指南分别见：<https://developers.openai.com/api/docs/models/gpt-5.6-sol>、<https://developers.openai.com/api/docs/guides/latest-model>。

<p align="center">
  <small>© 2026 DMXAPI GPT-5.6 Sol 推理摘要</small>
</p>
