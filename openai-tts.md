# OpenAI 请求格式 TTS 语音合成 API 文档
TTS (Text-to-Speech) 将文本转换为自然语音的技术

## 🔗 请求地址

```
https://www.dmxapi.cn/v1/audio/speech
```

## 🤖 支持的模型

| 模型名称 | 说明 |
|---------|------|
| `gpt-4o-mini-tts` | GPT-4o Mini TTS 模型 |
| `tts-1-hd` | 高清音质 TTS 模型 |
| `tts-1` | 标准 TTS 模型 |

## 📝 参数说明

| 参数 | 类型 | 必填 | 说明 | 可选值 |
|------|------|------|------|--------|
| `model` | string | ✅ | 语音合成模型 | `gpt-4o-mini-tts`, `tts-1-hd`, `tts-1` |
| `input` | string | ✅ | 待合成的文本内容 | - |
| `voice` | string | ✅ | 语音音色 | `alloy`, `ash`, `ballad`, `coral`, `echo`, `fable`, `onyx`, `nova`, `sage`, `shimmer`, `verse` |
| `speed` | float | ❌ | 语速 | `0.25` - `4.0` (默认: `1.0`) |
| `response_format` | string | ❌ | 音频格式 | `mp3`, `opus`, `aac`, `flac`, `wav`, `pcm` (默认: `mp3`) |


## 💻 Python 调用示例

```python
"""
DMXAPI 语音合成服务示例
功能:将文本转换为语音并保存为文件
"""

import requests
import json
import os
from datetime import datetime

# ==================== 配置部分 ====================
# DMXAPI接口地址
url = "https://www.dmxapi.cn/v1/audio/speech"

# API密钥(请替换为您自己的密钥)
api_key = "sk-*******************************************"

# 请求参数配置
payload = {
    "model": "gpt-4o-mini-tts",              # 语音合成模型
    "input": "我是DMXAPI,欢迎使用语音合成服务",  # 待合成的文本内容
    "voice": "alloy",                         # 语音音色选择(可选alloy, ash, ballad, coral, echo, fable, onyx, nova, sage, shimmer, and verse)
    "speed": 1 ,                            # 语速(可选0.25-4)
    "response_format": "mp3"                  # 响应格式(mp3, opus, aac, flac, wav, and pcm)
}

# ==================== 主程序 ====================
try:
    # 步骤1: 创建输出目录
    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)
    print("📁 输出目录已准备就绪")
    
    # 步骤2: 发送语音合成请求
    print("🚀 正在请求语音合成服务...")
    response = requests.post(url, 
                           headers={"Authorization": f"{api_key}"},
                           json=payload)
    
    # 步骤3: 检查响应状态码
    response.raise_for_status()
    
    # 步骤4: 处理并保存音频文件
    if response.headers["Content-Type"] in ("audio/mpeg", "audio/mp3"):
        # 生成时间戳格式: YYYYMMDD_HHMMSS
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # 构建带时间戳的输出文件路径
        output_path = os.path.join(output_dir, f"output_{timestamp}.mp3")
        
        # 以二进制模式写入音频文件
        with open(output_path, "wb") as f:
            f.write(response.content)
        
        print(f"✅ 语音合成成功!文件已保存至: {output_path}")
    else:
        # 处理非音频响应
        print("❌ 错误响应:", response.text)

except requests.exceptions.RequestException as e:
    # 捕获网络请求相关异常
    print(f"❌ 网络请求错误: {e}")
except Exception as e:
    # 捕获其他异常
    print(f"❌ 程序执行出错: {e}")
```

## 📤 返回示例

```bash
📁 输出目录已准备就绪
🚀 正在请求语音合成服务...
✅ 语音合成成功!文件已保存至: output\output_20251106_233105.mp3
```

## 🎯 注意事项

- 请确保 API 密钥的安全性,不要在公开代码中暴露
- 语速参数范围为 0.25 到 4.0,建议使用 0.5 到 2.0 之间的值
- 不同的音频格式适用于不同场景,`mp3` 适合一般用途,`flac` 适合高质量需求

---

<p align="center">
  <small>© 2025 DMXAPI OpenAI TTS</small>
</p>