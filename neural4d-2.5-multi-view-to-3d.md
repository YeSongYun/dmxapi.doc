# neural4d-2.5 多视图生 3D API 使用文档

本文介绍如何通过 DMXAPI 代理调用 Neural4D，使用同一物体 2–6 张不同视角的图片生成 3D 模型，其中必须包含正面 `front` 和背面 `back`，且同一视角不能重复。调用采用两阶段异步流程：先使用 `neural4d-2.5` 提交任务并获取批次任务 ID，再使用 `neural4d-get` 将该 ID 放入 `input.id` 查询模型结果；该模式固定使用 high 质量的三角网格，可设置贴图、PBR、目标面数和生成数量。

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

## 多视图生 3D 提交任务示例代码

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

# 【图片】同一物体不同角度的图片，每项填本地图片路径或公网 HTTPS 图片链接。
# 视角可选: "front"（正面）/ "back"（背面）/ "left"（左侧）/ "right"（右侧）/ "top"（顶部）/ "bottom"（底部）。
# 共 2-6 张，必须包含 front 和 back，同一视角只能出现一次。
# 图片支持 JPG、JPEG、PNG、WEBP，每张不超过 10 MiB，一次请求总量不超过 128 MiB。
# 示例图来自 Hunyuan3D-2 开源仓库的多视图样例。
views = {
    "front": "https://cdn.jsdelivr.net/gh/Tencent-Hunyuan/Hunyuan3D-2@main/assets/example_mv_images/1/front.png",
    "back": "https://cdn.jsdelivr.net/gh/Tencent-Hunyuan/Hunyuan3D-2@main/assets/example_mv_images/1/back.png",
    # 其余视角可选，按需添加，例如：
    # "left": "https://cdn.jsdelivr.net/gh/Tencent-Hunyuan/Hunyuan3D-2@main/assets/example_mv_images/1/left.png",
    # "right": "C:/path/to/your/right.png",
    # "top": "C:/path/to/your/top.png",
    # "bottom": "C:/path/to/your/bottom.png",
}

# 当前示例将本地图片按扩展名转成 base64 data URL，HTTPS 链接原样使用。
# 随附说明称网关会处理后续上传，不需要单独调用上传接口。
mime_types = {
    ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg",
    ".png": "image/png",
    ".webp": "image/webp",
}
multi_view_images = []
for view_type, image in views.items():
    if image.startswith("https://"):
        image_url = image
    else:
        extension = "." + image.rsplit(".", 1)[-1].lower()
        if extension not in mime_types:
            raise ValueError(f"只支持 JPG、JPEG、PNG、WEBP 图片：{image}")
        with open(image, "rb") as image_file:
            image_url = f"data:{mime_types[extension]};base64," + base64.b64encode(image_file.read()).decode()
    # 【input.multi_view_images[].view_type】(string, 必填) 图片视角。
    # 可选 front / back / left / right / top / bottom；必须含 front 和 back，且不能重复。
    # 【input.multi_view_images[].url】(string, 必填) 当前代理示例中的图片地址。
    # 使用上方处理结果，可为公网 HTTPS 或本地图片转换后的 data URL。
    multi_view_images.append({"view_type": view_type, "url": image_url})

payload = {
    # 【model】(string, 必填) 模型名称。
    # DMXAPI 代理的多视图生 3D 任务固定填写 neural4d-2.5。
    "model": "neural4d-2.5",

    # 【input】(object, 必填) DMXAPI 代理的生成参数对象。
    # 除 multi_view_images 外均为可选参数。
    # 多视图固定使用 high 质量的三角网格，不能传 mesh_quality、topology、pose、image_enhancement。
    "input": {
        # 【input.multi_view_images】(object[], 必填) 多视图参考图片数组。
        # 每个元素为 {"view_type": 视角, "url": 图片地址}，不需要 type 字段。
        "multi_view_images": multi_view_images,

        # 【input.with_texture】(bool, 可选) 是否生成纹理贴图。
        # 默认值为 false，即只生成白模；需要贴图时设为 true。
        "with_texture": False,

        # 【input.with_pbr】(bool, 可选) 是否生成 PBR 材质。
        # 默认值为 false；设为 true 时，with_texture 必须也为 true。
        "with_pbr": False,

        # 【input.target_polycount】(int, 可选) 目标面数。
        # 多视图使用 high 质量的三角网格，范围为 500000-1000000，默认 500000，以 1000 递增。
        "target_polycount": 500000,

        # 【input.n】(int, 可选) 生成的模型数量。
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
  "created_at": 1793011335,
  "mode": "multi_view_to_3d",
  "output": [
    {
      "type": "message",
      "content": [
        {
          "type": "output_text",
          "text": "cd92f9e3-a885-4a27-b2f5-4c0ef59a2bdd"
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
    "output_tokens": 7100,
    "output_tokens_details": {
      "reasoning_tokens": 0
    },
    "total_tokens": 7100
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
        "id": "cd92f9e3-a885-4a27-b2f5-4c0ef59a2bdd",
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
  "created_at": 1793011335,
  "mode": "multi_view_to_3d",
  "output": [
    {
      "type": "message",
      "content": [
        {
          "type": "output_text",
          "text": "425ebae3-987e-4533-b42b-b8579048ab35"
        },
        {
          "type": "output_text",
          "text": "https://s3.neural4d.com/openapi226850850354bccd7574d0e57a5890dad0b259bpng0_825a04a8-d8f8-40c8-b7cc-0342a8df3fc8_mesh.glb?sign=1788220800-dreammaker-0-9e17124ed8251af5f2756c0a903f997c&response-content-disposition=attachment;filename=b1372404c4d679a3e0821ec67c5a17c0.glb"
        },
        {
          "type": "output_text",
          "text": "https://s3.neural4d.com/openapi226850850354bccd7574d0e57a5890dad0b259bpng0_825a04a8-d8f8-40c8-b7cc-0342a8df3fc8_mesh_preview.jpg?sign=1788220800-dreammaker-0-46e25429a53240b1c3ca171b6bb53b1a&response-content-disposition=attachment;filename=8a11ecf52667a202ce8a892269f22148.jpg"
        }
      ]
    }
  ],
  "status": "succeeded",
  "updated_at": 1793011459,
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
  <small>© 2026 DMXAPI neural4d-2.5 多视图生 3D</small>
</p>
