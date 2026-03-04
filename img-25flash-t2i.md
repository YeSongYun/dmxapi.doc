# Gemini 2.5 Flash Image 文生图
通过 Gemini 2.5 Flash Image 模型快速生成图像，支持 10 种宽高比，固定 1K 分辨率。


## 接口地址

```
https://www.dmxapi.cn/v1beta/models/gemini-2.5-flash-image:generateContent

```
:::warning 注意：
需要升级谷歌sdk为最新版
:::

## 模型名称

### Gemini 2.5 Flash Image
- **模型名称**: `gemini-2.5-flash-image`
- **特点**: 快速生成，固定 1K 分辨率

## 示例代码

::: code-group

```python [SDK]
"""
DMXAPI Gemini 2.5 Flash Image 图像生成示例
使用 Google Gemini API 生成图像，并保存到本地 output 文件夹
"""

from google import genai
from google.genai import types
import os
from datetime import datetime

# ============================================================================
# 配置部分
# ============================================================================

# DMXAPI 密钥和基础 URL
api_key = "sk-************************************"  # 替换为你的 DMXAPI 密钥
BASE_URL = "https://www.dmxapi.cn"

# 创建 Gemini 客户端
client = genai.Client(api_key=api_key, http_options={'base_url': BASE_URL})

# ============================================================================
# 图像生成提示词
# ============================================================================

# 定义图像生成的提示词
prompt = (
    "Visualize the current weather forecast for the next 5 days in ShangHi as a clean, modern weather chart. Add a visual on what I should wear each day"
)

# ============================================================================
# 调用 DMXAPI 生成图像
# ============================================================================

response = client.models.generate_content(
    # 模型名称
    model="gemini-2.5-flash-image",

    # 输入内容
    contents=[prompt],

    # 生成配置
    config=types.GenerateContentConfig(
        # image_config: 图像配置选项
        image_config=types.ImageConfig(
            # aspect_ratio: 设置输出图片的宽高比
            #
            # ┌──────────┬─────────────┬────────┐
            # │ 宽高比    │ 分辨率      │ 令牌    │
            # ├──────────┼─────────────┼────────┤
            # │ 1:1      │ 1024x1024   │ 1290   │
            # │ 2:3      │ 832x1248    │ 1290   │
            # │ 3:2      │ 1248x832    │ 1290   │
            # │ 3:4      │ 864x1184    │ 1290   │
            # │ 4:3      │ 1184x864    │ 1290   │
            # │ 4:5      │ 896x1152    │ 1290   │
            # │ 5:4      │ 1152x896    │ 1290   │
            # │ 9:16     │ 768x1344    │ 1290   │
            # │ 16:9     │ 1344x768    │ 1290   │
            # │ 21:9     │ 1536x672    │ 1290   │
            # └──────────┴─────────────┴────────┘
            #
            aspect_ratio="1:1",
        ),
    )
)

# ============================================================================
# 处理响应并保存图像
# ============================================================================

for part in response.parts:
    # 处理文本响应（如果有）
    if part.text is not None:
        print(part.text)

    # 处理图像响应
    elif part.inline_data is not None:
        # 确保 output 文件夹存在
        os.makedirs("output", exist_ok=True)

        # 生成带时间戳的文件名
        # 格式: generated_image_20250121_143052.png (年月日_时分秒)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"output/generated_image_{timestamp}.png"

        # 将响应数据转换为 PIL Image 对象
        image = part.as_image()

        # 保存图像到文件
        image.save(filename)

        # 输出保存成功的提示信息
        print(f"图片已保存到 {filename}")
```

