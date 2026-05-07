# doubao-seedance-2-0-fast-260128 视频延长 API 使用文档

doubao-seedance-2-0-fast-260128 是字节跳动 Seedance 系列的快速版视频生成模型，支持**多模态参考生视频**——最多输入 9 张参考图、3 段参考视频、3 段参考音频与文本提示词的组合，可实现视频延长、多片段拼接与场景衔接等创作场景。在视频延长场景下，通过文本提示词描述各参考视频的衔接逻辑，模型可在多段参考视频之间自动生成过渡内容，生成时长支持 4–15 秒（或由模型自主选择），可选择是否生成与画面同步的音频。接口采用**异步两步模式**：先提交生成任务获取任务 ID，再凭任务 ID 调用查询接口获取生成视频的下载链接。

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

## 请求参数

| 参数名 | 类型 | 必填 | 默认值 | 说明 |
|--------|------|------|--------|------|
| `model` | string | 是 | — | 模型 ID，视频延长固定为 `doubao-seedance-2-0-fast-260128` |
| `input` | array | 是 | — | 输入内容列表，支持文本、视频、图片、音频的组合；延长场景传入文本提示词 + 1~3 个参考视频 |
| `input[].type` | string | 是 | — | 内容类型：`text` / `video_url` / `image_url` / `audio_url` / `draft_task` |
| `input[].text` | string | 条件 | — | 文本提示词，中文不超过 500 字，英文不超过 1000 词 |
| `input[].video_url.url` | string | 条件 | — | 视频公网 URL 或素材 ID；mp4/mov 格式，时长 [2,15] s，单文件不超过 50 MB |
| `input[].role` | string | 条件 | — | 内容用途；视频场景固定为 `reference_video`（最多 3 个，总时长 ≤ 15 s） |
| `generate_audio` | boolean | 否 | `true` | 是否生成同步音频；`true` 自动生成人声/音效/背景音乐（单声道），`false` 输出无声视频 |
| `ratio` | string | 否 | `adaptive` | 视频宽高比；可选 `16:9` / `4:3` / `1:1` / `3:4` / `9:16` / `21:9` / `adaptive`（根据输入自动选择） |
| `duration` | integer | 否 | `5` | 视频时长（秒）；seedance 2.0 fast 支持 [4, 15] 或 `-1`（模型自主选择）；与计费相关，请谨慎设置 |
| `watermark` | boolean | 否 | `false` | 是否在视频中添加水印；`true` 含水印，`false` 不含水印 |
| `resolution` | string | 否 | `720p` | 视频分辨率；可选 `480p` / `720p`（seedance 2.0 fast 不支持 `1080p`） |
| `seed` | integer | 否 | `-1` | 随机种子，取值范围 [-1, 2³²-1]；-1 使用随机数，相同 seed 可生成类似结果但不保证完全一致 |
| `callback_url` | string | 否 | — | 任务状态变化时的回调通知地址，方舟向此地址推送 POST 请求（含 queued/running/succeeded/failed/expired 状态） |
| `return_last_frame` | boolean | 否 | `false` | 是否返回生成视频的尾帧图像（png 格式，无水印）；设为 `true` 可实现连续视频生成 |
| `execution_expires_after` | integer | 否 | `172800` | 任务超时阈值（秒），取值范围 [3600, 259200]；超时后自动终止并标记为 `expired` |
| `tools` | array | 否 | — | 工具配置，仅 seedance 2.0 & 2.0 fast 支持；`type="web_search"` 开启联网搜索 |

## 视频延长 示例代码

