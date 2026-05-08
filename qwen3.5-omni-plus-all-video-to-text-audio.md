# Qwen3.5-Omni-Plus-All 文本+本地视频 生 文本+音频 API 使用文档

基于阿里云通义千问 Qwen3.5-Omni 系列最新一代全模态模型的 Responses 端点调用，支持文本、图片、音频、视频任意组合的多模态输入，可同步输出文本与语音（WAV 格式）。模型原生支持 3 小时音频或 1 小时视频的长序列理解，覆盖 113 种输入语言/方言、36 种输出语言/方言，提供 55 种拟人音色（含 Tina、Cherry、Serena、Ethan、Chelsie 等），适用于长视频分析、会议纪要、字幕生成、内容审核、音视频交互助手等场景。本接入通过 DMXAPI 的 `/v1/responses` 端点，统一以 SSE 流式事件返回文字增量与 Base64 编码的音频数据。

## 🌐 请求地址

```
https://www.dmxapi.cn/v1/responses
```


:::warning
请妥善保管您的 API Key！严禁将密钥泄露给他人、硬编码到代码中或提交到公开的代码仓库。如果怀疑密钥已泄露，请立即前往 DMXAPI 官网重新生成。
:::

## 🧠 模型名称

- `qwen3.5-omni-plus-all`

## 📹 文本+本地视频生成文本+音频 示例代码

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

# 本地视频路径，可直接填入绝对路径或相对路径
video_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "homelander.mp4")

# ═══════════════════════════════════════════════════════════════
# 步骤2: 配置请求头
# ═══════════════════════════════════════════════════════════════

headers = {
    "Content-Type": "application/json",
    "Authorization": f"{api_key}",
}

# ═══════════════════════════════════════════════════════════════
# 步骤3: 本地视频 Base64 编码
# ═══════════════════════════════════════════════════════════════


def encode_video(path):
    with open(path, "rb") as video_file:
        return base64.b64encode(video_file.read()).decode("utf-8")


base64_video = encode_video(video_path)

# ═══════════════════════════════════════════════════════════════
# 步骤4: 配置请求参数
# ═══════════════════════════════════════════════════════════════

payload = {
    # 【model】(string, 必填) 指定调用的模型名称
    # 本文档固定为 qwen3.5-omni-plus-all（Qwen3.5-Omni 系列最新一代全模态模型）
    # 适用于长视频分析、会议纪要、字幕生成、内容审核、音视频交互等场景
    "model": "qwen3.5-omni-plus-all",

    # 【input】(array, 必填) 多模态输入内容数组，Responses 端点专用字段（对应 Chat Completions 的 messages）
    # 每个元素是一条消息对象，包含 role 与 content
    # role 取值: "user"(用户消息) / "system"(系统消息，输出含音频时不支持) / "assistant"(助手消息)
    # content 为数组，可混合多种 type：
    #   - "text"      纯文本
    #   - "video_url" 视频(URL 或 data:;base64,... Data URL)
    #   - "image_url" 图像(URL 或 data:image/png;base64,... Data URL)
    #   - "input_audio" 音频
    # Qwen3.5-Omni 系列支持文本与图片、音频、视频的任意组合同时输入，不限于单一模态
    "input": [
        {
            "role": "user",
            "content": [
                {
                    # 【type=video_url】(string) 声明当前内容项为视频输入
                    "type": "video_url",
                    # 【video_url】(object) 视频的访问地址
                    # url 可以是公网可访问的视频 URL，也可以是本地视频的 Base64 Data URL
                    # 本地视频需先通过 base64 编码，再以 "data:;base64,<编码>" 传入
                    # 支持的视频文件格式: MP4、AVI、MKV、MOV、FLV、WMV 等
                    # Qwen3.5-Omni 系列输入限制: 最长 1 小时视频；视频文件中视觉与音频信息分开计费
                    "video_url": {"url": f"data:;base64,{base64_video}"},
                },
                {
                    # 【type=text】(string) 声明当前内容项为纯文本
                    "type": "text",
                    # 【text】(string) 与视频一同发送给模型的文本指令/提问
                    "text": "视频中呈现了什么内容？",
                },
            ],
        }
    ],

    # 【stream】(boolean, 必填) 是否使用流式输出
    # Qwen-Omni 模型在 modalities 含 "audio" 时必须设置为 True，否则会报错
    # 流式下服务器通过 SSE 协议逐步推送文字增量和音频分片
    "stream": True,

    # 【stream_options】(object, 可选) 流式输出附加配置
    # include_usage: True 表示在最后一条事件中返回 token 用量统计（input_tokens / output_tokens / total_tokens 等）
    "stream_options": {"include_usage": True},

    # 【modalities】(array, 可选) 指定模型输出的数据模态
    # 可选值:
    #   ["text"]           仅输出文本（思考模式下必须使用此值）
    #   ["text", "audio"]  同时输出文本和音频（默认推荐，需配合 audio 字段）
    # 当包含 "audio" 时，stream 必须为 True，且当前系列不支持在包含音频输出时设置 System Message
    "modalities": ["text", "audio"],

    # 【audio】(object, 可选) 当 modalities 包含 "audio" 时生效，控制音频输出参数
    "audio": {
        # 【voice】(string, 必填) 音色名称
        # Qwen3.5-Omni 系列提供 55 种拟人音色，常用示例:
        #   "Tina"(女声，温柔亲切) / "Cherry"(女声，甜美青春) / "Serena"(女声，知性优雅)
        #   "Ethan"(男声，沉稳) / "Chelsie"(女声，活泼) / "Dylan"(男声，磁性)
        # 完整音色列表请查阅阿里云百炼「Qwen-Omni 音色列表」页面
        "voice": "Tina",

        # 【format】(string, 必填) 音频输出格式
        # 目前主要支持 "wav"(采样率 24000Hz，int16 PCM 封装)
        "format": "wav",
    },
}

