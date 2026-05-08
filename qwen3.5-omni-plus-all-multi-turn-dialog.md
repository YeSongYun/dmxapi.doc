# Qwen3.5-Omni-Plus-All 多轮对话 API 使用文档

基于阿里云通义千问 Qwen3.5-Omni 全模态大模型的多轮对话接口，能够接收文本、音频、图像、视频等多种模态输入并生成文本或语音形式的回复。支持 113 种输入音频语种（含 74 种语言、39 种方言）、36 种输出音频语种，提供 55 种拟人音色，原生支持音视频理解与多轮上下文对话，可应用于内容审核、文本创作、视觉识别、音视频交互助手等场景。在多轮对话中，用户可在不同 User Message 中输入不同模态的数据，Assistant Message 仅保留文本内容用于上下文记忆。

## 🌐 请求地址

```
https://www.dmxapi.cn/v1/responses
```

:::warning
请妥善保管您的 API Key！严禁将密钥泄露给他人、硬编码到代码中或提交到公开的代码仓库。如果怀疑密钥已泄露，请立即前往 DMXAPI 官网重新生成。
:::

## 🤖 模型名称

- `qwen3.5-omni-plus-all`

## 💬 多轮对话示例代码

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
    # 本文档对应模型：qwen3.5-omni-plus-all（Qwen3.5-Omni 全模态系列，支持文本/音频/图片/视频输入，文本/音频输出）
    "model": "qwen3.5-omni-plus-all",

    # 【input】(array, 必填) 多轮对话消息列表
    # 每个元素代表一条消息，需依次按对话顺序排列（user -> assistant -> user ...）
    # 重要约束：
    #   - Assistant Message 只能包含文本数据（type=text）
    #   - User Message 支持文本和一种其他模态的组合（如文本+音频、文本+图片、文本+视频）
    #   - 在不同轮次的 User Message 中可切换不同模态输入
    "input": [
        {
            # 【role】(string, 必填) 角色类型
            # 可选值: "user"(用户) / "assistant"(助手) / "system"(系统)
            "role": "user",
            # 【content】(array 或 string, 必填) 消息内容
            # 多模态场景下为数组，每个元素指定一种模态的数据块
            "content": [
                {
                    # 【type】(string, 必填) 内容块类型
                    # 可选值: "text"(文本) / "input_audio"(音频) / "image_url"(图片) / "video_url"(视频)
                    "type": "input_audio",
                    # 【input_audio】(object, 当 type=input_audio 时必填) 音频数据对象
                    "input_audio": {
                        # 【data】(string, 必填) 音频数据，支持两种形式：
                        #   1. 公网可访问的音频 URL（如 mp3/wav/m4a 等格式）
                        #   2. Base64 编码后的音频字符串（编码后大小必须小于 10MB）
                        "data": "https://dashscope.oss-cn-beijing.aliyuncs.com/audios/welcome.mp3"
                    }
                },
                {
                    # 【type】(string, 必填) 文本内容块
                    "type": "text",
                    # 【text】(string, 必填) 文本内容
                    "text": "这段音频在说什么"
                }
            ]
        },
        {
            # 历史 Assistant 回复（仅保留文本用于上下文记忆）
            "role": "assistant",
            "content": [
                {
                    "type": "text",
                    "text": "这段音频在说：欢迎使用阿里云"
                }
            ]
        },
        {
            # 当前轮用户提问
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": "介绍一下这家公司？"
                }
            ]
        }
    ],

    # 【stream】(boolean, 必填) 是否启用流式输出
    # 重要：Qwen-Omni 系列模型所有请求必须设置为 True，否则会报错
    "stream": True,

    # 【stream_options】(object, 可选) 流式输出配置
    "stream_options": {
        # 【include_usage】(boolean, 可选) 是否在最后一个 chunk 中返回 token 用量统计信息
        # 默认值: false
        "include_usage": True
    },

    # 【modalities】(array, 必填) 输出数据模态
    # 可选值: ["text","audio"](文本+音频) / ["text"](仅文本)
    # 注意：思考模式下不支持输出音频，仅可使用 ["text"]
    "modalities": ["text", "audio"],

    # 【audio】(object, 当 modalities 包含 audio 时必填) 音频输出配置
    "audio": {
        # 【voice】(string, 必填) 输出音色
        # Qwen3.5-Omni 提供 55 种拟人音色，示例：Tina、Cherry、Serena、Ethan、Chelsie 等
        # 完整音色列表详见官方文档「音色列表」
        "voice": "Tina",
        # 【format】(string, 必填) 音频输出格式
        # 常用值: "wav"(无损，推荐) / "mp3"(有损压缩) 等
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

## 📬 返回示例

```
==================================================
生成的文字内容:
==================================================
**阿里云（Alibaba Cloud）** 是阿里巴巴集团旗下的云计算及人工智能科技公司，成立于 2009 年。它是全球领先的云计算服务提供商之一，也是亚太市场份额最大的云厂商。

以下是关于阿里云的核心介绍：

### 1. 市场地位
*   **全球排名**：根据 Gartner 等权威机构的数据，阿里云长期位居**全球前三**、**亚太第一**。
*   **中国第一**：在中国公有云市场，阿里云占据主导地位，拥有最大的客户群和最丰富的产品线。

### 2. 核心业务与服务
阿里云提供极其广泛的"云原生"服务，主要涵盖以下几大类：
*   **基础计算与存储**：包括弹性计算（ECS）、对象存储（OSS）、数据库（如 PolarDB、RDS）等，为企业提供最底层的 IT 基础设施。
*   **大数据与人工智能**：提供强大的数据处理平台（MaxCompute）和 AI 模型服务。其自研的超大规模语言模型系列被称为**通义千问（Qwen）**，在自然语言处理、代码生成等领域表现优异。
*   **安全能力**：拥有全球领先的安全防护体系，特别是在抵御 DDoS 攻击方面经验丰富（源于支撑淘宝、天猫等大促活动的实战积累）。
*   **行业解决方案**：为金融、政务、零售、制造、交通等行业提供定制化的数字化转型方案。

### 3. 技术亮点
*   **飞天操作系统（Apsara）**：这是阿里云自主研发的超大规模通用计算操作系统，能够将遍布全球的百万级服务器连成一台超级计算机，支持海量数据的实时处理。
*   **自研芯片**：推出了倚天（CPU）、含光（AI 推理芯片）等自研芯片，以提升性能和降低成本。
*   **双 11 实战验证**：每年"双 11"购物节期间，阿里云需要支撑每秒数十万次的交易峰值，这种极端场景下的稳定性验证了其技术的可靠性。

### 4. 全球布局
阿里云在全球拥有多个地域（Region）和可用区（Zone），数据中心遍布亚洲、欧洲、北美、中东等地，能够为全球企业提供低延迟、合规的本地化云服务。

### 5. 愿景与使命
阿里云的使命是"**为了无法计算的价值**"，致力于让计算成为普惠科技，降低企业使用技术的门槛，推动各行各业的数字化和智能化转型。

简单来说，如果你需要搭建网站、运行 APP、分析海量数据或开发人工智能应用，阿里云就是提供这些底层能力和工具的核心平台。
==================================================
Token 用量:
   input_tokens: 105
   input_tokens_details: {'cached_tokens': 0}
   output_tokens: 8551
   output_tokens_details: {'reasoning_tokens': 0}
   total_tokens: 8656
==================================================
音频已保存: ./20260417_000000.wav
```

<p align="center">
  <small>© 2026 DMXAPI Qwen3.5-Omni-Plus-All 多轮对话</small>
</p>
