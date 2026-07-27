# 批量删除令牌

先查询当前账号的令牌 ID 和名称，再使用令牌 ID 一次删除一个或多个 API Key。

::: danger 删除后不可恢复
请求体必须填写令牌 ID，不是令牌名称或 API Key。请在执行批量删除前仔细核对查询结果。
:::

## 接口

以下接口都使用 `SYSTEM_TOKEN` + `USER_ID` 认证。

### 查询令牌列表

- 方法：`GET`
- 地址：`https://www.dmxapi.cn/api/token/`
- 查询参数：`page`、`page_size`
- 用途：取得要删除的令牌 ID 和名称

### 批量删除令牌

- 方法：`POST`
- 地址：`https://www.dmxapi.cn/api/token/batch`
- Content-Type：`application/json`

## 删除请求体

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `ids` | integer[] | 是 | 要删除的令牌 ID 数组 |

```json
{
  "ids": [
    12345,
    12346
  ]
}
```

## 一、查询要删除的令牌 ID

安装依赖：

```powershell
pip install requests
```

填写系统访问令牌和用户 ID 后运行：

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
    params={"page": 1, "page_size": 100},
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
BASE_URL = "https://www.dmxapi.cn"  # 平台管理接口地址
PAGE_SIZE = 100  # 每页读取的令牌数量
headers = {
    "Authorization": f"Bearer {SYSTEM_TOKEN}",  # 使用系统访问令牌认证
    "Dmx-Api-User": str(USER_ID),  # 指定请求所属的用户 ID
    "Content-Type": "application/json",  # 删除请求体使用 JSON 格式
}


def response_data(response, error_message):
    """统一取得接口返回的 data。"""
    response.raise_for_status()
    result = response.json()
    if not result.get("success"):
        raise RuntimeError(result.get("message") or error_message)
    return result["data"]


if not token_ids:
    raise SystemExit("请至少填写一个要删除的令牌 ID")
token_ids = list(dict.fromkeys(token_ids))

# 删除前查询全部令牌，保存 ID 与名称的对应关系。
page = 1
name_map = {}
while True:
    data = response_data(requests.get(
        f"{BASE_URL}/api/token/",
        headers=headers,
        params={"page": page, "page_size": PAGE_SIZE},
        timeout=30,
    ), "查询令牌失败")
    for token in data["items"]:
        name_map[token["id"]] = token.get("name", "")
    if not data["items"] or page * PAGE_SIZE >= data["total"]:
        break
    page += 1

missing_ids = [token_id for token_id in token_ids if token_id not in name_map]
if missing_ids:
    raise SystemExit(f"未找到这些令牌 ID，已取消删除：{missing_ids}")

deleted_count = response_data(requests.post(
    f"{BASE_URL}/api/token/batch",
    headers=headers,
    json={"ids": token_ids},
    timeout=30,
), "批量删除失败")

print(f"删除成功，共删除 {deleted_count} 个令牌")
for token_id in token_ids:
    print(f"已删除 ID：{token_id}  令牌名称：{name_map[token_id]}")
```

## 删除结果输出示例

```text
删除成功，共删除 2 个令牌
已删除 ID：12345  令牌名称：project-a
已删除 ID：12346  令牌名称：project-b
```

## 成功响应示例

```json
{
  "data": 2,
  "message": "",
  "success": true
}
```

## 重要说明

- 必须先查询并核对令牌 ID；不要用名称或 API Key 代替 ID。
- 删除操作不可撤销，脚本不会自动恢复已删除的令牌。
- 接口返回非成功状态时，脚本会停止并显示错误。
- 删除后可通过 [搜索令牌](/Search_token) 或 [获取所有令牌](/Get_all_tokens) 再次确认。

<p align="center">
  <small>© 2026 DMXAPI 批量删除令牌</small>
</p>
