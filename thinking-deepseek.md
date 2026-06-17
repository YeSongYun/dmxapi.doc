# DeepSeek 模型思考参数功能说明

## 📖 概念介绍

思考功能(thinking)是 DeepSeek 系列模型（如 `deepseek-v4-pro`、`deepseek-v4-flash`）的特性参数，用于控制模型在给出最终答案前是否先输出思考过程（链式推理）。思考深度可通过思考强度(`reasoning_effort`)调节。该功能适用于数学推导、逻辑分析、代码调试等需要多步推理的场景。

## ⚙️ 思考参数配置

**思考开关** `thinking.type`：

| 参数值 | 说明 |
|--------|------|
| `enabled` | 强制开启思考过程（默认） |
| `disabled` | 强制关闭思考过程 |

**思考强度** `reasoning_effort`（仅在开启思考时生效）：

| 参数值 | 说明 |
|--------|------|
| `high` | 标准思考深度（普通请求默认值） |
| `max` | 最大思考深度（思考更长更细，速度更慢） |

> 注：旧值 `low`/`medium` 会映射为 `high`，`xhigh` 会映射为 `max`。

## 🔌 API 接口

**请求方法**: `POST`

**Base URL**: `https://www.dmxapi.cn/v1/chat/completions`

**支持模型**: DeepSeek 系列思考模型，如 `deepseek-v4-pro`、`deepseek-v4-flash`（均支持思考 / 非思考双模式），请按 DMXAPI 实际提供的模型名填写。

## 💻 示例代码

### 开启思考（enabled）

开启后，模型会先输出思考过程（链式推理），再给出最终答案。

```python
import json
import requests

# 配置 API 密钥
api_key = "sk-**************"  # 替换为你的 DMXAPI 令牌
url = "https://www.dmxapi.cn/v1/chat/completions"

# 设置请求头
headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}

# 构造请求数据
data = {
    "model": "deepseek-v4-pro-guan",  # DeepSeek 系列思考模型，可换成 deepseek-v4-flash 等（按 DMXAPI 实际提供的名称填写）
    "messages": [
        {
            "role": "user",
            "content": "从1加到10等于多少？"  # 用户提问
        }
    ],
    "thinking": {"type": "enabled"},     # 开启思考功能：先输出思考过程再给答案
    "reasoning_effort": "high"           # 思考强度：high 标准（默认）/ max 最大深度
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

### 关闭思考（disabled）

关闭后，模型跳过思考过程，直接给出最终答案。

```python
import json
import requests

# 配置 API 密钥
api_key = "sk-**************"  # 替换为你的 DMXAPI 令牌
url = "https://www.dmxapi.cn/v1/chat/completions"

# 设置请求头
headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}

# 构造请求数据
data = {
    "model": "deepseek-v4-pro-guan",  # DeepSeek 系列模型，可换成 deepseek-v4-flash 等（按 DMXAPI 实际提供的名称填写）
    "messages": [
        {
            "role": "user",
            "content": "从1加到10等于多少？"  # 用户提问
        }
    ],
    "thinking": {"type": "disabled"}  # 关闭思考功能：直接给出最终答案（无需 reasoning_effort）
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

1. 思考功能会增加少量响应时间
2. 对于简单问题建议使用 `disabled` 模式
3. 复杂推理问题使用 `enabled` 模式可获得更好的可解释性
4. 思考强度 `reasoning_effort` 仅在开启思考时生效，取值 `high`/`max`（旧值 `low`/`medium`→`high`，`xhigh`→`max`）
5. 开启思考模式时，`temperature`、`top_p` 等采样参数不生效，请勿传入

---

<p align="center">
  <small>© 2026 DMXAPI DeepSeek thinking</small>
</p>
