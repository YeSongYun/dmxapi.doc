# neural4d-2.5 单图生 3D API 使用文档

本文介绍如何通过 DMXAPI 代理调用 Neural4D，将一张本地图片或公网 HTTPS 图片生成 3D 模型。调用采用两阶段异步流程：先使用 `neural4d-2.5` 提交任务，从响应的 `output[0].content[0].text` 获取批次任务 ID，再使用 `neural4d-get` 将该 ID 放入 `input.id` 查询模型结果；可按需设置图片增强、贴图、PBR、网格质量、拓扑、目标面数、姿态和生成数量。

## 接口地址

| 接口 | 请求方式 | URL |
|------|---------|-----|
| 提交任务 | POST | `https://www.dmxapi.cn/v1/responses` |
| 获取结果 | POST | `https://www.dmxapi.cn/v1/responses` |

:::warning
请妥善保管您的 DMXAPI API Key！严禁向他人泄露、在公开代码中使用真实密钥或将其提交到公开仓库。文档中的密钥已替换为无效占位符，调用前请换成您自己的密钥。
:::

## 模型名称

- 提交任务：`neural4d-2.5`
- 获取结果：`neural4d-get`

## 单图生 3D 提交任务示例代码

```python
import requests
import json
import base64

# ===============================================================
# 步骤1: 配置 API 连接信息
# ===============================================================

# DMXAPI 服务端点地址
url = "https://www.dmxapi.cn/v1/responses"

# DMXAPI 密钥，请替换为您自己的密钥
api_key = "sk-***********************************************"

# ===============================================================
# 步骤2: 配置请求头
# ===============================================================

headers = {
    "Content-Type": "application/json",  # 请求体使用 JSON 格式
    "Authorization": f"Bearer {api_key}",  # Bearer 认证
}

# ===============================================================
# 步骤3: 配置请求参数
# ===============================================================

# 【图片】填本地图片路径，或可直接下载的公网 HTTPS 图片链接。
# 图片仅支持 JPG、JPEG、PNG、WEBP，每张不超过 20 MiB，一次请求总量不超过 128 MiB。
# image = "https://cdn.jsdelivr.net/gh/opencv/opencv/samples/data/fruits.jpg"
image = "C:/path/to/source-image.jpg"

# 当前示例将本地图片按扩展名转成 base64 data URL，HTTPS 链接原样使用。
# 随附说明称网关会处理后续上传，不需要单独调用上传接口。
mime_types = {
    ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg",
    ".png": "image/png",
    ".webp": "image/webp",
}
if image.startswith("https://"):
    image_url = image
else:
    extension = "." + image.rsplit(".", 1)[-1].lower()
    if extension not in mime_types:
        raise ValueError(f"只支持 JPG、JPEG、PNG、WEBP 图片：{image}")
    with open(image, "rb") as image_file:
        image_url = f"data:{mime_types[extension]};base64," + base64.b64encode(image_file.read()).decode()

payload = {
    # 【model】(string, 必填) 模型名称。
    # DMXAPI 代理的单图生 3D 任务固定填写 neural4d-2.5。
    "model": "neural4d-2.5",

    # 【input】(object, 必填) DMXAPI 代理的生成参数对象。
    # 除 input_references 外均为可选参数，不传时使用默认值。
    "input": {
        # 【input.input_references】(object[], 必填) 单张参考图片数组，长度必须为 1。
        "input_references": [
            {
                # 【input.input_references[].type】(string, 必填) 参考素材类型，固定填写 image。
                "type": "image",

                # 【input.input_references[].url】(string, 必填) 当前代理示例中的图片地址。
                # 使用上方处理结果，可为公网 HTTPS 或本地图片转换后的 data URL。
                "url": image_url,
            },
        ],

        # 【input.image_enhancement】(bool, 可选) 是否在生成前增强输入图片。
        # 默认值为 false。
        "image_enhancement": False,

        # 【input.with_texture】(bool, 可选) 是否生成纹理贴图。
        # 默认值为 false，即只生成白模；需要贴图时设为 true。
        "with_texture": True,

        # 【input.with_pbr】(bool, 可选) 是否生成 PBR 材质。
        # 默认值为 false；设为 true 时，with_texture 必须也为 true。
        "with_pbr": False,

        # 【input.mesh_quality】(string, 可选) 网格质量。
        # 默认值为 standard；可选值: "standard" / "high" / "extra_high"。
        "mesh_quality": "standard",

        # 【input.topology】(string, 可选) 网格拓扑。
        # 默认值为 triangle；可选值: "triangle"（三角面）/ "quad"（四边面）。
        "topology": "triangle",

        # 【input.target_polycount】(int, 可选) 目标面数，范围取决于拓扑和质量。
        # 三角面 standard 为 100000-500000，默认 500000；
        # 三角面 high、extra_high 为 500000-1000000，默认 1000000；三角面以 1000 递增。
        # 四边面为 1000-100000，默认 50000，以 100 递增。
        "target_polycount": 500000,

        # 【input.pose】(string, 可选) 角色姿态。
        # 默认值为 auto；可选值: "auto" / "A-pose" / "T-pose"。
        "pose": "auto",

        # 【input.n】(int, 可选) 根据这张图片生成的模型数量。
        # 默认值为 1，范围为 1-4。
        "n": 1,
    },
}

# ===============================================================
# 步骤4: 发送请求并输出结果
# ===============================================================

# 提交超时或断线时，任务可能已经提交并扣费；请先确认任务状态，不要直接重复提交。
response = requests.post(url, headers=headers, json=payload)

print(json.dumps(response.json(), indent=2, ensure_ascii=False))
```

