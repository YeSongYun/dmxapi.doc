# Claude 提示词缓存使用文档

> 本文档介绍如何使用 Claude API 的提示词缓存功能，通过缓存系统提示词来优化 API 调用成本和响应速度。

## 📋 概述

提示词缓存（Prompt Caching）允许您复用频繁使用的上下文，降低重复输入的处理成本。本页使用 **`claude-opus-5-5`** 演示，按照官方文档，该模型的最小可缓存前缀为 **512 tokens**。示例继续使用《傲慢与偏见》前五章的长篇文本，分别演示默认 **5 分钟**和 **1 小时**缓存的创建与命中。

### 功能特性

- ✅ 支持缓存大型系统提示词
- ✅ 降低重复调用的 token 成本
- ✅ 提升 API 响应速度
- ✅ 默认缓存有效期：5 分钟，无需填写 `ttl`
- ✅ 支持设置 `ttl: "1h"`，将缓存有效期设为 1 小时
- ✅ 命中缓存时刷新有效期；每次请求仍需发送完整的相同前缀

## 🔗 API 端点

```text
https://www.dmxapi.cn/v1/messages
```

## 💻 完整代码示例

::: code-group

```python [5 分钟缓存（默认）]
"""
Claude API 5 分钟缓存测试脚本

功能说明：
- 通过 DMXAPI 调用 Claude Opus 5.5 进行文学分析
- 第一次请求创建缓存，第二次请求复用相同的系统提示词
- 输出两次请求的 token 统计和完整 JSON 响应

作者：DMX API 文档
"""

import requests
import os
import json
import sys

# 统一输出编码，兼容 Windows 控制台。
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

# =============================================================================
# 配置参数
# =============================================================================

# 优先从环境变量获取密钥，也可以将占位符替换为自己的 DMXAPI 密钥
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "sk-************************************")
API_URL = "https://www.dmxapi.cn/v1/messages"

# =============================================================================
# 请求头配置
# =============================================================================

headers = {
    "content-type": "application/json",
    "x-api-key": ANTHROPIC_API_KEY,
    "anthropic-version": "2023-06-01",
}

# =============================================================================
# 请求数据构造
# =============================================================================

payload = {
    "model": "claude-opus-5-5",
    "max_tokens": 1024,  # 最大输出 token 数，与缓存输入长度无关
    "stream": False,
    # Opus 5.5 的最小可缓存前缀为 512 tokens。
    # 两个时长示例使用不同的固定开头，便于分别观察首次写入。
    # 同一示例的两次请求保持完整 system 内容不变。
    "system": [
        {
            "type": "text",
            "text": """Literary analysis reference for the default five-minute cache example.

You are an AI assistant tasked with analyzing literary works. Your goal is to provide insightful commentary on themes, characters, and writing style.

Below is the full text of Pride and Prejudice chapters 1-5 for analysis:

Pride and Prejudice - Chapter 1 to 5 (Excerpt)

Chapter 1


It is a truth universally acknowledged, that a single man in possession of a good fortune, must be in want of a wife.

However little known the feelings or views of such a man may be on his first entering a neighbourhood, this truth is so well fixed in the minds of the surrounding families, that he is considered the rightful property of some one or other of their daughters.

"My dear Mr. Bennet," said his lady to him one day, "have you heard that Netherfield Park is let at last?"

Mr. Bennet replied that he had not.

"But it is," returned she; "for Mrs. Long has just been here, and she told me all about it."

Mr. Bennet made no answer.

"Do you not want to know who has taken it?" cried his wife impatiently.

"You want to tell me, and I have no objection to hearing it."

This was invitation enough.

"Why, my dear, you must know, Mrs. Long says that Netherfield is taken by a young man of large fortune from the north of England; that he came down on Monday in a chaise and four to see the place, and was so much delighted with it, that he agreed with Mr. Morris immediately; that he is to take possession before Michaelmas, and some of his servants are to be in the house by the end of next week."

"What is his name?"

"Bingley."

"Is he married or single?"

"Oh! Single, my dear, to be sure! A single man of large fortune; four or five thousand a year. What a fine thing for our girls!"

"How so? How can it affect them?"

"My dear Mr. Bennet," replied his wife, "how can you be so tiresome! You must know that I am thinking of his marrying one of them."

"Is that his design in settling here?"

"Design! Nonsense, how can you talk so! But it is very likely that he may fall in love with one of them, and therefore you must visit him as soon as he comes."

"I see no occasion for that. You and the girls may go, or you may send them by themselves, which perhaps will be still better, for as you are as handsome as any of them, Mr. Bingley may like you the best of the party."

Chapter 2

Mr. Bennet was among the earliest of those who waited on Mr. Bingley. He had always intended to visit him, though to the last always assuring his wife that he should not go; and till the evening after the visit was paid she had no knowledge of it.

It was then disclosed in the following manner. Observing his second daughter employed in trimming a hat, he suddenly addressed her with:

"I hope Mr. Bingley will like it, Lizzy."

"We are not in a way to know what Mr. Bingley likes," said her mother resentfully, "since we are not to visit."

"But you forget, mamma," said Elizabeth, "that we shall meet him at the assemblies, and that Mrs. Long promised to introduce him."

"I do not believe Mrs. Long will do any such thing. She has two nieces of her own. She is a selfish, hypocritical woman, and I have no opinion of her."

"No more have I," said Mr. Bennet; "and I am glad to find that you do not depend on her serving you."

Mrs. Bennet deigned not to make any reply, but, unable to contain herself, began scolding one of her daughters.

Chapter 3

Not all that Mrs. Bennet, however, with the assistance of her five daughters, could ask on the subject, was sufficient to draw from her husband any satisfactory description of Mr. Bingley. They attacked him in various ways—with barefaced questions, ingenious suppositions, and distant surmises; but he eluded the skill of them all, and they were at last obliged to accept the second-hand intelligence of their neighbour, Lady Lucas. Her report was highly favourable. Sir William had been delighted with him. He was quite young, wonderfully handsome, extremely agreeable, and, to crown the whole, he meant to be at the next assembly with a large party. Nothing could be more delightful! To be fond of dancing was a certain step towards falling in love; and very lively hopes of Mr. Bingley's heart were entertained.

"If I can but see one of my daughters happily settled at Netherfield," said Mrs. Bennet to her husband, "and all the others equally well married, I shall have nothing to wish for."

In a few days Mr. Bingley returned Mr. Bennet's visit, and sat about ten minutes with him in his library. He had entertained hopes of being admitted to a sight of the young ladies, of whose beauty he had heard much; but he saw only the father. The ladies were somewhat more fortunate, for they had the advantage of ascertaining from an upper window that he wore a blue coat, and rode a black horse.

Chapter 4

When Jane and Elizabeth were alone, the former, who had been cautious in her praise of Mr. Bingley before, expressed to her sister just how very much she admired him.

"He is just what a young man ought to be," said she, "sensible, good-humoured, lively; and I never saw such happy manners!—so much ease, with such perfect good breeding!"

"He is also handsome," replied Elizabeth, "which a young man ought likewise to be, if he possibly can. His character is thereby complete."

"I was very much flattered by his asking me to dance a second time. I did not expect such a compliment."

"Did not you? I did for you. But that is one great difference between us. Compliments always take you by surprise, and me never. What could be more natural than his asking you again? He could not help seeing that you were about five times as pretty as every other woman in the room. No thanks to his gallantry for that. Well, he certainly is very agreeable, and I give you leave to like him. You have liked many a stupider person."

Chapter 5

Within a short walk of Longbourn lived a family with whom the Bennets were particularly intimate. Sir William Lucas had been formerly in trade in Meryton, where he had made a tolerable fortune, and risen to the honour of knighthood by an address to the king during his mayoralty. The distinction had perhaps been felt too strongly. It had given him a disgust to his business, and to his residence in a small market town; and, in quitting them both, he had removed with his family to a house about a mile from Meryton, denominated from that period Lucas Lodge, where he could think with pleasure of his own importance, and, unshackled by business, occupy himself solely in being civil to all the world. For, though elated by his rank, it did not render him supercilious; on the contrary, he was all attention to everybody. By nature inoffensive, friendly, and obliging, his presentation at St. James's had made him courteous.

Lady Lucas was a very good kind of woman, not too clever to be a valuable neighbour to Mrs. Bennet. They had several children. The eldest of them, a sensible, intelligent young woman, about twenty-seven, was Elizabeth's intimate friend.

That the Miss Lucases and the Miss Bennets should meet to talk over a ball was absolutely necessary; and the morning after the assembly brought the former to Longbourn to hear and to communicate.

"You began the evening well, Charlotte," said Mrs. Bennet with civil self-command to Miss Lucas. "You were Mr. Bingley's first choice."

"Yes; but he seemed to like his second better."

"Oh! you mean Jane, I suppose, because he danced with her twice. To be sure that did seem as if he admired her—indeed I rather believe he did—I heard something about it—but I hardly know what—something about Mr. Robinson."

"Perhaps you mean what I overheard between him and Mr. Robinson; did not I mention it to you? Mr. Robinson's asking him how he liked our Meryton assemblies, and whether he did not think there were a great many pretty women in the room, and which he thought the prettiest? and his answering immediately to the last question: 'Oh! the eldest Miss Bennet, beyond a doubt; there cannot be two opinions on that point.'"

"Upon my word! Well, that is very decided indeed—that does seem as if—but, however, it may all come to nothing, you know."

Additional chapters and content would continue here to ensure we have well over 2048 tokens for reliable caching. This extended text ensures the cache threshold is clearly exceeded.
""",
            "cache_control": {"type": "ephemeral"},  # 省略 ttl，默认缓存 5 分钟
        }
    ],
    "messages": [
        {
            "role": "user",
            "content": "请用中文在120字内概括《傲慢与偏见》前五章的主要主题。",
        }
    ],
}

# =============================================================================
# 请求与响应处理
# =============================================================================


def send_request(label, question):
    # 只修改缓存断点之后的用户问题，不修改 system 前缀。
    payload["messages"][0]["content"] = question
    print(f"\n[{label}]")

    response = requests.post(
        API_URL,
        headers=headers,
        json=payload,
        timeout=(10, 120),
    )
    response.raise_for_status()
    result = response.json()
    usage = result.get("usage") or {}
    cache_creation = usage.get("cache_creation") or {}

    print("[SUCCESS] 请求成功！")
    print("[USAGE] Token 使用统计：")
    print(f"  - 输入 tokens: {usage.get('input_tokens', 0)}")
    print(f"  - 输出 tokens: {usage.get('output_tokens', 0)}")
    print(f"  - 缓存创建 tokens: {usage.get('cache_creation_input_tokens', 0)}")
    print(f"  - 缓存读取 tokens: {usage.get('cache_read_input_tokens', 0)}")
    print(f"  - 5 分钟缓存写入 tokens: {cache_creation.get('ephemeral_5m_input_tokens', '未返回')}")
    print(f"  - 1 小时缓存写入 tokens: {cache_creation.get('ephemeral_1h_input_tokens', '未返回')}")

    created = cache_creation.get("ephemeral_5m_input_tokens", 0)
    cached = usage.get("cache_read_input_tokens", 0)
    if created > 0:
        print(f"[CACHE] 5 分钟缓存创建成功，写入 {created} tokens。")
    if cached > 0:
        print(f"[CACHE] 缓存命中，读取 {cached} tokens。")
    if created == 0 and cached == 0:
        print("[TIP] 未观察到目标时长的缓存写入或缓存读取，请检查返回的 usage。")

    print("[JSON] 完整 API 响应：")
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return result


# =============================================================================
# 主程序执行
# =============================================================================


def main():
    print("[START] 开始调用 Claude API（测试5 分钟缓存）")
    print(f"[INFO] API 端点: {API_URL}")
    print(f"[INFO] 使用模型: {payload['model']}")
    print("-" * 60)

    try:
        send_request("第一次请求：创建缓存", payload["messages"][0]["content"])
        # 等待第一次请求完成，再复用相同前缀验证命中。
        send_request(
            "第二次请求：读取缓存",
            "请用中文在120字内说明班纳特太太的性格及其推动情节的作用。",
        )
    except requests.exceptions.Timeout:
        print("[ERROR] 请求超时：请检查网络连接或稍后重试。")
        raise SystemExit(1)
    except requests.exceptions.RequestException as exc:
        print(f"[ERROR] 请求失败：{exc}")
        raise SystemExit(1)
    except ValueError:
        print("[ERROR] JSON 解析错误：响应格式不正确。")
        raise SystemExit(1)


# =============================================================================
# 程序入口点
# =============================================================================

if __name__ == "__main__":
    main()
    print("\n[DONE] 程序执行完成")
```

