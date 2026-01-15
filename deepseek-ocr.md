# DeepSeek OCR API 使用文档

DeepSeek-OCR 是一个强大的图像文字识别接口，能够精准识别图片中的文字内容，支持多种场景下的 OCR 处理。

## 模型名称

| 模型 | 说明 |
|------|------|
| `DeepSeek-OCR` | 标准版 OCR 模型 |

## 接口地址

```
https://www.dmxapi.cn/v1
```

## 支持的 Prompt 模板

| 场景 | Prompt 模板 |
|------|-------------|
| 无布局识别 | `<image>\nFree OCR.` |
| 文档转换 | `<image>\n<\|grounding\|>Convert the document to markdown.` |
| 普通图片 | `<image>\n<\|grounding\|>OCR this image.` |
| 文档中的图表 | `<image>\nParse the figure.` |
| 详细描述 | `<image>\nDescribe this image in detail.` |
| 定位识别 | `<image>\nLocate <\|ref\|>xxxx<\|/ref\|> in the image.` |

## 示例代码
```python
"""
DeepSeek OCR API 调用示例
使用 OpenAI Python SDK 兼容接口进行图像识别和 OCR 处理
安装依赖：pip install openai
"""

from openai import OpenAI

# ==================== 客户端初始化 ====================
# 配置 API 密钥和服务端点
client = OpenAI(
    api_key="sk-************************************************",  # 您的 API 密钥
    base_url="https://www.dmxapi.cn/v1"                              # API 服务地址
)

# ==================== 调用 OCR 接口 ====================
# 使用 DeepSeek-OCR 模型进行图像识别
response = client.chat.completions.create(
    model="DeepSeek-OCR",
    messages=[
        {
            "role": "system",
            "content": "<image>\nFree OCR."

            # 【不同场景的 Prompt 模板】
            # ┌─────────────────────────────────────────────────────────────────┐
            # │ 文档转换：<image>\n<|grounding|>Convert the document to markdown. │
            # │ 普通图片：<image>\n<|grounding|>OCR this image.                   │
            # │ 无布局识别：<image>\nFree OCR.                                     │
            # │ 文档中的图表：<image>\nParse the figure.                           │
            # │ 详细描述：<image>\nDescribe this image in detail.                 │
            # │ 定位识别：<image>\nLocate <|ref|>xxxx<|/ref|> in the image.      │
            # └─────────────────────────────────────────────────────────────────┘
        },
        {
            "role": "user",
            "content": [
                {
                    "type": "image_url",
                    "image_url": {
                        "url": "https://doc.dmxapi.cn/0_fenxiang/OCR_sample_file.jpg"
                    }
                }
            ]
        }
    ]
)

# ==================== 输出识别结果 ====================
print(response.choices[0].message.content)

```

## 返回示例


```json
<|ref|>text<|/ref|><|det|>[[90, 22, 185, 35]]<|/det|>
18:51

<|ref|>image<|/ref|><|det|>[[620, 20, 655, 35]]<|/det|>

<|ref|>image<|/ref|><|det|>[[661, 20, 701, 36]]<|/det|>

<|ref|>image<|/ref|><|det|>[[707, 20, 747, 36]]<|/det|>

<|ref|>image<|/ref|><|det|>[[755, 20, 804, 36]]<|/det|>

<|ref|>image<|/ref|><|det|>[[808, 20, 860, 36]]<|/det|>

<|ref|>image<|/ref|><|det|>[[869, 21, 939, 36]]<|/det|>

<|ref|>image<|/ref|><|det|>[[620, 22, 656, 36]]<|/det|>

<|ref|>image<|/ref|><|det|>[[771, 67, 828, 94]]<|/det|>

<|ref|>image<|/ref|><|det|>[[860, 67, 915, 94]]<|/det|>

<|ref|>image<|/ref|><|det|>[[634, 77, 678, 101]]<|/det|>

<|ref|>image<|/ref|><|det|>[[888, 130, 937, 152]]<|/det|>

<|ref|>text<|/ref|><|det|>[[57, 125, 692, 153]]<|/det|>
**打火机（哈基米南北绿豆）**

<|ref|>text<|/ref|><|det|>[[903, 135, 937, 147]]<|/det|>
1k+

<|ref|>text<|/ref|><|det|>[[57, 170, 380, 186]]<|/det|>
Sixteen 制作团队＞

<|ref|>title<|/ref|><|det|>[[57, 225, 567, 255]]<|/det|>
# 哈基米啊南北绿豆

<|ref|>text<|/ref|><|det|>[[55, 293, 306, 315]]<|/det|>
哈呀库奶露

<|ref|>text<|/ref|><|det|>[[55, 351, 450, 374]]<|/det|>
南北绿豆哈吉嘎西

<|ref|>text<|/ref|><|det|>[[55, 411, 404, 434]]<|/det|>
椰打耶南北绿豆

<|ref|>text<|/ref|><|det|>[[55, 470, 450, 493]]<|/det|>
哦嘛自立曼波哈吉

<|ref|>image<|/ref|><|det|>[[810, 520, 845, 535]]<|/det|>

<|ref|>text<|/ref|><|det|>[[55, 530, 306, 553]]<|/det|>
南北绿了豆

<|ref|>text<|/ref|><|det|>[[55, 590, 500, 612]]<|/det|>
啊西噶南北绿豆耶打

<|ref|>text<|/ref|><|det|>[[55, 650, 306, 672]]<|/det|>
曼波哈基米

<|ref|>text<|/ref|><|det|>[[55, 709, 450, 732]]<|/det|>
哈基米啊南北绿豆

<|ref|>text<|/ref|><|det|>[[55, 769, 306, 791]]<|/det|>
哈呀库奶露

<|ref|>text<|/ref|><|det|>[[57, 828, 450, 850]]<|/det|>
南北绿豆哈吉嘎西

<|ref|>image<|/ref|><|det|>[[57, 928, 125, 958]]<|/det|>

<|ref|>text<|/ref|><|det|>[[128, 934, 180, 945]]<|/det|>
138人

<|ref|>image<|/ref|><|det|>[[228, 930, 280, 958]]<|/det|>

<|ref|>text<|/ref|><|det|>[[228, 942, 260, 955]]<|/det|>
伴

<|ref|>image<|/ref|><|det|>[[385, 933, 444, 962]]<|/det|>

<|ref|>image<|/ref|><|det|>[[544, 933, 603, 962]]<|/det|>

<|ref|>image<|/ref|><|det|>[[798, 920, 884, 970]]<|/det|>

<|ref|>text<|/ref|><|det|>[[128, 949, 160, 960]]<|/det|>
off

<|ref|>text<|/ref|><|det|>[[128, 958, 160, 970]]<|/det|>
词
```

---

<p align="center">
  © 2025 DMXAPI · DeepSeek-OCR
</p>