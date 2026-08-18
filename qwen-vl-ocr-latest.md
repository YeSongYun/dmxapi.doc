# qwen-vl-ocr-latest文字提取 API 文档

通义千问OCR 是专用于文字提取的视觉理解模型，可从各类图像（如扫描文档、表格、票据等）中提取文本或解析结构化数据，支持识别多种语言，并能通过特定任务指令实现信息抽取、表格解析、公式识别等高级功能。

## 📍 请求地址

```
https://www.dmxapi.cn/v1/chat/completions
```

## 🎯 模型名称

`qwen-vl-ocr-latest` 

## 💻 文字提取（URL） 调用示例

以下示例将从火车票图片（URL）中提取关键信息，并以 JSON 格式返回。了解如何传入本地文件和图像限制。

```python
import requests

# ===================== 配置参数 =====================
url = "https://www.dmxapi.cn/v1/chat/completions"
api_key = "sk-**********************************************"  # 替换为你的 API Key

# ===================== 请求头 =====================
headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}

# ===================== 请求体 =====================
data = {
    "model": "qwen-vl-ocr-latest",
    "messages": [
        {
            "role": "user",
            "content": [
                # 图片输入
                {
                    "type": "image_url",
                    "image_url": {"url": "https://img.alicdn.com/imgextra/i2/O1CN01ktT8451iQutqReELT_!!6000000004408-0-tps-689-487.jpg"},
                    "min_pixels": 3072,      # 最小像素
                    "max_pixels": 8388608    # 最大像素
                },
                # 提示词
                {
                    "type": "text",
                    "text": "请提取车票图像中的发票号码、车次、起始站、终点站、发车日期和时间点、座位号、席别类型、票价、身份证号码、购票人姓名。要求准确无误的提取上述关键信息、不要遗漏和捏造虚假信息，模糊或者强光遮挡的单个文字可以用英文问号?代替。返回数据格式以json方式输出，格式为：{'发票号码'：'xxx', '车次'：'xxx', '起始站'：'xxx', '终点站'：'xxx', '发车日期和时间点'：'xxx', '座位号'：'xxx', '席别类型'：'xxx','票价':'xxx', '身份证号码'：'xxx', '购票人姓名'：'xxx'}"
                }
            ]
        }
    ]
}

# ===================== 发送请求 =====================
response = requests.post(url, headers=headers, json=data)
print(response.json())
```
## 💻 文字提取（本地base64）调用示例

通义千问VL 提供两种本地文件上传方式：Base64 编码上传和文件路径直接上传。可根据文件大小、SDK类型选择上传方式，具体建议请参见如何选择文件上传方式；两种方式均需满足图像限制中对文件的要求。

```python
import requests
import base64

# ===================== 配置参数 =====================
url = "https://www.dmxapi.cn/v1/chat/completions"
api_key = "sk-***********************************************"  # 替换为你的 API Key

# ===================== 图片转 Base64 =====================
def image_to_base64(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")

image_path = "C:/Users/15664/Desktop/模型上架/a.jpg"  # 本地图片路径
image_base64 = image_to_base64(image_path)

# ===================== 请求头 =====================
headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}

# ===================== 请求体 =====================
data = {
    "model": "qwen-vl-ocr-latest",
    "messages": [
        {
            "role": "user",
            "content": [
                # 图片输入（Base64 编码）
                {
                    "type": "image_url",
                    "image_url": {"url": f"data:image/png;base64,{image_base64}"}
                },
                # 提示词
                {
                    "type": "text",
                    "text": "请提取车票图像中的发票号码、车次、起始站、终点站、发车日期和时间点、座位号、席别类型、票价、身份证号码、购票人姓名。要求准确无误的提取上述关键信息、不要遗漏和捏造虚假信息，模糊或者强光遮挡的单个文字可以用英文问号?代替。返回数据格式以json方式输出，格式为：{'发票号码'：'xxx', '车次'：'xxx', '起始站'：'xxx', '终点站'：'xxx', '发车日期和时间点'：'xxx', '座位号'：'xxx', '席别类型'：'xxx','票价':'xxx', '身份证号码'：'xxx', '购票人姓名'：'xxx'}"
                }
            ]
        }
    ]
}

# ===================== 发送请求 =====================
response = requests.post(url, headers=headers, json=data)
print(response.json())
```

## 📚 阿里官方网站
```
https://help.aliyun.com/zh/model-studio/qwen-vl-ocr#ea4e1d92dbry2
```

---

<p align="center">
  <small>© 2026 DMXAPI qwen-vl-ocr-latest 文字提取模型 </small>
</p>