# Qwen3.8-Omni-Flash 多轮对话 API 使用文档

基于 Qwen3.8-Omni-Flash 全模态模型的多轮对话接口，通过 `/v1/chat/completions` 端点以 OpenAI SDK 流式调用。多轮对话不会由服务端自动保存上下文，客户端需在每次请求中把之前的用户消息和助手回复按顺序放入 `messages`；`preserve_thinking` 默认开启，思考开启时应将上一轮回复的思考内容放入历史 assistant 消息的 `reasoning_content` 字段一并传回（传回的思考内容计入输入 Token 和费用，assistant 消息只能包含文本数据），模型才能完整延续已有上下文。

## 接口地址

| 接口 | 请求方式 | URL |
|------|---------|-----|
| 多轮对话 | POST | `https://www.dmxapi.cn/v1/chat/completions` |

:::warning
请妥善保管您的 API Key！严禁将密钥泄露给他人、硬编码到代码中或提交到公开的代码仓库。如果怀疑密钥已泄露，请立即前往 DMXAPI 官网重新生成。
:::

## 模型名称

- `qwen3.8-omni-flash`

## 多轮对话示例代码

```python
from openai import OpenAI

# ===============================================================
# 步骤1: 初始化 OpenAI 客户端
# ===============================================================

client = OpenAI(
    # DMXAPI 密钥 (请替换为您自己的密钥)
    # 获取方式: 登录 DMXAPI 官网 -> 个人中心 -> API 密钥管理
    api_key="sk-******************************************",

    # DMXAPI 兼容 OpenAI SDK 的服务端点地址
    base_url="https://www.dmxapi.cn/v1",
)

# ===============================================================
# 步骤2: 配置请求参数并发送请求
# ===============================================================

# preserve_thinking 默认开启: 思考开启时，应把上一轮回复的思考内容
# 放入历史 assistant 消息的 reasoning_content 字段，随 messages 一并传回
# 传回的思考内容计入输入 Token 和费用
# 注意: messages 数组中的 assistant 消息只能包含文本数据
# 本示例开启了思考 (reasoning_effort="low")，历史 assistant 消息中携带了 reasoning_content

completion = client.chat.completions.create(
    # 【model】(string, 必填) 调用的模型名称
    model="qwen3.8-omni-flash",

    # 【reasoning_effort】(string, 可选) 思考强度，不传时默认开启思考，默认值为 "xhigh"
    # 可选值: "none"(关闭思考) / "minimal" / "low" / "medium" / "high" / "xhigh" / "max"
    # 取值映射: "minimal" 按 "low" 处理，"high" 和 "max" 按 "xhigh" 处理
    # 注意: reasoning_effort 和 thinking_budget 不能同时设置，否则请求报错
    # 本示例开启思考，使用 low 档
    reasoning_effort="low",

    # 【messages】(array, 必填) 对话消息列表，按时间顺序排列
    # 多轮对话需由客户端传入完整历史消息，音频 / 视频输入仅允许出现在 user 消息中
    messages=[
        {
            # 第一轮用户消息
            # 【role】(string, 必填) 消息角色
            # 可选值: "system"(系统提示，设定助手行为) / "user"(用户输入) / "assistant"(助手回复，用于多轮对话)
            "role": "user",

            # 【content】(array, 必填) 消息内容，对象数组形式
            "content": [
                {
                    # 【type】(string, 必填) 输入类型，此处为 "text"(文本)
                    "type": "text",

                    # 【text】(string, 必填) 文本内容
                    "text": "请介绍一下牛奶。",
                },
            ],
        },
        {
            # 第一轮模型回复 (assistant 消息只能包含文本数据)
            "role": "assistant",
            "content": [
                {
                    "type": "text",
                    "text": "牛奶是一种常见的乳制品，含有蛋白质、脂肪、钙和多种维生素。",
                },
            ],

            # 【reasoning_content】(string, 可选) 上一轮回复的思考内容
            # preserve_thinking 默认开启，思考开启时随回复一并传回
            # 传回的思考内容计入输入 Token 和费用
            "reasoning_content": "用户想了解牛奶，先给出定义，再概括主要营养成分。",
        },
        {
            # 第二轮用户消息
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": "牛奶中有哪些主要营养成分？",
                },
            ],
        },
        {
            # 第二轮模型回复
            "role": "assistant",
            "content": [
                {
                    "type": "text",
                    "text": "牛奶中主要含有蛋白质、脂肪、乳糖、钙、磷以及维生素B2等营养成分。",
                },
            ],

            # 第二轮回复的思考内容，随回复一并传回
            "reasoning_content": "用户追问营养成分，按蛋白质、脂肪、乳糖、钙和维生素分类列举。",
        },
        {
            # 第三轮用户消息
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": "哪些人适合喝牛奶？每天喝多少比较合适？",
                },
            ],
        },
    ],

    # 【modalities】(array, 可选) 输出模态
    # qwen3.8-omni-flash 仅支持文本输出，固定为 ["text"]
    modalities=["text"],

    # 【stream】(boolean, 可选) 是否使用流式输出
    stream=True,

    # 【stream_options】(object, 可选) 流式输出选项，仅在 stream=True 时生效
    stream_options={
        # 【include_usage】(boolean, 可选) 在流末尾的最后一个数据块返回 Token 用量
        "include_usage": True,
    },
)

# ===============================================================
# 步骤3: 处理流式响应
# ===============================================================

for chunk in completion:
    if chunk.choices:
        delta = chunk.choices[0].delta

        # 思考开启时，先输出思考内容 (delta.reasoning_content)
        reasoning_content = getattr(delta, "reasoning_content", None)
        if reasoning_content:
            print(reasoning_content, end="", flush=True)

        # 正式回答通过 delta.content 输出
        if delta.content:
            print(delta.content, end="", flush=True)
    else:
        # 最后一个数据块返回 Token 用量
        if chunk.usage:
            print("\n\nToken 用量：")
            print(chunk.usage)
```

