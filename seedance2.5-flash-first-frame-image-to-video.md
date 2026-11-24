# doubao-seedance-2-5-flash 首帧图生视频 API 使用文档

上传一张图片作为视频首帧，再用可选的提示词描述接下来的动作、镜头和声音。成片沿用首帧的宽高比。示例支持公网图片地址、素材 ID、Base64 和本地图片。

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

## 首帧图生视频 示例代码

```python
import base64
import json
import os

import requests

# ===============================================================
# 步骤1: 配置 API 连接信息
# ===============================================================

# 通过 POST 向 DMXAPI 网关提交首帧图生视频任务。
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
# 步骤3: 配置图片来源
# ===============================================================

# 首帧图片。
# 图片 URL：填入图片的公网 URL。​
# Base64 编码：将本地文件转换为 Base64 编码字符串后提交给大模型，遵循格式 data:image/<图片格式>;base64,<Base64 编码>，注意 <图片格式> 需小写，如 data:image/png;base64,{base64_image}。​
# 素材 ID：用于视频生成的预置素材及虚拟人像的 ID，遵循格式 asset://<ASSET_ID>。
# 支持 jpeg、png、webp、bmp、tiff、gif、heic、heif。宽和高各为 300–6000 像素，宽/高为 0.4–2.5（均含边界）。
# 每张原图须小于 30 MB。Base64 编码后的完整 JSON 请求体最多 64 MB，大文件宜用公网 URL 或素材 ID。
# 首帧图含真人人脸时，可用预置人像图片、本人认证并授权入库的素材，或平台支持的模型原始图片。
image_source = "https://img.shetu66.com/2023/07/14/1689320796087949.png"

# ===============================================================
# 步骤4: 配置请求参数
# ===============================================================

payload = {
    # 【content】(object[], 必填) 输入内容列表。
    # 放 1 张首帧图片，可附 1 条提示词描述接下来的动作。图片的 role 可省略或填 first_frame。
    "content": [
        {
            # 【text】(string, 文本项内必填) 带素材时可省略整个文本项。
            # 图片确定起始画面。文本可描述从该画面开始要发生的动作、运镜和声音。
            # 支持中文、英语、西班牙语、印度尼西亚语、葡萄牙语、日语、马来语、泰语、阿拉伯语、越南语和韩语。
            # 建议中文提示词不超过 500 字、英文不超过 1000 词，过长时模型可能忽略部分细节。
            "text": "图中小狗在跳舞",

            # 【type】(string, 必填) 内容类型，此处固定为 text
            "type": "text",
        },
        {
            # 【image_url】(object, 当 type="image_url" 时必填) 首帧图片。
            # 【image_url.url】(string, 必填) 填上方的图片来源。脚本会将本地图片路径转换为 data URI。
            "image_url": {"url": image_source},

            # 【role】(string, 可选) 首帧填 first_frame，也可以不填
            "role": "first_frame",

            # 【type】(string, 必填) 内容类型，此处固定为 image_url
            "type": "image_url",
        },
    ],

    # 【duration】(integer, 可选，默认 -1) 输出视频的目标时长，单位为秒。
    # 可填 4–30（含边界）的整数。省略或填 -1 时，由模型根据内容在该范围内选择整数秒。
    "duration": 10,

    # 【generate_audio】(boolean, 可选，默认 True) 是否生成与画面同步的声音。
    # True 时生成与首帧之后的动作同步的双声道音轨。可在提示词里描述环境音，或用双引号写出台词。
    # False 输出无声视频。
    "generate_audio": True,

    # 【model】(string, 必填) doubao-seedance-2-5-flash-261115 的完整模型 ID。
    "model": "doubao-seedance-2-5-flash-261115",

    # 【output_format】(string, 可选，默认 "mp4") 输出视频的容器格式。
    # mp4：通用格式，兼容性最好，采用标准色彩精度，可在网页、移动端、各类播放器及分发平台直接播放。​
    # mov：面向专业场景的高色彩精度格式，更好地保持画面色彩与亮度一致性、适用于调色、抠像、合成等对色彩还原要求高的专业后期加工。推荐在视频编辑、视频延长场景使用 mov 格式作为输入和输出。
    "output_format": "mp4",

    # 【ratio】(string, 可选，默认 "adaptive") 输出视频的宽高比（宽与高之比）。
    # 此字段只能省略或填 "adaptive"，成片跟随首帧图的宽高比。
    # 想要竖屏时使用竖版首帧。例如，首帧图为 9:16，成片也为 9:16。
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


def _resolve_media(value, field):
    """公网 URL 和 asset:// 原样使用，本地图片转成 data URI。"""
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field} 不能为空")
    value = value.strip()
    if value.startswith(("http://", "https://", "asset://", "data:")):
        return value
    if not os.path.isfile(value):
        raise ValueError(f"{field} 找不到本地文件：{value}")
    mime = _IMAGE_MIME.get(os.path.splitext(value)[1].lower())
    if mime is None:
        raise ValueError(f"{field} 图片格式不支持")
    if os.path.getsize(value) >= 30 * 1024 * 1024:
        raise ValueError(f"{field} 图片须小于 30MB")
    with open(value, "rb") as file:
        encoded = base64.b64encode(file.read()).decode("ascii")
    return f"data:{mime};base64,{encoded}"


for item in payload["content"]:
    if item.get("type") == "image_url":
        item["image_url"]["url"] = _resolve_media(item["image_url"]["url"], "首帧图片")

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
  "id": "task_kcF9kG5VINsa1xPG4H9vq6YxdAQTynRx"
}
```

## 获取生成视频 示例代码

运行下面的 Python 代码。任务排队（`queued`）或生成中（`running`）时，每隔 15 秒查询一次。到达终态后，脚本会打印格式化的 JSON。

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

task_id = "task_kcF9kG5VINsa1xPG4H9vq6YxdAQTynRx"  # 替换为刚才保存的 id
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
    "video_url": "https://ark-acg-cn-beijing.tos-cn-beijing.volces.com/doubao-seedance-2-5-flash/2112844032/Video/vl9kv-33136142116202-tgc_f4e1df72fd51caffff00000000000000000000916990905597120/cgt-20261124163133-vk9lv.mp4?X-Tos-Algorithm=TOS4-HMAC-SHA256&X-Tos-Credential=AKLTYWJkZTExNjA1ZDUyNDc3YzhjNTM5OGIyNjBhNDcyOTQ%2F20261124%2Fcn-beijing%2Ftos%2Frequest&X-Tos-Date=20261124T083222Z&X-Tos-Expires=86400&X-Tos-Max-Requests=100&X-Tos-Signature=c8138c6dc8996c646147f07de1328346e2426c245aaf2d1cdac4f5b1b62e477f&X-Tos-SignedHeaders=host"
  },
  "created_at": 1795509098,
  "draft": false,
  "duration": 10,
  "execution_expires_after": 172800,
  "framespersecond": 24,
  "generate_audio": true,
  "id": "task_kcF9kG5VINsa1xPG4H9vq6YxdAQTynRx",
  "model": "doubao-seedance-2-5-flash-261115",
  "output_format": "mp4",
  "priority": 0,
  "ratio": "265:397",
  "resolution": "480p",
  "seed": 71304,
  "service_tier": "default",
  "status": "succeeded",
  "updated_at": 1795509145,
  "usage": {
    "completion_tokens": 99040,
    "total_tokens": 99040
  }
}
```

<p align="center">
  <small>© 2026 DMXAPI doubao-seedance-2-5-flash 首帧图生视频</small>
</p>
