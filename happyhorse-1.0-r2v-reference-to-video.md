# happyhorse-1.0-r2v 参考生视频 API 使用文档

HappyHorse-参考生视频模型支持传入多张参考图像，通过文本提示词描述场景，将图像中的主体角色融合生成一段流畅的视频。模型可理解 character1、character2 等参考指代标识，将不同图像中的角色自然融入同一视频场景。视频支持 720P/1080P 分辨率、9 种宽高比（16:9/9:16/3:4/4:3/1:1/4:5/5:4/9:21/21:9）、3~15 秒时长，任务通常在 1~5 分钟内完成，采用异步模式提交后通过任务 ID 轮询获取结果。

## 模型名称

- `happyhorse-1.0-r2v`

## 接口地址

| 接口 | 请求方式 | URL |
|------|---------|-----|
| 提交任务 | POST | `https://www.dmxapi.cn/v1/responses` |
| 获取结果 | POST | `https://www.dmxapi.cn/v1/responses` |

:::warning
请妥善保管您的 API Key！严禁将密钥泄露给他人、硬编码到代码中或提交到公开的代码仓库。
:::

## 参考生视频 示例代码

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
api_key = "sk-***************************************************"

# ═══════════════════════════════════════════════════════════════
# 📋 步骤2: 配置请求头
# ═══════════════════════════════════════════════════════════════

headers = {
    "Content-Type": "application/json",      # 指定请求体为 JSON 格式
    "Authorization": f"{api_key}",           # token 认证方式
}

# ═══════════════════════════════════════════════════════════════
# 📁 步骤3: 配置参考图片来源 (本地路径 或 公网URL 任意混用)
# ═══════════════════════════════════════════════════════════════

# 按照数组顺序定义 prompt 中角色引用的顺序:
#   第 1 个对应 [Image 1], 第 2 个对应 [Image 2], 以此类推
# 参考图像数量限制: 1~9 张
# 参考图像要求: 格式 JPEG/JPG/PNG/WEBP; 短边 ≥ 300px; 单张 ≤ 20MB; 支持公网 URL 或 Base64
#
# 每个元素既可以是本地文件路径, 也可以是公网 URL 地址, 程序会自动识别:
#   - 本地路径示例: "C:/Users/15664/Desktop/hh-v2v-girl.jpg"
#   - 公网 URL 示例: "https://xxx/xxx.jpg"
reference_image_sources = [
    # 示例1: 本地图片路径 (请替换为您自己的图片路径)
    "C:/Users/a1/Pictures/hh-v2v-girl01.jpg",

    # 示例2: 公网 URL 地址 (与本地路径可混用)
    "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260424/fvuihk/hh-v2v2-folding-fan.jpg",

    # 示例3: 本地图片路径
    "C:/Users/a1/Pictures/hh-v2v-earrings03.jpg",
]


# ╔═══════════════════════════════════════════════════════════════╗
# ║        ⚙️ 图片处理逻辑（无需修改）                              ║
# ╚═══════════════════════════════════════════════════════════════╝

def image_to_base64(image_path):
    mime_map = {
        ".jpg": "image/jpeg", ".jpeg": "image/jpeg",
        ".png": "image/png",  ".webp": "image/webp",
    }
    ext = "." + image_path.rsplit(".", 1)[-1].lower()
    mime_type = mime_map.get(ext)
    if mime_type is None:
        mime_type = mimetypes.guess_type(image_path)[0] or "image/png"
    with open(image_path, "rb") as f:
        base64_data = base64.b64encode(f.read()).decode("utf-8")
    return f"data:{mime_type};base64,{base64_data}"

def build_image_url(image_source):
    src = image_source.strip()
    if src.lower().startswith(("http://", "https://")):
        return src
    else:
        return image_to_base64(src)

media_list = []
for source in reference_image_sources:
    media_list.append({
        "type": "reference_image",
        "url": build_image_url(source),
    })


# ═══════════════════════════════════════════════════════════════
# 💬 步骤4: 配置请求参数
# ═══════════════════════════════════════════════════════════════

