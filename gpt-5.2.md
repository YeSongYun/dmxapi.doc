# GPT-5.2 使用指南

## 🔗 请求地址

### Responses API

```text
https://www.dmxapi.cn/v1/responses
```

### Chat Completions API

```text
https://www.dmxapi.cn/v1/chat/completions
```

OpenAI 推出了三款新模型。总体而言，`gpt-5.2` 最适合处理那些需要广泛世界知识的复杂任务，它已取代此前的 `gpt-5.1` 模型。ChatGPT 所采用的模型是 `gpt-5.2-chat-latest`。第三款模型 `gpt-5.2-pro` 则通过投入更多计算资源，以进行更深入的思考，从而持续提供更优质的答案。

## 新特性
5.2 版本的新增特性涵盖：新增 `xhigh` 推理级别、新增简明的推理摘要，以及采用压缩技术的新型上下文管理机制。

### 降低推理难度 (Lower Reasoning Effort)
在 GPT-5.2 中，最低设置 `none` 可提供更低延迟的交互体验，这也是系统的默认配置。若需更深入的思考，可逐步调高至 `medium`，并根据效果进行调整。

在推理等级设为 `none` 的情况下，提示的作用尤为关键。为提升模型的推理质量，即便使用默认设置，也应鼓励模型先"思考"或列出步骤，再给出答案。
::: code-group
```python [SDK]
import json
from openai import OpenAI

client = OpenAI(
    # 🔐 DMXAPI 密钥 (请替换为您自己的密钥)
    # 获取方式: 登录 DMXAPI 官网 -> 个人中心 -> API 密钥管理
    api_key="sk-***************************************",

    # 🌐 DMXAPI 服务端点地址
    # 所有 API 请求都将发送到此基础 URL
    base_url="https://www.dmxapi.cn/v1",
    )

response = client.responses.create(
    model="gpt-5.2",
    input="您好！",
    reasoning={
        "effort": "none"
    }
)

# 将响应转换为 JSON 格式并格式化输出
response_dict = response.model_dump()
print(json.dumps(response_dict, indent=2, ensure_ascii=False))
```
```python [responses]
"""
功能描述：DMXAPI GPT-5.2 接口测试脚本
说明：演示如何调用 DMXAPI 的 responses 端点进行 AI 对话
"""

# 导入请求库和 JSON 处理库
import requests
import json

# API 端点地址
url = "https://www.dmxapi.cn/v1/responses"

# 请求头配置：包含认证信息和内容类型
headers = {
    "Authorization": "sk-***************************************",  # API 密钥
    "Content-Type": "application/json"  # 内容类型为 JSON
}

# 请求体：包含模型、输入和推理配置
data = {
    "model": "gpt-5.2",        # 使用的模型名称
    "input": "您好?",          # 用户输入内容
    "reasoning": {
        "effort": "none"       # 推理强度设置：none 表示不进行深度推理
    }
}

# 发送 POST 请求到 API 端点
response = requests.post(url, headers=headers, json=data)

# 格式化输出响应结果（支持中文显示）
print(json.dumps(response.json(), indent=2, ensure_ascii=False))

```
```python [chat completions]
"""
╔════════════════════════════════════════════════════════════════╗
║                    OpenAI API 调用示例                          ║
║                    使用 GPT-5.2 模型                            ║
╚════════════════════════════════════════════════════════════════╝
"""

import json
import requests

# ═══════════════════════════════════════════════════════════════
#                          API 配置
# ═══════════════════════════════════════════════════════════════

# API 请求地址
API_URL = "https://www.dmxapi.cn/v1/chat/completions"

# 从环境变量获取 API 密钥
API_KEY = "sk-***************************************"

# ═══════════════════════════════════════════════════════════════
#                          请求头配置
# ═══════════════════════════════════════════════════════════════

headers = {
    "Authorization": f"{API_KEY}",  # 身份认证
    "Content-Type": "application/json"      # 指定内容类型为 JSON
}

# ═══════════════════════════════════════════════════════════════
#                          请求体配置
# ═══════════════════════════════════════════════════════════════

payload = {
    "model": "gpt-5.2",           # 使用的模型名称
    "messages": [
        {
            "role": "user",       # 消息角色：用户
            "content": "您好?"
        }
    ],
    "reasoning_effort": "none"    # 推理强度设置
}

# ═══════════════════════════════════════════════════════════════
#                          发送请求
# ═══════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("正在发送请求到 OpenAI API...")
    print("-" * 60)

    try:
        # 发送 POST 请求
        response = requests.post(
            url=API_URL,
            headers=headers,
            json=payload
        )

        # 解析响应 JSON
        result = response.json()

        # 格式化输出 JSON（缩进4空格，确保中文正常显示）
        formatted_json = json.dumps(
            result,
            indent=4,
            ensure_ascii=False
        )

        print("响应结果：")
        print("-" * 60)
        print(formatted_json)

    except requests.exceptions.RequestException as e:
        # 处理网络请求异常
        print(f"请求失败: {e}")
    except json.JSONDecodeError as e:
        # 处理 JSON 解析异常
        print(f"JSON 解析失败: {e}")

```
:::

