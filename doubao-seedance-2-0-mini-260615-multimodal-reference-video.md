# doubao-seedance-2-0-mini-260615 多模态参考生视频 API 使用文档

doubao-seedance-2-0-mini-260615 支持多模态参考生视频：输入参考图片（0-9 张）+ 参考视频（0-3 个）+ 参考音频（0-3 个）+ 文本提示词（可选），生成 1 个融合各素材特征的视频。模型支持 480p/720p 分辨率（不支持 1080p 与 4k），视频时长范围 4~15 秒，可自动生成与画面同步的人声、音效及背景音乐。视频生成采用两步异步模式：先提交任务获取任务 ID，再通过 `seedance-2-0-get` 模型查询并获取视频结果。

## 模型名称

- `doubao-seedance-2-0-mini-260615`

## 接口地址

| 接口 | 请求方式 | URL |
|------|---------|-----|
| 提交任务 | POST | `https://www.dmxapi.cn/v1/responses` |
| 获取结果 | POST | `https://www.dmxapi.cn/v1/responses` |

:::warning
请妥善保管您的 API Key！严禁将密钥泄露给他人、硬编码到代码中或提交到公开的代码仓库。
:::

:::warning 异步任务，请妥善保存任务 ID
本模型为**异步任务**接口：提交任务后不会直接返回视频，只返回一个任务 ID（响应中的 `id` 字段），需再用查询模型 `seedance-2-0-get` 凭该 ID 换取最终视频地址。请在提交成功后立即将任务 ID 落库或写入日志妥善保存——一旦丢失将无法找回，本次生成结果也无法再取回，但费用已产生。
:::

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
api_key = "sk-******************************************"

# ===============================================================
# 步骤2: 配置请求头
# ===============================================================

headers = {
    "Content-Type": "application/json",      # 指定请求体为 JSON 格式
    "Authorization": f"{api_key}",           # token 认证方式
}

# ===============================================================
# 步骤3: 配置素材来源（每个素材选择一种即可）
# ===============================================================

# 参考图片 1（按顺序对应提示词中的 图片1）
# 【方式一】网络图片 URL（支持 HTTP / HTTPS 协议）
image1_source = "https://ark-project.tos-cn-beijing.volces.com/doc_image/r2v_tea_pic1.jpg"
# 【方式二】本地图片路径（代码自动转换为 Data URL）
# image1_source = "C:/Users/a1/Pictures/pic1.jpg"
# 【方式三】素材 ID
# image1_source = "asset://<IMAGE_ASSET_ID_1>"

# 参考图片 2（按顺序对应提示词中的 图片2）
image2_source = "https://ark-project.tos-cn-beijing.volces.com/doc_image/r2v_tea_pic2.jpg"
# image2_source = "C:/Users/a1/Pictures/pic2.jpg"
# image2_source = "asset://<IMAGE_ASSET_ID_2>"

# 参考视频 1（仅支持公网 URL 或素材 ID，不支持本地文件 Base64）
video1_source = "https://ark-project.tos-cn-beijing.volces.com/doc_video/r2v_tea_video1.mp4"
# video1_source = "asset://<VIDEO_ASSET_ID>"

# 参考音频 1（支持公网 URL、本地路径或素材 ID）
audio1_source = "https://ark-project.tos-cn-beijing.volces.com/doc_audio/r2v_tea_audio1.mp3"
# audio1_source = "C:/Users/a1/Music/reference_audio.mp3"
# audio1_source = "asset://<AUDIO_ASSET_ID>"

# ===============================================================
# 步骤4: 配置请求参数
# ===============================================================

