# Gemini 3 开发者使用指南
Gemini 3 是谷歌迄今为止最智能的模型系列，以先进的推理能力为基础。它旨在通过掌握智能体工作流、自主编码和复杂的多模态任务，将任何想法变为现实。本指南介绍了 Gemini 3 模型系列的主要功能，以及如何充分利用这些功能。
## 简介
Gemini 3 Pro 是新系列中的首款模型，最适合需要广泛的世界知识和跨模态高级推理的复杂任务。  
Gemini 3 Flash 是谷歌最新的 3 系列模型，具有专业级智能，但速度和价格与 Flash 相当。
:::tip 提示
使用前请先更新 Google SDK 到最新版本！
:::

## 快速开始
::: code-group

```python [SDK]
from google import genai

# DMXAPI 密钥：用于身份验证和授权
API_KEY = "sk-*******************************************"

# DMXAPI 基础 URL：指定 API 服务的端点地址
BASE_URL = "https://www.dmxapi.cn"

client = genai.Client(
    api_key=API_KEY,                           # 使用配置的 DMXAPI 密钥
    http_options={'base_url': BASE_URL}        # 设置自定义 DMXAPI 端点
)

response = client.models.generate_content(
    model="gemini-3-flash-preview",
    contents="您好",
)

print(response.text)
```

```python [request]
import requests
import json

# ============================================
# Gemini API 请求示例
# ============================================

# API 端点地址
url = "https://www.dmxapi.cn/v1beta/models/gemini-3-flash-preview:generateContent"

# 请求头配置
headers = {
    "x-goog-api-key": "sk-**********************************************",  # API 密钥
    "Content-Type": "application/json"  # 内容类型
}

# 请求体数据
data = {
    "contents": [{
        "parts": [{"text": "您好"}]  # 发送的消息内容
    }]
}

# 发送 POST 请求
response = requests.post(url, headers=headers, json=data)

# 格式化输出 JSON 响应
print(json.dumps(response.json(), indent=2, ensure_ascii=False))

```
:::

## 新功能

### 思考等级
Gemini 3 系列模型默认使用动态思考来对提示进行推理。您可以使用 thinking_level 参数，该参数可控制模型在生成回答之前执行的内部推理过程的最大深度。Gemini 3 将这些级别视为相对的思考余量，而不是严格的令牌保证。  
如果未指定 `thinking_level`，Gemini 3 将默认为 `high`。如果不需要复杂的推理，您可以将模型的思考水平限制为 `low`，以获得更快、延迟更低的回答。  
#### Gemini 3 Pro 和 Flash 的思维水平：
Gemini 3 Pro 和 Flash 均支持以下思考水平：  
- **low**：最大限度地缩短延迟时间并降低费用。最适合简单指令遵循、聊天或高吞吐量应用  
- **high（默认，动态）**：最大限度地提高推理深度。模型可能需要更长时间才能生成第一个 token，但输出结果会经过更仔细的推理
#### Gemini 3 Flash thinking 水平
除了上述级别之外，Gemini 3 Flash 还支持以下 Gemini 3 Pro 目前不支持的思维级别：
- **minimal**：与大多数查询的"无思考"设置相匹配。对于复杂的编码任务，该模型可能只会进行非常简单的思考。最大限度地缩短聊天应用或高吞吐量应用的延迟时间。  
:::tip 注意
即使将 Gemini 3 Flash 的思考水平设置为 minimal，也需要流通思考签名。
:::
- **medium**：平衡思考，适用于大多数任务。

#### 示例代码
::: code-group

```python [SDK]
# ============================================================
# Google Gemini AI 内容生成示例
# ============================================================

# 导入 Google GenAI 核心模块
from google import genai
# 导入类型配置模块，用于设置生成参数
from google.genai import types

# ------------------------------------------------------------
# API 配置
# ------------------------------------------------------------
# API 密钥：用于身份验证
API_KEY = "sk-***************************************"

# DMXAPI 基础 URL：指定 API 服务的端点地址
BASE_URL = "https://www.dmxapi.cn"

# ------------------------------------------------------------
# 初始化客户端
# ------------------------------------------------------------
client = genai.Client(
    api_key=API_KEY,
    http_options={"base_url": BASE_URL}
)

# ------------------------------------------------------------
# 调用模型生成内容
# ------------------------------------------------------------
response = client.models.generate_content(
    # 指定使用的模型：Gemini 3 Pro 预览版
    model="gemini-3-pro-preview",
    # 输入提示词：询问 AI 的工作原理
    contents="你好，你是谁",
    # 生成配置
    config=types.GenerateContentConfig(
        # 思考配置：设置思考深度为 "low"（低）
        # 可选值：low / medium / high
        thinking_config=types.ThinkingConfig(thinking_level="low")
    ),
)

# ------------------------------------------------------------
# 输出生成结果
# ------------------------------------------------------------
print(response.text)
```

