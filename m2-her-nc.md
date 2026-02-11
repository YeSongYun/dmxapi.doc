# M2-her 普通对话文档
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
api_key = "sk-**************************************"
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
# ═══════════════════════════════════════════════════════════════
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
api_key = "sk-******************************************"
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


    ],
    "stream": True, # 是否使用流式传输，默认为 false

    # 【max_completion_tokens】：指定生成内容长度的上限（Token 数），上限为 2048。
    #  超过上限的内容会被截断。如果生成因 length 原因中断，请尝试调高此值。必填范围: x >= 1
    "max_completion_tokens": 2000,

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
  "completed_at": 1770798191,
  "created_at": 1770798191,
  "id": "resp_fd306d14ca1e44eb8d52b7d691ace147",
  "model": "M2-her",
  "object": "response",
  "output": [
    {
      "content": [
        {
          "text": "鲁迅（1881年9月25日－1936年10月19日），浙江绍兴人，原名周樟寿，后改名周树人，字豫山，后改豫才，"鲁迅"是他1918年发表《狂人日记》时所用的笔名，也是他影响最为广泛的笔名。他是中国近现代文化巨匠，以文学家、思想家、革命家、教育家等多重身份闻名。鲁迅早年曾留学日本学医，后弃医从文，决心用笔唤醒国民意识。他一生笔耕不辍，代表作包括小说集《呐喊》《彷徨》，散文诗集《野草》，杂文集《热风》《华盖集》等。他的作品以犀利的笔锋批判封建礼教和社会黑暗，具有深刻的思想性和艺术性，对中国现代文学和思想文化产生深远影响。鲁迅先生逝世后，其作品被广泛整理和研究，成为中国现代文学的经典。",
          "type": "output_text"
        }
      ],
      "id": "msg_8efc88095bf94ff69ad95f1ebe715f45",
      "role": "assistant",
      "status": "completed",
      "type": "message"
    }
  ],
  "status": "completed",
  "usage": {
    "input_tokens": 181,
    "input_tokens_details": {
      "cached_tokens": 0
    },
    "output_tokens": 184,
    "output_tokens_details": {
      "reasoning_tokens": 0
    },
    "total_tokens": 365
  }
}
```

```json [返回示例（流式输出）]
event: response.created
data: {"response":{"created_at":1770798626,"id":"resp_54cc20ae0a094a8dac1ac3737f8bee6c","model":"M2-her","object":"response","output":[],"status":"in_progress"},"sequence_number":0,"type":"response.created"}
event: response.in_progress
data: {"response":{"created_at":1770798626,"id":"resp_54cc20ae0a094a8dac1ac3737f8bee6c","model":"M2-her","object":"response","output":[],"status":"in_progress"},"sequence_number":1,"type":"response.in_progress"}
event: response.output_item.added
data: {"item":{"content":[],"id":"msg_30eb5bc9f3ae418ba844ff4c70e5ac98","role":"assistant","status":"in_progress","type":"message"},"output_index":0,"sequence_number":2,"type":"response.output_item.added"}
event: response.content_part.added
data: {"content_index":0,"item_id":"msg_30eb5bc9f3ae418ba844ff4c70e5ac98","output_index":0,"part":{"text":"","type":"output_text"},"sequence_number":3,"type":"response.content_part.added"}
event: response.output_text.delta
data: {"content_index":0,"delta":"鲁迅，原","item_id":"msg_30eb5bc9f3ae418ba844ff4c70e5ac98","output_index":0,"sequence_number":4,"type":"response.output_text.delta"}
event: response.output_text.delta
data: {"content_index":0,"delta":"名周树人，是中国现代文学的奠基人之一。","item_id":"msg_30eb5bc9f3ae418ba844ff4c70e5ac98","output_index":0,"sequence_number":5,"type":"response.output_text.delta"}
event: response.output_text.delta
data: {"content_index":0,"delta":"1881年生于浙江绍兴，1902年赴日本留学学","item_id":"msg_30eb5bc9f3ae418ba844ff4c70e5ac98","output_index":0,"sequence_number":6,"type":"response.output_text.delta"}
event: response.output_text.delta
data: {"content_index":0,"delta":"医，后弃医从文，致力于唤醒国民意识。1918年发表","item_id":"msg_30eb5bc9f3ae418ba844ff4c70e5ac98","output_index":0,"sequence_number":7,"type":"response.output_text.delta"}
event: response.output_text.delta
data: {"content_index":0,"delta":"第一篇白话小说《狂人日记》，开创中国现代文学先","item_id":"msg_30eb5bc9f3ae418ba844ff4c70e5ac98","output_index":0,"sequence_number":8,"type":"response.output_text.delta"}
event: response.output_text.delta
data: {"content_index":0,"delta":"河。代表作包括《阿Q正传》《孔乙己》《祝福》等，","item_id":"msg_30eb5bc9f3ae418ba844ff4c70e5ac98","output_index":0,"sequence_number":9,"type":"response.output_text.delta"}
event: response.output_text.delta
data: {"content_index":0,"delta":"批判封建制度、揭露社会黑暗","item_id":"msg_30eb5bc9f3ae418ba844ff4c70e5ac98","output_index":0,"sequence_number":10,"type":"response.output_text.delta"}
event: response.output_text.delta
data: {"content_index":0,"delta":"。其杂文犀利深刻，如《呐喊》《坟","item_id":"msg_30eb5bc9f3ae418ba844ff4c70e5ac98","output_index":0,"sequence_number":11,"type":"response.output_text.delta"}
event: response.output_text.delta
data: {"content_index":0,"delta":"》，倡导新文化运动。1936年逝世，","item_id":"msg_30eb5bc9f3ae418ba844ff4c70e5ac98","output_index":0,"sequence_number":12,"type":"response.output_text.delta"}
event: response.output_text.delta
data: {"content_index":0,"delta":"鲁迅以"横眉冷对千夫指"的精神成为民族","item_id":"msg_30eb5bc9f3ae418ba844ff4c70e5ac98","output_index":0,"sequence_number":13,"type":"response.output_text.delta"}
event: response.output_text.delta
data: {"content_index":0,"delta":"魂，影响深远。","item_id":"msg_30eb5bc9f3ae418ba844ff4c70e5ac98","output_index":0,"sequence_number":14,"type":"response.output_text.delta"}
event: response.output_text.done
data: {"content_index":0,"item_id":"msg_30eb5bc9f3ae418ba844ff4c70e5ac98","output_index":0,"sequence_number":15,"text":"鲁迅，原名周树人，是中国现代文学的奠基人之一。1881 年生于浙江绍兴，1902年赴日本留学学医，后弃医从文，致力于唤醒国民意识。1918年发表第一篇白话小说《狂人日记》，开创中国现代文学先河。代表作包括《阿Q正传》《孔乙己》《祝福》等，批判封建制度、揭露社会黑暗。其杂文犀利深刻，如《呐喊》《坟》，倡导新文化运动。1936年逝世，鲁迅以"横眉冷对千夫指"的精神成为民族魂，影响深远。","type":"response.output_text.done"}
event: response.content_part.done
data: {"content_index":0,"item_id":"msg_30eb5bc9f3ae418ba844ff4c70e5ac98","output_index":0,"part":{"text":"鲁迅，原名周树人，是中国现代文学的奠基人之一。1881年生于浙江绍兴，1902年赴日本留学学医，后弃医从文，致力于唤醒国民意识。1918年发表第一篇白话小说《狂人日记》，开创中国现代文学先河。代表作包括《阿Q正传》《孔乙己》《祝福》等，批判封建制度、揭露社会黑暗。其杂文犀利深刻，如《呐喊》《坟》，倡导新文化运动。1936年逝世，鲁迅以"横眉冷对千夫指"的精神成为民族魂，影响深远。","type":"output_text"},"sequence_number":16,"type":"response.content_part.done"}
event: response.output_item.done
data: {"item":{"content":[{"text":"鲁迅，原名周树人，是中国现代文学的奠基人之一。1881年生于浙江绍兴，1902年赴日本留学学医，后弃医从文，致力于唤醒国民意识。1918年发表第一篇白话小说《狂人日记》，开创中国现代文学先河。代表作包括《阿Q正传》《孔乙己》《祝福》等，批判封建制度、揭露社会黑暗。其杂文犀利深刻，如《呐喊》《坟》，倡导新文化运动。1936年逝世，鲁迅以"横眉冷对千夫指"的精神成为民族魂，影响深远。","type":"output_text"}],"id":"msg_30eb5bc9f3ae418ba844ff4c70e5ac98","role":"assistant","status":"completed","type":"message"},"output_index":0,"sequence_number":17,"type":"response.output_item.done"}
event: response.completed
data: {"response":{"completed_at":1770798629,"created_at":1770798626,"id":"resp_54cc20ae0a094a8dac1ac3737f8bee6c","model":"M2-her","object":"response","output":[{"content":[{"text":"鲁迅，原名周树人，是中国现代文学的奠基人之一。1881年生于浙江绍兴，1902年赴日本留学学医，后弃医从文，致力于唤醒国民意识。1918年发表第一篇白话小说《狂人日记》，开创中国现代文学先河。代表作包括《阿Q正传》《孔乙己》《祝福》等，批判封建制度、揭露社会黑暗。其杂文犀利深刻，如《呐喊》《坟》，倡导新文化运动。1936年逝世，鲁迅以"横眉冷对千夫指"的精神成为民族魂，影响深远。","type":"output_text"}],"id":"msg_30eb5bc9f3ae418ba844ff4c70e5ac98","role":"assistant","status":"completed","type":"message"}],"status":"completed","usage":{"input_tokens":181,"input_tokens_details":{"cached_tokens":0},"output_tokens":121,"output_tokens_details":{"reasoning_tokens":0},"total_tokens":302}},"sequence_number":18,"type":"response.completed"}
```
:::


<p align="center">
  <small>© 2026 DMXAPI m2-her 普通对话</small>
</p>
