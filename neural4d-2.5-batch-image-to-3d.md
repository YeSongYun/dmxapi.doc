# neural4d-2.5 批量图生 3D API 使用文档

本文介绍如何通过 DMXAPI 代理调用 Neural4D，一次提交 2–10 张图片并让每张图片分别生成一个 3D 模型。调用采用两阶段异步流程：先使用 `neural4d-2.5` 提交批次任务，从响应的 `output[0].content[0].text` 获取批次任务 ID，再使用 `neural4d-get` 将该 ID 放入 `input.id` 查询本批全部模型；本地路径与公网 HTTPS 图片可以混用，计费按图片张数计算。

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

## 批量图生 3D 提交任务示例代码

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

# 批量图生 3D：一次提交 2-10 张图片，每张图片各生成一个模型。
# 【图片】每项填本地图片路径或可直接下载的公网 HTTPS 图片链接，可以混用。
# 图片仅支持 JPG、JPEG、PNG、WEBP，每张不超过 20 MiB，一次请求总量不超过 128 MiB。
images = [
    "https://cdn.jsdelivr.net/gh/opencv/opencv/samples/data/fruits.jpg",
    "https://cdn.jsdelivr.net/gh/opencv/opencv/samples/data/lena.jpg",
    # "C:/path/to/your/image.png",
]

# 当前示例将本地图片按扩展名转成 base64 data URL，HTTPS 链接原样使用。
# 随附说明称网关会处理后续上传，不需要单独调用上传接口。
mime_types = {
    ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg",
    ".png": "image/png",
    ".webp": "image/webp",
}
input_references = []
for image in images:
    if image.startswith("https://"):
        image_url = image
    else:
        extension = "." + image.rsplit(".", 1)[-1].lower()
        if extension not in mime_types:
            raise ValueError(f"只支持 JPG、JPEG、PNG、WEBP 图片：{image}")
        with open(image, "rb") as image_file:
            image_url = f"data:{mime_types[extension]};base64," + base64.b64encode(image_file.read()).decode()
    # 【input.input_references[].type】(string, 必填) 参考素材类型，固定填写 image。
    # 【input.input_references[].url】(string, 必填) 当前代理示例中的图片地址。
    # 使用上方处理结果，可为公网 HTTPS 或本地图片转换后的 data URL。
    input_references.append({"type": "image", "url": image_url})

payload = {
    # 【model】(string, 必填) 模型名称。
    # DMXAPI 代理的批量图生 3D 任务固定填写 neural4d-2.5。
    "model": "neural4d-2.5",

    # 【input】(object, 必填) DMXAPI 代理的生成参数对象。
    # 除 input_references 外均为可选参数；批量模式不支持 n 和 pose。
    "input": {
        # 【input.input_references】(object[], 必填) 2-10 张参考图片处理后的数组。
        # 每个元素为 {"type": "image", "url": 图片地址}，每张图片各生成一个模型。
        "input_references": input_references,

        # 【input.image_enhancement】(bool, 可选) 是否在生成前增强批次中的每张输入图片。
        # 默认值为 false。
        "image_enhancement": False,

        # 【input.with_texture】(bool, 可选) 是否生成纹理贴图。
        # 默认值为 false，即只生成白模；需要贴图时设为 true。
        "with_texture": False,

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
  "created_at": 1793011130,
  "mode": "batch_image_to_3d",
  "output": [
    {
      "type": "message",
      "content": [
        {
          "type": "output_text",
          "text": "8ce35661-d4d1-4799-9725-cb83e13884b4"
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
        "id": "8ce35661-d4d1-4799-9725-cb83e13884b4",
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
  "created_at": 1793011130,
  "mode": "batch_image_to_3d",
  "output": [
    {
      "type": "message",
      "content": [
        {
          "type": "output_text",
          "text": "2c4abbc0-b6e8-4c85-ab82-621ed4f531ed"
        },
        {
          "type": "output_text",
          "text": "https://s3.neural4d.com/71fa652d-08bb-4f7f-9003-6c8e3b56b469_0_mesh.glb?sign=1788220800-dreammaker-0-9b5e30ea1566edb2696015b6aa309e23&response-content-disposition=attachment;filename=4db47d647e2d699ce08aa86988ab0f63.glb"
        },
        {
          "type": "output_text",
          "text": "https://s3.neural4d.com/71fa652d-08bb-4f7f-9003-6c8e3b56b469_0_mesh_preview.jpg?sign=1788220800-dreammaker-0-2d38392871e8c1711b4813fccd076c06&response-content-disposition=attachment;filename=8752a63c8cb226cd62070379051812ec.jpg"
        }
      ]
    },
    {
      "type": "message",
      "content": [
        {
          "type": "output_text",
          "text": "69f17055-cdb5-410d-95df-f6b959b8d21e"
        },
        {
          "type": "output_text",
          "text": "https://s3.neural4d.com/16da0b0e-0b4c-49bc-b71b-3cb8a997ab04_0_mesh.glb?sign=1788220800-dreammaker-0-bfc255465e2835c6a8be4d4583cbac5f&response-content-disposition=attachment;filename=b52b07486db064cdd3997ab016ec879f.glb"
        },
        {
          "type": "output_text",
          "text": "https://s3.neural4d.com/16da0b0e-0b4c-49bc-b71b-3cb8a997ab04_0_mesh_preview.jpg?sign=1788220800-dreammaker-0-8b27fdc604167bf75e6cce4072b2eae5&response-content-disposition=attachment;filename=df12cf24bc269689d27f6e547d04b914.jpg"
        }
      ]
    }
  ],
  "status": "succeeded",
  "updated_at": 1793011232,
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
  <small>© 2026 DMXAPI neural4d-2.5 批量图生 3D</small>
</p>
