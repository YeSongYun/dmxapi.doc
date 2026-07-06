# happyhorse-1.1-r2v 参考生视频 API 使用文档

HappyHorse 参考生视频模型支持传入 1~9 张参考图像，通过文本提示词中的 [Image 1]、[Image 2] 等标识指代对应图像，将不同图像中的主体角色自然融合生成一段流畅的视频。支持 720P/1080P 分辨率、9 种宽高比（16:9/9:16/3:4/4:3/4:5/5:4/1:1/9:21/21:9）、3–15 秒时长，并支持水印控制与随机种子固定。任务通常需要 1–5 分钟完成，采用异步方式：先提交任务获取任务 ID，再通过任务 ID 轮询获取生成视频。

## 模型名称

- `happyhorse-1.1-r2v`

## 接口地址

| 接口 | 请求方式 | URL |
|------|---------|-----|
| 提交任务 | POST | `https://www.dmxapi.cn/v1/responses` |
| 获取结果 | POST | `https://www.dmxapi.cn/v1/responses` |

:::warning
请妥善保管您的 API Key！严禁将密钥泄露给他人、硬编码到代码中或提交到公开的代码仓库。
:::

## 参考生视频 示例代码

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
    # 可选值: "happyhorse-1.1-r2v" 
    "model": "happyhorse-1.1-r2v",
    # 【input】(object, 必填) 输入的基本信息，包括参考图像和提示词
    "input": {
        # 【prompt】(string, 必填) 文本提示词，用于描述期望生成的视频内容
        # 支持任何语言输入，长度不超过 5000 个非中文字符或 2500 个中文字符
        # 注意：需通过 [Image 1]、[Image 2] 等标识指代 media 数组中对应位置的参考图像，且需指明具体对象（如"[Image 1]中身着红色旗袍的女性"）
        "prompt": "[Image 1]中身着红色旗袍的女性，镜头先以侧面中景勾勒旗袍修身剪裁与S型曲线，随即切换至低角度仰拍，捕捉她轻抬玉手展开[Image 2]中的折扇的同时，[Image 3]中的流苏耳坠随头部转动轻盈摆动的细节，最后推近至面部特写，定格在她指尖轻点扇骨、眼波流转间的含蓄风情，多视角全方位展现东方韵味。",
        # 【media】(array, 必填) 媒体素材列表，用于指定参考图像
        # 数组顺序即 [Image N] 的引用顺序：第 1 个元素对应 [Image 1]，第 2 个对应 [Image 2]，以此类推
        # 参考图像数量: 1~9 张；格式: JPEG/JPG/PNG/WEBP；分辨率短边不低于 400 像素；文件大小不超过 20MB
        "media": [
            {
                # 【type】(string, 必填) 媒体素材类型，固定值: "reference_image"
                "type": "reference_image",
                # 【url】(string, 必填) 参考图像 URL，支持公网 HTTP/HTTPS 地址或 Base64 编码（data:{MIME_type};base64,{base64_data}）
                "url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260424/mvzfud/hh-v2v-girl.jpg"
            },
            {
                "type": "reference_image",
                "url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260424/fvuihk/hh-v2v2-folding-fan.jpg"
            },
            {
                "type": "reference_image",
                "url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260424/imerii/hh-v2v-earrings.jpg"
            }
        ]
    },
    # 【parameters】(object, 可选) 视频生成参数，如设置视频分辨率、宽高比、时长等
    "parameters": {
        # 【resolution】(string, 可选) 指定生成视频的分辨率档位
        # 可选值: "720P" / "1080P"（默认值）
        "resolution": "720P",
        # 【ratio】(string, 可选) 指定生成视频的宽高比
        # 可选值: "16:9"（默认值）/ "9:16" / "3:4" / "4:3" / "4:5" / "5:4" / "1:1" / "9:21" / "21:9"
        "ratio": "16:9",
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

### 返回示例

```json
{
  "request_id": "2257f2e9-24d2-97f6-a566-1c0a079355ab",
  "output": [
    {
      "type": "message",
      "content": [
        {
          "type": "output_text",
          "text": "{\"task_id\":\"c0ac076d-3381-4c21-bc4d-7d1327e21a3c\",\"task_status\":\"PENDING\"}"
        }
      ]
    }
  ],
  "usage": {
    "input_tokens": 0,
    "input_tokens_details": {
      "cached_tokens": 0
    },
    "output_tokens": 60000,
    "output_tokens_details": {
      "reasoning_tokens": 0
    },
    "total_tokens": 60000
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
    "input": "c0ac076d-3381-4c21-bc4d-7d1327e21a3c"
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
          "text": "{\"task_id\":\"c0ac076d-3381-4c21-bc4d-7d1327e21a3c\",\"task_status\":\"SUCCEEDED\",\"submit_time\":\"2026-07-06 ...\",\"scheduled_time\":\"2026-07-06 ...\",\"end_time\":\"2026-07-06 ...\",\"video_url\":\"https://dashscope-a717.oss-accelerate.aliyuncs.com/1d/aa/20260706/630c1e98/863....mp4?Expires=...\"}"
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
  <small>© 2026 DMXAPI happyhorse-1.1-r2v 参考生视频</small>
</p>
