# mimo-v2.5-tts-voicedesign 文本设计音色语音合成 API 使用文档

基于小米 MiMo v2.5 的文本设计音色（Voice Design）文本转语音接口，兼容 OpenAI 对话格式，通过 `/v1/chat/completions` 端点调用。无需提供任何音频样本，只需在 `user` 消息中用一句自然语言描述想要的音色特征（如 "Give me a young female tone."），即可即时设计出对应音色并朗读 `assistant` 消息中的目标文本；可选 `optimize_text_preview` 智能润色播报文本（开启后甚至可省略 `assistant`）。支持 `wav` / `pcm16` 输出与 24kHz 单声道音频，提供非流式与流式两种调用方式，适合快速试听、角色配音、创意音色探索等场景。

## 接口地址

| 接口 | 请求方式 | URL |
|------|---------|-----|
| 非流式语音合成 | POST | `https://www.dmxapi.cn/v1/chat/completions` |
| 流式语音合成 | POST | `https://www.dmxapi.cn/v1/chat/completions` |

:::warning
请妥善保管您的 API Key！严禁将密钥泄露给他人、硬编码到代码中或提交到公开的代码仓库。如果怀疑密钥已泄露，请立即前往 DMXAPI 官网重新生成。
:::

## 模型名称

- `mimo-v2.5-tts-voicedesign`

## 示例代码

::: code-group

```python [Python 流式]
"""
╔═══════════════════════════════════════════════════════════════╗
║        DMXAPI mimo-v2.5-tts-voicedesign 流式语音合成          ║
╚═══════════════════════════════════════════════════════════════╝

📝 功能说明:
   本脚本演示如何使用 requests 库以流式方式调用 DMXAPI 的
   mimo-v2.5-tts-voicedesign 文本设计音色接口，并实时拼接 PCM 音频后保存

═══════════════════════════════════════════════════════════════
"""

import base64
import os
import time
import json
import numpy as np
import soundfile as sf
import requests

# ═══════════════════════════════════════════════════════════════
# 🔑 步骤1: 配置 API 连接信息
# ═══════════════════════════════════════════════════════════════

# 🌐 DMXAPI 服务端点地址
url = "https://www.dmxapi.cn/v1/chat/completions"

# 🔐 DMXAPI 密钥 (请替换为您自己的密钥)
# 获取方式: 登录 DMXAPI 官网 -> 个人中心 -> API 密钥管理
API_KEY = "sk-************************************************"

# ═══════════════════════════════════════════════════════════════
# 📋 步骤2: 配置请求头
# ═══════════════════════════════════════════════════════════════

headers = {
    "Authorization": f"Bearer {API_KEY}",    # Bearer Token 认证方式
    "Content-Type": "application/json",       # 指定请求体为 JSON 格式
}

# ═══════════════════════════════════════════════════════════════
# 💬 步骤3: 配置请求参数
# ═══════════════════════════════════════════════════════════════

data = {
    # 【model】(string, 必填) 调用的模型名称
    "model": "mimo-v2.5-tts-voicedesign",

    # 【messages】(array, 必填) 对话消息列表，顺序固定为 user 在前、assistant 在后
    "messages": [
        {
            # 【role】(string, 必填) 消息角色
            # 文本设计音色模式下 user 消息必填，用自然语言描述想要设计的音色特征
            # 该描述用于设计音色，本身不会被朗读
            "role": "user",
            # 【content】(string, 必填) 音色设计描述文本
            "content": "Give me a young angey female tone."
        },
        {
            # 【role】(string, 必填) 消息角色
            # assistant 消息承载需要合成为语音的目标文本
            "role": "assistant",
            # 【content】(string) 待合成的目标文本
            # 当 optimize_text_preview 为 true 时，可省略本条 assistant 消息
            "content": "You are UN-BE-LIEVABLE! I am sooooo done with your constant lies. GET. OUT!"
        }
    ],

    # 【audio】(object, 必填) 音频输出配置
    "audio": {
        # 【format】(string, 必填) 输出音频格式
        # 可选值: "wav" / "pcm16"；流式建议使用 "pcm16" 以便分块拼接
        "format": "pcm16",
        # 【optimize_text_preview】(boolean, 可选) 是否智能润色目标播报文本，默认 false
        # 置为 true 时系统可自动生成/润色播报文本，此时可省略 assistant 消息
        "optimize_text_preview": True
    },

    # 【stream】(boolean, 可选) 是否流式输出，默认 false
    # 注意: 文本设计音色为流式兼容降级模式，会在全部推理完成后一次性返回音频
    "stream": True
}

# ═══════════════════════════════════════════════════════════════
# 📤 步骤4: 发送请求并实时接收、保存音频
# ═══════════════════════════════════════════════════════════════

response = requests.post(url, headers=headers, data=json.dumps(data), stream=True)

# 输出为 24kHz PCM16LE 单声道音频，逐块累积
collected_chunks = np.array([], dtype=np.float32)

for line in response.iter_lines():
    if not line:
        continue
    decoded_line = line.decode("utf-8")

    # SSE 格式，数据以 "data: " 开头
    if not decoded_line.startswith("data: "):
        continue

    content = decoded_line[len("data: "):]
    if content.strip() == "[DONE]":
        break

    try:
        chunk = json.loads(content)
    except json.JSONDecodeError:
        continue

    choices = chunk.get("choices")
    if not choices:
        continue

    delta = choices[0].get("delta", {})
    audio = delta.get("audio")

    if audio is not None:
        pcm_bytes = base64.b64decode(audio["data"])
        np_pcm = np.frombuffer(pcm_bytes, dtype=np.int16).astype(np.float32) / 32768.0
        collected_chunks = np.concatenate((collected_chunks, np_pcm))
        print(f"Received audio chunk of size {len(pcm_bytes)} bytes")

# 用时间戳命名保存音频
os.makedirs("tmp", exist_ok=True)
timestamp = time.strftime("%Y%m%d_%H%M%S")
output_file = f"tmp/output_{timestamp}.wav"
sf.write(output_file, collected_chunks, samplerate=24000)
print(f"音频已保存为 {output_file}")
```

