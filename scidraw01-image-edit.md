# scidraw01 图片编辑 API 使用文档

基于 SciDraw scidraw01 模型的科研绘图图片编辑接口，通过 DMXAPI 代理的 `/v1/responses` 端点以异步任务方式调用。提交阶段在 `input` 对象中同时传入一张源图（`image`，支持公网 URL 或本地图片自动转换的 Data URL）和一条自然语言编辑指令（`prompt`），并可通过 `resolution`、`count` 控制输出分辨率与张数；提交后立即返回状态为 `queued` 的任务对象，再以 `scidraw-get` 携带任务 ID 查询，任务成功后从 `data.result.files[].url`（或 `output[0].result`）读取编辑后图片的下载地址。

## 接口地址

| 接口 | 请求方式 | URL |
|------|---------|-----|
| 提交任务 | POST | `https://www.dmxapi.cn/v1/responses` |
| 获取结果 | POST | `https://www.dmxapi.cn/v1/responses` |

:::warning
请妥善保管您的 API Key！严禁将密钥泄露给他人、硬编码到代码中或提交到公开的代码仓库。如果怀疑密钥已泄露，请立即前往 DMXAPI 官网重新生成。
:::

## 模型名称

- 提交任务：`scidraw01`
- 获取结果：`scidraw-get`

## 图片编辑 示例代码

```python
import requests
import json
import base64
import binascii
import os

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
# 步骤3: 配置图片来源 (选择一种即可)
# ===============================================================

# 【方式一】网络图片 URL (支持 HTTP / HTTPS 协议)
# image_source = "https://example.com/image.png"

# 【方式二】本地图片路径 (代码自动转换为 Data URL)
image_source = "C:/path/to/input_image.png"

#   对源图的限制:
#   - 格式:          PNG、JPEG、WebP (服务端按文件签名检测，不信任声明的 MIME)
#   - 文件大小:      <= 10 MiB
#   - 解码后像素:    <= 4000 万像素
# 图片无效、过大或不安全时返回 400 INVALID_REQUEST

# ===============================================================
# 步骤4: 配置请求参数
# ===============================================================

payload = {
    # 【model】(string, 必填) 调用的模型名称
    "model": "scidraw01",

    # 【input】(object, 必填) 输入信息
    "input": {
        # 【count】(integer, 可选) 生成结果的数量
        #  默认值为 1，取值范围: 1~4
        "count": 1,

        # 【image】(string, 必填) 待编辑的源图
        # 支持公网 URL，或 "data:image/<格式>;base64,<Base64>" 形式的 Data URL
        # 本地文件路径由下方媒体处理逻辑自动转换为 Data URL
        "image": image_source,

        # 【prompt】(string, 必填) 自然语言编辑指令
        #  长度须在 5~2000 字符之间
        "prompt": "在猫的头上加一个具有黄金比例的图形",

        # 【resolution】(string, 可选) 输出图片的分辨率
        #  默认值为 "2K"，可选值: "2K" / "4K"
        "resolution": "2K"
    }
}

# 媒体处理逻辑 (无需修改)

_MEDIA_RULES = {
    "rule_1": {
        "allow_url": True,
        "allow_data_uri": True,
        "allow_raw_base64": False,
        "allow_asset": False,
        "allow_local_file": True,
        "local_encoding": "data_uri",
        "file_formats": {
            ".jpg": "image/jpeg",
            ".jpeg": "image/jpeg",
            ".png": "image/png",
            ".bmp": "image/bmp",
            ".webp": "image/webp",
            ".gif": "image/gif",
            ".heic": "image/heic",
            ".heif": "image/heif",
        },
        "data_types": ["image/bmp", "image/gif", "image/heic", "image/heif", "image/jpeg", "image/png", "image/webp"],
    },
}


def _resolve_media(value: str, rule: dict, field: str) -> tuple:
    if not isinstance(value, str) or not value:
        raise ValueError(f"{field} 必须是非空字符串")
    if value.startswith(("http://", "https://")):
        if rule["allow_url"]:
            return value, "url"
        raise ValueError(f"{field} 不接受 URL")
    if value.startswith("data:"):
        if not rule["allow_data_uri"]:
            raise ValueError(f"{field} 不接受 Data URI")
        header, sep, encoded = value.partition(",")
        expected = {f"data:{media_type};base64" for media_type in rule["data_types"]}
        if not sep or header not in expected or not encoded:
            raise ValueError(f"{field} 的 Data URI 头无效；允许: {sorted(expected)}")
        try:
            base64.b64decode(encoded, validate=True)
        except (binascii.Error, ValueError):
            raise ValueError(f"{field} 的 Data URI 正文不是合法 Base64")
        return value, "data_uri"
    if value.lower().startswith("asset://"):
        if rule["allow_asset"] and len(value) > len("asset://"):
            return value, "asset"
        raise ValueError(f"{field} 不接受素材 ID，或素材 ID 为空")
    if os.path.isfile(value):
        if not rule["allow_local_file"]:
            raise ValueError(f"{field} 不接受本地文件")
        ext = os.path.splitext(value)[1].lower()
        if ext not in rule["file_formats"]:
            raise ValueError(f"{field} 不支持本地文件格式 {ext}；允许: {sorted(rule['file_formats'])}")
        with open(value, "rb") as f:
            encoded = base64.b64encode(f.read()).decode("ascii")
        if rule["local_encoding"] == "raw_base64":
            return encoded, "raw_base64"
        media_type = rule["file_formats"][ext]
        return f"data:{media_type};base64,{encoded}", "data_uri"
    if rule["allow_raw_base64"]:
        try:
            base64.b64decode(value, validate=True)
            return value, "raw_base64"
        except (binascii.Error, ValueError):
            pass
    raise ValueError(f"{field} 不符合接口媒体契约")


payload["input"]["image"] = _resolve_media(payload["input"]["image"], _MEDIA_RULES["rule_1"], "payload[\"input\"][\"image\"]")[0]

# ===============================================================
# 步骤5: 发送请求并输出结果
# ===============================================================

# 发送 POST 请求到 API 服务器
response = requests.post(url, headers=headers, json=payload)

# 格式化输出 JSON 响应
# - indent=2: 缩进 2 空格，便于阅读
# - ensure_ascii=False: 正确显示中文字符
print(json.dumps(response.json(), indent=2, ensure_ascii=False))
```

