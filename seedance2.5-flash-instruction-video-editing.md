# doubao-seedance-2-5-flash 视频编辑 API 使用文档

用提示词指明要编辑的参考视频、编辑对象和改动。示例将人物手中的信封替换为红玫瑰，并修改风衣颜色。成片的画幅和时长随被编辑的原片确定。

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

## 视频编辑 示例代码

```python
import json

import requests

# ===============================================================
# 步骤1: 配置 API 连接信息
# ===============================================================

# 通过 POST 向 DMXAPI 网关提交视频编辑任务。
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

# 待编辑视频可填公网视频 URL 或 asset://<ASSET_ID>。
# 支持 MP4 或 MOV，视频编码为 H.264/AVC 或 H.265/HEVC。带音轨时，MP4 支持 AAC、MP3，MOV 还支持 PCM。
# 帧率 24–60 FPS，单段 4–30 秒，每段不超过 200 MB。一次最多 5 段，所有输入视频合计不超过 30 秒。
# 输入分辨率可为 480p、720p、1080p、4K。宽和高各为 300–6000 像素，宽/高为 0.4–2.5。
# 每帧总像素数（宽×高）为 407696–8847360，包含上下限。Flash 的输出分辨率在 payload 的 resolution 中选择。
# 待编辑的原片含真人人脸时，可用本人认证、授权后入库的视频，在 video_url.url 填该视频的 asset://<ASSET_ID>。
video_source = "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260402/ldnfdf/wan2.7-videoedit-style-change.mp4"

# ===============================================================
# 步骤4: 配置请求参数
# ===============================================================

payload = {
    # 【content】(object[], 必填) 输入内容列表。
    # 至少放入 1 段 role 为 reference_video 的视频。本例只有一段，在编辑指令中用“视频1”指明它。
    "content": [
        {
            # 【text】(string, 文本项内必填) 编辑时用“视频1”指明目标，并写出要改什么。
            # 明确写出编辑动作，例如“增加”“加上”“删除”“去掉”“修改”“替换”或“改成”。
            # 有多段输入时用“视频1”“视频2”指明对象，例如“把视频2中的信封替换为红玫瑰”。
            # 支持中文、英语、西班牙语、印度尼西亚语、葡萄牙语、日语、马来语、泰语、阿拉伯语、越南语和韩语。
            # 建议中文提示词不超过 500 字、英文不超过 1000 词，过长时模型可能忽略部分细节。
            # 将分辨率、宽高比、时长和水印分别填在 resolution、ratio、duration 和 watermark 中。
            "text": "把视频1里女生手中的信封换成一束红玫瑰，风衣改成红色。人物动作和车站背景保持不变。",

            # 【type】(string, 必填) 内容类型，此处固定为 text
            "type": "text",
        },
        {
            # 【video_url】(object, 当 type="video_url" 时必填) 待编辑的视频。
            # 【video_url.url】(string, 必填) 填公网视频 URL 或 asset://<ASSET_ID>。视频字段不接受 Base64。
            "video_url": {"url": video_source},

            # 【role】(string, 必填) 固定为 reference_video
            "role": "reference_video",

            # 【type】(string, 必填) 内容类型，此处固定为 video_url
            "type": "video_url",
        },
    ],

    # 【duration】(integer, 可选，默认 -1) 编辑任务只接受 -1。
    # 模型按提示词选定一段 4–30 秒的输入视频，使成片时长与其基本一致。成片可为非整数秒，可能比原片短约 0.4 秒。
    "duration": -1,

    # 【generate_audio】(boolean, 可选，默认 True) 是否生成与画面同步的声音。
    # True 时输出双声道音轨，编辑指令可写明要调整的对白、环境音或背景音乐。
    # False 输出无声视频。
    "generate_audio": True,

    # 【model】(string, 必填) doubao-seedance-2-5-flash-261115 的完整模型 ID。
    "model": "doubao-seedance-2-5-flash-261115",

    # 【omni_reference_task_type】(string, 可选，默认 "auto") 本例填 "edit"，明确对指定视频进行编辑。
    # 提示词要指出需要修改的内容。模型判断提示词与编辑意图不符时，可能返回 InvalidParameter.TaskTypeMismatch。
    "omni_reference_task_type": "edit",

    # 【output_format】(string, 可选，默认 "mp4") 输出视频的容器格式。
    # mp4：通用格式，兼容性最好，采用标准色彩精度，可在网页、移动端、各类播放器及分发平台直接播放。​
    # mov：面向专业场景的高色彩精度格式，更好地保持画面色彩与亮度一致性、适用于调色、抠像、合成等对色彩还原要求高的专业后期加工。推荐在视频编辑、视频延长场景使用 mov 格式作为输入和输出。
    "output_format": "mp4",

    # 【ratio】(string, 可选，默认 "adaptive") 输出视频的宽高比（宽与高之比）。
    # 此字段只能省略或填 "adaptive"，成片保持待编辑视频的宽高比。
    # 有多段视频时，以提示词选中的那一段为准。例如，指令指定修改“视频2”，成片就跟随视频2的画幅。
    "ratio": "adaptive",

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
# 步骤5: 发送请求并输出结果
# ===============================================================

if not str(video_source).startswith(("http://", "https://", "asset://")):
    raise ValueError("待编辑视频只支持公网 URL 或 asset://，不支持本地文件和 Base64。")

# 发送请求并格式化输出 JSON，保留响应中的任务 id 供下方查询使用。
response = requests.post(url, headers=headers, json=payload, timeout=(10, 60))
if not response.ok:
    raise SystemExit(f"提交失败（HTTP {response.status_code}）：{response.text[:500]}")
print(json.dumps(response.json(), indent=2, ensure_ascii=False))
```

