# Gemini 3.8 Flash 思考总结

Gemini 3.8 Flash 可以在生成最终回答时返回**思考摘要**。通过 `include_thoughts=True` 请求摘要，再根据每个 Part 的 `thought` 标记，将摘要与最终答案分开显示。


## 先分清三个概念

| 概念 | 用途 | 是否直接展示 |
| --- | --- | --- |
| 思考等级 `thinking_level` | 控制模型投入的推理资源 | 作为应用配置 |
| 思考摘要 `thought=true` 的文本 Part | 提供模型返回的推理概要 | 可单独展示为摘要 |
| 思考签名 `thought_signature` / `thoughtSignature` | 在后续请求中保留推理与工具调用上下文 | 原样保存和回传，不作为正文展示 |

思考摘要是模型提供的概要，不是完整内部推理过程。摘要文本与最终回答应分别保存；没有摘要文本，也不能据此判断模型没有进行思考。

`include_thoughts=False` 只是不请求返回摘要，不会关闭模型的思考能力。签名也不依赖摘要是否显示：即使界面只显示最终答案，多轮对话仍应保留完整响应内容。

## 选择思考等级并请求摘要

3.8 Flash 支持以下三个等级，默认是 `medium`：

| 等级 | 建议场景 |
| --- | --- |
| `low` | 简单判断、内容整理、需要较快响应的交互 |
| `medium` | 常规代码分析、业务推理、多步骤处理 |
| `high` | 困难数学、复杂规划、需要更多推理的任务 |

`minimal` 不受 3.8 Flash 支持，会返回错误。使用 `thinking_level`，不要照搬 Gemini 2.5 的 `thinking_budget` 配置。

SDK 与 REST 的字段名称不同：

| 含义 | Python SDK | REST 请求体 |
| --- | --- | --- |
| 思考配置 | `config.thinking_config` | `generationConfig.thinkingConfig` |
| 思考等级 | `thinking_level` | `thinkingLevel` |
| 返回摘要 | `include_thoughts` | `includeThoughts` |
| 思考 token 数 | `usage_metadata.thoughts_token_count` | `usageMetadata.thoughtsTokenCount` |

以下 JSON 是**请求配置片段**，并不是服务返回示例：

```json
{
  "generationConfig": {
    "thinkingConfig": {
      "thinkingLevel": "medium",
      "includeThoughts": true
    },
    "maxOutputTokens": 8192
  }
}
```

## 非流式：一次取回摘要与最终答案

