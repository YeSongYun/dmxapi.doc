# GPT-5.4 使用指南

GPT-5.4 是 OpenAI 迄今为止最强大的前沿模型，在 GPT-5.2 的基础上带来了多项突破性新特性：**百万 Token 上下文窗口**、**内置 Computer Use**（直接操控 UI）、**原生上下文压缩**以及更精细的输出控制。强烈推荐通过 **Responses API** 调用，以充分利用跨轮传递推理链（chain of thought）的能力。

## 请求地址

```
https://www.dmxapi.cn/v1/responses
```

<!-- ## 模型列表

| 模型名称 | 说明 |
|---|---|
| `gpt-5.4` | 标准版，均衡性能与速度 |
| `gpt-5.4-pro` | 增强推理版，投入更多计算资源进行深度思考 |
| `gpt-5.4-mini` | 轻量版，低延迟场景 | -->

## 快速入门

以下示例展示最简单的 GPT-5.4 调用：

::: code-group
```python [SDK]
import json
from openai import OpenAI

client = OpenAI(
    # 🔐 DMXAPI 密钥 (请替换为您自己的密钥)
    # 获取方式: 登录 DMXAPI 官网 -> 个人中心 -> API 密钥管理
    api_key="sk-***************************************",

    # 🌐 DMXAPI 服务端点地址
    base_url="https://www.dmxapi.cn/v1",
)

response = client.responses.create(
    model="gpt-5.4",
    input="请用三句话解释量子纠缠。",
)

# 将响应转换为 JSON 格式并格式化输出
response_dict = response.model_dump()
print(json.dumps(response_dict, indent=2, ensure_ascii=False))
```
```python [responses]
"""
功能描述：DMXAPI GPT-5.4 接口快速入门
说明：演示如何调用 DMXAPI 的 responses 端点进行 AI 对话
"""

import requests
import json

# API 端点地址
url = "https://www.dmxapi.cn/v1/responses"

# 请求头配置：包含认证信息和内容类型
headers = {
    "Authorization": "sk-***************************************",  # API 密钥
    "Content-Type": "application/json"
}

# 请求体
data = {
    "model": "gpt-5.4",
    "input": "请用三句话解释量子纠缠。"
}

# 发送 POST 请求
response = requests.post(url, headers=headers, json=data)

# 格式化输出响应结果（支持中文显示）
print(json.dumps(response.json(), indent=2, ensure_ascii=False))
```
```python [chat completions]
"""
功能描述：DMXAPI GPT-5.4 Chat Completions 接口快速入门
"""

import json
import requests

API_URL = "https://www.dmxapi.cn/v1/chat/completions"
API_KEY = "sk-***************************************"

headers = {
    "Authorization": f"{API_KEY}",
    "Content-Type": "application/json"
}

payload = {
    "model": "gpt-5.4",
    "messages": [
        {
            "role": "user",
            "content": "请用三句话解释量子纠缠。"
        }
    ]
}

if __name__ == "__main__":
    response = requests.post(url=API_URL, headers=headers, json=payload)
    result = response.json()
    print(json.dumps(result, indent=4, ensure_ascii=False))
```
:::

## 核心新特性

### 百万 Token 上下文窗口

GPT-5.4 支持高达 **1,000,000 个 Token** 的上下文窗口，适用于：
- 超长文档分析（整本书、完整代码库）
- 长对话历史保留
- 大规模数据摘要与问答

调用方式与普通请求相同，只需确保输入总长度不超过 1M tokens：

```python
import requests
import json

url = "https://www.dmxapi.cn/v1/responses"

headers = {
    "Authorization": "sk-***************************************",
    "Content-Type": "application/json"
}

# 可传入超长文档内容
long_document = "...（此处为超长文档内容，最多 100 万 token）..."

data = {
    "model": "gpt-5.4",
    "input": f"请总结以下文档的核心观点：\n\n{long_document}",
}

response = requests.post(url, headers=headers, json=data)
print(json.dumps(response.json(), indent=2, ensure_ascii=False))
```

### 内置 Computer Use

GPT-5.4 内置了 **Computer Use** 能力，模型可以直接接收屏幕截图，并输出结构化的 UI 操作指令（点击、输入、滚动、拖拽等），由调用方在本地执行这些指令，再将新截图反馈给模型，形成**视觉-操作循环**，从而实现自动化操控任何图形界面。

#### 工作原理

```
用户任务
  ↓
截图发给 GPT-5.4
  ↓
模型返回操作指令（click / type / scroll ...）
  ↓
本地执行指令（Playwright / Selenium / xdotool ...）
  ↓
重新截图 → 发回模型
  ↓
重复，直到任务完成
```

