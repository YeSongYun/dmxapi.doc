# Qwen3.5-Omni-Plus-All 文+图 生 文+音频 API 使用文档

基于阿里通义千问 Qwen3.5-Omni 全模态大模型的多模态对话接口，通过 DMXAPI `/v1/responses` 端点提供服务。支持文本与图片任意组合作为输入，流式同时返回文字回复与拟人化语音合成（WAV 音频 Base64 编码）。覆盖 55 种拟人音色、36 种输出语音语种（含 29 种语言、7 种方言），113 种输入音频语种，可应用于内容审核、文本创作、视觉识别、音视频交互助手等场景。

## 🌐 请求地址

```
https://www.dmxapi.cn/v1/responses
```

:::warning
请妥善保管您的 API Key！严禁将密钥泄露给他人、硬编码到代码中或提交到公开的代码仓库。如果怀疑密钥已泄露，请立即前往 DMXAPI 官网重新生成。
:::

## 🤖 模型名称

- `qwen3.5-omni-plus-all`

## 📝 文 + 图 生 文 + 音频 示例代码

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
    # 【model】(string, 必填) 指定要调用的模型名称
    # 本文档仅对应 qwen3.5-omni-plus-all，属于 Qwen3.5-Omni 全模态系列
    # 支持文本、图片、音频、视频的任意组合输入，支持长达 1 小时视频/3 小时音频
    "model": "qwen3.5-omni-plus-all",

    # 【input】(array, 必填) 对话消息数组
    # 每个元素为一条消息，包含 role 和 content
    # 用户消息 content 支持多模态数组（文本/图片/音频/视频的任意组合）
    "input": [
        {
            # 【role】(string, 必填) 消息角色
            # 可选值: "user"(用户) / "assistant"(助手) / "system"(系统)
            # 注意: Qwen-Omni 音频输出模式下不支持 system message
            "role": "user",
            # 【content】(array) 多模态内容数组，每个元素为一个输入片段
            "content": [
                {
                    # 【type】(string, 必填) 当前内容片段的类型
                    # 可选值: "text"(文本) / "image_url"(图片) / "input_audio"(音频) / "video_url"(视频)
                    "type": "image_url",
                    # 【image_url】(object) 图片输入对象
                    # 支持 公网URL 或 data URI base64 编码（base64 编码后需 < 10MB）
                    "image_url": {
                        # 【url】(string, 必填) 图片地址
                        # 支持 http(s) 公网链接或 data:image/png;base64,... 形式
                        "url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241022/emyrja/dog_and_girl.jpeg"
                    }
                },
                {
                    # 【type】(string, 必填) 指定为文本类型
                    "type": "text",
                    # 【text】(string, 必填) 文本内容，用户提问或指令
                    "text": "图中描绘的是什么景象？"
                }
            ]
        }
    ],

    # 【stream】(boolean, 必填) 是否使用流式输出
    # Qwen-Omni 模型必须设置为 True，否则会报错
    # 通过 SSE 协议逐步返回文字增量与音频片段
    "stream": True,

    # 【stream_options】(object, 可选) 流式输出的附加选项
    "stream_options": {
        # 【include_usage】(boolean) 是否在流式结束时返回 usage 统计信息
        # True 时最终事件会包含 input_tokens / output_tokens / total_tokens
        "include_usage": True
    },

    # 【modalities】(array, 可选) 指定输出模态
    # 可选值: ["text", "audio"](同时输出文字和音频) / ["text"](仅文字)
    # 默认为 ["text"]；若要生成语音必须显式加入 "audio"
    "modalities": ["text", "audio"],

    # 【audio】(object, 可选) 音频输出参数
    # 当 modalities 包含 "audio" 时必须提供
    "audio": {
        # 【voice】(string, 必填) 音色名称
        # Qwen3.5-Omni 系列支持 55 种音色，示例: "Tina"
        # 完整列表参见官方音色列表文档
        "voice": "Tina",
        # 【format】(string, 必填) 音频输出格式
        # 当前支持: "wav"，返回 PCM 16bit / 采样率 24000Hz 的 Base64 编码字符串
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

        # 文字增量事件
        if current_event == "response.output_text.delta":
            text = data.get("delta", "")
            if text:
                text_parts.append(text)

        # 音频数据事件（完整 WAV，base64 编码）
        elif current_event == "response.output_item.done":
            for part in data.get("item", {}).get("content", []):
                if "audio" in part and part["audio"].get("data"):
                    audio_parts.append(part["audio"]["data"])

        # usage 统计事件
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

## 📦 返回示例

```
==================================================
生成的文字内容:
==================================================
图中描绘的是一幅温馨、宁静的海滩日落景象：

- **主体人物与动物**：一位年轻女性坐在沙滩上，面带微笑，正与一只金毛寻回犬互动。狗狗坐着，抬起前爪，似乎在与主人"击掌"或握手，展现出亲密和训练有素的关系。

- **环境背景**：他们身处一片开阔的沙滩上，身后是平静的海洋，海浪轻轻拍打着岸边。天空被夕阳染成柔和的暖色调（橙黄与淡粉），阳光从右侧洒下，在人物和狗的轮廓上形成美丽的逆光效果，营造出温暖、浪漫的氛围。

- **细节元素**：
  - 女性穿着格子衬衫和深色裤子，赤脚坐在沙地上，显得放松自然。
  - 狗狗佩戴着彩色图案的胸背带，旁边还放着一条红色牵引绳。
  - 沙滩上有清晰的脚印和凹陷，增加了画面的真实感和生活气息。

整体画面传达出人宠之间深厚的情感纽带，以及在大自然中享受宁静时光的美好意境，充满治愈感和幸福感。
==================================================
Token 用量:
   input_tokens: 1266
   input_tokens_details: {'cached_tokens': 0}
   output_tokens: 5506
   output_tokens_details: {'reasoning_tokens': 0}
   total_tokens: 6772
==================================================
音频已保存: /path/to/output/20260417_153000.wav
```

<p align="center">
  <small>© 2026 DMXAPI qwen3.5-omni-plus-all 文 + 图 生 文 + 音频</small>
</p>
