# doubao-seedance-2-0-260128 视频编辑 API 使用文档

基于字节跳动 Seedance 2.0 多模态视频生成模型，doubao-seedance-2-0-260128 支持参考图片和视频进行智能视频编辑，可实现场景替换、主体替换、视频延长、风格迁移等多种编辑效果。支持多模态输入（文本 + 图片 + 视频 + 音频组合），最多接受 9 张参考图和 3 段参考视频，生成分辨率支持 480p/720p/1080p/4k，时长 4~15 秒可控。采用异步任务模式，提交任务后获取任务 ID，再通过专用接口获取生成的视频 URL。

## 🎬 模型名称
- `doubao-seedance-2-0-260128`
## 🔗 接口地址

| 接口 | 请求方式 | URL |
|------|---------|-----|
| 提交任务 | POST | `https://www.dmxapi.cn/v1/responses` |
| 获取结果 | POST | `https://www.dmxapi.cn/v1/responses` |

:::warning
请妥善保管您的 API Key！严禁将密钥泄露给他人、硬编码到代码中或提交到公开的代码仓库。如果怀疑密钥已泄露，请立即前往 DMXAPI 官网重新生成。
:::

:::warning 异步任务，请妥善保存任务 ID
本模型为**异步任务**接口：提交任务后不会直接返回视频，只返回一个任务 ID（响应中的 `id` 字段），需再用查询模型 `seedance-2-0-get` 凭该 ID 换取最终视频地址。请在提交成功后立即将任务 ID 落库或写入日志妥善保存——一旦丢失将无法找回，本次生成结果也无法再取回，但费用已产生。
:::


## 🎥 视频编辑 示例代码

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
# 步骤3: 配置参考图片来源（选择一种即可）
# ===============================================================

# 【方式一】网络图片 URL（支持 HTTP / HTTPS 协议）
# image_source = "https://ark-project.tos-cn-beijing.volces.com/doc_image/r2v_edit_pic1.jpg"

# 【方式二】本地图片路径（代码自动转换为 Data URL）
# image_source = "C:/Users/a1/Pictures/20230301120626930.jpg"

# 【方式三】素材 ID
image_source = "asset://asset-20260401123823-6d4x2"

# ===============================================================
# 步骤4: 配置请求参数
# ===============================================================

payload = {
    # 【input】(object[], 必填) 输入内容列表
    # 输入给模型生成视频的信息，支持文本、图片、视频、音频等多种类型的元素
    # 本示例传入 1 段编辑指令 + 1 张参考图片 + 1 个待编辑的参考视频
    "input": [
        {
            # 【type】(string, 必填) 内容类型
            # 输入内容的类型，此处固定为 text
            "type": "text",

            # 【text】(string, 可选) 文本提示词
            # 描述对原视频的编辑指令，如场景替换、主体替换、风格迁移等
            # 建议中文不超过 500 字，英文不超过 1000 词
            # 可使用 [图1][视频1] 等方式明确指定各素材的用途
            # 建议将对话部分置于双引号内以优化音频生成效果
            "text": "图片1中的人物将视频1礼盒中的香水拿起来喷到自己的身上"
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
                #   - 格式: jpeg、png、webp、bmp、tiff、gif
                #   - 宽高比(宽/高): [0.4, 2.5]
                #   - 宽高长度(px): [300, 6000]
                #   - 大小: 单张图片小于 30 MB，请求体大小不超过 64 MB
                #           大文件请勿使用 Base64 编码
                #   - 数量: Seedance 2.0 多模态参考生视频最多 9 张
                "url": image_source
            },

            # 【role】(string, 可选) 角色/用途
            # 图片的位置或用途，视频编辑场景中参考图对应的 role 为 reference_image
            # 注意: 图生视频-首帧、图生视频-首尾帧、多模态参考生视频为 3 种互斥场景，不可混用
            "role": "reference_image",

            # 【type】(string, 必填) 内容类型
            # 输入内容的类型，此处固定为 image_url
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
            # 输入给模型的待编辑视频对象
            "video_url": {
                # 【url】(string, 必填) 视频来源
                # 支持视频 URL、素材 ID 两种形式（不支持 Base64 编码）:
                #   - 视频 URL: 填入视频的公网 URL
                #   - 素材 ID: 遵循格式 asset://<ASSET_ID>，可从素材 & 虚拟人像库获取
                # 传入单个视频要求:
                #   - 视频格式: mp4、mov
                #   - 分辨率: 480p、720p、1080p
                #   - 时长: 单个视频 [2, 15] s，最多传入 3 个参考视频，所有视频总时长不超过 15 s
                #   - 帧率(FPS): [24, 60]
                #   - 大小: 单个视频不超过 50 MB
                #   - 建议: 传入视频的秒数最好是 15 s
                "url": "asset://asset-20260224190654-9nbbl"
            }
        }
    ],

    # 【callback_url】(string, 可选) 回调地址
    # 任务状态发生变化时，平台会向该地址推送 POST 请求，请求体结构与查询任务接口返回体一致
    # 回调状态: queued(排队中) / running(运行中) / succeeded(成功) / failed(失败) / expired(超时)
    # 若 5 秒内未收到成功发送的响应，会重试推送三次
    "callback_url": "https://www.dmxapi.cn",

    # 【duration】(integer, 可选) 视频时长
    # 生成视频时长（单位：秒），默认值 8
    # 取值范围: [8, 15]，视频编辑场景输出视频的秒数必须大于等于 8 s
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
    # 注意: 生成的有声视频均为单声道，和传入的音频声道数无关
    "generate_audio": True,

    # 【model】(string, 必填) 调用的模型名称
    "model": "doubao-seedance-2-0-260128",

    # 【ratio】(string, 可选) 视频宽高比
    # 生成视频的宽高比例，默认值 adaptive
    # 可选值: "16:9" / "4:3" / "1:1" / "3:4" / "9:16" / "21:9"
    #         "adaptive"(根据任务类型和输入内容自动适配宽高比)
    "ratio": "16:9",

    # 【resolution】(string, 可选) 视频分辨率
    # 视频分辨率，默认值 720p
    # 可选值: "480p" / "720p" / "1080p" / "4k"
    # 各宽高比对应的宽高像素值:
    #   - 480p : 16:9 854×480、4:3 752×560、1:1 640×640、3:4 560×752、9:16 480×854、21:9 992×432
    #   - 720p : 16:9 1280×720、4:3 1112×834、1:1 960×960、3:4 834×1112、9:16 720×1280、21:9 1470×630
    #   - 1080p: 16:9 1920×1080、4:3 1664×1248、1:1 1440×1440、3:4 1248×1664、9:16 1080×1920、21:9 2206×946
    "resolution": "480p",

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
    # 取值范围: [-1, 2^32-1]；-1 表示使用随机数
    # 相同请求下，相同 seed 会生成类似结果，但不保证完全一致
    "seed": -1,

    # 【tools】(object[], 可选) 工具配置
    # 仅 Seedance 2.0 与 2.0 fast 支持
    # web_search: 联网搜索工具，模型根据提示词自主判断是否搜索互联网内容（如商品、天气等）
    # 开启后可提升视频内容时效性，但会增加一定时延
    # 实际搜索次数可通过查询任务接口返回的 usage.tool_usage.web_search 字段获取
    "tools": [{"type": "web_search"}],

    # 【watermark】(boolean, 可选) 视频水印
    # 生成视频是否包含水印，默认值 false
    # 可选值:
    #   - True(生成视频右下角会展示「AI 生成」水印)
    #   - False(生成视频不含水印)
    "watermark": True
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
        },
        "data_types": ["image/bmp", "image/gif", "image/jpeg", "image/png", "image/tiff", "image/webp"],
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

