# API 统一请求格式

DMXAPI 代理将多种模型统一为 OpenAI 兼容请求格式。下面以 `gpt-5.6-sol` 演示 Chat Completions 的最小调用；使用其他兼容模型时，代理地址保持不变，但请求参数仍需按对应模型文档调整。

## 🔗 请求地址

```text
https://www.dmxapi.cn/v1/chat/completions
```

:::warning API 密钥安全
请将占位符替换为自己的 DMXAPI 令牌。不要在客户端代码、公开仓库或日志中暴露真实令牌。
:::

## 模型名称

- 本页示例：`gpt-5.6-sol`
- 其他模型：替换 `model`，并检查该模型对推理、输出长度和工具参数的支持情况

## Python 示例代码

```python
"""
DMXAPI 对话接口调用示例
功能：使用 gpt-5.6-sol 模型进行智能对话
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
    "model": "gpt-5.6-sol",  # 选择使用的模型
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

## 返回示例

以下结构依据 DMXAPI 实测结果整理，ID 与时间戳为虚构值。Chat Completions 可能返回带日期的模型快照名：

```json
{
  "id": "chatcmpl_example_gpt56_001",
  "object": "chat.completion",
  "created": 1787270400,
  "model": "gpt-5.6-sol-2026-07-09",
  "choices": [
    {
      "index": 0,
      "message": {
        "role": "assistant",
        "content": "不是。周树人是鲁迅的本名，鲁迅是他的笔名。"
      },
      "finish_reason": "stop"
    }
  ],
  "usage": {
    "prompt_tokens": 27,
    "completion_tokens": 26,
    "total_tokens": 53
  }
}
```

## DeepSeek 替换模型二次验收

2026-08-21 先使用文档模型 `gpt-5.6-sol` 逐一执行通用组 10 个实现，非流式、流式、结构化输出、图片、函数调用和多轮对话全部通过。随后将代码中的 `model` 单独替换为 `deepseek-v4-flash-0731`，结果如下：

| 代码类型 | 结果 |
|----------|------|
| 非流式 requests、SDK | 通过 |
| 流式 requests | 通过 |
| Pydantic 结构化输出 | 通过 |
| 函数调用 | 通过 |
| requests、SDK 多轮对话 | 通过 |
| 网络图片、Base64 图片 | 不兼容；接口返回 HTTP 400、错误码 10305 |

`deepseek-v4-flash-0731` 在本轮测试中不接受图片输入，因此图片分析代码继续使用页面注明的 `gpt-5.6-sol`。这属于替代模型能力边界，不代表 Chat Completions 请求格式或图片代码失效。

## Qwen3.8 Max 二次验收

2026-08-21 将通用 Chat Completions 组中每个独立实现的 `model` 临时替换为 `qwen3.8-max`，在不改变请求语义的前提下逐代码执行。返回模型名与请求模型或网关规范化别名相符，10 个实现全部通过：

| 文档与代码类型 | 验收条件 | 结果 |
|----------------|----------|------|
| `fanwei.md` requests 非流式 | 返回非空文本 | 通过 |
| `openai-chat.md` SDK | 返回非空文本 | 通过 |
| `openai-chat.md` requests | 返回非空文本 | 通过 |
| `openai-chat-stream.md` requests 流式 | 收到文本增量并正常结束 | 通过 |
| `openai-json.md` Pydantic 结构化输出 | 得到非空 `ProductInfo` | 通过 |
| `url-image.md` 网络图片 | 正确识别 Python 标志 | 通过 |
| `base64-image.md` Base64 图片 | 正确识别红色箭头指向“添加供应商” | 通过 |
| `function-call.md` 函数调用 | 返回指定工具名和可解析参数 | 通过 |
| `gpt-5.4_Multi-turn-dialogue.md` requests | 第二轮正确召回“蓝鲸” | 通过 |
| `gpt-5.4_Multi-turn-dialogue.md` SDK | 第二轮正确召回“蓝鲸” | 通过 |

“Openai 请求格式（新）”中本轮受影响的 11 个安全调用实现也已逐一执行：Responses SDK/requests 非流式、两种流式、网络图片、Base64 图片、PDF 文件、函数调用、两种推理摘要示例及 GPT-5.1 快速调用均通过。

Embedding、视频、STT、TTS、绘图和 GPT-5.2 Pro 页面使用专用端点或固定模型，不属于“仅替换聊天模型即可验证”的通用组，因此没有强行改成 `qwen3.8-max`。这避免把端点与模型类型不匹配造成的失败误判为代码错误。

<p align="center">
  <small>© 2026 DMXAPI API 统一请求格式</small>
</p>
