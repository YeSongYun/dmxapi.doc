# Seedance 2.0 私域虚拟人接入全流程（创建素材组 → 素材入库 → 生成视频）

火山「私域虚拟人像素材库」可以把您自有的**虚拟人物**建成可持续维护的素材档案。创建一次素材组后，可以不断向同一个素材组添加该虚拟人物的图片、视频或音频素材；素材审核通过后，使用 `asset://<素材 Id>` 即可在 Seedance 2.0 中引用。

整套接入分成 **3 个阶段、共 4 个步骤**：

- **阶段一 · 创建虚拟人档案**：调用 `volc-asset-group-create`，获得素材组 `Id`。
- **阶段二 · 素材入库**：把素材组 `Id` 作为 `GroupId` 上传素材，再轮询到 `Status=Active`。
- **阶段三 · 生成视频**：在 Seedance 请求中使用 `asset://<素材 Id>` 引用已入库素材。

一句话：**创建虚拟人素材组拿到 `GroupId` → 上传素材拿到 `Asset Id` → 等素材变为 `Active` → 使用 `asset://<Asset Id>` 生成视频。**

:::danger 重要：私域虚拟人和授权真人不是同一个流程

- **私域虚拟人**：直接调用 `volc-asset-group-create` 创建 `AIGC` 素材组，不需要扫脸。
- **授权真人**：必须由本人授权并完成真人扫脸，使用 `volc-visual-validate-create` 和 `volc-visual-validate-result` 获取真人 `GroupId`。
- 虚拟人物不得与任何自然人的肖像或形象雷同。请勿使用本流程给自然人照片创建 `AIGC` 素材组。


:::

:::warning 重要：请保存好 GroupId、Asset Id 和 ProjectName

本流程会产生两类需要长期保存的 ID：

- **素材组 ID**：步骤一返回的 `Id`，形如 `group-...`；步骤二要把它填入 `GroupId`。
- **素材 ID**：步骤二返回的 `Id`，形如 `asset-...`；步骤四使用 `asset://<Id>` 引用。

重要：所有 ID 请务必自己保存，丢失无法找回

:::

## 流程总览

```text
阶段一 · 创建虚拟人档案
══════════════════════════

步骤一 · 创建素材组 —— 调 volc-asset-group-create
        得到 Id（素材组 ID，形如 group-...）
   │
   ▼

阶段二 · 素材入库
══════════════════

步骤二 · 上传素材 —— 调 volc-asset-create
        把步骤一的 Id 填入 GroupId
        得到 Id（素材 ID，形如 asset-...）
   │
   ▼
步骤三 · 查询状态 —— 调 volc-asset-get
        Processing 继续等待 · Failed 上传失败 · Active 素材可用
   │
   ▼

阶段三 · 生成视频
══════════════════

步骤四 · 引用素材 —— 调 Seedance 2.0
        在 input 数组的 <模态>_url.url 中填写 asset://<素材 Id>
        提交生成任务，再用 seedance-2-0-get 查询结果
```

## 与真人扫脸方案的区别

| 对比项 | 私域虚拟人像 | 授权真人素材 |
|---|---|---|
| 适用对象 | 不与任何自然人形象雷同的虚拟人物 | 已完成本人授权和真人认证的自然人 |
| 素材组来源 | 调 `volc-asset-group-create` 创建 | 扫脸后调 `volc-visual-validate-result` 获取 |
| 是否需要扫脸 | 不需要 | 需要 |
| 素材组类型 | `AIGC` | 由真人授权流程生成 |
| 后续素材上传 | 使用 `volc-asset-create` | 使用 `volc-asset-create` |
| 后续状态查询 | 使用 `volc-asset-get` | 使用 `volc-asset-get` |
| 生成时引用方式 | `asset://<素材 Id>` | `asset://<素材 Id>` |

## 接口一览

| 阶段 | 步骤 | 功能 | `model` | 请求方式 | URL |
|---|---|---|---|---|---|
| 创建档案 | 步骤一 | 创建虚拟人素材组 | `volc-asset-group-create` | POST | `https://www.dmxapi.cn/v1/responses` |
| 素材入库 | 步骤二 | 上传图片、视频或音频 | `volc-asset-create` | POST | `https://www.dmxapi.cn/v1/responses` |
| 素材入库 | 步骤三 | 查询素材处理状态 | `volc-asset-get` | POST | `https://www.dmxapi.cn/v1/responses` |
| 生成视频 | 步骤四 | 提交 Seedance 2.0 任务 | `doubao-seedance-2-0-260128` | POST | `https://www.dmxapi.cn/v1/responses` |
| 生成视频 | 步骤四 | 查询 Seedance 2.0 结果 | `seedance-2-0-get` | POST | `https://www.dmxapi.cn/v1/responses` |



## 步骤一：创建虚拟人素材组（volc-asset-group-create）

调用本接口给一个虚拟人物创建 Asset Group（素材组）。创建成功后返回素材组 `Id`，下一步要把这个 `Id` 原样填入 `volc-asset-create` 的 `GroupId`。

