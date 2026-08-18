# Gemini 多轮对话 API使用文档

## 📋 概述

本文档介绍如何使用 Gemini API 进行多轮对话。


## 🌐 请求地址

```
https://www.dmxapi.cn/v1beta/models/{model}:generateContent

```

## 💻 Python 示例代码

::: code-group
```python[Requests]
# ================================================================
#
#   Gemini API 多轮对话示例
#
#   功能说明：演示如何使用 Gemini API 进行多轮对话
#   模型版本：gemini-2.5-flash
#   接口类型：REST API (POST 请求)
#
# ================================================================

import requests
import json

# --------------------------------
#   1. API 配置
# --------------------------------

# API 端点地址
# - 使用 generateContent 接口生成对话内容
# - v1beta 表示测试版本接口
url = "https://www.dmxapi.cn/v1beta/models/gemini-2.5-flash:generateContent"

# 请求头配置
# - Authorization: 令牌认证方式
# - Content-Type: 指定请求体为 JSON 格式
headers = {
    "Authorization": "sk-*****************************************",
    "Content-Type": "application/json"
}

# --------------------------------
#   2. 构建多轮对话内容
# --------------------------------

# 对话数据结构说明：
# - contents: 对话历史列表，按时间顺序排列
# - role: 角色标识，"user" 表示用户，"model" 表示 AI
# - parts: 消息内容列表，text 字段存放文本

data = {
    "contents": [
        # -------- 第一轮对话 --------
        {
            "role": "user",                         # 用户发言
            "parts": [{"text": "今天是几号"}]
        },
        {
            "role": "model",                        # 模型回复
            "parts": [{"text": "今天是2025年12月26日"}]
        },
        # -------- 第二轮对话 --------
        {
            "role": "user",                         # 用户追问
            "parts": [{"text": "明天是几号"}]
        }
        # 模型将根据上下文回答这个问题
    ]
}

# --------------------------------
#   3. 发送请求并输出结果
# --------------------------------

# 发送 POST 请求
# - url: API 端点
# - headers: 请求头（含认证信息）
# - json: 自动将 dict 转为 JSON 格式
response = requests.post(url, headers=headers, json=data)

# 格式化输出 JSON 响应
# - indent=2: 缩进 2 空格，便于阅读
# - ensure_ascii=False: 正确显示中文字符
print(json.dumps(response.json(), indent=2, ensure_ascii=False))

```

```python[SDK]
# ================================================================
#
#   Gemini API 多轮对话示例 (SDK 版本)
#
#   功能说明：使用 Google GenAI SDK 进行多轮对话
#   模型版本：gemini-2.5-flash
#   接口类型：Python SDK (google-genai)
#
#   优势：相比 REST API，SDK 自动管理对话历史，代码更简洁
#
# ================================================================

from google import genai

# --------------------------------
#   1. 初始化客户端
# --------------------------------

# 创建 GenAI 客户端
# - api_key: API 密钥，用于身份认证
# - http_options: 自定义请求配置
#   - api_version: API 版本 (v1beta 为测试版)
#   - base_url: 自定义 API 端点地址

client = genai.Client(
    api_key="sk-*****************************************",
    http_options={"api_version": "v1beta", "base_url": "https://www.dmxapi.cn"}
)

# --------------------------------
#   2. 创建对话会话
# --------------------------------

# 创建聊天会话
# - model: 指定使用的模型
# - 会话对象会自动维护对话历史，无需手动管理

chat = client.chats.create(model="gemini-2.5-flash")

# --------------------------------
#   3. 进行多轮对话
# --------------------------------

# 第一轮对话：告诉模型一些信息
response = chat.send_message("今天是2025年12月26日")
print(response.text)

# 第二轮对话：基于上下文提问
# - 模型会记住之前的对话内容
# - 能够理解 "my house" 指的是前面提到的房子
response = chat.send_message("明天是几号")
print(response.text)

# --------------------------------
#   4. 查看完整对话历史
# --------------------------------

# 遍历对话历史记录
# - chat.get_history(): 获取所有对话消息
# - message.role: 消息角色 (user/model)
# - message.parts[0].text: 消息文本内容

for message in chat.get_history():
    print(f'role - {message.role}', end=": ")
    print(message.parts[0].text)


```
:::


## 📤 返回示例

### 成功响应

::: code-group

```json[Requests]

{
  "candidates": [
    {
      "content": {
        "role": "model",
        "parts": [
          {
            "text": "明天是2025年12月27日。"
          }
        ]
      },
      "finishReason": "STOP",
      "index": 0,
      "safetyRatings": null
    }
  ],
  "promptFeedback": {
    "safetyRatings": null
  },
  "usageMetadata": {
    "promptTokenCount": 22,
    "candidatesTokenCount": 14,
    "totalTokenCount": 214,
    "thoughtsTokenCount": 178,
    "promptTokensDetails": [
      {
        "modality": "TEXT",
        "tokenCount": 22
      }
    ]
  },
  "modelVersion": "gemini-2.5-flash",
  "responseId": "awNOaYKaHebfjMcP-dyd4Ao"
}
```
```json[SDK]
好的，2025年12月26日。
明天是2025年12月27日。
role - user: 今天是2025年12月26日
role - model: 好的，2025年12月26日。
role - user: 明天是几号
role - model: 明天是2025年12月27日。
```
:::






## 🔑 获取 API Key

访问 [DMXAPI 官网](https://www.dmxapi.cn) 注册并获取您的 API 密钥。



## ⚠️ 注意事项

- 请妥善保管您的 API 密钥,不要将其暴露在公开代码中
- API 请求需要稳定的网络连接
- 建议在生产环境中添加重试机制和错误处理
- 注意监控 token 使用量以控制成本

---

<p align="center">
  <small>© 2026 DMXAPI Gemini  多轮对话</small>
</p>