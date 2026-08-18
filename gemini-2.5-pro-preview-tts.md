# Gemini系列 语音生成模型（TTS） API 文档 
Gemini API 可以使用原生文字转语音 (TTS) 生成功能将文本输入转换为单人或多人音频。文字转语音 (TTS) 生成是可控的，这意味着您可以使用自然语言来构建互动，并指导音频的风格、口音、节奏和语气。

TTS 功能不同于通过 Live API 提供的语音生成功能，后者专为交互式非结构化音频以及多模态输入和输出而设计。虽然 Live API 在动态对话上下文中表现出色，但通过 Gemini API 实现的 TTS 专门针对需要精确朗读文本并对风格和声音进行精细控制的场景，例如播客或有声读物生成。

## 请求地址
想要更换模型在url中替换名称就可以。
```
https://www.dmxapi.cn/v1beta/models/gemini-2.5-pro-preview-tts:generateContent"
```


## 🌻模型名称


`gemini-2.5-pro-preview-tts` 
`gemini-2.5-flash-preview-tts` 

## 🚀文字转单人语音 示例代码

```python
"""
================================================================================
Gemini 2.5 Pro Preview TTS - 单人语音合成
================================================================================

【功能说明】
    调用 Google Gemini TTS API 将文本转换为自然语音

【使用模型】
    gemini-2.5-pro-preview-tts（预览版专业模型）

【输出格式】
    WAV 音频文件（16位 PCM，24kHz 采样率，单声道）
    文件名格式：out_YYYYMMDD_HHMMSS.wav

【依赖库】
    - requests：发送 HTTP 请求
    - base64：解码音频数据
    - wave：生成 WAV 文件
    - datetime：生成时间戳

【可用声音】
    Aoede, Charon, Fenrir, Kore, Puck, Orbit, Orus, Trochilidae, Zephyr

【使用方法】
    1. 修改 text 字段为你想要转换的文本
    2. 修改 voiceName 选择喜欢的声音
    3. 运行脚本，音频将保存到当前目录

================================================================================
"""

import requests
import base64
import wave
from datetime import datetime

# ================================================================================
# API 配置
# ================================================================================
# 接口地址（使用代理服务）
url = "https://www.dmxapi.cn/v1beta/models/gemini-2.5-pro-preview-tts:generateContent"

# API 密钥（请妥善保管，不要泄露）
api_key = "sk-**************************************"

# 请求头
headers = {
    "x-goog-api-key": api_key,      # API 认证密钥
    "Content-Type": "application/json"  # 请求体格式
}

# ================================================================================
# 请求数据
# ================================================================================
data = {
    # 输入内容
    "contents": [{
        "parts": [{
            # 要转换为语音的文本
            # 支持多种语言，可以添加情感指令如 "Say cheerfully:"
            "text": "Say cheerfully: Have a wonderful day!"
        }]
    }],

    # 生成配置
    "generationConfig": {
        # 响应类型：AUDIO 表示返回音频
        "responseModalities": ["AUDIO"],

        # 语音配置
        "speechConfig": {
            "voiceConfig": {
                "prebuiltVoiceConfig": {
                    # 预置声音名称
                    # 可选：Aoede, Charon, Fenrir, Kore, Puck, Orbit, Orus, Trochilidae, Zephyr
                    "voiceName": "Kore"
                }
            }
        }
    }
}

# ================================================================================
# 发送请求
# ================================================================================
print("正在请求 API...")
response = requests.post(url, headers=headers, json=data)
result = response.json()

# ================================================================================
# 错误处理
# ================================================================================
# 检查 API 是否返回错误
if "error" in result:
    print("=" * 50)
    print("API 错误:")
    print(f"  错误码: {result['error'].get('code', '未知')}")
    print(f"  错误信息: {result['error'].get('message', '未知')}")
    print("=" * 50)
    exit(1)

# 检查响应格式是否正确
if "candidates" not in result:
    print("=" * 50)
    print("响应格式异常，完整响应内容:")
    print(result)
    print("=" * 50)
    exit(1)

# ================================================================================
# 解析并保存音频
# ================================================================================
print("正在解析音频数据...")

# 从响应中提取 Base64 编码的音频数据
audio_data = result["candidates"][0]["content"]["parts"][0]["inlineData"]["data"]

# 将 Base64 解码为原始字节
audio_bytes = base64.b64decode(audio_data)

# 生成带时间戳的文件名，避免覆盖
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
filename = f"out_{timestamp}.wav"

# 保存为 WAV 格式音频文件
print("正在保存音频文件...")
with wave.open(filename, "wb") as wav_file:
    wav_file.setnchannels(1)        # 声道数：1（单声道）
    wav_file.setsampwidth(2)        # 采样宽度：2 字节（16 位）
    wav_file.setframerate(24000)    # 采样率：24000 Hz
    wav_file.writeframes(audio_bytes)

# ================================================================================
# 完成提示
# ================================================================================
print("=" * 50)
print(f"音频已成功保存为: {filename}")
print(f"音频时长约: {len(audio_bytes) / (24000 * 2):.2f} 秒")
print("=" * 50)

```

