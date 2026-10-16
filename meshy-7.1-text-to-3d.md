# Meshy-7.1 文本生 3D API 使用文档

基于 Meshy 7.1 模型的文本生成 3D 接口，通过 DMXAPI 网关（Meshy Task Plugin）以异步任务方式调用：分 Preview 与 Refine 两步生成（可以理解为生成和再生成），再异步查询任务结果。Preview 任务根据文本描述生成 3D 模型形状（不生成纹理），Refine 任务为 Preview 模型再生成纹理；需先将 Preview 任务查询至 `SUCCEEDED`，再用该 Preview 任务 ID 提交 Refine 任务，Preview 与 Refine 任务共用同一查询接口。模型支持输出 glb、obj、fbx、stl、usdz、3mf 格式，纹理支持 2k、4k、8k 分辨率与可选 PBR 贴图。

## 接口地址

| 接口 | 请求方式 | URL |
|------|---------|-----|
| 提交 Preview 任务 | POST | `https://test.dmxapi.vip/meshy/v1/text-to-3d` |
| 提交 Refine 任务 | POST | `https://test.dmxapi.vip/meshy/v1/text-to-3d` |
| 查询任务 | GET | `https://test.dmxapi.vip/meshy/v1/text-to-3d/{task_id}` |

:::warning
请妥善保管您的 dmx-api API Key！严禁将密钥泄露给他人、硬编码到公开可见的代码中或提交到公开的代码仓库。如怀疑密钥已泄露，请立即更换密钥。
:::

## 模型名称

- `meshy-7.1`

## 提交 Preview 任务示例代码

```python
import requests


# ===============================================================
# 步骤1: 配置 API 连接信息
# ===============================================================

# dmx-api 网关地址
BASE_URL = "https://test.dmxapi.vip"

# dmx-api API Key (请替换为您自己的密钥)
API_KEY = "sk-***********************************************"

# Text-to-3D 创建接口（Preview 与 Refine 共用）
CREATE_URL = f"{BASE_URL}/meshy/v1/text-to-3d"

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
    # 【mode】(string, 必填) 创建 Preview 任务
    # Preview 阶段只生成 3D 模型形状，不生成纹理
    "mode": "preview",

    # 【prompt】(string, 必填) 描述需要生成的 3D 物体
    # 最多 800 个字符
    "prompt": "一只可爱的小猫",

    # 【ai_model】(string) 模型 ID，固定使用 Meshy 7.1
    "ai_model": "meshy-7.1",

    # 【model_type】(string) 模型类型
    # Meshy 7.1 使用 standard
    "model_type": "standard",

    # 【geometry_resolution】(string) 几何分辨率
    # standard：普通几何分辨率
    # 2k：Ultra geometry 2K
    # 4k：Ultra geometry 4K
    # 注意：参数值中没有 ultra，使用 2k 或 4k 表示 Ultra
    "geometry_resolution": "standard",

    # 【should_remesh】(bool) 是否启用 remesh
    # false：尽量保留原始几何细节
    # true：启用 remesh，可配合 topology 和 target_polycount 使用
    "should_remesh": False,

    # 【topology】(string) 网格拓扑类型
    # 可选值：quad、triangle
    "topology": "triangle",

    # 【target_formats】(array[string]) 输出文件格式
    # 可选值：glb、obj、fbx、stl、usdz、3mf
    # 这里只请求 glb，减少生成时间和输出内容
    "target_formats": ["glb"],
}

# ===============================================================
# 步骤4: 发送请求并输出结果
# ===============================================================


def read_json_response(response):
    """读取网关返回；若上游返回 HTML/纯文本，输出可读错误。"""
    content_type = response.headers.get("Content-Type", "")
    try:
        return response.json()
    except ValueError as error:
        preview = response.text[:500].replace("\n", " ")
        raise RuntimeError(
            f"网关返回的不是 JSON：HTTP {response.status_code}，"
            f"Content-Type={content_type!r}，响应内容={preview!r}"
        ) from error


# 发送 POST 请求创建 Preview 任务
response = requests.post(
    CREATE_URL,
    headers=headers,
    json=payload,
    timeout=60,
)

# 如果返回 400、401、402、429 等错误，这里会抛出异常
response.raise_for_status()

result = read_json_response(response)

# 创建成功同时返回 task_id（网关任务 ID）与 result（Meshy 原生 UUID）
# 查询接口只认 task_id（用 result 查询会 404），示例代码优先取 task_id
task_id = result.get("task_id") or result.get("result")
if not task_id:
    raise RuntimeError(f"Meshy 返回中没有任务 ID：{result}")

print("Preview 任务创建成功")
print("Preview task_id:", task_id)
print("请等待 Preview 状态变为 SUCCEEDED，再使用这个 ID 创建 Refine 任务")
```

