# GPT-6 使用指南

本页介绍如何通过 DMXAPI 代理调用 GPT-6 Astra（模型 ID 为 `gpt-6-astra`），涵盖最小请求、推理强度控制、**缓存创建和读取（`prompt_cache_key`）**、Chat Completions 调用以及工具调用注意事项。模型能力与参数限制参照 Azure 官方规范，接入地址和鉴权使用 DMXAPI 约定。推理与工具结合的任务使用 **Responses API**。

:::warning API 密钥安全
示例从环境变量读取令牌。真实 DMXAPI 令牌只能保存在服务端环境变量或密钥管理系统中，不要写入文档、前端代码、公开仓库或日志。
:::

## 模型名称

| 模型 | 说明 |
|------|------|
| `gpt-6-astra` | GPT-6 Astra；本文参考的 Azure 模型版本为 `2026-09-03` |

模型版本及规格参见 [Azure GPT-6 Astra 模型卡](https://ai.azure.com/catalog/models/gpt-6-astra)与 [Azure API 和功能支持表](https://learn.microsoft.com/en-us/azure/foundry/openai/how-to/reasoning#api-and-feature-support)。输入、可见输出和推理 token 会共同占用可用预算；长输入或较高推理强度会减少剩余生成空间。生产环境应同时检查响应状态、结束原因和 token 使用量。

<a id="🔗-请求地址"></a>
<a id="responses-api"></a>
<a id="chat-completions-api"></a>

## 接口地址

| 接口 | 请求方式 | URL |
|------|---------|-----|
| Responses API | POST | `https://www.dmxapi.cn/v1/responses` |
| Chat Completions API | POST | `https://www.dmxapi.cn/v1/chat/completions` |

以下地址均为 DMXAPI 代理接口，请求中的模型名使用 `gpt-6-astra`。Azure 官方规范用于界定本文介绍的模型能力；代理渠道的实际可用性仍以 DMXAPI 提供的服务为准。

## 快速入门请求示例 {#快速入门}

先安装依赖（`requests` 写法只需 `requests`，SDK 写法只需 `openai`）：

```bash
python -m pip install --upgrade requests openai
```

在运行 Python 的同一个 PowerShell 窗口中设置环境变量，输入时不会显示令牌：

```powershell
$env:DMXAPI_API_KEY = [System.Net.NetworkCredential]::new("", (Read-Host "请输入 DMXAPI 令牌" -AsSecureString)).Password
```

以下完整 Python 示例均从 `DMXAPI_API_KEY` 读取令牌；未设置时会报 `KeyError`。下面的最小请求只传模型与输入，不显式设置推理强度和最大输出。

::: code-group

```python [SDK]
import os

from openai import OpenAI


client = OpenAI(
    api_key=(
        os.environ["DMXAPI_API_KEY"]
    ),
    base_url="https://www.dmxapi.cn/v1",
    timeout=180,
    max_retries=0,
)

response = client.responses.create(
    model="gpt-6-astra",
    input="请用三句话解释量子纠缠。",
)

print(response.output_text)
```

```python [requests]
import json
import os

import requests


response = requests.post(
    "https://www.dmxapi.cn/v1/responses",
    headers={
        "Authorization": f"Bearer {os.environ['DMXAPI_API_KEY']}",
        "Content-Type": "application/json",
    },
    json={
        "model": "gpt-6-astra",
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
  "model": "gpt-6-astra",
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

推理等级越高，通常会增加推理用量和延迟，应按自己的任务评测。按照 [Azure 推理功能说明](https://learn.microsoft.com/en-us/azure/foundry/openai/how-to/reasoning#gpt-5-and-gpt-6-reasoning-features)，GPT-6 Astra 的推理档位包括 `low`、`medium`、`high`、`xhigh`、`max`，其中 `max` 仅适用于 Responses API。

| 强度 | 使用建议 |
|------|----------|
| `low` | 轻量分析，关注延迟 |
| `medium` | 可作为常规任务的评测起点 |
| `high` | 复杂分析、规划、调试 |
| `xhigh` | 高难度、多约束任务 |
| `max` | 仅 Responses API；质量优先，需关注延迟和 token 用量 |

### 字段与端点规则

以下支持范围按 Azure 的 GPT-6 Astra 规范列出：

| 接口 | 参数写法 | 支持的推理档位 |
|------|----------|--------------------|
| Responses API | `reasoning={"effort": "..."}` | `low`、`medium`、`high`、`xhigh`、`max` |
| Chat Completions | `reasoning_effort="..."` | `low`、`medium`、`high`、`xhigh` |

需要固定推理强度时，请显式传入上表中的值。本文将 `medium` 作为可选的评测起点，不将其声明为 Azure GPT-6 Astra 的默认档位。

**GPT-6 Astra 不支持 `none`，两个端点都不要使用该值。** Chat Completions 不支持工具调用；需要工具时使用 Responses API，详见后面的“工具调用注意事项”。

### 参数限制

按照 [Azure 不支持的参数说明](https://learn.microsoft.com/en-us/azure/foundry/openai/how-to/reasoning#unsupported-parameters)，GPT-6 Astra 不支持自定义 `temperature`、`top_p`，也不支持 `logprobs`。本页示例不传这些参数。

### 按需添加的推理参数

以下只是参数片段，不能作为独立请求运行。需要指定推理强度时，将其加入上面的完整请求：SDK 片段作为调用参数，JSON 片段合并进请求体。`high` 适用于两个端点。

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

多轮对话时，每次请求都会带上之前的聊天记录。这些请求开头重复的内容，就叫作“公共前缀”。给这些请求设置相同的 `prompt_cache_key`，可以帮助它们到达保存了相同前缀缓存的服务节点，提高复用已有缓存的机会。首次请求只有符合服务端条件的前缀才可能**写入**缓存；后续请求只有命中已有前缀时才会**读取**缓存。

命中缓存后，模型可以复用前面已经完成的计算，减少处理重复内容的时间。[Azure 缓存说明](https://learn.microsoft.com/en-us/azure/foundry/openai/how-to/prompt-caching)指出，GPT-5.6 及后续模型的缓存读取可享受相应优惠，**缓存写入也可能收费**。通过 DMXAPI 调用时，实际费用以 DMXAPI 计费规则为准。

| 参数 | 类型 | 是否必填 | 取值或示例 | 说明 |
|------|------|---------|---------|------|
| `prompt_cache_key` | 字符串 | 否 | `"gpt6-chat-v1"` | 缓存标识，名称自定义；同一段连续对话中保持不变 |
| `prompt_cache_options.mode` | 字符串 | 否 | `"implicit"` / `"explicit"` | 默认为 `implicit`，下方代码使用此模式 |
| `prompt_cache_options.ttl` | 字符串 | 否 | `"30m"` | 默认且目前唯一支持的值；表示断点的最低缓存寿命，不是最长保留时间 |

Azure 对两种缓存模式的定义如下：

- `implicit`：默认模式，在最新消息上设置断点，同时使用请求中提供的显式断点。
- `explicit`：仅使用显式断点进行缓存读写；请求没有显式断点时，不进行缓存读写，也不产生缓存写入费用。

下方示例没有手动设置显式断点，使用 `implicit`。示例省略 `ttl`，按 Azure 定义使用默认的 `30m`；缓存可能保留更久，不能将其解释为 30 分钟后必然删除。

`gpt6-chat-v1` 是自己起的名字，可以直接照用，也可以换成便于识别的名称。它不是 API 密钥，也不负责保存聊天记录。**它是帮助缓存匹配的可选参数。** 不传它也可能使用自动缓存；设置它也不保证每次命中，输入前缀仍需匹配，并满足服务端的缓存条件。

<a id="调用示例"></a>

### 多轮对话代码

先完成“快速入门”中的依赖安装和环境变量设置。

两种写法的重点都是请求参数里的 `prompt_cache_key`，取值为 `gpt6-chat-v1`。程序从空白聊天开始，每轮只显示模型回答，并打印本轮缓存写入和读取的 token 数。

::: code-group

```python [requests]
import os

import requests

# DMXAPI Responses 接口地址
url = "https://www.dmxapi.cn/v1/responses"

# 从当前进程环境变量读取 DMXAPI 密钥
api_key = (
    os.environ["DMXAPI_API_KEY"]
)

headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {api_key}",
}


