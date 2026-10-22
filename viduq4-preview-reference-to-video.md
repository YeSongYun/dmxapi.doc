# Vidu Q4 Preview 参考生视频 API 使用文档

基于 Vidu 最新旗舰模型（预览版）viduq4-preview 的参考生视频接口，通过 DMXAPI 网关以三步异步方式调用（提交任务 → 轮询查询 → 下载产物）。支持 1~15 张参考图与 0~3 条参考音频（mp3 格式，每条 3-12 秒），模型以传入图片中的主题为参考生成具备主体一致性的视频，并可通过必填提示词编排多参考图之间的场景与对白。模型支持音画同出（含台词和音效），视频时长 3-16 秒，画幅比例支持 1:1 / 9:16 / 16:9 / 3:4 / 4:3 共 5 种，分辨率覆盖 540p / 720p / 1080p / 2K / 4K 五档，另支持 AI 水印（位置可选）、任务状态回调与透传参数，适用于角色动画、多主体剧情短片、创意内容等需要保持主体一致的视频生成场景。

## 接口地址

| 接口 | 请求方式 | URL |
|------|---------|-----|
| 提交任务 | POST | `https://www.dmxapi.cn/vidu-q4-preview/v1/reference-to-video` |
| 查询任务 | GET | `https://www.dmxapi.cn/vidu-q4-preview/v1/reference-to-video/{task_id}` |

:::warning
请妥善保管您的 API Key！严禁将密钥泄露给他人、硬编码到代码中或提交到公开的代码仓库。如果怀疑密钥已泄露，请立即前往 DMXAPI 官网重新生成。
:::

## 模型名称

- `viduq4-preview`

## 参考生视频 示例代码

