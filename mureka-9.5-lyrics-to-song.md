# mureka-9.5 歌词生成歌曲 API 使用文档

基于 Mureka 9.5 模型的歌词生成歌曲接口，通过 `/v1/responses` 端点以异步任务方式调用。直接传入自己写好的歌词（最长 5000 个字符，支持 `[主歌]`、`[副歌]` 等段落标签），再用一段最长 1024 个字符的风格提示词描述编曲与演唱风格，即可生成带人声的完整歌曲；支持通过 `gender` 指定 female / male 两种人声性别倾向，单次请求最多生成 3 首（缺省 2 首，按数量计费），任务完成后一次性返回 mp3、flac、wav 三种格式的音频链接，适合已有词作需要快速成曲的原创音乐、翻唱改编与影视配乐场景。

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

## 歌词生成歌曲 示例代码

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
    # 【input】(string, 必填) 歌词内容，对应官方 lyrics 参数
    # 生成音乐的歌词，最大 5000 个字符
    # 可使用 [主歌]、[副歌] 等段落标签划分歌曲结构，用 \n 换行
    "input": "[主歌]\n在暴风雨的夜晚，我独自徘徊\n被雨淋湿，感觉像是被抛弃\n你的回忆，在我眼前闪现\n希望这一刻，能找到一丝幸福",

    # 【model】(string, 必填) 调用的模型名称
    "model": "mureka-9.5",

    # 【n】(integer, 可选) 每次请求生成的歌曲数量
    # 最大值为 3，缺省为 2
    # 注意会根据数量计费
    "n": 1,

    # 【prompt】(string, 可选) 通过输入提示词控制音乐生成
    # 最大 1024 个字符
    # 除单独此选项控制外，支持与其他控制选项的组合: prompt + vocal_id
    "prompt": "r&b, slow, passionate, male vocal",

    # 【gender】(string, 可选) 指定生成歌曲的人声性别倾向
    # 优先遵循上传音频的人声特征
    # 可选值: "female"(女声) / "male"(男声)
    "gender": "female"
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
  "id": "157741777879041",
  "output": [
    {
      "type": "message",
      "content": [
        {
          "type": "output_text",
          "text": "157741777879041"
        }
      ]
    }
  ],
  "usage": {
    "input_tokens": 0,
    "input_tokens_details": {
      "cached_tokens": 0
    },
    "output_tokens": 10000,
    "output_tokens_details": {
      "reasoning_tokens": 0
    },
    "total_tokens": 10000
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
    "input": "157741777879041"

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
  "created_at": 1787895541,
  "finished_at": 1787895621,
  "id": "157741777879041",
  "model": "mureka-9.5",
  "output": [
    {
      "type": "message",
      "content": [
        {
          "type": "output_text",
          "text": "https://cdn.mureka.cn/cos-prod/open/song/20260828/156296359706625-B7k7EFXkMZ4oS1y9kYoAHz.mp3"
        },
        {
          "type": "output_text",
          "text": "https://cdn.mureka.cn/cos-prod/open/song/20260828/156296359706625-7aGzH9ADa5gQsSfvxttTFF.flac"
        },
        {
          "type": "output_text",
          "text": "https://cdn.mureka.cn/cos-prod/open/song/20260828/156296359706625-7aGzH9ADa5gQsSfvxttTFF.wav"
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
  <small>© 2026 DMXAPI mureka-9.5 歌词生成歌曲</small>
</p>
