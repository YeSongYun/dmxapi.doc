# Agnes Image 2.0 Flash 图生图 API 文档

Sapiens AI 出品的高性能图像生成/编辑模型，支持基于输入图片进行智能编辑，返回图片格式支持 URL 和 Base64 两种输出


## 📌 接口地址

```text
https://www.dmxapi.cn/v1/images/generations
```

## 🎨 模型列表

- `agnes-image-2.0-flash`

## 💻 Python 示例代码

::: code-group

```python [URL 输出]
"""
┌─────────────────────────────────────────────────────────────────┐
│  Agnes Image 2.0 Flash 图生图 API 调用示例 - URL 输出              │
│                                                                 │
│  功能说明：传入参考图片进行图生图，返回图片下载链接                  │
└─────────────────────────────────────────────────────────────────┘
"""

import json
import base64
import requests

# ═══════════════════════════════════════════════════════════════════════════════
#  第一部分：用户配置区（按需修改以下内容）
# ═══════════════════════════════════════════════════════════════════════════════

# 接口地址
url = "https://www.dmxapi.cn/v1/images/generations"

# 请求头（请替换为你自己的 DMXAPI 密钥）
headers = {
    "Content-Type": "application/json",
    "Authorization": "sk-**********************************"
}

# 请求体
data = {
    # 模型名称
    "model": "agnes-image-2.0-flash",

    # 编辑指令（描述你希望如何编辑输入图片）
    "prompt": "Transform this image into a cinematic cyberpunk style while preserving the main subject and composition",

    # 输出图片尺寸（示例取值：1024x768、1024x1024、768x1024）
    "size": "1024x768",

    # ⚠️ 注意：image 和 response_format 都需放入 extra_body 内部，不可放在请求体顶层
    "extra_body": {
        # image - 输入图片（支持两种写法，代码会自动识别）
        # • 网络图片：直接填 URL，如 "https://example.com/input-image.png"
        # • 本地图片：直接填文件路径，如 "test/example.jpg"
        "image": [
            "https://example.com/input-image.png"
        ],

        # response_format - 返回格式
        # • url      → 返回图片下载链接
        # • b64_json → 返回 Base64 编码的 JSON 格式图像数据
        "response_format": "url"
    }
}

# ═══════════════════════════════════════════════════════════════════════════════
#  第二部分：请求逻辑（以下内容无需修改）
# ═══════════════════════════════════════════════════════════════════════════════

def encode_image_to_base64(image_path):
    """将本地图片编码为 Base64 格式的 Data URI"""
    with open(image_path, "rb") as image_file:
        encoded = base64.b64encode(image_file.read()).decode('utf-8')
        ext = image_path.split('.')[-1].lower()
        if ext == 'jpg':
            ext = 'jpeg'
        return f"data:image/{ext};base64,{encoded}"

# 自动识别输入图片类型：网络 URL 直接使用，本地路径编码为 Data URI
data["extra_body"]["image"] = [
    item if item.startswith(("http://", "https://")) else encode_image_to_base64(item)
    for item in data["extra_body"]["image"]
]

# 发送 POST 请求到 API
response = requests.post(url, headers=headers, json=data)

# 输出响应信息
print(f"状态码: {response.status_code}")
print(f"响应内容:\n{json.dumps(response.json(), indent=2, ensure_ascii=False)}")
```

```python [Base64 输出]
"""
┌─────────────────────────────────────────────────────────────────┐
│  Agnes Image 2.0 Flash 图生图 API 调用示例 - Base64 输出           │
│                                                                 │
│  功能说明：传入参考图片进行图生图，返回 Base64 编码的图像数据        │
└─────────────────────────────────────────────────────────────────┘
"""

import json
import base64
import requests

# ═══════════════════════════════════════════════════════════════════════════════
#  第一部分：用户配置区（按需修改以下内容）
# ═══════════════════════════════════════════════════════════════════════════════

# 接口地址
url = "https://www.dmxapi.cn/v1/images/generations"

# 请求头（请替换为你自己的 DMXAPI 密钥）
headers = {
    "Content-Type": "application/json",
    "Authorization": "sk-**********************************"
}

# 请求体
data = {
    # 模型名称
    "model": "agnes-image-2.0-flash",

    # 编辑指令（描述你希望如何编辑输入图片）
    "prompt": "Make the object orange while preserving the original composition",

    # 输出图片尺寸（示例取值：1024x768、1024x1024、768x1024）
    "size": "1024x768",

    # ⚠️ 注意：image 和 response_format 都需放入 extra_body 内部，不可放在请求体顶层
    "extra_body": {
        # image - 输入图片（支持两种写法，代码会自动识别）
        # • 网络图片：直接填 URL，如 "https://example.com/input.png"
        # • 本地图片：直接填文件路径，如 "test/example.jpg"
        "image": [
            "https://example.com/input.png"
        ],

        # response_format - 返回格式
        # • url      → 返回图片下载链接
        # • b64_json → 返回 Base64 编码的 JSON 格式图像数据
        "response_format": "b64_json"
    }
}

# ═══════════════════════════════════════════════════════════════════════════════
#  第二部分：请求逻辑（以下内容无需修改）
# ═══════════════════════════════════════════════════════════════════════════════

def encode_image_to_base64(image_path):
    """将本地图片编码为 Base64 格式的 Data URI"""
    with open(image_path, "rb") as image_file:
        encoded = base64.b64encode(image_file.read()).decode('utf-8')
        ext = image_path.split('.')[-1].lower()
        if ext == 'jpg':
            ext = 'jpeg'
        return f"data:image/{ext};base64,{encoded}"

# 自动识别输入图片类型：网络 URL 直接使用，本地路径编码为 Data URI
data["extra_body"]["image"] = [
    item if item.startswith(("http://", "https://")) else encode_image_to_base64(item)
    for item in data["extra_body"]["image"]
]

# 发送 POST 请求到 API
response = requests.post(url, headers=headers, json=data)

# 输出响应信息（data[0].b64_json 即为 Base64 编码的图像数据）
print(f"状态码: {response.status_code}")
print(f"响应内容:\n{json.dumps(response.json(), indent=2, ensure_ascii=False)}")
```

:::

## 📤 返回示例

::: code-group

```json [URL 输出]
状态码: 200
响应内容:
{
  "data": [
    {
      "url": "https://platform-outputs.agnes-ai.space/images/i2i/task_hgKQcM4L63s9kQYACF8jE7y9fcCdCEBP/output.png",
      "b64_json": "",
      "revised_prompt": ""
    }
  ],
  "created": 1784870723,
  "task_id": "task_hgKQcM4L63s9kQYACF8jE7y9fcCdCEBP"
}
```

```json [Base64 输出]
状态码: 200
响应内容:
{
  "data": [
    {
      "url": "",
      "b64_json": "iVBORw0KGgoAAAANSUhEUgAA...",
      "revised_prompt": ""
    }
  ],
  "created": 1784870962,
  "task_id": "task_HxWzaqG7MdrMUD2bk26r0dgwHpaSNSUF"
}
```

:::

<p align="center">
  <small>© 2026 DMXAPI Agnes Image 2.0 Flash 图生图 API 文档</small>
</p>
