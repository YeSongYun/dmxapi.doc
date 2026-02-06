# Claude 对话 API 文档

## 📋 概述

本文档详细介绍了如何使用 DMXAPI 提供的 Claude 对话 API 接口。

## 🔗 请求地址

```text
https://www.dmxapi.cn/v1/messages
```


## 💻 示例代码

```python
"""
DMXAPI Claude API 测试脚本
用于测试 DMXAPI 提供的 Claude 模型 API 接口
"""

import requests
import json

# ============================================
# DMXAPI 配置
# ============================================
url = 'https://www.dmxapi.cn/v1/messages'  # DMXAPI 端点
key = 'sk-********************************************'  # DMXAPI 密钥

# 请求头配置
headers = {
    'Accept': 'application/json',
    'Authorization': f'{key}',
    'Content-Type': 'application/json'
}

# ============================================
# 请求数据配置
# ============================================
data = {
    "model": "claude-sonnet-4-5-20250929",  # 使用的模型版本
    "max_tokens": 200000,  # 最大生成的 token 数量
    "messages": [  # 消息列表（当前为简单单轮对话）
        {
            "role": "user",
            "content": "你好"
        }
    ],

    # ========================================
    # 多轮对话示例
    # ========================================
    '''
    多轮对话需要包含完整的对话历史：
    [
        {"role": "user", "content": "你好。"},
        {"role": "assistant", "content": "你好！我是 Claude。有什么可以帮你的吗？"},
        {"role": "user", "content": "请用简单的话解释什么是 LLM？"}
    ]
    '''

    # ========================================
    # 部分填充响应示例（Prefill）
    # ========================================
    '''
    通过预先填充 assistant 的部分回答来引导模型的输出格式：
    [
        {"role": "user", "content": "太阳的希腊语名字是什么? (A) Sol (B) Helios (C) Sun"},
        {"role": "assistant", "content": "正确答案是 ("}
    ]
    模型会自动补全为 "正确答案是 (B) Helios"
    '''

    # ========================================
    # 发送图片示例（Vision）
    # ========================================
    '''
    支持发送图片进行多模态分析：
    {
        "role": "user",
        "content": [
            {
                "type": "image",
                "source": {
                    "type": "base64",
                    "media_type": "image/jpeg",  # 支持 jpeg, png, gif, webp
                    "data": "/9j/4AAQSkZJRg..."  # base64 编码的图片数据
                }
            },
            {
                "type": "text",
                "text": "这张图片里有什么?"
            }
        ]
    }
    '''

    # ========================================
    # Content 类型详解
    # ========================================
    '''
    1. 文本内容（Text Content）
    {
        "type": "text",              # 必需，内容类型
        "text": "Hello, Claude",     # 必需，文本内容，最小长度: 1
        "cache_control": {           # 可选，提示词缓存控制
            "type": "ephemeral"      # 枚举值: "ephemeral"
        }
    }

    2. 图片内容（Image Content）
    {
        "type": "image",             # 必需，内容类型
        "source": {                  # 必需，图片源
            "type": "base64",        # 必需，源类型
            "media_type": "image/jpeg",  # 必需，支持: jpeg, png, gif, webp
            "data": "/9j/4AAQSkZJRg..."  # 必需，base64 编码的图片数据
        },
        "cache_control": {           # 可选，提示词缓存控制
            "type": "ephemeral"
        }
    }

    3. 工具使用（Tool Use）
    {
        "type": "tool_use",          # 必需，内容类型
        "id": "toolu_xyz...",        # 必需，工具使用的唯一标识符
        "name": "get_weather",       # 必需，工具名称，最小长度: 1
        "input": {                   # 必需，工具的输入参数对象
            # 具体参数由工具的 input_schema 定义
        },
        "cache_control": {           # 可选，提示词缓存控制
            "type": "ephemeral"
        }
    }

    4. 工具结果（Tool Result）
    {
        "type": "tool_result",                # 必需，内容类型
        "tool_use_id": "toolu_xyz...",       # 必需，对应的工具使用 ID
        "content": "结果内容",                 # 必需，可以是字符串或内容块数组
        "is_error": false,                   # 可选，是否为错误结果
        "cache_control": {                   # 可选，提示词缓存控制
            "type": "ephemeral"
        }
    }

    5. 文档内容（Document Content）
    {
        "type": "document",          # 必需，内容类型
        "source": {                  # 必需，文档源数据
            # 文档源配置
        },
        "cache_control": {           # 可选，提示词缓存控制
            "type": "ephemeral"
        }
    }

    6. 组合示例（多类型内容）
    {
        "type": "tool_result",
        "tool_use_id": "toolu_xyz...",
        "content": [
            {
                "type": "text",
                "text": "分析结果",
                "cache_control": {"type": "ephemeral"}
            },
            {
                "type": "image",
                "source": {
                    "type": "base64",
                    "media_type": "image/jpeg",
                    "data": "..."
                },
                "cache_control": {"type": "ephemeral"}
            }
        ]
    }
    '''

    # ========================================
    # 其他可选参数
    # ========================================
    # "stop_sequences": ["### End"],  # 自定义停止生成的文本序列

    "stream": False,  # 是否启用流式响应

    # Opus 4.6 的扩展思维推荐方式是使用自适应思维，可以根据每个请求的复杂性动态地决定何时以及思考多少。
    # 可以用 【thinking: {"type": "adaptive"}】 结合 【effort】 参数来设置它
    # 【effort】：可选择的努力程度：
                # max - Claude 的思考深度不受任何限制（ Opus 4.6 独有）
                # high （默认）- 总是思考，为复杂任务提供深刻的推理。
                # medium - 思维能力适中，对于非常简单的问题可以跳过。
                # low - 减少思考，优先考虑简单任务的速度

    # "thinking": {"type": "adaptive"}, #可选 
    # "effort":"max"#可选

    # "temperature": 0.7  # 控制生成随机性，范围 0.0 - 1.0
    #   - 分析性/选择题任务：建议接近 0.0（更确定性）
    #   - 创造性/生成性任务：建议接近 1.0（更随机性）

    # ========================================
    # Tool Choice（工具选择模式）
    # ========================================
    # "tool_choice": {
    #     # 1. Auto 模式（自动选择）
    #     "type": "auto",                       # 必需，让模型自动决定是否使用工具
    #     "disable_parallel_tool_use": false    # 可选，默认 false
    #                                           # true: 模型最多只会使用一个工具
    #
    #     # 2. Any 模式（任意工具）
    #     "type": "any",                        # 必需，模型必须使用至少一个工具
    #     "disable_parallel_tool_use": false    # 可选，默认 false
    #                                           # true: 模型将恰好使用一个工具
    #
    #     # 3. Tool 模式（指定工具）
    #     "type": "tool",                       # 必需，指定使用特定工具
    #     "name": "get_weather",                # 必需，指定要使用的工具名称
    #     "disable_parallel_tool_use": false    # 可选，默认 false
    #                                           # true: 模型将恰好使用一个工具
    # }

    # ========================================
    # Tools（工具定义）
    # ========================================
    # "tools": [
    #     # 1. 自定义工具（Custom Tool）
    #     {
    #         "type": "custom",                 # 可选，枚举值: "custom"
    #         "name": "get_weather",            # 必需，工具名称，1-64 个字符
    #         "description": "获取指定位置的当前天气",  # 建议尽可能详细
    #         "input_schema": {                 # 必需，JSON Schema 定义
    #             "type": "object",
    #             "properties": {
    #                 "location": {
    #                     "type": "string",
    #                     "description": "城市名称，如：北京"
    #                 }
    #             },
    #             "required": ["location"]
    #         },
    #         "cache_control": {                # 可选，提示词缓存控制
    #             "type": "ephemeral"
    #         }
    #     },
    #
    #     # 2. 计算机工具（Computer Use Tool）
    #     {
    #         "type": "computer_20241022",      # 必需
    #         "name": "computer",               # 必需，枚举值: "computer"
    #         "display_width_px": 1024,         # 必需，显示宽度（像素）
    #         "display_height_px": 768,         # 必需，显示高度（像素）
    #         "display_number": 0,              # 可选，X11 显示编号
    #         "cache_control": {
    #             "type": "ephemeral"           # 可选
    #         }
    #     },
    #
    #     # 3. Bash 工具（Bash Tool）
    #     {
    #         "type": "bash_20241022",          # 必需
    #         "name": "bash",                   # 必需，枚举值: "bash"
    #         "cache_control": {
    #             "type": "ephemeral"           # 可选
    #         }
    #     },
    #
    #     # 4. 文本编辑器工具（Text Editor Tool）
    #     {
    #         "type": "text_editor_20241022",   # 必需
    #         "name": "str_replace_editor",     # 必需，枚举值: "str_replace_editor"
    #         "cache_control": {
    #             "type": "ephemeral"           # 可选
    #         }
    #     }
    # ]

    # ========================================
    # 工具使用流程示例
    # ========================================
    # 
    # 当模型决定使用工具时，会返回 tool_use 内容块：
    # [
    #     {
    #         "type": "tool_use",
    #         "id": "toolu_01D7FLrfh4GYq7yT1ULFeyMV",
    #         "name": "get_weather",
    #         "input": {"location": "北京"}
    #     }
    # ]
    #
    # 您需要执行工具并通过 tool_result 内容块返回结果：
    # [
    #     {
    #         "type": "tool_result",
    #         "tool_use_id": "toolu_01D7FLrfh4GYq7yT1ULFeyMV",
    #         "content": "北京当前天气晴朗，温度 25°C"
    #     }
    # ]

    # ========================================
    # 采样参数（Sampling Parameters）
    # ========================================
    # "top_k": 1      # 范围：x > 0，保留概率最高的 k 个 token
    # "top_p": 0.8    # 范围：0 < x < 1，核采样阈值
}


# ============================================
# 发送请求并处理响应
# ============================================
response = requests.post(url, headers=headers, json=data)

# 打印响应状态码
print(f"Status Code: {response.status_code}")

# 格式化打印 JSON 响应（美化输出，保持中文字符）
print("Response:")
print(json.dumps(response.json(), indent=4, ensure_ascii=False))
```


