# Gemini Nano Banana 2.1 文生图

通过 Gemini Nano Banana 2.1 模型根据文字提示生成图像，支持 1K、2K、4K 分辨率、宽高比配置和思考等级配置。本文使用 DMXAPI 兼容的 Gemini 原生调用格式，提供 SDK 和 requests 两种写法。

:::tip 模型升级说明
**Gemini Nano Banana 2.1** 是 Nano Banana 2（Gemini 3.1 Flash Image）的更新版本。Google 官方说明其改善了视觉质量、写实性、提示遵循、文字排版及多轮角色一致性，并修复了 2K / 4K 下部分极宽比例的平铺瑕疵。

- **分辨率**：支持 `1K` / `2K` / `4K`，默认 `1K`，不支持 `512`。
- **Thinking 思考配置**：支持 `minimal` / `medium` / `high`，默认 `medium`。
- **搜索能力**：支持 Google 网页搜索和图片搜索。

来源：[Google 官方模型说明](https://ai.google.dev/gemini-api/docs/models/gemini-nano-banana-2.1)。
:::

## 接口地址

| 接口 | 请求方式 | URL |
|------|---------|-----|
| 生成图片 | POST | `https://www.dmxapi.cn/v1beta/models/gemini-nano-banana-2.1:generateContent` |

示例沿用 DMXAPI 现有 Gemini 原生兼容调用格式；新模型的渠道可用性与参数支持未做在线验证，请以 DMXAPI 控制台为准。

:::warning 注意
请妥善保管 DMXAPI API Key，不要将真实密钥提交到公开仓库。使用 SDK 示例前，请更新 `google-genai`，并安装 `Pillow`；HTTP 示例需要 `requests`。
:::

## 模型名称

### Gemini Nano Banana 2.1

- **模型名称**：`gemini-nano-banana-2.1`
- **名称**：Nano Banana 2.1
- **特点**：支持文生图、图片编辑、多图融合和多轮对话改图。
- **配置**：支持 1K / 2K / 4K 分辨率及 Thinking 思考等级。

### 与 gemini-3.1-flash-image 的区别

| 对比项 | gemini-3.1-flash-image（Nano Banana 2） | gemini-nano-banana-2.1（Nano Banana 2.1） |
|--------|------------------------------------------------|-----------------------------------------------|
| 模型关系 | 前一代模型 | Nano Banana 2 的更新版本 |
| 输出分辨率 | 512、1K、2K、4K | 1K、2K、4K，不支持 512 |
| 思考等级 | minimal、high；默认 minimal | minimal、medium、high；默认 medium |
| 图像质量 | 原有生成与编辑能力 | 改善画质、文字排版、提示遵循和多轮一致性 |
| 极宽比例 | 支持 1:4、4:1、1:8、8:1 | 修复这些比例在 2K / 4K 下的平铺瑕疵 |
| 多图参考 | 最多 14 张参考图 | 同样最多 14 张参考图 |
| 搜索工具 | 网页搜索、图片搜索 | 同样支持网页搜索、图片搜索 |

对比依据：[官方模型说明](https://ai.google.dev/gemini-api/docs/models/gemini-nano-banana-2.1)、[官方图像生成指南](https://ai.google.dev/gemini-api/docs/generate-content/image-generation)。

## 示例代码

两种写法均请求生成方形图片。SDK 使用下划线参数名，HTTP JSON 使用驼峰参数名；模型名称位于请求路径中，无需在 HTTP 请求体中重复设置 `model`。

::: code-group

```python [SDK]
from datetime import datetime
from pathlib import Path

from google import genai
from google.genai import types

# DMXAPI 密钥和基础 URL
API_KEY = "sk-****************************************"
BASE_URL = "https://www.dmxapi.cn"
client = genai.Client(
    api_key=API_KEY,
    http_options={"base_url": BASE_URL},
)

# 描述需要生成的画面
prompt = "生成一个美丽的日落风景，色彩丰富，充满艺术感。"

response = client.models.generate_content(
    # 【model】模型名称
    model="gemini-nano-banana-2.1",
    # 【contents】输入文字提示词
    contents=[prompt],
    config=types.GenerateContentConfig(
        # 【response_modalities】返回图片；需要文字时改为 ["TEXT", "IMAGE"]
        response_modalities=["IMAGE"],
        image_config=types.ImageConfig(
            # 【aspect_ratio】输出宽高比，本例为方形
            aspect_ratio="1:1",
            # 【image_size】可选 1K / 2K / 4K，默认 1K；不支持 512
            image_size="1K",
        ),
        thinking_config=types.ThinkingConfig(
            # 【thinking_level】可选 MINIMAL / MEDIUM / HIGH，默认 MEDIUM
            thinking_level=types.ThinkingLevel.MEDIUM,
        ),
    ),
)

# 保存最终图片，跳过思考过程中的临时内容
output_dir = Path("output")
output_dir.mkdir(exist_ok=True)
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
image_count = 0

for part in response.parts or []:
    if part.thought:
        continue
    if part.text is not None:
        print(part.text)
    elif part.inline_data is not None:
        image_count += 1
        filename = output_dir / f"generated_image_{timestamp}_{image_count}.png"
        part.as_image().save(filename)
        print(f"图片已保存到 {filename}")

if image_count == 0:
    print("响应中没有图片，请检查响应内容。")
```

```python [request]
import base64
from datetime import datetime
from pathlib import Path

import requests

# DMXAPI 密钥和请求地址
API_KEY = "sk-****************************************"
API_URL = "https://www.dmxapi.cn/v1beta/models/gemini-nano-banana-2.1:generateContent"

headers = {
    "x-goog-api-key": API_KEY,
    "Content-Type": "application/json",
}

payload = {
    "contents": [{
        # 【parts[].text】描述需要生成的图片
        "parts": [{"text": "生成一个美丽的日落风景，色彩丰富，充满艺术感。"}],
    }],
    "generationConfig": {
        # 【responseModalities】返回图片；需要文字时改为 ["TEXT", "IMAGE"]
        "responseModalities": ["IMAGE"],
        "imageConfig": {
            # 【aspectRatio】输出宽高比，本例为方形
            "aspectRatio": "1:1",
            # 【imageSize】可选 1K / 2K / 4K，默认 1K；不支持 512
            "imageSize": "1K",
        },
        "thinkingConfig": {
            # 【thinkingLevel】可选 MINIMAL / MEDIUM / HIGH，默认 MEDIUM
            "thinkingLevel": "MEDIUM",
        },
    },
}

response = requests.post(API_URL, headers=headers, json=payload)
response.raise_for_status()
result = response.json()

# 从 JSON 响应提取图片，按实际 MIME 类型保存
output_dir = Path("output")
output_dir.mkdir(exist_ok=True)
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
image_count = 0

for candidate in result.get("candidates", []):
    for part in candidate.get("content", {}).get("parts", []):
        if part.get("thought"):
            continue
        if "text" in part:
            print(part["text"])
        elif "inlineData" in part:
            image = part["inlineData"]
            image_count += 1
            extension = image["mimeType"].split("/")[-1]
            filename = output_dir / f"generated_image_{timestamp}_{image_count}.{extension}"
            filename.write_bytes(base64.b64decode(image["data"]))
            print(f"图片已保存到 {filename}")

if image_count == 0:
    print("响应中没有图片，请检查响应内容。")
```

:::

## 返回示例

以下为成功执行后的控制台输出示意及 HTTP JSON 结构示意，并非本次在线调用结果。图片 Base64 数据和思考签名均已替换为占位内容，不能直接解码使用。

::: code-group

```text [SDK]
图片已保存到 output/generated_image_20261008_120000_1.png
```

```json [request]
{
  "candidates": [
    {
      "content": {
        "role": "model",
        "parts": [
          {
            "inlineData": {
              "mimeType": "image/png",
              "data": "<BASE64_IMAGE_DATA>"
            },
            "thoughtSignature": "<THOUGHT_SIGNATURE>"
          }
        ]
      }
    }
  ]
}
```

:::

## 注意事项

- 将 API Key 占位符替换为你自己的 DMXAPI 密钥；生成的图片保存在 `output` 文件夹。
- `imageSize` 中的 `K` 必须大写，例如 `1K`，不能写成 `1k`；本模型不支持 `512` / `512px`。
- `imageConfig` 可使用以下宽高比：`1:1`、`1:4`、`4:1`、`1:8`、`8:1`、`2:3`、`3:2`、`3:4`、`4:3`、`4:5`、`5:4`、`9:16`、`16:9`、`21:9`。参数定义见 [官方 ImageConfig](https://ai.google.dev/api/generate-content#ImageConfig)。
- 思考过程默认启用；`MINIMAL` 表示较少思考，并不代表关闭思考。可按需要选择 `MEDIUM` 或 `HIGH`，详见 [官方思考等级说明](https://ai.google.dev/gemini-api/docs/generate-content/image-generation#thinking-levels)。
- 本例未启用搜索工具；若需要实时信息或网页图片参考，可参考 [官方搜索接地示例](https://ai.google.dev/gemini-api/docs/generate-content/image-generation#image-search)，并确认所选 DMXAPI 渠道支持相关工具。

---

<p align="center">
  <small>© 2026 DMXAPI gemini-nano-banana-2.1 文生图</small>
</p>
