# GPT-6 使用指南

本页介绍如何通过 DMXAPI 代理调用 OpenAI 的 GPT-6 Astra（模型 ID 为 `gpt-6-astra`），涵盖最小请求、推理强度控制、**缓存创建和读取（`prompt_cache_key`）**、Chat Completions 兼容调用以及工具调用注意事项。新项目、推理任务、工具调用和多轮工作流优先使用 **Responses API**。

:::warning API 密钥安全
示例从环境变量读取令牌。真实 DMXAPI 令牌只能保存在服务端环境变量或密钥管理系统中，不要写入文档、前端代码、公开仓库或日志。
:::

## 模型名称

| 模型 | 说明 |
|------|------|
| `gpt-6-astra` | GPT-6 Astra；本页两个接口均已通过 DMXAPI 实测 |

上下文窗口、最大输出、训练数据截止等规格以 OpenAI 官方模型页与 DMXAPI 模型列表为准，本页不再单独罗列。输入、可见输出和推理 token 会共同占用可用预算；长输入或较高推理强度会减少剩余生成空间。生产环境应同时检查响应状态、结束原因和 token 使用量。

<a id="🔗-请求地址"></a>
<a id="responses-api"></a>
<a id="chat-completions-api"></a>

## 接口地址

| 接口 | 请求方式 | URL |
|------|---------|-----|
| Responses API | POST | `https://www.dmxapi.cn/v1/responses` |
| Chat Completions API | POST | `https://www.dmxapi.cn/v1/chat/completions` |

以下地址均为 DMXAPI 代理接口；上游规范与代理实际行为有差异时，本页分别说明。请求中的模型名使用 `gpt-6-astra`，响应可能返回带日期或渠道前缀的实际模型名。

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

推理等级越高，通常会增加推理用量和延迟，应按自己的任务评测。OpenAI 的 [GPT-6 Astra 模型页](https://developers.openai.com/api/docs/models/gpt-6-astra)列出的等级是 `low`、`medium`、`high`、`xhigh`、`max`。

| 强度 | 使用建议 |
|------|----------|
| `low` | 轻量分析，关注延迟 |
| `medium` | 可作为常规任务的评测起点 |
| `high` | 复杂分析、规划、调试 |
| `xhigh` | 高难度、多约束任务 |
| `max` | 质量优先，需关注延迟和 token 用量 |

### 字段与端点规则

以下是 **2026-09-08 使用 DMXAPI 的实测结果**，不代表所有账号或后续渠道配置：

| 接口 | 参数写法 | 已通过的文本请求档位 |
|------|----------|--------------------|
| Responses API | `reasoning={"effort": "..."}` | `low`、`medium`、`high`、`xhigh`、`max` |
| Chat Completions | `reasoning_effort="..."` | `low`、`medium`、`high`、`xhigh`、`max` |

本次省略推理强度的 Responses 请求回显 `reasoning.effort="medium"`；Chat 响应没有回显该字段，不能据此确认其默认值。**Chat Completions 的 `max` 已实测成功，并非仅限 Responses。**

DMXAPI 本次还接受了两个端点的 `none` 请求，但 OpenAI 的 [Astra 推理说明](https://developers.openai.com/api/docs/guides/reasoning#reasoning-effort)明确不支持 `none`。因此 `none` 仅作为本次代理兼容性结果记录，不作为上游通用能力或长期保证；常规示例省略该参数，或使用上表档位。

### 按需添加的推理参数

以下只是参数片段，不能作为独立请求运行。需要指定推理强度时，将其加入上面的完整请求：SDK 片段作为调用参数，JSON 片段合并进请求体。`high` 已在两个端点实测通过。

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

命中缓存后，模型可以复用前面已经完成的计算，减少处理重复内容的时间；重复输入也可按缓存价格计费，实际费用以所用服务为准。

| 参数 | 类型 | 是否必填 | 本页示例 | 说明 |
|------|------|---------|---------|------|
| `prompt_cache_key` | 字符串 | 否 | `"gpt6-chat-v1"` | 缓存标识，名称自定义；同一段连续对话中保持不变 |
| `prompt_cache_options.mode` | 字符串 | 否 | `"implicit"` | 上游定义的隐式缓存模式，在最新符合条件的 user/tool 消息末尾设置断点；本次 DMXAPI 请求已接受该参数 |

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

OpenAI 的 [Prompt caching 说明](https://developers.openai.com/api/docs/guides/prompt-caching)将 GPT-5.6 及后续模型的最低可缓存前缀设为 1,024 个可见输入 token；DMXAPI 是否写入和命中仍以返回的用量字段为准。短对话完全可能连续返回 `0`。

### 注意事项

- **保持内容稳定**：新问题追加在后面，尽量不要改写前面的聊天记录；相同的缓存标识不能让不同内容自动匹配。
- **两个参数各有用途**：`prompt_cache_key` 帮助路由匹配，`implicit` 的上游含义是自动选择缓存断点。请求接受该字段并不能单独证明代理按该字段执行，本示例通过返回的用量观察缓存。
- **聊天记录仍要传递**：`history` 保存本次运行中的问答；固定缓存标识不会替代它。输入 `清空` 重新开始，输入 `退出` 结束；重启程序也会从空白开始。
- **上下文限制**：本示例不会自动压缩历史，长时间对话仍需留意上下文限制。“清空”只清除本程序的聊天记录，不会主动删除服务端缓存。

## Chat Completions API 请求示例

以下为已经通过 DMXAPI 实测的纯文本请求。涉及工具时，请同时阅读后面的代理兼容性说明：

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

OpenAI 的 [GPT-6 Astra 指南](https://developers.openai.com/api/docs/guides/latest-model#update-api-and-model-parameters)要求工具调用使用 Responses API。本次 DMXAPI 验证中，Responses 携带函数工具与 `reasoning={"effort": "low"}`，成功返回 `function_call`。

DMXAPI 的 Chat 兼容行为需单独看待：本次同一函数工具请求使用 `reasoning_effort="low"` 返回 HTTP 400，改为 `reasoning_effort="none"` 后返回 `finish_reason="tool_calls"`。这仅证明当前代理配置接受该组合，不代表上游 Astra 支持，也不保证其他渠道一致。新项目的工具调用建议使用 Responses。

工具调用返回的是函数名称和参数，应用仍需执行相应函数、回传结果，才能完成整个工具流程。本页只验证工具调用的生成，没有演示完整的工具执行循环。

<p align="center">
  <small>© 2026 DMXAPI GPT-6 使用指南</small>
</p>
