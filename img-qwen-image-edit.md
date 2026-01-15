# 千问图片编辑 qwen-image-edit 接口API文档

## 模型名称
`qwen-image-edit`

## 接口地址
`https://www.DMXAPI.cn/v1/images/edits`


## 请求参数 (multipart/form-data)
| 参数名 | 类型 | 必需 | 说明 | 示例值 |
|--------|------|------|------|--------|
| image | file | 是 | 要编辑的图像文件，<4MB | - |
| prompt | string | 是 | 图像编辑的文本描述(最大1000字符) | A cute baby sea otter wearing a beret. |
| n | integer | 否 | 生成图像数量(1-10) | 2 |
| size | string | 否 | 输出图像尺寸| 1024x1024 |
| response_format | string | 否 | 响应格式(url 或 b64_json) | url |
| user | string | 否 | 用户标识符(用于滥用检测) | user-123 |
| model | string | 是 | 使用的AI模型 | qwen-image |

## Python调用示例
```python
import requests  # 导入 requests 库

# API 端点，用于图像编辑和操作
url = "https://www.DMXAPI.cn/v1/images/edits"
api_key ="sk-**********************************"  # 替换为你的 DMXAPI 令牌

headers = {
    "Authorization": f"{api_key}"  # 使用你的 API 密钥进行认证
}

# 请求参数，包含编辑的提示词
payload = {
    "model": "qwen-image-edit",  # 使用的模型名称
    "prompt": "给哪吒带上一个粉色的鸭舌帽，风格保持不变",  # 描述对上传图片的编辑要求
    "size": "1024x1024" # 可选参数，指定输出尺寸。注意：编辑通常保持原图比例，指定尺寸可能导致裁剪或缩放
}

# 需要编辑的图片文件，以 multipart/form-data 格式发送
files = [
    (
        "image",  # 参数名称必须是 "image"
        (
            "nezha1.png",  # 文件名
            open(
                "c:\\nezha1.png",  # <-- 请替换为你的图片文件完整路径
                "rb",  # 以二进制只读模式打开文件
            ),
            "image/png",  # 文件的 MIME 类型 (image/png, image/jpeg 等)
        ),
    )
]

# 发送 POST 请求
# requests 库会自动处理 multipart/form-data 的编码
response = requests.post(url, headers=headers, data=payload, files=files)

# 解析 JSON 响应
response_data = response.json()  # requests 库可以直接解析 JSON
print("响应数据:", response_data)  # 打印完整的响应数据以便调试

```


## 返回示例
```JSON
{
  'data': [
    {
      'url': 'https://........................'  # 生成的图片结果 URL
    }],
  'created': 1758427937,
  'extra': {
    'output': {
      'choices': [
        {
          'finish_reason': 'stop',
          'message': {
            'content': [
              {
                'image': 'https://............'  # 生成的图片结果 URL
              }],
            'role': 'assistant'
          }
        }]
    },
    'request_id': '33f9ea95-d509-4260-8352-0bc43cd68cef',
    'usage': {
      'height': 1024,
      'image_count': 1,
      'width': 1024
    }
  }
}

```

<p align="center">
  <small>© 2025 DMXAPI 千问图片编辑 q...</small>
</p>