## 🐯返回示例

```json
正在请求 API...
正在解析音频数据...
正在保存音频文件...
==================================================
音频已成功保存为: out_20260115_221023.wav
音频时长约: 2.41 秒
==================================================
```

## 🚗文字转双人语音 示例代码

```python
"""
================================================================================
Gemini 2.5 Pro Preview TTS - 双人对话语音合成
================================================================================

【功能说明】
    调用 Google Gemini TTS API 将多人对话文本转换为自然语音
    支持为不同说话人配置不同的声音，实现逼真的对话效果

【使用模型】
    gemini-2.5-pro-preview-tts（预览版专业模型）

【输出格式】
    WAV 音频文件（16位 PCM，24kHz 采样率，单声道）
    文件名格式：out_YYYYMMDD_HHMMSS.wav

【依赖库】
    - requests：发送 HTTP 请求
    - base64：解码音频数据
    - wave：生成 WAV 文件
    - datetime：生成时间戳

【可用声音】
    Aoede, Charon, Fenrir, Kore, Puck, Orbit, Orus, Trochilidae, Zephyr

【使用方法】
    1. 修改 text 字段，按格式编写对话内容：
       "TTS the following conversation between 角色A and 角色B:
        角色A: 对话内容
        角色B: 对话内容"
    2. 在 speakerVoiceConfigs 中为每个角色配置声音
    3. 运行脚本，音频将保存到当前目录

【与单人版的区别】
    - 使用 multiSpeakerVoiceConfig 替代 voiceConfig
    - 可以为每个说话人单独指定声音
    - 文本需要标注说话人名称

================================================================================
"""

import requests
import base64
import wave
from datetime import datetime

# ================================================================================
# API 配置
# ================================================================================
# 接口地址（使用代理服务）
url = "https://www.dmxapi.cn/v1beta/models/gemini-2.5-pro-preview-tts:generateContent"

# API 密钥（请妥善保管，不要泄露）
api_key = "sk-***********************************************"

# 请求头
headers = {
    "x-goog-api-key": api_key,          # API 认证密钥
    "Content-Type": "application/json"  # 请求体格式
}

# ================================================================================
# 请求数据（双人对话）
# ================================================================================
data = {
    # 输入内容
    "contents": [{
        "parts": [{
            # 对话文本格式：
            # 1. 首先声明对话参与者："TTS the following conversation between A and B:"
            # 2. 然后按 "角色名: 对话内容" 的格式编写对话
            "text": """TTS the following conversation between Joe and Jane:
                Joe: Hows it going today Jane?
                Jane: Not too bad, how about you?"""
        }]
    }],

    # 生成配置
    "generationConfig": {
        # 响应类型：AUDIO 表示返回音频
        "responseModalities": ["AUDIO"],

        # 语音配置（多人模式）
        "speechConfig": {
            # 多说话人配置
            "multiSpeakerVoiceConfig": {
                # 每个说话人的声音配置列表
                "speakerVoiceConfigs": [
                    {
                        # 第一个说话人
                        "speaker": "Joe",           # 说话人名称（需与文本中的名称一致）
                        "voiceConfig": {
                            "prebuiltVoiceConfig": {
                                "voiceName": "Kore"  # Joe 使用 Kore 声音
                            }
                        }
                    },
                    {
                        # 第二个说话人
                        "speaker": "Jane",          # 说话人名称（需与文本中的名称一致）
                        "voiceConfig": {
                            "prebuiltVoiceConfig": {
                                "voiceName": "Puck"  # Jane 使用 Puck 声音
                            }
                        }
                    }
                ]
            }
        }
    }
}

# ================================================================================
# 发送请求
# ================================================================================
print("正在请求 API...")
response = requests.post(url, headers=headers, json=data)
result = response.json()

# ================================================================================
# 错误处理
# ================================================================================
# 检查 API 是否返回错误
if "error" in result:
    print("=" * 50)
    print("API 错误:")
    print(f"  错误码: {result['error'].get('code', '未知')}")
    print(f"  错误信息: {result['error'].get('message', '未知')}")
    print("=" * 50)
    exit(1)

# 检查响应格式是否正确
if "candidates" not in result:
    print("=" * 50)
    print("响应格式异常，完整响应内容:")
    print(result)
    print("=" * 50)
    exit(1)

# ================================================================================
# 解析并保存音频
# ================================================================================
print("正在解析音频数据...")

# 从响应中提取 Base64 编码的音频数据
audio_data = result["candidates"][0]["content"]["parts"][0]["inlineData"]["data"]

# 将 Base64 解码为原始字节
audio_bytes = base64.b64decode(audio_data)

# 生成带时间戳的文件名，避免覆盖
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
filename = f"out_{timestamp}.wav"

# 保存为 WAV 格式音频文件
print("正在保存音频文件...")
with wave.open(filename, "wb") as wav_file:
    wav_file.setnchannels(1)        # 声道数：1（单声道）
    wav_file.setsampwidth(2)        # 采样宽度：2 字节（16 位）
    wav_file.setframerate(24000)    # 采样率：24000 Hz
    wav_file.writeframes(audio_bytes)

# ================================================================================
# 完成提示
# ================================================================================
print("=" * 50)
print(f"音频已成功保存为: {filename}")
print(f"音频时长约: {len(audio_bytes) / (24000 * 2):.2f} 秒")
print("=" * 50)
```


