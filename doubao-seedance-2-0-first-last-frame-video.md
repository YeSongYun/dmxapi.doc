# doubao-seedance-2-0-260128 首尾帧生视频 API 使用文档

基于 doubao-seedance-2-0-260128 模型的 AI 视频生成接口，支持输入首帧图片 + 尾帧图片 + 文本提示词生成目标视频。模型根据首尾两帧图像自动补全中间动态画面，支持自动音频生成，可选 480p / 720p /1080p / 4k 分辨率，宽高比支持 16:9、9:16、adaptive 等 7 种规格，视频时长范围 4~15 秒（可设为 -1 由模型自动决定）。采用异步任务模式，提交后通过单次查询获取结果视频 URL。

## 🎬 模型名称

- `doubao-seedance-2-0-260128`

## 🌐 接口地址

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


## 🎥 首尾帧生视频 示例代码

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
# 步骤3: 配置首帧与尾帧图片来源（每张图片选择一种即可）
# ===============================================================

# 首帧图片
# 【方式一】网络图片 URL（支持 HTTP / HTTPS 协议）
# first_frame_source = "https://img.shetu66.com/2023/07/14/1689320796087949.png"
# 【方式二】本地图片路径（代码自动转换为 Data URL）
first_frame_source = "C:/Users/a1/Pictures/1689320796087949.png"
# 【方式三】素材 ID
# first_frame_source = "asset://<ASSET_ID>"

# 尾帧图片
# 【方式一】网络图片 URL（支持 HTTP / HTTPS 协议）
# last_frame_source = "https://img.sucaijishi.com/uploadfile/2023/0301/20230301120626930.png"
# 【方式二】本地图片路径（代码自动转换为 Data URL）
last_frame_source = "C:/Users/a1/Pictures/20230301120626930.jpg"
# 【方式三】素材 ID
# last_frame_source = "asset://<ASSET_ID>"

# ===============================================================
# 步骤4: 配置请求参数
# ===============================================================

payload = {
    # 【input】(object[], 必填) 输入内容列表
    # 输入给模型生成视频的信息，支持文本、图片等多种类型的元素
    # 本示例传入 1 段文本提示词 + 首帧图片 + 尾帧图片
    "input": [
        {
            # 【type】(string, 必填) 内容类型
            # 输入内容的类型，此处固定为 text
            "type": "text",

            # 【text】(string, 必填) 文本提示词
            # 描述视频的动作、镜头与画面变化
            # 建议中文不超过 500 字，英文不超过 1000 词
            # 建议将对话部分置于双引号内以优化音频生成效果
            "text": "图1中小狗跳到图二小狗身上，对着镜头说\"茄子\"，360度环绕运镜"
        },
        {
            # 【image_url】(object, 必填) 图片对象
            # 输入给模型的首帧图片对象
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
                "url": first_frame_source
            },

            # 【role】(string, 必填) 角色/用途
            # 图片的位置或用途，首尾帧场景中首帧固定为 first_frame
            # 以首帧宽高比为准，尾帧会自动裁剪适配
            # 注意: 图生视频-首帧、图生视频-首尾帧、多模态参考生视频为 3 种互斥场景，不可混用
            "role": "first_frame",

            # 【type】(string, 必填) 内容类型
            # 输入内容的类型，此处固定为 image_url
            "type": "image_url"
        },
        {
            # 【image_url】(object, 必填) 图片对象
            # 输入给模型的尾帧图片对象，格式与大小要求同首帧
            "image_url": {
                # 【url】(string, 必填) 图片来源
                # 支持图片 URL、图片 Base64 编码、素材 ID 三种形式，要求同首帧
                "url": last_frame_source
            },

            # 【role】(string, 必填) 角色/用途
            # 图片的位置或用途，首尾帧场景中尾帧固定为 last_frame
            # 说明: 传入的首尾帧图片可以相同
            "role": "last_frame",

            # 【type】(string, 必填) 内容类型
            # 输入内容的类型，此处固定为 image_url
            "type": "image_url"
        }
    ],

    # 【callback_url】(string, 可选) 回调地址
    # 任务状态发生变化时，平台会向该地址推送 POST 请求，请求体结构与查询任务接口返回体一致
    # 回调状态: queued(排队中) / running(运行中) / succeeded(成功) / failed(失败) / expired(超时)
    # 若 5 秒内未收到成功发送的响应，会重试推送三次
    "callback_url": "https://www.dmxapi.cn",

    # 【duration】(integer, 可选) 视频时长
    # 生成视频时长（单位：秒），默认值 5
    # 取值范围: [4, 15]；或设置为 -1（智能选择，模型在有效取值范围内自主选择合适的整数秒时长）
    # 注意: 视频时长与计费相关，请谨慎设置
    "duration": 5,

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
    # 注意: 生成的有声视频均为单声道
    "generate_audio": True,

    # 【model】(string, 必填) 调用的模型名称
    "model": "doubao-seedance-2-0-260128",

    # 【ratio】(string, 可选) 视频宽高比
    # 生成视频的宽高比例，默认值 adaptive
    # 可选值: "16:9" / "4:3" / "1:1" / "3:4" / "9:16" / "21:9"
    #         "adaptive"(根据首帧图片比例自动选择最接近的宽高比)
    # 注意: 指定的宽高比与图片不一致时，方舟会对图片进行居中裁剪
    "ratio": "adaptive",

    # 【resolution】(string, 可选) 视频分辨率
    # 视频分辨率，默认值 720p
    # 可选值: "480p" / "720p" / "1080p" / "4k"
    # 各宽高比对应的宽高像素值:
    #   - 480p : 16:9 854×480、4:3 752×560、1:1 640×640、3:4 560×752、9:16 480×854、21:9 992×432
    #   - 720p : 16:9 1280×720、4:3 1112×834、1:1 960×960、3:4 834×1112、9:16 720×1280、21:9 1470×630
    #   - 1080p: 16:9 1920×1080、4:3 1664×1248、1:1 1440×1440、3:4 1248×1664、9:16 1080×1920、21:9 2206×946
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
        },
        "data_types": ["image/bmp", "image/gif", "image/jpeg", "image/png", "image/tiff", "image/webp"],
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

