# doubao-seedance-2-0-fast-260128 文生视频 API 使用文档

doubao-seedance-2-0-fast-260128 是字节跳动 Seedance 2.0 Fast 系列的多模态视频生成模型，支持文本、图片、视频、音频的灵活组合输入（共 8 种组合方式），能够生成 480p/720p 分辨率、16:9/adaptive 等多种宽高比的短视频，时长范围 4–15 秒（支持 -1 智能选择）。模型原生支持生成与画面同步的音频（人声、音效、背景音乐），并支持 web_search 工具增强内容准确性。视频生成采用两步异步模式：先提交任务获得任务 ID，再通过 seedance-2-0-get 查询并拉取视频链接，生成结果保存 7 天。

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

# 步骤1: 配置 API 连接信息

# DMXAPI 服务端点地址
url = "https://www.dmxapi.cn/v1/responses"

# DMXAPI 密钥 (请替换为您自己的密钥)
# 获取方式: 登录 DMXAPI 官网 -> 个人中心 -> API 密钥管理
api_key = "sk-******************************************"

# 步骤2: 配置请求头

headers = {
    "Content-Type": "application/json",      # 指定请求体为 JSON 格式
    "Authorization": f"{api_key}",           # token 认证方式
}

# 步骤3: 配置请求参数

payload = {
    # 【model】(string, 必填) 您需要调用的模型的 ID（Model ID）
    # 开通模型服务后可查询 Model ID
    "model": "doubao-seedance-2-0-fast-260128",

    # 【input】(array, 必填) 输入给模型，生成视频的信息
    # 支持文本、图片、视频、音频的组合输入，共 8 种组合方式：
    # 文本 / 文本+图片 / 文本+视频 / 文本+图片+音频 / 文本+图片+视频 / 文本+视频+音频 / 文本+图片+视频+音频
    # 注意：不可单独输入音频，应至少包含 1 个参考视频或图片
    # 注意：seedance 2.0 系列模型不支持直接上传含有真人脸的参考图/视频
    "input": [
        {
            # 文本信息，type 为 "text"，提供生成视频的提示词
            "type": "text",
            "text": "全程使用视频1的第一视角构图，全程使用音频1作为背景音乐。第一人称视角果茶宣传广告，seedance牌「苹苹安安」苹果果茶限定款；首帧为图片1，你的手摘下一颗带晨露的阿克苏红苹果，轻脆的苹果碰撞声；2-4 秒：快速切镜，你的手将苹果块投入雪克杯，加入冰块与茶底，用力摇晃，冰块碰撞声与摇晃声卡点轻快鼓点，背景音：「鲜切现摇」；4-6 秒：第一人称成品特写，分层果茶倒入透明杯，你的手轻挤奶盖在顶部铺展，在杯身贴上粉红包标，镜头拉近看奶盖与果茶的分层纹理；6-8 秒：第一人称手持举杯，你将图片2中的果茶举到镜头前（模拟递到观众面前的视角），杯身标签清晰可见，背景音「来一口鲜爽」，尾帧定格为图片2。背景声音统一为女生音色。"
        },
        {
            # 图片参考信息，type 为 "image_url"，role 为 "reference_image"
            # 仅 seedance 2.0 & 2.0 fast 支持输入图片
            "type": "image_url",
            "image_url": {
                "url": "https://ark-project.tos-cn-beijing.volces.com/doc_image/r2v_tea_pic1.jpg"
            },
            "role": "reference_image"
        },
        {
            "type": "image_url",
            "image_url": {
                "url": "https://ark-project.tos-cn-beijing.volces.com/doc_image/r2v_tea_pic2.jpg"
            },
            "role": "reference_image"
        },
        {
            # 视频参考信息，type 为 "video_url"，role 为 "reference_video"
            # 仅 seedance 2.0 & 2.0 fast 支持输入视频
            "type": "video_url",
            "video_url": {
                "url": "https://ark-project.tos-cn-beijing.volces.com/doc_video/r2v_tea_video1.mp4"
            },
            "role": "reference_video"
        },
        {
            # 音频参考信息，type 为 "audio_url"，role 为 "reference_audio"
            # 仅 seedance 2.0 & 2.0 fast 支持输入音频
            # 注意：不可单独输入音频，应至少包含 1 个参考视频或图片
            "type": "audio_url",
            "audio_url": {
                "url": "https://ark-project.tos-cn-beijing.volces.com/doc_audio/r2v_tea_audio1.mp3"
            },
            "role": "reference_audio"
        },
    ],

    # 【generate_audio】(boolean, 可选) 控制生成的视频是否包含与画面同步的声音，默认值 true
    # 仅 seedance 2.0 & 2.0 fast、seedance 1.5 pro 支持
    # true: 模型输出的视频包含同步音频，自动生成与画面匹配的人声、音效及背景音乐
    # false: 模型输出的视频为无声视频（生成输出的视频均为单声道，和传入的音频声道数无关）
    "generate_audio": True,

    # 【resolution】(string, 可选) 视频分辨率，seedance 2.0 & 2.0 fast 默认值 720p
    # 可选值: "480p" / "720p" / "1080p"（seedance 2.0 fast 不支持 1080p）
    "resolution": "720p",

    # 【ratio】(string, 可选) 生成视频的宽高比，seedance 2.0 & 2.0 fast 默认值 adaptive
    # 可选值: "16:9" / "4:3" / "1:1" / "3:4" / "9:16" / "21:9" / "adaptive"
    # adaptive: 根据输入自动选择最合适的宽高比（seedance 2.0 & 2.0 fast 支持）
    "ratio": "16:9",

    # 【duration】(integer, 可选) 生成视频时长，仅支持整数，单位：秒，默认值 5
    # seedance 2.0 & 2.0 fast 取值范围: [4, 15] 或设置为 -1（由模型自主选择合适时长）
    # duration 和 frames 二选一，frames 的优先级高于 duration
    # 注意：视频时长与计费相关，请谨慎设置
    "duration": 5,

    # 【seed】(integer, 可选) 种子整数，用于控制生成内容的随机性，默认值 -1
    # 取值范围: [-1, 2^32-1]
    # -1: 使用随机数替代，每次生成结果不同
    # 相同 seed 值: 会生成类似的结果，但不保证完全一致
    "seed": -1,

    # 【watermark】(boolean, 可选) 生成视频是否包含水印，默认值 false
    # false: 不含水印 / true: 含有水印
    "watermark": False,

    # 【callback_url】(string, 可选) 任务结果的回调通知地址
    # 当视频生成任务有状态变化时，方舟将向此地址推送 POST 请求
    # 回调状态枚举: queued（排队中）/ running（运行中）/ succeeded（成功）/ failed（失败）/ expired（任务超时）
    "callback_url": "https://www.dmxapi.cn",

    # 【return_last_frame】(boolean, 可选) 是否返回生成视频的尾帧图像，默认值 false
    # true: 返回尾帧图像（PNG 格式，宽高像素值与生成视频保持一致，无水印），可通过查询任务接口获取
    # false: 不返回生成视频的尾帧图像
    "return_last_frame": False,

    # 【execution_expires_after】(integer, 可选) 任务超时阈值，单位：秒，默认值 172800（48 小时）
    # 从 created_at 时间戳开始计算，超时后任务被自动停止并标记为 expired 状态
    # 取值范围: [3600, 259200]
    # 建议根据业务场景设置合适的超时时间
    "execution_expires_after": 172800,

    # 【tools】(array, 可选) 配置模型要调用的工具，仅 seedance 2.0 & 2.0 fast 支持
    # type 为 "web_search" 时表示启用网络搜索功能，辅助模型获取更准确的内容信息
    "tools": [{"type": "web_search"}]
}