```python [request]
"""
Gemini API 调用示例
使用 DMXAPI 代理服务调用 Gemini 3 Flash Preview 模型
"""

import requests
import json

# ============================================================
# API 配置
# ============================================================

# API 端点地址
url = "https://www.dmxapi.cn/v1beta/models/gemini-3-flash-preview:generateContent"

# 请求头配置
headers = {
    "x-goog-api-key": "sk-***************************************",  # API 密钥
    "Content-Type": "application/json"  # 内容类型
}

# ============================================================
# 请求数据
# ============================================================

data = {
    # 对话内容
    "contents": [{
        "parts": [{"text": "您好"}]  # 用户输入的文本
    }],
    # 生成配置
    "generationConfig": {
        "thinkingConfig": {
            "thinkingLevel": "low"  # 思考级别: low / medium / high
        }
    }
}

# ============================================================
# 发送请求并输出结果
# ============================================================

response = requests.post(url, headers=headers, json=data)

print("=" * 60)
print("状态码:", response.status_code)
print("=" * 60)

# 格式化输出 JSON 响应
if response.text:
    try:
        result = response.json()
        print(json.dumps(result, indent=2, ensure_ascii=False))
    except json.JSONDecodeError:
        print("响应内容 (非JSON):")
        print(response.text)
else:
    print("响应为空")
```
:::
:::tip 重要提示： 
您不能在同一请求中同时使用 thinking_level 和旧版 thinking_budget 参数。这样做会返回 400 错误。
:::

### 媒体分辨率

Gemini 3 通过`media_resolution` 参数引入了对多模态视觉处理的精细控制。分辨率越高，模型读取细小文字或识别细微细节的能力就越强，但 token 用量和延迟时间也会增加。`media_resolution` 参数用于确定为每个输入图片或视频帧分配的 token 数量上限。

现在，您可以为每个媒体部分单独设置分辨率，也可以全局设置分辨率（通过 `generation_config`，超高分辨率无法全局设置）。`media_resolution_low`、`media_resolution_medium`、`media_resolution_high` 或 `media_resolution_ultra_high`。如果未指定，模型会根据媒体类型使用最佳默认值。

#### 推荐设置

| 媒体类型 | 推荐设置 | Token 数量上限 | 使用指南 |
|---------|---------|---------------|---------|
| 图片 | `media_resolution_high` | 1120 | 建议用于大多数图片分析任务，以确保获得最佳质量。 |
| PDF | `media_resolution_medium` | 560 | 非常适合文档理解；质量通常在 medium 时达到饱和。增加到 high 很少能改进标准文档的 OCR 结果。 |
| 视频（常规） | `media_resolution_low`（或 `media_resolution_medium`） | 70（每帧） | 注意：对于视频，low 和 medium 设置的处理方式相同（70 个 tokens），以优化上下文使用情况。这对于大多数动作识别和描述任务来说已经足够。 |
| 视频（文字较多） | `media_resolution_high` | 280（每帧） | 仅当用例涉及读取密集文本（OCR）或视频帧中的微小细节时才需要。 |

:::info 注意
`media_resolution` 参数会根据输入类型映射到不同的 token 数量。虽然图片是线性缩放的（`media_resolution_low`：280，`media_resolution_medium`：560，`media_resolution_high`：1120），但视频的压缩程度更高。对于视频，`media_resolution_low` 和 `media_resolution_medium` 的上限均为每帧 70 个 tokens，`media_resolution_high` 的上限为 280 个 tokens。
:::

#### 示例代码
::: code-group

