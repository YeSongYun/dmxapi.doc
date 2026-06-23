# PixVerse-V6 首尾帧生视频 API 使用文档

PixVerse-V6 首尾帧生视频 API 支持通过指定起始帧和结束帧图片，由 AI 自动生成中间过渡动画，实现流畅的视频转场效果。接口采用异步两步模式：提交任务后获取 `video_id`，再通过 `video_id` 轮询获取最终视频链接。v6/c1 模型支持 1~15 秒任意时长，最高 1080p 画质，并可选开启 AI 音效生成功能。

## 模型名称

- `PixVerse-V6`

## 接口地址

| 接口 | 请求方式 | URL |
|------|---------|-----|
| 提交任务 | POST | `https://www.dmxapi.cn/v1/responses` |
| 获取结果 | POST | `https://www.dmxapi.cn/v1/responses` |

:::warning
使用本 API 前，请先完成前置依赖文档中的调用以获取所需的img_id。
本模型请使用 `pixverse-picture` 上传。

[图片上传](https://doc.dmxapi.cn/paiwo_image_upload.html)
:::

## 首尾帧生视频 示例代码

```python
import requests
import json

# 步骤1: 配置 API 连接信息

# DMXAPI 服务端点地址
url = "https://www.dmxapi.cn/v1/responses"

# DMXAPI 密钥 (请替换为您自己的密钥)
api_key = "sk-******************************************"

# 步骤2: 配置请求头
headers = {
    "Content-Type": "application/json",
    "Authorization": f"{api_key}",
}

# 步骤3: 配置请求参数
payload = {
    # 【model】(string, 必填) 模型名称
    "model": "PixVerse-V6",

    # 【input】(string, 必填) 视频内容描述提示词
    # 2048 Characters 以内
    "input": "可爱的小猫在海边愉快的玩耍",

    # 【first_frame_img】(integer, 必填) 首帧图片 ID
    # 通过上传图片接口获取的 img_id，作为视频起始帧
    "first_frame_img": 177602101,

    # 【last_frame_img】(integer, 必填) 尾帧图片 ID
    # 通过上传图片接口获取的 img_id，作为视频结束帧
    "last_frame_img": 177602101,

    # 【duration】(integer, 必填) 视频生成时长（秒）
    # 1~15s 任意时长
    "duration": 5,

    # 【quality】(string, 必填) 输出视频分辨率
    # 可选值: "360p" / "540p" / "720p" / "1080p"
    "quality": "540p",

    # 【generate_audio_switch】(boolean, 可选) AI 音效开关
    # true: 开启音效生成，false: 关闭音效生成
    "generate_audio_switch": True,

    # 【seed】(integer, 可选) 随机种子值
    # 取值范围: 0~2147483647，相同 seed 值可复现生成结果
    "seed": 0,

    # 【motion_mode】(string, 可选) 运动模式
    # 可选值: "normal"（标准运动）/ "fast"（快速运动）
    # 注意: "fast" 不支持 8s 时长
    "motion_mode": "normal",
}

# 步骤4: 发送请求并输出结果
response = requests.post(url, headers=headers, json=payload)

print(json.dumps(response.json(), indent=2, ensure_ascii=False))
```

## 返回示例

```json
{
  "video_id": 401770462988288,
  "credits": 45,
  "usage": {
    "total_tokens": 135000,
    "input_tokens": 0,
    "input_tokens_details": {
      "cached_tokens": 0
    },
    "output_tokens": 135000,
    "output_tokens_details": {
      "reasoning_tokens": 0
    }
  }
}
```

> 返回的 `video_id` 即为任务 ID，用于第二步查询视频生成结果。

## 获取结果 示例代码

```python
import requests
import json
import time
import urllib.parse

url = "https://www.dmxapi.cn/v1/responses"

api_key = "sk-*******************************************"

headers = {
    "Content-Type": "application/json",
    "Authorization": f"{api_key}",
}

# 将第一步返回的 video_id 填入此处
video_id = 403969648419292

payload = {
    # 【model】(string, 必填) 查询模型名称，固定格式为提交模型名 + "-get"
    "model": "paiwo-get",

    # 【input】(string, 必填) 第一步提交任务返回的 video_id
    "input": str(video_id),
}

# 轮询查询视频生成状态
# status 含义: 5=排队/处理中, 1=生成完成 (以 outputWidth>0 作为辅助判定)
while True:
    response = requests.post(url, headers=headers, json=payload)
    result = response.json()

    resp = result.get("Resp", {}) or {}
    # 修复 URL 中被双重编码的斜杠 (%2F -> /)
    if resp.get("url"):
        resp["url"] = urllib.parse.unquote(resp["url"])

    print(json.dumps(result, indent=2, ensure_ascii=False))

    status = resp.get("status")
    video_url = resp.get("url")
    width = resp.get("outputWidth", 0)

    # status == 1 且已有真实分辨率 视为生成完成
    if status == 1 and video_url and width > 0:
        print(f"\n✅ 视频生成完成，链接: {video_url}")
        break

    print(f"视频生成中 (status={status})，5 秒后重试...")
    time.sleep(5)
```

## 返回示例

```json
{
  "video_url": "https://cdn.pixverseai.cn/videos/401770462988288.mp4",
  "video_id": 401770462988288,
  "status": "succeeded",
  "credits": 45,
  "usage": {
    "total_tokens": 135000,
    "input_tokens": 0,
    "output_tokens": 135000
  }
}
```

<p align="center">
  <small>© 2026 DMXAPI PixVerse-V6 首尾帧生视频</small>
</p>
