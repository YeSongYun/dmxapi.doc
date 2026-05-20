# perplexity-sonar-reasoning-pro-ssvip 多模态推理 API 使用文档

基于 Perplexity Sonar Reasoning Pro 模型（`perplexity-sonar-reasoning-pro-ssvip`）的 Responses 端点接口，在视觉理解与联网搜索的基础上融入链式推理能力，答题前会先输出完整的思考过程（`reasoning`）再给出结论。相比 Sonar Pro，该接口更适合需要逐步分析、结合搜索结果推理的复杂视觉问答场景，返回结果同时包含推理过程（`reasoning`/`reasoning_details`）与 URL 引用注释（`annotations`）。

## 💡 在 Cherry Studio 中使用

如果你希望直接在 Cherry Studio 客户端中调用本搜索模型，请参考：[Cherry Studio 调用 Perplexity Sonar 系列搜索模型](/cherry_perplexity)。

## 🌐 请求地址

```
https://www.dmxapi.cn/v1/responses
```


:::warning
请妥善保管您的 API Key！严禁将密钥泄露给他人、硬编码到代码中或提交到公开的代码仓库。如果怀疑密钥已泄露，请立即前往 DMXAPI 官网重新生成。
:::

## 🤖 模型名称

- `perplexity-sonar-reasoning-pro-ssvip`

## 📋 多模态推理 示例代码

```python
import requests
import json

# 步骤1: 配置 API 连接信息

# DMXAPI 服务端点地址
url = "https://www.dmxapi.cn/v1/responses"

# DMXAPI 密钥 (请替换为您自己的密钥)
api_key = "sk-******************************************"

# 步骤2: 配置请求头

headers = {
    # 指定请求体为 JSON 格式
    "Content-Type": "application/json",
    # token 认证方式，直接传入 API Key（无需加 Bearer 前缀）
    "Authorization": f"{api_key}",
}

# 步骤3: 配置请求参数

payload = {
    # 【model】(string, 必填) 指定调用的模型名称
    # 使用 perplexity-sonar-reasoning-pro-ssvip 启用视觉理解、联网搜索与链式推理能力
    "model": "perplexity-sonar-reasoning-pro-ssvip",

    # 【input】(array, 必填) 对话输入内容，支持多模态混合数组
    # 每个元素为一条消息，包含 role 和 content 字段
    "input": [
        {
            # 【role】(string, 必填) 消息角色
            # 可选值: "user"(用户消息) / "assistant"(模型回复) / "system"(系统提示)
            "role": "user",

            # 【content】(array, 必填) 消息内容，支持文本与图像混合输入
            "content": [
                {
                    # 【type】(string, 必填) 内容类型为纯文本
                    # "input_text" 表示文本输入，对应用户的提问文字
                    "type": "input_text",

                    # 【text】(string, 必填) 针对图像提出的问题或指令
                    "text": "What is in this image?"
                },
                {
                    # 【type】(string, 必填) 内容类型为图像 URL
                    # "image_url" 表示通过公网 URL 传入图像，模型将对其进行视觉理解
                    "type": "image_url",

                    # 【image_url】(object, 必填) 图像地址对象
                    "image_url": {
                        # 【url】(string, 必填) 图像的公网可访问地址
                        # 支持常见图片格式（JPEG、PNG、WebP、GIF 等）
                        "url": "https://live.staticflickr.com/3851/14825276609_098cac593d_b.jpg"
                    }
                }
            ]
        }
    ]
}

# 步骤4: 发送请求并输出结果

# 发送 POST 请求到 API 服务器
response = requests.post(url, headers=headers, json=payload)

# 格式化输出 JSON 响应
# indent=2: 缩进 2 空格，便于阅读
# ensure_ascii=False: 正确显示中文字符
print(json.dumps(response.json(), indent=2, ensure_ascii=False))
```

## 📄 返回示例

```json
{
  "id": "gen-1775222825-xcRIplilrfVZtivtsuHv",
  "object": "chat.completion",
  "created": 1775222825,
  "model": "perplexity-sonar-reasoning-pro-ssvip",
  "choices": [
    {
      "index": 0,
      "logprobs": null,
      "finish_reason": "stop",
      "native_finish_reason": "stop",
      "message": {
        "role": "assistant",
        "content": "The image shows **bottlenose dolphins** swimming in ocean water, captured in what appears to be a close-up or near-surface view.[1] Multiple dolphins are visible moving through the blue-green water, with their distinctive curved dorsal fins and sleek bodies characteristic of the species.[4][5]",
        "refusal": null,
        "reasoning": "The user is asking me to describe what is in the image they've provided. Looking at the image, I can see dolphins in ocean water. The image shows what appears to be bottlenose dolphins swimming/moving through blue-green ocean water with whitecaps/waves visible.\n\nI should describe what's visible in the image: dolphins (appearing to be bottlenose dolphins) in ocean water with visible waves.",
        "reasoning_details": [
          {
            "type": "reasoning.text",
            "text": "The user is asking me to describe what is in the image they've provided. Looking at the image, I can see dolphins in ocean water...",
            "format": "unknown",
            "index": 0
          }
        ],
        "annotations": [
          {
            "type": "url_citation",
            "url_citation": {
              "url": "https://www.livenowfox.com/news/watch-spectacular-video-shows-dolphins-leaping-out-water-off-san-diego-coast",
              "title": "Watch: 'Spectacular' video shows dolphins leaping out of water off ...",
              "start_index": 0,
              "end_index": 0
            }
          },
          {
            "type": "url_citation",
            "url_citation": {
              "url": "https://www.istockphoto.com/photos/dolphin-jumping",
              "title": "12592 Dolphin Jumping Images and Stock Photos - iStock",
              "start_index": 0,
              "end_index": 0
            }
          },
          {
            "type": "url_citation",
            "url_citation": {
              "url": "https://www.gettyimages.com/photos/dolphin-jumping",
              "title": "2658 Dolphin Jumping Stock Photos, High-Res Pictures, and Images",
              "start_index": 0,
              "end_index": 0
            }
          }
        ]
      }
    }
  ],
  "usage": {
    "total_tokens": 906,
    "input_tokens": 0,
    "input_tokens_details": {
      "cached_tokens": 0
    },
    "output_tokens": 906,
    "output_tokens_details": {
      "reasoning_tokens": 0
    }
  }
}
```

### 返回字段说明

| 字段 | 说明 |
|------|------|
| `id` | 本次请求的唯一 ID |
| `object` | 固定为 `chat.completion` |
| `model` | 实际调用的模型名称 |
| `choices[].message.content` | 模型对图像内容的最终分析结论，引用来源以 `[n]` 标注 |
| `choices[].message.reasoning` | 模型作答前的完整推理过程文本，包含搜索结果的整合分析 |
| `choices[].message.reasoning_details` | 推理过程的结构化详情数组，`type` 固定为 `reasoning.text` |
| `choices[].message.annotations` | URL 引用注释列表，对应正文中 `[n]` 标注的来源链接 |
| `choices[].finish_reason` | 停止原因，`stop` 表示正常结束 |
| `usage.total_tokens` | 本次请求消耗的总 token 数 |

<p align="center">
  <small>© 2026 DMXAPI perplexity-sonar-reasoning-pro-ssvip 多模态推理</small>
</p>
