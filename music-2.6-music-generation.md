# music-2.6 音乐生成 API 使用文档

基于 MiniMax music-2.6 模型的音乐生成接口，通过 `/v1/responses` 端点同步调用，输入歌曲描述与歌词即可一键生成带人声的完整歌曲。支持 14 种歌词结构标签（[Intro]、[Verse]、[Chorus]、[Bridge]、[Outro] 等）精细编排曲式，提供 16000/24000/32000/44100 Hz 四档采样率、32/64/128/256 kbps 四档比特率以及 mp3/wav/pcm 三种音频编码格式，并支持纯音乐模式、歌词自动优化与 AIGC 水印，适合短视频配乐、广告 BGM、游戏音乐等需要快速生成原创歌曲的场景。

## 接口地址

| 接口 | 请求方式 | URL |
|------|---------|-----|
| 音乐生成 | POST | `https://www.dmxapi.cn/v1/responses` |



:::warning
请妥善保管您的 API Key！严禁将密钥泄露给他人、硬编码到代码中或提交到公开的代码仓库。如果怀疑密钥已泄露，请立即前往 DMXAPI 官网重新生成。
:::

## 模型名称

- `music-2.6`

## 音乐生成 示例代码

```python
import requests
import json
from datetime import datetime

# ===============================================================
# 步骤1: 配置 API 连接信息
# ===============================================================

# DMXAPI 服务端点地址
url = "https://www.dmxapi.cn/v1/responses"

# DMXAPI 密钥 (请替换为您自己的密钥)
# 获取方式: 登录 DMXAPI 官网 -> 个人中心 -> API 密钥管理
api_key = "sk-***********************************************"

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
    "model": "music-2.6",

    # 【input】(string, 可选) 音乐描述，用于指定风格、情绪和场景，例如"流行音乐, 难过, 适合在下雨的晚上"
    # 非纯音乐场景下为可选项，长度限制 [0, 2000] 个字符
    "input": "独立民谣,忧郁,内省,渴望,独自漫步,咖啡馆",

    # 【lyrics】(string, 必填) 歌曲歌词，使用 \n 分隔每行
    # 非纯音乐场景下必填，长度限制 [1, 3500] 个字符
    # 支持的结构标签: [Intro] / [Verse] / [Pre Chorus] / [Chorus] / [Interlude] / [Bridge] /
    #               [Outro] / [Post Chorus] / [Transition] / [Break] / [Hook] / [Build Up] / [Inst] / [Solo]
    "lyrics": "[verse]\n街灯微亮晚风轻抚\n影子拉长独自漫步\n旧外套裹着深深忧郁\n不知去向渴望何处\n[chorus]\n推开木门香气弥漫\n熟悉的角落陌生人看",

    # 【stream】(boolean, 可选) 是否使用流式传输，默认为 false
    "stream": False,

    # 【audio_setting】(object, 可选) 音频输出配置
    "audio_setting": {
        # 【audio_setting.sample_rate】(integer) 采样率
        # 可选值: 16000 / 24000 / 32000 / 44100
        "sample_rate": 44100,

        # 【audio_setting.bitrate】(integer) 比特率
        # 可选值: 32000 / 64000 / 128000 / 256000
        "bitrate": 256000,

        # 【audio_setting.format】(string) 音频编码格式
        # 可选值: "mp3" / "wav" / "pcm"
        "format": "mp3"
    },

    # 【aigc_watermark】(boolean, 可选) 是否在音频末尾添加水印，默认为 false
    # 仅在非流式 (stream: false) 请求时生效
    "aigc_watermark": False,

    # 【lyrics_optimizer】(boolean, 可选) 是否根据 input 描述自动生成歌词，默认为 false
    # 设为 true 且 lyrics 为空时，系统会根据描述自动生成歌词
    "lyrics_optimizer": False,

    # 【is_instrumental】(boolean, 可选) 是否生成纯音乐（无人声），默认为 false
    # 设为 true 时，lyrics 字段非必填
    "is_instrumental": False
}

# ===============================================================
# 步骤4: 发送请求并输出结果
# ===============================================================

# 发送 POST 请求到 API 服务器
response = requests.post(url, headers=headers, json=payload)
result = response.json()

# 提取 hex 编码的音频数据，转换为字节流后保存为本地音频文件
audio_hex = result.get("data", {}).get("audio", "")
if audio_hex:
    audio_bytes = bytes.fromhex(audio_hex)
    fmt = payload.get("audio_setting", {}).get("format", "mp3")
    output_file = datetime.now().strftime("%Y%m%d_%H%M%S") + f".{fmt}"
    with open(output_file, "wb") as f:
        f.write(audio_bytes)
    print(f"音频已保存：{output_file}")
    # 从 extra_info 中读取音频元信息并打印
    extra = result.get("extra_info", {})
    print(f"时长：{extra.get('music_duration', 0) / 1000:.1f} 秒")
    print(f"采样率：{extra.get('music_sample_rate')} Hz，声道数：{extra.get('music_channel')}，码率：{extra.get('bitrate', 0) // 1000} kbps")
else:
    print("未获取到音频数据")
    print(json.dumps(result, indent=2, ensure_ascii=False))
```

## 返回示例

```text
音频已保存：20260615_152009.mp3
时长：45.7 秒
采样率：44100 Hz，声道数：2，码率：256 kbps
```

<p align="center">
  <small>© 2026 DMXAPI music-2.6 音乐生成</small>
</p>
