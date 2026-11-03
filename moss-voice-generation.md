---
description: 使用 moss-voice-generator-1.0 根据文字描述生成音色与试听音频，支持返回可复用的 voice_id，附 Python 调用和下载示例。
---

# MOSS 音色生成 API 使用文档

通过 DMXAPI 的 MOSS 音色生成接口，用文字描述音色风格、年龄、情绪或语速，并用指定文本生成试听音频。设置 `create_voice=True` 时，同时创建可复用音色并返回 `voice_id`，供后续单人朗读或多人对话使用。该接口同步返回，无需查询任务状态。

## 接口地址

| 接口 | 请求方式 | URL |
|---|---|---|
| 音色生成与试听 | POST | `https://www.dmxapi.cn/moss-speech/v1/audio/voice/generations` |
:::warning
请妥善保管您的 API Key！下方示例直接在代码的 `api_key` 变量中填写密钥，请将占位值替换为您自己的 API Key，不要公开分享包含真实密钥的代码。
:::
## 模型名称
- `moss-voice-generator-1.0`
本接口固定使用该音色生成模型，不能替换为单人或多人文字转语音模型。
## 音色生成示例代码

```python
from pathlib import Path
from tempfile import NamedTemporaryFile
import json
from urllib.parse import urlparse

import requests


# ===============================================================
# 步骤1：配置 API 连接信息
# ===============================================================
url = "https://www.dmxapi.cn/moss-speech/v1/audio/voice/generations"
# DMXAPI API Key：直接将下方占位值替换为您自己的密钥
api_key = "YOUR_DMXAPI_API_KEY"
output_path = Path("outputs/voice_preview.mp3")
output_json_path = Path("outputs/voice_generation_result.json")
timeout = 120

# ===============================================================
# 步骤2：配置请求头
# ===============================================================
headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {api_key}",
    "Accept": "application/json",
}

# ===============================================================
# 步骤3：配置请求参数
# ===============================================================
payload = {
    # 【model】(string, 必填) 音色生成模型 ID，固定为 moss-voice-generator-1.0（TTS 模型不支持此接口）
    "model": "moss-voice-generator-1.0",

    # 【input】(string, 必填) 要生成的语音文本
    "input": "你好，这是音色生成测试。一二三四五六七",

    # 【instruction】(string, 必填) 音色风格、年龄、情绪、语速等描述
    "instruction": "年轻、温柔、清晰，语速适中的女声。",

    # 【response_format】(string, 可选) 同步生成的音频格式
    "response_format": "mp3",

    # 【delivery_method】(string, 可选) 使用 url，以 JSON 返回音频地址
    "delivery_method": "url",

    # 【create_voice】(boolean, 可选) true 时同时创建可复用音色并返回 voice_id
    "create_voice": True,
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


def is_http_url(value):
    parsed = urlparse(str(value))
    return parsed.scheme in {"http", "https"} and bool(parsed.netloc)


def download_audio(audio_url):
    if not is_http_url(audio_url):
        raise RuntimeError("响应中的音频 URL 不是有效的 HTTP(S) 地址")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    temporary_path = None
    try:
        with requests.get(audio_url, stream=True, timeout=timeout) as response:
            response.raise_for_status()
            content_type = response.headers.get("Content-Type", "").split(";", 1)[0].lower()
            if not content_type.startswith("audio/") and content_type != "application/octet-stream":
                preview = response.text[:200].replace("\n", " ")
                raise RuntimeError(
                    f"下载响应不是音频：Content-Type={content_type or 'missing'}，内容={preview!r}"
                )
            # 完整下载后再替换目标文件，避免中断时留下残缺音频。
            with NamedTemporaryFile(dir=output_path.parent, suffix=".part", delete=False) as output_file:
                temporary_path = Path(output_file.name)
                for chunk in response.iter_content(chunk_size=1024 * 1024):
                    if chunk:
                        output_file.write(chunk)

        if temporary_path.stat().st_size == 0:
            raise RuntimeError("下载的音频文件为空。")
        temporary_path.replace(output_path)
    finally:
        if temporary_path is not None:
            temporary_path.unlink(missing_ok=True)


def main():
    if not api_key.strip() or api_key == "YOUR_DMXAPI_API_KEY":
        raise RuntimeError("请先在代码顶部的 api_key 中填写您的 DMXAPI API Key。")
    response = requests.post(url, headers=headers, json=payload, timeout=timeout)
    result = print_response(response)
    if not response.ok:
        raise RuntimeError(f"音色生成请求失败：HTTP {response.status_code}")
    if not isinstance(result, dict) or "raw_text" in result:
        raise RuntimeError("音色生成响应不是有效的 JSON 对象。")

    output_json_path.parent.mkdir(parents=True, exist_ok=True)
    output_json_path.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")

    audio_url = result.get("url") or result.get("audio_url") or result.get("content_url")
    if audio_url:
        download_audio(audio_url)
        print(f"audio_path: {output_path}")
    else:
        print("响应中没有音频 URL，已仅保存 JSON 结果。")

    voice_id = result.get("voice_id")
    if voice_id:
        print(f"voice_id: {voice_id}")
    print(f"result_path: {output_json_path}")


if __name__ == "__main__":
    main()
```

## 返回示例
```json
{
  "content_type": "audio/mpeg",
  "created_at": 1793681047,
  "id": "task_YHSNYiv3hhHYs8FvNWRzU9JwEGsq0mv4",
  "object": "audio.voice_generation",
  "response_format": "mp3",
  "status": "SUCCESS",
  "url": "https://img.mosi.cn/matrix/transcoded/6ce809dd-104a-46ab-9d03-08b937b6cdf3/7fc31978-2347-483a-881c-b68814edc69e.mp3?Expires=1793921055&OSSAccessKeyId=REDACTED&Signature=REDACTED",
  "voice_id": "57b77fab-70c5-49a7-9ef0-dd0db69b3cad"
}
```
<p align="center">
  <small>© 2026 DMXAPI MOSS 音色生成</small>
</p>