payload["input"][1]["image_url"]["url"] = _resolve_media(payload["input"][1]["image_url"]["url"], _MEDIA_RULES["image"], "首帧图片")[0]
payload["input"][2]["image_url"]["url"] = _resolve_media(payload["input"][2]["image_url"]["url"], _MEDIA_RULES["image"], "尾帧图片")[0]

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
  "id": "task_p46dkakegnrlX8lTCI9Js3Ipkor4VvfO",
  "usage": {
    "total_tokens": 50000,
    "input_tokens": 0,
    "input_tokens_details": {
      "cached_tokens": 0
    },
    "output_tokens": 50000,
    "output_tokens_details": {
      "reasoning_tokens": 0
    }
  }
}
```

> 返回的 `id` 为视频生成任务 ID，保存期限为 7 天（从创建时间戳开始计算）。

## 📥 获取结果 示例代码

```python
import requests
import json

url = "https://www.dmxapi.cn/v1/responses"
api_key = "sk-******************************************"

headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {api_key}",
}

payload = {
    # 【model】(string, 必填) 固定值，用于查询 Seedance 视频生成结果
    "model": "seedance-2-0-get",
    # 【input】(string, 必填) 提交任务时返回的任务 ID
    "input": "task_p46dkakegnrlX8lTCI9Js3Ipkor4VvfO"
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
  "request_id": "task_p46dkakegnrlX8lTCI9Js3Ipkor4VvfO",
  "output": [
    {
      "type": "message",
      "content": [
        {
          "type": "output_text",
          "text": "{\"content\":{\"video_url\":\"https://ark-acg-cn-beijing.tos-cn-beijing.volces.com/doubao-seedance-2-0/02177520799968800000000000000000000ffffac14d8d3a26bee.mp4?...\"},\"id\":\"cgt-20260403171827-s64n7\",\"model\":\"doubao-seedance-2-0-260128\",\"status\":\"succeeded\"}"
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

视频链接: https://ark-acg-cn-beijing.tos-cn-beijing.volces.com/doubao-seedance-2-0/02177520799968800000000000000000000ffffac14d8d3a26bee.mp4?...
```


<p align="center">
  <small>© 2026 DMXAPI doubao-seedance-2-0-260128 首尾帧生视频</small>
</p>
