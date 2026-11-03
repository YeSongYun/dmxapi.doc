# Gemini 3.8 Flash 开发者使用指南

本指南通过 DMXAPI 演示 `gemini-3.8-flash` 的 Gemini 原生请求格式，涵盖文本生成、思考配置、图片输入、对话历史与联网结构化输出。

[查看本次实测报告：真实返回内容、耗时与已知限制](/gemini-3.8-flash-test-report)

所有可运行示例统一使用模型 ID `gemini-3.8-flash`。REST 请求使用 `/v1beta/models/gemini-3.8-flash:generateContent`，SDK 的 `base_url` 使用 `https://www.dmxapi.cn`。模型配额、价格与上下文上限以 DMXAPI 当前服务信息为准，不沿用旧版 Pro / Preview 模型的数值。

:::tip 运行准备
安装依赖：`pip install -U google-genai requests pydantic`。填写 DMXAPI 密钥；图片示例还需要准备 `test/example.jpg`。
:::

## 快速开始

::: code-group

```python [SDK]
from google import genai

API_KEY = "sk-*******************************************"
BASE_URL = "https://www.dmxapi.cn"

client = genai.Client(
    api_key=API_KEY,
    http_options={"base_url": BASE_URL, "timeout": 120000}
)

response = client.models.generate_content(
    model="gemini-3.8-flash",
    contents="您好",
)
print(response.text)
```

```python [REST]
import json
import requests

API_KEY = "sk-*******************************************"
url = "https://www.dmxapi.cn/v1beta/models/gemini-3.8-flash:generateContent"
headers = {"x-goog-api-key": API_KEY, "Content-Type": "application/json"}
data = {"contents": [{"parts": [{"text": "您好"}]}]}

response = requests.post(url, headers=headers, json=data, timeout=(10, 120))
response.raise_for_status()
print(json.dumps(response.json(), indent=2, ensure_ascii=False))
```

:::

## 思考等级

SDK 使用 `thinking_config.thinking_level`，REST 使用 `generationConfig.thinkingConfig.thinkingLevel` 设置思考等级。它表达相对的思考投入，不是严格的 token 上限。下方示例使用 `low`；未设置时由模型采用默认策略。

| 等级 | 用途 |
|------|------|
| `minimal` | 尽量减少思考投入，不保证完全关闭思考 |
| `low` | 简单问答与低延迟场景，本页示例使用此值 |
| `medium` | 在速度与推理投入之间折中 |
| `high` | 需要较多推理的任务，可能增加响应时间 |

具体等级是否可用以当前 `gemini-3.8-flash` 通道响应为准。不要在同一请求中同时设置 `thinking_level` 和旧版 `thinking_budget`。

::: code-group

```python [SDK]
from google import genai
from google.genai import types

API_KEY = "sk-*******************************************"
client = genai.Client(
    api_key=API_KEY,
    http_options={"base_url": "https://www.dmxapi.cn", "timeout": 120000}
)

response = client.models.generate_content(
    model="gemini-3.8-flash",
    contents="你好，你是谁？",
    config=types.GenerateContentConfig(
        thinking_config=types.ThinkingConfig(thinking_level="low")
    ),
)
print(response.text)
```

```python [REST]
import json
import requests

API_KEY = "sk-*******************************************"
url = "https://www.dmxapi.cn/v1beta/models/gemini-3.8-flash:generateContent"
headers = {"x-goog-api-key": API_KEY, "Content-Type": "application/json"}
data = {
    "contents": [{"parts": [{"text": "您好"}]}],
    "generationConfig": {"thinkingConfig": {"thinkingLevel": "low"}}
}

response = requests.post(url, headers=headers, json=data, timeout=(10, 120))
response.raise_for_status()
print(json.dumps(response.json(), indent=2, ensure_ascii=False))
```

:::

## 媒体分辨率

本节演示通过图片部分的 `media_resolution`（REST 为 `mediaResolution`）设置分辨率。较高分辨率可能改善文字和细节识别，同时增加用量与延迟。下面两种写法都使用 `media_resolution_high`。

一般图片分析可先使用默认设置，再通过实际任务比较不同分辨率。PDF 和视频请先运行对应文档中的基础示例。每张图片、每页 PDF 或每帧视频的 token 用量以实际响应为准。

::: code-group

