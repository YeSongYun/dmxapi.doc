# FLUX.2 FLEX 文生图和图片编辑 API 使用文档

FLUX.2 是 Black Forest Labs 推出的AI图像模型，专为实际创意工作流程设计。


## 概述

| 项目 | 说明 |
|------|------|
| **接口地址** | `https://www.dmxapi.cn/flux/v1/flux-2-flex` |
| **模型名称** | `flux-2-flex` |


## 第一步：提交生成图片任务
```python
import json
import requests

# ============================================================
# DMXAPI FLUX.2 FLEX 图像生成 API 示例
# ============================================================

API_URL = "https://www.dmxapi.cn/flux/v1/flux-2-flex"
API_KEY = "sk-*********************************"  # 改成你的 DMXAPI 令牌

payload = json.dumps(
    {
        # ==================== 必填参数 ====================
        "prompt": "一只小狗",                    # 图像生成提示词

        # ==================== 基础参数 ====================
        "prompt_upsampling": True,              # 提示词增强 (默认: true)
        "width": 1024,                          # 图像宽度 (最小: 64)
        "height": 1024,                         # 图像高度 (最小: 64)
        "guidance": 5,                          # 引导系数 (范围: 1.5-10, 默认: 5)
        "steps": 50,                            # 生成步数 (范围: 1-50, 默认: 50)
        "safety_tolerance": 2,                  # 安全容忍度 (范围: 0-5, 默认: 2)
        "output_format": "jpeg",                # 输出格式: jpeg | png (默认: jpeg)
        # "seed": 42,                           # 随机种子 (用于复现结果)

        # ==================== 图像编辑 ====================
        # "input_image": "图片URL或Base64",     # 输入图像
        # "input_image_2": "图片URL或Base64",   # 第二张输入图像
        # "input_image_3": "图片URL或Base64",   # 第三张输入图像
        # "input_image_4": "图片URL或Base64",   # 第四张输入图像

        # ==================== 多图参考 ====================
        # "input_image_5": "图片URL或Base64",   # 实验性多参考
        # "input_image_6": "图片URL或Base64",   # 实验性多参考
        # "input_image_7": "图片URL或Base64",   # 实验性多参考
        # "input_image_8": "图片URL或Base64",   # 实验性多参考
        # "input_image_blob_path": "blob路径",  # Blob 路径

        # ==================== Webhook ====================
        # "webhook_url": "回调URL",             # Webhook 通知 URL
        # "webhook_secret": "密钥",             # Webhook 签名验证密钥
    }
)

headers = {
    "x-key": API_KEY,
    "Content-Type": "application/json",
}

response = requests.request("POST", API_URL, headers=headers, data=payload)

print(response.text)
```

### 请求参数说明

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `prompt` | string | ✅ | 图像生成提示词 |
| `prompt_upsampling` | boolean | ❌ | 提示词增强，默认 `true` |
| `width` | integer | ❌ | 图像宽度，最小 64，默认 1024 |
| `height` | integer | ❌ | 图像高度，最小 64，默认 1024 |
| `guidance` | float | ❌ | 引导系数，范围 1.5-10，默认 5 |
| `steps` | integer | ❌ | 生成步数，范围 1-50，默认 50 |
| `safety_tolerance` | integer | ❌ | 安全容忍度，范围 0-5，默认 2 |
| `output_format` | string | ❌ | 输出格式：`jpeg` 或 `png`，默认 `jpeg` |
| `seed` | integer | ❌ | 随机种子，用于复现结果 |
| `input_image` | string | ❌ | 输入图像（URL 或 Base64） |
| `input_image_2` ~ `input_image_8` | string | ❌ | 额外参考图像 |
| `webhook_url` | string | ❌ | Webhook 通知 URL |
| `webhook_secret` | string | ❌ | Webhook 签名验证密钥 |

