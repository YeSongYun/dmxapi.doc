# Qwen-MT 翻译模型 API 文档

Qwen-MT模型是基于Qwen3模型优化的机器翻译大语言模型，支持92个语种（包括中、英、日、韩、法、西、德、泰、印尼、越、阿等）互译，且提供了术语干预、领域提示、记忆库等能力，提升模型在复杂应用场景下的翻译效果。


## 📍 请求地址

```
https://www.dmxapi.cn/v1/chat/completions
```

## 🎯 模型名称

`qwen-mt-flash` ,
`qwen-mt-plus` ,
`qwen-mt-turbo` 

## 💻 普通翻译 调用示例

```python
# ============================================================================
#                     Qwen-MT 机器翻译 API 调用示例
# ============================================================================
# 功能说明：使用通义千问机器翻译模型进行基础翻译
# 模型名称：qwen-mt-plus
# 特点：自动检测源语言，简单易用的基础翻译接口
# ============================================================================

import requests


# ----------------------------------------------------------------------------
#                              API 配置信息
# ----------------------------------------------------------------------------

# API 密钥（请替换为你自己的密钥）
api_key = "sk-***************************************"

# API 请求地址
url = "https://www.dmxapi.cn/v1/chat/completions"

# 请求头配置
headers = {
    "Authorization": f"Bearer {api_key}",  # 认证信息
    "Content-Type": "application/json"      # 内容类型为 JSON
}


# ----------------------------------------------------------------------------
#                              请求参数配置
# ----------------------------------------------------------------------------

data = {
    # 指定使用的翻译模型
    "model": "qwen-mt-plus",

    # 消息内容：包含需要翻译的文本
    "messages": [
        {
            "role": "user",
            "content": "我看到这个视频后没有笑"  # 待翻译的中文文本
        }
    ],

    # 翻译选项配置
    "translation_options": {
        "source_lang": "auto",     # 源语言：自动检测
        "target_lang": "English"   # 目标语言：英语
    }
}


# ----------------------------------------------------------------------------
#                              发送请求并输出结果
# ----------------------------------------------------------------------------

# 发送 POST 请求到翻译 API
response = requests.post(url, headers=headers, json=data)

# 打印返回的 JSON 结果
print(response.json())

```



## 🚀 普通翻译（流式输出）调用示例

```python
# ============================================================================
#                   Qwen-MT 机器翻译 API 调用示例（流式输出）
# ============================================================================
# 功能说明：使用通义千问机器翻译模型进行流式翻译输出
# 模型名称：qwen-mt-plus
# 特点：支持 SSE（Server-Sent Events）流式响应，实时显示翻译结果
# 适用场景：长文本翻译、需要实时反馈的翻译应用
# ============================================================================

import requests
import json


# ----------------------------------------------------------------------------
#                              API 配置信息
# ----------------------------------------------------------------------------

# API 请求地址
url = "https://www.dmxapi.cn/v1/chat/completions"

# API 密钥（请替换为你自己的密钥）
api_key = "sk-***************************************"

# 请求头配置
headers = {
    "Authorization": f"Bearer {api_key}",  # 认证信息
    "Content-Type": "application/json"      # 内容类型为 JSON
}

# ----------------------------------------------------------------------------
#                              请求参数配置
# ----------------------------------------------------------------------------

data = {
    # 指定使用的翻译模型
    "model": "qwen-mt-plus",

    # 消息内容：包含需要翻译的文本
    "messages": [
        {
            "role": "user",
            "content": "我看到这个视频后没有笑"  # 待翻译的中文文本
        }
    ],

    # 开启流式输出模式（关键参数）
    "stream": True,

    # 翻译选项配置
    "translation_options": {
        "source_lang": "Chinese",   # 源语言：中文
        "target_lang": "English"    # 目标语言：英语
    }
}


# ----------------------------------------------------------------------------
#                              发送流式请求
# ----------------------------------------------------------------------------

# 发送 POST 请求，启用流式响应
response = requests.post(url, headers=headers, json=data, stream=True)


# ----------------------------------------------------------------------------
#                           处理 SSE 格式的流式响应
# ----------------------------------------------------------------------------

# 记录已输出的内容长度，用于避免重复打印
printed_len = 0

# 逐行读取响应数据
for line in response.iter_lines():
    if line:
        # 将字节流解码为字符串
        line_str = line.decode('utf-8')

        # 检查是否为 SSE 数据行（以 'data:' 开头）
        if line_str.startswith('data:'):
            # 提取 JSON 数据部分
            json_str = line_str[5:].strip()

            # 排除空数据和结束标记
            if json_str and json_str != '[DONE]':
                # 解析 JSON 数据
                chunk = json.loads(json_str)

                # 检查是否包含有效的选择项
                if 'choices' in chunk and chunk['choices']:
                    # 获取增量内容
                    delta = chunk['choices'][0].get('delta', {})
                    content = delta.get('content', '')

                    if content:
                        # 只打印新增部分，避免重复输出
                        new_content = content[printed_len:]
                        print(new_content, end='', flush=True)
                        printed_len = len(content)

# 输出完成后换行
print()
```


