# qwen-image-2.1-turbo 图生图 API 使用文档

基于 `qwen-image-2.1-turbo` 的图生图（I2I）接口，通过 `/v1/images/edits` 端点同步调用。传入 1~10 张参考图并配合编辑指令，即可完成风格迁移、元素修改、内容重绘等操作；支持提示词智能改写（DPE）与思考模式，单次可输出 1~6 张图，输出分辨率总像素在 512×512 至 2048×2048 之间、宽高比 1:8 至 8:1 自由设置（不指定 `size` 时由模型自动推荐分辨率）；该模型价格为 0.1 元/张。

## 接口地址

| 接口 | 请求方式 | URL |
|------|---------|-----|
| 图生图 | POST | `https://www.dmxapi.cn/v1/images/edits` |

:::warning
请妥善保管您的 API Key！严禁将密钥泄露给他人、硬编码到代码中或提交到公开的代码仓库。如果怀疑密钥已泄露，请立即前往 DMXAPI 官网重新生成。
:::

## 模型名称

- `qwen-image-2.1-turbo`

## 图生图 示例代码

```python
import base64
import binascii
import os

import requests
import json

# ===============================================================
# 步骤1: 配置 API 连接信息
# ===============================================================

# DMXAPI 服务端点地址
url = "https://www.dmxapi.cn/v1/images/edits"

# DMXAPI 密钥 (请替换为您自己的密钥)
# 获取方式: 登录 DMXAPI 官网 -> 个人中心 -> API 密钥管理
api_key = "sk-***********************************************"

# ===============================================================
# 步骤2: 配置请求头
# ===============================================================

headers = {
    "Content-Type": "application/json",      # 指定请求体为 JSON 格式
    "Authorization": f"{api_key}",           # token 认证方式
}

# ===============================================================
# 步骤3: 配置请求参数
# ===============================================================

payload = {
    # 【model】(string, 必填) 调用的模型名称
    "model": "qwen-image-2.1-turbo",

    # 【prompt】(string, 必填) 正向提示词
    # 用于描述您期望编辑后的图像内容、风格和构图，支持中英文
    # 推荐不超过 4500 Token
    "prompt": "把主体改成美漫风格",

    # 【image】(string 或 array[string], 必填) 输入图像的 URL 或 Base64 编码数据
    # I2I 场景下支持传入 1~10 张图像；单图直接传字符串，多图传数组，数组顺序即图像顺序
    # 图像要求:
    #   - 图像格式: JPG、JPEG、PNG、BMP、TIFF、WEBP 和 GIF
    #   - 图像大小: 单张不超过 10MB
    #   - 图像宽高: 各为 1~8000 像素，长短边比例不超过 10:1
    # 支持的输入格式:
    #   - 公网 URL: 支持 HTTP 和 HTTPS 协议
    #   - Base64 编码: 格式为 data:{MIME_type};base64,{base64_data}
    "image": "https://cdn.jsdelivr.net/gh/opencv/opencv/samples/data/fruits.jpg",

    # 【n】(integer, 可选) 输出图像的数量，支持输出 1~6 张图片，默认值 1
    "n": 1,

    # 【prompt_extend】(bool, 可选) 是否开启提示词智能改写，默认值 True (建议开启)
    # 开启后模型会按照 prompt_extend_mode 指定的方式优化正向提示词
    # 对描述较简单的提示词效果提升明显
    "prompt_extend": True,

    # 【prompt_extend_mode】(string, 可选) 提示词改写方式，默认值 "direct"
    # 可选值:
    #   - "direct" 直接提示词增强(DPE)，适用于大多数场景，T2I 和 I2I 均支持
    #   - "agent"  智能体提示词增强(APE)，仅支持文生图(T2I)
    # 注意: 本接口为图生图(I2I)场景，传入 "agent" 将返回 400 错误，请保持 "direct"
    "prompt_extend_mode": "direct",

    # 【enable_thinking】(bool, 可选) 是否开启思考模式，默认值 True
    # 开启时模型将增强推理能力以提升出图质量，但会增加生成耗时
    # 仅在 prompt_extend=True 时生效
    "enable_thinking": True,

    # 【watermark】(bool, 可选) 是否添加水印，默认值 False
    "watermark": False,

    # ---------------------------------------------------------------
    # 以下为可选参数，按需取消注释后使用
    # ---------------------------------------------------------------

    # 【size】(string, 可选) 设置输出图像的分辨率，格式为 宽x高，例如 "1024x1024"
    # 未指定或填写 "auto" 时，由模型根据提示词自动推荐分辨率
    # 图生图(I2I): 像素面积范围 512x512 至 2048x2048，宽高比限制 1:8 至 8:1
    # "size": "1024x1024",

    # 【seed】(integer, 可选) 随机数种子，取值范围 [0, 2147483647]
    # 未传入时服务会随机选择种子，固定种子可使生成结果相对稳定
    # "seed": 42,
}

# ===============================================================
# 步骤4: 媒体输入处理（严格按每个参数自己的接口契约）
# ===============================================================
# 本段代码用于把 image 字段统一规整成接口能接受的形式，支持三种写法：
#   - 公网 URL       : 以 http:// 或 https:// 开头，原样透传
#   - Data URI       : data:{MIME_type};base64,{base64_data}，校验头部与正文合法性后透传
#   - 本地文件路径   : 自动读取文件、转 Base64，并按扩展名补上 MIME 头拼成 Data URI
# 若您只使用公网图片 URL，本段可以整体删除，不影响调用。
#
# - payload["image"]（图片）
#   限制：支持 1–10 张图（单图传字符串，多图传数组）
#   限制：单图不超过 10 MB
#   限制：宽高各为 1–8000 像素，长短边比例不超过 10:1

# 媒体契约表：描述该字段允许哪些输入形式、本地文件如何编码、支持哪些格式
_MEDIA_RULES = {
    "rule_1": {
        "allow_url": True,              # 允许公网 URL
        "allow_data_uri": True,         # 允许 Data URI
        "allow_raw_base64": False,      # 不允许裸 Base64（必须带 data: 头）
        "allow_local_file": True,       # 允许本地文件路径
        "local_encoding": "data_uri",   # 本地文件编码为 Data URI 形式
        # 本地文件扩展名 -> MIME 类型映射
        "file_formats": {
            ".jpg": "image/jpeg",
            ".jpeg": "image/jpeg",
            ".png": "image/png",
            ".bmp": "image/bmp",
            ".tif": "image/tiff",
            ".tiff": "image/tiff",
            ".webp": "image/webp",
            ".gif": "image/gif",
        },
        # Data URI 允许的 MIME 类型白名单
        "data_types": ["image/bmp", "image/gif", "image/jpeg", "image/png", "image/tiff", "image/webp"],
    },
}

def _resolve_media(value: str, rule: dict, field: str) -> tuple:
    """把媒体入参规整为接口可接受的形式，返回 (值, 形式)。形式为 url / data_uri / raw_base64。"""
    if not isinstance(value, str) or not value:
        raise ValueError(f"{field} 必须是非空字符串")

    # 情况一: 公网 URL，直接透传
    if value.startswith(("http://", "https://")):
        if rule["allow_url"]:
            return value, "url"
        raise ValueError(f"{field} 不接受 URL")

    # 情况二: Data URI，校验头部 MIME 与正文 Base64 合法性
    if value.startswith("data:"):
        if not rule["allow_data_uri"]:
            raise ValueError(f"{field} 不接受 Data URI")
        header, sep, encoded = value.partition(",")
        expected = {f"data:{media_type};base64" for media_type in rule["data_types"]}
        if not sep or header not in expected or not encoded:
            raise ValueError(f"{field} 的 Data URI 头无效；允许: {sorted(expected)}")
        try:
            base64.b64decode(encoded, validate=True)
        except (binascii.Error, ValueError):
            raise ValueError(f"{field} 的 Data URI 正文不是合法 Base64")
        return value, "data_uri"

    # 情况三: 本地文件路径，读取后按契约编码
    if os.path.isfile(value):
        if not rule["allow_local_file"]:
            raise ValueError(f"{field} 不接受本地文件")
        ext = os.path.splitext(value)[1].lower()
        if ext not in rule["file_formats"]:
            raise ValueError(f"{field} 不支持本地文件格式 {ext}；允许: {sorted(rule['file_formats'])}")
        with open(value, "rb") as f:
            encoded = base64.b64encode(f.read()).decode("ascii")
        if rule["local_encoding"] == "raw_base64":
            return encoded, "raw_base64"
        media_type = rule["file_formats"][ext]
        return f"data:{media_type};base64,{encoded}", "data_uri"

    # 情况四: 裸 Base64（仅当契约允许时）
    if rule["allow_raw_base64"]:
        try:
            base64.b64decode(value, validate=True)
            return value, "raw_base64"
        except (binascii.Error, ValueError):
            pass

    raise ValueError(f"{field} 不符合接口媒体契约")

# 就地规整 image 字段（多图数组时对每个元素逐一规整）
if isinstance(payload["image"], list):
    payload["image"] = [_resolve_media(item, _MEDIA_RULES["rule_1"], "payload[\"image\"]")[0] for item in payload["image"]]
else:
    payload["image"] = _resolve_media(payload["image"], _MEDIA_RULES["rule_1"], "payload[\"image\"]")[0]

# ===============================================================
# 步骤5: 发送请求并输出结果
# ===============================================================

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
  "created": 1792396999,
  "data": [
    {
      "url": "https://dashscope-a717.oss-accelerate.aliyuncs.com/1d/37/20261019/23f3d493/a061228c-0753-950b-a099-fa92d990b25e_qwen_image3_serving_output_0.png?..."
    }
  ],
  "usage": {
    "height": 1984,
    "image_count": 1,
    "width": 2112
  }
}
```

<p align="center">
  <small>© 2026 DMXAPI qwen-image-2.1-turbo 图生图</small>
</p>
