# doubao-seedance-2-5-260628 视频延长 API 使用文档

基于 Doubao Seedance 2.5 的视频延长接口，通过 `/v1/responses` 端点以异步任务方式调用：传入一个或多个参考视频（`role` 均设为 `reference_video`），由模型沿原片向前或向后续接新的镜头内容。提示词中可用「@视频1」「@视频2」等标记指定各素材的衔接顺序与转场意图，本示例即以三段素材串联出「窗户打开 → 进入美术馆 → 镜头入画」的连续叙事。将 `omni_reference_task_type` 显式设为 `extend` 可在提交时提前校验该任务的专属限制——输入中必须至少包含一个 `reference_video`、`ratio` 必须为 `adaptive`，输出视频宽高比自动与待延长视频保持一致。单次最多可传入 10 个参考视频、总时长不超过 30 秒，适合长片续写、镜头补拍与连续分镜拼接等场景。

## 接口地址

| 接口 | 请求方式 | URL |
|------|---------|-----|
| 提交任务 | POST | `https://www.dmxapi.cn/v1/responses` |
| 获取结果 | POST | `https://www.dmxapi.cn/v1/responses` |



:::warning
请妥善保管您的 API Key！严禁将密钥泄露给他人、硬编码到代码中或提交到公开的代码仓库。如果怀疑密钥已泄露，请立即前往 DMXAPI 官网重新生成。
:::

:::warning 异步任务，请妥善保存任务 ID
本模型为**异步任务**接口：提交任务后不会直接返回视频，只返回一个任务 ID（响应中的 `id` 字段），需再用查询模型 `seedance-2-5-get` 凭该 ID 换取最终视频地址。请在提交成功后立即将任务 ID 落库或写入日志妥善保存——一旦丢失将无法找回，本次生成结果也无法再取回，但费用已产生。
:::

## 模型名称

- `doubao-seedance-2-5-260628`

## 视频延长 示例代码

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
# 步骤3: 配置视频来源（每个位置选择一种即可）
# ===============================================================

# 参数位置: payload["input"][1]["video_url"]["url"]
# 【方式一】网络视频 URL（支持 HTTP / HTTPS 协议）
video_source_2 = "https://arkdocs.tos-cn-beijing.volces.com/videos/video-generation/r2v_extend_video1_75.mov"
# 【方式二】素材 ID
# video_source_2 = "asset://<ASSET_ID>"

# 参数位置: payload["input"][2]["video_url"]["url"]
# 【方式一】网络视频 URL（支持 HTTP / HTTPS 协议）
video_source_3 = "https://ark-project.tos-cn-beijing.volces.com/doc_video/r2v_extend_video2.mp4"
# 【方式二】素材 ID
# video_source_3 = "asset://<ASSET_ID>"

# 参数位置: payload["input"][3]["video_url"]["url"]
# 【方式一】网络视频 URL（支持 HTTP / HTTPS 协议）
video_source = "https://ark-project.tos-cn-beijing.volces.com/doc_video/r2v_extend_video3.mp4"
# 【方式二】素材 ID
# video_source = "asset://<ASSET_ID>"

# ===============================================================
# 步骤4: 配置请求参数
# ===============================================================

