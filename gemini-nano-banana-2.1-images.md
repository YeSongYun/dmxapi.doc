# Gemini Nano Banana 2.1 多图融合

通过 Gemini Nano Banana 2.1 模型，根据文字提示将多张输入图片融合生成新图片，可用于物体合成和场景混合。本文使用 DMXAPI 兼容的 Gemini 原生调用格式，提供 SDK 和 requests 两种写法。

:::tip 模型升级说明
**Gemini Nano Banana 2.1** 是 Nano Banana 2（Gemini 3.1 Flash Image）的更新版本。Google 官方说明其改善了视觉质量、写实性、提示遵循、文字排版及多轮角色一致性。

本模型支持 `1K` / `2K` / `4K`，不支持 `512`；Thinking 支持 `minimal` / `medium` / `high`，默认 `medium`。来源：[Google 官方模型说明](https://ai.google.dev/gemini-api/docs/models/gemini-nano-banana-2.1)。
:::

## 接口地址

| 接口 | 请求方式 | URL |
|------|---------|-----|
| 融合图片 | POST | `https://www.dmxapi.cn/v1beta/models/gemini-nano-banana-2.1:generateContent` |

示例沿用 DMXAPI 现有 Gemini 原生兼容调用格式；新模型的渠道可用性与参数支持未做在线验证，请以 DMXAPI 控制台为准。

:::warning 注意
请妥善保管 DMXAPI API Key，不要将真实密钥提交到公开仓库。使用 SDK 示例前，请更新 `google-genai`，并安装 `Pillow`；HTTP 示例需要 `requests`。
:::

## 模型名称

### Gemini Nano Banana 2.1

- **模型名称**：`gemini-nano-banana-2.1`
- **名称**：Nano Banana 2.1
- **特点**：根据文字提示融合多张输入图片。
- **参考图**：最多 14 张，可保持最多 4 个角色的一致性，并以较高保真度呈现最多 10 个物体；该数量限制并非相比 Nano Banana 2 的提升。
- **配置**：支持 1K / 2K / 4K 分辨率及 Thinking 思考等级。

参考图能力依据：[Google 官方模型说明](https://ai.google.dev/gemini-api/docs/models/gemini-nano-banana-2.1)、[官方图像生成指南](https://ai.google.dev/gemini-api/docs/generate-content/image-generation)。

## 示例代码

先将场景图片保存为 `b1.png`，将要加入场景的物体图片保存为 `b2.png`，两张图片均使用 PNG 格式。两种写法按相同顺序提交图片，提示词中的“第一张图”和“第二张图”与该顺序对应。SDK 使用下划线参数名，HTTP JSON 使用驼峰参数名；模型名称位于请求路径中，无需在 HTTP 请求体中重复设置 `model`。

::: code-group

```python [SDK]
from datetime import datetime
from pathlib import Path

from google import genai
from google.genai import types
from PIL import Image

# DMXAPI 密钥和基础 URL
API_KEY = "sk-****************************************"
BASE_URL = "https://www.dmxapi.cn"
client = genai.Client(
    api_key=API_KEY,
    http_options={"base_url": BASE_URL},
)

# 按提示词中的顺序读取两张 PNG 图片
image1 = Image.open("b1.png")
image2 = Image.open("b2.png")
prompt = "将第二张图的物体放到第一张图的场景中，保持主体细节和自然光照。"

response = client.models.generate_content(
    # 【model】模型名称
    model="gemini-nano-banana-2.1",
    # 【contents】输入融合提示词、场景图片和物体图片
    contents=[prompt, image1, image2],
    config=types.GenerateContentConfig(
        # 【response_modalities】返回图片；需要文字时改为 ["TEXT", "IMAGE"]
        response_modalities=["IMAGE"],
        image_config=types.ImageConfig(
            # 【aspect_ratio】输出宽高比，本例为横向图片
            aspect_ratio="16:9",
            # 【image_size】可选 1K / 2K / 4K，默认 1K；本例使用 2K
            image_size="2K",
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
        filename = output_dir / f"fused_image_{timestamp}_{image_count}.png"
        part.as_image().save(filename)
        print(f"融合后的图片已保存到 {filename}")

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

# 本例输入均为 PNG，保留场景图片在前、物体图片在后的顺序
image_parts = []
for image_path in ["b1.png", "b2.png"]:
    image_data = base64.b64encode(Path(image_path).read_bytes()).decode("utf-8")
    image_parts.append({
        "inlineData": {
            "mimeType": "image/png",
            "data": image_data,
        },
    })

payload = {
    "contents": [{
        "role": "user",
        "parts": [
            # 【parts[].text】描述两张输入图片的融合方式
            {"text": "将第二张图的物体放到第一张图的场景中，保持主体细节和自然光照。"},
            # 【inlineData】按顺序展开两张 PNG 图片的 MIME 类型和 Base64 数据
            *image_parts,
        ],
    }],
    "generationConfig": {
        # 【responseModalities】返回图片；需要文字时改为 ["TEXT", "IMAGE"]
        "responseModalities": ["IMAGE"],
        "imageConfig": {
            # 【aspectRatio】输出宽高比，本例为横向图片
            "aspectRatio": "16:9",
            # 【imageSize】可选 1K / 2K / 4K，默认 1K；本例使用 2K
            "imageSize": "2K",
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
            filename = output_dir / f"fused_image_{timestamp}_{image_count}.{extension}"
            filename.write_bytes(base64.b64decode(image["data"]))
            print(f"融合后的图片已保存到 {filename}")

if image_count == 0:
    print("响应中没有图片，请检查响应内容。")
```

:::

## 返回示例

以下为成功执行后的控制台输出示意及 HTTP JSON 结构示意，并非本次在线调用结果。图片 Base64 数据和思考签名均已替换为占位内容，不能直接解码使用。

::: code-group

```text [SDK]
融合后的图片已保存到 output/fused_image_20261008_120000_1.png
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

- 将 API Key 占位符替换为你自己的 DMXAPI 密钥，并确保当前目录中存在 `b1.png` 和 `b2.png`；融合后的图片保存在 `output` 文件夹。
- 两种写法均按 `b1.png`、`b2.png` 的顺序提交图片；增加图片时，提示词中对图片的引用也应与提交顺序保持一致。
- 本例输入均为 PNG；使用其他受支持的图片格式时，每个 HTTP 图片 part 中的 `mimeType` 必须与对应文件的实际格式匹配，不能只修改文件后缀。
- SDK 将响应图片转换并保存为 PNG；HTTP 直接解码返回数据，并按返回的 `mimeType` 使用相应扩展名。
- `imageSize` 中的 `K` 必须大写，例如 `2K`，不能写成 `2k`；本模型不支持 `512` / `512px`。
- `imageConfig` 可使用以下宽高比：`1:1`、`1:4`、`4:1`、`1:8`、`8:1`、`2:3`、`3:2`、`3:4`、`4:3`、`4:5`、`5:4`、`9:16`、`16:9`、`21:9`。参数定义见 [官方 ImageConfig](https://ai.google.dev/api/generate-content#ImageConfig)。
- 思考过程默认启用；`MINIMAL` 表示较少思考，并不代表关闭思考。可按需要选择 `MEDIUM` 或 `HIGH`，详见 [官方思考等级说明](https://ai.google.dev/gemini-api/docs/generate-content/image-generation#thinking-levels)。
- 本例未启用搜索工具；若需要实时信息或网页图片参考，可参考 [官方搜索接地示例](https://ai.google.dev/gemini-api/docs/generate-content/image-generation#image-search)，并确认所选 DMXAPI 渠道支持相关工具。

---

<p align="center">
  <small>© 2026 DMXAPI gemini-nano-banana-2.1 多图融合</small>
</p>
