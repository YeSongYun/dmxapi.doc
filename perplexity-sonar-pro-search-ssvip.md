# perplexity-sonar-pro-search-ssvip 联网搜索 API 使用文档

基于 Perplexity Sonar Pro Search 模型（`perplexity-sonar-pro-search-ssvip`）的 Responses 端点接口，专注于实时联网检索与结构化内容生成，能够自动聚合多源网络资料并以 Markdown 表格、列表等格式输出，同时附上 URL 引用注释。该接口支持通过 `reasoning.enabled` 参数按需开启推理模式，适合信息查询、资料汇总、对比分析等需要实时网络数据的场景。

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

- `perplexity-sonar-pro-search-ssvip`

## 📋 联网搜索 示例代码

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
    # 使用 perplexity-sonar-pro-search-ssvip 启用实时联网搜索能力
    "model": "perplexity-sonar-pro-search-ssvip",

    # 【input】(array, 必填) 对话输入内容
    # 每个元素为一条消息，包含 role 和 content 字段
    "input": [
        {
            # 【role】(string, 必填) 消息角色
            # 可选值: "user"(用户消息) / "assistant"(模型回复) / "system"(系统提示)
            "role": "user",

            # 【content】(array, 必填) 消息内容
            "content": [
                {
                    # 【type】(string, 必填) 内容类型
                    # "input_text" 表示纯文本输入
                    "type": "input_text",

                    # 【text】(string, 必填) 具体的查询问题或指令
                    "text": "请帮我查询下世界前十名胜古迹及其历史"
                }
            ]
        }
    ],

    # 【reasoning】(object, 可选) 推理模式配置
    # 控制模型是否在作答前进行显式推理，默认不启用
    "reasoning": {
        # 【enabled】(boolean, 可选) 是否启用推理模式
        # True: 开启推理，模型会先进行内部思考再输出答案
        # False: 关闭推理，直接输出搜索结果（默认）
        "enabled": True
    }
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
  "id": "gen-1775221481-8opsZokrqthvIDxan5UW",
  "object": "chat.completion",
  "created": 1775221481,
  "model": "perplexity-sonar-pro-search-ssvip",
  "choices": [
    {
      "index": 0,
      "logprobs": null,
      "finish_reason": "stop",
      "native_finish_reason": "stop",
      "message": {
        "role": "assistant",
        "content": "## 世界十大名胜古迹\n\n世界十大名胜古迹没有官方统一排名，常基于UNESCO世界遗产、新七大奇迹或受欢迎度选出。以下结合多个来源，列出十个最具代表性的古迹，包括其历史概述。[1][3]\n\n| 排名 | 名胜古迹 | 位置 | 建造年代 | 简史 |\n|------|----------|------|----------|------|\n| 1 | 吉萨大金字塔 | 埃及 | 前2580年 | 古埃及法老胡夫陵墓，唯一幸存的古代世界七大奇迹 |\n| 2 | 中国长城 | 中国 | 前221年起 | 抵御北方游牧民族入侵的防御工程，全长逾2万公里 |\n| 3 | 佩特拉古城 | 约旦 | 前4世纪 | 纳巴泰人雕刻于岩石的玫瑰红城市，丝绸之路贸易中心 |",
        "refusal": null,
        "reasoning": null,
        "annotations": [
          {
            "type": "url_citation",
            "url_citation": {
              "url": "https://www.kids-world-travel-guide.com/top-10-famous-landmarks.html",
              "title": "Top 10 Famous Landmarks in the World",
              "start_index": 0,
              "end_index": 0
            }
          },
          {
            "type": "url_citation",
            "url_citation": {
              "url": "https://wanderingcarol.com/historical-places-in-the-world/",
              "title": "30 Best Historical Places in the World to Visit - Wandering Carol",
              "start_index": 0,
              "end_index": 0
            }
          },
          {
            "type": "url_citation",
            "url_citation": {
              "url": "https://artsandculture.google.com/story/10-must-see-unesco-world-heritage-sites/UAURf5dVbFaD3g?hl=en",
              "title": "10 Must-see UNESCO World Heritage Sites — Google Arts & Culture",
              "start_index": 0,
              "end_index": 0
            }
          }
        ]
      }
    }
  ],
  "usage": {
    "total_tokens": 1618,
    "input_tokens": 0,
    "input_tokens_details": {
      "cached_tokens": 0
    },
    "output_tokens": 1618,
    "output_tokens_details": {
      "reasoning_tokens": 0
    }
  }
}
```



<p align="center">
  <small>© 2026 DMXAPI perplexity-sonar-pro-search-ssvip 联网搜索</small>
</p>
