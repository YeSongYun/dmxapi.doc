# DMXAPI sora-2-pro 图生视频 API 使用文档

基于 OpenAI sora-2-pro 模型的图生视频接口，支持将参考图片与文本提示词结合，生成高质量 AI 视频。可生成 4 秒、8 秒或 12 秒视频，分辨率支持竖屏（720x1280）和横屏（1280x720）等多种比例。
## 模型名称

- `sora-2-pro`

## 接口地址

| 接口 | 请求方式 | URL |
|------|---------|-----|
| 提交任务 | POST | `https://www.dmxapi.cn/v1/responses` |
| 查询结果 | POST | `https://www.dmxapi.cn/v1/responses` |

## 图生视频 示例代码

```python
import io
import json
import base64
import requests
from PIL import Image

# 连接信息
URL = "https://www.dmxapi.cn/v1/responses"
API_KEY = "sk-******************************************"
image_path = r"C:/Users/a1/Desktop/sora-2/b1.png"

HEADERS = {
    "Content-Type": "application/json",
    "Authorization": API_KEY,
}

payload = {
    # 【model】(string, 必填) 模型名称
    "model": "sora-2-pro",

    # 【input】(string, 必填) 视频描述文本，描述希望生成的视频内容
    "input": "吞噬星空，罗峰变装，要求炫酷，科技感满满",

    # 【size】(string, 可选) 视频分辨率
    # 可选值: "720x1280"(竖屏 9:16) / "1280x720"(横屏 16:9) / "1024x1792" / "1792x1024"
    # 默认值: "720x1280"
    "size": "720x1280",

    # 【seconds】(string, 可选) 视频时长（秒）
    # 可选值: "4" / "8" / "12"
    # 默认值: "4"
    "seconds": "12",

    # 【input_reference】(string, 可选) 参考图片，图生视频必填
    # 支持格式: URL / base64 编码 / data URL（如 "data:image/jpeg;base64,..."）
    # 图片将被缩放裁剪至目标分辨率后作为参考帧
    "input_reference": None,  # 由下方函数填充
}


def parse_size(size_str: str) -> tuple[int, int]:
    w, h = size_str.lower().split("x")
    return int(w), int(h)


def resize_center_crop(image_path: str, target_w: int, target_h: int) -> Image.Image:
    img = Image.open(image_path)
    src_w, src_h = img.size
    scale = max(target_w / src_w, target_h / src_h)
    new_w, new_h = int(src_w * scale), int(src_h * scale)

    resample = getattr(Image, "Resampling", Image).LANCZOS
    img = img.resize((new_w, new_h), resample)

    left = (new_w - target_w) // 2
    top = (new_h - target_h) // 2
    return img.crop((left, top, left + target_w, top + target_h))


def image_file_to_data_url(image_path: str, size_str: str, quality: int = 95) -> str:
    target_w, target_h = parse_size(size_str)
    img = resize_center_crop(image_path, target_w, target_h)
    buf = io.BytesIO()
    img.convert("RGB").save(buf, format="JPEG", quality=quality)
    b64 = base64.b64encode(buf.getvalue()).decode("utf-8")
    return f"data:image/jpeg;base64,{b64}"


# 生成 input_reference 并发起请求
payload["input_reference"] = image_file_to_data_url(image_path, payload["size"])

try:
    resp = requests.post(URL, headers=HEADERS, json=payload, timeout=(10, 300))
    print(resp.status_code)
    try:
        print(json.dumps(resp.json(), indent=2, ensure_ascii=False))
    except Exception:
        print(resp.text)
except requests.RequestException as e:
    print(f"请求失败：{e}")
```

## 返回示例

```json
200
{
  "id": "eyJtb2RlbCI6InNvcmEtMi1wcm8iLCJpZCI6InZpZGVvXzY5YjQwMDM5NzAwODgxOTE5ZTRhZDNhZTAzN2I4NzJlMGUxOTEwMGI1OTAyZmU2YiJ9channel4378",
  "object": "video",
  "created_at": 1773404217,
  "status": "queued",
  "model": "sora-2-pro",
  "prompt": "吞噬星空，罗峰变装，要求炫酷，科技感满满",
  "seconds": "12",
  "size": "720x1280",
  "usage": {
    "total_tokens": 262800,
    "input_tokens": 0,
    "input_tokens_details": {
      "cached_tokens": 0
    },
    "output_tokens": 262800,
    "output_tokens_details": {
      "reasoning_tokens": 0
    }
  }
}
```

> 提交成功后，`id` 字段即为任务 ID，复制此值用于下一步查询。

## 查询结果 示例代码

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
api_key = "sk-******************************************"

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
    "input": "eyJtb2RlbCI6InNvcmEtMi1wcm8iLCJpZCI6InZpZGVvXzY5Yjc3OTBhMjg4NDgxOTE4NGRjMjJlOTdjZDA0OGI1MGVjN2ViZDYyNjg3NmMzMSJ9channel4378",
    
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
JSON 响应大小: 12991263 字节
{
  "video_base64": "[base64 数据, 长度: 12991196]",
  "content_type": "video/mp4",
  "size_bytes": 9743395
}
从字段 'video_base64' 提取 base64 数据 (长度: 12991196)
解码后视频大小: 9743395 字节
视频已保存为 video_20260316_113821.mp4
```

<p align="center">
  <small>© 2026 DMXAPI sora-2-pro 图生视频</small>
</p>
