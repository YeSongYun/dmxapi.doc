# GPT-6 使用指南

GPT-6 是 OpenAI 最新一代前沿模型。本页介绍如何通过 DMXAPI 调用 `gpt-6`，涵盖最小请求、推理强度控制、**缓存创建和读取（`prompt_cache_key`）**、Chat Completions 兼容调用以及工具调用注意事项。新项目、推理任务、工具调用和多轮工作流优先使用 **Responses API**。

:::warning API 密钥安全
示例令牌全部是不可用占位符。真实 DMXAPI 令牌只能保存在服务端环境变量或密钥管理系统中，不要写入文档、前端代码、公开仓库或日志。
:::

## 模型名称

| 模型 | 说明 |
|------|------|
| `gpt-6` | GPT-6 标准模型，支持 Responses 与 Chat Completions 两种接口 |

上下文窗口、最大输出、训练数据截止等规格以 OpenAI 官方模型页与 DMXAPI 模型列表为准，本页不再单独罗列。输入、可见输出和推理 token 会共同占用可用预算；长输入或较高推理强度会减少剩余生成空间。生产环境应同时检查响应状态、结束原因和 token 使用量。

## 🔗 请求地址

### Responses API

```text
https://www.dmxapi.cn/v1/responses
```

### Chat Completions API

```text
https://www.dmxapi.cn/v1/chat/completions
```

## 快速入门

下面是最小可运行请求，只传模型与输入，不显式设置推理强度和最大输出。

::: code-group

```python [SDK]
from openai import OpenAI


client = OpenAI(
    api_key="sk-***************************************",
    base_url="https://www.dmxapi.cn/v1",
)

response = client.responses.create(
    model="gpt-6",
    input="请用三句话解释量子纠缠。",
)

print(response.output_text)
```

```python [requests]
import json

import requests


response = requests.post(
    "https://www.dmxapi.cn/v1/responses",
    headers={
        "Authorization": "sk-***************************************",
        "Content-Type": "application/json",
    },
    json={
        "model": "gpt-6",
        "input": "请用三句话解释量子纠缠。",
    },
    timeout=180,
)
response.raise_for_status()
print(json.dumps(response.json(), indent=2, ensure_ascii=False))
```

:::

## 返回示例

以下为结构示意，ID 与用量数值均为合成值；实际响应还可能包含推理项：

```json
{
  "id": "resp_example_gpt6_quickstart_001",
  "object": "response",
  "status": "completed",
  "model": "gpt-6",
  "output": [
    {
      "type": "message",
      "role": "assistant",
      "content": [
        {
          "type": "output_text",
          "text": "量子纠缠描述了多个粒子之间不可独立分割的量子关联。"
        }
      ]
    }
  ],
  "usage": {
    "input_tokens": 18,
    "input_tokens_details": {
      "cached_tokens": 0
    },
    "output_tokens": 64,
    "total_tokens": 82
  }
}
```

## 推理强度控制

推理等级越高，模型通常会投入更多推理 token，质量上限可能提高，但延迟与用量也会增加。下表档位与端点规则与 GPT-5.6 系列一致；GPT-6 实际支持范围以 OpenAI 官方与 DMXAPI 模型列表为准。

| 强度 | 推荐用途 | 选择建议 |
|------|----------|----------|
| `none` | 简单问答、抽取、分类、格式转换 | 最低延迟基线；不进行额外推理 |
| `low` | 轻量分析、常规代码修改 | 延迟敏感且需要少量推理时使用 |
| `medium` | 通用生产任务 | 默认值，建议作为首个评测基线 |
| `high` | 复杂分析、规划、调试 | 只有评测确认质量提升时再提高 |
| `xhigh` | 高难度、多约束问题 | 面向质量优先任务，关注延迟和 token |
| `max` | 最困难、需要充分探索与复核的任务 | 仅 Responses API；应与 `xhigh` 做对照评测 |

### 字段与端点规则

| 接口 | 参数写法 | 支持范围 | 重要限制 |
|------|----------|----------|----------|
| Responses API | `reasoning={"effort": "..."}` | `none`、`low`、`medium`、`high`、`xhigh`、`max` | 推荐用于推理与工具组合 |
| Chat Completions | `reasoning_effort="..."` | `none`、`low`、`medium`、`high`、`xhigh` | `max` 不适用于该接口 |

如果省略推理强度，默认使用 `medium`。Chat Completions 请求一旦携带 `tools`，必须显式设置 `reasoning_effort="none"`；需要模型先推理再调用工具时，应改用 Responses API。

### 按需添加的推理参数

只有业务需要覆盖默认 `medium` 时，才把对应片段加入请求。

::: code-group

```python [Responses SDK]
reasoning={"effort": "high"}
```

```json [Responses requests]
{
  "reasoning": {
    "effort": "high"
  }
}
```

```python [Chat Completions]
reasoning_effort="high"
```

:::

## 缓存创建和读取（prompt_cache_key）

