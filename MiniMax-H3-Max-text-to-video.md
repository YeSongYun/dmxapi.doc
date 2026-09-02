# MiniMax-H3-Max 文生视频 API 使用文档

基于 MiniMax H3 系列极速生成版本 MiniMax-H3-Max 的文生视频接口，通过 `/v1/responses` 端点以异步任务方式调用。仅凭一段文本提示词即可生成 5~15 秒视频，支持 480P / 768P 两档分辨率（默认 768P）与 21:9、16:9、4:3、1:1、3:4、9:16 六种宽高比，单条提示词最长 7000 个字符，并可选择为成片添加 AIGC 标识水印。提交任务后返回任务 ID，再用查询模型换取视频下载地址，适合广告分镜、短视频创意、影视概念预演等需要快速出片的场景。

## 接口地址

| 接口 | 请求方式 | URL |
|------|---------|-----|
| 提交任务 | POST | `https://www.dmxapi.cn/v1/responses` |
| 获取结果 | POST | `https://www.dmxapi.cn/v1/responses` |



:::warning
请妥善保管您的 API Key！严禁将密钥泄露给他人、硬编码到代码中或提交到公开的代码仓库。如果怀疑密钥已泄露，请立即前往 DMXAPI 官网重新生成。
:::

## 模型名称

- `MiniMax-H3-Max`

## 文生视频 示例代码

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
    # MiniMax-H3-Max 为极速生成版本，支持文生视频与图生视频（首帧 / 尾帧）
    # 不支持中间帧，也不支持多模态参考（参考图 / 参考视频 / 参考音频）
    "model": "MiniMax-H3-Max",

    # 【input】(array[object], 必填) 多模态输入内容数组，描述用于生成视频的信息
    # 每个元素通过 type 区分类型（text / image_url / video_url / audio_url）
    # 每次请求必须包含一个非空 text 项（提示词必填），缺失会返回参数错误
    # 文生视频场景：数组中仅含一个 text 元素
    "input": [
        {
            # 【type】(string, 必填) 输入内容的类型
            # 可选值: "text"(文本) / "image_url"(图片) / "video_url"(视频) / "audio_url"(音频)
            "type": "text",

            # 【text】(string, 必填) 文本提示词，描述期望生成的视频内容
            # 所有场景都需包含一个非空 text
            # 长度按字符数计算，单个 text 最多 7000 个字符
            "text": "简笔画，画里的小人国军队出发攻打特洛伊"
        }
    ],

    # 【resolution】(string, 必填) 视频分辨率
    # 可选值:
    #   - "480P"
    #   - "768P"(默认值)
    # 本模型不支持 2K 档位
    "resolution": "768P",

    # 【duration】(integer, 必填) 生成视频时长（秒），整数
    # 取值范围: 5~15，本模型不支持 4 秒
    "duration": 15,

    # 【ratio】(string, 条件必填) 生成视频的宽高比
    # 文生视频场景（input 仅含 text）下必填，且不能取 "adaptive"
    # 可选值: "21:9" / "16:9" / "4:3" / "1:1" / "3:4" / "9:16"
    "ratio": "16:9",

    # 【aigc_watermark】(boolean, 可选) 是否在生成视频中添加 AIGC 标识水印
    # 默认值: false
    "aigc_watermark": False
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

## 返回示例

提交成功后，`output[0].content[0].text` 即为任务 ID，用于第二步查询结果。

```json
{
  "output": [
    {
      "type": "message",
      "content": [
        {
          "type": "output_text",
          "text": "436676456050979"
        }
      ]
    }
  ],
  "usage": {
    "input_tokens": 0,
    "input_tokens_details": {
      "cached_tokens": 0
    },
    "output_tokens": 75000,
    "output_tokens_details": {
      "reasoning_tokens": 0
    },
    "total_tokens": 75000
  }
}
```

## 获取生成视频 示例代码

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

    "model": "MiniMax-H3-get",
    "input": "436676456050979"

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

`task.status` 为任务状态，取值 `queued`（排队中）、`running`（运行中）、`succeeded`（成功）、`failed`（失败）、`cancelled`（已取消）；状态为 `succeeded` 时，`task.content.url` 即为视频下载地址。

```json
{
  "task": {
    "id": "436676456050979",
    "model": "MiniMax-H3-Max",
    "status": "succeeded",
    "created_at": 1788163985,
    "updated_at": 1788164013,
    "content": {
      "url": "https://algeng-video-infer.oss-cn-shanghai.aliyuncs.com/h3-480p%2F2026%2F08%2F31%2Ffal%2F436676456050979-1-7bc5914c375bce10.mp4?Expires=1788250428&OSSAccessKeyId=LTAI5tA8yjKg7HvBRDpzZ8Nk&Signature=O%2BZZ8nospe1nCXIlgY2Eqax2Kz8%3D"
    },
    "resolution": "768P",
    "duration": 15,
    "usage": {
      "total_seconds": 15,
      "input_seconds": 0,
      "output_seconds": 15,
      "input_image_count": 0
    },
    "ratio": "16:9",
    "task_type": "generation"
  },
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
  <small>© 2026 DMXAPI MiniMax-H3-Max 文生视频</small>
</p>
