# kling-v3-video-generation 文生视频 API 使用文档

kling-v3-video-generation 是阿里云可灵 AI 推出的高性能视频生成模型，支持文生视频和多镜头分镜能力。通过 DMXAPI 封装的 `/v1/responses` 接口，用户可通过自然语言提示词生成最长 15 秒、最高 1080P 的高清视频，支持 16:9、9:16、1:1 三种宽高比，可按需开启自动配乐和水印。多镜头模式下，支持"智能分镜"（由模型自动规划）和"自定义分镜"（最多 6 段，每段独立指定提示词和时长）两种方式。视频生成为异步任务，提交后需使用 `kling-v3-get` 模型轮询获取结果。

## 模型名称

- `kling-v3-video-generation`

## 接口地址

| 接口 | 请求方式 | URL |
|------|---------|-----|
| 提交任务 | POST | `https://www.dmxapi.cn/v1/responses` |
| 获取结果 | POST | `https://www.dmxapi.cn/v1/responses` |

:::warning
请妥善保管您的 API Key！严禁将密钥泄露给他人、硬编码到代码中或提交到公开的代码仓库。
:::

## 文生视频（智能分镜）示例代码

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
    "Content-Type": "application/json",      # 指定请求体为 JSON 格式
    "Authorization": f"{api_key}",           # token 认证方式
}

# 步骤3: 配置请求参数

payload = {
    "model": "kling-v3-video-generation",
    "input": {
        # 【prompt】(string, 条件必填) 文本提示词，描述生成视频中期望包含的元素和视觉特点
        # 支持中英文，每个汉字/字母占一个字符，不超过 2500 个字符，超过部分自动截断
        # 当 shot_type=intelligence 时必填；当 shot_type=customize 时此参数不生效，以 multi_prompt 为准
        "prompt": "一只小猫在月光下奔跑",

        # 【multi_shot】(boolean, 可选) 是否开启多镜头生成
        # false：默认值，不开启多镜头
        # true：开启多镜头生成，同时需要填写 shot_type
        "multi_shot": False,

        # 【shot_type】(string, 条件必填) 多镜头模式类型，当 multi_shot=true 时必填
        # "intelligence"：智能分镜，由模型自动规划镜头内容
        # "customize"：自定义模式，支持自定义每个片段的提示词和时长
        "shot_type": "customize",

        # 【multi_prompt】(array, 条件必填) 多镜头自定义模式下的片段列表，当 shot_type=customize 时必填
        # 分镜数量为 1～6 个，索引从 1 开始
        "multi_prompt": [
            {
                # 【index】(integer, 必填) 分镜片段索引，分镜数量 1～6 个，索引从 1 开始
                "index": 1,
                # 【prompt】(string, 必填) 对应片段的提示词，支持中英文，不超过 512 个字符，超过自动截断
                "prompt": "夜晚，小猫从草丛中跳出",
                # 【duration】(integer, 必填) 对应片段的时长，单位为秒，取值为 [1, parameters.duration] 的整数
                "duration": 5
            },
            {
                "index": 2,
                "prompt": "小猫在月光下飞速奔跑，毛发随风飘动",
                "duration": 5
            },
            {
                "index": 3,
                "prompt": "小猫停下来，仰望圆月",
                "duration": 5
            }
        ]
    },
    "parameters": {
        # 【mode】(string, 可选) 视频生成模式
        # "pro"：默认值，专业模式，输出视频分辨率为 1080P
        # "std"：标准模式，输出视频分辨率为 720P
        "mode": "pro",

        # 【aspect_ratio】(string, 条件必填) 生成视频的宽高比例
        # 文生视频场景下必须设置此参数
        # "16:9"：默认值，横屏
        # "9:16"：竖屏
        # "1:1"：方形
        "aspect_ratio": "16:9",

        # 【duration】(integer, 可选) 生成视频的总时长，单位为秒
        # 取值范围：[3, 15] 之间的整数，默认值为 5
        # 注意：duration 直接影响费用，按秒计费，时间越长费用越高，请在调用前确认模型价格
        "duration": 15,

        # 【audio】(boolean, 可选) 是否生成有声视频
        # false：默认值，输出无声视频
        # true：输出有声视频，模型将根据视频内容自动生成匹配的背景音乐或音效
        # 注意：audio 开启后将影响费用，请在调用前确认模型价格
        "audio": False,

        # 【watermark】(boolean, 可选) 是否添加水印标识
        # 水印位于视频右下角，文案固定为"可灵AI"
        # false：默认值，不添加水印
        # true：添加水印
        "watermark": True
    }
}

