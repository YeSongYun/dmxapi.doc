# paiwo-itv-hd 数字人对口型视频 API 使用文档

paiwo-itv-hd 是拍我 AI 开放平台提供的数字人对口型（Lipsync）视频生成接口，通过 DMXAPI 统一接入。支持通过 PixVerse 平台生成的视频或用户自行上传的视频作为底板，结合用户上传的音频或平台内置 TTS 服务驱动口型，自动合成与语音内容精准匹配的数字人视频。

## 模型名称

- `paiwo-itv-hd`

## 接口地址

| 接口 | 请求方式 | URL |
|------|---------|-----|
| 提交任务 | POST | `https://www.dmxapi.cn/v1/responses` |
| 获取结果 | POST | `https://www.dmxapi.cn/v1/responses` |
   



### TTS 可用音色列表

使用 `lip_sync_tts_speaker_id` 参数时，可从以下音色中选择：

| 音色 ID (speaker_id) | 音色名称 |
|----------------------|---------|
| `Auto` | 随机 |
| `2` | 詹有鱼 |
| `4` | 外国阿利 |
| `6` | 李解 |
| `10` | 姜姜好 |
| `11` | 老森 |
| `12` | 李杰克 |
| `13` | 钱多多 |
| `14` | 呆萌王小拍 |
| `16` | 屯里大嗓 |
| `18` | 豫语汉子 |
| `19` | 宝岛囡囡 |
| `20` | 陕西掌柜 |
| `21` | 港风阿sir |
| `22` | ads_promale |
| `23` | ads_youngmale |
| `24` | ads_gracefemale |
| `25` | ads_jiangchuan_male |
| `26` | ads_panpan_female |
| `28` | ads_zhouyun_female |

## 提交任务 示例代码

> **参数组合说明**
>
> 视频来源（二选一）：
> - `source_video_id` — 使用 PixVerse 平台已生成的视频 ID（需先通过 [图生视频](/paiwo-v5.6-itv) 接口获取）
> - `video_media_id` — 使用用户自行上传的视频 ID（需先通过 [视频上传](/paiwo-video-upload) 接口获取）
>
> 音频来源（二选一）：
> - `audio_media_id` — 使用用户自行上传的音频 ID（需先通过 [音频上传](/paiwo-audio-upload) 接口获取）
> - `lip_sync_tts_speaker_id` + `lip_sync_tts_content` — 使用平台内置 TTS 服务合成音频
::: code-group

```python [PixVerse视频 + 上传音频]
import requests
import json

# 步骤1: 配置 API 连接信息

url = "https://www.dmxapi.cn/v1/responses"
api_key = "sk-******************************************"

# 步骤2: 配置请求头

headers = {
    "Content-Type": "application/json",
    "Authorization": f"{api_key}",
}

# 步骤3: 配置请求参数

payload = {
    # 【model】(string, 必填) 固定值: "paiwo-itv-hd"
    "model": "paiwo-itv-hd",

    # 【input】(string, 必填) 任务描述文本
    "input": "通过 PixVerse 生成的视频 + 用户上传音频 生成数字人",

    # 【source_video_id】(integer, 必填) PixVerse 平台生成的视频 ID
    # 通过文生视频/图生视频等接口生成视频后获取此 ID
    "source_video_id": 397190920840764,

    # 【audio_media_id】(integer, 必填) 用户上传音频的媒体 ID
    # 通过「音频上传」接口上传音频后获取此 ID
    "audio_media_id": 397190962941629,
}

# 步骤4: 发送请求并输出结果

response = requests.post(url, headers=headers, json=payload)
print(json.dumps(response.json(), indent=2, ensure_ascii=False))
```

```python [PixVerse视频 + TTS]
import requests
import json

# 步骤1: 配置 API 连接信息

url = "https://www.dmxapi.cn/v1/responses"
api_key = "sk-******************************************"

# 步骤2: 配置请求头

headers = {
    "Content-Type": "application/json",
    "Authorization": f"{api_key}",
}

# 步骤3: 配置请求参数

payload = {
    # 【model】(string, 必填) 固定值: "paiwo-itv-hd"
    "model": "paiwo-itv-hd",

    # 【input】(string, 必填) 任务描述文本
    "input": "通过 PixVerse 生成的视频 + TTS 生成数字人",

    # 【source_video_id】(integer, 必填) PixVerse 平台生成的视频 ID
    "source_video_id": 397190920840764,

    # 【lip_sync_tts_speaker_id】(string, 必填) TTS 音色 ID
    # 填写 "auto" 自动选择，或通过「获取TTS音色」接口查询具体音色 ID
    "lip_sync_tts_speaker_id": "auto",

    # 【lip_sync_tts_content】(string, 必填) TTS 合成文本内容
    # 系统将该文本转为语音，并生成对应口型的数字人视频
    "lip_sync_tts_content": "hello this is harry, where are you from?",
}

# 步骤4: 发送请求并输出结果

response = requests.post(url, headers=headers, json=payload)
print(json.dumps(response.json(), indent=2, ensure_ascii=False))
```

