# Tencent-Search 联网搜索 API 使用文档

腾讯云联网搜索，提供实时联网检索服务。支持三种返回模式：自然检索结果、多模态 VR 百科结果及二者混合，可按域名、时间范围精准过滤结果。搜索结果以结构化 JSON 数组返回，每条结果包含标题、摘要、来源 URL、发布时间、相关性得分（0–1）及图片列表等字段，适合需要结合实时网络信息进行问答、知识增强或内容摘要的 AI 应用场景。

## 🌐 请求地址

```
https://www.dmxapi.cn/v1/responses
```
:::warning
请妥善保管您的 API Key！严禁将密钥泄露给他人、硬编码到代码中或提交到公开的代码仓库。如果怀疑密钥已泄露，请立即前往 DMXAPI 官网重新生成。
:::

## 🤖 模型名称

- `Tencent-Search`

## 💻 联网搜索示例代码

```python
import requests
import json

# ===================================================================
# 步骤1: 配置 API 连接信息
# ===================================================================

# DMXAPI 服务端点地址
url = "https://www.dmxapi.cn/v1/responses"

# DMXAPI 密钥 (请替换为您自己的密钥)
# 获取方式: 登录 DMXAPI 官网 -> 个人中心 -> API 密钥管理
api_key = "sk-*************************************************"

# ===================================================================
# 步骤2: 配置请求头
# ===================================================================

headers = {
    "Content-Type": "application/json",      # 指定请求体为 JSON 格式
    "Authorization": f"{api_key}",           # token 认证方式
}

# ===================================================================
# 步骤3: 配置请求参数
# ===================================================================

payload = {
    # 【model】(string, 必填) 指定联网搜索模型
    # 固定填写 "Tencent-Search"，不可替换为其他模型名称，否则请求会报错
    "model": "Tencent-Search",

    # 【input】(string, 必填) 搜索词，即用户的查询内容
    # 对应腾讯云 SearchPro 接口的 Query 参数
    # 支持中文和英文；建议简洁表达核心意图，过长的查询词可能导致搜索精度下降
    # 示例值: "今天北京的天气"
    "input": "三星堆的由来",

    # 【Mode】(integer, 可选) 返回结果类型，默认值为 0
    # 可选值:
    #   0 - 自然检索结果：返回普通网页搜索结果，适合大多数问答和信息检索场景
    #   1 - 多模态VR结果：返回腾讯百科类图文结构化内容，结果条数较少但信息更丰富，
    #       适合查询人物、地点、概念等百科类问题；此模式下 Site/FromTime/ToTime 均无效
    #   2 - 混合结果：同时返回上述两种结果，内容最全面，
    #       适合对结果完整性要求高、对响应速度不敏感的场景
    "Mode": 0,

    # 【Site】(string, 可选) 指定域名站内搜索，用于过滤自然检索结果
    # 只填域名部分，不含 "http://" 协议头和路径，例如填 "zhihu.com" 而非 "https://www.zhihu.com/xxx"
    # 注意: mode=1 时该参数无效（VR百科是独立数据源，不支持站内过滤）
    #       mode=0 时对所有结果生效；mode=2 时仅对自然检索部分生效
    # 示例值: "zhihu.com"
    "Site": "zhihu.com",

    # 【FromTime】(integer, 可选) 搜索结果的起始发布时间，精确到秒的 Unix 时间戳
    # 注意: mode=1 时该参数无效；mode=0/2 时对自然检索结果生效
    # 示例值: 1745498501
    # "FromTime": 1778404417,

    # 【ToTime】(integer, 可选) 搜索结果的截止发布时间，精确到秒的 Unix 时间戳
    # 与 FromTime 用法相同，可单独使用或配合 FromTime 组成时间区间
    # 注意: mode=1 时该参数无效；mode=0/2 时对自然检索结果生效
    # 示例值: 1745498501
    # "ToTime": 1778663665,
}

# ===================================================================
# 步骤4: 发送请求并输出结果
# ===================================================================

# 发送 POST 请求到 API 服务器
response = requests.post(url, headers=headers, json=payload)

# 解析响应，将 Pages 里的 JSON 字符串展开再输出
result = response.json()
pages = result.get("Response", {}).get("Pages", [])
parsed_pages = []
for page in pages:
    try:
        parsed_pages.append(json.loads(page))
    except (json.JSONDecodeError, TypeError):
        parsed_pages.append(page)

if parsed_pages:
    result["Response"]["Pages"] = parsed_pages

print(json.dumps(result, indent=2, ensure_ascii=False))
```

## 📄 返回示例

```json
{
  "Response": {
    "RequestId": "ba26910913c44a6bb8911bc91d4c6b09",
    "Query": "三星堆的由来",
    "Pages": [
      {
        "passage": "三星堆 名字的由来:广汉位于成都平原的北部,广汉城外的一片平原上有三个大的土堆,这个地方就叫三星堆｡这三个土堆和一个低矮的弧形的台地被牧马河隔开,也有人称其为 三星伴月 ｡ 三星堆遗址分布范围约12平方干米｡城址面积约3.6平方干米,与商代王都河南郑州商城规模相当,是古蜀国的都邑所在｡ 三星堆文化 (约当夏-商时期) 三星堆是古蜀国鱼凫统治时期的文明,古蜀国经历了五位王,分别是蚕丛,柏灌, 鱼凫 ",
        "score": 0.78855467,
        "date": "2023-11-01 09:48:00",
        "title": "三星堆——揭开古蜀族神秘面纱 - 知乎",
        "url": "https://zhuanlan.zhihu.com/p/664206191",
        "site": "知乎",
        "images": [
          "https://pic1.zhimg.com/v2-70876e35e84a9f7e3a4a0bdba17c3618_r.jpg"
        ],
        "favicon": "http://img04.sogoucdn.com/app/a/200913/227e8153170b79598ec7048fb37f2c3f.png"
      },
      {
        "passage": "因当地有个村子就叫三星堆,而给考古遗址起名原则是以“小地名”为原则来命名｡另外,三星堆遗址所在的位置,从地图上来看,三个土堆呈直线排列,很像天上的三颗星星,加上遗址北边有一处形似弯月的台地,在风水学中称此为“三星伴月”｡因此,取名为三星堆｡ 三星堆在1929年时,被一位住在月亮湾的农民在其住宅旁淘沟车水灌田时,在沟底发现了璧､圭､琮､璋等玉石礼器,并拿到古玩市场售卖｡",
        "score": 0.7835149,
        "date": "2024-03-23 22:05:00",
        "title": "【三星堆05】话即历史,历史也将在代代相传中变为神话 - 知乎",
        "url": "https://zhuanlan.zhihu.com/p/688671391",
        "site": "知乎",
        "images": [
          "https://pic2.zhimg.com/v2-ababbf82f80afb02fde4882ed3e23e81_r.jpg"
        ],
        "favicon": "http://img04.sogoucdn.com/app/a/200913/227e8153170b79598ec7048fb37f2c3f.png"
      },
    ],
    "Version": "standard"
  }
}
```


<p align="center">
  <small>© 2026 DMXAPI Tencent-Search 联网搜索</small>
</p>
