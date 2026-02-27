# Claude 原生格式 函数调用 API 文档

## 📋 概述

本文档详细介绍了如何使用 Claude 原生格式进行函数调用 API 的集成与开发。

## 🔗 接口地址

**请求端点：** `https://www.dmxapi.cn/v1/messages`

## 💻 Python 示例代码

以下是一个完整的 Python 示例，演示如何使用 Claude 函数调用 API：

```python
"""
DMX API 测试脚本


功能说明：
- 测试 DMX API 的对话功能
- 演示工具调用（天气查询）的使用
- 包含完整的错误处理和响应格式化

作者：DMX API 团队
"""
import requests
import os
import json

# =============================================================================
# 配置参数区域
# =============================================================================

# API 密钥配置
# 优先从环境变量 DMXAPI_API_KEY 获取，如果不存在则使用默认密钥
api_key = os.getenv('DMXAPI_API_KEY', 'sk-**********************************')

# API 端点 URL
url = "https://www.dmxapi.cn/v1/messages"

# =============================================================================
# 请求头配置
# =============================================================================

headers = {
    "content-type": "application/json",      # 指定请求内容为 JSON 格式
    "x-api-key": api_key                     # 认证密钥
}

# =============================================================================
# 请求数据构造
# =============================================================================

data = {
    # 使用的模型名称
    "model": "claude-sonnet-4-6",
    
    # 对话消息列表
    "messages": [
        {
            "role": "user",                   # 用户角色
            "content": "今天北京的天气怎么样?"  # 用户输入内容
        }
    ],
    
    # 可用的工具定义
    "tools": [
        {
            "name": "get_weather",           # 工具名称
            "description": "获取指定位置的当前天气",  # 工具描述
            "input_schema": {                # 输入参数定义
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "城市名称,如:北京"  # 参数说明
                    }
                },
                "required": ["location"]     # 必需参数
            }
        }
    ]
}

# =============================================================================
# 主程序执行区域
# =============================================================================

def main():
    """
    主函数：执行 API 请求并处理响应
    """
    print("🚀 开始执行 DMX API 测试...")
    print("=" * 50)
    
    try:
        # 发送 POST 请求到 API 端点
        print("📡 正在发送请求到 DMX API...")
        response = requests.post(url, headers=headers, json=data)
        
        # 检查 HTTP 状态码，如果请求失败会抛出异常
        response.raise_for_status()
        
        print("✅ 请求成功完成！")
        print("-" * 30)
        
        # 打印响应状态码
        print(f"📊 状态码: {response.status_code}")
        
        # 解析并格式化 JSON 响应
        print("📄 响应内容:")
        formatted_json = json.dumps(response.json(), indent=2, ensure_ascii=False)
        print(formatted_json)
        
        print("=" * 50)
        print("🎉 测试执行完毕！")
        
    except requests.exceptions.RequestException as e:
        # 处理网络请求相关的错误
        print(f"❌ 请求错误: {e}")
        print("💡 建议检查网络连接或 API 密钥配置")
        
    except ValueError as e:
        # 处理 JSON 解析错误
        print(f"❌ JSON 解析错误: {e}")
        print("💡 建议检查 API 响应格式是否正确")
        
    except Exception as e:
        # 处理其他未预期的错误
        print(f"❌ 未预期的错误: {e}")
        print("💡 请联系技术支持")

# =============================================================================
# 程序入口点
# =============================================================================

if __name__ == "__main__":
    main()
```

## 📊 返回示例

成功调用后的响应示例：

```json
🚀 开始执行 DMX API 测试...
==================================================
📡 正在发送请求到 DMX API...
✅ 请求成功完成！
------------------------------
📊 状态码: 200
📄 响应内容:
{
  "id": "msg_01W6F1qRVQBh2fmwAscYixwQ",
  "type": "message",
  "role": "assistant",
  "model": "claude-sonnet-4-6",
  "content": [
    {
      "type": "text",
      "text": "好的，让我来帮您查询北京今天的天气情况！"
    },
    {
      "id": "toolu_bdrk_01BCcQnHxZoWQ98vojpdwSEh",
      "type": "tool_use",
      "name": "get_weather",
      "input": {
        "location": "北京"
      }
    }
  ],
  "stop_reason": "tool_use",
  "usage": {
    "input_tokens": 590,
    "cache_creation_input_tokens": 0,
    "cache_read_input_tokens": 0,
    "output_tokens": 77,
    "cache_creation": {},
    "claude_cache_creation_5_m_tokens": 0,
    "claude_cache_creation_1_h_tokens": 0
  }
}
==================================================
🎉 测试执行完毕！
```

## 📝 使用说明

1. **API 密钥配置**：建议通过环境变量 `DMXAPI_API_KEY` 设置密钥
2. **请求格式**：使用 JSON 格式，包含模型、消息和工具定义
3. **错误处理**：代码包含完整的异常处理机制
4. **工具调用**：支持自定义工具定义和参数验证

## 🔧 注意事项

- 确保网络连接正常
- 验证 API 密钥的有效性
- 检查请求参数的完整性
- 处理可能的网络超时情况

---

<p align="center">
  <small>© 2025 DMXAPI Claude函数调用</small>
</p>