---
description: 通过 MOSS 同步转写接口将公网音频或视频 URL 转成文字，包含模型选择、说话人分离、请求参数和 Python 示例。
---

# MOSS 音频 URL 转文字 API 使用文档
通过 DMXAPI 的 MOSS 同步转写接口，将服务端可访问的公网音频或视频链接转换为文字。适合已有云端音频地址的会议、访谈等场景。本示例使用 `moss-transcribe-diarize-pro` 并启用说话人分离；请求完成后直接返回结果，无需查询任务状态。
## 接口地址
| 接口 | 请求方式 | URL |
|---|---|---|
| 音频 URL 转文字 | POST | `https://www.dmxapi.cn/moss-speech/v1/audio/transcriptions` |
:::warning
请妥善保管您的 API Key！下方示例直接在代码的 `api_key` 变量中填写密钥，请将占位值替换为您自己的 API Key，不要公开分享包含真实密钥的代码。
:::

## 模型名称

- `moss-transcribe-1.0`：普通语音转文字。
- `moss-transcribe-diarize-pro`：多说话人转写、热词和 SSE 流式输出使用。

启用上述任一专业能力时，都必须选择 `moss-transcribe-diarize-pro`。

## 音频 URL 转文字示例代码

```python
import json
from pathlib import Path
from urllib.parse import urlparse

import requests

# ===============================================================
# 步骤1：配置 API 连接信息
# ===============================================================

# DMXAPI 网关的 MOSS 同步音频转写接口地址
# 使用 DMXAPI 网关地址，正式站域名为 www.dmxapi.cn
url = "https://www.dmxapi.cn/moss-speech/v1/audio/transcriptions"

# DMXAPI API Key：直接将下方占位值替换为您自己的密钥
api_key = "YOUR_DMXAPI_API_KEY"

# 转写结果保存路径；JSON 结果保存为格式化 JSON，text 结果保存为纯文本
output_path = Path("outputs/moss_transcription_url_result.json")

# 请求超时时间，单位：秒
request_timeout = 1000

# ===============================================================
# 步骤2：配置请求头
# ===============================================================

headers = {
    "Content-Type": "application/json",  # JSON 请求体
    "Authorization": f"Bearer {api_key}",  # DMXAPI 网关鉴权
    "Accept": "application/json",  # response_format=text 时也可以改成 text/plain
}

# ===============================================================
# 步骤3：配置请求参数
# ===============================================================

payload = {
    # 【model】(string, 必填) 普通转写使用 moss-transcribe-1.0
    # 启用 diarize 或填写非空 keyterms 时，必须改为 moss-transcribe-diarize-pro
    "model": "moss-transcribe-diarize-pro",

    # 【url】(string, 四选一) 服务端可访问的公网音频或视频 URL
    # 不能使用 localhost、回环地址或私网地址
    "url": "https://arkdocs.tos-cn-beijing.volces.com/files/advanced-usage/audio_demo_video_multispeaker_02.m4a",

    # 【response_format】(string, 可选) json、text 、diarized_json或verbose_json
    # json；启用 diarize 时包含说话人分段
    # text/plain:  纯文本，仅适用于非流式。
    # diarized_json 会返回说话人分段，并要求使用专业模型
    # verbose_json: 仅适用于流式请求，返回包含增量文本、说话人分段、时间戳和用量信息的 SSE 事件。当前事件结构与其他流式格式一致。
    "response_format": "json",

    # 【diarize】(boolean, 可选) 是否启用说话人分离
    # 设为 True 时必须使用 moss-transcribe-diarize-pro
    "diarize": True,

    # 【keyterms】(string[], 可选) 热词列表，最多 20 个，每个最多 30 个字符
    # 空数组表示不启用热词；非空数组必须使用 moss-transcribe-diarize-pro
    "keyterms": [],
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


def validate_public_url(value):
    """检查配置的输入地址是否为 HTTP(S) URL。"""
    parsed = urlparse(value)
    if parsed.scheme not in {"http", "https"} or not parsed.netloc:
        raise RuntimeError(f"payload['url'] 不是有效的 HTTP(S) 地址：{value!r}")


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
    validate_public_url(payload["url"])

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

    content_type = response.headers.get("Content-Type", "")
    if "text/html" in content_type.lower():
        raise RuntimeError(
            f"网关返回了 HTML 页面而不是接口结果（HTTP {response.status_code}），"
            "请检查 url 是否为本文列出的完整接口地址。"
        )

    result = read_result(response, payload.get("response_format", "json"))
    print_result(result)

    if not response.ok:
        request_id_detail = f"，request_id={header_request_id}" if header_request_id else ""
        raise RuntimeError(
            f"MOSS URL 转写请求失败：HTTP {response.status_code}{request_id_detail}"
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
  "duration": 6.5698125,
  "segments": [
    {
      "end": 1.55,
      "id": "seg_001",
      "speaker": "S01",
      "start": 0.63,
      "text": "太厉害了 真能上班",
      "type": "transcript.text.segment"
    },
    {
      "end": 3.28,
      "id": "seg_002",
      "speaker": "S02",
      "start": 1.51,
      "text": "没错 我觉得这个排版真的是让我",
      "type": "transcript.text.segment"
    },
    {
      "end": 4.56,
      "id": "seg_003",
      "speaker": "S01",
      "start": 3.29,
      "text": "这不很多朋友就",
      "type": "transcript.text.segment"
    },
    {
      "end": 5.59,
      "id": "seg_004",
      "speaker": "S02",
      "start": 4.57,
      "text": "神清气爽",
      "type": "transcript.text.segment"
    },
    {
      "end": 5.97,
      "id": "seg_005",
      "speaker": "S01",
      "start": 5.56,
      "text": "解放了",
      "type": "transcript.text.segment"
    }
  ],
  "task": "transcribe",
  "text": "太厉害了 真能上班没错 我觉得这个排版真的是让我这不很多朋友就神清气爽解放了",
  "usage": {
    "completion_tokens": 103,
    "input_audio_seconds": 6.5698125,
    "prompt_tokens": 170,
    "total_tokens": 273,
    "type": "duration"
  }
}
```

<p align="center">
  <small>© 2026 DMXAPI MOSS 音频 URL 转文字</small>
</p>