```python [Python 非流式]
import requests
import base64
import time

# ===============================================================
# 步骤1: 配置 API 连接信息
# ===============================================================

# DMXAPI 服务端点地址
url = "https://www.dmxapi.cn/v1/chat/completions"

# DMXAPI 密钥 (请替换为您自己的密钥)
# 获取方式: 登录 DMXAPI 官网 -> 个人中心 -> API 密钥管理
API_KEY = "sk-************************************************"

# ===============================================================
# 步骤2: 配置请求头
# ===============================================================

headers = {
    "Authorization": f"Bearer {API_KEY}",    # Bearer Token 认证方式
    "Content-Type": "application/json",       # 指定请求体为 JSON 格式
}

# ===============================================================
# 步骤3: 配置请求参数
# ===============================================================

data = {
    # 【model】(string, 必填) 调用的模型名称
    "model": "mimo-v2.5-tts-voicedesign",

    # 【messages】(array, 必填) 对话消息列表，顺序固定为 user 在前、assistant 在后
    "messages": [
        {
            # 【role】(string, 必填) 消息角色
            # 文本设计音色模式下 user 消息必填，用自然语言描述想要设计的音色特征
            # 该描述用于设计音色，本身不会被朗读
            "role": "user",
            # 【content】(string, 必填) 音色设计描述文本
            "content": "Give me a young female tone."
        },
        {
            # 【role】(string, 必填) 消息角色
            # assistant 消息承载需要合成为语音的目标文本
            "role": "assistant",
            # 【content】(string) 待合成的目标文本
            # 当 optimize_text_preview 为 true 时，可省略本条 assistant 消息
            "content": "Yes, I had a sandwich."
        }
    ],

    # 【audio】(object, 必填) 音频输出配置
    "audio": {
        # 【format】(string, 必填) 输出音频格式
        # 可选值: "wav" / "pcm16"；非流式可用 "wav"，流式建议用 "pcm16"
        "format": "wav",
        # 【optimize_text_preview】(boolean, 可选) 是否智能润色目标播报文本，默认 false
        # 置为 true 时系统可自动生成/润色播报文本，此时可省略 assistant 消息
        "optimize_text_preview": True
    }
}

# ===============================================================
# 步骤4: 发送请求并保存音频
# ===============================================================

response = requests.post(url, headers=headers, json=data)

if response.status_code == 200:
    result = response.json()
    # 提取返回的音频数据 (base64 编码)
    audio_b64 = result["choices"][0]["message"]["audio"]["data"]
    audio_bytes = base64.b64decode(audio_b64)

    filename = f"{int(time.time())}.wav"  # 以时间戳命名
    with open(filename, "wb") as f:
        f.write(audio_bytes)
    print(f"音频已保存为: {filename}")
else:
    print("请求失败:", response.status_code, response.text)
```

:::

## 返回示例

::: code-group

```text [流式返回]
Received audio chunk of size 422400 bytes
音频已保存为 tmp/output_20260623_180634.wav
```

```text [非流式返回]
音频已保存为: 1782208696.wav
```

:::

<p align="center">
  <small>© 2026 DMXAPI mimo-v2.5-tts-voicedesign 文本设计音色语音合成</small>
</p>
