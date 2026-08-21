# OpenAI Responses API 非流式调用

本页演示通过 DMXAPI 的 OpenAI 兼容 Responses API 调用 `gpt-5.6-sol`，分别给出 OpenAI Python SDK 与 `requests` 两种非流式写法。为保持普通问答的低延迟基线，示例显式设置 `reasoning.effort` 为 `none`。

## 接口地址

| 接口 | 请求方式 | URL |
|------|---------|-----|
| 创建响应 | POST | `https://www.dmxapi.cn/v1/responses` |

:::warning API 密钥安全
请将示例中的占位符替换为自己的 DMXAPI 令牌。不要把真实令牌提交到代码仓库、前端代码或公开日志中。
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

response = client.responses.create(
    # 【model】(string, 必填) 本示例固定调用 GPT-5.6 Sol。
    model="gpt-5.6-sol",
    # 【input】(string, 必填) 用户输入内容。
    input="请用一句话解释什么是 API。",
    # 【reasoning.effort】(string, 可选) 设为 none 以保持低延迟。
    reasoning={"effort": "none"},
    # 【max_output_tokens】(integer, 可选) 限制本次输出长度。
    max_output_tokens=256,
)

print(json.dumps(response.model_dump(), indent=2, ensure_ascii=False))
```

```python [requests]
import json

import requests


url = "https://www.dmxapi.cn/v1/responses"
api_key = "sk-***************************************"

headers = {
    "Authorization": api_key,
    "Content-Type": "application/json",
}

payload = {
    # 【model】(string, 必填) 本示例固定调用 GPT-5.6 Sol。
    "model": "gpt-5.6-sol",
    # 【input】(string, 必填) 用户输入内容。
    "input": "请用一句话解释什么是 API。",
    # 【reasoning.effort】(string, 可选) 设为 none 以保持低延迟。
    "reasoning": {"effort": "none"},
    # 【max_output_tokens】(integer, 可选) 限制本次输出长度。
    "max_output_tokens": 256,
}

response = requests.post(url, headers=headers, json=payload, timeout=120)
response.raise_for_status()
print(json.dumps(response.json(), indent=2, ensure_ascii=False))
```

:::

## 返回示例

以下响应结构依据 DMXAPI 实测结果整理，响应 ID 与时间戳已替换为虚构值：

```json
{
  "id": "resp_example_gpt56_nonstream_001",
  "object": "response",
  "created_at": 1787270400,
  "status": "completed",
  "model": "gpt-5.6-sol",
  "output": [
    {
      "id": "msg_example_gpt56_nonstream_001",
      "type": "message",
      "status": "completed",
      "content": [
        {
          "type": "output_text",
          "annotations": [],
          "text": "API 是一组让不同软件按照约定互相请求数据或功能的接口规则。"
        }
      ],
      "role": "assistant"
    }
  ],
  "reasoning": {
    "effort": "none"
  },
  "usage": {
    "input_tokens": 17,
    "output_tokens": 28,
    "total_tokens": 45
  }
}
```

## 注意事项

- GPT-5.6 官方默认推理强度为 `medium`；本页主动设置为 `none`，用于普通低延迟问答。
- 需要工具调用、多轮状态或 GPT-5.6 新能力时，优先继续使用 Responses API。
- 文本结果位于 `output` 数组中 `type` 为 `message` 的项目内；SDK 可直接读取 `response.output_text`。
- DMXAPI 代理请求地址与 OpenAI 上游原生地址不同，请保留本页的 DMXAPI Base URL。

<p align="center">
  <small>© 2026 DMXAPI OpenAI Responses 非流式调用</small>
</p>
