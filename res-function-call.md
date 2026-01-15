# Responses 接口 - 函数调用 (Function Call)

> 通过 Function Call 功能,让 AI 模型能够调用外部函数获取实时数据,实现更智能的交互体验。



## 📍 接口地址

```
https://www.dmxapi.cn/v1/responses
```



## 🚀 快速开始

### 功能特性

- ✨ **智能函数调用** - AI 自动识别并调用合适的工具函数
- 🔧 **灵活配置** - 支持多种工具选择模式 (auto/required/none)
- 🎯 **精准参数解析** - 自动提取用户输入中的关键信息



## 💻 Python 调用示例

### 完整代码示例
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
    "model": "gpt-5-mini",                               # 使用的 AI 模型
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


## 📄 响应示例

### 控制台输出

```json
📤 正在发送请求到 DMX API...
🎯 模型: gpt-5-mini
💬 问题: 今天北京的天气热吗？
✅ 响应成功:
==================================================
{
  "id": "resp_0395ef1c1e354ec500690df5babb388196bee9b50434572cf7",
  "object": "response",
  "created_at": 1762522554,
  "status": "completed",
  "background": false,
  "content_filters": null,
  "error": null,
  "incomplete_details": null,
  "instructions": null,
  "max_output_tokens": null,
  "max_tool_calls": null,
  "model": "gpt-5-mini",
  "output": [
    {
      "id": "rs_0395ef1c1e354ec500690df5bb2f14819689879ed49d5e2a17",
      "type": "reasoning",
      "summary": []
    },
    {
      "id": "fc_0395ef1c1e354ec500690df5bee1f08196aaaeeba0d71f3ea1",
      "type": "function_call",
      "status": "completed",
      "arguments": "{\"location\":\"Beijing, China\",\"unit\":\"celsius\"}",
      "call_id": "call_nbjLHa652V1Rlgt1eb8asFkr",
      "name": "get_current_weather"
    }
  ],
  "parallel_tool_calls": true,
  "previous_response_id": null,
  "prompt_cache_key": null,
  "reasoning": {
    "effort": "medium",
    "summary": null
  },
  "safety_identifier": null,
  "service_tier": "default",
  "store": true,
  "temperature": 1.0,
  "text": {
    "format": {
      "type": "text"
    },
    "verbosity": "medium"
  },
  "tool_choice": "auto",
  "tools": [
    {
      "type": "function",
      "description": "获取指定位置的当前天气",
      "name": "get_current_weather",
      "parameters": {
        "properties": {
          "location": {
            "description": "城市和州，例如 San Francisco, CA",
            "type": "string"
          },
          "unit": {
            "enum": [
              "celsius",
              "fahrenheit"
            ],
            "type": "string"
          }
        },
        "required": [
          "location",
          "unit"
        ],
        "type": "object",
        "additionalProperties": false
      },
      "strict": true
    }
  ],
  "top_logprobs": 0,
  "top_p": 1.0,
  "truncation": "disabled",
  "usage": {
    "input_tokens": 73,
    "input_tokens_details": {
      "cached_tokens": 0
    },
    "output_tokens": 157,
    "output_tokens_details": {
      "reasoning_tokens": 128
    },
    "total_tokens": 230
  },
  "user": null,
  "metadata": {}
}
==================================================
```



## 📋 响应字段说明

### 核心字段

| 字段 | 类型 | 说明 |
|------|------|------|
| `id` | string | 响应唯一标识符 |
| `model` | string | 使用的 AI 模型名称 |
| `status` | string | 响应状态 (completed/failed/in_progress) |
| `created_at` | integer | 创建时间戳 |

### 输出字段 (output)

函数调用成功时,`output` 数组会包含以下信息:

| 字段 | 类型 | 说明 |
|------|------|------|
| `type` | string | 输出类型 (function_call/reasoning) |
| `name` | string | 被调用的函数名称 |
| `arguments` | string | JSON 格式的函数参数 |
| `call_id` | string | 函数调用的唯一标识 |
| `status` | string | 调用状态 |

### 使用统计 (usage)

| 字段 | 说明 |
|------|------|
| `input_tokens` | 输入 token 数量 |
| `output_tokens` | 输出 token 数量 |
| `reasoning_tokens` | 推理 token 数量 |
| `total_tokens` | 总 token 数量 |



## 🔑 关键参数说明

### tool_choice 参数

| 值 | 说明 | 使用场景 |
|------|------|----------|
| `auto` | AI 自动判断是否调用函数 | 默认推荐,灵活性最高 |
| `required` | 强制 AI 必须调用函数 | 确保获取实时数据 |
| `none` | 禁用函数调用 | 仅需要文本回答 |

### 工具定义规范

每个工具需要包含以下字段:

- **type**: 固定为 `"function"`
- **name**: 函数名称 (建议使用下划线命名)
- **description**: 清晰描述函数用途,帮助 AI 理解调用时机
- **parameters**: 符合 JSON Schema 规范的参数定义


## 💡 最佳实践

### ✅ 推荐做法

1. **清晰的函数描述** - 让 AI 准确理解何时调用函数
2. **完整的参数定义** - 包含类型、描述、必填项等信息
3. **合理的枚举值** - 限制参数范围,避免无效输入
4. **错误处理** - 检查响应状态码和返回数据

### ⚠️ 注意事项

- 替换示例中的 API Key 为你的真实密钥
- 函数参数需要符合 JSON Schema 规范
- 建议设置合理的超时时间
- 生产环境建议添加重试机制

---

<p align="center">
  <small>© 2025 DMXAPI 函数调用</small>
</p>