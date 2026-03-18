# veo-3.1-generate-preview 文生视频 API 使用文档

基于 Google Veo 3.1 模型的 AI 视频生成接口，支持文生视频和图生视频两种模式。可生成 4 秒、6 秒或 8 秒视频，分辨率最高支持 4K，默认输出 720p（1280x720），支持 16:9 与 9:16 宽高比，并原生支持视频内音效生成。采用异步任务模式，提交生成请求后通过独立接口获取结果。

## 模型名称

- `veo-3.1-generate-preview`


## 接口地址

| 接口 | 请求方式 | URL |
|------|---------|-----|
| 提交任务 | POST | `https://www.dmxapi.cn/v1/responses` |
| 查询结果 | POST | `https://www.dmxapi.cn/v1/responses` |



## 生成视频 示例代码

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

# ═══════════════════════════════════════════════════════════════
# 🔑 步骤1: 配置 API 连接信息
# ═══════════════════════════════════════════════════════════════

# 🌐 DMXAPI 服务端点地址
url = "https://www.dmxapi.cn/v1/responses"

# 🔐 DMXAPI 密钥 (请替换为您自己的密钥)
# 获取方式: 登录 DMXAPI 官网 -> 个人中心 -> API 密钥管理
api_key = "sk-***************************************"

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
       # 【model】(string, 必填) 模型名称
       "model": "veo-3.1-generate-preview",
       # 【input】(string, 必填) 视频描述文本
       # 支持在 prompt 中描述音效，可触发原生音频生成
       "input": "一个宁静的日式庭院，樱花花瓣缓缓飘落，锦鲤在池塘中游动，背景传来悠扬的风铃声",
       # 【seconds】(string, 可选) 视频时长，默认为 "8"
       # 可选值: "4" / "6" / "8"；图生视频时固定为 "8"
       "seconds": "8",
       # 【size】(string, 可选) 输出分辨率，默认 720p
       # 可选值: "1280x720"(720p) / "1920x1080"(1080p)；4K 仅 Veo 3+ 支持
       "size": "1280x720",
}


# ═══════════════════════════════════════════════════════════════
# 📤 步骤4: 发送请求并输出结果
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
  "created": 1773319296,
  "duration": 8,
  "error": null,
  "height": 720,
  "id": "eyJtb2RlbCI6InZlby0zLjEtZ2VuZXJhdGUtcHJldmlldyIsImlkIjoicHJvamVjdHMvYWFka2Znbm5kL2xvY2F0aW9ucy9nbG9iYWwvcHVibGlzaGVycy9nb29nbGUvbW9kZWxzL3Zlby0zLjEtZ2VuZXJhdGUtcHJldmlldy9vcGVyYXRpb25zL2Q2ZDNjNzI5LTYwZjAtNDUxYy05NmVhLTNiM2Y1YmRkMzA0MiJ9channel4458",
  "model": "veo-3.1-generate-preview",
  "object": "video",
  "prompt": "",
  "status": "in_progress",
  "url": null,
  "width": 1280,
  "usage": {
    "total_tokens": 233600,
    "input_tokens": 0,
    "input_tokens_details": {
      "cached_tokens": 0
    },
    "output_tokens": 233600,
    "output_tokens_details": {
      "reasoning_tokens": 0
    }
  }
}
```

## 获取生成视频 示例代码

```python
import requests
import json
import base64
from datetime import datetime

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
    # 【model】(string, 必填) 固定填 "sora-get"，表示查询已提交的视频任务
    "model": "sora-get",
    # 【input】(string, 必填) 提交任务时响应中返回的 id 字段值（任务 ID）
    "input": "eyJtb2RlbCI6InZlby0zLjEtZ2VuZXJhdGUtcHJldmlldyIsImlkIjoicHJvamVjdHMvZWF6cmd0Zi9sb2NhdGlvbnMvZ2xvYmFsL3B1Ymxpc2hlcnMvZ29vZ2xlL21vZGVscy92ZW8tMy4xLWdlbmVyYXRlLXByZXZpZXcvb3BlcmF0aW9ucy8zOTVhYmE0OS1jM2NlLTQ5Y2MtYWNkNy03OGQ5MTcxMzU0OGMifQchannel4517",

}


# ═══════════════════════════════════════════════════════════════
# 📤 步骤4: 发送请求并输出结果
# ═══════════════════════════════════════════════════════════════

# 发送 POST 请求到 API 服务器
response = requests.post(url, headers=headers, json=payload)

content_type = response.headers.get("Content-Type", "")
print(f"状态码: {response.status_code}")
print(f"Content-Type: {content_type}")

if "json" in content_type:
    data = response.json()
    print(f"JSON 响应大小: {len(response.content)} 字节")
    # 打印 JSON 但跳过大段 base64 数据
    display_data = {}
    for k, v in data.items():
        if isinstance(v, str) and len(v) > 1000:
            display_data[k] = f"[base64 数据, 长度: {len(v)}]"
        else:
            display_data[k] = v
    print(json.dumps(display_data, indent=2, ensure_ascii=False))

    # 自动查找最长的字符串字段作为 base64 视频数据
    video_b64 = None
    if isinstance(data, dict):
        best_key = None
        best_len = 0
        for key, val in data.items():
            if isinstance(val, str) and len(val) > best_len:
                best_key = key
                best_len = len(val)
        if best_key and best_len > 1000:
            video_b64 = data[best_key]
            print(f"从字段 '{best_key}' 提取 base64 数据 (长度: {best_len})")

    if video_b64:
        # 去除可能的 data URI 前缀 (如 "data:video/mp4;base64,")
        if isinstance(video_b64, str) and video_b64.startswith("data:") and "," in video_b64:
            video_b64 = video_b64.split(",", 1)[1]

        video_bytes = base64.b64decode(video_b64)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"video_{timestamp}.mp4"
        with open(filename, "wb") as f:
            f.write(video_bytes)
        print(f"解码后视频大小: {len(video_bytes)} 字节")
        print(f"视频已保存为 {filename}")
    else:
        print("未找到 base64 视频数据")
else:
    # 非 JSON 响应：直接作为视频流保存
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"video_{timestamp}.mp4"
    print(f"视频流大小: {len(response.content)} 字节")
    with open(filename, "wb") as f:
        f.write(response.content)
    print(f"视频已保存为 {filename}")
```

## 返回示例

```json
状态码: 200
Content-Type: application/json; charset=utf-8
JSON 响应大小: 14131086 字节
{
  "video_base64": "[base64 数据, 长度: 14130996]",
  "content_type": "application/json; charset=UTF-8",
  "size_bytes": 10598247
}
从字段 'video_base64' 提取 base64 数据 (长度: 14130996)
解码后视频大小: 10598247 字节
视频已保存为 video_20260317_180719.mp4
```

<p align="center">
  <small>© 2026 DMXAPI veo-3.1-generate-preview 文生视频</small>
</p>
