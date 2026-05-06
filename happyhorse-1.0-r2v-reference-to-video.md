# happyhorse-1.0-r2v 参考生视频 API 使用文档

HappyHorse-参考生视频模型支持传入多张参考图像，通过文本提示词描述场景，将图像中的主体角色融合生成一段流畅的视频。模型可理解 character1、character2 等参考指代标识，将不同图像中的角色自然融入同一视频场景。视频支持 720P/1080P 分辨率、5 种宽高比（16:9/9:16/3:4/4:3/1:1）、3~15 秒时长，任务通常在 1~5 分钟内完成，采用异步模式提交后通过任务 ID 轮询获取结果。

## 模型名称

- `happyhorse-1.0-r2v`

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
    # 【model】(string, 必选) 模型名称
    # 固定值: happyhorse-1.0-r2v
    "model": "happyhorse-1.0-r2v",
    # 【input】(array, 必选) 输入的基本信息，包括参考图像和提示词
    # 数组中包含一个对象，对象有 prompt 和 media 两个字段
    "input": [{
        # 【prompt】(string, 必选) 文本提示词，用来描述生成视频中期望包含的元素和视觉特点
        # 支持任何语言输入，长度不超过 5000 个非中文字符或 2500 个中文字符，超出部分会自动截断
        # 参考指代: 在 prompt 中通过 character1、character2 标识指代 media 数组中对应位置的参考图像
        # 顺序与 media 数组顺序一致，第 1 张图对应 character1，第 2 张对应 character2，以此类推
        "prompt": "身着红色旗袍的女性character1，镜头先以侧面中景勾勒旗袍修身剪裁与S型曲线，随即切换至低角度仰拍，捕捉她轻抬玉手展开折扇character2时流苏耳坠character3随头部转动轻盈摆动的细节，最后推近至面部特写，定格在她指尖轻点扇骨、眼波流转间的含蓄风情，多视角全方位展现东方韵味。",
        # 【media】(array, 必选) 媒体素材列表，用于指定参考图像
        # 数组的每个元素为一个媒体对象，包含 type 和 url 字段
        # 按照数组顺序定义 prompt 中角色引用的顺序，第 1 个对应 character1，第 2 个对应 character2，以此类推
        # 参考图像数量限制: 1~9 张
        "media": [
            {
                # 【type】(string, 必选) 媒体素材类型
                # 固定值: reference_image（参考图像）
                "type": "reference_image",
                # 【url】(string, 必选) 图像文件的 URL 地址，必须为公网可访问的 URL
                # 支持 HTTP 或 HTTPS 协议，示例值: https://xxx/xxx.jpg
                # 图像限制: 格式 JPEG/JPG/PNG/WEBP，短边不低于 400 像素，推荐 720P 以上，文件大小不超过 10MB
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
    }],
    # 【parameters】(object, 可选) 视频生成参数，如设置视频分辨率、宽高比、时长等
    "parameters": {
        # 【resolution】(string, 可选) 生成视频的分辨率档位
        # 可选值: "1080P"(默认) / "720P"
        "resolution": "720P",
        # 【ratio】(string, 可选) 生成视频的宽高比
        # 可选值: "16:9"(默认) / "9:16" / "3:4" / "4:3" / "1:1"
        "ratio": "16:9",
        # 【duration】(integer, 可选) 生成视频的时长，单位为秒
        # 取值范围: 3~15 之间的整数，默认值为 5
        "duration": 5,
        # 【watermark】(boolean, 可选) 是否在生成的视频上添加水印标识
        # 水印位于视频右下角，文案固定为 "Happy Horse"
        # 可选值: true(默认，添加水印) / false(不添加水印)
        "watermark": True,
        # 【seed】(integer, 可选) 随机数种子
        # 取值范围: [0, 2147483647]，未指定时系统自动生成随机种子
        # 若需提升生成结果的可复现性，建议固定 seed 值
        # 注意: 由于模型生成具有概率性，即使使用相同 seed，也不能保证每次生成结果完全一致
        "seed": 11
    }
}

# 步骤4: 发送请求并输出结果
response = requests.post(url, headers=headers, json=payload)

# 格式化输出 JSON 响应
print(json.dumps(response.json(), indent=2, ensure_ascii=False))
```

### 返回示例

```json
{
  "request_id": "b6a5987e-d3d3-9b95-8466-f6cd427766c7",
  "output": [
    {
      "type": "message",
      "content": [
        {
          "type": "output_text",
          "text": "{\"task_id\":\"3ee935d2-e094-4146-8878-ade4d9336403\",\"task_status\":\"PENDING\"}"
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

## 获取结果 示例代码

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
    # 【model】(string, 必选) 查询模型名称
    # 固定值: happyhorse-get，用于查询 happyhorse-1.0-r2v 提交的任务结果
    "model": "happyhorse-get",
    # 【input】(string, 必选) 任务 ID
    # 填入提交任务时返回的 task_id，task_id 查询有效期为 24 小时
    # 任务状态流转: PENDING(排队中) -> RUNNING(处理中) -> SUCCEEDED(成功) / FAILED(失败)
    "input": "62967e89-6174-4d38-9828-aedd2c5d151f"
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
    else:
        print("\n未找到 video_url，任务状态:", inner.get("task_status"))
except (KeyError, IndexError, json.JSONDecodeError) as e:
    print("\n解析 video_url 失败:", e)
```

### 返回示例

```json
{
  "request_id": "a011c69c-ef4a-9903-a89e-78f72c9ef33c",
  "output": [
    {
      "type": "message",
      "content": [
        {
          "type": "output_text",
          "text": "{\"task_id\":\"62967e89-6174-4d38-9828-aedd2c5d151f\",\"task_status\":\"SUCCEEDED\",\"submit_time\":\"2026-04-28 14:26:42.286\",\"scheduled_time\":\"2026-04-28 14:26:42.330\",\"end_time\":\"2026-04-28 14:28:24.417\",\"video_url\":\"https://dashscope-a717.oss-accelerate.aliyuncs.com/1d/8a/20260428/17ae637c/51496466-metadata_video_720p_62967e89-6174-4d38-9828-aedd2c5d151f_refiner_watermark.mp4?Expires=1777444103&OSSAccessKeyId=LTAI5tPxpiCM2hjmWrFXrym1&Signature=pi9SIKuTr00DfRgkUfUyYpNRsVk%3D\"}"
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
https://dashscope-a717.oss-accelerate.aliyuncs.com/1d/8a/20260428/17ae637c/51496466-metadata_video_720p_62967e89-6174-4d38-9828-aedd2c5d151f_refiner_watermark.mp4?Expires=1777444103&OSSAccessKeyId=LTAI5tPxpiCM2hjmWrFXrym1&Signature=pi9SIKuTr00DfRgkUfUyYpNRsVk%3D
```

<p align="center">
  <small>© 2026 DMXAPI happyhorse-1.0-r2v 参考生视频</small>
</p>
