# doubao-seedance-2-5-260628 多模态参考视频 API 使用文档

基于 Doubao Seedance 2.5 的全模态参考生视频接口，通过 `/v1/responses` 端点以异步任务方式调用：可同时混合传入参考图片、参考视频与参考音频，由模型融合各素材的主体、构图、运镜与音色生成全新视频。单次最多支持 30 张参考图片、10 个参考视频（总时长 ≤ 30 秒）与 10 段参考音频（总时长 ≤ 30 秒），提示词中可用「@图像1」「@视频1」等标记精确指定每个素材的作用位置。通过 `omni_reference_task_type` 可在参考生视频（`reference`）、视频编辑（`edit`）、视频延长（`extend`）三类子任务间显式切换以提前校验参数，默认 `auto` 由模型自动判定，适合广告合成、多素材混剪、风格与运镜迁移等复杂创作场景。

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

## 多模态参考视频 示例代码

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
api_key = "sk------------------------------------------"

# ===============================================================
# 步骤2: 配置请求头
# ===============================================================

headers = {
    "Content-Type": "application/json",      # 指定请求体为 JSON 格式
    "Authorization": f"Bearer {api_key}",    # Bearer token 认证方式
}

# ===============================================================
# 步骤3: 配置请求参数
# ===============================================================