payload = {
    # 【input】(object[], 必填) 输入内容列表
    # 输入给模型生成视频的信息，支持文本、图片、视频、音频等多种类型的元素
    # 本示例传入 1 段提示词 + 2 张参考图片 + 1 个参考视频 + 1 段参考音频
    # 支持的输入组合: 纯文本 / 文本+图片 / 文本+视频 / 文本+图片+音频 /
    #                 文本+图片+视频 / 文本+视频+音频 / 文本+图片+视频+音频
    # 注意: 不可单独输入音频，应至少包含 1 个参考图片或参考视频
    "input": [
        {
            # 【type】(string, 必填) 内容类型
            # 输入内容的类型，此处固定为 text
            "type": "text",

            # 【text】(string, 可选) 文本提示词
            # 建议中文不超过 500 字，英文不超过 1000 词
            # 额外支持西班牙语、印度尼西亚语、葡萄牙语、日语
            # 可用「图片1」「视频1」「音频1」等方式明确指定各素材的作用位置
            # 建议将对话部分置于双引号内以优化音频生成效果
            "text": (
                "全程使用视频1的第一视角构图，全程使用音频1作为背景音乐。"
                "第一人称视角果茶宣传广告；首帧为图片1，你的手摘下一颗带晨露的红苹果；"
                "2-4 秒：快速切镜，将苹果块投入雪克杯，加入冰块与茶底用力摇晃；"
                "4-6 秒：成品特写，分层果茶倒入透明杯，轻挤奶盖在顶部铺展；"
                "6-8 秒：手持举杯将果茶举到镜头前，尾帧定格为图片2。"
            )
        },
        {
            # 【image_url】(object, 必填) 图片对象
            # 输入给模型的图片对象
            "image_url": {
                # 【url】(string, 必填) 图片来源
                # 支持图片 URL、图片 Base64 编码、素材 ID 三种形式:
                #   - 图片 URL: 填入图片的公网 URL
                #   - Base64 编码: 遵循格式 data:image/<图片格式>;base64,<Base64 编码>
                #                  注意 <图片格式> 需小写，如 data:image/png;base64,{base64_image}
                #   - 素材 ID: 遵循格式 asset://<ASSET_ID>，可从素材 & 虚拟人像库获取
                # 传入单张图片要求:
                #   - 格式: jpeg、png、webp、bmp、tiff、gif，额外支持 heic、heif
                #   - 宽高比(宽/高): [0.4, 2.5]
                #   - 宽高长度(px): [300, 6000]
                #   - 大小: 单张图片小于 30 MB，请求体大小不超过 64 MB
                #           大文件请勿使用 Base64 编码
                #   - 数量: seedance 2.0 mini 多模态参考生视频 0-9 张
                "url": image1_source
            },

            # 【role】(string, 可选) 角色/用途
            # 图片的位置或用途。多模态参考生视频中，每张参考图对应的 role 均为 reference_image
            # 注意: 图生视频-首帧、图生视频-首尾帧、多模态参考生视频为 3 种互斥场景，不可混用
            "role": "reference_image",

            # 【type】(string, 必填) 内容类型
            # 输入内容的类型，此处固定为 image_url
            "type": "image_url"
        },
        {
            # 【image_url】(object, 必填) 图片对象
            # 第 2 张参考图片，来源形式与格式要求同图片 1
            "image_url": {
                # 【url】(string, 必填) 图片来源
                "url": image2_source
            },

            # 【role】(string, 可选) 角色/用途
            "role": "reference_image",

            # 【type】(string, 必填) 内容类型
            "type": "image_url"
        },
        {
            # 【role】(string, 可选) 角色/用途
            # 视频的位置或用途，此处固定为 reference_video
            "role": "reference_video",

            # 【type】(string, 必填) 内容类型
            # 输入内容的类型，此处固定为 video_url
            "type": "video_url",

            # 【video_url】(object, 必填) 视频对象
            # 输入给模型的视频对象
            "video_url": {
                # 【url】(string, 必填) 视频来源
                # 支持视频 URL、素材 ID 两种形式（不支持 Base64 编码）:
                #   - 视频 URL: 填入视频的公网 URL
                #   - 素材 ID: 遵循格式 asset://<ASSET_ID>，可从素材 & 虚拟人像库获取
                # 传入单个视频要求:
                #   - 视频格式: mp4、mov
                #   - 时长: 单个视频 [2, 15] s，最多传入 3 个参考视频，所有视频总时长不超过 15 s
                #   - 宽高比(宽/高): [0.4, 2.5]
                #   - 宽高长度(px): [300, 6000]
                #   - 总像素数: [407696, 8295044]，即宽和高的乘积需落在该区间
                #   - 帧率(FPS): [24, 60]
                #   - 大小: 单个视频不超过 200 MB
                "url": video1_source
            }
        },
        {
            # 【audio_url】(object, 必填) 音频对象
            # 输入给模型的音频对象
            "audio_url": {
                # 【url】(string, 必填) 音频来源
                # 支持音频 URL、音频 Base64 编码、素材 ID 三种形式
                # 传入音频要求: 最多传入 3 段
                "url": audio1_source
            },

            # 【role】(string, 可选) 角色/用途
            # 音频的位置或用途，此处固定为 reference_audio
            "role": "reference_audio",

            # 【type】(string, 必填) 内容类型
            # 输入内容的类型，此处固定为 audio_url
            "type": "audio_url"
        }
    ],

    # 【callback_url】(string, 可选) 回调地址
    # 任务状态发生变化时，平台会向该地址推送 POST 请求，请求体结构与查询任务接口返回体一致
    # 回调状态: queued(排队中) / running(运行中) / succeeded(成功) / failed(失败) / expired(超时)
    "callback_url": "https://www.dmxapi.cn",

    # 【duration】(integer, 可选) 视频时长
    # 生成视频时长（单位：秒）
    # 取值范围: [4, 15]；或设置为 -1（智能选择，模型在有效取值范围内自主选择合适时长）
    # 传 -1 时按 15 秒预扣费，实际时长确定后多退少补
    # 注意: 视频时长与计费相关，请谨慎设置
    "duration": 8,

    # 【execution_expires_after】(integer, 可选) 任务超时阈值
    # 指定任务提交后的过期时间（单位：秒），从 created_at 时间戳开始计算，默认值 172800（48 小时）
    # 超过该时间后任务会被自动终止，并标记为 expired 状态
    # 取值范围: [3600, 259200]
    "execution_expires_after": 172800,

    # 【generate_audio】(boolean, 可选) 生成有声视频
    # 控制生成的视频是否包含与画面同步的声音，默认值 true
    # 可选值:
    #   - True(模型输出的视频包含同步音频，会基于文本提示词与视觉内容自动生成
    #          匹配的人声、音效及背景音乐)
    #   - False(模型输出的视频为无声视频)
    # 建议将对话部分置于双引号内以优化音频生成效果
    # 注意: 生成的有声视频均为单声道，与传入音频的声道数无关
    "generate_audio": True,

    # 【model】(string, 必填) 调用的模型名称
    "model": "doubao-seedance-2-0-mini-260615",

    # 【ratio】(string, 可选) 视频宽高比
    # 生成视频的宽高比例，默认值 adaptive
    # 可选值: "16:9" / "4:3" / "1:1" / "3:4" / "9:16" / "21:9"
    #         "adaptive"(由模型根据提示词在可选宽高比中自动选择)
    "ratio": "16:9",

    # 【resolution】(string, 可选) 视频分辨率
    # 视频分辨率，默认值 720p
    # 可选值: "480p" / "720p"（seedance 2.0 mini 不支持 1080p 和 4k）
    # 各宽高比对应的宽高像素值:
    #   - 480p: 16:9 854×480、4:3 752×560、1:1 640×640、3:4 560×752、9:16 480×854、21:9 992×432
    #   - 720p: 16:9 1280×720、4:3 1112×834、1:1 960×960、3:4 834×1112、9:16 720×1280、21:9 1470×630
    "resolution": "720p",

    # 【return_last_frame】(boolean, 可选) 返回尾帧
    # 是否返回生成视频的尾帧图像，默认值 false
    # 可选值:
    #   - True(返回尾帧图像，可通过查询视频生成任务接口获取；尾帧图像格式为 png，
    #          宽高像素值与生成的视频保持一致，无水印)
    #   - False(不返回尾帧图像)
    # 使用该参数可实现生成多个连续视频：以上一个生成视频的尾帧作为下一个视频任务的首帧
    "return_last_frame": False,

    # 【seed】(integer, 可选) 随机种子
    # 控制生成内容的随机性，默认值 -1
    # 取值范围: [-1, 2147483647]；-1 表示使用随机数
    # 相同请求下，相同 seed 会生成类似结果，但不保证完全一致
    "seed": -1,

    # 【tools】(object[], 可选) 工具配置
    # web_search: 联网搜索工具，模型根据提示词自主判断是否搜索互联网内容
    # 开启后可提升视频内容时效性，但会增加一定时延
    "tools": [{"type": "web_search"}],

    # 【watermark】(boolean, 可选) 视频水印
    # 生成视频是否包含水印，默认值 false
    # 可选值:
    #   - True(生成视频右下角会展示「AI 生成」水印)
    #   - False(生成视频不含水印)
    "watermark": False
}

