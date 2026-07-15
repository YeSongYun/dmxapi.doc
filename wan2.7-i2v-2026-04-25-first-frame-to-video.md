# wan2.7-i2v-2026-04-25 首帧生视频 API 使用文档

`wan2.7-i2v-2026-04-25` 是通义万相 2.7 系列的图生视频模型，通过 `/v1/responses` 端点以「提交任务 + 轮询查询」两步异步方式调用。以一张首帧图像为起点生成最长 15 秒、最高 1080P 的有声视频，并支持额外传入一段 2~30 秒的 wav/mp3 驱动音频，实现口型同步、动作卡点等音频驱动效果；未传入音频时模型将根据画面内容自动生成匹配的背景音乐或音效。首帧图像支持 JPEG/JPG/PNG/BMP/WEBP 格式，可通过公网 URL 或 Base64 编码传入，输出视频宽高比自动跟随首帧图像，适合让静态角色开口说话、演唱表演、图像动画化等场景。

## 接口地址

| 接口 | 请求方式 | URL |
|------|---------|-----|
| 提交任务 | POST | `https://www.dmxapi.cn/v1/responses` |
| 获取结果 | POST | `https://www.dmxapi.cn/v1/responses` |



:::warning
请妥善保管您的 API Key！严禁将密钥泄露给他人、硬编码到代码中或提交到公开的代码仓库。如果怀疑密钥已泄露，请立即前往 DMXAPI 官网重新生成。
:::

## 模型名称

- `wan2.7-i2v-2026-04-25`

## 首帧生视频 示例代码

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
    "model": "wan2.7-i2v-2026-04-25",

    # 【input】(object, 必填) 输入的基本信息，如提示词等
    "input": {
        # 【prompt】(string, 可选) 文本提示词，用来描述生成视频中期望包含的元素和视觉特点
        # 支持中英文，长度不超过 5000 个字符，每个汉字/字母占一个字符，超过部分会自动截断
        "prompt": "一幅都市奇幻艺术的场景。一个充满动感的涂鸦艺术角色。一个由喷漆所画成的少年，正从一面混凝土墙上活过来。他一边用极快的语速演唱一首英文rap，一边摆着一个经典的、充满活力的说唱歌手姿势。场景设定在夜晚一个充满都市感的铁路桥下。灯光来自一盏孤零零的街灯，营造出电影般的氛围，充满高能量和惊人的细节。视频的音频部分完全由rap构成，没有其他对话或杂音。",

        # 【media】(array, 必填) 媒体素材列表，用于指定视频生成所需的参考素材（图像、音频和视频）
        # 数组的每个元素为一个媒体对象，包含 type 与 url 字段
        # 首帧生视频仅支持以下素材组合，非法组合将报错:
        #   - 首帧: first_frame
        #   - 首帧+音频: first_frame + driving_audio
        # 每种 type 在 media 数组中最多出现一次（例如不可同时传入两个 first_frame）
        "media": [
            {
                # 【media[].type】(string, 必填) 媒体素材类型，此处为 "first_frame"(首帧)
                "type": "first_frame",
                # 【media[].url】(string, 必填) 首帧图像 URL 或 Base64 编码数据
                # 图像限制:
                #   - 格式: JPEG、JPG、PNG（不支持透明通道）、BMP、WEBP
                #   - 分辨率: 宽和高的范围为 [240, 8000] 像素
                #   - 宽高比: 1:8 ~ 8:1
                #   - 文件大小: 不超过 20MB
                # 支持公网 URL (HTTP/HTTPS)、OSS 临时 URL 或 Base64 编码
                # (数据格式 data:{MIME_type};base64,{base64_data})
                "url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250925/wpimhv/rap.png"
            },
            {
                # 【media[].type】(string, 必填) 媒体素材类型，此处为 "driving_audio"(驱动音频)
                "type": "driving_audio",
                # 【media[].url】(string, 必填) 音频文件的 URL
                # 传入音频: 模型将以该音频为驱动源生成视频（如口型同步、动作卡点等）
                # 未传入音频: 模型将根据视频画面内容，自动生成匹配的背景音乐或音效
                # 音频限制: 格式 wav/mp3；时长 2~30s；文件大小不超过 15MB
                # 截断处理: 若音频长度超过 duration 值（如 5 秒），自动截取前 5 秒，其余部分丢弃
                #           若音频长度不足视频时长，超出音频长度部分为无声视频
                "url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250925/ozwpvi/rap.mp3"
            }
        ]
    },

    # 【parameters】(object, 可选) 视频处理参数，如设置视频分辨率、设置视频时长、开启 prompt 智能改写、添加水印等
    "parameters": {
        # 【resolution】(string, 可选) 生成视频的分辨率档位，用于控制视频的清晰度（总像素）
        # 可选值: "720P" / "1080P"(默认值)
        # 模型根据选择的分辨率档位，自动缩放至相近总像素，视频宽高比尽量与输入素材（首帧或首段视频）保持一致
        # 注意: resolution 直接影响费用，请在调用前确认模型价格
        "resolution": "720P",

        # 【duration】(integer, 可选) 生成视频的时长，单位为秒
        # 取值范围: [2, 15] 之间的整数，默认值为 5
        # 注意: duration 直接影响费用，按秒计费，请在调用前确认模型价格
        "duration": 5,

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
        "seed": 43
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
payload["input"]["media"][0]["url"] = resolve_media(payload["input"]["media"][0]["url"])

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
  "request_id": "49a9ce7a-da55-918e-a0e8-419292b10509",
  "output": [
    {
      "type": "message",
      "content": [
        {
          "type": "output_text",
          "text": "{\"task_id\":\"7fb57497-4657-4a10-a94a-c40bd3077c47\",\"task_status\":\"PENDING\"}"
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
    "input": "7fb57497-4657-4a10-a94a-c40bd3077c47"

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
  "request_id": "592f0492-8d99-940b-826d-012bcfc92810",
  "output": [
    {
      "type": "message",
      "content": [
        {
          "type": "output_text",
          "text": "{\"task_id\":\"7fb57497-4657-4a10-a94a-c40bd3077c47\",\"task_status\":\"SUCCEEDED\",\"submit_time\":\"2026-07-14 16:43:28.681\",\"scheduled_time\":\"2026-07-14 16:43:28.711\",\"end_time\":\"2026-07-14 16:44:03.621\",\"orig_prompt\":\"一幅都市奇幻艺术的场景。一个充满动感的涂鸦艺术角色。一个由喷漆所画成的少年，正从一面混凝土墙上活过来。他一边用极快的语速演唱一首英文rap，一边摆着一个经典的、充满活力的说唱歌手姿势。场景设定在夜晚一个充满都市感的铁路桥下。灯光来自一盏孤零零的街灯，营造出电影般的氛围，充满高能量和惊人的细节。视频的音频部分完全由rap构成，没有其他对话或杂音。\",\"video_url\":\"https://dashscope-a717.oss-accelerate.aliyuncs.com/1d/f1/20260714/fa14b052/53344835-metadata_user_8999cf672ecdb780_watermark.mp4?Expires=1784105042&OSSAccessKeyId=LTAI5tJjG6wsHad1Sf7iezX4&Signature=ezciNJj1kNz0gZwtGcYxgpPFpHM%3D\"}"
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
  <small>© 2026 DMXAPI wan2.7-i2v-2026-04-25 首帧生视频</small>
</p>