## 冗长度设置 (Verbosity)
在使用 GPT-5.2 生成代码时，`medium` 和 `high` 详细级别会输出结构更完整、解释更详尽的长代码，而 `low` 详细级别则生成更为简洁、注释极少的短代码。
::: code-group
```python [SDK]
import json
from openai import OpenAI
client = OpenAI(
    # 🔐 DMXAPI 密钥 (请替换为您自己的密钥)
    # 获取方式: 登录 DMXAPI 官网 -> 个人中心 -> API 密钥管理
    api_key="sk-***************************************",

    # 🌐 DMXAPI 服务端点地址
    # 所有 API 请求都将发送到此基础 URL
    base_url="https://www.dmxapi.cn/v1"
    )

response = client.responses.create(
    model="gpt-5",
    input="您好?",
    text={
        "verbosity": "low"
    }
)

print(json.dumps(response.model_dump() if hasattr(response, 'model_dump') else response.dict(), indent=2, ensure_ascii=False))
```
```python [responses]
"""
功能描述：DMXAPI GPT-5.2 接口测试脚本
说明：演示如何调用 DMXAPI 的 responses 端点进行 AI 对话
"""

# 导入请求库和 JSON 处理库
import requests
import json

# API 端点地址
url = "https://www.dmxapi.cn/v1/responses"

# 请求头配置：包含认证信息和内容类型
headers = {
    "Authorization": "sk-***************************************",  # API 密钥
    "Content-Type": "application/json"  # 内容类型为 JSON
}

# 请求体：包含模型、输入和推理配置
data = {
    "model": "gpt-5.2",        # 使用的模型名称
    "input": "您好?",          # 用户输入内容
    "text": {
    "verbosity": "low"
  }
}

# 发送 POST 请求到 API 端点
response = requests.post(url, headers=headers, json=data)

# 格式化输出响应结果（支持中文显示）
print(json.dumps(response.json(), indent=2, ensure_ascii=False))
```
```python [chat completions]
"""
╔════════════════════════════════════════════════════════════════╗
║                    OpenAI API 调用示例                          ║
║                    使用 GPT-5.2 模型                            ║
╚════════════════════════════════════════════════════════════════╝
"""

import json
import requests

# ═══════════════════════════════════════════════════════════════
#                          API 配置
# ═══════════════════════════════════════════════════════════════

# API 请求地址
API_URL = "https://www.dmxapi.cn/v1/chat/completions"

# 从环境变量获取 API 密钥
API_KEY = "sk-***************************************"

# ═══════════════════════════════════════════════════════════════
#                          请求头配置
# ═══════════════════════════════════════════════════════════════

headers = {
    "Authorization": f"{API_KEY}",  # 身份认证
    "Content-Type": "application/json"      # 指定内容类型为 JSON
}

# ═══════════════════════════════════════════════════════════════
#                          请求体配置
# ═══════════════════════════════════════════════════════════════

payload = {
    "model": "gpt-5.2",           # 使用的模型名称
    "messages": [
        {
            "role": "user",       # 消息角色：用户
            "content": "您好?"
        }
    ],
    "verbosity": "low"    # 推理强度设置
}

# ═══════════════════════════════════════════════════════════════
#                          发送请求
# ═══════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("正在发送请求到 OpenAI API...")
    print("-" * 60)

    try:
        # 发送 POST 请求
        response = requests.post(
            url=API_URL,
            headers=headers,
            json=payload
        )

        # 解析响应 JSON
        result = response.json()

        # 格式化输出 JSON（缩进4空格，确保中文正常显示）
        formatted_json = json.dumps(
            result,
            indent=4,
            ensure_ascii=False
        )

        print("响应结果：")
        print("-" * 60)
        print(formatted_json)

    except requests.exceptions.RequestException as e:
        # 处理网络请求异常
        print(f"请求失败: {e}")
    except json.JSONDecodeError as e:
        # 处理 JSON 解析异常
        print(f"JSON 解析失败: {e}")
```
:::

