# GPT-5.6 Sol prompt_cache_key 自动缓存

`prompt_cache_key` 用于帮助共享相同提示词前缀的请求匹配缓存。本页通过 DMXAPI 兼容的 Responses 接口演示如何在多轮对话中使用它，示例从空白聊天开始，每轮只显示模型回答。

:::warning API 密钥安全
代码中的 API 密钥是占位符，请替换为你自己的 DMXAPI 密钥。不要把真实密钥放进公开文档或分享给他人。
:::

## 🔗 请求地址

```text
https://www.dmxapi.cn/v1/responses
```

## 模型名称

- 本页示例：`gpt-5.6-sol`
- 适用范围：GPT-5.6 模型及后续模型系列均支持 `prompt_cache_key`；替换 `model` 即可用于 `gpt-5.6-terra`、`gpt-5.6-luna` 等同系列模型。

## prompt_cache_key 参数说明

在 GPT-5.6 模型及后续模型系列上，设置 `prompt_cache_key` 参数，并对共享长公共提示词前缀的请求复用同一密钥。该参数可提升相关请求的缓存匹配效率。使用 `prompt_cache_key` 无需特定 API 版本。

多轮对话时，每次请求都会带上之前的聊天记录。这些请求开头重复的内容，就叫作“公共前缀”。给这些请求设置相同的 `prompt_cache_key`，可以帮助它们到达保存了相同前缀缓存的服务节点，提高复用已有缓存的机会。

| 参数 | 类型 | 是否必填 | 本页示例 |
|------|------|---------|---------|
| `prompt_cache_key` | 字符串 | 否 | `"chat-auto-v1"` |

`chat-auto-v1` 是自己起的名字，可以直接照用，也可以换成便于识别的名称。**同一段连续对话中保持不变，不要每轮生成一个新值。** 它不是 API 密钥，也不负责保存聊天记录。

## 为什么要使用它

对话越长，每轮重复发送的内容通常越多。命中缓存后，模型可以复用前面已经完成的计算，减少处理这些重复内容的时间；重复输入也可按缓存价格计费，实际费用以所用服务为准。

因此，对于连续聊天、反复使用同一段长说明或同一篇文档的场景，可以给相关请求使用相同的缓存标识。

**它是帮助缓存匹配的可选参数。** 不传它也可能使用自动缓存；设置它也不保证每次命中，输入前缀仍需匹配，并满足服务端的缓存条件。

## 调用示例

先安装依赖（`requests` 写法只需 `requests`，SDK 写法只需 `openai`）：

```bash
python -m pip install --upgrade requests openai
```

两种写法的重点都是请求参数里的 `prompt_cache_key`，取值为 `chat-auto-v1`。

::: code-group

```python [requests]
import requests

# DMXAPI Responses 接口地址
url = "https://www.dmxapi.cn/v1/responses"

# 替换为你自己的 DMXAPI 密钥
api_key = "sk-******************************************"

headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {api_key}",
}


# ==================== 请求参数 ====================
def ask_model(history):
    payload = {
        # 使用的模型名称
        "model": "gpt-5.6-sol",

        # 本次问题和之前的完整对话
        "input": history,

        # 不保存服务端响应对象；这不会关闭提示词缓存
        # 本示例由 history 保存并传递聊天记录
        "store": False,

        # 请求返回可供后续对话复用的加密推理项
        # 后面随完整输出一起保留即可，无需自行解读
        "include": ["reasoning.encrypted_content"],

        # 缓存标识：帮助共享相同前缀的请求匹配缓存
        # 名称可以自定义；同一对话中保持不变
        "prompt_cache_key": "chat-auto-v1",

        # implicit：自动在最新符合条件的消息末尾设置缓存断点
        "prompt_cache_options": {
            "mode": "implicit"
        },
    }

    response = requests.post(url, headers=headers, json=payload)

    # 非 2xx 状态码直接抛出异常，便于看到错误信息
    response.raise_for_status()
    return response.json()


def extract_text(result):
    """从返回的 output 列表中拼出模型的文本回答"""
    chunks = []
    for item in result.get("output", []):
        if item.get("type") != "message":
            continue
        for part in item.get("content", []):
            if part.get("type") == "output_text":
                chunks.append(part.get("text", ""))
    return "".join(chunks)


# 启动时没有文章，也没有历史对话
history = []

print("自动缓存示例：输入问题后按回车。")
print("输入“清空”重新开始；输入“退出”结束。")

while True:
    question = input("\n你：").strip()

    if question == "退出":
        break

    if question == "清空":
        history = []
        print("已清空当前对话。")
        continue

    if not question:
        continue

    # 把本次问题追加到聊天记录后面
    history.append({
        "role": "user",
        "content": question,
    })

    # 把完整聊天记录发送给模型
    result = ask_model(history)

    # 保留完整输出，下一轮连同之前的问答一起发送
    history.extend(result["output"])

    # 只显示模型回答
    print("\n助手：", extract_text(result))
```

