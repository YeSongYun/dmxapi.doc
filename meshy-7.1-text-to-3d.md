# Meshy-7.1 文本生成 3D API 使用文档

基于 Meshy 7.1 模型的文本生成 3D 接口，通过 DMXAPI 网关以异步任务方式调用，分为 Preview（生成形状）与 Refine（生成纹理）两个阶段。Preview 阶段根据文本描述生成仅含几何体的 3D 网格，支持 standard / 2K / 4K 三档几何分辨率与 quad / triangle 两种拓扑，目标面数可精确控制在 100–300,000；Refine 阶段为形状施加贴图，支持 2K / 4K / 8K 纹理分辨率与 PBR 材质（金属度 / 粗糙度 / 法线），可选文本或图片引导贴图生成。最终输出 glb / obj / fbx / stl / usdz / 3mf 六种格式，贴图与模型下载地址由查询接口统一返回，适合游戏资产、电商商品、创意设计等从文本快速构建 3D 模型的应用。价格详见价格表 meshy 分组。

## 接口地址

| 接口 | 请求方式 | URL |
|------|---------|-----|
| 创建 Preview 任务 | POST | `https://www.dmxapi.cn/meshy/v1/text-to-3d` |
| 创建 Refine 任务 | POST | `https://www.dmxapi.cn/meshy/v1/text-to-3d` |
| 查询任务 | GET | `https://www.dmxapi.cn/meshy/v1/text-to-3d/{task_id}` |

:::warning
请妥善保管您的 API Key！严禁将密钥泄露给他人、硬编码到代码中或提交到公开的代码仓库。如果怀疑密钥已泄露，请立即前往 DMXAPI 官网重新生成。
:::

## 模型名称

- `meshy-7.1`

## 文本生成 3D Preview 示例代码

