# qwen3.5-omni-plus-all 文+本地音频 生 文+音频 API 使用文档

qwen3.5-omni-plus-all 是 Qwen3.5-Omni 系列最新一代全模态大模型，支持多模态输入（文本、图像、音频、视频）与文本/语音输出。本接口演示通过 `/v1/responses` 端点，将本地音频（Base64 编码）+ 文本提示一并发送给模型，模型以流式方式同时返回文字回复与合成音频（WAV 格式），覆盖 74 种语言与 39 种方言的音频理解，以及 29 种语言、7 种方言共 55 种拟人音色的音频输出，适用于音频摘要、音视频交互助手、语音问答、有声内容创作等场景。

## 请求地址

```
https://www.dmxapi.cn/v1/responses
```

## 模型名称

- `qwen3.5-omni-plus-all`

:::warning
请妥善保管您的 API Key！严禁将密钥泄露给他人、硬编码到代码中或提交到公开的代码仓库。
:::

## 示例代码

```python
import requests
import json
import base64
import time
import os

# ═══════════════════════════════════════════════════════════════
# 步骤1: 配置 API 连接信息
# ═══════════════════════════════════════════════════════════════

url = "https://www.dmxapi.cn/v1/responses"

api_key = "sk-******************************************"

# 本地音频路径（相对路径或绝对路径均可）
audio_path = r"C:\Users\15664\Desktop\qwen多模态\qwen3.5-omni-plus\文 + 视频 生 【文 + 音频】\20260416_113855.wav"

# 本地音频格式（mp3 / wav 等，需与 audio_path 文件一致）
audio_format = "wav"

# ═══════════════════════════════════════════════════════════════
# 步骤2: 配置请求头
# ═══════════════════════════════════════════════════════════════

headers = {
    "Content-Type": "application/json",
    "Authorization": f"{api_key}",
}

# ═══════════════════════════════════════════════════════════════
# 步骤3: 本地音频 Base64 编码
# ═══════════════════════════════════════════════════════════════


def encode_audio(path):
    with open(path, "rb") as audio_file:
        return base64.b64encode(audio_file.read()).decode("utf-8")


base64_audio = encode_audio(audio_path)

# ═══════════════════════════════════════════════════════════════
# 步骤4: 配置请求参数
# ═══════════════════════════════════════════════════════════════

payload = {
    # 【model】(string, 必填) 模型名称。本文档仅对应 qwen3.5-omni-plus-all 全模态模型，
    # 该模型支持 3 小时音频或 1 小时视频，支持多模态组合输入与文本/音频输出。
    "model": "qwen3.5-omni-plus-all",

    # 【input】(array, 必填) 传递给大模型的上下文消息数组，按对话顺序排列。
    # 在 /v1/responses 端点下，该字段对应标准 messages 结构，每条消息包含 role 与 content。
    "input": [
        {
            # 【role】(string, 必填) 消息角色。可选值:
            # "system"(系统消息，用于设定模型角色或约束) / "user"(用户消息，传递问题或上下文)
            # / "assistant"(模型回复，多轮对话中回传)
            "role": "user",

            # 【content】(array, 必填) 消息内容数组，支持多模态 Part 混合。
            # 每个元素由 type 字段指定类型，可组合文本与本地/URL 音频、图像、视频。
            "content": [
                {
                    # 【type】(string, 必填) 内容片段类型。
                    # 可选值: "input_text"/"text"(文本) / "input_image"(图像)
                    # / "input_audio"(音频) / "input_video"(视频)
                    "type": "input_audio",

                    # 【input_audio】(object, 必填，type=input_audio 时) 音频内容配置对象。
                    "input_audio": {
                        # 【data】(string, 必填) 音频内容数据。
                        # 支持 Base64 编码(格式: data:;base64,{base64字符串})，也支持
                        # 公网可访问的音频 URL。本示例使用本地文件 Base64 编码后传入。
                        "data": f"data:;base64,{base64_audio}",

                        # 【format】(string, 必填) 音频文件格式，需与 data 中的实际音频格式一致。
                        # 可选值: "wav" / "mp3" 等常见音频格式。
                        "format": audio_format,
                    },
                },
                {
                    # 【type】(string, 必填) 此 Part 的类型为文本。
                    "type": "text",

                    # 【text】(string, 必填) 用户输入的文本内容，与音频共同构成本轮对话输入。
                    "text": "这段音频在说什么",
                },
            ],
        }
    ],

    # 【stream】(boolean, 可选) 默认值 false。是否以流式输出方式回复。
    # 注意: Qwen-Omni 模型所有请求必须设置为 true，否则会报错。
    # true: 边生成边输出，每生成一部分内容即返回一个数据块(chunk)；
    # false: 一次性返回全部内容(Omni 模型不支持)。
    "stream": True,

    # 【stream_options】(object, 可选) 流式输出的配置项，仅在 stream=true 时生效。
    "stream_options": {
        # 【include_usage】(boolean, 可选) 默认值 false。
        # 是否在响应的最后一个数据块包含 Token 消耗信息。
        # true: 包含 usage 字段 / false: 不包含。
        "include_usage": True
    },

    # 【modalities】(array, 可选) 默认值 ["text"]。输出数据的模态，仅适用于 Qwen-Omni 模型。
    # 可选值:
    # ["text", "audio"]: 同时输出文本与音频(本示例) / ["text"]: 仅输出文本。
    "modalities": ["text", "audio"],

    # 【audio】(object, 可选) 输出音频的音色与格式。
    # 仅适用于 Qwen-Omni 模型，且必须配合 modalities=["text","audio"] 使用。
    "audio": {
        # 【voice】(string, 必填，开启音频输出时) 输出音频的音色。
        # Qwen3.5-Omni 提供 55 种拟人音色(覆盖 29 种语言、7 种方言)，如 "Tina"、"Cherry"、
        # "Ethan" 等。完整列表参见官方音色列表文档。
        "voice": "Tina",

        # 【format】(string, 必填，开启音频输出时) 输出音频格式。
        # 可选值: "wav"(无损 PCM, 24kHz) 等。
        "format": "wav",
    },
}

# ═══════════════════════════════════════════════════════════════
# 步骤5: 发送请求并提取文字与音频
# ═══════════════════════════════════════════════════════════════

text_parts = []
audio_parts = []
usage_info = None
current_event = None

with requests.post(url, headers=headers, json=payload, stream=True) as response:
    if not response.ok:
        print(f"[HTTP {response.status_code}] {response.text}")
        response.raise_for_status()

    for line in response.iter_lines():
        if not line:
            continue
        line = line.decode("utf-8")

        if line.startswith("event:"):
            current_event = line[len("event:"):].strip()
            continue

        if not line.startswith("data:"):
            continue
        data_str = line[len("data:"):].strip()
        if data_str == "[DONE]":
            break

        try:
            data = json.loads(data_str)
        except json.JSONDecodeError:
            continue

        # 文字增量
        if current_event == "response.output_text.delta":
            text = data.get("delta", "")
            if text:
                text_parts.append(text)

        # 音频数据（完整 WAV，base64 编码）
        elif current_event == "response.output_item.done":
            for part in data.get("item", {}).get("content", []):
                if "audio" in part and part["audio"].get("data"):
                    audio_parts.append(part["audio"]["data"])

        # usage 统计
        elif current_event == "response.completed":
            usage_info = data.get("response", {}).get("usage")

# ═══════════════════════════════════════════════════════════════
# 步骤6: 输出文字内容
# ═══════════════════════════════════════════════════════════════

full_text = "".join(text_parts)
print("=" * 50)
print("生成的文字内容:")
print("=" * 50)
print(full_text if full_text else "(无文字输出)")
print("=" * 50)

# ═══════════════════════════════════════════════════════════════
# 步骤6.5: 输出 usage 信息
# ═══════════════════════════════════════════════════════════════

if usage_info:
    print("Token 用量:")
    for key, value in usage_info.items():
        print(f"   {key}: {value}")
    print("=" * 50)

# ═══════════════════════════════════════════════════════════════
# 步骤7: 保存音频为 WAV
# ═══════════════════════════════════════════════════════════════

if audio_parts:
    audio_bytes = base64.b64decode("".join(audio_parts))

    timestamp = time.strftime("%Y%m%d_%H%M%S")
    output_dir = os.path.dirname(os.path.abspath(__file__))

    wav_path = os.path.join(output_dir, f"{timestamp}.wav")
    with open(wav_path, "wb") as f:
        f.write(audio_bytes)
    print(f"音频已保存: {wav_path}")
else:
    print("未收到音频数据")
```

