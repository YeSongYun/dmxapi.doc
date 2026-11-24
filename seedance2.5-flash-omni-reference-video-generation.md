# doubao-seedance-2-5-flash 全模态参考生视频 API 使用文档

使用图片、视频或音频作为参考生成新视频。素材可以单用，也可以组合。示例在提示词中用“图片1”“视频1”“音频1”分别指明要参考的外貌、动作和音色。

## 接口地址

| 接口 | 请求方式 | URL |
|------|---------|-----|
| 提交任务 | POST | `https://www.dmxapi.cn/api/v3/contents/generations/tasks` |
| 获取结果 | GET | `https://www.dmxapi.cn/api/v3/contents/generations/tasks/{task_id}` |

:::warning
请妥善保管 API Key。分享示例或向公开仓库提交代码前，请移除密钥。如果密钥泄露，请前往 DMXAPI 官网重新生成。
:::

:::warning 异步任务，请妥善保存任务 ID
提交成功后，请保存响应体中的 `id`。在本页的“获取生成视频”示例中填入该 ID，使用同一把 API Key 即可查询进度和获取视频。响应头中的请求 ID 用于排查单次 HTTP 请求。
:::

## 模型名称

- `doubao-seedance-2-5-flash-261115`

## 全模态参考生视频 示例代码


