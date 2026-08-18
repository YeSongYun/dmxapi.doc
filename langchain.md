# LangChain

## LangChain 集成示例1
LangChain升级频繁，并且会有破坏性更新，请注意版本区别。
```python
"""
LangChain 结构化输出示例：自然语言转计算步骤

功能概述：
    本脚本演示如何使用 LangChain 将自然语言描述转换为结构化的 JSON 数据，
    通过 Pydantic 模型实现强类型校验，确保输出符合预期格式。

核心能力：
    - 调用兼容 OpenAI 接口的 DMXAPI 服务
    - 使用结构化输出（Structured Output）模式
    - 通过 Pydantic 进行数据验证和类型检查
    - 异步执行，提高处理效率

适用场景：
    - 将业务流程描述转为可执行步骤
    - 解析复杂的计算逻辑
    - 需要严格数据格式的 AI 应用
"""

from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from pydantic import BaseModel, Field
from typing import List
import asyncio


# ==================== 模型配置 ====================

llm = ChatOpenAI(
    api_key="sk-*********************************",  # 替换为您的 DMXAPI 密钥
    base_url="https://www.dmxapi.cn/v1",
    model="gemini-2.5-flash", )


# ==================== 数据模型定义 ====================

class CalculationStep(BaseModel):
    """单个计算步骤的数据结构"""

    step_idx: int = Field(
        description="步骤序号（从 1 开始）"
    )
    pseudocode: str = Field(
        description="步骤的伪代码或自然语言描述"
    )

    model_config = {
        "json_schema_extra": {
            "examples": [{
                "step_idx": 1,
                "pseudocode": "计算5日对数收益率"
            }]
        }
    }


class DecoupledSteps(BaseModel):
    """完整的计算步骤列表容器"""

    steps: List[CalculationStep] = Field(
        description="所有计算步骤的有序列表"
    )

    model_config = {
        "json_schema_extra": {
            "examples": [{
                "steps": [
                    {"step_idx": 1, "pseudocode": "计算5日对数收益率"},
                    {"step_idx": 2, "pseudocode": "对上一步的结果取反得到反转因子"}
                ]
            }]
        }
    }


# ==================== 主程序逻辑 ====================

async def main():
    """
    异步主函数：执行结构化输出流程

    流程说明：
        1. 将 LLM 包装为结构化输出模型
        2. 构造用户提示词
        3. 调用模型并自动解析为 Pydantic 对象
        4. 输出结构化结果
    """

    # 启用结构化输出模式（使用 json_mode 以兼容更多 API 提供商）
    model = llm.with_structured_output(
        schema=DecoupledSteps,
        method="json_mode"
    )

    # 构造用户消息
    msgs = [
        HumanMessage(content="""将这段文本转化为格式化的计算步骤列表：计算5日对数收益率，然后取反得到反转因子

请按照以下JSON格式返回结果：
{
  "steps": [
    {
      "step_idx": 1,
      "pseudocode": "计算5日对数收益率"
    },
    {
      "step_idx": 2,
      "pseudocode": "对上一步的结果取反得到反转因子"
    }
  ]
}

每个步骤必须包含：
- step_idx: 整数类型的步骤序号（从1开始）
- pseudocode: 字符串类型的伪代码描述""")
    ]

    # 异步调用并输出结果
    result = await model.ainvoke(msgs)
    print(result)


# ==================== 程序入口 ====================

if __name__ == "__main__":
    asyncio.run(main())
```
## LangChain 返回示例1
```json
steps=[CalculationStep(step_idx=1, pseudocode='计算5日对数收益率'), CalculationStep(step_idx=2, pseudocode='对上一步的结果取反得到反转因子')]
```

