# OpenAI Chat Completions 流式调用
## 🔗 请求地址
```text
https://www.dmxapi.cn/v1/chat/completions
```
## 模型名称
- 本页示例：`gpt-5.6-sol`
- 其他模型：替换 `model`，并检查该模型对推理、输出长度和工具参数的支持情况。
## Python 请求示例

```python
"""
=================================================================
OpenAI兼容API流式对话示例
=================================================================
本脚本演示如何使用流式传输(Server-Sent Events)方式调用AI聊天接口
实现实时接收和显示AI响应内容的效果
=================================================================
"""

# =================================================================
# 1. 导入依赖库
# =================================================================
import json      # JSON数据处理:用于解析API返回的JSON格式数据
import requests  # HTTP请求库:用于发送POST请求到API服务器

# =================================================================
# 2. 配置API连接参数
# =================================================================
url = "https://www.dmxapi.cn/v1/chat/completions"  # API端点地址

# 请求头配置
headers = {
    "Authorization": "sk-******************************",  # 身份认证令牌(请替换为您的真实API密钥)
    "Content-Type": "application/json"  # 声明请求体为JSON格式
}

# =================================================================
# 3. 构建请求数据
# =================================================================
payload = {
    "model": "gpt-5.6-sol",  # 选择AI模型(此处使用gpt-5.6-sol模型)
    "stream": True,  # 启用流式输出模式,可实时接收生成的内容片段
    "messages": [
        {
            "role": "system",  # 系统消息:定义AI的行为模式
            "content": "You are a helpful assistant."
        },
        {
            "role": "user",  # 用户消息:实际的问题或指令
            "content": "周树人和鲁迅是兄弟吗?"
        }
    ]
}

# =================================================================
# 4. 发送请求并处理流式响应
# =================================================================
# 发送POST请求,stream=True启用流式接收模式
response = requests.post(url, headers=headers, json=payload, stream=True)

# 数据缓冲区:由于网络传输可能分块到达,需要缓存不完整的数据
buffer = ""

# =================================================================
# 5. 逐块处理响应数据流
# =================================================================
for chunk in response.iter_content(chunk_size=None):
    if chunk:  # 确保接收到的数据块非空
        # 将二进制数据解码为UTF-8字符串并追加到缓冲区
        buffer += chunk.decode("utf-8")

        # -----------------------------------------------------------
        # 按行处理缓冲区数据(SSE协议是基于行的)
        # -----------------------------------------------------------
        while "\n" in buffer:
            # 提取第一行数据,剩余部分保留在缓冲区
            line, buffer = buffer.split("\n", 1)

            # 跳过空行(SSE协议中空行用于分隔事件)
            if not line.strip():
                continue

            # -----------------------------------------------------------
            # 解析SSE格式数据(Server-Sent Events)
            # SSE数据格式: "data: {JSON内容}"
            # -----------------------------------------------------------
            if line.startswith("data: "):
                # 提取"data: "后面的实际JSON数据
                data_line = line[6:].strip()

                # 检查流结束标记
                if data_line == "[DONE]":
                    break

                try:
                    # 解析JSON数据
                    data = json.loads(data_line)

                    # ---------------------------------------------------
                    # 提取AI生成的文本内容
                    # 数据结构: data.choices[0].delta.content
                    # ---------------------------------------------------
                    if "choices" in data and len(data["choices"]) > 0 and "delta" in data["choices"][0]:
                        content = data["choices"][0]["delta"].get("content", "")

                        # 只输出非空内容(过滤掉仅包含元数据的响应)
                        if content:
                            # end="": 不换行
                            # flush=True: 立即输出,不等待缓冲区满
                            # 实现打字机效果的实时显示
                            print(content, end="", flush=True)

                except json.JSONDecodeError:
                    # ---------------------------------------------------
                    # JSON解析失败处理
                    # 原因:数据块可能在JSON对象中间被截断
                    # 解决:将未完成的行放回缓冲区,等待下一个数据块
                    # ---------------------------------------------------
                    buffer = line + "\n" + buffer
                    break  # 退出while循环,继续接收下一个chunk
```

## 返回示例

```text
data: {"id":"chatcmpl_example_stream_001","model":"gpt-5.6-sol-2026-07-09","choices":[{"index":0,"delta":{"content":"不是。"}}]}

data: {"id":"chatcmpl_example_stream_001","model":"gpt-5.6-sol-2026-07-09","choices":[{"index":0,"delta":{"content":"周树人和鲁迅是同一个人。"}}]}

data: [DONE]
```

## 注意事项

- DMXAPI 实测流中会出现 `choices: []` 的元数据块；不要直接访问 `choices[0]`。
- 文本增量位于 `choices[0].delta.content`，结束标记为 `data: [DONE]`。
- 网络层使用 `stream=True`，请求体也必须包含 `"stream": true`。

<p align="center">
  <small>© 2026 DMXAPI OpenAI Chat Completions 流式调用</small>
</p>
