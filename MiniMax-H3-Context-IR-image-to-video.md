# MiniMax-H3-Context-IR 图生视频 API 使用文档

基于 MiniMax H3-Context-IR 的图生视频提示词增强接口，通过 `/v1/responses` 端点以异步任务方式调用。接口对文本与图像组成的多模态上下文进行深度理解，分析素材之间以及素材与目标生成结果之间的关系并进行复杂逻辑推理，将其转换为结构化、语义更丰富的视频提示词；请注意本接口只返回增强后的视频提示词，不会创建视频生成任务，任务成功后从 `content.prompt` 读取结果。图生视频场景由一个 `text` 元素搭配 `role` 为 `first_frame` 的首帧图片构成，单张图片支持 JPG、JPEG、PNG、WEBP、HEIC、HEIF 六种格式、不超过 30 MB、宽高在 [256, 5760] 像素且长宽比在 [0.4, 2.5] 区间，目标时长支持 4~15 秒的整数取值，宽高比由输入图片决定而恒为 `adaptive`，适合以一张定帧图为锚点扩写出连贯的镜头调度、声场与配乐描述。

## 接口地址

| 接口 | 请求方式 | URL |
|------|---------|-----|
| 提交任务 | POST | `https://www.dmxapi.cn/v1/responses` |
| 获取结果 | POST | `https://www.dmxapi.cn/v1/responses` |



:::warning
请妥善保管您的 API Key！严禁将密钥泄露给他人、硬编码到代码中或提交到公开的代码仓库。如果怀疑密钥已泄露，请立即前往 DMXAPI 官网重新生成。
:::

## 模型名称

- `MiniMax-H3-Context-IR`

## 图生视频 示例代码

