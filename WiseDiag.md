# WiseDiag 医疗大模型 API 文档
WiseDiag 是由智诊科技开发的医疗领域大语言模型，针对医疗推理任务做过专门调优，支持深度思考（Reasoning Content）、流式输出和多轮对话。接口完全兼容 OpenAI SDK（v1.0+），上下文窗口为 128k tokens（输入 + 输出共享）。

::: tip 重要提示
本模型已针对医疗推理任务做过专门调优，请**仅传入文档列出的参数**，其余采样字段沿用服务端默认即可。自行调整惩罚类、重复度类等高级采样参数会导致输出质量显著下降（典型表现：JSON 结构崩坏、内容重复、语义割裂）。
:::

## 🔗 请求地址

```
https://www.dmxapi.cn/v1/chat/completions
```

## 🤖 模型名称

```
wisediag-large-latest
```

## 💻 示例代码

::: code-group

```python [Python 流式]
from openai import OpenAI

# ═══════════════════════════════════════════════════════════════
# 🔑 步骤1: 配置 API 连接信息
# ═══════════════════════════════════════════════════════════════

# 🔐 配置客户端
client = OpenAI(
    api_key="sk-****************************************",  # 替换为你的 DMXAPI 密钥
    base_url="https://www.dmxapi.cn/v1",                    # DMXAPI 接口地址
)

# ═══════════════════════════════════════════════════════════════
# 💬 步骤2: 定义对话函数（流式输出）
# ═══════════════════════════════════════════════════════════════

def chat_with_wisediag(prompt):
    # 【messages】对话上下文列表，包含 role（user/system/assistant）和 content
    # 接口本身不维护对话状态，多轮对话需由调用方自行累积历史消息
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "prompt"}
    ]

    try:
        response = client.chat.completions.create(
            # 【model】（必填）固定值为 wisediag-large-latest
            model="wisediag-large-latest",
            # 【messages】（必填）对话上下文列表
            messages=messages,
            # 【max_tokens】生成内容的最大 Token 数
            # 推荐设置为 8192，可满足绝大多数业务场景
            # 模型上下文窗口为 128k，输入 + 输出共享该上限
            max_tokens=8192,
            # 【temperature】采样温度，控制输出的随机性，默认 0.6
            # 建议保持默认，自行调整可能导致输出质量下降
            temperature=0.6,
            # 【top_p】核采样概率，默认 0.95，建议保持默认
            top_p=0.95,
            # 【stream】是否开启流式传输，默认 false
            # 推荐设置为 true 以获得更好的实时响应体验
            stream=True,
            # 【extra_body】扩展控制参数
            # 如需关闭深度思考，使用：extra_body={"enable_thinking": False}
        )

        # ═══════════════════════════════════════════════════════════════
        # 📤 步骤3: 处理流式响应
        # ═══════════════════════════════════════════════════════════════

        print("--- 正在生成回答 ---")
        full_reasoning = ""
        full_content = ""

        for chunk in response:
            # 处理 Usage 信息（通常在最后一个 chunk）
            if hasattr(chunk, "usage") and chunk.usage:
                print(f"\n[Token Usage] Prompt: {chunk.usage.prompt_tokens}, Completion: {chunk.usage.completion_tokens}")
                break

            delta = chunk.choices[0].delta

            # 获取推理过程 (Reasoning Content)
            reasoning_piece = getattr(delta, "reasoning_content", None)
            if reasoning_piece:
                print(reasoning_piece, end="", flush=True)
                full_reasoning += reasoning_piece

            # 获取最终回复内容 (Content)
            content_piece = getattr(delta, "content", None)
            if content_piece:
                print(content_piece, end="", flush=True)
                full_content += content_piece

        return full_content

    except Exception as e:
        print(f"请求发生错误: {e}")
        return None

# ═══════════════════════════════════════════════════════════════
# 🚀 步骤4: 执行对话
# ═══════════════════════════════════════════════════════════════

if __name__ == "__main__":
    chat_with_wisediag("你好，请介绍一下你自己。")
```

```python [Python 非流式]
from openai import OpenAI
import json

# ═══════════════════════════════════════════════════════════════
# 🔑 步骤1: 配置 API 连接信息
# ═══════════════════════════════════════════════════════════════

# 🔐 配置客户端
client = OpenAI(
    api_key="sk-****************************************",  # 替换为你的 DMXAPI 密钥
    base_url="https://www.dmxapi.cn/v1",                    # DMXAPI 接口地址
)

# ═══════════════════════════════════════════════════════════════
# 💬 步骤2: 发送非流式请求
# ═══════════════════════════════════════════════════════════════

response = client.chat.completions.create(
    # 【model】（必填）固定值为 wisediag-large-latest
    model="wisediag-large-latest",
    # 【messages】（必填）对话上下文列表，包含 role（user/system/assistant）和 content
    # 接口不维护对话状态，多轮对话需调用方自行累积历史消息
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "帮我解释一下什么是血常规检查？"}
    ],
    # 【max_tokens】生成内容的最大 Token 数，默认 81920，推荐 8192
    # 模型上下文窗口 128k tokens，输入 + 输出共享
    max_tokens=8192,
    # 【temperature】采样温度，默认 0.6，建议保持默认
    temperature=0.6,
    # 【top_p】核采样概率，默认 0.95，建议保持默认
    top_p=0.95,
    # 【stream】是否开启流式传输，默认 false
    stream=False,
    # 【extra_body】扩展参数，可关闭深度思考：extra_body={"enable_thinking": False}
)

# ═══════════════════════════════════════════════════════════════
# 📤 步骤3: 输出结果
# ═══════════════════════════════════════════════════════════════

print("回复内容：")
print(response.choices[0].message.content)

print(f"\n[Token Usage] Prompt: {response.usage.prompt_tokens}, Completion: {response.usage.completion_tokens}")
```


