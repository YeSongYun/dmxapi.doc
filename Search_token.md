# 搜索令牌

本文档演示如何通过关键词搜索令牌，快速找到目标令牌的详细信息。

## 认证参数说明

| 参数 | 说明 |
| --- | --- |
| `SYSTEM_TOKEN` | 系统令牌，获取路径： 登录DMXAPI → 工作台 → 个人设置 → 更多选项 → 系统令牌 |
| `USER_ID` | 当前用户 ID，获取路径： 登录DMXAPI → 工作台 → 个人设置 |

## 接口说明

- 请求方式：`GET`
- 请求地址：`https://www.dmxapi.cn/api/token/search`
- 用途：按关键词搜索令牌，返回名称匹配的令牌列表

### 请求参数

| 参数 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `keyword` | string | 否 | 搜索关键词，按令牌名称模糊匹配。不传则返回全部令牌 |

## 代码示例

```python
import requests
from datetime import datetime

# ===== 只需修改这里 =====
SYSTEM_TOKEN = "你的系统令牌"  # 系统令牌
USER_ID = "你的用户id"        # 当前用户 ID
keyword = "我的令牌"           # 搜索关键词，按令牌名称模糊匹配，留空则返回全部令牌
# ========================

# 以下为自动处理逻辑，无需修改
headers = {
    "Authorization": f"Bearer {SYSTEM_TOKEN}",
    "Rix-Api-User": USER_ID,
    "Accept": "application/json"
}

params = {}
if keyword:
    params["keyword"] = keyword

resp = requests.get("https://www.dmxapi.cn/api/token/search", headers=headers, params=params)
tokens = resp.json()["data"]

if not tokens:
    print("未找到匹配的令牌")
else:
    print(f"共找到 {len(tokens)} 个令牌：\n")
    for t in tokens:
        # 额度显示
        if t["unlimited_quota"]:
            quota_str = "无限"
        else:
            quota_str = f"{t['remain_quota'] / 500000:.2f} 元"

        # 次数显示
        if t["unlimited_count"]:
            count_str = "无限"
        else:
            count_str = str(t["remain_count"])

        # 过期时间显示
        if t["expired_time"] == -1:
            expire_str = "永不过期"
        elif t["expired_time"] == 0:
            expire_str = "未设置"
        else:
            expire_str = datetime.fromtimestamp(t["expired_time"]).strftime("%Y-%m-%d %H:%M:%S")

        # Key 脱敏显示
        key = t["key"]
        masked_key = f"sk-{key}"

        print(f"ID: {t['id']}")
        print(f"  名称: {t['name']}")
        print(f"  Key: {masked_key}")
        print(f"  状态: {'已启用' if t['status'] == 1 else '已禁用'}")
        print(f"  额度: {quota_str}")
        print(f"  次数: {count_str}")
        print(f"  过期时间: {expire_str}")
        if t["model_limits_enabled"]:
            print(f"  模型限制: {t['model_limits']}")
        if t["allow_ips"]:
            print(f"  IP白名单: {t['allow_ips']}")
        if t["exclude_ips"]:
            print(f"  IP黑名单: {t['exclude_ips']}")
        print()
```

### 返回示例

```text
共找到 2 个令牌：

ID: 22017
  名称: 我的令牌A
  Key: sk-qlL6****************************xjEX
  状态: 已启用
  额度: 无限
  次数: 无限
  过期时间: 永不过期

ID: 51371
  名称: 我的令牌B
  Key: sk-lEm8****************************PoLd
  状态: 已启用
  额度: 无限
  次数: 无限
  过期时间: 永不过期
```

## 使用说明

1. 将 `SYSTEM_TOKEN` 替换为你自己的系统令牌。
2. 将 `USER_ID` 替换为实际用户 ID。
3. 修改 `keyword` 为你要搜索的关键词，留空则返回全部令牌。

## 注意事项

- 搜索按令牌**名称**进行模糊匹配，不支持按 Key 或 ID 搜索。
- 不传 `keyword` 时返回全部令牌，与「获取所有令牌」接口效果类似。
- 返回的数据结构与「获取所有令牌」略有不同，搜索接口的 `data` 直接是数组。

<p align="center">
  <small>© 2026 DMXAPI 搜索令牌</small>
</p>
