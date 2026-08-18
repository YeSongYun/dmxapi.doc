# OpenAI Response 接口格式调用

## 接口地址

```
https://www.dmxapi.cn/v1/responses
```

## 调用示例
::: code-group

```python[SDK]

"""
╔═══════════════════════════════════════════════════════════════╗
║                  DMXAPI GPT-5系列及其他模型调用示例             ║
╚═══════════════════════════════════════════════════════════════╝

📝 功能说明:
   本脚本演示如何使用 OpenAI SDK 调用 DMXAPI 的 GPT-5系列及其他模型
   通过 responses.create 接口进行对话交互

═══════════════════════════════════════════════════════════════
"""

from openai import OpenAI
import json

# ═══════════════════════════════════════════════════════════════
# 🔑 步骤1: 初始化 DMXAPI 客户端
# ═══════════════════════════════════════════════════════════════
client = OpenAI(
    # 🔐 DMXAPI 密钥 (请替换为您自己的密钥)
    # 获取方式: 登录 DMXAPI 官网 -> 个人中心 -> API 密钥管理
    api_key="sk-**********************************",
    
    # 🌐 DMXAPI 服务端点地址
    # 所有 API 请求都将发送到此基础 URL
    base_url="https://www.dmxapi.cn/v1",
)

# ═══════════════════════════════════════════════════════════════
# 💬 步骤2: 创建对话请求
# ═══════════════════════════════════════════════════════════════
response = client.responses.create(  
    # 🤖 模型选择
    # gpt-5.2: GPT-5系列模型,支持高级推理,适用于复杂问题和深度分析
    model="gpt-5.2",
    
    # 💭 用户输入
    # 您想要向模型提出的问题或对话内容（gtp-5-codex如果跑不通的话，需要改成结构化的组格式）
    input="你好!",

    # 📏 最大输出令牌数
    # 控制模型响应的最大长度 (范围: 1 - 128000)
    # 注意: 实际输出可能少于此值
    # max_output_tokens=128000,

    # 🌡️ 温度参数 (范围: 0.0 - 2.0)
    # 控制输出的随机性和创造性:
    #   - 较低值 (0.0-0.3): 输出更确定、更一致,适合事实性任务
    #   - 中等值 (0.4-0.8): 平衡创造性和一致性
    #   - 较高值 (0.9-2.0): 输出更随机、更有创意
    # ⚠️ 建议只调整 temperature 或 top_p 其中之一
    # temperature=1,

    # 🎯 核采样参数 (范围: 0.0 - 1.0)
    # 控制采样的概率质量阈值:
    #   - 0.1: 只考虑概率最高的 10% 的词
    #   - 0.5: 只考虑概率最高的 50% 的词
    #   - 1.0: 考虑所有可能的词
    # 💡 较低的值会让输出更集中,较高的值会增加多样性
    # ⚠️ 建议只调整 temperature 或 top_p 其中之一
    # op_p=1,
    
    # 🧠 推理配置选项
    # 仅适用于 GPT-5 和 O 系列推理模型
    reasoning={
        # 推理精力等级:
        "effort": "none"
    },
)


# ═══════════════════════════════════════════════════════════════
# 📤 步骤3: 输出响应结果
# ═══════════════════════════════════════════════════════════════
# 🖨️ 将响应对象转换为格式化的 JSON 字符串并打印到控制台
# 
# 参数说明:
#   - indent=2:           使用 2 个空格缩进,提高 JSON 可读性
#   - ensure_ascii=False: 保留中文字符,不转义为 Unicode 编码
print(json.dumps(response.model_dump(), indent=2, ensure_ascii=False))
```
```python[resquests]
"""
╔═══════════════════════════════════════════════════════════════╗
║                  DMXAPI GPT-5系列及其他模型调用示例             ║
╚═══════════════════════════════════════════════════════════════╝

📝 功能说明:
   本脚本演示如何使用 requests 库调用 DMXAPI 的 GPT-5系列及其他模型
   通过 responses 接口进行对话交互（非流式输出）

═══════════════════════════════════════════════════════════════
"""

import requests
import json

# ═══════════════════════════════════════════════════════════════
# 🔑 步骤1: 配置 API 连接信息
# ═══════════════════════════════════════════════════════════════

# 🌐 DMXAPI 服务端点地址
url = "https://www.dmxapi.cn/v1/responses"

# 🔐 DMXAPI 密钥 (请替换为您自己的密钥)
# 获取方式: 登录 DMXAPI 官网 -> 个人中心 -> API 密钥管理
api_key = "sk-**********************************"

# ═══════════════════════════════════════════════════════════════
# 📋 步骤2: 配置请求头
# ═══════════════════════════════════════════════════════════════

headers = {
    "Content-Type": "application/json",      # 指定请求体为 JSON 格式
    "Authorization": f"{api_key}",    # token 认证方式
}

# ═══════════════════════════════════════════════════════════════
# 💬 步骤3: 配置请求参数
# ═══════════════════════════════════════════════════════════════

data = {
    # ---------- 基础配置 ----------
    # 🤖 模型选择
    # gpt-5.2: GPT-5系列模型,支持高级推理,适用于复杂问题和深度分析
    "model": "gpt-5.2",

    # 💭 用户输入
    # 您想要向模型提出的问题或对话内容
    # (gpt-5-codex 如果跑不通的话，需要改成结构化的数组格式)
    "input": "你好!",

    # ---------- 输出控制参数 ----------
    # 📏 最大输出令牌数 (范围: 1 - 128000)
    # 控制模型响应的最大长度
    # 💡 提示: 实际输出可能少于此值
    # "max_output_tokens": 128000,

    # ---------- 采样参数 ----------
    # 🌡️ 温度参数 (范围: 0.0 - 2.0)
    # 控制输出的随机性和创造性:
    #   • 较低值 (0.0-0.3): 输出更确定、更一致,适合事实性任务
    #   • 中等值 (0.4-0.8): 平衡创造性和一致性
    #   • 较高值 (0.9-2.0): 输出更随机、更有创意
    # ⚠️ 建议: 只调整 temperature 或 top_p 其中之一
    # "temperature": 1,

    # 🎯 核采样参数 (范围: 0.0 - 1.0)
    # 控制采样的概率质量阈值:
    #   • 0.1: 只考虑概率最高的 10% 的词
    #   • 0.5: 只考虑概率最高的 50% 的词
    #   • 1.0: 考虑所有可能的词
    # 💡 提示: 较低的值会让输出更集中,较高的值会增加多样性
    # ⚠️ 建议: 只调整 temperature 或 top_p 其中之一
    # "top_p": 1,

    # ---------- 推理配置 ----------
    # 🧠 推理配置选项 (仅适用于 GPT-5 和 O 系列推理模型)
    "reasoning": {
        "effort": "none"    # 推理精力等级
    },
}

# ═══════════════════════════════════════════════════════════════
# 📤 步骤4: 发送请求并输出结果
# ═══════════════════════════════════════════════════════════════

# 发送 POST 请求到 API 服务器
response = requests.post(url, headers=headers, json=data)

# 格式化输出 JSON 响应
# - indent=2: 缩进 2 空格，便于阅读
# - ensure_ascii=False: 正确显示中文字符
print(json.dumps(response.json(), indent=2, ensure_ascii=False))
```
:::


