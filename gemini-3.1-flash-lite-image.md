# Gemini 3.1 Flash Lite Image 文生图（Nano Banana 2 Lite）
通过 Gemini 3.1 Flash Lite Image 模型快速生成图像，速度最快、成本最低，适合大批量、低延迟的图片生成任务。



## 接口地址

```
https://www.dmxapi.cn/v1beta/models/gemini-3.1-flash-lite-image:generateContent

```
:::warning 注意：
需要升级谷歌sdk为最新版
:::

## 模型名称

### Gemini 3.1 Flash Lite Image
- **模型名称**: `gemini-3.1-flash-lite-image`
- **别名**: Nano Banana 2 Lite
- **特点**: 速度最快、成本最低，仅支持 1K 分辨率
- **适用场景**: 大批量、低延迟的图片生成任务（官方提示：不适合处理多个参考输入或多轮连续编辑）

## 示例代码

::: code-group

```python [SDK]
"""
DMXAPI Gemini 3.1 Flash Lite Image 图像生成示例
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
    "Create a picture of a nano banana dish in a fancy restaurant with a Gemini theme"
)

# ============================================================================
# 调用 DMXAPI 生成图像
# ============================================================================

response = client.models.generate_content(
    # 模型名称
    model="gemini-3.1-flash-lite-image",

    # 输入内容
    contents=[prompt],

    # 生成配置
    config=types.GenerateContentConfig(
        # response_modalities: 设置响应模态
        # - ['Image']: 仅返回图片，不返回文本
        # - ['Text', 'Image']: 同时返回文本和图片（默认值）
        response_modalities=['Image'],

        # image_config: 图像配置选项
        image_config=types.ImageConfig(
            # aspect_ratio: 设置输出图片的宽高比
            #
            # ┌────────────────────────────────┐
            # │ Gemini 3.1 Flash Lite Image     │
            # ├──────────┬─────────────────────┤
            # │ 宽高比    │ 1K 分辨率           │
            # ├──────────┼─────────────────────┤
            # │ 1:1      │ 1024x1024           │
            # │ 2:3      │ 848x1264            │
            # │ 3:2      │ 1264x848            │
            # │ 3:4      │ 896x1200            │
            # │ 4:3      │ 1200x896            │
            # │ 4:5      │ 928x1152            │
            # │ 5:4      │ 1152x928            │
            # │ 9:16     │ 768x1376            │
            # │ 16:9     │ 1376x768            │
            # │ 21:9     │ 1584x672            │
            # └──────────┴─────────────────────┘
            # 注: gemini-3.1-flash-lite-image 仅支持 1K 分辨率
            #
            aspect_ratio="1:1",

            # image_size: 设置输出图片的分辨率
            # - "1K": 1K 分辨率（Lite 模型仅支持 1K）
            image_size="1K",
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
Gemini 3.1 Flash Lite Image - 文生图 API 调用示例
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
API_URL = "https://www.dmxapi.cn/v1beta/models/gemini-3.1-flash-lite-image:generateContent"

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
                "text": "Create a picture of a nano banana dish in a fancy restaurant with a Gemini theme",
            }
        ]
    }],

    # ========================================================================
    # 生成配置
    # ========================================================================
    "generationConfig": {
        # responseModalities: 设置响应模态
        # - ["IMAGE"]: 仅返回图片，不返回文本
        # - ["TEXT", "IMAGE"]: 同时返回文本和图片（默认值）
        "responseModalities": ["IMAGE"],

        # imageConfig: 图像配置选项
        "imageConfig": {
            # aspectRatio: 设置输出图片的宽高比
            #
            # ┌────────────────────────────────┐
            # │ Gemini 3.1 Flash Lite Image     │
            # ├──────────┬─────────────────────┤
            # │ 宽高比    │ 1K 分辨率           │
            # ├──────────┼─────────────────────┤
            # │ 1:1      │ 1024x1024           │
            # │ 2:3      │ 848x1264            │
            # │ 3:2      │ 1264x848            │
            # │ 3:4      │ 896x1200            │
            # │ 4:3      │ 1200x896            │
            # │ 4:5      │ 928x1152            │
            # │ 5:4      │ 1152x928            │
            # │ 9:16     │ 768x1376            │
            # │ 16:9     │ 1376x768            │
            # │ 21:9     │ 1584x672            │
            # └──────────┴─────────────────────┘
            # 注: gemini-3.1-flash-lite-image 仅支持 1K 分辨率
            "aspectRatio": "1:1",

            # imageSize: 设置输出图片的分辨率
            # - "1K": 1K 分辨率（Lite 模型仅支持 1K）
            # "imageSize": "1K",
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

```text [SDK]
图片已保存到 output/generated_image_20260702_103512.png
```

```json [request]
[成功] 图片已保存: gemini-native-image.png
```

:::

<p align="center">
  <small>© 2026 DMXAPI Gemini模型</small>
</p>