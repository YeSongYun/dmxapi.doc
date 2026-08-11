# Agnes Image 2.0 Flash 多图合成 API 文档

Sapiens AI 出品的高性能图像生成/编辑模型，支持将多张输入图像合成为一张新图像，返回图片格式支持 URL 和 Base64 两种输出


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
│  Agnes Image 2.0 Flash 多图合成 API 调用示例 - URL 输出            │
│                                                                 │
│  功能说明：传入多张图片合成生成一张新图像，返回图片下载链接           │
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

    # 合成指令（描述多张图片之间的合成关系及期望效果）
    "prompt": "Combine the two characters into an intense fantasy battle scene, dynamic lighting, detailed background, cinematic composition",

    # 输出图片尺寸（示例取值：1024x768、1024x1024、768x1024）
    "size": "1024x768",

    # ⚠️ 注意：image 和 response_format 都需放入 extra_body 内部，不可放在请求体顶层
    "extra_body": {
        # image - 输入图片列表，多图合成传入 2 张及以上（支持两种写法，可混用，代码会自动识别）
        # • 网络图片：直接填 URL，如 "https://example.com/character-1.png"
        # • 本地图片：直接填文件路径，如 "test/example.jpg"
        "image": [
            "https://example.com/character-1.png",
            "https://example.com/character-2.png",
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
│  Agnes Image 2.0 Flash 多图合成 API 调用示例 - Base64 输出         │
│                                                                 │
│  功能说明：传入多张图片合成生成一张新图像，返回 Base64 编码的图像数据 │
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

    # 合成指令（描述多张图片之间的合成关系及期望效果）
    "prompt": "Combine the two characters into an intense fantasy battle scene, dynamic lighting, detailed background, cinematic composition",

    # 输出图片尺寸（示例取值：1024x768、1024x1024、768x1024）
    "size": "1024x768",

    # ⚠️ 注意：image 和 response_format 都需放入 extra_body 内部，不可放在请求体顶层
    "extra_body": {
        # image - 输入图片列表，多图合成传入 2 张及以上（支持两种写法，可混用，代码会自动识别）
        # • 网络图片：直接填 URL，如 "https://example.com/character-1.png"
        # • 本地图片：直接填文件路径，如 "test/example.jpg"
        "image": [
            "https://example.com/character-1.png",
            "https://example.com/character-2.png",
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
      "url": "https://platform-outputs.agnes-ai.space/images/i2i/task_BwDHONWFv3oKQJOXom2DfVVlgE9qfskB/output.png",
      "b64_json": "",
      "revised_prompt": ""
    }
  ],
  "created": 1784870962,
  "task_id": "task_BwDHONWFv3oKQJOXom2DfVVlgE9qfskB"
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

## 📋 请求参数说明

| 参数 | 类型 | 是否必填 | 说明 |
|------|------|----------|------|
| `model` | string | 是 | 固定填 `agnes-image-2.0-flash` |
| `prompt` | string | 是 | 描述多张图片之间的合成关系及期望效果 |
| `size` | string | 是 | 输出图片尺寸，如 `1024x768`、`1024x1024`、`768x1024` |
| `extra_body.image` | string[] | 是 | 输入图片数组，多图合成场景下传入 2 张及以上，支持 URL 或 Data URI Base64 |
| `extra_body.response_format` | string | 否 | 输出格式：`url` 或 `b64_json`，需放在 `extra_body` 内部，不可放在请求体顶层 |

## 📋 返回字段说明

| 字段 | 类型 | 说明 |
|------|------|------|
| `created` | integer | 请求创建时间戳 |
| `data` | array | 生成的图像结果列表 |
| `data[].url` | string | 生成图片的 URL；Base64 输出时为空字符串 |
| `data[].b64_json` | string | Base64 图像数据；URL 输出时为空字符串 |
| `data[].revised_prompt` | string | 修订后的提示词（如有），否则为空字符串 |
| `task_id` | string | 多图合成任务 ID |

<p align="center">
  <small>© 2026 DMXAPI Agnes Image 2.0 Flash 多图合成 API 文档</small>
</p>
