# AICC-Doubao-Seedance-2.0 文生视频 API 使用文档

基于豆包 Seedance 2.0 模型的 AI 文生视频接口，可通过文本提示词生成高质量写实风格视频。支持最高 1080p 分辨率，视频时长 4～15 秒，支持 7 种宽高比（含 adaptive 自适应模式），并可同步生成匹配的人声、音效及背景音乐。采用异步任务模式，提交任务后通过任务 ID 直接查询获取视频结果。

## 🎬 模型名称

- `AICC-Doubao-Seedance-2.0`

## 🔗 接口地址

| 接口 | 请求方式 | URL |
|------|---------|-----|
| 提交任务 | POST | `https://www.dmxapi.cn/v1/responses` |
| 获取结果 | POST | `https://www.dmxapi.cn/v1/responses` |

:::warning
请妥善保管您的 API Key！严禁将密钥泄露给他人、硬编码到代码中或提交到公开的代码仓库。如果怀疑密钥已泄露，请立即前往 DMXAPI 官网重新生成。
:::


## 🎥 文生视频 示例代码

```python
import requests
import json

# 步骤1: 配置 API 连接信息

url = "https://www.dmxapi.cn/v1/responses"
api_key = "sk-******************************************"

# 步骤2: 配置请求头

headers = {
    "Content-Type": "application/json",
    "Authorization": f"{api_key}",
}

# 步骤3: 配置请求参数

payload = {
    # 【model】(string, 必填) 调用的模型 ID
    "model": "AICC-Doubao-Seedance-2.0",

    # 【input】(object[], 必填) 输入给模型的内容，文生视频只需提供文本
    # 也支持与图片（type: "image_url"）、视频（type: "video_url"）等组合输入
    "input": [
        {
            "type": "text",
            "text": "写实风格，晴朗的蓝天之下，一大片白色的雏菊花田，镜头逐渐拉近，最终定格在一朵雏菊花的特写上，花瓣上有几颗晶莹的露珠",
        }
    ],

    # 【ratio】(string, 可选) 生成视频的宽高比，默认 adaptive
    # 可选值: "16:9"(横屏) / "4:3" / "1:1"(方形) / "3:4" / "9:16"(竖屏) / "21:9"(超宽) / "adaptive"(根据提示词智能选择)
    "ratio": "16:9",

    # 【resolution】(string, 可选) 视频分辨率，默认 720p
    # 可选值: "480p" / "720p"/ "1080p"
    "resolution": "480p",

    # 【duration】(integer, 可选) 视频时长（秒），默认值 5
    # 取值范围: [4, 15]，仅支持范围内整数（不支持 -1 智能时长）
    "duration": 4,

    # 【generate_audio】(boolean, 可选) 是否生成与画面同步的音频，默认 true
    # true: 自动生成匹配的人声、音效及背景音乐（生成的有声视频均为单声道）
    # false: 生成无声视频
    "generate_audio": True,

    # 【seed】(integer, 可选) 随机种子，默认 -1（使用随机种子）
    # 注意：Seedance 2.0 系列暂不支持指定 seed，传入后会被上游忽略
    "seed": -1,

    # 【watermark】(boolean, 可选) 生成视频是否包含水印，默认 false
    # false: 不含水印；true: 含有水印
    "watermark": False,

    # 【return_last_frame】(boolean, 可选) 是否返回视频尾帧图像，默认 false
    # true: 返回 png 格式尾帧，宽高像素与生成视频一致，无水印，可用于衔接下一段连续视频
    "return_last_frame": False,

    # 【execution_expires_after】(integer, 可选) 任务超时阈值（秒），默认 172800（48 小时）
    # 取值范围: [3600, 259200]，超时后任务自动终止并标记为 expired 状态
    "execution_expires_after": 172800,

    # 【callback_url】(string, 可选) 任务状态回调地址
    # 状态变化时推送 POST 请求，状态枚举: queued(排队中) / running(运行中) / succeeded(成功) / failed(失败) / expired(超时)
    "callback_url": "https://www.dmxapi.cn",

    # 【tools】(array, 可选) 可选工具列表，模型根据提示词自主判断是否调用
    "tools": [{"type": "web_search"}],
}

# 步骤4: 发送请求并输出结果

response = requests.post(url, headers=headers, json=payload)
print(json.dumps(response.json(), indent=2, ensure_ascii=False))
```

