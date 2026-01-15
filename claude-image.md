# Claude 图片分析 API 文档

## 📋 概述

Claude 图片分析 API 允许开发者通过 DMXAPI 服务调用 Claude 模型对图片进行智能分析。支持本地图片和网络图片两种方式。

## 🔗 请求地址

```text
https://www.dmxapi.cn/v1/messages
```

## 📁 本地图片分析

### 🐍 本地图片Python 调用示例

```python
"""
==============================================
DMXAPI Claude 图片分析测试脚本
==============================================
功能说明：
    使用 DMXAPI Claude API 对本地图片进行智能分析
    支持 JPG、PNG、GIF、WebP 等常见图片格式
==============================================
"""

import requests
import os
import base64
import json
from pathlib import Path

# ============== 基础配置 ==============
# DMXAPI 服务地址
NEWAPI_BASE_URL = "https://www.dmxapi.cn"

# DMXAPI 密钥（优先使用环境变量，可提高安全性）
API_KEY = os.getenv("NEWAPI_API_KEY") or "sk-********************************************"

# 本地图片路径（请修改为你的实际图片路径）
image_path = "test/example.jpg"

# ============== 请求头配置 ==============
headers = {
    "content-type": "application/json",
    "x-api-key": API_KEY
}

# ============== 工具函数 ==============

def get_image_media_type(file_path):
    """
    获取图片的 MIME 类型

    参数:
        file_path (str): 图片文件路径

    返回:
        str: 图片的 MIME 类型（如 'image/jpeg'）

    说明:
        根据文件扩展名自动识别图片类型，默认返回 'image/jpeg'
    """
    ext = Path(file_path).suffix.lower()

    # 支持的图片格式映射表
    media_types = {
        '.jpg': 'image/jpeg',
        '.jpeg': 'image/jpeg',
        '.png': 'image/png',
        '.gif': 'image/gif',
        '.webp': 'image/webp'
    }

    return media_types.get(ext, 'image/jpeg')


def encode_image_to_base64(file_path):
    """
    将本地图片编码为 Base64 字符串

    参数:
        file_path (str): 图片文件路径

    返回:
        str: Base64 编码的图片数据

    说明:
        将图片文件读取为二进制数据，然后转换为 Base64 字符串
        这是调用 Claude API 传递图片的标准方式
    """
    with open(file_path, 'rb') as f:
        return base64.b64encode(f.read()).decode('utf-8')



# ============== 主程序逻辑 ==============

# 步骤 1: 验证图片文件是否存在
if not os.path.exists(image_path):
    print(f"错误: 图片文件不存在: {image_path}")
    exit(1)

# 步骤 2: 处理图片数据
print(f"正在读取图片: {image_path}")
# 获取图片的 Base64 编码
image_data = encode_image_to_base64(image_path)
# 获取图片的 MIME 类型
media_type = get_image_media_type(image_path)

# 步骤 3: 构建 API 请求体
# 注意：Claude API 使用 Anthropic Messages API 格式
payload = {
    # 使用的模型（Claude Sonnet 4.5）
    "model": "claude-sonnet-4-5-20250929",

    # 消息数组
    "messages": [
        {
            "role": "user",  # 用户角色
            "content": [
                {
                    # 图片内容块
                    "type": "image",
                    "source": {
                        "type": "base64",
                        "media_type": media_type,  # 图片 MIME 类型
                        "data": image_data         # Base64 编码的图片数据
                    }
                },
                {
                    # 文本内容块（向 Claude 提问）
                    "type": "text",
                    "text": "这张图片里有什么?"
                }
            ]
        }
    ]
}

# 步骤 4: 发送 API 请求
print(f"正在分析图片: {image_path}")
response = requests.post(
    f"{NEWAPI_BASE_URL}/v1/messages",  # API 端点
    headers=headers,                    # 请求头（包含 API Key）
    json=payload                        # JSON 格式的请求体
)

# 步骤 5: 处理 API 响应
if response.status_code == 200:
    # 请求成功
    result = response.json()
    print("\n" + "="*50)
    print("分析成功！")
    print("="*50)
    print("\n响应内容:")
    # 使用 json.dumps() 格式化输出 JSON，缩进 2 个空格，显示中文字符
    print(json.dumps(result, indent=2, ensure_ascii=False))
else:
    # 请求失败
    print("\n" + "="*50)
    print(f"请求失败 (状态码: {response.status_code})")
    print("="*50)
    print("\n错误详情:")
    # 尝试格式化 JSON 错误响应
    try:
        error_json = response.json()
        print(json.dumps(error_json, indent=2, ensure_ascii=False))
    except:
        # 如果不是 JSON 格式，直接输出原始文本
        print(response.text)
```

### 📊 本地图片返回示例

