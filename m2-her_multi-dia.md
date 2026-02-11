# M2-her 多轮对话文档
MiniMax-M2-her 是 MiniMax 专门为深度 AI 陪伴和角色扮演场景打造的模型，是星野/Talkie 产品的底层模型。支持角色扮演、多轮对话等对话场景。支持丰富的角色设定（system、user_system、group 等）和示例对话学习。  
该模型支持流式与非流式两种输出形式

## 请求地址

```
https://www.dmxapi.cn/v1/responses
```

## 模型名称

- `M2-her`

## 示例代码
::: code-group

```python [非流式输出]
import requests
import json
# ═══════════════════════════════════════════════════════════════
# 🔑 步骤1: 配置 API 连接信息
# ═══════════════════════════════════════════════════════════════

# 🌐 DMXAPI 服务端点地址
url = "https://www.dmxapi.cn/v1/responses"

# 🔐 DMXAPI 密钥 (请替换为您自己的密钥)
# 获取方式: 登录 DMXAPI 官网 -> 个人中心 -> API 密钥管理
api_key = "sk-*******************************************"
# ═══════════════════════════════════════════════════════════════
# 📋 步骤2: 配置请求头
# ═══════════════════════════════════════════════════════════════

headers = {
    "Content-Type": "application/json",      # 指定请求体为 JSON 格式
    "Authorization": f"{api_key}",    # token 认证方式
}
# ═══════════════════════════════════════════════════════════════
# 💬 步骤3: 配置请求参数
# ═══════════════════════════════════════════════════════════════

payload = {
    "model": "M2-her",
    "input": [
    {
            # 【role】:消息发送者的角色
            # system:系统角色
            # user:用户角色
            # assistant: 模型的历史回复
            # user_system: 设定用户的角色和人设
            # group: 对话的名称
            # sample_message_user: 示例的用户输入
            # sample_message_ai: 示例的模型输出
            "role": "system",

            # 【name】:发送者的名称。若同一类型的角色有多个，须提供具体名称以区分
            "name": "MiniMax AI"
        },
        {
            "role": "user",
            "content": "介绍下鲁迅，200字",
            "name": "用户"
        },

        {
        'role': 'assistant',
        'content': '鲁迅（1881—1936），原名周树人，字豫才，浙江绍兴人，中国现代文学奠基人、思想家与革命家。幼年接受传统私塾教育，1902年赴日学医，后弃医从文，立志以笔唤醒国民精神。1918年以"鲁迅"笔名发表白话小说《狂人日记》，开创中国现代小说先河。代表作《阿Q正传》《呐喊》《彷徨》等，以冷峻锋利的文笔揭露社会痼疾、批判封建礼教，塑造了孔乙己、祥林嫂等经典文学形象。晚年专注杂文创作，直指时弊，思想深邃，被誉为"民族魂"。其作品兼具文学性与思想性，对中国现代文化与社会变革影响深远。',
        'name': 'MiniMax AI',
        },

        {
        "role": "user",
        "content": "他为什么弃医从文",
        "name": "用户"
        },
    ],
    "stream": False, # 是否使用流式传输，默认为 false

    # 【max_completion_tokens】：指定生成内容长度的上限（Token 数），上限为 2048。
    #  超过上限的内容会被截断。如果生成因 length 原因中断，请尝试调高此值。必填范围: x >= 1
    "max_completion_tokens": 2000,

    # 【temperature】：温度系数，影响输出随机性，取值范围 (0, 1]，
    #  M2-her 模型默认值为 1.0。值越高，输出越随机；值越低，输出越确定，必填范围: 0 < x <= 1
    "temperature":  1,
    "top_p": 0.5 # 采样策略，影响输出随机性，取值范围 (0, 1]，M2-her 模型默认值为 0.95
}
# # ═══════════════════════════════════════════════════════════════
# 📤 步骤4: 发送请求并输出结果
# ═══════════════════════════════════════════════════════════════

# 发送 POST 请求到 API 服务器
response = requests.post(url, headers=headers, json=payload)

# 格式化输出 JSON 响应
# - indent=2: 缩进 2 空格，便于阅读
# - ensure_ascii=False: 正确显示中文字符
print(json.dumps(response.json(), indent=2, ensure_ascii=False))
```
```python [流式输出]
import requests
import json
# ═══════════════════════════════════════════════════════════════
# 🔑 步骤1: 配置 API 连接信息
# ═══════════════════════════════════════════════════════════════

# 🌐 DMXAPI 服务端点地址
url = "https://www.dmxapi.cn/v1/responses"

# 🔐 DMXAPI 密钥 (请替换为您自己的密钥)
# 获取方式: 登录 DMXAPI 官网 -> 个人中心 -> API 密钥管理
api_key = "sk-*******************************************"
# ═══════════════════════════════════════════════════════════════
# 📋 步骤2: 配置请求头
# ═══════════════════════════════════════════════════════════════

headers = {
    "Content-Type": "application/json",      # 指定请求体为 JSON 格式
    "Authorization": f"{api_key}",    # token 认证方式
}
# ═══════════════════════════════════════════════════════════════
# 💬 步骤3: 配置请求参数
# ═══════════════════════════════════════════════════════════════

payload = {
    "model": "M2-her",
    "input": [
    {
            # 【role】:消息发送者的角色
            # system:系统角色
            # user:用户角色
            # assistant: 模型的历史回复
            # user_system: 设定用户的角色和人设
            # group: 对话的名称
            # sample_message_user: 示例的用户输入
            # sample_message_ai: 示例的模型输出
            "role": "system",

            # 【name】:发送者的名称。若同一类型的角色有多个，须提供具体名称以区分
            "name": "MiniMax AI"
        },
        {
            "role": "user",
            "content": "介绍下鲁迅，200字",
            "name": "用户"
        },
        {
        'role': 'assistant',
        'content': '鲁迅（1881—1936），原名周树人，字豫才，浙江绍兴人，中国现代文学奠基人、思想家与革命家。幼年接受传统私塾教育，1902年赴日学医，后弃医从文，立志以笔唤醒国民精神。1918年以"鲁迅"笔名发表白话小说《狂人日记》，开创中国现代小说先河。代表作《阿Q正传》《呐喊》《彷徨》等，以冷峻锋利的文笔揭露社会痼疾、批判封建礼教，塑造了孔乙己、祥林嫂等经典文学形象。晚年专注杂文创作，直指时弊，思想深邃，被誉为"民族魂"。其作品兼具文学性与思想性，对中国现代文化与社会变革影响深远。',
        'name': 'MiniMax AI',
        },

        {
        "role": "user",
        "content": "他为什么弃医从文",
        "name": "用户"
        },
    ],
    "stream": True, # 是否使用流式传输，默认为 false

    # 【max_completion_tokens】：指定生成内容长度的上限（Token 数），上限为 2048。
    #  超过上限的内容会被截断。如果生成因 length 原因中断，请尝试调高此值。必填范围: x >= 1
    "max_completion_tokens": 2048,

    # 【temperature】：温度系数，影响输出随机性，取值范围 (0, 1]，
    #  M2-her 模型默认值为 1.0。值越高，输出越随机；值越低，输出越确定，必填范围: 0 < x <= 1
    "temperature":  1,
    "top_p": 0.5 # 采样策略，影响输出随机性，取值范围 (0, 1]，M2-her 模型默认值为 0.95
}
# ═══════════════════════════════════════════════════════════════
# 📤 步骤4: 发送请求并输出结果
# ═══════════════════════════════════════════════════════════════

# 发送 POST 请求到 API 服务器 (stream=True 启用流式传输)
response = requests.post(url, headers=headers, json=payload, stream=True)

# 逐行读取 SSE 流式响应
for line in response.iter_lines():
    if line:
        line = line.decode('utf-8')
        print(line)
```
:::

