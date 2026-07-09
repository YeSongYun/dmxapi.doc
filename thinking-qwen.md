# Qwen 千问模型思考参数功能说明

## 📖 概念介绍

思考功能(enable_thinking)是千问 Qwen3 系列混合思考模型的特性参数，用于控制模型在给出最终答案前是否先输出思考过程（链式推理）。思考长度可通过思考预算(`thinking_budget`)限制。该功能适用于数学推导、逻辑分析、代码调试等需要多步推理的场景。

## ⚙️ 思考参数配置

**思考开关** `enable_thinking`：

| 参数值 | 说明 |
|--------|------|
| `True` | 开启思考过程，先思考再回答（需配合流式调用，见注意事项） |
| `False` | 关闭思考过程，直接给出最终答案 |

**思考预算** `thinking_budget`（仅在开启思考时生效）：

| 参数 | 类型 | 说明 |
|------|------|------|
| `thinking_budget` | 整数 | 思考过程的最大 token 数（如 `4000`），达到上限立即停止思考并开始回答，防止资源过度消耗 |

> 注：各模型 `enable_thinking` 默认值不同（部分新版本模型默认开启思考），建议始终显式传入。

## 💻 示例代码

### 开启思考（enable_thinking: True）

```python
import json
import requests

# 配置 API 密钥
api_key = "sk-................................."  # 替换为你的 DMXAPI 令牌
url = "https://www.dmxapi.cn/v1/chat/completions"

# 设置请求头
headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}

# 构造请求数据
data = {
    "model": "qwen3.7-max",  # 千问 Qwen3 系列模型（按 DMXAPI 实际提供的名称填写）
    "messages": [
        {
            "role": "user",
            "content": "从1加到10等于多少？"  # 用户提问
        }
    ],
    "enable_thinking": True,   # 开启思考功能：先输出思考过程再给答案
    "thinking_budget": 4000,   # 可选：思考过程最大 token 数，达到上限立即停止思考
}

try:
    # 发送 API 请求
    response = requests.post(url, headers=headers, json=data)
    response.raise_for_status()  # 检查 HTTP 错误

    # 处理响应结果
    print("请求成功!")
    print(json.dumps(response.json(), indent=2, ensure_ascii=False))

except requests.exceptions.RequestException as e:
    # 异常处理
    print(f"请求失败: {e}")
```

### 关闭思考（enable_thinking: False）

```python
import json
import requests

# 配置 API 密钥
api_key = "sk-................................."  # 替换为你的 DMXAPI 令牌
url = "https://www.dmxapi.cn/v1/chat/completions"

# 设置请求头
headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}

# 构造请求数据
data = {
    "model": "qwen3.7-max",  # 千问 Qwen3 系列模型（按 DMXAPI 实际提供的名称填写）
    "messages": [
        {
            "role": "user",
            "content": "从1加到10等于多少？"  # 用户提问
        }
    ],
    "enable_thinking": False  # 关闭思考功能：直接给出最终答案（无需 thinking_budget）
}

try:
    # 发送 API 请求
    response = requests.post(url, headers=headers, json=data)
    response.raise_for_status()  # 检查 HTTP 错误

    # 处理响应结果
    print("请求成功!")
    print(json.dumps(response.json(), indent=2, ensure_ascii=False))

except requests.exceptions.RequestException as e:
    # 异常处理
    print(f"请求失败: {e}")
```

## ⚠️ 注意事项

1. 思考功能会增加少量响应时间，思考内容按输出 token 计费
2. 对于简单问题建议使用 `False` 模式，回复更快、更省 token
3. 复杂推理问题使用 `True` 模式可获得更好的可解释性
4. 使用 Python OpenAI SDK 调用时，`enable_thinking` / `thinking_budget` 为非标准参数，必须放进 `extra_body={"enable_thinking": True, "thinking_budget": 4000}`，写在顶层会报「unexpected keyword argument」；用 requests 直发 JSON 时直接写在请求体顶层即可
5. 思考模式与结构化输出（JSON mode）不兼容：需要 JSON 输出时请设置 `enable_thinking=false`
6. `enable_thinking` / `thinking_budget` 对 QwQ 等仅思考模型无效（恒为思考模式）
7. 思考过程在 `reasoning_content` 字段，最终回答在 `content` 字段

---

<p align="center">
  <small>© 2026 DMXAPI 千问 thinking</small>
</p>
