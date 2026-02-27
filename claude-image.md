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
API_KEY = os.getenv("NEWAPI_API_KEY") or "sk-******************************"

# 本地图片路径（请修改为你的实际图片路径）
image_path = "./b9.png"

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
    # 使用的模型（claude-sonnet-4-6）
    "model": "claude-sonnet-4-6",

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
正在读取图片: ./b9.png
正在分析图片: ./b9.png

==================================================
分析成功！
==================================================

响应内容:
{
  "id": "msg_01QRwmZJm4CUdiDgSca4m1ga",
  "type": "message",
  "role": "assistant",
  "model": "claude-sonnet-4-6",
  "content": [
    {
      "type": "text",
      "text": "# 图片描述\n\n这是一幅**奇幻/科幻风格的概念艺术作品**，展现了一个宏大壮观的超现实场景：\n\n## 主要元素\n\n- **巨型古树**：画面中央有一棵极其庞大的古老树木，树干粗壮且布满苔藓和纹理，树上还生长着**黄色小花**\n- **一个人物**：在巨树的树干上，可以看到一个渺小的**探险者/冒险者**正在行走，凸显了树木的巨大尺度\n- **悬浮岩石**：天空中漂浮着数块**浮空巨石**，上面覆盖着绿色植被\n- **藤蔓与根系**：粗壮的藤蔓和根系从树木延伸开来，连接着不同的岩石和地面\n- **远景山脉**：背景中有雾气缭绕的**山峦**和广阔的平原\n- **金色光线**：整个场景沐浴在**日出或日落**的温暖金色光芒中，营造出梦幻般的氛围\n\n## 整体风格\n\n这幅作品很可能是某款**电子游戏的概念设计图**，具有典型的奇幻冒险游戏风格，让人联想到类似《阿凡达》或某些开放世界游戏中的异世界景观。画面构图宏大，强调了**人与自然的巨大比例差异**，营造出敬畏与探索的感觉。"
    }
  ],
  "stop_reason": "end_turn",
  "usage": {
    "input_tokens": 1364,
    "cache_creation_input_tokens": 0,
    "cache_read_input_tokens": 0,
    "output_tokens": 473,
    "cache_creation": {},
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
API_KEY = os.getenv("NEWAPI_API_KEY") or "sk-**********************************************"

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
    # 使用的模型（claude-sonnet-4-6）
    "model": "claude-sonnet-4-6",

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
  "id": "msg_01R2fsWjqcCjMBre3BzCjEUu",
  "type": "message",
  "role": "assistant",
  "model": "claude-sonnet-4-6",
  "content": [
    {
      "type": "text",
      "text": "## 图片内容\n\n这张图片展示了一台 **Canon（佳能）计算器**，型号为 **WS-1212H**。\n\n### 主要特征：\n- **品牌**：Canon（佳能）\n- **型号**：WS-1212H\n- **显示屏**：12位数字液晶显示屏\n- **颜色**：白色/灰色机身，深灰色按键\n- **特殊按键**：\n  - 红色的 **ON/CA**（开机/全清）和 **CI/C** 键\n  - **MU**（加成计算）、**GT**（总计）、**CM/RM**（存储）等功能键\n  - **√**（开方）、**%±** 等运算键\n- **电源**：支持**太阳能+电池**双电源（顶部有太阳能板）\n\n### 背景：\n计算器放在一张**蓝色大理石花纹的鼠标垫**上，旁边可以看到一条**充电线**和一块**浅绿色毛巾/布料**。"
    }
  ],
  "stop_reason": "end_turn",
  "usage": {
    "input_tokens": 1584,
    "cache_creation_input_tokens": 0,
    "cache_read_input_tokens": 0,
    "output_tokens": 317,
    "cache_creation": {},
    "claude_cache_creation_5_m_tokens": 0,
    "claude_cache_creation_1_h_tokens": 0
  }
}
```

---

<p align="center">
  <small>© 2025 DMXAPI Claude图片分析</small>
</p>