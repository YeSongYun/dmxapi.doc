# hyper3d-gen2-260112 图生 3D 模型 API 使用文档

基于影眸 Hyper3D-Gen2（Rodin，hyper3d-gen2-260112）模型的图生 3D 接口，通过 `/v1/responses` 端点以异步任务方式调用。输入 1~5 张参考图片（支持公网 URL 或 Base64 编码）+ 可选英文提示词 + 可选参数命令，生成一个 3D 模型文件；支持三角面（Raw）/ 四边面（Quad）两种网格模式、PBR 等四种材质类型、最高 100 万面与 4K 高清贴图，输出格式支持 glb / obj / usdz / fbx / stl，生成结果以下载链接的形式返回（链接有效期 7 天）。本示例演示「前 + 侧 + 后」三张参考图的多视角生成场景，适合游戏资产、影视道具、数字孪生等对网格拓扑与材质质量有较高要求的应用。

## 接口地址

| 接口 | 请求方式 | URL |
|------|---------|-----|
| 提交任务 | POST | `https://www.dmxapi.cn/v1/responses` |
| 获取结果 | POST | `https://www.dmxapi.cn/v1/responses` |



:::warning
请妥善保管您的 API Key！严禁将密钥泄露给他人、硬编码到代码中或提交到公开的代码仓库。如果怀疑密钥已泄露，请立即前往 DMXAPI 官网重新生成。
:::

## 模型名称

- `hyper3d-gen2-260112`（提交任务）
- `hyper3d-gen2-260112-get`（获取结果）

## 多图生 3D 模型（3 张图）示例代码

