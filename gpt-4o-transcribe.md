# gpt-4o-transcribe 语音转文本STT模型 API文档

## 概念介绍
STT(Speech-to-Text)是将语音转换为文本的技术，基于OpenAI Whisper模型实现。适用于：
- 语音笔记转文字
- 会议录音转文字稿
- 语音助手开发
- 音频内容分析

gpt-4o-transcribe 是 Openai 2025上半年最新的语音识别转录 STT模型。

## API接口

### 语音转文本
**请求方式**：POST  
**Base URL**：`https://www.dmxapi.cn/v1/audio/transcriptions`

#### 请求参数
| 参数名 | 类型 | 必填 | 说明 |
|-------|------|------|------|
| model | string | 是 | "gpt-4o-transcribe" |
| file | binary | 是 | 音频文件(支持mp3,wav等格式) |

#### 请求头
```
Authorization: sk-******  # 替换为你的DMXAPI令牌
Content-Type: multipart/form-data
```

## Python调用示例

```python
import json  # 添加 json 库的导入

import requests


def q_voice_to_text(file_path_wav):
    url = "https://www.dmxapi.cn/v1/audio/transcriptions"

    payload = {"model": "gpt-4o-transcribe"}
    files = {"file": ("audio.mp3", open(file_path_wav, "rb"))}

    # 直接使用 API 密钥
    gpt_key = (
        "sk-**********************************************"  # 更换为你的 DMXAPI 令牌
    )

    headers = {"Authorization": f"{gpt_key}"}

    # 发送请求
    response = requests.request("POST", url, headers=headers, data=payload, files=files)

    # 处理响应
    data = json.loads(response.text)

    # 获取返回的文本内容
    voice_text = data["text"] if data["text"] is not None else ""

    return voice_text


print(q_voice_to_text("C:\\kywpy\\jay.mp3"))  # 替换为实际的音频文件路径


```

## 注意事项
1. 音频文件大小建议不超过25MB
2. 支持多种音频格式：mp3, mp4, mpeg, mpga, m4a, wav, webm
3. 请妥善保管API密钥，不要泄露
4. 调用频率限制请参考DMXAPI官方文档

<p align="center">
  <small>© 2025 DMXAPI GPT语音</small>
</p>