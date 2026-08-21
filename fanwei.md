# API 统一请求格式

DMXAPI 代理将多种模型统一为 OpenAI 兼容请求格式。下面以 `gpt-5.6-sol` 演示 Chat Completions 的最小调用；使用其他兼容模型时，代理地址保持不变，但请求参数仍需按对应模型文档调整。

## 接口地址

| 接口 | 请求方式 | URL |
|------|---------|-----|
| 创建聊天补全 | POST | `https://www.dmxapi.cn/v1/chat/completions` |

:::warning API 密钥安全
请将占位符替换为自己的 DMXAPI 令牌。不要在客户端代码、公开仓库或日志中暴露真实令牌。
:::

## 模型名称

- 本页示例：`gpt-5.6-sol`
- 其他模型：替换 `model`，并检查该模型对推理、输出长度和工具参数的支持情况

## Python 示例代码

```python
import json

import requests


url = "https://www.dmxapi.cn/v1/chat/completions"
headers = {
    "Authorization": "sk-***************************************",
    "Content-Type": "application/json",
}
payload = {
    "model": "gpt-5.6-sol",
    "messages": [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "周树人和鲁迅是兄弟吗？"},
    ],
    # GPT-5.6 官方默认值为 medium；普通问答可显式设为 none 降低延迟。
    "reasoning_effort": "none",
    "max_completion_tokens": 256,
}

response = requests.post(url, headers=headers, json=payload, timeout=120)
response.raise_for_status()
print(json.dumps(response.json(), indent=2, ensure_ascii=False))
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

2026-08-21 将上述通用组代码中的 `model` 单独替换为 `deepseek-v4-flash-0731` 后，逐代码实测结果如下：

| 代码类型 | 结果 |
|----------|------|
| 非流式 requests、SDK | 通过 |
| 流式 requests | 通过 |
| Pydantic 结构化输出 | 通过 |
| 函数调用 | 通过 |
| requests、SDK 多轮对话 | 通过 |
| 网络图片、Base64 图片 | 不兼容；接口返回 HTTP 400、错误码 10305 |

`deepseek-v4-flash-0731` 在本轮测试中不接受图片输入，因此图片分析代码继续使用页面注明的 `gpt-5.6-sol`。这属于替代模型能力边界，不代表 Chat Completions 请求格式或图片代码失效。

<p align="center">
  <small>© 2026 DMXAPI API 统一请求格式</small>
</p>
