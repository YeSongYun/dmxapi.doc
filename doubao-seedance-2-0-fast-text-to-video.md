# doubao-seedance-2-0-fast-260128 文生视频 API 使用文档

doubao-seedance-2-0-fast-260128 是字节跳动火山引擎 Seedance 2.0 Fast 系列的文生视频模型，支持根据文本提示词生成高质量视频。模型支持 480p/720p 分辨率（不支持 1080p），视频时长范围 4~15 秒，支持 7 种宽高比（含自适应 adaptive 模式），可自动生成与画面同步的人声、音效及背景音乐。视频生成采用两步异步模式：先提交任务获取任务 ID，再通过 `seedance-2-0-get` 模型查询并获取视频结果。

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

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| model | string | 是 | 模型名称，固定为 `doubao-seedance-2-0-fast-260128` |
| input | array | 是 | 输入内容数组，文生视频时包含一个 `type: text` 的对象 |
| ratio | string | 否 | 视频宽高比，可选：`16:9` / `4:3` / `1:1` / `3:4` / `9:16` / `21:9` / `adaptive` |
| resolution | string | 否 | 分辨率，可选：`480p` / `720p`（seedance 2.0 fast 不支持 1080p） |
| duration | integer | 否 | 视频时长（秒），范围 [4, 15] 或 -1（模型自主选择） |
| generate_audio | boolean | 否 | 是否生成同步音频，true 生成人声/音效/BGM，false 为无声视频 |
| seed | integer | 否 | 随机种子，-1 为随机，固定值可复现类似结果 |
| watermark | boolean | 否 | 是否包含水印，false 无水印，true 含水印 |
| return_last_frame | boolean | 否 | 是否返回视频尾帧图像，用于生成连续视频 |
| execution_expires_after | integer | 否 | 任务超时时间（秒），范围 [3600, 259200]，默认 172800（48小时） |
| callback_url | string | 否 | 任务状态回调地址，状态变化时推送 POST 请求 |
| tools | array | 否 | 工具配置，`[{"type": "web_search"}]` 开启联网搜索 |

**任务状态枚举：**

| 状态值 | 说明 |
|--------|------|
| `queued` | 排队中 |
| `running` | 任务运行中 |
| `succeeded` | 任务成功 |
| `failed` | 任务失败 |
| `expired` | 任务超时（运行或排队超过过期时间） |

## 文生视频 示例代码

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
    # 【model】(string, 必填) 模型名称，指定使用 doubao-seedance-2-0-fast 文生视频模型
    "model": "doubao-seedance-2-0-fast-260128",

    # 【input】(array, 必填) 输入内容数组，文生视频时传入一个 type=text 的对象
    # text 字段为视频生成的文本提示词，建议中文不超过500字，英文不超过1000词
    # 额外支持日语、印尼语、西班牙语、葡萄牙语
    "input": [
        {
            "type": "text",
            "text": "写实风格，晴朗的蓝天之下，一大片白色的雏菊花田，镜头逐渐拉近，最终定格在一朵雏菊花的特写上，花瓣上有几颗晶莹的露珠",
        }
    ],

    # 【ratio】(string, 可选) 视频宽高比
    # 可选值: "16:9" / "4:3" / "1:1" / "3:4" / "9:16" / "21:9" / "adaptive"
    # "adaptive": 根据输入的提示词，智能选择最合适的宽高比
    "ratio": "16:9",

    # 【resolution】(string, 可选) 视频分辨率
    # 可选值: "480p" / "720p"（seedance 2.0 fast 不支持 1080p）
    # 720p + 16:9 对应实际像素: 1280×720
    "resolution": "720p",

    # 【duration】(integer, 可选) 视频时长（秒）
    # 取值范围: [4, 15] 或 -1（由模型在有效范围内自主选择合适时长）
    # 注意: 视频时长与计费相关，请谨慎设置
    "duration": 5,

    # 【generate_audio】(boolean, 可选) 是否生成同步音频（人声/音效/背景音乐）
    # true: 模型基于文本提示词与视觉内容自动生成匹配的人声、音效及背景音乐
    # false: 输出无声视频
    # 建议将对话部分置于双引号内以优化音频生成效果
    "generate_audio": True,

    # 【seed】(integer, 可选) 随机种子
    # -1: 使用随机数，每次生成不同结果
    # 固定正整数: 相同请求下会生成类似结果（不保证完全一致）
    "seed": -1,

    # 【watermark】(boolean, 可选) 是否包含水印
    # false: 不含水印
    # true: 含有水印
    "watermark": False,

    # 【return_last_frame】(boolean, 可选) 是否返回视频尾帧图像
    # true: 返回生成视频的尾帧图像（png 格式，宽高与视频一致，无水印）
    # false: 不返回尾帧图像
    # 可配合下一个任务的首帧输入实现连续视频生成
    "return_last_frame": False,

    # 【execution_expires_after】(integer, 可选) 任务超时时间（秒）
    # 取值范围: [3600, 259200]，默认 172800（48小时）
    # 任务处于排队或运行中超过该时间后状态变为 expired
    "execution_expires_after": 172800,

    # 【callback_url】(string, 可选) 任务状态回调地址
    # 任务状态发生变化时，平台向该地址推送 POST 请求
    # 状态说明: queued(排队中) / running(运行中) / succeeded(成功) / failed(失败) / expired(超时)
    "callback_url": "https://www.dmxapi.cn",

    # 【tools】(array, 可选) 工具配置，开启联网搜索
    # web_search: 模型根据提示词自主判断是否搜索互联网内容（如商品、天气等）
    # 开启后可提升视频时效性，但会增加一定时延
    "tools": [{"type": "web_search"}],
}

# 步骤4: 发送请求并输出结果

response = requests.post(url, headers=headers, json=payload)
print(json.dumps(response.json(), indent=2, ensure_ascii=False))
```

### 返回示例

```json
{
  "id": "cgt-20260424185020-nqhpl",
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
          "text": "{\"content\":{\"video_url\":\"https://ark-acg-cn-beijing.tos-cn-beijing.volces.com/doubao-seedance-2-0-fast/...mp4?...\"},\"id\":\"cgt-20260428165939-ccb9g\",\"model\":\"doubao-seedance-2-0-fast-260128\",\"status\":\"succeeded\"}"
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

视频链接: https://ark-acg-cn-beijing.tos-cn-beijing.volces.com/doubao-seedance-2-0-fast/...mp4?...
```

<p align="center">
  <small>© 2026 DMXAPI doubao-seedance-2-0-fast-260128 文生视频</small>
</p>
