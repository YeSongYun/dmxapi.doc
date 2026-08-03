# music-3.0 文本生成音乐 API 使用文档

基于 MiniMax `music-3.0` 模型的文本生成音乐接口，通过 `/v1/responses` 端点接收音乐风格、情绪与场景描述以及分段歌词，生成完整歌曲。接口支持非流式一次性返回和流式接收，音频可输出为 URL 或十六进制数据，并支持 MP3、WAV、PCM 编码、16 kHz 至 44.1 kHz 的 4 档采样率、32 kbps 至 256 kbps 的 4 档比特率，以及歌词优化和纯音乐生成，适合歌曲创作、配乐制作与音乐内容批量生产等场景。

## 接口地址

| 接口 | 请求方式 | URL |
|------|---------|-----|
| 文本生成音乐 | POST | `https://www.dmxapi.cn/v1/responses` |



:::warning
请妥善保管您的 API Key！严禁将密钥泄露给他人、硬编码到代码中或提交到公开的代码仓库。如果怀疑密钥已泄露，请立即前往 DMXAPI 官网重新生成。
:::

## 模型名称

- `music-3.0`

## 文本生成音乐示例代码

::: code-group

```python [非流式输出]
import requests
import json

# ===============================================================
# 步骤1: 配置 API 连接信息
# ===============================================================

# DMXAPI 服务端点地址
url = "https://www.dmxapi.cn/v1/responses"

# DMXAPI 密钥 (请替换为您自己的密钥)
# 获取方式: 登录 DMXAPI 官网 -> 个人中心 -> API 密钥管理
api_key = "sk-******************************************"

# ===============================================================
# 步骤2: 配置请求头
# ===============================================================

headers = {
    "Content-Type": "application/json",      # 指定请求体为 JSON 格式
    "Authorization": f"{api_key}",           # token 认证方式
}

# ===============================================================
# 步骤3: 配置请求参数
# ===============================================================

payload = {
    # 【model】(string, 必填) 调用的模型名称
    # 当前文档固定使用 music-3.0
    "model": "music-3.0",

    # 【input】(string, 可选) 音乐描述，用于指定风格、情绪和场景
    # 当前非纯音乐场景的长度限制为 [0, 2000] 个字符
    "input": "独立民谣,忧郁,内省,渴望,独自漫步,咖啡馆",

    # 【lyrics】(string, 条件必填) 歌曲歌词，使用 \n 分隔每行
    # 当前 is_instrumental 为 false，因此必须传入，长度限制为 [1, 3500] 个字符
    # 支持的结构标签: [Intro]、[Verse]、[Pre Chorus]、[Chorus]、[Interlude]、
    # [Bridge]、[Outro]、[Post Chorus]、[Transition]、[Break]、[Hook]、
    # [Build Up]、[Inst]、[Solo]
    "lyrics": "[verse]\n街灯微亮晚风轻抚\n影子拉长独自漫步\n旧外套裹着深深忧郁\n不知去向渴望何处\n[chorus]\n推开木门香气弥漫\n熟悉的角落陌生人看",

    # 【stream】(boolean, 可选) 是否使用流式传输，默认值为 false
    "stream": False,

    # 【output_format】(string, 可选) 音频返回格式，默认值为 "hex"
    # 可选值: "url"(返回音频链接) / "hex"(返回十六进制音频数据)
    # 当值为 "url" 时，返回链接的有效期为 24 小时，请及时下载
    # 当 stream 为 true 时，仅支持 "hex"
    "output_format": "url",

    # 【audio_setting】(object, 可选) 音频输出配置
    "audio_setting": {
        # 【audio_setting.sample_rate】(integer, 可选) 采样率
        # 可选值: 16000 / 24000 / 32000 / 44100
        "sample_rate": 44100,

        # 【audio_setting.bitrate】(integer, 可选) 比特率
        # 可选值: 32000 / 64000 / 128000 / 256000
        "bitrate": 256000,

        # 【audio_setting.format】(string, 可选) 音频编码格式
        # 可选值: "mp3" / "wav" / "pcm"
        "format": "mp3",
    },

    # 【aigc_watermark】(boolean, 可选) 是否在音频末尾添加水印，默认值为 false
    # 仅在非流式请求中生效
    "aigc_watermark": False,

    # 【lyrics_optimizer】(boolean, 可选) 是否根据音乐描述自动生成歌词
    # 默认值为 false；设为 true 且 lyrics 为空时，系统将自动生成歌词
    "lyrics_optimizer": False,

    # 【is_instrumental】(boolean, 可选) 是否生成无人声的纯音乐，默认值为 false
    # 设为 true 时，lyrics 字段不再必填
    "is_instrumental": False,
}

# ===============================================================
# 步骤4: 发送请求并输出结果
# ===============================================================

# 发送非流式 POST 请求到 API 服务器
response = requests.post(url, headers=headers, json=payload, stream=False)

# 格式化输出 JSON 响应
# - indent=2: 缩进 2 空格，便于阅读
# - ensure_ascii=False: 正确显示中文字符
print(json.dumps(response.json(), indent=2, ensure_ascii=False))
```



:::

## 返回示例

::: code-group

```json [返回示例（非流式输出）]
{
  "data": {
    "audio": "https://minimax-algeng-chat-tts.oss-cn-wulanchabu.aliyuncs.com/audio%2Feffect%2F06bbcf3f101e6715fb64606e0ad3726d_1785502822667_7318.mp3?Expires=1785589222&OSSAccessKeyId=LTAI5tGLnRTkBjLuYPjNcKQ8&Signature=KDMY6EjGAG6A2vh%2BDKSiCfhEaDM%3D",
    "status": 2
  },
  "trace_id": "06bbcf3f101e6715fb64606e0ad3726d",
  "extra_info": {
    "music_duration": 63817,
    "music_sample_rate": 44100,
    "music_channel": 2,
    "bitrate": 256000,
    "music_size": 2044123
  },
  "analysis_info": null,
  "base_resp": {
    "status_code": 0,
    "status_msg": "success"
  },
  "usage": {
    "total_tokens": 10000,
    "input_tokens": 0,
    "input_tokens_details": {
      "cached_tokens": 0
    },
    "output_tokens": 10000,
    "output_tokens_details": {
      "reasoning_tokens": 0
    }
  }
}
```

:::

<p align="center">
  <small>© 2026 DMXAPI music-3.0 文本生成音乐</small>
</p>
