# Qwen3.5-Omni-Plus-All 多模态组合输入 API 使用文档

基于阿里云通义千问 Qwen3.5-Omni 全模态旗舰模型的 Responses 端点对话接口，支持在同一请求中任意组合文本、图片、音频、视频等多模态输入，并可同时生成文本与语音双模态输出。模型具备强大的音视频描述能力，支持 113 种输入音频语言（含 74 种语言、39 种方言）、36 种输出音频语言，提供 55 种拟人音色，最长可处理 3 小时音频或 1 小时视频，适用于长视频分析、会议纪要、字幕生成、内容审核、音视频交互助手等复杂场景。

## 🌐 请求地址

```
https://www.dmxapi.cn/v1/responses
```

:::warning
请妥善保管您的 API Key！严禁将密钥泄露给他人、硬编码到代码中或提交到公开的代码仓库。如果怀疑密钥已泄露，请立即前往 DMXAPI 官网重新生成。
:::

## 🤖 模型名称

- `qwen3.5-omni-plus-all`

## 💻 多模态组合输入 示例代码

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

# ═══════════════════════════════════════════════════════════════
# 步骤2: 配置请求头
# ═══════════════════════════════════════════════════════════════

headers = {
    "Content-Type": "application/json",
    "Authorization": f"{api_key}",
}

# ═══════════════════════════════════════════════════════════════
# 步骤3: 配置请求参数
# ═══════════════════════════════════════════════════════════════

payload = {
    # 【model】(string, 必填) 调用的模型名称
    # 本文档对应模型: qwen3.5-omni-plus-all
    # 该模型为 Qwen3.5-Omni 系列旗舰版本，支持文本与图片、音频、视频的任意多模态组合输入
    "model": "qwen3.5-omni-plus-all",

    # 【input】(array, 必填) 多模态输入数组
    # 每个元素为一条消息对象，包含 role 和 content 字段
    # content 为数组，支持以下四种 type：
    #   "image_url"   - 图片输入 (公网 URL 或 data:image/png;base64,... 格式)
    #   "input_audio" - 音频输入 (公网 URL 或 Base64 编码，需在 format 中指定格式)
    #   "video_url"   - 视频输入 (公网 URL，视频中的视觉信息与音频信息会分开计费)
    #   "text"        - 文本输入 (用户的提示词或问题)
    # 多模态组合输入仅 Qwen3.5-Omni 系列支持，一个请求中可同时包含图片+音频+视频+文本任意组合
    "input": [
        {
            # 【role】(string, 必填) 消息角色
            # 可选值: "user"(用户) / "assistant"(助手) / "system"(系统)
            # 多模态内容只能放在 user 消息中
            "role": "user",
            "content": [
                {
                    # 【type】(string, 必填) 内容类型 - 图片
                    "type": "image_url",
                    "image_url": {
                        # 【url】(string, 必填) 图片地址
                        # 支持两种格式:
                        #   1) 公网 URL: "https://..."
                        #   2) Base64 编码: "data:image/png;base64,{base64_string}"
                        # 使用 Base64 编码方式时，编码后字符串大小必须小于 10MB
                        # 文件格式支持: jpg、jpeg、png、bmp、webp 等
                        "url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241022/emyrja/dog_and_girl.jpeg"
                    }
                },
                {
                    # 【type】(string, 必填) 内容类型 - 音频
                    "type": "input_audio",
                    "input_audio": {
                        # 【data】(string, 必填) 音频数据
                        # 支持公网 URL 或 Base64 编码字符串 (Base64 编码后需小于 10MB)
                        "data": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250211/tixcef/cherry.wav",
                        # 【format】(string, 必填) 音频文件格式
                        # 可选值: "wav" / "mp3" / "m4a" / "aac" / "flac" / "opus" 等常见音频格式
                        "format": "wav"
                    }
                },
                {
                    # 【type】(string, 必填) 内容类型 - 视频文件
                    "type": "video_url",
                    "video_url": {
                        # 【url】(string, 必填) 视频地址
                        # 支持公网 URL 方式 (最多 2GB) 或 Base64 编码方式 (编码后小于 10MB)
                        # 时长限制: Qwen3.5-Omni 系列最长 1 小时
                        # 文件格式: MP4、AVI、MKV、MOV、FLV、WMV 等
                        # 视频文件形式下，模型可同时理解视频中的视觉信息与音频信息 (分开计费)
                        "url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241115/cqqkru/1.mp4"
                    }
                },
                {
                    # 【type】(string, 必填) 内容类型 - 文本
                    "type": "text",
                    # 【text】(string, 必填) 用户文本提示词
                    # 用于引导模型如何综合分析上述多模态输入
                    "text": "请描述图片内容、视频内容并告诉我音频在说什么。"
                }
            ]
        }
    ],

    # 【stream】(boolean, 必填) 是否启用流式输出
    # 所有对 Qwen-Omni 模型的请求必须设置 stream=True，否则会报错
    # 流式输出采用 SSE (Server-Sent Events) 格式逐块返回文本增量和音频增量
    "stream": True,

    # 【stream_options】(object, 可选) 流式输出配置
    "stream_options": {
        # 【include_usage】(boolean, 可选) 是否在最后一个事件中返回 token 用量统计
        # 推荐设置为 True 以便监控成本与消耗
        "include_usage": True
    },

    # 【modalities】(array, 可选) 输出数据的模态
    # 可选组合:
    #   ["text"]           - 仅输出文本
    #   ["text", "audio"]  - 同时输出文本和音频 (需搭配 audio 参数)
    # 注意: 思考模式下仅支持 ["text"]
    "modalities": ["text", "audio"],

    # 【audio】(object, 可选) 音频输出配置
    # 仅当 modalities 包含 "audio" 时生效
    "audio": {
        # 【voice】(string, 必填) 发音人音色
        # Qwen3.5-Omni 系列共提供 55 种音色，覆盖多语言与多方言
        # 常见示例: "Tina" / "Ethan" / "Chelsie" / "Cherry" / "Serena" / "Dylan" 等
        # 完整音色列表请参考官方文档 "音色列表"
        "voice": "Tina",
        # 【format】(string, 必填) 音频输出格式
        # 可选值: "wav"
        # 返回的是 Base64 编码的音频数据，解码后为对应格式的音频字节
        "format": "wav"
    }
}

