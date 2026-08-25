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

## 素材输入要求

| 素材类型 | 数量 | 来源 | 其他要求 |
|---------|------|------|---------|
| 图片 | 0-9 张 | 公网 URL / Base64 / `asset://<ASSET_ID>` | 格式 jpeg、png、webp、bmp、tiff、gif、heic、heif；宽高比 [0.4, 2.5]；宽高 [300, 6000] px；单张 < 30 MB |
| 视频 | 0-3 个 | 公网 URL / `asset://<ASSET_ID>`（**不支持 Base64**） | 格式 mp4、mov；单个时长 [2, 15] s 且所有视频总时长 ≤ 15 s；宽高比 [0.4, 2.5]；宽高 [300, 6000] px；总像素 [407696, 8295044]；单个 ≤ 200 MB；帧率 [24, 60] |
| 音频 | 0-3 个 | 公网 URL / Base64 / `asset://<ASSET_ID>` | — |

支持的输入组合：纯文本 / 文本+图片 / 文本+视频 / 文本+图片+音频 / 文本+图片+视频 / 文本+视频+音频 / 文本+图片+视频+音频。

:::warning
**不可单独输入音频**，应至少包含 1 个参考视频或图片。
seedance 2.0 系列模型不支持直接上传含有真人人脸的参考图 / 视频。
图生视频-首帧、图生视频-首尾帧、多模态参考生视频为 3 种互斥场景，不可混用。
:::

:::tip
多模态参考生视频可通过提示词指定某张参考图作为首帧 / 尾帧，间接实现「首尾帧 + 多模态参考」效果。若需严格保证首尾帧与指定图片一致，请改用[首尾帧生视频](./doubao-seedance-2-0-mini-260615-first-last-frame.md)。
:::

## 多模态参考生视频 示例代码