payload = {
    # 【input】(object[], 必填) 输入内容列表
    # 输入给模型生成视频的信息，本示例传入 1 段延长指令文本 + 3 个参考视频
    "input": [
        {
            # 【text】(string, 必填) 文本提示词
            # 输入给模型的文本提示词，描述期望生成的视频
            # 语言支持: 中英文，额外支持西班牙语、印度尼西亚语、葡萄牙语、日语、马来语、
            #           泰语、阿拉伯语、越南语、韩语
            # 字数建议: 中文提示词不超过 500 字，英文提示词不超过 1000 词
            #           字数过多易导致信息分散，模型可能忽略细节、仅关注重点，
            #           进而造成视频缺失部分元素
            "text": "延长@视频1，窗户打开后进入@视频2的美术馆室内，最后镜头进入@视频3的画内",

            # 【type】(string, 必填) 内容类型
            # 输入内容的类型，此处固定为 text
            "type": "text"
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
                # 支持视频 URL、素材 ID 两种形式:
                #   - 视频 URL: 填入视频的公网 URL
                #   - 素材 ID: 遵循格式 asset://<ASSET_ID>，可从素材 & 虚拟人像库获取
                # 传入单个视频要求:
                #   - 视频格式: mp4、mov
                #               MP4 支持视频编码 H.264/AVC、H.265/HEVC，音频编码 AAC、MP3
                #               MOV 支持视频编码 H.264/AVC、H.265/HEVC，音频编码 AAC、MP3、PCM
                #   - 分辨率: 480p、720p、1080p、4k
                #   - 时长: 非视频编辑任务单个视频 [2, 30] s；视频编辑任务单个视频 [4, 30] s
                #           最多传入 10 个参考视频，所有视频总时长不超过 30 s
                #   - 宽高比(宽/高): [0.4, 2.5]
                #   - 宽高长度(px): [300, 6000]
                #   - 总像素数: [407696, 8295044]，即宽和高的乘积需落在该区间
                #   - 大小: 单个视频不超过 200 MB
                #   - 帧率(FPS): [24, 60]
                "url": video_source_2
            }
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
                # 支持视频 URL、素材 ID 两种形式:
                #   - 视频 URL: 填入视频的公网 URL
                #   - 素材 ID: 遵循格式 asset://<ASSET_ID>，可从素材 & 虚拟人像库获取
                # 传入单个视频要求:
                #   - 视频格式: mp4、mov
                #               MP4 支持视频编码 H.264/AVC、H.265/HEVC，音频编码 AAC、MP3
                #               MOV 支持视频编码 H.264/AVC、H.265/HEVC，音频编码 AAC、MP3、PCM
                #   - 分辨率: 480p、720p、1080p、4k
                #   - 时长: 非视频编辑任务单个视频 [2, 30] s；视频编辑任务单个视频 [4, 30] s
                #           最多传入 10 个参考视频，所有视频总时长不超过 30 s
                #   - 宽高比(宽/高): [0.4, 2.5]
                #   - 宽高长度(px): [300, 6000]
                #   - 总像素数: [407696, 8295044]，即宽和高的乘积需落在该区间
                #   - 大小: 单个视频不超过 200 MB
                #   - 帧率(FPS): [24, 60]
                "url": video_source_3
            }
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
                # 支持视频 URL、素材 ID 两种形式:
                #   - 视频 URL: 填入视频的公网 URL
                #   - 素材 ID: 遵循格式 asset://<ASSET_ID>，可从素材 & 虚拟人像库获取
                # 传入单个视频要求:
                #   - 视频格式: mp4、mov
                #               MP4 支持视频编码 H.264/AVC、H.265/HEVC，音频编码 AAC、MP3
                #               MOV 支持视频编码 H.264/AVC、H.265/HEVC，音频编码 AAC、MP3、PCM
                #   - 分辨率: 480p、720p、1080p、4k
                #   - 时长: 非视频编辑任务单个视频 [2, 30] s；视频编辑任务单个视频 [4, 30] s
                #           最多传入 10 个参考视频，所有视频总时长不超过 30 s
                #   - 宽高比(宽/高): [0.4, 2.5]
                #   - 宽高长度(px): [300, 6000]
                #   - 总像素数: [407696, 8295044]，即宽和高的乘积需落在该区间
                #   - 大小: 单个视频不超过 200 MB
                #   - 帧率(FPS): [24, 60]
                "url": video_source
            }
        }
    ],

    # 【duration】(integer, 可选) 视频时长
    # 生成视频时长（单位：秒），默认值 -1
    # 取值范围: [4, 30]；或设置为 -1（智能选择，模型在有效取值范围内自主选择合适的整数秒时长）
    # 说明: 查询任务接口返回的 duration = 实际总帧数 / 24（向下取整），为整数秒约数
    "duration": 4,

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
    # 注意: 生成的有声视频均为单声道，和传入的音频声道数无关
    "generate_audio": True,

    # 【model】(string, 必填) 调用的模型名称
    "model": "doubao-seedance-2-5-260628",

    # 【omni_reference_task_type】(string, 可选) 任务类型引导
    # 全模态参考生视频任务包括参考生视频、视频编辑和视频延长 3 类子任务，不同任务类型对参数
    # 有特殊限制，可通过本参数指定子任务类型，以提前校验对应限制。默认值 auto
    # 可选值:
    #   - "auto"(由模型根据输入素材和提示词自动判定任务类型，再校验参数取值；如果参数与实际
    #            任务类型不兼容，任务将触发异步报错，错误码 InvalidParameter.TaskTypeConstraint)
    #   - "reference"(参考生视频任务，即基于参考图片、参考视频或参考音频生成新视频；
    #                 设置 reference 时，ratio 或 duration 无特殊限制)
    #   - "edit"(视频编辑任务，即对原视频的画面或音频进行编辑操作；设置 edit 时，输入内容中
    #            必须至少包含一个 reference_video，且视频时长必须为 4-30 秒；
    #            ratio 必须为 adaptive；duration 必须为 -1)
    #   - "extend"(视频延长任务，即对原视频向前或向后延长；设置 extend 时，输入内容中必须
    #              至少包含一个 reference_video；ratio 必须为 adaptive)
    # 说明: 显式指定任务类型时，接口在提交任务时提前校验对应限制，不符合要求会立即报错，任务不会创建
    # 注意: 实际处理任务时，模型仍会进一步结合提示词判断任务类型。若实际判定的任务类型和指定的
    #       不一致，仍会触发异步报错（错误码 InvalidParameter.TaskTypeMismatch）
    "omni_reference_task_type": "extend",

    # 【output_format】(string, 可选) 输出格式
    # 输出视频的格式，默认值 mp4
    # 可选值:
    #   - "mp4"(通用格式，兼容性最好，采用标准色彩精度，可在网页、移动端、各类播放器
    #           及分发平台直接播放)
    #   - "mov"(面向专业场景的高色彩精度格式，更好地保持画面色彩与亮度一致性，适用于调色、
    #           抠像、合成等对色彩还原要求高的专业后期加工；推荐在视频编辑、视频延长场景
    #           使用 mov 格式作为输入和输出)
    # 注意: mov 格式采用 H.264 视频编码 + yuv444p 色度采样 + PCM 音频编码，部分播放器可能
    #       不兼容，常见支持的播放器有 IINA(仅 macOS)、VLC、mpv、ffplay
    "output_format": "mp4",

    # 【ratio】(string, 可选) 视频宽高比
    # 生成视频的宽高比例，默认值 adaptive
    # 可选值: "16:9" / "4:3" / "1:1" / "3:4" / "9:16" / "21:9"
    #         "adaptive"(根据任务类型和输入内容自动适配宽高比)
    # 注意: 视频延长任务仅支持配置为 adaptive，不支持指定具体宽高比
    "ratio": "adaptive",

    # 【resolution】(string, 可选) 视频分辨率
    # 视频分辨率，默认值 720p
    # 可选值: "480p" / "720p" / "1080p"
    # 各宽高比对应的宽高像素值:
    #   - 480p : 16:9 854×480、4:3 752×560、1:1 640×640、3:4 560×752、9:16 480×854、21:9 992×432
    #   - 720p : 16:9 1280×720、4:3 1112×834、1:1 960×960、3:4 834×1112、9:16 720×1280、21:9 1470×630
    #   - 1080p: 16:9 1920×1080、4:3 1664×1248、1:1 1440×1440、3:4 1248×1664、9:16 1080×1920、21:9 2206×946
    # 注意: 1080p 视频采用 10bit 位深与 H.265/HEVC 编码，能保留更丰富的色彩层次与更平滑的渐变
    #       过渡；H.265/HEVC 在少数播放环境中可能不兼容，可使用 VLC、MPV、QuickTime Player 播放
    "resolution": "720p",

    # 【return_last_frame】(boolean, 可选) 返回尾帧
    # 是否返回生成视频的尾帧图像，默认值 false
    # 可选值:
    #   - True(返回尾帧图像，可通过查询视频生成任务接口获取；尾帧图像格式为 png，
    #          宽高像素值与生成的视频保持一致，无水印)
    #   - False(不返回尾帧图像)
    # 使用该参数可实现生成多个连续视频：以上一个生成视频的尾帧作为下一个视频任务的首帧
    "return_last_frame": False,

    # 【watermark】(boolean, 可选) 视频水印
    # 生成视频是否包含水印，默认值 false
    # 可选值:
    #   - True(生成视频右下角会展示「AI 生成」水印)
    #   - False(生成视频不含水印)
    "watermark": False
}

