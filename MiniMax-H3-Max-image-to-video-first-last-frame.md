# MiniMax-H3-Max 图生视频（首帧 - 尾帧）API 使用文档

基于 MiniMax H3 系列极速生成版本 MiniMax-H3-Max 的图生视频接口，通过 `/v1/responses` 端点以异步任务方式调用。以文本提示词搭配首帧（`first_frame`）和／或尾帧（`last_frame`）图片驱动生成 5~15 秒视频，宽高比由输入图片自适应决定，支持 480P / 768P 两档分辨率（默认 768P）；输入图片支持 JPG、JPEG、PNG、WEBP、HEIC、HEIF 六种格式，单张 ≤ 30 MB、边长 [256, 5760] px、长宽比 [0.4, 2.5]，首帧与尾帧各限 1 张，可传公网 URL、平台文件 ID 或 Data URI。本示例演示「文本 + 首帧图」的单图驱动场景，适合商品动效、静态海报转视频、角色动画等需要以既有画面为锚点的创作。

## 接口地址

| 接口 | 请求方式 | URL |
|------|---------|-----|
| 提交任务 | POST | `https://www.dmxapi.cn/v1/responses` |
| 获取结果 | POST | `https://www.dmxapi.cn/v1/responses` |



:::warning
请妥善保管您的 API Key！严禁将密钥泄露给他人、硬编码到代码中或提交到公开的代码仓库。如果怀疑密钥已泄露，请立即前往 DMXAPI 官网重新生成。
:::

## 模型名称

- `MiniMax-H3-Max`

## 图生视频（首帧 - 尾帧） 示例代码

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
# 步骤3: 配置图片来源（选择一种即可）
# ===============================================================

# 【方式一】网络图片 URL（支持 HTTP / HTTPS 协议）
# image_source = "https://cdn.hailuoai.com/prod/hailuo_demo/testsets/H3_AA_I2VA/gallery/sr_v17_variants_seed42_43_20260724/inputs/4a3a90bf9100_KDmcbkhzYo5sjjxr9FqcVmWVnzb.png"

# 【方式二】本地图片路径（代码自动转换为 Data URL）
image_source = "C:/path/input_image.png"

# 限制：本地图片不超过 30 MiB

# ===============================================================
# 步骤4: 配置请求参数
# ===============================================================

payload = {
    # 【model】(string, 必填) 调用的模型名称
    # MiniMax-H3-Max 为极速生成版本，支持文生视频与图生视频（首帧 / 尾帧）
    # 不支持中间帧，也不支持多模态参考（参考图 / 参考视频 / 参考音频）
    "model": "MiniMax-H3-Max",

    # 【input】(object, 必填) 输入对象，包含多模态内容数组与视频生成参数
    "input": {
        # 【content】(array[object], 必填) 多模态输入内容数组，描述用于生成视频的信息
        # 每个元素通过 type 区分类型（text / image_url / video_url / audio_url），并通过 role 标注用途
        # 每次请求必须包含一个非空 text 项（提示词必填），缺失会返回参数错误
        # 图生视频支持的输入组合：
        #   - 首帧:   text + 1 张 image_url（role=first_frame 或不填）
        #   - 尾帧:   text + 1 张 image_url（role=last_frame）
        #   - 首尾帧: text + 2 张 image_url（role 分别为 first_frame、last_frame）
        # 请求体总大小 ≤ 64 MB，大文件请用公网 URL，勿用 Base64
        "content": [
            {
                # 【type】(string, 必填) 输入内容的类型
                # 可选值: "text"(文本) / "image_url"(图片) / "video_url"(视频) / "audio_url"(音频)
                "type": "text",

                # 【text】(string, 必填) 文本提示词，描述期望生成的视频内容
                # 所有场景都需包含一个非空 text
                # 长度按字符数计算，单个 text 最多 7000 个字符
                "text": "Pull focus to the people in the background and add more steam to the ramen bowl."
            },
            {
                # 【type】(string, 必填) 输入内容的类型，此处为图片
                "type": "image_url",

                # 【image_url】(object, 条件必填) 当 type=image_url 时的图片对象
                "image_url": {
                    # 【url】(string, 必填) 图片地址，支持三种形式:
                    #   - 公网 URL
                    #   - mm_file://{file_id}（引用平台已有文件，如上传或历史产物的 file_id）
                    #   - data:image/<格式>;base64,<Base64> 形式的 Data URI（<格式> 小写）
                    # 图片限制:
                    #   - 格式: JPG、JPEG、PNG、WEBP、HEIC、HEIF
                    #   - 单文件大小: ≤ 30 MB
                    #   - 宽高范围: [256, 5760] px
                    #   - 长宽比（宽/高）: [0.4, 2.5]
                    #   - 数量: 首帧 ≤ 1、尾帧 ≤ 1
                    "url": image_source
                },

                # 【role】(string, 条件必填) 内容的位置或用途
                # 可选值:
                #   - "first_frame"(首帧图片；仅一张图且不填 role 时默认按 first_frame 处理)
                #   - "last_frame"(尾帧图片，需与 first_frame 成对使用)
                "role": "first_frame"
            }
        ],

        # 【resolution】(string, 必填) 视频分辨率
        # 可选值:
        #   - "480P"
        #   - "768P"(默认值)
        # 本模型不支持 2K 档位
        "resolution": "768P",

        # 【duration】(integer, 必填) 生成视频时长（秒），整数
        # 取值范围: 5~15，本模型不支持 4 秒
        "duration": 5,

        # 【ratio】(string, 可选) 生成视频的宽高比
        # 图生视频场景下宽高比由输入图片决定，ratio 恒为 "adaptive"
        # 传入其他合理值不会报错，但会被忽略并按 adaptive 处理
        # 实际生成比例可在获取结果接口的 ratio 字段中查看
        "ratio": "adaptive",

        # 【aigc_watermark】(boolean, 可选) 是否在生成视频中添加 AIGC 标识水印
        # 默认值: false
        "aigc_watermark": False
    }
}

