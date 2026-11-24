# doubao-seedance-2-5-flash 视频延长 API 使用文档

指定一段原片，用“向前延长”或“向后延长”说明从哪一端续写，再描述新画面和声音。示例从原片末尾延续城市镜头，新片段沿用原片的宽高比。

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

## 视频延长 示例代码

```python
import json

import requests

# ===============================================================
# 步骤1: 配置 API 连接信息
# ===============================================================

# 通过 POST 向 DMXAPI 网关提交视频延长任务。
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
# 步骤3: 配置视频来源
# ===============================================================

# 待延长视频可填公网视频 URL 或 asset://<ASSET_ID>。
# 支持 MP4 或 MOV，视频编码为 H.264/AVC 或 H.265/HEVC。带音轨时，MP4 支持 AAC、MP3，MOV 还支持 PCM。
# 帧率 24–60 FPS，单段 2–30 秒，每段不超过 200 MB。一次最多 5 段，所有输入视频合计不超过 30 秒。
# 输入分辨率可为 480p、720p、1080p、4K。宽和高各为 300–6000 像素，宽/高为 0.4–2.5。
# 每帧总像素数（宽×高）为 407696–8847360，包含上下限。Flash 的输出分辨率在 payload 的 resolution 中选择。
# 待编辑的原片含真人人脸时，可用本人认证、授权后入库的视频，在 video_url.url 填该视频的 asset://<ASSET_ID>。
video_source = "https://arkdocs.tos-cn-beijing.volces.com/videos/video-generation/r2v_extend_video1_75.mov"

# ===============================================================
# 步骤4: 配置请求参数
# ===============================================================

payload = {
    # 【content】(object[], 必填) 输入内容列表。
    # 至少放入 1 段 role 为 reference_video 的视频。本例只有一段，在延长指令中用“视频1”指明它。
    "content": [
        {
            # 【text】(string, 文本项内必填) 延长时用“视频1”指明目标和新画面的内容。
            # 用“向前延长”“向后延长”“延续”或“续写”说明生成意图，并写明目标视频和要发生的动作。
            # 例如“向后延长视频1，镜头向前穿过街道”。“向后延长”指接在原片末尾，镜头运动方向由后面的描述决定。
            # 支持中文、英语、西班牙语、印度尼西亚语、葡萄牙语、日语、马来语、泰语、阿拉伯语、越南语和韩语。
            # 建议中文提示词不超过 500 字、英文不超过 1000 词，过长时模型可能忽略部分细节。
            # 将分辨率、宽高比、时长和水印分别填在 resolution、ratio、duration 和 watermark 中。
            "text": "向后延长视频1，镜头继续从倾斜的高楼间向前滑过，黄昏的城市灯光逐渐亮起。",

            # 【type】(string, 必填) 内容类型，此处固定为 text
            "type": "text",
        },
        {
            # 【video_url】(object, 当 type="video_url" 时必填) 待延长的视频。
            # 【video_url.url】(string, 必填) 填公网视频 URL 或 asset://<ASSET_ID>。视频字段不接受 Base64。
            "video_url": {"url": video_source},

            # 【role】(string, 必填) 固定为 reference_video
            "role": "reference_video",

            # 【type】(string, 必填) 内容类型，此处固定为 video_url
            "type": "video_url",
        },
    ],

    # 【duration】(integer, 可选，默认 -1) 输出视频的目标时长，单位为秒。
    # 延长任务可填 4–30（含边界）的整数来指定输出时长，或填 -1 让模型在该范围内选择整数秒。
    "duration": 10,

    # 【generate_audio】(boolean, 可选，默认 True) 是否生成与画面同步的声音。
    # True 时为续写画面生成双声道音轨，可在提示词中描述要延续的环境音或新增的台词。
    # False 输出无声视频。
    "generate_audio": True,

    # 【model】(string, 必填) doubao-seedance-2-5-flash-261115 的完整模型 ID。
    "model": "doubao-seedance-2-5-flash-261115",

    # 【omni_reference_task_type】(string, 可选，默认 "auto") 视频延长功能填 "extend"，明确对指定视频进行延长。
    # 提示词要指出从哪一端续写以及接下来发生什么。模型判断提示词与延长意图不符时，可能返回 InvalidParameter.TaskTypeMismatch。
    "omni_reference_task_type": "extend",

    # 【output_format】(string, 可选，默认 "mp4") 输出视频的容器格式。
    # mp4：通用格式，兼容性最好，采用标准色彩精度，可在网页、移动端、各类播放器及分发平台直接播放。​
    # mov：面向专业场景的高色彩精度格式，更好地保持画面色彩与亮度一致性、适用于调色、抠像、合成等对色彩还原要求高的专业后期加工。推荐在视频编辑、视频延长场景使用 mov 格式作为输入和输出。
    "output_format": "mp4",

    # 【ratio】(string, 可选，默认 "adaptive") 输出视频的宽高比（宽与高之比）。
    # 此字段只能省略或填 "adaptive"，续写片段保持所选原片的宽高比。
    # 本例原片是 5:4，向前或向后延长都会沿用 5:4。
    "ratio": "adaptive",

    # 【resolution】(string, 可选，默认 "720p") Flash 输出有 "480p" 和 "720p" 两档。
    # 两档均输出 8 位视频。同一时长和比例下，720p 包含的像素更多，消耗的视频 token 也更多。
    "resolution": "480p",

    # 【return_last_frame】(boolean, 可选，默认 False) 是否另外返回成片的最后一帧。
    # True 时，成功查询的 content.last_frame_url 提供 JPEG 图片，与成片宽高相同，水印由 watermark 决定。
    # False 时只返回成片。
    "return_last_frame": False,

    # 【watermark】(boolean, 可选，默认 False) True 在成片右下角显示“AI 生成”水印，False 输出无水印画面。
    "watermark": False,
}

# ===============================================================
# 步骤5: 发送请求并输出结果
# ===============================================================

if not str(video_source).startswith(("http://", "https://", "asset://")):
    raise ValueError("待延长视频只支持公网 URL 或 asset://，不支持本地文件和 Base64。")

# 发送请求并格式化输出 JSON，保留响应中的任务 id 供下方查询使用。
response = requests.post(url, headers=headers, json=payload, timeout=(10, 60))
if not response.ok:
    raise SystemExit(f"提交失败（HTTP {response.status_code}）：{response.text[:500]}")
print(json.dumps(response.json(), indent=2, ensure_ascii=False))
```