多轮对话时，每次请求都会带上之前的聊天记录。这些请求开头重复的内容，就叫作“公共前缀”。给这些请求设置相同的 `prompt_cache_key`，可以帮助它们到达保存了相同前缀缓存的服务节点，提高复用已有缓存的机会。首轮请求会**创建**缓存，后续携带相同前缀与相同缓存标识的请求则**读取**缓存。

命中缓存后，模型可以复用前面已经完成的计算，减少处理重复内容的时间；重复输入也可按缓存价格计费，实际费用以所用服务为准。

| 参数 | 类型 | 是否必填 | 本页示例 | 说明 |
|------|------|---------|---------|------|
| `prompt_cache_key` | 字符串 | 否 | `"gpt6-chat-v1"` | 缓存标识，名称自定义；同一段连续对话中保持不变 |
| `prompt_cache_options.mode` | 字符串 | 否 | `"implicit"` | 自动在最新符合条件的消息末尾设置缓存断点，无需手动标记 |

`gpt6-chat-v1` 是自己起的名字，可以直接照用，也可以换成便于识别的名称。它不是 API 密钥，也不负责保存聊天记录。**它是帮助缓存匹配的可选参数。** 不传它也可能使用自动缓存；设置它也不保证每次命中，输入前缀仍需匹配，并满足服务端的缓存条件。

### 调用示例

先安装依赖（`requests` 写法只需 `requests`，SDK 写法只需 `openai`）：

```bash
python -m pip install --upgrade requests openai
```

两种写法的重点都是请求参数里的 `prompt_cache_key`，取值为 `gpt6-chat-v1`。程序从空白聊天开始，每轮只显示模型回答，并打印本轮读取到的缓存 token 数。

::: code-group

```python [requests]
import requests

# DMXAPI Responses 接口地址
url = "https://www.dmxapi.cn/v1/responses"

# 替换为你自己的 DMXAPI 密钥
api_key = "sk-******************************************"

headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {api_key}",
}


# ==================== 请求参数 ====================
def ask_model(history):
    payload = {
        # 使用的模型名称
        "model": "gpt-6",

        # 本次问题和之前的完整对话
        "input": history,

        # 不保存服务端响应对象；这不会关闭提示词缓存
        # 本示例由 history 保存并传递聊天记录
        "store": False,

        # 请求返回可供后续对话复用的加密推理项
        # 后面随完整输出一起保留即可，无需自行解读
        "include": ["reasoning.encrypted_content"],

        # 缓存标识：帮助共享相同前缀的请求匹配缓存
        # 名称可以自定义；同一对话中保持不变
        "prompt_cache_key": "gpt6-chat-v1",

        # implicit：自动在最新符合条件的消息末尾设置缓存断点
        "prompt_cache_options": {
            "mode": "implicit"
        },
    }

    response = requests.post(url, headers=headers, json=payload)

    # 非 2xx 状态码直接抛出异常，便于看到错误信息
    response.raise_for_status()
    return response.json()


def extract_text(result):
    """从返回的 output 列表中拼出模型的文本回答"""
    chunks = []
    for item in result.get("output", []):
        if item.get("type") != "message":
            continue
        for part in item.get("content", []):
            if part.get("type") == "output_text":
                chunks.append(part.get("text", ""))
    return "".join(chunks)


def cached_tokens(result):
    """读取本轮命中缓存的输入 token 数；字段缺失时按 0 处理"""
    usage = result.get("usage", {})
    return usage.get("input_tokens_details", {}).get("cached_tokens", 0)


# 启动时没有历史对话
history = []

print("缓存创建和读取示例：输入问题后按回车。")
print("输入“清空”重新开始；输入“退出”结束。")

while True:
    question = input("\n你：").strip()

    if question == "退出":
        break

    if question == "清空":
        history = []
        print("已清空当前对话。")
        continue

    if not question:
        continue

    # 把本次问题追加到聊天记录后面
    history.append({
        "role": "user",
        "content": question,
    })

    # 把完整聊天记录发送给模型
    result = ask_model(history)

    # 保留完整输出，下一轮连同之前的问答一起发送
    history.extend(result["output"])

    # 只显示模型回答，并显示本轮读取到的缓存 token 数
    print("\n助手：", extract_text(result))
    print(f"[缓存读取] cached_tokens = {cached_tokens(result)}")
```

