# doubao-seedance-2-0-fast-260128 首帧生视频 API 使用文档

doubao-seedance-2-0-fast-260128 是字节跳动豆包 Seedance 2.0 Fast 系列的高性能图生视频模型，支持以图片作为首帧参考、结合文本提示词生成高质量视频。通过 DMXAPI 的 `/v1/responses` 端点以两步异步方式完成：首先提交生成任务获得任务 ID，再通过查询接口获取生成的视频 URL。模型支持 480p/720p 分辨率，视频时长 4~15 秒，支持自动有声生成（含人声、音效及背景音乐）、多种宽高比（16:9 / 9:16 / adaptive 等 7 种），以及联网搜索工具增强视频内容的时效性。

## 模型名称

- `doubao-seedance-2-0-fast-260128`

## 接口地址

| 接口 | 请求方式 | URL |
|------|---------|-----|
| 提交任务 | POST | `https://www.dmxapi.cn/v1/responses` |
| 获取结果 | POST | `https://www.dmxapi.cn/v1/responses` |

:::warning
请妥善保管您的 API Key！严禁将密钥泄露给他人、硬编码到代码中或提交到公开的代码仓库。
:::

## 首帧生视频 示例代码

```python
import requests
import json
import base64
import os

# ==================================================================
#  ↓↓↓  用户配置区：只需修改下面这部分即可  ↓↓↓
# ==================================================================

# 步骤1: 配置 API 连接信息

# DMXAPI 服务端点地址
url = "https://www.dmxapi.cn/v1/responses"

# DMXAPI 密钥 (请替换为您自己的密钥)
# 获取方式: 登录 DMXAPI 官网 -> 个人中心 -> API 密钥管理
api_key = "sk-*****************************************"

# 选择图片输入方式 (二选一，取消注释对应行即可)
# 方式1: 本地图片上传 (填写本地图片路径)
image_input = r"C:\Users\a1\Pictures\1689320796087949.png"
# 方式2: 公网 URL 上传 (填写图片公网地址)
# image_input = "https://img.shetu66.com/2023/07/14/1689320796087949.png"

# 文本提示词 (中文不超过 500 字，英文不超过 1000 词)
# 建议将对话内容放入双引号内，以优化音频生成效果
prompt = "图中小狗对着镜头说\"茄子\"，360度环绕运镜"

# ==================================================================
#  ↑↑↑  用户配置区结束，以下内容一般无需修改  ↑↑↑
# ==================================================================


# ===== 工具函数: 读取本地图片并转为 Base64 Data URL =====
def image_to_base64(image_path):
    """
    读取本地图片文件并转换为 data:image/<格式>;base64,<编码> 形式的字符串

    :param image_path: 本地图片路径
    :return: data url 字符串
    """
    # 根据文件后缀确定图片格式 (MIME type)
    ext = os.path.splitext(image_path)[1].lower().lstrip(".")
    # 统一 jpg -> jpeg
    if ext == "jpg":
        ext = "jpeg"

    # 支持的图片格式校验 (jpeg、png、webp、bmp、tiff、gif)
    supported = {"jpeg", "png", "webp", "bmp", "tiff", "gif"}
    if ext not in supported:
        raise ValueError(f"不支持的图片格式: {ext}，支持的格式为 {supported}")

    # 以二进制方式读取图片并编码
    with open(image_path, "rb") as f:
        encoded = base64.b64encode(f.read()).decode("utf-8")

    # 拼接成 data url 格式
    return f"data:image/{ext};base64,{encoded}"


# ===== 工具函数: 统一解析图片输入，自动识别两种方式 =====
def resolve_image_url(image_input):
    """
    根据传入内容自动识别图片输入方式并返回 API 所需的 url 字符串：
      1) 本地图片路径   -> 读取并转为 Base64 Data URL
      2) 公网 URL       -> 以 http:// 或 https:// 开头，直接返回

    :param image_input: 本地路径 / 公网URL
    :return: API image_url 字段所需的 url 字符串
    """
    # 方式2: 公网 URL 上传 (http/https)，直接返回
    if image_input.startswith("http://") or image_input.startswith("https://"):
        return image_input

    # 方式1: 本地图片上传，读取并转为 Base64 Data URL
    if os.path.isfile(image_input):
        return image_to_base64(image_input)

    # 都不匹配则报错提示
    raise ValueError(
        f"无法识别的图片输入: {image_input}\n"
        f"请传入 本地图片路径 / 公网URL(http(s)://...) 两者之一"
    )


# 步骤2: 配置请求头
headers = {
    "Content-Type": "application/json",      # 指定请求体为 JSON 格式
    "Authorization": f"Bearer {api_key}",           # token 认证方式
}

# 统一解析为 API 所需的 url 字符串
image_url = resolve_image_url(image_input)


# 步骤3: 配置请求参数
payload = {
    # 【model】(string, 必填) 调用的模型 ID
    # 本文档使用 doubao-seedance-2-0-fast-260128 首帧生视频模型
    "model": "doubao-seedance-2-0-fast-260128",

    # 【input】(array, 必填) 输入给模型生成视频的信息
    # 首帧生视频场景：文本（可选）+ 图片（role="first_frame"）
    "input": [
        {
            # type: 输入内容类型，文本提示词填 "text"
            "type": "text",
            # text: 文本提示词，中文不超过 500 字，英文不超过 1000 词
            # 建议将对话内容放入双引号内，以优化音频生成效果
            "text": prompt
        },
        {
            # type: 输入内容类型，图片输入填 "image_url"
            "type": "image_url",
            "image_url": {
                # url: 图片公网 URL、Base64 编码（data:image/<格式>;base64,<编码>）或素材 ID
                # 图片格式: jpeg、png、webp、bmp、tiff、gif
                # 宽高比要求: (0.4, 2.5)，宽高长度 (300, 6000)px，单张大小 < 30 MB
                # 此处由 resolve_image_url() 自动识别 本地图片/公网URL 两种方式
                "url": image_url
            },
            # role: 图片角色。首帧生视频使用 "first_frame"；尾帧使用 "last_frame"；参考图使用 "reference_image"
            # 条件必填：图生视频-首帧、首尾帧、多模态参考为三种互斥场景，不可混用
            "role": "first_frame"
        },
    ],

    # 【generate_audio】(boolean, 可选) 是否生成有声视频，默认值 true
    # true: 模型自动生成与画面同步的人声、音效及背景音乐
    # false: 输出无声视频
    # 仅 seedance 2.0 & 2.0 fast、seedance 1.5 pro 支持；生成的有声视频均为单声道
    "generate_audio": True,

    # 【resolution】(string, 可选) 视频分辨率，默认值 720p
    # 可选值: "480p" / "720p"
    # 注意: seedance 2.0 fast 不支持 1080p
    "resolution": "480p",

    # 【ratio】(string, 可选) 生成视频的宽高比，默认值 adaptive
    # 可选值: "16:9" / "4:3" / "1:1" / "3:4" / "9:16" / "21:9" / "adaptive"
    # "adaptive": 根据首帧图片比例自动选择最接近的宽高比
    "ratio": "16:9",

    # 【duration】(integer, 可选) 视频时长（秒），默认值 5
    # seedance 2.0 & 2.0 fast 支持范围: [4, 15]
    # 设为 -1: 由模型在有效范围内自主选择合适时长（视频时长与计费相关，请谨慎设置）
    "duration": 4,

    # 【seed】(integer, 可选) 随机种子，默认值 -1
    # 取值范围: [-1, 2^32-1]
    # -1: 使用随机数，每次生成结果不同
    # 相同 seed + 相同请求 -> 生成类似结果（不保证完全一致）
    "seed": -1,

    # 【watermark】(boolean, 可选) 是否在视频中添加水印，默认值 false
    # false: 不含水印；true: 含水印
    "watermark": False,

    # 【callback_url】(string, 可选) 任务状态变化时的回调通知地址
    # 方舟会向此地址推送 POST 请求，回调内容与查询任务 API 返回体一致
    # 任务状态枚举: queued（排队中）/ running（运行中）/ succeeded（成功）/ failed（失败）/ expired（超时）
    "callback_url": "https://www.dmxapi.cn",

    # 【return_last_frame】(boolean, 可选) 是否返回生成视频的尾帧图像，默认值 false
    # true: 可通过查询接口获取 png 格式尾帧图像（宽高与视频一致，无水印），可用于生成多个连续视频
    # false: 不返回尾帧图像
    "return_last_frame": False,

    # 【execution_expires_after】(integer, 可选) 任务超时阈值（秒），默认值 172800
    # 取值范围: [3600, 259200]（1小时 ~ 72小时），默认 48 小时（172800 秒）
    # 超过该时间后任务自动终止并标记为 expired
    "execution_expires_after": 172800,

    # 【tools】(array, 可选) 工具配置，仅 seedance 2.0 & 2.0 fast 支持
    # type: "web_search" 开启联网搜索，模型根据提示词自主判断是否搜索互联网内容
    # 开启后可提升视频内容时效性，但会增加一定时延
    "tools": [{"type": "web_search"}]
}

# 步骤4: 发送请求并输出结果
response = requests.post(url, headers=headers, json=payload)

# 格式化输出 JSON 响应
# - indent=2: 缩进 2 空格，便于阅读
# - ensure_ascii=False: 正确显示中文字符
print(json.dumps(response.json(), indent=2, ensure_ascii=False))
```

