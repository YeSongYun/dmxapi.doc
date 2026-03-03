# DMXAPI 令牌余额查询接口

## 接口地址
`GET https://www.dmxapi.cn/api/token/key/sk-**********************`

## 准备需要查询的令牌
获取路径： 登录DMXAPI → 工作台 → 令牌 → 复制目标令牌贴到下面代码里

## 示例代码
```python
import requests
import json
# ----------- 1. 请求参数（自行替换 ↓）-----------
API_KEY = "sk-****************************************" # 换成你的 DMXAPI 令牌
url = f"https://www.dmxapi.cn/api/token/key/{API_KEY}"
headers = {
    "Accept": "application/json",
    "Rix-Api-User": "23201",  # 刚改为你的用户ID，在 个人设置 中获得
}
response = requests.request("GET", url, headers=headers)
data = response.json().get("data", {})
used_quota = data.get("used_quota", 0)
remain_quota = data.get("remain_quota", 0)
def fmt_quota(q):
    if q < 0:
        return "无限额度"
    return f"{q}  →  {q / 500000:.4f} 元"

print(f"已用额度: {fmt_quota(used_quota)}")
print(f"剩余额度: {fmt_quota(remain_quota)}")
```

## 返回示例
- `used_quota`: 令牌已用额度（整数）
- `remain_quota`:令牌剩余额度（整数）
- 实际人民币余额 = 对应quota / 500000

<p align="center">
  <small>© 2025 DMXAPI DMXAPI 令...</small>
</p>