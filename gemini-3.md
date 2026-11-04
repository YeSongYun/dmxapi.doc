# Gemini 3.8 Flash 开发者指南

`gemini-3.8-flash` 面向代码开发、多步骤工具调用和复杂业务处理，也支持图片、音频、视频与 PDF 理解。本指南按“建立连接 → 选择输出方式 → 处理媒体 → 管理对话和工具 → 迁移排错”的流程介绍接入方法。

## 先确认模型与接口

| 项目 | Gemini 3.8 Flash |
| --- | --- |
| 模型 ID | `gemini-3.8-flash` |
| 输入 | 文本、图片、音频、视频、PDF |
| 输出 | 文本，包括符合 JSON Schema 的结构化文本 |
| 官方输入上限 | 1,048,576 tokens |
| 官方输出上限 | 65,536 tokens |
| 思考等级 | `low`、`medium`、`high`，默认 `medium` |
| 常用能力 | 流式输出、函数调用、搜索 grounding、结构化输出 |
| 不支持的输出方式 | 图片生成、音频生成、Live API |

| 调用方式 | DMXAPI 地址 |
| --- | --- |
| 非流式生成 | `POST https://www.dmxapi.cn/v1beta/models/gemini-3.8-flash:generateContent` |
| 流式生成 | `POST https://www.dmxapi.cn/v1beta/models/gemini-3.8-flash:streamGenerateContent?alt=sse` |
| Google GenAI SDK | `base_url="https://www.dmxapi.cn"`，`api_version="v1beta"` |

## 建立第一个连接

### 安装依赖并设置密钥

使用 Google GenAI SDK `google-genai`，结构化输出示例另外使用 Pydantic。

```bash
pip install -U google-genai requests pydantic
```

在当前终端设置 `DMXAPI_API_KEY`，然后在同一终端运行示例。

::: code-group

```powershell [Windows PowerShell]
$env:DMXAPI_API_KEY = "填写你的 DMXAPI Key"
```

```bash [macOS / Linux]
export DMXAPI_API_KEY="填写你的 DMXAPI Key"
```

:::

### Python SDK


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
    contents="用三句话解释什么是 API，并举一个日常使用的例子。",
    config=types.GenerateContentConfig(
        thinking_config=types.ThinkingConfig(thinking_level="medium"),
        max_output_tokens=8192,
    ),
)

if not response.text:
    raise RuntimeError("未返回文本，请检查 candidates、finish_reason 和 prompt_feedback。")
print(response.text)
```

### REST / Requests

```python
import os
import requests

url = "https://www.dmxapi.cn/v1beta/models/gemini-3.8-flash:generateContent"
payload = {
    "contents": [{
        "role": "user",
        "parts": [{"text": "用三句话解释什么是 API，并举一个日常使用的例子。"}],
    }],
    "generationConfig": {
        "thinkingConfig": {"thinkingLevel": "medium"},
        "maxOutputTokens": 8192,
    },
}

response = requests.post(
    url,
    headers={"x-goog-api-key": os.environ["DMXAPI_API_KEY"]},
    json=payload,
    timeout=(10, 120),
)
response.raise_for_status()
data = response.json()
candidates = data.get("candidates") or []
if not candidates:
    raise RuntimeError(f"未返回候选内容：{data.get('promptFeedback')}")

candidate = candidates[0]
parts = (candidate.get("content") or {}).get("parts") or []
answer = "".join(
    part.get("text", "") for part in parts if not part.get("thought")
)
if not answer:
    raise RuntimeError(f"未返回最终文本，finishReason={candidate.get('finishReason')}")
