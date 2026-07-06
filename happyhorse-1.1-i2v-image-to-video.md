# happyhorse-1.1-i2v 首帧生视频 API 使用文档

HappyHorse 首帧生视频模型以首帧图片为基础，支持通过文本提示词进行引导，生成物理真实、运动流畅的视频。调用采用异步方式，任务通常需要 1–5 分钟完成；支持分辨率档位调节（720P/1080P）、时长设置（3–15 秒）、水印控制及随机种子固定，可满足多样化的图生视频应用需求。

## 模型名称

- `happyhorse-1.1-i2v`

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

# 步骤1: 配置 API 连接信息
url = "https://www.dmxapi.cn/v1/responses"
api_key = "sk-******************************************"

# 步骤2: 配置请求头
headers = {
    "Content-Type": "application/json",      # 指定请求体为 JSON 格式
    "Authorization": f"{api_key}",            # token 认证方式
}

# 步骤3: 配置请求参数
payload = {
    # 【model】(string, 必填) 模型名称
    # 可选值: "happyhorse-1.1-i2v" 
    "model": "happyhorse-1.1-i2v",
    # 【input】(object, 必填) 输入的基本信息，如提示词、首帧图像等
    "input": {
        # 【prompt】(string, 可选) 文本提示词，用于描述期望生成的视频内容
        # 支持任何语言输入，长度不超过 5000 个非中文字符或 2500 个中文字符，超过部分将自动截断
        "prompt": "一只猫在草地上奔跑",
        # 【media】(array, 必填) 输入媒体列表，用于指定视频生成所需的图像
        "media": [
            {
                # 【type】(string, 必填) 媒体素材类型
                # 可选值: "first_frame"（以此图作为视频首帧，有且仅有 1 张首帧图像）
                "type": "first_frame",
                # 【url】(string, 必填) 首帧图像的 URL
                # 支持公网 HTTP/HTTPS 图片 URL，或 Base64 编码图像（data:{MIME_type};base64,{base64_data}）
                # 格式：JPEG、JPG、PNG、WEBP；宽高比：1:2.5～2.5:1；宽高均不小于 300 像素；文件大小不超过 20MB
                "url": "https://cdn.translate.alibaba.com/r/wanx-demo-1.png"
            }
        ]
    },
    # 【parameters】(object, 可选) 视频处理参数，如设置视频分辨率、设置视频时长等
    "parameters": {
        # 【resolution】(string, 可选) 指定生成的视频分辨率档位，用于控制视频的清晰度（总像素）
        # 模型根据选择的分辨率档位，自动缩放至相近总像素；输出的视频宽高比与输入首帧近似一致
        # 可选值: "720P" / "1080P"（默认值）
        "resolution": "720P",
        # 【duration】(integer, 可选) 指定生成视频的时长，单位为秒
        # 取值范围: [3, 15] 之间的整数，默认值为 5
        "duration": 5,
        # 【watermark】(boolean, 可选) 是否在生成的视频上添加水印标识
        # 水印位于视频右下角，文案固定为 "Happy Horse"
        # true（默认值）: 添加水印 / false: 不添加水印
        "watermark": True,
        # 【seed】(integer, 可选) 随机数种子，用于提升生成结果的可复现性
        # 取值范围: [0, 2147483647]，未指定时系统自动生成随机种子
        # 注意：由于模型生成具有概率性，即使使用相同 seed 也不能保证每次结果完全一致
        "seed": 42
    }
}

