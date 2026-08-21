# OpenAI Chat Completions 本地图片分析

本页演示将本地图片编码为 Base64 数据 URI，再通过 DMXAPI 兼容代理的 Chat Completions 接口交给 `gpt-5.6-sol` 分析。该请求形状已通过 DMXAPI 实测。

## 🔗 请求地址

```text
https://www.dmxapi.cn/v1/chat/completions
```

:::warning API 密钥安全
示例中的令牌为不可用占位符。请妥善保管真实 DMXAPI 令牌，不要在客户端或日志中泄露。
:::

## 模型名称

- `gpt-5.6-sol`

## Python 调用示例

```python
"""
================================================================================
DMX API 图片分析示例脚本
================================================================================
功能描述：
    使用 DMX API 的 GPT-5.6 Sol 模型分析本地图片内容
================================================================================
"""

import base64
import json
import requests


# ============================================================================
# 工具函数定义
# ============================================================================

def encode_image(image_path):
    """
    将本地图片文件编码为 Base64 字符串

    参数:
        image_path (str): 本地图片文件的路径

    返回:
        str: Base64 编码后的图片字符串

    异常:
        FileNotFoundError: 当图片文件不存在时抛出
    """
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")


# ============================================================================
# API 配置参数
# ============================================================================

# API 基础地址
BASE_URL = "https://www.dmxapi.cn/"

# 聊天补全接口端点
API_ENDPOINT = BASE_URL + "v1/chat/completions"

# API 密钥（请替换为你的实际密钥）
API_KEY = "sk-*****************************************"


# ============================================================================
# 准备请求数据
# ============================================================================

# 读取并编码本地图片
image_data = encode_image("img/cc_01.png")

# 构建请求载荷
payload = {
    "model": "gpt-5.6-sol",              # 使用替换成你需要的模型名称，例如 "gpt-5.6-sol"
    "messages": [
        {
            "role": "user",         # 用户角色
            "content": [
                {
                    "type": "text",
                    "text": "红色箭头指向哪个蓝色按钮？只回复按钮文字。"
                },
                {
                    "type": "image_url",
                    "image_url": {
                        # Base64 格式的图片数据
                        "url": f"data:image/png;base64,{image_data}"
                    }
                }
            ]
        }
    ],
    "temperature": 0.1              # 较低的温度值,使输出更确定和客观
}

# 构建请求头
headers = {
    "Content-Type": "application/json",
    "Authorization": f"{API_KEY}"
}


# ============================================================================
# 发送请求并处理响应
# ============================================================================

print("=" * 80)
print("正在向 DMX API 发送图片分析请求...")
print("=" * 80)

# 发送 POST 请求到 API 端点
response = requests.post(API_ENDPOINT, headers=headers, json=payload)

# 解析响应数据
result = response.json()

# 格式化输出结果
print("=" * 80)
print("API 响应结果")
print("=" * 80)

# 输出完整的 JSON 响应（美化格式）
print("【完整响应】")
print(json.dumps(result, indent=2, ensure_ascii=False))

# 提取并单独显示关键信息
if "choices" in result and len(result["choices"]) > 0:
    print("-" * 80)
    print("【图片分析结果】")
    print("-" * 80)
    content = result["choices"][0]["message"]["content"]
    print(content)

    # 输出使用统计
    if "usage" in result:
        print("-" * 80)
        print("【Token 使用统计】")
        print("-" * 80)
        usage = result["usage"]
        print(f"提示 Token 数: {usage.get('prompt_tokens', 0)}")
        print(f"补全 Token 数: {usage.get('completion_tokens', 0)}")
        print(f"总计 Token 数: {usage.get('total_tokens', 0)}")

    # 输出模型信息
    if "model" in result:
        print("-" * 80)
        print("【模型信息】")
        print("-" * 80)
        print(f"使用模型: {result['model']}")
        if "created" in result:
            from datetime import datetime
            timestamp = result['created']
            created_time = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
            print(f"创建时间: {created_time}")
else:
    # 如果响应格式异常，输出错误信息
    print("【错误】响应格式异常或请求失败")
    if "error" in result:
        print(f"错误信息: {result['error']}")

print("=" * 80)
```

## 返回示例

```json
{
  "id": "chatcmpl_example_gpt56_base64_image_001",
  "object": "chat.completion",
  "created": 1787270400,
  "model": "gpt-5.6-sol-2026-07-09",
  "choices": [
    {
      "index": 0,
      "message": {
        "role": "assistant",
        "content": "添加供应商"
      },
      "finish_reason": "stop"
    }
  ]
}
```

## 注意事项

- Base64 会增加请求体积；大图应关注上传时间、输入 token 与超时设置。
- 本页示例直接读取仓库内的 `img/cc_01.png`；红色箭头指向“添加供应商”按钮，便于验证模型确实读取了图片内容。
- 数据 URI 的 MIME 类型应与实际图片格式一致。
- 本地路径仅由客户端读取，不会作为路径字符串直接发送给模型。
- 二次验收中，仅替换为 `deepseek-v4-flash-0731` 会返回 HTTP 400、错误码 10305；该模型不适用于本页图片输入。

<p align="center">
  <small>© 2026 DMXAPI OpenAI 本地图片分析</small>
</p>
