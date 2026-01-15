# 🌐 API 统一请求格式

## 📖 概述

所有模型（包括非 OpenAI 模型）的请求格式已统一转换为 OpenAI 格式，几乎兼容本站的所有模型。

## 🌐接口地址

`https://www.dmxapi.cn/v1/chat/completions`

## 🎯 使用方法

只需替换 `"model"` 参数为您需要的模型名称即可。

## ℹ️ 基础信息

| 项目 | 说明 |
|------|------|
| **Base URL** | `https://www.dmxapi.cn` |
| **认证方式** | API Key (Token) |
| **请求方法** | `POST` |
| **接口路径** | `/v1/chat/completions` |

## 💻 Python 示例代码
```python
"""
DMXAPI 对话接口调用示例
功能：使用 gpt-5-mini 模型进行智能对话
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
    "model": "gpt-5-mini",  # 选择使用的模型
    "messages": [
        {
            "role": "system", 
            "content": "You are a helpful assistant."  # 系统提示词：定义 AI 助手的角色
        },
        {
            "role": "user", 
            "content": "周树人和鲁迅是兄弟吗？"  # 用户问题
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

::: tip 提示
实际使用时请将 `sk-**********************************` 替换为你的真实 API 密钥
:::

## 📤 返回示例

### 成功响应结构

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
        "content": "不是兄弟。周树人就是鲁迅的本名／原名，鲁迅是他的笔名。鲁迅（周树人，1881—1936）是中国现代著名作家、思想家。",
        "refusal": null,
        "role": "assistant"
      }
    }
  ],
  "created": 1762512121,
  "id": "chatcmpl-CZECnsYuphVShao4a6XlUxvzFd5yi",
  "model": "gpt-5-mini-2025-08-07",
  "object": "chat.completion",
  "system_fingerprint": null,
  "usage": {
    "completion_tokens": 378,
    "completion_tokens_details": {
      "accepted_prediction_tokens": 0,
      "audio_tokens": 0,
      "reasoning_tokens": 320,
      "rejected_prediction_tokens": 0
    },
    "prompt_tokens": 27,
    "prompt_tokens_details": {
      "audio_tokens": 0,
      "cached_tokens": 0
    },
    "total_tokens": 405
  }
}
```

---

<p align="center">
  <small>© 2025 DMXAPI API请求格式</small>
</p>