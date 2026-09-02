# MiniMax-H3-Context-IR 多模态参考生视频 API 使用文档

基于 MiniMax H3-Context-IR 的多模态参考生视频提示词增强接口，通过 `/v1/responses` 端点以异步任务方式调用。接口对文本、图像、音频与视频等多模态上下文进行深度理解，分析素材之间以及素材与目标生成结果之间的关系并进行复杂逻辑推理，将其转换为结构化、语义更丰富的视频提示词；请注意本接口只返回增强后的视频提示词，不会创建视频生成任务，任务成功后从 `content.prompt` 读取结果。多模态参考场景由一个 `text` 元素搭配 `reference_image`、`reference_video`、`reference_audio` 三类参考素材自由组合，参考图最多 9 张、参考视频与参考音频各最多 3 个且单段时长均在 [2, 15] 秒、总时长不超过 15 秒，目标时长支持 4~15 秒的整数取值，宽高比默认 `adaptive` 亦可显式指定为 21:9、16:9、4:3、1:1、3:4、9:16，适合做角色一致性保持、音色迁移与画面风格参考等复杂改写。

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

## 多模态参考生视频 示例代码

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
# 步骤3: 配置视频来源 (选择一种即可)
# ===============================================================

# 参数位置: payload["input"]["content"][1]["video_url"]["url"]

# 【方式一】网络视频 URL (支持 HTTP / HTTPS 协议)
# video_source = "https://cdn.hailuoai.com/prod/hailuo_demo/testsets/h3_promo_eval_ref2va/gallery/sr_v2p26_trio_seed42_20260724/inputs/297573323635_00_%E8%A7%86%E9%A2%911_YnyRbxEwio_video_20260525_163755_1927e9d3.mp4"

# 【方式二】本地视频路径 (代码自动转换为 Data URL)
video_source = "C:/path/input_video.mp4"

# 限制: 本示例代码仅接受 MP4 容器的本地视频，单文件不超过 50 MB、单段时长 [2, 15] 秒
# 另请注意请求体总大小 <= 64 MB 且 Base64 会放大约 33%，大视频请改用公网 URL

# ===============================================================
# 步骤4: 配置音频来源 (选择一种即可)
# ===============================================================

# 参数位置: payload["input"]["content"][2]["audio_url"]["url"]

# 【方式一】网络音频 URL (支持 HTTP / HTTPS 协议)
# audio_source = "https://cdn.hailuoai.com/prod/hailuo_demo/testsets/h3_promo_eval_ref2va/gallery/sr_v2p26_trio_seed42_20260724/inputs/f463d523c5ce_01_%E9%9F%B3%E9%A2%911_RSLcbpzJPo_6%E6%9C%885%E6%97%A5(1).mp3"

# 【方式二】本地音频路径 (代码自动转换为 Data URL)
audio_source = "C:/path/input_audio.mp3"

# 限制: 本地音频单文件不超过 15 MB、单段时长 [2, 15] 秒

