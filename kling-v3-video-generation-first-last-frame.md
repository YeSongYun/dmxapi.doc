# kling-v3-video-generation 首尾帧生视频 API 使用文档

kling-v3-video-generation 是可灵系列最新一代视频生成模型，本文档介绍其基于首尾帧的图生视频能力：只需提供起始帧和结束帧两张图片，模型即可自动生成中间过渡视频。支持自定义分镜模式（最多 6 个片段，每段可独立设置提示词和时长）、主体绑定（最多 3 个主体）、背景音效生成，输出时长最长 15 秒，分辨率可选 720P 标准模式（std）或 1080P 专业模式（pro）。视频采用异步生成方式，通常需 1～5 分钟，建议每隔 15 秒轮询一次任务状态。

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

## 首尾帧生视频 示例代码

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
    # 【model】(string, 必填) 模型名称，固定为 "kling-v3-video-generation"
    "model": "kling-v3-video-generation",
    "input": {
        # 【prompt】(string, 条件必填) 文本提示词，描述生成视频中期望包含的元素和视觉特点
        # 支持中英文，不超过 2500 个字符，超过部分自动截断
        # 当 shot_type=intelligence 时此参数必填；当 shot_type=customize 时不生效，请以 multi_prompt 为准
        "prompt": "让图片中的猫动起来，夕阳西下",

        # 【media】(array, 可选) 媒体素材列表，首尾帧生视频需同时传入 first_frame 和 last_frame
        # 数量限制：首帧 1 张，尾帧 1 张
        # 图像格式：JPEG、JPG、PNG（不支持透明通道），分辨率范围 [300, 8000] 像素，文件大小不超过 10MB
        "media": [
            {
                # 【type】(string, 必填) 媒体素材类型
                # 可选值: "first_frame"(首帧图片) / "last_frame"(尾帧图片)
                "type": "first_frame",
                # 【url】(string, 必填) 图像 URL，支持 HTTP 或 HTTPS 协议
                "url": "https://wanx.alicdn.com/material/20250318/first_frame.png"
            },
            {
                "type": "last_frame",
                "url": "https://wanx.alicdn.com/material/20250318/last_frame.png"
            },
        ],

        # 【multi_shot】(boolean, 可选) 是否开启多镜头生成
        # false: 默认值，不开启多镜头；true: 开启多镜头生成
        "multi_shot": True,

        # 【shot_type】(string, 条件必填) 当 multi_shot=true 时必填，多镜头模式类型
        # "intelligence": 智能分镜，由模型自动规划镜头
        # "customize": 自定义模式，支持自定义每个片段的提示词和时长
        "shot_type": "customize",

        # 【multi_prompt】(array, 条件必填) 当 shot_type=customize 时必填，多镜头自定义模式下的片段列表
        # 分镜数量为 1～6 个
        "multi_prompt": [
            {
                # 【prompt】(string, 必填) 对应片段的提示词，支持中英文，不超过 512 个字符，超过自动截断
                "prompt": "近景，小猫跳到树上微微抬头，毛发被微风轻轻吹起",
                # 【index】(integer, 必填) 分镜片段索引，从 1 开始
                "index": 1,
                # 【duration】(integer, 必填) 对应片段的时长，单位为秒，取值为 [1, parameters.duration] 之间的整数
                "duration": 3
            },
            {
                "prompt": "中景，小猫转身回眸，看着夕阳",
                "index": 2,
                "duration": 2
            }
        ],

        # 【element_list】(array, 可选) 主体列表，用于指定视频中需要引入的主体元素
        # 首尾帧生视频最多支持 3 个主体，主体 ID 可在"可灵-主体 ID 列表"获取
        "element_list": [
            {
                # 【element_id】(integer, 条件必填) 传入 element_list 时必填，表示主体 ID
                "element_id": 105
            },
            {
                "element_id": 108
            }
        ],
    },
    "parameters": {
        # 【mode】(string, 可选) 视频生成模式
        # "pro": 默认值，专业模式，输出视频分辨率为 1080P
        # "std": 标准模式，输出视频分辨率为 720P
        "mode": "std",

        # 【aspect_ratio】(string, 条件必填) 生成视频的宽高比例
        # 可选值: "16:9"(默认) / "9:16" / "1:1"
        # 注意：首尾帧生视频场景无需设置此参数（由首尾帧图片比例决定）
        "aspect_ratio": "16:9",

        # 【duration】(integer, 可选) 生成视频的时长，单位为秒
        # 取值范围: [3, 15] 之间的整数，默认值为 5
        # 重要：duration 直接影响费用，按秒计费，时间越长费用越高，请在调用前确认模型价格
        "duration": 5,

        # 【audio】(boolean, 可选) 是否生成有声视频
        # false: 默认值，输出无声视频；true: 输出有声视频（模型根据视频内容自动生成匹配的背景音乐或音效）
        # 重要：audio 直接影响费用，请在调用前确认模型价格
        "audio": False,

        # 【watermark】(boolean, 可选) 是否添加水印标识
        # false: 默认值，不添加水印；true: 添加水印（位于视频右下角，文案固定为"可灵AI"）
        "watermark": True,
    }
}

# 步骤4: 发送请求并输出结果

# 发送 POST 请求到 API 服务器
response = requests.post(url, headers=headers, json=payload)

# 格式化输出 JSON 响应
# - indent=2: 缩进 2 空格，便于阅读
# - ensure_ascii=False: 正确显示中文字符
print(json.dumps(response.json(), indent=2, ensure_ascii=False))
```

### 返回示例

```json
{
  "request_id": "0b48301e-84fa-96ed-90bc-5718c0675522",
  "output": [
    {
      "type": "message",
      "content": [
        {
          "type": "output_text",
          "text": "{\"task_id\":\"c0116c61-e34d-43f4-9c08-2952b6688c14\",\"task_status\":\"PENDING\"}"
        }
      ]
    }
  ],
  "usage": {
    "total_tokens": 30000,
    "input_tokens": 0,
    "input_tokens_details": {
      "cached_tokens": 0
    },
    "output_tokens": 30000,
    "output_tokens_details": {
      "reasoning_tokens": 0
    }
  }
}
```

> 请保存返回结果中 `text` 字段内 JSON 字符串里的 `task_id`，用于第二步查询任务状态与结果。`task_id` 有效期为 24 小时。

## 获取结果 示例代码


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
https://v4-fdl.kechuangai.com/ksc2/ZQzbj_V0yVVlyJXG-f7rXuY0UXfZlC4aGm7enHbNuoUT...（省略）.mp4

水印版视频 URL：
（任务 watermark=false 时此字段为空）
```



<p align="center">
  <small>© 2026 DMXAPI kling-v3-video-generation 首尾帧生视频</small>
</p>
