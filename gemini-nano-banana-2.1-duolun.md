# Gemini Nano Banana 2.1 多轮图片修改 API 文档

Gemini Nano Banana 2.1 支持通过多轮对话生成并持续调整图片。你可以先描述画面生成初稿，再基于完整对话历史修改背景、文字、配色或人物细节。本文使用 DMXAPI 兼容的 Gemini 原生调用格式，演示“生成图片 → 保存历史 → 多轮修改”的完整流程。

:::tip 多轮一致性升级
Google 官方说明，Nano Banana 2.1 改善了多轮角色一致性、提示遵循及文字呈现；支持 1K / 2K / 4K 分辨率和 `minimal` / `medium` / `high` 思考等级，默认 `medium`。

来源：[Google 官方模型说明](https://ai.google.dev/gemini-api/docs/models/gemini-nano-banana-2.1)。
:::

## 接口地址

| 接口 | 请求方式 | URL |
|------|---------|-----|
| 生成图片与多轮修改 | POST | `https://www.dmxapi.cn/v1beta/models/gemini-nano-banana-2.1:generateContent` |

示例沿用 DMXAPI 现有 Gemini 原生兼容调用格式；新模型的渠道可用性与参数支持未做在线验证，请以 DMXAPI 控制台为准。

:::warning 注意
请妥善保管 DMXAPI API Key，不要将真实密钥提交到公开仓库。示例需要安装 `requests`。历史文件包含原图数据和对话内容，请按需要在本地保存。
:::

## 模型名称

### Gemini Nano Banana 2.1

- **模型名称**：`gemini-nano-banana-2.1`
- **名称**：Nano Banana 2.1
- **特点**：支持多轮对话式图片修改，每轮结合历史内容继续调整。
- **配置**：支持 1K / 2K / 4K 分辨率，不支持 512；思考等级默认 `medium`。

## 示例代码

先运行“生成图片”，再运行“多轮修改”。两个脚本必须在同一工作目录运行，使用同一个 `base64_data/history.json` 文件。

每轮都保存完整的模型 `content`，并按原顺序回传所有 `parts`、图片 MIME 类型和 `thoughtSignature`。不能只提取图片或重新拼接单个签名；文字部分也可能携带签名。官方说明见 [Thought signatures](https://ai.google.dev/gemini-api/docs/generate-content/image-generation#thought-signatures)。

::: code-group

```python [生成图片]
import base64
import json
from datetime import datetime
from pathlib import Path

import requests

# DMXAPI 密钥和请求地址
API_KEY = "sk-****************************************"
API_URL = "https://www.dmxapi.cn/v1beta/models/gemini-nano-banana-2.1:generateContent"
HISTORY_PATH = Path("base64_data/history.json")

headers = {
    "x-goog-api-key": API_KEY,
    "Content-Type": "application/json",
}

user_content = {
    # 【role】当前输入来自用户
    "role": "user",
    # 【parts[].text】首轮生成提示词
    "parts": [{"text": "一只可爱的小猫在愉快地玩耍。"}],
}

payload = {
    # 【contents】首轮只包含用户输入
    "contents": [user_content],
    "generationConfig": {
        # 【responseModalities】同时返回文字和图片
        "responseModalities": ["TEXT", "IMAGE"],
        "imageConfig": {
            # 【aspectRatio】输出宽高比
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

if not result.get("candidates"):
    raise ValueError(f"响应中没有候选结果：{result}")

# 原样保存完整模型内容，不丢弃文字、图片、思考部分或签名
model_content = result["candidates"][0]["content"]
history = [user_content, model_content]
HISTORY_PATH.parent.mkdir(exist_ok=True)
HISTORY_PATH.write_text(
    json.dumps(history, ensure_ascii=False, indent=2),
    encoding="utf-8",
)

# 保存最终图片时跳过 thought=true；历史中的这些部分仍然保留
output_dir = Path("output")
output_dir.mkdir(exist_ok=True)
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
image_count = 0

for part in model_content.get("parts", []):
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
print(f"完整对话历史已保存到 {HISTORY_PATH}")
```

```python [多轮修改]
import base64
import json
from datetime import datetime
from pathlib import Path

import requests

# 使用与首轮相同的密钥、模型和历史文件
API_KEY = "sk-****************************************"
API_URL = "https://www.dmxapi.cn/v1beta/models/gemini-nano-banana-2.1:generateContent"
HISTORY_PATH = Path("base64_data/history.json")

headers = {
    "x-goog-api-key": API_KEY,
    "Content-Type": "application/json",
}

# 读取已有完整历史，保留各个 parts 的内容、顺序、MIME 和签名
history = json.loads(HISTORY_PATH.read_text(encoding="utf-8"))

user_content = {
    # 【role】当前轮的用户输入
    "role": "user",
    # 【parts[].text】基于上一轮结果提出修改要求
    "parts": [{
        "text": "给这只小猫加一顶红色帽子，帽子上写着 Jonathan，保持小猫外貌和背景不变。",
    }],
}

payload = {
    # 【contents】全部历史 + 当前用户输入
    "contents": [*history, user_content],
    "generationConfig": {
        # 【responseModalities】同时返回文字和图片
        "responseModalities": ["TEXT", "IMAGE"],
        "imageConfig": {
            # 【aspectRatio】修改后图片的宽高比
            "aspectRatio": "1:1",
            # 【imageSize】本轮输出 2K；也可使用 1K 或 4K
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

if not result.get("candidates"):
    raise ValueError(f"响应中没有候选结果：{result}")

# 本轮成功后，将用户输入和完整模型输出一起追加到历史
model_content = result["candidates"][0]["content"]
history.extend([user_content, model_content])
HISTORY_PATH.write_text(
    json.dumps(history, ensure_ascii=False, indent=2),
    encoding="utf-8",
)

# 保存本轮最终图片；不对 history 中的模型 parts 做过滤
output_dir = Path("output")
output_dir.mkdir(exist_ok=True)
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
image_count = 0

for part in model_content.get("parts", []):
    if part.get("thought"):
        continue
    if "text" in part:
        print(part["text"])
    elif "inlineData" in part:
        image = part["inlineData"]
        image_count += 1
        extension = image["mimeType"].split("/")[-1]
        filename = output_dir / f"edited_image_{timestamp}_{image_count}.{extension}"
        filename.write_bytes(base64.b64decode(image["data"]))
        print(f"修改后的图片已保存到 {filename}")

if image_count == 0:
    print("响应中没有图片，请检查响应内容。")
print(f"完整对话历史已更新到 {HISTORY_PATH}")
```

:::

## 返回示例

以下为成功执行后的控制台输出示意，并非本次在线调用结果；实际文件名由运行时间和响应 MIME 类型决定。

::: code-group

```text [生成图片]
图片已保存到 output/generated_image_20261008_120000_1.png
完整对话历史已保存到 base64_data/history.json
```

```text [多轮修改]
修改后的图片已保存到 output/edited_image_20261008_120100_1.png
完整对话历史已更新到 base64_data/history.json
```

:::

下面是 `candidates[0].content` 的结构示意。实际响应可能包含更多 `parts`；占位 Base64 和签名不能用于真实请求，脚本会保存服务端返回的完整内容。

```json
{
  "role": "model",
  "parts": [
    {
      "text": "已生成图片。",
      "thoughtSignature": "<TEXT_THOUGHT_SIGNATURE>"
    },
    {
      "inlineData": {
        "mimeType": "image/png",
        "data": "<BASE64_IMAGE_DATA>"
      },
      "thoughtSignature": "<IMAGE_THOUGHT_SIGNATURE>"
    }
  ]
}
```

## 注意事项

- 将 API Key 占位符替换为自己的 DMXAPI 密钥，先运行首轮生成，再运行后续修改。
- 多轮调用应使用相同模型，并原样回传模型返回的所有 `thoughtSignature`，不能自行生成、修改或只保留最后一个签名。
- `history.json` 同时保存用户文字和模型完整输出；后续脚本会追加新一轮内容，可修改提示词后再次运行“多轮修改”。
- “生成图片”会新建并覆盖历史文件；需要开始新的作品时再运行它，继续同一作品应运行“多轮修改”。
- 历史文件中的 `mimeType` 使用真实响应值，不要将 PNG 数据硬编码为 `image/jpeg`；`thought: true` 部分仅在展示与保存最终图片时跳过。
- `imageSize` 支持 `1K` / `2K` / `4K`，不支持 `512` / `512px`。思考等级支持 `MINIMAL` / `MEDIUM` / `HIGH`，默认 `MEDIUM`。
- 如果使用官方 SDK 的聊天功能，SDK 会自动处理历史中的思考签名，见 [官方多轮图片编辑说明](https://ai.google.dev/gemini-api/docs/generate-content/image-generation#multi-turn-image-editing)。

---

<p align="center">
  <small>© 2026 DMXAPI gemini-nano-banana-2.1 多轮图片修改</small>
</p>
