# hitem3d-2-0-251223 多图生 3D 模型 API 使用文档

基于数美 Hitem3D-2.0（hitem3d-2-0-251223）模型的图生 3D 接口，通过 `/v1/responses` 端点以异步任务方式调用。输入 1~4 张物体多视角图片（仅支持公网 URL），配合 `--multi_images_bit` 视图标识位标记各图片对应的视角（前、后、左、右），生成一个 3D 模型文件；分辨率支持 1536 / 1536pro 两档，模型面数最高 200 万面，输出格式支持 obj / glb / stl / fbx / usdz，生成结果以下载链接的形式返回（链接有效期 7 天）。本示例演示「前 + 后」两张图的双视角生成场景，适合电商商品、手办模型、工业件等需要多视角精确重建 3D 模型的应用。

## 接口地址

| 接口 | 请求方式 | URL |
|------|---------|-----|
| 提交任务 | POST | `https://www.dmxapi.cn/v1/responses` |
| 获取结果 | POST | `https://www.dmxapi.cn/v1/responses` |



:::warning
请妥善保管您的 API Key！严禁将密钥泄露给他人、硬编码到代码中或提交到公开的代码仓库。如果怀疑密钥已泄露，请立即前往 DMXAPI 官网重新生成。
:::

## 模型名称

- `hitem3d-2-0-251223`（提交任务）
- `hitem3d-2-0-251223-get`（获取结果）

## 四种标准配置与计费

通过 `--resolution`（分辨率：`1536` 标准 / `1536pro` 高精）与 `--request_type`（`1` 仅生成纯几何白模 / `3` 一次性生成几何 + 纹理模型）两个参数的组合，对应以下四种标准配置。

| 配置 | `--resolution`（分辨率） | `--request_type`（生成类型） | 费用 |
|------|------|------|------|
| 标准白模 | `1536` | `1` | 5.80 元/次 |
| 标准纹理模型 | `1536` | `3` | 10.15 元/次 |
| 高精白模 | `1536pro` | `1` | 8.70 元/次 |
| 高精纹理模型 | `1536pro` | `3` | 13.05 元/次 |

## 多图生 3D 模型（2 张图）示例代码

