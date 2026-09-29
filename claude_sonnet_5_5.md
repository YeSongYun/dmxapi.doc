# Claude Sonnet 5.5 调整与破坏性更新

Claude Sonnet 5.5（模型名 `claude-sonnet-5-5`）于 2026 年 9 月 28 日发布，是 Claude Sonnet 5 的下一代。它比 Sonnet 5 更快，完成同样的工作通常用的 token 更少，官方定价与 Sonnet 5 相同。

不过，它也改掉了一些旧写法。在 Sonnet 5 上能正常运行的代码，有 5 处换成 Sonnet 5.5 后会直接返回 400 错误，这就是本文说的「破坏性更新」。另外还有 1 处不报错、但会让界面“变安静”的变化，以及一些默认值、安全规则和模型行为上的调整。

本文从头到尾按顺序讲，每一处变化都会说明：以前怎么写、现在会报什么错、应该怎么改。内容依据 Anthropic 官方文档整理，截至 2026 年 9 月 29 日。

::: tip
- 从 Sonnet 5 升级：按顺序读第一节到第七节。
- 从 Sonnet 4.6、Sonnet 4.5 或 Haiku 4.5 升级：还要再读第八节。
- 改完代码后，用第九节的检查清单逐项核对；遇到报错，查第十节。
:::

## 一、Sonnet 5.5 基本信息

| 项目 | 内容 |
| --- | --- |
| 模型名 | `claude-sonnet-5-5` |
| 发布日期 | 2026 年 9 月 28 日 |
| 上下文长度 | 100 万 token（1M） |
| 最大输出 | 12.8 万 token（128K） |
| 输入 / 输出 | 文本和图片 → 文本 |
| 思考（thinking） | 默认开启，由模型自己决定想多少（adaptive） |
| 默认 effort | `high` |
| 知识截止 | 2026 年 6 月 |
| 分词器 | 与 Sonnet 5 相同，同样的文字 token 数不变 |
| 官方定价 | 与 Sonnet 5 相同 |

## 二、先弄懂 5 个概念

后面的内容会反复用到下面几个词，先花两分钟看懂它们。

### 1. 思考（thinking）

模型在正式回答之前，可以先在内部“打草稿”推理一遍，这就是思考。推理的内容会以 `thinking` 块的形式出现在响应里。

Sonnet 5.5 默认使用**自适应思考（adaptive）**：简单问题可能不想，难题多想一些，由模型自己决定。你不用写任何参数，它就会思考。

### 2. effort（努力程度）

`effort` 控制模型这次回答愿意花多少 token，从低到高有五档：`low`、`medium`、`high`、`xhigh`、`max`。档位越高，想得越深、答得越细，也越慢、越贵。它写在 `output_config` 里：

```python
output_config={"effort": "medium"}
```

在 Sonnet 5.5 上，effort 是控制思考深浅的主要手段。

### 3. 响应由多个“内容块”组成

模型返回的 `response.content` 是一个列表，里面可能有几种块：

| 块类型 | 是什么 |
| --- | --- |
| `thinking` | 模型的思考内容。默认是空字符串，只带一个签名 `signature` |
| `text` | 给用户看的正文 |
| `tool_use` | 模型要调用某个工具 |

因为第一个块可能是 `thinking`，**不能直接用 `response.content[0].text` 取正文**，要按块的 `type` 来读。

### 4. 工具调用与 tool_choice

你可以给模型定义“工具”，比如查天气、查数据库，模型觉得需要时就会调用。`tool_choice` 决定模型怎么用工具：`auto` 让模型自己决定（默认值），`any` 和 `tool` 则是强制它必须调用。

### 5. beta 功能

一些新功能还在测试阶段（beta），使用时要在请求里写明开启哪个 beta。用 Python SDK 时，改为调用 `client.beta.messages.create`，并传入 `betas` 参数：

```python
client.beta.messages.create(..., betas=["beta 名称"])
```

## 三、先跑通一个最基本的请求

下面这个请求可以直接在 Sonnet 5.5 上运行：

```python
import anthropic

client = anthropic.Anthropic(
    api_key="YOUR_DMXAPI_KEY",
    base_url="https://www.dmxapi.cn",
)

response = client.messages.create(
    model="claude-sonnet-5-5",
    max_tokens=16000,                    # 思考也算在里面，要留足
    output_config={"effort": "medium"},
    messages=[
        {"role": "user", "content": "用三句话解释什么是微服务架构"}
    ],
)

print("停止原因:", response.stop_reason)

# 按块的类型读取，只打印正文
for block in response.content:
    if block.type == "text":
        print(block.text)
```

几点说明：

- 没有写 `thinking` 参数，模型也会自动思考。
- `max_tokens` 限制的是“思考 + 正文”的总长度，思考用的 token 也按输出计费。设得太小，正文可能被截断。
- 这个请求**故意没有写**下面五样东西，它们在 Sonnet 5.5 上都会返回 400：
  1. 思考预算 `budget_tokens`
  2. 非默认的 `temperature`、`top_p`、`top_k`
  3. 预填 assistant 回复（prefill）
  4. 强制工具调用
  5. `thinking: {"type": "disabled"}`

  前三样在 Sonnet 5 上就已经不能用了，只有从更老的模型升级才会遇到，在第八节讲；后两样是 Sonnet 5.5 新增的限制，在下一节讲。

## 四、五个破坏性更新

