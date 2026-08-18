# OpenAI Response 接口格式调用

## 接口地址

```
https://www.dmxapi.cn/v1/responses
```

## 模型名称

- `gpt-5.2-pro`
- `gpt-5-pro`


## 调用示例

```python
import requests
import json

# ============================================================================
# 配置部分 - API 连接信息
# ============================================================================

# DMXAPI 的 URL 地址
url = "https://www.dmxapi.cn/v1/responses"

# API 密钥 - 用于身份验证和访问控制
api_key = "sk-***************************"  # ⚠️ 请替换为你的API密钥

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
    "model": "gpt-5.2-pro",    # 指定使用的 AI 模型版本
    "input": "你好",          # 发送给 AI 的问题或指令
    "stream": True,          # 启用流式输出 - 实时接收响应而不是等待完整回复
    
    # ---------- 输出控制参数 ----------
    # 📏 最大输出令牌数 
    # 控制模型响应的最大长度
    # 💡 提示: 实际输出可能少于此值
    "max_output_tokens": 128000,

    # ---------- 采样参数 ----------
    # 🌡️ 温度参数 (范围: 0.0 - 2.0)
    # 控制输出的随机性和创造性:
    #   • 较低值 (0.0-0.3): 输出更确定、更一致,适合事实性任务
    #   • 中等值 (0.4-0.8): 平衡创造性和一致性
    #   • 较高值 (0.9-2.0): 输出更随机、更有创意
    # ⚠️ 建议: 只调整 temperature 或 top_p 其中之一
    "temperature": 1,

    # 🎯 核采样参数 (范围: 0.0 - 1.0)
    # 控制采样的概率质量阈值:
    #   • 0.1: 只考虑概率最高的 10% 的词
    #   • 0.5: 只考虑概率最高的 50% 的词
    #   • 1.0: 考虑所有可能的词
    # 💡 提示: 较低的值会让输出更集中,较高的值会增加多样性
    # ⚠️ 建议: 只调整 temperature 或 top_p 其中之一
    "top_p": 1,
    
    # ---------- 推理配置 ----------

    "reasoning": {
  
        # 📌 注意: gpt-5.2-pro 模型默认且仅支持 high 级别
        "effort": "high"
    }
}

# ============================================================================
# 发送请求并处理流式响应
# ============================================================================

# 发送 POST 请求到 API 服务器,启用流式响应模式
response = requests.post(url, headers=headers, json=data, stream=True)

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
                
                # 只处理包含文本内容的增量事件
                if current_event == 'response.output_text.delta' and current_data:
                    try:
                        # 解析 JSON 数据 - 将字符串转换为 Python 字典
                        json_data = json.loads(current_data)
                        
                        # 提取文本内容 - 根据实际数据结构,文本在 delta 字段中
                        if 'delta' in json_data:
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

## 返回示例

```json
{
  "id": "resp_0bc0cffd983db63400693fdeadd58481a2aa83ef0faac36caf",
  "created_at": 1765793453.0,
  "error": null,
  "incomplete_details": null,
  "instructions": null,
  "metadata": {},
  "model": "gpt-5.2-pro",
  "object": "response",
  "output": [
    {
      "id": "msg_0bc0cffd983db63400693fdeb7040881a2a3bab41b1908bdd8",
      "content": [
        {
          "annotations": [],
          "text": "你好！我能帮你做些什么？如果你愿意，可以告诉我你想聊的主题或需要解决的问题（比如学习、写作、编程、翻译、生活建议等）。",
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
  "top_p": 0.98,
  "background": false,
  "conversation": null,
  "max_output_tokens": null,
  "max_tool_calls": null,
  "previous_response_id": null,
  "prompt": null,
  "prompt_cache_key": null,
  "prompt_cache_retention": null,
  "reasoning": {
    "effort": "high",
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
    "verbosity": "medium"
  },
  "top_logprobs": 0,
  "truncation": "disabled",
  "usage": {
    "input_tokens": 8,
    "input_tokens_details": {
      "cached_tokens": 0
    },
    "output_tokens": 46,
    "output_tokens_details": {
      "reasoning_tokens": 0
    },
    "total_tokens": 54
  },
  "user": null,
  "billing": {
    "payer": "developer"
  },
  "store": true
}
```

## 注意事项

1. **API密钥安全**: 请妥善保管您的API密钥,不要泄露
2. **接口格式要求**: `gpt-5.2-pro` 模型必须使用 `response` 接口格式调用
3. **测试建议**: 建议在正式环境前先进行测试调用
4. **技术支持**: 如遇问题可联系 DMXAPI 技术支持

---

<p align="center">
  <small>© 2026 DMXAPI OpenAI 新接口</small>
</p>