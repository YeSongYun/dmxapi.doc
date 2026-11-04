# DMXAPI 单请求消费（cost）说明

调用 DMXAPI 对话接口后，可以从返回 JSON 的 **`usage.cost`** 字段读取本次请求的人民币消费金额。本文通过一次非流式对话调用，说明如何查看完整响应、读取 `cost`，以及在展示或计算金额时处理该字段。

## 📌 接口地址

```text
https://www.dmxapi.cn/v1/chat/completions
```

## 示例代码

```python
"""
DMXAPI 对话接口调用示例
功能：调用对话模型，仅输出完整响应体
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
    "model": "deepseek-v4.1-flash-1017",  # 选择使用的模型
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
    # 发送 POST 请求到 API，使用 json 参数自动编码请求数据
    response = requests.post(url, headers=headers, json=payload)

    # 未声明编码的文本响应默认按 UTF-8 解码，避免中文乱码
    if not response.encoding or response.encoding.lower() == "iso-8859-1":
        response.encoding = "utf-8"

    # 仅输出响应体；JSON 保留所有字段，非 JSON 直接输出全文
    try:
        response_data = response.json()
    except requests.exceptions.JSONDecodeError:
        print(response.text)
    else:
        print(json.dumps(response_data, indent=2, ensure_ascii=False))

except requests.exceptions.RequestException as e:
    print(f"❌ 请求失败: {e}")
```

## 返回示例

```json
{
  "choices": [
    {
      "finish_reason": "stop",
      "index": 0,
      "logprobs": null,
      "message": {
        "content": "不是兄弟，周树人和鲁迅是**同一个人**。鲁迅是笔名，本名周树人。",
        "reasoning_content": "我们需要回答中文问题。用户问“周树人和鲁迅是兄弟吗？” 这是一个 trick/常识：鲁迅原名周树人，周树人和鲁迅是同一个人，不是兄弟。需要解释。可能注意：周树人是鲁迅本名，鲁迅是笔名。所以不是兄弟关系。回答简洁。",
        "role": "assistant"
      }
    }
  ],
  "created": 1793780700,
  "id": "02179378069910153952e287ddd1b7d9109cd0048896ba077269a",
  "model": "DeepSeek-V4.1-Flash-261017",
  "service_tier": "default",
  "object": "chat.completion",
  "usage": {
    "prompt_tokens": 44,
    "completion_tokens": 87,
    "total_tokens": 131,
    "prompt_tokens_details": {
      "cached_tokens": 0,
      "text_tokens": 0,
      "audio_tokens": 0,
      "image_tokens": 0
    },
    "completion_tokens_details": {
      "text_tokens": 0,
      "audio_tokens": 0,
      "image_tokens": 0,
      "reasoning_tokens": 63
    },
    "input_tokens": 0,
    "output_tokens": 0,
    "input_tokens_details": null,
    "claude_cache_creation_5_m_tokens": 0,
    "claude_cache_creation_1_h_tokens": 0,
    "cost": "¥0.00062"
  }
}
```

## `cost` 字段说明

示例中的 **`"cost": "¥0.00062"` 表示本次请求消费 0.00062 元人民币**。
| 项目 | 说明 |
| --- | --- |
| 字段路径 | `usage.cost`，即返回 JSON 中 `usage` 对象下的 `cost` |
| 数据类型 | 字符串（`string`），包含货币符号和金额 |
| 示例值 | `"¥0.00062"` |
| 货币单位 | 人民币元（CNY），`¥` 为货币符号 |
| 金额范围 | 当前这一次模型请求的消费金额 |

同一响应中的 `usage.prompt_tokens`、`usage.completion_tokens` 和 `usage.total_tokens` 分别记录输入、输出和总 Token 用量。本例分别为 `44`、`87` 和 `131`；查看消费金额时，直接读取 `usage.cost` 即可。

#
---

<p align="center">
  <small>© 2026 DMXAPI 单请求消费（cost）说明</small>
</p>