# 媒体处理逻辑（无需修改）

_MEDIA_RULES = {
    "image": {
        "allow_url": True,
        "allow_data_uri": True,
        "allow_raw_base64": False,
        "allow_asset": True,
        "allow_local_file": True,
        "local_encoding": "data_uri",
        "file_formats": {
            ".jpg": "image/jpeg",
            ".jpeg": "image/jpeg",
            ".png": "image/png",
            ".bmp": "image/bmp",
            ".webp": "image/webp",
            ".tif": "image/tiff",
            ".tiff": "image/tiff",
            ".gif": "image/gif",
            ".heic": "image/heic",
            ".heif": "image/heif",
        },
        "data_types": ["image/bmp", "image/gif", "image/heic", "image/heif", "image/jpeg", "image/png", "image/tiff", "image/webp"],
    },
    "video": {
        # 视频仅支持公网 URL 或素材 ID，不支持本地文件转 Base64
        "allow_url": True,
        "allow_data_uri": False,
        "allow_raw_base64": False,
        "allow_asset": True,
        "allow_local_file": False,
        "local_encoding": None,
        "file_formats": {},
        "data_types": [],
    },
    "audio": {
        "allow_url": True,
        "allow_data_uri": True,
        "allow_raw_base64": False,
        "allow_asset": True,
        "allow_local_file": True,
        "local_encoding": "data_uri",
        "file_formats": {
            ".mp3": "audio/mpeg",
            ".wav": "audio/wav",
        },
        "data_types": ["audio/mpeg", "audio/wav"],
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
            raise ValueError(f"{field} 不接受本地文件，请先上传至素材库或对象存储获取 URL")
        ext = os.path.splitext(value)[1].lower()
        if ext not in rule["file_formats"]:
            raise ValueError(f"{field} 不支持本地文件格式 {ext}")
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

payload["input"][1]["image_url"]["url"] = _resolve_media(payload["input"][1]["image_url"]["url"], _MEDIA_RULES["image"], "参考图片1")[0]
payload["input"][2]["image_url"]["url"] = _resolve_media(payload["input"][2]["image_url"]["url"], _MEDIA_RULES["image"], "参考图片2")[0]
payload["input"][3]["video_url"]["url"] = _resolve_media(payload["input"][3]["video_url"]["url"], _MEDIA_RULES["video"], "参考视频1")[0]
payload["input"][4]["audio_url"]["url"] = _resolve_media(payload["input"][4]["audio_url"]["url"], _MEDIA_RULES["audio"], "参考音频1")[0]

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
  "id": "cgt-20260820142845-tq8dz",
  "usage": {
    "total_tokens": 43120,
    "input_tokens": 0,
    "input_tokens_details": {
      "cached_tokens": 0
    },
    "output_tokens": 43120,
    "output_tokens_details": {
      "reasoning_tokens": 0
    }
  }
}
```

> 返回的 `id` 字段即为任务 ID，用于第二步查询视频生成结果。

## 获取结果 示例代码

```python
import requests
import json

url = "https://www.dmxapi.cn/v1/responses"

# DMXAPI 密钥 (请替换为您自己的密钥)
api_key = "sk-******************************************"

headers = {
    "Content-Type": "application/json",
    # 获取结果接口使用 Bearer 认证方式
    "Authorization": f"Bearer {api_key}",
}

payload = {
    # 【model】(string, 必填) 查询模型，固定为 seedance-2-0-get
    "model": "seedance-2-0-get",

    # 【input】(string, 必填) 第一步提交任务返回的任务 ID
    "input": "cgt-20260820142845-tq8dz"
}

response = requests.post(url, headers=headers, json=payload)
result = response.json()

# 用量与计费：output_tokens 即本次实际扣费依据
print("用量:")
print(json.dumps(result.get("usage", {}), indent=2, ensure_ascii=False))

# 解析任务详情与视频链接
try:
    text = result["output"][0]["content"][0]["text"]
    inner = json.loads(text)

    # 格式化打印任务详情：含实际生成参数（时长/分辨率/宽高比/随机种子/帧率等）
    # text 本身是被转义的 JSON 字符串，直接打印会挤成一行，需先 json.loads 再格式化
    print("\n任务详情:")
    print(json.dumps(inner, indent=2, ensure_ascii=False))

    video_url = inner["content"]["video_url"]
    print(f"\n视频链接: {video_url}")
    last_frame_url = inner["content"].get("last_frame_url")
    if last_frame_url:
        print(f"尾帧图像: {last_frame_url}")
except Exception as e:
    print(f"提取 URL 失败: {e}")
```

## 返回示例

```json
{
  "request_id": "cgt-20260820142845-tq8dz",
  "output": [
    {
      "type": "message",
      "content": [
        {
          "type": "output_text",
          "text": "{\"content\":{\"video_url\":\"https://ark-acg-cn-beijing.tos-cn-beijing.volces.com/doubao-seedance-2-0-mini/02178747125300000000000000000000000ffffac1945e6f19d3.mp4?X-Tos-Algorithm=TOS4-HMAC-SHA256\\u0026X-Tos-Credential=YOUR_ACCESS_KEY_ID%2F20260820%2Fcn-beijing%2Ftos%2Frequest\\u0026X-Tos-Date=20260820T062845Z\\u0026X-Tos-Expires=86400\\u0026X-Tos-Signature=d4e5f60718293a4b5c6d7e8f90a1b2c3d4e5f60718293a4b5c6d7e8f90a1b2c3\\u0026X-Tos-SignedHeaders=host\"},\"id\":\"cgt-20260820142845-tq8dz\",\"model\":\"doubao-seedance-2-0-mini-260615\",\"status\":\"succeeded\"}"
        }
      ]
    }
  ],
  "usage": {
    "total_tokens": 43120,
    "input_tokens": 0,
    "input_tokens_details": {
      "cached_tokens": 0
    },
    "output_tokens": 43120,
    "output_tokens_details": {
      "reasoning_tokens": 0
    }
  }
}

视频链接: https://ark-acg-cn-beijing.tos-cn-beijing.volces.com/doubao-seedance-2-0-mini/02178747125300000000000000000000000ffffac1945e6f19d3.mp4?X-Tos-Algorithm=TOS4-HMAC-SHA256&X-Tos-Credential=YOUR_ACCESS_KEY_ID%2F20260820%2Fcn-beijing%2Ftos%2Frequest&X-Tos-Date=20260820T062845Z&X-Tos-Expires=86400&X-Tos-Signature=d4e5f60718293a4b5c6d7e8f90a1b2c3d4e5f60718293a4b5c6d7e8f90a1b2c3&X-Tos-SignedHeaders=host
```

<p align="center">
  <small>© 2026 DMXAPI doubao-seedance-2-0-mini-260615 多模态参考生视频</small>
</p>
