# mimo-v2-omni 音频理解 API 使用文档

基于 Xiaomi MiMo `mimo-v2-omni` 模型的音频理解接口，支持通过音频 URL 或 Base64 编码将音频内容输入到模型中进行分析与问答，适用于语音内容描述、音频语义理解等场景。可与文本输入组合使用，其中 URL 音频单文件最大 100 MB，Base64 音频字符串最大 10 MB。

## 🔗 请求地址

```text
https://www.dmxapi.cn/v1/chat/completions
```

## 🎯 模型名称

- `mimo-v2-omni`

## 🎵 音频理解 示例代码

```python
import requests

url = "https://www.dmxapi.cn/v1/chat/completions"

# API Key，建议从环境变量或安全配置中读取
API_KEY = "sk-******************************************"

headers = {
    "Authorization": API_KEY,
    "Content-Type": "application/json"
}

payload = {
    # 【model】(string, 必填) 要调用的模型名称
    "model": "mimo-v2-omni",
    # 【messages】(array, 必填) 对话消息列表，按顺序提供给模型
    # 官方示例中包含 system 和 user 两类消息；user 消息可混合音频与文本内容
    "messages": [
        {
            # 【role】(string, 必填) 当前消息的角色标识
            # 可选值: "system"(系统提示词) / "user"(用户输入)
            "role": "system",
            # 【content】(string, 必填) system 消息的文本内容
            # 用于设定助手身份、行为方式或补充上下文
            "content": "You are MiMo, an AI assistant developed by Xiaomi. Today is date: Tuesday, December 16, 2025. Your knowledge cutoff date is December 2024."
        },
        {
            # 【role】(string, 必填) 当前消息的角色标识
            # 可选值: "system"(系统提示词) / "user"(用户输入)
            "role": "user",
            # 【content】(array, 必填) user 消息内容数组
            "content": [
                {
                    # 【type】(string, 必填) 内容块类型
                    # 可选值: "input_audio"(音频输入块)
                    "type": "input_audio",
                    # 【input_audio】(object, 必填) 音频输入对象
                    # 当 type 为 "input_audio" 时，用于承载音频数据
                    "input_audio": {
                        # 【data】(string, 必填) 音频数据内容
                        # 支持两种形式：
                        # 1. 公网可访问的音频 URL，单个音频文件大小不能超过 100 MB
                        # 2. 带前缀的 Base64 字符串，格式为 data:{MIME_TYPE};base64,$BASE64_AUDIO，字符串大小不能超过 10 MB
                          # 请在 Base64 编码前携带前缀：data:{MIME_TYPE};base64,$BASE64_AUDIO
                            # {MIME_TYPE}：音频的 MIME 类型（媒体类型），用于标识音频格式，需替换为实际音频对应的 MIME 值。
                            # $BASE64_AUDIO：音频文件的纯 Base64 编码字符串（不含任何前缀）。
                        "data": "https://example-files.cnbj1.mi-fds.com/example-files/audio/audio_example.wav"
                    }
                },
                {
                    # 【type】(string, 必填) 内容块类型
                    # 可选值: "text"(文本输入块)
                    "type": "text",
                    # 【text】(string, 必填) 文本输入内容
                    # 用于告诉模型如何理解或处理已传入的音频
                    "text": "please describe the content of the audio"
                }
            ]
        }
    ],
    # 【max_completion_tokens】(number, 可选) 限制本次生成的最大输出 Token 数
    # 默认值为 32768
    "max_completion_tokens": 1024
}

resp = requests.post(url, json=payload, headers=headers, timeout=120)
resp.raise_for_status()
print(resp.json())
```

## 📦 返回示例

```json
{
  "id": "272d942b15534367abededc13e288f08",
  "choices": [
    {
      "finish_reason": "stop",
      "index": 0,
      "message": {
        "content": "The audio features a speaker asking a question. The speaker says, \"Good morning, could you tell me what the weather will be like today?\" This indicates a request for a weather forecast.",
        "role": "assistant",
        "tool_calls": null,
        "reasoning_content": "..."
      }
    }
  ],
  "created": 1773832402,
  "model": "mimo-v2-omni",
  "object": "chat.completion",
  "usage": {
    "completion_tokens": 1005,
    "prompt_tokens": 86,
    "total_tokens": 1091,
    "completion_tokens_details": {
      "reasoning_tokens": 970
    },
    "prompt_tokens_details": {
      "audio_tokens": 25,
      "cached_tokens": 84
    }
  }
}
```

<p align="center">
  <small>© 2026 DMXAPI Xiaomi MiMo mimo-v2-omni 音频理解</small>
</p>
