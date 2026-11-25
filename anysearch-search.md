# AnySearch 搜索 API 使用文档

AnySearch 搜索接口输入一个搜索词，返回一组搜索结果，每条结果包含标题、链接、摘要和正文片段。它有两种用法：只填 `query` 是通用网页搜索；再加上 `tag` 和 `params` 就是垂直搜索，可以在金融行情、学术论文、开发文档、空气质量等专业数据里查。`tag` 和 `params` 能填什么不是随便写的，要从 [AnySearch 能力发现](/anysearch-sub-domains) 里查，本页的“垂直搜索”部分写了完整的查法和填法。请求是同步的，一次请求直接返回结果，不需要提交任务再轮询。搜到的链接如果想读全文，把结果里的 `url` 交给 [AnySearch 网页正文提取](/anysearch-extract)。

## 接口地址

| 接口 | 请求方式 | URL |
|------|---------|-----|
| 搜索 | POST | `https://www.dmxapi.cn/v1/search` |


:::warning
请妥善保管您的 API Key！严禁将密钥泄露给他人、硬编码到代码中或提交到公开的代码仓库。如果怀疑密钥已泄露，请立即前往 DMXAPI 官网重新生成。
:::

## 模型名称

- `anysearch`




## 通用搜索示例代码

```python
import requests
import json

# ===============================================================
# 步骤1: 配置 API 连接信息
# ===============================================================

# DMXAPI AnySearch 搜索接口
url = "https://www.dmxapi.cn/v1/search"

# DMXAPI 密钥，请替换为您自己的密钥
# 获取方式: 登录 DMXAPI 官网 -> 个人中心 -> API 密钥管理
api_key = "sk-***********************************************"

# ===============================================================
# 步骤2: 配置请求头
# ===============================================================

headers = {
    "Content-Type": "application/json",  # 指定请求体为 JSON 格式
    "Authorization": f"Bearer {api_key}",  # Bearer 认证，填 DMXAPI 密钥
}

# ===============================================================
# 步骤3: 配置请求参数
# ===============================================================

payload = {
    # 【query】(string，必填) 搜索词
    #   不能为空。若是通用搜索只需要这一个参数
    "query": "全球 AI大模型厂商汇总",

    # 【max_results】(integer，可选) 最多返回几条结果
    #   取值 1 到 10 的整数，不填时为 10
    #   实际返回的条数可能更少，以响应里的 data.metadata.total_results 为准
    "max_results": 2,

    # 【zone】(string，可选) 搜索区域
    #   可选值: cn(中国大陆) / intl(国际)，不需要时删掉这一行
    "zone": "cn",

    # 【language】(string，可选) 偏好的结果语言
    #   例如 zh-CN、en，不需要时删掉这一行
    "language": "zh-CN",

    # 【format】(string，可选) 结果正文的格式
    #   可选值: json / markdown
    #   markdown 只改变每条结果里 content 的排版，整个响应的外层始终是 JSON
    "format": "json",

    # 【tag】【params】(可选) 垂直搜索用，通用搜索不要填
    #   写法见本页“垂直搜索”部分

    # 【model】(string，可选) 固定为 anysearch
    #   官方的请求里没有这一项，可以整行删掉；如果写，只能写 anysearch
    "model": "anysearch",
}

# ===============================================================
# 步骤4: 发送请求并输出结果
# ===============================================================

response = requests.post(url, headers=headers, json=payload, timeout=60)
print("status:", response.status_code)
result = response.json()
print(json.dumps(result, indent=2, ensure_ascii=False))
response.raise_for_status()

# 逐条打印搜索结果:
#   title    标题，一定有，但可能是空字符串
#   url      结果链接；想读全文时把它交给网页正文提取接口
#   snippet  摘要，没有时这个字段不出现
#   content  正文片段，没有时这个字段不出现
for index, item in enumerate(result["data"]["results"], start=1):
    print()
    print(f"第 {index} 条:", item.get("title", ""))
    print("  链接:", item.get("url", ""))
    print("  摘要:", item.get("snippet", ""))
    print("  正文:", item.get("content", "")[:200])
```

## 返回示例


