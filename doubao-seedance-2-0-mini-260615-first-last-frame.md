# doubao-seedance-2-0-mini-260615 首尾帧生视频 API 使用文档

doubao-seedance-2-0-mini-260615 支持图生视频-首尾帧模式：输入首帧图片 + 尾帧图片 + 文本提示词（可选），生成 1 个从首帧过渡到尾帧的视频。模型支持 480p/720p 分辨率（不支持 1080p 与 4k），视频时长范围 4~15 秒，可自动生成与画面同步的人声、音效及背景音乐。视频生成采用两步异步模式：先提交任务获取任务 ID，再通过 `seedance-2-0-get` 模型查询并获取视频结果。

## 模型名称

- `doubao-seedance-2-0-mini-260615`

## 接口地址

| 接口 | 请求方式 | URL |
|------|---------|-----|
| 提交任务 | POST | `https://www.dmxapi.cn/v1/responses` |
| 获取结果 | POST | `https://www.dmxapi.cn/v1/responses` |

:::warning
请妥善保管您的 API Key！严禁将密钥泄露给他人、硬编码到代码中或提交到公开的代码仓库。
:::

## 图片输入要求

| 项目 | 要求 |
|------|------|
| 图片数量 | 2 张（首帧 + 尾帧） |
| role 字段 | **必填**：首帧为 `first_frame`，尾帧为 `last_frame` |
| 示例代码输入 | 公网 URL / 本地文件路径（程序自动读取并编码）/ 素材 ID（`asset://<ASSET_ID>`） |
| 格式 | jpeg、png、webp、bmp、tiff、gif、heic、heif |
| 宽高比（宽/高） | [0.4, 2.5] |
| 宽高长度（px） | [300, 6000] |
| 大小 | 单张图片小于 30 MB，请求体不超过 64 MB（大文件请勿使用 Base64） |

:::tip
传入的首尾帧图片可以相同。首尾帧图片的宽高比不一致时，以首帧图片为主，尾帧图片会自动裁剪适配。
:::

:::warning
seedance 2.0 系列模型不支持直接上传含有真人人脸的参考图。
图生视频-首帧、图生视频-首尾帧、多模态参考生视频为 3 种互斥场景，不可混用。
:::

## 首尾帧生视频 示例代码

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
api_key = "sk-******************************************"

# ═══════════════════════════════════════════════════════════════
# 📋 步骤2: 配置请求头
# ═══════════════════════════════════════════════════════════════

headers = {
    "Content-Type": "application/json",  # 指定请求体为 JSON 格式
    "Authorization": f"{api_key}",       # token 认证方式
}

# ═══════════════════════════════════════════════════════════════
# 🖼️ 步骤3: 配置首帧和尾帧图片来源 (每张图片三选一即可)
# ═══════════════════════════════════════════════════════════════

# 首帧图片
# first_frame_source = "https://example.com/first_frame.png"  # 网络图片 URL
first_frame_source = "C:/Users/a1/Pictures/first_frame.png"    # 本地图片路径
# first_frame_source = "asset://<ASSET_ID>"                   # 素材 ID

# 尾帧图片
# last_frame_source = "https://example.com/last_frame.png"    # 网络图片 URL
last_frame_source = "C:/Users/a1/Pictures/last_frame.png"      # 本地图片路径
# last_frame_source = "asset://<ASSET_ID>"                    # 素材 ID

# ╔═══════════════════════════════════════════════════════════════╗
# ║  ⚙️ 图片处理函数（自动识别网络 URL、本地路径或素材 ID，无需修改） ║
# ╚═══════════════════════════════════════════════════════════════╝


def resolve_image_url(source):
    """
    自动识别图片来源并返回可用于 API 请求的 URL 字符串。

    - 网络图片或素材 ID: 直接返回原值
    - 本地图片: 读取文件并转换为 Base64 Data URL
    """
    if source.startswith(("http://", "https://", "asset://")):
        return source
    if not os.path.isfile(source):
        raise FileNotFoundError(f"本地图片不存在: {source}")
    if os.path.getsize(source) >= 30 * 1024 * 1024:
        raise ValueError("本地图片必须小于 30 MB")
    ext = os.path.splitext(source)[1].lower().lstrip(".")
    ext = {"jpg": "jpeg", "tif": "tiff"}.get(ext, ext)
    if ext not in {"jpeg", "png", "webp", "bmp", "tiff", "gif", "heic", "heif"}:
        raise ValueError(f"不支持的图片格式: {ext or '无扩展名'}")
    with open(source, "rb") as f:
        base64_data = base64.b64encode(f.read()).decode("utf-8")
    return f"data:image/{ext};base64,{base64_data}"