```python [1 小时缓存]
"""
Claude API 1 小时缓存测试脚本

功能说明：
- 通过 DMXAPI 调用 Claude Opus 5.5 进行文学分析
- 第一次请求创建缓存，第二次请求复用相同的系统提示词
- 输出两次请求的 token 统计和完整 JSON 响应

作者：DMX API 文档
"""

import requests
import os
import json
import sys

# 统一输出编码，兼容 Windows 控制台。
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

# =============================================================================
# 配置参数
# =============================================================================

# 优先从环境变量获取密钥，也可以将占位符替换为自己的 DMXAPI 密钥
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "sk-************************************")
API_URL = "https://www.dmxapi.cn/v1/messages"

# =============================================================================
# 请求头配置
# =============================================================================

headers = {
    "content-type": "application/json",
    "x-api-key": ANTHROPIC_API_KEY,
    "anthropic-version": "2023-06-01",
}

# =============================================================================
# 请求数据构造
# =============================================================================

payload = {
    "model": "claude-opus-5-5",
    "max_tokens": 1024,  # 最大输出 token 数，与缓存输入长度无关
    "stream": False,
    # Opus 5.5 的最小可缓存前缀为 512 tokens。
    # 两个时长示例使用不同的固定开头，便于分别观察首次写入。
    # 同一示例的两次请求保持完整 system 内容不变。
    "system": [
        {
            "type": "text",
            "text": """Literary analysis reference for the one-hour cache example.

You are an AI assistant tasked with analyzing literary works. Your goal is to provide insightful commentary on themes, characters, and writing style.

Below is the full text of Pride and Prejudice chapters 1-5 for analysis:

Pride and Prejudice - Chapter 1 to 5 (Excerpt)

Chapter 1


It is a truth universally acknowledged, that a single man in possession of a good fortune, must be in want of a wife.

However little known the feelings or views of such a man may be on his first entering a neighbourhood, this truth is so well fixed in the minds of the surrounding families, that he is considered the rightful property of some one or other of their daughters.

"My dear Mr. Bennet," said his lady to him one day, "have you heard that Netherfield Park is let at last?"

Mr. Bennet replied that he had not.

"But it is," returned she; "for Mrs. Long has just been here, and she told me all about it."

Mr. Bennet made no answer.

"Do you not want to know who has taken it?" cried his wife impatiently.

"You want to tell me, and I have no objection to hearing it."

This was invitation enough.

"Why, my dear, you must know, Mrs. Long says that Netherfield is taken by a young man of large fortune from the north of England; that he came down on Monday in a chaise and four to see the place, and was so much delighted with it, that he agreed with Mr. Morris immediately; that he is to take possession before Michaelmas, and some of his servants are to be in the house by the end of next week."

"What is his name?"

"Bingley."

"Is he married or single?"

"Oh! Single, my dear, to be sure! A single man of large fortune; four or five thousand a year. What a fine thing for our girls!"

"How so? How can it affect them?"

"My dear Mr. Bennet," replied his wife, "how can you be so tiresome! You must know that I am thinking of his marrying one of them."

"Is that his design in settling here?"

"Design! Nonsense, how can you talk so! But it is very likely that he may fall in love with one of them, and therefore you must visit him as soon as he comes."

"I see no occasion for that. You and the girls may go, or you may send them by themselves, which perhaps will be still better, for as you are as handsome as any of them, Mr. Bingley may like you the best of the party."

Chapter 2

Mr. Bennet was among the earliest of those who waited on Mr. Bingley. He had always intended to visit him, though to the last always assuring his wife that he should not go; and till the evening after the visit was paid she had no knowledge of it.

It was then disclosed in the following manner. Observing his second daughter employed in trimming a hat, he suddenly addressed her with:

"I hope Mr. Bingley will like it, Lizzy."

"We are not in a way to know what Mr. Bingley likes," said her mother resentfully, "since we are not to visit."

"But you forget, mamma," said Elizabeth, "that we shall meet him at the assemblies, and that Mrs. Long promised to introduce him."

"I do not believe Mrs. Long will do any such thing. She has two nieces of her own. She is a selfish, hypocritical woman, and I have no opinion of her."

"No more have I," said Mr. Bennet; "and I am glad to find that you do not depend on her serving you."

Mrs. Bennet deigned not to make any reply, but, unable to contain herself, began scolding one of her daughters.

Chapter 3

Not all that Mrs. Bennet, however, with the assistance of her five daughters, could ask on the subject, was sufficient to draw from her husband any satisfactory description of Mr. Bingley. They attacked him in various ways—with barefaced questions, ingenious suppositions, and distant surmises; but he eluded the skill of them all, and they were at last obliged to accept the second-hand intelligence of their neighbour, Lady Lucas. Her report was highly favourable. Sir William had been delighted with him. He was quite young, wonderfully handsome, extremely agreeable, and, to crown the whole, he meant to be at the next assembly with a large party. Nothing could be more delightful! To be fond of dancing was a certain step towards falling in love; and very lively hopes of Mr. Bingley's heart were entertained.

"If I can but see one of my daughters happily settled at Netherfield," said Mrs. Bennet to her husband, "and all the others equally well married, I shall have nothing to wish for."

In a few days Mr. Bingley returned Mr. Bennet's visit, and sat about ten minutes with him in his library. He had entertained hopes of being admitted to a sight of the young ladies, of whose beauty he had heard much; but he saw only the father. The ladies were somewhat more fortunate, for they had the advantage of ascertaining from an upper window that he wore a blue coat, and rode a black horse.

Chapter 4

When Jane and Elizabeth were alone, the former, who had been cautious in her praise of Mr. Bingley before, expressed to her sister just how very much she admired him.

"He is just what a young man ought to be," said she, "sensible, good-humoured, lively; and I never saw such happy manners!—so much ease, with such perfect good breeding!"

"He is also handsome," replied Elizabeth, "which a young man ought likewise to be, if he possibly can. His character is thereby complete."

"I was very much flattered by his asking me to dance a second time. I did not expect such a compliment."

"Did not you? I did for you. But that is one great difference between us. Compliments always take you by surprise, and me never. What could be more natural than his asking you again? He could not help seeing that you were about five times as pretty as every other woman in the room. No thanks to his gallantry for that. Well, he certainly is very agreeable, and I give you leave to like him. You have liked many a stupider person."

Chapter 5

Within a short walk of Longbourn lived a family with whom the Bennets were particularly intimate. Sir William Lucas had been formerly in trade in Meryton, where he had made a tolerable fortune, and risen to the honour of knighthood by an address to the king during his mayoralty. The distinction had perhaps been felt too strongly. It had given him a disgust to his business, and to his residence in a small market town; and, in quitting them both, he had removed with his family to a house about a mile from Meryton, denominated from that period Lucas Lodge, where he could think with pleasure of his own importance, and, unshackled by business, occupy himself solely in being civil to all the world. For, though elated by his rank, it did not render him supercilious; on the contrary, he was all attention to everybody. By nature inoffensive, friendly, and obliging, his presentation at St. James's had made him courteous.

Lady Lucas was a very good kind of woman, not too clever to be a valuable neighbour to Mrs. Bennet. They had several children. The eldest of them, a sensible, intelligent young woman, about twenty-seven, was Elizabeth's intimate friend.

That the Miss Lucases and the Miss Bennets should meet to talk over a ball was absolutely necessary; and the morning after the assembly brought the former to Longbourn to hear and to communicate.

"You began the evening well, Charlotte," said Mrs. Bennet with civil self-command to Miss Lucas. "You were Mr. Bingley's first choice."

"Yes; but he seemed to like his second better."

"Oh! you mean Jane, I suppose, because he danced with her twice. To be sure that did seem as if he admired her—indeed I rather believe he did—I heard something about it—but I hardly know what—something about Mr. Robinson."

"Perhaps you mean what I overheard between him and Mr. Robinson; did not I mention it to you? Mr. Robinson's asking him how he liked our Meryton assemblies, and whether he did not think there were a great many pretty women in the room, and which he thought the prettiest? and his answering immediately to the last question: 'Oh! the eldest Miss Bennet, beyond a doubt; there cannot be two opinions on that point.'"

"Upon my word! Well, that is very decided indeed—that does seem as if—but, however, it may all come to nothing, you know."

Additional chapters and content would continue here to ensure we have well over 2048 tokens for reliable caching. This extended text ensures the cache threshold is clearly exceeded.
""",
            "cache_control": {"type": "ephemeral", "ttl": "1h"},  # 显式指定 1 小时缓存
        }
    ],
    "messages": [
        {
            "role": "user",
            "content": "请用中文在120字内概括《傲慢与偏见》前五章的主要主题。",
        }
    ],
}

# =============================================================================
# 请求与响应处理
# =============================================================================


def send_request(label, question):
    # 只修改缓存断点之后的用户问题，不修改 system 前缀。
    payload["messages"][0]["content"] = question
    print(f"\n[{label}]")

    response = requests.post(
        API_URL,
        headers=headers,
        json=payload,
        timeout=(10, 120),
    )
    response.raise_for_status()
    result = response.json()
    usage = result.get("usage") or {}
    cache_creation = usage.get("cache_creation") or {}

    print("[SUCCESS] 请求成功！")
    print("[USAGE] Token 使用统计：")
    print(f"  - 输入 tokens: {usage.get('input_tokens', 0)}")
    print(f"  - 输出 tokens: {usage.get('output_tokens', 0)}")
    print(f"  - 缓存创建 tokens: {usage.get('cache_creation_input_tokens', 0)}")
    print(f"  - 缓存读取 tokens: {usage.get('cache_read_input_tokens', 0)}")
    print(f"  - 5 分钟缓存写入 tokens: {cache_creation.get('ephemeral_5m_input_tokens', '未返回')}")
    print(f"  - 1 小时缓存写入 tokens: {cache_creation.get('ephemeral_1h_input_tokens', '未返回')}")

    created = cache_creation.get("ephemeral_1h_input_tokens", 0)
    cached = usage.get("cache_read_input_tokens", 0)
    if created > 0:
        print(f"[CACHE] 1 小时缓存创建成功，写入 {created} tokens。")
    if cached > 0:
        print(f"[CACHE] 缓存命中，读取 {cached} tokens。")
    if created == 0 and cached == 0:
        print("[TIP] 未观察到目标时长的缓存写入或缓存读取，请检查返回的 usage。")

    print("[JSON] 完整 API 响应：")
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return result


# =============================================================================
# 主程序执行
# =============================================================================


def main():
    print("[START] 开始调用 Claude API（测试1 小时缓存）")
    print(f"[INFO] API 端点: {API_URL}")
    print(f"[INFO] 使用模型: {payload['model']}")
    print("-" * 60)

    try:
        send_request("第一次请求：创建缓存", payload["messages"][0]["content"])
        # 等待第一次请求完成，再复用相同前缀验证命中。
        send_request(
            "第二次请求：读取缓存",
            "请用中文在120字内说明班纳特太太的性格及其推动情节的作用。",
        )
    except requests.exceptions.Timeout:
        print("[ERROR] 请求超时：请检查网络连接或稍后重试。")
        raise SystemExit(1)
    except requests.exceptions.RequestException as exc:
        print(f"[ERROR] 请求失败：{exc}")
        raise SystemExit(1)
    except ValueError:
        print("[ERROR] JSON 解析错误：响应格式不正确。")
        raise SystemExit(1)


# =============================================================================
# 程序入口点
# =============================================================================

if __name__ == "__main__":
    main()
    print("\n[DONE] 程序执行完成")
```