```python [SDK]
"""
gemini-3-flash-preview图片分析示例
使用 DMXAPI 调用 gemini-3-flash-preview 模型进行图片内容识别
"""

from google import genai
from google.genai import types

# ===========================================
# DMXAPI 配置
# ===========================================
API_KEY = "sk-*******************************************"
BASE_URL = "https://www.dmxapi.cn"

# 初始化客户端
client = genai.Client(
    api_key=API_KEY,
    http_options={'base_url': BASE_URL}
)

# ===========================================
# 读取图片
# ===========================================
# 支持的图片格式: JPEG, PNG, GIF, WebP
# 对应的 mime_type:
#   - JPEG: "image/jpeg"
#   - PNG:  "image/png"
#   - GIF:  "image/gif"
#   - WebP: "image/webp"

image_path = "test/example.jpg"  # 替换为你的图片路径
with open(image_path, "rb") as f:
    image_data = f.read()

# ===========================================
# 调用模型
# ===========================================
# media_resolution 参数说明:
#   - media_resolution_low:    280 tokens, 适合快速处理
#   - media_resolution_medium: 560 tokens, 平衡质量与速度
#   - media_resolution_high:   1120 tokens, 最佳质量, 适合细节识别

response = client.models.generate_content(
    model="gemini-3-flash-preview",
    contents=[
        types.Content(
            parts=[
                types.Part(text="这张图片里有什么?"),
                types.Part(
                    inline_data=types.Blob(
                        mime_type="image/jpeg",
                        data=image_data
                    ),
                    media_resolution={"level": "media_resolution_high"}
                )
            ]
        )
    ]
)

# ===========================================
# 输出结果
# ===========================================
print(response.text)
```
```python [request]
import requests
import json
import base64

# ==================== 读取图片 ====================

with open("test/example.jpg", "rb") as f:
    image_data = base64.b64encode(f.read()).decode("utf-8")  # 读取并转为 Base64

# ==================== API 配置 ====================

# API 地址
url = "https://www.dmxapi.cn/v1beta/models/gemini-3-flash-preview:generateContent"

# 请求头
headers = {
    "x-goog-api-key": "sk-ThKDN72mfzpvKdhRT2yjzmxkRZF3aBNtZmQJq5hbbICu67DE",  # 从环境变量获取 API Key
    "Content-Type": "application/json"
}

# ==================== 请求体 ====================

data = {
    "contents": [{
        "parts": [
            {"text": "这张图片里有什么？"},           # 文本提示
            {
                "inlineData": {
                    "mimeType": "image/jpeg",             # 图片类型
                    "data": image_data                    # Base64 编码的图片数据
                },
                "mediaResolution": {
                    "level": "media_resolution_high"      # 高分辨率模式
                }
            }
        ]
    }]
}

# ==================== 发送请求 ====================

response = requests.post(url, headers=headers, json=data)

# ==================== 格式化输出 ====================

print(json.dumps(response.json(), indent=2, ensure_ascii=False))
```
:::


### 温度

对于 Gemini 3，谷歌强烈建议将温度参数保留为默认值`1.0`。  
虽然之前的模型通常可以通过调整温度来控制创造性与确定性，但 Gemini 3 的推理能力已针对默认设置进行了优化。更改温度（将其设置为低于`1.0`）可能会导致意外行为（例如循环或性能下降），尤其是在复杂的数学或推理任务中。

## 思考签名
Gemini 3 使用思路签名在 API 调用之间保持推理上下文。这些签名是模型内部思考过程的加密表示形式。为确保模型保持推理能力，您必须在请求中将这些签名原封不动地返回给模型：

- **函数调用（严格）**：API 会对“当前轮次”强制执行严格的验证。缺少签名会导致 400 错误。
::: tip 注意：
即使将 Gemini 3 Flash 的思考水平设置为 minimal，也需要循环使用思考签名。
:::
- 文本/聊天：验证并非强制执行，但省略签名会降低模型的推理能力和回答质量。

- 图片生成/编辑（严格）：API 会对所有模型部分（包括 thoughtSignature）强制执行严格的验证。缺少签名会导致 400 错误。

:::tip 小贴士： 
如果您使用官方 SDK（Python、Node、Java）和标准聊天记录，系统会自动处理思考签名。您无需手动管理这些字段。
:::
### 函数调用（严格验证）

当 Gemini 生成 functionCall 时，它会依赖 thoughtSignature 在下一轮中正确处理工具的输出。“当前对话轮次”包括自上次标准用户 text 消息以来发生的所有模型 (functionCall) 和用户 (functionResponse) 步骤。

