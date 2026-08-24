# OpenAI Chat Completions 网络图片分析

本页演示通过 DMXAPI 兼容代理调用 `gpt-5.6-sol`，使用 Chat Completions 的 `image_url` 内容项分析公网图片。
## 🔗 请求地址
```text
https://www.dmxapi.cn/v1/chat/completions
```
## 模型名称
- 本页示例：`gpt-5.6-sol`
- 其他模型：替换 `model`，并检查该模型对推理、输出长度和工具参数的支持情况。
## Python 调用示例

```python
"""
图片分析工具 - 使用 gpt-5.6-sol 模型进行网络图片内容分析
============================================================
本脚本演示如何通过 DMXAPI 调用 OpenAI 兼容的 chat/completions 接口
以图片 URL 方式传入网络图片，让模型分析并描述图片内容
适用于图片描述、物体识别、票据识别等应用场景
"""

import requests

# ============================================================
# API 配置区域
# ============================================================
BASE_URL = "https://www.dmxapi.cn/"                                      # API 基础地址
API_ENDPOINT = BASE_URL + "v1/chat/completions"                          # 对话完成接口
API_KEY = "sk-*************************************************"         # API 密钥(请替换为你的密钥)
MODEL = "gpt-5.6-sol"                                              # 使用的模型名称
IMAGE_URL = "https://www.python.org/static/community_logos/python-logo-master-v3-TM.png"                  # 待分析图片的 URL 地址

# ============================================================
# 核心功能函数
# ============================================================
def analyze_image(image_url, prompt):
    """
    调用模型分析网络图片内容

    功能说明:
        通过 DMXAPI 调用 gpt-5.6-sol 模型,对指定 URL 的图片进行智能分析
        支持图片描述、物体识别、场景理解等多种分析任务

    参数:
        image_url (str): 图片的 URL 地址,需要是公网可访问的链接
        prompt (str): 分析提示词,描述你希望模型如何分析这张图片
    """
    # 构建请求载荷(单条 user 消息,内容包含文本提示与图片 URL)
    payload = {
        "model": MODEL,                                                  # 使用的模型名称
        "messages": [
            {
                "role": "user",                                          # 用户角色:发送分析请求
                "content": [
                    {"type": "text", "text": prompt},                    # 分析提示词
                    {"type": "image_url", "image_url": {"url": image_url}}  # 图片 URL
                ]
            }
        ]
    }

    # 构建请求头
    headers = {
        "Content-Type": "application/json",                              # 内容类型:JSON 格式
        "Authorization": f"{API_KEY}"                                    # 授权令牌
    }

    # 发送 API 请求并处理响应
    try:
        response = requests.post(API_ENDPOINT, headers=headers, json=payload, timeout=120)
        response.raise_for_status()                                      # 检查 HTTP 状态码
        return response.json()["choices"][0]["message"]["content"]       # 提取分析结果文本
    except Exception as e:
        print(f"❌ 请求失败: {e}")                                        # 错误提示
        return None

# ============================================================
# 程序入口
# ============================================================
if __name__ == "__main__":
    print("=" * 60)
    print("开始分析图片...")
    print("=" * 60)

    # 调用图片分析函数
    result = analyze_image(
        IMAGE_URL,
        "图片中是哪一种编程语言的标志？只回复语言名称。",
    )

    # 输出分析结果
    if result:
        print("✅ 分析结果:")
        print("-" * 60)
        print(result)
        print("-" * 60)
    else:
        print("❌ 图片分析失败,请检查配置和网络连接")
```

## 返回示例

```json
{
  "id": "chatcmpl_example_gpt56_image_url_001",
  "object": "chat.completion",
  "created": 1787270400,
  "model": "gpt-5.6-sol-2026-07-09",
  "choices": [
    {
      "index": 0,
      "message": {
        "role": "assistant",
        "content": "Python"
      },
      "finish_reason": "stop"
    }
  ]
}
```

## 注意事项

- `image_url.url` 必须是模型服务可访问的公网图片直链。

<p align="center">
  <small>© 2026 DMXAPI OpenAI 网络图片分析</small>
</p>
