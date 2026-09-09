# GPT-5.6 专题：Sol、Terra 与 Luna

GPT-5.6 系列包含 `gpt-5.6-sol`、`gpt-5.6-terra` 和 `gpt-5.6-luna` 三个模型。本专题以 Microsoft Foundry 官方 GPT-5.6 模型表和推理模型文档为主要规格来源，并结合 OpenAI 官方模型指南说明三档定位。

:::warning API 密钥安全
示例令牌全部是不可用占位符。真实 DMXAPI 令牌只能保存在服务端环境变量或密钥管理系统中，不要写入文档、前端代码、公开仓库或日志。
:::

## 三个模型怎么选

三个模型使用相同的 GPT-5.6 接口能力，主要区别是质量、成本与吞吐量定位：

| 模型 | 官方定位 | 适合场景 |
|------|----------|----------|
| `gpt-5.6-sol` | 前沿能力档 | 高难度专业工作、复杂推理、编码与代理任务 |
| `gpt-5.6-terra` | 智能与成本平衡档 | 日常生产工作流、批量分析、兼顾质量与成本 |
| `gpt-5.6-luna` | 高效率档 | 高并发、低成本、大批量处理 |

OpenAI 官方还提供 `gpt-5.6` 别名，该别名会路由到 `gpt-5.6-sol`。通过 DMXAPI 调用时，建议显式填写需要的完整模型名称，避免业务代码依赖别名的后续路由变化。

## Microsoft Foundry 官方规格

Microsoft Foundry 当前将三款模型列为同一组能力规格：

| 项目 | `gpt-5.6-sol` | `gpt-5.6-terra` | `gpt-5.6-luna` |
|------|---------------|-----------------|----------------|
| Microsoft 模型版本 | 2026-07-09 | 2026-07-09 | 2026-07-09 |
| 总上下文窗口 | 1,050,000 tokens | 1,050,000 tokens | 1,050,000 tokens |
| 输入上限 | 922,000 tokens | 922,000 tokens | 922,000 tokens |
| 最大输出 | 128,000 tokens | 128,000 tokens | 128,000 tokens |
| 训练数据截至 | 2026 年 6 月 | 2026 年 6 月 | 2026 年 6 月 |
| 输入与输出 | 文本、图片输入；文本输出 | 文本、图片输入；文本输出 | 文本、图片输入；文本输出 |
| API | Responses、Chat Completions | Responses、Chat Completions | Responses、Chat Completions |
| 能力 | 推理、结构化输出、函数/工具、并行工具调用、流式、Computer use | 同左 | 同左 |

`128,000` 是最大输出上限，不代表每次请求都会预留这么多可见输出。输入、可见输出和推理 token 会共同占用可用预算；长输入或较高推理强度会减少剩余生成空间。生产环境应同时检查响应状态、结束原因和 token 使用量。

## 🔗 请求地址

### Responses API

```text
https://www.dmxapi.cn/v1/responses
```

### Chat Completions API

```text
https://www.dmxapi.cn/v1/chat/completions
```

新项目、推理任务、工具调用和多轮工作流优先使用 Responses API。Chat Completions 适合兼容已有项目，但部分推理与工具组合受到限制。

## 推理强度控制

GPT-5.6 支持六档推理强度。推理等级越高，模型通常会投入更多推理 token，质量上限可能提高，但延迟与用量也会增加。

| 强度 | 推荐用途 | 选择建议 |
|------|----------|----------|
| `none` | 简单问答、抽取、分类、格式转换 | 最低延迟基线；不进行额外推理 |
| `low` | 轻量分析、常规代码修改 | 延迟敏感且需要少量推理时使用 |
| `medium` | 通用生产任务 | 官方默认值，建议作为首个评测基线 |
| `high` | 复杂分析、规划、调试 | 只有评测确认质量提升时再提高 |
| `xhigh` | 高难度、多约束问题 | 面向质量优先任务，关注延迟和 token |
| `max` | 最困难、需要充分探索与复核的任务 | 仅 GPT-5.6 Responses API；应与 `xhigh` 做对照评测 |

### 字段与端点规则