## 返回示例

```json
{
  "id": "cgt-20260424185140-4bwl4",
  "usage": {
    "total_tokens": 32160,
    "input_tokens": 0,
    "input_tokens_details": {
      "cached_tokens": 0
    },
    "output_tokens": 32160,
    "output_tokens_details": {
      "reasoning_tokens": 0
    }
  }
}
```

> 返回的 `id` 字段即为视频生成任务 ID，用于第二步查询结果。任务 ID 仅保存 7 天，请及时获取视频。

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
    "input": "cgt-20260507191840-fpbsd"
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
    last_frame_url = inner["content"].get("last_frame_url")
    if last_frame_url:
        print(f"尾帧图像: {last_frame_url}")
except Exception as e:
    print(f"提取 URL 失败: {e}")
```

## 返回示例

```json
{
  "request_id": "cgt-20260428165939-ccb9g",
  "output": [
    {
      "type": "message",
      "content": [
        {
          "type": "output_text",
          "text": "{\"content\":{\"video_url\":\"https://ark-acg-cn-beijing.tos-cn-beijing.volces.com/doubao-seedance-2-0-fast/02177736688829100000000000000000000ffffac177fcdd9df5d.mp4?...\"},\"id\":\"cgt-20260428165939-ccb9g\",\"model\":\"doubao-seedance-2-0-fast-260128\",\"status\":\"succeeded\"}"
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

视频链接: https://ark-acg-cn-beijing.tos-cn-beijing.volces.com/doubao-seedance-2-0-fast/02177736688829100000000000000000000ffffac177fcdd9df5d.mp4?...
```

<p align="center">
  <small>© 2026 DMXAPI doubao-seedance-2-0-fast-260128 首帧生视频</small>
</p>
