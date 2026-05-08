# qwen3.5-omni-plus-all 文 生 文+音频 API 使用文档

qwen3.5-omni-plus-all 是阿里巴巴通义千问团队推出的全模态大模型，支持同时输出文本与音频双模态结果。模型内建 55 种可选音色（示例使用 Tina），支持 WAV 音频格式，流式输出配合 `include_usage` 可在末尾返回完整的 Token 用量统计，适用于智能问答、语音助手、有声内容生成等需要文本 + 语音联合输出的场景。

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
    # 【model】(string, 必填) 指定调用的模型名称
    # 本文档使用的模型: qwen3.5-omni-plus-all（全模态模型，支持文本+音频输出）
    "model": "qwen3.5-omni-plus-all",

    # 【input】(array, 必填) 对话输入消息数组，按顺序传递多轮对话上下文
    # 每个元素为一个消息对象，包含 role 和 content 字段
    "input": [
        {
            # 【role】(string, 必填) 消息角色
            # 可选值: "user"(用户) / "assistant"(助手) / "system"(系统提示)
            "role": "user",

            # 【content】(string 或 array, 必填) 消息正文内容
            # 单一字符串形式: 纯文本输入
            # 数组形式: 支持多模态混合(文本/图像/音频/视频)
            "content": "你是谁？"
        }
    ],

    # 【stream】(boolean, 必填) 是否启用流式输出
    # Qwen-Omni 系列强制要求 stream=true，非流式调用不被支持
    # 可选值: true(流式，唯一合法值)
    "stream": True,

    # 【stream_options】(object, 可选) 流式输出的附加配置项
    "stream_options": {
        # 【include_usage】(boolean, 可选) 是否在流式结束时返回 Token 用量统计
        # 设为 true 时，响应的最后一条事件包含 input_tokens / output_tokens / total_tokens 等字段
        # 默认值: false
        "include_usage": True
    },

    # 【modalities】(array, 必填) 指定模型的输出模态
    # 可选值: ["text"](仅文本) / ["text","audio"](文本+音频)
    # 注意: 思考模式(enable_thinking=true)下不支持音频输出，此字段只能为 ["text"]
    "modalities": ["text", "audio"],

    # 【audio】(object, 可选) 音频输出配置，仅在 modalities 含 "audio" 时生效
    "audio": {
        # 【voice】(string, 必填) 输出音色选择
        # qwen3.5-omni-plus 系列支持 55 种音色，示例使用 "Tina"
        # 完整音色列表需前往百炼控制台查询
        "voice": "Tina",

        # 【format】(string, 必填) 音频输出格式
        # 示例使用 "wav"(波形音频，无损格式)
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

```
==================================================
生成的文字内容:
==================================================
我是 Qwen3.5，是阿里巴巴集团最新推出的通义千问大语言模型。我具备强大的语言理解与生成能力，支持全球超过 100 种语言的流畅交互，并拥有 256K 的超长上下文窗口，能够精准处理长文档、复杂对话及多步骤任务。

我的核心优势包括：
- **深度推理升级**：在数学、逻辑及科学领域具备更强的分步推导能力
- **全栈代码赋能**：支持代码生成、调试、优化及将创意直接转化为可运行前端页面
- **智能体自主规划**：可独立制定多步骤计划，调用工具或 API 完成跨平台任务
- **多模态深度解析**：能分析图表/公式/科学图示中的因果关系，提供专业级解读
- **垂直领域精调**：在医疗、法律等场景经过专项优化，提供高准确率的专业建议

无论是需要创作万字小说、分析百页财报，还是开发完整应用程序，我都能以人类专家水准协助您高效达成目标。现在有什么具体任务需要我帮您完成吗？
==================================================
Token 用量:
   input_tokens: 14
   input_tokens_details: {'cached_tokens': 0}
   output_tokens: 5303
   output_tokens_details: {'reasoning_tokens': 0}
   total_tokens: 5317
==================================================
音频已保存: ./20260417_234443.wav
```

<p align="center">
  <small>© 2026 DMXAPI qwen3.5-omni-plus-all 文生文 + 音频</small>
</p>
