# mimo-v2.5-tts 预置音色语音合成 API 使用文档

基于小米 MiMo v2.5 的文本转语音（TTS）接口，兼容 OpenAI 对话格式，通过 `/v1/chat/completions` 端点调用。内置 9 种预置音色（`mimo_default` 及中文「冰糖 / 茉莉 / 苏打 / 白桦」、英文「Mia / Chloe / Milo / Dean」），以 `user` 消息下达自然语言风格指令、`assistant` 消息承载待合成文本，支持 `[吸气]`/`[笑]`/`[语速加快]` 等音频标签与 `(唱歌)` 歌唱合成；可输出 `wav` / `pcm16` 两种格式，并提供 24kHz 单声道的非流式与逐块流式两种调用方式，适合配音、播报、有声内容等场景。

## 接口地址

| 接口 | 请求方式 | URL |
|------|---------|-----|
| 非流式语音合成 | POST | `https://www.dmxapi.cn/v1/chat/completions` |
| 流式语音合成 | POST | `https://www.dmxapi.cn/v1/chat/completions` |

:::warning
请妥善保管您的 API Key！严禁将密钥泄露给他人、硬编码到代码中或提交到公开的代码仓库。如果怀疑密钥已泄露，请立即前往 DMXAPI 官网重新生成。
:::

## 模型名称

- `mimo-v2.5-tts`

## 示例代码

::: code-group

```python [Python 流式]
"""
╔═══════════════════════════════════════════════════════════════╗
║              DMXAPI mimo-v2.5-tts 流式语音合成                 ║
╚═══════════════════════════════════════════════════════════════╝

📝 功能说明:
   本脚本演示如何使用 requests 库以流式方式调用 DMXAPI 的
   mimo-v2.5-tts 预置音色语音合成接口，并实时拼接 PCM 音频后保存

═══════════════════════════════════════════════════════════════
"""

import base64
import os
import json
import time
from datetime import datetime
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
    "model": "mimo-v2.5-tts",

    # 【messages】(array, 必填) 对话消息列表，顺序固定为 user 在前、assistant 在后
    "messages": [
        {
            # 【role】(string, 必填) 消息角色
            # user 消息提供自然语言的风格/语气指令，用于控制合成语音的情感与表现力
            # 该内容不会被朗读，不会出现在最终音频中；预置音色模式下此条可选
            "role": "user",
            # 【content】(string) 风格/语气描述文本
            "content": "Bright, bouncy, slightly sing-song tone — like you're bursting with good news you can barely hold in. Fast pace, rising pitch at the end."
        },
        {
            # 【role】(string, 必填) 消息角色
            # assistant 消息承载需要合成为语音的目标文本
            "role": "assistant",
            # 【content】(string, 必填) 待合成的目标文本
            # 可内嵌音频标签 [..] 做行内精细控制（任意位置）：
            #   呼吸 [吸气]/[深呼吸]/[叹气]、情绪 [紧张]/[激动]/[疲惫]、特征 [颤抖]/[破音]/[气声]、哭笑 [笑]/[轻笑]/[抽泣]/[哽咽]
            # 也可在文本开头加风格标签 (..)（可多风格同标签，如 (开心 变快)）：
            #   情绪(开心/悲伤/愤怒)、语调(温柔/高冷/活泼/严肃)、人设(夹子音/御姐音/大叔音)、方言(东北话/四川话/粤语)、角色(孙悟空/林黛玉)
            # 唱歌：(唱歌)/(sing)/(singing) 等效，需单独使用、勿与其他风格混用，中文歌词更佳
            "content": "Hey boss — guess what, guess what? I just got the results back and I actually passed! Not just passed, I got a distinction! I know, I know — you told me I was cutting it close, but hey, here we are. Drinks are on me tonight, okay?"
        }
    ],

    # 【audio】(object, 必填) 音频输出配置
    "audio": {
        # 【format】(string, 必填) 输出音频格式
        # 可选值: "wav" / "pcm16"；流式调用建议指定为 "pcm16" 以便分块拼接
        "format": "pcm16",
        # 【voice】(string, 必填) 预置音色名称
        # 可选值: "mimo_default"(默认音色) /
        #   "冰糖"(中文女声) / "茉莉"(中文女声) / "苏打"(中文男声) / "白桦"(中文男声) /
        #   "Mia"(英文女声) / "Chloe"(英文女声) / "Milo"(英文男声) / "Dean"(英文男声)
        "voice": "Chloe"
    },

    # 【stream】(boolean, 可选) 是否流式输出，默认 false
    # 置为 true 时以 SSE 分块返回音频；mimo-v2.5-tts 支持逐块实时流式
    "stream": True
}

# ═══════════════════════════════════════════════════════════════
# 📤 步骤4: 发送请求并实时接收、保存音频
# ═══════════════════════════════════════════════════════════════

response = requests.post(url, headers=headers, json=data, stream=True)

# 输出为 24kHz PCM16LE 单声道音频，逐块累积
collected_chunks: np.ndarray = np.array([], dtype=np.float32)

for line in response.iter_lines():
    if not line:
        continue
    decoded_line = line.decode("utf-8")

    # SSE 格式去掉 "data: " 前缀
    if decoded_line.startswith("data: "):
        decoded_line = decoded_line[len("data: "):]

    if decoded_line.strip() == "[DONE]":
        break

    try:
        chunk = json.loads(decoded_line)
    except json.JSONDecodeError:
        continue

    if not chunk.get("choices"):
        continue

    delta = chunk["choices"][0].get("delta", {})
    audio = delta.get("audio", None)

    if audio is not None:
        pcm_bytes = base64.b64decode(audio["data"])
        np_pcm = np.frombuffer(pcm_bytes, dtype=np.int16).astype(np.float32) / 32768.0
        collected_chunks = np.concatenate((collected_chunks, np_pcm))
        print(f"已接收音频数据块，大小 {len(pcm_bytes)} 字节")

# 用时间戳命名文件保存
os.makedirs("tmp", exist_ok=True)
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
filename = f"tmp/output_{timestamp}.wav"
sf.write(filename, collected_chunks, samplerate=24000)
print(f"音频已保存至 {filename}")
```

