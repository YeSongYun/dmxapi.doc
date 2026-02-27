# Claude 提示词缓存使用文档

> 本文档介绍如何使用 Claude API 的提示词缓存功能，通过缓存系统提示词来优化 API 调用成本和响应速度。

## 📋 概述

提示词缓存（Prompt Caching）允许您缓存频繁使用的上下文内容，避免重复计费。缓存的内容至少需要 **1024 tokens**，建议使用 **2048+ tokens** 以确保缓存成功创建。

### 功能特性

- ✅ 支持缓存大型系统提示词
- ✅ 降低重复调用的 token 成本
- ✅ 提升 API 响应速度
- ⚠️ 缓存有效期：5 分钟

## 🔗 API 端点

```text
https://www.dmxapi.cn/v1/messages
```

## 💻 完整代码示例

```python
"""
Claude API 测试脚本

功能说明：
- 通过 DMX API 调用 Claude 模型进行文学分析
- 演示如何使用系统提示词和用户消息
- 包含完整的错误处理和响应解析

作者：DMX API 文档
"""

import requests
import os
import json

# =============================================================================
# 配置参数
# =============================================================================

# DMXAPI 密钥配置
# 优先从环境变量获取，如果不存在则使用默认值
# 注意：请将默认密钥替换为您的实际 API 密钥
ANTHROPIC_API_KEY = os.getenv('ANTHROPIC_API_KEY', 'sk-************************************')

# API 端点
API_URL = "https://www.dmxapi.cn/v1/messages"

# =============================================================================
# 请求头配置
# =============================================================================

# HTTP 请求头设置
headers = {
    "content-type": "application/json",              # 指定请求内容为 JSON 格式
    "x-api-key": ANTHROPIC_API_KEY,                  # API 认证密钥
    "anthropic-version": "2023-06-01",               # API 版本（缓存功能需要）
}

# =============================================================================
# 请求数据构造
# =============================================================================

# 构造完整的 API 请求载荷
payload = {
    "model": "claude-sonnet-4-6",           # 使用 Sonnet 模型（更好地支持缓存）
    # "max_tokens": 200000,                            # 最大输出 token 数量
    
    # 系统提示词配置
    # 注意：缓存需要至少 1024 tokens，建议使用 2048+ tokens 以确保成功
    "system": [
        {
            "type": "text",
            "text": """You are an AI assistant tasked with analyzing literary works. Your goal is to provide insightful commentary on themes, characters, and writing style.

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
            "cache_control": {"type": "ephemeral"}  # 缓存控制设置
        }
    ],
    
    # 用户消息
    "messages": [
        {
            "role": "user",
            "content": "Analyze the major themes in Pride and Prejudice."  # 分析《傲慢与偏见》的主要主题
        }
    ]
}

# =============================================================================
# 主程序执行
# =============================================================================

def main():
    """
    主函数：执行 API 调用并处理响应，检查缓存创建情况
    """
    print("[START] 开始调用 Claude API（测试缓存创建）")
    print(f"[INFO] API 端点: {API_URL}")
    print(f"[INFO] 使用模型: {payload['model']}")
    print("-" * 60)

    try:
        # 发送 POST 请求到 API 端点
        response = requests.post(
            API_URL,
            headers=headers,
            json=payload,
            timeout=30  # 设置 30 秒超时
        )

        # 检查 HTTP 响应状态码
        if response.status_code == 200:
            print("[SUCCESS] 请求成功!")

            # 解析 JSON 响应
            result = response.json()

            # 提取使用统计信息
            usage = result.get('usage', {})

            print(f"\n[USAGE] Token 使用统计:")
            print(f"  - 输入 tokens: {usage.get('input_tokens', 0)}")
            print(f"  - 输出 tokens: {usage.get('output_tokens', 0)}")
            print(f"  - 缓存创建 tokens: {usage.get('cache_creation_input_tokens', 0)}")
            print(f"  - 缓存读取 tokens: {usage.get('cache_read_input_tokens', 0)}")

            # 判断缓存状态
            cache_created = usage.get('cache_creation_input_tokens', 0)
            if cache_created > 0:
                print(f"\n[CACHE] 缓存创建成功！已缓存 {cache_created} tokens")
                print(f"[TIP] 提示：缓存仅保存5分钟，且命中率低")
            else:
                print("\n[WARNING] 缓存未创建")
                print("可能原因：")
                print("  1. 内容长度不足 1024 tokens")
                print("  2. 未正确设置 cache_control")
                print("  3. API 配置问题")

            # 显示响应内容（摘要）
            content = result.get('content', [])
            if content and len(content) > 0:
                text_content = content[0].get('text', '')
                print(f"\n[RESPONSE] Claude 回复（前 300 字符）:")
                print(f"{text_content[:300]}..." if len(text_content) > 300 else text_content)

            # 完整 JSON 输出（可选）
            print(f"\n[JSON] 完整 API 响应:")
            formatted_json = json.dumps(result, indent=2, ensure_ascii=False)
            print(formatted_json)

        else:
            # 处理错误响应
            print(f"[ERROR] 请求失败，状态码: {response.status_code}")
            print(f"[ERROR] 错误信息: {response.text}")

    except requests.exceptions.Timeout:
        print("[ERROR] 请求超时：请检查网络连接或稍后重试")
    except requests.exceptions.ConnectionError:
        print("[ERROR] 连接错误：无法连接到 API 服务器")
    except requests.exceptions.RequestException as e:
        print(f"[ERROR] 请求异常: {e}")
    except json.JSONDecodeError:
        print("[ERROR] JSON 解析错误：响应格式不正确")
    except Exception as e:
        print(f"[ERROR] 未知错误: {e}")

# =============================================================================
# 程序入口点
# =============================================================================

if __name__ == "__main__":
    main()
    print("\n[DONE] 程序执行完成")
```