```python [SDK]
from openai import OpenAI

client = OpenAI(
    # 替换为你自己的 DMXAPI 密钥
    api_key="sk-******************************************",

    # DMXAPI 服务地址
    base_url="https://www.dmxapi.cn/v1",

    # 请求失败时不自动重试
    max_retries=0,
)


# ==================== 请求参数 ====================
def ask_model(history):
    return client.responses.create(
        # 使用的模型名称
        model="gpt-6",

        # 本次问题和之前的完整对话
        input=history,

        # 不保存服务端响应对象；这不会关闭提示词缓存
        # 本示例由 history 保存并传递聊天记录
        store=False,

        # 请求返回可供后续对话复用的加密推理项
        # 后面随完整输出一起保留即可，无需自行解读
        include=["reasoning.encrypted_content"],

        # 缓存标识：帮助共享相同前缀的请求匹配缓存
        # 名称可以自定义；同一对话中保持不变
        prompt_cache_key="gpt6-chat-v1",

        # 通过 extra_body 把额外参数传给服务端
        extra_body={
            "prompt_cache_options": {
                # implicit：自动在最新符合条件的消息末尾设置缓存断点
                "mode": "implicit"
            }
        },
    )


def cached_tokens(response):
    """读取本轮命中缓存的输入 token 数；字段缺失时按 0 处理"""
    details = getattr(response.usage, "input_tokens_details", None)
    return getattr(details, "cached_tokens", 0) or 0


# 启动时没有历史对话
history = []

print("缓存创建和读取示例：输入问题后按回车。")
print("输入“清空”重新开始；输入“退出”结束。")

while True:
    question = input("\n你：").strip()

    if question == "退出":
        break

    if question == "清空":
        history = []
        print("已清空当前对话。")
        continue

    if not question:
        continue

    # 把本次问题追加到聊天记录后面
    history.append({
        "role": "user",
        "content": question,
    })

    # 把完整聊天记录发送给模型
    response = ask_model(history)

    # 保留完整输出，下一轮连同之前的问答一起发送
    history.extend(response.output)

    # 只显示模型回答，并显示本轮读取到的缓存 token 数
    print("\n助手：", response.output_text)
    print(f"[缓存读取] cached_tokens = {cached_tokens(response)}")
```

:::

### 运行效果

程序运行后，可以连续输入问题。下面仅展示交互形式，实际回答由模型生成，`cached_tokens` 数值仅为示意，是否命中以实际返回为准：

```text
你：请帮我制定一个学习 Python 的计划。
助手：<模型给出的学习计划>
[缓存读取] cached_tokens = 0

你：把第一天的安排详细展开。
助手：<模型根据前面的计划继续回答>
[缓存读取] cached_tokens = 1280

你：每天只有一个小时，应该怎样调整？
助手：<模型结合之前的对话调整计划>
[缓存读取] cached_tokens = 2048
```

这些请求都使用 `gpt6-chat-v1`，并通过 `history` 保留前面的问答，形成可复用的公共前缀。

### 如何确认缓存读取

返回体 `usage.input_tokens_details.cached_tokens` 表示本轮从缓存读取的输入 token 数：

- 首轮请求通常为 `0`，此时缓存被**创建**；
- 后续轮次若大于 `0`，说明已**读取**到缓存；
- 短对话可能仍为 `0`，因为缓存有最小长度等条件；部分返回可能省略 `input_tokens_details`，示例代码已按 `0` 处理。

### 注意事项

- **保持内容稳定**：新问题追加在后面，尽量不要改写前面的聊天记录；相同的缓存标识不能让不同内容自动匹配。
- **两个参数各有用途**：`prompt_cache_key` 帮助匹配缓存，`implicit` 自动选择缓存前缀的结束位置，本示例无需手动标记。
- **聊天记录仍要传递**：`history` 保存本次运行中的问答；固定缓存标识不会替代它。输入 `清空` 重新开始，输入 `退出` 结束；重启程序也会从空白开始。
- **上下文限制**：本示例不会自动压缩历史，长时间对话仍需留意上下文限制。“清空”只清除本程序的聊天记录，不会主动删除服务端缓存。

## Chat Completions API 请求示例

Chat Completions 适合兼容已有项目，但部分推理与工具组合受到限制：

```python
import json

import requests


response = requests.post(
    "https://www.dmxapi.cn/v1/chat/completions",
    headers={
        "Authorization": "sk-***************************************",
        "Content-Type": "application/json",
    },
    json={
        "model": "gpt-6",
        "messages": [
            {
                "role": "user",
                "content": "请用三句话解释量子纠缠。",
            }
        ],
    },
    timeout=180,
)
response.raise_for_status()
print(json.dumps(response.json(), indent=2, ensure_ascii=False))
```

## Chat Completions 返回示例

```json
{
  "id": "chatcmpl_example_gpt6_quickstart_001",
  "object": "chat.completion",
  "model": "gpt-6",
  "choices": [
    {
      "index": 0,
      "message": {
        "role": "assistant",
        "content": "量子纠缠描述了多个粒子之间不可独立分割的量子关联。"
      },
      "finish_reason": "stop"
    }
  ]
}
```

## 工具调用注意事项

在 Chat Completions 中不能同时使用工具与非 `none` 推理强度：

```json
{
  "reasoning_effort": "none",
  "tools": [
    {
      "type": "function",
      "function": {
        "name": "get_weather"
      }
    }
  ]
}
```

需要 `low` 到 `max` 推理强度并结合工具时，请使用 Responses API。这样还可以携带推理项处理后续回合。

<p align="center">
  <small>© 2026 DMXAPI GPT-6 使用指南</small>
</p>