```python
import base64
import json
import os

import requests

# ===============================================================
# 步骤1: 配置 API 连接信息
# ===============================================================

url = "https://www.dmxapi.cn/api/v3/contents/generations/tasks"

# DMXAPI 密钥 (请替换为您自己的密钥)
# 获取方式: 登录 DMXAPI 官网 -> 个人中心 -> API 密钥管理
api_key = "sk-请替换为您的DMXAPI密钥"

# ===============================================================
# 步骤2: 配置请求头
# ===============================================================

headers = {
    "Content-Type": "application/json",      # 指定请求体为 JSON 格式
    "Authorization": f"Bearer {api_key}",    # Bearer token 认证方式
}

# ===============================================================
# 步骤3: 配置素材来源
# ===============================================================

# 参考图片。
# 图片 URL：填入图片的公网 URL。​
# Base64 编码：将本地文件转换为 Base64 编码字符串后提交给大模型，遵循格式 data:image/<图片格式>;base64,<Base64 编码>，注意 <图片格式> 需小写，如 data:image/png;base64,{base64_image}。​
# 素材 ID：用于视频生成的预置素材及虚拟人像的 ID，遵循格式 asset://<ASSET_ID>。
# 支持 jpeg、png、webp、bmp、tiff、gif、heic、heif。宽和高各为 300–6000 像素，宽/高为 0.4–2.5（均含边界）。
# 每张原图须小于 30 MB。Base64 编码后的完整 JSON 请求体最多 64 MB，大文件宜用公网 URL 或素材 ID。
# 参考图含真人人脸时，可用预置人像图片，或用本人认证并授权入库的图片，在 image_url.url 填对应的 asset://<ASSET_ID>。
image_source = "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260408/sjuytr/wan-r2v-object-girl.jpg"

# 参考视频。
# 参考视频可填公网视频 URL 或 asset://<ASSET_ID>。
# 支持 MP4 或 MOV，视频编码为 H.264/AVC 或 H.265/HEVC。带音轨时，MP4 支持 AAC、MP3，MOV 还支持 PCM。
# 帧率 24–60 FPS，单段 2–30 秒（视频编辑任务要求 4–30 秒），每段不超过 200 MB。一次最多 5 段，所有输入视频合计不超过 30 秒。
# 输入分辨率可为 480p、720p、1080p、4K。宽和高各为 300–6000 像素，宽/高为 0.4–2.5。
# 每帧总像素数（宽×高）为 407696–8847360，包含上下限。Flash 的输出分辨率在 payload 的 resolution 中选择。
# 待编辑的原片含真人人脸时，可用本人认证、授权后入库的视频，在 video_url.url 填该视频的 asset://<ASSET_ID>。
# 参考视频含真人人脸时，可用本人认证并授权入库的视频，在 video_url.url 填对应的 asset://<ASSET_ID>。
video_source = "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260129/qigswt/wan-r2v-role2.mp4"

# 参考音频。
# 可填公网音频 URL、asset://<ASSET_ID> 或 data:audio/<小写格式>;base64,...。
# 支持 WAV、MP3。单段 2–30 秒，每段不超过 15 MB。最多 5 段音频，合计不超过 30 秒。
# 参考音频可单独使用。若编码为 Base64，图片、音频和其他字段合计仍受 64 MB 请求体上限约束。
audio_source = "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260408/gbqewz/wan-r2v-girl-voice.mp3"

# ===============================================================
# 步骤4: 配置请求参数
# ===============================================================

payload = {
    # 【content】(object[], 必填) 输入内容列表。
    # 至少提供一种参考素材，可单用图片、视频或音频，也可任意组合。网关还接受 1 条可选文本。
    # Flash 每次最多 10 张参考图、5 段参考视频、5 段参考音频。视频合计最多 30 秒，音频另计最多 30 秒。
    # 每项按素材类型填写角色，图片用 reference_image，视频用 reference_video，音频用 reference_audio。
    "content": [
        {
            # 【text】(string, 文本项内必填) 带素材时可省略整个文本项。若写 type="text"，这里必须填写非空提示词。
            # 按同一类型各自的出现顺序从 1 编号，可用“图片1”“视频1”“音频1”指明参考谁的外貌、动作或音色。
            # 支持中文、英语、西班牙语、印度尼西亚语、葡萄牙语、日语、马来语、泰语、阿拉伯语、越南语和韩语。
            # 建议中文提示词不超过 500 字、英文不超过 1000 词，过长时模型可能忽略部分细节。
            # 将分辨率、宽高比、时长和水印分别填在 resolution、ratio、duration 和 watermark 中。
            "text": "图片1中的女生路过视频1里正在弹吉他的男生身边，场景和男生的动作参考视频1。女生用音频1的音色说：真好听，能不能再唱一遍。",

            # 【type】(string, 必填) 内容类型，此处固定为 text
            "type": "text",
        },
        {
            # 【image_url】(object, 当 type="image_url" 时必填) 参考图片。
            # 【image_url.url】(string, 必填) 填上方的图片来源。脚本会将本地图片路径转换为 data URI。
            "image_url": {"url": image_source},

            # 【role】(string, 必填) 参考图片固定为 reference_image
            "role": "reference_image",

            # 【type】(string, 必填) 内容类型，此处固定为 image_url
            "type": "image_url",
        },
        {
            # 【video_url】(object, 当 type="video_url" 时必填) 参考视频。
            # 【video_url.url】(string, 必填) 填公网视频 URL 或 asset://<ASSET_ID>。视频字段不接受 Base64。
            "video_url": {"url": video_source},

            # 【role】(string, 必填) 参考视频固定为 reference_video
            "role": "reference_video",

            # 【type】(string, 必填) 内容类型，此处固定为 video_url
            "type": "video_url",
        },
        {
            # 【audio_url】(object, 当 type="audio_url" 时必填) 参考音频。
            # 【audio_url.url】(string, 必填) 填上方的音频来源。本地 WAV 或 MP3 经脚本编码为带音频 MIME 类型的 data URI。
            "audio_url": {"url": audio_source},

            # 【role】(string, 必填) 参考音频固定为 reference_audio
            "role": "reference_audio",

            # 【type】(string, 必填) 内容类型，此处固定为 audio_url
            "type": "audio_url",
        },
    ],

    # 【duration】(integer, 可选，默认 -1) 输出视频的目标时长，单位为秒。
    # 可填 4–30（含边界）的整数。省略或填 -1 时，由模型根据内容在该范围内选择整数秒。
    "duration": 5,

    # 【generate_audio】(boolean, 可选，默认 True) 是否生成与画面同步的声音。
    # True 时生成双声道音轨。可在提示词里用“音频1”指定要参考的音色，用双引号给出台词。
    # False 输出无声视频。
    "generate_audio": True,

    # 【model】(string, 必填) doubao-seedance-2-5-flash-261115 的完整模型 ID。
    "model": "doubao-seedance-2-5-flash-261115",

    # 【omni_reference_task_type】(string, 可选，默认 "auto") 全模态参考填 "reference"，让模型参考给定素材生成新视频。
    # 提示词应写清要借鉴的外貌、动作或音色。若提示词意图与指定的参考任务不符，可能返回 InvalidParameter.TaskTypeMismatch。
    "omni_reference_task_type": "reference",

    # 【output_format】(string, 可选，默认 "mp4") 输出视频的容器格式。
    # mp4：通用格式，兼容性最好，采用标准色彩精度，可在网页、移动端、各类播放器及分发平台直接播放。​
    # mov：面向专业场景的高色彩精度格式，更好地保持画面色彩与亮度一致性、适用于调色、抠像、合成等对色彩还原要求高的专业后期加工。推荐在视频编辑、视频延长场景使用 mov 格式作为输入和输出。
    "output_format": "mp4",

    # 【ratio】(string, 可选，默认 "adaptive") 输出视频的宽高比（宽与高之比）。
    # 例如，720p 搭配 "9:16" 得到 720×1280 的竖屏视频，搭配 "16:9" 得到 1280×720 的横屏视频。
    # ratio    480p       720p
    # 16:9     854×480    1280×720
    # 4:3      752×560    1112×834
    # 1:1      640×640    960×960
    # 3:4      560×752    834×1112
    # 9:16     480×854    720×1280
    # 21:9     992×432    1470×630
    "ratio": "16:9",

    # 【resolution】(string, 可选，默认 "720p") Flash 输出有 "480p" 和 "720p" 两档。
    # 两档均输出 8 位视频。同一时长和比例下，720p 包含的像素更多，消耗的视频 token 也更多。
    "resolution": "720p",

    # 【return_last_frame】(boolean, 可选，默认 False) 是否另外返回成片的最后一帧。
    # True 时，成功查询的 content.last_frame_url 提供 JPEG 图片，与成片宽高相同，水印由 watermark 决定。
    # False 时只返回成片。
    "return_last_frame": False,

    # 【watermark】(boolean, 可选，默认 False) True 在成片右下角显示“AI 生成”水印，False 输出无水印画面。
    "watermark": False,
}

# ===============================================================
# 媒体处理逻辑（无需修改）
# ===============================================================

_IMAGE_MIME = {
    ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg",
    ".png": "image/png",
    ".webp": "image/webp",
    ".bmp": "image/bmp",
    ".tif": "image/tiff",
    ".tiff": "image/tiff",
    ".gif": "image/gif",
    ".heic": "image/heic",
    ".heif": "image/heif",
}
_AUDIO_MIME = {".wav": "audio/wav", ".mp3": "audio/mpeg"}


def _resolve_media(value, kind, field):
    """图片和音频支持本地文件；视频只接受公网 URL 或 asset://。"""
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field} 不能为空")
    value = value.strip()
    if value.startswith(("http://", "https://", "asset://")):
        return value
    if kind == "video":
        raise ValueError(f"{field} 不支持本地文件或 Base64，只支持公网 URL 或 asset://")
    if value.startswith("data:"):
        return value
    if not os.path.isfile(value):
        raise ValueError(f"{field} 找不到本地文件：{value}")
    mime_map = _IMAGE_MIME if kind == "image" else _AUDIO_MIME
    mime = mime_map.get(os.path.splitext(value)[1].lower())
    if mime is None:
        raise ValueError(f"{field} 文件格式不支持")
    size = os.path.getsize(value)
    if kind == "image" and size >= 30 * 1024 * 1024:
        raise ValueError(f"{field}须小于 30 MB")
    if kind == "audio" and size > 15 * 1024 * 1024:
        raise ValueError(f"{field}不能超过 15 MB")
    with open(value, "rb") as file:
        encoded = base64.b64encode(file.read()).decode("ascii")
    return f"data:{mime};base64,{encoded}"


for item in payload["content"]:
    if item.get("type") == "image_url":
        item["image_url"]["url"] = _resolve_media(item["image_url"]["url"], "image", "参考图片")
    elif item.get("type") == "video_url":
        item["video_url"]["url"] = _resolve_media(item["video_url"]["url"], "video", "参考视频")
    elif item.get("type") == "audio_url":
        item["audio_url"]["url"] = _resolve_media(item["audio_url"]["url"], "audio", "参考音频")

# ===============================================================
# 步骤5: 发送请求并输出结果
# ===============================================================

# Base64 会增大请求体。按实际发送的 UTF-8 字节数检查 64 MB 上限。
body = json.dumps(payload, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
if len(body) > 64 * 1024 * 1024:
    raise ValueError("请求体超过 64 MB，请将较大的素材改为公网 URL 或 asset:// 素材 ID")

response = requests.post(url, headers=headers, data=body, timeout=(10, 60))
if not response.ok:
    raise SystemExit(f"提交失败（HTTP {response.status_code}）：{response.text[:500]}")
print(json.dumps(response.json(), indent=2, ensure_ascii=False))
```

