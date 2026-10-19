# DeepSeek 网页搜索与抓取 API 使用文档

本文档介绍如何通过 DMXAPI 平台调用 DeepSeek **网页搜索（Search）** 与 **网页抓取（Fetch）** 两大工具接口，为 Agent 与 RAG 应用提供实时网页内容。Search 接口由 DeepSeek 自研搜索引擎支持，按关键词检索网页并返回标题、摘要、正文等结构化结果；Fetch 接口抓取指定网页并以 Markdown 格式返回正文。两者均为只读的原始 JSON API，接口协议与 DeepSeek 官方完全兼容——只需将请求地址替换为 DMXAPI 平台地址、使用平台 API Key 鉴权即可直接调用。

## 🌐 网页搜索请求地址
```text
https://www.dmxapi.cn/v1/tools/search
```
## 🌐 网页抓取请求地址
```text
https://www.dmxapi.cn/v1/tools/fetch
```
:::warning
请妥善保管您的 API Key！严禁将密钥泄露给他人、硬编码到代码中或提交到公开的代码仓库。如果怀疑密钥已泄露，请立即前往 DMXAPI 官网重新生成。
:::

## 💻 网页搜索 示例代码

:::: code-group

```python [requests]
import requests
import json

# ===================================================================
# 步骤1: 配置 API 连接信息
# ===================================================================

# DMXAPI 服务端点地址
url = "https://www.dmxapi.cn/v1/tools/search"

# DMXAPI 密钥 (请替换为您自己的密钥)
# 获取方式: 登录 DMXAPI 官网 -> 个人中心 -> API 密钥管理
api_key = "sk-*************************************************"

# ===================================================================
# 步骤2: 配置请求头
# ===================================================================

headers = {
    "Content-Type": "application/json",         # 指定请求体为 JSON 格式
    "Authorization": f"Bearer {api_key}",       # Bearer token 认证方式
}

# ===================================================================
# 步骤3: 配置请求参数
# ===================================================================

payload = {
    # 【query】(string, 必填) 搜索关键词
    # 说明: 长度 1~128 个 Unicode 字符，不能全为空白字符
    #       query 中的搜索语法会原样传递给搜索服务，以下操作符与搜索词组合使用，
    #       也可以在一个 query 中组合多个操作符
    #
    # 搜索语法:
    #   操作符    示例                                                说明
    #   ------    ------------------------------------------------    --------------------------------------------
    #   site:     DeepSeek site:github.com                            将结果限制在指定站点，指定多个时用空格分隔
    #                                                                   并通过 OR 连接，例如
    #                                                                   DeepSeek site:github.com OR site:huggingface.co
    #   -site:    DeepSeek -site:example.com                          排除指定站点，指定多个时用空格分隔
    #   -         DeepSeek -广告                                      排除包含指定关键词的网页，指定多个时用空格分隔
    #   -"..."    DeepSeek -"release notes"                           排除包含指定短语的网页，短语内可以包含空格，
    #                                                                   指定多个时用空格分隔
    #   "..."     DeepSeek "精确短语"                                 精确匹配指定短语，指定多个时用空格分隔
    #   lang:     DeepSeek lang:zh,en                                 将结果限制在指定语言，多种语言用逗号分隔，
    #                                                                   例如 lang:zh,en
    #   after:    DeepSeek after:2025 或 DeepSeek after:2025-01-01    将结果限制在指定日期之后发布的网页
    #   before:   DeepSeek before:2026 或 DeepSeek before:2026-06-01  将结果限制在指定日期之前发布的网页
    "query": "DMXAPI 介绍",

    # 【count】(integer, 可选) 返回结果条数
    # 默认值: 10；取值范围: [1, 50]
    # 注意: count 只影响返回条数，不影响单次调用费用
    "count": 5,

    # 【need_content】(boolean, 可选) 是否在 content 字段中返回网页正文
    # 可选值:
    #   - False(默认): content 恒为空字符串，只返回标题与摘要，响应更快
    #   - True: 额外抓取并返回网页正文，可省去单独调用 Fetch 接口
    "need_content": True,

    # 【ori_question】(string, 可选) 触发搜索的用户原始问题
    # 说明: 长度 1~128 个字符，提供后有助于搜索引擎理解搜索意图；传 null 视为未提供
    "ori_question": "DMXAPI 是什么？",

    # 【localization】(string, 可选) 用于优先返回本地化结果的 IP 地址
    # 默认值: ""（不启用本地化优先）
    "localization": "",
}

# ===================================================================
# 步骤4: 发送请求并输出结果
# ===================================================================

# 发送 POST 请求到 API 服务器
response = requests.post(url, headers=headers, json=payload, timeout=60)

# 格式化输出 JSON 响应
# - indent=2: 缩进 2 空格，便于阅读
# - ensure_ascii=False: 正确显示中文字符
print(json.dumps(response.json(), indent=2, ensure_ascii=False))
```

```bash [cURL]
curl https://www.dmxapi.cn/v1/tools/search \
  -H "Authorization: Bearer sk-*************************************************" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "DMXAPI 介绍",
    "count": 5,
    "need_content": true,
    "ori_question": "DMXAPI 是什么？",
    "localization": ""
  }'
```

::::

##  返回示例

