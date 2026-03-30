# 创建令牌

本文档演示如何通过 API 创建令牌，支持自定义令牌名称、额度、过期时间等参数。

## 认证参数说明

| 参数 | 说明 |
| --- | --- |
| `SYSTEM_TOKEN` | 系统令牌，获取路径： 登录DMXAPI → 工作台 → 个人设置 → 更多选项 → 系统令牌 |
| `USER_ID` | 当前用户 ID，获取路径： 登录DMXAPI → 工作台 → 个人设置 |

## 接口说明

- 请求方式：`POST`
- 请求地址：`https://www.dmxapi.cn/api/token/`
- Content-Type：`application/json`
- 用途：创建一个新的令牌

## 参数说明

| 参数 | 必填 | 说明 |
| --- | --- | --- |
| `name` | 是 | 令牌名称 |
| `quota` | 否 | 额度，填 `"无限"` 或具体金额（单位：元），例如 `1` 表示 1 元，默认为 `"无限"` |
| `count` | 否 | 次数，填 `"无限"` 或具体次数，例如 `100` 表示 100 次，默认为 `"无限"` |
| `expired_time` | 否 | 过期时间，填 `"永不过期"` 或具体日期字符串，例如 `"2026-12-31 23:59:59"`，默认为 `"永不过期"` |
| `group` | 否 | 令牌分组，目前仅支持 `"default"` |
| `model_limits_enabled` | 否 | 是否启用模型限制，`True` 或 `False`，默认为 `False` |
| `model_limits` | 否 | 允许使用的模型列表，多个用逗号分隔，例如 `"gpt-4o,claude-sonnet-4-20250514"`，仅 `model_limits_enabled` 为 `True` 时生效 |
| `allow_ips` | 否 | IP 白名单，多个用逗号分隔，例如 `"192.168.1.1,10.0.0.1"`，为空表示不限制 |
| `exclude_ips` | 否 | IP 黑名单，多个用逗号分隔，例如 `"172.16.0.1,172.16.0.2"`，为空表示不限制 |

## 代码示例

```python
import requests
import json
from datetime import datetime

SYSTEM_TOKEN = "你的系统令牌"  # 系统令牌
USER_ID = "你的用户id"  # 当前用户 ID

headers = {
    "Authorization": f"Bearer {SYSTEM_TOKEN}",
    "Rix-Api-User": USER_ID,
    "Content-Type": "application/json"
}

# ===== 只需修改这里 =====
name = "我的自定义令牌"           # 令牌名称（必填）
quota = "无限"                   # 额度：填 "无限" 或金额（元），例如 1、0.5
count = "无限"                   # 次数：填 "无限" 或具体次数，例如 100
expired_time = "永不过期"         # 过期时间：填 "永不过期" 或日期，例如 "2026-12-31 23:59:59"
group = "default"                # 令牌分组，目前仅支持 default
model_limits_enabled = False     # 是否启用模型限制，设为 True 时需配合 model_limits 使用
model_limits = ""                # 允许使用的模型，多个用逗号分隔，例如 "gpt-4o,claude-sonnet-4-20250514"
allow_ips = ""                   # IP 白名单，例如 "192.168.1.1,10.0.0.1"，为空表示不限制
exclude_ips = ""                 # IP 黑名单，例如 "172.16.0.1,172.16.0.2"，为空表示不限制
# ========================

# 以下为自动处理逻辑，无需修改
data = {
    "name": name,
    "unlimited_quota": quota == "无限",
    "remain_quota": 0 if quota == "无限" else int(float(quota) * 500000),
    "unlimited_count": count == "无限",
    "remain_count": 0 if count == "无限" else int(count),
    "expired_time": -1 if expired_time == "永不过期" else int(datetime.strptime(expired_time, "%Y-%m-%d %H:%M:%S").timestamp()),
    "group": group,
    "model_limits_enabled": model_limits_enabled,
    "model_limits": model_limits,
    "allow_ips": allow_ips,
    "exclude_ips": exclude_ips
}

resp = requests.post("https://www.dmxapi.cn/api/token/", headers=headers, json=data)
print("状态码:", resp.status_code)
print("响应:", json.dumps(resp.json(), ensure_ascii=False, indent=2))
```

## 返回示例

```json
{
  "message": "",
  "success": true
}
```

## 注意事项

- `name` 是唯一的必填参数，其他参数均有默认值。
- 额度填 `"无限"` 表示不限额度；填数字则为对应人民币金额，例如 `1` 表示 1 元。
- 次数填 `"无限"` 表示不限次数；填数字则为具体调用次数。
- 创建成功后返回的响应中不包含令牌 Key，需通过「获取所有令牌」接口查看。

<p align="center">
  <small>© 2026 DMXAPI 创建令牌</small>
</p>
