# AICC-Doubao-Seedance-2.0 视频延长 API 使用文档

基于豆包 Seedance 2.0 模型的视频延长接口，支持输入原视频（可 1~3 段，单段时长 2~15 秒，总时长不超过 15 秒）配合文本提示词，生成 8~15 秒的延续视频。支持有声视频输出，可自动合成人声、音效与背景音乐；支持联网搜索增强生成效果；采用异步任务模式，提交任务后通过单次查询接口获取结果视频 URL。

## 模型名称

- `AICC-Doubao-Seedance-2.0`

## 接口地址

| 接口 | 请求方式 | URL |
|------|---------|-----|
| 提交任务 | POST | `https://www.dmxapi.cn/v1/responses` |
| 获取结果 | POST | `https://www.dmxapi.cn/v1/responses` |

:::warning
请妥善保管您的 API Key！严禁将密钥泄露给他人、硬编码到代码中或提交到公开的代码仓库。如果怀疑密钥已泄露，请立即前往 DMXAPI 官网重新生成。
:::

:::tip 重要：视频对象必须填 role: "reference_video"
所有视频输入都必须携带 `"role": "reference_video"`（缺失会被拒绝）。**视频延长与视频编辑按输入组合区分**：仅视频（无参考图）→ 视频延长；视频 + 参考图 → 视频编辑。
:::


##  视频延长 示例代码

```python
import requests
import json

# ═══════════════════════════════════════════════════════════════
# 步骤1: 配置 API 连接信息
# ═══════════════════════════════════════════════════════════════

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
    "model": "AICC-Doubao-Seedance-2.0",

    # 【input】(array, 必填) 输入内容数组
    # 视频延长场景：传入文本描述 + 1~3 段原视频（role 均为 reference_video）
    # 单段视频要求：格式 mp4/mov，分辨率 480p/720p，时长 [2, 15] s，大小 <= 50 MB，帧率 [24, 60] FPS
    # 所有视频总时长不超过 15 秒
    "input": [
        {
            # 【type】(string, 必填) 文本输入类型，固定为 text
            "type": "text",
            # 【text】(string) 文本提示词，描述视频延长的方向与内容
            # 支持中英文；建议中文不超过 500 字，英文不超过 1000 词
            "text": "视频1结束后镜头继续缓缓拉远，画面渐暗结束"
        },
        {
            # 【type】(string, 必填) 视频输入类型，固定为 video_url
            "type": "video_url",
            "video_url": {
                # 【url】(string) 视频公网 URL 或素材 ID（格式：asset://<ASSET_ID>）
                # ⚠️ 视频不支持 Base64 上传
                "url": "https://ark-project.tos-cn-beijing.volces.com/doc_video/r2v_tea_video1.mp4"
            },
            # 【role】(string, 必填) 视频延长场景固定为 reference_video（原视频）
            "role": "reference_video"
        },
    ],

    # 【generate_audio】(boolean, 可选) 是否生成有声视频，默认 true
    # true：自动生成与画面同步的人声、音效及背景音乐（单声道）
    # false：生成无声视频
    "generate_audio": True,

    # 【ratio】(string, 可选) 视频宽高比
    # 可选值: "16:9" / "4:3" / "1:1" / "3:4" / "9:16" / "21:9" / "adaptive"(自动适配)
    # 默认值: adaptive
    "ratio": "adaptive",

    # 【duration】(integer, 必填) 视频时长（秒）
    # 取值范围: [8, 15]，输出视频的秒数必须大于等于 8s
    # ⚠️ 视频延长场景 duration 为必填项，省略会被拒绝
    "duration": 8,

    # 【watermark】(boolean, 可选) 是否添加水印，默认 false
    # true: 含水印 / false: 不含水印
    "watermark": False,

    # 【resolution】(string, 可选) 视频分辨率
    # 可选值: "480p" / "720p"/ "1080p"
    # 默认值: 720p
    "resolution": "480p",

    # 【seed】(integer, 可选) 随机种子，默认 -1
    # 注意：Seedance 2.0 系列暂不支持指定 seed，传入后会被上游忽略
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

> 返回的 `id` 即为任务 ID，用于后续查询生成结果。任务 ID 仅保存 7 天，超时后自动清除。

##  获取结果 示例代码

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
          "text": "{\"content\":{\"video_url\":\"https://ark-acg-cn-beijing.tos-cn-beijing.volces.com/doubao-seedance-2-0/02178463059431000000000000000000000ffffac15e1d87c9b67.mp4?...\"},\"id\":\"cgt-20260721184314-9wrsf\",\"model\":\"doubao-seedance-2-0-260128\",\"status\":\"succeeded\"}"
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
  <small>© 2026 DMXAPI AICC-Doubao-Seedance-2.0 视频延长</small>
</p>
