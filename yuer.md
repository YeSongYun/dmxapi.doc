# DMXAPI 余额查询接口

该接口用来查询用户的余额。

## 📌 接口地址

```
https://www.dmxapi.cn/api/user/self
```

## 请求示例

```python
import requests

# 填写与同一账号对应的认证信息
SYSTEM_TOKEN = "请在这里填写系统访问令牌"
USER_ID = "请在这里填写用户 ID"
BASE_URL = "https://www.dmxapi.cn"

headers = {
    "Authorization": f"Bearer {SYSTEM_TOKEN}",
    "Dmx-Api-User": USER_ID,
}

response = requests.get(
    f"{BASE_URL}/api/user/self",
    headers=headers,
    timeout=30,
)
response.raise_for_status()
result = response.json()
if not result.get("success"):
    raise RuntimeError(result.get("message") or "获取用户信息失败")

quota = result["data"]["quota"]
print(f"人民币余额: ￥{quota / 500000:.6f}")
```

## 响应说明

- 实际人民币余额 = `quota / 500000`

<p align="center">
  <small>© 2026 DMXAPI 余额查询接口</small>
</p>
