# GPT-5.1 使用指南

## 请求地址

```
https://www.dmxapi.cn/v1/responses
```

:::tip 重要提示
GPT-5.1 系列模型只能通过 `responses` 接口调用
:::

## 模型列表

- `gpt-5.1` - 标准版本
- `gpt-5.1-chat` - 对话优化版本
- `gpt-5.1-codex` - 代码生成版本
- `gpt-5.1-codex-mini` - 轻量级代码版本

## 快速入门

GPT-5.1 新增了推理模式选项 `none`，适用于低延迟交互场景。系统默认将 GPT-5.1 的推理模式设置为 `none`。

### 示例代码

```python
"""
DMXAPI GPT-5.1 API 调用示例
====================
本脚本演示如何使用 OpenAI sdk调用 DMX API 服务
支持的模型：gpt-5.1
"""

from openai import OpenAI

# ============================================================
# API 配置
# ============================================================
# 你的 DMX API 密钥，用于身份验证
api_key = "sk-*******************************************"

# DMX API 服务的基础 URL 地址
base_url = "https://www.dmxapi.cn/v1"

# ============================================================
# 初始化客户端
# ============================================================
# 创建 OpenAI 客户端实例，配置 API 密钥和服务地址
client = OpenAI(
    api_key=api_key,      # API 认证密钥
    base_url=base_url     # API 服务端点
)

# ============================================================
# 发送请求
# ============================================================
# 调用 responses.create 方法创建一个响应
result = client.responses.create(
    model="gpt-5.1",                    # 使用的模型版本
    input="早上好",                      # 输入的提示文本
    reasoning={"effort": "none"},       # 推理配置：低推理程度
)

# ============================================================
# 输出结果
# ============================================================
# 打印 API 返回的文本内容
print(result.output_text)
```

### 返回示例

```json
早上好呀！🙂
今天有什么想聊的或需要我帮忙的吗？
```

## 新特性

与 GPT-5 类似，新一代 GPT-5.1 的 API 功能包括：
- 自定义工具
- 调节输出详细度与推理过程的参数
- 允许使用的工具列表

**5.1 版本亮点**：新增了推理强度 `none` 调控选项，进一步提升了模型的可操控性，并针对编程场景新增了两项实用工具。

### 推理强度控制

`reasoning.effort` 参数用于控制模型在输出回答前生成的推理标记数量。早期的推理模型（例如 o3）仅支持 `low`、`medium` 和 `high` 三种模式：
- **low**：侧重响应速度和较少标记消耗
- **high**：追求更深入的推理过程

在 **GPT-5.1** 版本中，最低响应档位现已调整为 `none`，以实现更低延迟的交互体验，此设置也是系统的默认选项。若需更充分的思考过程，可逐步提升至 `medium` 档位并观察输出效果。

:::warning 注意
请注意区分 GPT-5.1 的 `none` 推理档位与 GPT-5 版本中 `minimal` 推理档位及 `medium` 默认档位的差异。
:::

**最佳实践**：在推理强度设为 `none` 的情况下，提示设计尤为关键。即便使用默认设置，为提升模型的推理质量，也应引导其养成先"思考"或梳理步骤再作答的习惯。

### 输出详细程度

详细程度（verbosity）决定了生成的输出标记数量。减少标记数能够降低整体延迟。尽管模型的推理思路基本不变，但模型会采用更简洁的回答方式——具体效果取决于实际使用场景，可能提升也可能降低回答质量。

#### 使用场景

- **高详细程度模式（high）**：适用于需要模型对文档进行详细阐释或执行全面代码重构的场景
- **低详细度模式（low）**：适用于需要简短回复或基础代码生成的场景，例如 SQL 查询语句编写

#### 配置说明

GPT-5 已将该选项设置为可配置项，可选值为 `high`、`medium` 或 `low`。在 GPT-5.1 版本中，详细程度仍保持可配置，且默认设置为 `medium`。

生成代码时：
- `medium` 和 `high` 详细级别会输出结构更完整、带有行内注释的长代码
- `low` 详细级别则生成更为精简、注释极少的短代码

#### 示例代码

