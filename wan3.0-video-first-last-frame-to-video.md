# wan3.0-video 首尾帧生视频 API 使用文档

基于通义万相 3.0 视频生成模型的首尾帧生视频接口，通过 `/v1/responses` 端点以异步任务方式调用。同时指定首帧与尾帧两张图像，由模型补全中间的运动与转场过程，画面严格起止于给定图像；支持 480P / 720P / 1080P 三档分辨率、2~30 秒自定义时长与原生音频输出，适合表情/状态渐变、产品形态转换、场景过渡等需要精确控制起止画面的场景。

## 接口地址

| 接口 | 请求方式 | URL |
|------|---------|-----|
| 提交任务 | POST | `https://www.dmxapi.cn/v1/responses` |
| 获取结果 | POST | `https://www.dmxapi.cn/v1/responses` |


:::warning
请妥善保管您的 API Key！严禁将密钥泄露给他人、硬编码到代码中或提交到公开的代码仓库。如果怀疑密钥已泄露，请立即前往 DMXAPI 官网重新生成。
:::

## 模型名称

- `wan3.0-video`

## 首尾帧生视频 示例代码

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

# image_source = "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250925/wpimhv/rap.png"

# 【方式二】本地图片路径（代码自动转换为 Data URL）

image_source = "C:/path/input_image.png"

# ===============================================================
# 步骤4: 配置请求参数
# ===============================================================