## 提交任务返回示例

```json
{
  "data": {
    "id": "job_7b4d2e9f1c6a4d3fb8e5a2c0d9f1b7e3",
    "object": "image_job",
    "type": "image_edit",
    "status": "queued",
    "created_at": "2026-09-09T06:48:40.495Z",
    "completed_at": null,
    "credits_reserved": 10,
    "credits_consumed": 0,
    "result": null,
    "error": null
  },
  "output": [
    {
      "content": [
        {
          "text": "id: job_7b4d2e9f1c6a4d3fb8e5a2c0d9f1b7e3",
          "type": "output_text"
        },
        {
          "text": "status: queued",
          "type": "output_text"
        }
      ],
      "role": "assistant",
      "status": "completed",
      "type": "message"
    }
  ],
  "success": true,
  "usage": {
    "input_tokens": 0,
    "input_tokens_details": {
      "cached_tokens": 0
    },
    "output_tokens": 70000,
    "output_tokens_details": {
      "reasoning_tokens": 0
    },
    "total_tokens": 70000
  }
}
```

> `data.id` 的值即为任务 ID，用于后续查询任务状态与结果。按上游官方文档，`data.status` 可能为 `queued`（已接受，等待执行）、`processing`（正在处理）、`succeeded`（可读取 `result.files`）、`failed`（`error` 中包含错误码与文案）、`canceled`（任务不会继续运行），终态不会再次变化。

## 获取图片结果 示例代码

```python
import requests
import json

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
    # 【input】(string, 必填) 提交任务时返回的任务 ID (data.id)
    "input": "job_7b4d2e9f1c6a4d3fb8e5a2c0d9f1b7e3",

    # 【model】(string, 必填) 查询结果固定使用 "scidraw-get"
    "model": "scidraw-get"
}

# ===============================================================
# 步骤4: 发送请求并输出结果
# ===============================================================

# 发送 POST 请求到 API 服务器
response = requests.post(url, headers=headers, json=payload)

# 格式化输出 JSON 响应
# - indent=2: 缩进 2 空格，便于阅读
# - ensure_ascii=False: 正确显示中文字符
print(json.dumps(response.json(), indent=2, ensure_ascii=False))
```

## 获取结果返回示例

```json
{
  "data": {
    "id": "job_7b4d2e9f1c6a4d3fb8e5a2c0d9f1b7e3",
    "object": "image_job",
    "type": "image_edit",
    "status": "succeeded",
    "created_at": "2026-09-09T06:48:40.495Z",
    "completed_at": "2026-09-09T06:48:58.620Z",
    "credits_reserved": 10,
    "credits_consumed": 10,
    "result": {
      "files": [
        {
          "id": "file_2c9a5e1d7f3b4a8cb6d0e4f2a1c7b9d5",
          "url": "https://your-cdn.example.com/edited-image.jpeg",
          "format": "jpeg",
          "mime_type": "image/jpeg"
        }
      ]
    },
    "error": null
  },
  "output": [
    {
      "result": "https://your-cdn.example.com/edited-image.jpeg",
      "type": "image_generation_call"
    }
  ],
  "success": true,
  "usage": {
    "input_tokens": 0,
    "input_tokens_details": {
      "cached_tokens": 0
    },
    "output_tokens": 0,
    "output_tokens_details": {
      "reasoning_tokens": 0
    },
    "total_tokens": 0
  }
}
```

> 任务成功后，`data.result.files[].url` 与 `output[0].result` 均为编辑后图片的下载地址，`format` / `mime_type` 标明文件格式。

<p align="center">
  <small>© 2026 DMXAPI scidraw01 图片编辑</small>
</p>
