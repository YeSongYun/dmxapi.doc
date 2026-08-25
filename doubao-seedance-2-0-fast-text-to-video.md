# doubao-seedance-2-0-fast-260128 文生视频 API 使用文档

doubao-seedance-2-0-fast-260128 是字节跳动火山引擎 Seedance 2.0 Fast 系列的文生视频模型，支持根据文本提示词生成高质量视频。模型支持 480p/720p 分辨率（不支持 1080p 与 4k），视频时长范围 4~15 秒，支持 7 种宽高比（含自适应 adaptive 模式），可自动生成与画面同步的人声、音效及背景音乐。视频生成采用两步异步模式：先提交任务获取任务 ID，再通过 `seedance-2-0-get` 模型查询并获取视频结果。

## 🎬 模型名称

- `doubao-seedance-2-0-fast-260128`

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
    "model": "doubao-seedance-2-0-fast-260128",

    # 【input】(object[], 必填) 输入给模型的内容，文生视频只需提供文本
    # 也支持与图片（type: "image_url"）、视频（type: "video_url"）等组合输入
    # 文本建议中文不超过 500 字，英文不超过 1000 词
    # 额外支持日语、印尼语、西班牙语、葡萄牙语
    "input": [
        {
            "type": "text",
            "text": "写实风格，晴朗的蓝天之下，一大片白色的雏菊花田，镜头逐渐拉近，最终定格在一朵雏菊花的特写上，花瓣上有几颗晶莹的露珠",
        }
    ],

    # 【ratio】(string, 可选) 生成视频的宽高比，Seedance 2.0 fast 默认 adaptive
    # 可选值: "16:9"(横屏) / "4:3" / "1:1"(方形) / "3:4" / "9:16"(竖屏) / "21:9"(超宽) / "adaptive"(根据提示词智能选择)
    "ratio": "16:9",

    # 【resolution】(string, 可选) 视频分辨率，Seedance 2.0 fast 默认 720p
    # 可选值: "480p" / "720p"（Seedance 2.0 fast 不支持 1080p 与 4k）
    # 720p + 16:9 对应实际像素: 1280×720
    "resolution": "720p",

    # 【duration】(integer, 可选) 视频时长（秒），默认值 5
    # Seedance 2.0 fast 取值范围: [4, 15]
    # 设为 -1: 由模型在有效范围内自主选择合适时长（视频时长与计费相关，请谨慎设置）
    "duration": 5,

    # 【generate_audio】(boolean, 可选) 是否生成与画面同步的音频，默认 true
    # true: 自动生成匹配的人声、音效及背景音乐（生成的有声视频均为单声道）
    # false: 生成无声视频
    # 建议将对话部分置于双引号内以优化音频生成效果
    "generate_audio": True,

    # 【seed】(integer, 可选) 随机种子，默认 -1（使用随机种子）
    # 取值范围: [-1, 2^32-1]，固定相同 seed 值可复现类似结果，但不保证完全一致
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
    # web_search: 开启联网搜索，可提升视频内容时效性，但会增加一定时延
    "tools": [{"type": "web_search"}],
}

# 步骤4: 发送请求并输出结果

response = requests.post(url, headers=headers, json=payload)
print(json.dumps(response.json(), indent=2, ensure_ascii=False))
```

### 返回示例

```json
{
  "id": "cgt-20260424185020-nqhpl",
  "usage": {
    "total_tokens": 40200,
    "input_tokens": 0,
    "input_tokens_details": {
      "cached_tokens": 0
    },
    "output_tokens": 40200,
    "output_tokens_details": {
      "reasoning_tokens": 0
    }
  }
}
```

> 返回的 `id` 字段即为视频生成任务 ID，用于第二步查询视频生成结果。任务 ID 仅保存 7 天，请及时获取视频。

## 📥 获取结果 示例代码

```python
import requests
import json

url = "https://www.dmxapi.cn/v1/responses"
api_key = "sk-******************************************"

headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {api_key}",
}

payload = {
    # 【model】(string, 必填) 查询模型，固定为 seedance-2-0-get
    "model": "seedance-2-0-get",
    # 【input】(string, 必填) 第一步提交任务返回的任务 ID
    "input": "cgt-20260507191840-fpbsd"
}

response = requests.post(url, headers=headers, json=payload)
result = response.json()
print(json.dumps(result, indent=2, ensure_ascii=False))

# 提取 video_url
try:
    text = result["output"][0]["content"][0]["text"]
    inner = json.loads(text)
    video_url = inner["content"]["video_url"]
    print(f"\n视频链接: {video_url}")
    last_frame_url = inner["content"].get("last_frame_url")
    if last_frame_url:
        print(f"尾帧图像: {last_frame_url}")
except Exception as e:
    print(f"提取 URL 失败: {e}")
```

### 返回示例

```json
{
  "request_id": "cgt-20260507191840-fpbsd",
  "output": [
    {
      "type": "message",
      "content": [
        {
          "type": "output_text",
          "text": "{\"content\":{\"last_frame_url\":\"https://ark-acg-cn-beijing.tos-cn-beijing.volces.com/doubao-seedance-2-0-fast/02177815272087000000000000000000000ffffac1823a4881b48_last-frame.png?...\",\"video_url\":\"https://ark-acg-cn-beijing.tos-cn-beijing.volces.com/doubao-seedance-2-0-fast/02177815272087000000000000000000000ffffac1823a4881b48.mp4?...\"},\"id\":\"cgt-20260507191840-fpbsd\",\"model\":\"doubao-seedance-2-0-fast-260128\",\"status\":\"succeeded\"}"
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

视频链接: https://ark-acg-cn-beijing.tos-cn-beijing.volces.com/doubao-seedance-2-0-fast/02177815272087000000000000000000000ffffac1823a4881b48.mp4?...
尾帧图像: https://ark-acg-cn-beijing.tos-cn-beijing.volces.com/doubao-seedance-2-0-fast/02177815272087000000000000000000000ffffac1823a4881b48_last-frame.png?...
```

> **说明**：视频链接有效期为 24 小时，请及时下载保存。若 `status` 为 `running` 或 `queued`，可稍后重新调用获取接口查询。

<p align="center">
  <small>© 2026 DMXAPI doubao-seedance-2-0-fast-260128 文生视频</small>
</p>