```python
import requests
import json

# ===============================================================
# 步骤1: 配置 API 连接信息
# ===============================================================

# DMXAPI 服务端点地址
BASE_URL = "https://www.dmxapi.cn"

# DMXAPI 密钥 (请替换为您自己的密钥)
# 获取方式: 登录 DMXAPI 官网 -> 个人中心 -> API 密钥管理
API_KEY = "sk-******************************************"

# 文本生成 3D 创建任务接口
CREATE_URL = f"{BASE_URL}/meshy/v1/text-to-3d"

# ===============================================================
# 步骤2: 配置请求头
# ===============================================================

headers = {
    "Content-Type": "application/json",      # 指定请求体为 JSON 格式
    "Authorization": f"Bearer {API_KEY}",    # Bearer token 认证方式
}

# ===============================================================
# 步骤3: 配置请求参数
# ===============================================================

payload = {
    # 【mode】(string, 必填) 任务模式
    # Preview 阶段只生成 3D 模型形状，不生成纹理
    # 可选值: "preview"(生成形状)
    "mode": "preview",

    # 【prompt】(string, 必填) 描述需要生成的 3D 物体
    # 最多 800 个字符
    "prompt": "一只可爱的小猫",

    # 【ai_model】(string, 可选) 模型 ID
    # 固定使用 Meshy 7.1
    # 默认值: "latest"（即 Meshy 7.1）
    "ai_model": "meshy-7.1",

    # 【model_type】(string, 可选) 3D 网格生成类型
    # 可选值: "standard"(标准网格) / "smart-topology"(智能拓扑)
    # 默认值: "standard"
    "model_type": "standard",

    # 【geometry_resolution】(string, 可选) 几何分辨率档位
    # "2k" 按 2048³ 运行 Ultra 阶段，"4k" 按 4096³
    # 可选值: "standard"(普通) / "2k"(Ultra 2K) / "4k"(Ultra 4K)
    # 注意: 可选值中没有 "ultra"，使用 "2k" 或 "4k" 表示 Ultra
    # 默认值: "standard"
    "geometry_resolution": "standard",

    # 【should_remesh】(boolean, 可选) 是否启用 remesh 阶段
    # false: 保留原始几何细节（推荐高质量场景使用）
    # true: 启用 remesh，可配合 topology、target_polycount 使用
    # 默认值: false（Meshy 6/7 系列）
    "should_remesh": False,

    # 【topology】(string, 可选) 网格拓扑类型
    # 仅 should_remesh=true 时生效
    # 可选值: "quad"(四边形为主) / "triangle"(三角形)
    # 默认值: "triangle"
    # 当前关闭 remesh，因此不发送该字段
    # "topology": "triangle",

    # 【decimation_mode】(integer, 可选) 自适应简化等级
    # 设置后 target_polycount 会被忽略
    # 可选值: 1(超高面数) / 2(高面数) / 3(中等面数) / 4(低面数)
    # "decimation_mode": 2,

    # 【target_polycount】(integer, 可选) 目标面数
    # 仅 should_remesh=true 时生效
    # 取值范围: [100, 300000]，默认值为 30000
    # "target_polycount": 30000,

    # 【pose_mode】(string, 可选) 姿势模式
    # 可选值: ""(不应用) / "a-pose" / "t-pose"
    "pose_mode": "",

    # 【moderation】(boolean, 可选) 是否进行内容审核
    # true 时命中有害内容则不生成;将对 prompt 中的文本进行审查。
    # 默认值: false
    "moderation": False,

    # 【auto_size】(boolean, 可选) 是否自动估算真实尺寸并调整模型大小
    # 默认值: false
    "auto_size": False,

    # 【origin_at】(string, 可选) auto_size 的原点位置
    # 可选值: "bottom"(底部) / "center"(中心)
    # 仅 auto_size=true 时生效；默认不发送该字段
    # 默认值: "bottom"
    # "origin_at": "bottom",

    # 【alpha_thumbnail】(boolean, 可选) 是否生成透明背景缩略图
    # true 时额外返回 alpha_thumbnail_url
    # 默认值: false
    "alpha_thumbnail": False,

    # 【target_formats】(array[string], 可选) 输出文件格式
    # 可选值: "glb" / "obj" / "fbx" / "stl" / "usdz" / "3mf"
    # 省略时生成除 3mf 外全部格式；指定后仅生成所列格式，可缩短耗时
    "target_formats": ["glb"],
}

# ===============================================================
# 步骤4: 发送请求并输出结果
# ===============================================================

# 发送 POST 请求创建 Preview 任务
response = requests.post(CREATE_URL, headers=headers, json=payload, timeout=60)

# 如果返回 400、401、402、429 等错误，这里会抛出异常
response.raise_for_status()

# 读取网关 JSON；若上游返回 HTML/纯文本，输出可读错误
try:
    result = response.json()
except ValueError as error:
    preview = response.text[:500].replace("\n", " ")
    raise RuntimeError(
        f"网关返回的不是 JSON：HTTP {response.status_code}，响应内容={preview!r}"
    ) from error

# 提取 DMXAPI 任务 ID（查询接口只认 task_id）
# result 是 Meshy 原生 UUID，用于本文查询接口会返回 404，不要把它当作 task_id
task_id = result.get("task_id")
if not task_id:
    raise RuntimeError(f"DMXAPI 返回中没有 task_id：{result}")

# 格式化输出 JSON 响应
# - indent=2: 缩进 2 空格，便于阅读
# - ensure_ascii=False: 正确显示中文字符
print(json.dumps(result, indent=2, ensure_ascii=False))

print("Preview 任务创建成功")
print("Preview task_id:", task_id)
print("请等待 Preview 状态变为 SUCCEEDED，再使用这个 ID 创建 Refine 任务")
```

## 返回示例

```json
{
  "result": "01a1526c-cc5c-7020-980a-df39cb090c5b",
  "task_id": "task_9kFr6hQ2WkQ7JjzY0fhrVbfArTrxfTyi"
}
```

## 文本生成 3D Refine 示例代码