print(answer)
```
## 按任务选择思考与输出方式

### 调整思考等级

3.8 Flash 的默认等级是 `medium`，可以按任务选择：

| 等级 | 适合的任务 | 选择依据 |
| --- | --- | --- |
| `low` | 日常对话、草稿、简单提取、低延迟处理 | 减少推理开销，优先缩短等待时间 |
| `medium` | 代码分析、常见业务流程、多步骤任务 | 默认选项，兼顾质量与开销 |
| `high` | 困难数学、复杂规划、深入代码推理 | 为复杂任务投入更多推理资源 |

`minimal` 不受 3.8 Flash 支持，传入会报错。迁移时使用 `thinking_level`，不要同时传入旧的 `thinking_budget`。等级控制思考投入；`include_thoughts` 只控制是否返回思考摘要，两者用途不同。

`max_output_tokens` 包含思考和最终输出的预算。设置过小可能导致最终回答截断，甚至没有可显示的正文。需要降低开销时，先尝试 `low`，再根据实际用量调整输出上限。

### 要求可解析的 JSON


```python
import os
from google import genai
from google.genai import types
from pydantic import BaseModel, Field

class Invoice(BaseModel):
    invoice_no: str = Field(description="发票编号")
    amount: float = Field(description="发票金额")
    currency: str = Field(description="三位货币代码，例如 USD")

client = genai.Client(
    api_key=os.environ["DMXAPI_API_KEY"],
    http_options=types.HttpOptions(
        base_url="https://www.dmxapi.cn", api_version="v1beta", timeout=120_000
    ),
)
response = client.models.generate_content(
    model="gemini-3.8-flash",
    contents="提取发票信息：编号 INV-2026-001，金额 180 美元。",
    config=types.GenerateContentConfig(
        thinking_config=types.ThinkingConfig(thinking_level="low"),
        response_mime_type="application/json",
        response_json_schema=Invoice.model_json_schema(),
    ),
)
if not response.text:
    raise RuntimeError("未返回 JSON 正文。")
invoice = Invoice.model_validate_json(response.text)
print(invoice.model_dump_json(indent=2))
```

官方支持 JSON Schema 的一个子集，复杂 schema ，结构正确不代表业务事实正确，例如金额、币种与来源仍需应用校验。结构化输出用于返回数据；函数调用用于请求应用执行工具，两者不要混为一谈。

## 处理图片、文档和其他媒体


```python
import os
from pathlib import Path
from google import genai
from google.genai import types

client = genai.Client(
    api_key=os.environ["DMXAPI_API_KEY"],
    http_options=types.HttpOptions(
        base_url="https://www.dmxapi.cn", api_version="v1beta", timeout=120_000
    ),
)
image = types.Part.from_bytes(
    data=Path("test/example.jpg").read_bytes(),
    mime_type="image/jpeg",
)
response = client.models.generate_content(
    model="gemini-3.8-flash",
    contents=[image, "请列出图片中的主要形状、颜色和文字。"],
    config=types.GenerateContentConfig(
        media_resolution=types.MediaResolution.MEDIA_RESOLUTION_HIGH,
        thinking_config=types.ThinkingConfig(thinking_level="low"),
    ),
)
if not response.text:
    raise RuntimeError("未返回图片分析文本。")
print(response.text)
```

`media_resolution` 调整模型处理媒体时分配的 token 数量。可先使用默认值；识别小字、图表和细节时，再提高分辨率并比较质量、耗时与用量。音频使用固定的每秒 token 化方式，不能靠降低视觉分辨率来减少音频 token。

| 输入 | 常见 MIME 类型 | 接入要点 |
| --- | --- | --- |
| 图片 | `image/jpeg`、`image/png` | MIME 必须匹配真实文件格式 |
| PDF | `application/pdf` | 说明要提取的字段、页码范围或分析目标 |
| 音频 | `audio/mpeg`、`audio/wav` | 在文字指令中说明转写、翻译或内容分析需求 |
| 视频 | `video/mp4` | 说明需要总结、定位片段还是识别画面细节 |

详细示例：[本地图片](/gemini-image)、[PDF 分析](/gemini-pdf)、[本地音频](/gemini-stt)、[本地视频](/gemini-video)、[网络视频](/gemini-video1)。使用文件 URI 时，远端服务必须能访问该地址；本机磁盘路径不能作为远程 URI。

## 管理对话与工具

### 用 SDK 维护多轮历史

`generateContent` 请求本身不替应用保存会话。SDK 的 Chat 对象可以保存并发送历史内容，也会保留响应中的思考签名。下面两轮请求复用同一个 Chat 对象。

```python
import os
from google import genai
from google.genai import types

