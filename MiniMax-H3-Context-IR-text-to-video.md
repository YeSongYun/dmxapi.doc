# MiniMax-H3-Context-IR 文生视频 API 使用文档

MiniMax-H3-Context-IR 是 MiniMax-H3 的多模态上下文理解与提示词增强接口：它对文本、图像、音频、视频等多模态上下文进行深度理解，分析素材之间以及素材与目标生成结果之间的关系并进行复杂逻辑推理，再把理解结果转换为结构化表达，在尽量保持用户原始意图的前提下丰富语义细节。**本接口只返回增强后的视频提示词，不会创建视频生成任务、不产出视频**；拿到增强提示词后，可再把它作为最终 prompt 投喂给 MiniMax-H3 视频生成接口出片。文生视频场景仅需在 `input` 数组中提供一个非空文本项，单个 `text` 最多 7000 个字符；`duration` 必填、取 4~15 秒整数；文生视频场景下 `ratio` 必填且不可为 `adaptive`，可选 21:9、16:9、4:3、1:1、3:4、9:16。接口以异步任务方式工作：提交后返回任务 ID，再用查询模型换取增强后的提示词。

## 接口地址

| 接口 | 请求方式 | URL |
|------|---------|-----|
| 提交任务 | POST | `https://www.dmxapi.cn/v1/responses` |
| 获取结果 | POST | `https://www.dmxapi.cn/v1/responses` |



:::warning
请妥善保管您的 API Key！严禁将密钥泄露给他人、硬编码到代码中或提交到公开的代码仓库。如果怀疑密钥已泄露，请立即前往 DMXAPI 官网重新生成。
:::

:::warning 本接口只产出提示词，不产出视频
`MiniMax-H3-Context-IR` 是提示词增强接口，任务成功后返回的是结构化的增强提示词（`task.content.prompt`），**不会生成任何视频文件**。如需出片，请把该提示词作为 `text` 再提交给 MiniMax-H3 视频生成接口。
:::

:::warning 异步任务，请妥善保存 task_id
本模型为**异步任务**接口：提交任务后不会直接返回提示词，只返回一个任务 ID（`task_id`），需再用查询模型 `MiniMax-H3-get` 凭该 ID 换取增强后的提示词。请在提交成功后立即将 `task_id` 落库或写入日志妥善保存——一旦丢失将无法找回，本次生成结果也无法再取回，但费用已产生。
:::

## 模型名称

- `MiniMax-H3-Context-IR`

## 文生视频示例代码

```python
import requests
import json

# ===============================================================
# 步骤1: 配置 API 连接信息
# ===============================================================

# DMXAPI 服务端点地址
url = "https://www.dmxapi.cn/v1/responses"

# DMXAPI 密钥 (请替换为您自己的密钥)
# 获取方式: 登录 DMXAPI 官网 -> 个人中心 -> API 密钥管理
api_key = "sk-***********************************************"

# ===============================================================
# 步骤2: 配置请求头
# ===============================================================

headers = {
    "Content-Type": "application/json",      # 指定请求体为 JSON 格式
    "Authorization": f"{api_key}",           # token 认证方式
}

# ===============================================================
# 步骤3: 配置请求参数
# ===============================================================

payload = {
    # 【model】(enum<string>, 必填) 模型名称
    # 可用值: "MiniMax-H3-Context-IR"
    "model": "MiniMax-H3-Context-IR",

    # 【input】(object[], 必填) 多模态上下文输入数组，
    # 用于描述目标视频及各类素材之间的关系
    # 每个元素通过 type 区分类型("text" / "image_url" / "video_url" / "audio_url")，
    # 并可通过 role 标注用途
    # 每次请求必须包含一个非空 text 项(prompt 必填)，缺失会返回参数错误
    # 文生视频场景: 仅一个 text 元素
    "input": [
        {
            # 【type】(enum<string>, 必填) 输入内容的类型
            # 可用值: "text" / "image_url" / "video_url" / "audio_url"
            "type": "text",

            # 【text】(string, 必填) 文本提示词(prompt)
            # 所有场景都需包含一个非空 text，描述期望生成的视频
            # 按字符数计算长度，单个 text 最多 7000 个字符
            "text": "史诗级太空歌剧院线预告：女舰长独自站在巨大观景窗前，最后一支舰队正在集结并跃迁离去，强光爆闪、舰桥震动，她被留在原地。"
        }
    ],

    # 【duration】(enum<integer>, 必填) 目标视频时长(秒)，整数
    # 该值参与上下文推理，决定增强提示词中的镜头编排与节奏，
    # 并原样回显在查询结果的 task.duration 中
    # 可用值: 4 / 5 / 6 / 7 / 8 / 9 / 10 / 11 / 12 / 13 / 14 / 15
    "duration": 5,

    # 【ratio】(enum<string>, 条件必填) 目标视频的宽高比
    # 同样参与上下文推理(影响增强提示词中的构图与取景描述)，
    # 并原样回显在查询结果的 task.ratio 中
    # 文生视频(t2va，输入仅含 text)场景: ratio 必填，且不能为 "adaptive"
    # 本场景可用值: "21:9" / "16:9" / "4:3" / "1:1" / "3:4" / "9:16"
    "ratio": "16:9"
}


# ===============================================================
# 步骤4: 发送请求并输出结果
# ===============================================================

# 发送 POST 请求到 API 服务器
response = requests.post(url, headers=headers, json=payload)

# 格式化输出 JSON 响应
# - indent=2: 缩进 2 空格，便于阅读
# - ensure_ascii=False: 正确显示中文字符
print(json.dumps(response.json(), indent=2, ensure_ascii=False))
```

