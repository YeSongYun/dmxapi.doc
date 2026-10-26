# neural4d-2.5 文生 3D API 使用文档

本文介绍如何通过 DMXAPI 代理调用 Neural4D，将文本提示词生成 3D 模型。调用采用两阶段异步流程：先使用 `neural4d-2.5` 提交任务，从响应的 `output[0].content[0].text` 获取批次任务 ID，再使用 `neural4d-get` 将该 ID 放入 `input.id` 查询模型结果；可按需设置贴图、PBR、网格质量、拓扑、目标面数、姿态和生成数量。

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

## 文生 3D 提交任务示例代码

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
    # DMXAPI 代理的文生 3D 任务固定填写 neural4d-2.5。
    "model": "neural4d-2.5",

    # 【input】(object, 必填) DMXAPI 代理的生成参数对象。
    "input": {
        # 【input.prompt】(string, 必填) 描述待生成模型的文本提示词。
        # 不能为空，最多 500 个字符。
        "prompt": "白色摄影棚背景中的陶瓷茶壶",

        # 【input.with_texture】(bool, 可选) 是否生成纹理贴图。
        # 默认值为 false，即只生成白模；需要贴图时设为 true。
        "with_texture": True,

        # 【input.with_pbr】(bool, 可选) 是否生成 PBR 材质。
        # 默认值为 false；设为 true 时，with_texture 必须也为 true。
        "with_pbr": True,

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

        # 【input.n】(int, 可选) 生成的模型数量。
        # 默认值为 1，范围为 1-4；本示例设置为 2。
        "n": 2,
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
  "created_at": 1793009441,
  "mode": "text_to_3d",
  "output": [
    {
      "type": "message",
      "content": [
        {
          "type": "output_text",
          "text": "6131e530-7965-402c-85c6-37bff802057a"
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
    "output_tokens": 42600,
    "output_tokens_details": {
      "reasoning_tokens": 0
    },
    "total_tokens": 42600
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
        "id": "6131e530-7965-402c-85c6-37bff802057a",
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
  "created_at": 1793009441,
  "mode": "text_to_3d",
  "output": [
    {
      "type": "message",
      "content": [
        {
          "type": "output_text",
          "text": "41a54b90-ab8e-4f3d-92b5-89ebf6fa6145"
        },
        {
          "type": "output_text",
          "text": "https://cos.neural4d.com/pbr/857c602366fa4d048193ca389b849eb2/textured_mesh.glb?q-sign-algorithm=sha1&q-ak=AKIDVxDH8oGX9e0CCyW3KXgjbGl5FF5wmcVU&q-sign-time=1793013241;1795605241&q-key-time=1793013241;1795605241&q-header-list=host&q-url-param-list=response-content-disposition&q-signature=9ee31fbc5cae60458104caf97b30fdb97e288fbb&response-content-disposition=attachment;filename=b0115859739d0a05f907e0be89a0cc56.glb"
        },
        {
          "type": "output_text",
          "text": "https://cos.neural4d.com/pbr/857c602366fa4d048193ca389b849eb2/preview.jpg?q-sign-algorithm=sha1&q-ak=AKIDVxDH8oGX9e0CCyW3KXgjbGl5FF5wmcVU&q-sign-time=1793013241;1795605241&q-key-time=1793013241;1795605241&q-header-list=host&q-url-param-list=response-content-disposition&q-signature=4a768c0d9b7f96b4073cc9bbc067a10a37a372b6&response-content-disposition=attachment;filename=c5a06729fd3c3f15d4029d6e06f9f480.jpg"
        }
      ]
    },
    {
      "type": "message",
      "content": [
        {
          "type": "output_text",
          "text": "61b34ba0-21dd-4565-b5b5-48c8cc3ecd4a"
        },
        {
          "type": "output_text",
          "text": "https://cos.neural4d.com/pbr/1161207319e54cc883356d0f7cf4eaa6/textured_mesh.glb?q-sign-algorithm=sha1&q-ak=AKIDVxDH8oGX9e0CCyW3KXgjbGl5FF5wmcVU&q-sign-time=1793013241;1795605241&q-key-time=1793013241;1795605241&q-header-list=host&q-url-param-list=response-content-disposition&q-signature=bf54edb40300f991d1c35c13f19bcc26a40527ea&response-content-disposition=attachment;filename=ee8abee325ad7ef374274ca842b82679.glb"
        },
        {
          "type": "output_text",
          "text": "https://cos.neural4d.com/pbr/1161207319e54cc883356d0f7cf4eaa6/preview.jpg?q-sign-algorithm=sha1&q-ak=AKIDVxDH8oGX9e0CCyW3KXgjbGl5FF5wmcVU&q-sign-time=1793013241;1795605241&q-key-time=1793013241;1795605241&q-header-list=host&q-url-param-list=response-content-disposition&q-signature=46b2bbc2eb720c762ca105938d35f1a457166ae6&response-content-disposition=attachment;filename=67d04b35a4769cfc533a9c64090eb0ac.jpg"
        }
      ]
    }
  ],
  "status": "succeeded",
  "updated_at": 1793009858,
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
  <small>© 2026 DMXAPI neural4d-2.5 文生 3D</small>
</p>
