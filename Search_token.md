# 搜索令牌

按后台令牌列表中的名称或完整 API Key 查找令牌，并显示完整 API Key、状态、额度和时间信息。名称查询搜索的是**令牌名称**，不是模型名称或模型 ID。

::: danger 本示例会显示完整 API Key
脚本会在终端直接输出完整 API Key。请只在可信的本地设备运行，不要截图、分享或写入日志。
:::

## 📌 接口地址

```
GET   https://www.dmxapi.cn/api/token/
POST  https://www.dmxapi.cn/api/token/{token_id}/key
```

- 认证：`SYSTEM_TOKEN` + `USER_ID`，详见 [系统令牌与用户 ID](security_token_ID.md)
- 搜索内容只用于本地筛选

## 两种查询方式

- 按名称查询：`search_type = "name"`，`search_value` 填完整名称或名称的一部分。
- 按完整 API Key 查询：`search_type = "key"`，`search_value` 填包含 `sk-` 前缀的完整 Key。

## Python 示例

```python
from datetime import datetime
import requests

# 只需修改这里
SYSTEM_TOKEN = "请在这里填写系统访问令牌"
USER_ID = "请在这里填写用户 ID"
search_type = "name"  # name：按名称查询；key：按完整 API Key 查询
search_value = "DMXAPI创建测试"

# 下面无需修改
BASE_URL = "https://www.dmxapi.cn"
headers = {
    "Authorization": f"Bearer {SYSTEM_TOKEN}",
    "Dmx-Api-User": str(USER_ID),
}
search_value = search_value.strip()
if not search_value:
    raise ValueError("请填写搜索内容")


def time_text(value):
    return "永不过期" if value == -1 else (
        datetime.fromtimestamp(value).astimezone().strftime("%Y-%m-%d %H:%M:%S %z")
        if value else "无记录"
    )

tokens = requests.get(
    f"{BASE_URL}/api/token/",
    headers=headers,
    params={"page": 1, "page_size": 999},
    timeout=30,
).json()["data"]["items"]

if search_type == "name":
    tokens = [
        token for token in tokens
        if search_value.lower() in str(token.get("name") or "").lower()
    ]
elif search_type == "key":
    raw_key = search_value.removeprefix("sk-")
    tokens = [
        token for token in tokens
        if "*" not in (key := str(token.get("key") or "").removeprefix("sk-"))
        or (raw_key.startswith(key.partition("*")[0]) and raw_key.endswith(key.rpartition("*")[2]))
    ]
else:
    raise ValueError('search_type 只能填写 "name" 或 "key"')

def api_key_of(token):
    value = requests.post(
        f"{BASE_URL}/api/token/{token['id']}/key",
        headers=headers,
        timeout=30,
    ).json()["data"]["key"]
    return value if value.startswith("sk-") else f"sk-{value}"


tokens = [(token, api_key_of(token)) for token in tokens]
if search_type == "key":
    tokens = [(token, api_key) for token, api_key in tokens if api_key == search_value]

print(f"找到 {len(tokens)} 个令牌")
for token, api_key in tokens:
    remain_quota_text = (
        "无限额度"
        if token.get("unlimited_quota")
        else f"{token.get('remain_quota', 0) / 500000:.4f} CNY"  # 500000 原始额度 = 1 元
    )
    model_limits_text = (str(token.get("model_limits") or "").strip() if token.get("model_limits_enabled") else "") or "无限制"
    allow_ips_text = "、".join(
        filter(None, map(str.strip, str(token.get("allow_ips") or "").splitlines()))
    ) or "无限制"
    print(
        f"令牌名称：{token.get('name', '')}\n"
        f"所属用户 ID：{USER_ID}\n"
        f"状态：{'已启用' if token.get('status') == 1 else '已禁用'}\n"
        f"API 密钥：{api_key}\n"
        f"剩余额度：{remain_quota_text}\n"
        f"消耗额度：{token.get('used_quota', 0) / 500000:.4f} CNY\n"
        f"模型限制：{model_limits_text}\n"
        f"IP 限制：{allow_ips_text}\n"
        f"创建时间：{time_text(token.get('created_time'))}\n"
        f"最后使用时间：{time_text(token.get('accessed_time'))}\n"
        f"过期时间：{time_text(token.get('expired_time'))}\n"
        "----------------------------------------"
    )
```

## 输出示例

```text
找到 2 个令牌
令牌名称：DMXAPI创建测试
所属用户 ID：12345
状态：已启用
API 密钥：<此处会显示第一个完整 API Key>
剩余额度：无限额度
消耗额度：0.0000 CNY
模型限制：无限制
IP 限制：无限制
创建时间：2026-07-27 10:00:00 +0800
最后使用时间：2026-07-27 10:15:00 +0800
过期时间：永不过期
----------------------------------------
令牌名称：DMXAPI创建测试
所属用户 ID：12345
状态：已禁用
API 密钥：<此处会显示第二个完整 API Key>
剩余额度：1.0000 CNY
消耗额度：1.0000 CNY
模型限制：gpt-5.5,claude-sonnet-4-20250514
IP 限制：203.0.113.10、198.51.100.0/24
创建时间：2026-07-27 10:05:00 +0800
最后使用时间：无记录
过期时间：2026-08-26 10:05:00 +0800
----------------------------------------
```

<p align="center">
  <small>© 2026 DMXAPI 搜索令牌</small>
</p>
