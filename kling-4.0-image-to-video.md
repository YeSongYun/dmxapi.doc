# kling-4.0 图生视频 API 使用文档

基于可灵 Kling 4.0 的图生视频接口，通过 DMXAPI 网关以异步任务方式调用。用首帧、中间帧、尾帧控制画面，一次最多 10 张图；提示词写在 `contents` 里，没有最外层 `prompt`，也没有 `aspect_ratio`。时长为 3～30 秒的整数，分辨率支持 720p / 1080p。提交后立即返回网关任务 ID，再用该 ID 查询视频地址。

本接口只用关键帧。要传参考视频、主体或其他参考图，请改用全能参考生视频。

## 接口地址

| 接口 | 请求方式 | URL |
|------|---------|-----|
| 提交任务 | POST | `https://www.dmxapi.cn/image-to-video/kling-4.0` |
| 获取结果 | GET | `https://www.dmxapi.cn/tasks` |

:::warning
请妥善保管您的 API Key！严禁将密钥泄露给他人、硬编码到代码中或提交到公开的代码仓库。如果怀疑密钥已泄露，请立即前往 DMXAPI 官网重新生成。
:::

## 模型名称

- `kling-4.0`

## 图生视频示例代码

```python
import requests
import json

# ===============================================================
# 步骤1: 配置 API 连接信息
# ===============================================================

# DMXAPI Kling 4.0 图生视频接口
url = "https://www.dmxapi.cn/image-to-video/kling-4.0"

# DMXAPI 密钥 (请替换为您自己的密钥)
# 获取方式: 登录 DMXAPI 官网 -> 个人中心 -> API 密钥管理
api_key = "sk-***********************************************"

# ===============================================================
# 步骤2: 配置请求头
# ===============================================================

headers = {
    "Content-Type": "application/json",       # 指定请求体为 JSON 格式
    "Authorization": f"Bearer {api_key}",     # Bearer 认证
}

# ===============================================================
# 步骤3: 配置请求参数
# ===============================================================

payload = {
    # 【model】(string, 必填) 模型名称，固定为 kling-4.0
    "model": "kling-4.0",

    # 【contents】(array, 必填) 提示词和关键帧。没有最外层 prompt，也没有 aspect_ratio
    # 图片 type 只能是 first_frame、middle_frame、last_frame
    # 同时传三种帧时，数组顺序必须是首帧、中间帧、尾帧；多张中间帧按它们在成片中出现的顺序排列
    # 最多 10 张图。建议给每张图设置 id，并在提示词里用 @id 按同样顺序说明每张图的作用
    # 图片对象分别设置为 "id": "frame_1"、"id": "frame_2"、"id": "frame_3"，即可通过 @frame_1、@frame_2、@frame_3 引用。同时，关键帧图片传入顺序，需与引用顺序一致。
    "contents": [
        {
            # 【type】(string, 必填) 提示词固定为 prompt
            "type": "prompt",
            # 【text】(string, 必填) 描述动作、运镜，以及帧与帧之间如何过渡
            # 纯英文最多 26000 个字符；不是纯英文时最多 11000 个字符
            # 中英混合须满足：英文字符数 / 26000 + 非英文字符数 / 11000 ≤ 1
            "text": "图里的水果变身为机甲",
        },
        {
            # 【type】(string, 必填) 首帧固定为 first_frame，还可使用 middle_frame、last_frame
            "type": "first_frame",
            # 【url】(string, 必填) jpg、jpeg 或 png
            # 可以填图片网址，也可以填 data:image/jpeg;base64, 或 data:image/png;base64, 开头的 data URL
            # 不能只贴一段裸的 Base64
            # 单张不超过 30MB，宽和高都不小于 300px，宽高比在 2:5 到 5:2 之间
            "url": "https://cdn.jsdelivr.net/gh/opencv/opencv/samples/data/fruits.jpg",
            # 【id】(string, 可选) 提示词里用 @image_1 引用；同一请求内不能重复
            "id": "image_1",
        },
    ],

    # 【settings】(object, 可选) 视频生成设置。图生视频不要传 aspect_ratio
    "settings": {
        # 【duration】(integer, 可选) 3 到 30 的整数，单位秒
        # 传入后优先于提示词里写的时长
        # 不传时，若提示词里有明确时长则采用该时长，否则默认 10 秒
        "duration": 5,
        # 【resolution】(string, 可选) 仅支持 720p 或 1080p，默认 1080p
        "resolution": "720p",
    },

    # 【options】(object, 可选) 任务选项
    "options": {
        # 【watermark_info.enabled】(boolean, 可选) 是否同时生成带水印的结果，默认 false
        "watermark_info": {"enabled": False},
    },
}

# ===============================================================
# 步骤4: 发送请求并输出结果
# ===============================================================

response = requests.post(url, headers=headers, json=payload)
print("status:", response.status_code)
result = response.json()
print(json.dumps(result, indent=2, ensure_ascii=False))

# 异步任务的网关 task_id 在 result["data"]["id"]，交给下面的视频任务查询
data = result.get("data") if isinstance(result, dict) else None
if isinstance(data, dict):
    print("task_id:", data.get("id"))

response.raise_for_status()
```

