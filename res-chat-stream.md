# OpenAI Responses API 流式调用

本页演示通过 DMXAPI 兼容代理流式调用 `gpt-5.6-sol`，并处理 `response.output_text.delta` 事件。

## 🔗 请求地址

```text
https://www.dmxapi.cn/v1/responses
```

:::warning API 密钥安全
示例令牌为不可用占位符。请妥善保管真实 DMXAPI 令牌，不要写入公开仓库、前端代码或日志。
:::

## 模型名称

- `gpt-5.6-sol`

## Python 请求示例

::: code-group

```python [SDK]
"""
╔═══════════════════════════════════════════════════════════════╗
║                  DMXAPI GPT-5系列及其他模型调用示例             ║
╚═══════════════════════════════════════════════════════════════╝

📝 功能说明:
   本脚本演示如何使用 OpenAI SDK 调用 DMXAPI 的 GPT-5系列及其他模型
   通过 responses.create 接口进行对话交互（流式输出）

═══════════════════════════════════════════════════════════════
"""

from openai import OpenAI

# ═══════════════════════════════════════════════════════════════
# 🔑 步骤1: 初始化 DMXAPI 客户端
# ═══════════════════════════════════════════════════════════════

client = OpenAI(
    # 🔐 DMXAPI 密钥 (请替换为您自己的密钥)
    # 获取方式: 登录 DMXAPI 官网 -> 个人中心 -> API 密钥管理
    api_key="sk-**********************************",

    # 🌐 DMXAPI 服务端点地址
    # 所有 API 请求都将发送到此基础 URL
    base_url="https://www.dmxapi.cn/v1",
)

# ═══════════════════════════════════════════════════════════════
# 💬 步骤2: 创建流式对话请求
# ═══════════════════════════════════════════════════════════════

response = client.responses.create(
    # 🤖 模型选择
    # gpt-5.6-sol: GPT-5系列模型,支持高级推理,适用于复杂问题和深度分析
    model="gpt-5.6-sol",

    # 💭 用户输入
    # 您想要向模型提出的问题或对话内容
    # (gpt-5-codex 如果跑不通的话，需要改成结构化的数组格式)
    input="你好!",

    # 🔄 流式输出开关
    # True: 实时接收响应，边生成边输出
    stream=True,

    # ---------- 采样参数 ----------
    # 🌡️ 温度参数 (范围: 0.0 - 2.0)
    # 控制输出的随机性和创造性:
    #   • 较低值 (0.0-0.3): 输出更确定、更一致,适合事实性任务
    #   • 中等值 (0.4-0.8): 平衡创造性和一致性
    #   • 较高值 (0.9-2.0): 输出更随机、更有创意
    # ⚠️ 建议: 只调整 temperature 或 top_p 其中之一
    # temperature=1,

    # 🎯 核采样参数 (范围: 0.0 - 1.0)
    # 控制采样的概率质量阈值:
    #   • 0.1: 只考虑概率最高的 10% 的词
    #   • 0.5: 只考虑概率最高的 50% 的词
    #   • 1.0: 考虑所有可能的词
    # 💡 提示: 较低的值会让输出更集中,较高的值会增加多样性
    # ⚠️ 建议: 只调整 temperature 或 top_p 其中之一
    # top_p=1,

)

# ═══════════════════════════════════════════════════════════════
# 📤 步骤3: 处理流式响应
# ═══════════════════════════════════════════════════════════════

try:
    # 遍历流式响应事件
    for event in response:
        # 检查事件类型是否为文本增量输出
        if event.type == "response.output_text.delta":
            # 实时打印文本内容 - 不换行,立即刷新输出缓冲区
            print(event.delta, end="", flush=True)

except KeyboardInterrupt:
    # 处理用户中断 - 当用户按 Ctrl+C 时优雅退出
    print("\n\n⚠️ 用户中断了请求")

except Exception as e:
    # 处理其他异常 - 捕获并显示任何意外错误
    print(f"\n\n❌ 发生错误: {e}")

# 最后换行 - 确保输出格式整洁
print()
```