```bash [cURL]
curl --location 'https://www.dmxapi.cn/v1/chat/completions' \
--header 'Content-Type: application/json' \
--header 'Authorization: Bearer sk-****************************************' \
--data '{
    "model": "wisediag-large-latest",
    "messages": [
        {"role": "user", "content": "你好"}
    ],
    "max_tokens": 8192,
    "temperature": 0.6,
    "top_p": 0.95,
    "stream": true
}'
```

:::


## 📊 返回示例

::: code-group

```text [流式返回（SSE）]
data: {"id":"chatcmpl-xxx","choices":[{"delta":{"reasoning_content":"让我分析一下这个问题..."},"index":0}]}

data: {"id":"chatcmpl-xxx","choices":[{"delta":{"content":"血常规检查是..."},"index":0}]}

data: {"id":"chatcmpl-xxx","choices":[],"usage":{"prompt_tokens":25,"completion_tokens":512}}

data: [DONE]
```

```json [非流式返回]
{
  "id": "chatcmpl-xxxxxxxx",
  "object": "chat.completion",
  "created": 1700000000,
  "model": "wisediag-large-latest",
  "choices": [
    {
      "index": 0,
      "message": {
        "role": "assistant",
        "content": "血常规检查是临床上最基础、最常见的血液检验项目之一，通过采集少量外周血（通常为静脉血或末梢血），利用自动化血液分析仪对血液中的细胞成分进行计数和分类分析......"
      },
      "finish_reason": "stop"
    }
  ],
  "usage": {
    "prompt_tokens": 25,
    "completion_tokens": 512,
    "total_tokens": 537
  }
}
```

:::




## 🔄 多轮对话

本接口为**无状态接口**，服务端不会保存任何对话历史。每次请求都是独立的，如需实现多轮对话，调用方需要自行在客户端维护 `messages` 数组，将历史对话按顺序传入。

### 实现方式

每轮对话后，将模型返回的 `assistant` 回复追加到 `messages` 列表中，再将用户的新问题追加为新的 `user` 消息，一并发送给接口。

```python
from openai import OpenAI

client = OpenAI(
    api_key="sk-****************************************",  # 替换为你的 DMXAPI 密钥
    base_url="https://www.dmxapi.cn/v1",
)

conversation_history = [
    {"role": "system", "content": "You are a helpful assistant."}
]

def chat(user_input):
    conversation_history.append({"role": "user", "content": user_input})

    response = client.chat.completions.create(
        model="wisediag-large-latest",
        messages=conversation_history,
        stream=False,
    )

    assistant_reply = response.choices[0].message.content
    conversation_history.append({"role": "assistant", "content": assistant_reply})
    return assistant_reply

# 第一轮
print(chat("帮我解释一下什么是血常规检查？"))
# 第二轮（模型能理解"它"指的是上文的"血常规检查"）
print(chat("它一般包含哪些指标？"))
```

::: warning 注意事项
- **Token 累积**：每轮对话的 `messages` 会包含全部历史，Token 消耗会随轮次增长。建议在历史过长时做截断或摘要，控制在上下文窗口内。
- **上下文窗口**：模型的上下文窗口为 128k tokens，当历史消息总 Token 数超出限制时，请裁剪早期消息。
:::


## 🧠 深度思考控制

模型默认开启深度思考。在生成最终回答前，模型可能会先输出一段推理过程（通过 `reasoning_content` 字段返回）。

- **输出顺序**：流式模式下，`reasoning_content` 会在 `content` 之前输出。当推理完成后，才会开始返回最终回答内容。
- **额外耗时**：深度思考阶段会增加首个 `content` Token 的等待时间（通常数秒到十余秒），这属于正常行为，并非接口性能问题。
- **可能为空**：部分简单问题可能不触发深度思考，此时 `reasoning_content` 不会出现在响应中。

### 关闭深度思考

对于**严格结构化输出**（如要求返回固定 JSON 格式）或**追求低延迟**的场景，可主动关闭深度思考：

::: code-group

```python [Python]
response = client.chat.completions.create(
    model="wisediag-large-latest",
    messages=messages,
    stream=True,
    extra_body={"enable_thinking": False},  # 关闭深度思考
)
```

```bash [cURL]
curl --location 'https://www.dmxapi.cn/v1/chat/completions' \
--header 'Content-Type: application/json' \
--header 'Authorization: Bearer sk-****************************************' \
--data '{
    "model": "wisediag-large-latest",
    "messages": [{"role": "user", "content": "你好"}],
    "stream": true,
    "enable_thinking": false
}'
```

:::

关闭后，响应中将**不会**出现 `reasoning_content` 字段，模型会直接输出 `content`，首 Token 延迟显著降低。



<p align="center">
  <small>© 2025 DMXAPI WiseDiag 医疗大模型</small>
</p>
