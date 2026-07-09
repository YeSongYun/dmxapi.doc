# Gemini 模型思考参数功能说明

## 📖 概念介绍

思考功能(thinking)是 Gemini 思考模型的特性参数，用于控制模型在给出最终答案前的内部推理（链式推理）深度。和 Claude 不同，Gemini 的思考模型**默认按任务复杂度自动决定思考量（动态思考）**，不做任何配置也可以正常使用。两代模型的控制参数不同：Gemini 2.5 系列使用思考预算(`thinking_budget`，token 数)，Gemini 3 系列起改用思考等级(`thinking_level`，档位)。该功能适用于数学推导、逻辑分析、代码调试等需要多步推理的场景。

## ⚙️ 思考参数配置

### 方式一：思考预算 `thinking_budget`（Gemini 2.5 系列）

| 取值 | 说明 |
|------|------|
| `-1` | 动态思考：模型按任务复杂度自行决定思考量（官方推荐） |
| `0` | 关闭思考（仅 Flash / Flash-Lite 支持；2.5 Pro 无法关闭，最低 128） |
| 正整数 | 固定思考 token 预算上限，各型号范围不同（如 Flash 为 0–24576，Pro 为 128–32768） |

### 方式二：思考等级 `thinking_level`（Gemini 3 系列起）

| 参数值 | 说明 |
|--------|------|
| `minimal` | 最少思考，最大限度缩短延迟（仅部分型号支持，如 Gemini 3 Flash；不保证思考完全关闭） |
| `low` | 减少思考，优先速度、降低费用 |
| `medium` | 思考适中，适合大多数任务（部分型号支持） |
| `high` | 最大推理深度（默认值，动态思考） |

## 💻 示例代码

### 开启思考并返回思考摘要（Gemini 2.5：thinking_budget）

`thinking_budget=-1` 开启动态思考；`include_thoughts=True` 让响应中返回思考摘要（带 `thought=True` 标记的 part）。

```python
from google import genai
from google.genai import types

# 配置 API 密钥
API_KEY = "sk-**************"  # 替换为你的 DMXAPI 令牌
BASE_URL = "https://www.dmxapi.cn"

# 初始化客户端
client = genai.Client(
    api_key=API_KEY,
    http_options={"base_url": BASE_URL}
)

# 调用模型（开启思考）
response = client.models.generate_content(
    model="gemini-2.5-flash",  # Gemini 2.5 系列思考模型（按 DMXAPI 实际提供的名称填写）
    contents="从1加到10等于多少？",
    config=types.GenerateContentConfig(
        thinking_config=types.ThinkingConfig(
            thinking_budget=-1,     # -1 动态思考（推荐）；正整数为固定预算；0 为关闭
            include_thoughts=True,  # 返回思考摘要
        )
    ),
)

# 解析响应：区分思考摘要和最终回答
for part in response.candidates[0].content.parts:
    if part.thought:  # 思考摘要 part 带 thought=True 标记
        print(f"【思考摘要】\n{part.text}\n")
    else:
        print(f"【最终回答】\n{part.text}")

# 思考消耗的 token 数（按输出 token 计费）
print(f"\n本次思考消耗 token 数: {response.usage_metadata.thoughts_token_count}")
```

### 关闭思考（Gemini 2.5：thinking_budget: 0）

关闭后，模型跳过思考过程，直接给出最终答案。仅 Flash / Flash-Lite 支持关闭，`gemini-2.5-pro` 无法关闭思考。

```python
from google import genai
from google.genai import types

# 配置 API 密钥
API_KEY = "sk-**************"  # 替换为你的 DMXAPI 令牌
BASE_URL = "https://www.dmxapi.cn"

# 初始化客户端
client = genai.Client(
    api_key=API_KEY,
    http_options={"base_url": BASE_URL}
)

# 调用模型（关闭思考）
response = client.models.generate_content(
    model="gemini-2.5-flash",  # 仅 Flash / Flash-Lite 支持关闭思考
    contents="从1加到10等于多少？",
    config=types.GenerateContentConfig(
        thinking_config=types.ThinkingConfig(
            thinking_budget=0  # 0 关闭思考：直接给出最终答案
        )
    ),
)

print(response.text)
```

### 开启思考并返回思考摘要（Gemini 3 系列起：include_thoughts）

Gemini 3 系列同样通过 `include_thoughts=True` 返回思考摘要，可与 `thinking_level` 搭配使用。思考摘要在带 `thought=True` 标记的 part 中，最终回答在普通 part 中。

```python
from google import genai
from google.genai import types

# 配置 API 密钥
API_KEY = "sk-**************"  # 替换为你的 DMXAPI 令牌
BASE_URL = "https://www.dmxapi.cn"

# 初始化客户端
client = genai.Client(
    api_key=API_KEY,
    http_options={"base_url": BASE_URL}
)

# 调用模型（开启思考摘要）
response = client.models.generate_content(
    model="gemini-3-flash-preview",  # Gemini 3 系列模型（按 DMXAPI 实际提供的名称填写）
    contents="前 50 个质数的和是多少？",
    config=types.GenerateContentConfig(
        thinking_config=types.ThinkingConfig(
            thinking_level="high",   # 可选：思考等级，默认 high（动态思考）
            include_thoughts=True    # 返回思考摘要
        )
    ),
)

# 解析响应：区分思考摘要和最终回答
for part in response.candidates[0].content.parts:
    if not part.text:  # 跳过无文本的 part（如仅含思考签名的 part）
        continue
    if part.thought:   # 思考摘要 part 带 thought=True 标记
        print(f"【思考摘要】\n{part.text}\n")
    else:
        print(f"【最终回答】\n{part.text}")
```

## ⚠️ 注意事项

1. 思考功能会增加少量响应时间，思考内容按输出 token 计费，用量见响应的 `usage_metadata.thoughts_token_count`（REST 为 `usageMetadata.thoughtsTokenCount`）
2. Gemini 思考模型**默认即动态思考**：不传参数不等于不消耗思考 token，成本敏感场景请显式关闭思考或调低预算 / 档位
3. `gemini-2.5-pro` 无法关闭思考：`thinking_budget: 0` 仅对 Flash / Flash-Lite 生效，Pro 最低 128；`-thinking` 后缀对 pro 型号也只是展示思考过程
4. `thinking_level` 与 `thinking_budget` 不能在同一请求中同时使用，否则返回 400 错误
5. `include_thoughts=True` 返回的是**思考摘要**（带 `thought: true` 标记的 part），并非原始思考全文
6. Gemini 3 系列在函数调用场景必须原样回传思考签名(`thoughtSignature`)，缺失会报 400 错误；使用官方 SDK 和标准聊天记录时签名会自动处理，详见 [Gemini 3 开发者使用指南](https://doc.dmxapi.cn/gemini-3.html)
7. `minimal` 档并不保证思考完全关闭，对复杂任务模型仍可能进行简单思考

---

<p align="center">
  <small>© 2026 DMXAPI Gemini thinking</small>
</p>