## 返回示例

```json
==================================================
生成的文字内容:
==================================================
这段音频描述了一段视频的内容，具体如下：

*   **人物**：视频中有一位年轻女性，留着齐肩的棕色短发和刘海。她身穿粉色针织开衫，内搭白色T恤，并佩戴着一条简单的项链。
*   **背景与氛围**：背景是模糊的城市街景。整个视频的氛围温暖而明亮，像是在一个晴朗的日子拍摄的。
*   **表情与情绪**：这位女性的表情从微笑逐渐变为大笑，显得生动活泼、亲切友好，营造出一种愉悦和轻松的感觉。
*   **关键信息**：视频的右上角有一个水印，显示"通义AI合成"，这表明该视频内容很可能是由人工智能生成的。
==================================================
Token 用量:
   input_tokens: 2151
   input_tokens_details: {'cached_tokens': 0}
   output_tokens: 2457
   output_tokens_details: {'reasoning_tokens': 0}
   total_tokens: 4608
==================================================
音频已保存: c:\Users\15664\Desktop\qwen多模态\qwen3.5-omni-plus\音频本地文件\20260416_234248.wav
```

<p align="center">
  <small>© 2026 DMXAPI qwen3.5-omni-plus-all 文 + 本地音频 生 文 + 音频</small>
</p>
