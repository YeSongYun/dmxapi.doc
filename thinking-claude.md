# Claude 模型思考参数功能说明

## 📖 概念介绍

思考功能(thinking)是 Claude 系列模型（如 `claude-opus-4-8`、`claude-sonnet-4-6`）的特性参数，用于控制模型在给出最终答案前是否先进行思考（链式推理）。思考深度及回答详尽程度均可通过思考强度(`output_config.effort`)统一调节。该功能适用于数学推导、逻辑分析、代码调试等需要多步推理的场景。

## ⚙️ 思考参数配置

**思考开关** `thinking.type`：

| 参数值 | 说明 |
|--------|------|
| `adaptive` | 开启思考（自适应，Claude 自行决定何时思考及思考深度｜推荐） |
| `disabled` | 关闭思考过程 |

> 注：不传 `thinking` 字段等同于不思考（默认关闭）。**`display` 默认值按模型不同而不同**：`claude-opus-4-7`/`claude-opus-4-8` 默认 `"omitted"`，此时 `thinking` 字段是空字符串（思考仍会发生并计费），需显式设置 `thinking: {"type": "adaptive", "display": "summarized"}` 才能看到可读的思考摘要文本；`claude-sonnet-4-6` 默认就是 `"summarized"`，不用额外设置即可看到思考内容。

**思考强度** `output_config.effort`（影响本次响应的整体输出，含思考深度、文本详尽程度、工具调用次数；不要求必须开启思考也能生效）：

| 参数值 | 说明 |
|--------|------|
| `low` | 减少思考，优先速度 |
| `medium` | 思考适中，简单问题可跳过 |
| `high` | 标准思考深度（默认值） |
| `xhigh` | 更深思考（Opus 4.7 起及 Sonnet 5 支持，编程 / Agent 场景推荐） |
| `max` | 最大思考深度（思考更长更细，速度更慢） |

## 🔌 API 接口

**请求方法**: `POST`

**Base URL**: `https://www.dmxapi.cn/v1/messages`

**支持模型**: Claude 系列思考模型，如 `claude-opus-4-8`（推荐）、`claude-opus-4-7`、`claude-sonnet-4-6`（均支持思考 / 非思考双模式），请按 DMXAPI 实际提供的模型名填写。

## 💻 示例代码

### 开启思考（adaptive）

开启后，模型会先进行思考（链式推理），再给出最终答案。

```python
import json
import requests

# 配置 API 密钥
api_key = "sk-**************"  # 替换为你的 DMXAPI 令牌
url = "https://www.dmxapi.cn/v1/messages"

# 设置请求头
headers = {
    "Accept": "application/json",
    "Authorization": f"{api_key}",       # DMXAPI 令牌，直接填写（无需 Bearer 前缀）
    "Content-Type": "application/json"
}

# 构造请求数据
data = {
    "model": "claude-opus-4-8",  # Claude 系列思考模型，可换成 claude-opus-4-7、claude-sonnet-4-6 等（按 DMXAPI 实际提供的名称填写）
    "max_tokens": 2048,           # 最大输出 token 数
    "messages": [
        {
            "role": "user",
            "content": "从1加到10等于多少？"  # 用户提问
        }
    ],
    "thinking": {"type": "adaptive", "display": "summarized"},  # display:"summarized" 才能在返回中看到思考内容文本，否则默认返回空
    "output_config": {"effort": "high"}        # 思考强度：low / medium / high(默认) / xhigh / max
}

try:
    # 发送 API 请求
    response = requests.post(url, headers=headers, json=data)
    response.raise_for_status()  # 检查 HTTP 错误

    # 处理响应结果
    result = response.json()
    print("请求成功!")

    # 思考等级(effort)是只写的请求参数，响应中不会回显，只能展示本次请求时设置的值
    print(f"本次思考强度(effort): {data['output_config']['effort']}")

    # 遍历 content，分别取出思考内容与最终回答
    for block in result.get("content", []):
        if block["type"] == "thinking":
            print(f"\n【思考内容】\n{block['thinking']}")
        elif block["type"] == "text":
            print(f"\n【最终回答】\n{block['text']}")

    # 如果返回了思考实际消耗的 token 数，一并展示（体现真实思考深度）
    thinking_tokens = result.get("usage", {}).get("output_tokens_details", {}).get("thinking_tokens")
    if thinking_tokens is not None:
        print(f"\n本次思考消耗 token 数: {thinking_tokens}")

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
url = "https://www.dmxapi.cn/v1/messages"

# 设置请求头
headers = {
    "Accept": "application/json",
    "Authorization": f"{api_key}",       # DMXAPI 令牌，直接填写（无需 Bearer 前缀）
    "Content-Type": "application/json"
}

# 构造请求数据
data = {
    "model": "claude-opus-4-8",  # Claude 系列模型，可换成 claude-opus-4-7、claude-sonnet-4-6 等（按 DMXAPI 实际提供的名称填写）
    "max_tokens": 2048,           # 最大输出 token 数
    "messages": [
        {
            "role": "user",
            "content": "从1加到10等于多少？"  # 用户提问
        }
    ],
    "thinking": {"type": "disabled"}  # 关闭思考功能：直接给出最终答案（无需 output_config.effort）
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
2. 对于简单问题建议使用 `disabled` 模式，回复更快、更省 token
3. 复杂推理问题使用 `adaptive` 模式可获得更好的可解释性
4. 思考强度 `output_config.effort` 作用于本次响应的全部输出 token（含思考深度、文本详尽程度、工具调用次数），不要求必须开启思考也能生效，取值 `low`/`medium`/`high`(默认)/`xhigh`/`max`
5. 最新 Claude 模型（如 Opus 4.7/4.8）上已**移除** `temperature`、`top_p`、`top_k` 采样参数，请求中只要包含这些字段就会**返回 400**（与传什么值无关），请勿传入
6. 旧的 `thinking: {"type": "enabled", "budget_tokens": N}` 固定预算写法：在 `claude-opus-4-7`/`claude-opus-4-8` 上**已移除**（调用会报 400）；在 `claude-sonnet-4-6` 上已弃用但暂仍可用。新代码请一律改用 `thinking: {"type": "adaptive"}` + `output_config.effort`
7. 每个 `thinking` 内容块除 `thinking` 文本外还带一个 `signature`（签名）字段，用于验证该块确由 Claude 生成、并在多轮对话中还原完整思考供模型续用；如需在多轮对话中延续同一轮思考，需把上一轮返回的 thinking 块（含可能为空的 `thinking` 文本和 `signature`）原样传回，不要修改内容，被修改过的块会被服务器拒绝。`signature` 是不透明字符串，无需（也不能）解析
8. **`thinking` 字段返回为空字符串是预期行为（视模型而定）**：`claude-opus-4-7`/`claude-opus-4-8` 的 `display` 默认值为 `"omitted"`，此情况下思考仍会正常发生并计费，只是不在返回中展示；而 `claude-sonnet-4-6` 默认就是 `"summarized"`，无需额外设置即可看到思考内容。另外，思考等级（`effort`）是**请求参数**，Anthropic 响应体中不会回显本次调用使用的等级
9. 切换 `thinking` 模式（如 `adaptive` ↔ `disabled`）会导致消息缓存断点失效；只要连续请求保持同一种思考模式即可保留缓存，系统提示词与工具定义的缓存不受思考参数变化影响
10. 也可直接在模型名后加 `-thinking` / `-nothinking` 后缀，快速开启 / 关闭思考

---

<p align="center">
  <small>© 2026 DMXAPI Claude thinking</small>
</p>