## 返回示例

```json
{
  "created_at": 1793010538,
  "mode": "image_to_3d",
  "output": [
    {
      "type": "message",
      "content": [
        {
          "type": "output_text",
          "text": "ad5e6a88-8b8a-4cb6-8020-32f02c1f18aa"
        }
      ]
    }
  ],
  "status": "queued",
  "usage": {
    "input_tokens": 0,
    "input_tokens_details": {
      "cached_tokens": 0
    },
    "output_tokens": 14200,
    "output_tokens_details": {
      "reasoning_tokens": 0
    },
    "total_tokens": 14200
  }
}
```

## 获取结果示例代码

```python
import requests
import json

# ===============================================================
# 步骤1: 配置 API 连接信息
# ===============================================================

# DMXAPI 服务端点地址
url = "https://www.dmxapi.cn/v1/responses"

# DMXAPI 密钥，请替换为您自己的密钥
api_key = "sk-***********************************************"

# ===============================================================
# 步骤2: 配置请求头
# ===============================================================

headers = {
    "Content-Type": "application/json",  # 请求体使用 JSON 格式
    "Authorization": f"Bearer {api_key}",  # Bearer 认证
}

# ===============================================================
# 步骤3: 配置请求参数
# ===============================================================

payload = {
    # 【model】(string, 必填) 模型名称。
    # DMXAPI 代理的查询任务固定填写 neural4d-get。
    "model": "neural4d-get",

    # 【input】(object, 必填) 查询条件对象。
    "input": {
        # 【input.id】(string, 必填) 提交阶段返回的批次任务 ID。
        # 与提交响应中的 output[0].content[0].text 保持一致；返回该批次的全部模型。
        "id": "ad5e6a88-8b8a-4cb6-8020-32f02c1f18aa",
    },
}

# ===============================================================
# 步骤4: 发送请求并输出结果
# ===============================================================

# 任务未完成时，网关会等待任务结束再返回，最长约 1 小时，不需要自己循环查询。
# 查询不扣费，可以重复查询；随附交接说明记载结果链接 30 天内有效，过期后可重新查询。
response = requests.post(url, headers=headers, json=payload)

print(json.dumps(response.json(), indent=2, ensure_ascii=False))
```
## 返回示例

```json
{
  "created_at": 1793010538,
  "mode": "image_to_3d",
  "output": [
    {
      "type": "message",
      "content": [
        {
          "type": "output_text",
          "text": "0ba5ea49-b312-431e-af1d-1bb9f53ec164"
        },
        {
          "type": "output_text",
          "text": "https://s3.neural4d.com/880f51b3-1168-40ec-8b9e-f4046ab4c7e2_0.glb?sign=1788220800-dreammaker-0-57a62cab32b2a101416f1968a70d3932&response-content-disposition=attachment;filename=915417405ba251db24bb6ca77df321fd.glb"
        },
        {
          "type": "output_text",
          "text": "https://s3.neural4d.com/760573e0-8c1e-4419-a329-e5befc6114be_0.jpg?sign=1788220800-dreammaker-0-fa35a3853c7b0b1b851ff2834ed30ac9&response-content-disposition=attachment;filename=46aca65058dab2f4f3e502714c6dc007.jpg"
        }
      ]
    }
  ],
  "status": "succeeded",
  "updated_at": 1793010860,
  "usage": {
    "input_tokens": 0,
    "input_tokens_details": {
      "cached_tokens": 0
    },
    "output_tokens": 0,
    "output_tokens_details": {
      "reasoning_tokens": 0
    },
    "total_tokens": 0
  }
}
```
<p align="center">
  <small>© 2026 DMXAPI neural4d-2.5 单图生 3D</small>
</p>
