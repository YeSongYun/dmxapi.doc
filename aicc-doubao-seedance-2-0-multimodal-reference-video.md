# AICC-Doubao-Seedance-2.0 多模态参考生视频 API 使用文档

基于豆包 Seedance 2.0 模型的多模态参考生视频接口，支持同时输入参考图片（1~9 张）、参考视频（0~3 个）、参考音频（0~3 段）及文本提示词，生成高度贴合参考素材的目标视频。支持生成全新视频、编辑视频等多种创作模式，可生成最高 1080p 分辨率的有声视频。采用异步任务模式，提交后通过独立查询接口获取结果。

## 🎬 模型名称

- `AICC-Doubao-Seedance-2.0`

## 🔗 接口地址

| 接口 | 请求方式 | URL |
|------|---------|-----|
| 提交任务 | POST | `https://www.dmxapi.cn/v1/responses` |
| 获取结果 | POST | `https://www.dmxapi.cn/v1/responses` |

:::warning
请妥善保管您的 API Key！严禁将密钥泄露给他人、硬编码到代码中或提交到公开的代码仓库。如果怀疑密钥已泄露，请立即前往 DMXAPI 官网重新生成。
:::

:::tip 素材组合规则
- 参考图（role: `reference_image`）1~9 张 + 参考视频（role: `reference_video`）0~3 个 + 参考音频（role: `reference_audio`）0~3 段，文本提示词可选。
- **不可单独只传音频**：input 中至少包含 1 个参考图或参考视频。
- 视频时长：**含参考视频时 duration 必填且为 8~15 秒**；不含参考视频（纯图片 / 图片+音频）时 duration 为 4~15 秒、可省略（默认 5 秒）。
:::


## 🎥 多模态参考生视频 示例代码