```python
import requests
import json

# ===============================================================
# 步骤1: 配置 API 连接信息
# ===============================================================

# DMXAPI 服务端点地址
BASE_URL = "https://www.dmxapi.cn"

# DMXAPI 密钥 (请替换为您自己的密钥)
# 获取方式: 登录 DMXAPI 官网 -> 个人中心 -> API 密钥管理
API_KEY = "sk-******************************************"

# 填写 Text-to-3D Preview 成功返回的任务 ID
PREVIEW_TASK_ID = "task_MiccTq3Lxh4GqBB8Pv1WzoXdy9QQt0ab"

# 文本生成 3D 创建任务接口
CREATE_URL = f"{BASE_URL}/meshy/v1/text-to-3d"

# ===============================================================
# 步骤2: 配置请求头
# ===============================================================

headers = {
    "Content-Type": "application/json",      # 指定请求体为 JSON 格式
    "Authorization": f"Bearer {API_KEY}",    # Bearer token 认证方式
}

# ===============================================================
# 步骤3: 配置请求参数
# ===============================================================

payload = {
    # 【mode】(string, 必填) 任务模式
    # Refine 阶段给 Preview 模型生成纹理
    # 可选值: "preview"(生成形状) / "refine"(为形状生成纹理)
    "mode": "refine",

    # 【preview_task_id】(string, 必填) 已经成功完成的 Preview 任务 ID
    # 对应 Preview 任务状态必须为 SUCCEEDED
    "preview_task_id": PREVIEW_TASK_ID,

    # 【ai_model】(string, 可选) 模型 ID
    # 应与 Preview 阶段使用的模型一致
    # 默认值: 继承 Preview 任务的模型
    "ai_model": "meshy-7.1",

    # 【texture_resolution】(string, 可选) 基础颜色贴图分辨率
    # 可选值: "2k"(2048²) / "4k"(4096²) / "8k"(8192²)
    # 默认值: "2k"
    "texture_resolution": "2k",

    # 【enable_pbr】(boolean, 可选) 是否生成 PBR 纹理
    # true: 生成 metallic、roughness、normal 等 PBR 纹理
    # false: 只生成基础颜色纹理
    # 注意: Meshy 7.1 不生成 emission 发光贴图
    # 默认值: false
    "enable_pbr": True,

    # 【texture_prompt】(string, 可选) 纹理引导文字
    # 最多 800 个字符
    # 与 texture_image_url 二选一，同时提供时默认使用 texture_prompt
    # "texture_prompt": "green slimy skin with scales",

    # 【texture_image_url】(string, 可选) 纹理引导图片
    # 公开 URL 或 Base64 Data URI，支持 jpg/jpeg/png/webp，最大 20 MB
    # 与 texture_prompt 二选一，同时提供时默认使用 texture_prompt
    # "texture_image_url": "https://example.com/texture-guide.png",

    # 【moderation】(boolean, 可选) 是否进行内容审核
    # true 时同时审查 texture_prompt 与 texture_image_url
    # 默认值: false
    "moderation": False,

    # 【remove_lighting】(boolean, 可选) 是否从基础色移除高光阴影
    # 注意: 仅 Meshy 6 生效，Meshy 7.1 会忽略该参数
    # 默认值: true
    "remove_lighting": True,

    # 【auto_size】(boolean, 可选) 是否自动估算真实尺寸并调整模型大小
    # 默认值: false
    "auto_size": False,

    # 【origin_at】(string, 可选) auto_size 的原点位置
    # 可选值: "bottom"(底部) / "center"(中心)
    # 仅 auto_size=true 时生效；默认不发送该字段
    # 默认值: "bottom"
    # "origin_at": "bottom",

    # 【alpha_thumbnail】(boolean, 可选) 是否生成透明背景缩略图
    # true 时额外返回 alpha_thumbnail_url
    # 默认值: false
    "alpha_thumbnail": False,

    # 【target_formats】(array[string], 可选) 输出文件格式
    # 可选值: "glb" / "obj" / "fbx" / "stl" / "usdz" / "3mf"
    # 省略时生成除 3mf 外全部格式；指定后仅生成所列格式，可缩短耗时
    "target_formats": ["glb"],
}

# ===============================================================
# 步骤4: 发送请求并输出结果
# ===============================================================

# 发送 POST 请求创建 Refine 任务
response = requests.post(CREATE_URL, headers=headers, json=payload, timeout=60)

# 如果返回 400、401、402、429 等错误，这里会抛出异常
response.raise_for_status()

# 读取网关 JSON；若返回 HTML/纯文本，输出状态和响应摘要
try:
    result = response.json()
except ValueError as error:
    preview = response.text[:500].replace("\n", " ")
    raise RuntimeError(
        f"网关返回的不是 JSON：HTTP {response.status_code}，响应内容={preview!r}"
    ) from error

# 提取 DMXAPI Refine 任务 ID（查询接口只认 task_id）
# result 是 Meshy 原生 UUID，用于本文查询接口会返回 404，不要把它当作 task_id
refine_task_id = result.get("task_id")
if not refine_task_id:
    raise RuntimeError(f"DMXAPI 返回中没有 Refine task_id：{result}")

# 格式化输出 JSON 响应
print(json.dumps(result, indent=2, ensure_ascii=False))

print("Refine 任务创建成功")
print("Refine task_id:", refine_task_id)
print("请使用异步查询脚本查询这个 Refine 任务")
```

