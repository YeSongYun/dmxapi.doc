# scidraw01 图片生成 API 使用文档

基于 SciDraw scidraw01 模型的科研绘图文生图接口，通过 DMXAPI 代理的 `/v1/responses` 端点以异步任务方式调用。提交阶段以 `input` 传入图像描述文本，并可通过 `aspect_ratio`、`resolution`、`count` 控制输出比例、分辨率与张数；提交后立即返回状态为 `queued` 的任务对象，再以 `scidraw-get` 携带任务 ID 查询，任务成功后从 `data.result.files[].url`（或 `output[0].result`）读取生成图片的下载地址。适合细胞结构图、实验流程图、机理示意图等科研配图的快速产出。

## 接口地址

| 接口 | 请求方式 | URL |
|------|---------|-----|
| 提交任务 | POST | `https://www.dmxapi.cn/v1/responses` |
| 获取结果 | POST | `https://www.dmxapi.cn/v1/responses` |

:::warning
请妥善保管您的 API Key！严禁将密钥泄露给他人、硬编码到代码中或提交到公开的代码仓库。如果怀疑密钥已泄露，请立即前往 DMXAPI 官网重新生成。
:::

## 模型名称

- 提交任务：`scidraw01`
- 获取结果：`scidraw-get`

## 图片生成 示例代码

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
    "model": "scidraw01",

    # 【input】(string, 必填) 图像描述提示词
    # 描述期望生成的科研图像内容，本示例使用英文提示词
    # 去掉首尾空白后长度须在 5~2000 字符之间
    "input": "A labeled plant cell diagram",

    # 【aspect_ratio】(string, 可选) 输出图片的宽高比
    # 默认值为 "1:1"，可选值: "1:1" / "16:9" / "9:16" / "4:3" / "3:4" / "3:2" / "2:3" / "5:4" / "4:5" / "21:9"
    "aspect_ratio": "4:3",

    # 【resolution】(string, 可选) 输出图片的分辨率
    #  默认值为 "2K"，可选值: "2K" / "4K"
    "resolution": "2K",

    # 【count】(integer, 可选) 生成图片的数量
    #  默认值为 1，取值范围: 1~4
    "count": 1
}

# ===============================================================
# 步骤4: 发送请求并输出结果
# ===============================================================

# 发送 POST 请求到 API 服务器
response = requests.post(url, headers=headers, json=payload)

# 格式化输出 JSON 响应
# - indent=2: 缩进 2 空格，便于阅读
# - ensure_ascii=False: 正确显示中文字符
print(json.dumps(response.json(), indent=2, ensure_ascii=False))
```

## 提交任务返回示例

```json
{
  "data": {
    "id": "job_3f9c1a7e5b2d4c8ea1f6d0b7c9e2a4d1",
    "object": "image_job",
    "type": "image_generation",
    "status": "queued",
    "created_at": "2026-09-09T04:04:58.403Z",
    "completed_at": null,
    "credits_reserved": 5,
    "credits_consumed": 0,
    "result": null,
    "error": null
  },
  "output": [
    {
      "content": [
        {
          "text": "id: job_3f9c1a7e5b2d4c8ea1f6d0b7c9e2a4d1",
          "type": "output_text"
        },
        {
          "text": "status: queued",
          "type": "output_text"
        }
      ],
      "role": "assistant",
      "status": "completed",
      "type": "message"
    }
  ],
  "success": true,
  "usage": {
    "input_tokens": 0,
    "input_tokens_details": {
      "cached_tokens": 0
    },
    "output_tokens": 35000,
    "output_tokens_details": {
      "reasoning_tokens": 0
    },
    "total_tokens": 35000
  }
}
```

> `data.id` 的值即为任务 ID，用于后续查询任务状态与结果。按上游官方文档，`data.status` 可能为 `queued`（已接受，等待执行）、`processing`（正在处理）、`succeeded`（可读取 `result.files`）、`failed`（`error` 中包含错误码与文案）、`canceled`（任务不会继续运行），终态不会再次变化。

## 获取图片结果 示例代码

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
    # 【input】(string, 必填) 提交任务时返回的任务 ID (data.id)
    "input": "job_3f9c1a7e5b2d4c8ea1f6d0b7c9e2a4d1",

    # 【model】(string, 必填) 查询结果固定使用 "scidraw-get"
    "model": "scidraw-get"
}

# ===============================================================
# 步骤4: 发送请求并输出结果
# ===============================================================

# 发送 POST 请求到 API 服务器
response = requests.post(url, headers=headers, json=payload)

# 格式化输出 JSON 响应
# - indent=2: 缩进 2 空格，便于阅读
# - ensure_ascii=False: 正确显示中文字符
print(json.dumps(response.json(), indent=2, ensure_ascii=False))
```

## 获取结果返回示例

```json
{
  "data": {
    "id": "job_3f9c1a7e5b2d4c8ea1f6d0b7c9e2a4d1",
    "object": "image_job",
    "type": "image_generation",
    "status": "succeeded",
    "created_at": "2026-09-09T04:04:58.403Z",
    "completed_at": "2026-09-09T04:05:13.601Z",
    "credits_reserved": 5,
    "credits_consumed": 5,
    "result": {
      "files": [
        {
          "id": "file_8d2e6a4c1b7f4e9da3c5b1f0e7d2a6c8",
          "url": "https://your-cdn.example.com/generated-image.jpeg",
          "format": "jpeg",
          "mime_type": "image/jpeg"
        }
      ]
    },
    "error": null
  },
  "output": [
    {
      "result": "https://your-cdn.example.com/generated-image.jpeg",
      "type": "image_generation_call"
    }
  ],
  "success": true,
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

> 任务成功后，`data.result.files[].url` 与 `output[0].result` 均为生成图片的下载地址，`format` / `mime_type` 标明文件格式。

<p align="center">
  <small>© 2026 DMXAPI scidraw01 图片生成</small>
</p>
