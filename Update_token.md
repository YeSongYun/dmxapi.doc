# 更新令牌

根据令牌 ID 更新 API Key 的名称、额度、过期时间、模型/IP 限制和令牌限流配置。

::: danger 本示例会显示完整 API Key
更新成功后，脚本会在终端直接输出完整 API Key。请只在可信的本地设备运行，不要截图、分享或写入日志。
:::

认证：`SYSTEM_TOKEN` + `USER_ID`，详见 [系统令牌与用户 ID](security_token_ID.md)。

## 一、查询要更新的令牌 ID

先列出当前账号下的令牌，从结果中找到要更新的 `token_id`。

```python
import requests

# 只需修改这里
SYSTEM_TOKEN = "请在这里填写系统访问令牌"  # 管理接口使用的系统访问令牌
USER_ID = "请在这里填写用户 ID"  # 与系统访问令牌同账号的用户 ID

# 下面无需修改
BASE_URL = "https://www.dmxapi.cn"  # 平台管理接口地址
headers = {
    "Authorization": f"Bearer {SYSTEM_TOKEN}",  # 使用系统访问令牌认证
    "Dmx-Api-User": str(USER_ID),  # 指定请求所属的用户 ID
}

response = requests.get(
    f"{BASE_URL}/api/token/",
    headers=headers,
    params={"page": 1, "page_size": 999},
    timeout=30,
)
response.raise_for_status()
result = response.json()
if not result.get("success"):
    raise RuntimeError(result.get("message") or "查询令牌失败")

items = result["data"]["items"]
print(f"找到 {len(items)} 个令牌")
for token in items:
    print(f"ID：{token['id']}  令牌名称：{token.get('name', '')}")
```

### 查询 ID 输出示例

```text
找到 2 个令牌
ID：12345  令牌名称：DMXAPI创建测试
ID：12346  令牌名称：DMXAPI创建测试-2
```

把目标令牌前面的数字 ID 填入下一步的 `token_id`。

## 二、根据 ID 更新令牌

填写上一步查到的 `token_id`，再像创建令牌一样修改参数后运行。除 `token_id` 外，参数名称、顺序和含义与创建令牌完全一致。

```python
import time
from datetime import datetime

import requests

# 只需修改这里
SYSTEM_TOKEN = "请在这里填写系统访问令牌"  # 管理接口使用的系统访问令牌
USER_ID = "请在这里填写用户 ID"  # 与系统访问令牌同账号的用户 ID
token_id = 12345  # 填写第一步查询到的令牌 ID

name = "DMXAPI更新测试"  # 令牌名称
expired_time = -1  # 填 -1 表示永不过期；填正整数表示多少天后过期
unlimited_quota = True  # True 表示不限制令牌额度
remain_quota = 1  # 额度金额，单位 CNY；unlimited_quota=False 时生效，无限额度时忽略
model_limits_enabled = False  # 是否启用模型限制
model_limits = ""  # 允许的模型 ID，用英文逗号分隔
allow_ips = ""  # IP 白名单；换行分隔，留空表示不限制
rate_limits_enabled = True  # 是否启用单令牌限流
rate_limits_time = 60  # 限流时间窗口，单位为秒
rate_limits_count = 60  # 每个窗口允许的最大请求数
rate_limits_content = ""  # 超出限流时返回的提示语

# 下面无需修改
BASE_URL = "https://www.dmxapi.cn"
expired_time = -1 if expired_time == -1 else int(time.time() + expired_time * 86400)
headers = {
    "Authorization": f"Bearer {SYSTEM_TOKEN}",
    "Dmx-Api-User": str(USER_ID),
}

def time_text(value):
    if value == -1:
        return "永不过期"
    if not value:
        return "无记录"
    return datetime.fromtimestamp(value).astimezone().strftime("%Y-%m-%d %H:%M:%S %z")


response = requests.get(
    f"{BASE_URL}/api/token/{token_id}",
    headers=headers,
    timeout=30,
)
response.raise_for_status()
current = response.json()["data"]

payload = {
    "id": token_id,
    "name": name,
    "expired_time": expired_time,
    "remain_quota": int(remain_quota * 500000),  # 1 元 = 500000 原始额度
    "unlimited_quota": unlimited_quota,
    "model_limits_enabled": model_limits_enabled,
    "model_limits": model_limits,
    "allow_ips": allow_ips,
    "group": "default",
    "rate_limits_enabled": rate_limits_enabled,
    "rate_limits_time": rate_limits_time,
    "rate_limits_count": rate_limits_count,
    "rate_limits_content": rate_limits_content,
    "cross_group_retry": current.get("cross_group_retry", False),
    "status": current["status"],
}
response = requests.put(
    f"{BASE_URL}/api/token/",
    headers=headers,
    json=payload,
    timeout=30,
)
response.raise_for_status()
result = response.json()
if not result.get("success"):
    raise RuntimeError(result.get("message") or "更新令牌失败")
updated = result["data"]

response = requests.post(
    f"{BASE_URL}/api/token/{token_id}/key",
    headers=headers,
    timeout=30,
)
response.raise_for_status()
api_key = response.json()["data"]["key"]
api_key = api_key if api_key.startswith("sk-") else f"sk-{api_key}"

remain_quota_text = (
    "无限额度"
    if updated.get("unlimited_quota")
    else f"{updated.get('remain_quota', 0) / 500000:.4f} CNY"  # 500000 原始额度 = 1 元
)
model_limits_text = (
    str(updated.get("model_limits") or "").strip()
    if updated.get("model_limits_enabled")
    else ""
) or "无限制"
allow_ips_text = "、".join(
    item.strip()
    for item in str(updated.get("allow_ips") or "").splitlines()
    if item.strip()
) or "无限制"

print(
    "更新成功\n"
    f"令牌名称：{updated.get('name', '')}\n"
    f"所属用户 ID：{USER_ID}\n"
    f"状态：{'已启用' if updated.get('status') == 1 else '已禁用'}\n"
    f"API 密钥：{api_key}\n"
    f"剩余额度：{remain_quota_text}\n"
    f"消耗额度：{updated.get('used_quota', 0) / 500000:.4f} CNY\n"
    f"模型限制：{model_limits_text}\n"
    f"IP 限制：{allow_ips_text}\n"
    f"创建时间：{time_text(updated.get('created_time'))}\n"
    f"最后使用时间：{time_text(updated.get('accessed_time'))}\n"
    f"过期时间：{time_text(updated.get('expired_time'))}\n"
    "----------------------------------------"
)
```

## 更新结果输出示例

```text
更新成功
令牌名称：DMXAPI更新测试
所属用户 ID：12345
状态：已启用
API 密钥：<此处会显示完整 API Key>
剩余额度：5.0000 CNY
消耗额度：1.0000 CNY
模型限制：无限制
IP 限制：无限制
创建时间：2026-07-27 10:00:00 +0800
最后使用时间：2026-07-27 10:15:00 +0800
过期时间：永不过期
----------------------------------------
```

<p align="center">
  <small>© 2026 DMXAPI 更新令牌</small>
</p>
