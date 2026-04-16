# paiwo-audio 音频上传 API 使用文档

paiwo-audio 是拍我 AI 开放平台提供的音视频资源上传接口，通过 DMXAPI 代理调用。支持将本地音频文件（base64 编码）或远程 URL 上传至拍我 AI 平台，获取可用于后续数字人视频生成、对口型（Lipsync）等功能的 media_id 和资源 URL。支持 mp3、wav、m4a、aac 等主流音频格式，单文件最大 50MB、最长 30 秒。

## 请求地址

```
https://www.dmxapi.cn/v1/responses
```

## 模型名称

- `paiwo-audio`

:::warning
请妥善保管您的 API Key！严禁将密钥泄露给他人、硬编码到代码中或提交到公开的代码仓库。
:::

## 示例代码

::: code-group

```python [本地上传]
import requests
import json
import base64

# ═══════════════════════════════════════════════════════════════
# 步骤1: 配置 API 连接信息
# ═══════════════════════════════════════════════════════════════

# DMXAPI 服务端点地址
url = "https://www.dmxapi.cn/v1/responses"

# DMXAPI 密钥 (请替换为您自己的密钥)
# 获取方式: 登录 DMXAPI 官网 -> 个人中心 -> API 密钥管理
api_key = "sk-******************************************"

# ═══════════════════════════════════════════════════════════════
# 步骤2: 配置请求头
# ═══════════════════════════════════════════════════════════════

headers = {
    "Content-Type": "application/json",  # 指定请求体为 JSON 格式
    "Authorization": f"{api_key}",       # token 认证方式
}

# ═══════════════════════════════════════════════════════════════
# 步骤3: 配置请求参数
# ═══════════════════════════════════════════════════════════════

# 读取音频文件并转为 base64
# 替换为实际音频文件路径
# 支持格式: mp3、wav、m4a、aac
# 文件限制: 最大 50MB，最大时长 30 秒
audio_path = "C:/Users/15664/Desktop/PixVerse-Virtual human/audio_file.wav"
with open(audio_path, "rb") as f:
    audio_base64 = base64.b64encode(f.read()).decode("utf-8")

payload = {
    # 【model】(string, 必填) 模型标识符，固定填写 "paiwo-audio"
    # 指定调用拍我AI开放平台的音视频资源上传接口
    "model": "paiwo-audio",

    # 【input】(string, 必填) 音频文件内容的 base64 编码字符串
    # 将本地音频文件读取后进行 base64 编码传入
    # 支持格式: mp3 / wav / m4a / aac
    # 最大文件大小: 50MB
    # 最大时长: 30 秒
    "input": audio_base64,
}

# ═══════════════════════════════════════════════════════════════
# 步骤4: 发送请求并输出结果
# ═══════════════════════════════════════════════════════════════

# 发送 POST 请求到 API 服务器
response = requests.post(url, headers=headers, json=payload)

# 格式化输出 JSON 响应
# - indent=2: 缩进 2 空格，便于阅读
# - ensure_ascii=False: 正确显示中文字符
print(json.dumps(response.json(), indent=2, ensure_ascii=False))
```

```python [URL 上传]
import requests
import json

# ═══════════════════════════════════════════════════════════════
# 步骤1: 配置 API 连接信息
# ═══════════════════════════════════════════════════════════════

# DMXAPI 服务端点地址
url = "https://www.dmxapi.cn/v1/responses"

# DMXAPI 密钥 (请替换为您自己的密钥)
# 获取方式: 登录 DMXAPI 官网 -> 个人中心 -> API 密钥管理
api_key = "sk-******************************************"

# ═══════════════════════════════════════════════════════════════
# 步骤2: 配置请求头
# ═══════════════════════════════════════════════════════════════

headers = {
    "Content-Type": "application/json",      # 指定请求体为 JSON 格式
    "Authorization": f"{api_key}",           # token 认证方式
}

# ═══════════════════════════════════════════════════════════════
# 步骤3: 配置请求参数
# ═══════════════════════════════════════════════════════════════

payload = {
    # 【model】(string, 必填) 模型标识符，固定填写 "paiwo-audio"
    # 指定调用拍我AI开放平台的音视频资源上传接口
    "model": "paiwo-audio",

    # 【input】(string, 必填) 音频文件的远程 URL 地址
    # 与本地文件上传（base64）二选一，此处使用 URL 方式上传
    # 支持格式: mp3 / wav / m4a / aac
    # 对应 mime-type: audio/mpeg、audio/wav、audio/x-m4a、audio/aac 等
    # 文件限制: 最大文件大小 50MB，最大时长 30 秒
    "input": "",  # 替换为实际音频文件 URL
}

# ═══════════════════════════════════════════════════════════════
# 步骤4: 发送请求并输出结果
# ═══════════════════════════════════════════════════════════════

# 发送 POST 请求到 API 服务器
response = requests.post(url, headers=headers, json=payload)

# 格式化输出 JSON 响应
# - indent=2: 缩进 2 空格，便于阅读
# - ensure_ascii=False: 正确显示中文字符
print(json.dumps(response.json(), indent=2, ensure_ascii=False))
```

:::

## 返回示例

```json
{
  "ErrCode": 0,
  "ErrMsg": "success",
  "Resp": {
    "media_id": 397178991941405,
    "media_type": "audio",
    "url": "https://media.pixverseai.cn/openapi/eceae2a3-4c19-4173-a617-62d0280b667b.mp3"
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
  <small>© 2026 DMXAPI paiwo-audio 音频上传</small>
</p>
