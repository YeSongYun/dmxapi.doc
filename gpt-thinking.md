# GPT-5.6 Sol 推理摘要

本页演示通过 DMXAPI 兼容代理请求 `gpt-5.6-sol` 的推理摘要。`reasoning.summary` 返回的是模型生成的摘要，不是完整、逐字的内部思维链。

## 🔗 请求地址

```text
https://www.dmxapi.cn/v1/responses
```

:::warning API 密钥安全
示例令牌为不可用占位符。请妥善保管真实 DMXAPI 令牌，不要在公开仓库或日志中泄露。
:::

## 模型与参数

- 模型：`gpt-5.6-sol`
- 推理强度：`none`、`low`、`medium`、`high`、`xhigh`、`max`
- 默认推理强度：`medium`
- 推理摘要：`reasoning.summary` 设置为 `auto`

## 请求示例

::: code-group

```python [SDK]
# ============================================================
#  GPT-5 深度思考模式调用示例（SDK 版）
#  功能：通过 OpenAI Python SDK 调用 Responses API
# ============================================================

from openai import OpenAI

# ---------- 初始化客户端 ----------
client = OpenAI(
    api_key="sk-*****************************",
    base_url="https://www.dmxapi.cn/v1"
)

# ---------- 发送请求 ----------
response = client.responses.create(
    model="gpt-5.6-sol",                        # 使用的模型
    input="一加到十最复杂的方法",  # 用户输入的问题
    reasoning={
        "effort": "low",                  # 思考等级
        "summary": "auto"                 # 思考摘要：auto 自动返回思考过程
    }
)

# ---------- 输出结果 ----------
# 遍历 output 列表，分别提取「思考内容」和「响应结果」
for item in response.output:
    if item.type == "reasoning":
        print("【思考内容】")
        for content in item.summary:
            print(content.text)
        print()
    elif item.type == "message":
        print("【响应结果】")
        for content in item.content:
            print(content.text)

```

```python [requests]
# ============================================================
#  GPT-5 深度思考模式调用示例
#  功能：调用 OpenAI Responses API，获取模型的思考过程与最终回答
# ============================================================

import requests
import json
import sys
import io

# ---------- 终端编码设置 ----------
# 解决 Windows 终端输出中文乱码问题
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# ---------- API 配置 ----------
url = "https://www.dmxapi.cn/v1/responses"
api_key = "sk-*****************************"

headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {api_key}"
}

# ---------- 请求参数 ----------
data = {
    "model": "gpt-5.6-sol",                    # 使用的模型
    "input": "一加到十最复杂的方法",        # 用户输入的问题
    "reasoning": {
        "effort": "low",                  # 思考等级
        "summary": "auto"                 # 思考摘要：auto 自动返回思考过程
    }
}

# ---------- 发送请求 ----------·
response = requests.post(url, headers=headers, json=data)
result = response.json()

# ---------- 解析并输出结果 ----------
# 遍历 output 列表，分别提取「思考内容」和「响应结果」
for item in result.get("output", []):
    if item.get("type") == "reasoning":
        print("【思考内容】")
        for content in item.get("summary", []):
            print(content.get("text", ""))
        print()
    elif item.get("type") == "message":
        print("【响应结果】")
        for content in item.get("content", []):
            print(content.get("text", ""))


```

```shell [cURL]
curl -X POST https://www.dmxapi.cn/v1/responses \
  -H "Content-Type: application/json" \
  -H "Authorization: sk-***************************************" \
  -d '{
    "model": "gpt-5.6-sol",
    "input": "比较归并排序和快速排序，并说明各自更适合的场景。",
    "reasoning": {"effort": "low", "summary": "auto"}
  }'
```

:::

## 返回示例

```json
{
  "id": "resp_example_gpt56_reasoning_001",
  "object": "response",
  "status": "completed",
  "model": "gpt-5.6-sol",
  "output": [
    {
      "id": "rs_example_gpt56_reasoning_001",
      "type": "reasoning",
      "summary": [
        {
          "type": "summary_text",
          "text": "比较两种算法的时间复杂度、稳定性、额外空间与典型使用场景。"
        }
      ]
    },
    {
      "id": "msg_example_gpt56_reasoning_001",
      "type": "message",
      "status": "completed",
      "role": "assistant",
      "content": [
        {
          "type": "output_text",
          "text": "归并排序稳定且最坏时间复杂度为 O(n log n)，适合外部排序和要求稳定性的场景；快速排序通常原地且平均性能优秀，适合内存中的通用排序。",
          "annotations": []
        }
      ]
    }
  ]
}
```

## 注意事项
<p align="center">
  <small>© 2026 DMXAPI GPT-5.6 Sol 推理摘要</small>
</p>
