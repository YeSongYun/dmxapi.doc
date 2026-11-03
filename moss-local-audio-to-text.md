---
description: 使用 MOSS 以 multipart 表单上传本地音频或视频并同步转写，包含文件限制、模型选择和 Python 示例。
---

# MOSS 本地音频转文字 API 使用文档

通过 DMXAPI 的 MOSS 同步转写接口，以文件上传方式提交本地音频或视频，并直接获得识别结果。本示例使用 `moss-transcribe-1.0` 进行普通转写，适合本机录音文件的字幕、访谈记录和文本整理。

## 接口地址

| 接口 | 请求方式 | URL |
|---|---|---|
| 本地音频转文字 | POST | `https://www.dmxapi.cn/moss-speech/v1/audio/transcriptions` |
:::warning
请妥善保管您的 API Key！下方示例直接在代码的 `api_key` 变量中填写密钥，请将占位值替换为您自己的 API Key，不要公开分享包含真实密钥的代码。
:::
## 模型名称
- `moss-transcribe-1.0`：普通语音转文字。
- `moss-transcribe-diarize-pro`：多说话人转写、热词和 SSE 流式输出使用。
## 本地音频转文字示例代码
```python
import json
import mimetypes
from pathlib import Path

import requests

# ===============================================================
# 步骤1：配置 API 连接信息
# ===============================================================

# DMXAPI 网关的 MOSS 同步音频转写接口地址
# 使用 DMXAPI 网关地址，正式站域名为 www.dmxapi.cn
url = "https://www.dmxapi.cn/moss-speech/v1/audio/transcriptions"

# DMXAPI API Key：直接将下方占位值替换为您自己的密钥
api_key = "YOUR_DMXAPI_API_KEY"

# 本地音频或视频文件路径，单文件最大 512 MB
input_path = Path("input/audio.wav")

# 转写结果保存路径；JSON 结果保存为格式化 JSON，text 结果保存为纯文本
output_path = Path("outputs/moss_transcription_file_result.json")

# 请求超时时间，单位：秒
request_timeout = 1000

# ===============================================================
# 步骤2：配置请求头
# ===============================================================

headers = {
    # multipart/form-data 的 Content-Type 由 requests 自动生成，不能手动固定 boundary
    "Authorization": f"Bearer {api_key}",  # DMXAPI 网关鉴权
    "Accept": "application/json",  # response_format=text 时也可以改成 text/plain
}

# ===============================================================
# 步骤3：配置请求参数
# ===============================================================

form_data = {
    # 【model】(string, 必填) 普通转写使用 moss-transcribe-1.0
    # 启用 diarize 或填写非空 keyterms 时，必须改为 moss-transcribe-diarize-pro
    "model": "moss-transcribe-1.0",

    # 【response_format】(string, 可选) json、text 、diarized_json或verbose_json
    # json；启用 diarize 时包含说话人分段
    # text/plain:  纯文本，仅适用于非流式。
    # diarized_json 会返回说话人分段，并要求使用专业模型
    # verbose_json: 仅适用于流式请求，返回包含增量文本、说话人分段、时间戳和用量信息的 SSE 事件。当前事件结构与其他流式格式一致。
    "response_format": "json",

    # 【diarize】(string, 可选) multipart 中使用 true/false 字符串
    # 设为 true 时必须使用 moss-transcribe-diarize-pro
    "diarize": "false",

    # 【keyterms】(string, 可选) multipart 中必须传 JSON 字符串数组
    # 例如 json.dumps(["MOSS", "SGLang"], ensure_ascii=False)
    # 空数组表示不启用热词；非空数组必须使用 moss-transcribe-diarize-pro
    "keyterms": json.dumps([], ensure_ascii=False),
}


# ===============================================================
# 步骤4：发送请求、处理响应并保存结果
# ===============================================================

def read_result(response, response_format):
    """成功的 text 响应按原文保留；其他响应优先解析 JSON。"""
    if response.ok and response_format == "text":
        return response.text
    try:
        return response.json()
    except ValueError:
        return response.text


def print_result(result):
    """格式化输出 JSON 或纯文本转写结果。"""
    if isinstance(result, (dict, list)):
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print(result)


def save_result(result, output_path):
    """保存转写结果，不把错误响应当作成功结果保存。"""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    if isinstance(result, (dict, list)):
        output_path.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    else:
        output_path.write_text(str(result), encoding="utf-8")
    print("output_path:", output_path.resolve())


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
            url,
            headers=headers,
            data=form_data,
            files={"file": (input_path.name, input_file, mime_type)},
            timeout=request_timeout,
        )

    header_request_id = response.headers.get("x-request-id", "")
    print("status_code:", response.status_code)
    if header_request_id:
        print("header_request_id:", header_request_id)

    content_type = response.headers.get("Content-Type", "")
    if "text/html" in content_type.lower():
        raise RuntimeError(
            f"网关返回了 HTML 页面而不是接口结果（HTTP {response.status_code}），"
            "请检查 url 是否为本文列出的完整接口地址。"
        )

    result = read_result(response, form_data.get("response_format", "json"))
    print_result(result)

    if not response.ok:
        request_id_detail = f"，request_id={header_request_id}" if header_request_id else ""
        raise RuntimeError(
            f"MOSS 文件转写请求失败：HTTP {response.status_code}{request_id_detail}"
        )

    request_id = header_request_id
    if request_id:
        print("request_id:", request_id)
    save_result(result, output_path)


if __name__ == "__main__":
    main()
```
## 返回示例

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
  <small>© 2026 DMXAPI MOSS 本地音频转文字</small>
</p>
