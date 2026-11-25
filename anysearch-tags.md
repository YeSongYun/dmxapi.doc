---
outline: [2, 3]
---

# AnySearch 垂直搜索 tag 速查表

本页是 [AnySearch 能力发现](/anysearch-sub-domains) 接口能查到的内容的完整中文整理：17 个领域、39 个 `tag`、190 个参数。做垂直搜索时，`tag` 和 `params` 填哪个名字、填什么值，都在这里查，不调用接口也能直接写出请求。

用法：下文小标题上的完整名称（例如 `finance.quote`）就是搜索请求的 `tag`，它下面表格里的参数名就是 `params` 里的键。例如查苹果股价：

```json
{
  "query": "Apple stock price",
  "tag": "finance.quote",
  "params": {
    "type": "stock",
    "symbol": "AAPL"
  }
}
```

「必填」的参数一定要填，缺少会返回 400；「可选」的按需填，不需要就不写；写着「这个 tag 没有额外参数」的，搜索时只填 `tag`，不要填 `params`。完整的搜索请求写法和可运行代码见 [AnySearch 搜索](/anysearch-search) 的“垂直搜索”部分，这些参数从返回值里怎么找见 [AnySearch 能力发现](/anysearch-sub-domains) 的“把返回结果用到搜索接口”部分。

内容来自能力发现接口 2026 年 11 月 25 日的实际返回（能力定义版本 19），参数说明已译成中文。AnySearch 会不定期增减 `tag` 和参数，如果这里查不到，或者按这里填写后返回 400，请调用能力发现接口获取最新定义，以接口返回为准。

## tag 索引 {#index}

先按领域找到你要的 `tag`，点进去看它的参数。页面目录里也列出了每个 `tag`，可以直接跳转。

