# doubao-seedance-2-0-fast-260128 视频编辑 API 使用文档

doubao-seedance-2-0-fast-260128 是字节跳动火山引擎 Seedance 2.0 Fast 系列的多模态视频编辑模型，支持通过参考图片、参考视频与文本提示词组合驱动视频内容编辑，实现替换视频元素、风格迁移、延长视频等多种场景。模型支持 720p 分辨率输出，支持有声/无声视频生成，并可通过联网搜索工具增强时效性内容创作。接口采用两步异步模式：提交任务获取任务 ID，再通过轮询接口获取生成的视频链接。

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

## 视频编辑 示例代码

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
    # 【model】(string, 必填) 调用的模型 ID
    # 当前固定使用 doubao-seedance-2-0-fast-260128
    "model": "doubao-seedance-2-0-fast-260128",

    # 【input】(array, 必填) 输入给模型的多模态内容列表
    # 支持文本、图片、视频、音频四种类型的组合
    # 合法组合：文本；文本+图片；文本+视频；文本+图片+视频；文本+图片+音频；文本+视频+音频；文本+图片+视频+音频
    # 注意：不可单独输入音频，至少需包含 1 个参考视频或图片
    "input": [
        {
            # 【input[].type】(string) 内容类型，文本时固定为 "text"
            "type": "text",
            # 【input[].text】(string) 文本提示词，描述期望的视频编辑效果
            # 中文提示词不超过 500 字，英文不超过 1000 词
            # 可使用 [图1]、[视频1] 等方式指定对应参考素材
            "text": "将视频1礼盒中的香水替换成图片1中的面霜，运镜不变"
        },
        {
            # 【input[].type】(string) 内容类型，图片时固定为 "image_url"
            "type": "image_url",
            "image_url": {
                # 【input[].image_url.url】(string) 图片 URL、Base64 编码或素材 ID
                # 格式要求：jpeg/png/webp/bmp/tiff/gif，宽高比 (0.4, 2.5)，单张 < 30MB
                "url": "https://ark-project.tos-cn-beijing.volces.com/doc_image/r2v_edit_pic1.jpg"
            },
            # 【input[].role】(string, 条件必填) 图片的用途
            # 可选值: "first_frame"(首帧) / "last_frame"(尾帧) / "reference_image"(参考图)
            # 多模态参考生视频场景必填，每张参考图均填 "reference_image"
            "role": "reference_image"
        },
        {
            # 【input[].type】(string) 内容类型，视频时固定为 "video_url"
            "type": "video_url",
            "video_url": {
                # 【input[].video_url.url】(string) 视频 URL 或素材 ID
                # 格式：mp4/mov；分辨率：480p/720p/1080p；时长：[2, 15]s；单个 < 50MB
                # 最多传入 3 个参考视频，所有视频总时长不超过 15s
                "url": "https://ark-project.tos-cn-beijing.volces.com/doc_video/r2v_edit_video1.mp4"
            },
            # 【input[].role】(string, 条件必填) 视频用途
            # 当前仅支持 "reference_video"（参考视频）
            "role": "reference_video"
        },
    ],

    # 【generate_audio】(boolean, 可选) 是否生成与画面同步的声音，默认值 true
    # true：输出包含人声/音效/背景音乐的有声视频；false：输出无声视频
    # 注意：生成的有声视频均为单声道
    "generate_audio": True,

    # 【ratio】(string, 可选) 视频宽高比，默认值 "adaptive"
    # 可选值: "16:9" / "4:3" / "1:1" / "3:4" / "9:16" / "21:9" / "adaptive"
    # "adaptive" 表示根据输入素材或提示词自动选择最合适的宽高比
    "ratio": "16:9",

    # 【duration】(integer, 可选) 视频时长（秒），默认值 5
    # seedance 2.0 fast 取值范围：[4, 15] 或 -1（由模型自动选择合适时长）
    # 注意：视频时长与计费相关，设置 -1 时请注意可能产生较长视频的费用
    "duration": 5,

    # 【watermark】(boolean, 可选) 是否在视频中添加水印，默认值 false
    # true：含水印；false：不含水印
    "watermark": True,

    # 【resolution】(string, 可选) 视频分辨率，默认值 "720p"
    # seedance 2.0 fast 支持: "480p" / "720p"（不支持 1080p）
    "resolution": "720p",

    # 【seed】(integer, 可选) 随机种子，控制生成内容的随机性，默认值 -1
    # 取值范围：[-1, 2^32-1]
    # -1 表示使用随机数；相同 seed 值会生成类似但不保证完全一致的结果
    "seed": -1,

    # 【callback_url】(string, 可选) 任务状态变化时的回调通知地址
    # 方舟将向此地址推送 POST 请求，内容与查询任务接口返回体一致
    # 回调状态包括: queued / running / succeeded / failed / expired
    "callback_url": "https://www.dmxapi.cn",

    # 【return_last_frame】(boolean, 可选) 是否返回生成视频的尾帧图像，默认值 false
    # true：可通过查询接口获取 PNG 格式尾帧图像（无水印，分辨率与视频一致）
    # 可用于实现多段连续视频生成（以上一段尾帧作为下一段首帧）
    "return_last_frame": False,

    # 【execution_expires_after】(integer, 可选) 任务超时阈值（秒），默认值 172800
    # 取值范围：[3600, 259200]，从任务创建时间开始计算
    # 超时后任务自动终止并标记为 expired 状态
    "execution_expires_after": 172800,

    # 【tools】(array, 可选) 配置模型调用的工具，仅 seedance 2.0 & 2.0 fast 支持
    # type 可选值: "web_search"（联网搜索），开启后模型自主判断是否搜索互联网内容
    "tools": [{"type": "web_search"}]
}

# 步骤4: 发送请求并输出结果

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
  "id": "cgt-20260424185408-hxtsf",
  "usage": {
    "total_tokens": 47800,
    "input_tokens": 0,
    "input_tokens_details": {
      "cached_tokens": 0
    },
    "output_tokens": 47800,
    "output_tokens_details": {
      "reasoning_tokens": 0
    }
  }
}
```

> 返回的 `id` 字段即为视频生成任务 ID，用于第二步查询任务状态和获取视频链接。任务 ID 仅保存 7 天，超时后自动清除。

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
    # 【model】(string, 必填) 查询模型固定为 "seedance-2-0-get"
    "model": "seedance-2-0-get",
    # 【input】(string, 必填) 第一步返回的任务 ID
    # 任务状态: queued(排队中) / running(生成中) / succeeded(成功) / failed(失败) / expired(超时)
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
          "text": "{\"content\":{\"video_url\":\"https://ark-acg-cn-beijing.tos-cn-beijing.volces.com/doubao-seedance-2-0-fast/02177736688829100000000000000000000ffffac177fcdd9df5d.mp4?X-Tos-Algorithm=TOS4-HMAC-SHA256&X-Tos-Credential=...&X-Tos-Expires=86400\"},\"id\":\"cgt-20260428165939-ccb9g\",\"model\":\"doubao-seedance-2-0-fast-260128\",\"status\":\"succeeded\"}"
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
  <small>© 2026 DMXAPI doubao-seedance-2-0-fast-260128 视频编辑</small>
</p>
