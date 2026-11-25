# AnySearch 网页正文提取 API 使用文档

网页正文提取接口输入一个网页地址，返回这个网页的标题和正文文本，适合在搜索之后读取某条结果的全文，或者把任意公开网页的内容交给大模型做总结和问答。请求体只有一个参数 `url`，通常直接取自 [AnySearch 搜索](/anysearch-search) 返回的 `data.results[].url`，也可以填任何公开的 http 或 https 地址。支持 HTML、纯文本、JSON 和 Markdown 页面，不支持 PDF、图片、音频、视频，也不能读取需要登录的页面。返回的正文最多 50000 个字符，超出部分会被截断。请求是同步的，一次请求直接返回结果，单个网页最长处理 30 秒。

## 接口地址

| 接口 | 请求方式 | URL |
|------|---------|-----|
| 网页正文提取 | POST | `https://www.dmxapi.cn/v1/extract` |


:::warning
请妥善保管您的 API Key！严禁将密钥泄露给他人、硬编码到代码中或提交到公开的代码仓库。如果怀疑密钥已泄露，请立即前往 DMXAPI 官网重新生成。
:::

## 模型名称

- `anysearch`


## 请求参数

| 参数 | 类型 | 是否必填 | 说明 |
|------|------|---------|------|
| `url` | string | 必填 | 要提取正文的网页地址。必须是完整的公开地址，以 `http://` 或 `https://` 开头，中间不能有空格 |
| `model` | string | 可选 | 固定为 `anysearch`，可以不写 |

除了上面两个参数，请求体里不能再有其他字段。这个接口没有 `format`、Cookie、自定义请求头、等待时间之类的选项，多写任何一个字段都会返回 400，而且 message 是 `URL is invalid.`，容易误以为是地址写错了。

## url 从哪里来

最常见的用法是先搜索、再提取：

| 搜索返回的内容 | 填到本接口请求的哪里 |
|------|------|
| [AnySearch 搜索](/anysearch-search) 返回的 `data.results[].url` | `url`，原样填写 |

搜索结果里的 `content` 只是片段，把同一条结果的 `url` 交给本接口，就能拿到整页正文。三个接口怎么配合使用，见 [AnySearch 使用说明](/anysearch#usage)。

`url` 也可以不来自搜索，直接填你已经知道的网页地址。

## 能提取什么，不能提取什么

| 情况 | 是否支持 | 说明 |
|------|---------|------|
| HTML、XHTML 网页 | 支持 | 返回页面里的文字内容，链接、标题等会保留成 Markdown 写法。页面上的导航、页脚等文字也可能一并出现在正文里 |
| 纯文本、JSON、Markdown | 支持 | 返回文件的文本内容 |
| 需要执行 JavaScript 才显示内容的页面 | 由服务端决定 | 是否渲染由 AnySearch 自动判断，请求里无法指定 |
| 会跳转的地址 | 支持 | 会跟随跳转去取内容，但返回的 `data.url` 仍然是你提交的原地址 |
| PDF、图片、音频、视频 | 不支持 | 返回 422 |
| 需要登录才能看的页面 | 不支持 | 无法带 Cookie。有些网站会返回登录页或验证页，这时接口可能照样返回 200，`content` 是登录页的文字，使用前请检查内容 |
| `localhost`、`127.0.0.1` 等本机或内网地址 | 不支持 | 返回 403 |

## 正文长度和截断

- `content` 最多 50000 个字符（按 Unicode 字符计，一个汉字算一个）。
- HTML 和纯文本页面被截断时，末尾会加上 `...(content truncated)`。为了保持结构完整，HTML 页面截断后的长度可能略短于 50000。
- JSON 和 Markdown 页面被截断时，直接切到 50000 个字符，末尾没有任何标记，截断后的 JSON 可能无法解析。
- 响应里没有“是否被截断”的字段。需要判断时，检查 `content` 是否以 `...(content truncated)` 结尾，或者长度是否正好达到 50000。

## 网页正文提取示例代码

```python
import requests
import json

# ===============================================================
# 步骤1: 配置 API 连接信息
# ===============================================================

# DMXAPI AnySearch 网页正文提取接口
url = "https://www.dmxapi.cn/v1/extract"

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
    # 【url】(string，必填) 要提取正文的网页地址
    #   必须以 http:// 或 https:// 开头，是公开可访问的完整地址
    #   通常取自搜索接口返回的 data.results[].url，也可以直接填已知的网页地址
    #   支持: HTML、纯文本、JSON、Markdown 页面
    #   不支持: PDF、图片、音频、视频、需要登录的页面、本机和内网地址
    "url": "https://example.com",

    # 【model】(string，可选) 固定为 anysearch
    "model": "anysearch",

    # 注意: 除了 url 和 model，不要再加任何其他字段，否则返回 400
}

# ===============================================================
# 步骤4: 发送请求并输出结果
# ===============================================================

# 单个网页最长处理 30 秒，客户端超时建议设为 60 秒
response = requests.post(url, headers=headers, json=payload, timeout=60)
print("status:", response.status_code)
result = response.json()
print(json.dumps(result, indent=2, ensure_ascii=False))
response.raise_for_status()

# 取出标题和正文:
#   data.url      你提交的原地址(即使发生了跳转也不变)
#   data.title    网页标题，取不到时是空字符串
#   data.content  网页正文，最多 50000 个字符
title = result["data"]["title"]
content = result["data"]["content"]
print()
print("标题:", title)
print("正文字数:", len(content))

# HTML 和纯文本被截断时末尾有这个标记；JSON 和 Markdown 被截断时没有标记
if content.endswith("...(content truncated)"):
    print("提示: 正文超过长度上限，已被截断")

# 把正文保存成文本文件
with open("extract_result.txt", "w", encoding="utf-8") as file:
    file.write(content)
print("正文已保存到 extract_result.txt")
```

## 返回示例

HTTP 200

```json
{
  "code": 0,
  "data": {
    "content": "This domain is for use in documentation examples without needing permission. This is not a service; avoid relying on it for testing and monitoring purposes.",
    "title": "Example Domain",
    "url": "https://example.com"
  },
  "message": "success",
  "request_id": "b83bde0c36014388bfa39a8bc309edf5"
}
```

成功响应里还会多出一个 `usage.cost` 字段，表示本次请求的扣费金额。

## 返回字段说明

| 字段 | 类型 | 说明 |
|------|------|------|
| `code` | integer | `0` 表示成功，`-1` 表示失败 |
| `message` | string | 成功时为 `success`，失败时为错误说明 |
| `request_id` | string | AnySearch 生成的请求 ID，排查问题时提供 |
| `data.url` | string | 你提交的原地址。即使网页发生了跳转，这里也不会变成跳转后的地址 |
| `data.title` | string | 网页标题，取不到时是空字符串 |
| `data.content` | string | 网页正文，最多 50000 个字符，截断规则见上文 |
| `usage.cost` | string | 本次请求的扣费金额，带货币符号 |

:::warning
提取到的正文来自第三方网页，内容不受控制。把它交给大模型时，请当作资料处理，不要让模型执行其中的指令。
:::



<p align="center">
  <small>© 2026 DMXAPI AnySearch 网页正文提取</small>
</p>