# 媒体处理逻辑（无需修改）

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
            ".webp": "image/webp",
            ".heic": "image/heic",
            ".heif": "image/heif",
        },
        "data_types": ["image/heic", "image/heif", "image/jpeg", "image/jpg", "image/png", "image/webp"],
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


payload["input"]["content"][1]["image_url"]["url"] = _resolve_media(payload["input"]["content"][1]["image_url"]["url"], _MEDIA_RULES["rule_1"], "payload[\"input\"][\"content\"][1][\"image_url\"][\"url\"]")[0]

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

## 返回示例

提交成功后，`output[0].content[0].text` 即为任务 ID，用于第二步查询结果。

```json
{
  "output": [
    {
      "type": "message",
      "content": [
        {
          "type": "output_text",
          "text": "436678737211692"
        }
      ]
    }
  ],
  "usage": {
    "input_tokens": 0,
    "input_tokens_details": {
      "cached_tokens": 0
    },
    "output_tokens": 25000,
    "output_tokens_details": {
      "reasoning_tokens": 0
    },
    "total_tokens": 25000
  }
}
```

## 获取生成视频 示例代码

```python
"""
╔═══════════════════════════════════════════════════════════════╗
║                  DMXAPI 自研接口                               ║
╚═══════════════════════════════════════════════════════════════╝

📝 功能说明:
   本脚本演示如何使用 requests 库调用 DMXAPI 的自研接口

═══════════════════════════════════════════════════════════════
"""

import requests
import json

# ═══════════════════════════════════════════════════════════════
# 🔑 步骤1: 配置 API 连接信息
# ═══════════════════════════════════════════════════════════════

# 🌐 DMXAPI 服务端点地址
url = "https://www.dmxapi.cn/v1/responses"

# 🔐 DMXAPI 密钥 (请替换为您自己的密钥)
# 获取方式: 登录 DMXAPI 官网 -> 个人中心 -> API 密钥管理
api_key = "sk-***********************************************"

# ═══════════════════════════════════════════════════════════════
# 📋 步骤2: 配置请求头
# ═══════════════════════════════════════════════════════════════

headers = {
    "Content-Type": "application/json",      # 指定请求体为 JSON 格式
    "Authorization": f"{api_key}",    # token 认证方式
}

# ═══════════════════════════════════════════════════════════════
# 💬 步骤3: 配置请求参数
# ═══════════════════════════════════════════════════════════════

payload = {

    "model": "MiniMax-H3-get",
    "input": "436678737211692"

}


# ═══════════════════════════════════════════════════════════════
# 📤 步骤4: 发送请求并输出结果
# ═══════════════════════════════════════════════════════════════

# 发送 POST 请求到 API 服务器
response = requests.post(url, headers=headers, json=payload)

# 格式化输出 JSON 响应
# - indent=2: 缩进 2 空格，便于阅读
# - ensure_ascii=False: 正确显示中文字符
print(json.dumps(response.json(), indent=2, ensure_ascii=False))


```

## 返回示例

`task.status` 为任务状态，取值 `queued`（排队中）、`running`（运行中）、`succeeded`（成功）、`failed`（失败）、`cancelled`（已取消）；状态为 `succeeded` 时，`task.content.url` 即为视频下载地址。

```json
{
  "task": {
    "id": "436678737211692",
    "model": "MiniMax-H3-Max",
    "status": "succeeded",
    "created_at": 1788164487,
    "updated_at": 1788164505,
    "content": {
      "url": "https://algeng-video-infer.oss-cn-shanghai.aliyuncs.com/h3-480p%2F2026%2F08%2F31%2Ffal%2F436678737211692-1-6677cc5c0eb2b2cc.mp4?Expires=1788250910&OSSAccessKeyId=LTAI5tA8yjKg7HvBRDpzZ8Nk&Signature=kyfs2uZGvSP%2FKbXCg76s8pFehGQ%3D"
    },
    "resolution": "768P",
    "duration": 5,
    "usage": {
      "total_seconds": 5,
      "input_seconds": 0,
      "output_seconds": 5,
      "input_image_count": 1
    },
    "ratio": "adaptive",
    "task_type": "generation"
  },
  "usage": {
    "total_tokens": 0,
    "input_tokens": 0,
    "input_tokens_details": {
      "cached_tokens": 0
    },
    "output_tokens": 0,
    "output_tokens_details": {
      "reasoning_tokens": 0
    }
  }
}
```

<p align="center">
  <small>© 2026 DMXAPI MiniMax-H3-Max 图生视频（首帧 - 尾帧）</small>
</p>
