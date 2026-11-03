---
description: 分两步演示 MOSS 文件上传与 file_id 转写，分别提供可独立运行的 Python 示例，支持复用已有文件及保存转写结果。
---

# MOSS 上传文件并使用 file_id 转文字 API 使用文档

通过 DMXAPI 的 MOSS 接口，先上传本地音频或视频取得 `file_id`，再使用该标识获取识别文字。本文提供两个可独立运行的示例：第一部分上传文件并输出文件标识；第二部分填写该标识并执行转写。已有可用 `file_id` 时，可以直接使用第二部分。

## 接口地址

| 步骤 | 请求方式 | URL | 请求体类型 |
|---|---|---|---|
| 上传文件 | POST | `https://www.dmxapi.cn/moss-speech/v1/files` | `multipart/form-data` |
| 使用 file_id 转文字 | POST | `https://www.dmxapi.cn/moss-speech/v1/audio/transcriptions` | `application/json` |

:::warning
请妥善保管您的 API Key！下方两个示例均需在各自代码的 `api_key` 变量中填写密钥，请将占位值替换为您自己的 API Key，不要公开分享包含真实密钥的代码。
:::

## 调用流程

1. 运行第一部分，用 `file` 字段上传本地文件，`purpose` 填写 `transcription`。
2. 从终端输出中复制 `file_id`。上传响应也会保存到本地，便于后续查看。
3. 将标识填写到第二部分的 `payload["file_id"]`，配置模型和转写参数。
4. 运行第二部分，打印并保存识别结果。

后续需要再次识别同一个文件时，可以直接在第二部分复用已取得的 `file_id`。


## 模型名称

| 步骤 | 模型要求 |
|---|---|
| 上传文件 | 无需填写 `model` |
| 普通转写 | `moss-transcribe-1.0` |
| 说话人分离、热词或分段 JSON | `moss-transcribe-diarize-pro` |

## 第一步：上传文件获取 file_id
```python
import json
import mimetypes
from pathlib import Path

import requests

# ===============================================================
# 步骤1：配置上传接口和本地路径
# ===============================================================
upload_url = "https://www.dmxapi.cn/moss-speech/v1/files"
api_key = "YOUR_DMXAPI_API_KEY"
input_path = Path("input/audio.wav")
upload_result_path = Path("outputs/moss_file_upload_result.json")
request_timeout = 1000  # 客户端请求超时时间，单位：秒

# ===============================================================
# 步骤2：配置请求头和上传参数
# ===============================================================
headers = {
    "Authorization": f"Bearer {api_key}",
    "Accept": "application/json",
    # 不手动设置 Content-Type，由 requests 生成 multipart boundary
}
form_data = {
    "purpose": "transcription",
}

# ===============================================================
# 步骤3：上传文件，保存响应并打印 file_id
# ===============================================================
def main():
    if not api_key.strip() or api_key == "YOUR_DMXAPI_API_KEY":
        raise RuntimeError("请先在代码顶部的 api_key 中填写您的 DMXAPI API Key。")
    if not input_path.is_file():
        raise RuntimeError(f"找不到输入文件：{input_path.resolve()}")
    if input_path.stat().st_size > 512 * 1024 * 1024:
        raise RuntimeError("输入文件超过 MOSS 单文件 512 MB 限制。")

    mime_type = mimetypes.guess_type(input_path.name)[0] or "application/octet-stream"
    with input_path.open("rb") as input_file:
        response = requests.post(
            upload_url,
            headers=headers,
            data=form_data,
            files={"file": (input_path.name, input_file, mime_type)},
            timeout=request_timeout,
        )

    print("status_code:", response.status_code)
    request_id = response.headers.get("x-request-id") or response.headers.get("request-id")
    if request_id:
        print("request_id:", request_id)

    try:
        result = response.json()
    except ValueError as error:
        raise RuntimeError(
            f"文件上传接口返回的不是 JSON：HTTP {response.status_code}"
        ) from error
    print(json.dumps(result, indent=2, ensure_ascii=False))

    if not response.ok:
        raise RuntimeError(f"MOSS 文件上传失败：HTTP {response.status_code}")
    if not isinstance(result, dict):
        raise RuntimeError("文件上传响应不是 JSON 对象。")

    file_id = result.get("file_id") or result.get("id")
    if not isinstance(file_id, str) or not file_id.strip():
        raise RuntimeError("文件上传成功响应中没有 file_id 或 id。")

    upload_result_path.parent.mkdir(parents=True, exist_ok=True)
    upload_result_path.write_text(
        json.dumps(result, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    print("output_path:", upload_result_path.resolve())
    print("file_id:", file_id)
    print("请将上述文件标识复制到第二部分的 payload[\"file_id\"] 中。")


if __name__ == "__main__":
    main()
```

## 上传返回示例