下面五处写法在 Sonnet 5 上可以正常运行，换成 Sonnet 5.5 后会返回 400 错误。前三处建议每个项目都检查一遍；后两处只影响用到相关功能的项目。

### 1. 关闭思考：不能再用 disabled，改用 between_tools

**以前（Sonnet 5）**：想让模型不思考、直接回答，写 `thinking={"type": "disabled"}`。

**现在（Sonnet 5.5）**：`disabled` 在任何情况下都会返回 400，报错如下：

```text
"thinking.type.disabled" is not supported for this model. Use "thinking.type.between_tools" for the lowest thinking setting, or "thinking.type.adaptive" and "output_config.effort" to control thinking behavior.
```

**怎么改**：改成 `thinking={"type": "between_tools"}`。这是 Sonnet 5.5 最低的思考档，模型回答前不做思考。如果请求里带了工具，模型在两次工具调用之间写的简短进度说明，仍会以 `thinking` 块返回（带文字）；如果没带工具，响应里就只有正文，效果和以前的 `disabled` 一样。

改之前：

```python
response = client.messages.create(
    model="claude-sonnet-5",
    max_tokens=16000,
    thinking={"type": "disabled"},
    output_config={"effort": "xhigh"},
    messages=[{"role": "user", "content": "..."}],
)
```

改之后：

```python
response = client.messages.create(
    model="claude-sonnet-5-5",
    max_tokens=16000,
    thinking={"type": "between_tools"},
    output_config={"effort": "high"},    # 注意：最高只能到 high
    messages=[{"role": "user", "content": "..."}],
)
```

`between_tools` 有四条规则，违反任何一条都会返回 400：

1. **effort 只能是 `low`、`medium` 或 `high`。** 上面的例子原来用的是 `xhigh`，所以除了换成 `between_tools`，还要把 effort 降到 `high`，否则会报：

   ```text
   output_config.effort 'xhigh' is not supported when thinking is disabled on this model. Use effort 'high' or below, or enable thinking.
   ```

2. **`thinking` 里不能再写别的字段**，比如 `display`、`budget_tokens`。
3. **对话中途不能改 effort。** “逐消息 effort”这个新功能在第七节介绍，它和 `between_tools` 不能一起用。
4. **只有 Sonnet 5.5 认识 `between_tools`。** 如果你的代码出错时会把同一个请求换个模型重发，要先删掉这个字段，否则会报：

   ```text
   "thinking.type.between_tools" is not supported for this model.
   ```

::: warning
下面三种情况不要用 `between_tools`，改用默认的自适应思考（不写 `thinking`，或写 `{"type": "adaptive"}`）：

- 不带工具、但需要几步推导的任务，比如汇总数字、按规则判断、排序，特别是要求输出 JSON 时。`between_tools` 下模型不先想就作答，准确率会下降。
- 需要用 `xhigh` 或 `max` 档。
- 需要在对话中途调整 effort。
:::

::: tip
- 如果只是想让回答快一点、省一点，也可以不关思考，直接把 effort 调到 `low`：这一档下，模型遇到简单问题通常会跳过思考。
- 提示词里“不要思考”之类的指令要删掉。官方说明，这类指令会让模型更容易在正文里写出内部的 XML 标签。
:::

### 2. 强制工具调用不能用了

**以前**：想让模型必须调用工具，写 `tool_choice={"type": "tool", "name": "get_weather"}`（必须调用这个工具）或 `tool_choice={"type": "any"}`（必须调用任意一个工具）。

**现在**：这两种写法都会返回 400，连计算 token 数的接口 `/v1/messages/count_tokens` 也一样：

```text
tool_choice: type "tool" and "any" are not supported for this model.
```

`{"type": "auto"}`（默认值，让模型自己决定）和 `{"type": "none"}`（不调用工具）照常可用。

**怎么改**：分两种情况。

**情况一：你确实需要模型调用工具。** 改用 `auto`，并做三件事：

1. 在提示词里直接说明要用哪个工具，例如“请使用 get_weather 工具查询”。
2. 给工具加上 `"strict": True`，保证模型传入的参数符合你定义的格式。
3. 在代码里检查模型有没有真的调用工具。`auto` 模式下模型也可以选择不调用，没调用就重试。

```python
tools = [
    {
        "name": "get_weather",
        "description": "查询指定城市的当前天气",
        "input_schema": {
            "type": "object",
            "properties": {
                "location": {"type": "string", "description": "城市名，例如：北京"}
            },
            "required": ["location"],
            "additionalProperties": False,    # 使用 strict 时必须写
        },
        "strict": True,
    }
]

response = client.messages.create(
    model="claude-sonnet-5-5",
    max_tokens=4096,
    tools=tools,
    tool_choice={"type": "auto"},
    messages=[
        {"role": "user", "content": "北京今天天气怎么样？请使用 get_weather 工具查询。"}
    ],
)

# auto 模式不保证一定调用工具，要自己检查
called = any(block.type == "tool_use" for block in response.content)
if not called:
    print("模型没有调用工具，可以重试，或直接使用它的文字回答")
```

**情况二：强制调用工具只是为了拿到固定格式的 JSON。** 那就不必用工具了，改用结构化输出：在 `output_config.format` 里写好 JSON 格式，模型的回复就会严格符合这个格式。

