# MiniMax-H3 图生视频 API 使用文档

MiniMax-H3 视频生成 V2 接口，通过多模态 `content` 数组输入（文本 / 图片 / 视频 / 音频）驱动，2K 直出。图生视频场景在必填文本提示词之外附加图片项，通过 `role` 指定用途：`first_frame` 首帧、`last_frame` 尾帧，或两者成对构成首尾帧生成；首帧与尾帧各限 1 张，图片支持 JPG、JPEG、PNG、WEBP、HEIC、HEIF 六种格式，单文件 ≤ 30 MB、宽高 [256, 5760] px、长宽比 [0.4, 2.5]。图生视频场景下宽高比由输入图片决定，`ratio` 恒为 `adaptive`。接口以异步任务方式工作：提交后返回任务 ID，再用查询模型换取最终视频地址。

## 接口地址

| 接口 | 请求方式 | URL |
|------|---------|-----|
| 提交任务 | POST | `https://www.dmxapi.cn/v1/responses` |
| 获取结果 | POST | `https://www.dmxapi.cn/v1/responses` |



:::warning
请妥善保管您的 API Key！严禁将密钥泄露给他人、硬编码到代码中或提交到公开的代码仓库。如果怀疑密钥已泄露，请立即前往 DMXAPI 官网重新生成。
:::

:::warning 异步任务，请妥善保存 task_id
本模型为**异步任务**接口：提交任务后不会直接返回视频，只返回一个任务 ID（`task_id`），需再用查询模型 `MiniMax-H3-get` 凭该 ID 换取最终视频地址。请在提交成功后立即将 `task_id` 落库或写入日志妥善保存——一旦丢失将无法找回，本次生成结果也无法再取回，但费用已产生。
:::

## 模型名称

- `MiniMax-H3`

## 图生视频示例代码

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
    # 【model】(enum<string>, 必填) 模型名称
    # 可用值: "MiniMax-H3"
    "model": "MiniMax-H3",

    # 【input】(object[], 必填) 多模态输入内容数组，描述用于生成视频的信息
    # 每个元素通过 type 区分类型("text" / "image_url" / "video_url" / "audio_url")，
    # 并可通过 role 标注用途
    # 每次请求必须包含一个非空 text 项(prompt 必填)，缺失会返回参数错误
    # 图生视频支持的输入组合:
    #   - 首帧:   text + 1 张 image_url(role="first_frame" 或不填)
    #   - 尾帧:   text + 1 张 image_url(role="last_frame")
    #   - 首尾帧: text + 2 张 image_url(role 分别为 "first_frame"、"last_frame")
    # 图生视频与多模态参考生视频互斥: 出现 first_frame / last_frame 后，
    # 不能再出现 reference_image / reference_video / reference_audio
    # 图片限制: 格式 JPG、JPEG、PNG、WEBP、HEIC、HEIF；单文件 ≤ 30 MB；
    #   宽高范围 [256, 5760] px；长宽比(宽/高) [0.4, 2.5]；
    #   数量 首帧 ≤ 1、尾帧 ≤ 1、参考图 ≤ 9
    "input": [
        {
            # 【type】(enum<string>, 必填) 输入内容的类型
            # 可用值: "text" / "image_url" / "video_url" / "audio_url"
            "type": "text",

            # 【text】(string, 必填) 文本提示词(prompt)
            # 所有场景都需包含一个非空 text，描述期望生成的视频
            # 按字符数计算长度，单个 text 最多 7000 个字符
            "text": "Pull focus to the people in the background and add more steam to the ramen bowl."
        },
        {
            # 【type】(enum<string>, 必填) 输入内容的类型，此处为图片
            "type": "image_url",

            # 【image_url】(object) 当 type="image_url" 时的图片对象
            "image_url": {
                # 【image_url.url】(string, 必填) 图片地址，支持:
                #   - 公网 URL
                #   - mm_file://{file_id}(引用平台已有文件，如上传或历史产物的 file_id)
                #   - data:image/<格式>;base64,<Base64> data URI(<格式> 小写)
                "url": "https://your-cdn.example.com/h3-i2va-first-frame.png"
            },

            # 【role】(enum<string>, 条件必填) 内容的位置或用途
            # 可用值:
            #   - "first_frame"     首帧图片(图生视频；仅一张图且不填 role 时默认按 first_frame 处理)
            #   - "last_frame"      尾帧图片(图生视频-首尾帧，需与 first_frame 成对)
            "role": "first_frame"
        }
    ],

    # 【resolution】(enum<string>, 必填) 视频分辨率
    # 可用值: "768P" / "2K"
    "resolution": "2K",

    # 【duration】(enum<integer>, 必填) 生成视频时长(秒)，整数
    # 可用值: 4 / 5 / 6 / 7 / 8 / 9 / 10 / 11 / 12 / 13 / 14 / 15
    "duration": 5,

    # 【ratio】(enum<string>, 可选) 生成视频的宽高比
    # 默认 "adaptive"(自动，由输入自适应选择最合适的宽高比，
    # 图生视频(i2va，输入含 first_frame / last_frame 图片)场景:
    # 宽高比由输入图片决定，ratio 恒为 "adaptive"；
    # 传入其他合理值不会报错，但会被忽略并按 "adaptive" 处理
    "ratio": "adaptive",

    # 【aigc_watermark】(boolean, 可选) 是否在生成视频中添加 AIGC 标识水印
    # 默认值: false
    "aigc_watermark": False
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
payload["input"][1]["image_url"]["url"] = resolve_media(payload["input"][1]["image_url"]["url"])


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
  "task_id": "427083908907468",
  "usage": {
    "total_tokens": 40000,
    "input_tokens": 0,
    "input_tokens_details": {
      "cached_tokens": 0
    },
    "output_tokens": 40000,
    "output_tokens_details": {
      "reasoning_tokens": 0
    }
  }
}
```

返回中的 `task_id` 即任务 ID，用于后续查询任务状态与结果。**该 ID 仅在本次提交的响应中返回一次，请务必妥善保存**，丢失后无法找回本次任务。

## 获取生成视频 示例代码

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

    "model": "MiniMax-H3-get",
    "input": "427025706299794"

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

## 返回示例

```json
{
  "task": {
    "id": "427025706299794",
    "model": "MiniMax-H3",
    "status": "succeeded",
    "created_at": 1785809393,
    "updated_at": 1785809719,
    "content": {
      "url": "https://your-cdn.example.com/h3-generated-2k-output.mp4"
    },
    "resolution": "2K",
    "duration": 5,
    "usage": {
      "total_seconds": 11,
      "input_seconds": 6,
      "output_seconds": 5,
      "input_image_count": 0
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

任务状态 `status` 取值：`queued`（排队中）、`running`（运行中）、`succeeded`（成功）、`failed`（失败）、`cancelled`（已取消）。状态为 `succeeded` 时，`task.content.url` 即为生成视频的下载地址。

<p align="center">
  <small>© 2026 DMXAPI MiniMax-H3 图生视频</small>
</p>