```python
import requests
import json
import base64

# ===============================================================
# 步骤1: 配置 API 连接信息
# ===============================================================

# DMXAPI 服务端点地址
url = "https://www.dmxapi.cn/v1/responses"

# DMXAPI 密钥 (请替换为您自己的密钥)
# 获取方式: 登录 DMXAPI 官网 -> 个人中心 -> API 密钥管理
api_key = "sk-***********************************************"

# ===============================================================
# 步骤2: 准备输入图片
# ===============================================================

# 本地路径 或 远程 URL 均可，1~5 张
# 传入图片需要满足以下条件:
#   - 格式支持: jpg、jpeg、png
#   - 总像素: 小于 4096 x 4096 px
#   - 文件大小: 小于等于 30MB
#   - 数量: 最多上传 5 张图片
image_sources = [
    "./front_view.png",   # 参考图 1: 正视图
    "./side_view.png",    # 参考图 2: 侧视图
    "./back_view.png",    # 参考图 3: 背视图
]

def to_image_url(source):
    """将图片来源统一转换为接口可用的 url 值。

    远程 URL 直接返回（请确保可被公网访问）；
    本地文件读取后编码为 Base64 data URL，
    格式要求: data:image/<图片格式>;base64,<Base64编码>，<图片格式> 需小写。
    """
    if source.startswith("http://") or source.startswith("https://"):
        return source
    ext = source.rsplit(".", 1)[-1].lower()                            # 取文件扩展名并转小写
    mime = "image/jpeg" if ext in ("jpg", "jpeg") else f"image/{ext}"  # jpg/jpeg 统一映射为 image/jpeg
    with open(source, "rb") as f:
        image_data = base64.b64encode(f.read()).decode("utf-8")        # 二进制 -> Base64 字符串
    return f"data:{mime};base64,{image_data}"                          # 拼接为 data URL


# ===============================================================
# 步骤3: 配置请求头
# ===============================================================

headers = {
    "Content-Type": "application/json",      # 指定请求体为 JSON 格式
    "Authorization": f"{api_key}",           # token 认证方式
}

# ===============================================================
# 步骤4: 配置请求参数
# ===============================================================

payload = {
    # 【model】(string, 必填) 调用的模型名称
    "model": "hyper3d-gen2-260112",

    # 【input】(array[object], 必填) 输入给模型用于生成 3D 模型文件的信息
    # 图生 3D 支持的输入组合: 图片 / 图片+文本 / 图片+参数 / 图片+文本+参数
    "input": [
        {
            # 【文本信息】(object, 可选)
            # type (string, 必填) 输入内容的类型，此处应为 "text"
            "type": "text",

            # text (string, 必填) 文本提示词 + 参数命令:
            # 提示词: 仅支持英文，长度不超过 400 字符，超过后将截断
            #         本示例说明三张参考图分别为前、侧、后视图
            # 参数: 通过 --[parameters] 的方式控制 3D 文件输出的规格:
            #   --mesh_mode (string, 可选, 默认值 Quad)
            #     网格形状，可选值: "Raw"(三角面模型) / "Quad"(四边面模型)
            #   --hd_texture (boolean, 可选, 默认值 false)
            #     是否启用 HD 纹理，可选值: true / false
            #   --material (string, 可选, 默认值 PBR)
            #     材质类型，可选值:
            #       - "PBR"   : 物理基础材质，含基础颜色/金属度/法线/粗糙度纹理，
            #                   高真实感且动态光照下物理准确
            #       - "Shaded": 风格化材质，含基础颜色纹理和烘焙光照
            #       - "All"   : 同时生成 PBR 和 Shaded 材质
            #       - "None"  : 无纹理，即生成白模
            #   --addons (string, 可选)
            #     增强纹理贴图分辨率，可选值: "HighPack"(4K 贴图)；不配置默认 2K 贴图
            #   --quality_override (number, 可选)
            #     自定义多边形面数:
            #       - mesh_mode 为 Raw  时: 范围 [500, 1000000]，默认 500000
            #       - mesh_mode 为 Quad 时: 范围 [1000, 200000]，默认 18000
            #     注意: 与 --subdivisionlevel 同时使用时，--subdivisionlevel 将失效；
            #           官方建议指定面数 ≥ 150000
            #   --use_original_alpha (boolean, 可选, 默认值 false)
            #     透明度处理，可选值:
            #       - true : 保留上传图片透明部分，按原图透明轮廓处理
            #       - false: 透明部分自动填充，可能丢失原始透明效果
            #   --bbox_condition (integer[], 可选)
            #     模型边界尺寸与缩放因子数组: [宽(x轴), 高(y轴), 长(z轴)]
            #     官方建议: 如无特殊需求不指定，由模型自行判定边界
            #   --TAPose (boolean, 可选, 默认值 false)
            #     类人模型姿态控制，可选值:
            #       - true : 强制标准绑定姿态，T-Pose 还是 A-Pose 由模型判定
            #       - false: 不强制，由模型自行决定姿态
            #   --subdivisionlevel (string, 可选, 简写 sl)
            #     多边形面数档位（与 --quality_override 同时使用时失效，本示例已用 quality_override 指定面数，故未传）:
            #       - mesh_mode 为 Raw  时(默认 high)  : high=500k / medium=150k / low=20k
            #       - mesh_mode 为 Quad 时(默认 medium): high=50k  / medium=18k  / low=8k
            #   --fileformat (string, 可选, 默认值 glb, 简写 ff)
            #     输出 3D 模型文件格式，可选值: "glb" / "obj" / "usdz" / "fbx" / "stl"
            "text": "Generate a 3D model from these three reference images showing front, side, and back views. --mesh_mode Raw --hd_texture true --material PBR --addons HighPack --quality_override 1000000 --use_original_alpha false --TAPose false --fileformat glb"
        }
    ] + [
        {
            # 【图片信息】(object) 依次加入每张参考图（最多 5 张）
            # type (string, 必填) 输入内容的类型，此处应为 "image_url"
            # image_url.url (string, 必填) 图片 URL 或 Base64 编码 data URL
            "type": "image_url",
            "image_url": {
                "url": to_image_url(src)
            }
        }
        for src in image_sources
    ],

    # 【seed】(integer, 可选) 种子整数，用于控制生成内容的随机性
    # 取值范围: [0, 65535]
    # 注意: 相同请求下，不同 seed 生成不同结果；
    #       相同 seed 会生成类似的结果，但不保证完全一致
    "seed": 8648
}

# ===============================================================
# 步骤5: 发送请求并输出结果
# ===============================================================

# 发送 POST 请求到 API 服务器
response = requests.post(url, headers=headers, json=payload)

# 格式化输出 JSON 响应
# - indent=2: 缩进 2 空格，便于阅读
# - ensure_ascii=False: 正确显示中文字符
# 返回的 id 字段为 3D 生成任务 ID，用于下一步查询生成结果
print(json.dumps(response.json(), indent=2, ensure_ascii=False))
```

## 返回示例

```json
{
  "id": "cgt-20260611212113-kljvc",
  "usage": {
    "total_tokens": 18000,
    "input_tokens": 0,
    "input_tokens_details": {
      "cached_tokens": 0
    },
    "output_tokens": 18000,
    "output_tokens_details": {
      "reasoning_tokens": 0
    }
  }
}
```

## 获取生成模型 示例代码