```python
"""
DMXAPI GPT-5.1 模型调用示例脚本

本脚本演示如何使用 OpenAI SDK 调用 dmxapi 平台的 GPT-5.1 模型。
主要功能：发送问题并获取模型的响应结果。
"""

from openai import OpenAI
import json
# ============================================================================
# DMXAPI 配置部分
# ============================================================================
# 在这里填写你的 DMXAPI 配置信息
api_key = "sk-*******************************************"  # 你的 DMXAPI Key
base_url = "https://www.dmxapi.cn/v1"  # dmxapi 的 DMXAPI 基础地址

# ============================================================================
# 初始化客户端
# ============================================================================
# 使用提供的 API Key 和 base_url 创建 OpenAI 客户端实例
client = OpenAI(
    api_key=api_key,
    base_url=base_url
)

# ============================================================================
# 调用模型并获取响应
# ============================================================================
# 使用 responses.create 方法调用 GPT-5.1 模型
# model: 指定使用的模型名称
# input: 用户提出的问题或提示词
# text.verbosity: 控制输出的详细程度，可选值为 "low"（简洁）或 "high"（详细）
response = client.responses.create(
    model="gpt-5.1",
    input="生命的意义是什么?",
    text={
        "verbosity": "low"  # 使用简洁模式输出
    }
)

# ============================================================================
# 输出结果
# ============================================================================
# 将响应对象转换为字典并格式化输出
# indent=2: 使用 2 个空格缩进，提高可读性
# ensure_ascii=False: 正确显示中文字符，不转义为 Unicode
print(json.dumps(response.model_dump(), indent=2, ensure_ascii=False))
```

#### 返回示例
```json
{
  "id": "resp_08558b7c8c274c3900691ac28d31348194bdf49cd9bddb390f",
  "created_at": 1763361421.0,
  "error": null,
  "incomplete_details": null,
  "instructions": null,
  "metadata": {},
  "model": "gpt-5.1",
  "object": "response",
  "output": [
    {
      "id": "rs_08558b7c8c274c3900691ac28d76808194bb33748ba321ccff",
      "summary": [],
      "type": "reasoning",
      "content": null,
      "encrypted_content": null,
      "status": null
    },
    {
      "id": "msg_08558b7c8c274c3900691ac28d7fd0819490c845bffa43af6d",
      "content": [
        {
          "annotations": [],
          "text": "这个问题没有唯一标准答案，只能由你自己在生活中慢慢“活出来”。但人类历史上常见的几个方向是：\n\n1）关系：去爱与被爱，和家人、朋友、伴侣、社会建立真诚的连接。  \n2）成长：让自己在能力、见识、心性上持续进步，成为更好的自己。  \n3）贡献：用自己的方式对他人或世界有一点点帮助，比如工作、创作、服务、善举。  \n4）体验：认真地活一次，感受世界的美好与苦难，尝试你真正在意的事物。  \n5）自由与真实：逐渐摆脱外界单一标准的束缚，更真实地过自己认同的人生。\n\n简单说：  \n- 没有“统一答案”的意义；  \n- 你可以自己“制造意义”：在你愿意投入时间和心力的事情里；  \n- 当你觉得迷茫时，从小事开始：照顾好身体，维持几段真诚的关系，做一件对别人有益的小事，坚持一项能让你成长的练习。\n\n如果你愿意说说你现在所处的状态（年龄、困惑的重点，比如工作/学习/感情），我可以帮你一起更具体地梳理属于你的“意义线索”。",
          "type": "output_text",
          "logprobs": []
        }
      ],
      "role": "assistant",
      "status": "completed",
      "type": "message"
    }
  ],
  "parallel_tool_calls": true,
  "temperature": 1.0,
  "tool_choice": "auto",
  "tools": [],
  "top_p": 1.0,
  "background": false,
  "conversation": null,
  "max_output_tokens": null,
  "max_tool_calls": null,
  "previous_response_id": null,
  "prompt": null,
  "prompt_cache_key": null,
  "reasoning": {
    "effort": "none",
    "generate_summary": null,
    "summary": null
  },
  "safety_identifier": null,
  "service_tier": "default",
  "status": "completed",
  "text": {
    "format": {
      "type": "text"
    },
    "verbosity": "low"
  },
  "top_logprobs": 0,
  "truncation": "disabled",
  "usage": {
    "input_tokens": 11,
    "input_tokens_details": {
      "cached_tokens": 0
    },
    "output_tokens": 307,
    "output_tokens_details": {
      "reasoning_tokens": 0
    },
    "total_tokens": 318
  },
  "user": null,
  "content_filters": null,
  "store": true
}
```

## 参数兼容性

:::warning 重要提示
使用 GPT-5.1 系列模型时（如 `gpt-5.1`、`gpt-5.1-chat`、`gpt-5.1-codex` 等），以下参数**不被支持**：

- `temperature`
- `top_p`
- `logprobs`

含有这些字段的请求将会报错。
:::

### 推荐参数

请改用以下专用于 GPT-5 模型系列的控制选项：

| 参数 | 说明 | 可选值 |
|------|------|--------|
| `reasoning.effort` | 推理深度等级 | `none` \| `low` \| `medium` \| `high` |
| `text.verbosity` | 输出详细级别 | `low` \| `medium` \| `high` |
| `max_output_tokens` | 输出长度限制 | 正整数 |

---

<p align="center">
  <small>© 2025 DMXAPI GPT-5.1</small>
</p>