# Gemini 多轮对话 API使用文档

## 📋 概述

本文档介绍如何通过 DMXAPI 使用 `gemini-3.8-flash` 进行多轮对话。REST 调用需要按顺序传入 `user` / `model` 历史消息；SDK 的 `chat` 会话会自动维护历史。

运行前安装依赖（`pip install requests google-genai`）并填写 DMXAPI 密钥。示例中的日期是显式给定的上下文，不代表模型能读取当前日期；真实多轮请求应保留模型返回的完整 `content`，包括可能出现的 `thoughtSignature`。


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
#   模型版本：gemini-3.8-flash
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
url = "https://www.dmxapi.cn/v1beta/models/gemini-3.8-flash:generateContent"

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
response = requests.post(url, headers=headers, json=data, timeout=(10, 120))
response.raise_for_status()

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
#   模型版本：gemini-3.8-flash
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
    http_options={"api_version": "v1beta", "base_url": "https://www.dmxapi.cn", "timeout": 120000}
)

# --------------------------------
#   2. 创建对话会话
# --------------------------------

# 创建聊天会话
# - model: 指定使用的模型
# - 会话对象会自动维护对话历史，无需手动管理

chat = client.chats.create(model="gemini-3.8-flash")

# --------------------------------
#   3. 进行多轮对话
# --------------------------------

# 第一轮对话：告诉模型一些信息
response = chat.send_message("今天是2025年12月26日")
print(response.text)

# 第二轮对话：基于上下文提问
# - 模型会记住之前的对话内容
# - 根据前面给定的日期回答“明天是几号”
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

以下为 **2026-11-03** 使用 `gemini-3.8-flash` 的实测结果（HTTP 200），对应[测试记录](/reports/gemini-3.8-flash-2026-11-03/results.json)中的 `duolunduihua-1`（Requests）与 `duolunduihua-2`（SDK）。回复中的 2025-12-27 来自代码指定的对话日期，不是测试当天的“明天”。Requests 展示保存的响应 JSON，其中签名已省略；SDK 展示实际打印的两轮回答及历史。

### 成功响应

::: code-group

```json [Requests]
{
  "candidates": [
    {
      "content": {
        "parts": [
          {
            "text": "明天是2025年12月27日（星期六）。",
            "thoughtSignature": "[OMITTED]"
          }
        ],
        "role": "model"
      },
      "finishReason": "STOP",
      "index": 0
    }
  ],
  "usageMetadata": {
    "promptTokenCount": 22,
    "candidatesTokenCount": 17,
    "totalTokenCount": 314,
    "promptTokensDetails": [
      {
        "modality": "TEXT",
        "tokenCount": 22
      }
    ],
    "thoughtsTokenCount": 275,
    "serviceTier": "standard",
    "cost": "¥0.005518"
  },
  "modelVersion": "gemini-3.8-flash",
  "responseId": "FOXpapW6JfK_uMYPnZObMA"
}
```

```text [SDK]
好的，已记录当前的时间背景设定为 **2025年12月26日**（星期五）。

这一天是圣诞节的后一天（部分国家和地区称作“节礼日” Boxing Day），距离2026年元旦只剩不到一周的时间。

请问在这个时间节点上，有什么我可以为您效劳的吗？（例如日程规划、跨年总结、撰写文案等）
明天是 **2025年12月27日**，星期六。
role - user: 今天是2025年12月26日
role - model: 好的，已记录当前的时间背景设定为 **2025年12月26日**（星期五）。

这一天是圣诞节的后一天（部分国家和地区称作“节礼日” Boxing Day），距离2026年元旦只剩不到一周的时间。

请问在这个时间节点上，有什么我可以为您效劳的吗？（例如日程规划、跨年总结、撰写文案等）
role - user: 明天是几号
role - model: 明天是 **2025年12月27日**，星期六。
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