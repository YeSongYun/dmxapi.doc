# kling-v3 首尾帧生视频（一镜到底）API 使用文档

kling-v3 首尾帧生视频接口基于可灵 3.0 视频大模型，通过同时指定首帧图像与尾帧图像，并在提示词中描述两个主体的互动逻辑，实现一镜到底的连续视频生成。接口支持 std 标准模式与 pro 专家模式两档画质，视频时长可在 3 秒～15 秒区间灵活配置，并提供负向提示词、声音开关、自由度（cfg_scale）等细粒度控制，适用于角色互动、场景过渡、动态海报等创意视频生成场景。接口采用异步任务设计，提交后通过任务 ID 二次查询即可获取最终视频地址。

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

## 首尾帧生视频 示例代码

```python
import requests
import json
import base64
import os

# ═══════════════════════════════════════════════════════════════
# 步骤1: 配置 API 连接信息
# ═══════════════════════════════════════════════════════════════

# DMXAPI 服务端点地址
url = "https://www.dmxapi.cn/v1/responses"

# DMXAPI 密钥 (请替换为您自己的密钥)
# 获取方式: 登录 DMXAPI 官网 -> 个人中心 -> API 密钥管理
api_key = "sk-***********************************************"

# ═══════════════════════════════════════════════════════════════
# 步骤2: 配置请求头
# ═══════════════════════════════════════════════════════════════

headers = {
    "Content-Type": "application/json",       # 指定请求体为 JSON 格式
    "Authorization": f"{api_key}",            # token 认证方式
}

# ═══════════════════════════════════════════════════════════════
# 步骤3: 图片输入适配 (URL / 本地路径 二选一)
# ═══════════════════════════════════════════════════════════════
# 同时支持两种图片传入方式:
#   1) URL  : 以 http:// 或 https:// 开头的可访问图片链接，直接传给 API
#   2) 本地 : 本地图片文件路径，自动读取并转为 Base64 编码后传给 API
# 使用 Base64 时不要添加 data:image/png;base64, 之类的前缀，仅传 Base64 字符串本体

def load_image(source: str) -> str:
    """根据输入自动适配: URL 原样返回; 本地路径读取并转 Base64"""
    if source.startswith("http://") or source.startswith("https://"):
        return source
    if os.path.isfile(source):
        with open(source, "rb") as f:
            return base64.b64encode(f.read()).decode("utf-8")
    # 既不是 URL 也不是存在的本地文件，则按原样返回（例如已是 Base64 字符串）
    return source

# 首帧图片来源: 可填 URL，也可填本地路径，例如:
#   "C:/Users/15664/Desktop/startend2video-1.jpeg"
image_source = "https://prod-ss-images.s3.cn-northwest-1.amazonaws.com.cn/vidu-maas/template/startend2video-1.jpeg"

# 尾帧图片来源: 可填 URL，也可填本地路径，例如:
#   "C:/Users/15664/Desktop/startend2video-2.jpeg"
image_tail_source = "https://prod-ss-images.s3.cn-northwest-1.amazonaws.com.cn/vidu-maas/template/startend2video-2.jpeg"

# ═══════════════════════════════════════════════════════════════
# 步骤4: 配置请求参数
# ═══════════════════════════════════════════════════════════════

payload = {
    # 【模型名称】(string, 必填) 指定调用的视频生成模型
    # 可选值: "kling-v3"(可灵 3.0 视频生成模型)
    "model": "kling-v3",

    # 【参考图像 - 首帧】(string, 可选, 与 image_tail 至少二选一) 视频起始帧图像
    # 支持传入图片 Base64 编码或图片 URL（确保可访问）
    # 使用 Base64 时不要添加 data:image/png;base64, 之类的前缀，仅传 Base64 字符串本体
    # 图片格式支持 .jpg / .jpeg / .png
    # 图片文件大小不能超过 10MB
    # 图片宽高尺寸不小于 300px，图片宽高比介于 1:2.5 ~ 2.5:1 之间
    "image": load_image(image_source),

    # 【参考图像 - 尾帧】(string, 可选, 与 image 至少二选一) 视频结束帧图像（尾帧控制）
    # 支持传入图片 Base64 编码或图片 URL（确保可访问）
    # 使用 Base64 时不要添加 data:image/png;base64, 之类的前缀，仅传 Base64 字符串本体
    # 图片格式支持 .jpg / .jpeg / .png
    # 图片文件大小不能超过 10MB，图片宽高尺寸不小于 300px
    # image 与 image_tail 至少二选一，二者不能同时为空；同时提供两者即为首尾帧"一镜到底"模式
    "image_tail": load_image(image_tail_source),

    # 【文本提示词】(string, 必填) 描述视频内容的正向提示词
    # 可包含正向描述和负向描述，建议通过模板化提示词满足不同生成需求
    # 提示词长度不能超过 2500 个字符
    # 语法结构越简单越好，例如："男人说：你好"
    "input": "图一的鸟在图二的人头上，两个主体互动，跳舞,一镜到底",

    # 【负向文本提示词】(string, 可选, 默认空) 描述不希望在视频中出现的元素
    # 不能超过 2500 个字符
    "negative_prompt": "模糊, 抖动",

    # 【声音开关】(string, 可选, 默认 "off") 生成视频时是否同时生成声音
    # 可选值: "on"(同时生成声音) / "off"(不生成声音)
    "sound": "on",

    # 【生成自由度】(float, 可选, 默认 0.5) 控制模型自由度与提示词相关性
    # 取值范围: [0, 1]
    # 值越大，模型自由度越小，与用户输入的提示词相关性越强
    "cfg_scale": 0.5,

    # 【生成模式】(string, 可选, 默认 "std") 生成视频的画质模式
    # 可选值: "std"(标准模式，基础模式，性价比高) / "pro"(专家模式，高表现，生成视频质量更佳) / "4k"(4K 模式，高表现同 pro，输出 4K 分辨率)
    "mode": "pro",

    # 【视频时长】(string, 可选, 默认 "5", 单位秒) 生成视频的总时长
    # 可选值: "3" / "4" / "5" / "6" / "7" / "8" / "9" / "10" / "11" / "12" / "13" / "14" / "15"
    "duration": "5",

    # 【水印控制】(object, 可选, 默认空) 是否同时生成含水印的结果，暂不支持自定义水印
    "watermark_info": {
        # 【水印开关】(boolean, 必填) 是否生成含水印版本
        # 可选值: True(生成含水印版本) / False(不生成含水印版本)
        "enabled": False
    },
}

# ═══════════════════════════════════════════════════════════════
# 步骤5: 发送请求并输出结果
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
  "request_id": "tsk-geuaxceq61pqprmg",
  "output": [
    {
      "type": "message",
      "content": [
        {
          "type": "output_text",
          "text": "{\"taskId\":\"tsk-geuaxceq61pqprmg\"}"
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
> 提交任务成功后，`output[0].content[0].text` 中返回的 `taskId` 即为本次视频生成任务的任务 ID，请用于下一步「获取结果」接口的查询。

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
api_key = "sk-*************************************************"
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
    "input": "tsk-geuwsdb0vmkxf2px", 
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
  "request_id": "00a9600e-6ee0-47c0-b39f-080f5741ab88",
  "output": [
    {
      "type": "message",
      "content": [
        {
          "type": "output_text",
          "text": "{\"code\":0,\"message\":\"SUCCEED\",\"data\":{\"task_id\":\"tsk-geuwsdb0vmkxf2px\",\"task_status\":\"succeed\",\"task_info\":{},\"task_result\":{\"videos\":[{\"id\":\"mda-geuwti2im0n64hty\",\"url\":\"https://gcdy5vxfrcse3j396atj.exp.bcevod.com/mda-geuwti2im0n64hty/_src/mda-geuwti2im0n64hty/geuwqkc0jyuh03wq21j4.mp4\",\"duration\":\"3.041\"}]},\"task_status_msg\":\"\",\"created_at\":1779192428157,\"updated_at\":1779192542161,\"final_unit_deduction\":\"9\"},\"request_id\":\"00a9600e-6ee0-47c0-b39f-080f5741ab88\"}"
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
  ┌─ id            mda-geuwti2im0n64hty
  │  时长          3.041 秒
  │  无水印 URL    https://gcdy5vxfrcse3j396atj.exp.bcevod.com/mda-geuwti2im0n64hty/_src/mda-geuwti2im0n64hty/geuwqkc0jyuh03wq21j4.mp4
  └─
```
<p align="center">
  <small>© 2026 DMXAPI kling-v3 首尾帧生视频</small>
</p>