client = genai.Client(
    api_key=os.environ["DMXAPI_API_KEY"],
    http_options=types.HttpOptions(
        base_url="https://www.dmxapi.cn", api_version="v1beta", timeout=120_000
    ),
)
chat = client.chats.create(
    model="gemini-3.8-flash",
    config=types.GenerateContentConfig(
        thinking_config=types.ThinkingConfig(thinking_level="low")
    ),
)

for message in [
    "我的订单号是 427，金额是 180 美元，请记住这两个信息。",
    "刚才的订单号和金额分别是多少？",
]:
    response = chat.send_message(message)
    if not response.text:
        raise RuntimeError("这一轮未返回文本。")
    print(response.text)
```
### 接入 Google Search

实时信息需要实际的检索依据。启用 `google_search` 后，应读取返回的 `grounding_metadata`，确认是否有来源，并在产品中展示相关引用。

```python
import os
from google import genai
from google.genai import types

client = genai.Client(
    api_key=os.environ["DMXAPI_API_KEY"],
    http_options=types.HttpOptions(
        base_url="https://www.dmxapi.cn", api_version="v1beta", timeout=120_000
    ),
)
response = client.models.generate_content(
    model="gemini-3.8-flash",
    contents="查询 Google 官方 Gemini 3.8 Flash 模型文档，概括两项主要特性并提供来源。",
    config=types.GenerateContentConfig(
        tools=[types.Tool(google_search=types.GoogleSearch())],
        thinking_config=types.ThinkingConfig(thinking_level="low"),
    ),
)
if not response.text or not response.candidates:
    raise RuntimeError("未返回检索回答。")
metadata = response.candidates[0].grounding_metadata
sources = [
    chunk.web for chunk in (metadata.grounding_chunks or [])
    if chunk.web and chunk.web.uri
] if metadata else []
if not sources:
    raise RuntimeError("本次未返回搜索来源，不能将回答视为已验证的检索结果。")

print(response.text)
print("\n搜索来源：")
for source in sources:
    print(f"- {source.title or '来源'}：{source.uri}")
```
### 自定义函数调用的完整循环

函数调用时，模型返回函数名与参数，应用负责执行工具并回传结果。一次任务可能经过多轮工具调用：

1. 将函数声明与用户请求一起发送。
2. 保存模型返回的完整 `content`，包括 `functionCall` 和思考签名。
3. 校验参数并执行应用侧函数，为每个调用构造对应的 `FunctionResponse`，保留调用标识与函数名。
4. 将结果追加到历史并再次请求，直到模型返回最终回答。

并行调用时，先保留该轮模型返回的全部调用，再回传对应结果，不要把模型调用与工具结果交错拼接。Gemini 3 系列会校验当前工具调用轮次的思考签名，缺失可能返回 400。使用官方 SDK 自动工具调用或 Chat 时，应让 SDK 保留完整状态；

## 从旧模型迁移

更换模型名后，还要检查请求参数和历史消息。

| 旧写法或假设 | 迁移到 3.8 Flash |
| --- | --- |
| 旧模型 ID | 改为 `gemini-3.8-flash` |
| `thinking_budget` 或 `minimal` | 改用 `thinking_level`：`low` / `medium` / `high` |
| 默认思考为 `high` | 3.8 Flash 默认是 `medium`，按任务显式选择 |
| `temperature`、`top_p`、`top_k` | 删除；这些采样参数已弃用，当前会被忽略，后续模型代际可能报错 |
| `candidate_count` | 删除；Gemini 3 及后续模型不支持 |
| 在请求末尾预填一段 model 回复 | 删除预填内容；完整历史中的 model 回复仍可保留 |
| 最后一轮用户消息为空 | 提供非空的文字任务指令；工具结果按函数调用协议回传 |
| 只保留历史回复的正文 | 保留完整 `content.parts` 及思考签名 |

<p align="center">
  <small>© 2026 DMXAPI Gemini 3.8 Flash 开发者指南</small>
</p>