```python
"""
╔═══════════════════════════════════════════════════════════════╗
║                  DMXAPI 自研接口                               ║
╚═══════════════════════════════════════════════════════════════╝

📝 功能说明:
   本脚本演示如何查询 hyper3d-gen2-260112 图生 3D 任务结果，
   并从返回结果中解析出任务状态与 3D 模型文件（.glb）的下载链接

═══════════════════════════════════════════════════════════════
"""

import requests
import json

# ═══════════════════════════════════════════════════════════════
# 🔑 步骤1: 配置 API 连接信息
# ═══════════════════════════════════════════════════════════════

# 🌐 DMXAPI 服务端点地址
url = "https://www.dmxapi.cn/v1/responses"

# 🔐 DMXAPI 密钥 (请替换为您自己的密钥)
# 获取方式: 登录 DMXAPI 官网 -> 个人中心 -> API 密钥管理
api_key = "sk-***********************************************"

# ═══════════════════════════════════════════════════════════════
# 📋 步骤2: 配置请求头
# ═══════════════════════════════════════════════════════════════

headers = {
    "Content-Type": "application/json",      # 指定请求体为 JSON 格式
    "Authorization": f"{api_key}",           # token 认证方式
}

# ═══════════════════════════════════════════════════════════════
# 💬 步骤3: 配置请求参数
# ═══════════════════════════════════════════════════════════════

payload = {
    # 【model】(string, 必填) 查询任务使用的模型名称 (提交模型名 + "-get" 后缀)
    "model": "hyper3d-gen2-260112-get",

    # 【input】(string, 必填) 提交任务时返回的任务 ID
    "input": "cgt-20260611212113-kljvc"
}

# ═══════════════════════════════════════════════════════════════
# 📤 步骤4: 发送请求并输出结果
# ═══════════════════════════════════════════════════════════════

# 发送 POST 请求到 API 服务器
response = requests.post(url, headers=headers, json=payload)
result = response.json()

# 格式化输出 JSON 响应
# - indent=2: 缩进 2 空格，便于阅读
# - ensure_ascii=False: 正确显示中文字符
print(json.dumps(result, indent=2, ensure_ascii=False))

# ═══════════════════════════════════════════════════════════════
# 🔍 步骤5: 解析嵌套 JSON，提取任务状态与下载链接
# ═══════════════════════════════════════════════════════════════

# 返回体中 output[0].content[0].text 是一段 JSON 字符串（嵌套 JSON），
# 需要再次 json.loads 解析（json.loads 会自动把 \u0026 还原成 &）
# status 为 "succeeded" 表示生成成功；下载链接有效期 7 天，请及时保存
try:
    inner = json.loads(result["output"][0]["content"][0]["text"])   # 二次解析为字典
except (KeyError, IndexError, TypeError, json.JSONDecodeError):
    # 任务尚未完成或返回结构异常时走此分支，可稍后重试查询
    print("\n未解析到任务结果，请查看上方原始返回")
else:
    status = inner.get("status")                              # 任务状态
    file_url = (inner.get("content") or {}).get("file_url")   # 3D 模型文件下载链接
    print(f"\nstatus: {status}")
    if file_url:
        print(f"file_url: {file_url}")
```

## 返回示例

```json
{
  "request_id": "cgt-20260611212113-kljvc",
  "output": [
    {
      "type": "message",
      "content": [
        {
          "type": "output_text",
          "text": "{\"content\":{\"file_url\":\"https://ark-common-storage-prod-cn-beijing.tos-cn-beijing.volces.com/ark-async-gateway/hyper3d-gen2/cgt-20260611212113-kljvc/02178118407398100000000000000000000ffffac1921d05fdc05.glb?X-Tos-Algorithm=TOS4-HMAC-SHA256\\u0026X-Tos-Credential=AKLTYWJkZTExNjA1ZDUyNDc3YzhjNTM5OGIyNjBhNDcyOTQ%2F20260611%2Fcn-beijing%2Ftos%2Frequest\\u0026X-Tos-Date=20260611T132545Z\\u0026X-Tos-Expires=604800\\u0026X-Tos-Signature=71173dac3217290b0e4650c7a5f324c0a3f77c8c628a972eacdc340602438caf\\u0026X-Tos-SignedHeaders=host\"},\"id\":\"cgt-20260611212113-kljvc\",\"model\":\"hyper3d-gen2-260112\",\"status\":\"succeeded\"}"
        }
      ]
    }
  ],
  "usage": {
    "total_tokens": 0,
    "input_tokens": 0,
    "input_tokens_details": {
      "cached_tokens": 0
    },
    "output_tokens": 0,
    "output_tokens_details": {
      "reasoning_tokens": 0
    }
  }
}
```

<p align="center">
  <small>© 2026 DMXAPI hyper3d-gen2-260112 多图生 3D 模型（3 张图）</small>
</p>
