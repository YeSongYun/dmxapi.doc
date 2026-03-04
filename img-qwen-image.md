# 阿里 qwen-image 文生图 API接口文档



## 接口地址
```
https://www.dmxapi.cn/v1/images/generations
```

## 模型名称
`qwen-image`

## 示例代码
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
    "Authorization": "sk-rOQH5ITfGkp9pbvnIIbcQyPRCQclFUl8bSjD3dFRPeuDUQHl",  # DMXAPI的API密钥
    "Content-Type": "application/json",  # 指定请求内容类型为JSON
}

# 发送POST请求到DMXAPI
response = requests.request("POST", url, headers=headers, data=payload)

result = response.json()
output = result.get("extra", {}).get("output", {})
results = output.get("results", [{}])

print(f"任务状态: {output.get('task_status')}")
print(f"任务ID:   {output.get('task_id')}")
print(f"提交时间: {output.get('submit_time')}")
print(f"完成时间: {output.get('end_time')}")
print(f"消耗图片: {result.get('extra', {}).get('usage', {}).get('image_count')} 张")
print()
for i, r in enumerate(results, 1):
    print(f"[图片 {i}]")
    print(f"  原始提示词: {r.get('orig_prompt')}")
    print(f"  图片URL:    {r.get('url')}")
```
## 返回示例
```json
任务状态: SUCCEEDED
任务ID:   9bd6681c-7f3f-4c86-80ef-e7f9d8fe2663
提交时间: 2026-03-03 20:36:37.606
完成时间: 2026-03-03 20:36:46.006
消耗图片: 1 张

[图片 1]
  原始提示词: 真实科技感海报设计:DMXAPI
  图片URL:    https://dashscope-result-wlcb-acdr-1.oss-cn-wulanchabu-acdr-1.aliyuncs.com/7d/44/20260303/cfc32567/9bd6681c-7f3f-4c86-80ef-e7f9d8fe2663584158063.png?Expires=1773147205&OSSAccessKeyId=LTAI5tKPD3TMqf2Lna1fASuh&Signature=DYQrfXWIMieo3knj8ccGtzIelEU%3D
```


<p align="center">
  <small>© 2025 DMXAPI 阿里 qwen-...</small>
</p>