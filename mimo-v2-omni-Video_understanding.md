# mimo-v2-omni 视频理解 API 使用文档

基于 Xiaomi MiMo `mimo-v2-omni` 模型的视频理解能力，您可以通过 `/v1/chat/completions` 接口传入视频 URL 进行视频内容分析、描述与理解。该能力支持公网视频 URL 与 Base64 两种视频输入方式，其中 URL 方式单文件最大 300 MB，并可通过 `fps` 与 `media_resolution` 两个字段控制时间维度与视觉细节的理解精细度，适用于视频分析、多模态问答等场景。

## 🌐 请求地址

```bash
https://www.dmxapi.cn/v1/chat/completions
```

## 🤖 模型名称

- `mimo-v2-omni`

## 🎬 视频理解 示例代码

```python
import requests
url = "https://www.dmxapi.cn/v1/chat/completions"
api_key = "sk-******************************************"
headers = {
    "Authorization": api_key,
    "Content-Type": "application/json"
}

payload = {
    # 【model】(string, 必填) 要调用的模型名称
    "model": "mimo-v2-omni",
    # 【messages】(array, 必填) 对话消息列表，按顺序提供给模型
    # 视频理解请求中需在消息中同时传入指令文本与视频内容
    "messages": [
        {
            # 【role】(string, 必填) 消息角色
            # 可选值: "system"(系统提示) / "user"(用户输入) / "assistant"(助手回复)
            "role": "system",
            # 【content】(string, 必填) 消息内容
            # system 角色内容用于设定助手身份、行为方式和回答风格
            "content": "You are MiMo, an AI assistant developed by Xiaomi. Today is date: Tuesday, December 16, 2025. Your knowledge cutoff date is December 2024."
        },
        {
            "role": "user",
            # 【content】(array, 必填) 用户输入内容列表
            # 视频理解场景下可混合传入多模态内容，例如视频与文本问题
            "content": [
                {
                    # 【type】(string, 必填) 当前内容块类型
                    # 可选值: "video_url"(视频输入)
                    "type": "video_url",
                    # 【video_url】(object, 必填) 视频输入对象
                    # 用于提供待分析视频的访问地址；官方文档说明支持公网 URL 或 data:{MIME_TYPE};base64,$BASE64_VIDEO 格式
                    "video_url": {
                        # 【url】(string, 必填) 视频地址
                        # URL 方式时需为公网可访问的视频地址；Base64 方式时需携带 data:{MIME_TYPE};base64, 前缀
                        # URL 方式单个视频文件大小不能超过 300 MB
                        "url": "https://example-files.cnbj1.mi-fds.com/example-files/video/video_example.mp4"
                    },
                    # 【fps】(number, 可选) 每秒抽取的视频帧数，用于控制时间维度的理解精细度
                    # 取值范围: [0.1, 10]，默认值为 2
                    # 数值越高，抽帧越密集，时序理解越精细，但 Token 消耗也更高
                    "fps": 2,
                    # 【media_resolution】(string, 可选) 视频帧解析分辨率档次，用于控制单帧视觉理解精细度
                    # 默认值: "default"
                    # 可选值: "default"(平衡识别效果与处理效率) / "max"(最高分辨率档次，提升对小物体和细节纹理的识别能力)
                    "media_resolution": "default"
                },
                {
                    # 【type】(string, 必填) 当前内容块类型
                    # 可选值: "text"(文本提问)
                    "type": "text",
                    # 【text】(string, 必填) 用户希望模型执行的文本指令
                    # 例如要求模型描述、总结或分析视频内容
                    "text": "详细的分析下这个视频"
                }
            ]
        }
    ],
    # 【max_completion_tokens】(integer, 可选) 本次生成允许的最大输出 Token 数
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
  "id": "2cb45ce8504441c29f0601de5e5b61ff",
  "choices": [
    {
      "finish_reason": "stop",
      "index": 0,
      "message": {
        "content": "The video features a small, fluffy white kitten sitting on a polished wooden floor. The kitten is positioned near a window draped with light-colored, textured curtains. Bright sunlight streams through the window, casting distinct shadows and illuminating the kitten's fur. The kitten looks towards the left side of the frame and occasionally licks its nose or lips. In the background, to the right, a potted green plant with large leaves, resembling a Monstera, is visible against a plain wall. The overall scene is bright and peaceful.",
        "role": "assistant",
        "tool_calls": null,
        "reasoning_content": "The user wants a description of the video provided.\n1. **Analyze the video:**\n* **Subject:** A white kitten.\n* **Action:** The kitten is sitting on a wooden floor, looking towards the left side of the frame. It occasionally licks its lips or nose.\n* **Setting:** Indoors, near a window with light-colored curtains. Sunlight is streaming in, creating shadows on the floor. There is a plant in the background (Monstera)."
      }
    }
  ],
  "created": 1773831625,
  "model": "mimo-v2-omni",
  "object": "chat.completion",
  "usage": {
    "completion_tokens": 210,
    "prompt_tokens": 1278,
    "total_tokens": 1488,
    "completion_tokens_details": {
      "reasoning_tokens": 101
    },
    "prompt_tokens_details": {
      "audio_tokens": 20,
      "cached_tokens": 47,
      "video_tokens": 1170
    }
  }
}
```

<p align="center">
  <small>© 2026 DMXAPI Xiaomi MiMo mimo-v2-omni 视频理解</small>
</p>