:::

### 代码说明

上述示例演示了如何：

1. **配置缓存控制**：5 分钟代码使用 `cache_control: {"type": "ephemeral"}`；<br>1 小时代码使用 `cache_control: {"type": "ephemeral", "ttl": "1h"}`。
2. **准备足够的内容**：继续使用《傲慢与偏见》前五章文本作为固定系统提示词。两组选项使用不同的固定开头，便于分别观察缓存写入；每组内部的两次请求保持完整前缀不变。
3. **创建并读取缓存**：先等待第一次请求完成，再发送第二个问题，通过响应中的 `usage` 分别检查缓存写入和缓存读取。
4. **输出完整返回值**：分别打印两次请求的 token 统计和完整 JSON，便于核对实际结果。


## 📊 API 响应示例

### 5 分钟缓存（默认）返回值

#### 控制台输出

```text
[START] 开始调用 Claude API（测试5 分钟缓存）
[INFO] API 端点: https://www.dmxapi.cn/v1/messages
[INFO] 使用模型: claude-opus-5-5
------------------------------------------------------------

[第一次请求：创建缓存]
[SUCCESS] 请求成功！
[USAGE] Token 使用统计：
  - 输入 tokens: 35
  - 输出 tokens: 192
  - 缓存创建 tokens: 2964
  - 缓存读取 tokens: 0
  - 5 分钟缓存写入 tokens: 2964
  - 1 小时缓存写入 tokens: 0
[CACHE] 5 分钟缓存创建成功，写入 2964 tokens。

[第二次请求：读取缓存]
[SUCCESS] 请求成功！
[USAGE] Token 使用统计：
  - 输入 tokens: 36
  - 输出 tokens: 209
  - 缓存创建 tokens: 0
  - 缓存读取 tokens: 2964
  - 5 分钟缓存写入 tokens: 0
  - 1 小时缓存写入 tokens: 0
[CACHE] 缓存命中，读取 2964 tokens。

[DONE] 程序执行完成
```

