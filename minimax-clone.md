# MiniMax 音频文件上传 API 使用文档

上传音频文件用于声音克隆，支持两种用途：
- **voice_clone**: 上传复刻音频，用于快速复刻原始声音
- **prompt_audio**: 上传示例音频，用于增强语音合成的音色相似度和稳定性



## 请求地址

```
https://www.dmxapi.cn/v1/responses
```

## 模型名称

- `minimax-clone-upload`

## 示例代码

```python
import requests
import json
import base64
# ═══════════════════════════════════════════════════════════════
# 🔑 步骤1: 配置 API 连接信息
# ═══════════════════════════════════════════════════════════════

# 🌐 DMXAPI 服务端点地址
url = "https://www.dmxapi.cn/v1/responses"

# 🔐 DMXAPI 密钥 (请替换为您自己的密钥)
# 获取方式: 登录 DMXAPI 官网 -> 个人中心 -> API 密钥管理
api_key = "sk-*****************************************"
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

# 请替换为您自己的音频文件路径
# 上传的音频文件格式需为：mp3、m4a、wav格式；时长最少应不低于10秒，最长应不超过5分钟
# 上传的音频文件大小需不超过20mb
with open(r"C:\Users\a1\Desktop\测试保存代码\shili01.m4a", "rb") as f:
    audio_base64 = base64.b64encode(f.read()).decode()

payload = {
    "model": "minimax-clone-upload",
    "input": [{
        # 【purpose】文件用途，根据需求选择：
        #    - "voice_clone": 上传复刻音频（快速复刻原始声音）
        #    - "prompt_audio": 上传示例音频（用于克隆的提示音频）
        # 两种用途都支持 mp3、m4a、wav 格式
        "purpose": "prompt_audio"  # 或 "prompt_audio"
    }],
    "dataf": audio_base64
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
  "file": {
    "file_id": 365865350209649,
    "bytes": 203955,
    "created_at": 1770876014,
    "filename": "audio.mp3",
    "purpose": "prompt_audio"
  },
  "base_resp": {
    "status_code": 0,
    "status_msg": "success"
  },
  "usage": {
    "total_tokens": 203,
    "input_tokens": 0,
    "input_tokens_details": {
      "cached_tokens": 0
    },
    "output_tokens": 203,
    "output_tokens_details": {
      "reasoning_tokens": 0
    }
  }
}
```

<p align="center">
  <small>© 2026 DMXAPI MiniMax 音频文件上传</small>
</p>
