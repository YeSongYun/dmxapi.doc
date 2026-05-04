# viduq3-pro 文生视频 API 使用文档

viduq3-pro 文生视频 API 支持通过文本提示词异步创建高质量视频任务，可配置视频时长、画面比例、分辨率、音视频直出、水印和回调地址等参数。该模型支持 1-16 秒视频生成，分辨率最高可选 1080p，并支持 q3 系列专属的音画同步能力。

## 模型名称

- `viduq3-pro`

## 接口地址

| 接口 | 请求方式 | URL |
|------|---------|-----|
| 提交任务 | POST | `https://www.dmxapi.cn/v1/responses` |

:::warning
请妥善保管您的 API Key！严禁将密钥泄露给他人、硬编码到代码中或提交到公开的代码仓库。
:::

## 文生视频 示例代码

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

    # 【input】(string, 必填) DMXAPI 文本输入参数，对应 Vidu 官方文档中的 prompt 参数。
    # 用于填写生成视频的文本描述；官方限制 prompt 字符长度不能超过 5000 个字符。
    "input": "一只小猫在沙滩上肆意奔跑，跳跃 ，穿过一群在沙滩上打排球的小女孩",

    # 【duration】(int, 可选) 视频时长参数。
    # viduq3-pro 默认 5 秒，可选范围为 1-16 秒。
    "duration": 10,

    # 【seed】(int, 可选) 随机种子。
    # 默认不传或传 0 时，会使用随机数替代；手动设置时使用指定种子。
    "seed": 0,

    # 【aspect_ratio】(string, 可选) 视频画面比例。
    # 默认值为 16:9；可选值: "16:9" / "9:16" / "3:4" / "4:3" / "1:1"。
    # 其中 3:4、4:3 仅支持 q2、q3 系列模型。
    "aspect_ratio": "4:3",

    # 【resolution】(string, 可选) 视频分辨率。
    # viduq3-pro 在 1-16 秒时默认 720p，可选值: "540p" / "720p" / "1080p"。
    "resolution": "1080p",

    # 【audio】(bool, 可选) 是否使用音视频直出能力。
    # 默认值为 true；false 表示输出静音视频，true 表示需要音画同步并输出带声音的视频（包括台词和音效）。
    # 仅 q3 系列模型支持该参数。
    "audio": True,

    # 【watermark】(bool, 可选) 是否添加水印。
    # true 表示添加水印，false 表示不添加水印；官方说明目前水印内容固定，默认不添加。
    "watermark": False,

    # 【wm_position】(int, 可选) 水印位置。
    # 可选值: 1=左上角，2=右上角，3=右下角，4=左下角；默认值为 3。
    "wm_position": 3,

    # 【wm_url】(string, 可选) 水印内容图片 URL。
    # 不传或为空时，使用默认水印：内容由 AI 生成。
    "wm_url": "",

    # 【callback_url】(string, 可选) 任务状态变化回调地址。
    # 创建任务时主动设置 callback_url 后，当视频生成任务状态变化时，Vidu 将向该地址发送 POST 回调请求。
    # 回调状态包括: processing=任务处理中，success=任务完成，failed=任务失败；发送失败时会回调三次。
    "callback_url": "https://www.dmxapi.cn",
}

# 步骤4: 发送请求并输出结果

response = requests.post(url, headers=headers, json=payload)

print(json.dumps(response.json(), indent=2, ensure_ascii=False))
```

### 返回示例

```json
{
  "task_id": "947407951520337920",
  "type": "text2video",
  "state": "created",
  "model": "viduq3-pro",
  "style": "general",
  "prompt": "一只小猫在沙滩上肆意奔跑，跳跃 ，穿过一群在沙滩上打排球的小女孩",
  "images": [],
  "duration": 10,
  "seed": 1762978053,
  "aspect_ratio": "4:3",
  "resolution": "1080p",
  "movement_amplitude": "auto",
  "created_at": 1777551172,
  "credits": 300,
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
    "total_tokens": 93750,
    "input_tokens": 0,
    "input_tokens_details": {
      "cached_tokens": 0
    },
    "output_tokens": 93750,
    "output_tokens_details": {
      "reasoning_tokens": 0
    }
  }
}
```



<p align="center">
  <small>© 2026 DMXAPI viduq3-pro 文生视频</small>
</p>