```python
import json

response = client.messages.create(
    model="claude-sonnet-5-5",
    max_tokens=4096,
    output_config={
        "format": {
            "type": "json_schema",
            "schema": {
                "type": "object",
                "properties": {
                    "city": {"type": "string"},
                    "summary": {"type": "string"},
                },
                "required": ["city", "summary"],
                "additionalProperties": False,
            },
        }
    },
    messages=[{"role": "user", "content": "从这段话里提取城市，并用一句话概括：..."}],
)

# 正文就是符合格式的 JSON 字符串
for block in response.content:
    if block.type == "text":
        data = json.loads(block.text)
        print(data["city"], data["summary"])
```

::: info
使用 strict 的注意事项：schema 里每个 object 都要写 `"additionalProperties": False`；一个请求最多 20 个 strict 工具。
:::

### 3. thinking 块和模型、对话、账号绑定在一起

这一处最容易出问题，我们慢慢讲。

先回顾一下多轮对话是怎么进行的：每一轮请求，你都要把之前的全部消息（包括模型上一轮返回的内容）一起发给模型。模型返回的 `thinking` 块里，除了思考内容，还有一个 `signature`（签名）字段。

在 Sonnet 5.5 上，这个签名就像一张封条，记下了三件事：

- 这个块是哪个模型写的；
- 它前面的对话内容是什么；
- 它属于哪个账号。

你把它发回来时，API 会逐一核对，由此产生三条规则。

**规则一：换了模型，之前的思考会被丢掉。**

Sonnet 5.5 的 thinking 块，其他任何模型都读不了。如果一段对话中途从 Sonnet 5.5 换到别的模型（比如出错后换个模型重试），这些块会被自动丢掉：请求不报错，丢掉的部分也不计费，但新模型就看不到之前的推理了。

反过来，Sonnet 5.5 能读 Sonnet 5、Opus 4.8、Haiku 4.5 以及更早模型的块，所以从 Sonnet 5 切到 Sonnet 5.5 的对话，推理会保留下来。Opus 5、Opus 5.5 以及 Fable、Mythos 系列的块，Sonnet 5.5 读不了。

**规则二：改过前面的对话，再发回 thinking 块会报错。**

API 会检查每个 thinking 块“前面的内容”有没有被改过，包括 `system` 提示词、`tools` 工具列表和之前的每一条消息。官方对 2026 年 8 月 31 日及之后创建的账号默认开启这项检查，发现改过就返回 400：

```text
messages.1.content.0: Invalid `signature` in `thinking` block. The block is bound to a different conversation. Remove the block, or set `thinking.block_binding.prefix_mismatch_behavior` to "drop_block".
```

**规则三：换了账号，之前的思考会被丢掉。**

Sonnet 5.5 的 thinking 块，只在生成它的账号（或与之关联的账号）里有效。用别的账号发送时，这些块会被自动丢掉，请求照常成功。

**怎么做才不会出问题**：记住一句话，**对话历史只追加，不修改**。

1. 每一轮都把 `response.content` 原封不动地追加到 `messages` 里，包括 `thinking` 块，即使它的内容是空的。
2. 不要编辑、删除、调换前面的任何消息。
3. 同一段对话里，`system` 提示词和 `tools` 工具列表保持不变。
4. 需要中途追加指令时，在末尾加一条 `role` 为 `system` 的消息（第七节介绍），不要去改最前面的 `system`。

下面是正确的多轮对话写法：

```python
messages = [{"role": "user", "content": "帮我规划一个三天的北京旅行路线"}]

response = client.messages.create(
    model="claude-sonnet-5-5",
    max_tokens=16000,
    messages=messages,
)

# 正确：把整个 content 原样追加，而不是只取其中的文字
messages.append({"role": "assistant", "content": response.content})

# 下一轮：只在末尾追加新消息
messages.append({"role": "user", "content": "第二天改成去长城"})

response = client.messages.create(
    model="claude-sonnet-5-5",
    max_tokens=16000,
    messages=messages,
)
```

::: warning
下面这些常见写法，在 Sonnet 5.5 上都会让之前的 thinking 块失效：

- 只把回复里的文字取出来存进历史；
- 每一轮重新生成 system 提示词，比如在里面写上当前时间；
- 为了省 token，在客户端删掉旧的工具结果或旧的轮次。
:::

**已经报错了怎么办**：先把历史里所有 `thinking` 块删掉（其他内容保留），再重试一次，之后也不要再把它们放回去。然后找到修改历史的那段代码，改成只追加。

::: info
进阶做法：使用自适应思考时，可以让 API 自动丢掉失效的 thinking 块，而不是报错。需要开启 beta `thinking-binding-controls-2026-08-01`：

```python
response = client.beta.messages.create(
    model="claude-sonnet-5-5",
    max_tokens=16000,
    thinking={
        "type": "adaptive",
        "block_binding": {"prefix_mismatch_behavior": "drop_block"},
    },
    messages=messages,
    betas=["thinking-binding-controls-2026-08-01"],
)
```

`block_binding` 只能和 `adaptive` 一起用，和 `between_tools` 一起写会返回 400。这个办法只是不再报错，被丢掉的推理并不会回来，根本的解决办法还是让历史只追加。
:::

### 4. computer use（操作电脑）要换成新的工具集

没用到 computer use 的项目可以跳过这一小节。

computer use 是让模型看屏幕截图、操作鼠标和键盘的工具。

**以前**：声明 `computer_20251124` 工具，并开启 beta `computer-use-2025-11-24`。

**现在**：Sonnet 5.5 只接受新的工具集 `computer_toolset_20260801`，旧工具会返回 400，报错开头是：

```text
'claude-sonnet-5-5' does not support tool types: computer_20251124.
```

