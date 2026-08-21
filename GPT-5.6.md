# GPT-5.6 Sol 使用指南

`gpt-5.6-sol` 是 OpenAI 的前沿模型，面向专业知识工作、复杂推理、编码和代理任务。本指南区分两类信息：OpenAI 官方公布的上游能力，以及本次通过 DMXAPI 兼容代理实际验证的调用能力。

:::warning API 密钥安全
示例令牌全部是不可用占位符。真实 DMXAPI 令牌只能保存在服务端环境变量或密钥管理系统中，不要写入文档、前端代码、公开仓库或日志。
:::

## 接口地址

| 接口 | 请求方式 | URL |
|------|---------|-----|
| Responses API | POST | `https://www.dmxapi.cn/v1/responses` |
| Chat Completions API | POST | `https://www.dmxapi.cn/v1/chat/completions` |

Responses API 适合推理、工具、多轮与新项目，优先推荐；Chat Completions API 适合兼容现有项目。

## 模型名称

DMXAPI 文档和示例统一显式使用：

```text
gpt-5.6-sol
```

OpenAI 上游的 `gpt-5.6` 别名会路由到 GPT-5.6 Sol；通过 DMXAPI 调用时，建议使用本页已经实测的完整名称 `gpt-5.6-sol`。

## Responses API 请求示例

::: code-group

```python [Responses SDK]
from openai import OpenAI


client = OpenAI(
    api_key="sk-***************************************",
    base_url="https://www.dmxapi.cn/v1",
)

response = client.responses.create(
    model="gpt-5.6-sol",
    input="请用三句话解释量子纠缠。",
    reasoning={"effort": "none"},
    max_output_tokens=512,
)
print(response.output_text)
```

```python [Responses requests]
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
        "reasoning": {"effort": "none"},
        "max_output_tokens": 512,
    },
    timeout=120,
)
response.raise_for_status()
print(response.json())
```

:::

## Responses API 返回示例

Responses API 返回 `response` 对象；示例 ID 为合成值：

```json
{
  "id": "resp_example_gpt56_quickstart_001",
  "object": "response",
  "status": "completed",
  "model": "gpt-5.6-sol",
  "output": [
    {
      "id": "msg_example_gpt56_quickstart_001",
      "type": "message",
      "status": "completed",
      "role": "assistant",
      "content": [
        {
          "type": "output_text",
          "text": "量子纠缠描述了多个粒子之间不可独立分割的量子关联。",
          "annotations": []
        }
      ]
    }
  ]
}
```

## Chat Completions API 请求示例

```python
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
            {"role": "user", "content": "请用三句话解释量子纠缠。"}
        ],
        "reasoning_effort": "none",
        "max_completion_tokens": 512,
    },
    timeout=120,
)
response.raise_for_status()
print(response.json())
```

## Chat Completions API 返回示例

Chat Completions 可能返回带日期的模型快照名；示例 ID 为合成值：

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

## 官方规格

以下规格来自 OpenAI 官方模型页：

| 项目 | GPT-5.6 Sol |
|------|-------------|
| 上下文窗口 | 1,050,000 tokens |
| 最大输出 | 128,000 tokens |
| 知识截止日期 | 2026-02-16 |
| 输入 | 文本、图片 |
| 输出 | 文本 |
| API | Responses、Chat Completions |
| 支持 | 流式、函数调用、结构化输出 |
| 不支持 | 微调 |

官方资料：