# 步骤4: 发送请求并输出结果

response = requests.post(url, headers=headers, json=payload)
print(json.dumps(response.json(), indent=2, ensure_ascii=False))
```

### 返回示例

```json
{
  "request_id": "3a1e5556-3d19-955b-80e5-fd25541d47cf",
  "output": [
    {
      "type": "message",
      "content": [
        {
          "type": "output_text",
          "text": "{\"task_id\":\"4b117331-32e6-4c30-af95-e045956a89fe\",\"task_status\":\"PENDING\"}"
        }
      ]
    }
  ],
  "usage": {
    "total_tokens": 120000,
    "input_tokens": 0,
    "input_tokens_details": {
      "cached_tokens": 0
    },
    "output_tokens": 120000,
    "output_tokens_details": {
      "reasoning_tokens": 0
    }
  }
}
```

> 提交成功后，从返回的 `output[0].content[0].text` 中解析 JSON，获取 `task_id`，用于下一步查询结果。`task_id` 有效期为 24 小时。任务初始状态为 `PENDING`（排队中）。

## 获取结果 示例代码

视频生成通常需要 1~5 分钟，建议每隔 15 秒轮询一次，直到 `task_status` 变为 `SUCCEEDED`。

```python
import requests
import json

url = "https://www.dmxapi.cn/v1/responses"
api_key = "sk-******************************************"

headers = {
    "Content-Type": "application/json",
    "Authorization": f"{api_key}",
}

payload = {
    # 【model】(string, 必填) 查询模型名称，固定为 "kling-v3-get"
    "model": "kling-v3-get",
    # 【input】(string, 必填) 待查询的任务 ID
    # 填入提交任务时返回的 task_id，有效期为 24 小时
    "input": "3b2a24b8-b480-4950-8e27-1cdd19410f95"
}

response = requests.post(url, headers=headers, json=payload)
result = response.json()

try:
    text_str = result["output"][0]["content"][0]["text"]
    video_info = json.loads(text_str)
    print("视频 URL：")
    print(video_info.get("video_url", "未找到"))
    print("\n水印版视频 URL：")
    print(video_info.get("watermark_video_url", "未找到"))
except Exception as e:
    print(f"提取 URL 失败: {e}")
```

### 返回示例

```
视频 URL：
https://v4-fdl.kechuangai.com/ksc2/ZQzbj_V0yVVlyJXG-f7rXuY0UXfZlC4aGm7enHbNuoUTRkSd3fvQsf2rPvcP2abzF-8lrolus-NghOI2gUssARe9e18-w_0wUQ2Ogecg406UJuPjTntYLCnc3a4QzV-fLpvY6j1qtbNnb4ZGk01l694_ZuRthkw3grEFIlHuOr23ayALbxmSagmxHHhX8p2sGIhnjNCiXEQiZwZYwx0T0A.mp4?cacheKey=...

水印版视频 URL：
（任务 watermark=false 时此字段为空）
```

任务状态说明：

| 状态 | 说明 |
|------|------|
| PENDING | 任务排队中 |
| RUNNING | 任务处理中 |
| SUCCEEDED | 任务执行成功，响应中包含视频 URL |
| FAILED | 任务执行失败 |
| CANCELED | 任务已取消 |
| UNKNOWN | 任务不存在或状态未知（task_id 超过 24 小时有效期） |

<p align="center">
  <small>© 2026 DMXAPI kling-v3-video-generation 文生视频</small>
</p>
