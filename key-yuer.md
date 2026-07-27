# 查询令牌余额

填写 DMXAPI API Key、系统访问令牌和用户 ID。脚本会一次读取最多 999 个令牌并查找匹配项，只显示令牌名称、状态、已用额度、剩余额度和过期时间。

::: warning 凭据需要属于同一账号
完整 API Key 只在本地转换为脱敏形式，不会作为查询参数发送。
:::

## 接口

- 方法：`GET`
- 地址：`https://www.dmxapi.cn/api/token/`
- 认证：`SYSTEM_TOKEN` + `USER_ID`，详见 [系统令牌与用户 ID](security_token_ID.md)
- 查询参数：固定使用 `page=1`、`page_size=999`

## 需要填写的三个参数

| 参数 | 用途 | 获取位置 |
| --- | --- | --- |
| `API_KEY` | 要查询余额的 DMXAPI 调用令牌 | 工作台 → API 令牌 |
| `SYSTEM_TOKEN` | 调用平台管理接口 | 个人设置 → 安全 → 访问令牌 |
| `USER_ID` | 指定系统令牌所属用户 | 个人设置 → 个人资料 |

## Python 示例

```python
from datetime import datetime
import requests

# 只需修改这里
API_KEY = "sk-请在这里填写 DMXAPI 令牌"  # 要查询余额的模型调用令牌
SYSTEM_TOKEN = "请在这里填写系统访问令牌"  # 管理接口使用的系统访问令牌
USER_ID = "请在这里填写用户 ID"  # 三项凭据需属于同一账号

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

key = API_KEY.removeprefix("sk-")
target_key = f"{key[:4]}{'*' * 10}{key[-4:]}"
items = requests.get(
    f"{BASE_URL}/api/token/",
    headers=headers,
    params={"page": 1, "page_size": 999},
    timeout=30,
).json()["data"]["items"]
token = next(
    (item for item in items if item.get("key", "").removeprefix("sk-") == target_key),
    None,
)
if token is None:
    raise SystemExit("未找到该 API Key，请检查三项凭据是否属于同一账号")
remain_quota_text = (
    "无限额度"
    if token.get("unlimited_quota")
    else f"{token.get('remain_quota', 0) / QUOTA_PER_CNY:.4f} CNY"
)

print(
    f"令牌名称：{token.get('name', '')}\n"
    f"状态：{'启用' if token.get('status') == 1 else '禁用'}\n"
    f"已用额度：{token.get('used_quota', 0) / QUOTA_PER_CNY:.4f} CNY\n"
    f"剩余额度：{remain_quota_text}\n"
    f"过期时间：{time_text(token.get('expired_time'))}"
)
```

## 输出示例

```text
令牌名称：project-a
状态：启用
已用额度：0.1250 CNY
剩余额度：1.0000 CNY
过期时间：永不过期
```

<p align="center">
  <small>© 2026 DMXAPI 查询令牌余额</small>
</p>