# ===============================================================
# 步骤5: 配置请求参数
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
        # 多模态参考生视频场景的输入组合:
        #   text + 参考图片(role=reference_image) + 参考视频(role=reference_video)
        #        + 参考音频(role=reference_audio) 的组合
        # 互斥约束: content 中出现 reference_image / reference_video / reference_audio
        #           任一 role，就不能再出现 first_frame / last_frame (反之亦然)
        # 图片输入限制:
        #   - 格式:          JPG、JPEG、PNG、WEBP、HEIC、HEIF
        #   - 单文件大小:    <= 30 MB
        #   - 宽高范围:      [256, 5760] px
        #   - 长宽比(宽/高): [0.4, 2.5]
        #   - 数量:          参考图 <= 9
        # 视频输入限制 (仅多模态参考场景):
        #   - 容器 / 格式:   MP4(.mp4)、MOV(.mov)
        #   - 编码:          视频 H.264/AVC、H.265/HEVC；音频 AAC、MP3
        #   - 单文件大小:    <= 50 MB
        #   - 个数:          <= 3
        #   - 单段时长:      [2, 15] s；总时长 <= 15 s
        #   - 宽高范围:      [256, 5760] px
        #   - 长宽比(宽/高): [0.4, 2.5]
        #   - 帧率:          [23.976, 60]
        # 音频输入限制 (仅多模态参考场景):
        #   - 格式:       WAV、MP3
        #   - 单文件大小: <= 15 MB
        #   - 个数:       <= 3
        #   - 单段时长:   [2, 15] s；总时长 <= 15 s
        # 请求体总大小限制: <= 64 MB，大文件请用公网 URL，勿用 Base64
        # 本示例传入"一个 text + 一个参考视频 + 一个参考音频"
        "content": [
            {
                # 【type】(string, 必填) 输入内容的类型
                # 可选值: "text"(文本) / "image_url"(图片) / "video_url"(视频) / "audio_url"(音频)
                "type": "text",

                # 【text】(string, 必填) 文本提示词 (prompt)
                # 所有场景都需包含一个非空 text，描述期望生成的视频
                # 按字符数计算长度，单个 text 最多 7000 个字符
                "text": "角色说话：Follow the wind, live free.Leave worries behind, enjoy the moment，音色参考音频1"
            },
            {
                # 【type】(string, 必填) 输入内容的类型，视频项固定使用 "video_url"
                "type": "video_url",

                # 【video_url】(object, 条件必填) 当 type=video_url 时的视频对象
                # 参考视频，仅多模态参考场景可用
                "video_url": {
                    # 【url】(string, 必填) 视频地址，支持三种形式:
                    #   - 公网 URL
                    #   - "mm_file://{file_id}" 引用平台已有文件的 file_id
                    #   - "data:video/mp4;base64,<Base64>" data URI
                    "url": video_source
                },

                # 【role】(string, 条件必填) 内容的位置或用途
                # 可选值:
                #   - "first_frame"(首帧图片，图生视频；仅一张图且不填 role 时默认按 first_frame 处理)
                #   - "last_frame"(尾帧图片，图生视频-首尾帧，需与 first_frame 成对)
                #   - "reference_image"(参考图片，多模态参考生视频)
                #   - "reference_video"(参考视频，多模态参考生视频)
                #   - "reference_audio"(参考音频，多模态参考生视频)
                "role": "reference_video"
            },
            {
                # 【type】(string, 必填) 输入内容的类型，音频项固定使用 "audio_url"
                "type": "audio_url",

                # 【audio_url】(object, 条件必填) 当 type=audio_url 时的音频对象
                # 参考音频，仅多模态参考场景可用
                "audio_url": {
                    # 【url】(string, 必填) 音频地址，支持三种形式:
                    #   - 公网 URL
                    #   - "mm_file://{file_id}" 引用平台已有文件的 file_id
                    #   - "data:audio/<格式>;base64,<Base64>" data URI (<格式> 小写)
                    "url": audio_source
                },

                # 【role】(string, 条件必填) 内容的位置或用途，本项作为参考音频
                "role": "reference_audio"
            }
        ],

        # 【duration】(integer, 必填) 目标视频时长 (秒)，整数
        # 可选值: 4 / 5 / 6 / 7 / 8 / 9 / 10 / 11 / 12 / 13 / 14 / 15
        "duration": 5,

        # 【ratio】(string, 可选) 目标视频的宽高比，默认值为 "adaptive"
        # 多模态参考生视频 (content 含 reference_image / reference_video / reference_audio)
        # 场景下 ratio 可选，默认 "adaptive"，也可显式指定任一具体比例
        # 可选值:
        #   - "adaptive"(自适应，默认值)
        #   - "21:9"(超宽银幕)
        #   - "16:9"(横屏宽银幕)
        #   - "4:3"(横屏标准)
        #   - "1:1"(正方形)
        #   - "3:4"(竖屏标准)
        #   - "9:16"(竖屏全屏)
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
            ".mp4": "video/mp4",
        },
        "data_types": ["video/mp4"],
    },
    "rule_2": {
        "allow_url": True,
        "allow_data_uri": True,
        "allow_raw_base64": False,
        "allow_asset": False,
        "allow_local_file": True,
        "local_encoding": "data_uri",
        "file_formats": {
            ".mp3": "audio/mp3",
            ".wav": "audio/wav",
        },
        "data_types": ["audio/mp3", "audio/wav"],
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


payload["input"]["content"][1]["video_url"]["url"] = _resolve_media(payload["input"]["content"][1]["video_url"]["url"], _MEDIA_RULES["rule_1"], "payload[\"input\"][\"content\"][1][\"video_url\"][\"url\"]")[0]
payload["input"]["content"][2]["audio_url"]["url"] = _resolve_media(payload["input"]["content"][2]["audio_url"]["url"], _MEDIA_RULES["rule_2"], "payload[\"input\"][\"content\"][2][\"audio_url\"][\"url\"]")[0]


# ===============================================================
# 步骤6: 发送请求并输出结果
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
          "text": "436631041642788"
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
    "input": "436631041642788"

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
    "id": "436631041642788",
    "model": "MiniMax-H3",
    "status": "succeeded",
    "created_at": 1788153256,
    "updated_at": 1788153363,
    "content": {
      "prompt": "subject_definitions:\n<Subject 1> is the young man in <Video 1>, who has wavy blond hair and wears a bright pink suit jacket over a loosely unbuttoned white collared shirt, accessorized with rings on his right hand, a silver watch on his left wrist, and small earrings. He is holding a small black lamb securely against his chest in a vibrant green grassy field, with several white lambs grazing on the gently sloping hillside in the background.\n<Audio 2> is the voice timbre reference for <Subject 1>'s spoken dialogue, containing a resonant male voice.\n\nsummary:\n[reference generation + audio reference] The target video features <Subject 1> standing in a green grassy field holding a black lamb. He speaks a peaceful message to the camera, with his voice timbre and delivery guided by <Audio 2>.\n\nretention_analysis:\n<Subject 1> (appears in [Shot 1]): fully_preserved - the target video fully preserves the young man's wavy blond hair, bright pink suit jacket, unbuttoned white shirt, rings, silver watch, and earrings, as well as the small black lamb he holds and the green grassy field with white lambs in the background.\n<Audio 2>: reference - <Audio 2> serves as the voice timbre and delivery reference for the young man's spoken dialogue, transferring its resonant male vocal qualities without reusing its source lexical content.\n\ndetailed_description:\nThe target video is in a realistic, cinematic photographic style with warm golden-hour lighting.\n[Shot 1] The shot opens with a low-angle medium shot of <Subject 1>, the young man with wavy blond hair wearing a bright pink suit jacket and a loosely unbuttoned white collared shirt, accessorized with small earrings. He stands firmly planted in a lush, vibrant green grassy field that slopes gently upward behind him. Nestled securely against his chest is a small black lamb, its dark curly fleece contrasting sharply with the smooth, crisp fabric of the man's pink jacket and white shirt. His right hand, adorned with rings, supports the lamb, while a silver watch is visible on his left wrist. In the slightly out-of-focus background, several white lambs with fluffy coats are scattered across the hillside, peacefully grazing on the thick grass. The warm, directional sunlight from the left bathes the scene, casting soft, defining shadows across the man's jawline and highlighting the golden strands of his hair, while illuminating the vibrant green of the pasture. The gentle, continuous ambient sound of a breeze sweeping through the open countryside establishes a tranquil atmosphere before any words are spoken.\nThe young man (S1), with a resonant, calm male voice delivered at a steady, relaxed, and reassuring pace, looks directly forward with a serene, confident expression and speaks, <d>[English] Follow the wind, live free.</d> As he delivers the first sentence, his posture remains stable and grounded, anchoring the composition. During a brief, natural pause in his speech, he gently moves his right hand over the back of the small black lamb, his fingers softly stroking its dark fleece to soothe the animal. The black lamb rests comfortably in his embrace, its head held still. The young man (S1) maintains his gentle demeanor and continues speaking smoothly, <d>[English] Leave worries behind, enjoy the moment.</d> Immediately upon finishing the final word, his lips meet and close into a relaxed, satisfied smile. He slowly shifts his gaze away from the direct view, turning his head slightly toward the distant horizon on the right. As he turns, the warm sunlight catches the side of his face, emphasizing his peaceful expression. His right hand continues to rest supportively on the black lamb, holding it close to his body. A gentle gust of wind sweeps across the hillside, lightly rustling his wavy blond hair and causing the unbuttoned edges of his white shirt to flutter subtly against his pink jacket. In the background, the white lambs continue their quiet grazing, undisturbed by the subtle motion. The continuous natural ambience of the rustling grass and the open breeze remains audible, carrying the tranquil rural scene through to the end of the shot.\n\noverall_soundscape:\nThe target video features a tranquil outdoor soundscape with the continuous natural ambience of a gentle breeze rustling through the open grassy field, supporting the clear, resonant male spoken dialogue.\n\nnon_diegetic_music:\nN/A"
    },
    "duration": 5,
    "usage": {
      "total_tokens": 42629,
      "prompt_tokens": 33345,
      "completion_tokens": 9284
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
  <small>© 2026 DMXAPI MiniMax-H3-Context-IR 多模态参考生视频</small>
</p>