#### 三种集成方式

| 方式 | 适用场景 | 说明 |
|---|---|---|
| **内置循环**（推荐） | 快速原型、通用自动化 | 模型直接返回 UI 操作，由你的代码执行并循环 |
| **自定义工具/Harness** | 已有 Playwright/Selenium/VNC 框架 | 复用现有自动化框架，无需重构 |
| **代码执行 Harness** | 复杂混合任务 | 模型编写脚本，混合视觉交互与 DOM 编程访问 |

#### 支持的操作类型

| 操作类型 | 说明 |
|---|---|
| `click` | 单击指定坐标 |
| `double_click` | 双击指定坐标 |
| `scroll` | 在指定位置滚动（支持方向和距离） |
| `drag` | 从起点拖拽到终点 |
| `move` | 移动鼠标到指定位置（不点击） |
| `type` | 键盘输入文本 |
| `keypress` | 按下指定按键（如 Enter、Tab） |
| `wait` | 等待指定毫秒 |
| `screenshot` | 请求新截图 |

#### 代码示例

##### 基础单轮示例

将屏幕截图发给模型，获取第一步操作指令：

```python
import requests
import json
import base64

url = "https://www.dmxapi.cn/v1/responses"

headers = {
    "Authorization": "sk-***********************************",
    "Content-Type": "application/json"
}

# 将截图转为 base64
with open("./click.png", "rb") as f:
    image_b64 = base64.b64encode(f.read()).decode("utf-8")

data = {
    "model": "gpt-5.4",
    "input": [
        {
            "type": "message",
            "role": "user",
            "content": [
                {
                    "type": "input_image",
                    "image_url": f"data:image/png;base64,{image_b64}",
                    "detail": "original"   # 保持原始分辨率，提升点击精度
                },
                {
                    "type": "input_text",
                    "text": "请点击页面上的「立即购买」按钮。"
                }
            ]
        }
    ],
    "tools": [
        {
            "type": "computer"
        }
    ]
}

response = requests.post(url, headers=headers, json=data)
print(json.dumps(response.json(), indent=2, ensure_ascii=False))
```

##### 完整自动化循环（Playwright）

以下示例展示了一个完整的 Computer Use 自动化循环，使用 Playwright 执行模型返回的操作指令：