```python
import requests
import json

# 步骤1: 配置 API 连接信息

# DMXAPI 服务端点地址（参考生视频提交接口，DMXAPI 网关原生路由）
url = "https://www.dmxapi.cn/vidu-q4-preview/v1/reference-to-video"

# DMXAPI 密钥，请替换为您自己的密钥
# 获取方式: 登录 DMXAPI 官网 -> 个人中心 -> API 密钥管理
api_key = "sk-******************************************"

# 步骤2: 配置请求头

headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {api_key}",
}

# 步骤3: 配置请求参数

payload = {
    # 【model】(string, 必填) 模型名称。
    # 当前文档使用 viduq4-preview：Vidu 最新旗舰模型预览版，支持参考 1-15 张图片，支持参考 0-3 个音频。
    "model": "viduq4-preview",

    # 【prompt】(string, 必填) 生成视频的文本描述。
    # 字符长度不能超过 20000 个字符；可通过提示词编排多参考图之间的场景与对白。
    # 官方示例（原样保留，仅供参考）:
    # "在参考图1的场景中，参考图2使用参考音频1，对参考图3说：“你在干什么？”，参考图3激动地说：“q4大卖！！！”"
    "prompt": "在参考图的场景中，人物面向镜头挥手并说：“你好”。",

    # 【images】(array, 必填) 参考图片。
    # 模型将以传入图片中的主题为参考生成具备主体一致的视频；viduq4-preview 支持上传 1~15 张图片。
    # 支持图片 Base64 编码或可访问的图片 URL；图片格式支持 png、jpeg、jpg、webp，图片最大 50MB。
    # 使用 Base64 时，HTTP POST body 不超过 20MB，且编码需要包含适当的内容类型字符串，例如 data:image/png;base64,{base64_encode}。
    "images": [
        "https://prod-ss-images.s3.cn-northwest-1.amazonaws.com.cn/vidu-maas/template/reference2video-1.png",
        "https://prod-ss-images.s3.cn-northwest-1.amazonaws.com.cn/vidu-maas/template/reference2video-2.png",
        "https://prod-ss-images.s3.cn-northwest-1.amazonaws.com.cn/vidu-maas/template/reference2video-3.png",
    ],

    # 【sounds】(array, 可选) 参考音频。
    # 支持上传 0~3 个音频，模型将以传入的音频作为参考生成具备主体一致的视频。
    # 每个参考音频时长范围 3-12 秒；音频支持 mp3 格式；每个音频文件大小不超过 50MB。
    # 使用 Base64 时，HTTP POST body 不超过 20MB，且编码需要包含适当的内容类型字符串，例如 data:audio/mpeg;base64,{base64_encode}。
    # 官方示例: ["reference_sound_url1", "reference_sound_url2", "reference_sound_url3"]
    "sounds": [],

    # 【audio】(bool, 可选) 是否使用音视频直出能力。
    # false 表示输出静音视频，true 表示需要音画同步并输出有声视频（包括台词和音效）；默认值为 true。
    "audio": True,

    # 【duration】(int, 可选) 视频时长参数，单位秒。
    # 取值范围为 3-16 秒，默认值为 5。
    "duration": 3,

    # 【aspect_ratio】(string, 可选) 视频比例参数。
    # 可选值: "1:1" / "9:16" / "16:9" / "3:4" / "4:3"；默认值为 "16:9"。
    "aspect_ratio": "16:9",

    # 【resolution】(string, 可选) 视频分辨率参数。
    # 可选值: "540p" / "720p" / "1080p" / "2K" / "4K"；默认值为 "720p"。
    "resolution": "540p",

    # 【seed】(int, 可选) 随机种子。
    # 默认不传或传 0 时，会使用随机数替代；手动设置时使用指定种子。
    "seed": 0,

    # 【payload】(string, 可选) 透传参数，不做任何处理，仅数据传输。
    # 最多 1048576 个字符。
    "payload": "",

    # 【callback_url】(string, 可选) 任务状态变化回调地址。
    # 创建任务时主动设置 callback_url 后，当视频生成任务状态变化时，Vidu 将向该地址发送 POST 回调请求。
    # 回调请求内容结构与查询任务 API 的返回体一致；回调状态包括: processing=任务处理中，success=任务完成，failed=任务失败；发送失败时会回调三次。
    "callback_url": "",

    # 【watermark】(bool, 可选) 是否添加水印。
    # true 表示添加水印，false 表示不添加水印；默认值为 true；官方说明目前水印内容固定，内容由 AI 生成。
    "watermark": False,

    # 【wm_position】(int, 可选) 水印位置。
    # 可选值: 1=左上角，2=右上角，3=右下角，4=左下角；默认值为 3。
    "wm_position": 3,

    # 【wm_url】(string, 可选) 水印内容图片 URL。
    # 不传或为空时，使用默认水印：内容由 AI 生成。
    "wm_url": "",

    # 【meta_data】(string, 可选) 元数据标识，JSON 格式字符串，透传字段，可自定义格式或使用官方示例格式。
    # 该参数为空时，默认使用 Vidu 生成的元数据标识。
    # "meta_data": '{"Label":"your_label","ContentProducer":"yourcontentproducer","ContentPropagator":"your_content_propagator","ProduceID":"yourproductid","PropagateID":"your_propagate_id","ReservedCode1":"yourreservedcode1","ReservedCode2":"your_reserved_code2"}',
}

# 步骤4: 发送请求并输出结果

response = requests.post(url, headers=headers, json=payload)

print(json.dumps(response.json(), indent=2, ensure_ascii=False))
```

## 提交任务 返回示例

```json
{
  "aspect_ratio": "16:9",
  "created_at": "2026-10-21T15:22:27.074137616Z",
  "duration": 3,
  "images": [
    "https://prod-ss-images.s3.cn-northwest-1.amazonaws.com.cn/vidu-maas/template/reference2video-1.png",
    "https://prod-ss-images.s3.cn-northwest-1.amazonaws.com.cn/vidu-maas/template/reference2video-2.png",
    "https://prod-ss-images.s3.cn-northwest-1.amazonaws.com.cn/vidu-maas/template/reference2video-3.png"
  ],
  "is_rec": false,
  "meta_data": "",
  "model": "viduq4-preview",
  "payload": "",
  "prompt": "在参考图的场景中，人物面向镜头挥手并说：“你好”。",
  "resolution": "540p",
  "seed": 1060333279,
  "state": "created",
  "task_id": "task_gM0h4M3I3IeHbax73wBKtHI4kDtNO7Vd",
  "watermark": false,
  "wm_url": ""
}
```

