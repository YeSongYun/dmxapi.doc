# 获取所有令牌

本文档演示如何查询当前账号下已有的全部令牌详细信息，包括令牌 ID、Key、状态、额度、过期时间、IP 限制等。

## 认证参数说明

| 参数 | 说明 |
| --- | --- |
| `SYSTEM_TOKEN` | 系统令牌，获取路径： 登录DMXAPI → 个人设置 → 安全 → 访问令牌 |
| `USER_ID` | 当前用户 ID，获取路径： 登录DMXAPI → 个人设置 → 个人资料 |

## 接口说明

- 请求方式：`GET`
- 请求地址：`https://www.dmxapi.cn/api/token/`
- 用途：获取当前账号下全部令牌的详细信息

## 代码示例

```python
import requests
import time
from datetime import datetime
SYSTEM_TOKEN = "YOUR_SYSTEM_TOKEN"  # 系统令牌
USER_ID = "YOUR_USER_ID"  # 当前用户 ID
headers = {
    "Authorization": f"Bearer {SYSTEM_TOKEN}",
    "Dmx-Api-User": USER_ID,
    "Accept": "application/json"
}

QUOTA_PER_YUAN = 500000  # 额度换算：500000 额度 = 1 元（DMXAPI/new-api 默认单位；若与平台账单不符请调整此值）

def fmt_time(ts):
    if ts == -1:
        return "永不过期"
    return datetime.fromtimestamp(ts).strftime("%Y-%m-%d %H:%M:%S")

def fmt_money(quota):
    return f"¥{quota / QUOTA_PER_YUAN:.2f}"

def fmt_remain(token):
    if token['unlimited_quota']:
        return "无限制"
    q = token.get('remain_quota', 0)
    return f"{q}（{fmt_money(q)}）"

def fmt_bool(v):
    return "是" if v else "否"

def fmt_status(v):
    return "✅ 启用" if v == 1 else "❌ 禁用"

items = []
page = 1
while page <= 100:  # 最多100页防死循环
    resp = requests.get("https://www.dmxapi.cn/api/token/", headers=headers, params={"page": page, "page_size": 10})
    resp.raise_for_status()
    data = resp.json().get("data", {})
    batch = data.get("items", [])
    if not batch:
        if page == 1:
            print("令牌数量为 0")
        break
    items.extend(batch)
    print(f"第{page}页：获取{len(batch)}条，共{data['total']}条")
    if len(items) >= data["total"]:
        break
    time.sleep(1)  # 规避接口 IP 级限流
    page += 1

for i, token in enumerate(items, 1):
    print(f"{'='*50}")
    print(f"  令牌 {i}：{token['name']}")
    print(f"{'='*50}")
    print(f"  ID        : {token['id']}")
    print(f"  Key       : sk-{token['key']}")
    print(f"  状态      : {fmt_status(token['status'])}")
    print(f"  分组      : {token['group']}")
    print(f"  已用额度  : {token['used_quota']}（{fmt_money(token['used_quota'])}）")
    print(f"  剩余额度  : {fmt_remain(token)}")
    print(f"  剩余次数  : {'无限制' if token.get('unlimited_count') else token.get('remain_count', '—')}")
    print(f"  创建时间  : {fmt_time(token['created_time'])}")
    print(f"  最后访问  : {fmt_time(token['accessed_time'])}")
    print(f"  过期时间  : {fmt_time(token['expired_time'])}")
    print(f"  模型限制  : {fmt_bool(token['model_limits_enabled'])}")
    print(f"  限速      : {fmt_bool(token.get('rate_limits_enabled'))}")
    print(f"  IP白名单  : {token.get('allow_ips') or '无'}")
    print(f"  IP黑名单  : {token.get('exclude_ips') or '无'}")
    print()
```

## 返回示例

```text
第1页：获取1条，共1条
==================================================
  令牌 1：测试使用
==================================================
  ID        : 88129
  Key       : sk-**********
  状态      : ✅ 启用
  分组      : default
  已用额度  : 93941920（¥187.88）
  剩余额度  : 无限制
  剩余次数  : —
  创建时间  : 2026-06-17 14:55:58
  最后访问  : 2026-07-07 10:41:22
  过期时间  : 永不过期
  模型限制  : 否
  限速      : 否
  IP白名单  : 无
  IP黑名单  : 无
```

## 使用说明

1. 将 `SYSTEM_TOKEN` 替换为你自己的系统令牌。
2. 将 `USER_ID` 替换为实际用户 ID。
3. 执行脚本后即可查看当前账号下所有令牌的完整详情（ID、Key、状态、额度、过期时间、IP 限制等）。

## 注意事项

- 系统令牌和用户 ID 的获取方式请参考上方认证参数说明。
- 返回数据中的 `id` 是令牌的唯一标识，可用于后续的令牌操作（如批量删除）。
- 如果返回状态码不是 `200`，请检查系统令牌和用户 ID 是否正确。

<p align="center">
  <small>© 2026 DMXAPI 获取所有令牌</small>
</p>
