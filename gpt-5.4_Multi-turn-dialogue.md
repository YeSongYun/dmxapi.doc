# DMXAPI GPT-5.6 Sol 多轮对话

本页保留原有 URL 以兼容旧链接，内容已迁移到 `gpt-5.6-sol`。示例通过 DMXAPI 兼容代理的 Chat Completions 接口维护完整 `messages` 历史，实现多轮上下文。

## 🔗 请求地址

```text
https://www.dmxapi.cn/v1/chat/completions
```

:::warning API 密钥安全
示例令牌为不可用占位符。请妥善保管真实 DMXAPI 令牌，不要在公开仓库或日志中泄露。
:::

## 模型名称

- `gpt-5.6-sol`

## 多轮对话示例代码

::: code-group

```python [requests]
from __future__ import annotations

import json
from typing import Iterable

import requests

API_URL = "https://www.dmxapi.cn/v1/chat/completions"
API_KEY = "sk-******************************************"
MODEL = "gpt-5.6-sol"
SYSTEM_PROMPT = "你是一个简洁、友好的中文助手。请在多轮对话中记住用户已经提供的信息。"
DEMO_TURNS = [
    "请记住：我的代号是蓝鲸。只回复收到。",
    "我的代号是什么？只回复代号。",
]


def build_headers(api_key: str) -> dict[str, str]:
    return {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }


def extract_assistant_text(payload: dict) -> str:
    choices = payload.get("choices") or []
    if not choices:
        raise ValueError("响应中缺少 choices 字段。")

    message = choices[0].get("message") or {}
    content = message.get("content")

    if isinstance(content, str):
        text = content.strip()
        if text:
            return text

    if isinstance(content, list):
        chunks = []
        for item in content:
            if not isinstance(item, dict):
                continue
            text = item.get("text")
            if isinstance(text, str) and text.strip():
                chunks.append(text.strip())
                continue
            if isinstance(text, dict):
                value = text.get("value")
                if isinstance(value, str) and value.strip():
                    chunks.append(value.strip())
        if chunks:
            return "\n".join(chunks)

    raise ValueError(f"无法从响应中提取 assistant 内容：{payload}")


def print_request_error(round_number: int, exc: requests.RequestException) -> None:
    print(f"第 {round_number} 轮请求失败")
    print(f"异常类型: {type(exc).__name__}")

    response = getattr(exc, "response", None)
    if response is not None:
        status_code = getattr(response, "status_code", None)
        if status_code is not None:
            print(f"状态码: {status_code}")

        response_text = getattr(response, "text", "")
        if response_text:
            print(f"响应体: {response_text}")

    print("-" * 60)


def print_parse_error(round_number: int, exc: Exception, payload: object) -> None:
    print(f"第 {round_number} 轮响应解析失败")
    print(f"异常类型: {type(exc).__name__}")
    print(f"错误信息: {exc}")

    if isinstance(payload, str):
        print(f"原始响应文本: {payload}")
    else:
        print(f"原始响应JSON: {json.dumps(payload, ensure_ascii=False)}")

    print("-" * 60)


def run_multi_turn_demo(
    api_key: str,
    api_url: str = API_URL,
    model: str = MODEL,
    turns: Iterable[str] | None = None,
    verbose: bool = True,
    system_prompt: str = SYSTEM_PROMPT,
) -> list[dict[str, str]]:
    if not api_key:
        raise ValueError("请先在脚本中填写 API_KEY。")

    if turns is None:
        turns = DEMO_TURNS

    history: list[dict[str, str]] = []
    headers = build_headers(api_key)

    for round_number, user_text in enumerate(turns, start=1):
        history.append({"role": "user", "content": user_text})

        payload = {
            # 【model】(string, 必填) 要调用的模型名称。
            # 这里使用 gpt-5.6-sol 作为示例。
            "model": model,
            # 【messages】(array, 必填) 对话消息列表，用于承载完整上下文。
            # 多轮对话的关键就是在每次请求时带上历史消息。
            "messages": [
                # 【role】(string, 必填) 消息角色。
                # system 用于设定助手行为。
                {"role": "system", "content": system_prompt},
                *history,
            ],
        }

        try:
            response = requests.post(api_url, headers=headers, json=payload)
            response.raise_for_status()
        except requests.RequestException as exc:
            print_request_error(round_number, exc)
            break

        try:
            response_payload = response.json()
        except ValueError as exc:
            print_parse_error(round_number, exc, response.text)
            break

        try:
            assistant_text = extract_assistant_text(response_payload)
        except ValueError as exc:
            print_parse_error(round_number, exc, response_payload)
            break

        history.append({"role": "assistant", "content": assistant_text})

        if verbose:
            print(f"第 {round_number} 轮用户：{user_text}")
            print(f"第 {round_number} 轮助手：{assistant_text}")
            print("-" * 60)

    return history


def main() -> None:
    try:
        run_multi_turn_demo(api_key=API_KEY)
    except requests.RequestException as exc:
        print(f"请求失败：{exc}")
    except ValueError as exc:
        print(f"参数错误：{exc}")


if __name__ == "__main__":
    main()
```

