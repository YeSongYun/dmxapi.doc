# DMXAPI 令牌余额查询接口

## 接口地址
`GET https://www.dmxapi.cn/api/token/key/sk-**********************`

## 准备需要查询的令牌
获取路径： 登录DMXAPI → 工作台 → 令牌 → 复制目标令牌贴到下面代码里

## 请求示例
```python
import requests

# ----------- 1. 请求参数（自行替换 ↓）-----------
API_KEY = "sk-**********************" # 换成你的 DMXAPI 令牌

url = f"https://www.dmxapi.cn/api/token/key/{API_KEY}"

headers = {
    "Accept": "application/json",
    "Rix-Api-User": "你的用户ID",  # 刚改为你的用户ID，在 个人设置 中获得
}

response = requests.request("GET", url, headers=headers)

print(response.text)

```

## 响应说明
- `used_quota`: 令牌已用额度（整数）
- `remain_quota`:令牌剩余额度（整数）
- 实际人民币余额 = 对应quota / 500000

<p align="center">
  <small>© 2025 DMXAPI DMXAPI 令...</small>
</p>