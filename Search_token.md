# 搜索令牌

按后台令牌列表中的“名称”或完整 API Key 查找令牌，并显示完整 API Key、状态、额度和时间信息。名称查询搜索的是**令牌名称**，不是模型名称或模型 ID。

::: danger 本示例会显示完整 API Key
脚本会在终端直接输出完整 API Key。请只在可信的本地设备运行，不要截图、分享或写入日志。
:::

## 接口

第一步，分页读取当前账号的全部令牌：

- 方法：`GET`
- 地址：`https://www.dmxapi.cn/api/token/`
- 查询参数：`page`、`page_size`

第二步，批量读取匹配令牌的完整 Key：

- 方法：`POST`
- 地址：`https://www.dmxapi.cn/api/token/batch/keys`
- JSON 字段：`ids`，每批最多 `100` 个令牌 ID
- 完整 Key：位于响应的 `data.keys` 中

两个接口都使用 `SYSTEM_TOKEN` + `USER_ID` 认证。`keyword` 和 `API_KEY` 只用于脚本本地筛选，不会作为管理接口的认证信息。

## 两种查询方式

下面两个标签页是相互独立的完整代码，选择其中一个复制运行：

- **按令牌名称查询**：填写 `SYSTEM_TOKEN`、`USER_ID` 和 `keyword`。
- **按完整 API Key 查询**：填写 `SYSTEM_TOKEN`、`USER_ID` 和 `API_KEY`。

## Python 示例

安装依赖：

```powershell
pip install requests
```

选择下面一个标签页，修改代码顶部的三个参数后运行。

::: code-group

```python [按令牌名称查询]
from datetime import datetime

import requests

# 只需修改这里
SYSTEM_TOKEN = "请在这里填写系统访问令牌"  # 管理接口使用的系统访问令牌
USER_ID = "请在这里填写用户 ID"  # 与系统访问令牌同账号的用户 ID
keyword = "DMXAPI创建测试"  # 填写完整令牌名称或名称中的一部分

# 下面无需修改
BASE_URL = "https://www.dmxapi.cn"  # 平台管理接口地址
page_size = 100  # 每页读取的令牌数量
QUOTA_PER_CNY = 500_000  # 额度换算比例：500000 原始额度 = 1 CNY
headers = {
    "Authorization": f"Bearer {SYSTEM_TOKEN}",  # 使用系统访问令牌认证
    "Dmx-Api-User": str(USER_ID),  # 指定请求所属的用户 ID
}

keyword = keyword.strip()
if not keyword:
    raise ValueError("请填写令牌名称关键词")


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


# 分页读取当前账号的全部令牌。
tokens, page = [], 1
while True:
    data = response_data(requests.get(
        f"{BASE_URL}/api/token/",
        headers=headers,
        params={"page": page, "page_size": page_size},
        timeout=30,  # 单次请求最多等待 30 秒
    ))
    items = data["items"]
    tokens.extend(items)
    if not items or len(tokens) >= data["total"]:
        break
    page += 1

# 在本地按令牌名称查找，支持名称子串且不区分英文字母大小写。
tokens = [
    token for token in tokens
    if keyword.lower() in str(token.get("name") or "").lower()
]

# 每批最多读取 100 个完整 Key。
token_ids = [token["id"] for token in tokens]
full_keys = {}
for start in range(0, len(token_ids), 100):
    keys = response_data(requests.post(
        f"{BASE_URL}/api/token/batch/keys",
        headers=headers,
        json={"ids": token_ids[start:start + 100]},
        timeout=30,  # 单次请求最多等待 30 秒
    ))["keys"]
    full_keys.update(keys)

print(f"找到 {len(tokens)} 个令牌")
for token in tokens:
    api_key = full_keys[str(token["id"])]  # 完整 Key 响应使用字符串 ID
    api_key = api_key if api_key.startswith("sk-") else f"sk-{api_key}"
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
    print(
        f"令牌名称：{token.get('name', '')}\n"
        f"所属用户 ID：{USER_ID}\n"
        f"状态：{'已启用' if token.get('status') == 1 else '已禁用'}\n"
        f"API 密钥：{api_key}\n"
        f"剩余额度：{remain_quota_text}\n"
        f"消耗额度：{token.get('used_quota', 0) / QUOTA_PER_CNY:.4f} CNY\n"
        f"模型限制：{model_limits_text}\n"
        f"IP 限制：{allow_ips_text}\n"
        f"创建时间：{time_text(token.get('created_time'))}\n"
        f"最后使用时间：{time_text(token.get('accessed_time'))}\n"
        f"过期时间：{time_text(token.get('expired_time'))}\n"
        "----------------------------------------"
    )
```

