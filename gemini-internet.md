# Gemini 联网搜索工具调用 API 使用方法

## 功能概述

本示例通过 DMXAPI 调用 `gemini-3.8-flash`，使用 Google Search 工具查询互联网信息。模型会根据问题决定是否调用搜索；应结合 `grounding_metadata` 中的来源核对答案，而不是仅凭返回文本判断已联网。

运行前安装 SDK（`pip install -U google-genai`），设置环境变量 `GEMINI_API_KEY` 或替换示例中的密钥占位符。

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

以下为输出格式示意，日期和天气不是本次实测数据；实际答案与搜索来源以当次响应为准：

```json
今天（2025年11月20日）上海天气晴朗，气温在7°C到15°C之间。

具体天气情况如下：
*   **当前**: 部分多云，气温11°C，体感温度11°C，湿度约为47%。
*   **今天白天**: 晴朗。
*   **今晚**: 晴朗，有5%的降雨概率。
*   **风力**: 西北风3-4级。
*   **空气质量**: 良好到轻度污染，首要污染物为PM2.5。

未来几天的天气预报：
*   **11月21日（周五）**: 晴朗，气温7°C到16°C，西北风3-4级。
*   **11月22日（周六）**: 白天晴朗，夜间晴转局部多云，气温10°C到17°C，有5%的降雨概率。
*   **11月23日（周日）**: 白天大部分晴朗，夜间大部分多云，气温11°C到20°C，夜间有10%的降雨概率。
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

