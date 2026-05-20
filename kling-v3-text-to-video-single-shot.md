# kling-v3 文生视频（单镜头）API 使用文档

kling-v3 是可灵 AI 推出的新一代视频生成模型，本接口支持通过纯文本提示词一次性生成高质量单镜头视频，覆盖标准（std）/ 专家（pro）/ 4K 三种生成模式，支持 3~15 秒任意时长、16:9 / 9:16 / 1:1 三种画面比例，可选生成同步声音、自定义负向提示词、自由度控制（cfg_scale）以及水印开关。采用异步任务机制：提交后立即返回任务 ID，通过查询接口获取最终视频 URL。

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

## 文生视频 示例代码

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

    # 【input】(string, 必填) 文本提示词，可包含正向描述
    # 不能超过 2500 个字符
    # 语法结构越简单越好；当 multi_shot=false 或 shot_type=intelligence 时必填
    "input": "一只猫动起来",

    # 【multi_shot】(boolean, 可选) 是否生成多镜头视频
    # 默认值: false
    # 当前参数为 true 时，input(prompt) 参数无效
    # 当前参数为 false 时，shot_type 参数及 multi_prompt 参数无效
    "multi_shot": False,

    # 【negative_prompt】(string, 可选) 负向文本提示词
    # 不能超过 2500 个字符
    # 默认值: 空
    "negative_prompt": "小狗",

    # 【duration】(string, 可选) 生成视频时长，单位 s
    # 可选值: "3" / "4" / "5" / "6" / "7" / "8" / "9" / "10" / "11" / "12" / "13" / "14" / "15"
    # 默认值: "5"
    "duration": "5",

    # 【mode】(string, 可选) 生成视频的模式
    # 可选值:
    #   "std"(标准模式，基础模式，性价比高)
    #   "pro"(专家模式/高品质，高表现模式，生成视频质量更佳)
    #   "4k"(4K 模式，高表现同 pro，输出视频分辨率为 4K)
    # 默认值: "std"
    "mode": "std",

    # 【sound】(string, 可选) 生成视频时是否同时生成声音
    # 可选值: "on"(生成声音) / "off"(不生成声音)
    # 默认值: "off"
    "sound": "on",

    # 【cfg_scale】(float, 可选) 生成视频的自由度
    # 值越大，模型自由度越小，与用户输入的提示词相关性越强
    # 取值范围: [0, 1]
    # 默认值: 0.5
    "cfg_scale": 1,

    # 【watermark_info】(object, 可选) 是否同时生成含水印的结果
    # 暂不支持自定义水印
    # 默认值: 空
    "watermark_info": {
        # 【watermark_info.enabled】(boolean, 必填) 是否生成水印版本
        # 可选值: true(生成) / false(不生成)
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
  "request_id": "tsk-geuace0sf3c6evp5",
  "output": [
    {
      "type": "message",
      "content": [
        {
          "type": "output_text",
          "text": "{\"taskId\":\"tsk-geuace0sf3c6evp5\"}"
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

# 防 Windows GBK 控制台噎死中文
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
# ═══════════════════════════════════════════════════════════════
# 🔑 步骤1: 配置 API 连接信息
# ═══════════════════════════════════════════════════════════════
# 🌐 DMXAPI 服务端点地址
url = "https://www.dmxapi.cn/v1/responses"
# 🔐 DMXAPI 密钥 (请替换为您自己的密钥)
# 获取方式: 登录 DMXAPI 官网 -> 个人中心 -> API 密钥管理
api_key = "sk-*********************************************"
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

    "input": "tsk-geuvyb8stzgr3y2q",
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

```
============================================================
完整响应
============================================================
{
  "request_id": "abb73767-eb4c-473c-b034-32e00a6130d3",
  "output": [
    {
      "type": "message",
      "content": [
        {
          "type": "output_text",
          "text": "{\"code\":0,\"message\":\"SUCCEED\",\"data\":{\"task_id\":\"tsk-geuvyb8stzgr3y2q\",\"task_status\":\"succeed\",\"task_info\":{},\"task_result\":{\"videos\":[{\"id\":\"mda-geuvyauw1bnzfjss\",\"url\":\"https://gcdy5vxfrcse3j396atj.exp.bcevod.com/mda-geuv8016gdhwzdgh/_src/mda-geuv8016gdhwzdgh/geuvmp1mu9gqtq459ujh.mp4\",\"duration\":\"3.041\",\"watermark_url\":\"https://gcdy5vxfrcse3j396atj.exp.bcevod.com/mda-geuvyauw1bnzfjss/_src/mda-geuvyauw1bnzfjss/geuvzj2kft2eicyfhcmv.mp4\"}]},\"task_status_msg\":\"\",\"watermark_info\":{\"enabled\":true},\"created_at\":1779190926850,\"updated_at\":1779191012700,\"final_unit_deduction\":\"9\"},\"request_id\":\"abb73767-eb4c-473c-b034-32e00a6130d3\"}"
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
  ┌─ id            mda-geuvyauw1bnzfjss
  │  时长          3.041 秒
  │  无水印 URL    https://gcdy5vxfrcse3j396atj.exp.bcevod.com/mda-geuv8016gdhwzdgh/_src/mda-geuv8016gdhwzdgh/geuvmp1mu9gqtq459ujh.mp4
  │  水印版 URL    https://gcdy5vxfrcse3j396atj.exp.bcevod.com/mda-geuvyauw1bnzfjss/_src/mda-geuvyauw1bnzfjss/geuvzj2kft2eicyfhcmv.mp4
  └─
```

<p align="center">
  <small>© 2026 DMXAPI kling-v3 文生视频（单镜头）</small>
</p>


