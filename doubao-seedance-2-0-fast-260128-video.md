# doubao-seedance-2-0-fast-260128 多模态参考生视频 API 使用文档

doubao-seedance-2-0-fast-260128 是字节跳动 Seedance 2.0 Fast 系列的多模态视频生成模型，支持文本、图片、视频、音频的灵活组合输入（共 8 种组合方式），能够生成 480p/720p 分辨率、16:9/adaptive 等多种宽高比的短视频，时长范围 4–15 秒（支持 -1 智能选择）。模型原生支持生成与画面同步的音频（人声、音效、背景音乐），并支持 web_search 工具增强内容准确性。视频生成采用两步异步模式：先提交任务获得任务 ID，再通过 seedance-2-0-get 查询并拉取视频链接

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

## 多模态参考生视频 示例代码

```python
import requests
import json
import base64
import mimetypes
import os

# ==============================================================================
# ┌─────────────────────────────────────────────────────────────────────────┐
# │                     用户配置区（需要修改的内容放这里）                     │
# └─────────────────────────────────────────────────────────────────────────┘
# ==============================================================================

# ------------------------------------------------------------------------------
# 步骤1: 配置 API 连接信息
# ------------------------------------------------------------------------------

# DMXAPI 服务端点地址
url = "https://www.dmxapi.cn/v1/responses"

# DMXAPI 密钥 (请替换为您自己的密钥)
# 获取方式: 登录 DMXAPI 官网 -> 个人中心 -> API 密钥管理
api_key = "sk-************************************"


# ------------------------------------------------------------------------------
# 步骤2: 配置素材输入（图片 / 视频 / 音频）
#
# 不需要的素材可设为 None 或将列表留空。
# 注意：不可单独输入音频，应至少包含 1 个参考视频或图片
# 注意：seedance 2.0 系列模型不支持直接上传含有真人脸的参考图/视频
# ------------------------------------------------------------------------------

# 参考图片（可填多张，按顺序对应提示词中的 图片1 / 图片2 ...）
# 仅 seedance 2.0 & 2.0 fast 支持输入图片
# 图片支持三种来源，程序会自动识别：
#   1. 网络 URL      ：以 http:// 或 https:// 开头，例如 "https://xxx/a.jpg"
#   2. 素材 ID       ：以 asset:// 开头，例如 "asset://xxxxxxxx"
#   3. 本地文件路径  ：本地磁盘路径，例如 "C:/imgs/a.jpg"（自动转 base64 上传）
image_inputs = [
    "https://ark-project.tos-cn-beijing.volces.com/doc_image/r2v_tea_pic1.jpg",
    "https://ark-project.tos-cn-beijing.volces.com/doc_image/r2v_tea_pic2.jpg",
    # "asset://your_image_asset_id",   # 素材 ID 示例
    # "./local_image.jpg",             # 本地文件示例
]

# 参考视频（可填多个）
# 仅 seedance 2.0 & 2.0 fast 支持输入视频
# 视频仅支持两种来源（不支持本地文件 base64 上传）：
#   1. 网络 URL      ：以 http:// 或 https:// 开头，例如 "https://xxx/a.mp4"
#   2. 素材 ID       ：以 asset:// 开头，例如 "asset://xxxxxxxx"
# ⚠️ 建议：传入视频的总秒数最好是 15s
video_inputs = [
    "https://ark-project.tos-cn-beijing.volces.com/doc_video/r2v_tea_video1.mp4",
    # "asset://your_video_asset_id",   # 素材 ID 示例
]

# 参考音频（可填多个）
# 仅 seedance 2.0 & 2.0 fast 支持输入音频
# 注意：不可单独输入音频，应至少包含 1 个参考视频或图片
# 音频支持三种来源，程序会自动识别：
#   1. 网络 URL      ：以 http:// 或 https:// 开头，例如 "https://xxx/a.mp3"
#   2. 素材 ID       ：以 asset:// 开头，例如 "asset://xxxxxxxx"
#   3. 本地文件路径  ：本地磁盘路径，例如 "C:/audio/a.mp3"（自动转 base64 上传）
audio_inputs = [
    "https://ark-project.tos-cn-beijing.volces.com/doc_audio/r2v_tea_audio1.mp3",
    # "asset://your_audio_asset_id",   # 素材 ID 示例
    # "./local_audio.mp3",             # 本地文件示例
]


# ------------------------------------------------------------------------------
# 步骤3: 配置文本提示词与生成参数
# ------------------------------------------------------------------------------

# 生成视频的提示词（文本信息）
prompt_text = "全程使用视频1的第一视角构图，全程使用音频1作为背景音乐。第一人称视角果茶宣传广告，seedance牌「苹苹安安」苹果果茶限定款；首帧为图片1，你的手摘下一颗带晨露的阿克苏红苹果，轻脆的苹果碰撞声；2-4 秒：快速切镜，你的手将苹果块投入雪克杯，加入冰块与茶底，用力摇晃，冰块碰撞声与摇晃声卡点轻快鼓点，背景音：「鲜切现摇」；4-6 秒：第一人称成品特写，分层果茶倒入透明杯，你的手轻挤奶盖在顶部铺展，在杯身贴上粉红包标，镜头拉近看奶盖与果茶的分层纹理；6-8 秒：第一人称手持举杯，你将图片2中的果茶举到镜头前（模拟递到观众面前的视角），杯身标签清晰可见，背景音「来一口鲜爽」，尾帧定格为图片2。背景声音统一为女生音色。"

# 您需要调用的模型的 ID（Model ID）
# 开通模型服务后可查询 Model ID
model = "doubao-seedance-2-0-fast-260128"

# 其余可选生成参数（按需修改）
generate_audio = True            # 是否生成同步音频，默认 true
resolution = "720p"              # 视频分辨率: "480p" / "720p" / "1080p"（2.0 fast 不支持 1080p）
ratio = "16:9"                   # 宽高比: "16:9"/"4:3"/"1:1"/"3:4"/"9:16"/"21:9"/"adaptive"
duration = 8                     # 视频时长（秒），范围 [8,15]；输出视频的秒数必须大于等于8s
seed = -1                        # 随机种子，-1 为随机
watermark = False                # 是否含水印
callback_url = "https://www.dmxapi.cn"  # 任务结果回调通知地址
return_last_frame = False        # 是否返回尾帧图像
execution_expires_after = 172800  # 任务超时阈值（秒），范围 [3600, 259200]
enable_web_search = True          # 是否启用网络搜索工具（仅 2.0 & 2.0 fast 支持）


# ==============================================================================
# ┌─────────────────────────────────────────────────────────────────────────┐
# │                以下为内部逻辑（一般无需修改）                              │
# └─────────────────────────────────────────────────────────────────────────┘
# ==============================================================================

# ------------------------------------------------------------------------------
# 工具函数: 将素材来源转换为可提交的 url 字符串（图片 / 音频用）
#   - http/https URL : 原样返回
#   - asset:// 素材ID : 原样返回（服务端按素材 ID 解析）
#   - 本地文件路径    : 读取文件并编码为 base64 data URI
# ------------------------------------------------------------------------------
def resolve_source(src):
    if src is None:
        return None

    src = str(src).strip()
    if not src:
        return None

    # 网络 URL 或素材 ID，直接返回
    if src.startswith(("http://", "https://", "asset://")):
        return src

    # 本地文件路径：读取并转 base64 data URI
    if not os.path.isfile(src):
        raise FileNotFoundError(f"本地文件不存在: {src}")

    # 推断 MIME 类型，推断失败时使用通用二进制类型
    mime_type, _ = mimetypes.guess_type(src)
    if mime_type is None:
        mime_type = "application/octet-stream"

    with open(src, "rb") as f:
        encoded = base64.b64encode(f.read()).decode("utf-8")

    return f"data:{mime_type};base64,{encoded}"


# ------------------------------------------------------------------------------
# 工具函数: 仅处理视频来源（不支持本地文件，只允许 URL 或 asset:// 素材 ID）
# ------------------------------------------------------------------------------
def resolve_video_source(src):
    if src is None:
        return None

    src = str(src).strip()
    if not src:
        return None

    # 视频仅支持 URL 或 asset:// 素材 ID
    if src.startswith(("http://", "https://", "asset://")):
        return src

    # 其他来源（如本地文件路径）一律拒绝
    raise ValueError(f"视频仅支持 URL 或 asset:// 素材 ID，不支持本地文件: {src}")


# ------------------------------------------------------------------------------
# 组装 input 列表（文本 + 图片 + 视频 + 音频）
# 支持文本、图片、视频、音频的组合输入，共 8 种组合方式：
# 文本 / 文本+图片 / 文本+视频 / 文本+图片+音频 / 文本+图片+视频 / 文本+视频+音频 / 文本+图片+视频+音频
# ------------------------------------------------------------------------------
input_items = []

# 文本信息，type 为 "text"，提供生成视频的提示词
input_items.append({
    "type": "text",
    "text": prompt_text
})

# 图片参考信息，type 为 "image_url"，role 为 "reference_image"
# 仅 seedance 2.0 & 2.0 fast 支持输入图片
for img in (image_inputs or []):
    resolved = resolve_source(img)
    if resolved:
        input_items.append({
            "type": "image_url",
            "image_url": {"url": resolved},
            "role": "reference_image"
        })

# 视频参考信息，type 为 "video_url"，role 为 "reference_video"
# 仅 seedance 2.0 & 2.0 fast 支持输入视频
# 视频仅支持 URL 或 asset:// 素材 ID
for vid in (video_inputs or []):
    resolved = resolve_video_source(vid)
    if resolved:
        input_items.append({
            "type": "video_url",
            "video_url": {"url": resolved},
            "role": "reference_video"
        })

# 音频参考信息，type 为 "audio_url"，role 为 "reference_audio"
# 仅 seedance 2.0 & 2.0 fast 支持输入音频
# 注意：不可单独输入音频，应至少包含 1 个参考视频或图片
for aud in (audio_inputs or []):
    resolved = resolve_source(aud)
    if resolved:
        input_items.append({
            "type": "audio_url",
            "audio_url": {"url": resolved},
            "role": "reference_audio"
        })


# ------------------------------------------------------------------------------
# 步骤: 配置请求头
# ------------------------------------------------------------------------------
headers = {
    "Content-Type": "application/json",      # 指定请求体为 JSON 格式
    "Authorization": f"Bearer {api_key}",           # token 认证方式
}


# ------------------------------------------------------------------------------
# 步骤: 配置请求参数
# ------------------------------------------------------------------------------
payload = {
    # 【model】(string, 必填) 您需要调用的模型的 ID（Model ID）
    # 开通模型服务后可查询 Model ID
    "model": model,

    # 【input】(array, 必填) 输入给模型，生成视频的信息
    # 支持文本、图片、视频、音频的组合输入
    "input": input_items,

    # 【generate_audio】(boolean, 可选) 控制生成的视频是否包含与画面同步的声音，默认值 true
    # 仅 seedance 2.0 & 2.0 fast、seedance 1.5 pro 支持
    # true: 模型输出的视频包含同步音频，自动生成与画面匹配的人声、音效及背景音乐
    # false: 模型输出的视频为无声视频（生成输出的视频均为单声道，和传入的音频声道数无关）
    "generate_audio": generate_audio,

    # 【resolution】(string, 可选) 视频分辨率，seedance 2.0 & 2.0 fast 默认值 720p
    # 可选值: "480p" / "720p" / "1080p"（seedance 2.0 fast 不支持 1080p）
    "resolution": resolution,

    # 【ratio】(string, 可选) 生成视频的宽高比，seedance 2.0 & 2.0 fast 默认值 adaptive
    # 可选值: "16:9" / "4:3" / "1:1" / "3:4" / "9:16" / "21:9" / "adaptive"
    # adaptive: 根据输入自动选择最合适的宽高比（seedance 2.0 & 2.0 fast 支持）
    "ratio": ratio,

    # 【duration】(integer, 可选) 生成视频时长，仅支持整数，单位：秒，默认值 8
    # seedance 2.0 & 2.0 fast 取值范围: [8, 15]
    # 输出视频的秒数必须大于等于8s
    # duration 和 frames 二选一，frames 的优先级高于 duration
    # 注意：视频时长与计费相关，请谨慎设置
    "duration": duration,

    # 【seed】(integer, 可选) 种子整数，用于控制生成内容的随机性，默认值 -1
    # 取值范围: [-1, 2^32-1]
    # -1: 使用随机数替代，每次生成结果不同
    # 相同 seed 值: 会生成类似的结果，但不保证完全一致
    "seed": seed,

    # 【watermark】(boolean, 可选) 生成视频是否包含水印，默认值 false
    # false: 不含水印 / true: 含有水印
    "watermark": watermark,

    # 【callback_url】(string, 可选) 任务结果的回调通知地址
    # 当视频生成任务有状态变化时，方舟将向此地址推送 POST 请求
    # 回调状态枚举: queued（排队中）/ running（运行中）/ succeeded（成功）/ failed（失败）/ expired（任务超时）
    "callback_url": callback_url,

    # 【return_last_frame】(boolean, 可选) 是否返回生成视频的尾帧图像，默认值 false
    # true: 返回尾帧图像（PNG 格式，宽高像素值与生成视频保持一致，无水印），可通过查询任务接口获取
    # false: 不返回生成视频的尾帧图像
    "return_last_frame": return_last_frame,

    # 【execution_expires_after】(integer, 可选) 任务超时阈值，单位：秒，默认值 172800（48 小时）
    # 从 created_at 时间戳开始计算，超时后任务被自动停止并标记为 expired 状态
    # 取值范围: [3600, 259200]
    # 建议根据业务场景设置合适的超时时间
    "execution_expires_after": execution_expires_after,

    # 【tools】(array, 可选) 配置模型要调用的工具，仅 seedance 2.0 & 2.0 fast 支持
    # type 为 "web_search" 时表示启用网络搜索功能，辅助模型获取更准确的内容信息
    "tools": [{"type": "web_search"}] if enable_web_search else []
}


# ------------------------------------------------------------------------------
# 步骤: 发送请求并输出结果
# ------------------------------------------------------------------------------

# 发送 POST 请求到 API 服务器
response = requests.post(url, headers=headers, json=payload)

# 格式化输出 JSON 响应
# indent=2: 缩进 2 空格，便于阅读
# ensure_ascii=False: 正确显示中文字符
print(json.dumps(response.json(), indent=2, ensure_ascii=False))
```

## 返回示例

```json
{
  "id": "cgt-20260402203437-bfb5r",
  "usage": {
    "total_tokens": 60850,
    "input_tokens": 0,
    "input_tokens_details": {
      "cached_tokens": 0
    },
    "output_tokens": 60850,
    "output_tokens_details": {
      "reasoning_tokens": 0
    }
  }
}
```

> 返回的 `id` 字段为视频生成任务 ID，保存期限为 7 天（从 `created_at` 时间戳开始计算），超时后将自动消除。请将此 ID 用于下一步查询视频结果。

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
  <small>© 2026 DMXAPI doubao-seedance-2-0-fast-260128 文生视频</small>
</p>