### 返回示例
```json
{
    "id": "8d6b8e09-fd2b-4df3-9623-411d925de642",
    "polling_url": "https://api.us3.bfl.ai/v1/get_result?id=8d6b8e09-fd2b-4df3-9623-411d925de642",
    "cost": 6.0,
    "input_mp": 0.0,
    "output_mp": 1.0
}
```

### 返回字段说明

| 字段 | 类型 | 说明 |
|------|------|------|
| `id` | string | 任务唯一标识符 |
| `polling_url` | string | 用于查询结果的 URL |
| `cost` | float | 消耗的积分数 (本站不用此计费)|
| `input_mp` | float | 输入图像百万像素数 |
| `output_mp` | float | 输出图像百万像素数 |



## 第二步：获取生成图片结果

提交任务后，使用返回的 `polling_url` 轮询查询生成结果。

> **提示**：图片生成通常需要 60-120 秒
```python

import requests
import json
import os
from datetime import datetime

# ============================================================
# BFL API 结果查询与图片下载示例
# ============================================================

# ==================== 配置参数 ====================
API_URL = "https://api.us3.bfl.ai/v1/get_result?id=8d6b8e09-fd2b-4df3-9623-411d925de642" # 请替换为实际的 polling_url

# ==================== 发送请求 ====================
response = requests.get(API_URL)
data = response.json()

print("API 响应:")
print(json.dumps(data, indent=4, ensure_ascii=False))

# ==================== 处理结果 ====================
if data.get("status") == "Ready":
    sample_url = data["result"]["sample"]

    # 创建 output 文件夹
    output_dir = os.path.join(os.path.dirname(__file__), "output")
    os.makedirs(output_dir, exist_ok=True)

    # 生成带时间戳的文件名
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"image_{timestamp}.jpeg"
    filepath = os.path.join(output_dir, filename)

    # 下载并保存图片
    print(f"\n正在下载图片: {sample_url[:80]}...")
    img_response = requests.get(sample_url)

    with open(filepath, "wb") as f:
        f.write(img_response.content)

    print(f"图片已保存到: {filepath}")
else:
    print(f"状态不是 Ready，当前状态: {data.get('status')}")
```

### 返回示例
```json
API 响应:
{
    "id": "8d6b8e09-fd2b-4df3-9623-411d925de642",
    "status": "Ready",
    "result": {
        "start_time": 1764246146.4188287,
        "prompt": "hyper-realistic close-up photo of a small puppy sitting in the center of a cozy living room, soft warm natural light coming from a window on the left, the puppy has fluffy light brown and white fur, big round dark eyes looking curiously at the camera, small black nose, ears slightly folded forward, sitting on a light beige rug with subtle texture, shallow depth of field with a softly blurred background showing a simple sofa and a few green indoor plants, gentle and warm color palette, extremely detailed fur texture, 50mm lens, f/1.8, high resolution photography",
        "seed": 2092946386,
        "sample": "https://bfldeliveryscus.blob.core.windows.net/results/2025/11/27/636a70a331ac4d04a074ddd085238f38_sample.jpeg?se=2025-11-27T12%3A32%3A47Z&sp=r&sv=2024-11-04&sr=b&rsct=image/jpeg&sig=6gfcU1RZjOeXgxBIKxfUkgw0J6SdhpvHES6cdIrlqKU%3D"
    },
    "progress": null,
    "details": null,
    "preview": null
}

正在下载图片: https://bfldeliveryscus.blob.core.windows.net/results/2025/11/27/636a70a331ac4d0...
图片已保存到: output\image_20251127_203715.jpeg
```


### 结果字段说明

| 字段 | 类型 | 说明 |
|------|------|------|
| `id` | string | 任务 ID |
| `status` | string | 当前状态 |
| `result.prompt` | string | 实际使用的提示词（可能经过增强） |
| `result.seed` | integer | 生成使用的随机种子 |
| `result.sample` | string | 生成图片的下载 URL |



## 注意事项

1. **API Key 安全**：请妥善保管您的 API Key，不要在前端代码中暴露
2. **图片链接有效期**：生成的图片 URL 有时效性，具体时效官网未标明，建议及时下载保存
