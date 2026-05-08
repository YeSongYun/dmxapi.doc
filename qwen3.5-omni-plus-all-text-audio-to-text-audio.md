# qwen3.5-omni-plus-all 文+音频 生 文+音频 API 使用文档

qwen3.5-omni-plus-all 是阿里云通义千问最新一代的全模态大模型，能够接收文本、音频等多种模态的组合输入，并同步输出文字与语音形式的回复。该模型支持 113 种输入音频语种（74 种语言 + 39 种方言）、36 种输出音频语种，提供 55 种拟人化音色选择，最长可处理 3 小时的输入音频，广泛适用于内容审核、文本创作、视觉识别、音视频交互助手等场景，并支持联网搜索能力。

## 请求地址

```
https://www.dmxapi.cn/v1/responses
```

## 模型名称

- `qwen3.5-omni-plus-all`

:::warning
请妥善保管您的 API Key！严禁将密钥泄露给他人、硬编码到代码中或提交到公开的代码仓库。
:::

## 示例代码

```python
import requests
import json
import base64
import time
import os

# ═══════════════════════════════════════════════════════════════
# 步骤1: 配置 API 连接信息
# ═══════════════════════════════════════════════════════════════

url = "https://www.dmxapi.cn/v1/responses"

api_key = "sk-******************************************"

# ═══════════════════════════════════════════════════════════════
# 步骤2: 配置请求头
# ═══════════════════════════════════════════════════════════════

headers = {
    "Content-Type": "application/json",
    "Authorization": f"{api_key}",
}

# ═══════════════════════════════════════════════════════════════
# 步骤3: 配置请求参数
# ═══════════════════════════════════════════════════════════════

payload = {
    # 【model】(string, 必填) 指定调用的全模态模型名称
    # 本文档对应模型: qwen3.5-omni-plus-all
    "model": "qwen3.5-omni-plus-all",

    # 【input】(array, 必填) 对话消息数组，每项为一条消息对象
    # 每条消息包含 role（角色）和 content（内容数组）
    # 说明: 一条 User Message 可以同时包含文本和一种其他模态的数据（音频/图片/视频）
    "input": [
        {
            # 【role】(string, 必填) 消息角色
            # 可选值: "user"(用户) / "assistant"(助手) / "system"(系统)
            # 注意: Assistant Message 只可以包含文本数据
            "role": "user",

            # 【content】(array, 必填) 消息内容数组，元素为多模态内容对象
            "content": [
                {
                    # 【type】(string, 必填) 内容类型
                    # 可选值: "input_audio"(音频输入) / "text"(文本输入) / "image_url"(图片输入) / "video_url"(视频输入)
                    "type": "input_audio",

                    # 【input_audio】(object, 必填) 音频输入对象，仅当 type 为 input_audio 时使用
                    "input_audio": {
                        # 【data】(string, 必填) 音频文件的公网 URL 或 Base64 编码字符串
                        # 支持公网 URL（文件大小限制 2GB）或 Base64 编码（编码后小于 10MB）
                        "data": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250211/tixcef/cherry.wav",

                        # 【format】(string, 必填) 音频文件格式
                        # 可选值: "wav" / "mp3" / "aac" / "flac" / "ogg" 等常见音频格式
                        "format": "wav"
                    }
                },
                {
                    # 【type】(string, 必填) 内容类型，此处为文本
                    "type": "text",

                    # 【text】(string, 必填) 文本内容，可作为指令或问题
                    "text": "这段音频在说什么"
                }
            ]
        }
    ],

    # 【stream】(boolean, 必填) 是否启用流式输出
    # 注意: 所有对 Qwen-Omni 模型的请求都必须设置为 True，否则会报错
    "stream": True,

    # 【stream_options】(object, 可选) 流式输出选项配置
    "stream_options": {
        # 【include_usage】(boolean, 可选) 是否在流式输出末尾返回 Token 用量统计
        # 取值: True(返回) / False(不返回)，默认为 False
        "include_usage": True
    },

    # 【modalities】(array, 必填) 指定输出数据的模态
    # 可选值组合: ["text", "audio"](输出文字+音频) / ["text"](仅输出文字)
    # 注意: 思考模式下仅支持 ["text"]
    "modalities": ["text", "audio"],

    # 【audio】(object, 可选) 音频输出配置，当 modalities 包含 "audio" 时生效
    "audio": {
        # 【voice】(string, 必填) 输出音频的音色名称
        # 实测可用音色: "Tina" / "Serena"（Qwen3.5-Omni 官方声称支持 55 种音色）
        # 注意: 设置无效音色时服务端返回 HTTP 200 但响应为空（Silent Failure），请使用经过验证的音色
        # 完整音色列表请参考: https://help.aliyun.com/zh/model-studio/qwen-omni 的音色列表章节
        "voice": "Tina",

        # 【format】(string, 必填) 输出音频文件格式
        # 可选值: "wav" / "mp3" / "pcm" 等常见音频格式，当前模型推荐 "wav"
        "format": "wav"
    }
}

# ═══════════════════════════════════════════════════════════════
# 步骤4: 发送请求并提取文字与音频
# ═══════════════════════════════════════════════════════════════

text_parts = []
audio_parts = []
usage_info = None
current_event = None

with requests.post(url, headers=headers, json=payload, stream=True) as response:
    if not response.ok:
        print(f"[HTTP {response.status_code}] {response.text}")
        response.raise_for_status()

    for line in response.iter_lines():
        if not line:
            continue
        line = line.decode("utf-8")

        if line.startswith("event:"):
            current_event = line[len("event:"):].strip()
            continue

        if not line.startswith("data:"):
            continue
        data_str = line[len("data:"):].strip()
        if data_str == "[DONE]":
            break

        try:
            data = json.loads(data_str)
        except json.JSONDecodeError:
            continue

        # 文字增量
        if current_event == "response.output_text.delta":
            text = data.get("delta", "")
            if text:
                text_parts.append(text)

        # 音频数据（完整 WAV，base64 编码）
        elif current_event == "response.output_item.done":
            for part in data.get("item", {}).get("content", []):
                if "audio" in part and part["audio"].get("data"):
                    audio_parts.append(part["audio"]["data"])

        # usage 统计
        elif current_event == "response.completed":
            usage_info = data.get("response", {}).get("usage")

# ═══════════════════════════════════════════════════════════════
# 步骤5: 输出文字内容
# ═══════════════════════════════════════════════════════════════

full_text = "".join(text_parts)
print("=" * 50)
print("生成的文字内容:")
print("=" * 50)
print(full_text if full_text else "(无文字输出)")
print("=" * 50)

# ═══════════════════════════════════════════════════════════════
# 步骤5.5: 输出 usage 信息
# ═══════════════════════════════════════════════════════════════

if usage_info:
    print("Token 用量:")
    for key, value in usage_info.items():
        print(f"   {key}: {value}")
    print("=" * 50)

# ═══════════════════════════════════════════════════════════════
# 步骤6: 保存音频为 WAV
# ═══════════════════════════════════════════════════════════════

if audio_parts:
    audio_bytes = base64.b64decode("".join(audio_parts))

    timestamp = time.strftime("%Y%m%d_%H%M%S")
    output_dir = os.path.dirname(os.path.abspath(__file__))

    wav_path = os.path.join(output_dir, f"{timestamp}.wav")
    with open(wav_path, "wb") as f:
        f.write(audio_bytes)
    print(f"音频已保存: {wav_path}")
else:
    print("未收到音频数据")
```

## 返回示例

```text
==================================================
生成的文字内容:
==================================================
这段音频在描述一幅图画的内容。

说话者描述了这样一个场景：
*   **地点**：海滩上。
*   **人物**：一个女人和一只狗正在玩耍。
*   **背景**：海浪拍打着沙滩，天空有点发白，推测时间是日出或日落时分。

最后，说话者还表示如果还有想知道的，可以继续提问。
==================================================
Token 用量:
   input_tokens: 879
   input_tokens_details: {'cached_tokens': 0}
   output_tokens: 1889
   output_tokens_details: {'reasoning_tokens': 0}
   total_tokens: 2768
==================================================
音频已保存: ./20260417_143700.wav
```

<p align="center">
  <small>© 2026 DMXAPI qwen3.5-omni-plus-all 文 + 音频 生 文 + 音频</small>
</p>
