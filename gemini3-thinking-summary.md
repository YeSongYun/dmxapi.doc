# Gemini 3 思考总结

思考总结是模型原始思考的总结版本，可帮助您深入了解模型的内部推理过程。启用后，模型会在响应中返回思考总结和最终回答两部分内容。


## 功能说明

**启用方式**：在 `thinkingConfig` 中设置 `include_thoughts=True`。

**访问方式**：遍历响应的 `parts`，通过检查每个 part 的 `thought` 布尔属性来区分思考总结和最终回答。

**非流式 vs 流式**：
- **非流式**：返回单个最终思考总结。
- **流式**：在生成过程中逐步返回增量摘要，让您可以实时观察模型的推理过程。

## 非流式调用示例

```python
from google import genai
from google.genai import types

# DMXAPI 配置
API_KEY = "sk-rOQH5ITfGkp9pbvnIIbcQyPRCQclFUl8bSjD3dFRPeuDUQHl"
BASE_URL = "https://www.dmxapi.cn"

# 初始化客户端
client = genai.Client(
    api_key=API_KEY,
    http_options={"base_url": BASE_URL}
)

# 调用模型（启用思考总结）
response = client.models.generate_content(
    model="gemini-3-pro-preview",
    contents="9.11 和 9.8 哪个大？请解释你的推理过程。",
    config=types.GenerateContentConfig(
        thinking_config=types.ThinkingConfig(
            include_thoughts=True
        )
    ),
)

# 解析响应：区分思考总结和最终回答
for part in response.candidates[0].content.parts:
    if part.thought:
        print("💭 思考总结:")
        print(part.text)
        print("\n" + "="*60 + "\n")
    else:
        print("✅ 最终回答:")
        print(part.text)
```

### 返回示例

```text

```

## 流式调用示例

```python
from google import genai
from google.genai import types

# DMXAPI 配置
API_KEY = "sk-rOQH5ITfGkp9pbvnIIbcQyPRCQclFUl8bSjD3dFRPeuDUQHl"
BASE_URL = "https://www.dmxapi.cn"

# 初始化客户端
client = genai.Client(
    api_key=API_KEY,
    http_options={"base_url": BASE_URL}
)

# 流式调用（实时接收思考和回答）
thoughts = ""
answer = ""

for chunk in client.models.generate_content_stream(
    model="gemini-3-pro-preview",
    contents="9.11 和 9.8 哪个大？请解释你的推理过程。",
    config=types.GenerateContentConfig(
        thinking_config=types.ThinkingConfig(
            include_thoughts=True
        )
    )
):
    # 检查 chunk 是否包含有效内容
    if not chunk.candidates or not chunk.candidates[0].content:
        continue

    # 检查 parts 是否存在
    if not chunk.candidates[0].content.parts:
        continue

    # 遍历每个 chunk 的 parts
    for part in chunk.candidates[0].content.parts:
        if not part.text:
            continue
        elif part.thought:
            # 实时输出思考总结
            if not thoughts:
                print("💭 思考总结（流式）:")
            print(part.text, end="", flush=True)
            thoughts += part.text
        else:
            # 实时输出最终回答
            if not answer:
                print("\n\n✅ 最终回答（流式）:")
            print(part.text, end="", flush=True)
            answer += part.text

print("\n" + "="*60)
print("流式调用完成！")
```

### 返回示例

```text

```

<p align="center">
  <small>© 2026 DMXAPI Gemini 3 思考总结</small>
</p>
