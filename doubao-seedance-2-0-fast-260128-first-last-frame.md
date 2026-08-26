# doubao-seedance-2-0-fast-260128 首尾帧生视频 API 使用文档

基于 doubao-seedance-2-0-fast-260128 模型的 AI 视频生成接口，支持输入首帧图片 + 尾帧图片 + 文本提示词生成目标视频。模型根据首尾两帧图像自动补全中间动态画面，支持自动音频生成，可选 480p / 720p 分辨率（不支持 1080p 与 4k），宽高比支持 16:9、9:16、adaptive 等 7 种规格，视频时长范围 4~15 秒（可设为 -1 由模型自动决定）。采用异步任务模式，提交后通过单次查询获取结果视频 URL。

## 🎬 模型名称

- `doubao-seedance-2-0-fast-260128`

## 🌐 接口地址

| 接口 | 请求方式 | URL |
|------|---------|-----|
| 提交任务 | POST | `https://www.dmxapi.cn/v1/responses` |
| 获取结果 | POST | `https://www.dmxapi.cn/v1/responses` |

:::warning
请妥善保管您的 API Key！严禁将密钥泄露给他人、硬编码到代码中或提交到公开的代码仓库。如果怀疑密钥已泄露，请立即前往 DMXAPI 官网重新生成。
:::

:::warning 异步任务，请妥善保存任务 ID
本模型为**异步任务**接口：提交任务后不会直接返回视频，只返回一个任务 ID（响应中的 `id` 字段），需再用查询模型 `seedance-2-0-get` 凭该 ID 换取最终视频地址。请在提交成功后立即将任务 ID 落库或写入日志妥善保存——一旦丢失将无法找回，本次生成结果也无法再取回，但费用已产生。
:::


## 🎥 首尾帧生视频 示例代码

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
api_key = "sk-************************************************"

# ═══════════════════════════════════════════════════════════════
# 📋 步骤2: 配置请求头
# ═══════════════════════════════════════════════════════════════

headers = {
    "Content-Type": "application/json",      # 指定请求体为 JSON 格式
    "Authorization": f"{api_key}",           # token 认证方式
}

# ═══════════════════════════════════════════════════════════════
# 🖼️ 步骤3: 配置首帧和尾帧图片来源 (每张图片三选一即可)
# ═══════════════════════════════════════════════════════════════

# 首帧图片
# first_frame_source = "https://img.shetu66.com/2023/07/14/1689320796087949.png"   # 网络图片 URL
first_frame_source = "C:/Users/a1/Pictures/1689320796087949.png"                   # 本地图片路径
# first_frame_source = "asset://<ASSET_ID>"                                        # 素材 ID

# 尾帧图片
# last_frame_source = "https://img.sucaijishi.com/uploadfile/2023/0301/20230301120626930.png"   # 网络图片 URL
last_frame_source = "C:/Users/a1/Pictures/20230301120626930.jpg"                                # 本地图片路径
# last_frame_source = "asset://<ASSET_ID>"                                                      # 素材 ID


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
    if ext not in {"jpeg", "png", "webp", "bmp", "tiff", "gif"}:
        raise ValueError(f"不支持的图片格式: {ext or '无扩展名'}")
    with open(source, "rb") as f:
        base64_data = base64.b64encode(f.read()).decode("utf-8")
    return f"data:image/{ext};base64,{base64_data}"


# ═══════════════════════════════════════════════════════════════
# 💬 步骤4: 配置请求参数
# ═══════════════════════════════════════════════════════════════

