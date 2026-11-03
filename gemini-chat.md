# Gemini 原生格式 - 普通对话（非流式输出）

## 📋 概述

本文档介绍如何通过 DMXAPI 使用 `gemini-3.8-flash` 进行非流式文本生成。请求使用 Gemini 原生的 `contents` / `parts` 结构，完整回答在请求完成后一次返回。

运行前安装 `requests`（`pip install requests`），并将代码中的 API 密钥占位符替换为自己的 DMXAPI 密钥。


## 🌐 请求地址

```
https://www.dmxapi.cn/v1beta/models/{model}:generateContent
```

### 参数说明

| 参数 | 说明 | 示例 |
|------|------|------|
| `{model}` | Gemini 模型版本 | `gemini-3.8-flash` |



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
model = "gemini-3.8-flash"  # 使用的 Gemini 模型版本
API_KEY = "sk-*****************************************"  # 替换为你的 DMXAPI 密钥
API_URL = f"https://www.dmxapi.cn/v1beta/models/{model}:generateContent"  # 密钥通过 params 传入一次


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
            json=payload,
            timeout=(10, 120)
        )
        
        # 检查 HTTP 请求是否成功（状态码 2xx）
        response.raise_for_status()
        
        # 返回解析后的 JSON 响应数据
        return response.json()
        
    except requests.exceptions.RequestException as e:
        # 捕获请求异常并打印错误信息
        print(f"❌ 请求失败: {e}")
        
        # 如果存在响应对象，打印详细的错误信息
        if e.response is not None:
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

以下为 **2026-11-03** 使用 `gemini-3.8-flash` 的实测响应 JSON（HTTP 200），对应[测试记录](/reports/gemini-3.8-flash-2026-11-03/results.json)中的 `gemini-chat-1`。已去除控制台提示；`thoughtSignature` 在保存记录中以 `[OMITTED]` 省略，文本及用量保留当次返回值。

### 成功响应

```json
{
  "candidates": [
    {
      "content": {
        "role": "model",
        "parts": [
          {
            "text": "你好！我是 Gemini，是由 Google 训练的大型语言模型。\n\n你可以把我当成你的个人智能助手。无论你是想查找信息、解答疑问、撰写文章、翻译语言，还是构思创意、编写代码，我都可以为你提供帮助。\n\n今天有什么我可以帮你的吗？",
            "thoughtSignature": "[OMITTED]"
          }
        ]
      },
      "finishReason": "STOP"
    }
  ],
  "usageMetadata": {
    "promptTokenCount": 5,
    "candidatesTokenCount": 62,
    "totalTokenCount": 342,
    "trafficType": "ON_DEMAND",
    "promptTokensDetails": [
      {
        "modality": "TEXT",
        "tokenCount": 5
      }
    ],
    "candidatesTokensDetails": [
      {
        "modality": "TEXT",
        "tokenCount": 62
      }
    ],
    "thoughtsTokenCount": 275,
    "cost": "¥0.006292"
  },
  "modelVersion": "gemini-3.8-flash",
  "createTime": "2026-11-03T13:42:46.616405Z",
  "responseId": "1uTpatXPJdnhsbwPw86S4Ac"
}
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
  <small>© 2026 DMXAPI Gemini对话</small>
</p>