| 领域 | tag |
|------|------|
| `general` 通用搜索 | [`general.general`](#tag-general-general) |
| `resource` 图片素材 | [`resource.image`](#tag-resource-image) |
| `social_media` 社交媒体 | [`social_media.social_media`](#tag-social-media-social-media) |
| `finance` 金融 | [`finance.calendar`](#tag-finance-calendar)、[`finance.fundamental`](#tag-finance-fundamental)、[`finance.macro`](#tag-finance-macro)、[`finance.news`](#tag-finance-news)、[`finance.quote`](#tag-finance-quote)、[`finance.screen`](#tag-finance-screen) |
| `academic` 学术 | [`academic.citation`](#tag-academic-citation)、[`academic.dataset`](#tag-academic-dataset)、[`academic.paper`](#tag-academic-paper)、[`academic.person`](#tag-academic-person) |
| `legal` 法律 | [`legal.enforcement`](#tag-legal-enforcement)、[`legal.judicial`](#tag-legal-judicial)、[`legal.legislation`](#tag-legal-legislation) |
| `health` 医疗健康 | [`health.drug`](#tag-health-drug)、[`health.stats`](#tag-health-stats)、[`health.trial`](#tag-health-trial) |
| `business` 商业 | [`business.company`](#tag-business-company)、[`business.jobs`](#tag-business-jobs)、[`business.people`](#tag-business-people)、[`business.trade`](#tag-business-trade) |
| `security` 网络安全 | [`security.intel`](#tag-security-intel)、[`security.noise`](#tag-security-noise)、[`security.scan`](#tag-security-scan)、[`security.vuln`](#tag-security-vuln) |
| `ip` 专利 | [`ip.global`](#tag-ip-global) |
| `code` 代码 | [`code.doc`](#tag-code-doc)、[`code.snippet`](#tag-code-snippet) |
| `energy` 能源 | [`energy.electricity`](#tag-energy-electricity)、[`energy.production`](#tag-energy-production) |
| `environment` 环境 | [`environment.aqi`](#tag-environment-aqi) |
| `agriculture` 农业 | [`agriculture.fao`](#tag-agriculture-fao) |
| `travel` 出行 | [`travel.flight`](#tag-travel-flight)、[`travel.flight_status`](#tag-travel-flight-status) |
| `film` 影音 | [`film.torrent`](#tag-film-torrent) |
| `gaming` 游戏 | [`gaming.esports`](#tag-gaming-esports)、[`gaming.store`](#tag-gaming-store) |

## general（通用搜索） {#domain-general}

通用网页搜索。

### general.general {#tag-general-general}

通用网页搜索。只做通用搜索时，`tag` 可以不填。

这个 tag 没有额外参数，搜索时只填 `tag`，不用填 `params`。

## resource（图片素材） {#domain-resource}

图片搜索：专业摄影、SVG、插画和矢量图。

### resource.image {#tag-resource-image}

专业摄影图、各类图库照片、SVG、插画和矢量图。

这个 tag 没有额外参数，搜索时只填 `tag`，不用填 `params`。

## social_media（社交媒体） {#domain-social-media}

社交媒体信息搜索。

### social_media.social_media {#tag-social-media-social-media}

社交媒体信息搜索与检索。

| 参数 | 是否必填 | 说明 |
|------|---------|------|
| `type` | 可选 | 目标平台和搜索方式。可选值：`weibo`、`weibo_hot`、`zhihu`、`zhihu_hot`、`x_top`、`x_latest`、`x_media`、`x_people`、`x_lists`、`reddit_post`、`reddit_community`、`reddit_comment`、`reddit_media`、`reddit_people`、`linkedin_people`、`linkedin_jobs`、`linkedin_company`、`linkedin_posts`、`wechatmp` |
| `keyword` | 可选 | 搜索关键词，优先级高于 `query`。例如 `AI large models`、`Python developer`、`Musk` |
| `region` | 可选 | 地区过滤，仅 `type=weibo_hot` 时生效。例如 `Beijing`、`Shanghai`、`Guangdong` |

## finance（金融） {#domain-finance}

股票、外汇、加密货币、大宗商品、ETF、期货行情，以及财经新闻、基本面、宏观数据、选股、财经日历。

### finance.calendar {#tag-finance-calendar}

财报发布日、分红事件、经济数据发布、IPO 日程。

| 参数 | 是否必填 | 说明 |
|------|---------|------|
| `type` | **必填** | 日历类型：`earnings`（财报）、`dividends`（分红）、`ipos`（IPO）、`economic`（经济数据）。`earnings` 需要传 `symbol` 或 `cn_code`；`dividends` 只有国际市场的全市场数据，`symbol` 和 `cn_code` 对它不起作用 |
| `period` | 可选 | 向后查看的时间范围，默认 `7d`；`type=earnings` 时请固定传 `90d`。可选值：`7d`、`14d`、`30d`、`90d`、`180d`、`1y`、`5y`，或自定义 `{N}d`（N 为天数） |
| `symbol` | 可选 | 股票代码，仅 `type=earnings` 时使用，例如 `NVDA`、`AAPL`。留空返回全市场日程 |
| `cn_code` | 可选 | A 股代码，`type=earnings` 时使用，例如 `600519.SH`。留空返回全市场日程 |

### finance.fundamental {#tag-finance-fundamental}

财务报表、估值指标、分析师评级、股东结构、SEC 文件。代码怎么填取决于 `type`：`overview` 读 `symbol`，其余五种读 `cn_code`；但这两个参数每次都必须同时出现，用不到的那个传空字符串 `""`。

| 参数 | 是否必填 | 说明 |
|------|---------|------|
| `type` | **必填** | 数据类型：`overview`（概览）、`income`（利润表）、`balance`（资产负债表）、`cashflow`（现金流量表）、`indicator`（财务指标，返回 ROE、PE、利润率等估值和盈利比率）、`holder`（股东） |
| `symbol` | **必填** | 国际市场股票代码，`type=overview` 时用它定位公司，例如 `AAPL`；留空则从 `query` 里解析。`type` 为 `income`、`balance`、`cashflow`、`indicator`、`holder` 时传 `""` |
| `cn_code` | **必填** | A 股代码，`type` 为 `income`、`balance`、`cashflow`、`indicator`、`holder` 时用它定位公司，例如 `600519.SH`。`type=overview` 时传 `""` |
| `period` | 可选 | 只有两种 `type` 会读取：`overview`（填 `annual` 或 `quarter`，默认 `annual`；`annual` 是最近一个完整财年，`quarter` 是最近一个单季度，口径不同）和 `holder`（时间范围，默认 `1y`）。其余四种不使用 |

### finance.macro {#tag-finance-macro}

宏观经济指标：GDP、CPI、利率（Shibor、LPR、联邦基金利率）、货币供应量、社会融资规模。

| 参数 | 是否必填 | 说明 |
|------|---------|------|
| `type` | **必填** | 指标类型：`gdp`（中美 GDP）、`cpi`（中美 CPI）、`fed_funds`（美国联邦基金利率）、`treasury`（美国国债收益率曲线，1 个月至 30 年）、`unemployment`（美国失业率）、`nonfarm`（美国非农就业）、`shibor`（上海银行间同业拆放利率）、`lpr`（中国贷款市场报价利率）、`money_supply`（中国 M0、M1、M2）、`social_finance`（中国社会融资规模） |
| `period` | 可选 | 数据时间范围。默认值随 `type` 变化：`gdp` 默认 `2y`；`cpi`、`lpr`、`money_supply`、`social_finance` 默认 `1y`；`shibor` 默认 `30d`；美国指标按 `max_results` 截取。可选值：`7d`、`14d`、`30d`、`90d`、`180d`、`1y`、`5y`，或自定义 `{N}d`（N 为天数） |

### finance.news {#tag-finance-news}

全球财经新闻、上市公司公告、券商研报摘要。

| 参数 | 是否必填 | 说明 |
|------|---------|------|
| `type` | **必填** | 新闻类型：`general`（全球英文财经新闻）、`stock`（国际市场个股新闻）、`flash`（中文财经快讯）、`announcement`（A 股上市公司公告） |
| `symbol` | 可选 | 国际市场股票代码，仅 `type=stock` 时使用，例如 `AAPL`。留空则从 `query` 里解析 |
| `cn_code` | 可选 | A 股代码，仅 `type=announcement` 时使用，例如 `600519.SH`。留空返回全市场公告 |
| `period` | 可选 | 查询时间范围。`type` 为 `flash`、`announcement` 时默认 `1d`（当天）。可选值：`7d`、`14d`、`30d`、`90d`、`180d`、`1y`、`5y`，或自定义 `{N}d`（N 为天数） |
| `news_src` | 可选 | 中文快讯来源，仅 `type=flash` 时使用，默认 `sina`。可选值：`sina`（新浪财经）、`wallstreetcn`（华尔街见闻）、`10jqka`（同花顺）、`eastmoney`（东方财富）、`cls`（财联社）、`yicai`（第一财经）、`yuncaijing`（云财经）、`fenghuang`（凤凰财经）、`jinrongjie`（金融界） |

### finance.quote {#tag-finance-quote}

股票、外汇、加密货币、大宗商品、指数、ETF、期货的实时和历史价格、成交量、市值数据。

| 参数 | 是否必填 | 说明 |
|------|---------|------|
| `type` | **必填** | 资产类型：`stock`（全球股票和 A 股）、`forex`（外汇）、`crypto`（加密货币）、`commodity`（大宗商品）、`index`（中国指数）、`etf`（中国 ETF） |
| `symbol` | 可选 | 国际市场代码。`type=stock` 例如 `AAPL`；`type=forex` 例如 `EURUSD`（6 位货币对）；`type=crypto` 例如 `BTCUSD`（此时必填）；`type=commodity` 例如 `CLUSD`（留空返回市场快照） |
| `cn_code` | 可选 | 中国市场代码。`type=stock` 例如 `000001.SZ`、`600519.SH`；`type=index` 例如 `399300.SZ`；`type=etf` 例如 `510300.SH`；`type=forex` 例如 `USDCNH.FXCM` |
| `period` | 可选 | 历史数据时间范围。可选值：`7d`、`14d`、`30d`、`90d`、`180d`、`1y`、`5y`，或自定义 `{N}d`（N 为天数）。国际市场默认 `7d`，中国市场默认 `30d` |

### finance.screen {#tag-finance-screen}

按行业和国家筛选股票，按市值排序（仅国际市场）。

| 参数 | 是否必填 | 说明 |
|------|---------|------|
| `type` | **必填** | 筛选类型：`stock`（按行业、国家筛选股票）、`etf`（按名称搜索 ETF，`query` 作为过滤条件） |
| `sector` | 可选 | GICS 行业，仅 `type=stock` 时使用。可选值：`Technology`、`Healthcare`、`Financial Services`、`Consumer Cyclical`、`Consumer Defensive`、`Industrials`、`Energy`、`Basic Materials`、`Communication Services`、`Real Estate`、`Utilities` |
| `country` | 可选 | ISO 3166-1 两位国家代码，仅 `type=stock` 时使用，例如 `US`、`JP`、`GB`、`DE`、`CN`、`HK`。注意：按公司注册地过滤，不是按交易所所在地 |

## academic（学术） {#domain-academic}

学术论文、生物医学文献、预印本、引用关系、数据集。

### academic.citation {#tag-academic-citation}

按 DOI 或标题查询引用关系、被引次数、参考文献列表。

| 参数 | 是否必填 | 说明 |
|------|---------|------|
| `doi` | 可选 | DOI 标识符，例如 `10.1038/s41586-021-03819-2` |
| `op` | 可选 | 操作类型：`metadata`（查元数据，默认）、`citations`（被引列表）、`references`（参考文献列表）、`citation-count`（被引次数）、`reference-count`（参考文献数量）、`author`（某作者的作品）、`editor`（某编者的作品）、`venue-citation-count`（期刊被引次数）、`citation`（单条引用关系，需要 OCI） |
| `id_type` | 可选 | 标识符类型：`doi`、`pmid`、`issn`、`isbn`、`orcid`、`omid`。留空时按 `query` 的格式自动识别（如 `10.xxx/yyy` 识别为 doi，纯数字识别为 pmid） |
| `filter` | 可选 | RAMOSE 过滤表达式，格式 `字段:值`，例如 `creation:2020-*-*`（2020 年之后的引用） |
| `sort` | 可选 | RAMOSE 排序表达式，格式 `字段:顺序`，例如 `creation:desc`（按创建时间倒序） |
| `type` | 可选 | 有两种用法。① 文献类型过滤：`journal-article`（期刊论文）、`book`（图书）、`proceedings-article`（会议论文）、`dataset`（数据集）、`book-chapter`（图书章节）、`posted-content`（预印本）、`report`（报告）等，对应 Crossref 的 `filter=type:{value}`。② 出版类型，多个值用英文逗号分隔（不要空格），共 13 个可选值：`JournalArticle`、`Conference`、`Review`、`CaseReport`、`ClinicalTrial`、`Dataset`、`Editorial`、`LettersAndComments`、`MetaAnalysis`、`News`、`Study`、`Book`、`BookSection`，对应 `publicationTypes` 参数 |
| `year_from` | 可选 | 出版日期下限，格式 `YYYY`、`YYYY-MM` 或 `YYYY-MM-DD` |
| `year_to` | 可选 | 出版日期上限，格式 `YYYY`、`YYYY-MM` 或 `YYYY-MM-DD` |
| `min_citations` | 可选 | 最低被引次数，非负整数字符串，例如 `100`。用于筛选高质量文献 |
| `open_access` | 可选 | 是否开放获取。可选值：`true`、`false` |
| `venue` | 可选 | 期刊或会议名称，多个值用英文逗号分隔，必须与 Semantic Scholar 数据库中的名称完全一致。常用值：`NeurIPS`、`ICML`、`ICLR`、`CVPR`、`Nature`、`Science`、`Cell`、`Lancet` |
| `category` | 可选 | 学科分类，多个值用英文逗号分隔，共 22 个可选值：`Computer Science`、`Medicine`、`Biology`、`Chemistry`、`Physics`、`Mathematics`、`Materials Science`、`Engineering`、`Environmental Science`、`Geology`、`Geography`、`Sociology`、`Psychology`、`Economics`、`Business`、`Political Science`、`Linguistics`、`Philosophy`、`History`、`Art`、`Education`、`Law` |
| `id` | **必填** | 持久标识符的值，不要带 `doi:`、`pmid:` 这类前缀。支持的格式：DOI（如 `10.1038/s41586-021-03819-2`）、PMID（纯数字，如 `33817056`）、ISSN（如 `0138-9130`）、ISBN（如 `9781402096327`）、ORCID（如 `0000-0003-0530-4305`）、OMID（如 `br/06101801781`）、OCI（数字-数字，如 `06101801781-06180334099`，仅用于 `op=citation`） |

### academic.dataset {#tag-academic-dataset}

Zenodo、Dryad、Figshare 上的科研数据集、开源代码和科研软件。

| 参数 | 是否必填 | 说明 |
|------|---------|------|
| `client_id` | 可选 | 数据仓库标识，例如 `cern.zenodo`（Zenodo）、`figshare.ars`（Figshare）、`bl.dryad`（Dryad） |
| `resource_type` | 可选 | 资源类型过滤：`Dataset`（数据集）、`Software`（软件）、`Text`（文本）、`Image`（图片）、`Audiovisual`（音视频）、`Collection`（合集）、`InteractiveResource`（交互式资源）等 |
| `year_from` | 可选 | 发布年份下限（含），例如 `2020` |
| `year_to` | 可选 | 发布年份上限（含），例如 `2024` |

### academic.paper {#tag-academic-paper}

跨学科论文搜索：按关键词、标题、作者、机构检索，返回元数据和开放获取链接。下表中写着“目前仅出现在结果摘要中”的参数，官方定义注明当前还不能当过滤条件用。

| 参数 | 是否必填 | 说明 |
|------|---------|------|
| `authors` | 可选 | 作者姓名，多个值用英文逗号分隔。目前仅出现在结果摘要中，尚不能过滤（官方规划的过滤方式：in、contains） |
| `categories` | 可选 | 主题标签，例如 `cs.LG`、`Topic Modeling`，多个值用英文逗号分隔。目前仅出现在结果摘要中，尚不能过滤（官方规划的过滤方式：in、contains） |
| `category` | 可选 | 学科分类，写法随数据源不同：Semantic Scholar 用研究领域名称，arXiv 用分类代码（如 `cs.AI`），CORE 用研究领域名称 |
| `citation_count` | 可选 | 被引次数，非负数。目前仅出现在结果摘要中，尚不能过滤（官方规划的过滤方式：gt、gte、lte） |
| `citation_doi` | 可选 | 被引论文的 DOI，多个值用英文逗号分隔。目前仅出现在结果摘要中，尚不能过滤（官方规划的过滤方式：in、contains） |
| `data_source` | 可选 | 上游数据源过滤，多个值用英文逗号分隔，例如 `arxiv,openalex`。它和 Europe PMC 专用的 `source` 参数是两回事 |
| `date_type` | 可选 | PubMed 的日期维度。可选值：`pdat`、`edat`、`mdat` |
| `document_type` | 可选 | CORE 的文档类型，例如 `research`、`thesis`、`review`、`book` |
| `doi` | 可选 | 按 DOI 直接查找，OpenAlex、Semantic Scholar、Europe PMC、CORE 等数据源支持。目前仅出现在结果摘要中，尚不能过滤（官方规划的过滤方式：eq、in） |
| `domain` | 可选 | 按来源站点域名过滤，例如 `arxiv.org`。注意这是 `params` 里的参数，和能力发现接口的 `domain` 不是一回事 |
| `field` | 可选 | 限定检索字段。PubMed 可选值：`tiab`、`title`、`author`、`journal`、`mesh`、`all`；arXiv 可选值：`ti`、`au`、`abs`、`co`、`jr`、`cat`、`category`、`all`。其他数据源忽略此参数 |
| `has_pdf` | 可选 | 只返回带 PDF 全文的结果，仅 Europe PMC 支持 |
| `journal` | 可选 | 期刊或会议名称。目前仅出现在结果摘要中，尚不能过滤（官方规划的过滤方式：eq、in、contains） |
| `kind` | 可选 | 文档形态。可选值：`abstract`（摘要）、`fulltext`（全文）。目前仅出现在结果摘要中，尚不能过滤（官方规划的过滤方式：eq、in） |
| `language` | 可选 | ISO 639-1 语言代码过滤，OpenAlex、CORE、Sciverse 等数据源支持 |
| `min_citations` | 可选 | 最低被引次数，Semantic Scholar 和 OpenAlex 支持 |
| `open_access` | 可选 | 只返回开放获取的文献。Europe PMC、OpenAlex、Semantic Scholar 支持；PubMed 只支持 `true` |
| `order` | 可选 | arXiv 按日期排序时的方向。可选值：`asc`、`desc` |
| `publication_type` | 可选 | 出版类型。可选值：`journal_article`、`preprint`、`book_chapter`、`conference_paper`、`other`、`book`、`thesis`、`dataset`、`report`、`review`、`monograph`、`standard`、`component`、`journal_issue`、`edited_book`。目前仅出现在结果摘要中，尚不能过滤（官方规划的过滤方式：eq、in） |
| `sort` | 可选 | 排序方式。可选值：`relevance`（相关度）、`date`（日期）、`cited`（被引次数）。PubMed、Europe PMC、OpenAlex、arXiv 支持 |
| `source` | 可选 | Europe PMC 子库过滤。可选值：`MED`、`PMC`、`PPR`、`AGR`、`PAT` 等 |
| `type` | 可选 | 出版类型，写法随数据源不同。OpenAlex 可选值：`article`、`book`、`book-chapter`、`dataset`、`dissertation`、`preprint`、`report`、`review`、`other`；Semantic Scholar 使用它自己的出版类型词表；其他数据源忽略此参数 |
| `venue` | 可选 | 期刊或会议名称，多个值用英文逗号分隔，仅 Semantic Scholar 支持 |
| `year_from` | 可选 | 发表或提交年份下限。PubMed、Europe PMC、OpenAlex、Semantic Scholar、arXiv、CORE 等数据源支持 |
| `year_to` | 可选 | 发表或提交年份上限。PubMed、Europe PMC、OpenAlex、Semantic Scholar、arXiv、CORE 等数据源支持 |

### academic.person {#tag-academic-person}

按姓名或 ORCID 搜索学者，结果里带所属机构、毕业院校和研究方向。

| 参数 | 是否必填 | 说明 |
|------|---------|------|
| `orcid` | 可选 | ORCID 标识符，用于精确查找某位学者，例如 `0000-0002-1825-0097` |
| `name` | 可选 | 学者姓名 |
| `affiliations` | 可选 | 机构名称，多个值用英文逗号分隔；与结果中的所属机构匹配 |
| `schools` | 可选 | 院校名称，多个值用英文逗号分隔；与结果中的院校匹配 |
| `research_areas` | 可选 | 研究方向，多个值用英文逗号分隔；与结果中的研究方向匹配 |

## legal（法律） {#domain-legal}

法院案例、法律法规、立法跟踪。

### legal.enforcement {#tag-legal-enforcement}

各法域的行政执法决定、处罚和监管措施。

| 参数 | 是否必填 | 说明 |
|------|---------|------|
| `decision_number` | 可选 | 执法决定文号 |
| `authority` | 可选 | 执法机关名称 |
| `jurisdiction` | 可选 | 法域代码，例如 `CN`、`US`、`FR` |
| `decision_type` | 可选 | 决定类型。可选值：`penalty`（处罚）、`inspection`（检查）、`order`（命令）、`other`（其他） |
| `penalty_types` | 可选 | 处罚种类，多个值用英文逗号分隔，例如 `fine`（罚款）、`disgorgement`（没收违法所得）、`license_revocation`（吊销许可）、`business_suspension`（停业） |
| `regulatory_domain` | 可选 | 监管领域，例如 `data_protection`（数据保护）、`securities`（证券）、`market_regulation`（市场监管）、`other`（其他） |
| `legal_basis` | 可选 | 法律依据条文，多个值用英文逗号分隔 |
| `subject_names` | 可选 | 被处罚主体名称，多个值用英文逗号分隔 |
| `decision_date` | 可选 | 决定日期，格式 `YYYY-MM-DD`（仅部分数据源支持） |
| `penalty_amount` | 可选 | 处罚金额，写成数字字符串 |
| `currency` | 可选 | ISO 4217 货币代码，例如 `CNY`、`USD`、`EUR` |

### legal.judicial {#tag-legal-judicial}

全球各法域的司法案例、法院裁判和法律意见。

| 参数 | 是否必填 | 说明 |
|------|---------|------|
| `case_number` | 可选 | 案号，例如 `（2024）京01民终123号` |
| `court` | 可选 | 法院名称 |
| `jurisdiction` | 可选 | 法域代码，例如 `CN`、`US`、`CA`、`ECHR` |
| `case_type` | 可选 | 案件类型。可选值：`civil`（民事）、`criminal`（刑事）、`administrative`（行政）、`other`（其他）、`enforcement`（执行） |
| `cause_of_action` | 可选 | 案由，例如 `民间借贷纠纷` |
| `procedure` | 可选 | 审理程序。可选值：`first_instance`（一审）、`second_instance`（二审）、`retrial`（再审）、`other`（其他） |
| `judgment_date` | 可选 | 裁判日期，格式 `YYYY-MM-DD`（仅部分数据源支持） |
| `document_type` | 可选 | 文书类型（新版字段）。可选值：`judgment`（判决）、`ruling`（裁定）、`decision`（决定）、`order`（命令） |
| `legal_basis` | 可选 | 法律依据条文，多个值用英文逗号分隔 |
| `doc_type` | 可选 | 旧版的文书类型字段，取值随数据源而定，不支持的值会被忽略 |
| `respondent` | 可选 | 被申请国的国家代码，用于欧洲人权法院 HUDOC 数据库，例如 `TUR`、`FRA`、`RUS` |
| `language` | 可选 | 结果语言，ISO 639-1 代码，例如 `en`、`fr`（仅部分数据源支持） |
| `database_id` | 可选 | 数据源专用的法院数据库标识，例如 CanLII 的 `csc-scc`、`onca` |
| `service` | 可选 | 指定数据源的具体服务，例如北大法宝（pkulaw）的 `case`、`casekw` |
| `case_id` | 可选 | 数据源专用的案件标识，例如 CanLII 的案件 ID |

### legal.legislation {#tag-legal-legislation}

全球各法域的法律、法规、规章、监管规则和立法跟踪。

| 参数 | 是否必填 | 说明 |
|------|---------|------|
| `document_number` | 可选 | 官方文号，例如 `主席令第X号`、`法释〔2020〕X号` |
| `issuing_authority` | 可选 | 发布机关名称 |
| `jurisdiction` | 可选 | 法域代码，例如 `CN`、`CN-GD`、`US`、`FR`、`JP` |
| `legal_level` | 可选 | 效力层级。可选值：`local_regulation`（地方性法规）、`statute`（法律）、`regulation`（法规）、`judicial_interpretation`（司法解释）、`ministerial_rule`（部门规章）、`decision`（决定）、`other`（其他）、`bill`（法案）、`decree`（法令） |
| `effective_status` | 可选 | 时效状态。可选值：`effective`（现行有效）、`not_yet_effective`（尚未生效）、`repealed`（已废止） |
| `effective_from` | 可选 | 生效日期下限，格式 `YYYY`、`YYYY-MM` 或 `YYYY-MM-DD` |
| `effective_to` | 可选 | 生效日期上限，格式 `YYYY`、`YYYY-MM` 或 `YYYY-MM-DD` |
| `article_number` | 可选 | 条文序号，例如 `第二十条` |
| `collection` | 可选 | 数据源专用的文献集代码，例如 `FR`、`CFR`、`USCODE`、`BILLS` |
| `historical` | 可选 | 是否包含历史版本。可选值：`true`、`false` |
| `language` | 可选 | 结果语言，ISO 639-1 代码，例如 `zh`、`en`、`fr`、`de` |
| `doc_type` | 可选 | 旧版的文献类型字段，取值随数据源而定，不支持的值会被忽略 |
| `title` | 可选 | 数据源专用的标题，或美国联邦法规（CFR）的卷号 |
| `date_from` | 可选 | 发布或生效日期下限，格式 `YYYY-MM-DD`（仅部分数据源支持） |
| `date_to` | 可选 | 发布日期上限，格式 `YYYY-MM-DD`（仅部分数据源支持） |
| `agency` | 可选 | 发布机构的标识或名称（仅部分数据源支持） |
| `congress` | 可选 | 美国国会届次，例如 `118`、`119` |
| `service` | 可选 | 指定数据源的具体服务，例如北大法宝（pkulaw）的 `law`、`law-search` |
| `database_id` | 可选 | 数据源专用的数据库标识 |
| `resource_kind` | 可选 | 法规资源种类。可选值：`rules`、`resources`、`all` |

## health（医疗健康） {#domain-health}

药品信息、临床试验、公共卫生统计。

### health.drug {#tag-health-drug}

按药品名称、NDC 编码或条形码查询药品说明书、不良反应、相互作用、召回信息。

| 参数 | 是否必填 | 说明 |
|------|---------|------|
| `type` | **必填** | 查询方式：`name`（按药品名称搜索）、`ndc`（按 NDC 编码查询）、`upc`（按 UPC 条形码查询） |

### health.stats {#tag-health-stats}

194 个国家的全球公共卫生统计：死亡率、发病率、预期寿命、疾病负担。

这个 tag 没有额外参数，搜索时只填 `tag`，不用填 `params`。

### health.trial {#tag-health-trial}

临床试验注册库搜索：按疾病、药物、试验阶段、地区检索，返回入组标准和试验状态。

这个 tag 没有额外参数，搜索时只填 `tag`，不用填 `params`。

## business（商业） {#domain-business}

企业工商信息、商务联系人、招聘职位、国际贸易数据。

### business.company {#tag-business-company}

全球企业的工商注册、股东结构、高管和经营状态信息。

| 参数 | 是否必填 | 说明 |
|------|---------|------|
| `type` | 可选 | 数据类型：`ChineseEnterprise`（中国企业工商信息）、`GlobalLEI`（全球 LEI 法人识别编码）、`USFilings`（美国 SEC 文件） |
| `keyword` | 可选 | 公司名称、统一社会信用代码、LEI 编码或股票代码，例如 `Alibaba`、`Apple Inc.`、`AAPL` |

### business.jobs {#tag-business-jobs}

全球招聘职位搜索：按职位、技能、地点、薪资检索，覆盖 16 个以上国家。

| 参数 | 是否必填 | 说明 |
|------|---------|------|
| `keyword` | 可选 | 搜索关键词，例如 `software engineer`、`python` |
| `location` | 可选 | 城市、地区或国家，例如 `San Francisco`、`London`、`us` |
| `salary_min` | 可选 | 最低年薪（美元），例如 `80000`、`120000` |
| `type` | 可选 | 职位类型：`GeneralJobs`（普通职位）、`RemoteJobs`（远程职位）、`USFederalJobs`（美国联邦政府职位） |

### business.people {#tag-business-people}

商务联系人搜索：按职位、公司、地点检索，返回商务邮箱和职业背景。

| 参数 | 是否必填 | 说明 |
|------|---------|------|
| `keyword` | 可选 | 搜索关键词或公司域名，例如 `software engineer`、`stripe.com` |
| `location` | 可选 | 地点过滤，例如 `California`、`London` |
| `seniority` | 可选 | 职级过滤，例如 `executive`、`senior`、`entry` |
| `title` | 可选 | 职位过滤，例如 `CTO`、`Head of Engineering` |
| `type` | 可选 | 查询类型：`PeopleSearch`（联系人搜索）、`EmailLookup`（按域名查邮箱） |

### business.trade {#tag-business-trade}

国际贸易统计：按商品编码、国家和时间段查询进出口数据。

| 参数 | 是否必填 | 说明 |
|------|---------|------|
| `date_start` | 可选 | 年份，例如 `2023` |
| `flow` | 可选 | 贸易方向：`export`（出口）、`import`（进口）、`both`（进出口） |
| `hs_code` | 可选 | HS 商品编码，必须是 2、4、6 或 10 位，例如 `0902`、`8471` |
| `location` | 可选 | 贸易伙伴国名称，例如 `China`、`United States` |
| `type` | 可选 | 数据类型：`GlobalBilateralTrade`（全球双边贸易）、`USImportExport`（美国进出口） |

## security（网络安全） {#domain-security}

恶意样本扫描、威胁情报、背景噪声识别、CVE 漏洞。

### security.intel {#tag-security-intel}

IP、域名、URL 或文件哈希的威胁情报，含历史恶意记录和 IOC 指标。

| 参数 | 是否必填 | 说明 |
|------|---------|------|
| `ioc` | **必填** | 失陷指标（IOC）：域名、IP、URL 或文件哈希 |

### security.noise {#tag-security-noise}

判断一个 IPv4 地址是互联网背景扫描噪声，还是已知的正规服务。

| 参数 | 是否必填 | 说明 |
|------|---------|------|
| `ip` | **必填** | 要检查的单个 IPv4 地址，例如 `8.8.8.8` |

### security.scan {#tag-security-scan}

把文件哈希、URL、IP 或域名提交给 70 多家安全厂商做聚合扫描。

| 参数 | 是否必填 | 说明 |
|------|---------|------|
| `ioc` | **必填** | 要扫描的失陷指标（IOC）：域名、IP、URL 或文件哈希（MD5、SHA1、SHA256） |

### security.vuln {#tag-security-vuln}

CVE 漏洞详情：CVSS 评分、受影响版本、补丁链接、是否已被利用。

| 参数 | 是否必填 | 说明 |
|------|---------|------|
| `type` | **必填** | 查询意图：`cve`（CVE 编号）、`commit`（40 位十六进制提交哈希）、`package`（`生态:包名@版本`，生态名区分大小写）。标识符写在 `value` 里，`query` 也填同一个标识符 |
| `value` | **必填** | 与 `type` 对应的标识符：CVE 编号、40 位十六进制哈希，或 `生态:包名@版本`。多个值用英文逗号分隔可批量查询，重复项自动去除。<br>生态名必须与注册表名称完全一致且区分大小写：`npm`、`PyPI`、`Maven`、`NuGet`、`RubyGems`、`crates.io`、`Go`、`Packagist`、`Hex`、`Pub`、`CRAN`。Maven 的写法是 `Maven:groupId:artifactId@version`；操作系统软件包通常要带发行版后缀，例如 `Debian:12`、`Alpine:v3.16`。<br>为保证每一项都被检查，单次最多传 5 个 CVE 编号或 1000 个软件包条目。<br>返回空列表也可能是名称或版本拼错了，下结论“没有漏洞”之前请先核对拼写。<br>示例：`{"type": "cve", "value": "CVE-2021-44228"}`、`{"type": "package", "value": "PyPI:jinja2@2.4.1"}`、`{"type": "commit", "value": "6879efc2c1596d11a6a6ad296f80063b558d5e0f"}` |

## ip（专利） {#domain-ip}

全球专利检索、同族追踪、法律状态，覆盖 100 多个国家和地区。

### ip.global {#tag-ip-global}

基于 EPO DOCDB/INPADOC 的全球专利聚合与同族追踪，覆盖 100 多个国家和地区，含法律状态。

| 参数 | 是否必填 | 说明 |
|------|---------|------|
| `type` | 可选 | 数据类型：`GlobalPatent`（全球专利） |
| `keyword` | 可选 | 搜索关键词，例如 `solar cell`、`AI` |
| `applicant` | 可选 | 申请人或机构名称过滤，例如 `Huawei`、`Huawei Technologies` |
| `ipc` | 可选 | IPC/CPC 分类号过滤，例如 `H01L`、`G06N` |
| `date_start` | 可选 | 公开日或申请日的起始日期，例如 `2020`、`20200101` |

## code（代码） {#domain-code}

开发文档检索、GitHub 代码片段搜索。

### code.doc {#tag-code-doc}

按库名和主题查询开发文档与代码示例，覆盖 npm、PyPI、Cargo 生态。

| 参数 | 是否必填 | 说明 |
|------|---------|------|
| `library` | **必填** | 要查文档的库或框架名称，例如 `react`、`express` |

### code.snippet {#tag-code-snippet}

在 100 多万个 GitHub 公开仓库里搜索真实代码实现，支持正则和语言过滤。

| 参数 | 是否必填 | 说明 |
|------|---------|------|
| `lang` | 可选 | 按编程语言过滤，例如 `TypeScript`、`Python` |
| `path` | 可选 | 按文件路径过滤，例如 `src/components/` |
| `repo` | 可选 | 按 GitHub 仓库过滤，例如 `facebook/react` |

## energy（能源） {#domain-energy}

电力市场数据、能源生产与消费统计。

### energy.electricity {#tag-energy-electricity}

电力市场数据：电价、发电结构、用电需求、碳排放强度，覆盖 200 多个国家和地区。

| 参数 | 是否必填 | 说明 |
|------|---------|------|
| `date_end` | 可选 | 结束日期，例如 `2026-05-24`、`2025` |
| `date_start` | 可选 | 开始日期，例如 `2026-05-23`、`2020` |
| `location` | 可选 | 地区名称，例如 `France`、`New South Wales`、`California`、`China` |
| `metric` | 可选 | 指标：`price`（电价）、`generation`（发电量）、`emissions`（排放）、`demand`（需求）、`capacity`（装机容量） |
| `type` | 可选 | 数据类型：`EUElectricity`（欧洲）、`AustralianElectricity`（澳大利亚）、`USEnergyData`（美国）、`GlobalElectricity`（全球） |

### energy.production {#tag-energy-production}

石油、天然气、煤炭、核能、可再生能源的生产与消费统计，含产量和库存。

| 参数 | 是否必填 | 说明 |
|------|---------|------|
| `date_start` | 可选 | 开始日期，例如 `2023-01`、`2020` |
| `frequency` | 可选 | 数据频率：`monthly`（月度）、`annual`（年度）、`quarterly`（季度） |
| `keyword` | 可选 | 搜索关键词，例如 `crude oil production`、`residential electricity price` |
| `location` | 可选 | 地区名称，例如 `California`、`Texas`、`United States` |
| `type` | 可选 | 数据类型：`USEnergyData`（美国能源数据） |

## environment（环境） {#domain-environment}

空气质量指数（AQI）与 PM2.5 数据。

### environment.aqi {#tag-environment-aqi}

按城市名查询全球实时空气质量指数（AQI）和 PM2.5、PM10 数据。

| 参数 | 是否必填 | 说明 |
|------|---------|------|
| `type` | 可选 | 数据类型：`GlobalAirQuality`（全球空气质量） |
| `location` | 可选 | 邮编、经纬度或城市名，例如 `20002`、`38.9,-77.0`、`Beijing` |

## agriculture（农业） {#domain-agriculture}

联合国粮农组织（FAO）全球农业统计。

### agriculture.fao {#tag-agriculture-fao}

FAO 全球农业统计，覆盖生产、贸易和食品价格。

| 参数 | 是否必填 | 说明 |
|------|---------|------|
| `date_start` | 可选 | 年份，例如 `2023` |
| `domain` | 可选 | 数据范围：`production`（生产）、`trade`（贸易）、`prices`（价格）。注意这是 `params` 里的参数，和能力发现接口的 `domain` 不是一回事 |
| `keyword` | 可选 | 搜索关键词，例如 `wheat production`、`rice trade` |
| `location` | 可选 | 地区名称，例如 `World`、`China` |
| `type` | 可选 | 数据类型：`GlobalAgriculture`（全球农业数据） |

## travel（出行） {#domain-travel}

机票搜索、航班实时动态。

### travel.flight {#tag-travel-flight}

全球机票搜索：按出发地、目的地、日期、舱位检索，含行李额和比价。

| 参数 | 是否必填 | 说明 |
|------|---------|------|
| `adults` | 可选 | 成人人数 |
| `arrival` | **必填** | 到达机场的 IATA 三字码 |
| `cabin_class` | 可选 | 舱位。可选值：`Economy`（经济舱）、`Business`（商务舱）、`First`（头等舱）、`PremiumEconomy`（超级经济舱） |
| `children` | 可选 | 儿童人数 |
| `currency` | 可选 | 货币代码，例如 `USD`、`CNY` |
| `date` | **必填** | 出发日期，例如 `15/06/2026`、`2026-06-15` |
| `departure` | **必填** | 出发机场的 IATA 三字码，例如 `PEK`、`LAX` |
| `destination` | 可选 | 目的地的 IATA 代码或城市名，例如 `SFO`、`London` |
| `infants` | 可选 | 婴儿人数 |
| `origin` | 可选 | 出发地的 IATA 代码或城市名，例如 `HAN`、`PEK`、`Beijing` |
| `return_date` | 可选 | 返程日期，例如 `25/06/2026`；留空表示单程 |
| `type` | 可选 | 数据类型：`FlightSearch`（机票搜索） |

### travel.flight_status {#tag-travel-flight-status}

航班实时起降状态、登机口、延误信息和机场航显。

| 参数 | 是否必填 | 说明 |
|------|---------|------|
| `type` | 可选 | `FlightStatus`。可以不填，选了这个 tag 就已经是航班动态模式 |
| `flight_number` | **必填** | IATA 航班号，例如 `DL47`、`CA981` |
| `date` | 可选 | 航班日期，格式 `YYYY-MM-DD`，默认当天 |
| `departure` | **必填** | 出发机场的 IATA 代码，用于区分同号航班。官方定义的文字说明写的是“可选”，但字段标记为必填，实测不填会返回 400 |

## film（影音） {#domain-film}

影视与音乐种子搜索。

### film.torrent {#tag-film-torrent}

搜索影视和音乐的 BT 种子资源，返回磁力链接、文件大小和做种数。

这个 tag 没有额外参数，搜索时只填 `tag`，不用填 `params`。

## gaming（游戏） {#domain-gaming}

Steam 游戏价格、电竞选手数据与排名。

### gaming.esports {#tag-gaming-esports}

英雄联盟等游戏的电竞选手数据、排名、英雄属性和装备数据。

| 参数 | 是否必填 | 说明 |
|------|---------|------|
| `type` | **必填** | 查询类别，决定调用哪条数据链路、还需要哪些其他参数。可选值：`player`（最近 N 场对局记录和排位概况）、`ranked`（仅排位数据：段位、胜点、各队列胜负，不含对局详情）、`mastery`（英雄熟练度列表）、`live_game`（选手当前是否在对局中，在则返回对局状态）、`match_detail`（按对局 ID 返回全部参与者的详细数据）、`leaderboard`（某赛区某队列的顶尖选手榜）、`champion`（英雄静态数据：名称、称号，用 `query` 模糊搜索）、`item`（装备静态数据：名称、价格，用 `query` 模糊搜索）、`champion_rotation`（某平台当前的周免英雄） |
| `region` | 可选 | 服务器赛区。可选值：`kr`（韩国）、`na`（北美）、`euw`（西欧）、`eune`（北欧与东欧）、`jp`（日本）、`br`（巴西）、`la1`（拉丁美洲北部）、`la2`（拉丁美洲南部）、`oc`（大洋洲）、`tr`（土耳其）、`ru`（俄罗斯）、`sg` 或 `sea`（东南亚）。`type` 为 `player`、`ranked`、`mastery`、`live_game`、`leaderboard` 时必填；`champion_rotation` 可不填，默认 `na` |
| `game_name` | 可选 | 选手的游戏 ID。两种写法：用 `#` 带上 tagLine，例如 `Hide on Bush#KR1`（仍需填 `region`）；或不带 tagLine，例如 `Tyler1`（按 `region` 自动推断该服务器的默认 tagLine）。`type` 为 `player`、`ranked`、`mastery`、`live_game` 时必填。又如 `Faker#KR1` |
| `match_id` | 可选 | 完整的对局 ID，格式 `{赛区前缀}_{数字ID}`，赛区前缀会自动决定路由，不用再填 `region`。`type=match_detail` 时必填。例如 `KR_7482819248`、`NA1_4912837465`、`EUW1_6723541890` |
| `queue` | 可选 | 排位队列过滤。可选值：`RANKED_SOLO_5x5`（单双排）、`RANKED_FLEX_SR`（灵活组排）。`player`、`ranked` 不填则返回所有队列的数据；`leaderboard` 不填默认 `RANKED_SOLO_5x5`。适用于 `player`、`ranked`、`leaderboard` |
| `champion` | 可选 | 英雄名称的子串过滤，名称里包含该值的英雄都会匹配，例如 `Lee` 匹配 Lee Sin，`vi` 匹配 Vi 和 Sivir。不填则返回熟练度最高的若干英雄。适用于 `mastery` |
| `tier` | 可选 | 段位过滤。不填时自动按胜点取 Challenger、Grandmaster、Master。可选值：`CHALLENGER`、`GRANDMASTER`、`MASTER`、`DIAMOND`、`EMERALD`、`PLATINUM`、`GOLD`、`SILVER`、`BRONZE`、`IRON`。`CHALLENGER`、`GRANDMASTER`、`MASTER` 没有小段，不要填 `division`。适用于 `leaderboard` |
| `division` | 可选 | 段位内的小段，只在 `tier` 为 `DIAMOND` 到 `IRON` 时有意义；填了 `tier` 没填它时默认 `I`。可选值：`I`、`II`、`III`、`IV`。适用于 `leaderboard`（需要同时填 `tier`） |

### gaming.store {#tag-gaming-store}

Steam 游戏的实时价格、折扣、用户评价、在线人数、成就，含中国区定价。

这个 tag 没有额外参数，搜索时只填 `tag`，不用填 `params`。

<p align="center">
  <small>© 2026 DMXAPI AnySearch 垂直搜索 tag 速查表</small>
</p>
