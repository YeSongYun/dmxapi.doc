# Qwen3.5-Omni-Plus-All 文本+本地视频 生 文本+音频 API 使用文档

基于阿里云通义千问 Qwen3.5-Omni 系列最新一代全模态模型的 Responses 端点调用，支持文本、图片、音频、视频任意组合的多模态输入，可同步输出文本与语音（WAV 格式）。模型原生支持 3 小时音频或 1 小时视频的长序列理解，覆盖 113 种输入语言/方言、36 种输出语言/方言，提供 55 种拟人音色（含 Tina、Cherry、Serena、Ethan、Chelsie 等），适用于长视频分析、会议纪要、字幕生成、内容审核、音视频交互助手等场景。本接入通过 DMXAPI 的 `/v1/responses` 端点，统一以 SSE 流式事件返回文字增量与 Base64 编码的音频数据。

## 🌐 请求地址

```
https://www.dmxapi.cn/v1/responses
```
:::warning
请妥善保管您的 API Key！严禁将密钥泄露给他人、硬编码到代码中或提交到公开的代码仓库。如果怀疑密钥已泄露，请立即前往 DMXAPI 官网重新生成。
:::

## 🧠 模型名称

- `qwen3.5-omni-plus-all`

## 📹 文本+本地视频生成文本+音频 示例代码

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

api_key = "sk-************************************************"

# 本地视频路径，请改成你的视频绝对路径（前面的 r 必须保留，防止 \ 转义）
video_path = r"C:/Users/a1/Desktop/测试保存代码/111.mp4"

# ═══════════════════════════════════════════════════════════════
# 步骤2: 配置请求头
# ═══════════════════════════════════════════════════════════════

headers = {
    "Content-Type": "application/json",
    "Authorization": f"{api_key}",
}

# ═══════════════════════════════════════════════════════════════
# 步骤3: 本地视频 Base64 编码
# ═══════════════════════════════════════════════════════════════


def encode_video(path):
    with open(path, "rb") as video_file:
        return base64.b64encode(video_file.read()).decode("utf-8")


base64_video = encode_video(video_path)

# ═══════════════════════════════════════════════════════════════
# 步骤4: 配置请求参数
# ═══════════════════════════════════════════════════════════════

