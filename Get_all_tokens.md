# 获取所有令牌

一次获取当前账号下最多 999 个 API Key 令牌，包括状态、额度、时间、模型/IP 限制和令牌限流配置。

## 接口

- 方法：`GET`
- 地址：`https://www.dmxapi.cn/api/token/`
- 认证：`SYSTEM_TOKEN` + `USER_ID`，详见 [系统令牌与用户 ID](security_token_ID.md)
- 参数：`page`（页码）、`page_size`（每页条数，最大 100）

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
import time

# 只需修改这里
SYSTEM_TOKEN = "请在这里填写系统访问令牌"  # 管理接口使用的系统访问令牌
USER_ID = "请在这里填写用户 ID"  # 与系统访问令牌同账号的用户 ID
MASK_KEYS = False  # True 显示脱敏 Key；False 显示完整 Key
PAGE = 1  # 要查看的页码
PAGE_SIZE =10   # 每页显示条数

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

all_tokens = requests.get(
    f"{BASE_URL}/api/token/",
    headers=headers,
    params={"page": 1, "page_size": -1},
    timeout=30,
).json()["data"]["items"]

start = (PAGE - 1) * PAGE_SIZE
end = start + PAGE_SIZE
tokens = all_tokens[start:end] if start < len(all_tokens) else []

print(f"共获取 {len(all_tokens)} 个令牌，显示第 {PAGE} 页（共 {PAGE_SIZE} 条）")
for i, token in enumerate(tokens):
    token_id_text = str(token["id"])
    api_key = token["key"]
    if not MASK_KEYS:
        # 限流控制：每 10 秒最多 10 次，这里每获取一次等 1 秒
        if i > 0:
            time.sleep(1)
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
共获取 102 个令牌，显示第 102 页（共 1 条）
令牌 ID：94280
令牌名称：DMXAPI
所属用户 ID：12345
状态：已启用
API 密钥：sk-4Exb**********iVaU
剩余额度：无限额度
消耗额度：0.2658 CNY
模型限制：无限制
IP 限制：无限制
令牌限流：无限制
创建时间：2026-07-13 19:03:26 +0800
最后使用时间：2026-07-18 16:19:20 +0800
过期时间：永不过期
----------------------------------------
----------------------------------------
```

`MASK_KEYS=True` 时显示列表接口返回的脱敏 Key；改为 `False` 后，只有”API 密钥”一行会显示完整值，并且每个令牌会增加一次单令牌 Key 请求（每两个请求间隔 1 秒以控制限流）。

`PAGE` 和 `PAGE_SIZE` 控制分页，请求直接按参数分页获取，不会全量拉取后再本地截取。

<p align="center">
  <small>© 2026 DMXAPI 获取所有令牌</small>
</p>
