# Meshy-7.1 单图生 3D API 使用文档

基于 Meshy 7.1 模型的单图生成 3D 接口，通过 DMXAPI 网关（Meshy Task Plugin）以异步任务方式调用：先提交一张公开可访问的图片 URL 创建生成任务，再用返回的任务 ID 查询生成结果。模型支持输出 glb、obj、fbx、stl、usdz、3mf 格式的 3D 文件，可选生成纹理与 PBR 贴图；单图输入支持 standard、2k、4k 三档几何分辨率。单图与多图生成 3D 通过接口与输入字段区分（单图 `/meshy/v1/image-to-3d` 传 `image_url`，多图 `/meshy/v1/multi-image-to-3d` 传 `image_urls`），本文档对应单图输入。

## 接口地址

| 接口 | 请求方式 | URL |
|------|---------|-----|
| 提交任务 | POST | `https://test.dmxapi.vip/meshy/v1/image-to-3d` |
| 查询任务 | GET | `https://test.dmxapi.vip/meshy/v1/image-to-3d/{task_id}` |

:::warning
请妥善保管您的 dmx-api API Key！严禁将密钥泄露给他人、硬编码到公开可见的代码中或提交到公开的代码仓库。如怀疑密钥已泄露，请立即更换密钥。
:::

## 模型名称

- `meshy-7.1`

## 单图生成 3D 示例代码

```python
import requests


# ===============================================================
# 步骤1: 配置 API 连接信息
# ===============================================================

# dmx-api 网关地址
BASE_URL = "https://test.dmxapi.vip"

# dmx-api API Key (请替换为您自己的密钥)
API_KEY = "sk-***********************************************"

# 单图生成 3D 创建接口
CREATE_URL = f"{BASE_URL}/meshy/v1/image-to-3d"

# ===============================================================
# 步骤2: 配置请求头
# ===============================================================

headers = {
    # Meshy API 鉴权
    "Authorization": f"Bearer {API_KEY}",
    # POST JSON 请求需要这个请求头
    "Content-Type": "application/json",
}

# ===============================================================
# 步骤3: 配置请求参数
# ===============================================================

payload = {
    # 【image_url】(string, 必填) 公开可访问的图片 URL
    # 格式支持 jpg、jpeg、png、webp，最大 20 MB
    "image_url": "https://your-cdn.example.com/source-image.png",

    # 【ai_model】(string) 模型 ID，固定使用 Meshy 7.1
    "ai_model": "meshy-7.1",

    # 【geometry_resolution】(string) 几何分辨率
    # standard：普通几何分辨率
    # 2k：Ultra geometry 2K
    # 4k：Ultra geometry 4K
    # 注意：参数值中没有 ultra，使用 2k 或 4k 表示 Ultra
    "geometry_resolution": "standard",

    # 【should_texture】(bool) 是否生成纹理
    # True：生成模型和纹理
    # False：只生成模型形状，不生成纹理
    "should_texture": False,

    # 【enable_pbr】(bool) 是否生成 PBR 纹理
    # 生成 metallic、roughness、normal 等 PBR 纹理
    # 只有 should_texture=True 时才有意义
    "enable_pbr": False,

    # 【texture_resolution】(string) 纹理分辨率
    # 可选值：2k、4k、8k
    "texture_resolution": "2k",

    # 【target_formats】(array[string]) 输出文件格式
    # 可选值：glb、obj、fbx、stl、usdz、3mf
    "target_formats": ["glb"],
}

# ===============================================================
# 步骤4: 发送请求并输出结果
# ===============================================================

# 发送 POST 请求到 API 服务器
response = requests.post(
    CREATE_URL,
    headers=headers,
    json=payload,
    timeout=60,
)

# 如果返回 400、401、402、429 等错误，这里会抛出异常
response.raise_for_status()

try:
    result = response.json()
except ValueError as error:
    preview = response.text[:500].replace("\n", " ")
    raise RuntimeError(
        f"网关返回的不是 JSON：HTTP {response.status_code}，"
        f"响应内容={preview!r}"
    ) from error

# 创建成功同时返回 task_id（网关任务 ID）与 result（Meshy 原生 UUID）
# 查询接口只认 task_id（用 result 查询会 404），示例代码优先取 task_id
task_id = result.get("task_id") or result.get("result")
if not task_id:
    raise RuntimeError(f"Meshy 返回中没有任务 ID：{result}")

print("3D 任务创建成功")
print("task_id:", task_id)
```

## 单图生成 3D 返回示例

```json
{
  "result": "01a13e69-1d54-76f0-8610-15c78e334886",
  "task_id": "task_DzbvlJnVWj79wk0yqyoDYENOK0mKSACs"
}
```