```python [SDK]
from openai import OpenAI

client = OpenAI(
    # 替换为你自己的 DMXAPI 密钥
    api_key="sk-******************************************",

    # DMXAPI 服务地址
    base_url="https://www.dmxapi.cn/v1",

    # 请求失败时不自动重试
    max_retries=0,
)


# ==================== 请求参数 ====================
def ask_model(history):
    return client.responses.create(
        # 使用的模型名称
        model="gpt-5.6-sol",

        # 本次问题和之前的完整对话
        input=history,

        # 不保存服务端响应对象；这不会关闭提示词缓存
        # 本示例由 history 保存并传递聊天记录
        store=False,

        # 请求返回可供后续对话复用的加密推理项
        # 后面随完整输出一起保留即可，无需自行解读
        include=["reasoning.encrypted_content"],

        # 缓存标识：帮助共享相同前缀的请求匹配缓存
        # 名称可以自定义；同一对话中保持不变
        prompt_cache_key="chat-auto-v1",

        # 通过 extra_body 把额外参数传给服务端
        extra_body={
            "prompt_cache_options": {
                # implicit：自动在最新符合条件的消息末尾设置缓存断点
                "mode": "implicit"
            }
        },
    )


# 启动时没有文章，也没有历史对话
history = []

print("自动缓存示例：输入问题后按回车。")
print("输入“清空”重新开始；输入“退出”结束。")

while True:
    question = input("\n你：").strip()

    if question == "退出":
        break

    if question == "清空":
        history = []
        print("已清空当前对话。")
        continue

    if not question:
        continue

    # 把本次问题追加到聊天记录后面
    history.append({
        "role": "user",
        "content": question,
    })

    # 把完整聊天记录发送给模型
    response = ask_model(history)

    # 保留完整输出，下一轮连同之前的问答一起发送
    history.extend(response.output)

    # 只显示模型回答
    print("\n助手：", response.output_text)
```

:::

## 返回示例

程序运行后，可以连续输入问题。下面仅展示交互形式，实际回答由模型生成，不代表已命中缓存：

```text
你：请帮我制定一个学习 Python 的计划。
助手：<模型给出的学习计划>

你：把第一天的安排详细展开。
助手：<模型根据前面的计划继续回答>

你：每天只有一个小时，应该怎样调整？
助手：<模型结合之前的对话调整计划>
```

这些请求都使用 `chat-auto-v1`，并通过 `history` 保留前面的问答，形成可复用的公共前缀。

## 注意事项

- **保持内容稳定**：新问题追加在后面，尽量不要改写前面的聊天记录；相同的缓存标识不能让不同内容自动匹配。
- **两个参数各有用途**：`prompt_cache_key` 帮助匹配缓存，`implicit` 自动选择缓存前缀的结束位置，本示例无需手动标记。
- **短对话可能还不能缓存**：缓存有最小长度等条件，不是发一句“你好”就一定会生效。
- **聊天记录仍要传递**：`history` 保存本次运行中的问答；固定缓存标识不会替代它。输入 `清空` 重新开始，输入 `退出` 结束；重启程序也会从空白开始。
- **上下文限制**：本示例不会自动压缩历史，长时间对话仍需留意上下文限制。“清空”只清除本程序的聊天记录，不会主动删除服务端缓存。

<p align="center">
  <small>© 2026 DMXAPI GPT-5.6 Sol prompt_cache_key 自动缓存</small>
</p>
