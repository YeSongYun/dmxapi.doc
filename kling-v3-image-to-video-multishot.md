# kling-v3 图生视频（多镜头）API 使用文档

kling-v3 是可灵 AI 推出的新一代视频生成模型，本接口在「图生视频」基础上扩展为多镜头分镜生成：以一张参考图为视觉锚点，配合用户自定义（customize）或智能（intelligence）分镜方式，最多支持 6 个连续分镜，每个分镜独立指定提示词与时长，所有分镜时长之和等于任务总时长。覆盖 std / pro / 4K 三档生成模式，支持 3~15 秒任意总时长，并可叠加同步声音生成、负向提示词、自由度（cfg_scale）控制以及水印开关。采用异步任务机制：提交后立即返回任务 ID，通过查询接口获取最终视频 URL。

## 模型名称

- `kling-v3`

## 接口地址

| 接口 | 请求方式 | URL |
|------|---------|-----|
| 提交任务 | POST | `https://www.dmxapi.cn/v1/responses` |
| 获取结果 | POST | `https://www.dmxapi.cn/v1/responses` |

:::warning
请妥善保管您的 API Key！严禁将密钥泄露给他人、硬编码到代码中或提交到公开的代码仓库。
:::

## 图生视频（多镜头）示例代码

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
    # 【model】(string, 必填) 模型名称
    # 可选值: "kling-v3"(可灵 v3 视频生成模型)
    "model": "kling-v3",

    # 【image】(string, 必填) 参考图像
    # 支持传入图片 URL（确保可访问）或 Base64 编码字符串
    # 使用 Base64 时，请勿在前面添加 data:image/png;base64, 等前缀，仅传入纯 Base64 字符串
    # 图片格式: .jpg / .jpeg / .png
    # 图片文件大小不能超过 10MB
    # 图片宽高尺寸不小于 300px，宽高比介于 1:2.5 ~ 2.5:1 之间
    "image": "https://prod-ss-images.s3.cn-northwest-1.amazonaws.com.cn/vidu-maas/template/image2video.png",

    # 【multi_shot】(boolean, 可选) 是否生成多镜头视频
    # 默认值: false
    # 当前参数为 true 时，prompt 参数无效
    # 当前参数为 false 时，shot_type 参数及 multi_prompt(input) 参数无效
    "multi_shot": True,

    # 【shot_type】(string, 可选) 分镜方式
    # 可选值:
    #   "customize"(自定义分镜：用户通过 input/multi_prompt 指定每个分镜的 index/prompt/duration)
    #   "intelligence"(智能分镜：由模型基于 prompt 自动拆分镜头)
    # 当 multi_shot 参数为 true 时，当前参数必填
    "shot_type": "customize",

    # 【input】(array, 可选) 各分镜信息（对应官方 multi_prompt 字段）
    # 通过 index、prompt、duration 定义分镜序号及对应提示词与时长
    # 最多支持 6 个分镜，最少 1 个分镜
    # 每个分镜相关内容（prompt）的最大长度不超过 512
    # 每个分镜时长不大于当前任务总时长，且不小于 1
    # 所有分镜的时长之和必须等于当前任务的总时长（duration 参数）
    # 当 multi_shot=true 且 shot_type="customize" 时，当前参数不得为空
    "input": [
        # 【input[].index】(int, 必填) 分镜序号
        # 【input[].prompt】(string, 必填) 当前分镜的文本提示词，长度 ≤ 512
        # 【input[].duration】(string, 必填) 当前分镜的时长（秒），不小于 1，且不大于任务总时长
        {"index": 1, "prompt": "宇航员缓缓回头遥望星空", "duration": "3"},
        {"index": 2, "prompt": "打开面罩，欣慰的笑了起来", "duration": "2"},
    ],

    # 【negative_prompt】(string, 可选) 负向文本提示词
    # 不能超过 2500 个字符
    # 默认值: 空
    "negative_prompt": "模糊, 抖动",

    # 【sound】(string, 可选) 生成视频时是否同时生成声音
    # 可选值: "on"(生成声音) / "off"(不生成声音)
    # 默认值: "off"
    "sound": "on",

    # 【cfg_scale】(float, 可选) 生成视频的自由度
    # 值越大，模型自由度越小，与用户输入的提示词相关性越强
    # 取值范围: [0, 1]
    # 默认值: 0.5
    "cfg_scale": 0.5,

    # 【mode】(string, 可选) 生成视频的模式
    # 可选值:
    #   "std"(标准模式，基础模式，性价比高)
    #   "pro"(专家模式/高品质，高表现模式，生成视频质量更佳)
    #   "4k"(4K 模式，高表现同 pro，输出视频分辨率为 4K)
    # 默认值: "std"
    "mode": "pro",

    # 【duration】(string, 可选) 生成视频总时长，单位 s
    # 可选值: "3" / "4" / "5" / "6" / "7" / "8" / "9" / "10" / "11" / "12" / "13" / "14" / "15"
    # 默认值: "5"
    # 当 shot_type="customize" 时，input 数组内所有分镜 duration 之和必须等于本字段
    "duration": "5",

    # 【watermark_info】(object, 可选) 是否同时生成含水印的结果
    # 暂不支持自定义水印
    # 默认值: 空
    "watermark_info": {
        # 【watermark_info.enabled】(boolean, 必填) 是否生成水印版本
        # 可选值: true(生成) / false(不生成)
        "enabled": False
    },
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
  "request_id": "tsk-geuy499g0bnmmfuf",
  "output": [
    {
      "type": "message",
      "content": [
        {
          "type": "output_text",
          "text": "{\"taskId\":\"tsk-geuy499g0bnmmfuf\"}"
        }
      ]
    }
  ],
  "usage": {
    "total_tokens": 60000,
    "input_tokens": 0,
    "input_tokens_details": {
      "cached_tokens": 0
    },
    "output_tokens": 60000,
    "output_tokens_details": {
      "reasoning_tokens": 0
    }
  }
}
```

> 提交成功后，从 `output[0].content[0].text` 中解析 JSON 即可拿到 `taskId`（即提交返回的任务 ID），用于第二步查询结果。

## 获取结果 示例代码

视频生成通常需要 1~5 分钟，建议每隔 15 秒轮询一次，直到任务完成。

```python
"""
╔═══════════════════════════════════════════════════════════════╗
║                  DMXAPI 自研接口                               ║
╚═══════════════════════════════════════════════════════════════╝

📝 功能说明:
   本脚本演示如何使用 requests 库调用 DMXAPI 的自研接口

═══════════════════════════════════════════════════════════════
"""
import requests
import json
import io
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
# ═══════════════════════════════════════════════════════════════
# 🔑 步骤1: 配置 API 连接信息
# ═══════════════════════════════════════════════════════════════
# 🌐 DMXAPI 服务端点地址
url = "https://www.dmxapi.cn/v1/responses"