创建成功返回任务 ID：`task_id` 与 `result` 两个键同时返回且取值不同，`result` 为 Meshy 原生 UUID，`task_id` 为网关任务 ID。查询接口只认 `task_id`（用 `result` 查询会返回 404），示例代码优先取 `task_id`。后续查询使用该任务 ID。

## 获取生成结果示例代码

```python
import time

import requests


# ===============================================================
# 步骤1: 配置 API 连接信息
# ===============================================================

# dmx-api 网关地址
BASE_URL = "https://test.dmxapi.vip"

# dmx-api API Key (请替换为您自己的密钥)
API_KEY = "sk-***********************************************"

# 填写创建任务接口返回的 dmx-api 任务 ID
TASK_ID = "task_S1n2G3l4E5t6A7s8K9i0D1f2G3h4J5k6"

# 单图生成 3D 查询地址（任务 ID 位于 URL 路径中）
query_url = f"{BASE_URL}/meshy/v1/image-to-3d/{TASK_ID}"

# ===============================================================
# 步骤2: 配置请求头
# ===============================================================

headers = {
    # Meshy API 鉴权
    "Authorization": f"Bearer {API_KEY}",
}

# ===============================================================
# 步骤3: 轮询任务，直到任务成功、失败或取消
# ===============================================================


def read_json_response(response):
    """读取网关返回；若上游返回 HTML/纯文本，输出状态和响应摘要。"""
    content_type = response.headers.get("Content-Type", "")
    try:
        return response.json()
    except ValueError as error:
        preview = response.text[:500].replace("\n", " ")
        raise RuntimeError(
            f"网关返回的不是 JSON：HTTP {response.status_code}，"
            f"Content-Type={content_type!r}，响应内容={preview!r}"
        ) from error


# 最长等待时间：1 小时
MAX_WAIT_SECONDS = 60 * 60

started_at = time.monotonic()

while True:
    # 超时保护
    if time.monotonic() - started_at >= MAX_WAIT_SECONDS:
        raise TimeoutError("等待 Meshy 任务完成超时")

    # 查询任务状态
    response = requests.get(query_url, headers=headers, timeout=30)
    # 如果返回 400、401、402、429 等错误，这里会抛出异常
    response.raise_for_status()
    task = read_json_response(response)

    # 【status】(string) 任务状态
    # 实测上游返回小写 running / succeeded，任务排队时为 NOT_START
    # 示例代码将上游别名映射为统一取值：
    # NOT_START / QUEUED → PENDING，RUNNING → IN_PROGRESS，
    # SUCCESS → SUCCEEDED，FAILURE → FAILED
    status = str(task.get("status", "")).upper()
    status = {
        "NOT_START": "PENDING",
        "NOT_STARTED": "PENDING",
        "QUEUED": "PENDING",
        "RUNNING": "IN_PROGRESS",
        "SUCCEEDED": "SUCCEEDED",
        "SUCCESS": "SUCCEEDED",
        "FAILED": "FAILED",
        "FAILURE": "FAILED",
        "CANCELED": "CANCELED",
    }.get(status, status)

    # 【progress】(number) 生成进度
    progress = task.get("progress")
    print(f"任务状态：{status}，进度：{progress}")

    if status == "SUCCEEDED":
        # 【model_urls】(object) 生成的模型下载地址，键为输出格式
        # 只打印实际返回的格式，未返回的格式不会显示
        model_urls = task.get("model_urls") or {}
        print("任务完成")
        for file_format, url in model_urls.items():
            print(f"{file_format.upper()} 地址:", url)

        # 【thumbnail_url】(string) 预览图地址
        print("预览图地址:", task.get("thumbnail_url"))

        # 【texture_urls】(array) 基础颜色和 PBR 纹理地址
        # should_texture=True 生成纹理时才会返回
        print("纹理地址:", task.get("texture_urls"))
        break

    if status in {"FAILED", "CANCELED"}:
        # 【task_error】(object) 任务失败或取消时的错误信息
        print("任务失败或取消")
        print("错误信息:", task.get("task_error"))
        break

    if status not in {"PENDING", "IN_PROGRESS"}:
        raise RuntimeError(f"未知任务状态：{status}")

    # 任务还在排队或生成中，按 Retry-After 等待，缺省 5 秒
    retry_after = response.headers.get("Retry-After")
    if retry_after:
        try:
            delay = max(1, int(float(retry_after)))
        except ValueError:
            delay = 5
    else:
        delay = 5
    time.sleep(delay)
```

## 获取结果返回示例

