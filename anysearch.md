# AnySearch 使用说明

AnySearch 是一个搜索服务，共三个接口：**搜索**、**能力发现**、**网页正文提取**。发一次请求就直接返回 JSON 结果，不需要提交任务再查询。本页先说明三个接口各自做什么、什么时候用哪个、怎么配合，每个接口的全部参数和返回说明在各自的文档里。

## 接口地址

| 接口 | 请求方式 | URL | 作用 | 详细文档 |
|------|---------|-----|------|------|
| 搜索 | POST | `https://www.dmxapi.cn/v1/search` | 通用网页搜索；加上 `tag` 和 `params` 是垂直搜索 | [AnySearch 搜索](/anysearch-search) |
| 能力发现 | POST | `https://www.dmxapi.cn/v1/sub-domains` | 查询垂直搜索可用的 `tag` 和每个 `tag` 的参数 | [AnySearch 能力发现](/anysearch-sub-domains) |
| 网页正文提取 | POST | `https://www.dmxapi.cn/v1/extract` | 读取一个网页的标题和正文 | [AnySearch 网页正文提取](/anysearch-extract) |


:::warning
请妥善保管您的 API Key！严禁将密钥泄露给他人、硬编码到代码中或提交到公开的代码仓库。如果怀疑密钥已泄露，请立即前往 DMXAPI 官网重新生成。
:::

## 模型名称

- `anysearch`

## 使用方法 {#usage}

先看你要做什么，再决定调哪个接口：

| 你要做的事 | 怎么调 |
|------|------|
| 搜网页 | 调**搜索**，只填搜索词 `query`。见 [用法一](#usage-1) |
| 搜专业数据，例如股票行情、论文、开发文档 | 先调**能力发现**查出 `tag` 和参数，再调**搜索**并带上它们。见 [用法二](#usage-2) |
| 读某个网页的全文 | 调**网页正文提取**，填网页地址 `url`。见 [用法三](#usage-3) |

三种用法的请求头完全一样，区别只有请求地址 `url` 和请求体 `payload`。下面用法一给出完整代码，用法二、用法三只列出要替换的 `url` 和 `payload`。

### 用法一：搜网页 {#usage-1}

请求体里填一个 `query` 就可以：

```python
import requests
import json

url = "https://www.dmxapi.cn/v1/search"
api_key = "sk-***********************************************"

headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {api_key}",
}

payload = {
    "query": "全球 AI大模型厂商汇总",  # 搜索词，唯一的必填参数
}

response = requests.post(url, headers=headers, json=payload, timeout=60)
print("status:", response.status_code)
print(json.dumps(response.json(), indent=2, ensure_ascii=False))
```

搜索结果在响应的 `data.results` 里，每条结果有这几项：

| 字段 | 说明 |
|------|------|
| `title` | 标题 |
| `url` | 结果链接。想读这条结果的全文，把它交给网页正文提取，见 [用法三](#usage-3) |
| `snippet` | 摘要 |
| `content` | 正文片段 |

返回条数、区域、语言、正文格式等可选参数，以及完整的返回示例，见 [AnySearch 搜索](/anysearch-search)。

### 用法二：搜专业数据（垂直搜索） {#usage-2}

垂直搜索还是调搜索接口，只是请求体里多填 `tag` 和 `params`。这两项不能随便写，要先从能力发现里查出来，所以分两步。

**第一步：调能力发现，查这个领域有哪些 `tag`。** 这里查 `code`（代码）领域：

```python
url = "https://www.dmxapi.cn/v1/sub-domains"

payload = {
    "domain": "code",  # 领域名，只能填固定的 17 个之一
}
```

返回内容（节选）：

```json
{
  "sub_domain": "code.doc",
  "description": "Query developer documentation and code examples by library name and topic across npm, PyPI, Cargo ecosystems",
  "params": {
    "library": {
      "description": "Library or framework name to query docs for, e.g. react, express",
      "required": true,
      "sort_order": 0
    }
  }
}
```

从这段返回里读出两件事：

- `sub_domain` 的值 `code.doc` 就是搜索时要填的 `tag`，用来搜开发文档。
- `params` 里列出了这个 `tag` 的参数：它有一个参数 `library`（要查的库名），`required` 为 `true` 表示必填。

**第二步：调搜索，把第一步查到的内容填进去。**

```python
url = "https://www.dmxapi.cn/v1/search"

payload = {
    "query": "useEffect cleanup",  # 搜索词
    "tag": "code.doc",             # 第一步返回的 sub_domain，原样填写
    "params": {
        "library": "react",        # 键是第一步返回的参数名 library，值按参数说明填
    },
}
```

返回的结构和用法一相同，结果同样在 `data.results` 里，只是内容来自 React 的官方文档。

两步之间的对应关系：

| 第一步（能力发现）返回的内容 | 填到第二步（搜索）请求的哪里 |
|------|------|
| `sub_domain`，例如 `code.doc` | `tag` |
| `params` 里的参数名，例如 `library` | `params` 里的键 |
| `required` 为 `true` 的参数 | 必须填，缺少会返回 400 |

补充说明：

- 第一步的 `domain` 可以填哪些值，见 [17 个领域](/anysearch-sub-domains#domains)。
- `tag` 和参数是相对固定的，查过一次就可以直接写在代码里，不用每次搜索前都调能力发现。
- 也可以不调能力发现，直接在 [垂直搜索 tag 速查表](/anysearch-tags) 里查，那里有全部 `tag` 和参数的中文说明。
- 更多例子（例如查股票行情）和填写时的注意事项，见 [AnySearch 搜索](/anysearch-search) 的“垂直搜索”部分。

### 用法三：读网页全文 {#usage-3}

搜索结果里的 `content` 只是片段。要整页正文时，把网页地址交给网页正文提取：

```python
url = "https://www.dmxapi.cn/v1/extract"

payload = {
    # 网页地址。这里填的是用法二搜索结果里第一条的 url，也可以填任意公开网页的地址
    "url": "https://github.com/reactjs/react.dev/blob/main/src/content/reference/react/useEffect.md",
}
```

返回的 `data.title` 是网页标题，`data.content` 是网页正文。

和搜索的对应关系：

| 搜索返回的内容 | 填到网页正文提取请求的哪里 |
|------|------|
| `data.results[].url` | `url` |

支持哪些网页、正文长度上限和截断规则，见 [AnySearch 网页正文提取](/anysearch-extract)。

<p align="center">
  <small>© 2026 DMXAPI AnySearch 使用说明</small>
</p>
