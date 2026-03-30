# 批量删除令牌

本文档演示如何先查询当前账号下已有的令牌，再按令牌 ID 批量删除指定令牌。

## 认证参数说明

在下面两个示例里，你都需要先准备这两个参数：

| 参数 | 说明 |
| --- | --- |
| `SYSTEM_TOKEN` | 系统令牌，获取路径： 登录DMXAPI → 工作台 → 个人设置 → 更多选项 → 系统令牌 |
| `USER_ID` | 当前用户 ID，获取路径： 登录DMXAPI → 工作台 → 个人设置 |


## 接口说明

### 1. 查询令牌列表

- 请求方式：`GET`
- 请求地址：`https://www.dmxapi.cn/api/token/`
- 用途：获取当前账号下全部令牌的 `id` 和 `name`

### 2. 批量删除令牌

- 请求方式：`POST`
- 请求地址：`https://www.dmxapi.cn/api/token/batch`
- 用途：按令牌 ID 批量删除多个令牌


## 一、查询当前有哪些令牌

```python
import requests

SYSTEM_TOKEN = "你的系统令牌"  # 系统令牌
USER_ID = "你的用户id"  # 当前用户 ID

headers = {
    "Authorization": f"Bearer {SYSTEM_TOKEN}",
    "Rix-Api-User": USER_ID,
    "Accept": "application/json"
}

resp = requests.get("https://www.dmxapi.cn/api/token/", headers=headers)
items = resp.json()["data"]["items"]

for token in items:
    print(f"ID: {token['id']}  名称: {token['name']}")
```

### 返回示例

```json
ID: 51278  名称: 4
ID: 51277  名称: 3
ID: 51276  名称: 2
ID: 51107  名称: 1
ID: 22017  名称: Hukeer initial token
```

## 二、批量删除指定令牌

先查询令牌列表，确认要删除的令牌 ID，再将这些 ID 放进 `ids_to_delete` 数组中提交删除。

```python
import requests

SYSTEM_TOKEN = "你的系统令牌" # 系统令牌
USER_ID = "你的用户id" # 当前用户 ID

headers = {
    "Authorization": f"Bearer {SYSTEM_TOKEN}",
    "Rix-Api-User": USER_ID,
    "Content-Type": "application/json"
}

ids_to_delete = [51278, 51277]  # 改成你要删除的令牌 ID

# 先查名称，方便打印删除结果
resp = requests.get("https://www.dmxapi.cn/api/token/", headers=headers)
items = resp.json()["data"]["items"]
name_map = {t["id"]: t["name"] for t in items}

# 批量删除
resp = requests.post(
    "https://www.dmxapi.cn/api/token/batch",
    headers=headers,
    json={"ids": ids_to_delete}
)

if resp.status_code == 200:
    for token_id in ids_to_delete:
        print(f"已删除 ID: {token_id}  名称: {name_map.get(token_id, '未知')}")
else:
    print(f"失败: {resp.status_code}")
```

### 返回示例

```json
已删除 ID: 51278  名称: 4
已删除 ID: 51277  名称: 3
```





## 使用说明

1. 将 `SYSTEM_TOKEN` 替换为你自己的系统令牌。
2. 将 `USER_ID` 替换为实际用户 ID。
3. 先执行查询脚本，确认需要删除的令牌 ID。
4. 再执行批量删除脚本，删除目标令牌。

## 注意事项

- 批量删除前建议先查询一次，避免误删。
- `ids_to_delete` 中填写的是令牌 ID，不是令牌名称。
- 如果返回状态码不是 `200`，说明删除失败，需要进一步检查请求参数或权限。

<p align="center">
  <small>© 2026 DMXAPI 批量删除令牌</small>
</p>