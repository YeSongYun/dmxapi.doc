# music-cover 音乐生成 API 使用文档

基于 MiniMax music-cover 模型的音乐生成（翻唱）接口，通过 `/v1/responses` 端点调用。传入一段参考音频与目标翻唱风格描述，即可生成该音频的翻唱版本；不传歌词时会自动通过 ASR 从参考音频提取歌词，也可以配合「music-cover 翻唱前处理」接口拿到的 `cover_feature_id` 走**两步翻唱流程**，在修改歌词后再生成。支持流式与非流式两种传输方式，音频可返回 URL 或 hex 编码，并可自定义采样率、比特率与编码格式，适合翻唱创作、风格改编、二次创作配乐等场景。

## 接口地址

| 接口 | 请求方式 | URL |
|------|---------|-----|
| 音乐生成 | POST | `https://www.dmxapi.cn/v1/responses` |



:::warning
请妥善保管您的 API Key！严禁将密钥泄露给他人、硬编码到代码中或提交到公开的代码仓库。如果怀疑密钥已泄露，请立即前往 DMXAPI 官网重新生成。
:::

## 模型名称

- `music-cover`

## 音乐生成 示例代码

```python
import base64
import binascii
import json
import os

import requests


# ===============================================================
# 步骤1: 配置 API 连接信息
# ===============================================================

# DMXAPI 服务端点地址
url = "https://www.dmxapi.cn/v1/responses"

# DMXAPI 密钥，请直接替换为你新生成的密钥。
api_key = "请在这里填写你的 DMXAPI 密钥"
if not api_key or api_key == "请在这里填写你的 DMXAPI 密钥":
    raise RuntimeError("请先在代码中填写 api_key")


# ===============================================================
# 步骤2: 配置请求头
# ===============================================================

headers = {
    "Content-Type": "application/json",
    "Authorization": api_key,
}


# ===============================================================
# 步骤3: 配置请求参数
# ===============================================================

payload = {
    # 【model】(string, 必填) 调用的模型名称
    "model": "music-cover",

    # 【stream】(bool, 可选) 是否使用流式传输，默认值 False
    # 当 stream 为 True 时，output_format 仅支持 hex。
    "stream": False,

    # 【input】(object, 必填) 输入信息
    "input": {
        # 【aigc_watermark】(bool, 可选) 是否在音频末尾添加水印
        # 仅在非流式请求时生效。
        "aigc_watermark": False,

        # -------------------------------------------------------
        # 以下三个官方来源字段任意填入一个即可。
        # 直接保留要使用的那一行，另外两行不要放入 payload。
        # -------------------------------------------------------

        # 方式一：公网音频 URL
        "audio_url": "https://music.163.com/song/media/outer/url?id=1330348068.mp3",

        # 方式二：裸 Base64，或者本地音频文件路径
        # 如果填写本地路径，步骤4会自动读取并转换成裸 Base64。
        # "audio_base64": r"C:\Users\Y\Desktop\audio.mp3",
        # "audio_base64": "<裸 Base64 字符串>",

        # 方式三：「翻唱前处理」接口返回的特征 ID
        # 使用该字段时必须同时填写 lyrics。
        # "cover_feature_id": "c39f4e87d52f6b48a5837f60d84f2a38",

        # 【output_format】(string, 可选) url 或 hex
        "output_format": "url",

        # 【prompt】(string, 必填) 目标翻唱风格，长度 10～300 个字符
        "prompt": "流行音乐, 难过, 适合在下雨的晚上",

        # 【lyrics】(string, 可选) 使用 cover_feature_id 时必填
        # "lyrics": "[Verse]\n街灯微亮晚风轻抚\n影子拉长独自漫步",

        # 【audio_setting】(object, 可选) 音频输出配置
        # "audio_setting": {
        #     "sample_rate": 44100,
        #     "bitrate": 256000,
        #     "format": "mp3",
        # },
    },
}


# ===============================================================
# 步骤4: 自动识别并处理实际填入的官方来源字段
# ===============================================================

_MEDIA_RULES = {
    "audio": {
        "allow_url": True,
        "allow_data_uri": False,
        "allow_raw_base64": True,
        "allow_local_file": True,
        "local_encoding": "raw_base64",
        "file_formats": {
            ".mp3": "",
            ".wav": "",
            ".m4a": "",
            ".aac": "",
            ".ogg": "",
            ".flac": "",
        },
        "data_types": [],
    },
}


def _resolve_media(value: str, rule: dict, field: str) -> tuple:
    """返回 (处理后的值, url/raw_base64/data_uri)。"""
    if not isinstance(value, str) or not value:
        raise ValueError(f"{field} 必须是非空字符串")

    # 公网 URL
    if value.startswith(("http://", "https://")):
        if rule["allow_url"]:
            return value, "url"
        raise ValueError(f"{field} 不接受 URL")

    # Data URI
    if value.startswith("data:"):
        if not rule["allow_data_uri"]:
            raise ValueError(f"{field} 不接受 Data URI，请使用裸 Base64")
        header, separator, encoded = value.partition(",")
        expected = {
            f"data:{media_type};base64"
            for media_type in rule["data_types"]
        }
        if not separator or header not in expected or not encoded:
            raise ValueError(
                f"{field} 的 Data URI 头无效；允许: {sorted(expected)}"
            )
        try:
            base64.b64decode(encoded, validate=True)
        except (binascii.Error, ValueError) as exc:
            raise ValueError(
                f"{field} 的 Data URI 正文不是合法 Base64"
            ) from exc
        return value, "data_uri"

    # 本地文件路径
    if os.path.isfile(value):
        if not rule["allow_local_file"]:
            raise ValueError(f"{field} 不接受本地文件")
        extension = os.path.splitext(value)[1].lower()
        if extension not in rule["file_formats"]:
            raise ValueError(
                f"{field} 不支持本地文件格式 {extension}；"
                f"允许: {sorted(rule['file_formats'])}"
            )
        if os.path.getsize(value) > 50 * 1024 * 1024:
            raise ValueError(f"{field} 的本地文件不能超过 50MB")
        with open(value, "rb") as audio_file:
            encoded = base64.b64encode(audio_file.read()).decode("ascii")
        if rule["local_encoding"] == "raw_base64":
            return encoded, "raw_base64"
        media_type = rule["file_formats"][extension]
        return f"data:{media_type};base64,{encoded}", "data_uri"

    # 已经是裸 Base64
    if rule["allow_raw_base64"]:
        try:
            base64.b64decode(value, validate=True)
            return value, "raw_base64"
        except (binascii.Error, ValueError):
            pass

    raise ValueError(f"{field} 不符合接口媒体契约")


def _normalize_audio_source(input_data: dict) -> None:
    """自动识别 input 中实际填写的官方来源字段并原地规整。"""
    official_fields = (
        "audio_url",
        "audio_base64",
        "cover_feature_id",
    )
    provided_fields = [
        field for field in official_fields if field in input_data
    ]

    if not provided_fields:
        raise ValueError(
            "请在 input 中填入 audio_url、audio_base64、"
            "cover_feature_id 中的任意一个"
        )
    if len(provided_fields) > 1:
        raise ValueError(
            "audio_url、audio_base64、cover_feature_id "
            "不能同时填入多个"
        )

    source_field = provided_fields[0]
    source_value = input_data[source_field]
    field_path = f'payload["input"]["{source_field}"]'

    # cover_feature_id 是特征 ID，不是媒体内容，不做 Base64/URL 转换。
    if source_field == "cover_feature_id":
        if not isinstance(source_value, str) or not source_value:
            raise ValueError(f"{field_path} 必须是非空字符串")
        lyrics = input_data.get("lyrics")
        if not isinstance(lyrics, str) or not lyrics:
            raise ValueError(
                '使用 cover_feature_id 时必须填写 payload["input"]["lyrics"]'
            )
        return

    # audio_url 或 audio_base64：按实际内容判断 URL、本地文件或裸 Base64，
    # 然后写回接口真正需要的官方字段。
    media_value, media_form = _resolve_media(
        source_value,
        _MEDIA_RULES["audio"],
        field_path,
    )
    media_targets = {
        "url": "audio_url",
        "raw_base64": "audio_base64",
    }
    target_field = media_targets.get(media_form)
    if target_field is None:
        raise ValueError(f"{field_path} 解析出了接口不支持的媒体形式")

    input_data.pop("audio_url", None)
    input_data.pop("audio_base64", None)
    input_data[target_field] = media_value


_normalize_audio_source(payload["input"])

# 流式请求只支持 hex，并且不能发送 aigc_watermark。
if payload.get("stream") is True:
    if payload["input"].get("output_format", "hex") != "hex":
        raise ValueError("stream=True 时 output_format 必须为 hex")
    payload["input"].pop("aigc_watermark", None)


# ===============================================================
# 步骤5: 发送请求并输出结果
# ===============================================================

is_stream = payload.get("stream") is True
response = requests.post(
    url,
    headers=headers,
    json=payload,
    stream=is_stream,
    timeout=(15, 600),
)

if response.status_code >= 400:
    raise RuntimeError(
        f"请求失败，HTTP {response.status_code}: {response.text[:4000]}"
    )

if is_stream:
    response.encoding = "utf-8"
    for line in response.iter_lines(decode_unicode=True):
        if line:
            print(line)
else:
    try:
        result = response.json()
    except requests.exceptions.JSONDecodeError:
        print(response.text)
    else:
        print(json.dumps(result, indent=2, ensure_ascii=False))

```

