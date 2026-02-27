# MiniMax 声音克隆 API 使用文档
使用本接口进行音色快速复刻，支持可选的降噪、音量归一化等音频处理功能，并可生成试听音频。复刻得到的音色若 7 天内未正式调用，则系统会删除该音色。

## 请求地址

```
https://www.dmxapi.cn/v1/responses
```

## 模型名称

- `minimax-clone-lastversion`

## 示例代码

```python
import requests
import json
# ═══════════════════════════════════════════════════════════════
# 🔑 步骤1: 配置 API 连接信息
# ═══════════════════════════════════════════════════════════════

# 🌐 DMXAPI 服务端点地址
url = "https://www.dmxapi.cn/v1/responses"

# 🔐 DMXAPI 密钥 (请替换为您自己的密钥)
# 获取方式: 登录 DMXAPI 官网 -> 个人中心 -> API 密钥管理
api_key = "sk-**************************************"
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
    "model": "minimax-clone-lastversion",
    "input": [{
        # 待复刻音频的 file_id
        # 通过 minimax-clone 接口上传音频（purpose="voice_clone"）获取
        "file_id": 365592225681803
        }],

    # 克隆音色的 voice_id，正确示例："MiniMax001"。用户进行自定义 voice_id 时需注意：
    # 1.自定义的 voice_id 长度范围[8,256]
    # 2.首字符必须为英文字母
    # 3.允许数字、字母、-、_
    # 4.末位字符不可为 -、_
    # 5.voice_id 不可与已有 id 重复，否则会报错
    "voice_id": "Jonathan08",

    # 【clone_prompt】音色复刻示例音频
    # 提供本参数将有助于增强语音合成的音色相似度和稳定性。若使用本参数，需同时上传一小段示例音频
    # 上传的音频文件格式需为：mp3、m4a、wav 格式
    # 上传的音频文件的时长小于 8 秒
    # 上传的音频文件大小需不超过 20 mb

    "clone_prompt": {

        # 示例音频文件 ID
        # 通过 minimax-clone 接口上传音频（purpose="prompt_audio"）获取
        "prompt_audio": 365589324152946,
        
        # 提示文本（描述音频内容或风格）
        "prompt_text": "咬定青山不放松，立根原在破岩中。千磨万击还坚劲，任尔东西南北风。"
    },

    # ==================== 音频处理选项 ====================
    "need_noise_reduction": False,       # 音频复刻参数，表示是否开启降噪，默认值为 false
    "need_volume_normalization": False,  # 音频复刻参数，是否开启音量归一化，默认值为 false
    "aigc_watermark": False ,     # 是否在合成试听音频的末尾添加音频节奏标识，默认值为 false

    # 【language_boost】是否增强对指定的小语种和方言的识别能力。默认值为 null，可设置为 auto 让模型自主判断。
    "language_boost": ""                  
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
  "input_sensitive": false,
  "input_sensitive_type": 0,
  "demo_audio": "https://minimax-algeng-chat-tts.oss-cn-wulanchabu.aliyuncs.com/audio%2Feffect%2F05dcb500f1b53510f49f988b543c095f_1770881550285_8496.mp3?Expires=1771054350&OSSAccessKeyId=LTAI5tGLnRTkBjLuYPjNcKQ8&Signature=J4rvOlPU7PBAEEmwaLIDzbz0Wxc%3D",
  "base_resp": {
    "status_code": 0,
    "status_code": 0,
    "status_msg": "success"
  },
    "status_msg": "success"
  },
  "usage": {
    "total_tokens": 1,
  "usage": {
    "total_tokens": 1,
    "input_tokens": 0,
    "input_tokens": 0,
    "input_tokens_details": {
    "input_tokens_details": {
      "cached_tokens": 0
    },
    "output_tokens": 1,
    "output_tokens_details": {
      "reasoning_tokens": 0
    }
  }
}
```

<p align="center">
  <small>© 2026 DMXAPI MiniMax 声音克隆</small>
</p>
