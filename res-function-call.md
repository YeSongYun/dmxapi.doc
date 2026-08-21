# OpenAI Responses API 函数调用

本页演示通过 DMXAPI 兼容代理让 `gpt-5.6-sol` 生成函数调用。模型只返回函数名和参数，真实天气查询仍需由你的程序执行。

## 🔗 请求地址

```text
https://www.dmxapi.cn/v1/responses
```

:::warning API 密钥安全
示例令牌为不可用占位符。请妥善保管真实 DMXAPI 令牌，不要写入公开代码或日志。
:::

## 模型名称

- `gpt-5.6-sol`

## Python 请求示例

```python
"""
==============================================
DMX API Function Call 测试脚本
==============================================
功能说明：
    本脚本演示如何使用 DMX API 的 Function Call 功能
    通过定义工具函数，让 AI 模型能够调用外部函数获取实时数据

示例场景：
    查询天气信息 - AI 会自动调用 get_current_weather 函数

作者：DMX API 团队
==============================================
"""

import requests
import json

# ==================== 配置区域 ====================

# API 接口地址
url = "https://www.dmxapi.cn/v1/responses"

# 请求头配置
headers = {
    "Content-Type": "application/json",
    "Authorization": "sk-*********************************"  # ⚠️ 请替换为你的实际 API Key
}

# ==================== 工具函数定义 ====================

# 定义可供 AI 调用的工具列表
tools = [
    {
        "type": "function",                              # 工具类型：函数
        "name": "get_current_weather",                   # 函数名称
        "description": "获取指定位置的当前天气",          # 函数描述，帮助 AI 理解何时调用
        "parameters": {                                  # 函数参数定义
            "type": "object",
            "properties": {
                "location": {                            # 参数1：地理位置
                    "type": "string",
                    "description": "城市和州，例如 San Francisco, CA"
                },
                "unit": {                                # 参数2：温度单位
                    "type": "string",
                    "enum": ["celsius", "fahrenheit"]    # 可选值：摄氏度或华氏度
                }
            },
            "required": ["location", "unit"]             # 必填参数列表
        }
    }
]

# ==================== 请求数据准备 ====================

data = {
    "model": "gpt-5.6-sol",                               # 使用的 AI 模型
    "input": "今天北京的天气热吗？",                      # 用户输入的问题
    "tools": tools,                                      # 传入工具定义
    "tool_choice": "auto"                                # 工具选择模式：auto（自动）/ required（必须）/ none（不使用）
}

# ==================== 发送 API 请求 ====================

print("📤 正在发送请求到 DMX API...")
print(f"🎯 模型: {data['model']}")
print(f"💬 问题: {data['input']}")

response = requests.post(
    url=url,
    headers=headers,
    data=json.dumps(data)
)

# ==================== 处理响应结果 ====================

if response.status_code == 200:
    # 请求成功
    result = response.json()
    print("✅ 响应成功:")
    print("=" * 50)
    print(json.dumps(result, indent=2, ensure_ascii=False))
    print("=" * 50)
else:
    # 请求失败
    print(f"❌ 请求失败 (状态码: {response.status_code})")
    print("错误信息:")
    print(response.text)
```

## 返回示例

```json
{
  "id": "resp_example_gpt56_tool_001",
  "object": "response",
  "status": "completed",
  "model": "gpt-5.6-sol",
  "output": [
    {
      "id": "fc_example_weather_001",
      "type": "function_call",
      "status": "completed",
      "name": "get_current_weather",
      "arguments": "{\"location\":\"北京, 中国\",\"unit\":\"celsius\"}",
      "call_id": "call_example_weather_001"
    }
  ],
  "tool_choice": "auto"
}
```

## 注意事项

- `arguments` 是 JSON 字符串；反序列化后仍需按 schema、权限和业务规则再次校验。
- 收到 `function_call` 后，由应用执行真实工具，再把结果作为后续输入提交给模型。
- 本页使用 `tool_choice: "auto"`，已通过 DMXAPI 定点实测并成功返回 `function_call`。

<p align="center">
  <small>© 2026 DMXAPI OpenAI Responses API 函数调用</small>
</p>
