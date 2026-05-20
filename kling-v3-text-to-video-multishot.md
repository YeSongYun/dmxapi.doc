# kling-v3 文生视频（多镜头）API 使用文档

kling-v3 文生视频（多镜头）是可灵 V3 系列推出的多分镜视频生成能力，通过 `multi_shot` + `shot_type` 双控开关，允许在一次请求内最多自定义 6 个分镜，每个分镜支持独立的提示词与时长配置；同时提供智能分镜（intelligence）与自定义分镜（customize）两种模式、std/pro/4k 三档生成质量、3~15 秒任意时长、16:9 / 9:16 / 1:1 三种纵横比，并内置负向提示词、水印开关等参数，适配复杂叙事类视频的快速生产。

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

## 文生视频（多镜头）示例代码

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
    # 当前文档对应模型: kling-v3
    "model": "kling-v3",

    # 【input】(string, 必填) 文本提示词，可包含正向描述和负向描述
    # 可将提示词模板化来满足不同的视频生成需求
    # 不能超过 2500 个字符
    # 当 multi_shot 参数为 false 或当 shot_type 参数为 intelligence 时，当前参数必填
    "input": "一只猫动起来",

    # 【multi_shot】(boolean, 可选) 是否生成多镜头视频
    # 当前参数为 true 时，input(prompt) 参数无效
    # 当前参数为 false 时，shot_type 参数及 multi_prompt 参数无效
    # 默认值: false
    "multi_shot": True,

    # 【shot_type】(string, 可选) 分镜方式
    # 可选值: "customize"(自定义分镜) / "intelligence"(智能分镜)
    # 当 multi_shot 参数为 true 时，当前参数必填
    # 默认值: 空
    "shot_type": "customize",

    # 【multi_prompt】(array, 可选) 各分镜提示词，可包含正向描述和负向描述
    # 通过 index、prompt、duration 参数定义分镜序号及相应提示词和时长，其中：
    #   - 最多支持 6 个分镜，最小支持 1 个分镜
    #   - 每个分镜相关内容的最大长度不超过 512
    #   - 每个分镜的时长不大于当前任务的总时长，不小于 1
    #   - 所有分镜的时长之和等于当前任务的总时长
    # 当 multi_shot 参数为 true 且 shot_type 参数为 customize 时，当前参数不得为空
    # 默认值: 空
    "multi_prompt": [
        {
            # 【index】(int, 必填) 分镜序号
            "index": 1,
            # 【prompt】(string, 必填) 当前分镜的提示词，最大长度不超过 512
            "prompt": "一只猫缓缓出现在镜头中",
            # 【duration】(string, 必填) 当前分镜时长，单位 s，不大于总时长且不小于 1
            "duration": "2",
        },
        {
            "index": 2,
            "prompt": "猫稳稳往前走",
            "duration": "3",
        },
    ],

    # 【negative_prompt】(string, 可选) 负向文本提示词
    # 不能超过 2500 个字符
    # 默认值: 空
    "negative_prompt": "小狗",

    # 【duration】(string, 可选) 生成视频时长，单位 s
    # 可选值: "3" / "4" / "5" / "6" / "7" / "8" / "9" / "10" / "11" / "12" / "13" / "14" / "15"
    # 默认值: "5"
    "duration": "5",

    # 【mode】(string, 可选) 生成视频的模式
    # 可选值: "std"(标准模式，基础模式，性价比高) / "pro"(专家模式/高品质，高表现模式，生成视频质量更佳) / "4k"(4K 模式，输出视频分辨率为 4K)
    # 默认值: "std"
    "mode": "std",

    # 【sound】(string, 可选) 生成视频时是否同时生成声音
    # 可选值: "on"(开启) / "off"(关闭)
    # 默认值: "off"
    "sound": "on",

    # 【cfg_scale】(float, 可选) 生成视频的自由度
    # 值越大，模型自由度越小，与用户输入的提示词相关性越强
    # 取值范围: [0, 1]
    # 默认值: 0.5
    "cfg_scale": 1,

    # 【watermark_info】(array, 可选) 是否同时生成含水印的结果
    # 暂不支持自定义水印
    # 默认值: 空
    "watermark_info": {
        # 【enabled】(boolean, 必填) true 为生成含水印的结果，false 为不生成
        "enabled": True
    },

    # 【aspect_ratio】(string, 可选) 生成视频的画面纵横比（宽:高）
    # 可选值: "16:9" / "9:16" / "1:1"
    # 默认值: "16:9"
    "aspect_ratio": "9:16",
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

## 返回示例
```json
{
  "request_id": "tsk-geuaebugidep55vn",
  "output": [
    {
      "type": "message",
      "content": [
        {
          "type": "output_text",
          "text": "{\"taskId\":\"tsk-geuaebugidep55vn\"}"
        }
      ]
    }
  ],
  "usage": {
    "total_tokens": 45000,
    "input_tokens": 0,
    "input_tokens_details": {
      "cached_tokens": 0
    },
    "output_tokens": 45000,
    "output_tokens_details": {
      "reasoning_tokens": 0
    }
  }
}
```
> 返回示例中的 `request_id` 字段（同时在 `output[0].content[0].text` 中以 `taskId` 字段返回）即为任务 ID，用于第二步查询结果。

## 获取结果 示例代码
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
api_key = "sk-GSo30rearuurO4KP8wt3rvbWIWcGpWyHjelmpJHsEaETogVR"
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

    "input": "tsk-geuwh82xfidrbj6y",      
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
## 返回示例

```json
============================================================
完整响应
============================================================
{
  "request_id": "7978aa27-09c5-4f34-be39-61171c9a97b0",
  "output": [
    {
      "type": "message",
      "content": [
        {
          "type": "output_text",
          "text": "{\"code\":0,\"message\":\"SUCCEED\",\"data\":{\"task_id\":\"tsk-geuwh82xfidrbj6y\",\"task_status\":\"succeed\",\"task_info\":{},\"task_result\":{\"videos\":[{\"id\":\"mda-geuww2bfpq44fi99\",\"url\":\"https://gcdy5vxfrcse3j396atj.exp.bcevod.com/mda-geuwvu1fq5vgrhz0/_src/mda-geuwvu1fq5vgrhz0/geuw2uenxpunjq6v1fbc.mp4\",\"duration\":\"3.041\",\"watermark_url\":\"https://gcdy5vxfrcse3j396atj.exp.bcevod.com/mda-geuww2bfpq44fi99/_src/mda-geuww2bfpq44fi99/geuwy50cmn481hmy4k4n.mp4\"}]},\"task_status_msg\":\"\",\"watermark_info\":{\"enabled\":true},\"created_at\":1779192201061,\"updated_at\":1779192282758,\"final_unit_deduction\":\"9\"},\"request_id\":\"7978aa27-09c5-4f34-be39-61171c9a97b0\"}"
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
  ┌─ id            mda-geuww2bfpq44fi99
  │  时长          3.041 秒
  │  无水印 URL    https://gcdy5vxfrcse3j396atj.exp.bcevod.com/mda-geuwvu1fq5vgrhz0/_src/mda-geuwvu1fq5vgrhz0/geuw2uenxpunjq6v1fbc.mp4
  │  水印版 URL    https://gcdy5vxfrcse3j396atj.exp.bcevod.com/mda-geuww2bfpq44fi99/_src/mda-geuww2bfpq44fi99/geuwy50cmn481hmy4k4n.mp4
  └─
```

<p align="center">
  <small>© 2026 DMXAPI kling-v3 文生视频（多镜头）</small>
</p>

<!-- param-coverage: 14/14, missing: [] -->
