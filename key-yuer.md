# DMXAPI 令牌余额查询接口

## 接口地址
`GET https://www.dmxapi.cn/api/token/search`

> DMXAPI 接口不支持按 key 直接查询令牌详情。本脚本改为调用令牌搜索接口分页拉取令牌列表，再在本地用「前 4 位 + 10 个星号 + 后 4 位」的脱敏格式与目标 key 精确匹配，从而定位到对应令牌。

## 准备需要查询的令牌
获取路径： 登录DMXAPI → 工作台 → 令牌 → 复制目标令牌贴到下面代码里

## 示例代码
```python
import requests
from datetime import datetime

# ----------- 1. 请求参数（自行替换 ↓）-----------
API_KEY = "sk-YOUR_API_KEY"  # 要查询的 DMXAPI 令牌
SYSTEM_TOKEN = "YOUR_SYSTEM_TOKEN"  # 系统令牌（按 key 查询令牌详情需要管理员权限）
USER_ID = "YOUR_USER_ID"  # 你的用户ID，在 个人设置 中获得
BASE_URL = "https://www.dmxapi.cn"
# ------------------------------------------------

headers = {
    "Authorization": f"Bearer {SYSTEM_TOKEN}",
    "Dmx-Api-User": USER_ID,
    "Accept": "application/json",
}

# ----------- 2. 按 key 定位令牌 -----------
# 接口不支持按 key 直接查询，因此遍历令牌列表，用「前4位 + 后4位」匹配脱敏后的 key
raw_key = API_KEY[3:] if API_KEY.startswith("sk-") else API_KEY
# 接口只返回脱敏后的 key（前4位 + 10个星号 + 后4位），无法拿到完整 key，
# 因此把完整 key 转成同样的脱敏格式后做精确匹配
masked_key = f"{raw_key[:4]}{'*' * 10}{raw_key[-4:]}"

token = None
page = 1
while token is None:
    data = requests.get(
        f"{BASE_URL}/api/token/search",
        headers=headers,
        params={"page": page, "page_size": 100},
    ).json()["data"]
    for item in data["items"]:
        if item["key"] == masked_key:
            token = item
            break
    if not data["items"] or len(data["items"]) < data["page_size"]:
        break
    page += 1

if token is None:
    print("未找到该令牌，请检查 API_KEY 是否正确")
    exit()

d = token


# ----------- 3. 格式化输出 -----------
def fmt_quota(q, unlimited):
    return "无限额度" if unlimited else f"{q / 500000:.4f} 元"


def fmt_time(ts):
    if ts == -1:
        return "永不过期"
    if ts == 0:
        return "未设置"
    return datetime.fromtimestamp(ts).strftime("%Y-%m-%d %H:%M:%S")


print("=" * 40)
print(f"  令牌名称：{d['name']}")
print(f"  所属用户ID：{d['user_id']}")
print(f"  状态：{'正常' if d['status'] == 1 else '已禁用'}")
print("-" * 40)
print(f"  已用额度：{d['used_quota'] / 500000:.4f} 元")
print(f"  剩余额度：{fmt_quota(d['remain_quota'], d['unlimited_quota'])}")
print(f"  剩余次数：无限次数")  # 该接口无次数限制概念，固定显示
print("-" * 40)
print(f"  分组：{d['group']}")
print(f"  创建时间：{fmt_time(d['created_time'])}")
print(f"  最后访问：{fmt_time(d['accessed_time'])}")
print(f"  过期时间：{fmt_time(d['expired_time'])}")
print("-" * 40)
print(f"  模型限制：{d['model_limits'] if d['model_limits_enabled'] else '未启用'}")
print(f"  IP白名单：{d['allow_ips'] or '无'}")
print(f"  IP黑名单：无")  # 该接口无 IP 黑名单字段，固定显示
print("=" * 40)

```

## 返回示例
```text
========================================
  令牌名称：测试使用
  所属用户ID：10000
  状态：正常
----------------------------------------
  已用额度：187.8838 元
  剩余额度：无限额度
  剩余次数：无限次数
----------------------------------------
  分组：default
  创建时间：2026-06-17 14:55:58
  最后访问：2026-07-07 10:41:22
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