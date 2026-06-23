# Seedance 2.0 真人方案三 接入全流程（扫脸建档 → 素材入库）

火山「真人私域素材库」能把一个**真实人物**建成可反复调用的「虚拟人像档案」：建档一次，之后用 Seedance 2.0 等模型生成视频时，只要用 `asset://` 引用这个人的素材，就能稳定生成同一个人的视频。

整套接入要做两件事，分成 **2 个阶段、共 4 步**：

- **阶段一 · 扫脸建档**：让真人扫脸做活体核验，换到这个人的**档案号 `GroupId`**（步骤一拿扫脸网页，步骤二换档案号）。`GroupId` 是这个人的唯一身份，建档一次即可长期复用。
- **阶段二 · 素材入库**：把这个人的图 / 视频 / 音频素材挂进档案，拿到可用的**素材号 `Id`**（步骤三提交素材，步骤四轮询到 `Active`）。入库时系统会拿素材和扫脸的人脸比对，确保是本人。

一句话：**扫脸建档拿到「人」(GroupId) → 往档案塞「素材」(Id) → 等素材审核通过(Active) → 用素材号生成视频。**

:::danger 重要：所有 ID 请务必自己保存，丢失无法找回
本流程会产生两类需要你**自行长期保存**的 ID，平台不提供找回，一旦丢失即永久丢失、无法恢复：

- **档案号 `GroupId`**（步骤二返回）—— 某个真人的唯一身份；丢失只能让本人重新扫脸建档。
- **素材号 `Id`**（步骤三返回，形如 `asset-...`）—— 生成视频时用 `asset://<Id>` 引用；丢失需重新上传素材入库。

建议拿到后**立刻记录到自己的数据库 / 表格**，并与对应的真人、项目名（`ProjectName`）一一对应保存好。
:::

## 流程总览

```text
阶段一 · 扫脸建档
═══════════════════

步骤一 · 要扫脸网页 —— 调 volc-visual-validate-create
        得到 H5Link（扫脸网页）+ BytedToken
   │
   ▼
真人扫脸 —— 用手机 / 带摄像头的电脑打开 H5Link，做活体识别
        H5Link 120 秒内有效；通过后浏览器回跳，网址尾部带回 bytedToken
        超时 / 失败 → 回「步骤一」重新生成链接
   │
   ▼
步骤二 · 换档案号 —— 调 volc-visual-validate-result（带 bytedToken）
        得到 GroupId（档案号，务必保存，丢失无法找回）


阶段二 · 素材入库
═══════════════════

步骤三 · 素材入库 —— 调 volc-asset-create（带 GroupId + 素材公网URL + 类型）
        得到 Id（素材号）
   │
   ▼
步骤四 · 查素材状态 —— 调 volc-asset-get（带 Id），每 30 秒轮询 Status
        Processing 继续等  ·  Failed 换图重传回「步骤三」  ·  Active 完成
   │
   ▼
完成 —— 用 asset://<Id> 引用该真人生成视频
```

## 接口一览

| 阶段 | 步骤 | 功能 | `model` | 请求方式 | URL |
|------|------|------|---------|---------|-----|
| 扫脸建档 | 步骤一 | 要扫脸网页（CreateVisualValidateSession） | `volc-visual-validate-create` | POST | `https://www.dmxapi.cn/v1/responses` |
| 扫脸建档 | 步骤二 | 换档案号（GetVisualValidateResult） | `volc-visual-validate-result` | POST | `https://www.dmxapi.cn/v1/responses` |
| 素材入库 | 步骤三 | 素材入库（CreateAsset） | `volc-asset-create` | POST | `https://www.dmxapi.cn/v1/responses` |
| 素材入库 | 步骤四 | 查素材状态（GetAsset） | `volc-asset-get` | POST | `https://www.dmxapi.cn/v1/responses` |

---

## 步骤一：要扫脸网页（volc-visual-validate-create）

