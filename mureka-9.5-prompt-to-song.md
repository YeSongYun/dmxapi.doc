# mureka-9.5 提示词生成歌曲 API 使用文档

基于 Mureka 9.5 模型的提示词生成歌曲接口，通过 `/v1/responses` 端点以异步任务方式调用。只需一段自然语言提示词（最长 2000 个字符）即可生成带人声的完整歌曲，并可从 pop、rock、jazz、r&b、edm、ambient、folk、latin、k-pop、j-pop、house、gospel、lo-fi 共 13 种风格中任选一个或多个组合控制曲风；单次请求最多生成 3 首（缺省 2 首，按数量计费），任务完成后一次性返回 mp3、flac、wav 三种格式的音频链接，适合短视频配乐、游戏背景音乐、广告 BGM 等需要按描述快速产出成品歌曲的场景。

## 接口地址

| 接口 | 请求方式 | URL |
|------|---------|-----|
| 提交任务 | POST | `https://www.dmxapi.cn/v1/responses` |
| 获取结果 | POST | `https://www.dmxapi.cn/v1/responses` |



:::warning
请妥善保管您的 API Key！严禁将密钥泄露给他人、硬编码到代码中或提交到公开的代码仓库。如果怀疑密钥已泄露，请立即前往 DMXAPI 官网重新生成。
:::

## 模型名称

- `mureka-9.5`

## 提示词生成歌曲 示例代码

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
    "model": "mureka-9.5",

    # 【n】(integer, 可选) 每次请求生成的歌曲数量
    # 最大值为 3，缺省为 2
    # 注意会根据数量计费
    "n": 2,

    # 【styles】(array[string], 可选) 通过输入风格控制音乐生成
    # 可从枚举值中选择一个或多个风格
    # 可选值:
    #   "pop"(流行) / "rock"(摇滚) / "jazz"(爵士) / "r&b"(节奏布鲁斯)
    #   / "edm"(电子舞曲) / "ambient"(氛围) / "folk"(民谣) / "latin"(拉丁)
    #   / "k-pop"(韩流) / "j-pop"(日系流行) / "house"(浩室) / "gospel"(福音)
    #   / "lo-fi"(低保真)
    "styles": [
        "pop",
        "rock"
    ],

    # 【input】(string, 必填) 提示词内容，对应官方 prompt 参数
    # 通过输入提示词控制音乐生成，最大 2000 个字符
    "input": "一首明亮夏日氛围、带有抓耳副歌的情歌"
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
  "id": "157745145708545",
  "output": [
    {
      "type": "message",
      "content": [
        {
          "type": "output_text",
          "text": "157745145708545"
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

返回中的 `id` 即异步音乐生成任务的任务 ID，用于第二步查询生成结果。

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

    "model": "mureka-get",
    "input": "157745145708545"

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
  "created_at": 1787897147,
  "finished_at": 1787897257,
  "id": "157745145708545",
  "model": "mureka-9.5",
  "output": [
    {
      "type": "message",
      "content": [
        {
          "type": "output_text",
          "text": "https://cdn.mureka.cn/cos-prod/open/song/20260828/156296359706625-G8hoe3mZb3DJXtYPnDcB8g.mp3"
        },
        {
          "type": "output_text",
          "text": "https://cdn.mureka.cn/cos-prod/open/song/20260828/156296359706625-Lz8nJSscEMJnpim7k3UaC4.flac"
        },
        {
          "type": "output_text",
          "text": "https://cdn.mureka.cn/cos-prod/open/song/20260828/156296359706625-Lz8nJSscEMJnpim7k3UaC4.wav"
        }
      ]
    },
    {
      "type": "message",
      "content": [
        {
          "type": "output_text",
          "text": "https://cdn.mureka.cn/cos-prod/open/song/20260828/156296359706625-LvgPFJa3NwsUCrSwr1DvDZ.mp3"
        },
        {
          "type": "output_text",
          "text": "https://cdn.mureka.cn/cos-prod/open/song/20260828/156296359706625-RCkVyQLTYQDnRHNpFLztJX.flac"
        },
        {
          "type": "output_text",
          "text": "https://cdn.mureka.cn/cos-prod/open/song/20260828/156296359706625-RCkVyQLTYQDnRHNpFLztJX.wav"
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
  <small>© 2026 DMXAPI mureka-9.5 提示词生成歌曲</small>
</p>
