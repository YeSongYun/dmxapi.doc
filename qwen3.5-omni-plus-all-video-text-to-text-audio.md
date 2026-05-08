# Qwen3.5-Omni-Plus-All 文+视频 生 文+音频 API 使用文档

基于阿里通义千问 Qwen3.5-Omni 系列最新一代全模态大模型，可同时接收文本与视频输入，并以 SSE 流式方式返回文本与音频（WAV）。模型具备强大的音视频描述能力，覆盖 74 种语言、39 种方言的输入识别与 29 种语言、7 种方言的语音输出，支持 55 种拟人音色，最长 1 小时视频、3 小时音频理解，广泛应用于内容审核、音视频交互助手、字幕生成、多方言理解等场景。

## 🌐 请求地址

```
https://www.dmxapi.cn/v1/responses
```

:::warning
请妥善保管您的 API Key！严禁将密钥泄露给他人、硬编码到代码中或提交到公开的代码仓库。如果怀疑密钥已泄露，请立即前往 DMXAPI 官网重新生成。
:::

## 🤖 模型名称

- `qwen3.5-omni-plus-all`

## 🎬 文+视频生文+音频 示例代码

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
    # 【model】(string, 必填) 指定调用的模型名称
    # 本接口支持 Qwen3.5-Omni 系列全模态模型
    "model": "qwen3.5-omni-plus-all",

    # 【input】(array, 必填) 多模态消息列表，对应 Responses 端点的输入字段
    # 每条消息包含 role 与 content，content 是由多种类型项组成的数组
    # 一条 User Message 可以包含文本与一种其他模态的数据（视频/图片/音频）
    "input": [
        {
            # 【role】(string, 必填) 对话角色，当前示例为 "user"（用户消息）
            # 可选值: "user"(用户) / "assistant"(助手，仅文本) / "system"(系统设定)
            "role": "user",

            # 【content】(array, 必填) 多模态内容数组，每一项通过 type 指定数据类型
            "content": [
                {
                    # 【type】(string, 必填) 内容类型；"video_url" 表示以公网视频 URL 方式传入视频
                    # Qwen3.5-Omni 系列最长支持 1 小时视频、单文件最大 2GB
                    # 支持格式: MP4、AVI、MKV、MOV、FLV、WMV 等
                    "type": "video_url",

                    # 【video_url】(object, 必填) 视频资源对象
                    "video_url": {
                        # 【url】(string, 必填) 视频的公网可访问 URL
                        "url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241115/cqqkru/1.mp4"
                    }
                },
                {
                    # 【type】(string, 必填) 内容类型；"text" 表示纯文本提示
                    "type": "text",

                    # 【text】(string, 必填) 向模型发送的文本指令/问题
                    "text": "视频的内容是什么"
                }
            ]
        }
    ],

    # 【stream】(boolean, 必填) 是否开启流式输出（SSE）
    # 所有 Qwen-Omni 模型都必须设置为 True，否则会报错
    "stream": True,

    # 【stream_options】(object, 可选) 流式输出的附加选项
    "stream_options": {
        # 【include_usage】(boolean, 可选) 是否在流结束时返回 Token 用量统计
        # 设置为 True 可在 response.completed 事件中读取 usage 信息
        "include_usage": True
    },

    # 【modalities】(array, 必填) 指定输出数据的模态
    # 可选值: ["text","audio"](同时输出文本与音频) / ["text"](仅输出文本)
    # 注意: 思考模式下仅支持 ["text"]
    "modalities": ["text", "audio"],

    # 【audio】(object, 可选) 音频输出配置（仅当 modalities 含 "audio" 时生效）
    "audio": {
        # 【voice】(string, 必填) 音色名称
        # Qwen3.5-Omni 支持 55 种拟人音色，如 "Tina"、"Ethan"、"Chelsie" 等
        # 完整音色列表可参见阿里云百炼「音色列表」文档
        "voice": "Tina",

        # 【format】(string, 必填) 返回音频的容器格式
        # 可选值: "wav"(默认无损) / "mp3" 等（以官方文档为准）
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

## 📊 返回示例

```text
==================================================
生成的文字内容:
==================================================
这段视频展示了一位年轻女性，她面带微笑，穿着粉色毛衣和白色内搭。她的头发是齐肩短发，看起来非常柔和自然。背景模糊，可能是在户外拍摄的，给人一种温暖和轻松的感觉。视频中，这位女性时而微笑，时而说话，表情生动，展现出一种愉悦和自信的气质。整体氛围温馨且充满活力。
==================================================
Token 用量:
   input_tokens: 4307
   input_tokens_details: {'cached_tokens': 0}
   output_tokens: 1887
   output_tokens_details: {'reasoning_tokens': 0}
   total_tokens: 6194
==================================================
音频已保存: c:\Users\15664\Desktop\qwen多模态\qwen3.5-omni-plus\文 + 视频 生 【文 + 音频】\20260416_233528.wav
```

<p align="center">
  <small>© 2026 DMXAPI Qwen3.5-Omni-Plus-All 文+视频生文+音频</small>
</p>