```python [按完整 API Key 查询]
from datetime import datetime

import requests

# 只需修改这里
SYSTEM_TOKEN = "请在这里填写系统访问令牌"  # 管理接口使用的系统访问令牌
USER_ID = "请在这里填写用户 ID"  # 与系统访问令牌同账号的用户 ID
API_KEY = "sk-请在这里填写完整 API Key"  # 必须包含 sk- 前缀，不能使用脱敏 Key

# 下面无需修改
BASE_URL = "https://www.dmxapi.cn"  # 平台管理接口地址
page_size = 100  # 每页读取的令牌数量
QUOTA_PER_CNY = 500_000  # 额度换算比例：500000 原始额度 = 1 CNY
headers = {
    "Authorization": f"Bearer {SYSTEM_TOKEN}",  # 使用系统访问令牌认证
    "Dmx-Api-User": str(USER_ID),  # 指定请求所属的用户 ID
}

API_KEY = API_KEY.strip()
if not API_KEY.startswith("sk-") or "*" in API_KEY:
    raise ValueError("请输入包含 sk- 前缀且未经脱敏的完整 API Key")


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


# 分页读取当前账号的全部令牌。
tokens, page = [], 1
while True:
    data = response_data(requests.get(
        f"{BASE_URL}/api/token/",
        headers=headers,
        params={"page": page, "page_size": page_size},
        timeout=30,  # 单次请求最多等待 30 秒
    ))
    items = data["items"]
    tokens.extend(items)
    if not items or len(tokens) >= data["total"]:
        break
    page += 1

# 每批最多读取 100 个完整 Key。
token_ids = [token["id"] for token in tokens]
full_keys = {}
for start in range(0, len(token_ids), 100):
    keys = response_data(requests.post(
        f"{BASE_URL}/api/token/batch/keys",
        headers=headers,
        json={"ids": token_ids[start:start + 100]},
        timeout=30,  # 单次请求最多等待 30 秒
    ))["keys"]
    full_keys.update(keys)


# 完整 Key 缺少 sk- 前缀时自动补上。
def api_key_of(token):
    value = full_keys[str(token["id"])]
    return value if value.startswith("sk-") else f"sk-{value}"


# 使用区分大小写的完整值精确匹配。
tokens = [token for token in tokens if api_key_of(token) == API_KEY]

print(f"找到 {len(tokens)} 个令牌")
for token in tokens:
    api_key = api_key_of(token)
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
    print(
        f"令牌名称：{token.get('name', '')}\n"
        f"所属用户 ID：{USER_ID}\n"
        f"状态：{'已启用' if token.get('status') == 1 else '已禁用'}\n"
        f"API 密钥：{api_key}\n"
        f"剩余额度：{remain_quota_text}\n"
        f"消耗额度：{token.get('used_quota', 0) / QUOTA_PER_CNY:.4f} CNY\n"
        f"模型限制：{model_limits_text}\n"
        f"IP 限制：{allow_ips_text}\n"
        f"创建时间：{time_text(token.get('created_time'))}\n"
        f"最后使用时间：{time_text(token.get('accessed_time'))}\n"
        f"过期时间：{time_text(token.get('expired_time'))}\n"
        "----------------------------------------"
    )
```

:::

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

脚本会先显示匹配数量，再完整输出每个令牌的信息；不同令牌之间使用 `----------------------------------------` 分隔。

## 完整 Key 响应结构

```json
{
  "data": {
    "keys": {
      "12345": "<完整 API Key>"
    }
  },
  "message": "",
  "success": true
}
```

## 找不到令牌时

1. 确认 `SYSTEM_TOKEN` 和 `USER_ID` 属于同一账号；
2. 名称查询时，确认填写的是令牌名称，而不是模型名称或模型 ID；
3. API Key 查询时，必须填写包含 `sk-` 前缀的完整 Key，不能使用带 `*` 的脱敏 Key；
4. 完整 API Key 区分大小写，必须与令牌实际 Key 完全一致；
5. 确认令牌未被删除。

<p align="center">
  <small>© 2026 DMXAPI 搜索令牌</small>
</p>