## 提交 Preview 任务返回示例

```json
{
  "result": "01a13e69-19b1-710c-8e4a-8974bca85bd2",
  "task_id": "task_TPKIYnfNJ0nu2z2L1D22Fr7r1AdJ7drr"
}
```

创建 Preview 任务成功返回任务 ID：`task_id` 与 `result` 两个键同时返回且取值不同，`result` 为 Meshy 原生 UUID，`task_id` 为网关任务 ID。查询接口只认 `task_id`（用 `result` 查询会返回 404），示例代码优先取 `task_id`。将该 ID 查询至 `SUCCEEDED` 后，作为 Refine 任务的 `preview_task_id` 传入。

## 提交 Refine 任务示例代码

```python
import requests


# ===============================================================
# 步骤1: 配置 API 连接信息
# ===============================================================

# dmx-api 网关地址
BASE_URL = "https://test.dmxapi.vip"

# dmx-api API Key (请替换为您自己的密钥)
API_KEY = "sk-***********************************************"

# 填写已经成功完成（SUCCEEDED）的 Preview 任务 ID
PREVIEW_TASK_ID = "task_A1b2C3d4E5f6G7h8I9j0K1l2M3n4O5p6"

# Text-to-3D 创建接口（Preview 与 Refine 共用）
CREATE_URL = f"{BASE_URL}/meshy/v1/text-to-3d"

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
    # 【mode】(string, 必填) 创建 Refine 任务
    # Refine 阶段给 Preview 模型生成纹理（再生成）
    "mode": "refine",

    # 【preview_task_id】(string, 必填) 已经成功完成的 Preview 任务 ID
    # 该 Preview 任务状态须为 SUCCEEDED
    "preview_task_id": PREVIEW_TASK_ID,

    # 【ai_model】(string) 模型 ID，固定使用 Meshy 7.1
    # 该模型应与 Preview 阶段使用的模型一致
    "ai_model": "meshy-7.1",

    # 【texture_resolution】(string) 纹理分辨率
    # 可选值：2k、4k、8k
    "texture_resolution": "2k",

    # 【enable_pbr】(bool) 是否生成 PBR 纹理
    # true：生成 metallic、roughness、normal 等 PBR 纹理
    # false：只生成基础颜色纹理
    "enable_pbr": True,

    # 【target_formats】(array[string]) 输出文件格式
    # 可选值：glb、obj、fbx、stl、usdz、3mf
    "target_formats": ["glb"],
}

# ===============================================================
# 步骤4: 发送请求并输出结果
# ===============================================================


def read_json_response(response):
    """读取网关返回；若上游返回 HTML/纯文本，输出可读错误。"""
    content_type = response.headers.get("Content-Type", "")
    try:
        return response.json()
    except ValueError as error:
        preview = response.text[:500].replace("\n", " ")
        raise RuntimeError(
            f"网关返回的不是 JSON：HTTP {response.status_code}，"
            f"Content-Type={content_type!r}，响应内容={preview!r}"
        ) from error


# 发送 POST 请求创建 Refine 任务
response = requests.post(
    CREATE_URL,
    headers=headers,
    json=payload,
    timeout=60,
)

# 如果返回 400、401、402、429 等错误，这里会抛出异常
response.raise_for_status()

result = read_json_response(response)

# 创建成功同时返回 task_id（网关任务 ID）与 result（Meshy 原生 UUID）
# 查询接口只认 task_id，示例代码优先取 task_id
refine_task_id = result.get("task_id") or result.get("result")
if not refine_task_id:
    raise RuntimeError(f"Meshy 返回中没有 Refine 任务 ID：{result}")

print("Refine 任务创建成功")
print("Refine task_id:", refine_task_id)
print("请使用查询接口查询这个 Refine 任务")
```

## 提交 Refine 任务返回示例

```json
{
  "result": "01a13e6b-c26b-7453-bff5-fec7f98cfb5f",
  "task_id": "task_rMwb8VjnGS6NvOg87ZdbQmHgN1G2ssBH"
}
```

创建 Refine 任务成功返回任务 ID：`task_id` 与 `result` 两个键同时返回且取值不同，查询最终结果请使用 `task_id`（示例代码优先取 `task_id`）。

