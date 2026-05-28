# Tripo-P1.0 单图生3D模型（无贴图）API 使用文档

Tripo-P1.0 单图生3D模型（无贴图）接口用于基于一张参考图快速生成 3D 模型资产，并通过 `texture=false` 与 `pbr=false` 输出无贴图基础模型。该能力适合原型设计、轻量资产生产和需要后续自定义贴图的场景，输入图片支持 JPEG、PNG 格式，宽高范围为 [20, 6000] 像素，文件大小不超过 20 MB；接口采用异步任务模式，请求提交后会先返回 `task_id` 与任务状态。

## 接口地址

| 接口 | 请求方式 | URL |
|------|---------|-----|
| 提交任务 | POST | `https://www.dmxapi.cn/v1/responses` |
| 获取结果 | POST | `https://www.dmxapi.cn/v1/responses` |



:::warning
请妥善保管您的 API Key！严禁将密钥泄露给他人、硬编码到代码中或提交到公开的代码仓库。如果怀疑密钥已泄露，请立即前往 DMXAPI 官网重新生成。
:::

## 模型名称

- `Tripo-P1.0`


## 单图生3D模型（无贴图）示例代码

```python
import json
import requests

# 步骤1：配置 API 连接信息
url = "https://www.dmxapi.cn/v1/responses"
api_key = "sk-******************************************"

# 步骤2：配置请求头
headers = {
    "Content-Type": "application/json",
    "Authorization": f"{api_key}",
}

# 步骤3：配置请求参数
payload = {
    # 【model】(string, 必填) 模型名称
    "model": "Tripo-P1.0",
    # 【input】(object, 必填) 输入信息对象
    # prompt、image、images 三者互斥，当前示例使用 image 进行单图生3D模型生成
    "input": {
        # 【image】(string, 条件必填) 单张输入图片的公网 URL，仅在单图生3D模型时必填
        # 支持 HTTP 和 HTTPS；图片格式为 JPEG、PNG；宽高范围为 [20, 6000] 像素；文件大小不超过 20 MB
        "image": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260424/cfbxhg/tripo-single.jpg",
    },
    # 【parameters】(object, 可选) 3D 模型生成参数
    "parameters": {
        # 【texture_quality】(string, 可选) 贴图质量，决定模型表面纹理细节和视觉效果
        # 可选值: "standard"(默认，标清贴图) / "detailed"(高清贴图)
        "texture_quality": "standard",
        # 【texture】(boolean, 可选) 是否生成贴图，默认值为 true
        # 如需生成无贴图模型，需与 pbr 同时设置为 false
        "texture": False,
        # 【pbr】(boolean, 可选) 是否生成 PBR 材质模型，默认值为 true
        # 当 pbr 为 true 时会强制启用贴图；当前示例设为 false，用于生成无贴图基础模型
        "pbr": False,
    },
}

# 步骤4：发送请求并输出结果
response = requests.post(url, headers=headers, json=payload)
print(json.dumps(response.json(), indent=2, ensure_ascii=False))
```

## 返回示例

```json
{
  "request_id": "0c696123-04e5-9ffa-b689-d71db3d4277e",
  "output": [
    {
      "type": "message",
      "content": [
        {
          "type": "output_text",
          "text": "{\"task_id\":\"99fe5854-67ed-4b2b-9654-e1c6673006ac\",\"task_status\":\"PENDING\"}"
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
  <small>© 2026 DMXAPI Tripo-P1.0 单图生3D模型（无贴图）</small>
</p>
