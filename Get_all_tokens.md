# 获取所有令牌

分页获取当前账号下的全部 API Key 令牌，包括状态、额度、时间、模型/IP 限制和令牌限流配置。

## 接口

普通列表接口：

- 方法：`GET`
- 地址：`https://www.dmxapi.cn/api/token/`
- 认证：`SYSTEM_TOKEN` + `USER_ID`
- 参数：`page` 为页码，`page_size` 为每页数量

普通列表接口返回脱敏后的 `key`。如需显示完整 Key，脚本会调用：

- 方法：`POST`
- 地址：`https://www.dmxapi.cn/api/token/batch/keys`
- 请求字段：`ids`，每批最多 `100` 个令牌 ID

::: danger 完整 Key 会直接显示在终端
将 `mask_keys` 改为 `False` 后，脚本会读取并输出完整 Key。请只在可信的本地环境临时使用，用完立即恢复为 `True`。
:::

## 常用返回字段

| 字段 | 说明 |
| --- | --- |
| `id` / `name` / `key` | 令牌 ID、名称和 Key |
| `status` | `1` 表示启用 |
| `used_quota` / `remain_quota` | 已用和剩余原始额度 |
| `unlimited_quota` | 是否无限额度 |
| `created_time` / `accessed_time` / `expired_time` | 创建、最后访问和过期时间 |
| `model_limits_enabled` / `model_limits` | 模型限制 |
| `allow_ips` | IP/CIDR 白名单 |
| `rate_limits_*` | 令牌限流开关、时间窗口、次数和提示语 |

## Python 示例

安装依赖：

```powershell
pip install requests
```

