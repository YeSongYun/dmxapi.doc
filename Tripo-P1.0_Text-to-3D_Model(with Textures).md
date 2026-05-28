# Tripo-P1.0 文生3D模型（有贴图）API 使用文档

Tripo-P1.0 文生3D模型（有贴图）接口用于基于一段自然语言提示词直接生成带贴图的 3D 模型资产，无需提供任何参考图片。文本提示词支持中文、英文等多语言输入，每个字符均计为 1 个字符，最大长度 1024 个字符。贴图质量提供 `standard`（标清，默认）与 `detailed`（高清）两档可选，便于在生成速度与材质细节之间权衡。

## 接口地址

| 接口 | 请求方式 | URL |
|------|---------|-----|
| 提交任务 | POST | `https://www.dmxapi.cn/v1/responses` |
| 获取结果 | POST | `https://www.dmxapi.cn/v1/responses` |

:::tip
本接口使用 DMXAPI 的 Responses 端点封装底层 Tripo 异步 3D 生成能力。提交请求后不会直接返回 GLB 文件，而是先返回任务状态与 `task_id`。
:::

:::warning
请妥善保管您的 API Key！严禁将密钥泄露给他人、硬编码到代码中或提交到公开的代码仓库。如果怀疑密钥已泄露，请立即前往 DMXAPI 官网重新生成。
:::

## 模型名称

- `Tripo-P1.0`


## 文生3D模型（有贴图）示例代码

```python
import requests
import json

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
    # prompt、image、images 三者互斥，当前示例使用 prompt 进行文生3D模型生成
    "input": {
        # 【prompt】(string, 条件必填) 文本提示词，用于描述期望生成的 3D 模型，仅在文生3D模型时必填
        # 支持多语言（中文、英文等），每个字符（含中文汉字、英文字母等）均计为 1 个字符
        # 最大长度 1024 个字符
        # 示例值：一只可爱的猫
        "prompt": "一只可爱的猫"
    },
    # 【parameters】(object, 可选) 3D 模型生成参数
    "parameters": {
        # 【texture_quality】(string, 可选) 贴图质量
        # 贴图是覆盖在 3D 模型表面的纹理图像，决定模型的外观细节和视觉效果
        # 可选值: "standard"(默认，标清贴图) / "detailed"(高清贴图)
        "texture_quality": "standard"
    },
}

# 步骤4：发送请求并输出结果
response = requests.post(url, headers=headers, json=payload)
print(json.dumps(response.json(), indent=2, ensure_ascii=False))
```

## 返回示例

```json
{
  "request_id": "7d9c0844-41a2-961d-b30b-494bee27b083",
  "output": [
    {
      "type": "message",
      "content": [
        {
          "type": "output_text",
          "text": "{\"task_id\":\"637380a7-a0fb-449e-9a09-2f9bf77a88db\",\"task_status\":\"PENDING\"}"
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
  <small>© 2026 DMXAPI Tripo-P1.0 文生3D模型（有贴图）</small>
</p>