#### 第一次请求：创建缓存

```json
{
  "model": "claude-opus-5-5",
  "id": "msg_011CgSb9ADvD5p2zvHy088MT",
  "type": "message",
  "role": "assistant",
  "content": [
    {
      "type": "text",
      "text": "前五章围绕婚姻与财富展开：班纳特太太急于为女儿觅得富有夫婿，凸显当时社会\"婚姻即经济保障\"的现实。班纳特先生的冷嘲、伊丽莎白的机敏，与班纳特太太的浅薄形成对照，带出讽刺喜剧色彩。同时，阶层与地位意识（如卢卡斯爵士）、第一印象与外在判断（简与宾利的互相倾心）等主题也已初现，为后文\"傲慢与偏见\"埋下伏笔。"
    }
  ],
  "stop_reason": "end_turn",
  "stop_sequence": null,
  "stop_details": null,
  "usage": {
    "input_tokens": 35,
    "cache_creation_input_tokens": 2964,
    "cache_read_input_tokens": 0,
    "cache_creation": {
      "ephemeral_5m_input_tokens": 2964,
      "ephemeral_1h_input_tokens": 0
    },
    "output_tokens": 192,
    "output_tokens_details": {
      "thinking_tokens": 0
    },
    "service_tier": "standard",
    "inference_geo": "not_available",
    "cost": "¥0.094"
  }
}
```