```python
import requests
import json
import base64
import time
from playwright.sync_api import sync_playwright

# ── 配置 ──────────────────────────────────────────────────────────
API_URL = "https://www.dmxapi.cn/v1/responses"
API_KEY = "sk-*************************************"
MAX_STEPS = 20   # 最大循环步数，防止无限循环

headers = {
    "Authorization": API_KEY,
    "Content-Type": "application/json"
}

# ── 工具函数 ───────────────────────────────────────────────────────

def take_screenshot(page) -> str:
    """截取当前页面截图，返回 base64 字符串"""
    screenshot_bytes = page.screenshot()
    return base64.b64encode(screenshot_bytes).decode("utf-8")


def execute_action(page, action: dict) -> None:
    """
    根据模型返回的 action 执行对应的 UI 操作

    action 结构示例：
    {"type": "click", "x": 640, "y": 360}
    {"type": "type", "text": "Hello World"}
    {"type": "scroll", "x": 640, "y": 360, "direction": "down", "amount": 3}
    {"type": "keypress", "keys": ["Enter"]}
    """
    action_type = action.get("type")

    if action_type == "click":
        page.mouse.click(action["x"], action["y"])
        print(f"  → 点击 ({action['x']}, {action['y']})")

    elif action_type == "double_click":
        page.mouse.dblclick(action["x"], action["y"])
        print(f"  → 双击 ({action['x']}, {action['y']})")

    elif action_type == "type":
        page.keyboard.type(action["text"])
        print(f"  → 输入文本: {action['text'][:30]}...")

    elif action_type == "keypress":
        # 将模型返回的按键名映射到 Playwright 接受的格式
        key_map = {
            "CTRL": "Control", "ALT": "Alt", "SHIFT": "Shift",
            "META": "Meta", "WIN": "Meta", "CMD": "Meta",
            "ENTER": "Enter", "RETURN": "Enter", "ESC": "Escape",
            "ESCAPE": "Escape", "TAB": "Tab", "SPACE": " ",
            "BACKSPACE": "Backspace", "DELETE": "Delete", "DEL": "Delete",
            "UP": "ArrowUp", "DOWN": "ArrowDown", "LEFT": "ArrowLeft", "RIGHT": "ArrowRight",
            "HOME": "Home", "END": "End", "PAGEUP": "PageUp", "PAGEDOWN": "PageDown",
        }
        keys = action.get("keys", [])
        mapped_keys = [key_map.get(k.upper(), k) for k in keys]
        # 多个键组合（如 Ctrl+A）用 "+" 连接
        if len(mapped_keys) > 1:
            page.keyboard.press("+".join(mapped_keys))
        elif mapped_keys:
            page.keyboard.press(mapped_keys[0])
        print(f"  → 按键: {keys}")

    elif action_type == "scroll":
        # direction: "up" | "down" | "left" | "right"
        delta_y = -action.get("amount", 3) * 100 if action.get("direction") == "up" else action.get("amount", 3) * 100
        delta_x = -action.get("amount", 3) * 100 if action.get("direction") == "left" else 0
        page.mouse.wheel(delta_x, delta_y)
        print(f"  → 滚动: {action.get('direction')} x{action.get('amount', 3)}")

    elif action_type == "drag":
        page.mouse.move(action["startX"], action["startY"])
        page.mouse.down()
        page.mouse.move(action["endX"], action["endY"])
        page.mouse.up()
        print(f"  → 拖拽: ({action['startX']},{action['startY']}) → ({action['endX']},{action['endY']})")

    elif action_type == "move":
        page.mouse.move(action["x"], action["y"])

    elif action_type == "wait":
        ms = action.get("ms", 1000)
        time.sleep(ms / 1000)
        print(f"  → 等待 {ms}ms")

    elif action_type == "screenshot":
        print("  → 模型请求新截图")

    else:
        print(f"  ⚠ 未知操作类型: {action_type}")


def call_model(conversation: list) -> dict:
    """
    调用 GPT-5.4 Computer Use 接口
    conversation: 完整对话历史，每轮追加模型输出和 computer_call_output
    """
    data = {
        "model": "gpt-5.4",
        "tools": [{"type": "computer"}],
        "input": conversation,
    }
    response = requests.post(API_URL, headers=headers, json=data)
    return response.json()


# ── 主循环 ─────────────────────────────────────────────────────────

def run_computer_use(task: str, start_url: str):
    """
    执行 Computer Use 自动化任务

    参数:
        task: 自然语言任务描述
        start_url: 起始页面 URL
    """
    with sync_playwright() as p:
        # 启动浏览器（建议使用沙箱隔离）
        browser = p.chromium.launch(
            headless=False,           # 设为 True 可无界面运行
            args=["--no-sandbox"]
        )
        page = browser.new_page(viewport={"width": 1280, "height": 800})
        page.goto(start_url)
        page.wait_for_load_state("networkidle")

        print(f"🚀 开始任务: {task}")
        print(f"🌐 起始页面: {start_url}")
        print("-" * 60)

        # 完整对话历史，首条为任务描述
        conversation = [
            {
                "type": "message",
                "role": "user",
                "content": [{"type": "input_text", "text": task}]
            }
        ]

        for step in range(MAX_STEPS):
            print(f"\n[步骤 {step + 1}/{MAX_STEPS}]")

            result = call_model(conversation)

            # 调试：打印原始返回
            print(f"  [DEBUG] API 返回: {json.dumps(result, ensure_ascii=False)[:800]}")

            # 解析模型输出
            output = result.get("output", [])
            call_id = None
            actions_executed = 0
            has_computer_call = any(item.get("type") == "computer_call" for item in output)

            for item in output:
                # 将模型输出追加到对话历史
                conversation.append(item)

                if item.get("type") == "computer_call":
                    call_id = item.get("call_id")
                    for action in item.get("actions", []):
                        execute_action(page, action)
                        actions_executed += 1
                        time.sleep(0.5)   # 每步操作后短暂等待，让页面响应

                elif item.get("type") == "message":
                    for content in item.get("content", []):
                        if content.get("type") == "output_text":
                            text = content.get("text", "")
                            if text:
                                print(f"\n🤖 模型消息: {text}")

            # 只有没有 computer_call 的纯消息才表示任务结束
            if not has_computer_call:
                print("\n✅ 任务完成！")
                break

            # 执行完动作后截新图，追加 computer_call_output 到对话历史
            if call_id:
                time.sleep(1)   # 等待页面渲染稳定
                new_screenshot_b64 = take_screenshot(page)
                conversation.append({
                    "type": "computer_call_output",
                    "call_id": call_id,
                    "output": {
                        "type": "computer_screenshot",
                        "image_url": f"data:image/png;base64,{new_screenshot_b64}",
                        "detail": "original"
                    }
                })

        browser.close()


# ── 入口 ──────────────────────────────────────────────────────────

if __name__ == "__main__":
    run_computer_use(
        task="""请完成以下操作：
1. 在百度搜索"北京今天天气"，查看天气结果
2. 清空搜索框，再搜索"上海今天天气"，对比两地天气
3. 告诉我北京和上海今天的天气各是什么情况""",
        start_url="https://www.baidu.com"
    )

```

