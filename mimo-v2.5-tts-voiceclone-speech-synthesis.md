# mimo-v2.5-tts-voiceclone 音色复刻语音合成 API 使用文档

基于小米 MiMo v2.5 的音色复刻（Voice Clone）文本转语音接口，兼容 OpenAI 对话格式，通过 `/v1/chat/completions` 端点调用。只需在 `audio.voice` 中以 `data:{MIME_TYPE};base64,...` 形式传入一段参考音频（支持 mp3 / wav 样本，Base64 编码后不超过 10 MB），即可零样本复刻其音色，并用该音色朗读 `assistant` 消息中的目标文本；支持 `wav` / `pcm16` 输出与 24kHz 单声道音频，提供非流式与流式两种调用方式，适合个性化配音、品牌专属音色等场景。

## 接口地址

| 接口 | 请求方式 | URL |
|------|---------|-----|
| 非流式语音合成 | POST | `https://www.dmxapi.cn/v1/chat/completions` |
| 流式语音合成 | POST | `https://www.dmxapi.cn/v1/chat/completions` |

:::warning
请妥善保管您的 API Key！严禁将密钥泄露给他人、硬编码到代码中或提交到公开的代码仓库。如果怀疑密钥已泄露，请立即前往 DMXAPI 官网重新生成。
:::

## 模型名称

- `mimo-v2.5-tts-voiceclone`

## 示例代码

::: code-group

```python [Python 流式]
"""
╔═══════════════════════════════════════════════════════════════╗
║          DMXAPI mimo-v2.5-tts-voiceclone 流式语音合成         ║
╚═══════════════════════════════════════════════════════════════╝

📝 功能说明:
   本脚本演示如何使用 requests 库以流式方式调用 DMXAPI 的
   mimo-v2.5-tts-voiceclone 音色复刻接口，并实时拼接 PCM 音频后保存

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
API_URL = "https://www.dmxapi.cn/v1/chat/completions"

# 🔐 DMXAPI 密钥 (请替换为您自己的密钥)
# 获取方式: 登录 DMXAPI 官网 -> 个人中心 -> API 密钥管理
API_KEY = "sk-************************************************"

# ═══════════════════════════════════════════════════════════════
# 🎤 步骤2: 读取并编码参考音频
# ═══════════════════════════════════════════════════════════════

# 参考音频文件 (音色复刻来源)
# 目前仅支持 mp3 和 wav 格式，Base64 编码后大小不超过 10 MB
VOICE_FILE = r"C:\Users\a1\Desktop\测试专用\1782208645.wav"

with open(VOICE_FILE, "rb") as f:
    voice_base64 = base64.b64encode(f.read()).decode("utf-8")

# ═══════════════════════════════════════════════════════════════
# 📋 步骤3: 配置请求头
# ═══════════════════════════════════════════════════════════════

headers = {
    "Authorization": f"Bearer {API_KEY}",    # Bearer Token 认证方式
    "Content-Type": "application/json",       # 指定请求体为 JSON 格式
}

# ═══════════════════════════════════════════════════════════════
# 💬 步骤4: 配置请求参数
# ═══════════════════════════════════════════════════════════════

payload = {
    # 【model】(string, 必填) 调用的模型名称
    "model": "mimo-v2.5-tts-voiceclone",

    # 【messages】(array, 必填) 对话消息列表，顺序固定为 user 在前、assistant 在后
    "messages": [
        {
            # 【role】(string, 必填) 消息角色
            # 音色复刻模式下 user 留空即可，音色由参考音频决定；
            # 如有需要也可在此填入自然语言的表现力/语气指令
            "role": "user",
            # 【content】(string) 留空字符串
            "content": ""
        },
        {
            # 【role】(string, 必填) 消息角色
            # assistant 消息承载需要用复刻音色合成的目标文本
            "role": "assistant",
            # 【content】(string, 必填) 待合成的目标文本
            # 可内嵌音频标签做精细控制，如 [吸气] / [笑] / [语速加快]
            "content": "GO OUT! I HATE YOU! WHY YOU TAKE HER AWAY FROM ME!"
        }
    ],

    # 【audio】(object, 必填) 音频输出配置
    "audio": {
        # 【format】(string, 必填) 输出音频格式
        # 可选值: "wav" / "pcm16"；流式建议使用 "pcm16" 以便分块拼接
        "format": "wav",
        # 【voice】(string, 必填) 参考音频（音色复刻来源）
        # 以 data URI 形式传入: data:{MIME_TYPE};base64,{BASE64_AUDIO}
        # ⚠️ MIME 必须与样本真实格式匹配：wav 样本用 audio/wav，mp3 样本用 audio/mpeg
        # MIME 类型支持 "audio/wav" 或 "audio/mpeg"，仅支持 mp3 / wav 样本，
        # Base64 编码后不超过 10 MB
        "voice": f"data:audio/wav;base64,{voice_base64}",
    },

    # 【stream】(boolean, 可选) 是否流式输出，默认 false
    # 注意: 音色复刻为流式兼容降级模式，会在全部推理完成后一次性返回音频
    "stream": True
}

# ═══════════════════════════════════════════════════════════════
# 📤 步骤5: 发送请求并实时接收、保存音频
# ═══════════════════════════════════════════════════════════════

response = requests.post(API_URL, headers=headers, json=payload, stream=True)
response.raise_for_status()

# 输出为 24kHz PCM16LE 单声道音频，逐块累积
collected_chunks = np.array([], dtype=np.float32)

for line in response.iter_lines():
    if not line:
        continue
    line = line.decode("utf-8")
    if line.startswith("data: "):
        line = line[len("data: "):]
    if line.strip() == "[DONE]":
        break
    try:
        chunk = json.loads(line)
    except json.JSONDecodeError:
        continue

    choices = chunk.get("choices")
    if not choices:
        continue
    delta = choices[0].get("delta", {})
    audio = delta.get("audio")

    if audio is not None and "data" in audio:
        pcm_bytes = base64.b64decode(audio["data"])
        np_pcm = np.frombuffer(pcm_bytes, dtype=np.int16).astype(np.float32) / 32768.0
        collected_chunks = np.concatenate((collected_chunks, np_pcm))
        print(f"Received audio chunk of size {len(pcm_bytes)} bytes")

# 用时间戳命名保存音频
os.makedirs("tmp", exist_ok=True)
timestamp = time.strftime("%Y%m%d_%H%M%S")
output_file = os.path.join("tmp", f"{timestamp}.wav")
sf.write(output_file, collected_chunks, samplerate=24000)
print(f"音频文件已保存 {output_file}")
```