# ═══════════════════════════════════════════════════════════════
# 步骤4: 发送请求并提取文字与音频
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
# 步骤5: 输出文字内容
# ═══════════════════════════════════════════════════════════════

full_text = "".join(text_parts)
print("=" * 50)
print("生成的文字内容:")
print("=" * 50)
print(full_text if full_text else "(无文字输出)")
print("=" * 50)

# ═══════════════════════════════════════════════════════════════
# 步骤5.5: 输出 usage 信息
# ═══════════════════════════════════════════════════════════════

if usage_info:
    print("Token 用量:")
    for key, value in usage_info.items():
        print(f"   {key}: {value}")
    print("=" * 50)

# ═══════════════════════════════════════════════════════════════
# 步骤6: 保存音频为 WAV
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

## 📦 返回示例

```
==================================================
生成的文字内容:
==================================================
好的，根据您提供的输入，以下是图片、视频和音频的描述：

- **图片内容**:
    - 这是一张在海滩上拍摄的照片。画面中，一位女士和一只黄色的拉布拉多犬坐在沙滩上。
    - 女士穿着格子衬衫，面带微笑地看着狗狗。
    - 狗狗戴着背带，正抬起前爪，与女士的手掌相触，像是在握手或击掌。
    - 背景是平静的海面和明亮的天空，光线柔和温暖，看起来像是日出或日落时分。整个场景显得非常温馨和谐。

- **视频内容**:
    - 这是一个AI生成的短视频，右上角有"通义·AI合成"的水印。
    - 视频中是一位留着棕色波波头短发的年轻女性，她身穿粉色针织开衫和白色内搭。
    - 她正对着镜头，脸上带着灿烂的笑容，嘴巴在动，似乎正在唱歌或说话。
    - 背景是虚化的室外街景。

- **音频内容**:
    - 音频是一段中文流行歌曲的片段，由女声演唱。
    - 歌词内容为："春色恼人那不得眠，春雨涨满池塘花睡莲，春花开遍呢喃的燕，春风得意正少年。"
==================================================
Token 用量:
   input_tokens: 6434
   input_tokens_details: {'cached_tokens': 0}
   output_tokens: 5321
   output_tokens_details: {'reasoning_tokens': 0}
   total_tokens: 11755
==================================================
音频已保存: 20260417_101530.wav
```

<p align="center">
  <small>© 2026 DMXAPI Qwen3.5-Omni-Plus-All 多模态组合输入</small>
</p>