# 步骤4: 发送请求并输出结果
response = requests.post(url, headers=headers, json=payload)
print(json.dumps(response.json(), indent=2, ensure_ascii=False))
```

## 返回示例

```json
{
  "request_id": "7fe69352-cd4e-9688-aa98-4c6a0f11fbe3",
  "output": [
    {
      "type": "message",
      "content": [
        {
          "type": "output_text",
          "text": "{\"task_id\":\"2f8f6ef5-5b67-41ab-bd2b-30d054fa04a7\",\"task_status\":\"PENDING\"}"
        }
      ]
    }
  ],
  "usage": {
    "input_tokens": 0,
    "input_tokens_details": {
      "cached_tokens": 0
    },
    "output_tokens": 45000,
    "output_tokens_details": {
      "reasoning_tokens": 0
    },
    "total_tokens": 45000
  }
}
```

> 提交成功后，从 `output[0].content[0].text` 解析出的 JSON 中提取 `task_id`，用于第二步查询结果。任务 ID 有效期为 24 小时，请勿重复创建任务，轮询获取即可。

## 获取结果 示例代码

```python
import requests
import json

# 步骤1: 配置 API 连接信息
url = "https://www.dmxapi.cn/v1/responses"
api_key = "sk-******************************************"

# 步骤2: 配置请求头
headers = {
    "Content-Type": "application/json",      # 指定请求体为 JSON 格式
    "Authorization": f"{api_key}",            # token 认证方式
}

# 步骤3: 配置请求参数
payload = {
    # 【model】(string, 必填) 查询模型名称，固定为 "happyhorse-get"
    "model": "happyhorse-get",
    # 【input】(string, 必填) 提交任务时返回的 task_id，用于查询任务状态与结果
    # task_id 有效期为 24 小时，超时后将无法查询（接口返回状态 UNKNOWN）
    # 任务状态枚举: PENDING(排队中) / RUNNING(处理中) / SUCCEEDED(成功) / FAILED(失败) / CANCELED(已取消) / UNKNOWN(不存在或已过期)
    # 视频生成通常需要 1~5 分钟，建议每隔约 15 秒轮询一次（重新执行本步骤），直到状态变为 SUCCEEDED；请勿重复创建任务
    "input": "2f8f6ef5-5b67-41ab-bd2b-30d054fa04a7"
}

# 步骤4: 发送请求并输出结果
response = requests.post(url, headers=headers, json=payload)

data = response.json()
print(json.dumps(data, indent=2, ensure_ascii=False))

# 提取 video_url（嵌套在 output[0].content[0].text 的 JSON 字符串里）
try:
    text = data["output"][0]["content"][0]["text"]
    inner = json.loads(text)
    video_url = inner.get("video_url")
    if video_url:
        print("\n视频链接:")
        print(video_url)
        # 注意：video_url 有效期为 24 小时，请及时下载并转存至本地或永久存储（如 OSS）
    else:
        print("\n未找到 video_url，任务状态:", inner.get("task_status"))
except (KeyError, IndexError, json.JSONDecodeError) as e:
    print("\n解析 video_url 失败:", e)
```

### 返回示例

```json
{
  "request_id": "4597a2af-ae45-9b56-ad88-0539224dabd0",
  "output": [
    {
      "type": "message",
      "content": [
        {
          "type": "output_text",
          "text": "{\"task_id\":\"2f8f6ef5-5b67-41ab-bd2b-30d054fa04a7\",\"task_status\":\"SUCCEEDED\",\"submit_time\":\"2026-07-06 ...\",\"scheduled_time\":\"2026-07-06 ...\",\"end_time\":\"2026-07-06 ...\",\"video_url\":\"https://dashscope-a717.oss-accelerate.aliyuncs.com/1d/aa/20260706/630c1e98/863....mp4?Expires=...\"}"
        }
      ]
    }
  ],
  "usage": {
    "input_tokens": 0,
    "input_tokens_details": {
      "cached_tokens": 0
    },
    "output_tokens": 0,
    "output_tokens_details": {
      "reasoning_tokens": 0
    },
    "total_tokens": 0
  }
}

视频链接:
https://dashscope-a717.oss-accelerate.aliyuncs.com/1d/aa/20260706/630c1e98/863....mp4?Expires=...
```

<p align="center">
  <small>© 2026 DMXAPI happyhorse-1.1-i2v 首帧生视频</small>
</p>