## 返回示例


```json
{
  "id": "task_Yg9qT3EGHm5oSolP0WBsq9NpuNIF0PJZ"
}
```

## 获取生成视频 示例代码


```python
import json
import time
from urllib.parse import quote

import requests

# ===============================================================
# 步骤1: 配置 API 连接信息
# ===============================================================

url = "https://www.dmxapi.cn/api/v3/contents/generations/tasks"
api_key = "sk-请替换为您的DMXAPI密钥"  # 使用提交任务时的 API Key

# ===============================================================
# 步骤2: 配置请求头
# ===============================================================

headers = {"Authorization": f"Bearer {api_key}"}

# ===============================================================
# 步骤3: 填写提交响应中的任务 ID
# ===============================================================

task_id = "task_Yg9qT3EGHm5oSolP0WBsq9NpuNIF0PJZ"  # 替换为刚才保存的 id
query_url = f"{url}/{quote(task_id, safe='')}"

# ===============================================================
# 步骤4: 查询任务状态并输出结果
# ===============================================================

# 网络中断、响应体不完整或网关暂时不可用时，使用同一任务 ID 最多再查两次。
consecutive_errors = 0
with requests.Session() as session:
    while True:
        delay = 15
        try:
            response = session.get(query_url, headers=headers, timeout=(10, 60))
            if response.status_code in (429, 500, 502, 503, 504):
                retry_after = response.headers.get("Retry-After", "")
                if retry_after.isdecimal():
                    delay = int(retry_after)
                response.raise_for_status()
            if not response.ok:
                raise SystemExit(f"查询失败（HTTP {response.status_code}）：{response.text[:500]}")
            result = response.json()
        except (requests.RequestException, ValueError) as error:
            consecutive_errors += 1
            if consecutive_errors >= 3:
                raise SystemExit(f"查询连续失败 3 次：{error}") from error
            time.sleep(delay)
            continue

        consecutive_errors = 0
        if result["id"] != task_id:
            raise ValueError("查询返回的 id 与提交时保存的任务 ID 不一致")
        if result["status"] not in ("queued", "running"):
            break
        time.sleep(15)

# 终态只输出一份完整 JSON。成功时读取 content.video_url，失败时查看 error。
print(json.dumps(result, indent=2, ensure_ascii=False))
if result["status"] != "succeeded":
    raise SystemExit(f"任务未成功，状态为 {result['status']}")
```

