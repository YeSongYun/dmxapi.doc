---
description: 使用 MOSS Flash 或 Pro 模型和指定 voice_id 进行单人朗读，介绍语言、停顿、音频格式以及 Python 下载示例。
---
# MOSS 单人朗读 API 使用文档

通过 DMXAPI 的 MOSS 单人同步语音接口，使用指定 `voice_id` 将文字合成为音频。支持 `moss-tts-1.5-flash` 和 `moss-tts-1.0-pro`；本示例使用 Flash 模型，以 JSON 获取音频 URL，并可将音频下载到本地。
## 接口地址

| 接口 | 请求方式 | URL |
|---|---|---|
| 单人文字转语音 | POST | `https://www.dmxapi.cn/moss-speech/v1/audio/speech` |
:::warning
请妥善保管您的 API Key！下方示例直接在代码的 `api_key` 变量中填写密钥，请将占位值替换为您自己的 API Key，不要公开分享包含真实密钥的代码。
:::
## 模型名称
| 模型 | 用途与差异 |
|---|---|
| `moss-tts-1.5-flash` | 本例使用；支持 `language` 及 `[pause 0.1s]` 至 `[pause 10.0s]` 的停顿标记 |
| `moss-tts-1.0-pro` | 单人朗读模型；不支持上述 `language` 参数和停顿标记 |
切换为 `moss-tts-1.0-pro` 时，请删除 `language` 参数，并从 `input` 中移除 Flash 专用的停顿标记。
## 单人朗读示例代码