这个步骤只创建管理容器，不会上传素材，也不会直接生成视频。

### 请求参数

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `model` | string | 是 | 固定填写 `volc-asset-group-create`。 |
| `input` | string | 是 | 仅用于通过 DMXAPI 平台入口的通用校验，固定填写 `validate`。 |
| `Name` | string | 是 | 素材组名称，最多 64 个字符。 |
| `Description` | string | 否 | 素材组描述，最多 300 个字符。 |
| `GroupType` | string | 否 | 当前仅支持 `AIGC`，建议显式填写。 |
| `ProjectName` | string | 是 | 项目名称固定填写 `shuyuan`，请勿更改。 |

### 示例代码

```python
import json
import requests


url = "https://www.dmxapi.cn/v1/responses"
api_key = "sk-**********************************"

headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {api_key}",
}

payload = {
    # 【model】(string, 必填) 固定为 volc-asset-group-create
    "model": "volc-asset-group-create",

    # 【input】(string, 必填) 仅用于通过 DMXAPI 平台入口的通用校验
    "input": "validate",

    # 【Name】(string, 必填) 虚拟人素材组名称，最多 64 个字符
    "Name": "virtual-host-xiaomiao",

    # 【Description】(string, 选填) 素材组描述，最多 300 个字符
    "Description": "小妙虚拟主播的素材",

    # 【GroupType】(string, 选填) 当前仅支持 AIGC
    "GroupType": "AIGC",

    # 【ProjectName】(string, 必填) 项目名固定为 shuyuan，请勿更改
    "ProjectName": "shuyuan",
}

response = requests.post(
    url,
    headers=headers,
    json=payload,
    timeout=60,
)

print(response.status_code)
print(json.dumps(response.json(), indent=2, ensure_ascii=False))
```

## 返回示例

```json
{
  "Id": "group-20260811093000-abcde"
}
```

### 说明

- 返回的 `Id` 是素材组 ID，形如 `group-...`，请立即保存。
- 步骤二请求里的字段名是 `GroupId`，直接填写这里返回的 `Id` 即可。
- 一个素材组可以存放同一个虚拟人物的多份图片、视频或音频素材。
- `ProjectName` 必须保持为 `shuyuan`，后续上传、查询和生成都要处于同一项目。


## 步骤二：上传虚拟人素材（volc-asset-create）

用步骤一拿到的素材组 ID，上传一张图片、一段视频或一段音频。每次请求只能上传一个素材文件，文件必须先放在火山服务能够直接访问的公网 URL 中。

本接口是异步接口。返回素材 `Id` 后，还不能立即生成视频，必须继续执行步骤三，等 `Status` 变为 `Active`。

### 素材格式要求

:::tip 图片素材

- 格式：jpeg、jpg、png、webp、bmp、tiff、gif、heic/heif
- 大小：小于 30 MB
- 宽高比（宽/高）：`(0.4, 2.5)`
- 宽、高长度：`(300, 6000)` px
:::

:::tip 视频素材

- 格式：mp4、mov
- 素材库入库支持 2～30 秒；用于 Seedance 2.0 时建议控制在 2～15 秒
- Seedance 2.0 单次请求中的所有参考视频总时长不能超过 15 秒
:::

:::tip 音频素材

- 格式：wav、mp3
- 大小：不超过 15 MB
- 素材库入库支持 2～30 秒；用于 Seedance 2.0 时建议控制在 2～15 秒
:::

### 示例代码

```python
import json
import requests


url = "https://www.dmxapi.cn/v1/responses"
api_key = "sk-**********************************"

headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {api_key}",
}

payload = {
    # 【model】(string, 必填) 固定为 volc-asset-create
    "model": "volc-asset-create",

    # 【input】(string, 必填) 仅用于通过 DMXAPI 平台入口的通用校验
    "input": "validate",

    # 【GroupId】(string, 必填) 填写步骤一返回的素材组 Id
    "GroupId": "group-20260811093000-abcde",

    # 【URL】(string, 必填) 素材的公网可访问 URL，不支持本地路径或 Base64
    "URL": "https://example.com/virtual-host/front-view.png",

    # 【AssetType】(string, 必填) Image / Video / Audio 三选一
    "AssetType": "Image",

    # 【Name】(string, 选填) 便于管理和检索的素材名称
    "Name": "front-view",

    # 【ProjectName】(string, 必填) 必须与创建素材组时一致
    "ProjectName": "shuyuan",
}

response = requests.post(
    url,
    headers=headers,
    json=payload,
    timeout=60,
)

print(response.status_code)
print(json.dumps(response.json(), indent=2, ensure_ascii=False))
```

## 返回示例

```json
{
  "Id": "asset-20260811101530-fghij"
}
```

### 说明

