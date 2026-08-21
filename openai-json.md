# OpenAI Chat Completions 结构化 JSON 输出

本页使用 OpenAI Python SDK 的结构化输出解析功能，通过 DMXAPI 兼容代理调用 `gpt-5.6-sol`，并将结果校验为 Pydantic 模型。

## 🔗 请求地址

```text
https://www.dmxapi.cn/v1/chat/completions
```

:::warning API 密钥安全
请使用自己的 DMXAPI 令牌替换占位符。不要把真实令牌写进公开仓库或日志。
:::

## 模型名称

- `gpt-5.6-sol`

## Python 示例代码

```python
"""
================================================================================
DMXAPI 产品信息json格式化输出示例
================================================================================
功能说明：
    本脚本演示如何使用 DMXAPI 的 OpenAI 兼容接口，通过结构化输出功能
    从自然语言描述中提取产品信息（名称、价格、描述）并格式化为 JSON。
================================================================================
"""

from pydantic import BaseModel
from openai import OpenAI
import json
from textwrap import dedent


# API 工厂标识（用于区分不同的 API 提供商）
factory = "openai"


# ============================================================================
# 初始化 DMXAPI 客户端
# ============================================================================

client = OpenAI(
    # DMXAPI 的 API Key（请替换为您自己的密钥）
    api_key="sk-*******************************************",

    # DMXAPI 的基础 URL（注意必须包含 /v1/ 后缀）
    base_url="https://www.dmxapi.cn/v1/"
)


# ============================================================================
# 数据模型定义
# ============================================================================

class ProductInfo(BaseModel):
    """
    产品信息数据模型

    用于定义 AI 模型返回的结构化数据格式，确保输出内容符合预期结构。

    属性：
        product_name (str): 产品名称
        price (float): 产品价格（单位：元）
        description (str): 产品详细描述
    """
    product_name: str
    price: float
    description: str


# ============================================================================
# 提示词配置
# ============================================================================

# 系统提示词：指导 AI 模型按照指定格式输出产品信息
product_prompt = '''
根据给出的产品进行分析，按 JSON 格式用中文回答。
要求格式：product_name（产品名称）, price（价格）, description（产品描述）
'''


# ============================================================================
# 核心业务函数
# ============================================================================

def get_product_info(question: str):
    """
    调用 DMXAPI 提取产品信息

    参数：
        question (str): 用户输入的产品描述或查询内容

    返回：
        ProductInfo: 解析后的产品信息对象

    功能说明：
        使用 OpenAI 的 Structured Outputs 功能，确保模型返回的数据
        严格符合 ProductInfo 模型定义的结构。
    """
    # 调用 Chat Completions API 并启用结构化输出解析
    completion = client.beta.chat.completions.parse(
        # 使用的 AI 模型（支持结构化输出的版本）
        model="gpt-5.6-sol",

        # 对话消息列表
        messages=[
            # 系统消息：设定 AI 的角色和任务
            {"role": "system", "content": dedent(product_prompt)},

            # 用户消息：实际的查询内容
            {"role": "user", "content": question},
        ],

        # 指定响应格式为 ProductInfo 模型（强制结构化输出）
        response_format=ProductInfo,
    )

    # 返回解析后的结构化数据对象
    return completion.choices[0].message.parsed


# 初始化产品信息字典（用于存储转换后的数据）
product_inform = {}


def transform2JSON(parsed_result):  # pyright: ignore[reportUnknownParameterType, reportMissingParameterType]
    """
    将 Pydantic 模型转换为格式化的 JSON 字符串

    参数：
        parsed_result: ProductInfo 类型的解析结果对象

    返回：
        str: 格式化后的 JSON 字符串（支持中文显示）

    功能说明：
        将结构化的 Pydantic 对象转换为易读的 JSON 格式，
        便于存储、传输或展示。
    """
    # 从 Pydantic 对象中提取字段值并存入字典
    product_inform["product_name"] = parsed_result.product_name  # pyright: ignore[reportUnknownMemberType]
    product_inform["price"] = parsed_result.price  # pyright: ignore[reportUnknownMemberType]
    product_inform["description"] = parsed_result.description  # pyright: ignore[reportUnknownMemberType]

    # 转换为 JSON 字符串
    # ensure_ascii=False: 允许中文字符正常显示（不转义为 \uXXXX）
    # indent=4: 使用 4 个空格缩进，提高可读性
    return json.dumps(product_inform, ensure_ascii=False, indent=4)


# ============================================================================
# 主程序执行
# ============================================================================

if __name__ == "__main__":
    # 定义测试查询：用户想要了解的产品
    question = "75寸小米电视机"

    # 步骤 1：调用 API 获取结构化的产品信息
    print("正在查询产品信息...")
    result = get_product_info(question)

    # 步骤 2：将结果转换为 JSON 格式
    json_result = transform2JSON(result)

    # 步骤 3：输出最终结果
    print("\n" + "="*60)
    print("产品信息提取结果")
    print("="*60)
    print(json_result)
    print("="*60)

```

## 返回示例

```json
{
  "product_name": "75 寸电视",
  "price": 4999.0,
  "description": "适合客厅观影的大屏电视。"
}
```

## 注意事项

- 本页使用 SDK 的 `response_format=ProductInfo` 生成并校验结构化输出。
- DMXAPI 已实测 `gpt-5.6-sol` 可完成该 `client.beta.chat.completions.parse(...)` 调用。
- 生产环境仍应处理拒答、解析为空、超时和 HTTP 错误。

<p align="center">
  <small>© 2026 DMXAPI OpenAI 结构化 JSON 输出</small>
</p>