payload = {
    # 【model】(string, 必填) 指定调用的模型名称
    # 本文档固定为 qwen3.5-omni-plus-all（Qwen3.5-Omni 系列最新一代全模态模型）
    # 适用于长视频分析、会议纪要、字幕生成、内容审核、音视频交互等场景
    "model": "qwen3.5-omni-plus-all",

    # 【input】(array, 必填) 多模态输入内容数组，Responses 端点专用字段（对应 Chat Completions 的 messages）
    # 每个元素是一条消息对象，包含 role 与 content
    # role 取值: "user"(用户消息) / "system"(系统消息，输出含音频时不支持) / "assistant"(助手消息)
    # content 为数组，可混合多种 type：
    #   - "text"      纯文本
    #   - "video_url" 视频(URL 或 data:;base64,... Data URL)
    #   - "image_url" 图像(URL 或 data:image/png;base64,... Data URL)
    #   - "input_audio" 音频
    # Qwen3.5-Omni 系列支持文本与图片、音频、视频的任意组合同时输入，不限于单一模态
    "input": [
        {
            "role": "user",
            "content": [
                {
                    # 【type=video_url】(string) 声明当前内容项为视频输入
                    "type": "video_url",
                    # 【video_url】(object) 视频的访问地址
                    # url 可以是公网可访问的视频 URL，也可以是本地视频的 Base64 Data URL
                    # 本地视频需先通过 base64 编码，再以 "data:;base64,<编码>" 传入
                    # 支持的视频文件格式: MP4、AVI、MKV、MOV、FLV、WMV 等
                    # Qwen3.5-Omni 系列输入限制: 最长 1 小时视频；视频文件中视觉与音频信息分开计费
                    "video_url": {"url": f"data:;base64,{base64_video}"},
                },
                {
                    # 【type=text】(string) 声明当前内容项为纯文本
                    "type": "text",
                    # 【text】(string) 与视频一同发送给模型的文本指令/提问
                    "text": "视频中呈现了什么内容？",
                },
            ],
        }
    ],

    # 【stream】(boolean, 必填) 是否使用流式输出
    # Qwen-Omni 模型在 modalities 含 "audio" 时必须设置为 True，否则会报错
    # 流式下服务器通过 SSE 协议逐步推送文字增量和音频分片
    "stream": True,

    # 【stream_options】(object, 可选) 流式输出附加配置
    # include_usage: True 表示在最后一条事件中返回 token 用量统计（input_tokens / output_tokens / total_tokens 等）
    "stream_options": {"include_usage": True},

    # 【modalities】(array, 可选) 指定模型输出的数据模态
    # 可选值:
    #   ["text"]           仅输出文本（思考模式下必须使用此值）
    #   ["text", "audio"]  同时输出文本和音频（默认推荐，需配合 audio 字段）
    # 当包含 "audio" 时，stream 必须为 True，且当前系列不支持在包含音频输出时设置 System Message
    "modalities": ["text", "audio"],

    # 【audio】(object, 可选) 当 modalities 包含 "audio" 时生效，控制音频输出参数
    "audio": {
        # 【voice】(string, 必填) 音色名称
        # Qwen3.5-Omni 系列提供 55 种拟人音色，常用示例:
        #   "Tina"(女声，温柔亲切) / "Cherry"(女声，甜美青春) / "Serena"(女声，知性优雅)
        #   "Ethan"(男声，沉稳) / "Chelsie"(女声，活泼) / "Dylan"(男声，磁性)
        # 完整音色列表请查阅阿里云百炼「Qwen-Omni 音色列表」页面
        "voice": "Tina",

        # 【format】(string, 必填) 音频输出格式
        # 目前主要支持 "wav"(采样率 24000Hz，int16 PCM 封装)
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
chunks = []

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
            chunks.append({"event": current_event, "data": "[DONE]"})
            break

        try:
            data = json.loads(data_str)
        except json.JSONDecodeError:
            chunks.append({"event": current_event, "data": data_str, "error": "JSONDecodeError"})
            continue

        chunks.append({"event": current_event, "data": data})

        if current_event == "response.output_text.delta":
            text = data.get("delta", "")
            if text:
                text_parts.append(text)

        elif current_event == "response.output_item.done":
            for part in data.get("item", {}).get("content", []):
                if "audio" in part and part["audio"].get("data"):
                    audio_parts.append(part["audio"]["data"])

        elif current_event == "response.completed":
            usage_info = data.get("response", {}).get("usage")

output_json_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "b_1_output.json")
with open(output_json_path, "w", encoding="utf-8") as f:
    json.dump(chunks, f, ensure_ascii=False, indent=2)
print(f"已保存 {len(chunks)} 条 SSE 数据到: {output_json_path}")

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

## 📨 返回示例

```text
已保存 77 条 SSE 数据到: c:\Users\a1\Desktop\测试保存代码\b_1_output.json
==================================================
生成的文字内容:
==================================================
视频展示了一本黄色封面的书，书名为《都柏林人》（Dubliners），作者是詹姆斯·乔伊斯。封面上有一幅插图，描绘了一位穿着大衣、戴着帽子的人物，背景是城市街景。书的旁边放着一支白色和蓝色相间的笔。视频中有一只手在翻动书页或调整书的位置。背景中可以看到一些办公用品和设备。
==================================================
Token 用量:
   input_tokens: 2624
   input_tokens_details: {'cached_tokens': 0}
   output_tokens: 1708
   output_tokens_details: {'reasoning_tokens': 0}
   total_tokens: 4332
==================================================
音频已保存: c:\Users\a1\Desktop\测试保存代码\20260520_185006.wav
```

<p align="center">
  <small>© 2026 DMXAPI qwen3.5-omni-plus-all 文本+本地视频 → 文本+音频</small>
</p>