```python
import json
from pathlib import Path
from tempfile import NamedTemporaryFile
from urllib.parse import urlparse

import requests

# ===============================================================
# 步骤1：配置 API 连接信息
# ===============================================================

# DMXAPI 网关的 MOSS 单人同步语音接口地址
# 使用 DMXAPI 网关地址，正式站域名为 www.dmxapi.cn
url = "https://www.dmxapi.cn/moss-speech/v1/audio/speech"

# DMXAPI API Key：直接将下方占位值替换为您自己的密钥
api_key = "YOUR_DMXAPI_API_KEY"

# 是否把返回的音频 URL 下载到本地；留空字符串则只输出 URL
output_path = "outputs/moss_single_speech.mp3"

# 请求超时时间，单位：秒
request_timeout = 1000

# ===============================================================
# 步骤2：配置请求头
# ===============================================================

headers = {
    "Content-Type": "application/json",  # JSON 请求体
    "Authorization": f"Bearer {api_key}",  # DMXAPI 网关鉴权
    "Accept": "application/json",  # delivery_method=url 返回 JSON
}

# ===============================================================
# 步骤3：配置请求参数
# ===============================================================

payload = {
    # 【model】(string, 必填) MOSS 单人语音模型
    # 可选：moss-tts-1.5-flash、moss-tts-1.0-pro
    "model": "moss-tts-1.5-flash",

    # 【input】(string, 必填) 要合成的文本
    # 只有 moss-tts-1.5-flash 支持 [pause 0.1s] 至 [pause 10.0s]
    "input": "你好，[pause 0.2s]欢迎使用 DMXAPI。",

    # 【voice_id】(string, 必填) MOSS 音色 ID
    # 请替换为创建音色、音色生成或已有音色库中的真实 ID
    "voice_id": "YOUR_MOSS_VOICE_ID",

    # 【language】(string, 可选) 发音语言，不负责翻译文本
    # 仅 moss-tts-1.5-flash 支持；必须填写英文全称，例如 Chinese、English
    "language": "Chinese",

    # 【response_format】(string, 可选) 输出格式
    # 可选：mp3、wav、flac、aac、opus
    "response_format": "mp3",

    # 【delivery_method】(string, 必填) 返回音频 URL 的 JSON
    "delivery_method": "url",

    # 【expected_duration_sec】(number, 可选) 期望时长，单位为秒，必须大于 0
    # 不需要时可以删除这一项
    "expected_duration_sec": 3.0,
}


# ===============================================================
# 步骤4：发送请求、处理响应并保存结果
# ===============================================================

def read_json_response(response):
    """解析网关 JSON 响应，并在错误时保留可定位信息。"""
    try:
        result = response.json()
    except ValueError as exc:
        preview = response.text[:500].replace("\n", " ")
        raise RuntimeError(
            f"网关返回的不是有效 JSON：HTTP {response.status_code}，响应内容={preview!r}"
        ) from exc

    if not isinstance(result, dict):
        raise RuntimeError("网关返回的 JSON 顶层不是对象。")
    return result


def validate_http_url(value, field_name):
    """只接受 HTTP(S) 地址，避免把错误内容当作音频地址使用。"""
    if not isinstance(value, str) or not value.strip():
        raise RuntimeError(f"响应中没有有效的 {field_name}。")
    parsed = urlparse(value)
    if parsed.scheme not in {"http", "https"} or not parsed.netloc:
        raise RuntimeError(f"响应中的 {field_name} 不是有效的 HTTP(S) 地址：{value!r}")
    return value


def save_audio(audio_url, output_path):
    """校验并下载音频，完整下载后再替换目标文件。"""
    destination = Path(output_path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    temporary_path = None
    try:
        with requests.get(audio_url, stream=True, timeout=request_timeout) as audio_response:
            audio_response.raise_for_status()
            content_type = audio_response.headers.get("Content-Type", "").split(";", 1)[0].lower()
            if not content_type.startswith("audio/") and content_type != "application/octet-stream":
                preview = audio_response.text[:200].replace("\n", " ")
                raise RuntimeError(
                    f"下载响应不是音频：Content-Type={content_type or 'missing'}，内容={preview!r}"
                )
            with NamedTemporaryFile(dir=destination.parent, suffix=".part", delete=False) as output_file:
                temporary_path = Path(output_file.name)
                for chunk in audio_response.iter_content(chunk_size=1024 * 1024):
                    if chunk:
                        output_file.write(chunk)

        if temporary_path.stat().st_size == 0:
            raise RuntimeError("下载的音频文件为空。")
        temporary_path.replace(destination)
    finally:
        if temporary_path is not None:
            temporary_path.unlink(missing_ok=True)
    print("output_path:", destination.resolve())


def main():
    if not api_key.strip() or api_key == "YOUR_DMXAPI_API_KEY":
        raise RuntimeError("请先在代码顶部的 api_key 中填写您的 DMXAPI API Key。")
    if payload["voice_id"] == "YOUR_MOSS_VOICE_ID":
        raise RuntimeError("请先在步骤3配置区填写真实的 payload['voice_id']。")

    response = requests.post(
        url,
        headers=headers,
        json=payload,
        timeout=request_timeout,
    )

    header_request_id = response.headers.get("x-request-id", "")
    print("status_code:", response.status_code)
    if header_request_id:
        print("header_request_id:", header_request_id)

    result = read_json_response(response)
    print(json.dumps(result, indent=2, ensure_ascii=False))

    if not response.ok:
        error = result.get("error")
        request_id_detail = f"，request_id={header_request_id}" if header_request_id else ""
        raise RuntimeError(
            f"MOSS 单人语音请求失败：HTTP {response.status_code}{request_id_detail}，error={error or result}"
        )

    audio_url = validate_http_url(
        result.get("audio_url") or result.get("url"),
        "audio_url",
    )
    request_id = header_request_id
    if request_id:
        print("request_id:", request_id)
    print("audio_url:", audio_url)

    if output_path.strip():
        save_audio(audio_url, output_path)


if __name__ == "__main__":
    main()
```

## 返回示例
```json
{
  "content_type": "audio/mpeg",
  "created_at": 1793681139,
  "id": "task_howt2giUeCNA0c0ZkXP9jQYMsoN2R5oq",
  "object": "audio.speech",
  "response_format": "mp3",
  "status": "SUCCESS",
  "url": "https://img.mosi.cn/matrix/transcoded/6ce809dd-104a-46ab-9d03-08b937b6cdf3/6ba826d0-b0c4-46ff-8a1f-0f11fd25c883.mp3?Expires=1793921143&OSSAccessKeyId=REDACTED&Signature=REDACTED",
  "usage": {
    "completion_tokens": 38,
    "input_characters": 27,
    "prompt_tokens": 134,
    "total_tokens": 172
  }
}
```
<p align="center">
  <small>© 2026 DMXAPI MOSS 单人朗读</small>
</p>
