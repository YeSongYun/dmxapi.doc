# OpenAI 语音转文本 API 文档

> STT (Speech-to-Text) / ASR (Automatic Speech Recognition) 语音识别服务

## 📡 接口地址

| 服务类型 | 接口地址 | 说明 |
|---------|---------|------|
| 音频翻译 | `https://www.dmxapi.cn/v1/audio/translations` | 将音频翻译成英文 |
| 音频转写 | `https://www.dmxapi.cn/v1/audio/transcriptions` | 将音频转写为繁体中文 |

## 🤖 模型名称

`whisper-1`



## 🎯 Python 音频翻译示例

### 功能说明
使用 Whisper 模型将音频文件翻译成英文

### 代码示例
```python
"""
音频翻译 API 调用脚本
使用 Whisper 模型将音频文件翻译成英文
"""

import requests
import os
import json

# ==================== 配置部分 ====================

# 从环境变量获取 API 密钥(可选,当前代码中使用硬编码的密钥)
api_key = os.getenv("OPENAI_API_KEY")

# DMXAPI 端点地址 - 音频翻译服务
url = "https://www.dmxapi.cn/v1/audio/translations"

# 请求头配置 - 包含身份验证信息
headers = {
    "Authorization": f"sk-********************************" # 请替换为你的DMXAPI真实密钥
}

# 待翻译的音频文件路径
audio_file_path = "test/output_20251104_113808.mp3"

# ==================== 发送请求 ====================

# 以二进制只读模式打开音频文件
with open(audio_file_path, "rb") as audio_file:
    # 构建 multipart/form-data 格式的文件数据
    files = {
        "file": audio_file,              # 音频文件对象(支持 flac, mp3, mp4, mpeg, mpga, m4a, ogg, wav, or webm)
        "model": (None, "whisper-1"),    # 使用的模型名称
    }
    
    # 发送 POST 请求到翻译 API
    response = requests.post(url, headers=headers, files=files)

# ==================== 处理响应 ====================

# 打印响应的基本信息
print(f"状态码: {response.status_code}")
print("=" * 50)
print("响应内容:")
print("=" * 50)

# 如果请求成功(状态码 200),尝试解析 JSON 响应
if response.status_code == 200:
    try:
        # 解析并以格式化的 JSON 格式打印响应数据
        response_data = response.json()
        print(json.dumps(response_data, ensure_ascii=False, indent=2))
    except requests.exceptions.JSONDecodeError:
        # 如果响应不是有效的 JSON 格式,输出原始文本
        print(f"响应不是 JSON 格式:")
        print(response.text)
else:
    # 如果请求失败,也尝试格式化输出错误信息
    try:
        error_data = response.json()
        print(json.dumps(error_data, ensure_ascii=False, indent=2))
    except:
        print(response.text)
```
### 📊 返回示例
```json
状态码: 200
==================================================
响应内容:
==================================================
{
  "text": "Hello, Oliver Smith. I am your smart virtual assistant, Max. Thank you for calling. I have found your file. The phone number is 14154-159921. The balance is 1234.56 yuan. The related IP address is 192.168.1.1. Your next payment date is May 6, 2032. If you have any questions, please contact support-vip at technet.com."
}
```


## 🎯 Python 音频转写示例

### 功能说明
使用 Whisper 模型将音频文件转写为文字

### 代码示例
```python
"""
┌─────────────────────────────────────────────────────────────┐
│ 音频转写 API 调用脚本                                        │
│ 功能: 使用 Whisper 模型将音频文件转写为文字                   │
│ API: DMXAPI - Whisper 音频转写服务                           │
└─────────────────────────────────────────────────────────────┘
"""

import requests
import os
import json

# ╔════════════════════════════════════════════════════════════╗
# ║                         配置部分                           ║
# ╚════════════════════════════════════════════════════════════╝

# 【API 密钥配置】
# 从环境变量获取 API 密钥(推荐使用环境变量以保护密钥安全)
api_key = os.getenv("OPENAI_API_KEY")

# 【API 端点配置】
# DMXAPI 音频转写服务地址
url = "https://www.dmxapi.cn/v1/audio/transcriptions"

# 【请求头配置】
# 包含 Token 身份验证信息
headers = {
    "Authorization": f"sk-*******************************************"  # ⚠️ 请替换为你的DMXAPI真实 API 密钥
}

# 【音频文件配置】
# 待转写的音频文件路径(支持 flac, mp3, mp4, mpeg, mpga, m4a, ogg, wav, or webm)
audio_file_path = "test/output_20251104_113808.mp3"

# ╔════════════════════════════════════════════════════════════╗
# ║                      发送 API 请求                         ║
# ╚════════════════════════════════════════════════════════════╝

# 【文件上传与请求】
# 以二进制只读模式打开音频文件
with open(audio_file_path, "rb") as audio_file:
    # 构建 multipart/form-data 格式的文件数据
    files = {
        "file": audio_file,              # 音频文件二进制流
        "model": (None, "whisper-1"),    # 指定使用 Whisper-1 模型
    }
    
    # 发送 POST 请求到音频转写 API
    response = requests.post(url, headers=headers, files=files)

# ╔════════════════════════════════════════════════════════════╗
# ║                      处理 API 响应                         ║
# ╚════════════════════════════════════════════════════════════╝

# 【输出基本信息】
print(f"📊 HTTP 状态码: {response.status_code}")
print("=" * 60)
print("📄 响应内容:")
print("=" * 60)

# 【成功响应处理】
# 如果请求成功(HTTP 200),解析并格式化输出 JSON 数据
if response.status_code == 200:
    try:
        # 解析 JSON 响应数据
        response_data = response.json()
        # 格式化输出,保留中文字符,缩进 2 个空格
        print(json.dumps(response_data, ensure_ascii=False, indent=2))
    except requests.exceptions.JSONDecodeError:
        # 如果响应不是有效的 JSON 格式,输出原始文本
        print("⚠️ 响应不是 JSON 格式:")
        print(response.text)
else:
    # 【错误响应处理】
    # 如果请求失败,尝试格式化输出错误信息
    try:
        error_data = response.json()
        print("❌ 错误详情:")
        print(json.dumps(error_data, ensure_ascii=False, indent=2))
    except:
        # 如果错误响应也不是 JSON 格式,直接输出原始文本
        print("❌ 请求失败,原始响应:")
        print(response.text)
```
### 📊 返回示例
```json
📊 HTTP 状态码: 200
============================================================
📄 响应内容:
============================================================
{
  "text": "您好,Oliver Smith,我是您的智能虛擬助手,Max,感謝您的來電,我已找到您的檔案,電話號碼14154-159921的未付清餘額為1234.56元,關聯的IP地址是192.168.1.1,您的下一個付款到7日,是2032年5月6日,如有任何疑問,請聯繫support-vip at technet.com。 多謝您收睇時局新聞,再會!"
}    
```


## ⚠️ 注意事项

- **文件大小限制**: 音频文件大小建议不超过 25MB
- **支持语言**: 支持中文、英文等多种语言
- **安全提醒**: 请妥善保管 API 密钥,切勿泄露或提交到公共代码仓库

---

<p align="center">
  <small>© 2026 DMXAPI OpenAI STT</small>
</p>