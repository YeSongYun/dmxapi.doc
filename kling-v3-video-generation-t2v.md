# kling-v3-video-generation 文生视频 API 使用文档

可灵 kling-v3-video-generation 是阿里云百炼平台推出的高质量文生视频模型，支持通过文字提示词生成视频内容。模型提供 std（720P）和 pro（1080P）两种生成模式，支持 16:9、9:16、1:1 三种宽高比，视频时长可在 3～15 秒之间自由设置，并可选开启背景音效生成及水印添加功能。采用异步两步式调用：先提交任务获取 task_id，再通过 task_id 轮询查询结果（视频生成通常需要 1～5 分钟）。

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

## 文生视频 示例代码

```python
import requests
import json

# ═══════════════════════════════════════════════════════════════
# 步骤1: 配置 API 连接信息
# ═══════════════════════════════════════════════════════════════

# DMXAPI 服务端点地址
url = "https://www.dmxapi.cn/v1/responses"

# DMXAPI 密钥 (请替换为您自己的密钥)
# 获取方式: 登录 DMXAPI 官网 -> 个人中心 -> API 密钥管理
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
    # 【model】(string, 必填) 模型名称
    # 可选值: "kling-v3-video-generation"（标准文生视频）/ "kling-v3-omni-video-generation"（多模态参考生视频）
    "model": "kling-v3-video-generation",
    "input": {
        # 【prompt】(string, 条件必填) 文本提示词，用于描述生成视频中期望包含的元素和视觉特点
        # 支持中英文，每个汉字/字母占一个字符，不超过 2500 个字符，超过部分自动截断
        # 填写逻辑：shot_type=intelligence 时必填；shot_type=customize 时此参数不生效
        "prompt": "一只小猫在月光下奔跑",
    },
    "parameters": {
        # 【mode】(string, 可选) 视频生成模式
        # 可选值: "pro"（默认，专业模式，输出分辨率 1080P）/ "std"（标准模式，输出分辨率 720P）
        "mode": "pro",
        # 【aspect_ratio】(string, 条件必填) 生成视频的宽高比例
        # 文生视频场景必须设置此参数
        # 可选值: "16:9"（默认）/ "9:16" / "1:1"
        "aspect_ratio": "16:9",
        # 【duration】(integer, 可选) 生成视频的时长，单位为秒
        # 取值范围: [3, 15] 之间的整数，默认值为 5
        # 注意: duration 直接影响费用，按秒计费，时间越长费用越高，请在调用前确认模型价格
        "duration": 10,
        # 【audio】(boolean, 可选) 是否生成有声视频
        # 开启后模型将根据视频内容自动生成匹配的背景音乐或音效
        # 可选值: false（默认，输出无声视频）/ true（输出有声视频）
        # 注意: audio 直接影响费用，请在调用前确认模型价格
        "audio": False,
        # 【watermark】(boolean, 可选) 是否添加水印标识
        # 水印位于视频右下角，文案固定为"可灵AI"
        # 可选值: false（默认，不添加水印）/ true（添加水印）
        "watermark": True
    }
}

# ═══════════════════════════════════════════════════════════════
# 步骤4: 发送请求并输出结果
# ═══════════════════════════════════════════════════════════════

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
  "request_id": "bfb43b2f-0830-9c1c-8a45-03a11eb5c36e",
  "output": [
    {
      "type": "message",
      "content": [
        {
          "type": "output_text",
          "text": "{\"task_id\":\"9d616f2054b8-4aea-a966-5a0d4aac-b089\",\"task_status\":\"PENDING\"}"
        }
      ]
    }
  ],
  "usage": {
    "total_tokens": 80000,
    "input_tokens": 0,
    "input_tokens_details": {
      "cached_tokens": 0
    },
    "output_tokens": 80000,
    "output_tokens_details": {
      "reasoning_tokens": 0
    }
  }
}
```

> **说明**：提交成功后，从 `output[0].content[0].text` 中解析 JSON 字符串，获取 `task_id`，用于第二步查询结果。`task_id` 有效期为 24 小时。任务状态枚举：`PENDING`（排队中）→ `RUNNING`（处理中）→ `SUCCEEDED`（成功）/ `FAILED`（失败）/ `CANCELED`（已取消）/ `UNKNOWN`（不存在或状态未知）。

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
https://v4-fdl.kechuangai.com/ksc2/ZQzbj_V0yVVlyJXG-f7rXuY0UXfZlC4aGm7enHbNuoUTRkSd3fvQsf2rPvcP2abzF-8lrolus-NghOI2gUssARe9e18-w_0wUQ2Ogecg406UJuPjTntYLCnc3a4QzV-fLpvY6j1qtbNnb4ZGk01l694_ZuRthkw3grEFIlHuOr23ayALbxmSagmxHHhX8p2sGIhnjNCiXEQiZwZYwx0T0A.mp4

水印版视频 URL：
（任务 watermark=false 时此字段为空）
```

<p align="center">
  <small>© 2026 DMXAPI kling-v3-video-generation 文生视频</small>
</p>
