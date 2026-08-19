# DMXAPI 模型列表查询接口
获取模型列表。
## 接口地址
`GET https://www.dmxapi.cn/v1/models`  


## 请求示例
```python

import requests

# ----------- 1. 请求参数（自行替换 ↓） -----------
API_KEY = "sk-请在这里填写 DMXAPI 令牌"  # 模型调用令牌，不是系统访问令牌
BASE_URL = "https://www.dmxapi.cn"  # 平台根地址

headers = {
    "Authorization": API_KEY,
    "Accept": "application/json",
}

# ----------- 2. 发送请求 -----------
response = requests.get(f"{BASE_URL}/v1/models", headers=headers, timeout=10)
print("请求成功，响应内容：", response.text)


```

<p align="center">
  <small>© 2026 DMXAPI 模型信息接口</small>
</p>
