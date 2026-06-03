# happyhorse-1.0-i2v 首帧生视频 API 使用文档

HappyHorse 首帧生视频模型以首帧图片为基础，支持通过文本提示词进行引导，生成物理真实、运动流畅的视频。调用采用异步方式，任务通常需要 1–5 分钟完成；支持分辨率档位调节（720P）、时长设置（3–15 秒）、水印控制及随机种子固定，可满足多样化的图生视频应用需求。

## 模型名称

- `happyhorse-1.0-i2v`

## 接口地址

| 接口 | 请求方式 | URL |
|------|---------|-----|
| 提交任务 | POST | `https://www.dmxapi.cn/v1/responses` |
| 获取结果 | POST | `https://www.dmxapi.cn/v1/responses` |

:::warning
请妥善保管您的 API Key！严禁将密钥泄露给他人、硬编码到代码中或提交到公开的代码仓库。
:::

## 首帧生视频 示例代码

```python
import requests
import json
import base64
import mimetypes


# ═══════════════════════════════════════════════════════════════
# 🔑 步骤1: 配置 API 连接信息
# ═══════════════════════════════════════════════════════════════

# 🌐 DMXAPI 服务端点地址
url = "https://www.dmxapi.cn/v1/responses"

# 🔐 DMXAPI 密钥 (请替换为您自己的密钥)
# 获取方式: 登录 DMXAPI 官网 -> 个人中心 -> API 密钥管理
api_key = "sk-******************************************"

# ═══════════════════════════════════════════════════════════════
# 📋 步骤2: 配置请求头
# ═══════════════════════════════════════════════════════════════

headers = {
    "Content-Type": "application/json",      # 指定请求体为 JSON 格式
    "Authorization": f"{api_key}",           # token 认证方式
}

# ═══════════════════════════════════════════════════════════════
# 📁 步骤3: 选择图片来源 (二选一即可)
# ═══════════════════════════════════════════════════════════════

# 【方式一】本地图片路径 (请替换为您自己的图片路径)
# image_source = "C:/Users/a1/Pictures/1689320796087949.png"

# 【方式二】网络图片 URL (支持 HTTP / HTTPS 协议)
# 格式: JPEG、JPG、PNG、WEBP；宽高比: 1:2.5～2.5:1
image_source = "https://cdn.translate.alibaba.com/r/wanx-demo-1.png"


# ╔═══════════════════════════════════════════════════════════════╗
# ║          ⚙️ 图片处理逻辑（无需修改）                            ║
# ╚═══════════════════════════════════════════════════════════════╝

def image_to_base64(image_path):
    mime_map = {
        ".jpg":  "image/jpeg",
        ".jpeg": "image/jpeg",
        ".png":  "image/png",
        ".webp": "image/webp",
    }
    ext = "." + image_path.rsplit(".", 1)[-1].lower()
    mime_type = mime_map.get(ext)
    if mime_type is None:
        mime_type = mimetypes.guess_type(image_path)[0] or "image/png"
    with open(image_path, "rb") as f:
        base64_data = base64.b64encode(f.read()).decode("utf-8")
    return f"data:{mime_type};base64,{base64_data}"

def get_image_url(image_source):
    if image_source.lower().startswith(("http://", "https://")):
        return image_source
    else:
        return image_to_base64(image_source)

image_url = get_image_url(image_source)


# ═══════════════════════════════════════════════════════════════
# 💬 步骤4: 配置请求参数
# ═══════════════════════════════════════════════════════════════

payload = {
    # 【model】(string, 必填) 指定使用的首帧图生视频模型
    "model": "happyhorse-1.0-i2v",
    "input": [{
        # 【prompt】(string, 可选) 文本提示词，用于描述期望生成的视频内容
        # 支持任何语言输入，长度不超过5000个非中文字符或2500个中文字符，超过部分将自动截断。
        "prompt": "一只猫在草地上奔跑",
        "media": [
            {
                # 【type】(string, 必填) 媒体素材类型
                # 可选值: "first_frame"(以此图作为视频首帧)
                # 素材限制：有且仅有 1 张首帧图像
                "type": "first_frame",
                # 【url】(string, 必填) 首帧图像的 URL
                # 兼容两种格式:
                #   1. 网络图像 URL (支持 HTTP 或 HTTPS 协议)
                #   2. 本地图像 Base64 Data URL (data:image/png;base64,xxxxxx)
                # 格式：JPEG、JPG、PNG、WEBP
                # 宽高比：1:2.5～2.5:1
                "url": image_url
            }
        ]
    }],
    "parameters": {
        # 【resolution】(string, 可选) 指定生成的视频分辨率档位，用于控制视频的清晰度（总像素）
        # 模型根据选择的分辨率档位，自动缩放至相近总像素
        # 输出的视频宽高比与输入首帧近似一致
        # 可选值: "720P"(标准高清)
        "resolution": "720P",
        # 【duration】(integer, 可选) 指定生成视频的时长，单位为秒
        # 取值范围: [3, 15] 之间的整数
        "duration": 5,
        # 【watermark】(boolean, 可选) 是否在生成的视频上添加水印标识
        # 水印位于视频右下角，文案固定为 "Happy Horse"
        # true: 默认值，添加水印；false: 不添加水印
        "watermark": True,
        # 【seed】(integer, 可选) 随机数种子，用于提升生成结果的可复现性
        # 取值范围: [0, 2147483647]
        # 未指定时系统自动生成随机种子；即使固定 seed，也不能保证每次结果完全一致
        "seed": 11
    }
}


# ═══════════════════════════════════════════════════════════════
# 📤 步骤5: 发送请求并输出结果
# ═══════════════════════════════════════════════════════════════

response = requests.post(url, headers=headers, json=payload)
print(json.dumps(response.json(), indent=2, ensure_ascii=False))
```

