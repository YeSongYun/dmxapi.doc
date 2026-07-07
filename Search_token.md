# 搜索令牌

本文档演示如何通过关键词搜索令牌，快速找到目标令牌的详细信息。

## 认证参数说明

| 参数 | 说明 |
| --- | --- |
| `SYSTEM_TOKEN` | 系统令牌，获取路径： 登录DMXAPI → 个人设置 → 安全 → 访问令牌 |
| `USER_ID` | 当前用户 ID，获取路径： 登录DMXAPI → 个人设置 → 个人资料 |

## 接口说明

- 请求方式：`GET`
- 请求地址：`https://www.dmxapi.cn/api/token/search`
- 用途：按关键词搜索令牌，返回名称匹配的令牌列表

### 脚本过滤参数

| 参数 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `keyword` | string | 否 | 搜索关键词，**在脚本本地按令牌名称模糊匹配**（并非发送给接口的参数）。留空则返回全部令牌 |

> 后端 `/api/token/search` 接口本身只接受分页参数（`page`、`page_size`），不支持按名称模糊查询。脚本的做法是先拉取全部令牌，再在本地用 `keyword` 做名称子串过滤。

## 代码示例

```python
import requests
from datetime import datetime

# ===== 只需修改这里 =====
SYSTEM_TOKEN = "YOUR_SYSTEM_TOKEN"  # 系统令牌
USER_ID = "YOUR_USER_ID"  # 当前用户 ID
keyword = "测试"           # 搜索关键词，按令牌名称模糊匹配，留空则返回全部令牌
# ========================

# 以下为自动处理逻辑，无需修改
headers = {
    "Authorization": f"Bearer {SYSTEM_TOKEN}",
    "Dmx-Api-User": USER_ID,
    "Accept": "application/json"
}

# 后端 keyword 是精确匹配，做不到模糊查询，
# 因此拉取全部令牌后在本地按名称子串过滤
all_tokens = []
page = 1
while True:
    data = requests.get(
        "https://www.dmxapi.cn/api/token/search",
        headers=headers,
        params={"page": page, "page_size": 100},
    ).json()["data"]
    all_tokens += data["items"]
    if not data["items"] or len(data["items"]) < data["page_size"]:
        break
    page += 1

if keyword:
    tokens = [t for t in all_tokens if keyword in t["name"]]
else:
    tokens = all_tokens

def fmt_time(ts):
    if ts == -1:
        return "永不过期"
    if ts == 0:
        return "未设置"
    return datetime.fromtimestamp(ts).strftime("%Y-%m-%d %H:%M:%S")


if not tokens:
    print("未找到匹配的令牌")
else:
    print(f"共找到 {len(tokens)} 个令牌：")
    for d in tokens:
        print("=" * 40)
        print(f"  令牌名称：{d['name']}")
        print(f"  所属用户ID：{d['user_id']}")
        print(f"  状态：{'正常' if d['status'] == 1 else '已禁用'}")
        print("-" * 40)
        print(f"  已用额度：{d['used_quota'] / 500000:.4f} 元")
        print(f"  剩余额度：{'无限额度' if d['unlimited_quota'] else f'{d['remain_quota'] / 500000:.4f} 元'}")
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

### 返回示例

```text
共找到 1 个令牌：
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

## 使用说明

1. 将 `SYSTEM_TOKEN` 替换为你自己的系统令牌。
2. 将 `USER_ID` 替换为实际用户 ID。
3. 修改 `keyword` 为你要搜索的关键词，留空则返回全部令牌。

## 注意事项

- 搜索按令牌**名称**进行模糊匹配，不支持按 Key 或 ID 搜索。
- 不传 `keyword` 时返回全部令牌，与「获取所有令牌」接口效果类似。
- 接口返回的 `data` 是一个对象，包含 `items`（令牌数组）、`page_size`、`total` 等字段，结构与「获取所有令牌」一致；脚本从 `data["items"]` 取出令牌列表后再做本地过滤。

<p align="center">
  <small>© 2026 DMXAPI 搜索令牌</small>
</p>