# 步骤4: 发送请求并输出结果

# 发送 POST 请求到 API 服务器
response = requests.post(url, headers=headers, json=payload)

# 格式化输出 JSON 响应
# indent=2: 缩进 2 空格，便于阅读
# ensure_ascii=False: 正确显示中文字符
print(json.dumps(response.json(), indent=2, ensure_ascii=False))
```

### 返回示例

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
    "Authorization": f"Bearer {api_key}",
}

payload = {
    # 【model】(string, 必填) 查询视频生成任务结果的固定模型 ID
    "model": "seedance-2-0-get",

    # 【input】(string, 必填) 提交任务时返回的任务 ID（id 字段）
    # 任务 ID 格式如: cgt-20260428165939-ccb9g
    "input": "cgt-20260428165939-ccb9g"
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

### 返回示例

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

> 当 `status` 为 `succeeded` 时，从 `text` 字段中解析 JSON 可获取 `content.video_url`，即生成视频的下载链接。若任务尚未完成，可稍后重试查询。任务状态枚举：`queued`（排队中）/ `running`（运行中）/ `succeeded`（成功）/ `failed`（失败）/ `expired`（已超时）。

<p align="center">
  <small>© 2026 DMXAPI doubao-seedance-2-0-fast-260128 文生视频</small>
</p>