```python [request]
"""
Gemini 2.5 Flash Image - 文生图 API 调用示例
=================================================
"""

import requests  # HTTP 请求库
import base64    # Base64 编解码库

# ============================================================================
# API 配置
# ============================================================================
# DMXAPI 密钥 (请替换为你的实际密钥)
API_KEY = "sk-****************************************"

# API 请求地址
API_URL = "https://www.dmxapi.cn/v1beta/models/gemini-2.5-flash-image:generateContent"

# ============================================================================
# 请求头
# ============================================================================
headers = {
    "x-goog-api-key": API_KEY,       # API 认证密钥
    "Content-Type": "application/json"  # 请求内容类型为 JSON
}

# ============================================================================
# 请求体
# ============================================================================
data = {
    "contents": [{                   # 内容数组
        "parts": [                   # 消息部分
            {
                # 图片生成提示词 (修改此处描述你想要生成的图片)
                "text": "生成一个美丽的日落风景，色彩丰富，充满艺术感。",
            }
        ]
    }],

    # ========================================================================
    # 生成配置
    # ========================================================================
    "generationConfig": {
        # imageConfig: 图像配置选项
        "imageConfig": {
            # aspectRatio: 设置输出图片的宽高比
            #
            # ┌──────────┬─────────────┬────────┐
            # │ 宽高比    │ 分辨率      │ 令牌    │
            # ├──────────┼─────────────┼────────┤
            # │ 1:1      │ 1024x1024   │ 1290   │
            # │ 2:3      │ 832x1248    │ 1290   │
            # │ 3:2      │ 1248x832    │ 1290   │
            # │ 3:4      │ 864x1184    │ 1290   │
            # │ 4:3      │ 1184x864    │ 1290   │
            # │ 4:5      │ 896x1152    │ 1290   │
            # │ 5:4      │ 1152x896    │ 1290   │
            # │ 9:16     │ 768x1344    │ 1290   │
            # │ 16:9     │ 1344x768    │ 1290   │
            # │ 21:9     │ 1536x672    │ 1290   │
            # └──────────┴─────────────┴────────┘
            "aspectRatio": "1:1"
        }
    }
}

# ============================================================================
# 发送请求
# ============================================================================
response = requests.post(
    API_URL,          # 请求地址
    headers=headers,  # 请求头
    json=data         # 请求体 (自动序列化为 JSON)
)

# ============================================================================
# 响应处理
# ============================================================================
if response.status_code == 200:
    # 请求成功，解析 JSON 响应
    result = response.json()

    try:
        # 响应结构: candidates[0].content.parts[].inlineData.data
        parts = result["candidates"][0]["content"]["parts"]

        for part in parts:
            # 检查是否包含图片数据
            if "inlineData" in part:
                # 提取 Base64 编码的图片数据
                image_data = part["inlineData"]["data"]

                # Base64 解码为二进制数据
                image_bytes = base64.b64decode(image_data)

                # 输出文件名
                output_file = "gemini-native-image.png"

                # 写入文件
                with open(output_file, "wb") as f:
                    f.write(image_bytes)

                print(f"[成功] 图片已保存: {output_file}")
                break

    except (KeyError, IndexError) as e:
        # 响应结构异常
        print(f"[错误] 响应解析失败: {e}")
        print(f"[调试] 响应内容: {result}")

else:
    # 请求失败
    print(f"[错误] API 请求失败, 状态码: {response.status_code}")
    print(f"[调试] 错误信息: {response.text}")
```

:::

## 返回示例

::: code-group

```json [SDK]
图片已保存到 output/generated_image_20260227_183649.png
```

```json [request]
[成功] 图片已保存: gemini-native-image.png
```

:::

## 注意事项

- 请将代码中的 API 密钥替换为你自己的 DMXAPI 密钥
- 生成的图像会自动保存到 `output` 文件夹（如不存在会自动创建）
- gemini-2.5-flash-image 仅支持 1K 分辨率，不支持 `image_size`、`response_modalities`、`tools` 参数
- 为获得最佳性能，请使用以下语言：英语、阿拉伯语（埃及）、德语（德国）、西班牙语（墨西哥）、法语（法国）、印地语（印度）、印度尼西亚语（印度尼西亚）、意大利语（意大利）、日语（日本）、韩语（韩国）、葡萄牙语（巴西）、俄语（俄罗斯）、乌克兰语（乌克兰）、越南语（越南）、中文（中国）。

---

<p align="center">
  <small>© 2025 DMXAPI Gemini模型</small>
</p>