# ═══════════════════════════════════════════════════════════════
# 💬 步骤4: 配置请求参数
# ═══════════════════════════════════════════════════════════════

payload = {
    # 【model】(string, 必填) 模型名称，指定使用 doubao-seedance-2-0-mini 模型
    "model": "doubao-seedance-2-0-mini-260615",

    # 【input】(array, 必填) 输入内容数组
    # 首尾帧生视频需传入 2 个 type=image_url 的对象，且 role 必填
    # 可同时传入一个 type=text 的对象作为文本提示词（可选）
    # 提示词建议中文不超过500字，英文不超过1000词
    # 额外支持西班牙语、印度尼西亚语、葡萄牙语、日语
    "input": [
        {
            "type": "text",
            "text": "镜头平稳推进，画面自然过渡，光线由清晨转为正午",
        },
        {
            # 【image_url.url】自动解析首帧的网络 URL、本地图片路径或素材 ID
            "type": "image_url",
            "image_url": {
                "url": resolve_image_url(first_frame_source)
            },
            # 【role】(string, 必填) 首帧图片固定为 "first_frame"
            "role": "first_frame",
        },
        {
            # 【image_url.url】自动解析尾帧的网络 URL、本地图片路径或素材 ID
            "type": "image_url",
            "image_url": {
                "url": resolve_image_url(last_frame_source)
            },
            # 【role】(string, 必填) 尾帧图片固定为 "last_frame"
            "role": "last_frame",
        },
    ],

    # 【ratio】(string, 可选) 视频宽高比，默认值 adaptive
    # 可选值: "16:9" / "4:3" / "1:1" / "3:4" / "9:16" / "21:9" / "adaptive"
    # "adaptive": 由模型根据首帧图在可选宽高比中自动选择
    # 注意: 指定的宽高比与图片不一致时，方舟会对图片进行居中裁剪
    "ratio": "adaptive",

    # 【resolution】(string, 可选) 视频分辨率，默认值 720p
    # 可选值: "480p" / "720p"（seedance 2.0 mini 不支持 1080p 和 4k）
    "resolution": "720p",

    # 【duration】(integer, 可选) 视频时长（秒）
    # 取值范围: [4, 15]，或 -1 由模型在有效范围内自主选择合适时长
    # 传 -1 时按 15 秒预扣费，实际时长确定后多退少补
    # 注意: 视频时长与计费相关，请谨慎设置
    "duration": 5,

    # 【generate_audio】(boolean, 可选) 是否生成同步音频（人声/音效/背景音乐），默认值 true
    # true: 模型自动生成与画面匹配的人声、音效及背景音乐
    # false: 输出无声视频
    # 注意: 生成的有声视频均为单声道
    "generate_audio": True,

    # 【seed】(integer, 可选) 随机种子，默认值 -1
    # 取值范围: [-1, 2147483647]；-1 表示使用随机数
    "seed": -1,

    # 【watermark】(boolean, 可选) 是否包含水印，默认值 false
    # true: 生成视频右下角展示「AI 生成」水印
    "watermark": False,

    # 【return_last_frame】(boolean, 可选) 是否返回视频尾帧图像，默认值 false
    # true: 返回尾帧图像（png 格式，宽高与视频一致，无水印）
    "return_last_frame": False,

    # 【execution_expires_after】(integer, 可选) 任务超时时间（秒）
    # 取值范围: [3600, 259200]，默认 172800（48小时）
    # 从 created_at 开始计算，超时后任务终止并标记为 expired
    "execution_expires_after": 172800,

    # 【callback_url】(string, 可选) 任务状态回调地址
    # 状态说明: queued(排队中) / running(运行中) / succeeded(成功) / failed(失败) / expired(超时)
    "callback_url": "https://www.dmxapi.cn",

    # 【tools】(array, 可选) 工具配置，开启联网搜索
    # web_search: 模型根据提示词自主判断是否搜索互联网内容，可提升视频时效性但增加时延
    "tools": [{"type": "web_search"}],
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
  "id": "cgt-20260820141507-hj3vn",
  "usage": {
    "total_tokens": 11500,
    "input_tokens": 0,
    "input_tokens_details": {
      "cached_tokens": 0
    },
    "output_tokens": 11500,
    "output_tokens_details": {
      "reasoning_tokens": 0
    }
  }
}
```

> 返回的 `id` 字段即为任务 ID，用于第二步查询视频生成结果。

## 获取结果 示例代码

```python
import requests
import json

