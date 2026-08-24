# OpenAI Chat Completions 函数调用

本页演示通过 DMXAPI 兼容代理让 `gpt-5.6-sol` 返回函数调用参数。模型只负责选择工具并生成参数，真实天气查询仍需由你的程序执行。

## 🔗 请求地址

```text
https://www.dmxapi.cn/v1/chat/completions
```
## 模型名称
- 本页示例：`gpt-5.6-sol`
- 其他模型：替换 `model`，并检查该模型对推理、输出长度和工具参数的支持情况。
## Python 请求示例

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
    "model": "gpt-5.6-sol",              # 使用的 AI 模型
    "reasoning_effort": "none",          # Chat Completions 携带 tools 时必须关闭推理
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
  "id": "chatcmpl_example_gpt56_tool_001",
  "object": "chat.completion",
  "created": 1787270400,
  "model": "gpt-5.6-sol-2026-07-09",
  "choices": [
    {
      "index": 0,
      "message": {
        "role": "assistant",
        "content": null,
        "tool_calls": [
          {
            "id": "call_example_weather_001",
            "type": "function",
            "function": {
              "name": "get_current_weather",
              "arguments": "{\"location\":\"上海, 中国\",\"unit\":\"celsius\"}"
            }
          }
        ]
      },
      "finish_reason": "tool_calls"
    }
  ]
}
```

## 注意事项

- GPT-5.6 的 Chat Completions 请求携带 `tools` 时，必须显式设置 `reasoning_effort: "none"`；省略该字段会采用默认的 `medium` 并导致请求失败。
- 如果工作流需要模型推理、执行工具并继续多轮处理，优先使用 Responses API。
- 不要直接信任模型生成的函数参数；执行工具前应做 schema 校验、权限检查和输入过滤。

<p align="center">
  <small>© 2026 DMXAPI OpenAI Chat Completions 函数调用</small>
</p>
