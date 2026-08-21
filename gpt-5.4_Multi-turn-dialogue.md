# DMXAPI GPT-5.6 Sol 多轮对话

本页保留原有 URL 以兼容旧链接，内容已迁移到 `gpt-5.6-sol`。示例通过 DMXAPI 兼容代理的 Chat Completions 接口维护完整 `messages` 历史，实现多轮上下文。

## 接口地址

| 接口 | 请求方式 | URL |
|------|---------|-----|
| 多轮聊天补全 | POST | `https://www.dmxapi.cn/v1/chat/completions` |

:::warning API 密钥安全
示例令牌为不可用占位符。请妥善保管真实 DMXAPI 令牌，不要在公开仓库或日志中泄露。
:::

## 模型名称

- `gpt-5.6-sol`

## 多轮对话示例代码

::: code-group

```python [requests]
import requests


API_URL = "https://www.dmxapi.cn/v1/chat/completions"
API_KEY = "sk-***************************************"
MODEL = "gpt-5.6-sol"

headers = {
    "Authorization": API_KEY,
    "Content-Type": "application/json",
}
messages = [
    {"role": "system", "content": "你是一个简洁的中文助手。"}
]

for user_text in [
    "请记住：我的代号是蓝鲸。只回复收到。",
    "我的代号是什么？只回复代号。",
]:
    messages.append({"role": "user", "content": user_text})
    payload = {
        "model": MODEL,
        "messages": messages,
        "reasoning_effort": "none",
        "max_completion_tokens": 256,
    }
    response = requests.post(
        API_URL,
        headers=headers,
        json=payload,
        timeout=120,
    )
    response.raise_for_status()
    assistant_text = response.json()["choices"][0]["message"]["content"]
    messages.append({"role": "assistant", "content": assistant_text})
    print(f"用户：{user_text}")
    print(f"助手：{assistant_text}")
```

```python [SDK]
from openai import OpenAI


client = OpenAI(
    api_key="sk-***************************************",
    base_url="https://www.dmxapi.cn/v1",
)
messages = [
    {"role": "system", "content": "你是一个简洁的中文助手。"}
]

for user_text in [
    "请记住：我的代号是蓝鲸。只回复收到。",
    "我的代号是什么？只回复代号。",
]:
    messages.append({"role": "user", "content": user_text})
    response = client.chat.completions.create(
        model="gpt-5.6-sol",
        messages=messages,
        reasoning_effort="none",
        max_completion_tokens=256,
    )
    assistant_text = response.choices[0].message.content or ""
    messages.append({"role": "assistant", "content": assistant_text})
    print(f"用户：{user_text}")
    print(f"助手：{assistant_text}")
```

:::

## 返回示例

```text
用户：请记住：我的代号是蓝鲸。只回复收到。
助手：收到。
用户：我的代号是什么？只回复代号。
助手：蓝鲸
```

## 注意事项

- 每一轮都要把此前的 `user` 和 `assistant` 消息按原顺序带回。
- 对话变长时要关注上下文 token、延迟与成本；不要无限累积无关历史。
- DMXAPI 修改前实测已验证两轮上下文能正确保留“蓝鲸”代号。

<p align="center">
  <small>© 2026 DMXAPI GPT-5.6 Sol 多轮对话</small>
</p>