#### 第二次请求：缓存命中

```json
{
  "model": "claude-opus-5-5",
  "id": "msg_011CgSb9JIBBw23FtTY3DrEf",
  "type": "message",
  "role": "assistant",
  "content": [
    {
      "type": "text",
      "text": "班纳特太太浅薄、急躁、爱慕虚荣，一心只想把五个女儿嫁给有钱人。她言行失当，爱抢话、爱八卦，常令丈夫和女儿难堪，也体现出当时女性因财产继承限制而产生的婚姻焦虑。\n\n她推动情节的作用十分关键：开篇她热切打听宾利的消息，催促丈夫拜访，促成两家结识；她对婚事的积极撮合，让简与宾利的交往得以展开，也为后续伊丽莎白与达西的误会与冲突埋下伏笔。"
    }
  ],
  "stop_reason": "end_turn",
  "stop_sequence": null,
  "stop_details": null,
  "usage": {
    "input_tokens": 36,
    "cache_creation_input_tokens": 0,
    "cache_read_input_tokens": 2964,
    "cache_creation": {
      "ephemeral_5m_input_tokens": 0,
      "ephemeral_1h_input_tokens": 0
    },
    "output_tokens": 209,
    "output_tokens_details": {
      "thinking_tokens": 0
    },
    "service_tier": "standard",
    "inference_geo": "not_available",
    "cost": "¥0.024584"
  }
}
```