```python
import requests
import json
import base64
import binascii
import os

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
# 步骤3: 配置图片来源 (选择一种即可)
# ===============================================================

# 【方式一】网络图片 URL (支持 HTTP / HTTPS 协议)
# image_source = "https://cdn.hailuoai.com/prod/hailuo_demo/testsets/H3_AA_I2VA/gallery/sr_v17_variants_seed42_43_20260724/inputs/4a3a90bf9100_KDmcbkhzYo5sjjxr9FqcVmWVnzb.png"

# 【方式二】本地图片路径 (代码自动转换为 Data URL)
image_source = "C:/path/input_image.png"

# 限制: 本地图片不超过 30 MB
# 另请注意请求体总大小 <= 64 MB，大文件建议改用公网 URL

# ===============================================================
# 步骤4: 配置请求参数
# ===============================================================

payload = {
    # 【model】(string, 必填) 调用的模型名称
    "model": "MiniMax-H3-Context-IR",

    # 【input】(object, 必填) 输入信息
    "input": {
        # 【content】(array[object], 必填) 多模态上下文输入数组
        # 用于描述目标视频及各类素材之间的关系
        # 每个元素通过 type 区分类型，并可通过 role 标注用途
        # 每次请求必须包含一个非空 text 项 (prompt 必填)，缺失会返回参数错误
        # 图生视频场景的输入组合:
        #   - 首帧:   text + 1 张 image_url (role=first_frame 或不填)
        #   - 尾帧:   text + 1 张 image_url (role=last_frame)
        #   - 首尾帧: text + 2 张 image_url (role 分别为 first_frame、last_frame)
        # 互斥约束: content 中出现 reference_image / reference_video / reference_audio
        #           任一 role，就不能再出现 first_frame / last_frame (反之亦然)
        # 图片输入限制:
        #   - 格式:          JPG、JPEG、PNG、WEBP、HEIC、HEIF
        #   - 单文件大小:    <= 30 MB
        #   - 宽高范围:      [256, 5760] px
        #   - 长宽比(宽/高): [0.4, 2.5]
        #   - 数量:          首帧 <= 1、尾帧 <= 1、参考图 <= 9
        # 请求体总大小限制: <= 64 MB，大文件请用公网 URL，勿用 Base64
        # 本示例传入"一个 text + 一张首帧图片"，对应图生视频-首帧场景
        "content": [
            {
                # 【type】(string, 必填) 输入内容的类型
                # 可选值: "text"(文本) / "image_url"(图片) / "video_url"(视频) / "audio_url"(音频)
                "type": "text",

                # 【text】(string, 必填) 文本提示词 (prompt)
                # 所有场景都需包含一个非空 text，描述期望生成的视频
                # 按字符数计算长度，单个 text 最多 7000 个字符
                "text": "Pull focus to the people in the background and add more steam to the ramen bowl."
            },
            {
                # 【type】(string, 必填) 输入内容的类型，图片项固定使用 "image_url"
                "type": "image_url",

                # 【image_url】(object, 条件必填) 当 type=image_url 时的图片对象
                "image_url": {
                    # 【url】(string, 必填) 图片地址，支持三种形式:
                    #   - 公网 URL
                    #   - "mm_file://{file_id}" 引用平台已有文件 (如上传或历史产物的 file_id)
                    #   - "data:image/<格式>;base64,<Base64>" data URI (<格式> 小写)
                    "url": image_source
                },

                # 【role】(string, 条件必填) 内容的位置或用途
                # 可选值:
                #   - "first_frame"(首帧图片，图生视频；仅一张图且不填 role 时默认按 first_frame 处理)
                #   - "last_frame"(尾帧图片，图生视频-首尾帧，需与 first_frame 成对)
                #   - "reference_image"(参考图片，多模态参考生视频)
                #   - "reference_video"(参考视频，多模态参考生视频)
                #   - "reference_audio"(参考音频，多模态参考生视频)
                "role": "first_frame"
            }
        ],

        # 【duration】(integer, 必填) 目标视频时长 (秒)，整数
        # 可选值: 4 / 5 / 6 / 7 / 8 / 9 / 10 / 11 / 12 / 13 / 14 / 15
        "duration": 5,

        # 【ratio】(string, 可选) 目标视频的宽高比，默认值为 "adaptive"
        # 图生视频 (content 含 first_frame / last_frame 图片) 场景下，
        # 宽高比由输入图片决定，ratio 恒为 "adaptive"；
        # 传入其他合理值不会报错，但会被忽略并按 "adaptive" 处理
        # 参数可选值: "adaptive" / "21:9" / "16:9" / "4:3" / "1:1" / "3:4" / "9:16"
        "ratio": "adaptive"
    }
}

# 媒体处理逻辑 (无需修改)

_MEDIA_RULES = {
    "rule_1": {
        "allow_url": True,
        "allow_data_uri": True,
        "allow_raw_base64": False,
        "allow_asset": False,
        "allow_local_file": True,
        "local_encoding": "data_uri",
        "file_formats": {
            ".jpg": "image/jpeg",
            ".jpeg": "image/jpeg",
            ".png": "image/png",
            ".webp": "image/webp",
            ".heic": "image/heic",
            ".heif": "image/heif",
        },
        "data_types": ["image/heic", "image/heif", "image/jpeg", "image/jpg", "image/png", "image/webp"],
    },
}


def _resolve_media(value: str, rule: dict, field: str) -> tuple:
    if not isinstance(value, str) or not value:
        raise ValueError(f"{field} 必须是非空字符串")
    if value.startswith(("http://", "https://")):
        if rule["allow_url"]:
            return value, "url"
        raise ValueError(f"{field} 不接受 URL")
    if value.startswith("data:"):
        if not rule["allow_data_uri"]:
            raise ValueError(f"{field} 不接受 Data URI")
        header, sep, encoded = value.partition(",")
        expected = {f"data:{media_type};base64" for media_type in rule["data_types"]}
        if not sep or header not in expected or not encoded:
            raise ValueError(f"{field} 的 Data URI 头无效；允许: {sorted(expected)}")
        try:
            base64.b64decode(encoded, validate=True)
        except (binascii.Error, ValueError):
            raise ValueError(f"{field} 的 Data URI 正文不是合法 Base64")
        return value, "data_uri"
    if value.lower().startswith("asset://"):
        if rule["allow_asset"] and len(value) > len("asset://"):
            return value, "asset"
        raise ValueError(f"{field} 不接受素材 ID，或素材 ID 为空")
    if os.path.isfile(value):
        if not rule["allow_local_file"]:
            raise ValueError(f"{field} 不接受本地文件")
        ext = os.path.splitext(value)[1].lower()
        if ext not in rule["file_formats"]:
            raise ValueError(f"{field} 不支持本地文件格式 {ext}；允许: {sorted(rule['file_formats'])}")
        with open(value, "rb") as f:
            encoded = base64.b64encode(f.read()).decode("ascii")
        if rule["local_encoding"] == "raw_base64":
            return encoded, "raw_base64"
        media_type = rule["file_formats"][ext]
        return f"data:{media_type};base64,{encoded}", "data_uri"
    if rule["allow_raw_base64"]:
        try:
            base64.b64decode(value, validate=True)
            return value, "raw_base64"
        except (binascii.Error, ValueError):
            pass
    raise ValueError(f"{field} 不符合接口媒体契约")


payload["input"]["content"][1]["image_url"]["url"] = _resolve_media(payload["input"]["content"][1]["image_url"]["url"], _MEDIA_RULES["rule_1"], "payload[\"input\"][\"content\"][1][\"image_url\"][\"url\"]")[0]


# ===============================================================
# 步骤5: 发送请求并输出结果
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
          "text": "436622744678867"
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

> `output[0].content[0].text` 的值即为任务 ID，用于后续查询任务状态与结果。

## 获取生成结果 示例代码

```python
"""
╔═══════════════════════════════════════════════════════════════╗
║                  DMXAPI 自研接口                               ║
╚═══════════════════════════════════════════════════════════════╝

📝 功能说明:
   本脚本演示如何使用 requests 库调用 DMXAPI 的自研接口

═══════════════════════════════════════════════════════════════
"""

import requests
import json