## LangChain 集成示例2
LangChain升级频繁，并且会有破坏性更新，请注意版本区别。
```python
"""
LangChain Agent 工具调用示例：智能天气助手

功能概述：
    演示如何使用 LangChain 创建一个可自动调用工具的智能 Agent，
    实现从用户输入到工具执行再到自然语言回复的完整流程。

核心能力：
    - 创建支持工具调用的 Agent
    - 定义自定义工具函数
    - 配置系统提示词控制行为
    - 智能解析多种返回格式
    - 异常处理与用户友好提示

适用场景：
    - 需要调用外部 API 的对话系统
    - 多功能智能助手
    - 自动化任务执行代理
"""

from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
import os


# ==================== 模型初始化 ====================

# 优先从环境变量读取 API 密钥（安全最佳实践）
api_key = (
    os.getenv("DMXAPI_API_KEY") or
    os.getenv("OPENAI_API_KEY") or
    "sk-*********************************"  # 替换为您的实际密钥
)

if not api_key:
    print("[提示] 未检测到密钥，请设置环境变量 DMXAPI_API_KEY 或 OPENAI_API_KEY")

# 初始化兼容 OpenAI 接口的模型
llm = ChatOpenAI(
    model="gpt-4o-mini",
    base_url="https://www.dmxapi.cn/v1",
    api_key=api_key,
)


# ==================== 工具定义 ====================

@tool
def get_weather(city: str) -> str:
    """
    查询指定城市的天气信息

    参数：
        city: 城市名称（中文或英文）

    返回：
        天气描述字符串

    注意：
        这是一个示例工具，返回模拟数据。
        实际应用中可接入真实天气 API（如和风天气、OpenWeatherMap）。
    """
    return f"{city} 今天晴朗，25°C，微风徐徐。"

# 工具列表（可扩展更多工具）
tools = [get_weather]


# ==================== Agent 配置 ====================

system_prompt = """
你是一个多功能智能助理，能够根据用户的自然语言请求，
自动调用可用工具并生成友好、有创意的回答。

你可以使用的工具包括：
- get_weather(city: str): 用于获取指定城市的天气。

使用策略：
1. 当用户询问天气时，请自动调用 get_weather 工具。
2. 在获取结果后，将天气信息用自然语言转述。
3. 如果用户请求生成朋友圈文案，请生成一句具有文艺气息的短句。
4. 最终输出自然流畅的中文回答，不显示工具调用过程。

回答示例：
用户："查下北京天气并写一句朋友圈文案"
回答："北京今天晴朗，微风不燥，温度宜人。这样的天气，最适合晒晒心情☀️"
"""

# 创建 Agent 实例
agent = create_agent(
    model=llm,
    tools=tools,
    system_prompt=system_prompt
)


# ==================== 执行与输出 ====================

def extract_output(response) -> str:
    """
    从不同格式的 Agent 响应中提取文本输出

    兼容多种返回结构：
        - 字典格式：output / final_output 字段
        - LangGraph 格式：messages 列表
        - 对象格式：content 属性

    参数：
        response: Agent 返回的响应对象

    返回：
        提取的文本内容
    """
    if isinstance(response, dict):
        # 优先尝试标准字段
        output = response.get("output") or response.get("final_output")
        if output:
            return output

        # 从 messages 列表中提取
        messages = response.get("messages")
        if isinstance(messages, list) and messages:
            last_message = messages[-1]
            content = getattr(last_message, "content", None)

            if content is None and isinstance(last_message, dict):
                content = last_message.get("content")

            # 处理列表类型的 content
            if isinstance(content, list):
                text_parts = []
                for part in content:
                    if isinstance(part, dict) and part.get("type") == "text":
                        text_parts.append(part["text"])
                    elif isinstance(part, str):
                        text_parts.append(part)
                if text_parts:
                    return "\n".join(text_parts)

            # 处理字符串类型的 content
            elif isinstance(content, str):
                return content

    # 兜底策略
    return getattr(response, "content", None) or str(response)


# 主执行流程
try:
    response = agent.invoke({
        "input": "帮我查下深圳天气并写一句文艺朋友圈文案"
    })

    output = extract_output(response)
    print("🤖 输出：", output)

except Exception as e:
    print(f"[错误] 调用失败：{e}")
    print("""
[排查建议]
- 401 错误：请检查 API 密钥是否有效
- 确认 base_url 为 https://www.dmxapi.cn/v1
- 确认模型名称正确（如 gpt-4o-mini）
- 检查网络连接是否正常
    """.strip())
```
## LangChain 返回示例2
```json
🤖 输出： 北京今天阳光明媚，气温25°C，微风拂面，很适合外出活动。而在上海，天气同样晴朗，气温也是25°C，微风轻轻吹来。
这样的好天气，分享一句朋友圈文案吧：“在这个阳光洒满的日子里，心情也随之绽放。”☀️
```

<p align="center">
  <small>© 2026 DMXAPI LangChain</small>
</p>