## 返回示例

```json
{
  "output": [
    {
      "type": "message",
      "content": [
        {
          "type": "output_text",
          "text": "436617845764531"
        }
      ]
    }
  ],
  "usage": {
    "input_tokens": 0,
    "input_tokens_details": {
      "cached_tokens": 0
    },
    "output_tokens": 1000,
    "output_tokens_details": {
      "reasoning_tokens": 0
    },
    "total_tokens": 1000
  }
}
```

`output[0].content[0].text` 即任务 ID（本例为 `436617845764531`），用于后续查询任务状态与结果。**该 ID 仅在本次提交的响应中返回一次，请务必妥善保存**，丢失后无法找回本次任务。

## 获取增强提示词 示例代码

```python
import requests
import json

# ===============================================================
# 步骤1: 配置 API 连接信息
# ===============================================================

# DMXAPI 服务端点地址
url = "https://www.dmxapi.cn/v1/responses"

# DMXAPI 密钥 (请替换为您自己的密钥)
# 获取方式: 登录 DMXAPI 官网 -> 个人中心 -> API 密钥管理
api_key = "sk-***********************************************"

# ===============================================================
# 步骤2: 配置请求头
# ===============================================================

headers = {
    "Content-Type": "application/json",      # 指定请求体为 JSON 格式
    "Authorization": f"{api_key}",           # token 认证方式
}

# ===============================================================
# 步骤3: 配置请求参数
# ===============================================================

payload = {

    "model": "MiniMax-H3-get",
    "input": "436617845764531"

}


# ===============================================================
# 步骤4: 发送请求并输出结果
# ===============================================================

# 发送 POST 请求到 API 服务器
response = requests.post(url, headers=headers, json=payload)

# 格式化输出 JSON 响应
# - indent=2: 缩进 2 空格，便于阅读
# - ensure_ascii=False: 正确显示中文字符
print(json.dumps(response.json(), indent=2, ensure_ascii=False))
```

## 返回示例

```json
{
  "task": {
    "id": "436617845764531",
    "model": "MiniMax-H3",
    "status": "succeeded",
    "created_at": 1788150688,
    "updated_at": 1788150709,
    "content": {
      "prompt": "integrated_multimodal_description: [Shot 1] Cinematic, medium wide shot from behind, the camera slowly pushes in on a female starship captain in her mid-forties with short, sharp black hair. She is wearing a structured dark navy officer's uniform with silver epaulettes, standing dead center in the foreground with her hands clasped behind her back. Before her lies a colossal, curved observation window that spans the entire background, framing the cold, deep blue void of space. The dimly lit bridge features sleek obsidian floors and subtle amber holographic consoles glowing in the periphery. Outside the massive glass pane, a heavily armored fleet of dark grey dreadnoughts with intensely glowing blue thrusters assembles. Suddenly, the warships stretch out and streak forward, triggering a blinding white-blue flash that floods the dark interior, throwing the captain into a stark, sharp silhouette. As the immense energy of the jump ripples outward, the camera shakes strongly, capturing the violent, physical vibration of the bridge. The captain braces her legs and slightly broadens her shoulders, holding her ground without flinching. The intense light quickly fades back to a dim, cold ambient glow, revealing the vast, star-speckled expanse outside to be completely empty.\noverall_soundscape: A deep, continuous low-frequency hum of the ship's massive engines fills the room, suddenly overwhelmed by a piercing, high-pitched synthetic crackle and a massive booming thud as the fleet initiates the jump. A loud metallic clatter and heavy rattling instantly follow, reflecting the violent shaking of the hull, before sharply receding into a hollow, quiet ambient drone.\nnon_diegetic_music: Cinematic orchestral score, slow tempo, featuring a sweeping brass crescendo that peaks powerfully with the flash of light and abruptly drops out, leaving only a solitary, sustained low cello drone."
    },
    "duration": 5,
    "usage": {
      "total_tokens": 7802,
      "prompt_tokens": 5689,
      "completion_tokens": 2113
    },
    "ratio": "16:9",
    "task_type": "h3_context_ir",
    "modality": "text"
  },
  "usage": {
    "total_tokens": 0,
    "input_tokens": 0,
    "input_tokens_details": {
      "cached_tokens": 0
    },
    "output_tokens": 0,
    "output_tokens_details": {
      "reasoning_tokens": 0
    }
  }
}
```

<p align="center">
  <small>© 2026 DMXAPI MiniMax-H3-Context-IR 文生视频</small>
</p>