- **单个函数调用**：functionCall 部分包含签名。您必须归还。
- **并行函数调用**：只有列表中的第一个 functionCall 部分会包含签名。您必须按收到的确切顺序退回这些部件。
- **多步（顺序）**：如果模型调用某个工具、收到结果，然后（在同一轮次内）调用另一个工具，则两个函数调用都有签名。您必须返回历史记录中的所有累积签名。

### 文字和流式传输

对于标准聊天或文本生成，谷歌无法保证签名一定会显示。

- **非流式传输**：回答的最终内容部分可能包含 thoughtSignature，但并非始终存在。如果返回了此类令牌，您应将其发送回去，以保持最佳性能。
- **流式传输**：如果生成了签名，则该签名可能位于包含空文本部分的最终块中。确保您的流解析器即使在文本字段为空的情况下也会检查签名。

### 示例
::: code-group

```json [多步骤函数调用（顺序）]
// 场景：用户在一个回合中提出需要两个单独步骤（查看航班 -> 预订出租车）的问题。

// ═══════════════════════════════════════════════════════════════
// 第 1 步：模型调用 Flight Tool，返回签名 <Sig_A>
// ═══════════════════════════════════════════════════════════════

// 模型响应 (回合 1, 步骤 1)
{
  "role": "model",
  "parts": [
    {
      "functionCall": { "name": "check_flight", "args": {...} },
      "thoughtSignature": "<Sig_A>"  // 保存此签名
    }
  ]
}

// ═══════════════════════════════════════════════════════════════
// 第 2 步：用户发送航班结果
// 必须发送回 <Sig_A>，以保持模型的思路
// ═══════════════════════════════════════════════════════════════

// 用户请求 (回合 1, 步骤 2)
[
  { "role": "user", "parts": [{ "text": "Check flight AA100..." }] },
  {
    "role": "model",
    "parts": [
      {
        "functionCall": { "name": "check_flight", "args": {...} },
        "thoughtSignature": "<Sig_A>"  // 必须包含
      }
    ]
  },
  { "role": "user", "parts": [{ "functionResponse": { "name": "check_flight", "response": {...} } }] }
]

// ═══════════════════════════════════════════════════════════════
// 第 3 步：模型调用出租车工具
// 模型通过 <Sig_A> 记住航班延误情况，决定预订出租车，生成新签名 <Sig_B>
// ═══════════════════════════════════════════════════════════════

// 模型响应 (回合 1, 步骤 3)
{
  "role": "model",
  "parts": [
    {
      "functionCall": { "name": "book_taxi", "args": {...} },
      "thoughtSignature": "<Sig_B>"  // 保存此签名
    }
  ]
}

// ═══════════════════════════════════════════════════════════════
// 第 4 步：用户发送出租车结果
// 必须发送整个签名链：<Sig_A> 和 <Sig_B>
// ═══════════════════════════════════════════════════════════════

// 用户请求 (回合 1, 步骤 4)
[
  // ... 之前的历史记录 ...
  {
    "role": "model",
    "parts": [
      { "functionCall": { "name": "check_flight", ... }, "thoughtSignature": "<Sig_A>" }
    ]
  },
  { "role": "user", "parts": [{ "functionResponse": {...} }] },
  {
    "role": "model",
    "parts": [
      { "functionCall": { "name": "book_taxi", ... }, "thoughtSignature": "<Sig_B>" }
    ]
  },
  { "role": "user", "parts": [{ "functionResponse": {...} }] }
]
```

```json [并行函数调用]
// 场景：用户询问"查看巴黎和伦敦的天气"，模型在一个回答中返回两个函数调用

// 用户请求（发送并行结果）
[
  {
    "role": "user",
    "parts": [
      { "text": "Check the weather in Paris and London." }
    ]
  },
  {
    "role": "model",
    "parts": [
      // 第一个函数调用包含签名
      {
        "functionCall": { "name": "check_weather", "args": { "city": "Paris" } },
        "thoughtSignature": "<Signature_A>"
      },
      // 后续的并行调用不包含签名
      {
        "functionCall": { "name": "check_weather", "args": { "city": "London" } }
      }
    ]
  },
  {
    "role": "user",
    "parts": [
      // 函数响应在下一个块中分组
      {
        "functionResponse": { "name": "check_weather", "response": { "temp": "15C" } }
      },
      {
        "functionResponse": { "name": "check_weather", "response": { "temp": "12C" } }
      }
    ]
  }
]
```