url = "https://www.dmxapi.cn/v1/responses"

# DMXAPI 密钥 (请替换为您自己的密钥)
api_key = "sk-******************************************"

headers = {
    "Content-Type": "application/json",
    # 获取结果接口使用 Bearer 认证方式
    "Authorization": f"Bearer {api_key}",
}

payload = {
    # 【model】(string, 必填) 查询模型，固定为 seedance-2-0-get
    "model": "seedance-2-0-get",

    # 【input】(string, 必填) 第一步提交任务返回的任务 ID
    "input": "cgt-20260820141507-hj3vn"
}

response = requests.post(url, headers=headers, json=payload)
result = response.json()

# 用量与计费：output_tokens 即本次实际扣费依据
print("用量:")
print(json.dumps(result.get("usage", {}), indent=2, ensure_ascii=False))

# 解析任务详情与视频链接
try:
    text = result["output"][0]["content"][0]["text"]
    inner = json.loads(text)

    # 格式化打印任务详情：含实际生成参数（时长/分辨率/宽高比/随机种子/帧率等）
    # text 本身是被转义的 JSON 字符串，直接打印会挤成一行，需先 json.loads 再格式化
    print("\n任务详情:")
    print(json.dumps(inner, indent=2, ensure_ascii=False))

    video_url = inner["content"]["video_url"]
    print(f"\n视频链接: {video_url}")
    last_frame_url = inner["content"].get("last_frame_url")
    if last_frame_url:
        print(f"尾帧图像: {last_frame_url}")
except Exception as e:
    print(f"提取 URL 失败: {e}")
```

## 返回示例

```json
{
  "request_id": "cgt-20260820141507-hj3vn",
  "output": [
    {
      "type": "message",
      "content": [
        {
          "type": "output_text",
          "text": "{\"content\":{\"video_url\":\"https://ark-acg-cn-beijing.tos-cn-beijing.volces.com/doubao-seedance-2-0-mini/02178746310700000000000000000000000ffffac1834d5e08c2.mp4?X-Tos-Algorithm=TOS4-HMAC-SHA256\\u0026X-Tos-Credential=AKLTYWJkZTExNjA1ZDUyNDc3YzhjNTM5OGIyNjBhNDcyOTQ%2F20260820%2Fcn-beijing%2Ftos%2Frequest\\u0026X-Tos-Date=20260820T061507Z\\u0026X-Tos-Expires=86400\\u0026X-Tos-Signature=c3d4e5f60718293a4b5c6d7e8f90a1b2c3d4e5f60718293a4b5c6d7e8f90a1b2\\u0026X-Tos-SignedHeaders=host\"},\"id\":\"cgt-20260820141507-hj3vn\",\"model\":\"doubao-seedance-2-0-mini-260615\",\"status\":\"succeeded\"}"
        }
      ]
    }
  ],
  "usage": {
    "total_tokens": 11500,
    "input_tokens": 0,
    "input_tokens_details": {
      "cached_tokens": 0
    },
    "output_tokens": 11500,
    "output_tokens_details": {
      "reasoning_tokens": 0
    }
  }
}

视频链接: https://ark-acg-cn-beijing.tos-cn-beijing.volces.com/doubao-seedance-2-0-mini/02178746310700000000000000000000000ffffac1834d5e08c2.mp4?X-Tos-Algorithm=TOS4-HMAC-SHA256&X-Tos-Credential=AKLTYWJkZTExNjA1ZDUyNDc3YzhjNTM5OGIyNjBhNDcyOTQ%2F20260820%2Fcn-beijing%2Ftos%2Frequest&X-Tos-Date=20260820T061507Z&X-Tos-Expires=86400&X-Tos-Signature=c3d4e5f60718293a4b5c6d7e8f90a1b2c3d4e5f60718293a4b5c6d7e8f90a1b2&X-Tos-SignedHeaders=host
```

<p align="center">
  <small>© 2026 DMXAPI doubao-seedance-2-0-mini-260615 首尾帧生视频</small>
</p>
