# Tripo-P1.0 多图生3D模型（无贴图）API 使用文档

Tripo-P1.0 是基于 Tripo 官方 P1-20260311 版本封装的 3D 模型生成接口，本文聚焦多图生 3D 无贴图模型变体：传入 2～4 张多视角图片（数组顺序固定为前、左、后、右），模型自动重建几何并输出最高 2 万面的 GLB 格式基础模型，相比贴图版本生成速度更快、产物体积更小，适合需要后期自定义贴图或仅做几何展示的场景。整体采用异步任务模式，通过 DMXAPI 封装的"提交任务 → 轮询获取"两步流程完成 3D 模型生成。

## 模型名称

- `Tripo-P1.0`

## 接口地址

| 接口 | 请求方式 | URL |
|------|---------|-----|
| 提交任务 | POST | `https://www.dmxapi.cn/v1/responses` |
| 获取结果 | POST | `https://www.dmxapi.cn/v1/responses` |

:::warning
请妥善保管您的 API Key！严禁将密钥泄露给他人、硬编码到代码中或提交到公开的代码仓库。如果怀疑密钥已泄露，请立即前往 DMXAPI 官网重新生成。
:::

## 多图生3D模型（无贴图）示例代码

```python
import requests
import json

# 步骤1: 配置 API 连接信息

# DMXAPI 服务端点地址
url = "https://www.dmxapi.cn/v1/responses"

# DMXAPI 密钥 (请替换为您自己的密钥)
# 获取方式: 登录 DMXAPI 官网 -> 个人中心 -> API 密钥管理
api_key = "sk-******************************************"

# 步骤2: 配置请求头

headers = {
    "Content-Type": "application/json",
    "Authorization": f"{api_key}",
}

# 步骤3: 配置请求参数

payload = {
    # 【model】(string, 必填) 调用的模型 ID
    "model": "Tripo-P1.0",

    # 【input】(object, 必填) 输入信息
    # prompt / image / images 三者互斥，仅能选择其中一种输入方式，同时传入多个将报错
    # 多图生 3D 模型使用 images 字段
    "input": {
        # 【images】(array[object], 条件必填) 多张图像的对象列表，仅在多图生 3D 模型时必填
        # 数组长度固定为 4，对应图片顺序为前、左、后、右
        # 如某个视角不需要传入图片，传入空对象 {} 即可
        # 实际传入的有效图片数量为 2～4 张
        # 多张图像的分辨率和宽高比不要求一致
        # 单张图像限制：
        #   - 格式：JPEG、PNG
        #   - 分辨率：宽和高的范围为 [20, 6000] 像素，建议边长大于 256 像素
        #   - 文件大小：不超过 20 MB
        #   - 公网 URL：支持 HTTP / HTTPS 协议
        "images": [
            # 【type】(string, 必填) 图像格式，可选值：jpeg / png
            # 【file_token】(string, 必填) 图像的公网 URL
            {"type": "png", "file_token": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260424/liafix/tripo-images-1.png"},
            {"type": "png", "file_token": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260424/slgluy/tripo-images-2.png"},
            {"type": "png", "file_token": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260424/zjqhyn/tripo-images-3.png"},
            {"type": "png", "file_token": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260424/mqfzww/tripo-images-4.png"},
        ]
    },

    # 【parameters】(object, 可选) 3D 模型生成参数
    "parameters": {
        # 【texture_quality】(string, 可选) 贴图质量
        # 贴图是覆盖在 3D 模型表面的纹理图像，决定模型外观细节和视觉效果
        # 可选值：
        #   "standard"：默认值，标清贴图
        #   "detailed"：高清贴图
        # 注意：当前请求 texture/pbr 均为 false（无贴图模式），该字段不参与最终产物渲染
        "texture_quality": "standard",

        # 【texture】(boolean, 可选) 是否生成贴图，默认值为 true
        # 如需生成无贴图模型，需同时设置 texture 和 pbr 为 false
        # 此时返回结果中包含 base_model_url（无贴图基础模型）
        "texture": False,

        # 【pbr】(boolean, 可选) 是否生成 PBR 材质模型，默认值为 true
        # 当 pbr 为 true 时会强制启用贴图（即 texture 也会被设为 true），返回 pbr_model_url
        # 无贴图模式必须将 pbr 与 texture 同时设为 false
        "pbr": False
    },
}

# 步骤4: 发送请求并输出结果

# 发送 POST 请求到 API 服务器
response = requests.post(url, headers=headers, json=payload)

# 格式化输出 JSON 响应
# - indent=2: 缩进 2 空格，便于阅读
# - ensure_ascii=False: 正确显示中文字符
print(json.dumps(response.json(), indent=2, ensure_ascii=False))
```

