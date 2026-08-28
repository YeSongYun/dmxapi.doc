# mureka-9.5-pure 生成纯音乐 API 使用文档

基于 Mureka 9.5 纯音乐模型的器乐生成接口，通过 `/v1/responses` 端点以异步任务方式调用。只需一段最长 1024 个字符的提示词描述曲风、速度与情绪即可生成无人声的纯器乐作品，单次请求最多生成 3 首（缺省 2 首，按数量计费），任务完成后一次性返回 mp3、flac、wav 三种格式的音频链接，适合视频配乐、播客垫乐、店铺循环 BGM 等只需要伴奏与氛围音乐的场景。

## 接口地址

| 接口 | 请求方式 | URL |
|------|---------|-----|
| 提交任务 | POST | `https://www.dmxapi.cn/v1/responses` |
| 获取结果 | POST | `https://www.dmxapi.cn/v1/responses` |



:::warning
请妥善保管您的 API Key！严禁将密钥泄露给他人、硬编码到代码中或提交到公开的代码仓库。如果怀疑密钥已泄露，请立即前往 DMXAPI 官网重新生成。
:::

## 模型名称

- `mureka-9.5-pure`

## 生成纯音乐 示例代码

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
    "model": "mureka-9.5-pure",

    # 【n】(integer, 可选) 每次请求生成的纯音乐数量
    # 最大值为 3，缺省为 2
    # 注意会根据数量计费
    "n": 2,

    # 【input】(string, 可选) 提示词内容，对应官方 prompt 参数
    # 通过输入提示词控制纯音乐的生成，最大 1024 个字符
    # 除单独此选项控制外，不支持与其他控制选项的组合
    "input": "r&b, slow, passionate, male vocal"
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

```json
{
  "id": "157744881467393",
  "output": [
    {
      "type": "message",
      "content": [
        {
          "type": "output_text",
          "text": "157744881467393"
        }
      ]
    }
  ],
  "usage": {
    "input_tokens": 0,
    "input_tokens_details": {
      "cached_tokens": 0
    },
    "output_tokens": 20000,
    "output_tokens_details": {
      "reasoning_tokens": 0
    },
    "total_tokens": 20000
  }
}
```

返回中的 `id` 即异步纯音乐生成任务的任务 ID，用于第二步查询生成结果。

## 获取生成音乐 示例代码

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

    "model": "mureka-get-pure",
    "input": "157744881467393"

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
  "created_at": 1787897021,
  "finished_at": 1787897105,
  "id": "157744881467393",
  "model": "mureka-9.5",
  "output": [
    {
      "type": "message",
      "content": [
        {
          "type": "output_text",
          "text": "https://cdn.mureka.cn/cos-prod/open/instrumental/20260828/156296359706625-7vviyXwVD6Kk21eAVub9b2.mp3"
        },
        {
          "type": "output_text",
          "text": "https://cdn.mureka.cn/cos-prod/open/instrumental/20260828/156296359706625-WSqQAc8riWJN4N2Q4pn5FW.flac"
        },
        {
          "type": "output_text",
          "text": "https://cdn.mureka.cn/cos-prod/open/instrumental/20260828/156296359706625-WSqQAc8riWJN4N2Q4pn5FW.wav"
        }
      ]
    },
    {
      "type": "message",
      "content": [
        {
          "type": "output_text",
          "text": "https://cdn.mureka.cn/cos-prod/open/instrumental/20260828/156296359706625-KhyEZ8e936asB1wsiJ2RJQ.mp3"
        },
        {
          "type": "output_text",
          "text": "https://cdn.mureka.cn/cos-prod/open/instrumental/20260828/156296359706625-VCMADUxWrpPDf3AkYccNRq.flac"
        },
        {
          "type": "output_text",
          "text": "https://cdn.mureka.cn/cos-prod/open/instrumental/20260828/156296359706625-VCMADUxWrpPDf3AkYccNRq.wav"
        }
      ]
    }
  ],
  "status": "succeeded",
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
  },
  "watermarked": true
}
```

字段说明：`status` 为任务的当前状态，取值为 `preparing`、`queued`、`running`、`streaming`、`reviewing`、`succeeded`、`failed`、`timeouted`、`cancelled`；`created_at` / `finished_at` 为任务创建与完成的时间戳（以秒为单位）；`watermarked` 为 `true` 时表示在生成音乐的尾部添加了 5s 水印音频。

<p align="center">
  <small>© 2026 DMXAPI mureka-9.5-pure 生成纯音乐</small>
</p>
