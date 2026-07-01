# happyhorse-1.0-video-edit-15s 视频编辑 API 使用文档

> **计费说明：** 该模型视频编辑固定计费 **13.5 元 / 条**，与输出的视频时长和分辨率无关。

HappyHorse 视频编辑模型支持输入视频与参考图，结合文本指令完成风格变换、局部替换等编辑任务。采用异步两步调用方式：先提交任务获取任务 ID，再轮询查询任务状态并获取编辑后的视频链接。输出视频时长最长 15 秒，支持 720P 与 1080P 两种分辨率，可选保留原始声音或由模型自动生成音效，适用于人物换装、场景风格迁移、局部内容替换等多种视频创意编辑场景。

## 模型名称

- `happyhorse-1.0-video-edit-15s`

## 接口地址

| 接口 | 请求方式 | URL |
|------|---------|-----|
| 提交任务 | POST | `https://www.dmxapi.cn/v1/responses` |
| 获取结果 | POST | `https://www.dmxapi.cn/v1/responses` |

:::warning
请妥善保管您的 API Key！严禁将密钥泄露给他人、硬编码到代码中或提交到公开的代码仓库。
:::

## 视频编辑请求 示例代码

```python
import requests
import json
import base64
import os


# ═══════════════════════════════════════════════════════════════
# 🔑 步骤1: 配置 API 连接信息
# ═══════════════════════════════════════════════════════════════

# 🌐 DMXAPI 服务端点地址
url = "https://www.dmxapi.cn/v1/responses"

# 🔐 DMXAPI 密钥 (请替换为您自己的密钥)
# 获取方式: 登录 DMXAPI 官网 -> 个人中心 -> API 密钥管理
api_key = "sk-**********************************************"

# ═══════════════════════════════════════════════════════════════
# 📋 步骤2: 配置请求头
# ═══════════════════════════════════════════════════════════════

headers = {
    "Content-Type": "application/json",      # 指定请求体为 JSON 格式
    "Authorization": f"{api_key}",           # token 认证方式
}

# ═══════════════════════════════════════════════════════════════
# 📁 步骤3: 配置参考图片来源 (二选一即可)
# ═══════════════════════════════════════════════════════════════

# 【方式一】本地图片路径 (请替换为您自己的图片路径)
reference_image_source = "C:/Users/a1/Pictures/wan-video-edit-clothes-1.webp"

# 【方式二】网络图片 URL (支持 HTTP / HTTPS 协议)
# reference_image_source = "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260415/hynnff/wan-video-edit-clothes.webp"


# ╔═══════════════════════════════════════════════════════════════╗
# ║        ⚙️ 图片处理逻辑（无需修改）                              ║
# ╚═══════════════════════════════════════════════════════════════╝

MIME_TYPE_MAP = {
    ".jpg": "image/jpeg", ".jpeg": "image/jpeg",
    ".png": "image/png",  ".webp": "image/webp",
}

def image_to_base64(image_path):
    ext = os.path.splitext(image_path)[1].lower()
    if ext not in MIME_TYPE_MAP:
        raise ValueError(f"不支持的图片格式: {ext}，仅支持: {list(MIME_TYPE_MAP.keys())}")
    mime_type = MIME_TYPE_MAP[ext]
    with open(image_path, "rb") as f:
        base64_data = base64.b64encode(f.read()).decode("utf-8")
    return f"data:{mime_type};base64,{base64_data}"

def resolve_image_url(image):
    if image.startswith("http://") or image.startswith("https://"):
        return image
    return image_to_base64(image)

reference_image_url = resolve_image_url(reference_image_source)


# ═══════════════════════════════════════════════════════════════
# 💬 步骤4: 配置请求参数
# ═══════════════════════════════════════════════════════════════

payload = {
    # 【model】(string, 必选) 模型名称
    # 固定值，使用 happyhorse-1.0-video-edit-15s 进行视频编辑
    "model": "happyhorse-1.0-video-edit-15s",

    # 【input】(array, 必选) 输入信息，包括待编辑的视频、参考图片和提示词
    "input": [{
        # 【prompt】(string, 必选) 文本提示词，描述对视频的编辑意图（如风格转换、局部替换）
        # 支持任何语言输入，最长 5000 个非中文字符或 2500 个中文字符，超出部分自动截断
        "prompt": "让视频中的马头人身角色穿上图片中的条纹毛衣",

        # 【media】(array, 必选) 媒体素材列表，指定待编辑的视频和参考图像
        # 必须包含 1 个 video 类型元素；可选包含 0~5 个 reference_image 类型元素
        "media": [
            {
                # 【type】(string, 必选) 媒体素材类型
                # 可选值: "video"（必传，待编辑的视频）/ "reference_image"（可选，参考图像）
                "type": "video",
                # 【url】(string, 必选) 待编辑视频的公网可访问 URL
                # 视频要求: 格式 MP4/MOV（建议 H.264 编码），时长 3~60 秒
                # 分辨率: 长边不超过 4096px，短边不小于 360px，宽高比 1:2.5~2.5:1
                # 文件大小不超过 100MB，帧率大于 8fps
                # 输出时长: 3~15 秒（超过 15 秒的输入自动截取前 15 秒作为有效片段）
                "url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260409/dozxak/Wan_Video_Edit_33_1.mp4"
            },
            {
                # 【type】(string, 必选) 媒体素材类型，此处为参考图像
                "type": "reference_image",
                # 【url】(string, 必选) 参考图像地址
                # 既可以是公网 URL，也可以是本地图片转换后的 Base64 Data URL
                # 图像要求: 格式 JPEG/JPG/PNG/WEBP，宽高尺寸不小于 300px
                # 宽高比 1:2.5~2.5:1，文件大小不超过 20MB
                "url": reference_image_url
            }
        ]
    }],

    # 【parameters】(object, 可选) 视频编辑参数
    "parameters": {
        # 【resolution】(string, 可选) 生成视频的分辨率档位
        # 可选值: "1080P"（默认值）/ "720P"
        "resolution": "720P",

        # 【audio_setting】(string, 可选) 声音控制
        # 可选值: "auto"（默认值，由模型自行控制）/ "origin"（保留输入视频的原始声音）
        "audio_setting": "auto",

        # 【watermark】(boolean, 可选) 是否在生成视频上添加水印标识
        # 水印位于视频右下角，文案固定为 "Happy Horse"
        # 可选值: true（默认值，添加水印）/ false（不添加水印）
        "watermark": True,

        # 【seed】(integer, 可选) 随机数种子，取值范围 [0, 2147483647]
        # 未指定时系统自动生成随机种子；固定 seed 值可提升结果可复现性
        # 注意: 由于模型生成具有概率性，相同 seed 不保证每次结果完全一致
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
  "request_id": "ae9d104d-c0f8-9b55-8825-1aac95620735",
  "output": [
    {
      "type": "message",
      "content": [
        {
          "type": "output_text",
          "text": "{\"task_id\":\"75719032-e04d-4c2c-91f4-bc7cb6b444fe\",\"task_status\":\"PENDING\"}"
        }
      ]
    }
  ],
  "usage": {
    "input_tokens": 0,
    "input_tokens_details": {
      "cached_tokens": 0
    },
    "output_tokens": 135000,
    "output_tokens_details": {
      "reasoning_tokens": 0
    },
    "total_tokens": 135000
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
# 获取方式: 登录 DMXAPI 官网 -> 个人中心 -> API 密钥管理
api_key = "sk-******************************************"

# ═══════════════════════════════════════════════════════════════
# 步骤2: 配置请求头
# ═══════════════════════════════════════════════════════════════

headers = {
    "Content-Type": "application/json",   # 指定请求体为 JSON 格式
    "Authorization": f"{api_key}",        # token 认证方式
}

# ═══════════════════════════════════════════════════════════════
# 步骤3: 配置请求参数
# ═══════════════════════════════════════════════════════════════

payload = {
    # 【model】(string, 必选) 查询任务使用的模型名称，固定为 happyhorse-get
    "model": "happyhorse-get",

    # 【input】(string, 必选) 提交任务时返回的 task_id，用于查询任务状态与结果
    # task_id 有效期为 24 小时，超时后将无法查询（接口返回状态 UNKNOWN）
    # 任务状态枚举: PENDING(排队中) / RUNNING(处理中) / SUCCEEDED(成功) / FAILED(失败) / CANCELED(已取消) / UNKNOWN(不存在或已过期)
    # 视频生成通常需要 1~5 分钟，建议每隔约 15 秒轮询一次（重新执行本步骤），直到状态变为 SUCCEEDED；请勿重复创建任务
    "input": "62967e89-6174-4d38-9828-aedd2c5d151f"
}

# ═══════════════════════════════════════════════════════════════
# 步骤4: 发送请求并输出结果
# ═══════════════════════════════════════════════════════════════

# 发送 POST 请求到 API 服务器
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
        # 注意：video_url 有效期为 24 小时，请及时下载并转存至本地或永久存储（如 OSS）
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
          "text": "{\"task_id\":\"62967e89-6174-4d38-9828-aedd2c5d151f\",\"task_status\":\"SUCCEEDED\",\"submit_time\":\"2026-04-28 14:26:42.286\",\"scheduled_time\":\"2026-04-28 14:26:42.330\",\"end_time\":\"2026-04-28 14:28:24.417\",\"video_url\":\"https://dashscope-a717.oss-accelerate.aliyuncs.com/...\"}"
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
https://dashscope-a717.oss-accelerate.aliyuncs.com/...（有效期链接，需尽快下载）
```

<p align="center">
  <small>© 2026 DMXAPI happyhorse-1.0-video-edit-15s 视频编辑</small>
</p>