```json
{
  "code": 0,
  "data": {
    "metadata": {
      "search_time_ms": 654,
      "total_results": 2
    },
    "results": [
      {
        "content": "- Gartner client? Log in for personalized search results. ##### Gartner Magic Quadrant Abstract # Gartner Magic Quadrant for Generative AI Model Providers Publi…",
        "snippet": "Alibaba Cloud - Amazon - Anthropic - Cohere - DeepSeek - IBM - Microsoft - MiniMax - Mistral - Moonshot AI - NVIDIA - OpenAI - SpaceXAI - Zhipu AI",
        "title": "Magic Quadrant for Generative AI Model Providers - - Gartner client",
        "url": "https://www.gartner.com/en/documents/8335717#1"
      },
      {
        "content": "xAI (founded 2023 by Elon Musk) developed the Grok series and the Colossus 100,000-GPU training cluster. China. DeepSeek (founded 2023, backed by quantitative t…",
        "snippet": "Alibaba released Qwen 3.5 (February 16, 2026); ByteDance launched Doubao 2.0; Zhipu AI unveiled GLM-5, trained entirely on Huawei Ascend chips (further demonstr…",
        "title": "Punctuated Equilibria in Artificial Intelligence: The Institutional Scaling Law and the Speciation of Sovereign AI - xAI (founded 2023 by Elon Musk) developed the Grok series and the Colossus 100,000-GPU training cluster",
        "url": "https://ar5iv.labs.arxiv.org/html/2603.14664#4"
      }
    ]
  },
  "message": "success",
  "request_id": "6271523ad3cd457cbe38cea3772327bd",
  "usage": {
    "cost": "¥0.003"
  }
}
```


## 返回字段说明

| 字段 | 类型 | 说明 |
|------|------|------|
| `code` | integer | `0` 表示成功，`-1` 表示失败 |
| `message` | string | 成功时为 `success`，失败时为错误说明 |
| `request_id` | string | AnySearch 生成的请求 ID，排查问题时提供 |
| `data.results` | array | 搜索结果列表 |
| `data.results[].title` | string | 标题。一定有这个字段，但可能是空字符串 |
| `data.results[].url` | string | 结果链接。**想读全文时把它填到 [网页正文提取](/anysearch-extract) 请求的 `url`** |
| `data.results[].snippet` | string | 摘要。没有摘要时这个字段不出现，读取时要按可能缺失处理 |
| `data.results[].content` | string | 正文片段。没有时这个字段不出现。`format` 为 `markdown` 时是 Markdown 排版。垂直搜索时这里是结构化的数据文本，例如行情的各项数值 |
| `data.metadata.total_results` | integer | 本次实际返回的结果条数 |
| `data.metadata.search_time_ms` | integer | 搜索耗时，单位毫秒 |
| `usage.cost` | string | 本次请求的扣费金额，带货币符号 |

## 垂直搜索

垂直搜索和通用搜索是同一个接口，只是多填两个参数：

- `tag`：选哪一种专业数据，例如 `code.doc` 是开发文档，`finance.quote` 是金融行情。
- `params`：这个 `tag` 自己的附加参数，例如 `code.doc` 要填库名 `library`。

这两个参数的取值都来自 [AnySearch 能力发现](/anysearch-sub-domains)，按下面三步做：