```json
{
  "art_style": "",
  "consumed_credits": 20,
  "created_at": 1792048440948,
  "expires_at": 4945648465189,
  "finished_at": 1792048465189,
  "id": "task_DzbvlJnVWj79wk0yqyoDYENOK0mKSACs",
  "image_style_url": "",
  "model_url": "https://assets.meshy.ai/d191b714-523d-4a82-91ed-29264a13e231/tasks/01a13e69-1d54-76f0-8610-15c78e334886/output/model.glb?Expires=4945648465&Signature=K-9koNkLgZOB4MpE-uMiMX9yOZJQYsoRRlVr3pwUk3WnrShd9BVGLiJg3uVTeKsGdLFR~xswXVmGyGprnu-tPjnOn8YYM38qS~BAUhlY8FIRWsLtHadukbxpuKY1gaybH46mQ8MM~HMce7Phd82vRr2XdHF9GwwQqqKgmNINuQtxZXEWzDl0Htlg8MfmUb2LLmeXLdIrmyGAaVwSKdNG8xwQrzvRcI86vca0-HOn30WSXj~MTjYPycTF-Kuw82~F4u~rDT3ajwr17wKlgWJ-E7F1e~gLZrwzMwGPSTaROkYfCjEIz9hTrxmI~ZbFVyWKJBIYBilVhzQGkuybRPmjUA__&Key-Pair-Id=K1VGYTHIYLM9UM",
  "model_urls": {
    "glb": "https://assets.meshy.ai/d191b714-523d-4a82-91ed-29264a13e231/tasks/01a13e69-1d54-76f0-8610-15c78e334886/output/model.glb?Expires=4945648465&Signature=K-9koNkLgZOB4MpE-uMiMX9yOZJQYsoRRlVr3pwUk3WnrShd9BVGLiJg3uVTeKsGdLFR~xswXVmGyGprnu-tPjnOn8YYM38qS~BAUhlY8FIRWsLtHadukbxpuKY1gaybH46mQ8MM~HMce7Phd82vRr2XdHF9GwwQqqKgmNINuQtxZXEWzDl0Htlg8MfmUb2LLmeXLdIrmyGAaVwSKdNG8xwQrzvRcI86vca0-HOn30WSXj~MTjYPycTF-Kuw82~F4u~rDT3ajwr17wKlgWJ-E7F1e~gLZrwzMwGPSTaROkYfCjEIz9hTrxmI~ZbFVyWKJBIYBilVhzQGkuybRPmjUA__&Key-Pair-Id=K1VGYTHIYLM9UM"
  },
  "name": "",
  "negative_prompt": "",
  "object_prompt": "",
  "progress": 100,
  "started_at": 1792048440956,
  "status": "succeeded",
  "style_prompt": "",
  "task_error": null,
  "task_id": "task_DzbvlJnVWj79wk0yqyoDYENOK0mKSACs",
  "text_style_prompt": "",
  "texture_image_url": "",
  "texture_prompt": "",
  "texture_urls": [],
  "thumbnail_url": "https://assets.meshy.ai/d191b714-523d-4a82-91ed-29264a13e231/tasks/01a13e69-1d54-76f0-8610-15c78e334886/output/preview.png?Expires=4945648465&Signature=hKHJsxf~qPpPK7dS~X0Js2mHQl0PLPova2~yLMfpVyHMKK3OLp4lBvg2tTpvgpPusGkvoZlhdmpHB69wuhaAQGlKZUmkAaEQjWJhudBiGhmO4OgnBxhvSxcRUqb2FKydkw7dcvytuke0AShWNxtTEhTyiQgO6QS~xtQW~1HJgCr87GTHXyPOpNWwImHi2oe-E3h5qxVqdrYGtbi0yEOMeqOYXgbmmaWE4uYUKkBixF1n63Dr1cS5kzzbsFIZpwUFfIXDxzmxkjX5Nqp2RMCZjcRJS~6G0lcuP-TD0JvNvQIZT6AH0AvOPvMfAuhlMxAgERYVbFGrzj3ANGH1R8DCMQ__&Key-Pair-Id=K1VGYTHIYLM9UM",
  "type": "image-to-3d"
}
```

任务成功时返回模型与预览图地址：上游状态字段是小写 `succeeded`（示例代码映射为 `SUCCEEDED`）；示例对应 `should_texture=False` 的无纹理结果，因此 `texture_urls` 为空数组。生成纹理（`should_texture=True`）时响应还会包含 `texture_urls`（基础颜色与 PBR 纹理地址），示例代码会一并读取打印。任务失败或取消时状态为 `failed` / `canceled`（映射为 `FAILED` / `CANCELED`），代码读取 `task_error` 字段获取错误信息。

<p align="center">
  <small>© 2026 DMXAPI Meshy-7.1 单图生 3D</small>
</p>