- [GPT-5.6 Sol 模型页](https://developers.openai.com/api/docs/models/gpt-5.6-sol)
- [最新模型使用指南](https://developers.openai.com/api/docs/guides/latest-model)

## 推理强度

GPT-5.6 Sol 支持六档推理强度：

| 强度 | 典型用途 |
|------|---------|
| `none` | 简单聊天、抽取、格式转换和低延迟任务 |
| `low` | 轻量分析与常规代码修改 |
| `medium` | 默认值，兼顾质量与延迟 |
| `high` | 复杂分析、规划和调试 |
| `xhigh` | 高难度、多约束问题 |
| `max` | 需要最大推理预算的任务 |

Responses API 使用嵌套对象，Chat Completions 使用顶层字段：

```json
{
  "reasoning": {
    "effort": "high",
    "summary": "auto"
  }
}
```

```json
{
  "reasoning_effort": "high"
}
```

本仓库的基础示例显式设置 `none`，便于控制简单任务的延迟。不要把它误认为模型默认值；OpenAI 官方默认值是 `medium`。迁移现有任务时，应先保留旧任务的推理强度，再分别测试同档和低一档的质量、延迟与成本。

## 输出详细程度

Responses API 可通过 `text.verbosity` 控制回答详细程度：

```python
response = client.responses.create(
    model="gpt-5.6-sol",
    input="解释这个 Python 函数的性能瓶颈。",
    reasoning={"effort": "medium"},
    text={"verbosity": "low"},
)
```

可选值为 `low`、`medium` 和 `high`。它控制答案展开程度，不等同于推理强度。本字段已使用 `low` 通过 DMXAPI 定点实测。

## 为什么优先使用 Responses API

OpenAI 官方建议推理、工具调用和多轮工作流优先使用 Responses API。它把消息、推理项、函数调用和其他输出组织在统一的 `output` 数组中，也更适合传递先前响应状态。

Chat Completions 仍受支持，适合对现有项目做低风险迁移。DMXAPI 实测中，Chat 和 Responses 都可能返回带日期或网关前缀的规范化模型名；业务逻辑不应依赖返回模型名必须与请求字符串完全相同。

## 图片、文件和工具

本次 DMXAPI 实测确认以下路径可用：

- 网络图片 URL 与 Base64 Data URL 输入；
- 公开文件 URL 分析；
- Chat Completions 和 Responses 的函数调用；
- 流式文本输出；
- Chat 多轮上下文；
- Responses 推理摘要。

GPT-5.6 Sol 上游还支持图片的 `original` 细节级别，适合需要保留原始分辨率信息的视觉任务。此参数尚未在 DMXAPI 本轮验证矩阵中单独测试，生产使用前应先做小流量验证。

## OpenAI 上游新增能力

以下能力由 OpenAI 官方公布，但本轮没有通过 DMXAPI 逐项验证。它们不应被当作 DMXAPI 当前兼容性承诺：

| 能力 | 上游说明 | DMXAPI 状态 |
|------|---------|-------------|
| Pro 模式 | `reasoning.mode: "pro"`，面向最高质量任务 | 未验证 |
| 持久化推理上下文 | 使用 `reasoning.context` 延续推理状态 | 未验证 |
| 显式提示缓存 | 使用 `prompt_cache_options` 控制缓存 | 未验证 |
| PTC | 程序化工具调用能力 | 未验证 |
| Multi-agent | 多代理能力，官方标记为 beta | 未验证 |

OpenAI 官方说明显式提示缓存的写入价格按相应输入价格的 1.25 倍计算。价格和兼容性可能变化，使用前应查看官方最新模型指南和 DMXAPI 当前计费说明。

## 迁移建议

从旧模型迁移时，建议按以下顺序进行：

1. 只替换模型名为 `gpt-5.6-sol`，保留现有接口、提示词和推理强度。
2. 建立一组固定评测样本，对比正确率、格式稳定性、延迟和 token 用量。
3. 在质量达标后，测试同一推理强度和低一档强度，选择更合适的成本与延迟。
4. 删除提示词中为旧模型补充的重复步骤、过度强调和互相冲突的约束。
5. 新工作流优先迁移到 Responses API，再逐步启用工具、缓存或持久化推理能力。

## 本次 DMXAPI 验证结果

验证日期：2026-08-21。

| 接口能力 | 结果 |
|----------|------|
| Chat 非流式与 SDK | 通过 |
| Chat 流式 | 通过；需兼容 `choices: []` 的元数据块 |
| Chat 结构化 JSON | 通过 |
| Chat 网络图片与本地图片 | 通过 |
| Chat 函数调用 | 通过；省略或显式传入 `reasoning_effort: none` 均可 |
| Chat 多轮上下文 | 通过 |
| Responses 非流式与 SDK | 通过 |
| Responses 流式 | 通过 |
| Responses 网络图片、本地图片和文件 | 通过 |
| Responses 函数调用 | 通过 |
| Responses 推理项与摘要 | 推理项通过；`summary` 可能为空 |

测试结果只代表验证时的 DMXAPI 服务状态。上线前仍应使用你自己的输入、超时、错误处理和配额进行回归测试。

<p align="center">
  <small>© 2026 DMXAPI GPT-5.6 Sol 使用指南</small>
</p>