更老的 `computer_20250124` 同样不再接受。

**第一步：改请求。**

改之前：

```python
response = client.beta.messages.create(
    model="claude-sonnet-5",
    max_tokens=4096,
    betas=["computer-use-2025-11-24"],
    tools=[{
        "type": "computer_20251124",
        "name": "computer",
        "display_width_px": 1024,
        "display_height_px": 768,
    }],
    messages=[{"role": "user", "content": "打开显示设置"}],
)
```

改之后：

```python
response = client.messages.create(
    model="claude-sonnet-5-5",
    max_tokens=4096,
    tools=[{"type": "computer_toolset_20260801"}],    # 不用 beta，也不写 name 和屏幕尺寸
    messages=[{"role": "user", "content": "打开显示设置"}],
)
```

**第二步：改处理动作的代码。** 新工具集的返回格式变了：

1. 动作名直接写在 `tool_use` 块的 `name` 里，比如 `screenshot`、`left_click`、`type`，不再放在 `input.action` 里。
2. 模型一次可能返回好几个动作。要按顺序逐个执行，并为每个动作各回一个 `tool_result`，全部放在下一条 user 消息里。
3. 每个 `tool_result` 都要带上 `"toolset_name": "computer"`，漏了会被拒绝。只有截图、放大这类动作需要返回图片，其他动作回一个 `OK` 即可。
4. 某个动作执行失败时，后面的动作不要再执行，每个都返回 `is_error: true`，内容写 `Not executed: an earlier computer action in this turn failed.`
5. 截图大小要自己控制，长边不超过 2576 像素。API 不会帮你缩小，图片太大会直接报错。

```python
# 回复一轮中的多个动作（示意）
{"role": "user", "content": [
    {"type": "tool_result", "tool_use_id": "toolu_01...", "toolset_name": "computer",
     "content": [{"type": "text", "text": "OK"}]},
    {"type": "tool_result", "tool_use_id": "toolu_02...", "toolset_name": "computer",
     "content": [{"type": "image", "source": {"type": "base64", "media_type": "image/png", "data": "..."}}]},
]}
```

::: warning
- 如果请求里带着 beta `fine-grained-tool-streaming-2025-05-14`，要删掉，它和新工具集一起用会返回 400。
- 不要为了省 token 在客户端删掉旧截图。这属于修改历史，会让之后的 thinking 块失效，原因见上一小节。
:::

### 5. advisor（顾问）工具能用的顾问变少了

没用到 advisor 工具的项目可以跳过这一小节。

advisor 工具让干活的模型（执行模型）在工作过程中，去请教一个更强的顾问模型。顾问只出主意、不干活：它看完整段对话后给出建议，执行模型再接着干。

**以前**：Sonnet 5 作执行模型时，可以用 Opus 4.8、Opus 4.7、Sonnet 5 当顾问。

**现在**：Sonnet 5.5 作执行模型时，这三个顾问都会返回 400。能用的顾问只有 7 个：Opus 5、Opus 5.5、Fable 5、Fable 5.1、Mythos 5、Mythos 5.1，以及 Sonnet 5.5 自己。

改之前：

```python
response = client.beta.messages.create(
    model="claude-sonnet-5",
    max_tokens=4096,
    betas=["advisor-tool-2026-03-01"],
    tools=[{"type": "advisor_20260301", "name": "advisor", "model": "claude-opus-4-8"}],
    messages=[{"role": "user", "content": "..."}],
)
```

改之后：

```python
response = client.beta.messages.create(
    model="claude-sonnet-5-5",
    max_tokens=4096,
    betas=["advisor-tool-2026-03-01"],
    tools=[{"type": "advisor_20260301", "name": "advisor", "model": "claude-opus-5-5"}],
    messages=[{"role": "user", "content": "..."}],
)
```

::: info
- 换成新顾问后，顾问的建议会以加密形式返回（`advisor_redacted_result` 块）：执行模型能读，你的程序读不到建议原文。如果你的界面以前展示过顾问的建议，这部分要去掉。
- 不能再用 `tool_choice` 强制模型去问顾问（见本节第 2 点），要在提示词里引导它。
:::

## 五、不报错，但界面会“变安静”

这一处变化不会让请求报错。但如果你的产品会把模型的中间说明展示给用户看，就要注意了。

**以前**：模型在两次工具调用之间写的说明，比如“已找到问题，下一步修改 auth.py”，以 `text` 块返回，界面可以直接显示。

**现在**：超过一两句话的说明，改为以 `thinking` 块返回，官方叫它“进度说明”。默认情况下 `thinking` 块的内容是空的，所以只显示 `text` 块的界面，在模型连续调用工具时会一直没有动静。

**怎么改**：两种方法任选一种。

**方法一：使用自适应思考时，开启 `display: "updates"`（beta）。** 思考内容仍然隐藏，但进度说明会以文字返回：

```python
response = client.beta.messages.create(
    model="claude-sonnet-5-5",
    max_tokens=16000,
    thinking={"type": "adaptive", "display": "updates"},
    tools=tools,
    messages=messages,
    betas=["thinking-display-updates-2026-08-18"],
)

for block in response.content:
    if block.type == "thinking" and block.thinking:    # 内容不为空的 thinking 块就是进度说明
        print("[进度]", block.thinking)
    elif block.type == "text":
        print(block.text)
```

如果把 `display` 设成 `"summarized"`，也能拿到进度说明，不过会和思考摘要混在一起，分不出来。

