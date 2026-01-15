# 阿里 qwen-image 文生图 API接口文档

## 模型名称
`qwen-image`

## POST请求调用方法

### 接口地址
```
POST https://www.dmxapi.cn/v1/images/generations
```

### 请求头
```
Authorization: YOUR_API_KEY
Content-Type: application/json
```

### 请求参数
| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| model | string | 是 | 模型名称，固定值：`qwen-image` |
| prompt | string | 是 | 图像生成的提示词描述 |
| size | string | 否 | 图片尺寸，格式为"宽*高"，默认："1024*1024" |
| n | integer | 否 | 生成图片数量，默认：1（建议保持为1） |
| response_format | string | 否 | 返回格式，可选："url"或"base64"，默认："url" |

### 请求示例
```bash
curl -X POST "https://www.dmxapi.cn/v1/images/generations" \
  -H "Authorization: YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "qwen-image",
    "prompt": "真实科技感海报设计:DMXAPI",
    "size": "1328*1328",
    "n": 1,
    "response_format": "url"
  }'
```

### Python调用示例
```python
# 导入所需的库
import json  # 用于处理JSON数据
import requests  # 用于发送HTTP请求

# DMXAPI图像生成接口的URL
url = "https://www.dmxapi.cn/v1/images/generations"

# 构建请求参数
payload = json.dumps(
    {
        "model": "qwen-image",  # 使用的AI模型名称
        "prompt": "真实科技感海报设计:DMXAPI",  # 图像生成的提示词
        "size": "1328*1328",  # 图片尺寸，格式为宽*高
        "n": 1,  # 生成图片的数量（注意：修改此值可能会导致错误）
        "response_format": "url",  # 返回格式：可选择"url"或"base64"
    }
)

# 设置请求头
headers = {
    "Authorization": "sk-ucCvUA7AlSmTDqDt0ne2l8lnyHDPTepWnHUvt5XTNpGWbSyt",  # DMXAPI的API密钥
    "Content-Type": "application/json",  # 指定请求内容类型为JSON
}

# 发送POST请求到DMXAPI
response = requests.request("POST", url, headers=headers, data=payload)

# 处理API响应，将URL中的转义字符\u0026替换为正常的&符号
response_text = response.text.replace("\\u0026", "&")

# 打印处理后的响应结果
print(response_text)



```

<p align="center">
  <small>© 2025 DMXAPI 阿里 qwen-...</small>
</p>