```python
from datetime import datetime

import requests

# 只需修改这里
SYSTEM_TOKEN = "请在这里填写系统访问令牌"  # 管理接口使用的系统访问令牌
USER_ID = "请在这里填写用户 ID"  # 与系统访问令牌同账号的用户 ID
mask_keys = True  # True 显示脱敏 Key；False 读取并显示完整 Key

# 下面无需修改
BASE_URL = "https://www.dmxapi.cn"  # 平台管理接口地址
page_size = 100  # 每页读取的令牌数量
max_pages = 1000  # 异常响应保护：最多读取 1000 页
QUOTA_PER_CNY = 500_000  # 额度换算比例：500000 原始额度 = 1 CNY
headers = {
    "Authorization": f"Bearer {SYSTEM_TOKEN}",  # 使用系统访问令牌认证
    "Dmx-Api-User": str(USER_ID),  # 指定请求所属的用户 ID
}


# 统一取得接口返回的 data。
def response_data(response):
    response.raise_for_status()
    result = response.json()
    if not result.get("success"):
        raise RuntimeError(result.get("message") or "接口调用失败")
    return result["data"]


# 把 Unix 秒时间戳转换为本地时间。
def time_text(value):
    if value == -1:
        return "永不过期"
    if not value:
        return "无记录"
    return datetime.fromtimestamp(value).astimezone().strftime("%Y-%m-%d %H:%M:%S %z")


# 为接口返回的 Key 补齐 sk- 前缀。
def api_key_text(value):
    value = str(value or "").strip()
    if not value:
        return ""
    return value if value.startswith("sk-") else f"sk-{value}"


# 从第一页开始自动翻页，直到取得全部令牌。
tokens, page, seen_ids = [], 1, set()
while True:
    data = response_data(requests.get(
        f"{BASE_URL}/api/token/",
        headers=headers,
        params={"page": page, "page_size": page_size},
        timeout=30,  # 单次请求最多等待 30 秒
    ))
    if "total" not in data:
        raise RuntimeError("令牌列表响应缺少 total")
    total = int(data["total"])
    items = data.get("items") or []
    page_ids = [str(token["id"]) for token in items]
    if len(page_ids) != len(set(page_ids)) or seen_ids.intersection(page_ids):
        raise RuntimeError(f"第 {page} 页返回了重复的令牌 ID")
    if total < len(tokens) + len(items):
        raise RuntimeError("令牌列表响应中的 total 小于已返回数量")
    seen_ids.update(page_ids)
    tokens.extend(items)
    if not items or len(tokens) >= total:
        break
    page += 1
    if page > max_pages:
        raise RuntimeError(f"读取页数超过安全上限 {max_pages}")

full_keys = {}
if not mask_keys:
    token_ids = [token["id"] for token in tokens]
    for start in range(0, len(token_ids), 100):  # 完整 Key 接口每批最多接收 100 个 ID
        keys = response_data(requests.post(
            f"{BASE_URL}/api/token/batch/keys",
            headers=headers,
            json={"ids": token_ids[start:start + 100]},
            timeout=30,  # 单次请求最多等待 30 秒
        ))["keys"]
        full_keys.update(keys)

print(f"共获取 {len(tokens)} 个令牌")
for token in tokens:
    token_id_text = str(token["id"])
    if mask_keys:
        api_key = api_key_text(token.get("key")) or "<未返回脱敏 Key>"
    else:
        if token_id_text not in full_keys:
            raise RuntimeError(f"完整 Key 响应缺少令牌 ID：{token_id_text}")
        api_key = api_key_text(full_keys[token_id_text])
        if not api_key:
            raise RuntimeError(f"令牌 ID {token_id_text} 的完整 Key 为空")

    remain_quota_text = (
        "无限额度"
        if token.get("unlimited_quota")
        else f"{token.get('remain_quota', 0) / QUOTA_PER_CNY:.4f} CNY"
    )
    model_limits_text = (
        str(token.get("model_limits") or "").strip()
        if token.get("model_limits_enabled")
        else ""
    ) or "无限制"
    allow_ips_text = "、".join(
        item.strip()
        for item in str(token.get("allow_ips") or "").splitlines()
        if item.strip()
    ) or "无限制"
    rate_limits_text = "无限制"
    if token.get("rate_limits_enabled"):
        rate_limits_text = (
            f"{token.get('rate_limits_time', 0)} 秒内最多 "
            f"{token.get('rate_limits_count', 0)} 次"
        )
        if token.get("rate_limits_content"):
            rate_limits_text += f"，提示：{token['rate_limits_content']}"

    print(
        f"令牌 ID：{token_id_text}\n"
        f"令牌名称：{token.get('name', '')}\n"
        f"所属用户 ID：{USER_ID}\n"
        f"状态：{'已启用' if token.get('status') == 1 else '已禁用'}\n"
        f"API 密钥：{api_key}\n"
        f"剩余额度：{remain_quota_text}\n"
        f"消耗额度：{token.get('used_quota', 0) / QUOTA_PER_CNY:.4f} CNY\n"
        f"模型限制：{model_limits_text}\n"
        f"IP 限制：{allow_ips_text}\n"
        f"令牌限流：{rate_limits_text}\n"
        f"创建时间：{time_text(token.get('created_time'))}\n"
        f"最后使用时间：{time_text(token.get('accessed_time'))}\n"
        f"过期时间：{time_text(token.get('expired_time'))}\n"
        "----------------------------------------"
    )
```

## 输出示例

```text
共获取 1 个令牌
令牌 ID：12345
令牌名称：DMXAPI创建测试
所属用户 ID：12345
状态：已启用
API 密钥：sk-abcd**********wxyz
剩余额度：1.0000 CNY
消耗额度：0.1250 CNY
模型限制：gpt-5.5,claude-sonnet-4-20250514
IP 限制：203.0.113.10、198.51.100.0/24
令牌限流：60 秒内最多 60 次
创建时间：2026-07-24 10:00:00 +0800
最后使用时间：2026-07-24 10:05:00 +0800
过期时间：2026-08-24 10:00:00 +0800
----------------------------------------
```

当 `mask_keys = True` 时，脚本只使用列表接口返回的脱敏 Key；改为 `False` 后，完整 Key 接口返回的 JSON 对象会按字符串 ID 读取。

## 下一步

- [搜索令牌](/Search_token)
- [更新令牌](/Update_token)
- [令牌余额](/key-yuer)

<p align="center">
  <small>© 2026 DMXAPI 获取所有令牌</small>
</p>