# ═══════════════════════════════════════════════════════════════
# 🔑 步骤1: 配置 API 连接信息
# ═══════════════════════════════════════════════════════════════

# 🌐 DMXAPI 服务端点地址
url = "https://www.dmxapi.cn/v1/responses"

# 🔐 DMXAPI 密钥 (请替换为您自己的密钥)
# 获取方式: 登录 DMXAPI 官网 -> 个人中心 -> API 密钥管理
api_key = "sk-***********************************************"

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

    "model": "MiniMax-H3-get",
    "input": "436622744678867"

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

## 返回示例

```json
{
  "task": {
    "id": "436622744678867",
    "model": "MiniMax-H3",
    "status": "succeeded",
    "created_at": 1788151136,
    "updated_at": 1788151210,
    "content": {
      "prompt": "For the target video, at 0.00 seconds into the target video, <Picture 1> (from [Shot 1]) is fully referenced.\n\nintegrated_multimodal_description: [Shot 1] This is a live-action, cinematic shot. The camera holds a perfectly static shot throughout the sequence, capturing a warm family dining scene. In the immediate foreground, resting on a polished wooden table, sits a large, ornate ceramic ramen bowl decorated with blue-and-white floral patterns. The bowl is filled with a rich broth, thick yellow noodles, two round slices of chashu pork with spiral fat patterns, a generous mound of chopped green onions, and a crisp, dark green rectangular sheet of nori seaweed tucked against the inner rim. To the left, a pair of plain wooden chopsticks rests on a small dark wooden chopstick rest, next to a cylindrical ceramic teacup. On the right side, a glowing, spherical paper lantern with a ribbed texture emits a soft yellow light onto the table. In the gently blurred background, a family of six is gathered around the extended wooden dining table in a bright room. On the left side, an adult woman with short dark hair wearing a light blue textured long-sleeve shirt sits next to a young girl in a white t-shirt, while a man in a dark navy shirt and another child are seated further down. On the right side, an adult woman in a grey shirt sits beside an on-screen adult woman on the far right, who has her dark hair tied back and wears a light grey button-down shirt (S1). Behind them, traditional Japanese shoji screens with wooden lattice frames reveal a softly blurred green outdoor landscape. Early in the shot, the foreground ramen bowl is in crisp, sharp clarity. Immediately, thick clouds of white steam begin to rise much more vigorously from the surface of the hot broth, expanding in volume and swirling upward in dense wisps that catch the ambient light. In the middle of the shot, a deliberate shift in visual clarity occurs: the foreground ramen bowl, chopsticks, and ribbed paper lantern gradually soften into a hazy blur. Simultaneously, the family members in the background come into crisp, sharp view. With the background now clearly visible, the lively, overlapping ambient chatter of the family becomes distinctly audible as their interactions become apparent. The woman in the light grey button-down shirt (S1) smiles warmly at the group. The woman in the light grey button-down shirt (S1) says, in a gentle, mid-pitched voice: <d>[Chinese] 趁热吃吧，大家。</d> Reacting to her words, the woman in the grey shirt nods enthusiastically, her mouth moving silently in agreement. On the left side, the woman in the light blue textured shirt turns her head toward the young girl beside her, flashing a tender smile, while the man in the dark navy shirt reaches forward, extending his wooden chopsticks toward a central ceramic serving dish filled with green vegetables. Throughout the later portion of the shot, the dramatically increased volume of thick white steam continues to rise from the blurred foreground bowl, creating a shifting hazy veil that partially obscures the lower center of the frame, contrasting beautifully with the sharp, joyful family gathering in the background.\n\noverall_soundscape: The soundscape begins with the subtle, continuous ambient room tone of a quiet dining room, accompanied by the faint rustling of leaves from the outdoor landscape. In the foreground, the gentle, rhythmic bubbling and soft sizzling of the hot ramen broth are clearly audible. As the thick white steam begins to rise more vigorously, a pronounced, continuous hissing and soft vaporous whooshing sound dominates the immediate foreground. When the visual clarity shifts to the background, the lively, overlapping ambient chatter of the family members becomes distinctly audible, anchoring the transition. This is followed by the sharp, clear clinking of wooden chopsticks against ceramic bowls and the dull, hollow thud of a serving dish being adjusted on the wooden table. Immediately after, the gentle, mid-pitched voice of the woman in the light grey button-down shirt rings out clearly, cutting through the ambient dining noise. The scene concludes with the sustained, comforting sounds of the family meal continuing amidst the persistent, soft hissing of the rising steam.\n\nnon_diegetic_music: A warm, acoustic guitar melody plays softly in the background, featuring gentle, finger-picked chords that evoke a sense of familial comfort and peaceful togetherness."
    },
    "duration": 5,
    "usage": {
      "total_tokens": 19870,
      "prompt_tokens": 12886,
      "completion_tokens": 6984
    },
    "ratio": "adaptive",
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
  <small>© 2026 DMXAPI MiniMax-H3-Context-IR 图生视频</small>
</p>
