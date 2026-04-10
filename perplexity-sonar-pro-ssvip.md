# perplexity-sonar-pro-ssvip 多模态理解 API 使用文档

基于 Perplexity Sonar Pro 模型（`perplexity-sonar-pro-ssvip`）的 Responses 端点接口，支持文本与图像混合输入，能够对图片内容进行识别与描述，并自动联网检索相关资料附上 URL 引用注释。相比纯文本对话模型，该接口具备视觉理解与实时搜索双重能力，适合图像内容分析、以图搜索、多模态问答等场景。

## 🌐 请求地址

```
https://www.dmxapi.cn/v1/responses
```

:::warning
请妥善保管您的 API Key！严禁将密钥泄露给他人、硬编码到代码中或提交到公开的代码仓库。如果怀疑密钥已泄露，请立即前往 DMXAPI 官网重新生成。
:::

## 🤖 模型名称

- `perplexity-sonar-pro-ssvip`

## 📋 多模态理解 示例代码

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
    # 使用 perplexity-sonar-pro-ssvip 启用视觉理解与联网搜索能力
    "model": "perplexity-sonar-pro-ssvip",

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
  "id": "gen-1775222516-XlZ8xFipoaTooZaZm0Iv",
  "object": "chat.completion",
  "created": 1775222516,
  "model": "perplexity-sonar-pro-ssvip",
  "choices": [
    {
      "index": 0,
      "logprobs": null,
      "finish_reason": "stop",
      "native_finish_reason": "stop",
      "message": {
        "role": "assistant",
        "content": "This image shows **two dolphins leaping or surfacing through ocean waves**. The dolphins appear to be **bottlenose dolphins**, characterized by their distinctive gray coloring with lighter undersides, curved dorsal fins, and streamlined bodies. They are captured mid-action in blue-green seawater, with one dolphin more prominently featured in the foreground while another is visible to the left.",
        "refusal": null,
        "reasoning": null,
        "annotations": [
          {
            "type": "url_citation",
            "url_citation": {
              "url": "https://www.istockphoto.com/photos/dolphin-jumping",
              "title": "12592 Dolphin Jumping Images and Stock Photos",
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
    "total_tokens": 1020,
    "input_tokens": 0,
    "input_tokens_details": {
      "cached_tokens": 0
    },
    "output_tokens": 1020,
    "output_tokens_details": {
      "reasoning_tokens": 0
    }
  }
}
```

<p align="center">
  <small>© 2026 DMXAPI perplexity-sonar-pro-ssvip 多模态理解</small>
</p>