调本接口拿到「扫脸网页 `H5Link`」，把 `H5Link` 发给真人去扫脸；识别通过后浏览器会跳回你设的 `CallbackURL`，并在网址尾巴带上 `bytedToken`，下一步用它换档案号。

> **扫脸前必读**：`H5Link` 必须用**手机**或**带摄像头的电脑**打开——页面要调用摄像头做**活体人脸识别**（真人按提示完成动作核验），无摄像头的设备无法完成。**注意时效：`H5Link` 有效期仅 120 秒，下发后请尽快打开并完成扫脸，过期需重新调用本接口生成新链接。**

### 示例代码

```python
import requests
import json


url = "https://www.dmxapi.cn/v1/responses"
api_key = "sk-****************************************"
headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {api_key}",
}

payload = {
    # 【model】(string, 必填) 固定为 volc-visual-validate-create
    "model": "volc-visual-validate-create",
    # 【CallbackURL】(string, 必填) 你的回调网址；真人扫脸完成后浏览器跳回此地址，
    # 并在网址 query 上带回 bytedToken、resultCode（resultCode=10000 表示通过）。
    "CallbackURL": "https://www.dmxapi.cn/callback",
    # 【ProjectName】项目名为ltyzs，请勿更改，
    "ProjectName": "ltyzs",
}

response = requests.post(url, headers=headers, json=payload)
print(response.status_code)
print(json.dumps(response.json(), indent=2, ensure_ascii=False))
```

## 返回示例

```json
200
{
  "BytedToken": "20260...B5B813",
  "H5Link": "https://h5-v2.kyaccess....055FB813&lng=zh",
  "CallbackURL": "https://www.dmxapi.cn/callback"
}
```

### 说明

- **务必留好扫完脸后回跳链接尾部的 `bytedToken`**：扫脸完成后浏览器跳回 `你的回调?bytedToken=***&resultCode=10000&...`，`resultCode=10000` 表示通过；**这个回跳链接同样有时效，请第一时间把网址尾部的 `bytedToken` 复制留存**，紧接着用于步骤二换档案号，过期需重新扫脸。


## 步骤二：换档案号（volc-visual-validate-result）

真人扫脸通过后，从回跳网址里读到 `bytedToken`，调本接口换取这个真人的「档案号 `GroupId`」。建档完成后，下一步用这个 `GroupId` 往档案里传素材。`bytedToken` 有效期 120 秒，要尽快用。

### 示例代码

```python
import requests
import json

url = "https://www.dmxapi.cn/v1/responses"
api_key = "sk-*********************************"

headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {api_key}",
}

payload = {
    # 【model】(string, 必填) 固定为 volc-visual-validate-result
    "model": "volc-visual-validate-result",
    # 【BytedToken】(string, 必填) 第 1 步扫脸回跳网址里读到的bytedToken，有效期 120 秒，要尽快用
    "BytedToken": "20260618131...089A",
    # 【ProjectName】(string, 选填) 项目名为ltyzs，请勿更改
    "ProjectName": "ltyzs",
}

response = requests.post(url, headers=headers, json=payload)
print(response.status_code)
print(json.dumps(response.json(), indent=2, ensure_ascii=False))
```

## 返回示例

```json
200
{
  "GroupId": "group-20260....-v6stv"
}
```

### 说明

- **`GroupId` 必须自己妥善保留**：它（形如 `group-...`）是这个真人的档案号，**系统不提供找回，一旦丢失无法恢复**，只能重新扫脸建档；请务必记录保存，下一步入库以及以后给这个人加素材都要用。
- 一次扫脸反复用：以后给这个人加新素材，直接往同一 `GroupId` 里传，不必再扫脸。

## 步骤三：素材入库（volc-asset-create）

用第 2 步拿到的档案号 `GroupId`，把一张图 / 一段视频 / 一段音频的公网地址传进档案。本接口是异步的，返回素材号 `Id` 后，要用下一步轮询直到状态变 `Active` 才算入库成功、可用于生成视频。每次请求传一个素材文件。

