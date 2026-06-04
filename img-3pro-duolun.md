# Gemini 3 Pro Image Preview 多轮图片修改 API 文档

Gemini 3 Pro Image 的多轮图片修改功能支持你以"对话"的方式来生成并持续调整图片：你可以先用一句话描述想要的画面生成初稿，然后像和设计师沟通一样，在后续轮次里不断补充细节或提出修改要求，例如更换背景、调整风格与色调、添加或删除元素、改变人物姿态与表情等。系统会理解上下文并记住前几轮的修改结果，每一次调整都会基于上一张图继续迭代，因此不需要你反复从头描述。整体上，建议用聊天或多轮对话逐步打磨作品，从"先有大方向"到"再精修细节"，效率更高、效果也更可控。

## 模型名称
`gemini-3-pro-image-preview`



## 请求地址


```
 https://www.dmxapi.cn/v1beta/models/gemini-3-pro-image-preview:generateContent

```
:::warning

 注意：请妥善保管API密钥，不要泄露给他人。
:::

## 图片生成 调用示例
```python
"""
================================================================================
Gemini 3 Pro Image 图片生成示例 - 01
================================================================================
功能说明：
    本脚本演示如何使用 Gemini 3 Pro Image API 根据文本提示生成图片。
    生成的图片会保存到本地，同时 base64 数据和思考签名也会保存以供后续多轮对话使用。
================================================================================
"""

import requests
import json
import base64
import os
from datetime import datetime

# ==============================================================================
# 配置区域
# ==============================================================================

# API 请求地址
url = "https://www.dmxapi.cn/v1beta/models/gemini-3-pro-image-preview:generateContent"

# API 密钥（请妥善保管，不要泄露）
api_key = "sk-**********************************************************************"

# 请求头配置
headers = {
    "x-goog-api-key": api_key,          # API 认证密钥
    "Content-Type": "application/json"   # 内容类型为 JSON
}

# ==============================================================================
# 请求数据构建
# ==============================================================================

data = {
    # -------------------------------------------------------------------------
    # contents: 对话内容列表
    # -------------------------------------------------------------------------
    "contents": [{
        "role": "user",
        "parts": [
            {"text": "一只4B铅笔"}  # 图片生成提示词
        ]
    }],

    # -------------------------------------------------------------------------
    # tools: Google 搜索工具（可选）
    # -------------------------------------------------------------------------
    "tools": [
        {"google_search": {}}
    ],

    # -------------------------------------------------------------------------
    # generationConfig: 生成配置
    # -------------------------------------------------------------------------
    "generationConfig": {
        "responseModalities": ["TEXT", "IMAGE"]  # 响应模态：同时返回文本和图片
    }
}

# ==============================================================================
# 创建数据保存目录
# ==============================================================================

base64_folder = "base64_data"
if not os.path.exists(base64_folder):
    os.makedirs(base64_folder)
    print(f"已创建目录: {base64_folder}")

# 新增：思考签名保存目录
signature_folder = "signature_data"
if not os.path.exists(signature_folder):
    os.makedirs(signature_folder)
    print(f"已创建目录: {signature_folder}")

# ==============================================================================
# 发送 API 请求
# ==============================================================================

print("=" * 60)
print("正在发送请求到 Gemini API...")
print("=" * 60)

response = requests.post(url, headers=headers, json=data)
result = response.json()

if result.get("candidates"):
    print("\n" + "=" * 60)
    print("响应解析成功！")
    print("=" * 60 + "\n")

    for candidate in result["candidates"]:
        if "content" in candidate and "parts" in candidate["content"]:
            for part in candidate["content"]["parts"]:
                # 统一生成时间戳（同一 part 的多种数据共用）
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

                # -------------------------------------------------------------
                # 处理文本部分
                # -------------------------------------------------------------
                if "text" in part:
                    print("+" + "-" * 58 + "+")
                    print("| 文本内容                                                 |")
                    print("+" + "-" * 58 + "+")
                    print(part["text"])
                    print("+" + "-" * 58 + "+\n")

                # -------------------------------------------------------------
                # 处理图片部分（Base64 格式）
                # -------------------------------------------------------------
                if "inlineData" in part:
                    mime_type = part["inlineData"].get("mimeType", "image/png")
                    base64_data = part["inlineData"].get("data", "")

                    # 生成带时间戳的文件名
                    extension = mime_type.split("/")[-1]
                    filename = f"gemini_image_{timestamp}.{extension}"

                    # 解码 Base64 数据并保存图片到本地
                    image_data = base64.b64decode(base64_data)
                    with open(filename, "wb") as f:
                        f.write(image_data)

                    # 保存 Base64 数据到文件（供多轮对话使用）
                    base64_filename = os.path.join(base64_folder, f"gemini_base64_{timestamp}.txt")
                    with open(base64_filename, "w", encoding="utf-8") as f:
                        f.write(base64_data)

                    print("+" + "-" * 58 + "+")
                    print("| 图片信息                                                 |")
                    print("+" + "-" * 58 + "+")
                    print(f"| 图片文件: {filename:<46} |")
                    print(f"| Base64文件: {base64_filename:<44} |")
                    print(f"| MIME类型: {mime_type:<46} |")
                    print(f"| 数据长度: {len(base64_data):,} 字符{' ' * (39 - len(f'{len(base64_data):,}'))} |")
                    print("+" + "-" * 58 + "+")
                    print("| 图片和 Base64 数据已成功保存！                            |")
                    print("+" + "-" * 58 + "+\n")

                # -------------------------------------------------------------
                # 处理图片部分（URL 格式）
                # -------------------------------------------------------------
                if "fileData" in part:
                    file_uri = part["fileData"].get("fileUri", "")
                    mime_type = part["fileData"].get("mimeType", "")

                    print("+" + "-" * 58 + "+")
                    print("| 图片链接                                                 |")
                    print("+" + "-" * 58 + "+")
                    print(f"| URL: {file_uri[:50]:<52} |")
                    print(f"| MIME类型: {mime_type:<46} |")
                    print("+" + "-" * 58 + "+\n")

                # -------------------------------------------------------------
                # 处理思考签名部分（thoughtSignature）  ← 新增
                # - 用于多轮对话时保持思维链连续性，需原样回传
                # -------------------------------------------------------------
                if "thoughtSignature" in part:
                    thought_signature = part["thoughtSignature"]

                    # 保存思考签名到文件（供多轮对话使用）
                    signature_filename = os.path.join(
                        signature_folder, f"gemini_signature_{timestamp}.txt"
                    )
                    with open(signature_filename, "w", encoding="utf-8") as f:
                        f.write(thought_signature)

                    print("+" + "-" * 58 + "+")
                    print("| 思考签名 (thoughtSignature)                              |")
                    print("+" + "-" * 58 + "+")
                    print(f"| 签名文件: {signature_filename:<46} |")
                    print(f"| 签名长度: {len(thought_signature):,} 字符{' ' * (39 - len(f'{len(thought_signature):,}'))} |")
                    print("+" + "-" * 58 + "+")
                    print("| 思考签名已成功保存！（多轮对话需原样回传）                |")
                    print("+" + "-" * 58 + "+\n")

    # -------------------------------------------------------------------------
    # 额外：保存完整的 model parts（含思考签名），方便多轮对话直接复用  ← 新增
    # -------------------------------------------------------------------------
    full_timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    model_parts_filename = os.path.join(signature_folder, f"model_parts_{full_timestamp}.json")
    model_parts = result["candidates"][0].get("content", {}).get("parts", [])
    with open(model_parts_filename, "w", encoding="utf-8") as f:
        json.dump(model_parts, f, ensure_ascii=False, indent=2)
    print(f"完整 model parts（含签名）已保存: {model_parts_filename}\n")

else:
    # -------------------------------------------------------------------------
    # 错误处理：响应中没有 candidates 字段
    # -------------------------------------------------------------------------
    print("\n" + "=" * 60)
    print("响应异常，完整内容如下：")
    print("=" * 60)
    print(json.dumps(result, indent=2, ensure_ascii=False))
    print("=" * 60 + "\n")

# ==============================================================================
# 脚本结束
# ==============================================================================
print("\n" + "=" * 60)
print("脚本执行完毕")
print("=" * 60)
```

