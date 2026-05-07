# kling-v3-video-generation 首帧生视频 API 使用文档

可灵 kling-v3-video-generation 是阿里云百炼平台提供的高质量视频生成模型，支持以图像首帧为起点生成流畅视频。模型支持标准模式（720P）与专业模式（1080P），视频时长可设置 3～15 秒，并提供多镜头自定义分镜（最多 6 个片段）、主体元素引入（最多 3 个主体）、背景音乐生成及水印控制等能力。采用异步两步调用：提交任务获取 task_id，再轮询查询视频 URL，全程通过 `/v1/responses` 端点完成。

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

## 首帧生视频 示例代码

```python
import requests
import json

# ═══════════════════════════════════════════════════════════════
# 步骤1: 配置 API 连接信息
# ═══════════════════════════════════════════════════════════════

# DMXAPI 服务端点地址
url = "https://www.dmxapi.cn/v1/responses"

# DMXAPI 密钥 (请替换为您自己的密钥)
api_key = "sk-******************************************"

# ═══════════════════════════════════════════════════════════════
# 步骤2: 配置请求头
# ═══════════════════════════════════════════════════════════════

headers = {
    "Content-Type": "application/json",
    "Authorization": f"{api_key}",
}

# ═══════════════════════════════════════════════════════════════
# 步骤3: 配置请求参数
# ═══════════════════════════════════════════════════════════════

payload = {
    # 【model】(string, 必填) 模型名称，固定为 "kling-v3-video-generation"
    # 支持首帧生视频、首尾帧生视频等图生视频任务
    "model": "kling-v3-video-generation",
    "input": {
        # 【prompt】(string, 条件必填) 文本提示词，描述视频中期望的元素和视觉特点
        # 支持中英文，每个汉字/字母占一个字符，不超过 2500 个字符，超出自动截断
        # 当 shot_type=intelligence 时必填；当 shot_type=customize 时此参数不生效，以 multi_prompt 为准
        "prompt": "让图片中的人物动起来，头发被微风吹动",

        # 【media】(array, 可选) 媒体素材列表，指定图像素材
        # kling-v3-video-generation 首帧生视频：仅传入 first_frame，数量限制为 1 张
        "media": [
            {
                # 【media[].type】(string, 必填) 媒体素材类型
                # 可选值: "first_frame"(首帧图片) / "last_frame"(尾帧图片)
                # 首帧生视频场景固定传入 "first_frame"
                "type": "first_frame",
                # 【media[].url】(string, 必填) 图像 URL
                # 支持 HTTP 或 HTTPS 协议
                # 图像格式：JPEG、JPG、PNG（不支持透明通道）
                # 分辨率：宽和高范围为 [300, 8000] 像素
                # 文件大小：不超过 10MB
                "url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260121/zlpocv/wan-i2v-haigui.webp"
            }
        ],

        # 【multi_shot】(boolean, 可选) 是否开启多镜头生成
        # false: 默认值，不开启多镜头
        # true: 开启多镜头生成，最多支持 6 个分镜片段
        "multi_shot": True,

        # 【shot_type】(string, 条件必填) 多镜头模式类型，当 multi_shot=true 时必填
        # 可选值: "intelligence"(智能分镜，模型自动规划镜头) / "customize"(自定义模式，支持自定义每个片段的提示词和时长)
        "shot_type": "customize",

        # 【multi_prompt】(array, 条件必填) 多镜头自定义模式下的片段列表，当 shot_type=customize 时必填
        # 分镜数量为 1～6 个，各片段 duration 之和建议与 parameters.duration 一致
        "multi_prompt": [
            {
                # 【multi_prompt[].prompt】(string, 必填) 对应片段的提示词
                # 支持中英文，不超过 512 个字符，超过自动截断
                "prompt": "近景，人物微微抬头，头发被微风轻轻吹起",
                # 【multi_prompt[].index】(integer, 必填) 分镜片段索引，从 1 开始
                # 取值范围：1～6
                "index": 1,
                # 【multi_prompt[].duration】(integer, 必填) 对应片段的时长，单位为秒
                # 取值为 [1, parameters.duration] 之间的整数
                "duration": 3
            },
            {
                "prompt": "中景，人物转身回眸，衣角随风飘动",
                "index": 2,
                "duration": 2
            }
        ],

        # 【element_list】(array, 可选) 主体列表，用于指定视频中需要引入的主体元素
        # 首帧生视频场景最多支持 3 个主体
        # 主体 ID 请在「可灵-主体ID列表」页面获取
        "element_list": [
            {
                # 【element_list[].element_id】(integer, 条件必填) 主体 ID
                # 传入 element_list 时必填
                "element_id": 105
            },
            {
                "element_id": 108
            }
        ],
    },
    "parameters": {
        # 【mode】(string, 可选) 视频生成模式
        # 可选值: "pro"(默认值，专业模式，输出 1080P) / "std"(标准模式，输出 720P)
        "mode": "std",

        # 【aspect_ratio】(string, 条件必填) 生成视频的宽高比例
        # 可选值: "16:9"(默认值) / "9:16" / "1:1"
        # 注意：首帧生视频（仅传 first_frame）场景无需强制设置，视频比例跟随首帧图像
        "aspect_ratio": "16:9",

        # 【duration】(integer, 可选) 生成视频的时长，单位为秒
        # 取值范围：[3, 15] 之间的整数，默认值为 5
        # 注意：duration 直接影响费用，按秒计费，调用前请确认模型价格
        "duration": 5,

        # 【audio】(boolean, 可选) 是否生成有声视频
        # false: 默认值，输出无声视频
        # true: 输出有声视频，模型根据视频内容自动生成匹配的背景音乐或音效
        # 注意：audio=true 会影响费用，调用前请确认模型价格
        "audio": False,

        # 【watermark】(boolean, 可选) 是否添加水印
        # false: 默认值，不添加水印
        # true: 添加水印，水印位于视频右下角，文案固定为"可灵AI"
        "watermark": True,
    }
}

# ═══════════════════════════════════════════════════════════════
# 步骤4: 发送请求并输出结果
# ═══════════════════════════════════════════════════════════════

response = requests.post(url, headers=headers, json=payload)

print(json.dumps(response.json(), indent=2, ensure_ascii=False))
```

### 返回示例

```json
{
  "request_id": "5b79409b-8525-9d93-8a45-f5ef155e0769",
  "output": [
    {
      "type": "message",
      "content": [
        {
          "type": "output_text",
          "text": "{\"task_id\":\"05f59029-ab02-4976-854a-5c70df275879\",\"task_status\":\"PENDING\"}"
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

> 提交成功后，从 `output[0].content[0].text` 解析 JSON 字符串，取出 `task_id`，用于下一步查询。`task_id` 有效期为 24 小时。

## 获取结果 示例代码

视频生成通常需要 1～5 分钟，建议每隔 15 秒轮询一次，直到 `task_status` 变为 `SUCCEEDED`。

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
https://v4-fdl.kechuangai.com/ksc2/ZQzbj_V0yVVlyJXG-...xxx.mp4

水印版视频 URL：
（watermark=false 时此字段为空）
```

<p align="center">
  <small>© 2026 DMXAPI kling-v3-video-generation 首帧生视频</small>
</p>