**方法二：使用 `between_tools`。** 这时进度说明会自动带文字返回，不需要、也不能设置 `display`。

不管用哪种方法，都要注意两点：

- 进度说明块和其他 thinking 块一样，要原样放回对话历史。
- 如果回复因为 `max_tokens` 用完等原因中途停止，最后一个进度说明块的文字可能是 `This part of the response was interrupted before it finished.`，表示这部分工作还没做完。要继续的话，把这一轮回复原样放回历史，再追加一条新的 user 消息。

::: tip
如果界面还是太久没有动静，可以在 system 提示词里写明希望模型什么时候汇报，比如开始前说一句要做什么、结束时给个简短总结，模型会照做。
:::

## 六、其他需要知道的调整

### 1. effort 档位重新校准

默认值还是 `high`，但同一档位的思考量和 Sonnet 5 不一样了。官方建议重新测试，不要直接沿用 Sonnet 5 的设置。官方给出的起点如下：

| 场景 | 建议的起始 effort |
| --- | --- |
| 一般任务 | `high` |
| 编程 agent、多步工具调用（任务描述清楚的） | `medium` |
| 编程 agent、多步工具调用（更难或更长的） | `high` |
| 聊天等需要快速响应的场景 | `medium` 或 `low` |
| `xhigh`、`max` | 只在测试证明效果确实更好时使用 |

几个要点：

- **想让模型少想，就降低 effort。** 从 `medium` 档起，模型几乎每次回答前都会先想一下，连打招呼也是，所以第一个字出来得会慢一些。在提示词里要求“少思考”没有可靠效果；`low` 档下，简单问题通常会跳过思考。
- **`max_tokens` 要给思考留出空间。** 思考也计入 `max_tokens`。做编程 agent 时，官方建议直接设为 128000（模型上限），并使用流式输出：

  ```python
  with client.messages.stream(
      model="claude-sonnet-5-5",
      max_tokens=128000,
      output_config={"effort": "medium"},
      messages=messages,
  ) as stream:
      response = stream.get_final_message()
  ```

- **不同产品的默认值不一样。** 通过 API 调用时默认是 `high`；在 Claude Code 和 Claude 应用里默认是 `medium`。

### 2. 可能收到“拒答”：先检查 stop_reason

Sonnet 5.5 带有安全分类器，遇到某些请求会拒绝回答。拒答不会报错：HTTP 状态码仍然是 200，但 `stop_reason` 是 `"refusal"`，`content` 为空。所以**读取正文之前，先检查 `stop_reason`**：

```python
response = client.messages.create(
    model="claude-sonnet-5-5",
    max_tokens=16000,
    messages=messages,
)

if response.stop_reason == "refusal":
    category = response.stop_details.category if response.stop_details else None
    print("请求被拒绝，类别：", category)
else:
    for block in response.content:
        if block.type == "text":
            print(block.text)
```

`stop_details.category` 表示拒答的类别，一共 5 种：

| 类别 | 含义 |
| --- | --- |
| `cyber` | 可能帮助网络攻击，比如编写恶意软件、漏洞利用。在源代码里找漏洞是允许的 |
| `bio` | 可能造成生物危害，比如危险的实验方法。日常健康、教育类问题不受影响 |
| `frontier_llm` | 可能帮助开发与之竞争的 AI 模型 |
| `reasoning_extraction` | 要求模型把内部推理过程写进回答正文 |
| `general_harms` | 属于其他使用政策范围，正常请求偶尔也会触发 |

拒答没有对应到具体类别时，`category` 为 `null`，这是正常情况。

::: tip
- 提示词里如果要求模型“把推理过程写出来”，要删掉，否则容易触发 `reasoning_extraction` 拒答。需要看推理过程时，改用 `thinking={"type": "adaptive", "display": "summarized"}`，从 thinking 块里读取思考摘要。
- 官方还提供了自动回退功能：请求被拒答时，自动换一个模型重试。对 Sonnet 5.5 来说，只有 `cyber` 和 `frontier_llm` 两类会回退到 Sonnet 5，其余三类不会回退。
:::

### 3. 缓存门槛降低

提示词缓存（prompt caching）可以让重复发送的长前缀更便宜、更快。Sonnet 5.5 能缓存的最短长度，从 Sonnet 5 的 1024 token 降到了 512 token。以前因为太短而没法缓存的提示词，现在可能可以缓存了。

### 4. 模型行为的几处变化

下面这些变化不会报错，但可能让效果和以前不一样。每一条都附上了官方建议的处理办法，其中的提示词是官方原文，可以直接复制到 system 提示词里使用。

**编程任务没做完，就停下来问你。** 在 `low` 和 `medium` 档，模型有时会中途停下来确认计划，或者做完一部分就问要不要继续。先试试提高 effort；不想提高的话，加上：

```text
Keep working until everything the user asked for is done, and only stop to ask when you can't go on without the user or before a risky step.

When the work the user asked for is done and checked, stop and report. Don't add features, tests, files, docs or refactors that weren't asked for. If you think one would help, mention it at the end instead of doing it.
```

**主动加上你没要求的测试、文档。** 各档位都有这个倾向，档位越高越明显。如果只想要你明确要求的改动，只加上面提示词的第二段（以 “When the work the user asked for is done” 开头的那段）。

**`xhigh`、`max` 档会自己反复复查。** 做完任务后，模型会主动再做几轮检查，甚至启动子 agent 来审查，花掉更多时间和 token。日常任务用 `high` 或更低档即可。想保留高档位、又不想让它自己加复查，加上：

