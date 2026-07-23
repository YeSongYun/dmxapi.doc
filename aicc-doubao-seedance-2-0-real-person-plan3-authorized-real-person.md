# AICC-Doubao-Seedance-2.0 真人方案三 接入全流程（扫脸建组 → 素材入库）

「真人私域素材库」能把一个**真实人物**建成可反复调用的「虚拟人像档案」：建档一次，之后用 AICC-Doubao-Seedance-2.0 生成视频时，只要用 `asset://` 引用这个人的素材，就能稳定生成同一个人的视频。

整套接入分成 **2 个阶段、共 4 步**：

- **阶段一 · 扫脸建组**：让真人扫脸做活体核验，扫完后**在页面上当场建档**，程序侧再查回这个人的**档案号 `GroupId`**（步骤一拿扫脸网页，步骤二查档案号）。`GroupId` 是这个人的唯一身份，建档一次即可长期复用。
- **阶段二 · 素材入库**：把这个人的图 / 视频 / 音频素材挂进档案，拿到可用的**素材号 `Id`**（步骤三提交素材，步骤四轮询到 `ACTIVE`）。入库时系统会拿素材和扫脸的人脸比对，确保是本人。

一句话：**扫脸建档拿到「人」(GroupId) → 往档案塞「素材」(Id) → 等素材审核通过(ACTIVE) → 用素材号生成视频。**

:::tip 扫完脸当场建档
认证成功后，扫脸页面会让本人直接填写**资产组名称**（必填，最长 64 字）和**描述**（选填，最长 300 字）并提交，提交后页面直接显示档案号（`group-xxx`）；步骤二只是程序侧拿到同一个档案号的途径，无需依赖用户抄写屏幕。
:::

:::danger 重要：所有 ID 请务必自己保存，丢失无法找回
本流程会产生两类需要你**自行长期保存**的 ID，平台不提供找回，一旦丢失即永久丢失、无法恢复：

- **档案号 `GroupId`**（步骤二返回，扫脸页面上也会显示）—— 某个真人的唯一身份；丢失只能让本人重新扫脸建档。
- **素材号 `Id`**（步骤三返回，形如 `asset-...`）—— 生成视频时用 `asset://<Id>` 引用；丢失需重新上传素材入库。

建议拿到后**立刻记录到自己的数据库 / 表格**，并与对应的真人一一对应保存好。
:::

## 流程总览

```text
阶段一 · 扫脸建组
═══════════════════

步骤一 · 要扫脸网页 —— 调 aicc-visual-validate-create
        直接返回 h5Link（扫脸网页）+ BytedToken（认证Token）
   │
   ▼
真人扫脸建档 —— 用手机打开 h5Link，完成活体识别；
        认证成功后在页面上填写资产组名称（必填）与描述（选填）并提交，
        页面即显示档案号（group-xxx）
        超时 / 失败 → 回「步骤一」重新生成链接
   │
   ▼
步骤二 · 查档案号 —— 调 aicc-visual-validate-result（带 BytedToken）
        得到 GroupId（与页面显示的一致；务必保存，丢失无法找回）


阶段二 · 素材入库
═══════════════════

步骤三 · 素材入库 —— 调 aicc-asset-create（带 GroupId + 素材公网URL + 类型）
        得到 Id（素材号）
   │
   ▼
步骤四 · 查素材状态 —— 调 aicc-asset-get（带 Id），每 30 秒轮询 status
        PROCESSING 继续等  ·  FAILED 换图重传回「步骤三」  ·  ACTIVE 完成
   │
   ▼
完成 —— 用 asset://<Id> 引用该真人生成视频
```

## 接口一览

| 阶段 | 步骤 | 功能 | `model` | 请求方式 | URL |
|------|------|------|---------|---------|-----|
| 扫脸建组 | 步骤一 | 要扫脸网页（创建H5认证会话） | `aicc-visual-validate-create` | POST | `https://www.dmxapi.cn/v1/responses` |
| 扫脸建组 | 步骤二 | 查档案号（bytedToken换素材组） | `aicc-visual-validate-result` | POST | `https://www.dmxapi.cn/v1/responses` |
| 素材入库 | 步骤三 | 素材入库（创建素材） | `aicc-asset-create` | POST | `https://www.dmxapi.cn/v1/responses` |
| 素材入库 | 步骤四 | 查素材状态（查询素材详情） | `aicc-asset-get` | POST | `https://www.dmxapi.cn/v1/responses` |

---

## 步骤一：要扫脸网页（aicc-visual-validate-create）

