# Gemini 联网搜索工具调用 API 使用方法
## 功能概述
本示例通过 DMXAPI 调用 `gemini-3.8-flash`，使用 Google Search 工具查询互联网信息。模型会根据问题决定是否调用搜索；应结合 `grounding_metadata` 中的来源核对答案，而不是仅凭返回文本判断已联网。
## 接口地址
```
https://www.dmxapi.cn/v1beta/models/{model}:generateContent

```
## 示例代码
```python
"""
DMXAPI Gemini API 工具调用示例 - Google 搜索联网功能

本示例演示如何使用 Gemini API 的工具调用功能，
让模型通过 Google 搜索获取实时信息并生成回答。

工具：Google Search
"""

import os
from google import genai
from google.genai import types

# ============================================================
# 配置部分
# ============================================================

# 从环境变量读取 DMXAPI 密钥，如果未设置则使用默认值
api_key = os.getenv("GEMINI_API_KEY", "sk-*******************************************")

# 从环境变量读取 DMXAPI 基础 URL
BASE_URL = os.getenv("GEMINI_API_BASE_URL", "https://www.dmxapi.cn")

# 创建 Gemini 客户端实例
client = genai.Client(
    api_key=api_key,
    http_options={'base_url': BASE_URL} 
)

# ============================================================
# 工具配置
# ============================================================

# 配置 Google 搜索工具
# 该工具允许模型通过 Google 搜索获取实时信息
grounding_tool = types.Tool(
    google_search=types.GoogleSearch()
)

# 生成内容配置
# 将 Google 搜索工具添加到配置中
config = types.GenerateContentConfig(
    tools=[grounding_tool]
)

# ============================================================
# 执行查询
# ============================================================

# 调用 Gemini API 生成内容
# model: 使用 gemini-3.8-flash 模型
# contents: 用户的问题（查询上海天气）
# config: 包含 Google 搜索工具的配置
response = client.models.generate_content(
    model="gemini-3.8-flash",
    contents="今天上海的天气怎么样?",
    config=config,
)

# ============================================================
# 输出结果
# ============================================================

# 打印模型生成的回答
# 模型会先通过 Google 搜索获取实时天气信息，然后生成回答
print(response.text)

# 输出搜索来源；未返回来源时，不将回答视为已验证的联网结果
metadata = response.candidates[0].grounding_metadata if response.candidates else None
if metadata and metadata.grounding_chunks:
    for chunk in metadata.grounding_chunks:
        if chunk.web:
            print(f"来源: {chunk.web.title} {chunk.web.uri}")
else:
    print("本次响应未返回搜索来源，请核对工具调用情况。")
```

## 返回示例

```text
今天（11月3日，周二）上海的天气情况如下：

* **天气状况**：白天以**多云到阴**为主，夜间转为**阴有阵雨或小到中雨**。
* **气温**：全天气温大致在 **15℃ ～ 20℃** 之间，当前夜间气温约 **16℃ ~ 17℃**，体感较为凉爽。
* **湿度与风向**：湿度较高（约 75%～85%），风力较小。

**出行提示**：
夜间降水概率较高，若晚间有外出需求建议备好雨具；早晚体感偏凉，可搭配夹克、薄外套或针织衫穿着。
来源: Weather information for , CN https://www.google.com/search?q=weather+in+,+CN
来源: weather.com.cn https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQGajs9yz8seSSlIz2gNukmKSlEyKi13wIi7KX1Etsw988MKDZMKV6J4ib-Jrj7kavATmu-XKCjFLJEH18Lqtmb8bNrCvWjMw63ydtHvlfAqa8RP4oM9LWNAntn9Wh2ObS1zqwwF_hhUClLeEbjT
来源: weathernews.com https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQGW2l8mJcn7f6_e6-tIir1-_mNcrNds3HZ869Sm-eW6KTBnXYXBUWYg06CMPb7SobN7mmEY__p3wNJAeOo49JRgxPKTSMN5JvEneU5-L4hmMMLLIiKWhaRemWb17t1JXCYxkc-ja24Bmr9vy9Upo2xZaARF7ANyOqXNUFsXQY8sAi95xSLjYHDxSJvZdXyHcD7s
```

## 注意事项

1. **API 密钥安全**：
   - 不要在代码中硬编码 API 密钥
   - 建议使用环境变量 `GEMINI_API_KEY` 存储密钥
   - 不要将包含密钥的代码提交到公共代码仓库

2. **模型选择**：
   - 本文统一使用 `gemini-3.8-flash`
   - Google Search 的可用性以当前模型通道及响应中的来源信息为准

3. **查询优化**：
   - 提出明确、具体的问题以获得更准确的结果
   - 模型会自动判断是否需要联网搜索
   - 不是所有问题都需要联网，模型会智能选择

---
<p align="center">
  <small>© 2026 DMXAPI 联网搜索</small>
</p>

