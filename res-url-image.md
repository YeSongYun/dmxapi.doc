# OpenAI Responses API 网络图片分析

本页演示通过 DMXAPI 兼容代理向 `gpt-5.6-sol` 传入公开图片 URL，并获取图片分析结果。

## 🔗 请求地址

```text
https://www.dmxapi.cn/v1/responses
```

:::warning API 密钥安全
示例令牌为不可用占位符。请妥善保管真实 DMXAPI 令牌，不要在公开代码或日志中泄露。
:::

## 模型名称
- 本页示例：`gpt-5.6-sol`
- 其他模型：替换 `model`，并检查该模型对推理、输出长度和工具参数的支持情况。
## Python 请求示例

```python
"""
================================================================
DMXAPI 多模态图片识别示例（Responses 接口）
================================================================
功能说明：
    本脚本演示如何使用 DMXAPI 的 responses 接口进行网络图片内容识别。
    支持通过 URL 方式传入图片，让 AI 模型分析并描述图片内容。

作者：DMXAPI 团队
================================================================
"""

import json
import requests

# ========================================
# API 配置信息
# ========================================
# 你的 DMXAPI 密钥（请替换为真实密钥）
API_KEY = "sk-***************************"

# DMXAPI 请求地址
url = "https://www.dmxapi.cn/v1/responses"

# ========================================
# 构建请求头
# ========================================
headers = {
    "Content-Type": "application/json",           # 指定请求内容类型为 JSON
    "Authorization": f"{API_KEY}"                 # 携带 API 密钥进行身份验证
}

# ========================================
# 构建请求体
# ========================================
payload = {
    "model": "gpt-5.6-sol",                 # 指定使用的 AI 模型
    "input": [                                    # 输入消息数组
        {
            "role": "user",                       # 消息角色：用户
            "content": [                          # 多模态内容数组
                {
                    "type": "input_text",         # 内容类型：文本
                    "text": "图片中是哪一种编程语言的标志？只回复语言名称。"  # 用户的文本提示
                },
                {
                    "type": "input_image",        # 内容类型：图片
                    "image_url": "https://www.python.org/static/community_logos/python-logo-master-v3-TM.png"  # 图片 URL 地址
                },
            ],
        }
    ],
}

# ========================================
# 发送 API 请求并处理响应
# ========================================
try:
    # 发送 POST 请求到 API 服务器
    response = requests.post(url, headers=headers, data=json.dumps(payload), timeout=120)

    # 检查 HTTP 响应状态码，如果出错会抛出异常
    response.raise_for_status()

    # ========================================
    # 输出成功结果
    # ========================================
    print("✅ 请求成功!")
    print("=" * 60)
    print("API 返回结果：")
    print("=" * 60)
    # 格式化输出 JSON 响应结果（保持中文显示）
    print(json.dumps(response.json(), indent=4, ensure_ascii=False))

except requests.exceptions.RequestException as e:
    # 捕获网络请求相关的所有异常（连接错误、超时、HTTP 错误等）
    print(f"❌ 请求失败: {e}")
except ValueError as e:
    # 捕获 JSON 解析错误等值相关的异常
    print(f"❌ 数据解析错误: {e}")
```

## 返回示例

```json
{
  "id": "resp_example_gpt56_url_image_001",
  "object": "response",
  "status": "completed",
  "model": "gpt-5.6-sol",
  "output": [
    {
      "id": "msg_example_gpt56_url_image_001",
      "type": "message",
      "status": "completed",
      "role": "assistant",
      "content": [
        {
          "type": "output_text",
          "text": "Python",
          "annotations": []
        }
      ]
    }
  ]
}
```

<p align="center">
  <small>© 2026 DMXAPI OpenAI Responses API 网络图片分析</small>
</p>
