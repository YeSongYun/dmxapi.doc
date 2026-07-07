# 更新令牌

本文档演示如何先查询当前账号下已有的令牌，再根据令牌 ID 更新指定令牌的信息。

## 认证参数说明

| 参数 | 说明 |
| --- | --- |
| `SYSTEM_TOKEN` | 系统令牌，获取路径： 登录DMXAPI → 个人设置 → 安全 → 访问令牌 |
| `USER_ID` | 当前用户 ID，获取路径： 登录DMXAPI → 个人设置 → 个人资料 |

## 接口说明

### 1. 查询令牌列表

- 请求方式：`GET`
- 请求地址：`https://www.dmxapi.cn/api/token/`
- 用途：获取当前账号下全部令牌，找到要更新的令牌 ID

### 2. 查询单个令牌

- 请求方式：`GET`
- 请求地址：`https://www.dmxapi.cn/api/token/{token_id}`
- 用途：按令牌 ID 查询单条令牌的当前完整数据（更新前先拉取，用于合并字段避免误覆盖）

### 3. 更新令牌

- 请求方式：`PUT`
- 请求地址：`https://www.dmxapi.cn/api/token/`
- Content-Type：`application/json`
- 用途：根据令牌 ID 更新指定令牌的信息

::: warning 注意
此接口为**全量更新**，未传的字段会被重置为默认值。代码示例中已自动处理：先查询当前令牌数据，再合并你的修改，避免误覆盖。
:::

## 可修改参数说明

| 参数 | 说明 |
| --- | --- |
| `name` | 令牌名称 |
| `quota` | 额度：填 `"无限"` 或金额（单位：元），例如 `1` 表示 1 元 |
| `expired_time` | 过期时间：填 `"永不过期"` 或日期，例如 `"2026-12-31 23:59:59"` |
| `group` | 令牌分组，目前仅支持 `"default"` |
| `model_limits_enabled` | 是否启用模型限制，`True` 或 `False` |
| `model_limits` | 允许使用的模型，多个用逗号分隔，例如 `"gpt-4o,claude-sonnet-4-20250514"` |
| `allow_ips` | IP 白名单，多个用逗号分隔，例如 `"192.168.1.1,10.0.0.1"`，为空表示不限制 |
| `exclude_ips` | IP 黑名单，多个用逗号分隔，例如 `"172.16.0.1,172.16.0.2"`，为空表示不限制 |

## 一、查询当前有哪些令牌

```python
import requests

SYSTEM_TOKEN = "YOUR_SYSTEM_TOKEN"  # 系统令牌
USER_ID = "YOUR_USER_ID"  # 当前用户 ID

headers = {
    "Authorization": f"Bearer {SYSTEM_TOKEN}",
    "Dmx-Api-User": USER_ID,
    "Accept": "application/json"
}

resp = requests.get("https://www.dmxapi.cn/api/token/", headers=headers)
items = resp.json()["data"]["items"]

for token in items:
    print(f"ID: {token['id']}  名称: {token['name']}")
```

### 返回示例

```text
ID: 93103  名称: 测试令牌
ID: 88129  名称: 测试使用
```

## 二、根据令牌 ID 更新指定令牌

先查询令牌列表，确认要更新的令牌 ID，再将 ID 填入下方脚本，修改你需要变更的参数。

```python
import requests
import json
from datetime import datetime

SYSTEM_TOKEN = "YOUR_SYSTEM_TOKEN"  # 系统令牌
USER_ID = "YOUR_USER_ID"  # 当前用户 ID

headers = {
    "Authorization": f"Bearer {SYSTEM_TOKEN}",
    "Dmx-Api-User": USER_ID,
    "Content-Type": "application/json"
}

# ===== 只需修改这里 =====
token_id = 93103                     # 要更新的令牌 ID（从第一步查询结果中获取）
name = "我的新名称"                   # 令牌名称
quota = "无限"                       # 额度：填 "无限" 或金额（元），例如 1、0.5
expired_time = "永不过期"             # 过期时间：填 "永不过期" 或日期，例如 "2026-12-31 23:59:59"
group = "default"                    # 令牌分组，目前仅支持 default
model_limits_enabled = False         # 是否启用模型限制，设为 True 时需配合 model_limits 使用
model_limits = ""                    # 允许使用的模型，多个用逗号分隔，例如 "gpt-4o,claude-sonnet-4-20250514"
allow_ips = ""                       # IP 白名单，例如 "192.168.1.1,10.0.0.1"，为空表示不限制
exclude_ips = ""                     # IP 黑名单，例如 "172.16.0.1,172.16.0.2"，为空表示不限制
# ========================

# 以下为自动处理逻辑，无需修改

# 先查询当前令牌数据，防止全量更新覆盖未修改的字段
resp = requests.get(f"https://www.dmxapi.cn/api/token/{token_id}", headers=headers)
current = resp.json()["data"]

# 合并修改
current["name"] = name
current["unlimited_quota"] = (quota == "无限")
current["remain_quota"] = current["remain_quota"] if quota == "无限" else int(float(quota) * 500000)
current["expired_time"] = -1 if expired_time == "永不过期" else int(datetime.strptime(expired_time, "%Y-%m-%d %H:%M:%S").timestamp())
current["group"] = group
current["model_limits_enabled"] = model_limits_enabled
current["model_limits"] = model_limits
current["allow_ips"] = allow_ips
current["exclude_ips"] = exclude_ips

# 提交更新
resp = requests.put("https://www.dmxapi.cn/api/token/", headers=headers, json=current)
print("状态码:", resp.status_code)
print("响应:", json.dumps(resp.json(), ensure_ascii=False, indent=2))
```

### 返回示例

```json
状态码: 200
响应: {
  "data": {
    "id": 93103,
    "user_id": 10000,
    "key": "sk-**********",
    "status": 1,
    "name": "我的新名称",
    "created_time": 1783398902,
    "accessed_time": 1783398902,
    "expired_time": -1,
    "remain_quota": 2500000,
    "unlimited_quota": true,
    "model_limits_enabled": false,
    "model_limits": "",
    "allow_ips": "",
    "used_quota": 0,
    "group": "default",
    "cross_group_retry": false,
    "DeletedAt": null
  },
  "message": "",
  "success": true
}
```

## 注意事项

- 先执行第一步查询令牌列表，确认要更新的令牌 ID。
- 此接口为**全量更新**，第二步代码会自动查询该令牌的当前数据并合并你的修改，避免未修改的字段被重置。
- 额度填 `"无限"` 会保持无限额度；填数字则为对应人民币金额，例如 `1` 表示 1 元。
- 更新成功后响应中会返回更新后的完整令牌数据。

<p align="center">
  <small>© 2026 DMXAPI 更新令牌</small>
</p>