# ==================== 请求参数 ====================
def ask_model(history):
    payload = {
        # 使用的模型名称
        "model": "gpt-6-astra",

        # 本次问题和之前的完整对话
        "input": history,

        # 不保存服务端响应对象；这不会关闭提示词缓存
        # 本示例由 history 保存并传递聊天记录
        "store": False,

        # 兼容性参数：保留可供后续对话复用的加密推理项
        # 后面随完整输出一起保留即可，无需自行解读
        "include": ["reasoning.encrypted_content"],

        # 缓存标识：帮助共享相同前缀的请求匹配缓存
        # 名称可以自定义；同一对话中保持不变
        "prompt_cache_key": "gpt6-chat-v1",

        # implicit：默认模式，自动在最新消息上设置缓存断点
        "prompt_cache_options": {
            "mode": "implicit"
        },
    }

    response = requests.post(url, headers=headers, json=payload, timeout=180)

    # 非 2xx 状态码直接抛出异常，便于看到错误信息
    response.raise_for_status()
    result = response.json()
    if result.get("status") != "completed":
        raise RuntimeError(f"响应未完成：{result.get('status')}，详情：{result.get('incomplete_details')}")
    return result


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


def cache_tokens(result):
    """读取缓存用量；字段缺失时返回 None，表示未报告"""
    usage = result.get("usage") or {}
    details = usage.get("input_tokens_details") or {}
    return details.get("cache_write_tokens"), details.get("cached_tokens")


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

    # 显示模型回答与缓存用量；None 表示服务端未报告该字段
    print("\n助手：", extract_text(result))
    written, cached = cache_tokens(result)
    print(f"[缓存] cache_write_tokens = {written}, cached_tokens = {cached}")
