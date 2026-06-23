# doubao-seedance-2-0-260128 视频延长 API 使用文档

基于 doubao-seedance-2-0-260128 模型的多模态视频延长接口，支持输入 1~3 段参考视频（单段时长 2~15 秒，总时长不超过 15 秒）配合文本提示词，生成 4~15 秒的延续视频。支持有声视频输出，可自动合成人声、音效与背景音乐；支持联网搜索增强生成效果；采用异步任务模式，提交任务后通过单次查询接口获取结果视频 URL。

##  模型名称

- `doubao-seedance-2-0-260128`

##  接口地址

| 接口 | 请求方式 | URL |
|------|---------|-----|
| 提交任务 | POST | `https://www.dmxapi.cn/v1/responses` |
| 获取结果 | POST | `https://www.dmxapi.cn/v1/responses` |

:::warning
请妥善保管您的 API Key！严禁将密钥泄露给他人、硬编码到代码中或提交到公开的代码仓库。如果怀疑密钥已泄露，请立即前往 DMXAPI 官网重新生成。
:::


##  视频延长 示例代码

```python
import requests
import json

# ═══════════════════════════════════════════════════════════════
# 步骤1: 配置 API 连接信息
# ═══════════════════════════════════════════════════════════════

# DMXAPI 服务端点地址
url = "https://www.dmxapi.cn/v1/responses"

# DMXAPI 密钥 (请替换为您自己的密钥)
api_key = "sk-******************************************"

# ═══════════════════════════════════════════════════════════════
# 步骤2: 配置请求头
# ═══════════════════════════════════════════════════════════════

headers = {
    "Content-Type": "application/json",
    # 【鉴权】token 认证方式（注意本接口不需要 Bearer 前缀）
    "Authorization": f"{api_key}",
}

# ═══════════════════════════════════════════════════════════════
# 步骤3: 配置请求参数
# ═══════════════════════════════════════════════════════════════

payload = {
    # 【model】(string, 必填) 模型 ID
    "model": "doubao-seedance-2-0-260128",

    # 【input】(array, 必填) 输入内容数组，支持文本 + 视频/图片/音频组合
    # 视频延长场景：传入文本描述 + 1~3 段参考视频（role 均为 reference_video）
    # 单段视频要求：格式 mp4/mov，分辨率 480p/720p，时长 [2, 15] s，大小 <= 50 MB
    # 所有参考视频总时长不超过 15 秒
    "input": [
        {
            # 【type】(string, 必填) 文本输入类型，固定为 text
            "type": "text",
            # 【text】(string) 文本提示词，描述视频延长的方向与内容
            # 支持中英文；建议中文不超过 500 字，英文不超过 1000 词
            "text": "视频1中的拱形窗户打开，进入美术馆室内，接视频2，之后镜头进入画内，接视频3"
        },
        {
            # 【type】(string, 必填) 视频输入类型，固定为 video_url
            "type": "video_url",
            "video_url": {
                # 【url】(string) 视频公网 URL 或素材 ID（格式：asset://<ASSET_ID>）
                "url": "https://ark-project.tos-cn-beijing.volces.com/doc_video/r2v_extend_video1.mp4"
            },
            # 【role】(string, 条件必填) 视频用途，延长场景固定为 reference_video（参考视频）
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

    # 【generate_audio】(boolean, 可选) 是否生成有声视频，默认 true
    # true：自动生成与画面同步的人声、音效及背景音乐（单声道）
    # false：生成无声视频
    "generate_audio": True,

    # 【ratio】(string, 可选) 视频宽高比
    # 可选值: "16:9" / "4:3" / "1:1" / "3:4" / "9:16" / "21:9" / "adaptive"(自动适配)
    # Seedance 2.0 默认值: adaptive
    "ratio": "16:9",

    # 【duration】(integer, 可选) 视频时长（秒）
    # 取值范围: [4, 15]
    # 默认值: 5
    "duration": 4,

    # 【watermark】(boolean, 可选) 是否添加水印，默认 false
    # true: 含水印 / false: 不含水印
    "watermark": True,

    # 【resolution】(string, 可选) 视频分辨率
    # 可选值: "480p" / "720p"/ "1080p"
    # 默认值: 720p
    "resolution": "480p",

    # 【seed】(integer, 可选) 随机种子，控制生成内容的随机性
    # 取值范围: [-1, 2^32-1]；-1 表示使用随机数，相同 seed 生成结果类似但不保证完全一致
    # 默认值: -1
    "seed": -1,

    # 【callback_url】(string, 可选) 结果回调通知地址
    # 任务状态变更（queued/running/succeeded/failed/expired）时，平台向此地址推送 POST 请求
    "callback_url": "https://www.dmxapi.cn",

    # 【return_last_frame】(boolean, 可选) 是否返回生成视频的尾帧图像
    # true: 返回 PNG 格式尾帧，可用于多段连续视频生成（以上段尾帧作为下段首帧）
    # false: 不返回尾帧
    # 默认值: false
    "return_last_frame": False,

    # 【execution_expires_after】(integer, 可选) 任务超时阈值（秒）
    # 取值范围: [3600, 259200]；超时后任务自动终止并标记为 expired
    # 默认值: 172800（48 小时）
    "execution_expires_after": 172800,

    # 【tools】(array, 可选) 工具配置，启用联网搜索可提升时效性内容的生成质量
    # type 可选值: "web_search"（联网搜索）
    "tools": [{"type": "web_search"}]
}

# ═══════════════════════════════════════════════════════════════
# 步骤4: 发送请求并输出结果
# ═══════════════════════════════════════════════════════════════

response = requests.post(url, headers=headers, json=payload)
print(json.dumps(response.json(), indent=2, ensure_ascii=False))
```

## 返回示例

```json
{
  "id": "cgt-20260402222046-9vmsw",
  "usage": {
    "total_tokens": 97360,
    "input_tokens": 0,
    "input_tokens_details": {
      "cached_tokens": 0
    },
    "output_tokens": 97360,
    "output_tokens_details": {
      "reasoning_tokens": 0
    }
  }
}
```

> 返回的 `id` 即为任务 ID，用于后续查询生成结果。任务 ID 仅保存 7 天，超时后自动清除。

##  获取结果 示例代码

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
    # 【model】(string, 必填) 获取结果专用模型，固定填写 seedance-2-0-get
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

> **说明**：视频链接有效期为 24 小时，请及时下载保存。若 `status` 为 `running` 或 `queued`，可稍后重新调用获取接口查询。

<p align="center">
  <small>© 2026 DMXAPI doubao-seedance-2-0-260128 视频延长</small>
</p>
