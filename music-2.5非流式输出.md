# MiniMax-Music-2.5 AI音乐大模型API使用文档（非流式输出）
MiniMax Music 2.5 聚焦解决 AI 音乐创作的两大核心难题：可控性与真实度。模型支持段落级强控制，可在生成前通过标签精确规划整首歌的结构与情绪走向，覆盖 Intro、Bridge、Interlude、Build-up、Hook 等在内的 14 种段落变体；同时在“物理级高保真”上全面提升人声、风格与混音质量，带来更自然的咬字与中英文衔接、更细腻的转音与颤音、更贴合风格的自动混音，并提供 100+ 乐器音色与更清晰的人声/伴奏分离，适配流行成品、影视配乐、游戏声场与品牌音效等专业工作流。

## 请求地址

```
https://www.dmxapi.cn/v1/responses
```

## 模型名称

- `music-2.5`

## 示例代码

```python
import requests
import json

url = "https://www.dmxapi.cn/v1/responses"
api_key = "sk-***********************************" # 请替换为你的 DMXAPI 密钥

headers = {
    "Content-Type": "application/json",
    "Authorization": f"{api_key}",
}

payload = {
    "model": "music-2.5",

    # 【input】: 音乐的描述，用于指定风格、情绪和场景。例如"流行音乐, 难过, 适合在下雨的晚上"。
    # 注意：对于 music-2.5：可选，长度限制为 [0, 2000] 个字符。对于非 music-2.5 模型：必填，长度限制为 [10, 2000] 个字符
    "input": "独立民谣,忧郁,内省,渴望,独自漫步,咖啡馆",

    # 【lyrics】:歌曲的歌词。使用 \n 分隔每行。你可以在歌词中加入 [Intro], [Verse], [Pre Chorus], [Chorus], [Interlude],
    # [Bridge], [Outro], [Post Chorus], [Transition], [Break], [Hook], [Build Up], [Inst], [Solo] 等结构标签来优化生成的音乐结
    # 构。长度限制：对于 music-2.5：[1, 3500] 个字符。对于非 music-2.5 模型：[10, 3500] 个字符
    "lyrics": "[verse]\n街灯微亮晚风轻抚\n影子拉长独自漫步\n旧外套裹着深深忧郁\n不知去向渴望何处\n[chorus]\n推开木门香气弥漫\n熟悉的角落陌生人看",

    # 【audio_setting】: 音频输出配置
    # 子属性为：
    # sample_rate: 采样率。可选值：16000, 24000, 32000, 44100
    # bitrate: 比特率。可选值：32000, 64000, 128000, 256000
    # format: 音频编码格式。可选值：mp3 , wav , pcm
    "audio_setting": {"sample_rate": 44100, "bitrate": 256000, "format": "mp3"},

    # 【output_format】: 音频的返回格式，可选值为 url 或 hex，默认为 hex。当 stream 为 true 时，仅支持 hex 格式。注意：url 的有效期为 24 小时，请
    # 尽快下载。可用选项: url, hex
    "output_format": "url",
    "stream": False,   # 是否使用流式传输，默认为 False
    "aigc_watermark": True,# 是否在音频末尾添加水印，默认为 false。仅在非流式 (stream: False) 请求时生效
}

resp = requests.post(url, headers=headers, json=payload, timeout=(10, 600))
print("status:", resp.status_code)
print("content-type:", resp.headers.get("Content-Type"))
resp.raise_for_status()

data = resp.json()
print(json.dumps(data, indent=2, ensure_ascii=False))

audio_url = None
try:
    audio_url = data["output"][0]["content"][0].get("audio")
except Exception:
    pass

print("audio_url:", audio_url)
```

---

## 返回示例

```json
status: 200
content-type: application/json; charset=utf-8
{
  "task_id": "05d90bb300da5ff052a85144ea28ff57",
  "type": "music_generation",
  "state": "completed",
  "model": "music-2.5",
  "prompt": "音乐剧，欢快，合唱",
  "lyrics": "[verse]\n街灯微亮晚风轻抚\n影子拉长独自漫步\n旧外套裹着深深忧郁\n不知去向渴望何处\n[chorus]\n推开木门香气弥漫\n熟悉的角落陌生人看",
  "created_at": 1770641690,
  "usage": {
    "total_tokens": 646,
    "input_tokens": 199,
    "input_tokens_details": {
      "cached_tokens": 0
    },
    "output_tokens": 447,
    "output_tokens_details": {
      "reasoning_tokens": 0
    }
  },

  "output": [
    {
      "type": "message",
      "content": [
        {
          "type": "output_audio",
          "audio": "https://minimax-algeng-chat-tts.oss-cn-wulanchabu.aliyuncs.com/audio%2Feffect%2F05d90bb300da5ff052a85144ea28ff57_1770641689990_3218.mp3?Expires=1770728090&OSSAccessKeyId=LTAI5tGLnRTkBjLuYPjNcKQ8&Signature=KHItUHccC4BhkBCLBHOTSasSsi8%3D"
        }
      ]
    }
  ],
  "extra_info": {
    "music_duration": 44773,
    "music_sample_rate": 44100,
    "music_channel": 2,
    "bitrate": 256000,
    "music_size": 727552
  }
}
audio_url: https://minimax-algeng-chat-tts.oss-cn-wulanchabu.aliyuncs.com/audio%2Feffect%2F05d90bb300da5ff052a85144ea28ff57_1770641689990_3218.mp3?Expires=1770728090&OSSAccessKeyId=LTAI5tGLnRTkBjLuYPjNcKQ8&Signature=KHItUHccC4BhkBCLBHOTSasSsi8%3D
```

<p align="center">
  <small>© 2026 DMXAPI music-2.5 音乐模型</small>
</p>