```

```python [SDK]
import os

from openai import OpenAI

client = OpenAI(
    # 从当前进程环境变量读取 DMXAPI 密钥
    api_key=(
        os.environ["DMXAPI_API_KEY"]
    ),

    # DMXAPI 服务地址
    base_url="https://www.dmxapi.cn/v1",

    # 单次请求超时为 180 秒
    timeout=180,

    # 请求失败时不自动重试
    max_retries=0,
)


# ==================== 请求参数 ====================
def ask_model(history):
    return client.responses.create(
        # 使用的模型名称
        model="gpt-6-astra",

        # 本次问题和之前的完整对话
        input=history,

        # 不保存服务端响应对象；这不会关闭提示词缓存
        # 本示例由 history 保存并传递聊天记录
        store=False,

        # 兼容性参数：保留可供后续对话复用的加密推理项
        # 后面随完整输出一起保留即可，无需自行解读
        include=["reasoning.encrypted_content"],

        # 缓存标识：帮助共享相同前缀的请求匹配缓存
        # 名称可以自定义；同一对话中保持不变
        prompt_cache_key="gpt6-chat-v1",

        # 通过 extra_body 把额外参数传给服务端
        extra_body={
            "prompt_cache_options": {
                # implicit：默认模式，自动在最新消息上设置缓存断点
                "mode": "implicit"
            }
        },
    )


def cache_tokens(response):
    """读取缓存用量；字段缺失时返回 None，表示未报告"""
    details = getattr(response.usage, "input_tokens_details", None)
    return getattr(details, "cache_write_tokens", None), getattr(details, "cached_tokens", None)


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
    if response.status != "completed":
        raise RuntimeError(f"响应未完成：{response.status}，详情：{response.incomplete_details}")
    history.extend(item.model_dump(exclude_none=True) for item in response.output)

    # 显示模型回答与缓存用量；None 表示服务端未报告该字段
    print("\n助手：", response.output_text)
    written, cached = cache_tokens(response)
    print(f"[缓存] cache_write_tokens = {written}, cached_tokens = {cached}")