#### 环境类型说明

`environment` 参数指定运行环境，影响模型生成操作指令的方式：

| 值 | 适用场景 |
|---|---|
| `browser` | Playwright、Selenium 等浏览器自动化 |
| `mac` | macOS 桌面应用（通过 Accessibility API） |
| `windows` | Windows 桌面应用（通过 Win32 API） |
| `ubuntu` | Linux 桌面（通过 xdotool、xdg-open 等） |

### 原生上下文压缩（Compaction）

GPT-5.4 引入了**原生 Compaction** 机制，在长 Agent 任务中自动压缩历史上下文，在保留关键信息的同时大幅降低 token 消耗，支持更长的 Agent 轨迹。

```python
import requests
import json

url = "https://www.dmxapi.cn/v1/responses"

headers = {
    "Authorization": "sk-***************************************",
    "Content-Type": "application/json"
}

data = {
    "model": "gpt-5.4",
    "input": "请帮我完成一个复杂的多步骤数据分析任务...",
    # 启用上下文压缩，适合长 Agent 任务
    "truncation": "auto"
}

response = requests.post(url, headers=headers, json=data)
print(json.dumps(response.json(), indent=2, ensure_ascii=False))
```

> **提示**：`truncation: "auto"` 让模型自动管理上下文压缩策略。对于需要多轮迭代的 Agent 场景，推荐始终开启此选项。

### 增强的代码生成能力

GPT-5.4 在代码生成领域有显著提升，支持更大规模的代码库理解与生成。结合百万 Token 上下文，可一次性读取整个项目并生成完整解决方案：

```python
import requests
import json

url = "https://www.dmxapi.cn/v1/responses"

headers = {
    "Authorization": "sk-***************************************",
    "Content-Type": "application/json"
}

data = {
    "model": "gpt-5.4",
    "input": "请为以下 Python 项目编写完整的单元测试套件...",
    "reasoning": {
        "effort": "medium"   # 代码任务推荐 medium 或 high
    },
    "text": {
        "verbosity": "high"  # 代码任务推荐 high 以获得完整注释
    }
}

response = requests.post(url, headers=headers, json=data)
print(json.dumps(response.json(), indent=2, ensure_ascii=False))
```

## 推理强度控制

GPT-5.4 支持四档推理强度：`none`（默认，最低延迟）、`low`、`medium`、`high`。推理等级越高，模型思考越深入，但响应时间也相应增加。

::: code-group
```python [SDK]
import json
from openai import OpenAI

client = OpenAI(
    api_key="sk-***************************************",
    base_url="https://www.dmxapi.cn/v1",
)

response = client.responses.create(
    model="gpt-5.4",
    input="请分析以下商业计划书的可行性...",
    reasoning={
        "effort": "high"  # none | low | medium | high
    }
)

response_dict = response.model_dump()
print(json.dumps(response_dict, indent=2, ensure_ascii=False))
```
```python [responses]
import requests
import json

url = "https://www.dmxapi.cn/v1/responses"

headers = {
    "Authorization": "sk-***************************************",
    "Content-Type": "application/json"
}

data = {
    "model": "gpt-5.4",
    "input": "请分析以下商业计划书的可行性...",
    "reasoning": {
        "effort": "high"   # none | low | medium | high
    }
}

response = requests.post(url, headers=headers, json=data)
print(json.dumps(response.json(), indent=2, ensure_ascii=False))
```
```python [chat completions]
import json
import requests

API_URL = "https://www.dmxapi.cn/v1/chat/completions"
API_KEY = "sk-***************************************"

headers = {
    "Authorization": f"{API_KEY}",
    "Content-Type": "application/json"
}

payload = {
    "model": "gpt-5.4",
    "messages": [
        {
            "role": "user",
            "content": "请分析以下商业计划书的可行性..."
        }
    ],
    "reasoning_effort": "high"   # none | low | medium | high
}

if __name__ == "__main__":
    response = requests.post(url=API_URL, headers=headers, json=payload)
    result = response.json()
    print(json.dumps(result, indent=4, ensure_ascii=False))
```
:::

推理强度说明：

