# Gemini 原生格式 - 普通对话（非流式输出）

## 📋 概述

本文档介绍如何使用 Gemini API 进行非流式文本生成对话。


## 🌐 请求地址

```
https://www.dmxapi.cn/v1beta/models/{model}:generateContent
```

### 参数说明

| 参数 | 说明 | 示例 |
|------|------|------|
| `{model}` | Gemini 模型版本 | `gemini-2.5-flash` |



## 💻 Python 示例代码

```python
"""
================================================
DMXAPI Gemini API 文本生成示例脚本
================================================
功能说明：
    本脚本演示如何使用 Gemini API 进行文本生成
    支持通过自定义提示词与 AI 模型进行交互

作者：DMXAPI
================================================
"""

import requests
import json

# ========================================
# API 配置信息
# ========================================
prompt = "Hi, 你是谁？"  # 用户提示词 - 可在此处修改你想问的问题
model = "gemini-2.5-flash"  # 使用的 Gemini 模型版本
API_KEY = "sk-*****************************************"  # 替换为你的 DMXAPI 密钥
API_URL = f"https://www.dmxapi.cn/v1beta/models/{model}:generateContent?key={API_KEY}"  # DMXAPI gemini 请求地址


def generate_text(prompt):
    """
    调用 DMXAPI Gemini API 生成文本
    
    功能说明：
        向 DMXAPI Gemini API 发送文本提示，获取 AI 生成的响应内容
    
    参数：
        prompt (str): 用户输入的提示文本，用于指导 AI 生成内容
        
    返回值：
        dict: API 响应的 JSON 数据，包含生成的文本内容
        None: 请求失败时返回 None
        
    异常处理：
        捕获所有网络请求相关异常，并打印详细错误信息
    """
    # 设置请求头，指定内容类型为 JSON
    headers = {"Content-Type": "application/json"}
    
    # 构建请求负载数据
    payload = {
        "contents": [{
            "role": "user",  # 角色标识为用户
            "parts": [{"text": prompt}]  # 用户提示文本
        }]
    }
    
    try:
        # 发送 POST 请求到 Gemini API
        response = requests.post(
            API_URL,
            headers=headers,
            params={"key": API_KEY},
            json=payload
        )
        
        # 检查 HTTP 请求是否成功（状态码 2xx）
        response.raise_for_status()
        
        # 返回解析后的 JSON 响应数据
        return response.json()
        
    except requests.exceptions.RequestException as e:
        # 捕获请求异常并打印错误信息
        print(f"❌ 请求失败: {e}")
        
        # 如果存在响应对象，打印详细的错误信息
        if e.response:
            print(f"📊 状态码: {e.response.status_code}")
            print(f"📄 响应内容: {e.response.text}")
        
        return None


# ========================================
# 主程序入口
# ========================================
if __name__ == "__main__":
    print("=" * 50)
    print("🚀 Gemini API 文本生成测试")
    print("=" * 50)
    
    # 调用函数生成文本
    result = generate_text(prompt) 
    
    # 如果请求成功，格式化输出结果
    if result:
        print("✅ 请求成功！API 响应结果：")
        print("-" * 50)
        print(json.dumps(result, indent=2, ensure_ascii=False))
        print("-" * 50)
    else:
        print("❌ 请求失败，请检查 API 密钥和网络连接。")
```



## 📤 返回示例

### 成功响应

```json
==================================================
🚀 Gemini API 文本生成测试
==================================================
✅ 请求成功！API 响应结果：
--------------------------------------------------
{
  "candidates": [
    {
      "content": {
        "role": "model",
        "parts": [
          {
            "text": "你好！我是一个大型语言模型，由 Google 训练。"
          }
        ]
      },
      "finishReason": "STOP",
      "safetyRatings": [
        {
          "category": "HARM_CATEGORY_HATE_SPEECH",
          "probability": "NEGLIGIBLE",
          "probabilityScore": 5.7630864e-06,
          "severity": "HARM_SEVERITY_NEGLIGIBLE",
          "severityScore": 0.033027172
        },
        {
          "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
          "probability": "NEGLIGIBLE",
          "probabilityScore": 5.4859487e-07,
          "severity": "HARM_SEVERITY_NEGLIGIBLE",
          "severityScore": 0.0122974515
        },
        {
          "category": "HARM_CATEGORY_HARASSMENT",
          "probability": "NEGLIGIBLE",
          "probabilityScore": 1.3191487e-05,
          "severity": "HARM_SEVERITY_NEGLIGIBLE"
        },
        {
          "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
          "probability": "NEGLIGIBLE",
          "probabilityScore": 2.6473836e-07,
          "severity": "HARM_SEVERITY_NEGLIGIBLE",
          "severityScore": 0.02153945
        }
      ],
      "avgLogprobs": -0.6024571932279147
    }
  ],
  "usageMetadata": {
    "promptTokenCount": 5,
    "candidatesTokenCount": 13,
    "totalTokenCount": 46,
    "trafficType": "PROVISIONED_THROUGHPUT",
    "promptTokensDetails": [
      {
        "modality": "TEXT",
        "tokenCount": 5
      }
    ],
    "candidatesTokensDetails": [
      {
        "modality": "TEXT",
        "tokenCount": 13
      }
    ],
    "thoughtsTokenCount": 28
  },
  "modelVersion": "gemini-2.5-flash",
  "createTime": "2025-11-11T08:22:12.483945Z",
  "responseId": "NPISaenEHYqWsbwPn7GC4QI"
}
--------------------------------------------------
```



## 📊 响应字段说明

| 字段 | 类型 | 说明 |
|------|------|------|
| `candidates` | Array | 生成的候选响应列表 |
| `candidates[].content.parts[].text` | String | AI 生成的文本内容 |
| `candidates[].finishReason` | String | 完成原因(如 `STOP`) |
| `candidates[].safetyRatings` | Array | 安全性评级信息 |
| `usageMetadata.promptTokenCount` | Integer | 输入提示的 token 数量 |
| `usageMetadata.candidatesTokenCount` | Integer | 生成内容的 token 数量 |
| `usageMetadata.totalTokenCount` | Integer | 总 token 数量 |
| `modelVersion` | String | 使用的模型版本 |



## 🔑 获取 API Key

访问 [DMXAPI 官网](https://www.dmxapi.cn) 注册并获取您的 API 密钥。



## ⚠️ 注意事项

- 请妥善保管您的 API 密钥,不要将其暴露在公开代码中
- API 请求需要稳定的网络连接
- 建议在生产环境中添加重试机制和错误处理
- 注意监控 token 使用量以控制成本

---

<p align="center">
  <small>© 2025 DMXAPI Gemini对话</small>
</p>