```json [文本/上下文推理（无验证）]
// 场景：用户提出需要上下文推理但不使用外部工具的问题
// 虽然未经过严格验证，但包含签名有助于模型针对后续问题保持推理链

// 用户请求（后续问题）
[
  {
    "role": "user",
    "parts": [{ "text": "What are the risks of this investment?" }]
  },
  {
    "role": "model",
    "parts": [
      {
        "text": "I need to calculate the risk step-by-step. First, I'll look at volatility...",
        "thoughtSignature": "<Signature_C>"  // 建议包含
      }
    ]
  },
  {
    "role": "user",
    "parts": [{ "text": "Summarize that in one sentence." }]
  }
]
```

```text [绕过验证]
如果您要从其他模型（例如 Gemini 2.5）或注入并非由 Gemini 3 生成的自定义函数调用，
您将无法获得有效的签名。

如需在这些特定场景中绕过严格验证，请使用以下特定虚拟字符串填充相应字段：

"thoughtSignature": "context_engineering_is_the_way_to_go"
```
:::

## 使用工具生成结构化输出(联网搜索)

Gemini 3 可让您将结构化输出与内置工具（包括依托 Google 搜索进行接地、网址上下文和代码执行）结合使用。

### 示例代码
::: code-group

```python [SDK]
"""
DMXAPI Gemini 3 Pro 工具调用联网搜索示例
====================================
本示例演示如何使用 Gemini 3 Pro 的 Google Search 工具进行联网搜索，
并将搜索结果转换为结构化的 JSON 输出。

主要功能：
- 调用 Google Search 工具获取实时天气信息
- 使用 Pydantic 模型定义输出结构
- 自动将 AI 响应解析为结构化数据
"""

import os
from google import genai
from google.genai import types
from pydantic import BaseModel, Field
from typing import List

# ==================== 配置部分 ====================
# 从环境变量读取 DMXAPI 配置，如果环境变量不存在则使用默认值
api_key = os.getenv("GEMINI_API_KEY", "sk-*******************************************")
BASE_URL = os.getenv("GEMINI_API_BASE_URL", "https://www.dmxapi.cn")

# ==================== 数据模型定义 ====================
# 使用 Pydantic 定义天气信息的结构化输出模型
# 这个模型将作为 JSON Schema 传递给 AI，确保返回符合预期格式的数据
class WeatherInfo(BaseModel):
    """天气信息数据模型"""
    city: str = Field(description="城市名称")
    temperature: str = Field(description="当前温度")
    weather_condition: str = Field(description="天气状况，例如晴、多云、雨等")
    humidity: str = Field(description="湿度百分比", default="")
    wind_speed: str = Field(description="风速", default="")
    forecast: List[str] = Field(description="未来几天的天气预报", default_factory=list)

# ==================== 初始化客户端 ====================
# 创建 Gemini AI 客户端实例
client = genai.Client(api_key=api_key, http_options={'base_url': BASE_URL})

# ==================== 开始测试 ====================
print("开始测试 Gemini 3 Pro 工具调用生成结构化输出...")
print("=" * 60)

try:
    # ==================== 调用 AI 模型 ====================
    # 使用 Gemini 3 Pro 模型生成内容
    # 关键配置说明：
    # 1. tools: 启用 google_search 工具，允许模型进行实时联网搜索
    # 2. response_mime_type: 指定返回 JSON 格式
    # 3. response_json_schema: 传入 Pydantic 模型的 JSON Schema，确保输出符合预定义结构
    response = client.models.generate_content(
        model="gemini-3-pro-preview",
        contents="搜索今天上海的详细天气信息，包括温度、天气状况、湿度、风速和未来几天的预报。",
        config={
            "tools": [
                {"google_search": {}},  # 启用 Google 搜索工具
            ],
            "response_mime_type": "application/json",  # 要求返回 JSON 格式
            "response_json_schema": WeatherInfo.model_json_schema(),  # 指定 JSON 结构
        },
    )

    # ==================== 处理原始响应 ====================
    print("原始响应文本:")
    print(response.text)
    print("\n" + "=" * 60)

    # ==================== 清理 JSON 文本 ====================
    # AI 可能返回包含 ```json 或 ``` 标记的文本，需要清理这些标记
    # 确保文本可以被正确解析为 JSON
    cleaned_text = response.text.strip()
    if cleaned_text.startswith("```json"):
        cleaned_text = cleaned_text[7:]  # 移除开头的 ```json
    if cleaned_text.startswith("```"):
        cleaned_text = cleaned_text[3:]  # 移除开头的 ```
    if cleaned_text.endswith("```"):
        cleaned_text = cleaned_text[:-3]  # 移除末尾的 ```
    cleaned_text = cleaned_text.strip()

    print("清理后的 JSON:")
    print(cleaned_text)
    print("\n" + "=" * 60)

    # ==================== 解析为结构化对象 ====================
    # 使用 Pydantic 将 JSON 文本解析为 WeatherInfo 对象
    # 这将自动验证数据是否符合模型定义的结构
    result = WeatherInfo.model_validate_json(cleaned_text)

    # ==================== 输出结构化数据 ====================
    print("\n解析后的结构化数据:")
    print(f"城市: {result.city}")
    print(f"温度: {result.temperature}")
    print(f"天气状况: {result.weather_condition}")
    print(f"湿度: {result.humidity}")
    print(f"风速: {result.wind_speed}")
    print(f"未来天气预报: {', '.join(result.forecast) if result.forecast else '无'}")

    print("\n" + "=" * 60)
    print("测试成功！")