```python
import requests
import json

# ===============================================================
# 步骤1: 配置 API 连接信息
# ===============================================================

# DMXAPI 服务端点地址
url = "https://www.dmxapi.cn/v1/responses"

# DMXAPI 密钥 (请替换为您自己的密钥)
# 获取方式: 登录 DMXAPI 官网 -> 个人中心 -> API 密钥管理
api_key = "sk-***********************************************"

# ===============================================================
# 步骤2: 配置请求头
# ===============================================================

headers = {
    "Content-Type": "application/json",      # 指定请求体为 JSON 格式
    "Authorization": f"{api_key}",           # token 认证方式
}

# ===============================================================
# 步骤3: 配置请求参数
# ===============================================================

payload = {
    # 【model】(string, 必填) 调用的模型名称
    "model": "hitem3d-2-0-251223",

    # 【input】(array[object], 必填) 输入给模型用于生成 3D 模型文件的信息
    # 包含一个文本信息元素和 1~4 个图片信息元素
    "input": [
        {
            # 【文本信息】(object, 可选) 当前仅支持参数命令，不支持自然语言提示词
            # type (string, 必填) 输入内容的类型，此处应为 "text"
            "type": "text",

            # text (string, 必填) 通过 --[parameters] 的方式控制 3D 文件输出的规格:
            #   --ff (integer, 可选, 默认值 1, fileformat 的简写)
            #     生成的有纹理的 3D 模型文件格式，可选值:
            #       - 1: obj    - 2: glb    - 3: stl    - 4: fbx    - 5: usdz
            #   --resolution (string, 可选, 默认值 1536)
            #     3D 模型的分辨率，可选值: "1536" / "1536pro"
            #   --face (integer, 可选)
            #     模型面数，取值范围 [100000, 2000000]
            #     1536 与 1536pro 分辨率的官方推荐面数均为 2000000
            #   --request_type (integer, 可选, 默认值 3)
            #     请求类型，可选值:
            #       - 1: 仅生成纯几何模型
            #       - 3: 一次性生成几何 + 纹理模型
            #   --multi_images_bit (string, 可选)
            #     上传图像的位图标识，由 0/1 组成，按位标记各视图是否传入图像
            #     视图顺序依次为: 前视图、后视图、左视图、右视图
            #     1 表示该位置有对应视图图像，图片数组顺序与值为 1 的视图顺序一致
            #     取值示例:
            #       - "1100": 前视图 + 后视图，图片顺序 [前视图, 后视图]（本示例）
            #       - "1010": 前视图 + 左视图，图片顺序 [前视图, 左视图]
            #       - "1111": 四视图齐全，图片顺序 [前视图, 后视图, 左视图, 右视图]
            #       - "0101": 后视图 + 右视图，图片顺序 [后视图, 右视图]
            "text": "--ff 2 --resolution 1536pro --face 2000000 --request_type 3 --multi_images_bit 1100 ",
        },
        {
            # 【图片信息 1】前视图 (对应 multi_images_bit 第 1 位)
            # type (string, 必填) 输入内容的类型，此处应为 "image_url"
            # image_url.url (string, 必填) 图片信息，仅支持图片 URL（不支持 Base64），
            # 请确保图片 URL 可被公网访问。传入图片需要满足以下条件:
            #   - 格式支持: jpg、jpeg、png、webp
            #   - 文件大小: 小于等于 10MB
            #   - 总像素: 小于 4096 x 4096 px
            #   - 数量: 最多上传 4 张图片
            "type": "image_url",
            "image_url": {
                "url": "https://ark-project.tos-cn-beijing.volces.com/doc_3D/front_view.png",
            },
        },
        {
            # 【图片信息 2】后视图 (对应 multi_images_bit 第 2 位)
            "type": "image_url",
            "image_url": {
                "url": "https://ark-project.tos-cn-beijing.volces.com/doc_3D/back_view.png",
            },
        },
    ],
}

# ===============================================================
# 步骤4: 发送请求并输出结果
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
  "id": "cgt-20260611224507-4fj62",
  "usage": {
    "total_tokens": 130500,
    "input_tokens": 0,
    "input_tokens_details": {
      "cached_tokens": 0
    },
    "output_tokens": 130500,
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
   本脚本演示如何查询 hitem3d-2-0-251223 图生 3D 任务结果，
   并从返回结果中解析出 3D 模型文件（.glb）的下载链接

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
    "model": "hitem3d-2-0-251223-get",

    # 【input】(string, 必填) 提交任务时返回的任务 ID
    "input": "cgt-20260611224507-4fj62"
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

def extract_file_url(data):
    """从查询返回体中提取 3D 模型文件下载链接。

    返回体中 output[].content[].text 是一段 JSON 字符串（嵌套 JSON），
    需要再次 json.loads 解析，才能取到 content.file_url 字段。
    任务未完成或结构异常时返回 None。
    下载链接有效期 7 天，请及时保存。
    """
    try:
        for item in data.get("output", []):              # 遍历 output 数组
            for content in item.get("content", []):      # 遍历每条消息的 content 数组
                text = content.get("text")               # 取出嵌套的 JSON 字符串
                if not text:
                    continue
                inner = json.loads(text)                 # 二次解析为字典
                file_url = inner.get("content", {}).get("file_url")   # 提取下载链接
                if file_url:
                    return file_url
    except (json.JSONDecodeError, AttributeError, TypeError):
        pass                                             # 解析失败时静默返回 None
    return None

file_url = extract_file_url(result)
if file_url:
    print("\n可直接打开的下载链接：")
    print(file_url)
else:
    print("\n未获取到文件链接（任务可能尚未完成或返回结构异常）")
```

## 返回示例

```json
{
  "request_id": "cgt-20260611224507-4fj62",
  "output": [
    {
      "type": "message",
      "content": [
        {
          "type": "output_text",
          "text": "{\"content\":{\"file_url\":\"https://ark-common-storage-prod-cn-beijing.tos-cn-beijing.volces.com/ark-async-gateway/hitem3d-2-0/cgt-20260611224507-4fj62/02178118910836000000000000000000000ffffac1921d078a6f7.glb?X-Tos-Algorithm=TOS4-HMAC-SHA256\\u0026X-Tos-Credential=AKLTYWJkZTExNjA1ZDUyNDc3YzhjNTM5OGIyNjBhNDcyOTQ%2F20260611%2Fcn-beijing%2Ftos%2Frequest\\u0026X-Tos-Date=20260611T145809Z\\u0026X-Tos-Expires=604800\\u0026X-Tos-Signature=4dd1dc98d12781ab445e80517fa61ef4c4d5f45ae9b87f73bcf2defbde79986f\\u0026X-Tos-SignedHeaders=host\"},\"id\":\"cgt-20260611224507-4fj62\",\"model\":\"hitem3d-2-0-251223\",\"status\":\"succeeded\"}"
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
  <small>© 2026 DMXAPI hitem3d-2-0-251223 多图生 3D 模型（2 张图）</small>
</p>