```python [SDK]
from google import genai
from google.genai import types

API_KEY = "sk-*******************************************"
client = genai.Client(
    api_key=API_KEY,
    http_options={"base_url": "https://www.dmxapi.cn", "timeout": 120000}
)

# 本示例使用 JPEG；更换格式时同步修改 mime_type
with open("test/example.jpg", "rb") as f:
    image_data = f.read()

response = client.models.generate_content(
    model="gemini-3.8-flash",
    contents=[
        types.Content(parts=[
            types.Part(text="这张图片里有什么？"),
            types.Part(
                inline_data=types.Blob(mime_type="image/jpeg", data=image_data),
                media_resolution={"level": "media_resolution_high"}
            )
        ])
    ]
)
print(response.text)
```

```python [REST]
import base64
import json
import requests

API_KEY = "sk-*******************************************"
url = "https://www.dmxapi.cn/v1beta/models/gemini-3.8-flash:generateContent"
headers = {"x-goog-api-key": API_KEY, "Content-Type": "application/json"}

with open("test/example.jpg", "rb") as f:
    image_data = base64.b64encode(f.read()).decode("utf-8")

data = {
    "contents": [{"parts": [
        {"text": "这张图片里有什么？"},
        {
            "inlineData": {"mimeType": "image/jpeg", "data": image_data},
            "mediaResolution": {"level": "media_resolution_high"}
        }
    ]}]
}

response = requests.post(url, headers=headers, json=data, timeout=(10, 120))
response.raise_for_status()
print(json.dumps(response.json(), indent=2, ensure_ascii=False))
```

:::

## 温度

本页示例不覆盖 `temperature`，使用模型默认采样策略。需要调整时，应通过实际任务比较质量和稳定性，避免直接沿用旧模型的参数结论。

## 思考签名与多轮对话

`thoughtSignature` 是服务返回的不透明签名，用于在后续请求中保持上下文；它不是可阅读的思考总结。多轮对话应保留完整的模型 `content`，不要只提取文本后重建历史，也不要自行生成或修改签名。

- **函数调用**：将模型返回的 `functionCall` 和对应签名原样放入历史，再追加 `functionResponse`。遗漏签名可能触发服务端验证错误。
- **并行或多步工具调用**：保留全部模型部分及原始顺序，不合并、不丢弃签名。
- **文本与流式传输**：签名不保证每次出现，也可能位于文本为空的最后一个块中。用于继续对话时，需保存这些非文本部分。
- **SDK 聊天会话**：使用 `client.chats.create(...)` 管理历史，可避免手工拼装时遗漏返回字段，参见[多轮对话](/duolunduihua)。

以下只展示字段结构；占位签名不能直接用于实际请求。应用应使用上一次响应中的真实 `content`。

```json
{
  "role": "model",
  "parts": [
    {
      "functionCall": {
        "name": "check_weather",
        "args": {"city": "上海"}
      },
      "thoughtSignature": "<保留服务返回的原始签名>"
    }
  ]
}
```

图片生成与编辑需要专门的图像生成模型，不能从本页的图片分析示例推断支持情况。思考总结的读取方法见 [Gemini 3.8 Flash 思考总结](/gemini3-thinking-summary)。

## 使用工具生成结构化输出（联网搜索）

下面分两次请求完成“联网搜索 → JSON 整理”：先确认搜索响应中有 `groundingMetadata` / `grounding_metadata` 来源，再将搜索结果交给同一模型按 JSON Schema 整理。这样可以分别验证联网和结构化输出。

:::info 当前通道的实测情况
本次测试中，在同一次请求里组合 Google Search 与 JSON Schema 可以返回 JSON，但 SDK / REST 均未返回搜索来源，因此无法确认联网结果。下面采用两步写法；如果第一步没有来源，示例会报错停止，不把普通回答当作已验证的搜索结果。天气内容仍需结合来源的日期与可靠性核对。
:::

::: code-group