## 📚 术语干预 调用示例

当文本包含品牌名、产品名或专业术语时，为保证翻译的准确性和一致性，可通过 terms 字段提供一个术语表，引导模型参考术语表进行翻译。

```python
# ============================================================================
#                   Qwen-MT 机器翻译 API 调用示例（术语干预）
# ============================================================================
# 功能说明：使用通义千问机器翻译模型进行带术语干预的翻译
# 模型名称：qwen-mt-plus
# 特点：支持自定义术语表，确保专业术语翻译的一致性和准确性
# 适用场景：技术文档翻译、专业领域翻译、企业术语规范化翻译
# ============================================================================

import requests


# ----------------------------------------------------------------------------
#                              API 配置信息
# ----------------------------------------------------------------------------

# API 请求地址
url = "https://www.dmxapi.cn/v1/chat/completions"

# 请求头配置
headers = {
    # API 密钥认证（请替换为你自己的密钥）
    "Authorization": "sk-****************************************",
    "Content-Type": "application/json"  # 内容类型为 JSON
}


# ----------------------------------------------------------------------------
#                              请求参数配置
# ----------------------------------------------------------------------------

data = {
    # 指定使用的翻译模型
    "model": "qwen-mt-plus",

    # 消息内容：包含需要翻译的文本
    "messages": [
        {
            "role": "user",
            # 待翻译的中文文本（包含专业术语）
            "content": '而这套生物传感器运用了石墨烯这种新型材料，它的目标物是化学元素，敏锐的"嗅觉"让它能更深度、准确地体现身体健康状况。'
        }
    ],

    # 翻译选项配置（包含术语干预）
    "translation_options": {
        "source_lang": "Chinese",   # 源语言：中文
        "target_lang": "English",   # 目标语言：英语

        # ================================================================
        # 术语表配置（terms）
        # ================================================================
        # 作用：指定特定术语的翻译方式，确保翻译结果符合预期
        # 格式：包含 source（源术语）和 target（目标翻译）的对象数组
        # ================================================================
        "terms": [
            {
                "source": "生物传感器",           # 源术语
                "target": "biological sensor"    # 指定的英文翻译
            },
            {
                "source": "身体健康状况",                # 源术语
                "target": "health status of the body"   # 指定的英文翻译
            }
        ]
    }
}


# ----------------------------------------------------------------------------
#                              发送请求并输出结果
# ----------------------------------------------------------------------------

# 发送 POST 请求到翻译 API
response = requests.post(url, headers=headers, json=data)

# 打印返回的 JSON 结果
print(response.json())

```
## ✈️领域提示 调用示例