```python [requests]

import requests
import json

# ============================================================================
# 配置部分 - API 连接信息
# ============================================================================

# DMXAPI 的 URL 地址
url = "https://www.dmxapi.cn/v1/responses"

# API 密钥 - 用于身份验证和访问控制
api_key = "sk-**************************************"  # ⚠️ 请替换为你的API密钥

# ============================================================================
# 请求头配置 - 设置内容类型和授权信息
# ============================================================================
headers = {
    "Content-Type": "application/json",      # 指定请求体为 JSON 格式
    "Authorization": f"{api_key}",    # token 认证方式
}

# ============================================================================
# 请求参数配置 - AI 模型与输入内容
# ============================================================================
data = {
    # ---------- 基础配置 ----------
    "model": "gpt-5.6-sol",    # 指定使用的 AI 模型版本
    "input": "你好",          # 发送给 AI 的问题或指令
    "stream": True,          # 启用流式输出 - 实时接收响应而不是等待完整回复

}

# ============================================================================
# 发送请求并处理流式响应
# ============================================================================

# 发送 POST 请求到 API 服务器,启用流式响应模式
response = requests.post(url, headers=headers, json=data, stream=True)
response.raise_for_status()

# ----------------------------------------------------------------------------
# 处理流式响应 - 实时解析服务器返回的数据流
# ----------------------------------------------------------------------------
try:
    # 初始化变量用于跟踪当前事件和数据
    current_event = None    # 当前 SSE 事件类型
    current_data = None     # 当前 SSE 事件数据

    # 逐行读取响应流 - 处理服务器发送的每一行数据
    for line in response.iter_lines():
        if line:  # 如果行不为空
            # 解码字节数据为 UTF-8 字符串并去除首尾空白
            line_text = line.decode('utf-8').strip()

            # ---- 处理 SSE (Server-Sent Events) 格式的事件流 ----
            if line_text.startswith('event: '):
                # 解析事件类型 - 提取事件名称
                current_event = line_text[7:]

            elif line_text.startswith('data: '):
                # 解析事件数据 - 提取数据内容
                current_data = line_text[6:]

                # 兼容同时带 event 行、或只在 data JSON 中携带 type 的 SSE。
                if current_data:
                    try:
                        # 解析 JSON 数据 - 将字符串转换为 Python 字典
                        json_data = json.loads(current_data)
                        event_type = current_event or json_data.get('type')

                        # 提取文本内容 - 根据实际数据结构,文本在 delta 字段中
                        if event_type == 'response.output_text.delta' and 'delta' in json_data:
                            content = json_data['delta']    # 获取增量文本内容
                            if content:
                                # 实时打印文本内容 - 不换行,立即刷新输出缓冲区
                                print(content, end='', flush=True)

                    except json.JSONDecodeError:
                        # 静默处理 JSON 解析错误 - 避免干扰正常输出
                        pass

            elif line_text == '':
                # 空行表示一个事件结束 - 重置事件状态
                current_event = None
                current_data = None

# ----------------------------------------------------------------------------
# 异常处理
# ----------------------------------------------------------------------------
except KeyboardInterrupt:
    # 处理用户中断 - 当用户按 Ctrl+C 时优雅退出
    print("\n\n⚠️ 用户中断了请求")

except Exception as e:
    # 处理其他异常 - 捕获并显示任何意外错误
    print(f"\n\n❌ 发生错误: {e}")

# 最后换行 - 确保输出格式整洁
print()
```

:::

## 返回示例

流式响应使用 SSE。下面仅展示文本增量事件；实际响应还会包含创建、完成等生命周期事件。

```text
event: response.output_text.delta
data: {"type":"response.output_text.delta","item_id":"msg_example_001","output_index":0,"content_index":0,"delta":"你好！有什么可以帮助你的？"}

event: response.completed
data: {"type":"response.completed","response":{"id":"resp_example_gpt56_stream_001","status":"completed","model":"gpt-5.6-sol"}}
```

## 注意事项

- SDK 已封装 SSE；直接使用 HTTP 时，要同时解析 `event:` 和 `data:` 行。
- 每个事件由空行分隔，文本增量只处理 `response.output_text.delta`。
- 本页普通流式调用不显式设置思考等级和最大输出，直接使用模型默认行为。

<p align="center">
  <small>© 2026 DMXAPI OpenAI Responses API 流式调用</small>
</p>