## 🐶返回示例

```json
正在请求 API...
正在解析音频数据...
正在保存音频文件...
==================================================
音频已成功保存为: out_20260115_221307.wav
音频时长约: 3.53 秒
==================================================
```

## 🚢通过提示控制说话风格
您可以使用自然语言提示来控制单人或多人 TTS 的风格、语气、口音和节奏。 例如，在单音箱提示中，您可以说：
```python
Say in an spooky whisper:
"By the pricking of my thumbs...
Something wicked this way comes"

```
在多位发言者的提示中，为模型提供每位发言者的姓名和相应的转写内容。您还可以单独为每个音箱提供指导：
```python
Make Speaker1 sound tired and bored, and Speaker2 sound excited and happy:

Speaker1: So... what's on the agenda today?
Speaker2: You're never going to guess!

```
## 🥊语音选项
TTS 模型在 voice_name 字段中支持以下 30 种语音选项：

| 语音名称 | 风格特点 | 语音名称 | 风格特点 |
|----------|----------|----------|----------|
| Zephyr | 明亮 | Puck | 欢快 |
| Charon | 信息丰富 | Kore | Firm (坚定) |
| Fenrir | Excitable (兴奋) | Leda | 青春 |
| Orus | 公司 | Aoede | Breezy (轻快) |
| Callirrhoe | 轻松 | Autonoe | 明亮 |
| Enceladus | 气声 | Iapetus | 清晰 |
| Umbriel | 轻松自在 | Algieba | 平滑 |
| Despina | 平滑 | Erinome | 清除 |
| Algenib | Gravelly (沙哑) | Rasalgethi | 信息丰富 |
| Laomedeia | 欢快 | Achernar | 软 |
| Alnilam | Firm (坚定) | Schedar | Even (平稳) |
| Gacrux | 成熟 | Pulcherrima | 直率 |
| Achird | 友好 | Zubenelgenubi | 随意 |
| Vindemiatrix | 温柔 | Sadachbia | 活泼 |
| Sadaltager | 知识渊博 | Sulafat | 偏高 |


## 🎉 支持的语言
TTS 模型会自动检测输入语言。它们支持以下 24 种语言：

| 语言 | BCP-47 代码 | 语言 | BCP-47 代码 |
|------|-------------|------|-------------|
| 阿拉伯语（埃及语） | ar-EG | 德语（德国） | de-DE |
| 英语（美国） | en-US | 西班牙语（美国） | es-US |
| 法语（法国） | fr-FR | 印地语（印度） | hi-IN |
| 印度尼西亚语（印度尼西亚） | id-ID | 意大利语（意大利） | it-IT |
| 日语（日本） | ja-JP | 韩语（韩国） | ko-KR |
| 葡萄牙语（巴西） | pt-BR | 俄语（俄罗斯） | ru-RU |
| 荷兰语（荷兰） | nl-NL | 波兰语（波兰） | pl-PL |
| 泰语（泰国） | th-TH | 土耳其语（土耳其） | tr-TR |
| 越南语（越南） | vi-VN | 罗马尼亚语（罗马尼亚） | ro-RO |
| 乌克兰语（乌克兰） | uk-UA | 孟加拉语（孟加拉） | bn-BD |
| 英语（印度） | en-IN 和 hi-IN 套装 | 马拉地语（印度） | mr-IN |
| 泰米尔语（印度） | ta-IN | 泰卢固语（印度） | te-IN |



---

<p align="center">
  <small>© 2026 DMXAPI gemini-2.5-pro-preview-tts 语音生成</small>
</p>