# 获取所有令牌

一次获取当前账号下最多 999 个 API Key 令牌，包括状态、额度、时间、模型/IP 限制和令牌限流配置。

## 接口

- 方法：`GET`
- 地址：`https://www.dmxapi.cn/api/token/`
- 认证：`SYSTEM_TOKEN` + `USER_ID`，详见 [系统令牌与用户 ID](security_token_ID.md)
- 参数：固定使用 `page=1`、`page_size=999`

列表接口返回脱敏后的 `key`，本页直接使用该值展示。

不脱敏时，脚本会逐个读取完整 Key：

- 方法：`POST`
- 地址：`https://www.dmxapi.cn/api/token/{token_id}/key`
- 完整 Key：响应中的 `data.key`

::: danger 完整 Key 会直接显示在终端
将 `MASK_KEYS` 改为 `False` 后，请只在可信终端运行，不要截图、分享或记录输出。
:::


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
MASK_KEYS = True  # True 显示脱敏 Key；False 显示完整 Key

# 下面无需修改
BASE_URL = "https://www.dmxapi.cn"
QUOTA_PER_CNY = 500_000
headers = {
    "Authorization": f"Bearer {SYSTEM_TOKEN}",
    "Dmx-Api-User": str(USER_ID),
}

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

print(f"共获取 {len(tokens)} 个令牌")
for token in tokens:
    token_id_text = str(token["id"])
    api_key = token["key"]
    if not MASK_KEYS:
        api_key = requests.post(
            f"{BASE_URL}/api/token/{token['id']}/key", headers=headers, timeout=30
        ).json()["data"]["key"]
    api_key = api_key if api_key.startswith("sk-") else f"sk-{api_key}"
    remain_quota_text = (
        "无限额度"
        if token.get("unlimited_quota")
        else f"{token.get('remain_quota', 0) / QUOTA_PER_CNY:.4f} CNY"
    )
    model_limits_text = (str(token.get("model_limits") or "").strip() if token.get("model_limits_enabled") else "") or "无限制"
    allow_ips_text = "、".join(
        filter(None, map(str.strip, str(token.get("allow_ips") or "").splitlines()))
    ) or "无限制"
    rate_limits_text = "无限制"
    if token.get("rate_limits_enabled"):
        rate_limits_text = f"{token.get('rate_limits_time', 0)} 秒内最多 {token.get('rate_limits_count', 0)} 次"
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

`MASK_KEYS=True` 时显示列表接口返回的脱敏 Key；改为 `False` 后，只有“API 密钥”一行会显示完整值，并且每个令牌会增加一次单令牌 Key 请求。

<p align="center">
  <small>© 2026 DMXAPI 获取所有令牌</small>
</p>