```json
{
  "results": [
    {
      "title": "LangChain 接入 DMXAPI 接口文档",
      "site_name": "dmxapi.com",
      "site_icon": "https://cdn.deepseek.com/site-icons/dmxapi.com",
      "authority": 2,
      "rerank_score": 2.164104461669922,
      "date": null,
      "url": "https://doc.dmxapi.com/langchain.html",
      "summary": "# LangChain 接入 DMXAPI 接口文档\n\n## 概念介绍\n\nDMXAPI 是一个提供 AI 模型服务的 API 平台，支持多种大语言模型调用。开发者可以通过简单的 API 调用访问强大的 AI 能力……（约 600 字符，此处截断）",
      "snippet": "概念介绍 DMXAPI 是一个提供 AI 模型服务的 API 平台，支持多种大语言模型调用。开发者可以通过简单的 API 调用访问强大的 AI 能力。 ## 基础信息 - 基础 URL:https://www.dmxapi.cn/v1",
      "content": "Skip to content\n\n# LangChain 接入 DMXAPI 接口文档\n\n## 概念介绍\n\nDMXAPI 是一个提供 AI 模型服务的 API 平台，支持多种大语言模型调用。开发者可以通过简单的 API 调用访问强大的 AI 能力……（约 900 字符，此处截断）"
    },
    {
      "title": "dmxapi-cli",
      "site_name": "NPM",
      "site_icon": "https://cdn.deepseek.com/site-icons/npmjs.com",
      "authority": 3,
      "rerank_score": 2.070382833480835,
      "date": "2026-03-26T16:00:00+00:00",
      "url": "https://www.npmjs.com/package/dmxapi-cli?activeTab=readme#1",
      "summary": "# dmxapi-cli\n\n### DMXAPI CLI 统一命令行工具 —— 一个 Key 调用全球 500+ AI 模型。\n\nDMXAPI 是大模型 API 聚合平台，支持 OpenAI、Claude、Gemini、千问等主流模型……（约 1200 字符，此处截断）",
      "snippet": "DMXAPI CLI 统一命令行工具 —— 一个 Key 调用全球 500+ AI 模型。 DMXAPI 是大模型 API 聚合平台，支持 OpenAI、Claude、Gemini、千问等主流模型。dmxapi-cli 对文生文、文生图、文生视频、文生音乐等能力做统一的 CLI 封装……（此处截断）",
      "content": "⚠️\n\n# dmxapi-cli\n0.2.2 • Public • Published \n\n### DMXAPI CLI 统一命令行工具 —— 一个 Key 调用全球 500+ AI 模型。\n\nDMXAPI 是大模型 API 聚合平台，支持 OpenAI、Claude、Gemini、千问等主流模型……（约 6000 字符，此处截断）"
    }
  ]
}
```
## 💻 网页抓取 示例代码

抓取单个网页并以 Markdown 格式返回正文内容。Fetch 结果受目标站点可用性和访问策略影响。

:::: code-group

```python [requests]
import requests
import json

# ===================================================================
# 步骤1: 配置 API 连接信息
# ===================================================================

# DMXAPI 服务端点地址
url = "https://www.dmxapi.cn/v1/tools/fetch"

# DMXAPI 密钥 (请替换为您自己的密钥)
# 获取方式: 登录 DMXAPI 官网 -> 个人中心 -> API 密钥管理
api_key = "sk-*************************************************"

# ===================================================================
# 步骤2: 配置请求头
# ===================================================================

headers = {
    "Content-Type": "application/json",         # 指定请求体为 JSON 格式
    "Authorization": f"Bearer {api_key}",       # Bearer token 认证方式
}

# ===================================================================
# 步骤3: 配置请求参数
# ===================================================================

payload = {
    # 【url】(string, 必填) 要抓取的网页地址
    # 说明: 长度不超过 8192 个字符
    # 注意: 必须是含 host 的 HTTP/HTTPS URL，且不能携带用户名或密码
    "url": "https://doc.dmxapi.cn/doubao-seedance-2-5-260628-text-to-video.html",
}

# ===================================================================
# 步骤4: 发送请求并输出结果
# ===================================================================

# 发送 POST 请求到 API 服务器
response = requests.post(url, headers=headers, json=payload, timeout=60)

# 格式化输出 JSON 响应
# - indent=2: 缩进 2 空格，便于阅读
# - ensure_ascii=False: 正确显示中文字符
print(json.dumps(response.json(), indent=2, ensure_ascii=False))
```

```bash [cURL]
curl https://www.dmxapi.cn/v1/tools/fetch \
  -H "Authorization: Bearer sk-*************************************************" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://doc.dmxapi.cn/doubao-seedance-2-5-260628-text-to-video.html"
  }'
```

::::

##  返回示例

```json
{
  "title": "doubao-seedance-2-5-260628 文生视频 API 使用文档",
  "content": "Skip to content\n\n\\# doubao\\-seedance\\-2\\-5\\-260628 文生视频 API 使用文档\n\n基于 Doubao Seedance 2\\.5 的文生视频接口，通过\\/v1\\/responses 端点以异步任务方式调用：仅输入一段文本提示词即可直出带同步音效的视频。模型原生支持有声视频生成，会依据提示词与画面内容自动配上人声、音效与背景音乐……（抓取后的 Markdown 正文共约 11700 字符，此处截断）"
}
```

<p align="center">
  <small>© 2026 DMXAPI DeepSeek 网页搜索与抓取</small>
</p>