## 查询任务并下载视频 示例代码

```python
"""
================================================================================
DMXAPI Vidu Q4 Preview 视频生成任务查询与下载脚本
================================================================================

功能说明:
    本脚本用于轮询查询 Vidu Q4 Preview 视频生成任务的状态，
    任务成功后通过 DMXAPI 网关产物接口获取下载地址并保存视频文件。
依赖库:
    - requests: HTTP 请求库，用于发送 API 请求
    - json: JSON 解析库，用于处理响应数据

================================================================================
"""

import requests  # HTTP 请求库 - 用于发送网络请求
import json      # JSON 处理库 - 用于解析 API 响应数据
import time      # 时间处理库 - 用于轮询间隔与超时控制
from pathlib import Path  # 路径处理库 - 用于保存视频文件

# ╔════════════════════════════════════════════════════════════════════════════╗
# ║                           第一部分: API 连接配置                              ║
# ╚════════════════════════════════════════════════════════════════════════════╝
#
# 说明: 此部分配置 API 服务器地址、身份验证信息和轮询参数
#       请确保 API 密钥的安全性，不要泄露给他人
#

# API 服务端点地址
base_url = "https://www.dmxapi.cn"

# API 密钥 (API Key)
# - 用途: 身份验证，确保只有授权用户可以访问 API
# - 格式: 以 "sk-" 开头的字符串
# - 注意: 请妥善保管，不要将密钥提交到公开代码仓库
api_key = "sk-***********************************************"

# 任务类型
# - 可选值: "image_to_video"(图生视频) / "reference_to_video"(参考生视频)
# - 用于拼接对应的原生查询接口路径，需与提交任务时使用的接口一致
task_type = "reference_to_video"

# 要查询的任务 ID
# - 此 ID 由创建任务时返回（提交任务响应中的 task_id）
# - 请替换为您实际的任务 ID
task_id = "task_gM0h4M3I3IeHbax73wBKtHI4kDtNO7Vd"

# 轮询配置
# - poll_interval: 每次查询的间隔时间（秒）
# - max_wait_seconds: 轮询总超时时间（秒），超时后停止等待
poll_interval = 10
max_wait_seconds = 1800

# 视频保存目录
output_dir = Path("viduq4_outputs")

# task_type 到查询接口路径的映射
TASK_TYPE_QUERY_SEGMENT = {
    "image_to_video": "image-to-video",
    "reference_to_video": "reference-to-video",
}

# ╔════════════════════════════════════════════════════════════════════════════╗
# ║                          第二部分: HTTP 请求头配置                            ║
# ╚════════════════════════════════════════════════════════════════════════════╝
#
# 说明: HTTP 请求头用于告知服务器请求的格式和认证信息
#       这是 RESTful API 调用的标准配置
#

headers = {
    # Authorization: 身份验证头
    # - 认证方案: Bearer 令牌认证方式
    # - 服务器通过此字段验证请求者身份
    "Authorization": f"Bearer {api_key}",
}

# ╔════════════════════════════════════════════════════════════════════════════╗
# ║                       第三部分: 轮询查询任务状态                              ║
# ╚════════════════════════════════════════════════════════════════════════════╝
#
# 说明: 视频生成为异步任务，提交成功后需定期查询任务状态
#       state 为 created / queueing / processing 时继续等待
#       state 为 success 时查询完成，failed 时任务失败
#

# 拼接查询接口地址
query_url = f"{base_url}/vidu-q4-preview/v1/{TASK_TYPE_QUERY_SEGMENT[task_type]}/{task_id}"

print("=" * 60)
print("🚀 开始轮询查询任务状态...")
print("=" * 60)

start_time = time.time()
while True:
    # 发送 GET 请求查询任务最新状态
    response = requests.get(query_url, headers=headers)
    result = response.json()
    state = result.get("state", "")

    # 任务成功: 打印结果并退出轮询
    if state == "success":
        print("✅ 视频生成完成！")
        print(json.dumps(result, indent=2, ensure_ascii=False))
        break

    # 任务失败: 输出错误信息并终止
    if state == "failed":
        raise RuntimeError(f"❌ 任务失败: {result.get('err_code') or result}")

    # 超时判断: 超过最长等待时间则停止轮询
    if time.time() - start_time > max_wait_seconds:
        raise TimeoutError(f"❌ 任务轮询超时（{max_wait_seconds} 秒）")

    # 任务仍在进行中: 等待后再次查询
    print(f"当前状态: {state}，{poll_interval} 秒后再次查询...")
    time.sleep(poll_interval)

# ╔════════════════════════════════════════════════════════════════════════════╗
# ║                       第四部分: 下载视频产物                                  ║
# ╚════════════════════════════════════════════════════════════════════════════╝
#
# 说明: 任务成功后，通过网关产物接口获取视频下载地址并保存到本地
#       注意: 查询返回 creations 中的 url / cover_url / watermarked_url
#             均只有 24 小时有效期，请及时下载保存
#

# 请求产物列表接口
artifacts_url = f"{base_url}/v1/tasks/{task_id}/artifacts"
response = requests.get(artifacts_url, headers=headers)
artifacts = response.json().get("artifacts", [])

# 从产物列表中选取视频下载地址（优先 key 为 video 的产物）
content_url = None
for item in artifacts:
    if item.get("key") == "video" and item.get("content_url"):
        content_url = item["content_url"]
        break
if content_url is None and artifacts:
    content_url = artifacts[0].get("content_url")
if not content_url:
    raise RuntimeError("❌ 产物列表中没有可下载的视频地址")

# 下载视频并保存到输出目录
output_dir.mkdir(parents=True, exist_ok=True)
output_path = output_dir / f"{task_type}_{task_id}.mp4"

video_response = requests.get(content_url, headers=headers, stream=True)
with output_path.open("wb") as output_file:
    for chunk in video_response.iter_content(chunk_size=1024 * 1024):
        if chunk:
            output_file.write(chunk)

print(f"💾 视频已保存到: {output_path}")
```

