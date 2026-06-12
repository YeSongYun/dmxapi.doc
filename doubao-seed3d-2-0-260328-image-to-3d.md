# doubao-seed3d-2-0-260328 图生 3D 模型 API 使用文档

基于豆包（火山引擎）doubao-seed3d-2-0-260328 模型的图生 3D 接口，通过 `/v1/responses` 端点以异步任务方式调用。输入 1 张图片（支持公网 URL 或 Base64 编码）+ 可选参数命令，生成一个带纹理和 PBR 材质的 3D 模型文件，输出格式支持 glb / obj / usd / usdz，多边形面数最高 100 万面，生成结果以 zip 压缩包下载链接的形式返回（链接有效期 24 小时），适合电商商品展示、游戏资产制作、3D 打印等从单张图片快速重建 3D 模型的应用。
## 接口地址

| 接口 | 请求方式 | URL |
|------|---------|-----|
| 提交任务 | POST | `https://www.dmxapi.cn/v1/responses` |
| 获取结果 | POST | `https://www.dmxapi.cn/v1/responses` |



:::warning
请妥善保管您的 API Key！严禁将密钥泄露给他人、硬编码到代码中或提交到公开的代码仓库。如果怀疑密钥已泄露，请立即前往 DMXAPI 官网重新生成。
:::

## 模型名称

- `doubao-seed3d-2-0-260328`（提交任务）
- `doubao-seed3d-2-0-260328-get`（获取结果）

## 图生 3D 模型示例代码

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

# 本地路径 或 远程 URL，二选一
# 传入图片需要满足以下条件:
#   - 总像素: 小于 4096 x 4096 px
#   - 文件大小: 小于等于 10MB
#   - 宽高比: (0.4, 2.5)
#   - 格式支持: jpg、jpeg、png、webp、bmp
image_source = "your_image.png"

if image_source.startswith("http://") or image_source.startswith("https://"):
    # 远程图片: 直接使用 URL，请确保图片 URL 可被公网访问
    image_url_value = image_source
else:
    # 本地图片: 读取文件并编码为 Base64 data URL
    # 格式要求: data:image/<图片格式>;base64,<Base64编码>，<图片格式> 需小写
    ext = image_source.rsplit(".", 1)[-1].lower()                      # 取文件扩展名并转小写
    mime = "image/jpeg" if ext in ("jpg", "jpeg") else f"image/{ext}"  # jpg/jpeg 统一映射为 image/jpeg
    with open(image_source, "rb") as f:
        image_data = base64.b64encode(f.read()).decode("utf-8")        # 二进制 -> Base64 字符串
    image_url_value = f"data:{mime};base64,{image_data}"               # 拼接为 data URL

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
    "model": "doubao-seed3d-2-0-260328",

    # 【input】(array[object], 必填) 输入给模型用于生成 3D 文件的信息
    # 包含文本信息和图片信息两类元素
    "input": [
        {
            # 【文本信息】(object, 可选) 当前仅支持参数命令，不支持自然语言提示词
            # type (string, 必填) 输入内容的类型，此处应为 "text"
            "type": "text",

            # text (string, 必填) 通过 --[parameters] 的方式控制 3D 文件输出的规格:
            #   --subdivisionlevel (string, 可选, 默认值 medium, 简写 sl)
            #     3D 文件中多边形面的数量，本模型实际取值:
            #       - "high"  : 1000000 面
            #       - "medium": 500000 面
            #       - "low"   : 100000 面
            #   --fileformat (string, 可选, 默认值 glb, 简写 ff)
            #     生成的 3D 文件格式，可选值: "glb" / "obj" / "usd" / "usdz"
            "text": "--subdivisionlevel medium --fileformat glb",
        },
        {
            # 【图片信息】(object, 必填) 模型根据输入的 2D 图像生成完整的 3D 文件
            # type (string, 必填) 输入内容的类型，此处应为 "image_url"
            "type": "image_url",

            # image_url (object, 必填) 输入给模型的图片对象
            #   - url (string, 必填) 图片 URL 或 Base64 编码 data URL
            "image_url": {
                "url": image_url_value
            },
        },
    ],
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
  "id": "cgt-20260611175315-tjsbh",
  "usage": {
    "total_tokens": 24000,
    "input_tokens": 0,
    "input_tokens_details": {
      "cached_tokens": 0
    },
    "output_tokens": 24000,
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
   本脚本演示如何查询 doubao-seed3d-2-0-260328 图生 3D 任务结果，
   并从返回结果中解析出 3D 模型文件（zip 压缩包）的下载链接

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
    "model": "doubao-seed3d-2-0-260328-get",

    # 【input】(string, 必填) 提交任务时返回的任务 ID
    "input": "cgt-20260611175315-tjsbh"
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
# 🔍 步骤5: 解析嵌套 JSON，提取 3D 文件下载链接
# ═══════════════════════════════════════════════════════════════

# 返回体中 output[0].content[0].text 是一段 JSON 字符串（嵌套 JSON），
# 需要再次 json.loads 解析，才能取到 content.file_url 和 status 字段
# status 为 "succeeded" 表示生成成功；下载链接有效期 24 小时，请及时保存
try:
    text = result["output"][0]["content"][0]["text"]   # 取出嵌套的 JSON 字符串
    inner = json.loads(text)                           # 二次解析为字典
    file_url = inner["content"]["file_url"]            # 提取 zip 压缩包下载链接
    print("\n=== 下载链接 ===")
    print(file_url)
except Exception:
    # 任务尚未完成或返回结构异常时走此分支，可稍后重试查询
    print("\n未获取到文件链接（任务可能尚未完成或返回结构异常）")
```

## 返回示例

```json
{
  "request_id": "cgt-20260611175315-tjsbh",
  "output": [
    {
      "type": "message",
      "content": [
        {
          "type": "output_text",
          "text": "{\"content\":{\"file_url\":\"https://ark-content-generation-cn-beijing.tos-cn-beijing.volces.com/doubao-seed3d-2-0/doubao-seed3d-2-0-02178117159741000000000000000000000ffffac19272e1ed196.zip?X-Tos-Algorithm=TOS4-HMAC-SHA256\\u0026X-Tos-Credential=AKLTYWJkZTExNjA1ZDUyNDc3YzhjNTM5OGIyNjBhNDcyOTQ%2F20260611%2Fcn-beijing%2Ftos%2Frequest\\u0026X-Tos-Date=20260611T095916Z\\u0026X-Tos-Expires=86400\\u0026X-Tos-Signature=1c5ffe4304ab049e4825f2da3adff09958aa127464d92d28f7725f50b232a6af\\u0026X-Tos-SignedHeaders=host\"},\"id\":\"cgt-20260611175315-tjsbh\",\"model\":\"doubao-seed3d-2-0-260328\",\"status\":\"succeeded\"}"
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
  <small>© 2026 DMXAPI doubao-seed3d-2-0-260328 图生 3D 模型</small>
</p>