```python
import requests
import json
import base64
import mimetypes

# ╔═══════════════════════════════════════════════════════════════╗
# ║              👇 以下为用户配置区，按需修改                       ║
# ╚═══════════════════════════════════════════════════════════════╝

# ══════════════════════════════════════════════════════════════
# 🔑 API 连接信息
# ═══════════════════════════════════════════════════════════════

# 🌐 DMXAPI 服务端点地址
url = "https://www.dmxapi.cn/v1/responses"

# 🔐 DMXAPI 密钥 (请替换为您自己的密钥)
# 获取方式: 登录 DMXAPI 官网 -> 个人中心 -> API 密钥管理
api_key = "sk-************************************************"

# 📋 请求头
headers = {
    "Content-Type": "application/json",
    "Authorization": f"{api_key}",           # token 认证方式，注意此处不加 Bearer 前缀
}


# ═══════════════════════════════════════════════════════════════
# 📁 素材路径（图片/音频支持 本地路径 / 公网URL / 素材ID，自动识别）
# ═══════════════════════════════════════════════════════════════

# 🖼️ 图片（支持 本地路径 / 公网URL / 素材ID asset://...）
image1_path = "https://ark-project.tos-cn-beijing.volces.com/doc_image/r2v_tea_pic2.jpg"

# 🎵 音频（支持 本地路径 / 公网URL / 素材ID asset://...）
audio1_path = "https://ark-project.tos-cn-beijing.volces.com/doc_audio/r2v_tea_audio1.mp3"

# 🎬 视频（支持 公网URL / 素材ID，不支持本地上传）
video1_url = "https://ark-project.tos-cn-beijing.volces.com/doc_video/r2v_tea_video1.mp4"


# ═══════════════════════════════════════════════════════════════
# 📝 文本提示词
# ═══════════════════════════════════════════════════════════════

prompt_text = (
    "全程使用视频1的第一视角构图，全程使用音频1作为背景音乐。"
    "第一人称视角果茶宣传广告，成品特写参考图片1，"
    "镜头缓缓拉近，杯身标签清晰可见。背景声音统一为女生音色。"
)


# ╔═══════════════════════════════════════════════════════════════╗
# ║               ⚙️ 内部工具函数（无需修改）                       ║
# ╚═══════════════════════════════════════════════════════════════╝

def is_url(path):
    """判断是否为公网 URL"""
    return path.startswith("http://") or path.startswith("https://")

def is_asset_id(path):
    """判断是否为素材 ID（格式如 asset://asset-20260721165658-m57z9）"""
    return path.startswith("asset://")

def file_to_base64_data_url(file_path, default_mime="application/octet-stream"):
    mime_type, _ = mimetypes.guess_type(file_path)
    if mime_type is None:
        mime_type = default_mime
    with open(file_path, "rb") as f:
        encoded = base64.b64encode(f.read()).decode("utf-8")
    return f"data:{mime_type};base64,{encoded}"

def resolve_resource(path, default_mime="application/octet-stream"):
    """
    智能解析资源路径：
    - 公网 URL  (http:// 或 https://) → 原样返回
    - 素材 ID   (asset://...)         → 原样返回
    - 本地文件路径                     → 转为 base64 data URL
    """
    if is_url(path):
        return path
    elif is_asset_id(path):
        return path
    else:
        return file_to_base64_data_url(path, default_mime=default_mime)

# 智能解析：本地文件自动转 base64，公网URL / 素材ID 原样使用
image1_data = resolve_resource(image1_path, default_mime="image/jpeg")
audio1_data = resolve_resource(audio1_path, default_mime="audio/mpeg")

# ╔═══════════════════════════════════════════════════════════════╗
# ║              👇 以下为请求参数配置，按需修改                      ║
# ╚═══════════════════════════════════════════════════════════════╝

# ═══════════════════════════════════════════════════════════════
# 💬 请求参数
# ═══════════════════════════════════════════════════════════════

payload = {
    # 【model】(string, 必填) 模型 ID
    "model": "AICC-Doubao-Seedance-2.0",

    # 【input】(array, 必填) 多模态输入内容数组
    # 支持文本、图片（1~9 张）、视频（0~3 个）、音频（0~3 段）
    # 注意：不可单独传入音频，必须至少包含 1 个参考图片或视频
    "input": [
        {
            # 【type】(string, 必填) 输入类型，此处为文本提示词
            "type": "text",
            # 【text】(string, 可选) 文本提示词，建议中文不超过 500 字
            # 可用 "图片1""视频1""音频1" 按素材顺序指代，
            # 建议用 "[图1]xxx，[图2]xxx" 格式显式指定多张图片的作用
            "text": prompt_text
        },
        {
            # 【type】(string, 必填) 输入类型，此处为图片
            "type": "image_url",
            "image_url": {
                # 【url】(string) 图片公网 URL、Base64 编码或素材 ID
                # 支持格式：jpeg/png/webp/bmp/tiff/gif/heic/heif
                # 宽高比范围 (0.4, 2.5)，宽高像素范围 (300, 6000)，单张小于 30 MB
                "url": image1_data
            },
            # 【role】(string, 条件必填) 图片角色，多模态参考场景固定为 reference_image
            "role": "reference_image"
        },
        {
            # 【type】(string, 必填) 输入类型，此处为视频
            "type": "video_url",
            "video_url": {
                # 【url】(string) 视频公网 URL 或素材 ID（不支持 Base64）
                # 支持格式：mp4/mov，分辨率 480p/720p，帧率 [24, 60] FPS
                # 单个视频时长 [2, 15]s，最多传入 3 个，总时长不超过 15s，大小不超过 50 MB
                "url": video1_url
            },
            # 【role】(string, 条件必填) 视频角色，多模态参考场景固定为 reference_video（参考视频）
            "role": "reference_video"
        },
        {
            # 【type】(string, 必填) 输入类型，此处为音频
            "type": "audio_url",
            "audio_url": {
                # 【url】(string) 音频公网 URL、Base64 编码或素材 ID
                # 支持格式：wav/mp3，单段时长 [2, 15]s，最多传入 3 段，总时长不超过 15s，大小不超过 15 MB
                "url": audio1_data
            },
            # 【role】(string, 条件必填) 音频角色，固定为 reference_audio（参考音频）
            "role": "reference_audio"
        },
    ],

    # 【generate_audio】(boolean, 可选) 是否生成同步音频，默认 true
    # true：模型自动生成匹配的人声、音效及背景音乐
    # false：输出无声视频
    "generate_audio": True,

    # 【resolution】(string, 可选) 视频分辨率
    # 可选值: "480p" / "720p"/ "1080p"
    # 默认值: 720p
    "resolution": "480p",

    # 【ratio】(string, 可选) 视频宽高比
    # 可选值: "16:9" / "4:3" / "1:1" / "3:4" / "9:16" / "21:9" / "adaptive"（模型自动选择）
    # 默认值: adaptive
    "ratio": "adaptive",

    # 【duration】(integer, 条件必填) 视频时长（秒）
    # 含参考视频时：必填，取值范围 [8, 15]
    # 不含参考视频时（纯图片/图片+音频）：可省略（默认 5），取值范围 [4, 15]
    "duration": 8,

    # 【seed】(integer, 可选) 随机种子，默认 -1
    # 注意：Seedance 2.0 系列暂不支持指定 seed，传入后会被上游忽略
    "seed": -1,

    # 【watermark】(boolean, 可选) 是否添加水印，默认 false
    "watermark": False,

    # 【callback_url】(string, 可选) 任务状态变更回调地址
    # 回调状态枚举: "queued" / "running" / "succeeded" / "failed" / "expired"
    "callback_url": "https://www.dmxapi.cn",

    # 【return_last_frame】(boolean, 可选) 是否返回视频尾帧图片，默认 false
    # true：返回 PNG 格式尾帧，可用于生成多个连续视频（以上一视频尾帧作为下一视频首帧）
    "return_last_frame": False,

    # 【execution_expires_after】(integer, 可选) 任务超时阈值（秒），默认 172800（48 小时）
    # 取值范围: [3600, 259200]，超时后任务自动终止并标记为 expired 状态
    "execution_expires_after": 172800,

    # 【tools】(array, 可选) 工具配置
    # "web_search"：联网搜索工具，模型自主判断是否搜索互联网内容，可提升视频时效性
    "tools": [{"type": "web_search"}]
}
# ═══════════════════════════════════════════════════════════════
# 📤 发送请求并输出结果
# ═══════════════════════════════════════════════════════════════

response = requests.post(url, headers=headers, json=payload)
print(json.dumps(response.json(), indent=2, ensure_ascii=False))
```

