# OpenAI Responses API 文件分析

本页演示通过 DMXAPI 兼容代理把公开 PDF 文件 URL 传给 `gpt-5.6-sol`，并让模型读取文件内容。

## 🔗 请求地址

```text
https://www.dmxapi.cn/v1/responses
```
## 模型名称
- 本页示例：`gpt-5.6-sol`
- 其他模型：替换 `model`，并检查该模型对推理、输出长度和工具参数的支持情况。
## Python 请求示例

```python
"""
DMXAPI 文件分析示例
功能：使用 DMXAPI 的 responses 接口分析 PDF 文件内容
"""

import json
import requests

# ============================================================
# 第一步：配置 API 信息
# ============================================================
API_KEY = "sk-*****************************************"  # 你的 DMXAPI 令牌
url = "https://www.dmxapi.cn/v1/responses"  # DMXAPI 响应接口地址

# 设置请求头信息
headers = {
    "Authorization": f"{API_KEY}",  # 身份验证令牌
    "Content-Type": "application/json"      # 指定内容类型为 JSON
}

# ============================================================
# 第二步：构建请求数据
# ============================================================
payload = json.dumps({
    "model": "gpt-5.6-sol",  # 使用的 AI 模型
    "input": [{
        "role": "user",  # 用户角色
        "content": [
            {
                "type": "input_file",  # 输入类型：文件
                "file_url": "https://www.berkshirehathaway.com/letters/2024ltr.pdf"  # PDF 文件的 URL 地址
            },
            {
                "type": "input_text",  # 输入类型：文本
                "text": "这份文件是哪家公司写给股东的信？只回复公司名称。"  # 对文件的分析指令
            }
        ]
    }]
})

# ============================================================
# 第三步：发送 API 请求
# ============================================================
print("正在发送请求到 DMXAPI...")
response = requests.post(url, headers=headers, data=payload)

# ============================================================
# 第四步：处理返回结果
# ============================================================
if response.status_code == 200:
    # 请求成功，解析 JSON 响应
    result = response.json()
    print("="*60)
    print("📄 分析结果：")
    print("="*60)
    # 使用格式化输出，indent=4 表示缩进 4 个空格
    # ensure_ascii=False 保证中文正常显示
    print(json.dumps(result, indent=4, ensure_ascii=False))
    print("="*60)
else:
    # 请求失败，显示错误信息
    print("="*60)
    print("❌ 请求失败")
    print("="*60)
    print(f"状态码: {response.status_code}")
    print(f"错误信息: {response.text}")
    print("="*60)
```

## 返回示例

```json
{
  "id": "resp_example_gpt56_file_001",
  "object": "response",
  "status": "completed",
  "model": "gpt-5.6-sol",
  "output": [
    {
      "id": "msg_example_gpt56_file_001",
      "type": "message",
      "status": "completed",
      "role": "assistant",
      "content": [
        {
          "type": "output_text",
          "text": "伯克希尔·哈撒韦公司",
          "annotations": []
        }
      ]
    }
  ]
}
```
<p align="center">
  <small>© 2026 DMXAPI OpenAI Responses API 文件分析</small>
</p>