如果您希望翻译的风格更符合某个领域的特性，如法律、政务领域翻译用语应当严肃正式，社交领域用语应当口语化，可以通过translation_options参数传入领域提示语句。
```python
# ============================================================================
#                   Qwen-MT 机器翻译 API 调用示例（领域提示）
# ============================================================================
# 功能说明：使用通义千问机器翻译模型进行带领域提示的翻译
# 模型名称：qwen-mt-plus
# 特点：支持领域提示（Domain Prompt），引导模型按照特定领域风格进行翻译
# 适用场景：IT 技术文档、医疗文献、法律文件、金融报告等专业领域翻译
# ============================================================================

import requests


# ----------------------------------------------------------------------------
#                              API 配置信息
# ----------------------------------------------------------------------------

# API 请求地址
url = "https://www.dmxapi.cn/v1/chat/completions"

# 请求头配置
headers = {
    # API 密钥认证（请替换为你自己的密钥）
    "Authorization": "sk-****************************************",
    "Content-Type": "application/json"  # 内容类型为 JSON
}


# ----------------------------------------------------------------------------
#                              请求参数配置
# ----------------------------------------------------------------------------

data = {
    # 指定使用的翻译模型
    "model": "qwen-mt-plus",

    # 消息内容：包含需要翻译的文本
    "messages": [
        {
            "role": "user",
            # 待翻译的中文文本（IT 技术领域相关）
            "content": "第二个SELECT语句返回一个数字，表示在没有LIMIT子句的情况下，第一个SELECT语句返回了多少行。"
        }
    ],

    # 翻译选项配置（包含领域提示）
    "translation_options": {
        "source_lang": "Chinese",   # 源语言：中文
        "target_lang": "English",   # 目标语言：英语

        # ================================================================
        # 领域提示配置（domains）
        # ================================================================
        # 作用：向模型提供领域背景信息，引导其采用特定领域的翻译风格
        # 格式：字符串形式的领域描述，包含：
        #   1. 文本来源说明（如：阿里云 IT 领域）
        #   2. 内容特点描述（如：涉及软件开发和使用方法）
        #   3. 翻译注意事项（如：注意专业术语和句式）
        #   4. 目标风格要求（如：翻译成 IT 领域风格）
        # ================================================================
        "domains": "The sentence is from Ali Cloud IT domain. It mainly involves computer-related software development and usage methods, including many terms related to computer software and hardware. Pay attention to professional troubleshooting terminologies and sentence patterns when translating. Translate into this IT domain style."
    }
}


# ----------------------------------------------------------------------------
#                              发送请求并输出结果
# ----------------------------------------------------------------------------

# 发送 POST 请求到翻译 API
response = requests.post(url, headers=headers, json=data)

# 打印返回的 JSON 结果
print(response.json())

```
## 🚄 翻译记忆 调用示例
如果您希望模型参考特定的翻译风格或句式，可通过 tm_list 字段提供“源文-译文”句对作为示例。模型将在本次翻译任务中模仿这些示例的风格。
```python

# ============================================================================
#                   Qwen-MT 机器翻译 API 调用示例（翻译记忆）
# ============================================================================
# 功能说明：使用通义千问机器翻译模型进行带翻译记忆的翻译
# 模型名称：qwen-mt-plus
# 特点：支持翻译记忆库（TM），利用历史翻译提高翻译质量和一致性
# 适用场景：大型翻译项目、需要保持翻译风格一致的文档、技术手册翻译
# ============================================================================

import requests


# ----------------------------------------------------------------------------
#                              API 配置信息
# ----------------------------------------------------------------------------

# API 请求地址
url = "https://www.dmxapi.cn/v1/chat/completions"

# 请求头配置
headers = {
    # API 密钥认证（请替换为你自己的密钥）
    "Authorization": "sk-****************************************",
    "Content-Type": "application/json"  # 内容类型为 JSON
}


# ----------------------------------------------------------------------------
#                              请求参数配置
# ----------------------------------------------------------------------------

data = {
    # 指定使用的翻译模型
    "model": "qwen-mt-plus",

    # 消息内容：包含需要翻译的文本
    "messages": [
        {
            "role": "user",
            # 待翻译的中文文本
            "content": "通过如下命令可以看出安装thrift的版本信息；"
        }
    ],

    # 翻译选项配置（包含翻译记忆）
    "translation_options": {
        "source_lang": "Chinese",   # 源语言：中文
        "target_lang": "English",   # 目标语言：英语

        # ================================================================
        # 翻译记忆库配置（tm_list）
        # ================================================================
        # 作用：提供历史翻译对照，帮助模型学习翻译风格和术语用法
        # 格式：包含 source（源文本）和 target（已翻译文本）的对象数组
        # 优势：
        #   1. 提高翻译一致性
        #   2. 保持特定项目的翻译风格
        #   3. 利用已有的高质量翻译作为参考
        # ================================================================
        "tm_list": [
            {
                # 翻译记忆条目 1：关于查看版本信息的表述
                "source": "您可以通过如下方式查看集群的内核版本信息:",
                "target": "You can use one of the following methods to query the engine version of a cluster:"
            },
            {
                # 翻译记忆条目 2：关于 Thrift 环境配置的说明
                "source": "我们云HBase的thrift环境是0.9.0,所以建议客户端的版本也为 0.9.0,可以从这里下载thrift的0.9.0 版本,下载的源码包我们后面会用到,这里需要先安装thrift编译环境,对于源码安装可以参考thrift官网;",
                "target": "The version of Thrift used by ApsaraDB for HBase is 0.9.0. Therefore, we recommend that you use Thrift 0.9.0 to create a client. Click here to download Thrift 0.9.0. The downloaded source code package will be used later. You must install the Thrift compiling environment first. For more information, see Thrift official website."
            },
            {
                # 翻译记忆条目 3：关于 SDK 安装命令的说明
                "source": "您可以通过PyPI来安装SDK,安装命令如下:",
                "target": "You can run the following command in Python Package Index (PyPI) to install Elastic Container Instance SDK for Python:"
            }
        ]
    }
}


# ----------------------------------------------------------------------------
#                              发送请求并输出结果
# ----------------------------------------------------------------------------

# 发送 POST 请求到翻译 API
response = requests.post(url, headers=headers, json=data)

# 打印返回的 JSON 结果
print(response.json())
```