| 推理等级 | 适用场景 | 延迟 |
|---|---|---|
| `none` | 简单问答、实时对话（默认） | 最低 |
| `low` | 一般性分析任务 | 低 |
| `medium` | 复杂推理、代码生成 | 中 |
| `high` | 数学证明、深度分析、复杂规划 | 高 |

## 输出详细程度

`verbosity` 控制模型的输出详尽程度，影响代码注释量、解释长度等。默认值为 `medium`。

::: code-group
```python [SDK]
import json
from openai import OpenAI

client = OpenAI(
    api_key="sk-***************************************",
    base_url="https://www.dmxapi.cn/v1",
)

response = client.responses.create(
    model="gpt-5.4",
    input="用 Python 实现一个二叉搜索树。",
    text={
        "verbosity": "high"  # low | medium | high
    }
)

response_dict = response.model_dump()
print(json.dumps(response_dict, indent=2, ensure_ascii=False))
```
```python [responses]
import requests
import json

url = "https://www.dmxapi.cn/v1/responses"

headers = {
    "Authorization": "sk-***************************************",
    "Content-Type": "application/json"
}

data = {
    "model": "gpt-5.4",
    "input": "用 Python 实现一个二叉搜索树。",
    "text": {
        "verbosity": "high"  # low | medium | high
    }
}

response = requests.post(url, headers=headers, json=data)
print(json.dumps(response.json(), indent=2, ensure_ascii=False))
```
```python [chat completions]
import json
import requests

API_URL = "https://www.dmxapi.cn/v1/chat/completions"
API_KEY = "sk-***************************************"

headers = {
    "Authorization": f"{API_KEY}",
    "Content-Type": "application/json"
}

payload = {
    "model": "gpt-5.4",
    "messages": [
        {
            "role": "user",
            "content": "用 Python 实现一个二叉搜索树。"
        }
    ],
    "verbosity": "high"   # low | medium | high
}

if __name__ == "__main__":
    response = requests.post(url=API_URL, headers=headers, json=payload)
    result = response.json()
    print(json.dumps(result, indent=4, ensure_ascii=False))
```
:::

| 详细级别 | 代码场景效果 |
|---|---|
| `low` | 代码简洁，注释极少 |
| `medium` | 适度注释，结构清晰（默认） |
| `high` | 完整注释，详细解释，适合教学场景 |

## Phase 参数

`phase` 是放在**输入侧（input）**assistant 消息里的字段，用于多轮对话**回放历史消息**时，告诉模型哪些是过渡性前言（`commentary`）、哪些是最终答案（`final_answer`），从而避免模型把前言误判为最终输出，导致多步任务早停。

> **注意**：如果使用 `previous_response_id` 传递历史，`phase` 由 API 自动保留，无需手动处理。只有手动构建对话历史时，才需要把上一轮 assistant 消息的 `phase` 值原样带回。

### 场景一：流式输出推理过程

推理内容通过 `response.reasoning_summary_text.delta` 事件返回，最终答案通过 `response.output_text.delta` 返回：

```python
import requests
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

url = "https://www.dmxapi.cn/v1/responses"

headers = {
    "Authorization": "sk-***************************************",
    "Content-Type": "application/json"
}

data = {
    "model": "gpt-5.4",
    "input": "请一步步推导：为什么耳机总是会缠在一起",
    "stream": True,
    "reasoning": {"effort": "medium"}
}

response = requests.post(url, headers=headers, json=data, stream=True)

print("=" * 60)

in_reasoning = False  # 标记当前是否处于思考阶段

for line in response.iter_lines():
    if line:
        line_str = line.decode("utf-8")
        if line_str.startswith("data: "):
            event_data = line_str[6:]
            if event_data == "[DONE]":
                break
            try:
                event = json.loads(event_data)
                event_type = event.get("type", "")

                # 思考阶段开始：打一次标题
                if event_type == "response.reasoning_summary_text.delta":
                    if not in_reasoning:
                        print("【思考过程】")
                        in_reasoning = True
                    print(event.get("delta", ""), end="", flush=True)

                # 思考阶段结束
                elif event_type == "response.reasoning_summary_text.done":
                    if in_reasoning:
                        print("\n" + "=" * 60)
                        print("【最终回答】")
                        in_reasoning = False

                # 最终答案
                elif event_type == "response.output_text.delta":
                    print(event.get("delta", ""), end="", flush=True)

            except json.JSONDecodeError:
                pass

print("\n" + "=" * 60)
```

### 场景二：多轮对话，手动构建历史

手动构建对话历史时，需把上一轮 assistant 消息的 `phase` 原样带回：