```

:::

### 运行效果

程序运行后，可以连续输入问题。下面仅展示交互形式，实际回答由模型生成，缓存用量数值仅为示意，是否命中以实际返回为准：

```text
你：请帮我制定一个学习 Python 的计划。
助手：<模型给出的学习计划>
[缓存] cache_write_tokens = 0, cached_tokens = 0

你：把第一天的安排详细展开。
助手：<模型根据前面的计划继续回答>
[缓存] cache_write_tokens = 0, cached_tokens = 0

你：每天只有一个小时，应该怎样调整？
助手：<模型结合之前的对话调整计划>
[缓存] cache_write_tokens = 0, cached_tokens = 0
```

这些请求都使用 `gpt6-chat-v1`，并通过 `history` 保留前面的问答，形成可复用的公共前缀。

<a id="如何确认缓存读取"></a>

### 如何确认缓存写入和读取

检查返回体的 `usage.input_tokens_details`：

- `cache_write_tokens > 0`：服务端报告本轮写入了缓存。
- `cached_tokens > 0`：服务端报告本轮读取了缓存。
- `cached_tokens = 0`：只能说明没有读取到缓存，**不能据此判断已创建缓存**。
- 字段缺失时，上面的程序显示 `None`（未报告），不能当成缓存用量为零。

按照 [Azure 缓存条件](https://learn.microsoft.com/en-us/azure/foundry/openai/how-to/prompt-caching#getting-started)，可复用前缀至少需要 1,024 个 token，且前缀内容必须相同。是否写入和命中以返回的用量字段为准；短对话完全可能连续返回 `0`。

### 注意事项

- **保持内容稳定**：新问题追加在后面，尽量不要改写前面的聊天记录；相同的缓存标识不能让不同内容自动匹配。
- **缓存标识与缓存模式**：`prompt_cache_key` 帮助匹配共享前缀，`prompt_cache_options.mode` 决定断点的使用方式；相同标识或使用 `implicit` 都不保证每次命中。
- **保留完整输出**：`store=False` 时，通过完整的 `output` 回传推理项和回答。[Azure 无状态推理说明](https://learn.microsoft.com/en-us/azure/foundry/openai/how-to/reasoning#preserve-reasoning-without-stored-responses)说明加密推理内容默认返回，示例保留 `include=["reasoning.encrypted_content"]` 作为兼容写法。
- **聊天记录仍要传递**：`history` 保存本次运行中的问答；固定缓存标识不会替代它。输入 `清空` 重新开始，输入 `退出` 结束；重启程序也会从空白开始。
- **上下文限制**：本示例不会自动压缩历史，长时间对话仍需留意上下文限制。“清空”只清除本程序的聊天记录，不会主动删除服务端缓存。

## Chat Completions API 请求示例

以下为 Chat Completions 的纯文本请求。按照 Azure GPT-6 Astra 规范，此接口不支持工具调用，也不支持 `max` 推理档位：

```python
import json
import os

import requests


response = requests.post(
    "https://www.dmxapi.cn/v1/chat/completions",
    headers={
        "Authorization": f"Bearer {os.environ['DMXAPI_API_KEY']}",
        "Content-Type": "application/json",
    },
    json={
        "model": "gpt-6-astra",
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
  "model": "gpt-6-astra",
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

按照 [Azure 工具调用说明](https://learn.microsoft.com/en-us/azure/foundry/openai/how-to/reasoning#tool-calling-with-reasoning-models)，**GPT-6 Astra 的工具调用必须使用 Responses API**。

Chat Completions 不支持 GPT-6 Astra 的工具调用；由于 Astra 不支持 `none`，也不能通过设置 `reasoning_effort="none"` 来启用 Chat 工具。已有 Chat 工具工作流需要迁移到 Responses API。

函数工具调用返回的是函数名称和参数，应用仍需执行相应函数、回传结果，才能完成整个工具流程。本页介绍接口选择与限制，没有演示完整的工具执行循环。

<p align="center">
  <small>© 2026 DMXAPI GPT-6 使用指南</small>
</p>
