# Doubao 豆包模型思考参数功能说明

## 📖 概念介绍

思考功能(thinking)是豆包 doubao-seed 系列模型的特性参数，用于控制模型在给出最终答案前是否先进行深度思考（链式推理）。与其他厂商不同，豆包额外提供 `auto` 档位，可由模型根据问题难度自动决定是否思考。该功能适用于数学推导、逻辑分析、代码调试等需要多步推理的场景。

## ⚙️ 思考参数配置

**思考开关** `thinking.type`：

| 参数值 | 说明 |
|--------|------|
| `enabled` | 强制开启深度思考，每次先思考再回答 |
| `disabled` | 强制关闭深度思考，直接给出最终答案 |
| `auto` | 由模型按问题难度自动决定是否思考（部分型号支持） |


## 🔌 API 接口

**请求方法**: `POST`

**Base URL**: `https://www.dmxapi.cn/v1/chat/completions`

## 💻 示例代码

### 开启思考（enabled）

开启后，模型会先输出思考过程（链式推理），再给出最终答案。思考过程在响应的 `reasoning_content` 字段，最终回答在 `content` 字段。

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
    "model": "doubao-seed-2-1-pro-260628",  # 豆包 doubao-seed 系列思考模型（按 DMXAPI 实际提供的名称填写）
    "messages": [
        {
            "role": "user",
            "content": "从1加到10等于多少？"  # 用户提问
        }
    ],
    "thinking": {"type": "enabled"}  # 开启思考功能：先输出思考过程再给答案，可选 enabled / disabled / auto
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
api_key = "sk-............................."  # 替换为你的 DMXAPI 令牌
url = "https://www.dmxapi.cn/v1/chat/completions"

# 设置请求头
headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}

# 构造请求数据
data = {
    "model": "doubao-seed-2-1-pro-260628",  # 豆包 doubao-seed 系列模型（按 DMXAPI 实际提供的名称填写）
    "messages": [
        {
            "role": "user",
            "content": "从1加到10等于多少？"  # 用户提问
        }
    ],
    "thinking": {"type": "disabled"}  # 关闭思考功能：直接给出最终答案
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
2. 对于简单问题建议使用 `disabled` 模式
3. 复杂推理问题使用 `enabled` 模式可获得更好的可解释性
4. 思考过程在响应的 `reasoning_content` 字段，最终回答在 `content` 字段
5. 各模型默认值不同，成本敏感场景请显式传入 `disabled`
6. 使用 Python OpenAI SDK 调用时，`thinking` 为非标准参数，必须放进 `extra_body={"thinking": {"type": "enabled"}}`，写在顶层会报错；用 requests 直发 JSON 时直接写在请求体顶层即可

---

<p align="center">
  <small>© 2026 DMXAPI Doubao thinking</small>
</p>
