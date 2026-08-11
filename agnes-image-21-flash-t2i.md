# Agnes Image 2.1 Flash 文生图 API 文档
Sapiens AI 出品的升级版图像生成模型，优化高信息密度图像生成，返回图片格式支持 URL 和 Base64 两种输出


## 📌 接口地址

```text
https://www.dmxapi.cn/v1/images/generations
```

## 🎨 模型列表

- `agnes-image-2.1-flash`

## 💻 Python 示例代码

::: code-group

```python [URL 输出]
"""
┌─────────────────────────────────────────────────────────────────┐
│  Agnes Image 2.1 Flash 文生图 API 调用示例 - URL 输出              │
│                                                                 │
│  功能说明：根据文字提示词生成图像，返回图片下载链接                  │
└─────────────────────────────────────────────────────────────────┘
"""

import json
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
    "model": "agnes-image-2.1-flash",

    # 图像生成提示词（描述期望生成的目标图像内容）
    "prompt": "A luminous floating city above a misty canyon at sunrise, cinematic realism",

    # 输出图片分辨率档位（可选值：1K、2K、3K、4K）
    "size": "1K",

    # 输出图片宽高比（可选值：1:1、3:4、4:3、16:9、9:16、2:3、3:2、21:9，默认 1:1）
    #
    # ┌──────────┬─────────────┬─────────────┬─────────────┬─────────────┐
    # │ 宽高比    │ 1K          │ 2K          │ 3K          │ 4K          │
    # ├──────────┼─────────────┼─────────────┼─────────────┼─────────────┤
    # │ 1:1      │ 1024x1024   │ 2048x2048   │ 3072x3072   │ 4096x4096   │
    # │ 3:4      │ 864x1152    │ 1728x2304   │ 2592x3456   │ 3456x4608   │
    # │ 4:3      │ 1152x864    │ 2304x1728   │ 3456x2592   │ 4608x3456   │
    # │ 16:9     │ 1312x736    │ 2624x1472   │ 3936x2208   │ 5248x2944   │
    # │ 9:16     │ 736x1312    │ 1472x2624   │ 2208x3936   │ 2944x5248   │
    # │ 2:3      │ 832x1248    │ 1664x2496   │ 2496x3744   │ 3328x4992   │
    # │ 3:2      │ 1248x832    │ 2496x1664   │ 3744x2496   │ 4992x3328   │
    # │ 21:9     │ 1568x672    │ 3136x1344   │ 4704x2016   │ 6272x2688   │
    # └──────────┴─────────────┴─────────────┴─────────────┴─────────────┘
    "ratio": "1:1",

    # response_format - 返回格式
    # ⚠️ 注意：response_format 不要放在请求体顶层，需放入 extra_body 内部
    # • url      → 返回图片下载链接
    # • b64_json → 返回 Base64 编码的 JSON 格式图像数据
    "extra_body": {
        "response_format": "url"
    }
}

# ═══════════════════════════════════════════════════════════════════════════════
#  第二部分：请求逻辑（以下内容无需修改）
# ═══════════════════════════════════════════════════════════════════════════════

# 发送 POST 请求到 API
response = requests.post(url, headers=headers, json=data)

# 输出响应信息
print(f"状态码: {response.status_code}")
print(f"响应内容:\n{json.dumps(response.json(), indent=2, ensure_ascii=False)}")
```

```python [Base64 输出]
"""
┌─────────────────────────────────────────────────────────────────┐
│  Agnes Image 2.1 Flash 文生图 API 调用示例 - Base64 输出           │
│                                                                 │
│  功能说明：根据文字提示词生成图像，返回 Base64 编码的图像数据        │
└─────────────────────────────────────────────────────────────────┘
"""

import json
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
    "model": "agnes-image-2.1-flash",

    # 图像生成提示词（描述期望生成的目标图像内容）
    "prompt": "A clean product photo of a glass cube on a white studio background, soft shadows, high detail",

    # 输出图片分辨率档位（可选值：1K、2K、3K、4K）
    "size": "1K",

    # 输出图片宽高比（可选值：1:1、3:4、4:3、16:9、9:16、2:3、3:2、21:9，默认 1:1）
    #
    # ┌──────────┬─────────────┬─────────────┬─────────────┬─────────────┐
    # │ 宽高比    │ 1K          │ 2K          │ 3K          │ 4K          │
    # ├──────────┼─────────────┼─────────────┼─────────────┼─────────────┤
    # │ 1:1      │ 1024x1024   │ 2048x2048   │ 3072x3072   │ 4096x4096   │
    # │ 3:4      │ 864x1152    │ 1728x2304   │ 2592x3456   │ 3456x4608   │
    # │ 4:3      │ 1152x864    │ 2304x1728   │ 3456x2592   │ 4608x3456   │
    # │ 16:9     │ 1312x736    │ 2624x1472   │ 3936x2208   │ 5248x2944   │
    # │ 9:16     │ 736x1312    │ 1472x2624   │ 2208x3936   │ 2944x5248   │
    # │ 2:3      │ 832x1248    │ 1664x2496   │ 2496x3744   │ 3328x4992   │
    # │ 3:2      │ 1248x832    │ 2496x1664   │ 3744x2496   │ 4992x3328   │
    # │ 21:9     │ 1568x672    │ 3136x1344   │ 4704x2016   │ 6272x2688   │
    # └──────────┴─────────────┴─────────────┴─────────────┴─────────────┘
    "ratio": "1:1",

    # response_format - 返回格式
    # ⚠️ 注意：response_format 不要放在请求体顶层，需放入 extra_body 内部
    # ⚠️ 注意：顶层 return_base64 参数经实测无效，请使用本参数获取 Base64 输出
    "extra_body": {
        "response_format": "b64_json"
    }
}

# ═══════════════════════════════════════════════════════════════════════════════
#  第二部分：请求逻辑（以下内容无需修改）
# ═══════════════════════════════════════════════════════════════════════════════

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
  "created": 1784883902,
  "background": null,
  "data": [
    {
      "b64_json": null,
      "revised_prompt": null,
      "url": "https://platform-outputs.agnes-ai.space/images/t2i/36a8af17f9534467a50c757623813f04.png"
    }
  ],
  "output_format": null,
  "quality": null,
  "size": null,
  "usage": {
    "total_tokens": 0,
    "input_tokens": 0,
    "input_tokens_details": {
      "image_tokens": 0,
      "text_tokens": 0
    },
    "output_tokens": 0
  }
}
```

```json [Base64 输出]
状态码: 200
响应内容:
{
  "created": 1784883940,
  "background": null,
  "data": [
    {
      "b64_json": "iVBORw0KGgoAAAANSUhEUgAA...",
      "revised_prompt": null,
      "url": null
    }
  ],
  "output_format": null,
  "quality": null,
  "size": null,
  "usage": {
    "total_tokens": 0,
    "input_tokens": 0,
    "input_tokens_details": {
      "image_tokens": 0,
      "text_tokens": 0
    },
    "output_tokens": 0
  }
}
```

:::

<p align="center">
  <small>© 2026 DMXAPI Agnes Image 2.1 Flash 文生图 API 文档</small>
</p>
