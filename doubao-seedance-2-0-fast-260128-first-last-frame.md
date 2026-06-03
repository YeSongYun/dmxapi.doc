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

# 步骤1: 配置 API 连接信息

# DMXAPI 服务端点地址
url = "https://www.dmxapi.cn/v1/responses"

# DMXAPI 密钥 (请替换为您自己的密钥)
api_key = "sk-******************************************"

# 步骤2: 配置请求头

headers = {
    "Content-Type": "application/json",
    "Authorization": f"{api_key}",
}

# 步骤3: 配置请求参数

payload = {
    # 【model】(string, 必填) 模型 ID
    "model": "doubao-seedance-2-0-fast-260128",

    # 【input】(array, 必填) 输入内容列表
    # 首尾帧生视频场景：文本（可选）+ 首帧图片 + 尾帧图片
    "input": [
        {
            # 【input[].type】(string, 必填) 输入类型，文本时填 "text"
            "type": "text",
            # 【input[].text】(string, 必填) 文本提示词，描述期望生成的视频内容
            # 中文提示词不超过 500 字，英文提示词不超过 1000 词
            # seedance 2.0 fast 额外支持日语、印尼语、西班牙语、葡萄牙语
            "text": "图1中小狗跳到图二小狗身上，对着镜头说\"茄子\"，360度环绕运镜"
        },
        {
            # 【input[].type】(string, 必填) 输入类型，图片时填 "image_url"
            "type": "image_url",
            "image_url": {
                # 【input[].image_url.url】(string, 必填) 图片 URL、Base64 编码或素材 ID
                # 格式：jpeg、png、webp、bmp、tiff、gif
                # 宽高比（宽/高）范围：(0.4, 2.5)；宽高像素：(300, 6000)；单张大小 < 30 MB
                "url": "https://img.shetu66.com/2023/07/14/1689320796087949.png"
            },
            # 【input[].role】(string, 条件必填) 图片位置/用途
            # 首帧图片填 "first_frame"，尾帧图片填 "last_frame"
            # 说明：传入的首尾帧图片可相同；宽高比不一致时以首帧为主，尾帧自动裁剪适配
            "role": "first_frame"
        },
        {
            "type": "image_url",
            "image_url": {
                "url": "https://img.sucaijishi.com/uploadfile/2023/0301/20230301120626930.png?imageMogr2/format/jpg/blur/1x0/quality/60"
            },
            # 尾帧图片对应的 role 为 "last_frame"
            "role": "last_frame"
        },
    ],

    # 【generate_audio】(boolean, 可选) 是否生成同步音频，默认值 true
    # true：视频包含与画面同步的人声、音效及背景音乐，对话建议置于双引号内以优化效果
    # false：输出无声视频；注意生成的有声视频均为单声道
    "generate_audio": True,

    # 【resolution】(string, 可选) 视频分辨率，默认值 "720p"
    # 可选值："480p" / "720p"（seedance 2.0 fast 不支持 "1080p"）
    "resolution": "720p",

    # 【ratio】(string, 可选) 视频宽高比，默认值 "adaptive"
    # 可选值："16:9" / "4:3" / "1:1" / "3:4" / "9:16" / "21:9" / "adaptive"
    # adaptive（首尾帧生视频）：根据首帧图片比例自动选择最接近的宽高比
    "ratio": "adaptive",

    # 【duration】(integer, 可选) 视频时长（秒），默认值 5
    # seedance 2.0 & 2.0 fast 支持取值范围 [4, 15]，或设置为 -1 由模型智能选择
    "duration": 5,

    # 【seed】(integer, 可选) 随机种子，默认值 -1
    # 取值范围：[-1, 2^32-1]；-1 表示使用随机数
    # 相同 seed 值生成类似结果，但不保证完全一致
    "seed": -1,

    # 【watermark】(boolean, 可选) 是否添加水印，默认值 false
    # false：不含水印；true：含水印
    "watermark": False,

    # 【callback_url】(string, 可选) 任务状态变化时的回调通知地址
    # 方舟向此地址推送 POST 请求，回调状态包括：
    # "queued"（排队中）/ "running"（运行中）/ "succeeded"（成功）/ "failed"（失败）/ "expired"（超时）
    "callback_url": "https://www.dmxapi.cn",

    # 【return_last_frame】(boolean, 可选) 是否返回生成视频的尾帧图像，默认值 false
    # true：可通过查询任务接口获取视频尾帧（PNG 格式，与视频同分辨率，无水印）
    # 可用于生成多段连续视频：将上一段视频的尾帧作为下一段的首帧
    "return_last_frame": False,

    # 【execution_expires_after】(integer, 可选) 任务超时阈值（秒），默认值 172800（48 小时）
    # 取值范围：[3600, 259200]；超时后任务自动终止并标记为 "expired" 状态
    "execution_expires_after": 172800,

    # 【tools】(array, 可选) 工具配置，仅 seedance 2.0 & 2.0 fast 支持
    # tools[].type：工具类型，目前支持 "web_search"（联网搜索）
    # 开启后模型根据提示词自主判断是否搜索互联网内容，可提升时效性但会增加时延
    "tools": [{"type": "web_search"}]
}

# 步骤4: 发送请求并输出结果

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