### 代码说明

上述示例演示了如何：

1. **配置缓存控制**：在 `system` 消息中添加 `cache_control: {"type": "ephemeral"}`
2. **准备足够的内容**：使用《傲慢与偏见》前 5 章文本（超过 2048 tokens）
3. **检查缓存状态**：通过响应中的 `usage` 字段验证缓存创建情况

### 重要参数说明

| 参数 | 说明 |
|------|------|
| `anthropic-version` | 必须设置为 `2023-06-01` 或更高版本 |
| `cache_control` | 设置为 `{"type": "ephemeral"}` 启用临时缓存 |
| `model` | 推荐使用 `claude-sonnet-4-6` |

## 📊 API 响应示例

### 控制台输出

```json
[START] 开始调用 Claude API（测试缓存创建）
[INFO] API 端点: https://www.dmxapi.cn/v1/messages
[INFO] 使用模型: claude-sonnet-4-6
------------------------------------------------------------
[SUCCESS] 请求成功!

[USAGE] Token 使用统计:
  - 输入 tokens: 17
  - 输出 tokens: 1043
  - 缓存创建 tokens: 2073
  - 缓存读取 tokens: 0

[CACHE] 缓存创建成功！已缓存 2073 tokens
[TIP] 提示：缓存仅保存5分钟，且命中率低

[RESPONSE] Claude 回复（前 300 字符）:
# Major Themes in Pride and Prejudice

Based on the opening chapters provided, here is an analysis of the major themes Austen establishes — and how they develop throughout the novel as a whole.

---

## 1. Marriage as Social and Economic Institution

The **very first sentence** announces this theme ...

[JSON] 完整 API 响应:
{
  "id": "msg_01QmF3bbu8KTPV4FFv8RMWZw",
  "type": "message",
  "role": "assistant",
  "model": "claude-sonnet-4-6",
  "content": [
    {
      "type": "text",
      "text": "# Major Themes in Pride and Prejudice\n\nBased on the opening chapters provided, here is an analysis of the major themes Austen establishes — and how they develop throughout the novel as a whole.\n\n---\n\n## 1. Marriage as Social and Economic Institution\n\nThe **very first sentence** announces this theme with deliberate irony:\n\n> *\"It is a truth universally acknowledged, that a single man in possession of a good fortune, must be in want of a wife.\"*\n\nAusten immediately signals that marriage is not primarily about love — it is about **property, security, and social positioning**. Mrs. Bennet's frantic interest in Bingley is entirely transactional. Her daughters represent investment opportunities rather than individuals with autonomous desires. This tension between **marriage for practical necessity** versus **marriage for genuine affection** drives the entire narrative.\n\n---\n\n## 2. Pride and Its Consequences\n\nThe title itself foregrounds this theme. Pride manifests in multiple forms:\n\n- **Darcy's aristocratic pride** — his sense of social superiority initially makes him dismissive and insulting\n- **Elizabeth's wounded pride** — her sharp wit can harden into prejudgment\n- **Sir William Lucas's pride** — Chapter 5 offers a gentle satirical portrait of a man whose knighthood has rendered him somewhat self-important, though harmlessly so\n\nAusten suggests that pride, unchecked, **distorts one's perception of others** and obstructs genuine human connection.\n\n---\n\n## 3. Prejudice and First Impressions\n\nNotably, Austen's working title for the novel was **\"First Impressions\"** — which captures this theme with equal precision. The opening chapters already demonstrate how characters form rapid judgments:\n\n- Mrs. Bennet judges Mrs. Long as *\"selfish and hypocritical\"* based on self-interest\n- The Bennet women evaluate Bingley entirely from **a window and secondhand reports**\n- Elizabeth's razor-sharp assessments, while often accurate, can also **calcify into unfair prejudice**\n\nThe novel ultimately argues that **first impressions require revision** through deeper knowledge and honest self-reflection.\n\n---\n\n## 4. The Role of Women in Society\n\nThese opening chapters quietly expose the **severely constrained position of women** in Regency England:\n\n- The Bennet daughters **cannot inherit** Longbourn due to the entail\n- Their financial security is entirely dependent on making advantageous marriages\n- They observe Bingley **from an upstairs window** — literally positioned as spectators rather than participants in their own social futures\n\nAusten treats this reality with both **sympathy and irony**, never allowing readers to forget the genuine stakes beneath the comic surface.\n\n---\n\n## 5. Wit, Intelligence, and Social Performance\n\nElizabeth Bennet's voice emerges immediately as the novel's moral compass, characterized by:\n\n- Sharp, self-aware humor\n- The ability to **see through social pretension**\n- Genuine affection balanced with critical intelligence\n\nHer exchange with Jane in Chapter 4 is telling — Elizabeth *expected* Bingley's attentions toward Jane because she assessed the situation clearly, while Jane was merely *delighted*. Austen implicitly values **clear-eyed intelligence** over passive sentiment.\n\n---\n\n## 6. Irony as a Moral Instrument\n\nAusten's narrative voice deserves recognition as a thematic vehicle in itself. Her irony is never merely decorative — it serves a **moral and critical function**:\n\n- The opening sentence mocks the community's assumptions while also acknowledging their social reality\n- Mr. Bennet's dry wit exposes his wife's absurdities while also revealing **his own irresponsibility** as a father\n- Sir William Lucas is described charitably yet the description gently **undermines his self-importance**\n\nThis sustained ironic register invites readers to **question surface appearances** — which is, essentially, what the entire novel asks its characters to do as well.\n\n---\n\n## Summary Table\n\n| Theme | Primary Expression |\n|---|---|\n| Marriage & Economics | Mrs. Bennet's matchmaking; the entail |\n| Pride | Darcy's social hauteur; class distinctions |\n| Prejudice | Elizabeth's swift judgments; community gossip |\n| Women's Social Position | Dependence on marriage for security |\n| Intelligence & Wit | Elizabeth as moral and intellectual center |\n| Irony | Austen's narrative voice throughout |\n\n---\n\nThese themes are introduced with **remarkable economy** in just five chapters, demonstrating Austen's extraordinary craft in embedding complex social criticism within the conventions of drawing-room comedy."
    }
  ],
  "stop_reason": "end_turn",
  "usage": {
    "input_tokens": 17,
    "cache_creation_input_tokens": 2073,
    "cache_read_input_tokens": 0,
    "output_tokens": 1043,
    "cache_creation": {
      "ephemeral_5m_input_tokens": 2073
    },
    "claude_cache_creation_5_m_tokens": 0,
    "claude_cache_creation_1_h_tokens": 0
  }
}

[DONE] 程序执行完成
```