安装依赖，并在运行代码的终端中设置 `DMXAPI_API_KEY`。环境变量设置方式见[开发者指南](/gemini-3#安装依赖并设置密钥)。



### Python SDK

不要只读取 `response.text` 来寻找摘要，应遍历 `response.candidates[0].content.parts`，按 `part.thought` 分流。

```python
import os
from google import genai
from google.genai import types

client = genai.Client(
    api_key=os.environ["DMXAPI_API_KEY"],
    http_options=types.HttpOptions(
        base_url="https://www.dmxapi.cn",
        api_version="v1beta",
        timeout=120_000,
    ),
)
response = client.models.generate_content(
    model="gemini-3.8-flash",
    contents="比较 9.11 和 9.8 的大小，并给出简短理由。",
    config=types.GenerateContentConfig(
        thinking_config=types.ThinkingConfig(
            thinking_level="medium",
            include_thoughts=True,
        ),
        max_output_tokens=8192,
    ),
)

if not response.candidates:
    raise RuntimeError(f"未返回候选内容：{response.prompt_feedback}")
candidate = response.candidates[0]
parts = candidate.content.parts or [] if candidate.content else []
summary = "".join(part.text or "" for part in parts if part.thought)
answer = "".join(part.text or "" for part in parts if not part.thought)

print("=== 思考摘要 ===")
print(summary or "本次未返回可显示的思考摘要。")
if not answer.strip():
    raise RuntimeError(f"未返回最终答案，finish_reason={candidate.finish_reason}")
print("\n=== 最终答案 ===")
print(answer)
print("\n结束原因：", candidate.finish_reason)

usage = response.usage_metadata
if usage:
    print("思考 tokens：", usage.thoughts_token_count)
    print("回答 tokens：", usage.candidates_token_count)
    print("总 tokens：", usage.total_token_count)
```

摘要可能使用与最终答案不同的语言，也可能为空。应用应保留模型实际返回的内容，不要在未返回摘要时自行生成一段文字并标为模型思考。

### REST / Requests

REST 的正文和摘要位于 `candidates[0].content.parts`，通过 `thought` 布尔值区分。只有签名而没有 `text` 的 Part 不应被打印为 `None`。

```python
import os
import requests

response = requests.post(
    "https://www.dmxapi.cn/v1beta/models/gemini-3.8-flash:generateContent",
    headers={"x-goog-api-key": os.environ["DMXAPI_API_KEY"]},
    json={
        "contents": [{
            "role": "user",
            "parts": [{"text": "比较 9.11 和 9.8 的大小，并给出简短理由。"}],
        }],
        "generationConfig": {
            "thinkingConfig": {
                "thinkingLevel": "medium",
                "includeThoughts": True,
            },
            "maxOutputTokens": 8192,
        },
    },
    timeout=(10, 120),
)
response.raise_for_status()
data = response.json()
candidates = data.get("candidates") or []
if not candidates:
    raise RuntimeError(f"未返回候选内容：{data.get('promptFeedback')}")

candidate = candidates[0]
parts = (candidate.get("content") or {}).get("parts") or []
summary = "".join(part.get("text", "") for part in parts if part.get("thought"))
answer = "".join(part.get("text", "") for part in parts if not part.get("thought"))

print("=== 思考摘要 ===")
print(summary or "本次未返回可显示的思考摘要。")
if not answer.strip():
    raise RuntimeError(f"未返回最终答案，finishReason={candidate.get('finishReason')}")
print("\n=== 最终答案 ===")
print(answer)
print("\n结束原因：", candidate.get("finishReason"))
print("Token 用量：", data.get("usageMetadata", {}))
```

## 流式：按 Part 分流并检查结束状态

流式摘要可能分多次返回。不要假设“第一个 chunk 是摘要，其余全部是答案”，也不要因为某个 chunk 没有文本就停止读取。

下面的示例按接收顺序显示内容，同时分别累积摘要和答案。最终只有正常结束且存在答案时，才将整次请求视为完成。

```python
import os
from google import genai
from google.genai import types

client = genai.Client(
    api_key="sk--------------------------------",
    http_options=types.HttpOptions(
        base_url="https://www.dmxapi.cn",
        api_version="v1beta",
        timeout=120_000,
    ),
)
stream = client.models.generate_content_stream(
    model="gemini-3.8-flash",
    contents="比较 9.11 和 9.8 的大小，并给出简短理由。",
    config=types.GenerateContentConfig(
        thinking_config=types.ThinkingConfig(
            thinking_level="medium",
            include_thoughts=True,
        ),
        max_output_tokens=8192,
    ),
)

summary_parts = []
answer_parts = []
active_section = None
finish_reason = None
usage = None

for chunk in stream:
    if chunk.usage_metadata:
        usage = chunk.usage_metadata
    if not chunk.candidates:
        continue
    candidate = chunk.candidates[0]
    if candidate.finish_reason:
        finish_reason = candidate.finish_reason.value
    parts = candidate.content.parts or [] if candidate.content else []
    for part in parts:
        if not part.text:
            continue  # 此处只处理显示文本，不用于构造下一轮历史
        section = "思考摘要" if part.thought else "最终答案"
        target = summary_parts if part.thought else answer_parts
        target.append(part.text)
        if section != active_section:
            print(f"\n=== {section} ===")
            active_section = section
        print(part.text, end="", flush=True)

print()
summary = "".join(summary_parts)
answer = "".join(answer_parts)
if not answer.strip():
    raise RuntimeError(f"流式请求没有返回最终答案，finish_reason={finish_reason}")
if finish_reason != "STOP":
    raise RuntimeError(f"流式结果未正常完成，finish_reason={finish_reason}")
if not summary:
    print("本次未返回可显示的思考摘要。")
print("结束原因：", finish_reason)
if usage:
    print("思考 tokens：", usage.thoughts_token_count)
    print("回答 tokens：", usage.candidates_token_count)
```

## 常见问题

| 现象 | 处理方式 |
| --- | --- |
| 有最终答案，但没有摘要 | 确认 `include_thoughts=True`、字段层级正确，并遍历全部 Part；仍无摘要时按实际结果显示 |
| `minimal` 报错 | 改为 `low`、`medium` 或 `high` |
| 想关闭思考 | 3.8 Flash 没有关闭思考的等级；需要较低开销时使用 `low` |
| 摘要有内容，最终答案为空 | 检查结束原因、输出预算和请求是否中断；摘要不能替代答案 |
| `MAX_TOKENS` | 结合实际用量增大输出上限，或降低思考等级、缩小任务 |
| 流式过程中没有文本 | 继续读取元数据和结束状态，避免丢掉只有签名或用量的块 |
| 多轮或工具调用返回 400 | 检查完整历史、调用标识、函数名与思考签名是否原样保留 |
| SDK 读取超时 | 记录异常与已收到的部分结果，检查客户端等待时间和渠道状态 |

<p align="center">
  <small>© 2026 DMXAPI Gemini 3.8 Flash 思考总结</small>
</p>