## 返回示例
```json
============================================================
正在发送请求到 Gemini API...
============================================================

============================================================
响应解析成功！
============================================================

+----------------------------------------------------------+
| 图片信息                                                 |
+----------------------------------------------------------+
| 图片文件: gemini_image_20260604_123835.jpeg              |
| Base64文件: base64_data\gemini_base64_20260604_123835.txt |
| MIME类型: image/jpeg                                     |
| 数据长度: 815,800 字符                                 |
+----------------------------------------------------------+
| 图片和 Base64 数据已成功保存！                            |
+----------------------------------------------------------+

+----------------------------------------------------------+
| 思考签名 (thoughtSignature)                              |
+----------------------------------------------------------+
| 签名文件: signature_data\gemini_signature_20260604_123835.txt |
| 签名长度: 738,356 字符                                 |
+----------------------------------------------------------+
| 思考签名已成功保存！（多轮对话需原样回传）                |
+----------------------------------------------------------+

完整 model parts（含签名）已保存: signature_data\model_parts_20260604_123835.json


============================================================
脚本执行完毕
============================================================
```


## 多轮对话 示例代码

```python
"""
================================================================================
Gemini 3 Pro Image 多轮图片修改示例 - 02（含思考签名回传）
================================================================================
功能说明：
    本脚本演示如何使用 Gemini 3 Pro Image API 进行多轮对话式图片编辑。
    通过传递历史对话、之前生成的图片，以及思考签名（thoughtSignature），
    可以让大模型在原图基础上进行修改，并保持思维链连续性。
================================================================================
"""
import requests
import json
import base64
import os
from datetime import datetime

# ==============================================================================
# 配置区域
# ==============================================================================

# API 请求地址
url = "https://www.dmxapi.cn/v1beta/models/gemini-3-pro-image-preview:generateContent"

# API 密钥（请妥善保管，不要泄露）
api_key = "sk-**********************************************************************"

# -----------------------------------------------------------------------------
# 上一轮生成的图片 base64 数据文件路径
# 注意：请替换为示例 01 实际生成的 base64 文件名（文件名带时间戳）
# -----------------------------------------------------------------------------
base64_file = r"base64_data\gemini_base64_20260604_123835.txt"
with open(base64_file, "r", encoding="utf-8") as f:
    previous_image_data = f.read().strip()

# -----------------------------------------------------------------------------
# 上一轮生成的思考签名文件路径（由脚本 01 保存）  ← 新增
# - 如果存在则读取，并在第 2 轮 model part 中原样回传
# 注意：请替换为示例 01 实际生成的签名文件名（文件名带时间戳）
# -----------------------------------------------------------------------------
signature_file = r"signature_data\gemini_signature_20260604_123835.txt"
previous_thought_signature = None
if os.path.exists(signature_file):
    with open(signature_file, "r", encoding="utf-8") as f:
        previous_thought_signature = f.read().strip()
    print(f"已读取上一轮思考签名: {signature_file}（长度 {len(previous_thought_signature):,} 字符）")
else:
    print(f"未找到思考签名文件，将不回传签名: {signature_file}")

# 请求头配置
headers = {
    "x-goog-api-key": api_key,          # API 认证密钥
    "Content-Type": "application/json"   # 内容类型为 JSON
}


# ==============================================================================
# 多轮对话数据构建
# ==============================================================================
#
# 对话结构说明：
# ┌─────────────────────────────────────────────────────────────────────────────┐
# │  第 1 轮 (user)  : 用户发起初始请求                                          │
# │  第 2 轮 (model) : 模型返回的图片 + 思考签名（原样回传）                      │
# │  第 3 轮 (user)  : 用户基于上一轮图片，提出修改要求                           │
# └─────────────────────────────────────────────────────────────────────────────┘
#

# -----------------------------------------------------------------------------
# 构建第 2 轮 model 的 part：图片数据 + 思考签名
# -----------------------------------------------------------------------------
model_image_part = {
    "inline_data": {
        "mime_type": "image/jpeg",           # 图片 MIME 类型
        "data": previous_image_data          # 从文件读取的 base64 数据
    }
}

# 如果上一轮返回了思考签名，则原样附加到该 part 中  ← 新增
if previous_thought_signature:
    model_image_part["thoughtSignature"] = previous_thought_signature

data = {
    # -------------------------------------------------------------------------
    # contents: 对话内容列表，按时间顺序排列
    # -------------------------------------------------------------------------
    "contents": [
        # 第 1 轮：用户初始请求
        {
            "role": "user",
            "parts": [{"text": "一只4B铅笔"}]
        },
        # 第 2 轮：模型返回的图片（含思考签名）
        {
            "role": "model",
            "parts": [model_image_part]
        },
        # 第 3 轮：用户的修改请求
        {
            "role": "user",
            "parts": [{"text": "给铅笔加上小翅膀"}]
        }
    ],

    # -------------------------------------------------------------------------
    # tools: Google 搜索工具（可选）
    # -------------------------------------------------------------------------
    "tools": [
        {"google_search": {}}
    ],

    # -------------------------------------------------------------------------
    # generationConfig: 生成配置
    # -------------------------------------------------------------------------
    "generationConfig": {
        # 响应模态：同时返回文本和图片
        "responseModalities": ["TEXT", "IMAGE"],

        # 图片配置
        "imageConfig": {
            "aspectRatio": "16:9",           # 宽高比：16:9
            "imageSize": "2K"                # 图片分辨率：2K 高清
        }
    }
}


# ==============================================================================
# 创建数据保存目录
# ==============================================================================

base64_folder = "base64_data"
if not os.path.exists(base64_folder):
    os.makedirs(base64_folder)

signature_folder = "signature_data"
if not os.path.exists(signature_folder):
    os.makedirs(signature_folder)


# ==============================================================================
# 发送 API 请求
# ==============================================================================

print("=" * 60)
print("正在发送请求到 Gemini API...")
print("=" * 60)

response = requests.post(url, headers=headers, json=data)
result = response.json()

if result.get("candidates"):
    print("\n" + "=" * 60)
    print("响应解析成功！")
    print("=" * 60 + "\n")

    for candidate in result["candidates"]:
        if "content" in candidate and "parts" in candidate["content"]:
            for part in candidate["content"]["parts"]:
                # 统一时间戳
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

                # -------------------------------------------------------------
                # 处理文本部分
                # -------------------------------------------------------------
                if "text" in part:
                    print("+" + "-" * 58 + "+")
                    print("| 文本内容                                                 |")
                    print("+" + "-" * 58 + "+")
                    print(part["text"])
                    print("+" + "-" * 58 + "+\n")

                # -------------------------------------------------------------
                # 处理图片部分（Base64 格式）
                # -------------------------------------------------------------
                if "inlineData" in part:
                    mime_type = part["inlineData"].get("mimeType", "image/png")
                    base64_data = part["inlineData"].get("data", "")

                    extension = mime_type.split("/")[-1]
                    filename = f"gemini_image_{timestamp}.{extension}"

                    # 解码 Base64 数据并保存图片
                    image_data = base64.b64decode(base64_data)
                    with open(filename, "wb") as f:
                        f.write(image_data)

                    # 保存本轮 base64 数据（供下一轮继续使用）
                    base64_filename = os.path.join(base64_folder, f"gemini_base64_{timestamp}.txt")
                    with open(base64_filename, "w", encoding="utf-8") as f:
                        f.write(base64_data)

                    print("+" + "-" * 58 + "+")
                    print("| 图片信息                                                 |")
                    print("+" + "-" * 58 + "+")
                    print(f"| 文件名称: {filename:<46} |")
                    print(f"| Base64文件: {base64_filename:<44} |")
                    print(f"| MIME类型: {mime_type:<46} |")
                    print(f"| 数据长度: {len(base64_data):,} 字符{' ' * (39 - len(f'{len(base64_data):,}'))} |")
                    print("+" + "-" * 58 + "+")
                    print("| 图片已成功保存到本地！                                    |")
                    print("+" + "-" * 58 + "+\n")

                # -------------------------------------------------------------
                # 处理图片部分（URL 格式）
                # -------------------------------------------------------------
                if "fileData" in part:
                    file_uri = part["fileData"].get("fileUri", "")
                    mime_type = part["fileData"].get("mimeType", "")

                    print("+" + "-" * 58 + "+")
                    print("| 图片链接                                                 |")
                    print("+" + "-" * 58 + "+")
                    print(f"| URL: {file_uri[:50]:<52} |")
                    print(f"| MIME类型: {mime_type:<46} |")
                    print("+" + "-" * 58 + "+\n")

                # -------------------------------------------------------------
                # 处理思考签名部分（thoughtSignature）  ← 新增
                # - 保存本轮返回的签名，供再下一轮对话继续回传
                # -------------------------------------------------------------
                if "thoughtSignature" in part:
                    thought_signature = part["thoughtSignature"]

                    signature_filename = os.path.join(
                        signature_folder, f"gemini_signature_{timestamp}.txt"
                    )
                    with open(signature_filename, "w", encoding="utf-8") as f:
                        f.write(thought_signature)

                    print("+" + "-" * 58 + "+")
                    print("| 思考签名 (thoughtSignature)                              |")
                    print("+" + "-" * 58 + "+")
                    print(f"| 签名文件: {signature_filename:<46} |")
                    print(f"| 签名长度: {len(thought_signature):,} 字符{' ' * (39 - len(f'{len(thought_signature):,}'))} |")
                    print("+" + "-" * 58 + "+")
                    print("| 思考签名已保存！（下一轮对话可继续回传）                  |")
                    print("+" + "-" * 58 + "+\n")

else:
    # -------------------------------------------------------------------------
    # 错误处理
    # -------------------------------------------------------------------------
    print("\n" + "=" * 60)
    print("响应异常，完整内容如下：")
    print("=" * 60)
    print(json.dumps(result, indent=2, ensure_ascii=False))
    print("=" * 60 + "\n")


# ==============================================================================
# 脚本结束
# ==============================================================================
print("\n" + "=" * 60)
print("脚本执行完毕")
print("=" * 60)
```

## 返回示例
```json
已读取上一轮思考签名: signature_data\gemini_signature_20260604_123835.txt（长度 738,356 字符）
============================================================
正在发送请求到 Gemini API...
============================================================

============================================================
响应解析成功！
============================================================

+----------------------------------------------------------+
| 图片信息                                                 |
+----------------------------------------------------------+
| 文件名称: gemini_image_20260604_124234.jpeg              |
| Base64文件: base64_data\gemini_base64_20260604_124234.txt |
| MIME类型: image/jpeg                                     |
| 数据长度: 3,066,852 字符                               |
+----------------------------------------------------------+
| 图片已成功保存到本地！                                    |
+----------------------------------------------------------+

+----------------------------------------------------------+
| 思考签名 (thoughtSignature)                              |
+----------------------------------------------------------+
| 签名文件: signature_data\gemini_signature_20260604_124234.txt |
| 签名长度: 3,221,988 字符                               |
+----------------------------------------------------------+
| 思考签名已保存！（下一轮对话可继续回传）                  |
+----------------------------------------------------------+


============================================================
脚本执行完毕
============================================================
```


<p align="center">
  <small>© 2026 DMXAPI gemini多轮图片修改</small>
</p>