## 返回示例

```text
用户继续询问关于牛奶的问题，这次问的是适合喝牛奶的人群以及每日建议饮用量。我需要根据营养学常识来回答这个问题。

关键点：
1. 适合人群：大多数人，尤其是儿童、青少年、孕妇、老年人等需要补钙的人群
2. 不适合人群：乳糖不耐受者、牛奶过敏者等
3. 每日建议量：中国居民膳食指南建议每天300-500ml

我来组织一个清晰完整的回答。
## 适合喝牛奶的人群

**推荐人群：**
- **儿童和青少年**：处于生长发育期，需要充足的蛋白质和钙质。
- **孕妇和哺乳期女性**：对钙和蛋白质的需求增加。
- **中老年人**：有助于预防骨质疏松。
- **一般成年人**：作为日常营养补充。

**不太适合的人群：**
- **乳糖不耐受者**：饮用后可能出现腹胀、腹泻等症状，可选择低乳糖奶或酸奶替代。
- **牛奶蛋白过敏者**：尤其多见于婴幼儿，应避免饮用。
- **某些消化系统疾病患者**：如急性胃肠炎期间，建议暂缓饮用。

---

## 每日建议饮用量

根据《中国居民膳食指南（2022）》的建议：

| 人群 | 每日建议量 |
|------|-----------|
| 一般成年人 | 300～500 ml |
| 儿童（学龄前） | 350～500 ml |
| 青少年 | 300～500 ml |
| 孕妇/乳母 | 300～500 ml |
| 老年人 | 300～500 ml |

---

## 小贴士

- 可以分次饮用，比如早餐一杯、睡前一杯。
- 搭配主食一起食用，吸收效果更好。
- 如果空腹喝牛奶容易不适，可以先吃点面包、饼干等再喝。
- 全脂奶、脱脂奶可根据自身健康需求选择，一般人群喝全脂奶即可。

Token 用量：
CompletionUsage(completion_tokens=437, prompt_tokens=116, total_tokens=553, completion_tokens_details=CompletionTokensDetails(accepted_prediction_tokens=None, audio_tokens=None, reasoning_tokens=100, rejected_prediction_tokens=None, text_tokens=337), prompt_tokens_details=PromptTokensDetails(audio_tokens=None, cached_tokens=0, text_tokens=116))
```

<p align="center">
  <small>© 2026 DMXAPI Qwen3.8-Omni-Flash 多轮对话</small>
</p>