```python
import requests
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

url = "https://www.dmxapi.cn/v1/responses"
headers = {
    "Authorization": "sk-**********************************",
    "Content-Type": "application/json"
}

# 第一轮对话
resp1 = requests.post(url, headers=headers, json={
    "model": "gpt-5.4",
    "input": "请介绍一下大语言模型的核心原理，包括 Transformer 架构和注意力机制。"
}).json()

# 从响应中提取 assistant 消息，保留原始 phase 值
assistant_messages = [
    item for item in resp1.get("output", [])
    if item.get("type") == "message" and item.get("role") == "assistant"
]

# 第二轮对话：把上一轮 assistant 消息的 phase 原样带回
resp2 = requests.post(url, headers=headers, json={
    "model": "gpt-5.4",
    "input": [
        {"role": "user", "content": "请介绍一下大语言模型的核心原理，包括 Transformer 架构和注意力机制。"},
        # ↓ 保留原始 phase，避免模型把前言误判为最终输出而早停
        *[
            {
                "role": "assistant",
                "phase": msg.get("phase"),
                "content": msg.get("content")
            }
            for msg in assistant_messages
        ],
        {"role": "user", "content": "能用一个通俗的比喻解释注意力机制吗？让完全不懂技术的人也能理解。"}
    ]
}).json()

# 打印第二轮回答
for item in resp2.get("output", []):
    if item.get("type") == "message":
        for block in item.get("content", []):
            if isinstance(block, dict) and block.get("type") == "output_text":
                print(f"\n第二轮回答:\n{block['text']}")
```

### phase 使用场景说明

| 场景 | phase 的位置 | 作用 |
|---|---|---|
| 单轮输出 | 响应的 output 字段中（只读） | 标记该条 assistant 消息是前言还是最终答案 |
| 多轮对话（手动构建历史） | 输入的 assistant 消息中 | 告诉模型历史中哪些是前言，避免早停 |
| 多轮对话（用 `previous_response_id`） | 无需处理 | API 自动保留 |
| 推理过程的流式输出 | 不通过 phase 传递 | 通过 `response.reasoning_summary_text.delta` 独立事件返回 |

## 自定义工具

GPT-5.4 延续了 GPT-5 系列的自定义工具（Custom Tools）功能，支持以任意原始文本作为工具调用输入，并可按需约束输出格式。

```python
import math
import requests
import json

url = "https://www.dmxapi.cn/v1/responses"

headers = {
    "Authorization": "sk-****************************",
    "Content-Type": "application/json"
}

TOOLS = [
    {
        "type": "custom",
        "name": "calculator",
        "description": "计算数学表达式，输入为合法的 Python 数学表达式字符串，返回计算结果"
    }
]

# 测试用例：(描述, 问题, 预期是否调用工具)
TEST_CASES = [
    ("【应调用工具】订单计算", "我有一个订单，单价 99.8 元，买了 37 件，再打 8.5 折，最终要付多少钱？", True),
    ("【应调用工具】面积计算", "一个半径为 7.5 米的圆形水池，面积是多少平方米？", True),
    ("【不应调用工具】闲聊",  "你好，请介绍一下你自己。", False),
    ("【不应调用工具】常识题", "中国的首都是哪里？", False),
]


def calculator(expression: str) -> str:
    """本地执行数学表达式，只允许 math 模块内的函数"""
    try:
        allowed = {k: v for k, v in math.__dict__.items() if not k.startswith("_")}
        result = eval(expression, {"__builtins__": {}}, allowed)
        return str(round(result, 4))
    except Exception as e:
        return f"计算错误: {e}"


def extract_text(output):
    """从模型 output 中提取纯文本回答"""
    for item in output:
        for content in item.get("content", []):
            if content.get("type") == "output_text":
                return content.get("text", "")
    return ""


def run_case(desc, question, expect_tool):
    print("\n" + "=" * 60)
    print(f"测试: {desc}")
    print(f"问题: {question}")
    print("=" * 60)

    # 第一轮：让模型决定是否调用工具
    resp1 = requests.post(url, headers=headers, json={
        "model": "gpt-5.4",
        "input": question,
        "tools": TOOLS,
    }).json()

    tool_call = next(
        (item for item in resp1.get("output", []) if item.get("type") == "custom_tool_call"),
        None
    )

    called = tool_call is not None
    tag = "✅" if called == expect_tool else "❌"
    print(f"{tag} 模型{'调用了' if called else '未调用'}工具  (预期: {'调用' if expect_tool else '不调用'})")

    if not called:
        # 模型直接回答，不需要工具
        print("模型直接回答：", extract_text(resp1.get("output", [])) or json.dumps(resp1, ensure_ascii=False)[:200])
        return

    tool_name    = tool_call.get("name", "")
    tool_input   = tool_call.get("input", "")
    tool_id      = tool_call.get("id")
    tool_call_id = tool_call.get("call_id")

    print(f"   工具名: {tool_name}")
    print(f"   表达式: {tool_input}")
    print(f"   id={tool_id}  call_id={tool_call_id}")

    # input 为空则无法计算，终止本轮
    if not tool_input:
        print("❌ 工具调用缺少 input 字段，无法执行")
        return

    # 第二轮：执行工具，把结果回传
    tool_result = calculator(tool_input)
    print(f"   计算结果: {tool_result}")

    # 回传时按实际有无 id/call_id 动态组装
    tool_call_msg = {"type": "custom_tool_call", "name": tool_name, "input": tool_input}
    if tool_id is not None:
        tool_call_msg["id"] = tool_id
    if tool_call_id is not None:
        tool_call_msg["call_id"] = tool_call_id

    tool_result_msg = {"type": "custom_tool_call_output", "output": tool_result}
    if tool_call_id is not None:
        tool_result_msg["call_id"] = tool_call_id

    resp2 = requests.post(url, headers=headers, json={
        "model": "gpt-5.4",
        "input": [
            {"type": "message", "role": "user", "content": question},
            tool_call_msg,
            tool_result_msg,
        ],
    }).json()

    final = extract_text(resp2.get("output", []))
    print("模型最终回答：", final or json.dumps(resp2, ensure_ascii=False)[:200])


for desc, question, expect_tool in TEST_CASES:
    run_case(desc, question, expect_tool)
```