调本接口拿到「扫脸网页 `h5Link`」和「认证 Token `bytedToken`」，把 `h5Link` 发给真人去扫脸；`bytedToken` 由你的程序留存，扫脸完成后用它换档案号（步骤二）。

> **扫脸前必读**：`h5Link` 必须用**手机**打开——页面要调用摄像头做**活体人脸识别**（真人按提示完成动作核验）。**注意时效：接口返回的 `expiresIn` 为 120（秒），有效期较短，下发后请尽快打开并完成扫脸，过期需重新调用本接口生成新链接。**认证成功后，页面会让本人填写**资产组名称**（必填）与**描述**（选填）并提交建档，页面直接显示档案号。

### 示例代码

```python
import requests
import json

url = "https://www.dmxapi.cn/v1/responses"
api_key = "sk-**********************************"
headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {api_key}",
}

payload = {
    # 【model】(string, 必填) 固定为 aicc-visual-validate-create
    "model": "aicc-visual-validate-create",
    # 【input】(必填) 仅为通过 dmxapi 平台入口的通用校验，后端不使用，保持该值即可
    "input": "validate",
}

response = requests.post(url, headers=headers, json=payload)
print(response.status_code)
print(json.dumps(response.json(), indent=2, ensure_ascii=False))
```

## 返回示例

```json
200
{
  "bytedToken": "202607221154048C61BAEE......A944F2",
  "h5Link": "https://ark.volcengine.com/region:cn-beijing/mobile/livenees-face-manage/authorization?pl=krPqBw......&uid=0b806b14-......",
  "expiresIn": 120
}
```

### 说明

- **`bytedToken` 由程序留存**：它直接在本接口响应里返回（无需配置回调、无需从任何网址里抠），扫脸完成后紧接着用于步骤二查档案号。
- **`h5Link` 发给真人**：复制到手机端打开完成活体检测；认证成功后本人在页面上填资产组名称 / 描述提交，页面即显示档案号 `group-xxx`。
- 一次会话对应一个人：并发给多人建档时，每人单独调一次本接口，各自的 `bytedToken` 对应各自的档案，不会串。


## 步骤二：查档案号（aicc-visual-validate-result）

真人扫脸并在页面提交建档后，用步骤一留存的 `BytedToken` 调本接口，程序侧拿到这个真人的「档案号 `GroupId`」（与扫脸页面显示的一致）。建档完成后，下一步用这个 `GroupId` 往档案里传素材。`bytedToken` 有效期较短，扫脸完成后要尽快调用。

### 示例代码

```python
import requests
import json

url = "https://www.dmxapi.cn/v1/responses"
api_key = "sk-********************************"

headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {api_key}",
}

payload = {
    # 【model】(string, 必填) 固定为 aicc-visual-validate-result
    "model": "aicc-visual-validate-result",
    # 【input】(必填) 仅为通过 dmxapi 平台入口的通用校验，后端不使用，保持该值即可
    "input": "validate",
    # 【BytedToken】(string, 必填) 步骤一响应里返回的 bytedToken，扫脸完成后尽快使用
    "BytedToken": "202607221154048C61BAEE......A944F2",
}

response = requests.post(url, headers=headers, json=payload)
print(response.status_code)
print(json.dumps(response.json(), indent=2, ensure_ascii=False))
```

## 返回示例

```json
200
{
  "GroupId": "group-20260722121343-v5vtp"
}
```

### 说明

- **`GroupId` 必须自己妥善保留**：它（形如 `group-...`）是这个真人的档案号，**系统不提供找回，一旦丢失无法恢复**，只能重新扫脸建档；请务必记录保存，下一步入库以及以后给这个人加素材都要用。
- 一次扫脸反复用：以后给这个人加新素材，直接往同一 `GroupId` 里传，不必再扫脸。

## 步骤三：素材入库（aicc-asset-create）

用步骤二拿到的档案号 `GroupId`，把一张图 / 一段视频 / 一段音频的公网地址传进档案。本接口是异步的，返回素材号 `Id` 后，要用步骤四轮询直到状态变 `ACTIVE` 才算入库成功、可用于生成视频。每次请求传一个素材文件。

### 素材格式要求

::: tip 图片素材
- 格式：jpeg, jpg, png, webp, gif, heic
- 大小：小于30MB
- 宽高比（宽/高）：(0.4, 2.5)
- 宽高长度（px）：(300, 6000)
:::