1. **查有哪些 tag。** 在 [17 个领域](/anysearch-sub-domains#domains) 里选一个领域，调用能力发现接口，或者直接看 [垂直搜索 tag 速查表](/anysearch-tags)。返回里每个 `sub_domain` 的值就是一个可以用的 `tag`。
2. **看这个 tag 的参数。** 同一处返回里的 `params` 列出了参数名、含义和是否必填（`required`）。
3. **填进搜索请求。** `sub_domain` 的值原样填到 `tag`；参数名作为键填到 `params`；必填参数一定要填，可选参数按需填；`query` 换成对应的搜索词。

对应关系如下：

| 能力发现返回的内容 | 填到搜索请求的哪里 |
|------|------|
| `sub_domains[].sub_domain`，例如 `code.doc` | `tag` |
| `params` 里的参数名，例如 `library` | `params` 对象里的键 |
| `required` 为 `true` 的参数 | 必须出现在 `params` 里，缺少会返回 400 |
| 没有附加参数的 `tag`，例如 `health.stats` | 只填 `tag`，不要填 `params` |

填写规则：

- `tag` 必须是完整的 `领域.子领域`。只写 `finance` 会返回 400，message 为 `Invalid tag: finance.`。
- 缺少必填参数会返回 400，message 会写明缺哪个，例如 `Missing required params for tag 'finance.quote': type.`。
- 标成可选的参数，在某些取值组合下仍然可能是必须的，条件写在参数说明里。例如 `finance.quote` 的 `symbol` 是可选，但 `type` 为 `crypto` 时必须填。
- 参数值统一写成字符串即可，数值也一样，例如 `"period": "30d"`。
- 垂直搜索按搜索计费，和通用搜索同价。

### 垂直搜索示例代码

下面用 `code.doc`（开发文档搜索）查 React 的 `useEffect` 清理函数怎么写。`code.doc` 有一个必填参数 `library`，参数定义见 [code.doc](/anysearch-tags#tag-code-doc)。

```python
import requests
import json

# ===============================================================
# 步骤1: 配置 API 连接信息
# ===============================================================

# DMXAPI AnySearch 搜索接口(垂直搜索和通用搜索是同一个地址)
url = "https://www.dmxapi.cn/v1/search"

# DMXAPI 密钥，请替换为您自己的密钥
# 获取方式: 登录 DMXAPI 官网 -> 个人中心 -> API 密钥管理
api_key = "sk-***********************************************"

# ===============================================================
# 步骤2: 配置请求头
# ===============================================================

headers = {
    "Content-Type": "application/json",  # 指定请求体为 JSON 格式
    "Authorization": f"Bearer {api_key}",  # Bearer 认证，填 DMXAPI 密钥
}

# ===============================================================
# 步骤3: 配置请求参数
# ===============================================================

payload = {
    # 【query】(string，必填) 搜索词
    #   垂直搜索时写成这个领域里要查的内容
    "query": "useEffect cleanup",

    # 【tag】(string，垂直搜索必填) 能力标签
    #   必须写完整的“领域.子领域”，只写领域名(如 code)会返回 400
    #   取值来自能力发现接口返回的 sub_domain
    "tag": "code.doc",

    # 【params】(object，按 tag 的定义填) 这个 tag 的附加参数
    #   参数名、含义、是否必填都以能力发现返回的 params 为准
    #   code.doc 只有一个参数:
    #     library (必填) 要查文档的库或框架名，例如 react、express
    "params": {
        "library": "react",
    },

    # 【max_results】(integer，可选) 最多返回几条结果，1 到 10，不填时为 10
    "max_results": 3,

    # 【zone】【language】【format】(可选) 含义和通用搜索相同
    #   注意 zone 会影响垂直搜索取到的数据，不确定时不要填

    # 【model】
    "model": "anysearch",
}

# ===============================================================
# 步骤4: 发送请求并输出结果
# ===============================================================

response = requests.post(url, headers=headers, json=payload, timeout=60)
print("status:", response.status_code)
result = response.json()
print(json.dumps(result, indent=2, ensure_ascii=False))
response.raise_for_status()

# 垂直搜索的响应结构和通用搜索完全一样，数据同样在 data.results 里
for index, item in enumerate(result["data"]["results"], start=1):
    print()
    print(f"第 {index} 条:", item.get("title", ""))
    print("  链接:", item.get("url", ""))
    print("  摘要:", item.get("snippet", ""))
```

### 垂直搜索返回示例

HTTP 200

```json
{
  "code": 0,
  "data": {
    "metadata": {
      "search_time_ms": 4829,
      "total_results": 3
    },
    "results": [
      {
        "content": "Call useEffect at the top level of your component to connect to an external system. Pass a setup function that connects and returns a cleanup function that disconnects, plus a dependency array with ev…",
        "snippet": "Call useEffect at the top level of your component to connect to an external system. Pass a setup function that connects and returns a cleanup function that disconnects, plus a dependency array with ev…",
        "title": "Connect to an external system with useEffect",
        "url": "https://github.com/reactjs/react.dev/blob/main/src/content/reference/react/useEffect.md"
      },
      {
        "content": "Return a cleanup function from `useEffect` to disconnect from external systems when the component unmounts. In development, React runs setup and cleanup an extra time to verify cleanup logic. ```javas…",
        "snippet": "Return a cleanup function from `useEffect` to disconnect from external systems when the component unmounts. In development, React runs setup and cleanup an extra time to verify cleanup logic.",
        "title": "Clean up external connections in an Effect",
        "url": "https://github.com/reactjs/react.dev/blob/main/src/content/learn/escape-hatches.md"
      },
      {
        "content": "Returning a cleanup function from the Effect ensures React calls disconnect() before the Effect runs again and when the component unmounts. ```js useEffect(() => { const connection = createConnection(…",
        "snippet": "Returning a cleanup function from the Effect ensures React calls disconnect() before the Effect runs again and when the component unmounts.",
        "title": "Return cleanup function to disconnect on unmount",
        "url": "https://github.com/reactjs/react.dev/blob/main/src/content/learn/synchronizing-with-effects.md"
      }
    ]
  },
  "message": "success",
  "request_id": "03b4550e84774412b42ecf60a322879b"
}
```

示例里过长的 `snippet` 和 `content` 只保留了开头。和通用搜索一样，成功响应里还会带 `usage.cost`。

### 多个参数的例子：查股票行情

`finance.quote`（金融行情）有 4 个参数，其中 `type` 必填，完整定义见 [finance.quote](/anysearch-tags#tag-finance-quote)：

| 参数 | 是否必填 | 说明 |
|------|---------|------|
| `type` | 必填 | 资产类型：`stock` 股票（全球股票和 A 股）、`forex` 外汇、`crypto` 加密货币、`commodity` 大宗商品、`index` 中国指数、`etf` 中国 ETF |
| `symbol` | 可选 | 国际市场代码。股票如 `AAPL`，外汇如 `EURUSD`，加密货币如 `BTCUSD`（`type` 为 `crypto` 时必填），大宗商品如 `CLUSD` |
| `cn_code` | 可选 | 中国市场代码。股票如 `000001.SZ`，指数如 `399300.SZ`，ETF 如 `510300.SH` |
| `period` | 可选 | 历史数据的时间范围：`7d`、`14d`、`30d`、`90d`、`180d`、`1y`、`5y`，或自定义天数如 `45d`。国际市场默认 `7d`，中国市场默认 `30d` |

查苹果公司股价，请求体这样写（把上面示例代码里的 `payload` 换成下面的内容即可）：

```json
{
  "query": "Apple stock price",
  "tag": "finance.quote",
  "params": {
    "type": "stock",
    "symbol": "AAPL"
  },
  "max_results": 2
}
```

返回示例：

```json
{
  "code": 0,
  "data": {
    "metadata": {
      "search_time_ms": 1000,
      "total_results": 2
    },
    "results": [
      {
        "content": "Symbol: AAPL | Name: Apple Inc. | Exchange: NASDAQ | Price: 354.07 | Open: 348.12 | PrevClose: 349.08 | Change: +4.99 | Change%: +1.43% | DayHigh: 354.29 | DayLow: 345.88 | YearHigh: 360.83 | YearLow: 243.42 | Volume: 40235897 | MarketCap: 5145416054000 | Avg50: 342.13 | Avg200: 303.60",
        "snippet": "$354.07 ▲1.43% · 7d: High $356.42 / Low $340.56",
        "title": "Apple Inc. (AAPL)",
        "url": "https://site.financialmodelingprep.com/?ref=quote-AAPL"
      },
      {
        "content": "Symbol: AAPL.L | Name: LS 1x Apple Tracker ETC | Exchange: LSE | Price: 672.65 | Open: 0.00 | PrevClose: 637.67 | Change: +34.98 | Change%: +5.48% | DayHigh: 672.65 | DayLow: 672.65 | YearHigh: 672.65 | YearLow: 672.65 | Volume: 49 | MarketCap: 0 | Avg50: 0.00 | Avg200: 0.00",
        "snippet": "$672.65 ▲5.48%",
        "title": "LS 1x Apple Tracker ETC (AAPL.L)",
        "url": "https://site.financialmodelingprep.com/?ref=quote-AAPL.L"
      }
    ]
  },
  "message": "success",
  "request_id": "57da22fbcba64500ad246abd7ff167e1"
}
```

可以看到垂直搜索的结果不是网页，而是数据：`snippet` 是一句行情概括，`content` 是用 `|` 分隔的各项数值。

:::warning
垂直搜索返回 200 不代表一定取到了专业数据。下面两种情况接口不会报错，但返回的是普通网页结果：

- **`zone` 和要查的数据不匹配。** 查美股 `AAPL` 时带上 `"zone": "cn"`，返回的是普通网页；不填 `zone` 或填 `intl` 才返回行情数据。查 A 股（填 `cn_code`）时填 `cn` 是正常的。
- **参数没填够。** `finance.quote` 只填 `type` 不填 `symbol` 或 `cn_code`，返回的也是普通网页。

如果返回的内容不像这个领域的数据，先去掉 `zone` 再试，再检查 `params` 是否把要查的对象填上了。以上是 `finance.quote` 的实际表现，其他 `tag` 可以按同样的思路排查。
:::

## 把搜索结果交给网页正文提取

搜索结果里的 `content` 只是片段。需要整页正文时，把某条结果的 `url` 原样填到 [AnySearch 网页正文提取](/anysearch-extract) 请求的 `url` 字段：

| 搜索返回的内容 | 填到网页正文提取请求的哪里 |
|------|------|
| `data.results[].url` | `url` |

例如上面垂直搜索返回的第一条结果，提取请求体就是：

```json
{
  "url": "https://github.com/reactjs/react.dev/blob/main/src/content/reference/react/useEffect.md"
}
```

三个接口怎么配合使用，见 [AnySearch 使用说明](/anysearch#usage)。



<p align="center">
  <small>© 2026 DMXAPI AnySearch 搜索</small>
</p>