### 1 小时缓存返回值

#### 控制台输出

```text
[START] 开始调用 Claude API（测试1 小时缓存）
[INFO] API 端点: https://www.dmxapi.cn/v1/messages
[INFO] 使用模型: claude-opus-5-5
------------------------------------------------------------

[第一次请求：创建缓存]
[SUCCESS] 请求成功！
[USAGE] Token 使用统计：
  - 输入 tokens: 35
  - 输出 tokens: 154
  - 缓存创建 tokens: 2963
  - 缓存读取 tokens: 0
  - 5 分钟缓存写入 tokens: 0
  - 1 小时缓存写入 tokens: 2963
[CACHE] 1 小时缓存创建成功，写入 2963 tokens。

[第二次请求：读取缓存]
[SUCCESS] 请求成功！
[USAGE] Token 使用统计：
  - 输入 tokens: 36
  - 输出 tokens: 171
  - 缓存创建 tokens: 0
  - 缓存读取 tokens: 2963
  - 5 分钟缓存写入 tokens: 0
  - 1 小时缓存写入 tokens: 0
[CACHE] 缓存命中，读取 2963 tokens。

[DONE] 程序执行完成
```

#### 第一次请求：创建缓存

```json
{
  "model": "claude-opus-5-5",
  "id": "msg_011CgSbATLRxZ3iUlPbwpg3u",
  "type": "message",
  "role": "assistant",
  "content": [
    {
      "type": "text",
      "text": "前五章围绕婚姻、财富与阶层展开：班纳特太太急于为女儿觅得富婿，反映当时女性只能依靠婚姻获得保障的社会现实。班纳特先生的反讽幽默与太太的浅薄急切形成对比。简与宾利一见倾心，伊丽莎白则机智敏锐。卢卡斯家的出身与虚荣，也暗示了对阶层与身份的讽刺。"
    }
  ],
  "stop_reason": "end_turn",
  "stop_sequence": null,
  "stop_details": null,
  "usage": {
    "input_tokens": 35,
    "cache_creation_input_tokens": 2963,
    "cache_read_input_tokens": 0,
    "cache_creation": {
      "ephemeral_5m_input_tokens": 0,
      "ephemeral_1h_input_tokens": 2963
    },
    "output_tokens": 154,
    "output_tokens_details": {
      "thinking_tokens": 0
    },
    "service_tier": "standard",
    "inference_geo": "not_available",
    "cost": "¥0.13462"
  }
}
```