## ☀️**支持的语言**

| **语言**             | **英文名**             | **代码** |
| -------------------- | ---------------------- | -------- |
| 英语                 | English                | en       |
| 简体中文             | Chinese                | zh       |
| 繁体中文             | Traditional Chinese    | zh_tw    |
| 俄语                 | Russian                | ru       |
| 日语                 | Japanese               | ja       |
| 韩语                 | Korean                 | ko       |
| 西班牙语             | Spanish                | es       |
| 法语                 | French                 | fr       |
| 葡萄牙语             | Portuguese             | pt       |
| 德语                 | German                 | de       |
| 意大利语             | Italian                | it       |
| 泰语                 | Thai                   | th       |
| 越南语               | Vietnamese             | vi       |
| 印度尼西亚语         | Indonesian             | id       |
| 马来语               | Malay                  | ms       |
| 阿拉伯语             | Arabic                 | ar       |
| 印地语               | Hindi                  | hi       |
| 希伯来语             | Hebrew                 | he       |
| 缅甸语               | Burmese                | my       |
| 泰米尔语             | Tamil                  | ta       |
| 乌尔都语             | Urdu                   | ur       |
| 孟加拉语             | Bengali                | bn       |
| 波兰语               | Polish                 | pl       |
| 荷兰语               | Dutch                  | nl       |
| 罗马尼亚语           | Romanian               | ro       |
| 土耳其语             | Turkish                | tr       |
| 高棉语               | Khmer                  | km       |
| 老挝语               | Lao                    | lo       |
| 粤语                 | Cantonese              | yue      |
| 捷克语               | Czech                  | cs       |
| 希腊语               | Greek                  | el       |
| 瑞典语               | Swedish                | sv       |
| 匈牙利语             | Hungarian              | hu       |
| 丹麦语               | Danish                 | da       |
| 芬兰语               | Finnish                | fi       |
| 乌克兰语             | Ukrainian              | uk       |
| 保加利亚语           | Bulgarian              | bg       |
| 塞尔维亚语           | Serbian                | sr       |
| 泰卢固语             | Telugu                 | te       |
| 南非荷兰语           | Afrikaans              | af       |
| 亚美尼亚语           | Armenian               | hy       |
| 阿萨姆语             | Assamese               | as       |
| 阿斯图里亚斯语       | Asturian               | ast      |
| 巴斯克语             | Basque                 | eu       |
| 白俄罗斯语           | Belarusian             | be       |
| 波斯尼亚语           | Bosnian                | bs       |
| 加泰罗尼亚语         | Catalan                | ca       |
| 宿务语               | Cebuano                | ceb      |
| 克罗地亚语           | Croatian               | hr       |
| 埃及阿拉伯语         | Egyptian Arabic        | arz      |
| 爱沙尼亚语           | Estonian               | et       |
| 加利西亚语           | Galician               | gl       |
| 格鲁吉亚语           | Georgian               | ka       |
| 古吉拉特语           | Gujarati               | gu       |
| 冰岛语               | Icelandic              | is       |
| 爪哇语               | Javanese               | jv       |
| 卡纳达语             | Kannada                | kn       |
| 哈萨克语             | Kazakh                 | kk       |
| 拉脱维亚语           | Latvian                | lv       |
| 立陶宛语             | Lithuanian             | lt       |
| 卢森堡语             | Luxembourgish          | lb       |
| 马其顿语             | Macedonian             | mk       |
| 马加希语             | Maithili               | mai      |
| 马耳他语             | Maltese                | mt       |
| 马拉地语             | Marathi                | mr       |
| 美索不达米亚阿拉伯语 | Mesopotamian Arabic    | acm      |
| 摩洛哥阿拉伯语       | Moroccan Arabic        | ary      |
| 内志阿拉伯语         | Najdi Arabic           | ars      |
| 尼泊尔语             | Nepali                 | ne       |
| 北阿塞拜疆语         | North Azerbaijani      | az       |
| 北黎凡特阿拉伯语     | North Levantine Arabic | apc      |
| 北乌兹别克语         | Northern Uzbek         | uz       |
| 书面语挪威语         | Norwegian Bokmål       | nb       |
| 新挪威语             | Norwegian Nynorsk      | nn       |
| 奥克语               | Occitan                | oc       |
| 奥里亚语             | Odia                   | or       |
| 邦阿西楠语           | Pangasinan             | pag      |
| 西西里语             | Sicilian               | scn      |
| 信德语               | Sindhi                 | sd       |
| 僧伽罗语             | Sinhala                | si       |
| 斯洛伐克语           | Slovak                 | sk       |
| 斯洛文尼亚语         | Slovenian              | sl       |
| 南黎凡特阿拉伯语     | South Levantine Arabic | ajp      |
| 斯瓦希里语           | Swahili                | sw       |
| 他加禄语             | Tagalog                | tl       |
| 塔伊兹-亚丁阿拉伯语  | Ta’izzi-Adeni Arabic   | acq      |
| 托斯克阿尔巴尼亚语   | Tosk Albanian          | sq       |
| 突尼斯阿拉伯语       | Tunisian Arabic        | aeb      |
| 威尼斯语             | Venetian               | vec      |
| 瓦莱语               | Waray                  | war      |
| 威尔士语             | Welsh                  | cy       |
| 西波斯语             | Western Persian        | fa       |


## 🎩 qwen官方网站
```
https://help.aliyun.com/zh/model-studio/machine-translation

```


<p align="center">
  <small>© 2026 DMXAPI Qwen-MT系列翻译模型</small>
</p>