---
description: 上传参考录音创建 MOSS 音色，获取可用于单人朗读与多人对话的 voice_id，包含录音要求和 Python 示例。
---

# MOSS 创建音色 API 使用文档

通过 DMXAPI 的 MOSS 音色创建接口，上传一段参考录音，生成可复用的音色标识 `voice_id`。适合已有目标声音录音、希望使用该音色进行后续语音合成的场景。接口同步返回结果，创建后的音色可用于单人朗读或多人对话。

## 接口地址

| 接口 | 请求方式 | URL |
|---|---|---|
| 创建音色 | POST | `https://www.dmxapi.cn/moss-speech/v1/audio/voices` |
:::warning
请妥善保管您的 API Key！下方示例直接在代码的 `api_key` 变量中填写密钥，请将占位值替换为您自己的 API Key，不要公开分享包含真实密钥的代码。
:::
## 模型名称
本接口不需要填写 `model`。
## 创建音色示例代码

```python
from pathlib import Path
import json
import mimetypes

import requests


# ===============================================================
# 步骤1：配置 API 连接信息
# ===============================================================
url = "https://www.dmxapi.cn/moss-speech/v1/audio/voices"
# DMXAPI API Key：直接将下方占位值替换为您自己的密钥
api_key = "YOUR_DMXAPI_API_KEY"
input_path = "input/voice_sample.mp3"  # 本地参考音频，支持 wav、mp3、m4a、flac，最大 10 MB，最长 30 秒
output_json_path = Path("outputs/moss_voice_result.json")
timeout = 120

# ===============================================================
# 步骤2：配置请求头
# ===============================================================
headers = {
    # multipart/form-data 的 Content-Type 由 requests 自动生成，不能手动固定 boundary
    "Authorization": f"Bearer {api_key}",
    "Accept": "application/json",
}

# ===============================================================
# 步骤3：配置请求参数
# ===============================================================
form_data = {
    "name": "my_voice",  # 可选：创建后的音色名称
}


# ===============================================================
# 步骤4：发送请求、处理响应并保存结果
# ===============================================================

def print_response(response):
    request_id = response.headers.get("x-request-id") or response.headers.get("request-id")
    print(f"status_code: {response.status_code}")
    if request_id:
        print(f"request_id: {request_id}")
    try:
        result = response.json()
    except ValueError:
        result = {"raw_text": response.text}
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return result


def main():
    if not api_key.strip() or api_key == "YOUR_DMXAPI_API_KEY":
        raise RuntimeError("请先在代码顶部的 api_key 中填写您的 DMXAPI API Key。")
    audio_path = Path(input_path)
    if not audio_path.is_file():
        raise FileNotFoundError(f"参考音频不存在：{audio_path}")
    if audio_path.suffix.lower() not in {".wav", ".mp3", ".m4a", ".flac"}:
        raise RuntimeError("参考录音仅支持 WAV、MP3、M4A、FLAC 格式。")
    if audio_path.stat().st_size > 10 * 1024 * 1024:
        raise RuntimeError("参考录音不能超过 10 MB。")
    # 文件扩展名与大小在此检查；实际格式和最长 30 秒的时长需在上传前确认。

    content_type = mimetypes.guess_type(audio_path.name)[0] or "application/octet-stream"
    with audio_path.open("rb") as audio_file:
        files = {
            "audio_sample": (audio_path.name, audio_file, content_type),
        }
        response = requests.post(
            url,
            headers=headers,
            data=form_data,
            files=files,
            timeout=timeout,
        )

    result = print_response(response)
    if not response.ok:
        raise RuntimeError(f"创建音色失败：HTTP {response.status_code}")
    if not isinstance(result, dict):
        raise RuntimeError("创建音色响应的 JSON 顶层不是对象。")

    voice_id = result.get("id") or result.get("voice_id")
    if not isinstance(voice_id, str) or not voice_id.strip():
        raise RuntimeError("创建音色成功，但响应中没有有效的 id/voice_id")

    output_json_path.parent.mkdir(parents=True, exist_ok=True)
    output_json_path.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"voice_id: {voice_id}")
    print(f"result_path: {output_json_path}")


if __name__ == "__main__":
    main()
```

## 返回示例
```json
{
  "created_at": 1793681094,
  "id": "task_smaNJzl52uuca2QOUAkYm0JHTpM2f0aK",
  "name": "my_voice",
  "object": "audio.voice",
  "voice_id": "3f3d63df-0dbf-47df-a33d-c53bb6c3a0e9"
}
```

<p align="center">
  <small>© 2026 DMXAPI MOSS 创建音色</small>
</p>