```python
import requests
import json

# ═══════════════════════════════════════════════════════════════
# 步骤1: 配置 API 连接信息
# ═══════════════════════════════════════════════════════════════

# DMXAPI 服务端点地址
url = "https://www.dmxapi.cn/v1/responses"

# DMXAPI 密钥 (请替换为您自己的密钥)
# 获取方式: 登录 DMXAPI 官网 -> 个人中心 -> API 密钥管理
api_key = "sk-******************************************"

# ═══════════════════════════════════════════════════════════════
# 步骤2: 配置请求头
# ═══════════════════════════════════════════════════════════════

headers = {
    "Content-Type": "application/json",      # 指定请求体为 JSON 格式
    "Authorization": f"{api_key}",           # token 认证方式
}

# ═══════════════════════════════════════════════════════════════
# 步骤3: 配置请求参数
# ═══════════════════════════════════════════════════════════════

payload = {
    # 【model】(string, 必填) 模型 ID
    # 指定用于视频延长的 doubao-seedance-2-0-fast-260128 模型
    "model": "doubao-seedance-2-0-fast-260128",

    # 【input】(array, 必填) 输入内容列表，支持文本、视频、图片、音频的组合
    # 视频延长场景: 传入文本提示词 + 1~3 个参考视频 (role 为 reference_video)
    "input": [
        {
            # 【input[].type】(string) 内容类型，此处为文本提示词
            # 可选值: "text" / "video_url" / "image_url" / "audio_url" / "draft_task"
            "type": "text",
            # 【input[].text】(string) 描述各参考视频的衔接方式和镜头逻辑
            # 中文提示词不超过 500 字，英文不超过 1000 词
            "text": "视频1中的拱形窗户打开，进入美术馆室内，接视频2，之后镜头进入画内，接视频3"
        },
        {
            # 【input[].type】(string) 内容类型，此处为视频 URL
            "type": "video_url",
            "video_url": {
                # 【input[].video_url.url】(string) 视频公网 URL 或素材 ID
                # 单个视频要求: mp4/mov 格式，时长 [2,15] s，大小不超过 50 MB，分辨率 480p/720p/1080p
                "url": "https://ark-project.tos-cn-beijing.volces.com/doc_video/r2v_extend_video1.mp4"
            },
            # 【input[].role】(string, 条件必填) 视频用途
            # 视频场景仅支持 "reference_video" (参考视频，最多 3 个，所有视频总时长不超过 15 s)
            "role": "reference_video"
        },
        {
            "type": "video_url",
            "video_url": {
                "url": "https://ark-project.tos-cn-beijing.volces.com/doc_video/r2v_extend_video2.mp4"
            },
            "role": "reference_video"
        },
        {
            "type": "video_url",
            "video_url": {
                "url": "https://ark-project.tos-cn-beijing.volces.com/doc_video/r2v_extend_video3.mp4"
            },
            "role": "reference_video"
        },
    ],

    # 【generate_audio】(boolean, 可选) 是否生成与画面同步的音频，默认值 true
    # true: 模型自动生成人声、音效、背景音乐 (单声道)
    # false: 输出无声视频
    "generate_audio": True,

    # 【ratio】(string, 可选) 视频宽高比，seedance 2.0 & 2.0 fast 默认值 adaptive
    # 可选值: "16:9" / "4:3" / "1:1" / "3:4" / "9:16" / "21:9" / "adaptive" (根据输入自动选择)
    "ratio": "16:9",

    # 【duration】(integer, 可选) 生成视频时长，单位秒，默认值 5
    # seedance 2.0 & 2.0 fast 支持: [4, 15] 内的整数，或 -1 (由模型自动选择)
    # 注意: 视频时长影响计费，请谨慎设置
    "duration": 8,

    # 【watermark】(boolean, 可选) 是否在视频中添加水印，默认值 false
    # true: 含水印  /  false: 不含水印
    "watermark": True,

    # 【resolution】(string, 可选) 视频分辨率，默认值 720p
    # 可选值: "480p" / "720p" (seedance 2.0 fast 不支持 "1080p")
    "resolution": "720p",

    # 【seed】(integer, 可选) 随机种子，用于控制生成内容的随机性，默认值 -1
    # 取值范围: [-1, 2^32-1]；-1 表示使用随机数，相同 seed 可生成类似结果但不保证完全一致
    "seed": -1,

    # 【callback_url】(string, 可选) 任务状态变化时的回调通知地址
    # 任务进入 queued/running/succeeded/failed/expired 状态时，方舟向此地址发送 POST 请求
    "callback_url": "https://www.dmxapi.cn",

    # 【return_last_frame】(boolean, 可选) 是否返回生成视频的尾帧图像，默认值 false
    # true: 可通过查询接口获取 png 格式尾帧 (无水印，宽高与视频一致)，可用于实现连续视频生成
    # false: 不返回尾帧
    "return_last_frame": False,

    # 【execution_expires_after】(integer, 可选) 任务超时阈值，单位秒，默认值 172800 (48 小时)
    # 取值范围: [3600, 259200]；超时后任务自动终止并标记为 expired 状态
    "execution_expires_after": 172800,

    # 【tools】(array, 可选) 工具配置，仅 seedance 2.0 & 2.0 fast 支持
    # type="web_search": 开启联网搜索，模型根据提示词自主判断是否搜索互联网内容
    # 开启后会增加一定时延，实际搜索次数可通过查询接口的 usage.tool_usage.web_search 字段获取
    "tools": [{"type": "web_search"}]
}

# ═══════════════════════════════════════════════════════════════
# 步骤4: 发送请求并输出结果
# ═══════════════════════════════════════════════════════════════

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
  "id": "cgt-20260424185253-24kgq",
  "usage": {
    "total_tokens": 76480,
    "input_tokens": 0,
    "input_tokens_details": {
      "cached_tokens": 0
    },
    "output_tokens": 76480,
    "output_tokens_details": {
      "reasoning_tokens": 0
    }
  }
}
```

> 返回的 `id` 字段即为任务 ID，用于第二步查询视频生成结果。任务 ID 保存 7 天，请及时查询。

## 获取结果 示例代码

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
    # 【model】(string, 必填) 查询模型，固定为 "seedance-2-0-get"
    "model": "seedance-2-0-get",
    # 【input】(string, 必填) 提交视频延长任务时返回的任务 ID
    # 格式示例: "cgt-20260428165939-ccb9g"，任务 ID 保存 7 天
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

> **任务状态说明**：查询接口返回的 `status` 字段枚举值：`queued`（排队中）/ `running`（运行中）/ `succeeded`（成功）/ `failed`（失败）/ `expired`（已超时）。视频链接包含在 `status: "succeeded"` 的响应中。

<p align="center">
  <small>© 2026 DMXAPI doubao-seedance-2-0-fast-260128 视频延长</small>
</p>
