# 获取所有令牌

本文档演示如何查询当前账号下已有的全部令牌详细信息，包括令牌 ID、Key、状态、额度、过期时间、IP 限制等。

## 认证参数说明

| 参数 | 说明 |
| --- | --- |
| `SYSTEM_TOKEN` | 系统令牌，获取路径： 登录DMXAPI → 工作台 → 个人设置 → 更多选项 → 系统令牌 |
| `USER_ID` | 当前用户 ID，获取路径： 登录DMXAPI → 工作台 → 个人设置 |

## 接口说明

- 请求方式：`GET`
- 请求地址：`https://www.dmxapi.cn/api/token/`
- 用途：获取当前账号下全部令牌的详细信息

## 代码示例

```python
import requests 
from datetime import datetime
SYSTEM_TOKEN = ""  # 系统令牌
USER_ID = ""  # 当前用户 ID
headers = {
    "Authorization": f"Bearer {SYSTEM_TOKEN}",
    "Rix-Api-User": USER_ID,
    "Accept": "application/json"
}

def fmt_time(ts):
    if ts == -1:
        return "永不过期"
    return datetime.fromtimestamp(ts).strftime("%Y-%m-%d %H:%M:%S")

def fmt_bool(v):
    return "是" if v else "否"

def fmt_status(v):
    return "✅ 启用" if v == 1 else "❌ 禁用"

items = []
page = 1
while page <= 100:  # 最多100页防死循环
    resp = requests.get("https://www.dmxapi.cn/api/token/", headers=headers, params={"p": page, "size": 100})
    data = resp.json()["data"]
    batch = data["items"]
    if not batch:
        print("令牌数量为 0")
        break
    items.extend(batch)
    print(f"第{page}页：获取{len(batch)}条，共{data['total']}条")
    if len(items) >= data["total"]:
        break
    page += 1

for i, token in enumerate(items, 1):
    print(f"{'='*50}")
    print(f"  令牌 {i}：{token['name']}")
    print(f"{'='*50}")
    print(f"  ID        : {token['id']}")
    print(f"  Key       : sk-{token['key']}")
    print(f"  状态      : {fmt_status(token['status'])}")
    print(f"  分组      : {token['group']}")
    print(f"  已用额度  : {token['used_quota']}")
    print(f"  剩余额度  : {'无限制' if token['unlimited_quota'] else token['remain_quota']}")
    print(f"  剩余次数  : {'无限制' if token['unlimited_count'] else token['remain_count']}")
    print(f"  创建时间  : {fmt_time(token['created_time'])}")
    print(f"  最后访问  : {fmt_time(token['accessed_time'])}")
    print(f"  过期时间  : {fmt_time(token['expired_time'])}")
    print(f"  模型限制  : {fmt_bool(token['model_limits_enabled'])}")
    print(f"  限速      : {fmt_bool(token['rate_limits_enabled'])}")
    print(f"  IP白名单  : {token['allow_ips'] or '无'}")
    print(f"  IP黑名单  : {token['exclude_ips'] or '无'}")
    print()
```

## 返回示例

```text
第1页：获取10条，共15条
第2页：获取5条，共15条
==================================================
  令牌 1：45
==================================================
  ID        : 86139
  Key       : sk-****************************
  状态      : ✅ 启用
  分组      : default
  已用额度  : 0
  剩余额度  : 无限制
  剩余次数  : 无限制
  创建时间  : 2026-06-10 18:31:24
  最后访问  : 2026-06-10 18:31:24
  过期时间  : 永不过期
  模型限制  : 否
  限速      : 否
  IP白名单  : 无
  IP黑名单  : 无

==================================================
  令牌 2：34
==================================================
  ID        : 86138
  Key       : sk-****************************
  状态      : ✅ 启用
  分组      : default
  已用额度  : 0
  剩余额度  : 无限制
  剩余次数  : 无限制
  创建时间  : 2026-06-10 18:31:21
  最后访问  : 2026-06-10 18:31:21
  过期时间  : 永不过期
  模型限制  : 否
  限速      : 否
  IP白名单  : 无
  IP黑名单  : 无

==================================================
  令牌 3：1
==================================================
  ID        : 86137
  Key       : sk-****************************
  状态      : ✅ 启用
  分组      : default
  已用额度  : 0
  剩余额度  : 无限制
  剩余次数  : 无限制
  创建时间  : 2026-06-10 18:31:16
  最后访问  : 2026-06-10 18:31:16
  过期时间  : 永不过期
  模型限制  : 否
  限速      : 否
  IP白名单  : 无
  IP黑名单  : 无

==================================================
  令牌 4：ttt
==================================================
  ID        : 74584
  Key       : sk-****************************
  状态      : ✅ 启用
  分组      : default
  已用额度  : 698180
  剩余额度  : 无限制
  剩余次数  : 无限制
  创建时间  : 2026-05-12 11:44:19
  最后访问  : 2026-06-05 23:01:21
  过期时间  : 永不过期
  模型限制  : 否
  限速      : 否
  IP白名单  : 无
  IP黑名单  : 无



==================================================
  令牌 5：222
==================================================
  ID        : 70369
  Key       : sk-****************************
  状态      : ❌ 禁用
  分组      : default
  已用额度  : 993631604
  剩余额度  : 无限制
  剩余次数  : 无限制
  创建时间  : 2026-04-30 20:06:42
  最后访问  : 2026-05-09 11:42:08
  过期时间  : 永不过期
  模型限制  : 否
  限速      : 否
  IP白名单  : 无
  IP黑名单  : 无

==================================================
  令牌 6：2333
==================================================
  ID        : 70295
  Key       : sk-****************************
  状态      : ❌ 禁用
  分组      : default
  已用额度  : 7564656
  剩余额度  : 无限制
  剩余次数  : 无限制
  创建时间  : 2026-04-30 15:50:41
  最后访问  : 2026-04-30 20:06:17
  过期时间  : 永不过期
  模型限制  : 否
  限速      : 否
  IP白名单  : 无
  IP黑名单  : 无
.
.
.

```

## 使用说明

1. 将 `SYSTEM_TOKEN` 替换为你自己的系统令牌。
2. 将 `USER_ID` 替换为实际用户 ID。
3. 执行脚本后即可查看当前账号下所有令牌的 ID 和名称。

## 注意事项

- 系统令牌和用户 ID 的获取方式请参考上方认证参数说明。
- 返回数据中的 `id` 是令牌的唯一标识，可用于后续的令牌操作（如批量删除）。
- 如果返回状态码不是 `200`，请检查系统令牌和用户 ID 是否正确。

<p align="center">
  <small>© 2026 DMXAPI 获取所有令牌</small>
</p>
