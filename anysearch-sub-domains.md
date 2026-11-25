# AnySearch 能力发现 API 使用文档

能力发现接口是 AnySearch 垂直搜索的“菜单”：你告诉它一个或多个领域名（例如 `finance`），它返回这些领域下有哪些可用的 `tag`，以及每个 `tag` 还能填哪些附加参数。它本身不做搜索，返回的内容是给 [AnySearch 搜索](/anysearch-search) 接口用的：`sub_domain` 填到搜索请求的 `tag`，`params` 里的参数名填到搜索请求的 `params`。只做通用搜索（不填 `tag`）时不需要调用这个接口。能力发现不计费，请求是同步的，结果直接在响应里返回。全部 `tag` 和参数的中文说明在 [AnySearch 垂直搜索 tag 速查表](/anysearch-tags) 里，也可以不调用接口直接查表。

## 接口地址

| 接口 | 请求方式 | URL |
|------|---------|-----|
| 能力发现 | POST | `https://www.dmxapi.cn/v1/sub-domains` |

:::warning
请妥善保管您的 API Key！严禁将密钥泄露给他人、硬编码到代码中或提交到公开的代码仓库。如果怀疑密钥已泄露，请立即前往 DMXAPI 官网重新生成。
:::

## 模型名称

- `anysearch`


## 请求参数

| 参数 | 类型 | 是否必填 | 说明 |
|------|------|---------|------|
| `domain` | string 或 array | 必填 | 要查询的领域名。查一个领域写字符串，如 `"finance"`；查多个领域写数组，如 `["finance", "code"]`。只能填下面“17 个领域”表格里的名字，必须全小写。一次最多 32 个，重复的名字会自动去重 |
| `model` | string | 可选 | 固定为 `anysearch`，可以不写 |

注意事项：

- 领域名必须拼写正确且全小写。填了不存在的名字（包括大小写不对，例如 `Finance`）时，整个请求会返回 502，即使同一次请求里其他领域名是对的。
- `domain` 填的是领域名（如 `finance`），不是完整的 `tag`（如 `finance.quote`）。
- 领域名只能包含字母、数字、下划线、点和短横线，含其他字符会返回 400。

## 17 个领域 {#domains}

