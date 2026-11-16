# MiniMax-H3-Image 图片编辑 API 使用文档

基于 MiniMax-H3-Image 的图片编辑接口，调用 `POST /v1/images/edits`，按 1 到 16 张参考图和编辑说明生成新图片。参考图按数组顺序对应「图1」「图2」。标准版 `MiniMax-H3-Image` 与极速版 `MiniMax-H3-Image-Highspeed` 参数相同。

## 接口地址

| 接口 | 请求方式 | URL |
|------|---------|-----|
| 图片编辑 | POST | `https://www.dmxapi.cn/v1/images/edits` |

:::warning
请妥善保管您的 API Key！严禁将密钥泄露给他人、硬编码到代码中或提交到公开的代码仓库。如果怀疑密钥已泄露，请立即前往 DMXAPI 官网重新生成。
:::

## 模型名称

- `MiniMax-H3-Image`
- `MiniMax-H3-Image-Highspeed`

## 图片编辑示例代码

```python
import requests
import json
import os
import base64
from urllib.parse import urlparse

# ===============================================================
# 步骤1: 配置 API 连接信息
# ===============================================================

# DMXAPI 服务端点地址
url = "https://www.dmxapi.cn/v1/images/edits"

# DMXAPI 密钥 (请替换为您自己的密钥)
# 获取方式: 登录 DMXAPI 官网 -> 个人中心 -> API 密钥管理
api_key = "sk-******************************************"

# 图片保存目录
output_dir = "output"

# 客户端超时（秒）。官方服务端最长等待 600 秒，客户端必须不小于 600。
# 这个接口不幂等：超时或断开后服务端仍会继续生成，成功的图照样计费；重试会再生成并再次计费。
# 编辑接口没有 disable_prompt_enhanced，提示词增强始终开启。
timeout = 620

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
    # 【model】(string, 必填) 模型名称
    # 可选值:
    #   - "MiniMax-H3-Image"(标准版)
    #   - "MiniMax-H3-Image-Highspeed"(极速版，参数与标准版相同)
    "model": "MiniMax-H3-Image",

    # 【prompt】(string, 必填) 编辑说明
    # 按 Unicode 字符计，不含首尾空白，最长 32000。空白 prompt 返回 400。
    # images 按数组顺序对应「图1」「图2」。本示例是 JSON；也可以改用 multipart，
    # 字段名是 image 或 image[]。不支持 mask，传了返回 400。
    "prompt": "把图2的蓝色闹钟放到图1的右上角，保持图1的人物和背景不变",

    # 【images】(object[], 必填) 参考图
    # 1 到 16 张，顺序就是「图1」到「图16」。每项只有 image_url。
    # image_url 三选一：
    #   - 公网可访问的 URL
    #   - "mm_file://{file_id}"，file_id 由文件上传接口以 purpose=image_generation_input 获得
    #   - "data:image/<格式>;base64,<Base64>"，格式名小写，例如 png、jpeg、webp
    # 格式只支持 JPG、JPEG、PNG、WEBP、HEIC、HEIF。单文件不超过 64MiB，
    # 宽和高都在 128 到 8192，长边/短边不超过 4:1。整个请求体不超过 64MiB。
    # Base64 大约是原文件的 4/3，放不下时改用 URL。
    "images": [
        {
            # 【image_url】(string, 必填) 参考图地址
            "image_url": "https://img.alicdn.com/tps/TB19O79MVXXXXcZXVXXXXXXXXXX-1024-1024.jpg",
        },
        {
            # 【image_url】(string, 必填) 参考图地址
            "image_url": "https://img.alicdn.com/imgextra/i3/O1CN0157XGE51l6iL9441yX_!!6000000004770-49-tps-1104-1472.webp",
        },
    ],

    # 【n】(integer, 可选) 生成数量
    # 取值范围 [1, 10]，默认 1。
    # data 的长度始终等于 n，和请求顺序对齐。只对成功的图片计费，失败项不算。
    "n": 1,

    # 【aspect_ratio】(string, 可选) 宽高比
    # 只在 size 不传或为 auto 时使用，默认 auto（结合参考图和提示词决定）。
    # 可选值: "auto" 或 "X:Y"。X、Y 是 1 到 300 的整数，宽高比含边界 1:3 到 3:1。
    # 与下面的 size「宽x高」二选一。改用「宽x高」时，本字段和 area 都不能再传，传了返回 400，即使值是 auto。
    "aspect_ratio": "16:9",

    # 【area】(string, 可选) 面积档位
    # 只在 size 不传或为 auto 时使用，默认 4K。
    # 可选值: "1K" / "2K" / "4K"，分别按 1024²、2048²、4096² 的面积生成。
    # 这是面积，不是固定成 1024x1024。实际宽高还要看 aspect_ratio。
    "area": "4K",

    # 【size】(string, 可选) 精确输出尺寸
    # 默认 auto。写成「宽x高」时，宽和高必须是正整数，面积含边界 655360 到 20000000，
    # 宽高比含边界 1:3 到 3:1。不合规不缩放、不取整，直接返回 400。
    # 使用「宽x高」时不能再传 aspect_ratio 和 area，即使它们的值是 auto。
    # 下面这行是 2K 的 16:9 预设，不是上面 area=4K 的结果。启用时请删掉 aspect_ratio 和 area。
    # 常用预设：
    #   2K 1:1 2048x2048，4:3 2368x1760，16:9 2720x1536，3:1 3552x1184，竖图把宽高对调
    #   4K 1:1 4096x4096，4:3 4736x3552，16:9 5472x3072，3:1 7104x2368
    # 16:9 的 4K 不是 2720 乘 2。2720 乘 2 是 5440，官方预设和实测都是 5472x3072。
    # "size": "2720x1536",

    # 【output_format】(string, 可选) 图片格式
    # 默认 jpeg。可选值: "png" / "jpeg" / "jpg" / "webp"。
    # jpg 与 jpeg 等价，响应里的 output_format 写成 jpeg。
    "output_format": "png",

    # 【output_compression】(integer, 可选) 压缩质量
    # 取值范围 [0, 100]，默认 95。只对 jpeg / webp 生效，png 忽略。
    # 请求里的 jpg 按 jpeg 处理，所以也会压缩。
    "output_compression": 95,

    # 【response_format】(string, 可选) 返回方式
    # 可选值:
    #   - "url"(默认，图片地址 24 小时内有效)
    #   - "b64_json"(图片放在 data[].b64_json，不能和 stream: true 同时使用)
    # b64_json 按 n×宽×高 限制总面积，含边界：png 最大 20000000（约一张 4K），
    # jpeg / webp 最大 80000000（约四张 4K 或十张 2K）。size 为 auto 时，每张按 area 那一档的面积计算。
    "response_format": "url",

    # 【aigc_watermark】(boolean, 可选) 画面可见水印
    # 默认 false。true 时在画面上添加可见的 AIGC 标识。
    # 文件元数据里的隐式 AIGC 标识始终会写，不受这个参数控制。
    "aigc_watermark": False,
}

# ===============================================================
# 步骤4: 发送请求并输出结果
# ===============================================================

# 发送 POST 请求到 API 服务器
response = requests.post(url, headers=headers, json=payload, timeout=timeout)

# 格式化输出 JSON 响应
# - indent=2: 缩进 2 空格，便于阅读
# - ensure_ascii=False: 正确显示中文字符
# 至少一张成功才是 200。部分失败时 data 里对应项只有 error。
# 全部失败时上游是 402、422 或 500，网关会改成自己的 error。
result = response.json()
print(json.dumps(result, indent=2, ensure_ascii=False))

if response.status_code == 200:
    os.makedirs(output_dir, exist_ok=True)
    output_format = result.get("output_format") or "jpeg"
    if output_format == "jpg":
        output_format = "jpeg"
    for index, item in enumerate(result.get("data") or []):
        if "error" in item:
            print(f"第 {index} 张失败:", item["error"].get("message"))
            continue
        output_path = os.path.join(output_dir, f"minimax-h3-edit-{index}.{output_format}")
        if payload["response_format"] == "b64_json":
            with open(output_path, "wb") as image_file:
                image_file.write(base64.b64decode(item["b64_json"]))
        else:
            image_url = item["url"]
            parsed = urlparse(image_url)
            if parsed.scheme not in ("http", "https") or not parsed.netloc:
                raise SystemExit(f"拒绝下载非法地址: {image_url}")
            download_headers = {}
            if parsed.netloc.endswith("dmxapi.cn"):
                download_headers["Authorization"] = api_key
            image_response = requests.get(image_url, headers=download_headers, timeout=timeout)
            content_type = image_response.headers.get("Content-Type", "")
            if image_response.status_code != 200 or not content_type.startswith("image/"):
                raise SystemExit(f"下载失败 {image_response.status_code}: {image_response.text[:300]}")
            with open(output_path, "wb") as image_file:
                image_file.write(image_response.content)
        print("已保存:", output_path)
```

## 返回示例

```json
{
  "created": 1792308678,
  "data": [
    {
      "url": "https://example.com/h3-image/output-0.png",
      "size": "5472x3072",
      "revised_prompt": "把图2中的蓝色闹钟放到图1画面的右上角，闹钟的颜色和外形与图2一致，图1中的人物、姿态和背景保持不变，光线与透视自然衔接"
    }
  ],
  "output_format": "png",
  "usage": {
    "generated_images": 1,
    "total_tokens": 40225,
    "input_tokens": 23905,
    "output_tokens": 16320,
    "input_tokens_details": {
      "text_tokens": 12093,
      "image_tokens": 11812
    },
    "output_tokens_details": {
      "image_tokens": 16320
    }
  },
  "request_id": "021792308678142a2c883cf675b9804d"
}
```

<p align="center">
  <small>© 2026 DMXAPI MiniMax-H3-Image 图片编辑</small>
</p>