## 返回示例

```json
{
  "request_id": "8239652d-f3ec-9c8f-a787-4d0f14c36580",
  "output": [
    {
      "type": "message",
      "content": [
        {
          "type": "output_text",
          "text": "{\"task_id\":\"346a4285-e244-4a0e-ba53-c887bdb239fe\",\"task_status\":\"PENDING\"}"
        }
      ]
    }
  ],
  "usage": {
    "input_tokens": 0,
    "input_tokens_details": {
      "cached_tokens": 0
    },
    "output_tokens": 45000,
    "output_tokens_details": {
      "reasoning_tokens": 0
    },
    "total_tokens": 45000
  }
}
```

## 获取结果 示例代码

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
    "Authorization": f"{api_key}",
}

# ═══════════════════════════════════════════════════════════════
# 步骤3: 配置请求参数
# ═══════════════════════════════════════════════════════════════

payload = {
    # 【model】(string, 必填) 查询视频生成任务结果的专用模型
    "model": "happyhorse-get",
    # 【input】(string, 必填) 提交任务时返回的 task_id，用于查询任务状态与结果
    # task_id 有效期为 24 小时，超时后将无法查询（接口返回状态 UNKNOWN）
    # 任务状态枚举: PENDING(排队中) / RUNNING(处理中) / SUCCEEDED(成功) / FAILED(失败) / CANCELED(已取消) / UNKNOWN(不存在或已过期)
    "input": "62967e89-6174-4d38-9828-aedd2c5d151f"
}

# ═══════════════════════════════════════════════════════════════
# 步骤4: 发送请求并输出结果
# ═══════════════════════════════════════════════════════════════

response = requests.post(url, headers=headers, json=payload)

data = response.json()
print(json.dumps(data, indent=2, ensure_ascii=False))

# 提取 video_url（嵌套在 output[0].content[0].text 的 JSON 字符串里）
try:
    text = data["output"][0]["content"][0]["text"]
    inner = json.loads(text)
    video_url = inner.get("video_url")
    if video_url:
        print("\n视频链接:")
        print(video_url)
    else:
        print("\n未找到 video_url，任务状态:", inner.get("task_status"))
except (KeyError, IndexError, json.JSONDecodeError) as e:
    print("\n解析 video_url 失败:", e)
```

### 返回示例

```json
{
  "request_id": "a011c69c-ef4a-9903-a89e-78f72c9ef33c",
  "output": [
    {
      "type": "message",
      "content": [
        {
          "type": "output_text",
          "text": "{\"task_id\":\"62967e89-6174-4d38-9828-aedd2c5d151f\",\"task_status\":\"SUCCEEDED\",\"submit_time\":\"2026-04-28 14:26:42.286\",\"scheduled_time\":\"2026-04-28 14:26:42.330\",\"end_time\":\"2026-04-28 14:28:24.417\",\"video_url\":\"https://dashscope-a717.oss-accelerate.aliyuncs.com/...mp4\"}"
        }
      ]
    }
  ],
  "usage": {
    "input_tokens": 0,
    "input_tokens_details": {
      "cached_tokens": 0
    },
    "output_tokens": 0,
    "output_tokens_details": {
      "reasoning_tokens": 0
    },
    "total_tokens": 0
  }
}

视频链接:
https://dashscope-a717.oss-accelerate.aliyuncs.com/...mp4
```

<p align="center">
  <small>© 2026 DMXAPI happyhorse-1.0-i2v 首帧生视频</small>
</p>
