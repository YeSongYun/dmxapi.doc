# DMXAPI Sora-2 文生视频 API 使用文档

基于 OpenAI Sora-2 模型的 AI 文生视频生成接口，可生成 4 秒、8 秒或 12 秒时长的视频，分辨率支持 "720x1280"(竖屏标准) 或 "1280x720"(横屏标准)。

## 模型名称

- `sora-2`

## 接口地址

| 接口 | 请求方式 | URL |
|------|---------|-----|
| 提交任务 | POST | `https://www.dmxapi.cn/v1/responses` |
| 查询结果 | POST | `https://www.dmxapi.cn/v1/responses` |

## 生成视频 示例代码

```python
import requests
import json

# 步骤1: 配置 API 连接信息
# DMXAPI 服务端点地址
url = "https://www.dmxapi.cn/v1/responses"

# DMXAPI 密钥（请替换为您自己的密钥）
# 获取方式: 登录 DMXAPI 官网 -> 个人中心 -> API 密钥管理
api_key = "sk-******************************************"

# 步骤2: 配置请求头
headers = {
    "Content-Type": "application/json",
    "Authorization": f"{api_key}",
}

# 步骤3: 配置请求参数
payload = {
    # 【model】(string, 必填) 指定视频生成模型
    "model": "sora-2",

    # 【input】(string, 必填) 视频场景描述文本（提示词）
    # 描述越详细，生成效果越好
    "input": "一群人在菜市场交流，有说有笑",

    # 【size】(string, 可选) 输出视频分辨率
    # 可选值: "720x1280"(竖屏标准) / "1280x720"(横屏标准)
    # 默认值: "720x1280"
    "size": "720x1280",

    # 【seconds】(string, 可选) 视频时长（秒）
    # 可选值: "4" / "8" / "12"
    # 默认值: "4"
    "seconds": "4"
}

# 步骤4: 发送请求并输出结果
response = requests.post(url, headers=headers, json=payload)
print(json.dumps(response.json(), indent=2, ensure_ascii=False))
```

## 返回示例

```json
{
  "id": "eyJtb2RlbCI6InNvcmEtMiIsImlkIjoidmlkZW9fNjliNzc5MWJmNmM0ODE5MGE1YTI4NjQ1ZjNjZGE0MjYifQchannel4429",
  "object": "video",
  "created_at": 1773631772,
  "status": "queued",
  "model": "sora-2",
  "prompt": "一群人在菜市场交流，有说有笑",
  "seconds": "4",
  "size": "720x1280",
  "usage": {
    "total_tokens": 29200,
    "input_tokens": 0,
    "input_tokens_details": {
      "cached_tokens": 0
    },
    "output_tokens": 29200,
    "output_tokens_details": {
      "reasoning_tokens": 0
    }
  }
}
```

> 请保存返回的 `id` 字段值，用于下一步查询任务结果。

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
api_key = "sk-*******************************************"

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
    "model": "sora-get",
    "input": "eyJtb2RlbCI6InNvcmEtMiIsImlkIjoidmlkZW9fNjliNzc5MWJmNmM0ODE5MGE1YTI4NjQ1ZjNjZGE0MjYifQchannel4429",
    
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
{
状态码: 200
Content-Type: application/json; charset=utf-8
JSON 响应大小: 6289331 字节
{
  "video_base64": "[base64 数据, 长度: 6289264]",
  "content_type": "video/mp4",
  "size_bytes": 4716948
}
从字段 'video_base64' 提取 base64 数据 (长度: 6289264)
解码后视频大小: 4716948 字节
视频已保存为 video_20260316_113300.mp4

}
```

<p align="center">
  <small>© 2026 DMXAPI Sora-2 文生视频</small>
</p>
