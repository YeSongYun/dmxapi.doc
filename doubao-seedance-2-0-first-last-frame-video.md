# doubao-seedance-2-0-260128 首尾帧生视频 API 使用文档

基于 doubao-seedance-2-0-260128 模型的 AI 视频生成接口，支持输入首帧图片 + 尾帧图片 + 文本提示词生成目标视频。模型根据首尾两帧图像自动补全中间动态画面，支持自动音频生成，可选 480p / 720p /1080p 分辨率，宽高比支持 16:9、9:16、adaptive 等 7 种规格，视频时长范围 4~15 秒（可设为 -1 由模型自动决定）。采用异步任务模式，提交后通过单次查询获取结果视频 URL。

## 🎬 模型名称

- `doubao-seedance-2-0-260128`

## 🌐 接口地址

| 接口 | 请求方式 | URL |
|------|---------|-----|
| 提交任务 | POST | `https://www.dmxapi.cn/v1/responses` |
| 获取结果 | POST | `https://www.dmxapi.cn/v1/responses` |

:::warning
请妥善保管您的 API Key！严禁将密钥泄露给他人、硬编码到代码中或提交到公开的代码仓库。如果怀疑密钥已泄露，请立即前往 DMXAPI 官网重新生成。
:::


## 🎥 首尾帧生视频 示例代码

```python
import requests
import json

# 步骤1: 配置 API 连接信息

url = "https://www.dmxapi.cn/v1/responses"

api_key = "sk-******************************************"

# 步骤2: 配置请求头

headers = {
    "Content-Type": "application/json",
    # 【鉴权方式】使用 token 认证，直接传入 API Key
    "Authorization": f"{api_key}",
}

# 步骤3: 配置请求参数

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
                "url": "https://img.shetu66.com/2023/07/14/1689320796087949.png"
            },
            # 【role】(string, 必填) 首尾帧场景必填
            # first_frame: 首帧图片（以首帧宽高比为准，尾帧会自动裁剪适配）
            "role": "first_frame"
        },
        {
            "type": "image_url",
            "image_url": {
                "url": "https://img.sucaijishi.com/uploadfile/2023/0301/20230301120626930.png?imageMogr2/format/jpg/blur/1x0/quality/60"
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

# 步骤4: 发送请求并输出结果

response = requests.post(url, headers=headers, json=payload)
print(json.dumps(response.json(), indent=2, ensure_ascii=False))
```

### 返回示例

```json
{
  "id": "cgt-20260402221125-9lb5p",
  "usage": {
    "total_tokens": 50000,
    "input_tokens": 0,
    "input_tokens_details": {
      "cached_tokens": 0
    },
    "output_tokens": 50000,
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
api_key = "sk-******************************************"

headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {api_key}",
}

payload = {
    # 【model】(string, 必填) 固定值，用于查询 Seedance 视频生成结果
    "model": "seedance-2-0-get",
    # 【input】(string, 必填) 提交任务时返回的任务 ID
    "input": "cgt-20260403171827-s64n7"
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
  "request_id": "cgt-20260403171827-s64n7",
  "output": [
    {
      "type": "message",
      "content": [
        {
          "type": "output_text",
          "text": "{\"content\":{\"video_url\":\"https://ark-acg-cn-beijing.tos-cn-beijing.volces.com/doubao-seedance-2-0/02177520799968800000000000000000000ffffac14d8d3a26bee.mp4?...\"},\"id\":\"cgt-20260403171827-s64n7\",\"model\":\"doubao-seedance-2-0-260128\",\"status\":\"succeeded\"}"
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

视频链接: https://ark-acg-cn-beijing.tos-cn-beijing.volces.com/doubao-seedance-2-0/02177520799968800000000000000000000ffffac14d8d3a26bee.mp4?...
```


<p align="center">
  <small>© 2026 DMXAPI doubao-seedance-2-0-260128 首尾帧生视频</small>
</p>