```python
import requests
import json
import base64
import mimetypes
import os

# 步骤1: 配置 API 连接信息

# DMXAPI 服务端点地址
url = "https://www.dmxapi.cn/v1/responses"

# DMXAPI 密钥 (请替换为您自己的密钥)
api_key = "sk-******************************************"

# 步骤2: 配置素材输入

# 参考图片（0-9 张，按顺序对应提示词中的 图片1 / 图片2 ...）
# 支持三种来源，程序会自动识别：网络 URL / 素材 ID（asset://）/ 本地文件路径（自动转 base64）
image_inputs = [
    "https://ark-project.tos-cn-beijing.volces.com/doc_image/r2v_tea_pic1.jpg",
    "https://ark-project.tos-cn-beijing.volces.com/doc_image/r2v_tea_pic2.jpg",
]

# 参考视频（0-3 个，所有视频总时长不超过 15 秒）
# 仅支持网络 URL 或素材 ID（asset://），不支持本地文件 base64 上传
video_inputs = [
    "https://ark-project.tos-cn-beijing.volces.com/doc_video/r2v_tea_video1.mp4",
]

# 参考音频（0-3 个）
# 注意：不可单独输入音频，应至少包含 1 个参考视频或图片
audio_inputs = [
    "https://ark-project.tos-cn-beijing.volces.com/doc_audio/r2v_tea_audio1.mp3",
]

# 生成视频的提示词
prompt_text = "全程使用视频1的第一视角构图，全程使用音频1作为背景音乐。第一人称视角果茶宣传广告；首帧为图片1，你的手摘下一颗带晨露的红苹果；2-4 秒：快速切镜，将苹果块投入雪克杯，加入冰块与茶底用力摇晃；4-6 秒：成品特写，分层果茶倒入透明杯，轻挤奶盖在顶部铺展；6-8 秒：手持举杯将果茶举到镜头前，尾帧定格为图片2。"


# 工具函数: 将图片 / 音频来源转换为可提交的 url 字符串
#   - http/https URL、asset:// 素材 ID : 原样返回
#   - 本地文件路径 : 读取文件并编码为 base64 data URI
def resolve_source(src):
    src = str(src).strip()
    if not src:
        return None
    if src.startswith(("http://", "https://", "asset://")):
        return src
    if not os.path.isfile(src):
        raise FileNotFoundError(f"本地文件不存在: {src}")
    mime_type, _ = mimetypes.guess_type(src)
    if mime_type is None:
        mime_type = "application/octet-stream"
    with open(src, "rb") as f:
        encoded = base64.b64encode(f.read()).decode("utf-8")
    return f"data:{mime_type};base64,{encoded}"


# 工具函数: 视频来源仅允许 URL 或 asset:// 素材 ID（不支持本地文件）
def resolve_video_source(src):
    src = str(src).strip()
    if not src:
        return None
    if src.startswith(("http://", "https://", "asset://")):
        return src
    raise ValueError(f"视频仅支持 URL 或 asset:// 素材 ID，不支持本地文件: {src}")


# 组装 input 列表（文本 + 图片 + 视频 + 音频）
input_items = [{"type": "text", "text": prompt_text}]

for img in (image_inputs or []):
    resolved = resolve_source(img)
    if resolved:
        input_items.append({
            "type": "image_url",
            "image_url": {"url": resolved},
            "role": "reference_image",
        })

for vid in (video_inputs or []):
    resolved = resolve_video_source(vid)
    if resolved:
        input_items.append({
            "type": "video_url",
            "video_url": {"url": resolved},
            "role": "reference_video",
        })

for aud in (audio_inputs or []):
    resolved = resolve_source(aud)
    if resolved:
        input_items.append({
            "type": "audio_url",
            "audio_url": {"url": resolved},
            "role": "reference_audio",
        })

# 步骤3: 配置请求头

headers = {
    "Content-Type": "application/json",
    "Authorization": f"{api_key}",
}

# 步骤4: 配置请求参数

payload = {
    # 【model】(string, 必填) 模型名称，指定使用 doubao-seedance-2-0-mini 模型
    "model": "doubao-seedance-2-0-mini-260615",

    # 【input】(array, 必填) 输入内容数组，支持文本、图片、视频、音频的组合输入
    # 各素材的 role 分别为 reference_image / reference_video / reference_audio
    # 提示词建议中文不超过500字，英文不超过1000词
    # 额外支持西班牙语、印度尼西亚语、葡萄牙语、日语
    "input": input_items,

    # 【ratio】(string, 可选) 视频宽高比，默认值 adaptive
    # 可选值: "16:9" / "4:3" / "1:1" / "3:4" / "9:16" / "21:9" / "adaptive"
    # "adaptive": 由模型根据提示词在可选宽高比中自动选择
    "ratio": "16:9",

    # 【resolution】(string, 可选) 视频分辨率，默认值 720p
    # 可选值: "480p" / "720p"（seedance 2.0 mini 不支持 1080p 和 4k）
    "resolution": "720p",

    # 【duration】(integer, 可选) 视频时长（秒）
    # 取值范围: [4, 15]，或 -1 由模型在有效范围内自主选择合适时长
    # 传 -1 时按 15 秒预扣费，实际时长确定后多退少补
    # 注意: 视频时长与计费相关，请谨慎设置
    "duration": 8,

    # 【generate_audio】(boolean, 可选) 是否生成同步音频（人声/音效/背景音乐），默认值 true
    # true: 模型自动生成与画面匹配的人声、音效及背景音乐
    # false: 输出无声视频
    # 注意: 生成的有声视频均为单声道，与传入音频的声道数无关
    "generate_audio": True,

    # 【seed】(integer, 可选) 随机种子，默认值 -1
    # 取值范围: [-1, 2147483647]；-1 表示使用随机数
    "seed": -1,

    # 【watermark】(boolean, 可选) 是否包含水印，默认值 false
    # true: 生成视频右下角展示「AI 生成」水印
    "watermark": False,

    # 【return_last_frame】(boolean, 可选) 是否返回视频尾帧图像，默认值 false
    # true: 返回尾帧图像（png 格式，宽高与视频一致，无水印）
    "return_last_frame": False,

    # 【execution_expires_after】(integer, 可选) 任务超时时间（秒）
    # 取值范围: [3600, 259200]，默认 172800（48小时）
    # 从 created_at 开始计算，超时后任务终止并标记为 expired
    "execution_expires_after": 172800,

    # 【callback_url】(string, 可选) 任务状态回调地址
    # 状态说明: queued(排队中) / running(运行中) / succeeded(成功) / failed(失败) / expired(超时)
    "callback_url": "https://www.dmxapi.cn",

    # 【tools】(array, 可选) 工具配置，开启联网搜索
    # web_search: 模型根据提示词自主判断是否搜索互联网内容，可提升视频时效性但增加时延
    "tools": [{"type": "web_search"}],
}

# 步骤5: 发送请求并输出结果

response = requests.post(url, headers=headers, json=payload)
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
          "text": "{\"content\":{\"video_url\":\"https://ark-acg-cn-beijing.tos-cn-beijing.volces.com/doubao-seedance-2-0-mini/02178747125300000000000000000000000ffffac1945e6f19d3.mp4?X-Tos-Algorithm=TOS4-HMAC-SHA256\\u0026X-Tos-Credential=AKLTYWJkZTExNjA1ZDUyNDc3YzhjNTM5OGIyNjBhNDcyOTQ%2F20260820%2Fcn-beijing%2Ftos%2Frequest\\u0026X-Tos-Date=20260820T062845Z\\u0026X-Tos-Expires=86400\\u0026X-Tos-Signature=d4e5f60718293a4b5c6d7e8f90a1b2c3d4e5f60718293a4b5c6d7e8f90a1b2c3\\u0026X-Tos-SignedHeaders=host\"},\"id\":\"cgt-20260820142845-tq8dz\",\"model\":\"doubao-seedance-2-0-mini-260615\",\"status\":\"succeeded\"}"
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

视频链接: https://ark-acg-cn-beijing.tos-cn-beijing.volces.com/doubao-seedance-2-0-mini/02178747125300000000000000000000000ffffac1945e6f19d3.mp4?X-Tos-Algorithm=TOS4-HMAC-SHA256&X-Tos-Credential=AKLTYWJkZTExNjA1ZDUyNDc3YzhjNTM5OGIyNjBhNDcyOTQ%2F20260820%2Fcn-beijing%2Ftos%2Frequest&X-Tos-Date=20260820T062845Z&X-Tos-Expires=86400&X-Tos-Signature=d4e5f60718293a4b5c6d7e8f90a1b2c3d4e5f60718293a4b5c6d7e8f90a1b2c3&X-Tos-SignedHeaders=host
```

<p align="center">
  <small>© 2026 DMXAPI doubao-seedance-2-0-mini-260615 多模态参考生视频</small>
</p>