## 返回示例

```json
{
  "data": {
    "audio": "https://minimax-algeng-chat-tts.oss-cn-wulanchabu.aliyuncs.com/audio%2Feffect%2F06d1f7c615375d107aee43f29ab403f0_1786955119882_3488.mp3?Expires=1787041520&OSSAccessKeyId=LTAI5tGLnRTkBjLuYPjNcKQ8&Signature=WMI21SNnJDTDtE43IYk7azCtwt8%3D",
    "status": 2
  },
  "trace_id": "06d1f7c615375d107aee43f29ab403f0",
  "extra_info": {
    "music_duration": 335072,
    "music_sample_rate": 44100,
    "music_channel": 2,
    "bitrate": 256000,
    "music_size": 10724299
  },
  "analysis_info": null,
  "base_resp": {
    "status_code": 0,
    "status_msg": "success"
  }
}
```

主要返回字段说明：

- `data.audio`：生成的音频。当 `output_format` 为 `url` 时返回音频链接（**有效期 24 小时**，请及时下载）；当 `output_format` 为 `hex` 时返回音频文件的 16 进制编码字符串。
- `data.status`：音乐合成状态。`1` 合成中；`2` 已完成。
- `trace_id`：请求追踪 ID。
- `extra_info`：生成音频的附加信息，包含时长 `music_duration`（毫秒）、采样率 `music_sample_rate`、声道数 `music_channel`、比特率 `bitrate` 和文件大小 `music_size`（字节）。

<p align="center">
  <small>© 2026 DMXAPI music-cover 音乐生成</small>
</p>
