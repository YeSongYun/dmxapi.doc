# doubao-seedance-2-0-fast-260128 首尾帧生视频 API 使用文档

doubao-seedance-2-0-fast-260128 首尾帧生视频是字节跳动豆包 Seedance 2.0 Fast 系列的高速视频生成模型，通过指定首帧图片和尾帧图片（配合文本提示词），自动生成一段流畅连贯的过渡视频。模型支持生成 4~15 秒有声或无声视频，分辨率最高 720p，视频宽高比支持自适应或多种固定比例（16:9、4:3、1:1、3:4、9:16、21:9），并额外支持联网搜索增强（web_search 工具）、回调通知及尾帧返回等特性。采用异步两步调用模式：先提交任务获取任务 ID，再通过查询接口轮询获取视频链接。

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


## 首尾帧生视频 示例代码

```python
import requests
import json
import base64
import os


# ═══════════════════════════════════════════════════════════════
# 🔑 步骤1: 配置 API 连接信息
# ═══════════════════════════════════════════════════════════════

# 🌐 DMXAPI 服务端点地址
url = "https://www.dmxapi.cn/v1/responses"

# 🔐 DMXAPI 密钥 (请替换为您自己的密钥)
# 获取方式: 登录 DMXAPI 官网 -> 个人中心 -> API 密钥管理
api_key = "sk-**********************************************"

# ═══════════════════════════════════════════════════════════════
# 📋 步骤2: 配置请求头
# ═══════════════════════════════════════════════════════════════

headers = {
    "Content-Type": "application/json",      # 指定请求体为 JSON 格式
    # 【鉴权方式】使用 token 认证，直接传入 API Key
    "Authorization": f"{api_key}",           # token 认证方式
}

# ═══════════════════════════════════════════════════════════════
# 🖼️ 步骤3: 配置首帧 / 尾帧图片来源 (每张图片二选一即可)
# ═══════════════════════════════════════════════════════════════

# -------- 首帧图片 --------
# 【方式一】网络图片 URL
# first_frame_source = "https://img.shetu66.com/2023/07/14/1689320796087949.png"
# 【方式二】本地图片路径
first_frame_source = "C:/Users/a1/Pictures/1689320796087949.png"

# -------- 尾帧图片 --------
# 【方式一】网络图片 URL
last_frame_source = "https://img.sucaijishi.com/uploadfile/2023/0301/20230301120626930.png?imageMogr2/format/jpg/blur/1x0/quality/60"
# 【方式二】本地图片路径
# last_frame_source = "C:/Users/a1/Pictures/dog2.png"


# ╔═══════════════════════════════════════════════════════════════╗
# ║     ⚙️ 图片处理函数（自动识别网络URL或本地路径，无需修改）       ║
# ╚═══════════════════════════════════════════════════════════════╝

def resolve_image_url(source):
    """
    自动识别图片来源并返回可用的 URL 字符串

    - 网络图片: 直接返回原始 URL
    - 本地图片: 读取文件并转换为 Base64 Data URL

    :param source: 网络图片 URL 或本地图片文件路径
    :return: 可直接用于 API 请求的图片 URL 字符串
    """
    # 如果是网络 URL，直接返回
    if source.startswith("http://") or source.startswith("https://"):
        return source

    # 否则按本地文件处理：读取并转换为 Base64 Data URL
    ext = os.path.splitext(source)[1].lower().lstrip(".")
    if ext == "jpg":
        ext = "jpeg"
    with open(source, "rb") as f:
        base64_data = base64.b64encode(f.read()).decode("utf-8")
    return f"data:image/{ext};base64,{base64_data}"


# ═══════════════════════════════════════════════════════════════
# 💬 步骤4: 配置请求参数
# ═══════════════════════════════════════════════════════════════

payload = {
    # 【model】(string, 必填) 模型 ID
    "model": "doubao-seedance-2-0-260128",

    # 【input】(array, 必填) 输入内容数组
    # 首尾帧场景需传入: 1个文本对象 + 2个图片对象（分别指定 first_frame / last_frame）
    "input": [
        {
            # 【type】(string, 必填) 内容类型，文本时固定为 text
            "type": "text",
            # 【text】(string, 必填) 文本提示词，描述视频动作和镜头
            # 建议中文不超过 500 字，英文不超过 1000 词
            "text": "图1中小狗跳到图二小狗身上，对着镜头说\"茄子\"，360度环绕运镜"
        },
        {
            # 【type】(string, 必填) 内容类型，图片时固定为 image_url
            "type": "image_url",
            "image_url": {
                # 【url】(string, 必填) 图片公网 URL、Base64 编码或素材 ID
                # 格式要求: jpeg/png/webp/bmp/tiff/gif，宽高比 (0.4, 2.5)，单张 < 30 MB
                "url": resolve_image_url(first_frame_source)
            },
            # 【role】(string, 必填) 首尾帧场景必填
            # first_frame: 首帧图片（以首帧宽高比为准，尾帧会自动裁剪适配）
            "role": "first_frame"
        },
        {
            "type": "image_url",
            "image_url": {
                "url": resolve_image_url(last_frame_source)
            },
            # last_frame: 尾帧图片
            "role": "last_frame"
        },
    ],

    # 【generate_audio】(boolean, 可选) 是否生成同步音频，默认 true
    # true: 自动生成人声、音效及背景音乐（对话建议加双引号以优化效果）
    # false: 输出无声视频
    "generate_audio": True,

    # 【resolution】(string, 可选) 视频分辨率，默认 720p
    # 可选值: "480p" / "720p"/ "1080p"
    "resolution": "720p",

    # 【ratio】(string, 可选) 视频宽高比，默认 adaptive
    # 可选值: "16:9" / "4:3" / "1:1" / "3:4" / "9:16" / "21:9" / "adaptive"
    # adaptive: 根据首帧图片比例自动选择最接近的宽高比
    "ratio": "adaptive",

    # 【duration】(integer, 可选) 视频时长（秒），默认 5
    # Seedance 2.0 支持范围: [4, 15]
    "duration": 5,

    # 【seed】(integer, 可选) 随机种子，默认 -1（使用随机数）
    # 取值范围: [-1, 2^32-1]，相同 seed 在相同请求下生成结果相似（不保证完全一致）
    "seed": -1,

    # 【watermark】(boolean, 可选) 是否添加水印，默认 false
    "watermark": False,

    # 【callback_url】(string, 可选) 任务状态变化时的回调通知地址
    # 状态包括: queued / running / succeeded / failed / expired
    "callback_url": "https://www.dmxapi.cn",

    # 【return_last_frame】(boolean, 可选) 是否返回生成视频的尾帧图像，默认 false
    # true: 可通过查询接口获取 PNG 格式的尾帧图像（无水印，宽高与视频一致）
    # 适用场景: 将尾帧作为下一段视频的首帧，实现连续视频生成
    "return_last_frame": False,

    # 【execution_expires_after】(integer, 可选) 任务超时阈值（秒），默认 172800（48小时）
    # 取值范围: [3600, 259200]，超时后任务自动终止并标记为 expired
    "execution_expires_after": 172800,

    # 【tools】(array, 可选) 工具配置，仅 Seedance 2.0 支持
    # web_search: 启用联网搜索，模型自主判断是否搜索互联网内容，提升时效性但会增加时延
    "tools": [{"type": "web_search"}]
}


# ═══════════════════════════════════════════════════════════════
# 📤 步骤5: 发送请求并输出结果
# ═══════════════════════════════════════════════════════════════

response = requests.post(url, headers=headers, json=payload)
print(json.dumps(response.json(), indent=2, ensure_ascii=False))
```

## 返回示例

```json
{
  "id": "cgt-20260424185225-sb9vm",
  "usage": {
    "total_tokens": 40200,
    "input_tokens": 0,
    "input_tokens_details": {
      "cached_tokens": 0
    },
    "output_tokens": 40200,
    "output_tokens_details": {
      "reasoning_tokens": 0
    }
  }
}
```

> 返回的 `id` 字段为视频生成任务 ID，用于下一步查询任务结果。任务 ID 仅保存 7 天，超时后自动清除。

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
  <small>© 2026 DMXAPI doubao-seedance-2-0-fast-260128 首尾帧生视频</small>
</p>