```python [Python 非流式]
import requests
import json
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
# 步骤3: 读取并编码参考音频
# ===============================================================

# 参考音频的 MIME 类型，目前仅支持 "audio/wav" 或 "audio/mpeg"(即 wav / mp3 样本)
MIME_TYPE = "audio/wav"

# 读取本地参考音频并转为 Base64 字符串
# 约束: Base64 编码后大小不超过 10 MB
with open(r"C:\Users\a1\Desktop\测试专用\1782208645.wav", "rb") as f:
    BASE64_AUDIO = base64.b64encode(f.read()).decode("utf-8")

# ===============================================================
# 步骤4: 配置请求参数
# ===============================================================

payload = {
    # 【model】(string, 必填) 调用的模型名称
    "model": "mimo-v2.5-tts-voiceclone",

    # 【messages】(array, 必填) 对话消息列表，顺序固定为 user 在前、assistant 在后
    "messages": [
        {
            # 【role】(string, 必填) 消息角色
            # 音色复刻模式下 user 留空即可，音色由参考音频决定；
            # 如有需要也可在此填入自然语言的表现力/语气指令
            "role": "user",
            # 【content】(string) 留空字符串
            "content": ""
        },
        {
            # 【role】(string, 必填) 消息角色
            # assistant 消息承载需要用复刻音色合成的目标文本
            "role": "assistant",
            # 【content】(string, 必填) 待合成的目标文本
            # 可内嵌音频标签做精细控制，如 [吸气] / [笑] / [语速加快]
            "content": "Nope,who are you?"
        }
    ],

    # 【audio】(object, 必填) 音频输出配置
    "audio": {
        # 【format】(string, 必填) 输出音频格式
        # 可选值: "wav" / "pcm16"；非流式可用 "wav"，流式建议用 "pcm16"
        "format": "wav",
        # 【voice】(string, 必填) 参考音频（音色复刻来源）
        # 以 data URI 形式传入: data:{MIME_TYPE};base64,{BASE64_AUDIO}
        # ⚠️ MIME 必须与样本真实格式匹配：wav 样本用 audio/wav，mp3 样本用 audio/mpeg
        # 目前仅支持 mp3 和 wav 格式的音频样本，Base64 编码后不超过 10 MB
        "voice": f"data:{MIME_TYPE};base64,{BASE64_AUDIO}"
    }
}

# ===============================================================
# 步骤5: 发送请求并保存音频
# ===============================================================

response = requests.post(url, headers=headers, data=json.dumps(payload))
response.raise_for_status()

result = response.json()

# 提取返回的音频数据 (base64 编码)
audio_data = result["choices"][0]["message"]["audio"]["data"]
audio_bytes = base64.b64decode(audio_data)

# 以时间戳命名保存为音频文件
filename = f"{int(time.time())}.wav"
with open(filename, "wb") as f:
    f.write(audio_bytes)

print(f"音频已保存：{filename}")
```

:::

## 返回示例

::: code-group

```text [流式返回]
Received audio chunk of size 176684 bytes
音频文件已保存 tmp\20260623_182909.wav
```

```text [非流式返回]
音频已保存：1782210020.wav
```

:::

<p align="center">
  <small>© 2026 DMXAPI mimo-v2.5-tts-voiceclone 音色复刻语音合成</small>
</p>