```json
正在读取图片: test/example.jpg
正在分析图片: test/example.jpg

==================================================
分析成功！
==================================================

响应内容:
{
  "id": "msg_0143pgS3etx891xjeozb2ieK",
  "type": "message",
  "role": "assistant",
  "model": "claude-sonnet-4-5-20250929",
  "content": [
    {
      "type": "text",
      "text": "这张图片显示的是一台**佳能(Canon)计算器**，型号为WS-1212H。\n\n主要特征包括：\n\n1. **显示屏**：顶部有一个LCD显示屏，显示12位数字\n\n2. **按键布局**：\n   - 数字键：0-9，还有\"00\"键\n   - 基本运算键：加(+)、减(-)、乘(×)、除(÷)、等于(=)\n   - 功能键：包括MU、GT、CM、RM、M±、M=等记忆功能键\n   - 特殊键：平方根(√)、百分比(%±)、货币转换(£)\n   - 电源键：红色的ON/CA键和CI/C键\n\n3. **颜色**：银灰色和深灰色的配色方案，带有红色的功能键\n\n4. **背景**：计算器放置在 一块有蓝色和黄色花纹图案的布料上，旁边还能看到一条浅蓝色毛巾的边缘\n\n这是一款常见的办公或家用计算器，具备基本的算术运算和记忆功能。"
    }
  ],
  "stop_reason": "end_turn",
  "usage": {
    "input_tokens": 1584,
    "cache_creation_input_tokens": 0,
    "cache_read_input_tokens": 0,
    "output_tokens": 341,
    "claude_cache_creation_5_m_tokens": 0,
    "claude_cache_creation_1_h_tokens": 0
  }
}
```

## 🌐 URL 图片分析

### 🐍 Python 调用示例

```python
"""
==============================================
DMXAPI Claude 图片分析测试脚本
==============================================
功能说明：
    使用 DMXAPI Claude API 对图片 URL 进行智能分析
    支持任何可访问的图片 URL（JPG、PNG、GIF、WebP 等）
==============================================
"""

import requests
import os
import json

# ============== 基础配置 ==============
# DMXAPI 服务地址
NEWAPI_BASE_URL = "https://www.dmxapi.cn"

# DMXAPI 密钥（优先使用环境变量，可提高安全性）
API_KEY = os.getenv("NEWAPI_API_KEY") or "sk-********************************************"

# 图片 URL（请修改为你要分析的图片 URL）
image_url = "https://doc.dmxapi.cn/example.jpg"

# ============== 请求头配置 ==============
headers = {
    "content-type": "application/json",
    "x-api-key": API_KEY
}

# ============== 主程序逻辑 ==============

# 步骤 1: 验证图片 URL 格式
if not image_url.startswith(('http://', 'https://')):
    print(f"错误: 无效的图片 URL: {image_url}")
    exit(1)

# 步骤 2: 构建 API 请求体
# 注意：Claude API 使用 Anthropic Messages API 格式
print(f"正在分析图片: {image_url}")

payload = {
    # 使用的模型（Claude Sonnet 4.5）
    "model": "claude-sonnet-4-5-20250929",

    # 消息数组
    "messages": [
        {
            "role": "user",  # 用户角色
            "content": [
                {
                    # 图片内容块（使用 URL 方式）
                    "type": "image",
                    "source": {
                        "type": "url",
                        "url": image_url  # 直接传入图片 URL
                    }
                },
                {
                    # 文本内容块（向 Claude 提问）
                    "type": "text",
                    "text": "这张图片里有什么?"
                }
            ]
        }
    ]
}

# 步骤 3: 发送 API 请求
response = requests.post(
    f"{NEWAPI_BASE_URL}/v1/messages",  # API 端点
    headers=headers,                    # 请求头（包含 API Key）
    json=payload                        # JSON 格式的请求体
)

# 步骤 4: 处理 API 响应
if response.status_code == 200:
    # 请求成功
    result = response.json()
    print("\n" + "="*50)
    print("分析成功！")
    print("="*50)
    print("\n响应内容:")
    # 使用 json.dumps() 格式化输出 JSON，缩进 2 个空格，显示中文字符
    print(json.dumps(result, indent=2, ensure_ascii=False))
else:
    # 请求失败
    print("\n" + "="*50)
    print(f"请求失败 (状态码: {response.status_code})")
    print("="*50)
    print("\n错误详情:")
    # 尝试格式化 JSON 错误响应
    try:
        error_json = response.json()
        print(json.dumps(error_json, indent=2, ensure_ascii=False))
    except:
        # 如果不是 JSON 格式，直接输出原始文本
        print(response.text)
```

### 📊 返回示例

```json
正在分析图片: https://doc.dmxapi.cn/example.jpg

==================================================
分析成功！
==================================================

响应内容:
{
  "id": "msg_012L46ngXpVWzbicPbnr7ccB",
  "type": "message",
  "role": "assistant",
  "model": "claude-sonnet-4-5-20250929",
  "content": [
    {
      "type": "text",
      "text": "这张图片显示的是一台**佳能(Canon)计算器**，型号为WS-1212H。\n\n主要特点包括：\n\n1. **显示屏**：顶部有一个液晶显示屏\n2. **按键布局**：\n   - 数字键：0-9\n   - 基本运算键：加(+)、减(-)、乘(×)、除(÷)\n   - 功能键：MU、GT、CM 、RM、M±、M=（记忆功能）\n   - 特殊功能：百分比(%)、平方根(√)、货币转换(£)\n   - 电源键：红色的ON/CA键和CI/C键\n\n3. **颜色**：银灰色和白色相间的外观设计\n\n4. **背景**：计算器放在一张带有蓝色花纹图案的床单或布料上，旁边还能看到一条青绿色 的毛巾\n\n这是一款常见的桌面型商务计算器，适合日常计算和办公使用。"
    }
  ],
  "stop_reason": "end_turn",
  "usage": {
    "input_tokens": 1584,
    "cache_creation_input_tokens": 0,
    "cache_read_input_tokens": 0,
    "output_tokens": 303,
    "claude_cache_creation_5_m_tokens": 0,
    "claude_cache_creation_1_h_tokens": 0
  }
}
```

---

<p align="center">
  <small>© 2025 DMXAPI Claude图片分析</small>
</p>