```python [SDK]
from __future__ import annotations
from typing import Iterable
from openai import OpenAI
BASE_URL = "https://www.dmxapi.cn/v1"
API_KEY = "sk-******************************************"
MODEL = "gpt-5.6-sol"
SYSTEM_PROMPT = "你是一个简洁、友好的中文助手。请在多轮对话中记住用户已经提供的信息。"
DEMO_TURNS = [
    "请记住：我的代号是蓝鲸。只回复收到。",
    "我的代号是什么？只回复代号。",
]


def build_client(api_key: str, base_url: str = BASE_URL) -> OpenAI:
    return OpenAI(
        # 【api_key】(string, 必填) DMXAPI 平台的 API 密钥。
        api_key=api_key,
        # 【base_url】(string, 必填) DMXAPI 兼容 OpenAI SDK 的基础地址。
        base_url=base_url,
    )


def extract_assistant_text(response) -> str:
    choices = getattr(response, "choices", None) or []
    if not choices:
        raise ValueError("响应中缺少 choices 字段。")

    message = getattr(choices[0], "message", None)
    if message is None:
        raise ValueError("响应中缺少 message 字段。")

    content = getattr(message, "content", None)
    if isinstance(content, str) and content.strip():
        return content.strip()

    raise ValueError(f"无法从响应中提取 assistant 内容：{response}")


def run_multi_turn_demo(
    api_key: str,
    model: str = MODEL,
    turns: Iterable[str] | None = None,
    verbose: bool = True,
    system_prompt: str = SYSTEM_PROMPT,
) -> list[dict[str, str]]:
    if not api_key:
        raise ValueError("请先在代码里填写 API_KEY。")

    if turns is None:
        turns = DEMO_TURNS

    client = build_client(api_key)
    history: list[dict[str, str]] = []

    for round_number, user_text in enumerate(turns, start=1):
        history.append({"role": "user", "content": user_text})

        response = client.chat.completions.create(
            # 【model】(string, 必填) 要调用的模型名称。
            model=model,
            # 【messages】(array, 必填) 对话消息列表，按顺序传入 system、user、assistant 等历史消息。
            messages=[
                # 【role】(string, 必填) 消息角色。
                # system 表示系统提示词，用于控制助手行为。
                {"role": "system", "content": system_prompt},
                *history,
            ],
        )

        assistant_text = extract_assistant_text(response)
        history.append({"role": "assistant", "content": assistant_text})

        if verbose:
            print(f"第 {round_number} 轮用户：{user_text}")
            print(f"第 {round_number} 轮助手：{assistant_text}")
            print("-" * 60)

    return history


def main() -> None:
    try:
        run_multi_turn_demo(api_key=API_KEY)
    except Exception as exc:
        print(f"运行失败：{type(exc).__name__}: {exc}")


if __name__ == "__main__":
    main()
```

:::

## 返回示例

```text
用户：请记住：我的代号是蓝鲸。只回复收到。
助手：收到。
用户：我的代号是什么？只回复代号。
助手：蓝鲸
```

## 注意事项

- 每一轮都要把此前的 `user` 和 `assistant` 消息按原顺序带回。
- 对话变长时要关注上下文 token、延迟与成本；不要无限累积无关历史。
- DMXAPI 修改前实测已验证两轮上下文能正确保留“蓝鲸”代号。

<p align="center">
  <small>© 2026 DMXAPI GPT-5.6 Sol 多轮对话</small>
</p>