## 返回示例
::: code-group

```json[SDK]
{
  "id": "resp_030315874d6d301e00693fc2e4ff4c8192a1bc3ec97d3172ee",
  "created_at": 1765786341.0,
  "error": null,
  "incomplete_details": null,
  "instructions": null,
  "metadata": {},
  "model": "gpt-5.2",
  "object": "response",
  "output": [
    {
      "id": "msg_030315874d6d301e00693fc2e540908192af21c52a2e4e7f3c",
      "content": [
        {
          "annotations": [],
          "text": "你好！我在。想聊什么，或者需要我帮你做什么？",
          "type": "output_text",
          "logprobs": []
        }
      ],
      "role": "assistant",
      "status": "completed",
      "type": "message"
    }
  ],
  "parallel_tool_calls": true,
  "temperature": 1.0,
  "tool_choice": "auto",
  "tools": [],
  "top_p": 0.98,
  "background": false,
  "conversation": null,
  "max_output_tokens": null,
  "max_tool_calls": null,
  "previous_response_id": null,
  "prompt": null,
  "prompt_cache_key": null,
  "prompt_cache_retention": null,
  "reasoning": {
    "effort": "high",
    "generate_summary": null,
    "summary": null
  },
  "safety_identifier": null,
  "service_tier": "default",
  "status": "completed",
  "text": {
    "format": {
      "type": "text"
    },
    "verbosity": "medium"
  },
  "top_logprobs": 0,
  "truncation": "disabled",
  "usage": {
    "input_tokens": 8,
    "input_tokens_details": {
      "cached_tokens": 0
    },
    "output_tokens": 21,
    "output_tokens_details": {
      "reasoning_tokens": 0
    },
    "total_tokens": 29
  },
  "user": null,
  "billing": {
    "payer": "developer"
  },
  "store": true
}
```
```json[requests]
{
  "id": "resp_028de2c59db26ba2006959e4352a0881948d98e7761ddb9e58",
  "object": "response",
  "model": "gpt-5.2",
  "usage": {
    "total_tokens": 38,
    "input_tokens": 8,
    "input_tokens_details": {
      "cached_tokens": 0
    },
    "output_tokens": 30,
    "output_tokens_details": {
      "reasoning_tokens": 0
    }
  },
  "created_at": 1767498805,
  "status": "completed",
  "background": false,
  "content_filters": null,
  "error": null,
  "incomplete_details": null,
  "instructions": null,
  "max_output_tokens": null,
  "max_tool_calls": null,
  "output": [
    {
      "id": "msg_028de2c59db26ba2006959e4359128819486d1d0c2ae49e660",
      "type": "message",
      "status": "completed",
      "content": [
        {
          "type": "output_text",
          "annotations": [],
          "logprobs": [],
          "text": "你好！有什么我可以帮你的吗？如果你愿意，可以告诉我你想聊的话题或需要解决的问题。"
        }
      ],
      "role": "assistant"
    }
  ],
  "parallel_tool_calls": true,
  "previous_response_id": null,
  "prompt_cache_key": null,
  "prompt_cache_retention": null,
  "reasoning": {
    "effort": "none",
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
  "tools": [],
  "top_logprobs": 0,
  "top_p": 0.98,
  "truncation": "disabled",
  "user": null,
  "metadata": {}
}
```
:::

## 注意事项

1. **API密钥安全**: 请妥善保管您的API密钥,不要泄露
2. **测试建议**: 建议在正式环境前先进行测试调用
3. **技术支持**: 如遇问题可联系 DMXAPI 技术支持

---

<p align="center">
  <small>© 2026 DMXAPI OpenAI 新接口</small>
</p>