## 返回示例

```json
{
  "id": "cgt-20260721165804-z5qjx",
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

> 返回的 `id` 为视频生成任务 ID，保存期限为 7 天（从创建时间戳开始计算）。

## 📥 获取结果 示例代码

```python
import requests
import json

url = "https://www.dmxapi.cn/v1/responses"
api_key = "sk-*************************************"

headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {api_key}",
}

payload = {
    # 【model】(string, 必填) 获取结果专用模型标识，固定为 AICC-Doubao-Seedance-2.0-get
    "model": "AICC-Doubao-Seedance-2.0-get",
    # 【input】(string, 必填) 提交任务时返回的任务 ID（id 字段的值）
    # 任务 ID 仅保存 7 天，超时后自动清除
    "input": "cgt-2026****************nsn"
}

response = requests.post(url, headers=headers, json=payload)
result = response.json()

display_result = result
try:
    display_result = json.loads(result["output"][0]["content"][0]["text"])
except Exception:
    pass
print(json.dumps(display_result, indent=2, ensure_ascii=False))

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
  "request_id": "cgt-20260721184314-9wrsf",
  "output": [
    {
      "type": "message",
      "content": [
        {
          "type": "output_text",
          "text": "{\"content\":{\"video_url\":\"https://ark-acg-cn-beijing.tos-cn-beijing.volces.com/doubao-seedance-2-0/02178463059431000000000000000000000ffffac15e1d87c9b67.mp4?X-Tos-Algorithm=TOS4-HMAC-SHA256\\u0026X-Tos-Credential=...\\u0026X-Tos-Date=20260721T104528Z\\u0026X-Tos-Expires=86400\\u0026X-Tos-Signature=...\\u0026X-Tos-SignedHeaders=host\"},\"id\":\"cgt-20260721184314-9wrsf\",\"model\":\"doubao-seedance-2-0-260128\",\"status\":\"succeeded\"}"
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

视频链接: https://ark-acg-cn-beijing.tos-cn-beijing.volces.com/doubao-seedance-2-0/02178463059431000000000000000000000ffffac15e1d87c9b67.mp4?...（有效期 24 小时的临时下载链接）
```

> **说明**：视频链接有效期为 24 小时，请及时下载保存。若 `status` 为 `running` 或 `queued`，可稍后重新调用获取接口查询。若提交任务时设置了 `return_last_frame: true`，成功返回的 `content` 中还会包含 `last_frame_url`（尾帧图 URL，24 小时有效）。

<p align="center">
  <small>© 2026 DMXAPI AICC-Doubao-Seedance-2.0 多模态参考生视频</small>
</p>