payload = {
    # 【model】(string, 必填) 调用的模型名称
    "model": "doubao-seedance-2-5-260628",

    # 【input】(object[], 必填) 输入内容列表
    # 所有文本、图片和视频参数均直接写在 payload 中。
    "input": [
        {           
            # 【text】(string, 必填) 文本提示词
            # 输入给模型的文本提示词，描述期望生成的视频
            # 语言支持: 中英文，额外支持西班牙语、印度尼西亚语、葡萄牙语、日语、马来语、
            #           泰语、阿拉伯语、越南语、韩语
            # 字数建议: 中文提示词不超过 500 字，英文提示词不超过 1000 词
            #           字数过多易导致信息分散，模型可能忽略细节、仅关注重点，
            #           进而造成视频缺失部分元素
            "type": "text",
            # 【type】(string, 必填) 内容类型
            # 输入内容的类型，此处固定为 text
            "text": (
                "明亮多彩的广告片风格，果味饼干为主角，包含草莓、苹果、葡萄、橙子四种口味，"
                "草莓味参考@图像1，饼干与对应水果以强秩序感的几何阵列排布，整体画面干净、高级、节奏强。"
                "开场水果快速建立视觉聚焦，参考@视频1的构图，音乐重拍切入。随后不同口味饼干整齐排列，切特写，"
                "参考@视频2的动态和运镜。高潮段一块饼干被折断，瞬间进入慢动作，果味夹心爆开，碎屑飞溅，"
                "果汁感与颗粒冲击被放大展示，参考@视频3的冲击感。横向阵列，形成节奏抛物感，参考@视频4的运动，"
                "突出秩序美感与产品丰富度。随后迅速回到快节奏剪辑。结尾英文文字 "
                "One bite of crispness, a heart full of delight 快速分词切换入画，"
                "配合强节奏文字运动与产品定格，参考@视频5，最终品牌感收束，饼干和水果向四周发散，"
                "参考@视频6画面充满年轻、活力、好吃、想分享的广告氛围。"
            ),
        },
        {
            # 【type】(string, 必填) 图片内容类型，固定为 image_url
            "type": "image_url",
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
            "image_url": {
                "url": "https://arkdocs.tos-cn-beijing.volces.com/images/video-generation/seedance2.5_reference1.png"
            },
            # 【role】(string, 可选)角色/用途 全模态参考图固定为 reference_image
            "role": "reference_image",
        },
        {
            # 【参考视频1】提示词中的 @视频1，对应官方 reference2.mp4
            "type": "video_url",
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
            "video_url": {
                "url": "https://arkdocs.tos-cn-beijing.volces.com/videos/video-generation/seedance2.5_reference2.mp4"
            },
            # 【role】(string, 可选) 角色/用途
            # 视频的位置或用途，此处固定为 reference_video
            "role": "reference_video",
        },
        {
            # 【参考视频2】提示词中的 @视频2，对应官方 reference3.mp4
            "type": "video_url",
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
            "video_url": {
                "url": "https://arkdocs.tos-cn-beijing.volces.com/videos/video-generation/seedance2.5_reference3.mp4"
            },
            "role": "reference_video",
        },
        {
            # 【参考视频3】提示词中的 @视频3，对应官方 reference4.mp4
            "type": "video_url",
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
            "video_url": {
                "url": "https://arkdocs.tos-cn-beijing.volces.com/videos/video-generation/seedance2.5_reference4.mp4"
            },
            "role": "reference_video",
        },
        {
            # 【参考视频4】提示词中的 @视频4，对应官方 reference5.mp4
            "type": "video_url",
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
            "video_url": {
                "url": "https://arkdocs.tos-cn-beijing.volces.com/videos/video-generation/seedance2.5_reference5.mp4"
            },
            "role": "reference_video",
        },
        {
            "type": "video_url",
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
            "video_url": {
                "url": "https://arkdocs.tos-cn-beijing.volces.com/videos/video-generation/seedance2.5_reference6.mp4"
            },
            "role": "reference_video",
        },
        {
            # 【参考视频6】提示词中的 @视频6，对应官方 reference7.mp4
            "type": "video_url",
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
            "video_url": {
                "url": "https://arkdocs.tos-cn-beijing.volces.com/videos/video-generation/seedance2.5_reference7.mp4"
            },
            # 【type】(string, 必填) 内容类型
            # 输入内容的类型，此处固定为 video_url
            "role": "reference_video",
        },
    ],

    # 【generate_audio】(boolean, 可选) 是否生成与画面同步的音频，默认为 true
    "generate_audio": True,

    # 【ratio】(string, 可选) 视频宽高比
    # 生成视频的宽高比例，默认值 adaptive
    # 可选值: "16:9" / "4:3" / "1:1" / "3:4" / "9:16" / "21:9"
    #         "adaptive"(根据任务类型和输入内容自动适配宽高比)
    "ratio": "16:9",

    # 【duration】(integer, 可选) 生成时长，单位为秒；可用范围 [4, 30] 或 -1
    "duration": 15,

    # 【omni_reference_task_type】(string, 可选) auto / reference / edit / extend
    # reference 表示基于参考图片、视频或音频生成新视频。
    "omni_reference_task_type": "reference",

    # 【output_format】(string, 可选) 输出格式
    # 输出视频的格式，默认值 mp4
    # 可选值:
    #   - "mp4"(通用格式，兼容性最好，采用标准色彩精度，可在网页、移动端、各类播放器
    #           及分发平台直接播放)
    #   - "mov"(面向专业场景的高色彩精度格式，更好地保持画面色彩与亮度一致性，适用于调色、
    #           抠像、合成等对色彩还原要求高的专业后期加工；推荐在视频编辑、视频延长场景
    #           使用 mov 格式作为输入和输出)
    # 注意: mov 格式采用 H.264 视频编码 + yuv444p 色度采样 + PCM 音频编码，部分播放器可能
    #       不兼容，常见支持的播放器有 IINA(仅 macOS)、VLC、mpv、ffpla
    "output_format": "mov",

    # 【execution_expires_after】(integer, 可选) 任务过期时间，单位为秒，取值范围 [3600, 259200]
    "execution_expires_after": 172800,

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
    "watermark": False,
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

# 按类型遍历全部输入项：text 跳过，image_url 用 rule_1，video_url 用 rule_2
for _i, _item in enumerate(payload["input"]):
    _type = _item.get("type")
    if _type == "image_url":
        _key, _rule = "image_url", _MEDIA_RULES["rule_1"]
    elif _type == "video_url":
        _key, _rule = "video_url", _MEDIA_RULES["rule_2"]
    else:
        continue
    _field = f'payload["input"][{_i}]["{_key}"]["url"]'
    _item[_key]["url"] = _resolve_media(_item[_key]["url"], _rule, _field)[0]

# ===============================================================
# 步骤5: 发送请求并输出结果
# ===============================================================

# 发送 POST 请求到 API 服务器（timeout 防止网络异常时永久阻塞）
response = requests.post(url, headers=headers, json=payload, timeout=60)

# 先检查 HTTP 状态码，避免服务端返回错误页时被 JSON 解析异常掩盖真实原因
if response.status_code != 200:
    print(f"请求失败，HTTP {response.status_code}")
    print(response.text)
    raise SystemExit(1)

# 格式化输出 JSON 响应
# - indent=2: 缩进 2 空格，便于阅读
# - ensure_ascii=False: 正确显示中文字符
try:
    print(json.dumps(response.json(), indent=2, ensure_ascii=False))
except ValueError:
    print("响应不是合法 JSON，原始内容如下：")
    print(response.text)
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
          "text": "Task ID: task_n1D0emjKbBcCcdIBqpzLIk2eaqLAeQyk"
        }
      ]
    }
  ],
  "usage": {
    "input_tokens": 0,
    "input_tokens_details": {
      "cached_tokens": 0
    },
    "output_tokens": 195300,
    "output_tokens_details": {
      "reasoning_tokens": 0
    },
    "total_tokens": 195300
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
    "input": "task_n1D0emjKbBcCcdIBqpzLIk2eaqLAeQyk"

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
  "created_at": 1787320339,
  "duration": 4,
  "execution_expires_after": 172800,
  "framespersecond": 24,
  "generate_audio": true,
  "id": "task_n1D0emjKbBcCcdIBqpzLIk2eaqLAeQyk",
  "model": "doubao-seedance-2-5-260628",
  "output": [
    {
      "type": "message",
      "content": [
        {
          "type": "output_text",
          "text": "https://ark-acg-cn-bejing.tos-cn-beijing.volces.com/doubao-seedance-2-5/8313196f9731415998f0563d28b8867f.mp4?X-Tos-Algorithm=TOS4-HMAC-SHA256&X-Tos-Credential=AKLTMWIyYzNkNGU1ZjY0Nzg4OTlhYWJiY2NkZGVlZmYwMA%2F20260821%2Fcn-beijing%2Ftos%2Frequest&X-Tos-Date=20260821T135541Z&X-Tos-Expires=86399&X-Tos-Signature=f60718293a4b5c6d7e8f90a1b2c3d4e5f60718293a4b5c6d7e8f90a1b2c3d4e5&X-Tos-SignedHeaders=host"
        }
      ]
    }
  ],
  "ratio": "16:9",
  "resolution": "720p",
  "seed": 78797,
  "service_tier": "default",
  "status": "succeeded",
  "updated_at": 1787320527,
  "usage": {
    "completion_tokens": 195300,
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
  <small>© 2026 DMXAPI doubao-seedance-2-5-260628 多模态参考视频</small>
</p>