- 返回的 `Id` 是素材 ID，形如 `asset-...`，请立即保存。
- `URL` 必须是公网可访问地址；本接口不接收本地文件路径或 Base64。
- 每次请求只上传一个素材，需要上传多份素材时，请分别调用多次。
- 上传成功仅代表已经创建异步处理任务，不代表素材已经可用于 Seedance。
- 下一步使用这里返回的素材 `Id` 调用 `volc-asset-get`。



## 步骤三：查询素材状态（volc-asset-get）

素材入库是异步的。调用本接口轮询素材 `Id` 的 `Status`：

- `Processing`：素材仍在处理，等待 30 秒后继续查询。
- `Active`：素材已经可用，可以进入步骤四生成视频。
- `Failed`：素材处理或安全审核失败，不能用于生成；请检查素材后重新上传。

### 示例代码

```python
import json
import time
import requests


url = "https://www.dmxapi.cn/v1/responses"
api_key = "sk-**********************************"

headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {api_key}",
}

payload = {
    # 【model】(string, 必填) 固定为 volc-asset-get
    "model": "volc-asset-get",

    # 【input】(string, 必填) 仅用于通过 DMXAPI 平台入口的通用校验
    "input": "validate",

    # 【Id】(string, 必填) 填写步骤二返回的素材 Id
    "Id": "asset-20260811101530-fghij",

    # 【ProjectName】(string, 必填) 必须与创建和上传素材时一致
    "ProjectName": "shuyuan",
}

while True:
    response = requests.post(
        url,
        headers=headers,
        json=payload,
        timeout=60,
    )
    result = response.json()
    status = result.get("Status")

    if status == "Active":
        print("素材已可用：")
        print(json.dumps(result, indent=2, ensure_ascii=False))
        break

    if status == "Failed":
        print("素材处理失败：")
        print(json.dumps(result, indent=2, ensure_ascii=False))
        break

    if status == "Processing":
        print("素材仍在处理，30 秒后继续查询……")
        time.sleep(30)
        continue

    print("收到未预期的返回：")
    print(json.dumps(result, indent=2, ensure_ascii=False))
    break
```

## 返回示例

```json
{
  "Id": "asset-20260811101530-fghij",
  "Name": "front-view",
  "URL": "https://ark-media-asset.example.com/virtual-host/front-view.png",
  "AssetType": "Image",
  "GroupId": "group-20260811093000-abcde",
  "Status": "Active",
  "Moderation": {
    "Strategy": "Default"
  },
  "CreateTime": "2026-08-11T02:15:30Z",
  "UpdateTime": "2026-08-11T02:15:35Z",
  "ProjectName": "shuyuan"
}
```

### 说明

- 只有 `Status=Active` 的素材才能使用。
- 返回的 `URL` 可能是临时下载地址，不要把它当作长期素材标识保存。
- 生成视频时使用的是素材 `Id`，不是这里返回的 `URL`。
- 正确写法为 `asset://asset-20260811101530-fghij`。





### 使用限制与合规要求

- 本流程创建的是私域**虚拟人像**素材组，当前 `GroupType` 仅支持 `AIGC`。
- 虚拟人物不得与任何自然人肖像或形象雷同；真人必须使用已授权真人扫脸流程。
- 调用方应合法拥有上传素材，并确保素材不侵犯第三方的人格权、商标权、著作权等合法权益。
- 创建素材组不代表素材已经可用；每份素材仍需经过预处理和安全审核。
- 只有 `volc-asset-get` 返回 `Status=Active` 的素材才能用于 Seedance 推理。
- `volc-asset-create` 只接收公网 URL，不接收本地文件路径或 Base64。

### 常见问题

### 返回的是 Id，为什么下一步参数叫 GroupId？

`volc-asset-group-create` 的响应字段名是 `Id`，表示素材组 ID；`volc-asset-create` 的请求字段名是 `GroupId`。把前一步返回的值原样填入即可：

```text
步骤一返回：Id = group-xxx
步骤二填写：GroupId = group-xxx
```

### 创建素材组后能直接生成视频吗？

不能。素材组只是管理容器，还要执行步骤二上传素材，并执行步骤三等待素材状态变为 `Active`。

### 一个素材组可以放多份素材吗？

可以。建议把同一个虚拟人物的全身图、人脸特写、视频和音频素材放入同一个素材组，方便持续管理和调用。

### 可以直接上传本地文件或 Base64 吗？

不可以。`volc-asset-create` 接收的是公网可访问 URL。本地文件应先上传到对象存储或其他公网文件服务。

### 平台预置虚拟人也需要创建素材组吗？

不需要。平台预置虚拟人已经带有可用的 Asset ID，可以直接在 Seedance 请求中使用。`volc-asset-group-create` 用于您自行上传和管理的私域虚拟人物。

### 这个流程会修改 Seedance 的生成参数吗？

不会。Seedance 生成逻辑保持不变，只需在 `input` 数组对应条目的 `<模态>_url.url` 中填写 `asset://<素材 Id>`。



<p align="center">
  <small>© 2026 DMXAPI Seedance 2.0 私域虚拟人接入全流程</small>
</p>
