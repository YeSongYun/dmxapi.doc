# OpenAI Chat Completions 流式调用

本页演示通过 DMXAPI 兼容代理调用 `gpt-5.6-sol` 的 Chat Completions 流式接口，并从 `text/event-stream` 响应中提取 `choices[].delta.content`。

## 接口地址

| 接口 | 请求方式 | URL |
|------|---------|-----|
| 创建流式聊天补全 | POST | `https://www.dmxapi.cn/v1/chat/completions` |

:::warning API 密钥安全
示例中的令牌为不可用占位符。请勿在浏览器端或公开代码中保存、泄露真实 DMXAPI 令牌。
:::

## 模型名称

- `gpt-5.6-sol`

## Python 请求示例

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
        {"role": "user", "content": "周树人和鲁迅是兄弟吗？"}
    ],
    "reasoning_effort": "none",
    "max_completion_tokens": 256,
    "stream": True,
}

response = requests.post(
    url,
    headers=headers,
    json=payload,
    stream=True,
    timeout=120,
)
response.raise_for_status()

for raw_line in response.iter_lines():
    if not raw_line:
        continue

    # 先按字节切出完整行，再统一按 UTF-8 解码，避免中文被拆成半截 JSON。
    line = raw_line.decode("utf-8")
    if not line.startswith("data: "):
        continue

    event_data = line[6:]
    if event_data == "[DONE]":
        break

    event = json.loads(event_data)
    # 某些流式元数据块的 choices 为空，解析前必须检查。
    choices = event.get("choices") or []
    if not choices:
        continue

    content = choices[0].get("delta", {}).get("content")
    if content:
        print(content, end="", flush=True)

print()
```

## 返回示例

```text
data: {"id":"chatcmpl_example_stream_001","model":"gpt-5.6-sol-2026-07-09","choices":[{"index":0,"delta":{"content":"不是。"}}]}

data: {"id":"chatcmpl_example_stream_001","model":"gpt-5.6-sol-2026-07-09","choices":[{"index":0,"delta":{"content":"周树人和鲁迅是同一个人。"}}]}

data: [DONE]
```

## 注意事项

- DMXAPI 实测流中会出现 `choices: []` 的元数据块；不要直接访问 `choices[0]`。
- 文本增量位于 `choices[0].delta.content`，结束标记为 `data: [DONE]`。
- 网络层使用 `stream=True`，请求体也必须包含 `"stream": true`。

<p align="center">
  <small>© 2026 DMXAPI OpenAI Chat Completions 流式调用</small>
</p>