## 返回示例

```json
{
  "id": "cgt-20260721165804-z5qjx",
  "usage": {
    "total_tokens": 18480,
    "input_tokens": 0,
    "input_tokens_details": {
      "cached_tokens": 0
    },
    "output_tokens": 18480,
    "output_tokens_details": {
      "reasoning_tokens": 0
    }
  }
}
```

> 返回的 `id` 为视频生成任务 ID，保存期限为 7 天（从创建时间戳开始计算）。

## 📥 获取结果 示例代码

```python
import requests
import json

url = "https://www.dmxapi.cn/v1/responses"
api_key = "sk-*************************************"

headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {api_key}",
}

payload = {
    # 【model】(string, 必填) 获取结果专用模型标识，固定为 AICC-Doubao-Seedance-2.0-get
    "model": "AICC-Doubao-Seedance-2.0-get",
    # 【input】(string, 必填) 提交任务时返回的任务 ID（id 字段的值）
    # 任务 ID 仅保存 7 天，超时后自动清除
    "input": "cgt-2026****************nsn"
}

response = requests.post(url, headers=headers, json=payload)
result = response.json()

display_result = result
try:
    display_result = json.loads(result["output"][0]["content"][0]["text"])
except Exception:
    pass
print(json.dumps(display_result, indent=2, ensure_ascii=False))

# 提取 video_url
try:
    text = result["output"][0]["content"][0]["text"]
    inner = json.loads(text)
    video_url = inner["content"]["video_url"]
    print(f"\n视频链接: {video_url}")
except Exception as e:
    print(f"提取 URL 失败: {e}")
```

### 返回示例

```json
{
  "request_id": "cgt-20260721184314-9wrsf",
  "output": [
    {
      "type": "message",
      "content": [
        {
          "type": "output_text",
          "text": "{\"content\":{\"video_url\":\"https://ark-acg-cn-beijing.tos-cn-beijing.volces.com/doubao-seedance-2-0/02178463059431000000000000000000000ffffac15e1d87c9b67.mp4?X-Tos-Algorithm=TOS4-HMAC-SHA256\\u0026X-Tos-Credential=...\\u0026X-Tos-Date=20260721T104528Z\\u0026X-Tos-Expires=86400\\u0026X-Tos-Signature=...\\u0026X-Tos-SignedHeaders=host\"},\"id\":\"cgt-20260721184314-9wrsf\",\"model\":\"doubao-seedance-2-0-260128\",\"status\":\"succeeded\"}"
        }
      ]
    }
  ],
  "usage": {
    "total_tokens": 0,
    "input_tokens": 0,
    "input_tokens_details": {
      "cached_tokens": 0
    },
    "output_tokens": 0,
    "output_tokens_details": {
      "reasoning_tokens": 0
    }
  }
}

视频链接: https://ark-acg-cn-beijing.tos-cn-beijing.volces.com/doubao-seedance-2-0/02178463059431000000000000000000000ffffac15e1d87c9b67.mp4?...（有效期 24 小时的临时下载链接）
```

> **说明**：视频链接有效期为 24 小时，请及时下载保存。若 `status` 为 `running` 或 `queued`，可稍后重新调用获取接口查询。返回内容中的 `model` 字段为上游模型版本标识。若提交任务时设置了 `return_last_frame: true`，成功返回的 `content` 中还会包含 `last_frame_url`（尾帧图 URL，24 小时有效）。

<p align="center">
  <small>© 2026 DMXAPI AICC-Doubao-Seedance-2.0 文生视频</small>
</p>