payload = {
    # 【input】(object, 必填) 输入的基本信息
    # prompt 和 media 必填其一
    "input": {
        # 【media】(array[object], 条件必选) 媒体素材数组
        # 支持图像、视频、音频、文件和网页作为输入，和 prompt 必填其一
        # 数组中每个元素为一个媒体对象，包含 type 与 url 字段
        # 在参考生视频模式下，按照数组顺序定义 prompt 中素材引用的顺序
        # 图和视频分别计数，即可同时存在图1、视频1:
        #   - 第 1 个 reference_image 对应 图1，第 2 个对应 图2，以此类推
        #   - 第 1 个 reference_video 对应 视频1，第 2 个对应 视频2，以此类推
        #   - 第 1 个 reference_audio 对应 音频1，第 2 个对应 音频2，以此类推
        # 注意: reference_xx / file / link 类型和 first_frame / last_frame 类型互斥，
        # 不能在同一请求中混用
        "media": [
            {
                # 【type】(string, 必选) 媒体素材类型
                # 本示例取值 "first_frame"：首帧图像。最多 1 张，严格作为视频第一帧
                "type": "first_frame",
                # 【url】(string, 必选) 媒体素材 URL 或 Base64 编码数据
                # 图像 URL 或 Base64 编码数据。图像限制:
                #   - 格式: JPEG、JPG、PNG(不支持透明通道)、BMP、WEBP
                #   - 分辨率: 单边 [240, 8000] 像素
                #   - 长宽比: 不超过 8:1
                #   - 文件大小: 不超过 20MB
                # 支持公网 URL(HTTP / HTTPS)、OSS 协议临时 URL、Base64 编码字符串
                "url": image_source
            },
            {
                # 【type】(string, 必选) 媒体素材类型
                # 本示例取值 "last_frame"：尾帧图像。最多 1 张，严格作为视频最后一帧
                "type": "last_frame",
                # 【url】(string, 必选) 媒体素材 URL 或 Base64 编码数据
                # 图像 URL 或 Base64 编码数据。图像限制:
                #   - 格式: JPEG、JPG、PNG(不支持透明通道)、BMP、WEBP
                #   - 分辨率: 单边 [240, 8000] 像素
                #   - 长宽比: 不超过 8:1
                #   - 文件大小: 不超过 20MB
                # 支持公网 URL(HTTP / HTTPS)、OSS 协议临时 URL、Base64 编码字符串
                "url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260408/sjuytr/wan-r2v-object-girl.jpg"
            },
        ],
        # 【prompt】(string, 条件必选) 文本提示词，用来描述期望生成的视频内容
        # 和 media 必填其一
        # 支持中英文，每个汉字/字母占一个字符，不超过 20000 个字符，超过部分会自动截断
        # 在全能参考模式下，prompt 中可以用"图1""视频1""音频1"等指代 media 数组中
        # 对应顺序的媒体素材
        "prompt": "一个年轻女孩从微笑逐渐变为大笑，镜头缓缓推进，背景光线从冷色调渐变为暖色调。"
    },

    # 【model】(string, 必填) 调用的模型名称
    # wan3.0-video：标准版
    "model": "wan3.0-video",

    # 【parameters】(object, 可选) 视频处理参数
    "parameters": {
        # 【duration】(integer, 可选) 生成视频的时长，单位为秒
        # 默认值为 5
        #   - 无视频输入时: 取值范围为 [2, 30] 的整数
        #   - 有视频输入时: 输入视频总时长 + 输出视频时长不超过 30 秒
        #   - 传 -1 时: 智能时长模式，模型根据输入的 prompt、内容和富媒体自动推荐合适时长生成
        "duration": 5,
        # 【prompt_extend】(boolean, 可选) 是否开启 prompt 智能改写
        # 开启后使用大模型对输入 prompt 进行智能改写
        # 对于较短的 prompt 生成效果提升明显，但会增加耗时
        # 可选值: True(默认值，开启智能改写) / False(不开启智能改写)
        "prompt_extend": True,
        # 【ratio】(string, 可选) 生成视频的宽高比
        # 可选值:
        #   - "adaptive"(默认值，自适应长宽比，根据输入媒体比例和意图自动推荐合适的长宽比)
        #   - "16:9" / "4:3" / "1:1" / "3:4" / "9:16"
        "ratio": "adaptive",
        # 【resolution】(string, 可选) 生成视频的分辨率档位
        # 默认值为 1080P
        # 可选值: "1080P" / "720P" / "480P"
        "resolution": "480P",
        # 【audio】(boolean, 可选) 输出视频是否包含音频
        # 可选值:
        #   - True(默认值，输出视频包含声音)
        #   - False(输出视频不包含音轨)
        # 开关声音价格相同
        "audio": True,
        # 【seed】(integer, 可选) 随机种子，用于复现生成结果
        # 取值范围: [0, 2147483647]
        "seed": 0,
        # 【watermark】(boolean, 可选) 是否添加水印标识
        # 可选值: False(默认值，不添加水印) / True(添加水印)
        "watermark": False
    },
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

payload["input"]["media"][0]["url"] = _resolve_media(payload["input"]["media"][0]["url"], _MEDIA_RULES["rule_1"], "payload[\"input\"][\"media\"][0][\"url\"]")[0]

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

```json
{
  "output": [
    {
      "type": "message",
      "content": [
        {
          "type": "output_text",
          "text": "d912ed04-599a-4bed-bfda-90136f119691"
        }
      ]
    }
  ],
  "request_id": "c895c568-2f65-9b0d-ba81-c44bb233810a",
  "usage": {
    "input_tokens": 0,
    "input_tokens_details": {
      "cached_tokens": 0
    },
    "output_tokens": 15000,
    "output_tokens_details": {
      "reasoning_tokens": 0
    },
    "total_tokens": 15000
  }
}
```

返回中的 `task_id`（即 `output` 数组内的任务 ID 文本）用于第二步查询生成结果，`task_status` 为 `PENDING` 表示任务已排队等待处理。

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

    "model": "wan3.0-get",
    "input": "d912ed04-599a-4bed-bfda-90136f119691"

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

```json
{
  "output": [
    {
      "type": "message",
      "content": [
        {
          "type": "output_text",
          "text": "https://dashscope-a717.oss-accelerate.aliyuncs.com/1d/6e/20260828/e4b11e52/d912ed04-599a-4bed-bfda-90136f119691.mp4?Expires=1787974310&OSSAccessKeyId=LTAI5tPxpiCM2hjmWrFXrym1&Signature=K8wySou5GJXdAylTwMeb9uu0k5M%3D"
        }
      ]
    }
  ],
  "request_id": "ef82480d-20b2-9e95-b76e-d915dcdfe1f2",
  "usage": {
    "SR": 480,
    "duration": 5,
    "fps": 30,
    "input_tokens": 0,
    "input_tokens_details": {
      "cached_tokens": 0
    },
    "input_video_duration": 0,
    "output_tokens": 0,
    "output_tokens_details": {
      "reasoning_tokens": 0
    },
    "output_video_duration": 5,
    "ratio": "1632:937",
    "total_tokens": 0,
    "video_count": 1
  }
}
```

任务成功后 `output` 中返回视频的临时下载链接（有效期由 `Expires` 参数决定，请及时转存）；`usage` 中的 `SR` 为输出分辨率短边、`duration` / `output_video_duration` 为视频时长（秒）、`fps` 为帧率、`ratio` 为实际输出的宽高比、`video_count` 为生成视频数量。

<p align="center">
  <small>© 2026 DMXAPI wan3.0-video 首尾帧生视频</small>
</p>
