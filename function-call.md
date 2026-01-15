# OpenAI 函数调用(Function Calling) API 文档

## 概念介绍
函数调用(Function Calling)是AI大模型的一种能力。允许大语言模型在对话过程中调用外部函数/工具。当用户提问需要实时数据(如天气、股票等)时，模型会返回函数调用请求，开发者可以在后端执行相应函数并返回结果。

## 接口地址
`https://www.dmxapi.cn/v1/chat/completions`


## 请求示例

```python
"""
DMXAPI Function Calling 示例
功能:演示如何使用 DMXAPI 的函数调用功能查询天气信息
"""

import http.client
import json

# ========== 第一步:建立连接 ==========
# 创建到 DMXAPI 服务器的 HTTPS 安全连接
conn = http.client.HTTPSConnection("www.dmxapi.cn")

# ========== 第二步:构造请求数据 ==========
payload = json.dumps({
    # 模型配置
    "model": "gpt-5-mini",              # 使用的 AI 模型
    "max_tokens": 16384,              # 限制返回的最大 token 数量
    "temperature": 1,             # 控制生成文本的随机性(0-2,越高越随机)
    "stream": False,                # 是否使用流式输出(False 为一次性返回)
    
    # 对话消息
    "messages": [{
        "role": "user",             # 消息角色:用户
        "content": "上海今天几度？"  # 用户的问题内容
    }],
    
    # 工具定义(Function Calling)
    "tools": [{
        "type": "function",         # 工具类型:函数
        "function": {
            # 函数基本信息
            "name": "get_current_weather",        # 函数名称(模型会调用此函数)
            "description": "获得天气信息",         # 函数功能描述(帮助模型理解何时调用)
            
            # 函数参数结构定义
            "parameters": {
                "type": "object",                 # 参数类型为对象
                "properties": {
                    # 参数1: 地点(必填)
                    "location": {
                        "type": "string",
                        "description": "上海, 中国" # 位置描述
                    },
                    # 参数2: 温度单位(可选)
                    "unit": {
                        "type": "string",
                        "enum": ["celsius", "fahrenheit"]  # 枚举值:摄氏度或华氏度
                    }
                },
                "required": ["location"]          # 声明 location 为必填参数
            }
        }
    }]
})

# ========== 第三步:设置请求头 ==========
headers = {
    "Accept": "application/json",                           # 接受 JSON 格式响应
    "Authorization": "sk-********************************",  # DMXAPI 密钥认证(请替换为你的真实密钥)
    "Content-Type": "application/json"                      # 请求体为 JSON 格式
}

# ========== 第四步:发送 POST 请求 ==========
# 向 /v1/chat/completions 端点发送请求
conn.request("POST", "/v1/chat/completions", payload, headers)

# ========== 第五步:接收并处理响应 ==========
res = conn.getresponse()            # 获取响应对象
data = res.read()                   # 读取响应数据(字节格式)

# ========== 第六步:输出结果 ==========
# 将字节数据解码为 UTF-8 字符串并格式化输出 JSON
response_data = json.loads(data.decode("utf-8"))
print(json.dumps(response_data, indent=2, ensure_ascii=False))
```

## 返回示例
```json
{
  "id": "chatcmpl-CZEX9yYU5w2C97QyimOkQR0tjr3ID",
  "object": "chat.completion",
  "created": 1762513383,
  "model": "gpt-5-mini-2025-08-07",
  "choices": [
    {
      "index": 0,
      "message": {
        "role": "assistant",
        "content": null,
        "refusal": null,
        "tool_calls": [
          {
            "function": {
              "arguments": "{\"location\":\"上海, 中国\",\"unit\":\"celsius\"}",
              "name": "get_current_weather"
            },
            "id": "call_Syfqyc3RXs1XNjjhUfDUwH76",
            "type": "function"
          }
        ],
        "annotations": []
      },
      "logprobs": null,
      "finish_reason": "tool_calls"
    }
  ],
  "usage": {
    "prompt_tokens": 146,
    "completion_tokens": 96,
    "total_tokens": 242,
    "prompt_tokens_details": {
      "cached_tokens": 0,
      "audio_tokens": 0
    },
    "completion_tokens_details": {
      "reasoning_tokens": 64,
      "audio_tokens": 0,
      "accepted_prediction_tokens": 0,
      "rejected_prediction_tokens": 0
    }
  },
  "system_fingerprint": null
}
```

---

<p align="center">
  <small>© 2025 DMXAPI OpenAI 函数调用</small>
</p>