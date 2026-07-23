# AICC-Doubao-Seedance-2.0 首尾帧生视频 API 使用文档

基于豆包 Seedance 2.0 模型的 AI 视频生成接口，支持输入首帧图片 + 尾帧图片 + 文本提示词生成目标视频。模型根据首尾两帧图像自动补全中间动态画面，支持自动音频生成，可选 480p / 720p / 1080p 分辨率，宽高比支持 16:9、9:16、adaptive 等 7 种规格，视频时长范围 4~15 秒。采用异步任务模式，提交后通过单次查询获取结果视频 URL。

## 🎬 模型名称

- `AICC-Doubao-Seedance-2.0`

## 🌐 接口地址

| 接口 | 请求方式 | URL |
|------|---------|-----|
| 提交任务 | POST | `https://www.dmxapi.cn/v1/responses` |
| 获取结果 | POST | `https://www.dmxapi.cn/v1/responses` |

:::warning
请妥善保管您的 API Key！严禁将密钥泄露给他人、硬编码到代码中或提交到公开的代码仓库。如果怀疑密钥已泄露，请立即前往 DMXAPI 官网重新生成。
:::


## 🎥 首尾帧生视频 示例代码

```python
import requests
import json
import base64
import os

# ╔═══════════════════════════════════════════════════════════════╗
# ║                 👇 用户配置区域 (请根据需要修改)               ║
# ╚═══════════════════════════════════════════════════════════════╝
# ═══════════════════════════════════════════════════════════════
# 🔑 API 连接信息
# ═══════════════════════════════════════════════════════════════

url = "https://www.dmxapi.cn/v1/responses"

# 🔐 DMXAPI 密钥 (请替换为您自己的密钥)
api_key = "sk-***************************************************"

# ═══════════════════════════════════════════════════════════════
# 🖼️ 图片上传方式选择
# ═══════════════════════════════════════════════════════════════

# 【upload_mode】图片上传方式
#   "base64" : 方式1 - 本地图片通过 Base64 编码上传
#   "url"    : 方式2 - 使用图片公网 URL 直接传入
upload_mode = "base64"

# ---------- 方式1: 本地图片路径 (upload_mode = "base64" 时生效) ----------
first_frame_path = r"C:\Users\a1\Pictures\1689320796087949.png"   # 首帧图片路径
last_frame_path  = r"C:\Users\a1\Pictures\20230301120626930.jpg"   # 尾帧图片路径

# ---------- 方式2: 图片公网 URL (upload_mode = "url" 时生效) ----------
# 格式要求: jpeg/png/webp/bmp/tiff/gif/heic/heif，宽高比 (0.4, 2.5)，单张 < 30 MB
first_frame_url = "https://img.shetu66.com/2023/07/14/1689320796087949.png"
last_frame_url  = "https://img.sucaijishi.com/uploadfile/2023/0301/20230301120626930.png?imageMogr2/format/jpg/blur/1x0/quality/60"

# ═══════════════════════════════════════════════════════════════
# 💬 视频生成参数
# ═══════════════════════════════════════════════════════════════

# 【model】(string, 必填) 模型 ID
model = "AICC-Doubao-Seedance-2.0"

# 【text】(string, 必填) 文本提示词，描述视频动作和镜头
# 建议中文不超过 500 字，英文不超过 1000 词
prompt_text = "图1中小狗跳到图二小狗身上，对着镜头说\"茄子\"，360度环绕运镜"

# 【generate_audio】(boolean, 可选) 是否生成同步音频，默认 true
# true: 自动生成人声、音效及背景音乐（对话建议加双引号以优化效果）
# false: 输出无声视频
generate_audio = True

# 【resolution】(string, 可选) 视频分辨率，默认 720p
# 可选值: "480p" / "720p" / "1080p"
resolution = "720p"

# 【ratio】(string, 可选) 视频宽高比，默认 adaptive
# 可选值: "16:9" / "4:3" / "1:1" / "3:4" / "9:16" / "21:9" / "adaptive"
# adaptive: 根据首帧图片比例自动选择最接近的宽高比
ratio = "adaptive"

# 【duration】(integer, 可选) 视频时长（秒），默认 5
# 取值范围: [4, 15]，仅支持范围内整数（不支持 -1 智能时长）
duration = 5

# 【seed】(integer, 可选) 随机种子，默认 -1
# 注意：Seedance 2.0 系列暂不支持指定 seed，传入后会被上游忽略
seed = -1

# 【watermark】(boolean, 可选) 是否添加水印，默认 false
watermark = False

# 【callback_url】(string, 可选) 任务状态变化时的回调通知地址
# 状态包括: queued / running / succeeded / failed / expired
callback_url = "https://www.dmxapi.cn"

# 【return_last_frame】(boolean, 可选) 是否返回生成视频的尾帧图像，默认 false
# true: 可通过查询接口获取 PNG 格式的尾帧图像（无水印，宽高与视频一致）
# 适用场景: 将尾帧作为下一段视频的首帧，实现连续视频生成
return_last_frame = False

# 【execution_expires_after】(integer, 可选) 任务超时阈值（秒），默认 172800（48小时）
# 取值范围: [3600, 259200]，超时后任务自动终止并标记为 expired
execution_expires_after = 172800

# 【tools】(array, 可选) 工具配置
# web_search: 启用联网搜索，模型自主判断是否搜索互联网内容，提升时效性但会增加时延
# 设为 True 启用，False 禁用
enable_web_search = True


# ╔═══════════════════════════════════════════════════════════════╗
# ║           👇 以下为处理逻辑，一般无需修改                       ║
# ╚═══════════════════════════════════════════════════════════════╝

# ═══════════════════════════════════════════════════════════════
# 🖼️ 本地图片转 Base64 的工具函数
# ═══════════════════════════════════════════════════════════════

def image_to_base64(image_path):
    """
    将本地图片文件转换为 Base64 编码的 Data URL 字符串

    :param image_path: 本地图片路径
    :return: 格式为 data:image/<格式>;base64,<编码> 的字符串
    """
    ext = os.path.splitext(image_path)[1].lower().lstrip(".")
    ext_map = {
        "jpg": "jpeg",
        "tif": "tiff",
    }
    ext = ext_map.get(ext, ext)
    with open(image_path, "rb") as f:
        base64_str = base64.b64encode(f.read()).decode("utf-8")
    return f"data:image/{ext};base64,{base64_str}"

# ═══════════════════════════════════════════════════════════════
# 🔄 根据上传方式获取图片 URL
# ═══════════════════════════════════════════════════════════════
if upload_mode == "base64":
    print(f"📂 使用本地图片 Base64 编码上传")
    print(f"   首帧: {first_frame_path}")
    print(f"   尾帧: {last_frame_path}")
    first_frame_image_url = image_to_base64(first_frame_path)
    last_frame_image_url = image_to_base64(last_frame_path)

elif upload_mode == "url":
    print(f"🌐 使用图片公网 URL 直接传入")
    print(f"   首帧: {first_frame_url}")
    print(f"   尾帧: {last_frame_url}")
    first_frame_image_url = first_frame_url
    last_frame_image_url = last_frame_url

else:
    raise ValueError(f"❌ 不支持的上传方式: {upload_mode}，请选择 'base64' 或 'url'")

# ═══════════════════════════════════════════════════════════════
# 📋 配置请求头
# ═══════════════════════════════════════════════════════════════

headers = {
    "Content-Type": "application/json",
    "Authorization": f"{api_key}",
}
# ═══════════════════════════════════════════════════════════════
# 📦 构建请求体
# ═══════════════════════════════════════════════════════════════

payload = {
    "model": model,
    "input": [
        {
            # 【type】(string, 必填) 内容类型，文本时固定为 text
            "type": "text",
            "text": prompt_text
        },
        {
            # 【type】(string, 必填) 内容类型，图片时固定为 image_url
            "type": "image_url",
            "image_url": {
                # 【url】(string, 必填) 图片公网 URL、Base64 编码或素材 ID
                "url": first_frame_image_url
            },
            # 【role】(string, 必填) 首尾帧场景两张图片的 role 均必填
            # first_frame: 首帧图片（以首帧宽高比为准，尾帧会自动裁剪适配；两张图片可以相同）
            "role": "first_frame"
        },
        {
            "type": "image_url",
            "image_url": {
                "url": last_frame_image_url
            },
            # last_frame: 尾帧图片
            "role": "last_frame"
        },
    ],
    "generate_audio": generate_audio,
    "resolution": resolution,
    "ratio": ratio,
    "duration": duration,
    "seed": seed,
    "watermark": watermark,
    "callback_url": callback_url,
    "return_last_frame": return_last_frame,
    "execution_expires_after": execution_expires_after,
}
# 根据配置决定是否启用联网搜索工具
if enable_web_search:
    payload["tools"] = [{"type": "web_search"}]

# ═══════════════════════════════════════════════════════════════
# 📤 发送请求并输出结果
# ═══════════════════════════════════════════════════════════════
print("\n🚀 正在发送请求...")
response = requests.post(url, headers=headers, json=payload)

print("\n📨 响应结果:")
print(json.dumps(response.json(), indent=2, ensure_ascii=False))
```

## 返回示例

```json
{
  "id": "cgt-20260721165804-z5qjx",
  "usage": {
    "total_tokens": 50000,
    "input_tokens": 0,
    "input_tokens_details": {
      "cached_tokens": 0
    },
    "output_tokens": 50000,
    "output_tokens_details": {
      "reasoning_tokens": 0
    }
  }
}
```

> 返回的 `id` 为视频生成任务 ID，保存期限为 7 天（从创建时间戳开始计算）。

## 📥 获取结果 示例代码

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
  <small>© 2026 DMXAPI AICC-Doubao-Seedance-2.0 首尾帧生视频</small>
</p>