## 返回示例

```json
{
  "id": "task_9wPh9UbBEB58m8RQnBnSeK9liMWBHCbF"
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

task_id = "task_9wPh9UbBEB58m8RQnBnSeK9liMWBHCbF"  # 替换为刚才保存的 id
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
    "video_url": "https://ark-acg-cn-beijing.tos-cn-beijing.volces.com/doubao-seedance-2-5-flash/2112844032/Video/qkhz8-41738142116202-tgc_217407bddd51caffff00000000000000000000147146615597120/cgt-20261124183714-8zhkq.mp4?X-Tos-Algorithm=TOS4-HMAC-SHA256&X-Tos-Credential=AKLTYWJkZTExNjA1ZDUyNDc3YzhjNTM5OGIyNjBhNDcyOTQ%2F20261124%2Fcn-beijing%2Ftos%2Frequest&X-Tos-Date=20261124T103759Z&X-Tos-Expires=86400&X-Tos-Max-Requests=100&X-Tos-Signature=3b8667e3ecde6398e04f2bad98746e40537767ef44a7d01b80565965986b900b&X-Tos-SignedHeaders=host"
  },
  "created_at": 1795516640,
  "draft": false,
  "duration": 10,
  "execution_expires_after": 172800,
  "framespersecond": 24,
  "generate_audio": true,
  "id": "task_9wPh9UbBEB58m8RQnBnSeK9liMWBHCbF",
  "model": "doubao-seedance-2-5-flash-261115",
  "output_format": "mp4",
  "priority": 0,
  "ratio": "363:290",
  "resolution": "480p",
  "seed": 68788,
  "service_tier": "default",
  "status": "succeeded",
  "updated_at": 1795516682,
  "usage": {
    "completion_tokens": 167774,
    "total_tokens": 167774
  }
}
```

<!--@include: /.vitepress/includes/seedance-2-5-flash-artifacts.md-->

<p align="center">
  <small>© 2026 DMXAPI doubao-seedance-2-5-flash 视频延长</small>
</p>
