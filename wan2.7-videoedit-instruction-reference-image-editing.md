# wan2.7-videoedit 指令+参考图编辑(局部替换) API 使用文档

`wan2.7-videoedit` 是通义万相 2.7 系列的视频编辑模型，通过 `/v1/responses` 端点以「提交任务 + 轮询查询」两步异步方式调用。本文档演示指令+参考图编辑用法：传入一段 2~10 秒的 mp4/mov 待编辑视频，搭配最多 4 张参考图像与一句自然语言指令（如"将视频中女孩的衣服替换为图片中的衣服"），即可按参考图完成服饰替换、物体置换等局部编辑，画面其余部分保持原样。输出最高 1080P、支持 5 种宽高比（16:9/9:16/1:1/4:3/3:4，不传则跟随输入视频），audio_setting 参数可在模型智能配音（auto）与强制保留原声（origin）之间切换，适合电商换装展示、素材二创、广告物料快速改版等场景。

## 接口地址

| 接口 | 请求方式 | URL |
|------|---------|-----|
| 提交任务 | POST | `https://www.dmxapi.cn/v1/responses` |
| 获取结果 | POST | `https://www.dmxapi.cn/v1/responses` |



:::warning
请妥善保管您的 API Key！严禁将密钥泄露给他人、硬编码到代码中或提交到公开的代码仓库。如果怀疑密钥已泄露，请立即前往 DMXAPI 官网重新生成。
:::

## 模型名称

- `wan2.7-videoedit`

## 指令+参考图编辑(局部替换) 示例代码