## 返回示例
::: code-group

```json [返回示例（非流式输出）]
{
  "completed_at": 1770802024,
  "created_at": 1770802024,
  "id": "resp_c118a113e2fe44dfaad104e48acf4602",
  "model": "M2-her",
  "object": "response",
  "output": [
    {
      "content": [
        {
          "text": "鲁迅弃医从文的核心原因是他在日本留学期间的深刻触动。在仙台医专学习时，他通过幻灯片看到中国人围观同胞被日军处决的麻木场景，意识到"医学并非要紧事，凡是愚弱的国民，即使体格如何健全，如何茁壮，也只能做毫无意义的示众的材料和看客"。这一经历让他认识到，拯救民族的根本在于改变国民的精神状态，而非医治身体。因此，他决定以文学为武器，通过文字唤醒民众的觉醒，揭露社会的黑暗与不公，从而推动社会的进步。",
          "type": "output_text"
        }
      ],
      "id": "msg_edafa051e85c4adfa06a1023cb733d5a",
      "role": "assistant",
      "status": "completed",
      "type": "message"
    }
  ],
  "status": "completed",
  "usage": {
    "input_tokens": 366,
    "input_tokens_details": {
      "cached_tokens": 0
    },
    "output_tokens": 107,
    "output_tokens_details": {
      "reasoning_tokens": 0
    },
    "total_tokens": 473
  }
}
```
```json [返回示例（流式输出）]
event: response.created
data: {"response":{"created_at":1770800197,"id":"resp_f95bdaccd5f04041a07cabab45cd94b0","model":"M2-her","object":"response","output":[],"status":"in_progress"},"sequence_number":0,"type":"response.created"}
event: response.in_progress
data: {"response":{"created_at":1770800197,"id":"resp_f95bdaccd5f04041a07cabab45cd94b0","model":"M2-her","object":"response","output":[],"status":"in_progress"},"sequence_number":1,"type":"response.in_progress"}
event: response.output_item.added
data: {"item":{"content":[],"id":"msg_1f2ec4a8af8440139b5a279b947cb3b3","role":"assistant","status":"in_progress","type":"message"},"output_index":0,"sequence_number":2,"type":"response.output_item.added"}
event: response.content_part.added
data: {"content_index":0,"item_id":"msg_1f2ec4a8af8440139b5a279b947cb3b3","output_index":0,"part":{"text":"","type":"output_text"},"sequence_number":3,"type":"response.content_part.added"}
event: response.output_text.delta
data: {"content_index":0,"delta":"鲁迅在日本","item_id":"msg_1f2ec4a8af8440139b5a279b947cb3b3","output_index":0,"sequence_number":4,"type":"response.output_text.delta"}
event: response.output_text.delta
data: {"content_index":0,"delta":"学医时，曾看到一部日俄战争教育片中，中国","item_id":"msg_1f2ec4a8af8440139b5a279b947cb3b3","output_index":0,"sequence_number":5,"type":"response.output_text.delta"}
event: response.output_text.delta
data: {"content_index":0,"delta":"人围观日军处决同胞","item_id":"msg_1f2ec4a8af8440139b5a279b947cb3b3","output_index":0,"sequence_number":6,"type":"response.output_text.delta"}
event: response.output_text.delta
data: {"content_index":0,"delta":"，神情麻木。这让他意识到，医学能","item_id":"msg_1f2ec4a8af8440139b5a279b947cb3b3","output_index":0,"sequence_number":7,"type":"response.output_text.delta"}
event: response.output_text.delta
data: {"content_index":0,"delta":"治疗身体，却无法唤醒精神上的麻木。此后","item_id":"msg_1f2ec4a8af8440139b5a279b947cb3b3","output_index":0,"sequence_number":8,"type":"response.output_text.delta"}
event: response.output_text.delta
data: {"content_index":0,"delta":"他弃医从文，以笔为剑","item_id":"msg_1f2ec4a8af8440139b5a279b947cb3b3","output_index":0,"sequence_number":9,"type":"response.output_text.delta"}
event: response.output_text.delta
data: {"content_index":0,"delta":"，致力改变国民精神，以文学为武器批判封建社会","item_id":"msg_1f2ec4a8af8440139b5a279b947cb3b3","output_index":0,"sequence_number":10,"type":"response.output_text.delta"}
event: response.output_text.delta
data: {"content_index":0,"delta":"、唤醒民众意识。","item_id":"msg_1f2ec4a8af8440139b5a279b947cb3b3","output_index":0,"sequence_number":11,"type":"response.output_text.delta"}
event: response.output_text.done
data: {"content_index":0,"item_id":"msg_1f2ec4a8af8440139b5a279b947cb3b3","output_index":0,"sequence_number":12,"text":"鲁迅在日本学医时，曾看到一部日俄战争教育片中，中国人围观日军处决同胞，神情麻木。这让他意识到，医学能治疗身体，却无法唤醒精神上的麻木。此后他弃医从文，以笔为剑，致力改变国民精神，以文学为武器批判封建社会、唤醒民众意识。","type":"response.output_text.done"}
event: response.content_part.done
data: {"content_index":0,"item_id":"msg_1f2ec4a8af8440139b5a279b947cb3b3","output_index":0,"part":{"text":"鲁迅在日本学医时，曾看到一部日俄战争教育片中，中国人围观日军处决同胞，神情麻木。这让他意识到，医学能治疗身体，却无法唤醒精神上的麻木。此后他弃医从文，以笔为剑，致力改变国民精神，以文学为武器批判封建社会、唤醒民众意识。","type":"output_text"},"sequence_number":13,"type":"response.content_part.done"}
event: response.output_item.done
data: {"item":{"content":[{"text":"鲁迅在日本学医时，曾看到一部日俄战争教育片中，中国人围观日军处决同胞，神情麻木。这让他意识到，医学能治疗身体，却无法唤醒精神上的麻木。此后他弃医从文，以笔为剑，致力改变国民精神，以文学为武器批判封建社会、唤醒民众意识。","type":"output_text"}],"id":"msg_1f2ec4a8af8440139b5a279b947cb3b3","role":"assistant","status":"completed","type":"message"},"output_index":0,"sequence_number":14,"type":"response.output_item.done"}
event: response.completed
data: {"response":{"completed_at":1770800199,"created_at":1770800197,"id":"resp_f95bdaccd5f04041a07cabab45cd94b0","model":"M2-her","object":"response","output":[{"content":[{"text":"鲁迅在日本学医时，曾看到一部日俄战争教育片中，中国人围观日军处决同胞，神情麻木。这让他意识到，医学能治疗身体，却无法唤醒精神上的麻木。此后他弃医从文，以笔为剑，致力改变国民精神，以文学为武器批判封建社会、唤醒民众意识。","type":"output_text"}],"id":"msg_1f2ec4a8af8440139b5a279b947cb3b3","role":"assistant","status":"completed","type":"message"}],"status":"completed","usage":{"input_tokens":366,"input_tokens_details":{"cached_tokens":0},"output_tokens":63,"output_tokens_details":{"reasoning_tokens":0},"total_tokens":429}},"sequence_number":15,"type":"response.completed"}
```
:::


<p align="center">
  <small>© 2026 DMXAPI m2-her 多轮对话</small>
</p>