## 返回示例

```json
{
  "request_id": "9eb88905-2ae4-917f-a922-281fe3b121a8",
  "output": [
    {
      "type": "message",
      "content": [
        {
          "type": "output_text",
          "text": "{\"task_id\":\"8e38c8ca-eee9-405d-ad7e-59323eab5267\",\"task_status\":\"PENDING\"}"
        }
      ]
    }
  ],
  "usage": {
    "total_tokens": 28000,
    "input_tokens": 0,
    "input_tokens_details": {
      "cached_tokens": 0
    },
    "output_tokens": 28000,
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
   本脚本演示如何使用 requests 库调用 DMXAPI 的自研接口

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
    "Authorization": f"{api_key}",    # token 认证方式
}

# ═══════════════════════════════════════════════════════════════
# 💬 步骤3: 配置请求参数
# ═══════════════════════════════════════════════════════════════

payload = {

    "model": "Tripo-P1.0-get",
    "input": "83357750-efae-452f-9dfd-8dddf906df4e"

}


# ═══════════════════════════════════════════════════════════════
# 📤 步骤4: 发送请求并输出结果
# ═══════════════════════════════════════════════════════════════

# 发送 POST 请求到 API 服务器
response = requests.post(url, headers=headers, json=payload)

# 格式化输出 JSON 响应
# - indent=2: 缩进 2 空格，便于阅读
# - ensure_ascii=False: 正确显示中文字符
print(json.dumps(response.json(), indent=2, ensure_ascii=False))


```

## 返回示例

```json
{
  "request_id": "47fe482e-acb2-9e41-8bac-d1017ca068ea",
  "output": [
    {
      "type": "message",
      "content": [
        {
          "type": "output_text",
          "text": "{\"task_id\":\"a57f88ad-5ada-4257-b8bd-163d31337db4\",\"task_status\":\"SUCCEEDED\",\"submit_time\":\"2026-05-28 23:13:55.082\",\"scheduled_time\":\"2026-05-28 23:13:55.111\",\"end_time\":\"2026-05-28 23:15:13.369\",\"results\":[{\"pbr_model_url\":\"https://openapi.cdn.tripo3d.com/tcli_6ec7f9db277c4bca984cf4ee598502c1/20260528/f830f982-3ad5-4d1a-a062-02f57ecdd609/tripo_pbr_model_f830f982-3ad5-4d1a-a062-02f57ecdd609.glb?auth_key=1779988512-IUSzc8lR-0-1f19a2b6a2b0038a9d24fc02c09422b4\",\"rendered_image_url\":\"https://openapi.cdn.tripo3d.com/tcli_6ec7f9db277c4bca984cf4ee598502c1/20260528/f830f982-3ad5-4d1a-a062-02f57ecdd609/legacy_mesh.webp?auth_key=1779988512-lHDHysK4-0-6dd610c8ab8ee02450d75550bd7ffa8e\"}]}"
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
  <small>© 2026 DMXAPI Tripo-P1.0 多图生3D模型（无贴图）</small>
</p>
