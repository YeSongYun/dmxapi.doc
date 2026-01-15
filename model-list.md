# DMXAPI 模型信息接口

## 接口地址
`GET https://www.dmxapi.cn/v1/models`  
获取模型列表及倍率信息。

## 请求示例
```python

import requests

# ----------- 1. 请求参数（自行替换 ↓） -----------
url = "https://www.dmxapi.cn/v1/models"
api_token = (
    "sk-****************************"  # 替换为你的 API令牌，注意不是系统令牌
)

headers = {
    "Authorization": f"{api_token}",
    "Accept": "application/json",
    "Rix-Api-User": "你的用户ID号",  # 填上你的用户ID序号，在个人设置页面获取。
}

# ----------- 2. 发送请求 -----------
resp = requests.get(url, headers=headers, timeout=10)
print("请求成功，响应内容：", resp.text)


```

<p align="center">
  <small>© 2025 DMXAPI DMXAPI 模...</small>
</p>