payload = {
    # 【model】(string, 必填) 模型名称，指定使用 doubao-seedance-2-0-fast 模型
    "model": "doubao-seedance-2-0-fast-260128",

    # 【input】(array, 必填) 输入内容数组
    # 首尾帧生视频需传入 2 个 type=image_url 的对象，且 role 必填
    # 可同时传入一个 type=text 的对象作为文本提示词
    # 提示词建议中文不超过 500 字，英文不超过 1000 词
    # 额外支持日语、印度尼西亚语、西班牙语、葡萄牙语
    "input": [
        {
            # 【type】(string, 必填) 内容类型，文本固定为 "text"
            "type": "text",
            # 【text】(string, 必填) 文本提示词，描述视频动作与镜头
            # 建议将对话内容放入双引号内，以优化音频生成效果
            "text": "图1中小狗跳到图二小狗身上，对着镜头说\"茄子\"，360度环绕运镜",
        },
        {
            # 【image_url.url】自动解析首帧的网络 URL、本地图片路径或素材 ID
            # 图片格式：jpeg、png、webp、bmp、tiff、gif
            # 宽高比要求：(0.4, 2.5)，宽高长度：(300, 6000) px，单张不超过 30 MB
            "type": "image_url",
            "image_url": {
                "url": resolve_image_url(first_frame_source)
            },
            # 【role】(string, 必填) 首帧图片固定为 "first_frame"
            # 以首帧宽高比为准，尾帧会自动裁剪适配
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
    # "adaptive": 根据首帧图片比例自动选择最接近的宽高比
    # 注意: 指定的宽高比与图片不一致时，方舟会对图片进行居中裁剪
    "ratio": "adaptive",

    # 【resolution】(string, 可选) 视频分辨率，默认值 720p
    # 可选值: "480p" / "720p"（seedance 2.0 fast 不支持 1080p 和 4k）
    "resolution": "720p",

    # 【duration】(integer, 可选) 视频时长（秒），默认值 5
    # 取值范围: [4, 15]，或 -1 由模型在有效范围内自主选择合适时长
    # 注意: 视频时长与计费相关，请谨慎设置
    "duration": 5,

    # 【generate_audio】(boolean, 可选) 是否生成同步音频（人声/音效/背景音乐），默认值 true
    # true: 模型自动生成与画面匹配的人声、音效及背景音乐
    # false: 输出无声视频
    # 注意: 生成的有声视频均为单声道
    "generate_audio": True,

    # 【seed】(integer, 可选) 随机种子，默认值 -1
    # 取值范围: [-1, 2^32-1]，-1 表示使用随机数
    # 相同 seed 在相同请求下生成结果相似（不保证完全一致）
    "seed": -1,

    # 【watermark】(boolean, 可选) 是否包含水印，默认值 false
    # true: 生成视频右下角展示「AI 生成」水印
    "watermark": False,

    # 【return_last_frame】(boolean, 可选) 是否返回视频尾帧图像，默认值 false
    # true: 返回尾帧图像（png 格式，宽高与视频一致，无水印）
    # 可将本次的尾帧作为下一个任务的首帧，实现连续视频生成
    "return_last_frame": False,

    # 【execution_expires_after】(integer, 可选) 任务超时时间（秒）
    # 取值范围: [3600, 259200]，默认 172800（48小时）
    # 从 created_at 开始计算，超时后任务终止并标记为 expired
    "execution_expires_after": 172800,

    # 【callback_url】(string, 可选) 任务状态回调地址
    # 状态说明: queued(排队中) / running(运行中) / succeeded(成功) / failed(失败) / expired(超时)
    "callback_url": "https://www.dmxapi.cn",

    # 【tools】(array, 可选) 工具配置，仅 seedance 2.0 与 2.0 fast 支持
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
  "id": "cgt-20260424185225-sb9vm",
  "usage": {
    "total_tokens": 40200,
    "input_tokens": 0,
    "input_tokens_details": {
      "cached_tokens": 0
    },
    "output_tokens": 40200,
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
api_key = "sk-******************************************"

headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {api_key}",
}

payload = {
    # 【model】(string, 必填) 固定值，用于查询 Seedance 视频生成结果
    "model": "seedance-2-0-get",
    # 【input】(string, 必填) 提交任务时返回的任务 ID
    "input": "cgt-20260428165939-ccb9g"
}

response = requests.post(url, headers=headers, json=payload)
result = response.json()
print(json.dumps(result, indent=2, ensure_ascii=False))

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
  "request_id": "cgt-20260428165939-ccb9g",
  "output": [
    {
      "type": "message",
      "content": [
        {
          "type": "output_text",
          "text": "{\"content\":{\"video_url\":\"https://ark-acg-cn-beijing.tos-cn-beijing.volces.com/doubao-seedance-2-0-fast/02177736688829100000000000000000000ffffac177fcdd9df5d.mp4?...\"},\"id\":\"cgt-20260428165939-ccb9g\",\"model\":\"doubao-seedance-2-0-fast-260128\",\"status\":\"succeeded\"}"
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

视频链接: https://ark-acg-cn-beijing.tos-cn-beijing.volces.com/doubao-seedance-2-0-fast/02177736688829100000000000000000000ffffac177fcdd9df5d.mp4?...
```


<p align="center">
  <small>© 2026 DMXAPI doubao-seedance-2-0-fast-260128 首尾帧生视频</small>
</p>
