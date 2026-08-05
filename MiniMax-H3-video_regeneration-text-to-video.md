# MiniMax-H3 视频再生成-文生视频 API 使用文档

MiniMax-H3 视频再生成接口，把符合 MiniMax-H3 768P 输出规格的源视频再生成为 2K 视频。文生视频场景的再生成需在 `input` 数组中原样提交生成 768P 源视频时实际送入模型的全部输入（此处即那一条最终 prompt，单个 `text` 最多 40000 个字符），并附加一个 `role` 为 `base_video` 的源视频项，该项必须且只能有一个。源视频须包含音轨、帧率 24 fps、宽高均能被 32 整除、面积 ≤ 768 × 1344（1,032,192 像素）、总帧数 107~362 帧（每档递增 17 帧，约 4~15 秒）；本接口不支持任意视频的通用处理。目标分辨率 `resolution` 当前仅支持 `2K`。接口以异步任务方式工作：提交后返回任务 ID，再用查询模型换取最终视频地址。

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

- `MiniMax-H3-video_regeneration`

## 视频再生成-文生视频示例代码

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
    # 可用值: "MiniMax-H3-video_regeneration"
    "model": "MiniMax-H3-video_regeneration",

    # 【input】(object[], 必填) 视频再生成输入内容数组
    # 每个元素通过 type 区分类型("text" / "image_url" / "video_url" / "audio_url")，
    # 并可通过 role 标注用途
    # 数组中必须包含:
    #   1. 生成 768P 源视频时实际送入模型的全部输入，原样提交。其中 text 必须使用当时
    #      实际送入模型的最终 prompt，不可使用 H3-Context-IR 处理前的原始 prompt；
    #      所有参考图片、视频和音频也必须与生成时一致。
    #      任何输入不一致，都可能无法达到预期的再生成效果
    #   2. 一个 768P 源视频项，type="video_url" 且 role="base_video"；
    #      该项必须且只能有一个
    # 文生视频场景的再生成: 一个 text 元素 + 一个 base_video 元素
    # base_video 必须符合以下 MiniMax-H3 768P 输出规格
    # (本接口不支持任意视频的通用再生成):
    #   音轨:            需包含音轨，不支持无音轨视频
    #   帧率:            24 fps
    #   宽 / 高:         均需能被 32 整除
    #   面积(宽 × 高):   ≤ 768 × 1344(1,032,192 像素)
    #   总帧数:          107-362 帧，每档递增 17 帧(约 4-15 秒)
    # 输入媒体限制: 请求体总大小 ≤ 64 MB，大文件请用公网 URL，勿用 Base64
    "input": [
        {
            # 【type】(enum<string>, 必填) 输入内容的类型
            # 可用值: "text" / "image_url" / "video_url" / "audio_url"
            "type": "text",

            # 【text】(string) 文本提示词(prompt)
            # 必须使用生成 768P 源视频时实际送入模型的最终 prompt，
            # 不可使用 H3-Context-IR 处理前的原始 prompt
            # 按字符数计算长度，单个 text 最多 40000 个字符
            "text": "史诗级太空歌剧院线预告：女舰长独自站在巨大观景窗前，最后一支舰队正在集结并跃迁离去，强光爆闪、舰桥震动，她被留在原地。"
        },
        {
            # 【type】(enum<string>, 必填) 输入内容的类型，此处为视频
            "type": "video_url",

            # 【video_url】(object) 当 type="video_url" 时的视频对象
            "video_url": {
                # 【video_url.url】(string, 必填) 视频地址，支持:
                #   - 公网 URL
                #   - mm_file://{file_id}(引用平台已有文件的 file_id)
                #   - data:video/mp4;base64,<Base64> data URI
                # 注意请求体总大小 ≤ 64 MB、Base64 会放大约 33%，
                # 大视频请用公网 URL 或 mm_file://
                "url": "https://your-cdn.example.com/h3-768p-source-video.mp4"
            },

            # 【role】(enum<string>, 条件必填) 内容的位置或用途
            # 可用值:
            #   - "base_video"      视频再生成源视频(仅视频再生成接口使用)；
            #                       源视频项必须显式设置该 role，input 中必须且只能有 1 个
            "role": "base_video"
        }
    ],

    # 【resolution】(enum<string>, 必填) 视频再生成的目标分辨率
    # 可用值: "2K"
    "resolution": "2K",

    # 【aigc_watermark】(boolean, 可选) 是否为生成视频添加 AIGC 水印
    # 默认值: false
    "aigc_watermark": False
}

# ===============================================================
# 步骤4: 媒体输入处理
# ===============================================================
# - 公网 URL (http/https): 原样传入
# - 本地文件路径: 自动读取并转为 data:{格式};base64,{base64_data}
# 注意: data URI 里的 {格式} 取文件扩展名，不是标准 MIME 类型。
#   例如 .mov 要写 video/mov(而非标准 MIME 的 video/quicktime)、
#   .avi 写 video/avi(而非 video/x-msvideo)、
#   .mkv 写 video/mkv(而非 video/x-matroska)，
#   否则服务端报 "MiniMax-H3 media data URI is invalid"。

_MIME_MAP = {
    ".avi": "video/avi",
    ".mkv": "video/mkv",
    ".mov": "video/mov",
    ".mp4": "video/mp4",
    ".webm": "video/webm",
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


# 遍历 input，把视频里的本地路径统一转成 data URI
# （按 type 取对象，不写死下标，增删输入项时不会错位）
for _item in payload["input"]:
    _key = _item.get("type")
    if _key in ("image_url", "video_url", "audio_url"):
        _item[_key]["url"] = resolve_media(_item[_key]["url"])


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
  "task_id": "427453262668145",
  "输出视频秒数": 4.458333333,
  "usage": {
    "total_tokens": 13375,
    "input_tokens": 0,
    "input_tokens_details": {
      "cached_tokens": 0
    },
    "output_tokens": 13375,
    "output_tokens_details": {
      "reasoning_tokens": 0
    }
  }
}
```

返回中的 `task_id` 即任务 ID，用于后续查询任务状态与结果。**该 ID 仅在本次提交的响应中返回一次，请务必妥善保存**，丢失后无法找回本次任务。

`输出视频秒数` 为本次再生成的视频时长（秒），由源视频总帧数按 24 fps 换算得出，因此通常为小数（如 107 帧 ÷ 24 ≈ 4.458333333）。该值是本次任务的计费依据，与 `usage.output_tokens` 对应；查询接口返回的 `duration` 是取整后的秒数，两者口径不同，解析时请勿混用。

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
    "input": "427453262668145"

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
    "id": "427453262668145",
    "model": "MiniMax-H3",
    "status": "succeeded",
    "created_at": 1785823202,
    "updated_at": 1785823286,
    "content": {
      "url": "https://your-cdn.example.com/h3-regenerated-2k-output.mp4"
    },
    "resolution": "2K",
    "duration": 4,
    "usage": {
      "total_seconds": 8,
      "input_seconds": 4,
      "output_seconds": 4,
      "input_image_count": 0
    },
    "ratio": "",
    "task_type": "regeneration",
    "modality": "video"
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

任务状态 `status` 取值：`queued`（排队中）、`running`（运行中）、`succeeded`（成功）、`failed`（失败）、`cancelled`（已取消）。状态为 `succeeded` 时，`task.content.url` 即为生成视频的下载地址。再生成任务的 `task_type` 为 `regeneration`。

<p align="center">
  <small>© 2026 DMXAPI MiniMax-H3 视频再生成-文生视频</small>
</p>
