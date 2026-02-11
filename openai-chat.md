# OpenAI API 请求格式（非流式输出）

## 📌 接口地址

```
https://www.dmxapi.cn/v1/chat/completions
```

## 📖 使用方法

只需替换 `model` 参数为您需要的模型名称即可。

---

## 方法一：Requests 库 python调用示例

```python
"""
DMXAPI 对话接口调用示例
功能：使用 GPT-5-mini 模型进行智能对话
"""

import json
import requests

# ==================== API 配置 ====================

# API 接口地址
url = "https://www.dmxapi.cn/v1/chat/completions"

# 请求头配置
headers = {
    "Authorization": "sk-**********************************",  # 替换为你的 DMXAPI 令牌
    "Content-Type": "application/json"
}

# ==================== 请求参数 ====================

# 构造请求数据
payload = {
    "model": "DeepSeek-V3.2-Fast",  # 选择使用的模型
    "messages": [
        {
            "role": "system", 
            "content": "You are a helpful assistant."  # 系统提示词：定义 AI 助手的角色
        },
        {
            "role": "user", 
            "content": "介绍下鲁迅"  # 用户问题
        }
    ]
}

# ==================== 发送请求 ====================

try:
    # 发送 POST 请求到 API
    response = requests.post(url, headers=headers, data=json.dumps(payload))
    response.raise_for_status()  # 检查 HTTP 错误
    
    # 输出响应结果
    print("=" * 50)
    print("API 响应结果：")
    print("=" * 50)
    print(json.dumps(response.json(), indent=2, ensure_ascii=False))
    
except requests.exceptions.RequestException as e:
    # 异常处理
    print(f"❌ 请求失败: {e}")

```

### 📥 返回示例
```json
==================================================
API 响应结果：
==================================================
{
  "choices": [
    {
      "finish_reason": "stop",
      "index": 0,
      "logprobs": null,
      "message": {
        "annotations": [],
        "content": "不是。周树人就是鲁迅本人。鲁迅是他的笔名（本名周树人，生卒年1881—1936），因此两者不是兄弟，而是同一人。",
        "refusal": null,
        "role": "assistant"
      }
    }
  ],
  "created": 1762512287,
  "id": "chatcmpl-CZEFTZKtwzH7x5Dgiliucuc7qIzfg",
  "model": "gpt-5-mini-2025-08-07",
  "object": "chat.completion",
  "system_fingerprint": null,
  "usage": {
    "completion_tokens": 502,
    "completion_tokens_details": {
      "accepted_prediction_tokens": 0,
      "audio_tokens": 0,
      "reasoning_tokens": 448,
      "rejected_prediction_tokens": 0
    },
    "prompt_tokens": 27,
    "prompt_tokens_details": {
      "audio_tokens": 0,
      "cached_tokens": 0
    },
    "total_tokens": 529
  }
}
```

---

## 方法二：OpenAI 官方 SDK python调用示例

```python
"""
DMXAPI OpenAI SDK 调用示例
功能：使用 OpenAI 官方 SDK 调用 DMXAPI 接口进行对话
"""

from openai import OpenAI
import json

# ==================== 客户端初始化 ====================

# 创建 OpenAI 客户端实例
client = OpenAI(
    api_key="sk-**************************************",  # 替换为你的 DMXAPI 令牌
    base_url="https://www.dmxapi.cn/v1"  # DMXAPI 接口地址
)

# ==================== 发送对话请求 ====================

# 调用对话完成接口
chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "user",  # 用户角色
            "content": "周树人和鲁迅是兄弟吗？"  # 用户提问
        }
    ],
    model="gpt-5-mini"  # 指定使用的模型
)

# ==================== 格式化输出结果 ====================

# 将响应对象转换为字典
result = chat_completion.model_dump()

# 美化输出
print("=" * 50)
print("✨ API 响应结果")
print("=" * 50)
print(json.dumps(result, indent=2, ensure_ascii=False))
print("=" * 50)

# 输出关键信息摘要
print("📊 关键信息摘要：")
print(f"  • 模型: {result['model']}")
print(f"  • 回复: {result['choices'][0]['message']['content']}")
print(f"  • Token 使用: {result['usage']['total_tokens']} (输入: {result['usage']['prompt_tokens']}, 输出: {result['usage']['completion_tokens']})")
```

### 📥 返回示例
```json
==================================================
✨ API 响应结果
==================================================
{
  "id": "chatcmpl-CZEGlYYxCrQ7JBt8fefXKBJ2MnIfJ",
  "choices": [
    {
      "finish_reason": "stop",
      "index": 0,
      "logprobs": null,
      "message": {
        "content": "不是。周树人就是鲁迅的本名，鲁迅是他的笔名，所以两者是同一个人，不是兄弟。鲁迅（本名周树人，1881–1936）是中国现代著名作家。（他的弟弟是周作人。）",
        "refusal": null,
        "role": "assistant",
        "annotations": [],
        "audio": null,
        "function_call": null,
        "tool_calls": null
      }
    }
  ],
  "created": 1762512367,
  "model": "gpt-5-mini-2025-08-07",
  "object": "chat.completion",
  "service_tier": null,
  "system_fingerprint": null,
  "usage": {
    "completion_tokens": 392,
    "prompt_tokens": 17,
    "total_tokens": 409,
    "completion_tokens_details": {
      "accepted_prediction_tokens": 0,
      "audio_tokens": 0,
      "reasoning_tokens": 320,
      "rejected_prediction_tokens": 0
    },
    "prompt_tokens_details": {
      "audio_tokens": 0,
      "cached_tokens": 0
    }
  }
}
==================================================
📊 关键信息摘要：
  • 模型: gpt-5-mini-2025-08-07
  • 回复: 不是。周树人就是鲁迅的本名，鲁迅是他的笔名，所以两者是同一个人，不是兄弟。鲁迅（本名周树人，1881–1936）是中国现代著名作家。（他的弟弟是周作人。）
  • Token 使用: 409 (输入: 17, 输出: 392)
```


## ⚠️ 注意事项

1. **API Key 安全**：请妥善保管 API Key,不要泄露
2. **HTTPS 协议**：所有请求必须通过 HTTPS 发送
3. **响应格式**:响应格式为 JSON

---

<p align="center">
  <small>© 2025 DMXAPI OpenAI Chat</small>
</p>