## 返回示例

```json
{
  "code": 0,
  "message": "SUCCEED",
  "request_id": "91de40aa-2c77-4b18-a6e0-55f0c1890d34",
  "data": {
    "id": "task_RZlT1eybOQHadzUuWjc2h16j4raRovqa",
    "status": "submitted",
    "create_time": 1768000000000,
    "update_time": 1768000000000,
    "external_id": ""
  }
}
```


## 获取生成视频 示例代码

```python
import requests
import json
import time

# ===============================================================
# 步骤1: 配置 API 连接信息
# ===============================================================

# DMXAPI Kling 4.0 视频任务查询接口
# 文生视频、图生视频、全能参考生视频共用此接口
url = "https://www.dmxapi.cn/tasks"

# DMXAPI 密钥 (请替换为您自己的密钥)
api_key = "sk-***********************************************"

# ===============================================================
# 步骤2: 配置请求头
# ===============================================================

headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {api_key}",
}

# ===============================================================
# 步骤3: 配置请求参数
# ===============================================================

params = {
    # 【task_ids】(string, 必填) 填写视频创建接口返回的 data.id
    # 与 external_task_ids 二选一，不能同时传
    # 支持英文逗号分隔的批量查询；本示例每次只查一个任务
    "task_ids": "task_RZlT1eybOQHadzUuWjc2h16j4raRovqa",
}

# ===============================================================
# 步骤4: 轮询直到任务结束
# ===============================================================

# 查询接口会立刻返回当前状态。视频仍在生成时 status 为 submitted 或 processing。
# 每 25 秒查询一次，最多等待 600 秒；等待期间不打印，结束后只输出一次。
# 视频任务成功状态是 succeeded。失败时看该条记录的 message。
end_time = time.time() + 600
while time.time() < end_time:
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    result = response.json()
    data = result.get("data") if isinstance(result, dict) else None
    record = data[0] if isinstance(data, list) and data else data
    record = record if isinstance(record, dict) else {}
    status = str(record.get("status") or record.get("task_status") or "").lower()
    if status in {"succeeded", "succeed", "failed", "cancelled", "timed_out"}:
        break
    time.sleep(25)
else:
    raise TimeoutError("视频任务在 600 秒内没有结束")

print("status:", response.status_code)
print(json.dumps(result, indent=2, ensure_ascii=False))

# 成功时，视频地址在 data[0].outputs 里 type 为 video 的 url
# 地址带防盗链，生成结果保留 30 天，请及时转存
outputs = record.get("outputs") if isinstance(record.get("outputs"), list) else []
for item in outputs:
    if isinstance(item, dict) and item.get("type") == "video" and item.get("url"):
        print("video_url:", item.get("url"))
```

## 返回示例

```json
{
  "code": 0,
  "message": "SUCCEED",
  "data": [
    {
      "id": "task_RZlT1eybOQHadzUuWjc2h16j4raRovqa",
      "status": "succeeded",
      "message": "",
      "create_time": 1768000000000,
      "update_time": 1768001800000,
      "external_id": "",
      "outputs": [
        {
          "type": "video",
          "id": "893605946402811986",
          "url": "https://cdn.example.com/kling/image-to-video.mp4",
          "watermark_url": "",
          "duration": "5"
        }
      ],
      "usage": {
        "output_duration": "5"
      }
    }
  ]
}
```

`outputs[].url` 是成片地址。计费使用的输出时长看 `usage.output_duration`，单位秒。生成结果保留 30 天。

<p align="center">
  <small>© 2026 DMXAPI Kling-4.0 图生视频</small>
</p>