```text
When the work the user asked for is done and its checks pass, stop and report. Don't start extra rounds of review or hardening on your own, and don't launch reviewer sub-agents unless the user asked for a review. If you think a deeper review is worth doing, say so at the end.
```

**只想要点子，它却直接开干。** 比如你问“这个能做什么”，它可能直接开始做演示稿或报告。加上：

```text
When the user asks for ideas, options or a plan, give them that and stop. Don't start building or changing anything until they say to go ahead.
```

**需要推导的 JSON 任务，答案可能不准。** 比如汇总文档里的数字，在 `low`、`medium` 档，模型常常不先思考就直接给出 JSON。使用自适应思考，并在 system 提示词末尾加上这一句：

```text
Think the problem through before you answer.
```

另外，如果回复因为 `max_tokens` 用完而停止（`stop_reason` 为 `"max_tokens"`），即使内容看起来是完整的 JSON，也要当作失败，重新请求一次。

**有搜索工具却不用，凭记忆回答。** 先删掉提示词里“尽量少用工具”之类的话，模型会照字面执行。然后加上：

```text
Use the search tool to check specifics that may have changed since your training, such as what is allowed, required or charged, even when you feel confident. For researched work such as a report or a comparison, gather current sources rather than writing from your training knowledge.
```

**用户中途插的话，可能被当成可疑内容。** 模型会防范藏在工具结果里的恶意指令（提示词注入），有时会误伤真正的用户消息。所以不要把用户的话放进 `tool_result` 块里，而是放在同一条 user 消息中、最后一个 `tool_result` 之后，作为单独的 text 块：

```python
{"role": "user", "content": [
    {"type": "tool_result", "tool_use_id": "toolu_01...", "content": "测试全部通过"},
    {"type": "text", "text": "另外，顺便把更新日志也改一下"},    # 用户中途说的话放这里
]}
```

**`low` 档编程时，可能没测试就说做完了。** 加上：

```text
When you change code that can be run, built, or type-checked, run a real check that exercises the change before reporting it done: the project's tests, type-checker, or build, or the changed command itself. A syntax-only check, or a check command that failed to start, does not count; if all that is missing is the project's declared dependencies, install them with its own package manager and lockfile (e.g. npm install, pip install -r requirements.txt), never via sudo or the system package manager, unless told not to. Only if no real check can run here, say which one you did not run and why instead of reporting the change as done.
```

**工具名的大小写偶尔写错。** 比如把 `Bash` 写成 `bash`。不要直接报错中断：能确定是哪个工具就照常执行；或者返回一个 `is_error: true` 的 `tool_result`，写明正确的名字，模型下一轮通常会改正。

**看复杂图表、技术图纸不够准。** 给模型一个能裁剪、放大图片的工具。对图表来说，这比提高 effort 更有效。

## 七、新增的功能

下面这些功能在 Sonnet 5 上用不了，在 Sonnet 5.5 上可以用。它们的共同目的是：**不修改对话历史，也能调整指令、工具和 effort**。这样既保住了缓存，也不会让 thinking 块失效。除了第一个，其余都是 beta 功能。

| 功能 | 作用 | beta 名称 |
| --- | --- | --- |
| 对话中途的 system 消息 | 在对话中间追加一条指令，从这里开始生效 | 不需要 |
| 对话中途增删工具 | 在对话中途开放或收回某个工具 | `inline-tools-2026-09-15` |
| 在消息里定义工具 | 对话中途加入一个开头时没有的新工具 | `inline-tools-2026-09-15` |
| 逐消息 effort | 对话中途调整 effort，缓存不受影响 | `mid-conversation-output-config-2026-07-01` |
| 只在当前轮生效的 system 消息 | 发一条只管这一轮的提醒，之后自动失效 | `mid-conversation-system-clear-at-2026-08-21` |
| `display: "updates"` | 只返回进度说明，思考内容保持隐藏（见第五节） | `thinking-display-updates-2026-08-18` |
| 任务预算（task budgets） | 给整个 agent 任务一个 token 预算，模型据此安排节奏，最少 20000 | `task-budgets-2026-03-13` |

最常用的是第一个，而且不需要 beta：在 `messages` 末尾加一条 `role` 为 `system` 的消息即可。

```python
messages = [
    {"role": "user", "content": "帮我审查 utils.py 里的 process() 函数"},
    {"role": "assistant", "content": "..."},    # 上一轮模型的回复，原样保留
    {"role": "user", "content": "再看看调用它的代码"},
    {"role": "system", "content": "从现在开始，所有代码建议都要带上类型注解。"},
]

response = client.messages.create(
    model="claude-sonnet-5-5",
    max_tokens=16000,
    system="你是一个代码审查助手，回答要简洁。",    # 最前面的 system 保持不变
    messages=messages,
)
```

::: warning
对话中途的 system 消息有位置要求：必须紧跟在一条 user 消息后面，并且要么是最后一条消息，要么后面紧跟着 assistant 回复。它不能放在第一条，也不能插在 `tool_use` 和对应的 `tool_result` 之间，放错位置会返回 400。
:::

逐消息 effort 也很实用：加一条内容为空、只带 `output_config` 的 system 消息，从下一条 user 消息开始就换成新的档位。它需要自适应思考，不能和 `between_tools` 一起用。