以下为测试环境上传 `audio.wav` 后的实际返回；该文件由音色生成示例的试听音频转换得到。

```json
{
  "bytes": 218958,
  "created_at": 1793681093,
  "file_id": "59d3247a-de98-4aa7-978c-cc760589501f",
  "filename": "audio.wav",
  "id": "task_5ysSyUWSU0Dpa9i3mxolfLw56v4Uk074",
  "object": "file",
  "purpose": "transcription",
  "status": "processed"
}
```

第二步请使用响应中的 `file_id`。本次响应里的 `id` 是上传请求的任务标识；文件标识请以您实际上传时返回的值为准。
## 第二步：使用 file_id 转文字

将代码另存为 `moss_transcribe_file_id.py`，填写该示例中的 `api_key`，并将第一步获得的标识替换到 `payload["file_id"]`，运行 `python moss_transcribe_file_id.py`。此示例只调用转写接口，无需读取本地音频或第一部分的代码。

```python
import json
from pathlib import Path

import requests

# ===============================================================
# 步骤1：配置转写接口和结果路径
# ===============================================================
transcription_url = "https://www.dmxapi.cn/moss-speech/v1/audio/transcriptions"
api_key = "YOUR_DMXAPI_API_KEY"
transcription_result_path = Path("outputs/moss_transcription_file_id_result.json")
request_timeout = 1000  # 客户端请求超时时间，单位：秒

# ===============================================================
# 步骤2：配置请求头和转写参数
# ===============================================================
headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json",
    "Accept": "application/json",
}
payload = {
    # 普通转写使用 moss-transcribe-1.0
    # 启用说话人分离、非空热词或 diarized_json 时改为 moss-transcribe-diarize-pro
    "model": "moss-transcribe-1.0",
    # 填写第一部分返回的实际文件标识，也可以复用已有的 file_id
    "file_id": "YOUR_FILE_ID",
    "response_format": "json",  # json、text 或 diarized_json
    "diarize": False,
    "keyterms": [],  # 最多 20 个，每个最多 30 个字符
    # 使用 file_id 时，不要再添加 file、url 或 audio_url
}

# ===============================================================
# 步骤3：提交转写请求，打印并保存结果
# ===============================================================
def read_result(response, response_format):
    """成功的 text 响应按原文保留；其他响应优先解析 JSON。"""
    if response.ok and response_format == "text":
        return response.text
    try:
        return response.json()
    except ValueError:
        return response.text


def main():
    if not api_key.strip() or api_key == "YOUR_DMXAPI_API_KEY":
        raise RuntimeError("请先在代码顶部的 api_key 中填写您的 DMXAPI API Key。")
    file_id = payload.get("file_id")
    if not isinstance(file_id, str) or not file_id.strip() or file_id.strip() == "YOUR_FILE_ID":
        raise RuntimeError("请在 payload[\"file_id\"] 中填写第一部分返回的实际文件标识。")
    payload["file_id"] = file_id.strip()

    request_headers = dict(headers)
    if payload.get("response_format") == "text":
        request_headers["Accept"] = "text/plain"

    response = requests.post(
        transcription_url,
        headers=request_headers,
        json=payload,
        timeout=request_timeout,
    )
    print("status_code:", response.status_code)
    request_id = response.headers.get("x-request-id") or response.headers.get("request-id")
    if request_id:
        print("request_id:", request_id)

    content_type = response.headers.get("Content-Type", "").lower()
    if "text/html" in content_type:
        raise RuntimeError(
            f"网关返回了 HTML 页面而不是转写结果（HTTP {response.status_code}），"
            "请检查 transcription_url 是否为本文列出的完整接口地址。"
        )

    result = read_result(response, payload.get("response_format", "json"))
    if isinstance(result, (dict, list)):
        text = json.dumps(result, indent=2, ensure_ascii=False) + "\n"
    else:
        text = str(result)
    print(text)

    if not response.ok:
        raise RuntimeError(f"MOSS file_id 转写失败：HTTP {response.status_code}")

    transcription_result_path.parent.mkdir(parents=True, exist_ok=True)
    transcription_result_path.write_text(text, encoding="utf-8")
    print("output_path:", transcription_result_path.resolve())


if __name__ == "__main__":
    main()
```
## 转写返回示例

以下为测试环境使用第一步返回的 `file_id`，按上方 `response_format="json"` 配置执行转写的实际返回。

```json
{
  "text": "你好，这是音色生成测试一二三四五六七。",
  "usage": {
    "completion_tokens": 13,
    "input_audio_seconds": 4.56,
    "prompt_tokens": 57,
    "seconds": 5,
    "total_tokens": 70,
    "type": "duration"
  }
}
```
<p align="center">
  <small>© 2026 DMXAPI MOSS 上传文件并使用 file_id 转文字</small>
</p>