payload = {
    # 【model】(string, 必选) 模型名称, 固定值: happyhorse-1.0-r2v
    "model": "happyhorse-1.0-r2v",

    # 【input】(array, 必选) 输入的基本信息, 包括参考图像和提示词
    "input": [{
        # 【prompt】(string, 必选) 文本提示词
        # 支持任何语言, 长度不超过 5000 个非中文字符或 2500 个中文字符
        # 注意! prompt 中必须明确标明 [Image 1]、[Image 2] 等, 否则模型会报错
        "prompt": (
            "[Image 1]中身着红色旗袍的女性，镜头先以侧面中景勾勒旗袍修身剪裁与S型曲线，"
            "随即切换至低角度仰拍，捕捉她轻抬玉手展开[Image 2]中的折扇的同时，"
            "[Image 3]中的流苏耳坠随头部转动轻盈摆动的细节，最后推近至面部特写，"
            "定格在她指尖轻点扇骨、眼波流转间的含蓄风情，多视角全方位展现东方韵味。"
        ),

        # 【media】(array, 必选) 媒体素材列表
        # 由步骤3的 reference_image_sources 自动构建, 无需手动修改
        "media": media_list,
    }],

    # 【parameters】(object, 可选) 视频生成参数
    "parameters": {
        # 【resolution】(string, 可选) 分辨率档位: "1080P"(默认) / "720P"
        "resolution": "720P",
        # 【ratio】(string, 可选) 宽高比: "16:9"(默认)/"9:16"/"3:4"/"4:3"/"1:1"/"4:5"/"5:4"/"9:21"/"21:9"
        "ratio": "16:9",
        # 【duration】(integer, 可选) 时长(秒), 取值 3~15, 默认 5
        "duration": 3,
        # 【watermark】(boolean, 可选) 是否添加水印, true(默认)/false
        # 水印位于视频右下角, 文案固定为 "Happy Horse"
        "watermark": True,
        # 【seed】(integer, 可选) 随机数种子, 取值 [0, 2147483647]
        # 固定 seed 可提升结果可复现性 (但不保证完全一致)
        "seed": 11,
    },
}


# ═══════════════════════════════════════════════════════════════
# 📤 步骤5: 发送请求并输出结果
# ═══════════════════════════════════════════════════════════════

response = requests.post(url, headers=headers, json=payload)
print(json.dumps(response.json(), indent=2, ensure_ascii=False))
```

### 返回示例

```json
{
  "request_id": "3adf70fc-8ad8-98b2-b56e-b5741e21fd58",
  "output": [
    {
      "type": "message",
      "content": [
        {
          "type": "output_text",
          "text": "{\"task_id\":\"f6801082-d1f5-470b-b81e-74360fe72d29\",\"task_status\":\"PENDING\"}"
        }
      ]
    }
  ],
  "usage": {
    "input_tokens": 0,
    "input_tokens_details": {
      "cached_tokens": 0
    },
    "output_tokens": 27000,
    "output_tokens_details": {
      "reasoning_tokens": 0
    },
    "total_tokens": 27000
  }
}
```

## 获取结果 示例代码

```python
import requests
import json

# 步骤1: 配置 API 连接信息
# DMXAPI 服务端点地址
url = "https://www.dmxapi.cn/v1/responses"

# DMXAPI 密钥 (请替换为您自己的密钥)
api_key = "sk-******************************************"

# 步骤2: 配置请求头
headers = {
    "Content-Type": "application/json",      # 指定请求体为 JSON 格式
    "Authorization": f"{api_key}",           # token 认证方式
}

# 步骤3: 配置请求参数
payload = {
    # 【model】(string, 必选) 查询模型名称
    # 固定值: happyhorse-get，用于查询 happyhorse-1.0-r2v 提交的任务结果
    "model": "happyhorse-get",
    # 【input】(string, 必选) 提交任务时返回的 task_id，用于查询任务状态与结果
    # task_id 有效期为 24 小时，超时后将无法查询（接口返回状态 UNKNOWN）
    # 任务状态枚举: PENDING(排队中) / RUNNING(处理中) / SUCCEEDED(成功) / FAILED(失败) / CANCELED(已取消) / UNKNOWN(不存在或已过期)
    # 视频生成通常需要 1~5 分钟，建议每隔约 15 秒轮询一次（重新执行本步骤），直到状态变为 SUCCEEDED；请勿重复创建任务
    "input": "62967e89-6174-4d38-9828-aedd2c5d151f"
}

# 步骤4: 发送请求并输出结果
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
          "text": "{\"task_id\":\"62967e89-6174-4d38-9828-aedd2c5d151f\",\"task_status\":\"SUCCEEDED\",\"submit_time\":\"2026-04-28 14:26:42.286\",\"scheduled_time\":\"2026-04-28 14:26:42.330\",\"end_time\":\"2026-04-28 14:28:24.417\",\"video_url\":\"https://dashscope-a717.oss-accelerate.aliyuncs.com/1d/8a/20260428/17ae637c/51496466-metadata_video_720p_62967e89-6174-4d38-9828-aedd2c5d151f_refiner_watermark.mp4?Expires=1777444103&OSSAccessKeyId=LTAI5tPxpiCM2hjmWrFXrym1&Signature=pi9SIKuTr00DfRgkUfUyYpNRsVk%3D\"}"
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
https://dashscope-a717.oss-accelerate.aliyuncs.com/1d/8a/20260428/17ae637c/51496466-metadata_video_720p_62967e89-6174-4d38-9828-aedd2c5d151f_refiner_watermark.mp4?Expires=1777444103&OSSAccessKeyId=LTAI5tPxpiCM2hjmWrFXrym1&Signature=pi9SIKuTr00DfRgkUfUyYpNRsVk%3D
```

<p align="center">
  <small>© 2026 DMXAPI happyhorse-1.0-r2v 参考生视频</small>
</p>
