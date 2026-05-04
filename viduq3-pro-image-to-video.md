# viduq3-pro 图生视频 API 使用文档

viduq3-pro 图生视频 API 支持上传单张首帧图片并结合文本提示词异步生成高质量视频，可配置 1-16 秒时长、540p/720p/1080p 分辨率、音视频直出、水印和任务回调等参数。该模型面向高质量音视频内容生成场景，支持以图片 URL 或 Base64 作为首帧输入，让静态图像生成更生动、更立体的视频内容。

## 模型名称

- `viduq3-pro`

## 接口地址

| 接口 | 请求方式 | URL |
|------|---------|-----|
| 提交任务 | POST | `https://www.dmxapi.cn/v1/responses` |

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

# DMXAPI 密钥，请替换为您自己的密钥
# 获取方式: 登录 DMXAPI 官网 -> 个人中心 -> API 密钥管理
api_key = "sk-******************************************"

# 步骤2: 配置请求头

headers = {
    "Content-Type": "application/json",
    "Authorization": f"{api_key}",
}

# 步骤3: 配置请求参数

payload = {
    # 【model】(string, 必填) 模型名称。
    # 当前文档使用 viduq3-pro：高效生成优质音视频内容，让视频内容更生动、更形象、更立体，效果更好。
    "model": "viduq3-pro",

    # 【images】(array[string], 必填) 首帧图像。
    # 模型将以此参数中传入的图片为首帧画面生成视频；支持图片 Base64 编码或可访问的图片 URL。
    # 官方限制: 只支持输入 1 张图；图片格式支持 png、jpeg、jpg、webp；图片比例需要小于 1:4 或 4:1；图片大小不超过 50 MB。
    # 使用 Base64 时，HTTP POST body 不超过 20 MB，且编码需要包含适当的内容类型字符串，例如 data:image/png;base64,{base64_encode}。
    "images": [
        "https://prod-ss-images.s3.cn-northwest-1.amazonaws.com.cn/vidu-maas/template/image2video.png"
    ],

    # 【input】(string, 可选) DMXAPI 文本输入参数，对应 Vidu 官方文档中的 prompt 参数。
    # 用于填写生成视频的文本描述；官方限制 prompt 字符长度不能超过 5000 个字符。
    # 若使用 is_rec 推荐提示词参数，模型将不考虑此参数所输入的提示词。
    "input": "图片中的宇航员，跟特朗普在海边跳舞",

    # 【audio】(bool, 可选) 是否使用音视频直出能力。
    # 官方默认值为 false；false 表示输出静音视频，true 表示输出带台词以及背景音的视频。
    # 当 model 为 viduq3-pro、viduq3-turbo 或 viduq3-pro-fast 时，该参数默认值为 true；该参数为 true 时，voice_id 参数才生效。
    "audio": True,

    # 【is_rec】(bool, 可选) 是否使用推荐提示词。
    # true 表示由系统自动推荐提示词并使用推荐内容生成视频，推荐提示词数量为 1；false 表示根据输入的 prompt 生成视频。
    "is_rec": False,

    # 【duration】(int, 可选) 视频时长。
    # viduq3-pro 默认 5 秒，可选范围为 1-16 秒。
    "duration": 10,

    # 【seed】(int, 可选) 随机种子。
    # 默认不传或传 0 时，会使用随机数替代；手动设置时使用指定种子。
    "seed": 0,

    # 【resolution】(string, 可选) 视频分辨率。
    # viduq3-pro 在 1-16 秒时默认 720p，可选值: "540p" / "720p" / "1080p"。
    "resolution": "540p",

    # 【watermark】(bool, 可选) 是否添加水印。
    # true 表示添加水印，false 表示不添加水印；官方说明目前水印内容固定，默认不添加。
    # 可通过 watermarked_url 参数查询获取带水印的视频内容，详情见查询任务接口。
    "watermark": False,

    # 【wm_position】(int, 可选) 水印位置。
    # 可选值: 1=左上角，2=右上角，3=右下角，4=左下角；默认值为 3。
    "wm_position": 3,

    # 【wm_url】(string, 可选) 水印内容图片 URL。
    # 不传或为空时，使用默认水印：内容由 AI 生成。
    "wm_url": "",

    # 【callback_url】(string, 可选) 任务状态变化回调地址。
    # 创建任务时主动设置 callback_url 后，当视频生成任务状态变化时，Vidu 将向该地址发送 POST 回调请求。
    # 回调请求内容结构与查询任务 API 的返回体一致；回调状态包括: processing=任务处理中，success=任务完成，failed=任务失败。
    # success 或 failed 状态发送失败时会回调三次；Vidu 采用回调签名算法进行认证。
    "callback_url": "https://www.dmxapi.cn",
}

# 步骤4: 发送请求并输出结果

response = requests.post(url, headers=headers, json=payload)

print(json.dumps(response.json(), indent=2, ensure_ascii=False))
```

### 返回示例

```json
{
  "task_id": "947408163915751424",
  "type": "img2video",
  "state": "created",
  "model": "viduq3-pro",
  "style": "general",
  "prompt": "图片中的宇航员，跟特朗普在海边跳舞",
  "images": [
    "https://prod-ss-images.s3.cn-northwest-1.amazonaws.com.cn/vidu-maas/template/image2video.png"
  ],
  "duration": 10,
  "seed": 1829851532,
  "aspect_ratio": "",
  "resolution": "540p",
  "movement_amplitude": "auto",
  "created_at": 1777551223,
  "credits": 100,
  "payload": "",
  "cus_priority": 0,
  "off_peak": false,
  "watermark": false,
  "is_rec": false,
  "wm_position": "bottom_right",
  "wm_url": "",
  "meta_data": "",
  "client_request_id": "",
  "audio_type": "all",
  "usage": {
    "total_tokens": 31250,
    "input_tokens": 0,
    "input_tokens_details": {
      "cached_tokens": 0
    },
    "output_tokens": 31250,
    "output_tokens_details": {
      "reasoning_tokens": 0
    }
  }
}
```



<p align="center">
  <small>© 2026 DMXAPI viduq3-pro 图生视频</small>
</p>