## 返回示例

```json
{
  "id": "task_P3JUAaBI81DdcZMxwQsUMpkU45m4XcUl"
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

task_id = "task_P3JUAaBI81DdcZMxwQsUMpkU45m4XcUl"  # 替换为刚才保存的 id
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

以下是成功响应的部分字段，任务 ID 和下载地址为示例值。`content.video_url` 是成片地址。提交时若设置了 `return_last_frame=True`，还会返回 `content.last_frame_url`。

```json
{
  "content": {
    "video_url": "https://ark-acg-cn-beijing.tos-cn-beijing.volces.com/doubao-seedance-2-5-flash/2112844032/Video/tnlsd-60738142116202-tgc_8d3788332e51caffff00000000000000000000006336615597120/cgt-20261124183706-dslnt.mp4?X-Tos-Algorithm=TOS4-HMAC-SHA256&X-Tos-Credential=AKLTYWJkZTExNjA1ZDUyNDc3YzhjNTM5OGIyNjBhNDcyOTQ%2F20261124%2Fcn-beijing%2Ftos%2Frequest&X-Tos-Date=20261124T103749Z&X-Tos-Expires=86400&X-Tos-Max-Requests=100&X-Tos-Signature=cc22b4166674eaf24cdd7b6db3ed76d0f59fbef1d401de99309d1899ea37c88f&X-Tos-SignedHeaders=host"
  },
  "created_at": 1795516632,
  "draft": false,
  "duration": 4,
  "execution_expires_after": 172800,
  "framespersecond": 24,
  "generate_audio": true,
  "id": "task_P3JUAaBI81DdcZMxwQsUMpkU45m4XcUl",
  "model": "doubao-seedance-2-5-flash-261115",
  "output_format": "mp4",
  "priority": 0,
  "ratio": "16:9",
  "resolution": "720p",
  "seed": 89779,
  "service_tier": "default",
  "status": "succeeded",
  "updated_at": 1795516672,
  "usage": {
    "completion_tokens": 209700,
    "total_tokens": 209700
  }
}
```

<p align="center">
  <small>© 2026 DMXAPI doubao-seedance-2-5-flash 视频编辑</small>
</p>