## 查询任务示例代码

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

# 填写创建接口返回的 dmx-api 任务 ID（Preview 或 Refine 任务 ID）
# Preview 与 Refine 任务共用同一个查询地址
TASK_ID = "task_B2c3D4e5F6g7H8i9J0k1L2m3N4o5P6q7"

# Text-to-3D 查询地址（任务 ID 位于 URL 路径中）
query_url = f"{BASE_URL}/meshy/v1/text-to-3d/{TASK_ID}"

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
    # 实测上游返回小写 running / succeeded，Refine 提交后先出现 NOT_START
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
        # Refine 任务生成纹理后返回
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

## 查询任务返回示例

```json
{
  "consumed_credits": 10,
  "created_at": 1792048611976,
  "finished_at": 1792048943013,
  "id": "task_rMwb8VjnGS6NvOg87ZdbQmHgN1G2ssBH",
  "mode": "refine",
  "model_type": "standard",
  "model_urls": {
    "glb": "https://assets.meshy.ai/d191b714-523d-4a82-91ed-29264a13e231/tasks/01a13e6b-c26b-7453-bff5-fec7f98cfb5f/output/model.glb?Expires=4945622400&Signature=DeB7vDhXitve7yDytnQTTw8c9dkEtTMcQyCXtvp6g3a2sSJKql4fUn-8j34c3HEwMLPPAlSoHsGeM5zkFU8PKNBz5o0SiJYWLUf5UVeGr7a6eJuFA-wTZ5CtwHyjrARU2ppYL5dG5mz46SAm9EtdNAMKV6TsNbozu3BYOyXp2NYmhuFG6ql7QxRXSXtXzp6zMm1BKw97wO~pByX1DLrUgoXH9zgf1hG8JtVq2DZPszVwb1cXtpd6OqOdfH85Jj8zNi5m0ao4~6c-7dqOmJg6feLE~li4OphpiMuSbDzRehxrsOUTvn0OCCCc~MNmEu6bOnrLHfDMmn2GfmRCC4T4Rw__&Key-Pair-Id=K1VGYTHIYLM9UM"
  },
  "name": "",
  "progress": 100,
  "prompt": "一只可爱的小猫",
  "seed": 729873608,
  "started_at": 1792048612459,
  "status": "succeeded",
  "task_error": null,
  "task_id": "task_rMwb8VjnGS6NvOg87ZdbQmHgN1G2ssBH",
  "texture_image_url": "",
  "texture_prompt": "",
  "texture_urls": [
    {
      "base_color": "https://assets.meshy.ai/d191b714-523d-4a82-91ed-29264a13e231/tasks/01a13e6b-c26b-7453-bff5-fec7f98cfb5f/output/texture_0.png?Expires=4945622400&Signature=LKuXLTnHOuWQ1sQqh8CeXKHnuA19LqTEQ9PxlwV38CASx~yxr4toAFmJpgM88eSaUuvQSQkPOqT~gKWgcFzjbhZDx8xhhW-bu-Oq854374tnrRHEuOyLjPdj9m6-ggEFphP35ExokKnocbPvfkwi-SlRzg33cW8tcUK6JQk5EnnrcXK7ZoEoRpatIyyMAaL7yqXq9Dc4ZcAEA4aUBZft1o9bQFyFNdzvgEKGc24kZLK-~pQnKpuiWWyaLesXaUN6EgQdo5tH24Knr1aa5dvNMqcU7WdQsvkrdH-BhV3DLIeYiT-VDlamfDQXdVuGV8IaP06lLtRcCBegtE5vkX-r0w__&Key-Pair-Id=K1VGYTHIYLM9UM",
      "metallic": "https://assets.meshy.ai/d191b714-523d-4a82-91ed-29264a13e231/tasks/01a13e6b-c26b-7453-bff5-fec7f98cfb5f/output/texture_0_metallic.png?Expires=4945622400&Signature=aaxsKGKx0PcSX5jFB38anRqZtbNO9yEkJs2zgVWyMWRNXN5CQloG5ui2Cp0Vrm1W1eyoUk8sZlvNEFJ84~gyWubX-4hte160WChDyd8snTwITt3GxmUCq1nxDgwuf-hcS8mP7ZjiQoeDMlgQ3K1eAJVkPDcfDGK2UhbvJjH419CSoEeoiJnjDqAWEwFqMJJOeR7CoYLU4qhOmemZKM4q6i69BKhb3NzKeFjl1Ta5JCpuayb8EFiN35femt9Moryiz5rvbpVM4OzRNBHWRR5nZqbOlOkl2xkK8RKWMHM4u20SadIAsA1pQf71k0xxRA9FKnj1OqHbCiKp4O6EGJD-kw__&Key-Pair-Id=K1VGYTHIYLM9UM",
      "normal": "https://assets.meshy.ai/d191b714-523d-4a82-91ed-29264a13e231/tasks/01a13e6b-c26b-7453-bff5-fec7f98cfb5f/output/texture_0_normal.png?Expires=4945622400&Signature=NDvIf7R9MlYSJjVtV9H91z-7flepB0s0Icfx06xbbIbyUh5Gheyu88rz2EqG0NfHYEns574Px~v6eG3Vp3nY5TVQ8xslq1yg13dUYt9Hoo1vvzDl-lLVByHsbWQkMI6NalHAZoalxr8NFJr1PonGCItMll9-DPwdgL3VqYlZO7tv7YGmelML--YnIeTnxaVI8Gw6V2kdPB8ZvxoI50yjWU4xANT5saQSHAWspBwjpzS-yr~Kq7JRZgHCL5pYdhlJUO00PuMPL8FvWk2XUdXN2BoOxnDz0AMOB5DHVFjEokBNaZT4PaKO2fjWURIUJqQjdFRKNywAxB~ZCZhOx6Q8yg__&Key-Pair-Id=K1VGYTHIYLM9UM",
      "roughness": "https://assets.meshy.ai/d191b714-523d-4a82-91ed-29264a13e231/tasks/01a13e6b-c26b-7453-bff5-fec7f98cfb5f/output/texture_0_roughness.png?Expires=4945622400&Signature=kipWbyG2wZ8zkhgUJp6jbK7EofkFvl0eXv~ESzycXGXc~lqlrZv3rUxYDE0osubUQXjFGAyBIT9V-Jvq2yIWxKCnCNZfNmIQtu5KCjzpUWA8aKO4Pgl9h090ImgTksyFLzpcCoVvu~cq47IvBa9BITzvQdmWaX1tQ9qL6tMbNHFHjWZjy6si5FjKIDPiBm796NiytHecY3khexpXEaN2Cp58-L05LGxqke5E63q2RgT3LgkQwRxn2t97uxw5VK3Z2xM4f09k5NdhUgRkpC9RwHDkpjGfycjf0-ZNd4zZDjsfo7FUDgAEiuFXVGcrcKiBLZnfDVQtsoGDnWg0zbtrFg__&Key-Pair-Id=K1VGYTHIYLM9UM"
    }
  ],
  "thumbnail_url": "https://assets.meshy.ai/d191b714-523d-4a82-91ed-29264a13e231/tasks/01a13e6b-c26b-7453-bff5-fec7f98cfb5f/output/preview.png?Expires=4945622400&Signature=cT8Edi9nXL~5JmiasGx7og5mWi8ltjEP6ymrvkQlAXlA8LxSKBjDxHa7f2vmH3QSoYBOJ4OV~azN53m5hgUomzvN~MHcViJEggHC8HwWLeBnoJ1lfh18bhmgi-l1LZoU4OykvN7KcKh8lWGN5-Xr0tfpL36p76SnwNjN7B8WkOgnmPvRkVjb9Sk~JBEzYhKtHq9sc9beeWkzld5TRoDP~9n2n9tJV9FdNVt1rbVumoHaHMRodbchbxOeP9ho9RdOte2PbtZ0NWKabn0Sbs~lTF7ZUGV45U--Dx769dXlp8YRb7oRVwjDpjSm49pXvzfRoCxUTCQNXRH6uRiH0jnrSw__&Key-Pair-Id=K1VGYTHIYLM9UM",
  "type": "text-to-3d-refine"
}
```

示例为 Refine 任务成功后的返回：上游状态字段是小写 `succeeded`（示例代码映射为 `SUCCEEDED`），包含模型下载地址、预览图与纹理地址；`enable_pbr` 为 `true` 时纹理含 metallic、normal、roughness 等 PBR 贴图，为 `false` 时只含基础颜色纹理。查询 Preview 任务时使用同一查询接口；任务失败或取消时状态为 `failed` / `canceled`（映射为 `FAILED` / `CANCELED`），代码读取 `task_error` 字段获取错误信息。

<p align="center">
  <small>© 2026 DMXAPI Meshy-7.1 文本生 3D</small>
</p>