```python
import base64
import os

import requests
import json

# ===============================================================
# 步骤1: 配置 API 连接信息
# ===============================================================

# DMXAPI 服务端点地址
url = "https://www.dmxapi.cn/v1/responses"

# DMXAPI 密钥 (请替换为您自己的密钥)
# 获取方式: 登录 DMXAPI 官网 -> 个人中心 -> API 密钥管理
api_key = "sk-******************************************"

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
    # 【model】(string, 必填) 调用的模型名称
    "model": "wan2.7-videoedit",

    # 【input】(object, 必填) 输入的基本信息，如提示词等
    "input": {
        # 【prompt】(string, 可选) 文本提示词，用来描述生成视频中期望包含的元素和视觉特点
        # 支持中英文，每个汉字/字母占一个字符，长度不超过 5000 个字符，超过部分会自动截断
        "prompt": "将视频中女孩的衣服替换为图片中的衣服",

        # 【negative_prompt】(string, 可选) 反向提示词，用来描述不希望在视频画面中出现的内容，可以对视频画面进行限制
        # 支持中英文，长度不超过 500 个字符，超过部分会自动截断
        "negative_prompt": "汽车",

        # 【media】(array, 必填) 媒体素材列表，用于指定视频生成所需的参考素材（图像、视频）
        # 数组的每个元素为一个媒体对象，包含 type 与 url 字段
        # 素材限制: 视频有且仅有 1 个；参考图像最多传入 4 张
        "media": [
            {
                # 【media[].type】(string, 必填) 媒体素材类型
                # 可选值: "video"(必传，待编辑的视频) / "reference_image"(可选，参考图像)
                "type": "video",
                # 【media[].url】(string, 必填) 待编辑的视频文件的 URL
                # 视频限制:
                #   - 格式: mp4、mov
                #   - 时长: 2~10s
                #   - 分辨率: 宽度和高度范围为 [240, 4096] 像素
                #   - 宽高比: 1:8 ~ 8:1
                #   - 文件大小: 不超过 100MB
                # 支持公网 URL (HTTP/HTTPS) 或 OSS 临时 URL
                "url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260403/nlspwm/T2VA_22.mp4"
            },
            {
                # 参考图像 (type=reference_image)
                "type": "reference_image",
                # 【media[].url】(string, 必填) 参考图像 URL 或 Base64 编码数据
                # 图像限制:
                #   - 格式: JPEG、JPG、PNG（不支持透明通道）、BMP、WEBP
                #   - 分辨率: 宽度和高度范围为 [240, 8000] 像素
                #   - 宽高比: 1:8 ~ 8:1
                #   - 文件大小: 不超过 20MB
                # 支持公网 URL (HTTP/HTTPS)、OSS 临时 URL 或 Base64 编码
                # (数据格式 data:{MIME_type};base64,{base64_data})
                "url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260402/fwjpqf/wan2.7-videoedit-change-clothes.png"
            }
        ]
    },

    # 【parameters】(object, 可选) 视频处理参数，如设置视频分辨率、设置视频时长、开启 prompt 智能改写、添加水印等
    "parameters": {
        # 【resolution】(string, 可选) 生成视频的分辨率档位，用于控制视频的清晰度（总像素）
        # 可选值: "720P" / "1080P"(默认值)
        "resolution": "720P",

        # 【ratio】(string, 可选) 生成视频的宽高比
        # 可选值: "16:9" / "9:16" / "1:1" / "4:3" / "3:4"
        # 生效逻辑:
        #   - 不传 ratio 参数: 以输入视频的宽高比生成近似比例的视频
        #   - 传入 ratio 参数: 按指定的 ratio 生成视频
        # 输出视频分辨率（宽*高）对照:
        #   - 720P 档位: 16:9=1280*720 / 9:16=720*1280 / 1:1=960*960 / 4:3=1104*832 / 3:4=832*1104
        #   - 1080P 档位: 16:9=1920*1080 / 9:16=1080*1920 / 1:1=1440*1440 / 4:3=1648*1248 / 3:4=1248*1648
        "ratio": "16:9",

        # 【duration】(integer, 可选) 生成视频的时长，单位为秒
        # 使用建议: 此参数仅在需要"截断视频"时才需配置；如果希望输出视频与输入视频时长一致，
        #           无需设置（或传入默认值 0）
        # 使用规则:
        #   - 默认行为: 默认值为 0，代表直接使用输入视频的时长，不进行截断
        #   - 截断生效: 当传入指定时长时，系统会从原视频的 0 秒起，截取至 duration 设置的长度
        #   - 取值范围: 支持 [2, 10] 之间的整数
        "duration": 5,

        # 【audio_setting】(string, 可选) 视频声音设置
        # 可选值:
        #   - "auto"(默认): 模型根据 prompt 内容智能判断，若提示词涉及声音描述，
        #     可能重新生成音频；否则可能保留输入素材的原声
        #   - "origin": 强制保留输入视频的原声，不重新生成
        "audio_setting": "auto",

        # 【prompt_extend】(boolean, 可选) 是否开启 prompt 智能改写，开启后使用大模型对输入 prompt 进行智能改写
        # 对于较短的 prompt 生成效果提升明显，但会增加耗时
        # 可选值: True(默认值，开启智能改写) / False(不开启智能改写)
        "prompt_extend": True,

        # 【watermark】(boolean, 可选) 是否添加水印标识，水印位于视频右下角，文案固定为"AI生成"
        # 可选值: False(默认值，不添加水印) / True(添加水印)
        "watermark": True,

        # 【seed】(integer, 可选) 随机数种子，取值范围为 [0, 2147483647]
        # 未指定时，系统自动生成随机种子；若需提升生成结果的可复现性，建议固定 seed 值
        # 由于模型生成具有概率性，即使使用相同 seed，也不能保证每次生成结果完全一致
        "seed": 23
    }
}

# ===============================================================
# 步骤4: 媒体输入处理
# ===============================================================
# - 公网 URL (http/https): 原样传入
# - 本地文件路径: 自动读取并转为 data:{MIME_type};base64,{base64_data}

_MIME_MAP = {
    ".bmp": "image/bmp",
    ".gif": "image/gif",
    ".jpeg": "image/jpeg",
    ".jpg": "image/jpeg",
    ".png": "image/png",
    ".webp": "image/webp",
}

def _file_to_data_uri(path: str) -> str:
    ext = os.path.splitext(path)[1].lower()
    mime = _MIME_MAP.get(ext)
    if mime is None:
        raise ValueError(f"不支持的文件格式 {ext}: {path}")
    with open(path, "rb") as f:
        data = base64.b64encode(f.read()).decode("ascii")
    return f"data:{mime};base64,{data}"

def resolve_media(path_or_url: str) -> str:
    """公网 URL 原样返回; 本地文件转 base64 data URI; 其他一律报错。"""
    if path_or_url.startswith(("http://", "https://")):
        return path_or_url
    if path_or_url.startswith("data:"):
        return path_or_url
    if os.path.isfile(path_or_url):
        return _file_to_data_uri(path_or_url)
    raise ValueError(f"无法识别的输入（不是公网 URL，本地文件也不存在）: {path_or_url}")

# 图片：可填公网 URL 或本地文件路径（如 r"C:\文件\示例.bmp"）
payload["input"]["media"][1]["url"] = resolve_media(payload["input"]["media"][1]["url"])

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
  "request_id": "2db35de0-7261-9c77-9bf1-69c9d723052b",
  "output": [
    {
      "type": "message",
      "content": [
        {
          "type": "output_text",
          "text": "{\"task_id\":\"4eb60e23-3b4a-4d7a-8f7b-791d593db8b8\",\"task_status\":\"PENDING\"}"
        }
      ]
    }
  ],
  "usage": {
    "input_tokens": 0,
    "input_tokens_details": {
      "cached_tokens": 0
    },
    "output_tokens": 30000,
    "output_tokens_details": {
      "reasoning_tokens": 0
    },
    "total_tokens": 30000
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
   本脚本通过任务 ID 查询视频生成任务的状态与结果
   任务状态: PENDING(排队中) / RUNNING(处理中) / SUCCEEDED(成功)
             FAILED(失败) / CANCELED(已取消) / UNKNOWN(任务不存在或状态未知)

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
api_key = "sk-******************************************"

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

    "model": "wan2.7-get",
    "input": "4eb60e23-3b4a-4d7a-8f7b-791d593db8b8"

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
  "request_id": "9b91e8dd-b506-94ea-bb11-fa3e6508c67e",
  "output": [
    {
      "type": "message",
      "content": [
        {
          "type": "output_text",
          "text": "{\"task_id\":\"4eb60e23-3b4a-4d7a-8f7b-791d593db8b8\",\"task_status\":\"SUCCEEDED\",\"submit_time\":\"2026-07-14 17:18:31.634\",\"scheduled_time\":\"2026-07-14 17:18:31.656\",\"end_time\":\"2026-07-14 17:23:56.030\",\"orig_prompt\":\"将视频中女孩的衣服替换为图片中的衣服\",\"video_url\":\"https://dashscope-a717.oss-accelerate.aliyuncs.com/1d/ce/20260714/d10f54ed/3716466-metadata_user_5c38a4a3924ae79a_watermark.mp4?Expires=1784107434&OSSAccessKeyId=LTAI5tJjG6wsHad1Sf7iezX4&Signature=TWjy4mzB6UpfRKVtqL8XHkG%2FptI%3D\"}"
        }
      ]
    }
  ],
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

<p align="center">
  <small>© 2026 DMXAPI wan2.7-videoedit 指令+参考图编辑(局部替换)</small>
</p>