::: tip 视频素材
- 格式：mp4，mov
- 大小：不超过50MB
- 时长：[2, 15]s
- 帧率：[24, 60]
- 宽高比（宽/高）：[0.4, 2.5]
- 宽高长度（px）：[300, 6000]
- 画面像素（宽 × 高）：[409600, 927408]
:::

::: tip 音频素材
- 格式：mp3，wav
- 大小：不超过15MB
- 时长：[2,15]s
:::

### 示例代码

```python
import requests
import json

url = "https://www.dmxapi.cn/v1/responses"
api_key = "sk-**********************************"

headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {api_key}",
}

payload = {
    # 【model】(string, 必填) 固定为 aicc-asset-create
    "model": "aicc-asset-create",
    # 【input】(必填) 仅为通过 dmxapi 平台入口的通用校验，后端不使用，保持该值即可
    "input": "validate",
    # 【GroupId】(string, 必填) 档案号，即步骤二拿到的 group-...，决定素材塞进哪个档案
    "GroupId": "group-20260722121343-v5vtp",
    # 【URL】(string, 必填) 图片/视频/音频可访问的公网 URL，系统会去这里下载素材
    "URL": "https://image.dmxa.......................052e6b4b03.png",
    # 【AssetType】(string, 必填) 素材类型，三选一
    # 可选值: "Image"(图片) / "Video"(视频) / "Audio"(音频)
    "AssetType": "Image",
    # 【Name】(string, 选填) 素材名称，最长 64 个字符
    "Name": "test",
}
response = requests.post(url, headers=headers, json=payload)
print(json.dumps(response.json(), indent=2, ensure_ascii=False))
```

## 返回示例

```json
{
  "Id": "asset-20260722******-*****"
}
```

### 说明

- 入库有门槛：系统会拿传入的素材与扫脸的人脸比对，不是同一人 / 一图多脸 → 入库失败（状态 `FAILED`）。建议传清晰、单人、正面的素材。
- 返回的 `Id`（形如 `asset-...`）是素材号；生成视频时套上 `asset://` 前缀使用（`asset://asset-...`）。
- 单个用户素材数量上限 10000。



## 步骤四：查素材状态（aicc-asset-get）

素材入库是异步的，调本接口轮询素材号的 `status`——`PROCESSING` 还在处理（过 30 秒再查）、`ACTIVE` 好了能用、`FAILED` 处理失败（`errorMessage` 为失败原因）。状态变 `ACTIVE` 后即可用该素材号生成视频。

### 示例代码

```python
import requests
import json
import time

url = "https://www.dmxapi.cn/v1/responses"
api_key = "sk-**********************************"

headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {api_key}",
}

payload = {
    # 【model】(string, 必填) 固定为 aicc-asset-get
    "model": "aicc-asset-get",
    # 【input】(必填) 仅为通过 dmxapi 平台入口的通用校验，后端不使用，保持该值即可
    "input": "validate",
    # 【Id】(string, 必填) 要查询的素材号，即步骤三返回的 asset-...
    "Id": "asset-20260722******-*****",
}

# 轮询直到 ACTIVE / FAILED（注意状态为全大写）
while True:
    r = requests.post(url, headers=headers, json=payload).json()
    status = r.get("status")
    if status == "ACTIVE":
        print("可用：", json.dumps(r, indent=2, ensure_ascii=False)); break
    if status == "FAILED":
        print("失败：", r.get("errorMessage"), r); break
    print(f"还在处理（{status}），30 秒后再查"); time.sleep(30)
```

## 返回示例

```json
可用： {
  "assetId": "asset-20260722******-*****",
  "groupId": "group-20260722121343-v5vtp",
  "assetName": "test",
  "assetType": "Image",
  "url": "https://ark-media-asset.to........ers=host",
  "status": "ACTIVE",
  "errorMessage": "",
  "createTime": "2026-07-22 12:20:01",
  "updateTime": "2026-07-22 12:20:05"
}
```

### 说明

- `status`：`ACTIVE` 可用 / `PROCESSING` 处理中 / `FAILED` 失败（多半没过人脸比对，`errorMessage` 为具体原因）。**注意状态值为全大写**。
- 返回的 `url` 是临时下载链接，约 12 小时后失效。
- 拿到 `status=ACTIVE` 后，即可在 AICC-Doubao-Seedance-2.0 生成视频时以 `asset://<素材号 Id>` 引用该真人素材。

<p align="center">
  <small>© 2026 DMXAPI 移动云真人私域素材库 扫脸建档与素材入库全流程</small>
</p>
