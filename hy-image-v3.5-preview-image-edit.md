# hy-image-v3.5-preview 图片编辑 API 使用文档

基于腾讯混元 Hy-Image-3.5-preview 模型的图片编辑接口，通过 `/v1/images/generations` 端点传入「参考图 + 编辑指令」，一次请求同步返回编辑结果，无需提交任务与轮询。参考图支持公网 URL 与 Base64 Data URL 两种传入方式，最多 20 张、单张不超过 20MB，格式支持 png / jpeg / jpg；输出最高支持 4096×4096（4K）分辨率，宽高可在 [256, 8192] 范围内自由指定，并支持生成种子复现、外部搜索增强与最长 16 字符的自定义水印脚注，返回有效期 12 小时的临时图片地址。

## 🌐 请求地址

```text
https://www.dmxapi.cn/v1/images/generations
```

:::warning
请妥善保管您的 API Key！严禁将密钥泄露给他人、硬编码到代码中或提交到公开的代码仓库。如果怀疑密钥已泄露，请立即前往 DMXAPI 官网重新生成。
:::

## 模型名称

- `hy-image-v3.5-preview`

## 图片编辑 示例代码

```python
import base64
import json
import os

import requests

# ===============================================================
# 步骤1: 配置 API 连接信息
# ===============================================================

# DMXAPI 服务端点地址
url = "https://www.dmxapi.cn/v1/images/generations"

# DMXAPI 密钥 (请替换为您自己的密钥)
# 获取方式: 登录 DMXAPI 官网 -> 个人中心 -> API 密钥管理
api_key = "sk-***********************************************"

# ===============================================================
# 步骤2: 配置请求头
# ===============================================================

headers = {
    "Authorization": f"Bearer {api_key}",    # Bearer token 认证方式
    "Content-Type": "application/json",      # 指定请求体为 JSON 格式
}

# ===============================================================
# 步骤3: 配置请求参数
# ===============================================================

# 参考图来源，三选一：
# 1. 公网图片 URL
image_source = "https://cdn.jsdelivr.net/gh/opencv/opencv/samples/data/fruits.jpg"

# 2. 本地图片路径，代码会在后面自动转换为 Base64 Data URL
# image_source = r"C:\Users\a1\Pictures\lolita2.png"

# 3. 已经转换好的 Data URL
# image_source = "data:image/png;base64,xxxxxxxx"

payload = {
    # 【model】(string, 必填) 调用的模型名称
    # 取值: hy-image-v3.5-preview
    "model": "hy-image-v3.5-preview",

    # 【prompt】(string, 必填) 图片编辑指令
    # DMXAPI 兼容接口的提示词字段（官方文档未明确说明）
    "prompt": "把图片转成素描风格",

    # 【images】(array[string], 必填) 参考图片列表
    # 支持图片 URL 或 Base64 Data URL，格式 png / jpeg / jpg
    # 单张图片大小不超过 20MB，最多支持 20 张图片
    "images": [
        image_source
    ],

    # 【size】(string, 可选) 生成尺寸，格式 ${宽}x${高}
    # 宽、高均为正整数，取值范围 [256, 8192]
    # 宽 × 高（面积）不超过 16777216，即最高支持 4096x4096（4K）
    # 不传或传空串时，由模型基于 prompt 语义与 generate_max_pixels 自主决定尺寸
    # 传入具体值时强制按指定尺寸出图；需要 4K 输出时传 "4096x4096" 即可
    "size": "1024x1024",

    # 【seed】(integer, 可选) 生成种子
    # int64 类型，取值范围 [0, 2^63-1]；为 0 或不传时服务端随机分配，负值将被拒绝
    "seed": 0,

    # 【generate_max_pixels】(integer, 可选) 生成图片的目标面积（像素数）
    # 仅在未传 size 时生效，支持 3 个枚举档位:
    #   - 1048576: 1K（1024x1024）
    #   - 2359296: 1.5K（默认档位）
    #   - 4194304: 2K
    # 传入非枚举中间值时按最近面积归档
    # 该参数最高档位为 2K，需要更高分辨率请改用 size 指定
    "generate_max_pixels": 4194304,

    # 【resize_max_pixels】(integer, 可选) 输入参考图面积上限（像素数）
    # 原图面积不超过阈值时原样透传；超过阈值时按比例等比缩放到接近阈值后再送入模型
    # 用于控制大图（4K/6K）带来的上下文 token 消耗
    # 不传时默认 1048576（1024x1024）
    "resize_max_pixels": 1048576,

    # 【footnote】(string, 可选) 业务自定义水印内容
    # 最长 16 个字符（按 utf8.RuneCount 计算，不区分中英文），生成在图片右下角
    "footnote": "DMXAPI",

    # 【use_search_tool】(object, 可选) 外部搜索增强开关
    # 结构固定为 {"value": true} 或 {"value": false}，当前默认关闭
    "use_search_tool": {
        "value": False
    }
}

# 本地图片路径 / Data URL 的统一转换逻辑

IMAGE_MIME_TYPES = {
    ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg",
    ".png": "image/png",
    ".webp": "image/webp",
    ".bmp": "image/bmp",
    ".tif": "image/tiff",
    ".tiff": "image/tiff",
    ".gif": "image/gif",
    ".heic": "image/heic",
    ".heif": "image/heif",
}

MAX_IMAGE_SIZE = 20 * 1024 * 1024


def resolve_image_source(source):
    # 公网 URL 直接传递
    if source.startswith(("http://", "https://")):
        return source

    # 已经是 Data URL，直接传递
    if source.startswith("data:image/"):
        return source

    # 本地文件不存在时抛出错误
    if not os.path.isfile(source):
        raise FileNotFoundError(f"图片文件不存在：{source}")

    # 检查图片格式
    extension = os.path.splitext(source)[1].lower()
    mime_type = IMAGE_MIME_TYPES.get(extension)

    if mime_type is None:
        raise ValueError(
            f"不支持的图片格式：{extension}，"
            f"支持格式：{', '.join(IMAGE_MIME_TYPES)}"
        )

    # 检查图片大小
    file_size = os.path.getsize(source)

    if file_size > MAX_IMAGE_SIZE:
        raise ValueError("单张图片大小不能超过 20MB")

    # 读取本地图片并转换为 Base64
    with open(source, "rb") as image_file:
        encoded_image = base64.b64encode(
            image_file.read()
        ).decode("ascii")

    # 组装 Data URL
    return f"data:{mime_type};base64,{encoded_image}"


# 将 images 中的本地路径转换为 Data URL
payload["images"] = [
    resolve_image_source(image)
    for image in payload["images"]
]

# ===============================================================
# 步骤4: 发送请求并输出结果
# ===============================================================

# 发送 POST 请求到 API 服务器
response = requests.post(
    url,
    headers=headers,
    json=payload,
    timeout=300
)

response.raise_for_status()

result = response.json()

# 格式化输出 JSON 响应
# - indent=2: 缩进 2 空格，便于阅读
# - ensure_ascii=False: 正确显示中文字符
print(json.dumps(result, indent=2, ensure_ascii=False))

# 打印生成的图片地址（临时签名 URL，有效期 12 小时，请及时下载转存）
if result.get("data"):
    print("\n图片地址：")
    print(result["data"][0].get("url"))
```

## 返回示例

```json
{
  "created": 1789720605,
  "data": [
    {
      "url": "https://aigc-output-image-file-1326893053.cos.ap-guangzhou.myqcloud.com/xxx/sketch.png?..."
    }
  ],
  "request_id": "b2d11e18-152c-5ebb-cbf0-c8fcg3cd45cb",
  "usage": {
    "total_tokens": 20000
  }
}
```

<p align="center">
  <small>© 2026 DMXAPI hy-image-v3.5-preview 图片编辑</small>
</p>
