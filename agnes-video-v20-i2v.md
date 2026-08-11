# Agnes Video V2.0 图生视频 API 文档

Agnes Video V2.0 是面向生产场景的视频生成模型，图生视频功能可基于输入图片生成动态视频。采用异步任务模式：先提交任务创建视频生成请求，再通过任务 ID 查询获取视频结果。

## 🎬 模型名称

| 用途 | 模型名称 |
|------|---------|
| 提交任务 | `agnes-video-v2.0` |
| 获取结果 | `agnes-video-get` |

## 🔗 接口地址

| 接口 | 请求方式 | URL |
|------|---------|-----|
| 提交任务 | POST | `https://www.dmxapi.cn/v1/videos` |
| 获取结果 | GET | `https://www.dmxapi.cn/v1/videos/<TASK_ID>?model=agnes-video-get` |



## 🎥 提交任务 示例代码

```python
"""
┌─────────────────────────────────────────────────────────────────┐
│  Agnes Video V2.0 图生视频 API 调用示例 - 提交任务                 │
│                                                                 │
│  功能说明：基于输入图片提交视频生成任务，返回任务 ID                │
└─────────────────────────────────────────────────────────────────┘
"""

import json
import requests

# ═══════════════════════════════════════════════════════════════════════════════
#  第一部分：用户配置区（按需修改以下内容）
# ═══════════════════════════════════════════════════════════════════════════════

# 接口地址
url = "https://www.dmxapi.cn/v1/videos"

# 请求头（请替换为你自己的 DMXAPI 密钥）
headers = {
    "Content-Type": "application/json",
    "Authorization": "sk-**********************************"
}

# 请求体
data = {
    # 模型名称
    "model": "agnes-video-v2.0",

    # 视频内容描述（描述期望的画面运动与镜头效果）
    "prompt": "The woman slowly turns around and looks back at the camera, natural facial expression, cinematic camera movement",

    # 输入图片 URL（视频将以此图为基础生成）
    "image": "https://example.com/image.png",

    # 视频宽度（默认 1152）
    "width": 1152,

    # 视频高度（默认 768）
    "height": 768,

    # 总帧数（最大 441，须满足 8n+1 规则，如 25、121、241）
    # 视频时长（秒）= num_frames / frame_rate，121 ÷ 24 ≈ 5 秒
    "num_frames": 121,

    # 帧率（取值范围 1-60）
    "frame_rate": 24
}

# ═══════════════════════════════════════════════════════════════════════════════
#  第二部分：请求逻辑（以下内容无需修改）
# ═══════════════════════════════════════════════════════════════════════════════

# 发送 POST 请求到 API
response = requests.post(url, headers=headers, json=data)

# 输出响应信息（task_id 用于下一步查询视频结果）
print(f"状态码: {response.status_code}")
print(f"响应内容:\n{json.dumps(response.json(), indent=2, ensure_ascii=False)}")
```

##  返回示例

```json
状态码: 200
响应内容:
{
  "id": "task_Imy7KsBBnNgdGEIZciCErv9WJ1oSZKib",
  "task_id": "task_Imy7KsBBnNgdGEIZciCErv9WJ1oSZKib",
  "object": "video",
  "model": "agnes-video-v2.0",
  "status": "queued",
  "progress": 0,
  "created_at": 1784887385,
  "seconds": "5.0",
  "size": "1152x768"
}
```

## 📥 获取视频 示例代码

```python
"""
┌─────────────────────────────────────────────────────────────────┐
│  Agnes Video V2.0 图生视频 API 调用示例 - 获取视频                 │
│                                                                 │
│  功能说明：根据任务 ID 自动轮询视频生成状态（每 30 秒查询一次），    │
│  完成后输出视频下载链接                                            │
└─────────────────────────────────────────────────────────────────┘
"""

import json
import time
import requests

# ═══════════════════════════════════════════════════════════════════════════════
#  第一部分：用户配置区（按需修改以下内容）
# ═══════════════════════════════════════════════════════════════════════════════

# 任务 ID（请替换为提交任务返回的 task_id）
task_id = "task_Imy7KsBBnNgdGEIZciCErv9WJ1oSZKib"

# 接口地址（model=agnes-video-get 为获取结果的模型名，需保留）
url = f"https://www.dmxapi.cn/v1/videos/{task_id}?model=agnes-video-get"

# 请求头（请替换为你自己的 DMXAPI 密钥）
headers = {
    "Authorization": "sk-**********************************"
}

# 轮询间隔（秒）
poll_interval = 30

# ═══════════════════════════════════════════════════════════════════════════════
#  第二部分：请求逻辑（以下内容无需修改）
# ═══════════════════════════════════════════════════════════════════════════════

# 自动轮询任务状态，直到完成或失败
# 状态枚举：queued(排队中) / in_progress(生成中) / completed(已完成) / failed(失败)
while True:
    response = requests.get(url, headers=headers)
    result = response.json()
    status = result.get("status")

    if status == "completed":
        print(f"响应内容:\n{json.dumps(result, indent=2, ensure_ascii=False)}")
        video_url = result.get("metadata", {}).get("url", "")
        print(f"\n视频链接: {video_url}")
        break
    elif status == "failed":
        print(f"响应内容:\n{json.dumps(result, indent=2, ensure_ascii=False)}")
        print("\n任务失败，请检查参数后重新提交")
        break
    else:
        print(f"任务进行中（状态 {status}，进度 {result.get('progress', 0)}%），{poll_interval} 秒后再次查询...")
        time.sleep(poll_interval)
```

##  返回示例

```text
任务进行中（状态 in_progress，进度 30%），30 秒后再次查询...
任务进行中（状态 in_progress，进度 30%），30 秒后再次查询...
任务进行中（状态 in_progress，进度 30%），30 秒后再次查询...
任务进行中（状态 in_progress，进度 30%），30 秒后再次查询...
任务进行中（状态 in_progress，进度 30%），30 秒后再次查询...
任务进行中（状态 in_progress，进度 30%），30 秒后再次查询...
任务进行中（状态 in_progress，进度 30%），30 秒后再次查询...
任务进行中（状态 in_progress，进度 30%），30 秒后再次查询...
任务进行中（状态 in_progress，进度 30%），30 秒后再次查询...
任务进行中（状态 in_progress，进度 30%），30 秒后再次查询...
任务进行中（状态 in_progress，进度 30%），30 秒后再次查询...
响应内容:
{
  "id": "task_5uQYhCUJPpcg9NS80iMk5orRvDEKLm70",
  "size": "1088x832",
  "model": "agnes-video-v2.0",
  "object": "video",
  "status": "completed",
  "seconds": "10.0",
  "task_id": "task_FXF2jUmCVq8lDhqFjFKeZ5AzVX4GGKkP",
  "metadata": {
    "url": "https://plat.....KkP.mp4",
    "size_mapping": {
      "ratio": "4:3",
      "width": 1088,
      "height": 832,
      "message": "Input size 1152x768 was mapped to nearest preset 720p/4:3 (1088x832)",
      "adjusted": true,
      "resolution": "720p",
      "requested_width": 1152,
      "requested_height": 768
    }
  },
  "progress": 100,
  "video_id": "task_FXF2jUmCVq8lDhqFjFKeZ5AzVX4GGKkP",
  "created_at": 1784889330,
  "completed_at": 1784889672
}

视频链接: https://platform-output...zVX4GGKkP.mp4
```

<p align="center">
  <small>© 2026 DMXAPI Agnes Video V2.0 图生视频 API 文档</small>
</p>
