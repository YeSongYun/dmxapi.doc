# Qwen3.5-Omni-Plus-All 文本+本地图片 生 文本+音频 API 使用文档

基于阿里云最新一代全模态大模型 qwen3.5-omni-plus-all 的 Responses 端点多模态接口，支持在同一请求中同时传入文本与本地图片（Base64 编码），并以流式方式返回文本与音频（WAV）回复。该模型具备 74 种语言与 39 种方言的理解能力、29 种语言与 7 种方言的语音合成能力、覆盖 55 种拟人音色，可广泛应用于视觉识别、内容审核、音视频交互助手、无障碍读图等场景。

## 🌐 请求地址

```
https://www.dmxapi.cn/v1/responses
```


:::warning
请妥善保管您的 API Key！严禁将密钥泄露给他人、硬编码到代码中或提交到公开的代码仓库。如果怀疑密钥已泄露，请立即前往 DMXAPI 官网重新生成。
:::

## 🤖 模型名称

- `qwen3.5-omni-plus-all`

## 🖼️ 文本 + 本地图片 生成 文本 + 音频 示例代码

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

# 本地图片路径，可直接填入绝对路径或相对路径
image_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "dog_and_girl(3).jpeg")

# ═══════════════════════════════════════════════════════════════
# 步骤2: 配置请求头
# ═══════════════════════════════════════════════════════════════

headers = {
    "Content-Type": "application/json",
    "Authorization": f"{api_key}",
}

# ═══════════════════════════════════════════════════════════════
# 步骤3: 本地图片 Base64 编码
# ═══════════════════════════════════════════════════════════════


def encode_image(path):
    with open(path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")


base64_image = encode_image(image_path)

# ═══════════════════════════════════════════════════════════════
# 步骤4: 配置请求参数
# ═══════════════════════════════════════════════════════════════

payload = {
    # 【model】(string, 必填) 调用的模型名称
    # 本文档对应 qwen3.5-omni-plus-all 模型（最新一代全模态大模型，支持文本/图片/音频/视频输入，文本+音频输出）
    "model": "qwen3.5-omni-plus-all",

    # 【input】(array, 必填) 多模态消息内容数组
    # 每个元素为一条消息，包含 role 与 content；content 内可以混合 image_url 和 text 两种 type
    # 说明：单条 User Message 中可以同时包含文本与一种其他模态（图片/音频/视频），
    # qwen3.5-omni 系列还支持文本与多种模态的任意组合同时输入
    "input": [
        {
            # 【role】(string, 必填) 消息角色，取值 "user"/"assistant"/"system"
            # Assistant Message 只能包含文本；图片/音频/视频必须放在 User Message 的 content 中
            "role": "user",
            "content": [
                {
                    # 【type】(string, 必填) 内容块类型
                    # 可选值: "text"(文本) / "image_url"(图片，支持公网 URL 或 Base64 Data URL)
                    #         / "input_audio"(音频) / "video_url"(视频)
                    "type": "image_url",

                    # 【image_url】(object, 必填当 type="image_url") 图片数据对象
                    "image_url": {
                        # 【url】(string, 必填) 图片地址
                        # 支持两种形式:
                        #   1) 公网 URL: "https://example.com/xxx.jpg"
                        #   2) Base64 Data URL: "data:image/png;base64,{BASE64_STRING}"
                        # 使用 Base64 方式时，编码后的字符串大小必须小于 10 MB
                        "url": f"data:image/png;base64,{base64_image}"
                    },
                },
                {
                    # 文本输入块
                    "type": "text",
                    # 【text】(string, 必填当 type="text") 传给模型的提示词/问题
                    "text": "图中描绘的是什么景象？",
                },
            ],
        }
    ],

    # 【stream】(boolean, 必填) 是否以 SSE 流式返回结果
    # 注意: Qwen-Omni 所有请求都必须设置 stream=True，否则会报错
    "stream": True,

    # 【stream_options】(object, 可选) 流式选项
    "stream_options": {
        # 【include_usage】(boolean, 可选) 是否在最终事件中返回 Token 用量统计
        # 默认 False；设为 True 时会在 response.completed 事件中包含 usage 字段
        "include_usage": True
    },

    # 【modalities】(array[string], 可选) 指定模型输出的模态
    # 可选值: ["text", "audio"](文本 + 音频) / ["text"](仅文本)
    # 说明: qwen3-omni-flash 在思考模式下仅支持 ["text"]；本文档模型同时支持两种组合
    "modalities": ["text", "audio"],

    # 【audio】(object, 可选) 音频输出配置，当 modalities 含 "audio" 时生效
    "audio": {
        # 【voice】(string, 必填当输出音频) 拟人音色名称
        # qwen3.5-omni 系列共支持 55 种音色，示例: "Tina"/"Chelsie"/"Serena"/"Ethan"/"Cherry" 等
        # 完整音色列表请查阅阿里云百炼「音色列表」页面
        "voice": "Tina",

        # 【format】(string, 必填当输出音频) 音频编码格式
        # 可选值: "wav"(推荐，24000 Hz 16-bit 单声道 PCM)
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
chunks = []  # 收集所有 SSE 数据，用于保存到 JSON

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

        # 记录本条 SSE（事件 + 数据）
        chunks.append({"event": current_event, "data": data})

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

# 保存所有 SSE chunk 到 JSON 文件
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

## 📦 返回示例

```
==================================================
生成的文字内容:
==================================================
图中描绘的是一个温馨宁静的海滩日落场景：

- **人物与动物**：一位年轻女性坐在沙滩上，面带微笑，正与一只浅黄色的拉布拉多犬互动。狗狗坐着，抬起前爪，似乎在和她"击掌"或握手，展现出亲密和谐的关系。

- **环境与氛围**：
  - 背景是平静的海洋，海浪轻柔地拍打着岸边。
  - 天空被夕阳染成柔和的暖色调（金黄、淡橙），阳光从右侧洒下，在人物和狗的轮廓上形成温暖的逆光效果，营造出浪漫、放松的氛围。
  - 沙滩细腻，上面有脚印和自然的纹理，显示出有人在此活动过。

- **细节**：
  - 女子穿着格子衬衫和深色裤子，赤脚坐在沙地上，显得随意而舒适。
  - 狗狗戴着彩色图案的胸背带，旁边还放着一条红色牵引绳。
  - 整体画面充满人与宠物之间的温情，以及大自然带来的宁静美感。

总结：这是一幅展现人与宠物在海边共度美好时光的摄影作品，捕捉了夕阳下的温柔瞬间，传递出陪伴、快乐与自然之美的主题。
==================================================
Token 用量:
   input_tokens: 1266
   input_tokens_details: {'cached_tokens': 0}
   output_tokens: 7419
   output_tokens_details: {'reasoning_tokens': 0}
   total_tokens: 8685
==================================================
音频已保存: ./20260417_234813.wav
```

<p align="center">
  <small>© 2026 DMXAPI qwen3.5-omni-plus-all 文本 + 本地图片 生成 文本 + 音频</small>
</p>