## 返回示例

```json
{
  "content": {
    "video_url": "https://ark-acg-cn-beijing.tos-cn-beijing.volces.com/doubao-seedance-2-5-flash/2112844032/Video/y5k1f-23738142116202-tgc_d20b631b8d51caffff00000000000000000000259856615597120/cgt-20261124183732-f1k5y.mp4?X-Tos-Algorithm=TOS4-HMAC-SHA256&X-Tos-Credential=AKLTYWJkZTExNjA1ZDUyNDc3YzhjNTM5OGIyNjBhNDcyOTQ%2F20261124%2Fcn-beijing%2Ftos%2Frequest&X-Tos-Date=20261124T103825Z&X-Tos-Expires=86400&X-Tos-Max-Requests=100&X-Tos-Signature=9e851119fd4d5deec6eac55875aa2e3d449062084b80288ccf67e2aa7388b35a&X-Tos-SignedHeaders=host"
  },
  "created_at": 1795516658,
  "draft": false,
  "duration": 5,
  "execution_expires_after": 172800,
  "framespersecond": 24,
  "generate_audio": true,
  "id": "task_Yg9qT3EGHm5oSolP0WBsq9NpuNIF0PJZ",
  "model": "doubao-seedance-2-5-flash-261115",
  "output_format": "mp4",
  "priority": 0,
  "ratio": "16:9",
  "resolution": "720p",
  "seed": 68884,
  "service_tier": "default",
  "status": "succeeded",
  "updated_at": 1795516709,
  "usage": {
    "completion_tokens": 216900,
    "total_tokens": 216900
  }
}
```

<!--@include: /.vitepress/includes/seedance-2-5-flash-artifacts.md-->

<p align="center">
  <small>© 2026 DMXAPI doubao-seedance-2-5-flash 全模态参考生视频</small>
</p>
