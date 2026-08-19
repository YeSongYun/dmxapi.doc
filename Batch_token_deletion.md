# 批量删除令牌

先查询当前账号的令牌 ID 和名称，再使用令牌 ID 一次删除一个或多个 API Key。

::: danger 删除后不可恢复
请求体必须填写令牌 ID，不是令牌名称或 API Key。请在执行批量删除前仔细核对查询结果。
:::

## 接口

认证：`SYSTEM_TOKEN` + `USER_ID`，详见 [系统令牌与用户 ID](security_token_ID.md)。


## 一、查询要删除的令牌 ID

填写系统访问令牌和用户 ID 后运行：

```python
import requests

# 只需修改这里
SYSTEM_TOKEN = "请在这里填写系统访问令牌"  # 管理接口使用的系统访问令牌
USER_ID = "请在这里填写用户 ID"  # 与系统访问令牌同账号的用户 ID

# 下面无需修改
BASE_URL = "https://www.dmxapi.cn"
headers = {
    "Authorization": f"Bearer {SYSTEM_TOKEN}",
    "Dmx-Api-User": str(USER_ID),
}

items = requests.get(
    f"{BASE_URL}/api/token/",
    headers=headers,
    params={"page": 1, "page_size": 999},
    timeout=30,
).json()["data"]["items"]
print(f"找到 {len(items)} 个令牌")
for token in items:
    print(f"ID：{token['id']}  令牌名称：{token.get('name', '')}")
```

### 查询 ID 输出示例

```text
找到 2 个令牌
ID：12345  令牌名称：project-a
ID：12346  令牌名称：project-b
```

把要删除的一个或多个数字 ID 填入下一步的 `token_ids`。

## 二、根据 ID 批量删除令牌

脚本会在删除前读取当前令牌清单并保存 ID 与名称的对应关系。确认 `token_ids` 无误后再运行。

```python
import requests

# 只需修改这里
SYSTEM_TOKEN = "请在这里填写系统访问令牌"  # 管理接口使用的系统访问令牌
USER_ID = "请在这里填写用户 ID"  # 与系统访问令牌同账号的用户 ID
token_ids = [12345, 12346]  # 第一步查询到的令牌 ID，不是名称或 Key

# 下面无需修改
BASE_URL = "https://www.dmxapi.cn"
headers = {
    "Authorization": f"Bearer {SYSTEM_TOKEN}",
    "Dmx-Api-User": str(USER_ID),
}
if not token_ids:
    raise SystemExit("请至少填写一个要删除的令牌 ID")
token_ids = list(dict.fromkeys(token_ids))

items = requests.get(
    f"{BASE_URL}/api/token/",
    headers=headers,
    params={"page": 1, "page_size": 999},
    timeout=30,
).json()["data"]["items"]
name_map = {
    token["id"]: token.get("name", "")
    for token in items
    if token["id"] in token_ids
}
missing_ids = [token_id for token_id in token_ids if token_id not in name_map]
if missing_ids:
    raise SystemExit(f"未找到这些令牌 ID，已取消删除：{missing_ids}")
response = requests.post(
    f"{BASE_URL}/api/token/batch",
    headers=headers,
    json={"ids": token_ids},
    timeout=30,
)
response.raise_for_status()
result = response.json()
if not result.get("success"):
    raise RuntimeError(result.get("message") or "批量删除失败")

print(f"删除成功，共删除 {result['data']} 个令牌")
for token_id in token_ids:
    print(f"已删除 ID：{token_id}  令牌名称：{name_map[token_id]}")
```

## 删除结果输出示例

```text
删除成功，共删除 2 个令牌
已删除 ID：12345  令牌名称：project-a
已删除 ID：12346  令牌名称：project-b
```

<p align="center">
  <small>© 2026 DMXAPI 批量删除令牌</small>
</p>
