# perplexity-deep-research-ssvip 深度研究 API 使用文档

基于 Perplexity 深度研究模型（`perplexity-deep-research-ssvip`）的 Responses 端点接口，能够对复杂问题展开多步骤网络检索与深度推理，自动引用来源并输出带注释的长篇研究报告。相比普通对话模型，该接口内置搜索与推理链，适合需要综合大量资料、输出结构化深度内容的场景，返回结果包含完整的推理过程（`reasoning`）和 URL 引用注释（`annotations`）。

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

- `perplexity-deep-research-ssvip`

## 📋 深度研究 示例代码

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
    # 使用 perplexity-deep-research-ssvip 启用 Perplexity 深度研究能力
    "model": "perplexity-deep-research-ssvip",

    # 【input】(array, 必填) 对话输入内容，支持多轮消息数组
    # 每个元素为一条消息，包含 role 和 content 字段
    "input": [
        {
            # 【role】(string, 必填) 消息角色
            # 可选值: "user"(用户消息) / "assistant"(模型回复) / "system"(系统提示)
            "role": "user",

            # 【content】(array, 必填) 消息内容，支持多模态数组格式
            "content": [
                {
                    # 【type】(string, 必填) 内容类型
                    # "input_text" 表示纯文本输入
                    "type": "input_text",

                    # 【text】(string, 必填) 具体的文本内容，即用户的研究问题
                    "text": "介绍下鲁迅",
                }
            ],
        }
    ],
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
  "id": "gen-1775214439-ps2lfNaI2lxqE8Ahuzpl",
  "object": "chat.completion",
  "created": 1775214439,
  "model": "perplexity-deep-research-ssvip",
  "choices": [
    {
      "index": 0,
      "logprobs": null,
      "finish_reason": "stop",
      "native_finish_reason": "stop",
      "message": {
        "role": "assistant",
        "content": "# 鲁迅：中国现代文学的奠基人\n\n鲁迅（1881-1936）...",
        "refusal": null,
        "reasoning": "用户在询问鲁迅，这是中国现代文学最重要的作家之一...",
        "reasoning_details": [
          {
            "type": "reasoning.text",
            "text": "用户在询问鲁迅，这是中国现代文学最重要的作家之一...",
            "format": "unknown",
            "index": 0
          }
        ],
        "annotations": [
          {
            "type": "url_citation",
            "url_citation": {
              "url": "https://en.wikipedia.org/wiki/Lu_Xun",
              "title": "Lu Xun - Wikipedia",
              "start_index": 0,
              "end_index": 0
            }
          }
        ]
      }
    }
  ],
  "usage": {
    "total_tokens": 106819,
    "input_tokens": 0,
    "input_tokens_details": {
      "cached_tokens": 0
    },
    "output_tokens": 106819,
    "output_tokens_details": {
      "reasoning_tokens": 0
    }
  }
}
```



<p align="center">
  <small>© 2026 DMXAPI perplexity-deep-research-ssvip 深度研究</small>
</p>