## 📊 返回示例

```json
Status Code: 200
Response:
{
    "id": "msg_01PKLmBfi7yjbx9eU54JRu22",
    "type": "message",
    "role": "assistant",
    "model": "claude-sonnet-4-5-20250929",
    "content": [
        {
            "type": "text",
            "text": "你好！很高兴见到你。有什么我可以帮助你的吗？"
        }
    ],
    "stop_reason": "end_turn",
    "usage": {
        "input_tokens": 10,
        "cache_creation_input_tokens": 0,
        "cache_read_input_tokens": 0,
        "output_tokens": 29,
        "claude_cache_creation_5_m_tokens": 0,
        "claude_cache_creation_1_h_tokens": 0
    }
}
```


## 🔧 功能特性

### ✅ 支持的功能

- **多轮对话** - 支持完整的对话历史管理
- **图片分析** - 支持发送图片进行多模态分析
- **工具调用** - 支持自定义工具和系统工具
- **流式响应** - 支持实时流式输出
- **参数调优** - 支持温度、top-k、top-p 等采样参数

### 📝 内容类型

1. **文本内容** - 纯文本对话
2. **图片内容** - 支持多种图片格式
3. **工具使用** - 模型调用工具
4. **工具结果** - 工具执行结果返回
5. **文档内容** - 文档处理功能

### ⚙️ 配置选项

- **模型选择** - 支持不同版本的 Claude 模型
- **Token 限制** - 可设置最大输出 token 数量
- **停止序列** - 自定义停止生成的条件
- **温度控制** - 调整生成结果的随机性

<p align="center">
  <small>© 2025 DMXAPI Claude对话</small>
</p>