| 接口 | 参数写法 | 支持范围 | 重要限制 |
|------|----------|----------|----------|
| Responses API | `reasoning={"effort": "..."}` | `none`、`low`、`medium`、`high`、`xhigh`、`max` | 推荐用于推理与工具组合 |
| Chat Completions | `reasoning_effort="..."` | `none`、`low`、`medium`、`high`、`xhigh` | `max` 不适用于该接口 |

如果省略推理强度，GPT-5.6 默认使用 `medium`。Chat Completions 请求一旦携带 `tools`，必须显式设置 `reasoning_effort="none"`；即使省略该字段，也会因为默认 `medium` 而失败。需要模型先推理再调用工具时，应改用 Responses API。

### 按需添加的推理参数

完整调用示例默认不显式设置推理强度；只有业务需要覆盖默认 `medium` 时，才把对应片段加入请求。

::: code-group

```python [Responses SDK]
reasoning={"effort": "high"}
```

```json [Responses requests]
{
  "reasoning": {
    "effort": "high"
  }
}
```

```python [Chat Completions]
reasoning_effort="high"
```

:::

## Responses API 请求示例

下面的代码参考修改前的基础示例编写，只保留调用所需的模型与输入参数，不显式设置推理强度和最大输出。

::: code-group

```python [SDK]
from openai import OpenAI


client = OpenAI(
    api_key="sk-***************************************",
    base_url="https://www.dmxapi.cn/v1",
)

response = client.responses.create(
    model="gpt-5.6-sol",
    input="请用三句话解释量子纠缠。",
)

print(response.output_text)
```

```python [requests]
import json

import requests


response = requests.post(
    "https://www.dmxapi.cn/v1/responses",
    headers={
        "Authorization": "sk-***************************************",
        "Content-Type": "application/json",
    },
    json={
        "model": "gpt-5.6-sol",
        "input": "请用三句话解释量子纠缠。",
    },
    timeout=180,
)
response.raise_for_status()
print(json.dumps(response.json(), indent=2, ensure_ascii=False))
```

:::

## Responses API 返回示例

以下为结构示意，ID 为合成值；实际响应还可能包含推理项和用量字段：

```json
{
  "id": "resp_example_gpt56_quickstart_001",
  "object": "response",
  "status": "completed",
  "model": "gpt-5.6-sol-2026-07-09",
  "output": [
    {
      "type": "message",
      "role": "assistant",
      "content": [
        {
          "type": "output_text",
          "text": "量子纠缠描述了多个粒子之间不可独立分割的量子关联。"
        }
      ]
    }
  ]
}
```

## Chat Completions API 请求示例

本例同样沿用修改前的基础结构，不显式设置推理强度和最大输出：

```python
import json

import requests


response = requests.post(
    "https://www.dmxapi.cn/v1/chat/completions",
    headers={
        "Authorization": "sk-***************************************",
        "Content-Type": "application/json",
    },
    json={
        "model": "gpt-5.6-sol",
        "messages": [
            {
                "role": "user",
                "content": "请用三句话解释量子纠缠。",
            }
        ],
    },
    timeout=180,
)
response.raise_for_status()
print(json.dumps(response.json(), indent=2, ensure_ascii=False))
```

## Chat Completions 返回示例

```json
{
  "id": "chatcmpl_example_gpt56_quickstart_001",
  "object": "chat.completion",
  "model": "gpt-5.6-sol-2026-07-09",
  "choices": [
    {
      "index": 0,
      "message": {
        "role": "assistant",
        "content": "量子纠缠描述了多个粒子之间不可独立分割的量子关联。"
      },
      "finish_reason": "stop"
    }
  ]
}
```

## 工具调用注意事项

Microsoft 官方明确说明，GPT-5.6 在 Chat Completions 中不能同时使用工具与非 `none` 推理强度：

```json
{
  "reasoning_effort": "none",
  "tools": [
    {
      "type": "function",
      "function": {
        "name": "get_weather"
      }
    }
  ]
}
```

需要 `low` 到 `max` 推理强度并结合工具时，请使用 Responses API。这样还可以携带推理项处理后续回合。
<p align="center">
  <small>© 2026 DMXAPI GPT-5.6 专题</small>
</p>