```python [上传视频 + 上传音频]
import requests
import json

# 步骤1: 配置 API 连接信息

url = "https://www.dmxapi.cn/v1/responses"
api_key = "sk-******************************************"

# 步骤2: 配置请求头

headers = {
    "Content-Type": "application/json",
    "Authorization": f"{api_key}",
}

# 步骤3: 配置请求参数

payload = {
    # 【model】(string, 必填) 固定值: "paiwo-itv-hd"
    "model": "paiwo-itv-hd",

    # 【input】(string, 必填) 任务描述文本
    "input": "用户上传视频 + 用户上传音频 生成数字人",

    # 【video_media_id】(integer, 必填) 用户上传视频的媒体 ID
    # 通过「视频上传」接口上传视频后获取此 ID
    "video_media_id": 397190920840764,

    # 【audio_media_id】(integer, 必填) 用户上传音频的媒体 ID
    # 通过「音频上传」接口上传音频后获取此 ID
    "audio_media_id": 397190962941629,
}

# 步骤4: 发送请求并输出结果

response = requests.post(url, headers=headers, json=payload)
print(json.dumps(response.json(), indent=2, ensure_ascii=False))
```

```python [上传视频 + TTS]
import requests
import json

# 步骤1: 配置 API 连接信息

url = "https://www.dmxapi.cn/v1/responses"
api_key = "sk-******************************************"

# 步骤2: 配置请求头

headers = {
    "Content-Type": "application/json",
    "Authorization": f"{api_key}",
}

# 步骤3: 配置请求参数

payload = {
    # 【model】(string, 必填) 固定值: "paiwo-itv-hd"
    "model": "paiwo-itv-hd",

    # 【input】(string, 必填) 任务描述文本
    "input": "用户上传视频 + TTS 生成数字人",

    # 【video_media_id】(integer, 必填) 用户上传视频的媒体 ID
    # 通过「视频上传」接口上传视频后获取此 ID
    "video_media_id": 397190920840764,

    # 【lip_sync_tts_speaker_id】(string, 必填) TTS 音色 ID
    # 填写 "auto" 自动选择，或通过「获取TTS音色」接口查询具体音色 ID
    "lip_sync_tts_speaker_id": "auto",

    # 【lip_sync_tts_content】(string, 必填) TTS 合成文本内容
    # 系统将该文本转为语音，并生成对应口型的数字人视频
    "lip_sync_tts_content": "hello this is harry, where are you from?",
}

# 步骤4: 发送请求并输出结果

response = requests.post(url, headers=headers, json=payload)
print(json.dumps(response.json(), indent=2, ensure_ascii=False))
```

:::

### 返回示例

```json
{
  "ErrCode": 0,
  "ErrMsg": "Success",
  "Resp": {
    "video_id": 397196251000476,
    "credits": 12
  },
  "usage": {
    "total_tokens": 36000,
    "input_tokens": 0,
    "input_tokens_details": {
      "cached_tokens": 0
    },
    "output_tokens": 36000,
    "output_tokens_details": {
      "reasoning_tokens": 0
    }
  }
}
```

> 返回的 `Resp.video_id` 即为任务 ID，请保存此值用于第二步查询结果

## 获取结果 示例代码

```python
import requests
import json

# 步骤1: 配置 API 连接信息

url = "https://www.dmxapi.cn/v1/responses"
api_key = "sk-******************************************"

# 步骤2: 配置请求头

headers = {
    "Content-Type": "application/json",
    "Authorization": f"{api_key}",
}

# 步骤3: 配置请求参数

payload = {
    # 【model】(string, 必填) 固定值: "paiwo-get"
    "model": "paiwo-get",

    # 【input】(string, 必填) 提交任务后返回的 video_id（转为字符串）
    "input": "397257570749203",
}

# 步骤4: 发送请求并输出结果

response = requests.post(url, headers=headers, json=payload)
result = response.json()

print(json.dumps(result, indent=2, ensure_ascii=False))

# 提取视频链接（status=1 表示生成成功）
if result.get("ErrCode") == 0 and result.get("Resp", {}).get("status") == 1:
    video_url = result["Resp"]["url"]
    print(f"\n视频链接: {video_url}")
```

### 返回示例

```json
{
  "ErrCode": 0,
  "ErrMsg": "Success",
  "Resp": {
    "id": 397592243780327,
    "prompt": "",
    "negative_prompt": "",
    "url": "https://media.pixverseai.cn/pixverse%2Fmp4%2Fmedia%2Fweb%2Fori%2F0b44a4fe-3745-4558-8a6c-8874050dc186_seed0.mp4",
    "status": 1,
    "seed": 0,
    "create_time": "2026-04-15T13:19:52Z",
    "modify_time": "2026-04-15T13:20:28Z",
    "outputWidth": 852,
    "outputHeight": 480,
    "has_audio": true,
    "credits": 16
  }
}

视频链接: https://media.pixverseai.cn/pixverse%2Fmp4%2Fmedia%2Fweb%2Fori%2F0b44a4fe-3745-4558-8a6c-8874050dc186_seed0.mp4
```

> `Resp.url` 为生成完成的视频下载链接，`Resp.status` 为 `1` 表示生成成功，`Resp.has_audio` 为 `true` 表示视频包含音频轨道。

<p align="center">
  <small>© 2026 DMXAPI paiwo-itv-hd 数字人对口型视频</small>
</p>
