# OpenAI Responses API 流式调用

本页演示通过 DMXAPI 兼容代理流式调用 `gpt-5.6-sol`，并处理 `response.output_text.delta` 事件。

## 接口地址

| 接口 | 请求方式 | URL |
|------|---------|-----|
| 创建流式响应 | POST | `https://www.dmxapi.cn/v1/responses` |

:::warning API 密钥安全
示例令牌为不可用占位符。请妥善保管真实 DMXAPI 令牌，不要写入公开仓库、前端代码或日志。
:::

## 模型名称

- `gpt-5.6-sol`

## Python 请求示例

::: code-group

```python [SDK]
from openai import OpenAI


client = OpenAI(
    api_key="sk-***************************************",
    base_url="https://www.dmxapi.cn/v1",
)

stream = client.responses.create(
    model="gpt-5.6-sol",
    input="用一句话介绍上海。",
    reasoning={"effort": "none"},
    max_output_tokens=256,
    stream=True,
)

for event in stream:
    if event.type == "response.output_text.delta":
        print(event.delta, end="", flush=True)
print()
```

```python [requests]
import json
import requests


url = "https://www.dmxapi.cn/v1/responses"
headers = {
    "Authorization": "sk-***************************************",
    "Content-Type": "application/json",
}
payload = {
    "model": "gpt-5.6-sol",
    "input": "用一句话介绍上海。",
    "reasoning": {"effort": "none"},
    "max_output_tokens": 256,
    "stream": True,
}

with requests.post(
    url,
    headers=headers,
    json=payload,
    stream=True,
    timeout=120,
) as response:
    response.raise_for_status()
    current_event = ""
    for raw_line in response.iter_lines():
        # 先按字节切出完整行，再统一按 UTF-8 解码，避免中文被拆成半截 JSON。
        line = raw_line.decode("utf-8").strip() if raw_line else ""
        if line.startswith("event:"):
            current_event = line[6:].strip()
        elif line.startswith("data:"):
            data = line[5:].strip()
            if data == "[DONE]":
                break
            if current_event == "response.output_text.delta":
                event_data = json.loads(data)
                print(event_data.get("delta", ""), end="", flush=True)
        elif not line:
            current_event = ""
print()
```

:::

## 返回示例

流式响应使用 SSE。下面仅展示文本增量事件；实际响应还会包含创建、完成等生命周期事件。

```text
event: response.output_text.delta
data: {"type":"response.output_text.delta","item_id":"msg_example_001","output_index":0,"content_index":0,"delta":"上海是一座融合现代都市活力与深厚海派文化的国际化城市。"}

event: response.completed
data: {"type":"response.completed","response":{"id":"resp_example_gpt56_stream_001","status":"completed","model":"gpt-5.6-sol"}}
```

## 注意事项

- SDK 已封装 SSE；直接使用 HTTP 时，要同时解析 `event:` 和 `data:` 行。
- 每个事件由空行分隔，文本增量只处理 `response.output_text.delta`。
- 本页显式设置 `reasoning.effort` 为 `none` 以降低简单任务延迟；模型默认值是 `medium`。

<p align="center">
  <small>© 2026 DMXAPI OpenAI Responses API 流式调用</small>
</p>