```python [SDK]
import os
from google import genai
from pydantic import BaseModel, Field

API_KEY = os.getenv("GEMINI_API_KEY", "sk-*******************************************")
client = genai.Client(
    api_key=API_KEY,
    http_options={"base_url": "https://www.dmxapi.cn", "timeout": 120000}
)

class WeatherInfo(BaseModel):
    city: str = Field(description="城市名称")
    temperature: str = Field(description="当前温度")
    weather_condition: str = Field(description="天气状况")
    humidity: str = Field(description="湿度百分比", default="")
    wind_speed: str = Field(description="风速", default="")
    forecast: list[str] = Field(description="未来几天的预报", default_factory=list)

# 第一步：执行搜索并确认返回来源
search = client.models.generate_content(
    model="gemini-3.8-flash",
    contents="请使用 Google Search 搜索今天上海的天气，包括温度、天气状况、湿度、风速和未来几天的预报，并引用来源。",
    config={"tools": [{"google_search": {}}]},
)
metadata = search.candidates[0].grounding_metadata if search.candidates else None
sources = [chunk.web for chunk in (metadata.grounding_chunks or []) if chunk.web] if metadata else []
if not search.text or not sources:
    raise RuntimeError("搜索响应缺少正文或来源，不能确认已联网。")
for source in sources:
    print(f"来源: {source.title} {source.uri}")

# 第二步：只整理上一步的结果，不再次查询或自行补充数据
response = client.models.generate_content(
    model="gemini-3.8-flash",
    contents="仅根据以下搜索结果整理天气 JSON；未提及的字段留空，不要添加新信息：\n" + search.text,
    config={
        "response_mime_type": "application/json",
        "response_json_schema": WeatherInfo.model_json_schema(),
    },
)
result = WeatherInfo.model_validate_json(response.text)
print(result.model_dump_json(indent=2))
```

```python [REST]
import json
import requests

API_KEY = "sk-*******************************************"
url = "https://www.dmxapi.cn/v1beta/models/gemini-3.8-flash:generateContent"
headers = {"x-goog-api-key": API_KEY, "Content-Type": "application/json"}
# 第一步：联网搜索
payload = {
    "contents": [{"parts": [{
        "text": "请使用 Google Search 搜索今天上海的天气，包括城市、温度和天气状况，并引用来源。"
    }]}],
    "tools": [{"googleSearch": {}}]
}
response = requests.post(url, headers=headers, json=payload, timeout=(10, 120))
response.raise_for_status()
search = response.json()
parts = search["candidates"][0]["content"]["parts"]
search_text = "".join(part.get("text", "") for part in parts if not part.get("thought"))
metadata = search["candidates"][0].get("groundingMetadata", {})
sources = [chunk["web"] for chunk in metadata.get("groundingChunks", []) if "web" in chunk]
if not search_text or not sources:
    raise RuntimeError("搜索响应缺少正文或来源，不能确认已联网。")
for source in sources:
    print(f"来源: {source.get('title', '')} {source.get('uri', '')}")

# 第二步：将已搜索到的内容整理为 JSON
payload = {
    "contents": [{"parts": [{"text": "仅根据以下搜索结果整理天气 JSON；未提及的字段留空，不要添加新信息：\n" + search_text}]}],
    "generationConfig": {
        "responseMimeType": "application/json",
        "responseSchema": {
            "type": "OBJECT",
            "properties": {
                "city": {"type": "STRING"},
                "temperature": {"type": "STRING"},
                "weather_condition": {"type": "STRING"}
            },
            "required": ["city", "temperature", "weather_condition"]
        }
    }
}
response = requests.post(url, headers=headers, json=payload, timeout=(10, 120))
response.raise_for_status()
result = response.json()
parts = result["candidates"][0]["content"]["parts"]
text = "".join(part.get("text", "") for part in parts if not part.get("thought"))
print(json.dumps(json.loads(text), indent=2, ensure_ascii=False))
```

:::

## OpenAI 兼容性

本页验证 Gemini 原生格式。OpenAI 兼容接口的 `reasoning_effort` 与 Gemini 的 `thinking_level` 映射由服务端实现，使用兼容接口时应查阅对应说明并单独验证。

## 提示与常见问题

- **如何写提示？** 清楚说明目标、输入资料与输出格式；需要详细回答或固定风格时，在提示中明确要求。
- **模型名称是什么？** 本页统一使用 `gemini-3.8-flash`，不使用旧版 Pro / Preview 模型。
- **知识截止日期、上下文长度和价格是多少？** 请以 DMXAPI 当前模型信息为准。
- **旧 `thinking_budget` 能否直接迁移？** 本页使用 `thinking_level`，旧参数兼容性需单独验证，不要同时设置两者。
- **为什么没有搜索来源或思考总结？** 这些字段不是每次响应都保证出现。应区分“接口返回成功”和“所需功能已在响应中确认”，避免将缺少证据的结果视为功能验证通过。