## 返回示例

```json
{
  "result": "01a1526e-4f41-7098-a515-cc999cf9773f",
  "task_id": "task_Ysavks78X6RHwHyuX2o1agnUiqNBNCq3"
}
```

## 查询任务结果 示例代码

```python
"""
╔═══════════════════════════════════════════════════════════════╗
║                  DMXAPI 自研接口                               ║
╚═══════════════════════════════════════════════════════════════╝

📝 功能说明:
   本脚本演示如何轮询查询 Meshy 文本生成 3D 任务的状态与结果

═══════════════════════════════════════════════════════════════
"""

import time
import requests
import json

# ═══════════════════════════════════════════════════════════════
# 🔑 步骤1: 配置 API 连接信息
# ═══════════════════════════════════════════════════════════════

# 🌐 DMXAPI 服务端点地址
BASE_URL = "https://www.dmxapi.cn"

# 🔐 DMXAPI 密钥 (请替换为您自己的密钥)
# 获取方式: 登录 DMXAPI 官网 -> 个人中心 -> API 密钥管理
API_KEY = "sk-******************************************"

# 填写创建任务接口返回的 task_id
# 查询接口只认 task_id；result 是 Meshy 原生 UUID，用于查询会返回 404
TASK_ID = "task_9DdN3kVyoPC0zmhmjN46p1OoSiaAcFL1"

# Text Preview 和 Text Refine 共用同一个查询接口
query_url = f"{BASE_URL}/meshy/v1/text-to-3d/{TASK_ID}"

# 最长等待时间：1 小时
MAX_WAIT_SECONDS = 60 * 60

# ═══════════════════════════════════════════════════════════════
# 📋 步骤2: 配置请求头
# ═══════════════════════════════════════════════════════════════

headers = {
    "Authorization": f"Bearer {API_KEY}",    # Bearer token 认证方式
}

# ═══════════════════════════════════════════════════════════════
# 💬 步骤3: 配置查询与轮询逻辑
# ═══════════════════════════════════════════════════════════════

def read_json_response(response):
    """读取网关 JSON；若返回 HTML/纯文本，输出状态和响应摘要。"""
    content_type = response.headers.get("Content-Type", "")
    try:
        return response.json()
    except ValueError as error:
        preview = response.text[:500].replace("\n", " ")
        raise RuntimeError(
            f"网关返回的不是 JSON：HTTP {response.status_code}，"
            f"Content-Type={content_type!r}，响应内容={preview!r}"
        ) from error

def get_retry_delay(response):
    """读取网关返回的 Retry-After，没有时默认等待 5 秒。"""
    retry_after = response.headers.get("Retry-After")
    if retry_after:
        try:
            return max(1, int(float(retry_after)))
        except ValueError:
            pass
    return 5

# ═══════════════════════════════════════════════════════════════
# 📤 步骤4: 轮询查询并输出结果
# ═══════════════════════════════════════════════════════════════

def wait_for_task(query_url):
    """轮询任务，直到任务成功、失败、取消或超时。"""
    started_at = time.monotonic()

    while True:
        # 超时保护
        if time.monotonic() - started_at >= MAX_WAIT_SECONDS:
            raise TimeoutError("等待 Meshy 任务完成超时")

        # 查询任务状态
        response = requests.get(query_url, headers=headers, timeout=30)
        response.raise_for_status()
        task = read_json_response(response)

        # 状态别名映射：兼容不同状态命名
        status_aliases = {
            "NOT_START": "PENDING",
            "QUEUED": "PENDING",
            "RUNNING": "IN_PROGRESS",
            "SUCCEEDED": "SUCCEEDED",
            "SUCCESS": "SUCCEEDED",
            "FAILED": "FAILED",
            "FAILURE": "FAILED",
            "CANCELED": "CANCELED",
        }
        status = status_aliases.get(
            str(task.get("status", "")).upper(),
            str(task.get("status", "")).upper(),
        )
        progress = task.get("progress")

        print(f"任务状态：{status}，进度：{progress}")

        if status == "SUCCEEDED":
            # 生成的模型下载地址
            # 只打印 Meshy 实际返回的格式，未返回的格式不会显示
            model_urls = task.get("model_urls") or {}
            print("任务完成")
            for file_format, url in model_urls.items():
                print(f"{file_format.upper()} 地址:", url)

            # 普通预览图
            print("预览图地址:", task.get("thumbnail_url"))

            # 多视角预览图
            print("多视角预览图:", task.get("thumbnail_urls"))

            # 基础颜色和 PBR 纹理地址
            print("纹理地址:", task.get("texture_urls"))

            # 格式化输出完整 JSON 响应
            print(json.dumps(task, indent=2, ensure_ascii=False))
            return task

        if status in {"FAILED", "CANCELED"}:
            print("任务失败或取消")
            print("错误信息:", task.get("task_error"))
            return task

        if status not in {"PENDING", "IN_PROGRESS"}:
            raise RuntimeError(f"未知任务状态：{status}")

        # 任务还在排队或生成中，按 Retry-After 等待
        time.sleep(get_retry_delay(response))

# 开始轮询
final_task = wait_for_task(query_url)
```