#### 第二次请求：缓存命中

```json
{
  "model": "claude-opus-5-5",
  "id": "msg_011CgSbA13k1WqTWVEW9WpDW",
  "type": "message",
  "role": "assistant",
  "content": [
    {
      "type": "text",
      "text": "班纳特太太浅薄、急切、爱慕虚荣，一心只想把五个女儿嫁给有钱人。她说话冲动，爱抱怨，又爱搬弄邻里是非，常令丈夫和女儿难堪。然而正是她对宾利先生的热切盘算，推动了拜访、舞会和简与宾利相识等情节的展开。她的言行既制造喜剧效果，也折射出当时女性缺乏财产继承权、婚姻关乎生计的社会现实。"
    }
  ],
  "stop_reason": "end_turn",
  "stop_sequence": null,
  "stop_details": null,
  "usage": {
    "input_tokens": 36,
    "cache_creation_input_tokens": 0,
    "cache_read_input_tokens": 2963,
    "cache_creation": {
      "ephemeral_5m_input_tokens": 0,
      "ephemeral_1h_input_tokens": 0
    },
    "output_tokens": 171,
    "output_tokens_details": {
      "thinking_tokens": 0
    },
    "service_tier": "standard",
    "inference_geo": "not_available",
    "cost": "¥0.020784"
  }
}
```