# 🔐 DMXAPI 密钥 (请替换为您自己的密钥)
# 获取方式: 登录 DMXAPI 官网 -> 个人中心 -> API 密钥管理
api_key = "sk-************************************************"
# ═══════════════════════════════════════════════════════════════
# 📋 步骤2: 配置请求头
# ═══════════════════════════════════════════════════════════════
headers = {
    "Content-Type": "application/json",      # 指定请求体为 JSON 格式
    "Authorization": f"{api_key}",    # token 认证方式
}

# ═══════════════════════════════════════════════════════════════
# 💬 步骤3: 配置请求参数
# ═══════════════════════════════════════════════════════════════
payload = {
    "model": "kling-v3-get-all",
    "input": "tsk-ge0vtur0xjesi736", 
}

# ═══════════════════════════════════════════════════════════════
# 📤 步骤4: 发送请求并输出结果
# ═══════════════════════════════════════════════════════════════
# 发送 POST 请求到 API 服务器
response = requests.post(url, headers=headers, json=payload)
data = response.json()
# ═══════════════════════════════════════════════════════════════
# 📊 步骤5: 输出完整响应 + 视频清单
# ═══════════════════════════════════════════════════════════════

print("=" * 60)
print("完整响应")
print("=" * 60)
print(json.dumps(data, indent=2, ensure_ascii=False))

# Responses API 把上游真实 JSON 字符串化塞进 output[0].content[0].text，需要再解一层
try:
    inner = json.loads(data["output"][0]["content"][0]["text"])
    videos = (inner.get("data", {}).get("task_result") or {}).get("videos", [])
except (KeyError, IndexError, json.JSONDecodeError, TypeError):
    videos = []

if videos:
    print(f"\n视频输出（共 {len(videos)} 个）")
    for v in videos:
        print(f"  ┌─ id            {v.get('id')}")
        print(f"  │  时长          {v.get('duration')} 秒")
        print(f"  │  无水印 URL    {v.get('url')}")
        if v.get("watermark_url"):
            print(f"  │  水印版 URL    {v.get('watermark_url')}")
        print(f"  └─")
```

### 返回示例

```
============================================================
完整响应
============================================================
{
  "request_id": "d173b308-9e8d-467d-92b0-9f36c2c8fec0",
  "output": [
    {
      "type": "message",
      "content": [
        {
          "type": "output_text",
          "text": "{\"code\":0,\"message\":\"SUCCEED\",\"data\":{\"task_id\":\"tsk-ge0vtur0xjesi736\",\"task_status\":\"succeed\",\"task_info\":{},\"task_result\":{\"videos\":[{\"id\":\"mda-ge0vt6fvv0m91uw8\",\"url\":\"https://gcdy5vxfrcse3j396atj.exp.bcevod.com/mda-ge0vt6fvv0m91uw8/_src/mda-ge0vt6fvv0m91uw8/ge0vjeg3nw7nn9vbux89.mp4\",\"duration\":\"5.041\"}]},\"task_status_msg\":\"\",\"created_at\":1779707654605,\"updated_at\":1779707770260,\"final_unit_deduction\":\"6\"},\"request_id\":\"d173b308-9e8d-467d-92b0-9f36c2c8fec0\"}"
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

视频输出（共 1 个）
  ┌─ id            mda-ge0vt6fvv0m91uw8
  │  时长          5.041 秒
  │  无水印 URL    https://gcdy5vxfrcse3j396atj.exp.bcevod.com/mda-ge0vt6fvv0m91uw8/_src/mda-ge0vt6fvv0m91uw8/ge0vjeg3nw7nn9vbux89.mp4
  └─
```

<p align="center">
  <small>© 2026 DMXAPI kling-v3 图生视频（多镜头）</small>
</p>

<!-- param-coverage: 13/13, missing: [] -->