`domain` 可以填的值只有下面这 17 个，必须全小写。每个领域下有哪些 `tag`，见 [tag 索引](/anysearch-tags#index)。

| 领域名 | 中文名 | 内容 |
|------|------|------|
| `general` | 通用搜索 | 通用网页搜索 |
| `resource` | 图片素材 | 图片搜索：专业摄影、SVG、插画和矢量图 |
| `social_media` | 社交媒体 | 社交媒体信息搜索 |
| `finance` | 金融 | 股票、外汇、加密货币、大宗商品、ETF、期货行情，以及财经新闻、基本面、宏观数据、选股、财经日历 |
| `academic` | 学术 | 学术论文、生物医学文献、预印本、引用关系、数据集 |
| `legal` | 法律 | 法院案例、法律法规、立法跟踪 |
| `health` | 医疗健康 | 药品信息、临床试验、公共卫生统计 |
| `business` | 商业 | 企业工商信息、商务联系人、招聘职位、国际贸易数据 |
| `security` | 网络安全 | 恶意样本扫描、威胁情报、背景噪声识别、CVE 漏洞 |
| `ip` | 专利 | 全球专利检索、同族追踪、法律状态，覆盖 100 多个国家和地区 |
| `code` | 代码 | 开发文档检索、GitHub 代码片段搜索 |
| `energy` | 能源 | 电力市场数据、能源生产与消费统计 |
| `environment` | 环境 | 空气质量指数（AQI）与 PM2.5 数据 |
| `agriculture` | 农业 | 联合国粮农组织（FAO）全球农业统计 |
| `travel` | 出行 | 机票搜索、航班实时动态 |
| `film` | 影音 | 影视与音乐种子搜索 |
| `gaming` | 游戏 | Steam 游戏价格、电竞选手数据与排名 |

## 能力发现示例代码

下面的例子一次查询 `code` 和 `environment` 两个领域，并把每个 `tag` 和它的参数整理打印出来。

```python
import requests
import json

# ===============================================================
# 步骤1: 配置 API 连接信息
# ===============================================================

# DMXAPI AnySearch 能力发现接口
url = "https://www.dmxapi.cn/v1/sub-domains"

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
    # 【domain】(string 或 array，必填) 要查询的领域名
    #   查一个领域: "domain": "finance"
    #   查多个领域: "domain": ["finance", "code"]
    #   可填的 17 个领域名(必须全小写):
    #     general       通用搜索        resource      图片素材
    #     social_media  社交媒体        finance       金融
    #     academic      学术            legal         法律
    #     health        医疗健康        business      商业
    #     security      网络安全        ip            专利
    #     code          代码            energy        能源
    #     environment   环境            agriculture   农业
    #     travel        出行            film          影音
    #     gaming        游戏
    #   名字拼错或大小写不对会返回 502，一次最多 32 个
    "domain": ["code", "environment"],

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

# 把每个 tag 和它的参数整理出来，后面照着填进搜索接口:
#   sub_domain            -> 搜索请求的 tag
#   params 里的每个参数名 -> 搜索请求的 params 里的键
#   required 为 true      -> 这个参数必须填
for domain in result["data"]["domains"]:
    print()
    print("领域:", domain["domain"], "-", domain.get("description", ""))
    for sub in domain.get("sub_domains", []):
        print("  tag:", sub["sub_domain"], "-", sub.get("description", ""))
        # 没有附加参数的 tag，返回里可能没有 params 这个字段
        params = sub.get("params") or {}
        if not params:
            print("    (没有附加参数，搜索时不用填 params)")
        # sort_order 是官方给出的参数展示顺序，数字小的排前面
        for name, info in sorted(params.items(), key=lambda item: item[1].get("sort_order", 0)):
            required = "必填" if info.get("required") else "可选"
            print(f"    params.{name} ({required}): {info.get('description', '')}")
```

## 返回示例


```json
{
  "code": 0,
  "data": {
    "billing_contract_version": 1,
    "domains": [
      {
        "description": "Developer documentation, code snippet search across GitHub",
        "domain": "code",
        "sub_domains": [
          {
            "description": "Query developer documentation and code examples by library name and topic across npm, PyPI, Cargo ecosystems",
            "params": {
              "library": {
                "description": "Library or framework name to query docs for, e.g. react, express",
                "required": true,
                "sort_order": 0
              }
            },
            "sub_domain": "code.doc"
          },
          {
            "description": "Search real code implementations across 1M+ public GitHub repositories with regex and language filtering",
            "params": {
              "lang": {
                "description": "Filter by programming language, e.g. TypeScript, Python",
                "required": false,
                "sort_order": 0
              },
              "path": {
                "description": "Filter by file path pattern, e.g. src/components/",
                "required": false,
                "sort_order": 0
              },
              "repo": {
                "description": "Filter by GitHub repository, e.g. facebook/react",
                "required": false,
                "sort_order": 0
              }
            },
            "sub_domain": "code.snippet"
          }
        ]
      },
      {
        "description": "Air quality index, AQI and PM2.5 data",
        "domain": "environment",
        "sub_domains": [
          {
            "description": "Real-time global air quality index (AQI) and PM2.5/PM10 data by city name",
            "params": {
              "location": {
                "description": "20002 / 38.9,-77.0 / Beijing (zip code / coordinates / city name)",
                "required": false,
                "sort_order": 1
              },
              "type": {
                "description": "GlobalAirQuality (global air quality)",
                "required": false,
                "sort_order": 0
              }
            },
            "sub_domain": "environment.aqi"
          }
        ]
      }
    ],
    "topology_generation": "e3ca65f1-5c8a-4142-a6d9-540ce67d6eba",
    "topology_version": 19
  },
  "message": "success",
  "request_id": "96693cf965b94e1f8ef223285dd59327"
}
```

成功响应里还会多出一个 `usage.cost` 字段，表示本次请求的扣费金额。能力发现不计费。

## 返回字段说明

| 字段 | 类型 | 说明 |
|------|------|------|
| `code` | integer | `0` 表示成功，`-1` 表示失败 |
| `message` | string | 成功时为 `success`，失败时为错误说明 |
| `request_id` | string | AnySearch 生成的请求 ID，排查问题时提供 |
| `data.domains` | array | 查到的领域列表，每个领域一项 |
| `data.domains[].domain` | string | 领域名，和请求里填的一致 |
| `data.domains[].description` | string | 领域说明（英文） |
| `data.domains[].sub_domains` | array | 这个领域下的全部 `tag` |
| `data.domains[].sub_domains[].sub_domain` | string | 完整的 `tag`，格式是 `领域.子领域`，例如 `code.doc`。**原样填到搜索请求的 `tag`** |
| `data.domains[].sub_domains[].description` | string | 这个 `tag` 能搜什么（英文） |
| `data.domains[].sub_domains[].params` | object | 这个 `tag` 的附加参数定义，键是参数名。没有附加参数时这个字段可能不出现 |
| `…params.参数名.description` | string | 参数含义、可选值和示例（英文） |
| `…params.参数名.required` | boolean | `true` 表示搜索时必须在 `params` 里填这个参数 |
| `…params.参数名.sort_order` | integer | 参数的展示顺序，数字小的在前，对请求没有影响 |
| `data.billing_contract_version`、`data.topology_generation`、`data.topology_version` | — | 能力定义的版本信息，调用搜索时用不到 |

参数定义只提供 `description`、`required`、`sort_order` 三项，不提供数据类型和枚举列表，可选值都写在 `description` 的文字里。

## 把返回结果用到搜索接口

能力发现的返回和 [AnySearch 搜索](/anysearch-search) 请求的对应关系：

| 能力发现返回的内容 | 填到搜索请求的哪里 |
|------|------|
| `sub_domains[].sub_domain`，例如 `code.doc` | `tag`，原样填写，例如 `"tag": "code.doc"` |
| `params` 里的参数名，例如 `library` | `params` 对象里的键，例如 `"params": {"library": "react"}` |
| `required` 为 `true` 的参数 | 必须出现在 `params` 里，缺少会返回 400 |
| `required` 为 `false` 的参数 | 按需填写，不需要就不写 |
| 没有附加参数的 `tag`，例如 `health.stats` | 只填 `tag`，不要填 `params` |

以上面返回示例里的 `code.doc` 为例：它有一个必填参数 `library`（要查文档的库名），所以搜索请求这样写：

```json
{
  "query": "useEffect cleanup",
  "tag": "code.doc",
  "params": {
    "library": "react"
  }
}
```

再看 `environment.aqi`：`type` 和 `location` 都是可选参数，查北京空气质量可以这样写：

```json
{
  "query": "北京空气质量",
  "tag": "environment.aqi",
  "params": {
    "location": "Beijing"
  }
}
```

填写时要注意：

- 标成可选（`required` 为 `false`）的参数，在某些取值组合下仍然可能是必须的，这类条件写在参数说明里。例如 `finance.quote` 的 `symbol` 标的是可选，但 `type` 为 `crypto` 时必须填。
- 参数值统一写成字符串即可，数值也一样，例如 `"period": "30d"`、`"min_citations": "100"`。
- 完整的搜索请求写法、可运行的代码和返回示例见 [AnySearch 搜索](/anysearch-search) 的“垂直搜索”部分。

## 完整的 tag 与参数列表

能力发现接口能查到的全部内容（17 个领域、39 个 `tag`、190 个参数），已经整理成中文放在 [AnySearch 垂直搜索 tag 速查表](/anysearch-tags) 里，不调接口也能直接查。需要最新定义时以本页接口的返回为准。

<p align="center">
  <small>© 2026 DMXAPI AnySearch 能力发现</small>
</p>