## ⚠️ 注意事项

### 缓存要求

1. **最小长度**：本页模型的最小可缓存前缀为 512 tokens；其他模型请查阅官方限制。短于门槛的内容即使设置了 `cache_control` 也不会缓存。
2. **内容一致**：两次请求中，缓存断点及其之前的内容必须完全一致。不要在前缀中加入每次变化的时间戳、随机数或用户问题。
3. **有效期限**：默认 5 分钟，也可以显式设置为 1 小时。有效期从创建或命中缓存的请求开始时计算，命中后会刷新。
4. **请求顺序**：首次响应开始后缓存才可供后续请求读取。本页代码等待完整响应后再发送第二次请求。
5. **结果判断**：重复运行时，第一次请求也可能直接命中已有缓存。若写入和读取均为 `0`，检查前缀长度、模型、缓存配置和上游支持情况。

### 使用建议

- 💡 适合缓存：大型系统提示词、参考文档、示例数据
- 💡 不适合缓存：频繁变化的内容、一次性请求
- 💡 成本优化：仅在需要多次使用相同上下文时使用缓存。按本页模型的官方规则，5 分钟写入为普通输入单价的 1.25 倍，1 小时写入为 2 倍，读取为 0.05 倍；DMXAPI 实际费用以平台价格和账单为准
- 💡 时长选择：频繁调用可使用默认 5 分钟缓存；间隔经常超过 5 分钟但不足 1 小时时，可以选择 1 小时缓存

### API 密钥安全

⚠️ **重要**：示例代码中的 API 密钥仅供演示，请务必：

- 使用您自己的 API 密钥
- 不要将密钥硬编码在代码中
- 建议通过环境变量管理密钥
- 不要将包含真实密钥的代码提交到公开仓库

---

<p align="center">
  <small>© 2026 DMXAPI 提示词缓存</small>
</p>