```python
messages = [
    {"role": "user", "content": "..."},
    {"role": "assistant", "content": "..."},
    {"role": "system", "content": [], "output_config": {"effort": "high"}},    # 从下一轮起用 high
    {"role": "user", "content": "这个问题比较难：..."},
]

response = client.beta.messages.create(
    model="claude-sonnet-5-5",
    max_tokens=16000,
    output_config={"effort": "low"},    # 整段对话原本用 low
    messages=messages,
    betas=["mid-conversation-output-config-2026-07-01"],
)
```

## 八、从更老的模型升级

如果你是从 Sonnet 4.6、Sonnet 4.5 或 Haiku 4.5 升级，除了前面七节，还要处理下面这些变化。这些限制在 Sonnet 5 上就已经存在，所以从 Sonnet 5 升级的项目可以跳过这一节。

### 1. 从 Sonnet 4.6 或更早的模型升级

**不写 thinking 也会思考。** 以前不写 `thinking` 参数，模型就不思考；现在默认会思考，响应开头可能出现 `thinking` 块。所以要做三件事：按块的 `type` 读取正文；把 thinking 块原样放回历史；调大 `max_tokens`，给思考留出空间。

**思考预算 budget_tokens 会报错。** 以前的写法 `thinking={"type": "enabled", "budget_tokens": 10000}` 会返回 400：

```text
"thinking.type.enabled" is not supported for this model. Use "thinking.type.adaptive" and "output_config.effort" to control thinking behavior.
```

改成自适应思考加 effort。预算和 effort 之间没有固定的换算关系，建议用两三个档位分别测试效果：

```python
# 改之前
thinking={"type": "enabled", "budget_tokens": 10000}

# 改之后
thinking={"type": "adaptive"}
output_config={"effort": "high"}    # 也可以是 low、medium、xhigh、max
```

**temperature、top_p、top_k 会报错。** 设置成非默认值就会返回 400，直接删掉即可。想调整语气或风格，写在提示词里。

**思考内容默认不返回。** thinking 块的内容默认是空字符串。需要展示思考摘要时，设置 `thinking={"type": "adaptive", "display": "summarized"}`。

**同样的文字，token 数多约 30%。** Sonnet 5.5 使用新的分词器，和 Sonnet 4.6、Sonnet 4.5、Haiku 4.5 相比，同样的文字大约多出 30% 的 token（具体取决于内容）。要重新估算 `max_tokens` 和成本，可以用 `/v1/messages/count_tokens` 接口实际计数。

**图片消耗的 token 可能更多。** Sonnet 5.5 支持更高分辨率的图片：长边最多 2576 像素，每张最多约 4784 个 token；以前最多 1568 像素、1568 个 token。一张 2000×1500 的图片，token 大约是以前的 2.5 倍。不需要高清细节时，发送前先把图片缩小。

**新增网络安全方面的拒答。** 以前不会遇到这类拒答，处理方法见第六节第 2 点。

### 2. 从 Sonnet 4.5 或更早的模型升级

**预填（prefill）会报错。** 以前可以在 `messages` 的最后放一条 assistant 消息，让模型接着往下写。现在会返回 400：

```text
This model does not support assistant message prefill. The conversation must end with a user message.
```

按原来的用途替换：

| 原来用 prefill 做什么 | 现在的做法 |
| --- | --- |
| 控制输出格式，比如让回复以 `{` 开头输出 JSON | 使用结构化输出 `output_config.format`（写法见第四节第 2 点） |
| 跳过开场白 | 在 system 提示词里要求直接回答 |
| 避免不必要的拒答 | 在 user 消息里把要求写清楚，通常就够了 |
| 续写被中断的回答 | 放到 user 消息里，例如 “Your previous response was interrupted and ended with `[previous_response]`. Continue from where you left off.” |
| 提醒上下文 | 放进 user 消息 |

**output_format 参数已弃用。** 改用 `output_config.format`。如果继续用 `output_format`，必须开启 beta `structured-outputs-2025-11-13`，否则返回 400。

**旧版 computer use 工具 `computer_20250124` 不再支持。** 改法见第四节第 4 点。

**工具参数要用 JSON 解析器处理。** 工具调用参数里字符的转义方式可能和以前不同，要用 `json.loads` 这类标准方法解析，不要直接对原始字符串做匹配。

**要显式设置 effort。** Sonnet 4.5 没有 effort 参数，升级后记得在 `output_config` 里写上。

**清理旧的 beta。**

- 删掉上下文窗口相关的 beta，1M 上下文已经不需要 beta。
- 删掉 `interleaved-thinking-2025-05-14`，现在工具调用之间会自动思考。
- `fine-grained-tool-streaming-2025-05-14` 换成在需要的工具定义上写 `"eager_input_streaming": True`。

### 3. 从 Sonnet 4 或 Claude 3.7 Sonnet 升级

- 工具版本更新：文本编辑工具用 `text_editor_20250728`（工具名 `str_replace_based_edit_tool`，没有 `undo_edit` 命令）；代码执行工具用 `code_execution_20260521`。
- 处理两种停止原因：`refusal`（拒答）和 `model_context_window_exceeded`（上下文用满）。
- 工具调用的字符串参数会保留结尾的换行符，检查依赖这一点的代码。
- 删掉旧的 beta：`token-efficient-tools-2025-02-19`、`output-128k-2025-02-19`。
- 对照官方的提示词最佳实践，把提示词检查一遍。

### 4. 从 Haiku 4.5 升级

先做完上面第 1、2 小节（第 3 小节不用做），再做下面几项：