## 自定义工具
GPT-5 模型系列发布时，openai推出了名为“自定义工具”的新功能，它支持模型以任意原始文本作为工具调用的输入，同时可按需对输出进行约束。这一工具特性在 GPT-5.2 中得以延续。
::: code-group
```python [responses]
"""
功能描述：DMXAPI GPT-5.2 接口测试脚本
说明：演示如何调用 DMXAPI 的 responses 端点进行 AI 对话
"""

# 导入请求库和 JSON 处理库
import requests
import json

# API 端点地址
url = "https://www.dmxapi.cn/v1/responses"

# 请求头配置：包含认证信息和内容类型
headers = {
    "Authorization": "sk-***************************************",  # API 密钥
    "Content-Type": "application/json"  # 内容类型为 JSON
}

# 请求体：包含模型、输入和推理配置
data = {
    "model": "gpt-5.2",        # 使用的模型名称
    "input": "您好?",          # 用户输入内容
    "tools": [
        {
        "type": "custom",
        "name": "code_exec",
        "description": "Executes arbitrary python code"
        }
    ]
}

# 发送 POST 请求到 API 端点
response = requests.post(url, headers=headers, json=data)

# 格式化输出响应结果（支持中文显示）
print(json.dumps(response.json(), indent=2, ensure_ascii=False))
```
```python [chat completions]
"""
╔════════════════════════════════════════════════════════════════╗
║                    OpenAI API 调用示例                          ║
║                    使用 GPT-5.2 模型                            ║
╚════════════════════════════════════════════════════════════════╝
"""

import json
import requests

# ═══════════════════════════════════════════════════════════════
#                          API 配置
# ═══════════════════════════════════════════════════════════════

# API 请求地址
API_URL = "https://www.dmxapi.cn/v1/chat/completions"

# 从环境变量获取 API 密钥
API_KEY = "sk-***************************************"

# ═══════════════════════════════════════════════════════════════
#                          请求头配置
# ═══════════════════════════════════════════════════════════════

headers = {
    "Authorization": f"{API_KEY}",  # 身份认证
    "Content-Type": "application/json"      # 指定内容类型为 JSON
}

# ═══════════════════════════════════════════════════════════════
#                          请求体配置
# ═══════════════════════════════════════════════════════════════

payload = {
    "model": "gpt-5.2",           # 使用的模型名称
    "messages": [
        {
            "role": "user",       # 消息角色：用户
            "content": "您好?"
        }
    ],
    "tools": [
    {
      "type": "custom",
      "custom": {
        "name": "code_exec",
        "description": "Executes arbitrary python code"
      }
    }
  ]
}

# ═══════════════════════════════════════════════════════════════
#                          发送请求
# ═══════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("正在发送请求到 OpenAI API...")
    print("-" * 60)

    try:
        # 发送 POST 请求
        response = requests.post(
            url=API_URL,
            headers=headers,
            json=payload
        )

        # 解析响应 JSON
        result = response.json()

        # 格式化输出 JSON（缩进4空格，确保中文正常显示）
        formatted_json = json.dumps(
            result,
            indent=4,
            ensure_ascii=False
        )

        print("响应结果：")
        print("-" * 60)
        print(formatted_json)

    except requests.exceptions.RequestException as e:
        # 处理网络请求异常
        print(f"请求失败: {e}")
    except json.JSONDecodeError as e:
        # 处理 JSON 解析异常
        print(f"JSON 解析失败: {e}")
```
:::
## GPT-5.2 参数兼容性
以下参数仅在使用 GPT-5.2 且推理等级设置为 `none` 时支持：

- `temperature`
- `top_p`
- `logprobs`

若对 GPT-5.2 或 GPT-5.1 使用其他推理强度设置，或对包含这些字段的旧版 GPT-5 模型（如 `gpt-5`、`gpt-5-mini`、`gpt-5-nano`）发起请求，系统将返回错误。
若想通过提高推理强度或改用其他 GPT-5 系列模型来获得类似效果，可尝试以下替代参数：

- **推理深度**：`reasoning: { effort: "none" | "low" | "medium" | "high" | "xhigh" }`
- **输出详细程度**：`text: { verbosity: "low" | "medium" | "high" }`
- **输出长度**：`max_output_tokens`
