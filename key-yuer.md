# DMXAPI 令牌余额查询接口

## 接口地址
`https://www.dmxapi.cn/api/token/key/sk-**********************`

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
    "Rix-Api-User": "23201",  # 更改为你的用户ID，在 个人设置 中获得
}
response = requests.request("GET", url, headers=headers)
result = response.json()

if not result.get("success"):
    print("请求失败:", result.get("message"))
    exit()

d = result["data"]

def fmt_quota(q, unlimited):
    if unlimited:
        return "无限额度"
    return f"{q}  →  {q / 500000:.4f} 元"

def fmt_time(ts):
    if ts == -1:
        return "永不过期"
    import datetime
    return datetime.datetime.fromtimestamp(ts).strftime("%Y-%m-%d %H:%M:%S")

def fmt_status(s):
    return "正常" if s == 1 else "已禁用"

print("=" * 40)
print(f"  令牌名称：{d['name']}")
print(f"  所属用户ID：{d['user_id']}")
print(f"  状态：{fmt_status(d['status'])}")
print("-" * 40)
print(f"  已用额度：{d['used_quota'] / 500000:.4f} 元")
print(f"  剩余额度：{fmt_quota(d['remain_quota'], d['unlimited_quota'])}")
print(f"  剩余次数：{'无限次数' if d['unlimited_count'] else d['remain_count']}")
print("-" * 40)
print(f"  分组：{d['group']}")
print(f"  创建时间：{fmt_time(d['created_time'])}")
print(f"  最后访问：{fmt_time(d['accessed_time'])}")
print(f"  过期时间：{fmt_time(d['expired_time'])}")
print("-" * 40)
print(f"  模型限制：{'已启用' if d['model_limits_enabled'] else '未启用'}")
print(f"  IP白名单：{d['allow_ips'] or '无'}")
print(f"  IP黑名单：{d['exclude_ips'] or '无'}")
print("=" * 40)
```

## 返回示例
```json
========================================
  令牌名称：new_key
  所属用户ID：23201
  状态：正常
----------------------------------------
  已用额度：1767.1495 元
  剩余额度：无限额度
  剩余次数：无限次数
----------------------------------------
  分组：default
  创建时间：2026-02-09 11:36:56
  最后访问：2026-03-18 12:12:02
  过期时间：永不过期
----------------------------------------
  模型限制：未启用
  IP白名单：无
  IP黑名单：无
========================================

```

<p align="center">
  <small>© 2026 DMXAPI DMXAPI 令...</small>
</p>