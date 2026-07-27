# DMXAPI 用户信息接口

## 接口地址
`GET https://www.dmxapi.cn/api/user/self`

## 认证方式
需要在请求头中同时携带系统访问令牌和用户 ID。两项必须属于同一个账号。

- 系统访问令牌：个人设置 → 安全 → 访问令牌
- 用户 ID：个人设置 → 个人资料

## 请求示例

```python
import requests

# 填写与同一账号对应的认证信息
SYSTEM_TOKEN = "请在这里填写系统访问令牌"  # 调用平台管理接口的凭据
USER_ID = "请在这里填写用户 ID"  # 要查询余额的用户 ID
BASE_URL = "https://www.dmxapi.cn"  # 平台根地址
QUOTA_PER_CNY = 500_000  # 500000 原始额度等于 1 CNY

headers = {
    "Authorization": f"Bearer {SYSTEM_TOKEN}",  # Bearer 后携带系统访问令牌
    "Dmx-Api-User": USER_ID,  # 指定要查询的用户
}

response = requests.get(
    f"{BASE_URL}/api/user/self",  # 当前用户信息接口
    headers=headers,
    timeout=30,  # 单次请求最多等待 30 秒
)
response.raise_for_status()
result = response.json()
if not result.get("success"):
    raise RuntimeError(result.get("message") or "获取用户信息失败")

quota = result["data"]["quota"]  # 账户原始额度；500000 等于 1 CNY
print(f"账户额度: {quota:,}")
print(f"人民币余额: ￥{quota / QUOTA_PER_CNY:.6f}")
```

## 响应说明

- `quota`: 账户额度（整数）
- 实际人民币余额 = `quota / 500000`

<p align="center">
  <small>© 2026 DMXAPI 用户信息接口</small>
</p>
