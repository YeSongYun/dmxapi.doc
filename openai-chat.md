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
功能：使用 DeepSeek-V3.2-Fast 模型进行智能对话
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
    "model": "deepseek-v4-flash",  # 选择使用的模型
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
        "content": "鲁迅（1881年9月25日－1936年10月19日），原名周树人，字豫才，浙江绍兴人，是中国现代文学的奠基人之一、著名文学家、思想家、革命家。他以犀利的笔锋揭露旧社会的黑暗与国民性的弱点，被誉为“民族魂”。代表作品包括中国第一篇现代白话小说《狂人日记》，以及小说集《呐喊》《彷徨》、散文集《朝花夕拾》、散文诗集《野草》、杂文集《坟》《热风》等。其作品深刻影响了中国现代文学和思想的发展。",
        "reasoning_content": "我们被问到“介绍下鲁迅”。这是一个中文问题，需要提供关于鲁迅的简介。鲁迅是中国现代文学的重要人物，原名周树人。我们需要给出一个简明扼要的介绍，包括他的生卒、主要成就、代表作品、文学地位等。使用中文回答。",
        "role": "assistant"
      }
    }
  ],
  "created": 1781774236,
  "id": "chatcmpl-3eaf7cfa-cc25-9fde-a77a-89abe3d07a53",
  "model": "deepseek-v4-flash",
  "object": "chat.completion",
  "system_fingerprint": null,
  "usage": {
    "completion_tokens": 181,
    "completion_tokens_details": {
      "reasoning_tokens": 57
    },
    "prompt_tokens": 13,
    "prompt_tokens_details": {
      "cached_tokens": 0
    },
    "total_tokens": 194
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
    model= "deepseek-v4-flash"  # 指定使用的模型
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
  "id": "chatcmpl-bfd8742b-34e6-9953-92d1-a49066669e7a",
  "choices": [
    {
      "finish_reason": "stop",
      "index": 0,
      "logprobs": null,
      "message": {
        "content": "不是的。**周树人和鲁迅是同一个人**。\n\n鲁迅（1881年9月25日－1936年10月19日），原名**周樟寿**，后改名**周树人**，“鲁迅”是他1918年发表《狂人日记》时开始使用的笔名。因此，周树人是鲁迅的本名，他们是同一人，而非兄弟关系。",
        "refusal": null,
        "role": "assistant",
        "annotations": null,
        "audio": null,
        "function_call": null,
        "tool_calls": null,
        "reasoning_content": "用户问的是周树人和鲁迅是不是兄弟。这是一个常见的误解。周树人是鲁迅的本名，鲁迅是他的笔名。所以他们是同一个人，不是兄弟。需要直接澄清这个事实。解释清楚名字和笔名的关系，避免用户继续困惑。"
      }
    }
  ],
  "created": 1781774332,
  "model": "deepseek-v4-flash",
  "object": "chat.completion",
  "service_tier": null,
  "system_fingerprint": null,
  "usage": {
    "completion_tokens": 134,
    "prompt_tokens": 12,
    "total_tokens": 146,
    "completion_tokens_details": {
      "accepted_prediction_tokens": null,
      "audio_tokens": null,
      "reasoning_tokens": 53,
      "rejected_prediction_tokens": null
    },
    "prompt_tokens_details": {
      "audio_tokens": null,
      "cached_tokens": 0
    }
  }
}
==================================================
📊 关键信息摘要：
  • 模型: deepseek-v4-flash
  • 回复: 不是的。**周树人和鲁迅是同一个人**。

鲁迅（1881年9月25日－1936年10月19日），原名**周樟寿**，后改名**周树人**，“鲁迅”是他1918年发表《狂人日记》时开始使用的笔名。因此，周树人是鲁迅的本名，他们是同一人，而非兄弟关系。
  • Token 使用: 146 (输入: 12, 输出: 134)
==================================================
```


## ⚠️ 注意事项

1. **API Key 安全**：请妥善保管 API Key,不要泄露
2. **HTTPS 协议**：所有请求必须通过 HTTPS 发送
3. **响应格式**:响应格式为 JSON

---

<p align="center">
  <small>© 2026 DMXAPI OpenAI Chat</small>
</p>