# ═══════════════════════════════════════════════════════════════
# 步骤5: 发送请求并提取文字与音频
# ═══════════════════════════════════════════════════════════════

text_parts = []
audio_parts = []
usage_info = None
current_event = None
chunks = []

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
            chunks.append({"event": current_event, "data": "[DONE]"})
            break

        try:
            data = json.loads(data_str)
        except json.JSONDecodeError:
            chunks.append({"event": current_event, "data": data_str, "error": "JSONDecodeError"})
            continue

        chunks.append({"event": current_event, "data": data})

        if current_event == "response.output_text.delta":
            text = data.get("delta", "")
            if text:
                text_parts.append(text)

        elif current_event == "response.output_item.done":
            for part in data.get("item", {}).get("content", []):
                if "audio" in part and part["audio"].get("data"):
                    audio_parts.append(part["audio"]["data"])

        elif current_event == "response.completed":
            usage_info = data.get("response", {}).get("usage")

output_json_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "b_1_output.json")
with open(output_json_path, "w", encoding="utf-8") as f:
    json.dump(chunks, f, ensure_ascii=False, indent=2)
print(f"已保存 {len(chunks)} 条 SSE 数据到: {output_json_path}")

# ═══════════════════════════════════════════════════════════════
# 步骤6: 输出文字内容
# ═══════════════════════════════════════════════════════════════

full_text = "".join(text_parts)
print("=" * 50)
print("生成的文字内容:")
print("=" * 50)
print(full_text if full_text else "(无文字输出)")
print("=" * 50)

# ═══════════════════════════════════════════════════════════════
# 步骤6.5: 输出 usage 信息
# ═══════════════════════════════════════════════════════════════

if usage_info:
    print("Token 用量:")
    for key, value in usage_info.items():
        print(f"   {key}: {value}")
    print("=" * 50)

# ═══════════════════════════════════════════════════════════════
# 步骤7: 保存音频为 WAV
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

## 📨 返回示例

```text
==================================================
生成的文字内容:
==================================================
本视频片段全长约9.5秒，画面中呈现了一名白人男性演员（角色为"祖国人"，Homelander），身着深蓝色带有红色条纹的超级英雄战衣，肩部配有金色护甲，内穿橙黄色高领服装。整个场景背景为纯绿色幕布，无其他环境元素，凸显出人物主体。

镜头采用静态中近景构图，焦点始终锁定在演员上半身和面部表情上。灯光均匀、明亮且柔和，无明显阴影或色彩变化，确保演员五官及服饰细节清晰可见。

剧情动作方面，视频开头（00:00）演员头部略微偏向右侧，眼睛睁大，嘴巴微张，表现出惊讶或警觉的情绪。随后（00:01-00:02），他迅速将头转向左侧，目光紧锁某处，表情紧张专注。紧接着（00:03-00:04），他又将头转回正前方，眉头微皱，嘴唇紧闭，显露出困惑与警惕。之后（00:05-00:06），眼神继续游移，仿佛在观察周围情况。最后（00:07-00:08），演员嘴角微微上扬，露出一丝自信甚至略带轻蔑的笑容，眼神依旧保持警觉。

音频方面，全程伴有激昂的小提琴独奏音乐，节奏急促，营造出紧张氛围。伴随音乐的是多次出现的金属撞击声、物体摩擦声以及短促的喘息声，暗示场景中可能存在激烈动作或冲突，但这些声音并未在视觉上体现出来。

整体来看，该片段通过演员丰富的面部表情和紧凑的动作切换，配合充满张力的音效，成功塑造了一个高度警觉、情绪复杂的超级英雄形象。虽然缺乏具体情节线索，但通过视觉与听觉的结合，观众能感受到角色所处的高压环境和内心波动。
==================================================
Token 用量:
   input_tokens: 4616
   input_tokens_details: {'cached_tokens': 0}
   output_tokens: 9014
   output_tokens_details: {'reasoning_tokens': 0}
   total_tokens: 13630
==================================================
音频已保存: c:\Users\15664\Desktop\qwen多模态\qwen3.5-omni-plus\视频本地文件\20260416_235218.wav
```

<p align="center">
  <small>© 2026 DMXAPI qwen3.5-omni-plus-all 文本+本地视频 → 文本+音频</small>
</p>
