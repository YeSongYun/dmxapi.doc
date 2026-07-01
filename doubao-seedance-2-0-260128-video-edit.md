# doubao-seedance-2-0-260128 视频编辑 API 使用文档

基于字节跳动 Seedance 2.0 多模态视频生成模型，doubao-seedance-2-0-260128 支持参考图片和视频进行智能视频编辑，可实现场景替换、主体替换、视频延长、风格迁移等多种编辑效果。支持多模态输入（文本 + 图片 + 视频 + 音频组合），最多接受 9 张参考图和 3 段参考视频，生成分辨率支持 480p/720p/1080p，时长 4~15 秒可控。采用异步任务模式，提交任务后获取任务 ID，再通过专用接口获取生成的视频 URL。

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


## 🎥 视频编辑 示例代码

```python
import requests
import json
import base64
import os

# ╔═══════════════════════════════════════════════════════════════╗
# ║              ⚙️ 基础配置（密钥 & 输入素材）                     ║
# ╚═══════════════════════════════════════════════════════════════╝

# ---------- 🔐 API 密钥 ----------
# 获取方式: 登录 DMXAPI 官网 -> 个人中心 -> API 密钥管理
api_key = "sk-****************************************"

# ---------- 🖼️ 图片输入 ----------
# 无需手动选择模式，直接填入即可，程序会自动识别以下三种格式：
#   1. 网络图片 URL    （http:// 或 https:// 开头）
#   2. 素材库 ID       （asset:// 开头，如 asset://asset-20260401123823-6d4x2）
#   3. 本地图片路径    （上述两种以外，按本地文件读取并转 Base64）
# image_input = "C:/Users/a1/Pictures/20230301120626930.jpg"
# image_input = "https://ark-project.tos-cn-beijing.volces.com/doc_image/r2v_edit_pic1.jpg"
image_input = "asset://asset-20260401123823-6d4x2"

# ---------- 🎬 视频输入 ----------
# 无需手动选择模式，直接填入即可，程序会自动识别以下两种格式：
#   1. 网络视频 URL    （http:// 或 https:// 开头）
#   2. 素材库 ID       （asset:// 开头，如 asset://asset-20260224190654-9nbbl）
# ⚠️ 注意：视频仅支持 URL / 素材 ID，不支持本地路径转 Base64
# ⚠️ 建议：传入视频的秒数最好是 15s
video_url = "asset://asset-20260224190654-9nbbl"

# ---------- 📝 提示词 ----------
prompt_text = "图片1中的人物将视频1礼盒中的香水拿起来喷到自己的身上"


# ╔═══════════════════════════════════════════════════════════════╗
# ║           🔩 内部处理逻辑（无需修改）                            ║
# ╚═══════════════════════════════════════════════════════════════╝

def encode_image_to_base64(path):
    """读取本地图片并转换为 Base64 Data URL"""
    ext = path.lower().split(".")[-1]
    mime_map = {
        "jpg": "image/jpeg", "jpeg": "image/jpeg",
        "png": "image/png",  "webp": "image/webp",
        "gif": "image/gif",
    }
    mime_type = mime_map.get(ext, "image/jpeg")
    with open(path, "rb") as f:
        encoded = base64.b64encode(f.read()).decode("utf-8")
    return f"data:{mime_type};base64,{encoded}"


def resolve_image_url(source):
    """
    自动识别图片来源并返回可用的 URL 字符串：
      - 网络图片 URL  : 直接返回原始 URL
      - 素材库 ID     : 形如 asset://asset-xxx，直接返回原始素材 ID
      - 本地图片路径  : 读取文件并转换为 Base64 Data URL
    """
    source = source.strip()

    # 网络图片 URL：直接返回
    if source.startswith("http://") or source.startswith("https://"):
        return source

    # 素材库 ID：形如 asset://asset-20260401123823-6d4x2，直接返回
    if source.startswith("asset://"):
        return source

    # 其余情况按本地图片路径处理
    return encode_image_to_base64(source)


def resolve_video_url(source):
    """
    自动识别视频来源并返回可用的 URL 字符串：
      - 网络视频 URL  : 直接返回原始 URL（http:// 或 https:// 开头）
      - 素材库 ID     : 形如 asset://asset-xxx，直接返回原始素材 ID
    ⚠️ 注意：视频仅支持 URL / 素材 ID 方式，不支持本地路径转 Base64。
            如需使用本地视频，请先上传至素材库或对象存储获取 URL。
    """
    source = source.strip()

    # 网络视频 URL：直接返回
    if source.startswith("http://") or source.startswith("https://"):
        return source

    # 素材库 ID：形如 asset://asset-20260224190654-9nbbl，直接返回
    if source.startswith("asset://"):
        return source

    # 其余情况（如本地路径）不被支持，主动报错提示
    raise ValueError(
        f"❌ 视频输入不支持该格式: {source}\n"
        f"   视频仅支持: 1) 公网 URL(http/https)  2) 素材库 ID(asset://)\n"
        f"   如需使用本地视频，请先上传至素材库或对象存储获取 URL。"
    )


# ╔═══════════════════════════════════════════════════════════════╗
# ║              📋 请求参数配置（按需调整）                         ║
# ╚═══════════════════════════════════════════════════════════════╝

headers = {
    "Content-Type": "application/json",
    "Authorization": f"{api_key}",
}

payload = {
    # 【model】(string, 必填) 调用的模型 ID
    "model": "doubao-seedance-2-0-260128",
    # 【input】(object[], 必填) 多模态输入内容数组
    "input": [
        {
            # 【type】(string, 必填) 内容类型，text 表示文本提示词
            "type": "text",
            # 【text】(string, 可选) 文本提示词，描述编辑指令
            # 支持中英文，建议中文不超过 500 字，英文不超过 1000 词
            # 可使用 [图1][图2] 等方式明确指定参考图片的用途
            "text": prompt_text,
        },
        {
            # 【type】(string, 必填) 内容类型，image_url 表示图片
            "type": "image_url",
            "image_url": {
                # 【url】(string) 图片地址，支持以下三种格式（程序自动识别）：
                #   1. 公网 URL（http:// 或 https://）
                #   2. Base64 编码（data:image/...;base64,...，由本地图片自动生成）
                #   3. 素材库 ID（形如 asset://asset-20260401123823-6d4x2）
                # 图片格式：jpeg/png/webp/bmp/tiff/gif
                # 宽高比：(0.4, 2.5)，宽高长度：(300, 6000) px，单张不超过 30 MB
                "url": resolve_image_url(image_input),
            },
            # 【role】(string, 条件必填) 图片用途
            # 可选值: "first_frame"(首帧) / "last_frame"(尾帧) / "reference_image"(参考图)
            # 多模态参考生视频场景必填，最多支持 9 张参考图
            "role": "reference_image",
        },
        {
            # 【type】(string, 必填) 内容类型，video_url 表示视频
            "type": "video_url",
            "video_url": {
                # 【url】(string) 视频 URL 或素材 ID（视频仅支持 URL / 素材 ID 方式，程序自动识别）：
                #   1. 公网 URL（http:// 或 https://）
                #   2. 素材库 ID（形如 asset://asset-20260224190654-9nbbl）
                # 视频格式：mp4/mov，分辨率：480p/720p/1080p
                # 时长：[2, 15] s，最多传入 3 个参考视频，总时长不超过 15s
                # 单个视频不超过 50 MB，帧率：[24, 60] FPS
                # ⚠️ 建议：传入视频的秒数最好是 15s
                "url": resolve_video_url(video_url),
            },
            # 【role】(string, 条件必填) 视频用途
            # 可选值: "reference_video"(参考视频)
            "role": "reference_video",
        },
    ],
    # 【generate_audio】(boolean, 可选) 是否生成同步音频
    # true: 生成包含人声、音效和背景音乐的有声视频（建议将对话置于双引号内）
    # false: 生成无声视频
    # 默认值: true
    "generate_audio": True,
    # 【ratio】(string, 可选) 视频宽高比
    # 可选值: "16:9" / "4:3" / "1:1" / "3:4" / "9:16" / "21:9" / "adaptive"(根据输入自动选择)
    # Seedance 2.0 默认值: adaptive
    "ratio": "16:9",
    # 【duration】(integer, 可选) 视频时长（秒）
    # Seedance 2.0 & 2.0 fast 取值范围: [8, 15]
    # 输出视频的秒数必须大于等于8s
    # 默认值: 8
    "duration": 8,
    # 【watermark】(boolean, 可选) 是否添加水印
    # false: 不含水印 / true: 含水印
    # 默认值: false
    "watermark": True,
    # 【resolution】(string, 可选) 视频分辨率
    # 可选值: "480p" / "720p"/ "1080p"
    # 默认值: 720p
    "resolution": "480p",
    # 【seed】(integer, 可选) 随机种子，控制生成内容的随机性
    # 取值范围: [-1, 2^32-1]，-1 表示使用随机数
    # 相同 seed 值生成类似结果，但不保证完全一致
    # 默认值: -1
    "seed": -1,
    # 【callback_url】(string, 可选) 任务状态变更回调地址
    # 任务状态包括: queued(排队中) / running(运行中) / succeeded(成功) / failed(失败) / expired(超时)
    # 失败时回调最多重试 3 次（5 秒超时）
    "callback_url": "https://www.dmxapi.cn",
    # 【return_last_frame】(boolean, 可选) 是否返回生成视频的尾帧图像（png 格式，无水印）
    # 可用于生成多段连续视频：以上一段视频的尾帧作为下一段的首帧
    # 默认值: false
    "return_last_frame": False,
    # 【execution_expires_after】(integer, 可选) 任务超时时间（秒）
    # 取值范围: [3600, 259200]，从任务创建时间开始计算，超时后任务自动终止并标记为 expired
    # 默认值: 172800（48 小时）
    "execution_expires_after": 172800,
    # 【tools】(object[], 可选) 工具配置，仅 Seedance 2.0 & 2.0 fast 支持
    # web_search: 联网搜索工具，可提升视频时效性，但会增加一定时延
    "tools": [{"type": "web_search"}],
}


# ╔═══════════════════════════════════════════════════════════════╗
# ║              📤 发送请求（无需修改）                             ║
# ╚═══════════════════════════════════════════════════════════════╝

response = requests.post("https://www.dmxapi.cn/v1/responses", headers=headers, json=payload)
print(json.dumps(response.json(), indent=2, ensure_ascii=False))
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
    "input": "cgt-20260402221419-2kcc7"
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
  "request_id": "cgt-20260403171827-s64n7",
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