```python [Python 非流式]
import base64
import requests
from datetime import datetime

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

payload = {
    # 【model】(string, 必填) 调用的模型名称
    "model": "mimo-v2.5-tts",

    # 【messages】(array, 必填) 对话消息列表，顺序固定为 user 在前、assistant 在后
    "messages": [
        {
            # 【role】(string, 必填) 消息角色
            # user 消息提供自然语言的风格/语气指令，用于控制合成语音的情感与表现力
            # 该内容不会被朗读，不会出现在最终音频中；预置音色模式下此条可选
            "role": "user",
            # 【content】(string) 风格/语气描述文本
            "content": "Bright, bouncy, slightly sing-song tone — like you are bursting with good news you can barely hold in. Fast pace, rising pitch at the end."
        },
        {
            # 【role】(string, 必填) 消息角色
            # assistant 消息承载需要合成为语音的目标文本
            "role": "assistant",
            # 【content】(string, 必填) 待合成的目标文本
            # 可内嵌音频标签 [..] 做行内精细控制（任意位置）：
            #   呼吸 [吸气]/[深呼吸]/[叹气]、情绪 [紧张]/[激动]/[疲惫]、特征 [颤抖]/[破音]/[气声]、哭笑 [笑]/[轻笑]/[抽泣]/[哽咽]
            # 也可在文本开头加风格标签 (..)（可多风格同标签，如 (开心 变快)）：
            #   情绪(开心/悲伤/愤怒)、语调(温柔/高冷/活泼/严肃)、人设(夹子音/御姐音/大叔音)、方言(东北话/四川话/粤语)、角色(孙悟空/林黛玉)
            # 唱歌：(唱歌)/(sing)/(singing) 等效，需单独使用、勿与其他风格混用，中文歌词更佳
            "content": "Hey boss — guess what, guess what? I just got the results back and I actually passed! Not just passed, I got a distinction! I know, I know — you told me I was cutting it close, but hey, here we are. Drinks are on me tonight, okay?"
        }
    ],

    # 【audio】(object, 必填) 音频输出配置
    "audio": {
        # 【format】(string, 必填) 输出音频格式
        # 可选值: "wav" / "pcm16"；非流式可用 "wav"，流式建议用 "pcm16"
        "format": "wav",
        # 【voice】(string, 必填) 预置音色名称
        # 可选值: "mimo_default"(默认音色) /
        #   "冰糖"(中文女声) / "茉莉"(中文女声) / "苏打"(中文男声) / "白桦"(中文男声) /
        #   "Mia"(英文女声) / "Chloe"(英文女声) / "Milo"(英文男声) / "Dean"(英文男声)
        "voice": "Chloe"
    }
}

# ===============================================================
# 步骤4: 发送请求并保存音频
# ===============================================================

response = requests.post(url, headers=headers, json=payload)
response.raise_for_status()

data = response.json()

# 提取返回的音频数据 (base64 编码)
audio_b64 = data["choices"][0]["message"]["audio"]["data"]
audio_bytes = base64.b64decode(audio_b64)

# 以时间戳命名保存为音频文件
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
output_file = f"output_{timestamp}.wav"

with open(output_file, "wb") as f:
    f.write(audio_bytes)

print(f"✅ 音频已保存到 {output_file}")
```

:::

## 返回示例

::: code-group

```text [流式返回]
已接收音频数据块，大小 7680 字节
已接收音频数据块，大小 15360 字节
已接收音频数据块，大小 15360 字节
已接收音频数据块，大小 15360 字节
已接收音频数据块，大小 15360 字节
.
.
.
已接收音频数据块，大小 15360 字节
已接收音频数据块，大小 23040 字节
音频已保存至 tmp/output_20260623_171635.wav
```

```text [非流式返回]
✅ 音频已保存到 output_20260623_165655.wav
```

:::

<p align="center">
  <small>© 2026 DMXAPI mimo-v2.5-tts 预置音色语音合成</small>
</p>