## 工具搜索（Tool Search）

GPT-5.4 新增了**工具搜索（Tool Search）**功能，结合 CFG（Context-Free Grammar）约束输出，模型可以在大量工具定义中自动检索最相关的工具，无需手动传入完整工具列表。

```python
import requests
import json
import os
from datetime import datetime

url = "https://www.dmxapi.cn/v1/responses"

headers = {
    "Authorization": "sk-*******************************",
    "Content-Type": "application/json"
}

tools = [
    {
        "type": "custom",
        "name": "list_directory",
        "description": "列出指定目录下的所有文件名"
    },
    {
        "type": "custom",
        "name": "get_datetime",
        "description": "获取当前日期和时间"
    },
    {
        "type": "custom",
        "name": "write_file",
        "description": "将内容写入指定路径的文件（会覆盖原有内容）"
    },
    {
        "type": "custom",
        "name": "read_file",
        "description": "读取指定路径文件的内容"
    },
    {
        "type": "custom",
        "name": "append_to_file",
        "description": "向指定文件末尾追加内容，不覆盖原有内容"
    },
    {
        "type": "custom",
        "name": "get_file_info",
        "description": "获取文件的元信息，包括大小、创建时间、修改时间"
    },
    {
        "type": "custom",
        "name": "calculate",
        "description": "计算数学表达式，返回结果，支持加减乘除和括号"
    },
    {
        "type": "custom",
        "name": "count_lines",
        "description": "统计指定文件的行数和字符数"
    },

]

# ─────────────────────────────────────────────
# 真实工具实现（纯标准库，无需外部 API）
# ─────────────────────────────────────────────
def execute_tool(name, tool_input):
    print(f"  [执行工具] {name}，参数：{json.dumps(tool_input, ensure_ascii=False)}")

    raw = tool_input.get("raw", "").strip()

    if name == "list_directory":
        path = tool_input.get("path") or raw or "."
        try:
            files = os.listdir(path)
            return "\n".join(files) if files else "目录为空"
        except Exception as e:
            return f"错误：{e}"

    elif name == "get_datetime":
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    elif name == "write_file":
        if "path" in tool_input and "content" in tool_input:
            path = tool_input["path"]
            content = tool_input["content"]
        else:
            # raw 字符串：第一行是路径，其余是内容
            lines = raw.split("\n", 1)
            path = lines[0].strip()
            content = lines[1].lstrip("\n") if len(lines) > 1 else ""
        try:
            with open(path, "w", encoding="utf-8") as f:
                f.write(content)
            return f"文件已写入：{path}"
        except Exception as e:
            return f"错误：{e}"

    elif name == "read_file":
        path = tool_input.get("path") or raw
        try:
            with open(path, "r", encoding="utf-8") as f:
                return f.read()
        except Exception as e:
            return f"错误：{e}"

    elif name == "append_to_file":
        if "path" in tool_input and "content" in tool_input:
            path = tool_input["path"]
            content = tool_input["content"]
        else:
            lines = raw.split("\n", 1)
            path = lines[0].strip()
            content = lines[1].lstrip("\n") if len(lines) > 1 else ""
        try:
            with open(path, "a", encoding="utf-8") as f:
                f.write(content)
            return f"内容已追加到：{path}"
        except Exception as e:
            return f"错误：{e}"

    elif name == "get_file_info":
        path = tool_input.get("path") or raw
        try:
            stat = os.stat(path)
            size = stat.st_size
            modified = datetime.fromtimestamp(stat.st_mtime).strftime("%Y-%m-%d %H:%M:%S")
            created = datetime.fromtimestamp(stat.st_ctime).strftime("%Y-%m-%d %H:%M:%S")
            return f"路径：{path}\n大小：{size} 字节\n创建时间：{created}\n修改时间：{modified}"
        except Exception as e:
            return f"错误：{e}"

    elif name == "calculate":
        expr = tool_input.get("expression") or raw
        try:
            result = eval(expr, {"__builtins__": {}}, {})
            return str(result)
        except Exception as e:
            return f"计算错误：{e}"

    elif name == "count_lines":
        path = tool_input.get("path") or raw
        try:
            with open(path, "r", encoding="utf-8") as f:
                content = f.read()
            lines = content.splitlines()
            return f"文件：{path}\n行数：{len(lines)}\n字符数：{len(content)}"
        except Exception as e:
            return f"错误：{e}"

    elif name == "search_in_file":
        if "path" in tool_input and "keyword" in tool_input:
            path = tool_input["path"]
            keyword = tool_input["keyword"]
        else:
            lines = raw.split("\n", 1)
            path = lines[0].strip()
            keyword = lines[1].strip() if len(lines) > 1 else ""
        try:
            with open(path, "r", encoding="utf-8") as f:
                matched = [l.rstrip() for l in f if keyword in l]
            if matched:
                return f"找到 {len(matched)} 行：\n" + "\n".join(matched)
            else:
                return f'未找到包含"{keyword}"的行'
        except Exception as e:
            return f"错误：{e}"

    elif name == "create_directory":
        path = tool_input.get("path") or raw
        try:
            os.makedirs(path, exist_ok=True)
            return f"目录已创建：{path}"
        except Exception as e:
            return f"错误：{e}"

    else:
        return f"未知工具：{name}"


# ─────────────────────────────────────────────
# 多轮工具调用循环
# ─────────────────────────────────────────────
input_messages = (
    "请列出 C:/Users/a1/Desktop/测试保存代码 目录下的所有文件，"
    "获取当前时间，然后把文件清单（含生成时间）写入 "
    "C:/Users/a1/Desktop/测试保存代码/report.txt"
)

round_num = 0
while True:
    round_num += 1
    print(f"\n{'='*50}")
    print(f"第 {round_num} 轮请求")
    print('='*50)

    data = {
        "model": "gpt-5.4",
        "input": input_messages,
        "tools": tools,
        "tool_choice": "auto",
        "reasoning": {"effort": "high"}
    }

    response = requests.post(url, headers=headers, json=data)
    result = response.json()

    output = result.get("output", [])
    tool_calls = [item for item in output if item.get("type") == "custom_tool_call"]

    if not tool_calls:
        # 没有工具调用，输出最终回答
        for item in output:
            if item.get("type") == "message":
                for block in item.get("content", []):
                    if block.get("type") == "output_text":
                        print(f"\n模型回答：\n{block['text']}")
        print("\n✅ 完成。")
        break

    print(f"\n模型请求调用 {len(tool_calls)} 个工具：")

    # 构建下一轮 input（历史 + 工具结果）
    if isinstance(input_messages, str):
        history = [{"role": "user", "content": input_messages}]
    else:
        history = list(input_messages)

    for item in output:
        if item.get("type") != "reasoning":
            history.append(item)

    for tc in tool_calls:
        call_id = tc.get("call_id", "")
        tool_name = tc.get("name", "")
        tool_input = tc.get("input", {})

        if isinstance(tool_input, str):
            try:
                tool_input = json.loads(tool_input)
            except Exception:
                tool_input = {"raw": tool_input}

        tool_result = execute_tool(tool_name, tool_input)

        history.append({
            "type": "custom_tool_call_output",
            "call_id": call_id,
            "output": tool_result
        })

    input_messages = history

print("\n" + "="*50)
print("流程结束")

```

> **提示**：工具搜索特别适合工具数量庞大（数十甚至数百个）的场景。将所有工具注册后，模型会智能选择最匹配当前任务的工具，而非遍历全部工具。



<p align="center">
  <small>© 2026 GPT-5.4 使用指南</small>
</p>