## 返回示例

```json
{
  "consumed_credits": 10,
  "created_at": 1792384323415,
  "finished_at": 1792384588351,
  "id": "task_Ysavks78X6RHwHyuX2o1agnUiqNBNCq3",
  "mode": "refine",
  "model_type": "standard",
  "model_urls": {
    "glb": "https://assets.meshy.ai/d191b714-523d-4a82-91ed-29264a13e231/tasks/01a1526e-4f41-7098-a515-cc999cf9773f/output/model.glb?Expires=4945968000&Signature=***&Key-Pair-Id=***"
  },
  "name": "",
  "progress": 100,
  "prompt": "一只可爱的小猫",
  "seed": 348115579,
  "started_at": 1792384323420,
  "status": "succeeded",
  "task_error": null,
  "task_id": "task_Ysavks78X6RHwHyuX2o1agnUiqNBNCq3",
  "texture_image_url": "",
  "texture_prompt": "",
  "texture_urls": [
    {
      "base_color": "https://assets.meshy.ai/d191b714-523d-4a82-91ed-29264a13e231/tasks/01a1526e-4f41-7098-a515-cc999cf9773f/output/texture_0.png?Expires=4945968000&Signature=***&Key-Pair-Id=***",
      "metallic": "https://assets.meshy.ai/d191b714-523d-4a82-91ed-29264a13e231/tasks/01a1526e-4f41-7098-a515-cc999cf9773f/output/texture_0_metallic.png?Expires=4945968000&Signature=***&Key-Pair-Id=***",
      "normal": "https://assets.meshy.ai/d191b714-523d-4a82-91ed-29264a13e231/tasks/01a1526e-4f41-7098-a515-cc999cf9773f/output/texture_0_normal.png?Expires=4945968000&Signature=***&Key-Pair-Id=***",
      "roughness": "https://assets.meshy.ai/d191b714-523d-4a82-91ed-29264a13e231/tasks/01a1526e-4f41-7098-a515-cc999cf9773f/output/texture_0_roughness.png?Expires=4945968000&Signature=***&Key-Pair-Id=***"
    }
  ],
  "thumbnail_url": "https://assets.meshy.ai/d191b714-523d-4a82-91ed-29264a13e231/tasks/01a1526e-4f41-7098-a515-cc999cf9773f/output/preview.png?Expires=4945968000&Signature=***&Key-Pair-Id=***",
  "type": "text-to-3d-refine"
}
```

## 完整工作流程

1. **创建 Preview 任务** → 调用创建接口（`mode: "preview"`），获得 `task_id`
2. **创建 Refine 任务** → 等待 Preview 状态为 `SUCCEEDED` 后，调用同一接口（`mode: "refine"`），传入 `preview_task_id`
3. **轮询查询** → 定期调用查询接口，等待 `status: "SUCCEEDED"`，从 `model_urls` 获取模型下载地址、`texture_urls` 获取纹理地址

<p align="center">
  <small>© 2026 DMXAPI Meshy-7.1 文本生成 3D</small>
</p>
