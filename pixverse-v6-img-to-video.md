# PixVerse-V6 图生视频 API 使用文档

PixVerse V6 是 PixVerse 最新一代图生视频模型，支持将参考图片与文字描述结合，生成高质量视频内容。通过 DMXAPI 提供的异步接口，可生成 1~15 秒任意时长的视频，最高支持 1080p 分辨率。V6 版本新增多镜头控制、智能音频生成及提示词优化能力，支持动漫、3D 动画、赛博朋克等 5 种风格渲染，并可通过 template_id 叠加特效模板，采用「提交任务→获取结果」两步异步模式完成视频生成。

## 模型名称

- `PixVerse-V6`

## 接口地址

| 接口 | 请求方式 | URL |
|------|---------|-----|
| 提交任务 | POST | `https://www.dmxapi.cn/v1/responses` |
| 获取结果 | POST | `https://www.dmxapi.cn/v1/responses` |

:::warning
使用本 API 前，请先完成前置依赖文档中的调用以获取所需的 img_id。
本模型请使用 `pixverse-picture` 上传。

[图片上传](https://doc.dmxapi.cn/paiwo_image_upload.html)
:::

:::warning
请妥善保管您的 API Key！严禁将密钥泄露给他人、硬编码到代码中或提交到公开的代码仓库。
:::

## 图生视频 示例代码

```python
import requests
import json

# 步骤1: 配置 API 连接信息

# DMXAPI 服务端点地址
url = "https://www.dmxapi.cn/v1/responses"

# DMXAPI 密钥 (请替换为您自己的密钥)
# 获取方式: 登录 DMXAPI 官网 -> 个人中心 -> API 密钥管理
api_key = "sk-******************************************"

# 步骤2: 配置请求头

headers = {
    "Content-Type": "application/json",      # 指定请求体为 JSON 格式
    "Authorization": f"{api_key}",           # token 认证方式
}

# 步骤3: 配置请求参数

payload = {
    # 【model】(string, 必需) 视频生成模型名称
    "model": "PixVerse-V6",

    # 【input】(string, 必需) 视频生成的文字描述（提示词）
    # 2048 字符以内，描述视频的内容、动作和场景
    "input": "可爱的小猫在海边愉快的玩耍",

    # 【img_id】(integer <uint64>, 必需) 参考图片 ID
    # 通过上传图片接口获取，指定图生视频所使用的参考图片
    "img_id": 177602101,

    # 【style】(string, 可选) 视频风格
    # 可选值: "anime"(动漫) / "3d_animation"(3D 动画) / "day"(日间写实) / "cyberpunk"(赛博朋克) / "comic"(漫画)
    # 如非必要可不传
    "style": "3d_animation",

    # 【duration】(integer, 必需) 视频生成时长（秒）
    # 支持 1~15s 任意时长
    "duration": 5,

    # 【quality】(string, 必需) 视频分辨率
    # 可选值: "360p" / "540p" / "720p" / "1080p"
    "quality": "540p",

    # 【generate_audio_switch】(boolean, 可选) 音频生成开关
    # 支持 v5.5/v5.6/v6/c1；true: 开启音频生成，false: 关闭音频生成
    "generate_audio_switch": True,

    # 【seed】(integer, 可选) 随机种子
    # 取值范围: [0, 2147483647]，相同 seed 可复现相似结果；传 0 表示随机
    "seed": 0,

    # 【negative_prompt】(string, 可选) 负向提示词
    # 2048 字符以内，描述不希望出现在视频中的内容
    "negative_prompt": "",

    # 【motion_mode】(string, 可选) 运动模式
    # 可选值: "normal"(普通) / "fast"(快速)；"fast" 不支持 8s
    "motion_mode": "normal",

    # 【template_id】(integer, 可选) 特效模板 ID
    # 使用前需先激活对应模板；传 0 表示不使用模板
    "template_id": 0,

    # 【generate_multi_clip_switch】(boolean, 可选) 多镜头控制开关
    # 支持 v5.6/v6；True: 多镜头模式，False: 单镜头模式
    "generate_multi_clip_switch": True,

    # 【thinking_type】(string, 可选) 提示词智能优化
    # 支持 v5.5/v5.6/v6；"enabled": 开启优化，"disabled": 关闭优化，"auto": 模型自动决定
    "thinking_type": "auto",
}

# 步骤4: 发送请求并输出结果

response = requests.post(url, headers=headers, json=payload)

print(json.dumps(response.json(), indent=2, ensure_ascii=False))
```

## 返回示例

```json
{
  "video_id": 401770290104009,
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

## 获取结果 示例代码

```python
import requests
import json

# 步骤1: 配置 API 连接信息

url = "https://www.dmxapi.cn/v1/responses"
api_key = "sk-******************************************"

# 从提交任务的响应中提取 video_id，作为查询参数
video_id = 401770290104009  # 替换为实际的 video_id

# 步骤2: 配置请求头

headers = {
    "Content-Type": "application/json",
    "Authorization": f"{api_key}",
}

# 步骤3: 配置请求参数

payload = {
    # 【model】(string, 必需) 查询模型名称，固定填写 "PixVerse-V6-get"
    "model": "paiwo-get",

    # 【input】(string, 必需) 提交任务时返回的 video_id
    # 用于查询视频生成状态与获取最终视频链接
    "input": str(video_id),
}

# 步骤4: 发送请求并提取视频链接

response = requests.post(url, headers=headers, json=payload)
result = response.json()

print(json.dumps(result, indent=2, ensure_ascii=False))

# 提取视频 URL
video_url = result.get("video_url")
if video_url:
    print(f"\n视频下载链接: {video_url}")
```

## 返回示例

```json
{
  "video_id": 401770290104009,
  "status": "succeeded",
  "video_url": "https://cdn.pixverse.ai/output/401770290104009.mp4",
  "usage": {
    "total_tokens": 135000,
    "input_tokens": 0,
    "output_tokens": 135000
  }
}
```

<p align="center">
  <small>© 2026 DMXAPI PixVerse-V6 图生视频</small>
</p>