# 媒体处理逻辑（无需修改）

_MEDIA_RULES = {
    "rule_1": {
        "allow_url": True,
        "allow_data_uri": False,
        "allow_raw_base64": False,
        "allow_asset": True,
        "allow_local_file": False,
        "local_encoding": "",
        "file_formats": {
        },
        "data_types": [],
    },
    "rule_2": {
        "allow_url": True,
        "allow_data_uri": False,
        "allow_raw_base64": False,
        "allow_asset": True,
        "allow_local_file": False,
        "local_encoding": "",
        "file_formats": {
        },
        "data_types": [],
    },
    "rule_3": {
        "allow_url": True,
        "allow_data_uri": False,
        "allow_raw_base64": False,
        "allow_asset": True,
        "allow_local_file": False,
        "local_encoding": "",
        "file_formats": {
        },
        "data_types": [],
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

payload["input"][3]["video_url"]["url"] = _resolve_media(payload["input"][3]["video_url"]["url"], _MEDIA_RULES["rule_1"], "payload[\"input\"][3][\"video_url\"][\"url\"]")[0]
payload["input"][1]["video_url"]["url"] = _resolve_media(payload["input"][1]["video_url"]["url"], _MEDIA_RULES["rule_2"], "payload[\"input\"][1][\"video_url\"][\"url\"]")[0]
payload["input"][2]["video_url"]["url"] = _resolve_media(payload["input"][2]["video_url"]["url"], _MEDIA_RULES["rule_3"], "payload[\"input\"][2][\"video_url\"][\"url\"]")[0]

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
          "text": "Task ID: task_S971J45OtBnfTnlagSm0FCZkUN2mApma"
        }
      ]
    }
  ],
  "usage": {
    "input_tokens": 0,
    "input_tokens_details": {
      "cached_tokens": 0
    },
    "output_tokens": 339660,
    "output_tokens_details": {
      "reasoning_tokens": 0
    },
    "total_tokens": 339660
  }
}
```
## 获取生成视频 示例代码

```python
"""
╔═══════════════════════════════════════════════════════════════╗
║                  DMXAPI 自研接口                               ║
╚═══════════════════════════════════════════════════════════════╝

📝 功能说明:
   本脚本演示如何使用 requests 库查询视频生成任务并获取生成视频链接

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

    # 【model】(string, 必填) 查询视频生成任务使用的模型名称（官方文档未明确说明）
    "model": "seedance-2-5-get",

    # 【input】(string, 必填) 提交任务时返回的任务 ID
    # 视频生成任务 ID 仅保存 7 天（从 created_at 时间戳开始计算），超时后将自动清除
    # 创建视频生成任务为异步接口，获取 ID 后需通过本接口查询任务状态，
    # 任务成功后会输出生成视频的链接
    "input": "task_S971J45OtBnfTnlagSm0FCZkUN2mApma"

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
  "created_at": 1787320062,
  "duration": 4,
  "execution_expires_after": 172800,
  "framespersecond": 24,
  "generate_audio": true,
  "id": "task_S971J45OtBnfTnlagSm0FCZkUN2mApma",
  "model": "doubao-seedance-2-5-260628",
  "output": [
    {
      "type": "message",
      "content": [
        {
          "type": "output_text",
          "text": "https://ark-acg-cn-bejing.tos-cn-beijing.volces.com/doubao-seedance-2-5/d1ee881dc31840cb9471483848f61c67.mp4?X-Tos-Algorithm=TOS4-HMAC-SHA256&X-Tos-Credential=AKLTNTEwMTIwZTEzYWE0NDcwOWE1Yzk2MzQ0ZjViYTk3OWU%2F20260821%2Fcn-beijing%2Ftos%2Frequest&X-Tos-Date=20260821T135034Z&X-Tos-Expires=86399&X-Tos-Signature=d0082a4a3181d76312ea50e9d6d60345649f408e1352e20b42c072afe42726e4&X-Tos-SignedHeaders=host"
        }
      ]
    }
  ],
  "ratio": "269:215",
  "resolution": "720p",
  "seed": 96342,
  "service_tier": "default",
  "status": "succeeded",
  "updated_at": 1787320227,
  "usage": {
    "completion_tokens": 325321,
    "input_tokens": 0,
    "input_tokens_details": {
      "cached_tokens": 0
    },
    "output_tokens": 0,
    "output_tokens_details": {
      "reasoning_tokens": 0
    },
    "total_tokens": 0
  }
}
```

<p align="center">
  <small>© 2026 DMXAPI doubao-seedance-2-5-260628 视频延长</small>
</p>