### 响应字段解析

#### Usage 统计信息

| 字段 | 值 | 说明 |
|------|-----|------|
| `input_tokens` | 17 | 本次请求的新输入 tokens（用户消息部分） |
| `output_tokens` | 1043 | AI 生成的响应 tokens |
| `cache_creation_input_tokens` | 2073 | **缓存创建的 tokens 数量** ✅ |

## ⚠️ 注意事项

### 缓存要求

1. **最小长度**：缓存内容必须 ≥ 1024 tokens
2. **推荐长度**：建议使用 2048+ tokens 以提高成功率
3. **有效期限**：缓存保存 5 分钟后自动失效
4. **命中率**：实际场景中缓存命中率非常低

### 使用建议

- 💡 适合缓存：大型系统提示词、参考文档、示例数据
- 💡 不适合缓存：频繁变化的内容、一次性请求
- 💡 成本优化：仅在需要多次使用相同上下文时使用缓存

### API 密钥安全

⚠️ **重要**：示例代码中的 API 密钥仅供演示，请务必：

- 使用您自己的 API 密钥
- 不要将密钥硬编码在代码中
- 建议通过环境变量管理密钥
- 不要将包含真实密钥的代码提交到公开仓库


---

<p align="center">
  <small>© 2025 DMXAPI 提示词缓存</small>
</p>