payload["input"][1]["image_url"]["url"] = _resolve_media(payload["input"][1]["image_url"]["url"], _MEDIA_RULES["image"], "参考图片")[0]
payload["input"][2]["video_url"]["url"] = _resolve_media(payload["input"][2]["video_url"]["url"], _MEDIA_RULES["video"], "参考视频")[0]

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
### 返回示例

```json
{
  "id": "task_vhlevrcYnOEomUprf92xIlOjYWqLklDB",
  "usage": {
    "total_tokens": 64630,
    "input_tokens": 0,
    "input_tokens_details": {
      "cached_tokens": 0
    },
    "output_tokens": 64630,
    "output_tokens_details": {
      "reasoning_tokens": 0
    }
  }
}
```
## 📥 获取结果 示例代码

```python
import requests
import json

url = "https://www.dmxapi.cn/v1/responses"

# DMXAPI 密钥 (请替换为您自己的密钥)
api_key = "sk-******************************************"

headers = {
    "Content-Type": "application/json",
    # Authorization: Bearer 方式鉴权
    "Authorization": f"Bearer {api_key}",
}

payload = {
    # 【model】(string, 必填) 固定值，用于获取视频生成结果
    "model": "seedance-2-0-get",
    # 【input】(string, 必填) 提交任务时返回的任务 ID
    "input": "task_vhlevrcYnOEomUprf92xIlOjYWqLklDB"
}

response = requests.post(url, headers=headers, json=payload)
result = response.json()
print(json.dumps(result, indent=2, ensure_ascii=False))

# 提取 video_url
try:
    text = result["output"][0]["content"][0]["text"]
    inner = json.loads(text)
    video_url = inner["content"]["video_url"]
    print(f"\n视频链接: {video_url}")
except Exception as e:
    print(f"提取 URL 失败: {e}")
```

## 返回示例

```json
{
  "request_id": "task_vhlevrcYnOEomUprf92xIlOjYWqLklDB",
  "output": [
    {
      "type": "message",
      "content": [
        {
          "type": "output_text",
          "text": "{\"content\":{\"video_url\":\"https://ark-acg-cn-beijing.tos-cn-beijing.volces.com/doubao-seedance-2-0/...mp4\"},\"id\":\"cgt-20260403171827-s64n7\",\"model\":\"doubao-seedance-2-0-260128\",\"status\":\"succeeded\"}"
        }
      ]
    }
  ],
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
  <small>© 2026 DMXAPI doubao-seedance-2-0-260128 视频编辑</small>
</p>
