# 支持模型原厂 SDK

## 支持的厂商

- OpenAI SDK
- Anthropic Claude SDK  
- Google Gemini SDK

## 配置方法

安装 SDK：

```bash
pip install openai
```

::: warning
Python 版本过高可能导致安装失败。
:::

```python
from openai import OpenAI

client = OpenAI(
    api_key="sk-******************************",
    base_url="https://www.dmxapi.cn/v1"
)

response = client.chat.completions.create(
    model="gpt-5-mini",
    messages=[{"role": "user", "content": "你好"}]
)

print(response.choices[0].message.content)
```

示例输出：

```text
你好！我可以帮你解答问题、写作与润色、翻译、编程、学习辅导或提供建议。你想从哪方面开始？
```

::: tip
提示：将 `******` 替换为你实际的 API Key，其他厂商 SDK 配置方式类似
:::

---

<p align="center">
  <small>© 2025 DMXAPI  SDK</small>
</p>