## 查询与下载 返回示例

轮询过程控制台输出：

```text
============================================================
🚀 开始轮询查询任务状态...
============================================================
当前状态: processing，10 秒后再次查询...
✅ 视频生成完成！
```

任务成功后查询接口返回：

```json
{
  "creations": [
    {
      "cover_url": "https://prod-ss-vidu.s3.oss-cn-beijing.aliyuncs.com/infer_60/tasks/26/1021/15/1010511147364802560/creation-01/cover.jpeg?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=***&X-Amz-Date=20261021T152523Z&X-Amz-Expires=86400&X-Amz-SignedHeaders=host&x-id=GetObject&X-Amz-Signature=***",
      "id": "1010511803899203584",
      "url": "https://prod-ss-vidu.s3.oss-cn-beijing.aliyuncs.com/infer_60/tasks/26/1021/15/1010511147364802560/creation-01/video.mp4?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=***&X-Amz-Date=20261021T152523Z&X-Amz-Expires=86400&X-Amz-SignedHeaders=host&x-id=GetObject&X-Amz-Signature=***",
      "watermarked_url": ""
    }
  ],
  "err_code": "",
  "id": "task_gM0h4M3I3IeHbax73wBKtHI4kDtNO7Vd",
  "payload": "",
  "state": "success"
}
```

视频产物下载保存：

```text
💾 视频已保存到: viduq4_outputs/reference_to_video_task_gM0h4M3I3IeHbax73wBKtHI4kDtNO7Vd.mp4
```

<p align="center">
  <small>© 2026 DMXAPI Vidu Q4 Preview 参考生视频</small>
</p>
