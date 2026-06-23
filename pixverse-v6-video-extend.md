# PixVerse-V6 视频延长 API 使用文档

PixVerse-V6 视频延长（Extend）API 支持对已有视频进行续写延长，通过提供源视频 ID 与提示词，驱动 V6 模型在原视频基础上生成连贯的延长内容。V6 模型支持 1~15 秒任意时长延长，提供 360p 至 1080p 四档画质选项，并可通过 motion_mode 控制运动速度。整体采用异步模式：提交任务后获取 video_id，再轮询查询获取最终视频链接。

## 模型名称

- `PixVerse-V6`

## 接口地址

| 接口 | 请求方式 | URL |
|------|---------|-----|
| 提交任务 | POST | `https://www.dmxapi.cn/v1/responses` |
| 获取结果 | POST | `https://www.dmxapi.cn/v1/responses` |

:::warning
视频来源二选一，且都必须是 **PixVerse-V6 / PixVerse-C1** 产出的：
- `source_video_id`：V6 / C1 **已生成完成**的视频 id（无需上传）
- `video_media_id`：用 `pixverse-video` 上传外部视频得到的 id

不能使用 paiwo-v5.6 系生成或 `paiwo-video` 上传的 id，否则会报 `701009`。

[视频上传](https://doc.dmxapi.cn/paiwo-video-upload.html)
:::

:::warning
请妥善保管您的 API Key！严禁将密钥泄露给他人、硬编码到代码中或提交到公开的代码仓库。
:::

## 视频延长 示例代码

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
    # 【model】(string, 必填) 使用的视频延长模型
    "model": "PixVerse-V6",

    # 【source_video_id】(integer, 可选) 要延长的源视频 ID（来自平台已生成视频）
    # 必须传入 source_video_id 或 video_media_id 之一
    "source_video_id": 401770290104009,

    # 【video_media_id】(integer, 可选) 要延长的媒体资源 ID（来自上传接口）
    # 与 source_video_id 二选一，不可同时传入
    # "video_media_id": 401771420158031,

    # 【input】(string, 必填) 延长视频的提示词（对应原生 API 的 prompt 字段）
    # 描述延长内容的方向或风格，2048 字符以内
    "input": "across the universe",

    # 【duration】(integer, 必填) 延长的视频时长（秒）
    # 支持 1~15 任意整数时长
    "duration": 5,

    # 【quality】(string, 必填) 输出视频分辨率
    # 可选值: "360p" / "540p" / "720p" / "1080p"
    "quality": "720p",

    # 【motion_mode】(string, 可选) 运动速度模式
    # 可选值: "normal"（正常）/ "fast"（快速）
    # 注意: "fast" 不支持 8s 时长；v5 模型不支持此字段
    "motion_mode": "normal",

    # 【style】(string, 可选) 视频风格描述
    # 留空表示不指定风格
    "style": "",

    # 【seed】(integer, 可选) 随机种子，用于复现生成结果
    # 相同 seed 与参数组合可获得一致的输出
    "seed": 123456789,

    # 【water_mark】(boolean, 必填) 是否添加水印
    # true: 添加水印；false: 无水印
    "water_mark": False,
}

# 步骤4: 发送请求并输出结果

response = requests.post(url, headers=headers, json=payload)

print(json.dumps(response.json(), indent=2, ensure_ascii=False))
```

## 返回示例

```json
{
  "video_id": 401828562288405,
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

> `video_id` 即为任务 ID，用于第二步查询视频生成状态和获取视频链接。

## 获取结果 示例代码

```python
import requests
import json
import time
import urllib.parse

# DMXAPI 服务端点地址
url = "https://www.dmxapi.cn/v1/responses"

# DMXAPI 密钥 (请替换为您自己的密钥)
api_key = "sk-****************************************"

headers = {
    "Content-Type": "application/json",
    "Authorization": f"{api_key}",
}

# 将第一步返回的 video_id 填入此处
video_id = 403970341870197

payload = {
    # 【model】(string, 必填) 查询模型，固定使用提交模型名加 "-get" 后缀
    "model": "paiwo-get",

    # 【input】(string, 必填) 传入第一步返回的 video_id（字符串形式）
    "input": str(video_id),
}

# 轮询查询，直到视频生成完成
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

    # 失败状态 (根据需要扩展)
    if status in (7, 8):
        print(f"❌ 任务失败，status={status}")
        break

    print(f"视频生成中 (status={status})，10 秒后重试...")
    time.sleep(10)
```

## 返回示例

```json
{
  "status": "succeeded",
  "video_url": "https://cdn.pixverse.ai/video/xxxxxxxx.mp4",
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

<p align="center">
  <small>© 2026 DMXAPI PixVerse-V6 视频延长</small>
</p>