### 示例代码

```python
import requests
import json

url = "https://www.dmxapi.cn/v1/responses"
api_key = "sk-***********************************"

headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {api_key}",
}

payload = {
    # 【model】(string, 必填) 固定为 volc-asset-create
    "model": "volc-asset-create",
    # 【GroupId】(string, 必填) 素材组合 ID（档案号），即第 2 步拿到的 group-...，决定素材塞进哪个档案
    "GroupId": "group-20260....v6stv",
    # 【URL】(string, 必填) 图片/视频/音频可访问的公网 URL，系统会去这里下载素材
    "URL": "https://image.dmxapi.cn/thumbn......cf6c25837.png",
    # 【AssetType】(string, 必填) 素材类型，三选一
    # 可选值: "Image"(图片) / "Video"(视频) / "Audio"(音频)
    "AssetType": "Image",
    # 【Name】(string, 选填) 素材名称
    "Name": "test",
    # 【ProjectName】项目名为ltyzs，请勿更改
    "ProjectName": "ltyzs",
}
response = requests.post(url, headers=headers, json=payload)
print(json.dumps(response.json(), indent=2, ensure_ascii=False))
```

## 返回示例

```json
{
  "Id": "asset-20260318******-*****"
}
```

### 说明

- 入库有门槛：系统会拿传入的图与扫脸的人脸比对，不是同一人 / 一图多脸 → 入库失败（状态 `Failed`）。建议传清晰、单人、正面的素材。
- 返回的 `Id`（形如 `asset-...`）是素材号；生成视频时套上 `asset://` 前缀使用（`asset://asset-...`）。



## 步骤四：查素材状态（volc-asset-get）

素材入库是异步的，调本接口轮询素材号的 `Status`——`Processing` 还在处理（过 30 秒再查）、`Active` 好了能用、`Failed` 处理失败。状态变 `Active` 后即可用该素材号生成视频。

### 示例代码

```python
import requests
import json
import time

url = "https://www.dmxapi.cn/v1/responses"
api_key = "sk-****************************************"

headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {api_key}",
}

payload = {
    # 【model】(string, 必填) 固定为 volc-asset-get
    "model": "volc-asset-get",
    # 【Id】(string, 必填) 要查询的素材资产 ID，即第 3 步返回的 asset-...
    "Id": "asset-2026....wsbcl",
    # 【ProjectName】项目名为ltyzs，请勿更改
    "ProjectName": "ltyzs",
}

# 轮询直到 Active / Failed
while True:
    r = requests.post(url, headers=headers, json=payload).json()
    status = r.get("Status")
    if status == "Active":
        print("可用：", json.dumps(r, indent=2, ensure_ascii=False)); break
    if status == "Failed":
        print("失败：", r); break
    print(f"还在处理（{status}），30 秒后再查"); time.sleep(30)
```

## 返回示例

```json
可用： {
  "Id": "asset-202606.......bcl",
  "Name": "wen",
  "URL": "https://ark-media-asset.to........ers=host",
  "AssetType": "Image",
  "GroupId": "group-20260.......stv",
  "Status": "Active",
  "Moderation": {
    "Strategy": "Default"
  },
  "CreateTime": "2026-06-18T05:31:02Z",
  "UpdateTime": "2026-06-18T05:31:05Z",
  "ProjectName": "shuyuan"
}
```

### 说明

- `Status`：`Active` 可用 / `Processing` 处理中 / `Failed` 失败（多半没过人脸比对）。
- 返回的 `URL` 是临时下载链接，约 12 小时（`X-Tos-Expires=43200`）后失效。
- 拿到 `Status=Active` 后，即可在生成视频时以 `asset://<素材号 Id>` 引用该真人素材。

<p align="center">
  <small>© 2026 DMXAPI 火山真人私域素材库 扫脸建档与素材入库全流程</small>
</p>