except Exception as e:
    # ==================== 错误处理 ====================
    print(f"测试失败，错误信息: {str(e)}")
    print(f"错误类型: {type(e).__name__}")

```
```python [request]
# ============================================
# Gemini API 谷歌搜索示例
# ============================================

import requests
import json
import os

# --------------------------------------------
# API 配置
# --------------------------------------------
API_KEY = "sk-********************************************"
API_URL = "https://www.dmxapi.cn/v1beta/models/gemini-3-flash-preview:generateContent"

# --------------------------------------------
# 请求头
# --------------------------------------------
headers = {
    "x-goog-api-key": API_KEY,
    "Content-Type": "application/json"
}

# --------------------------------------------
# 请求体（只启用谷歌搜索工具）
# --------------------------------------------
payload = {
    "contents": [{
        "parts": [{"text": "现在的股市怎么样？"}]
    }],
    "tools": [
        {"googleSearch": {}}
    ]
}

# --------------------------------------------
# 发送请求
# --------------------------------------------
response = requests.post(API_URL, headers=headers, json=payload)

# --------------------------------------------
# 格式化输出
# --------------------------------------------
print(json.dumps(response.json(), indent=2, ensure_ascii=False))

```
:::

## OpenAI 兼容性

对于使用 OpenAI 兼容层的用户，标准参数会自动映射到 Gemini 等效参数：

`reasoning_effort`（OpenAI）映射到 `thinking_level`（Gemini）。请注意，`reasoning_effort` medium 映射到 `thinking_level` high。

## 提示最佳实践

Gemini 3 是一种推理模型，因此您需要改变提示方式。

**精确的指令：** 输入提示应简洁明了。Gemini 3 最适合处理直接、清晰的指令。它可能会过度分析用于旧模型的冗长或过于复杂的提示工程技术。

**输出详细程度：** 默认情况下，Gemini 3 的输出详细程度较低，更倾向于提供直接、高效的答案。如果您的使用情形需要更具对话性或"聊天"风格的角色，您必须在提示中明确引导模型（例如，"以友善健谈的助理的身份解释一下"）。

**上下文管理：** 处理大型数据集（例如整本书、代码库或长视频）时，请将具体指令或问题放在提示末尾的数据上下文之后。在提问时，以"根据上述信息…"之类的短语开头，将模型的推理锚定到提供的数据。

## 常见问题解答

**Q: Gemini 3 Pro 的知识截止日期是什么？**
A: Gemini 3 的知识截止日期为 2025 年 1 月。

**Q: 上下文窗口有哪些限制？**
A: Gemini  支持 100 万个 tokens 的输入上下文窗口，输出最多可达 6.4 万个 tokens。

**Q: 我的旧 `thinking_budget` 代码是否仍然有效？**
A: 可以，为了实现向后兼容性，谷歌仍支持 `thinking_budget`，但建议您迁移到 `thinking_level` 以获得更可预测的性能。请勿在同一请求中同时使用这两个参数。