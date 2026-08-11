# DeepSeek 模型思考参数功能说明

## 📖 概念介绍

思考功能(enable_thinking)是 DeepSeek 系列模型（如 `deepseek-v4-flash`、`deepseek-v4-pro`）的特性参数，用于控制模型在给出最终答案前是否先输出思考过程（链式推理）。思考过程在响应的 `reasoning_content` 字段返回，与最终回答 `content` 同级。

## ⚙️ 思考参数配置

**思考开关** `enable_thinking`：

| 参数值 | 说明 |
|--------|------|
| `True` | 开启思考过程，先输出思考再回答 |
| `False` | 关闭思考过程，直接给出最终答案（`deepseek-v4-pro` 上不生效，见注意事项 7） |

**各模型默认思考状态**（不传思考参数时的行为）：

| 模型 | 默认状态 | 说明 |
|------|---------|------|
| `deepseek-v4-flash` | 默认不思考 | 不传参数不输出 `reasoning_content`，需思考时显式传 `True` |
| `deepseek-v4-pro` | 默认思考 | 不传参数即输出 `reasoning_content`，需省 token 时显式关闭 |

## 🔌 API 接口

**请求方法**: `POST`

**Base URL**: `https://www.dmxapi.cn/v1/chat/completions`

**支持模型**: DeepSeek 系列思考模型，如 `deepseek-v4-flash`、`deepseek-v4-pro`（均支持思考 / 非思考双模式），请按 DMXAPI 实际提供的模型名填写。

## 💻 示例代码

### 开启思考（enable_thinking: True）

开启后，模型会先输出思考过程（链式推理），再给出最终答案。思考过程在 `reasoning_content` 字段，最终回答在 `content` 字段。

::: code-group

```python [非流式]
import requests

# 配置 API 密钥
api_key = "sk-***************************"  # 替换为你的 DMXAPI 令牌
url = "https://www.dmxapi.cn/v1/chat/completions"

headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json",
}

# 构造请求数据
data = {
    "model": "deepseek-v4-flash",  # DeepSeek 系列思考模型，可换成 deepseek-v4-pro 等（按 DMXAPI 实际提供的名称填写）
    "messages": [
        {
            "role": "user",
            "content": "从1加到10等于多少？",  # 用户提问
        }
    ],
    "enable_thinking": True,   # 开启思考功能：先输出思考过程再给答案
}

try:
    response = requests.post(url, headers=headers, json=data, timeout=300)
    response.raise_for_status()
    result = response.json()

    # 思考过程与最终回答分别在 reasoning_content 和 content 字段
    message = result["choices"][0]["message"]
    reasoning = message.get("reasoning_content") or ""
    answer = message.get("content") or ""

    print("请求成功!\n")
    if reasoning:
        print("========== 思考过程 ==========")
        print(reasoning)
    else:
        print("!!! 未返回思考内容，检查模型是否支持 enable_thinking")

    print("\n========== 最终回答 ==========")
    print(answer)

    # 思考内容按输出 token 计费，reasoning_tokens 体现本次思考的实际消耗
    usage = result.get("usage", {})
    details = usage.get("completion_tokens_details", {})
    print("\n========== Token 用量 ==========")
    print(f"思考 token: {details.get('reasoning_tokens', 0)}")
    print(f"输出 token: {usage.get('completion_tokens', 0)}")
    print(f"总计 token: {usage.get('total_tokens', 0)}")

except requests.exceptions.RequestException as e:
    print(f"请求失败: {e}")
```

```python [流式]
import json
import requests

# 配置 API 密钥
api_key = "sk-***************************"  # 替换为你的 DMXAPI 令牌
url = "https://www.dmxapi.cn/v1/chat/completions"

headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json",
}

# 构造请求数据
data = {
    "model": "deepseek-v4-flash",  # DeepSeek 系列思考模型，可换成 deepseek-v4-pro 等（按 DMXAPI 实际提供的名称填写）
    "messages": [
        {"role": "user", "content": "一个池塘里的睡莲每天面积翻一倍，第30天铺满整个池塘。第几天铺满一半？"}
    ],
    "enable_thinking": True,   # 开启思考功能：先输出思考过程再给答案
    "stream": True,            # 流式返回，边生成边输出
}

try:
    with requests.post(url, headers=headers, json=data, stream=True, timeout=300) as response:
        response.raise_for_status()

        in_reasoning = False
        in_answer = False

        # 注意：必须按 bytes 分行再手动 utf-8 解码。
        # decode_unicode=True 会用 response.encoding（默认 ISO-8859-1）逐块解码，
        # 中文会乱码且 JSON 行会被切断。
        for raw in response.iter_lines(decode_unicode=False):
            if not raw:
                continue
            line = raw.decode("utf-8")
            if not line.startswith("data: "):
                continue
            payload = line[6:]
            if payload == "[DONE]":
                break

            chunk = json.loads(payload)
            delta = chunk["choices"][0].get("delta", {})

            # 思考增量
            reasoning = delta.get("reasoning_content")
            if reasoning:
                if not in_reasoning:
                    print("========== 思考过程 ==========")
                    in_reasoning = True
                print(reasoning, end="", flush=True)

            # 正文增量
            content = delta.get("content")
            if content:
                if not in_answer:
                    print("\n\n========== 最终回答 ==========")
                    in_answer = True
                print(content, end="", flush=True)

        print()

except requests.exceptions.RequestException as e:
    print(f"请求失败: {e}")
```

:::

### 关闭思考（enable_thinking: False）

关闭后，模型跳过思考过程，直接给出最终答案，`reasoning_content` 不再返回内容。

```python
import requests

# 配置 API 密钥
api_key = "sk-***************************"  # 替换为你的 DMXAPI 令牌
url = "https://www.dmxapi.cn/v1/chat/completions"

headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json",
}

# 构造请求数据
data = {
    "model": "deepseek-v4-flash",  # DeepSeek 系列模型，可换成 deepseek-v4-pro 等（按 DMXAPI 实际提供的名称填写）
    "messages": [
        {
            "role": "user",
            "content": "从1加到10等于多少？",  # 用户提问
        }
    ],
    "enable_thinking": False,  # 关闭思考功能：直接给出最终答案
    # deepseek-v4-pro 上 enable_thinking: False 不生效，需改用下面这行：
    # "thinking": {"type": "disabled"},
}

try:
    response = requests.post(url, headers=headers, json=data, timeout=300)
    response.raise_for_status()
    result = response.json()

    # 关闭思考后 reasoning_content 为空，最终回答仍在 content 字段
    message = result["choices"][0]["message"]
    reasoning = message.get("reasoning_content") or ""
    answer = message.get("content") or ""

    print("请求成功!\n")
    if reasoning:
        print('!!! 仍返回了思考内容，deepseek-v4-pro 需改用 thinking: {"type": "disabled"}')

    print("========== 最终回答 ==========")
    print(answer)

    # 思考已关闭，思考 token 应为 0
    usage = result.get("usage", {})
    details = usage.get("completion_tokens_details", {})
    print("\n========== Token 用量 ==========")
    print(f"思考 token: {details.get('reasoning_tokens', 0)}")
    print(f"输出 token: {usage.get('completion_tokens', 0)}")
    print(f"总计 token: {usage.get('total_tokens', 0)}")

except requests.exceptions.RequestException as e:
    print(f"请求失败: {e}")
```

<p align="center">
  <small>© 2026 DMXAPI DeepSeek thinking</small>
</p>