- 模型名 `claude-haiku-4-5-20251001`（或 `claude-haiku-4-5`）改成 `claude-sonnet-5-5`。
- 单价更高，同样的文字 token 也更多，要重新估算成本。
- 能缓存的最短长度从 4096 token 降到 512 token，以前太短缓存不了的提示词，现在可以缓存了。
- 工具调用之间的思考会自动进行，不需要开启任何 beta。
- Sonnet 5.5 能读 Haiku 4.5 的 thinking 块，从 Haiku 升到 Sonnet 5.5 的对话能保留推理；反过来，从 Sonnet 5.5 降回 Haiku 4.5，Sonnet 5.5 的 thinking 块会被丢掉。

## 九、升级检查清单

下面是官方迁移检查清单，共 30 项，分成 5 组。从第 1 组往下做，做到你的起始模型对应的那一组为止：

| 起始模型 | 要做的组 |
| --- | --- |
| Sonnet 5 | 第 1 组 |
| Sonnet 4.6 | 第 1、2 组 |
| Sonnet 4.5 | 第 1、2、3 组 |
| Sonnet 4、Claude 3.7 Sonnet | 第 1、2、3、4 组 |
| Haiku 4.5 | 第 1、2、3、5 组 |

**第 1 组：所有项目都要做（10 项）**

1. 模型名改成 `claude-sonnet-5-5`，没有日期后缀。
2. 按 `type` 读取内容块，thinking 块原样放回历史。
3. 需要关闭思考时，改用 `between_tools`，effort 不超过 `high`。
4. 强制工具调用改成 `auto` 加 strict 工具。
5. 对话历史只追加、不修改。
6. computer use 换成 `computer_toolset_20260801`，并删掉 `fine-grained-tool-streaming-2025-05-14`。
7. advisor 工具换成支持的顾问，并接受顾问建议是加密的。
8. 从 thinking 块读取工具调用之间的说明文字。
9. 处理拒答，按需配置回退。
10. 重新测试 effort 档位，重新估算成本。

**第 2 组：从 Sonnet 4.6 或更早升级（5 项）**

11. 不写 thinking 也会思考，调大 `max_tokens`。
12. 思考预算 `budget_tokens` 改成 effort。
13. 删掉非默认的 `temperature`、`top_p`、`top_k`。
14. 需要展示思考内容时，设置 `display: "summarized"`。
15. 重新计算 token 数，重新估算图片的 token。

**第 3 组：从 Sonnet 4.5 或更早升级（7 项）**

16. 替换 prefill。
17. 用标准 JSON 解析器处理工具参数。
18. 把 `computer_20250124` 换成新的工具集。
19. 显式设置 `output_config.effort`。
20. 删掉上下文窗口相关的 beta。
21. 删掉 `interleaved-thinking-2025-05-14`，把 `fine-grained-tool-streaming-2025-05-14` 换成 `eager_input_streaming`。
22. `output_format` 改成 `output_config.format`。

**第 4 组：从 Sonnet 4 或 Claude 3.7 Sonnet 升级（5 项）**

23. 工具版本更新到 `text_editor_20250728` 和 `code_execution_20260521`。
24. 处理 `refusal` 和 `model_context_window_exceeded` 两种停止原因。
25. 检查工具字符串参数结尾的换行符。
26. 删掉 `token-efficient-tools-2025-02-19` 和 `output-128k-2025-02-19`。
27. 检查一遍提示词。

**第 5 组：只针对 Haiku 4.5（3 项）**

28. 替换 `claude-haiku-4-5-20251001` 或它的别名 `claude-haiku-4-5`。
29. 按更高的单价重新估算成本。
30. 检查以前因为太短而没法缓存的提示词。

## 十、常见报错速查

| 报错信息 | 原因 | 解决办法 |
| --- | --- | --- |
| `"thinking.type.disabled" is not supported for this model...` | 用了 `thinking: disabled` | 改用 `between_tools`，或者不写 thinking、调低 effort |
| `"thinking.type.enabled" is not supported for this model...` | 用了思考预算 `budget_tokens` | 改用自适应思考加 effort |
| `output_config.effort 'xhigh' is not supported when thinking is disabled...` | `between_tools` 配了 `xhigh` 或 `max` | effort 降到 `high` 及以下，或改用自适应思考 |
| `...effort cannot change when thinking is disabled on this model...` | `between_tools` 下中途改了 effort | 删掉逐消息 effort，或改用自适应思考 |
| `"thinking.type.between_tools" is not supported for this model.` | 把 `between_tools` 发给了其他模型 | 换模型之前先删掉这个字段 |
| `tool_choice: type "tool" and "any" are not supported for this model.` | 强制工具调用 | 改用 `auto` 加 strict |
| ``Invalid `signature` in `thinking` block. The block is bound to a different conversation...`` | 改过对话历史后，又发回了 thinking 块 | 历史只追加；临时可以删掉所有 thinking 块再重试一次 |
| `'claude-sonnet-5-5' does not support tool types: computer_20251124.` | 用了旧版 computer use 工具 | 换成 `computer_toolset_20260801` |
| `This model does not support assistant message prefill...` | 用了预填（prefill） | 按用途替换，见第八节第 2 点 |

另外还有两种情况也会返回 400，但官方没有公布具体的报错文字：`temperature`、`top_p`、`top_k` 设置了非默认值；advisor 工具用了 Sonnet 5.5 不支持的顾问模型。

<p align="center">
  <small>© 2026 DMXAPI Claude Sonnet 5.5 调整与破坏性更新</small>
</p>
