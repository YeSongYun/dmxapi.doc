# gpt-image-2 图片编辑 API 使用文档

基于 gpt-image-2 的图片编辑接口，可通过一张或多张参考图配合文本提示词生成新图，也支持结合蒙版进行局部重绘。该接口支持自动或自定义尺寸、质量、背景、输出格式与压缩等级；其中尺寸最大边长可到 3840px，总像素范围为 655,360 到 8,294,400，适合从快速草稿到高分辨率成图的多种编辑场景。

## 🌐 请求地址

```text
https://www.dmxapi.cn/v1/images/edits
```

:::warning
请妥善保管您的 API Key！严禁将密钥泄露给他人、硬编码到代码中或提交到公开的代码仓库。如果怀疑密钥已泄露，请立即前往 DMXAPI 官网重新生成。
:::

## 🤖 模型名称

- `gpt-image-2`

## 🧪 图片编辑 示例代码

```python
import base64
import json
import os
from datetime import datetime

import requests

# 图片文件配置：官方文档说明可使用一张或多张图片作为参考图
image_paths = [
    "C:/Users/a1/Desktop/测试保存代码/c1.png",
    # "input/source_image_2.png",
]

# API 配置
url = "https://www.dmxapi.cn/v1/images/edits"
api_key = "sk-******************************************"
headers = {
    "Authorization": f"Bearer {api_key}",
}

# 请求参数
payload = {
    # 【model】(string, 必填) 指定要调用的图像模型
    # 当前文档对应官方页面中的 GPT Image 系列模型 gpt-image-2
    # 可选值: "gpt-image-2"(当前示例使用的图片编辑模型)
    "model": "gpt-image-2",

    # 【prompt】(string, 必填) 描述希望模型如何编辑输入图片
    # 官方文档说明图片编辑基于文本提示词执行，可整体修改，也可结合 mask 做局部替换
    "prompt": "给图里加上卡通版的卡皮巴拉",

    # 【size】(string, 可选) 输出图像尺寸
    # gpt-image-2 支持满足约束条件的任意分辨率，正方形通常生成更快
    # 常用值: "1024x1024" / "1536x1024" / "1024x1536" / "2048x2048" / "2048x1152" / "3840x2160" / "2160x3840" / "auto"(默认)
    # 约束: 最大边长 <= 3840px；宽高必须都是 16 的倍数；长宽比不能超过 3:1；总像素必须在 655,360 到 8,294,400 之间
    "size": "1024x1024",

    # 【background】(string, 可选) 控制输出背景模式
    # 官方文档给出的模式为 opaque 或 auto，且 background 支持 auto 自动选择
    # 可选值: "auto"(默认，由模型自动选择) / "opaque"(不透明背景)
    "background": "auto",

    # 【output_compression】(number, 可选) 控制 JPEG  输出压缩等级
    # 仅在 output_format 为 jpeg 时生效；数值越高，压缩越强
    # 取值范围: 0-100
    "output_compression": 100,

    # 【output_format】(string, 可选) 指定输出文件格式
    # Image API 默认格式为 png，也支持 jpeg 
    # 使用 jpeg 通常比 png 更快；若选择 jpeg ，可再配合 output_compression 调整压缩率
    # 可选值: "png"(默认) / "jpeg"(延迟更低) 
    "output_format": "png",

    # 【quality】(string, 可选) 控制渲染质量
    # 官方提供 low / medium / high / auto 四档，其中 low 适合快速草稿、缩略图和快速迭代
    # 超过 2560x1440（3,686,400 像素）的输出在官方文档中标注为 experimental
    # 可选值: "low" / "medium" / "high" / "auto"(默认)
    # "quality": "auto",

    # 【n】(number, 可选) 单次请求生成的图片数量
    # 官方文档说明可一次返回多张图片，默认返回 1 张；当前页面未给出 gpt-image-2 的明确最大值
    # 使用建议: 先从 1 开始，便于稳定处理返回结果和落盘逻辑
    "n": 1,
}

# 准备图片文件
files = []
for img_path in image_paths:
    try:
        file_name = os.path.basename(img_path)
        ext = img_path.lower().rsplit(".", 1)[-1]
        mime_map = {
            "png": "image/png",
            "jpg": "image/jpeg",
            "jpeg": "image/jpeg",
            "webp": "image/webp",
        }
        mime_type = mime_map.get(ext, "image/png")

        # 【image】(file, 必填) 待编辑的输入图片文件
        # 官方文档说明可使用一张或多张图片作为参考图；若同时提供 mask，mask 会作用在第一张输入图上
        # 在 mask 编辑场景下，原图与 mask 必须具有相同格式和尺寸，且文件大小需小于 50MB
        # mask 还必须包含 alpha 通道；若使用黑白图作为 mask，需要先补充 alpha 通道后再上传
        files.append(("image", (file_name, open(img_path, "rb"), mime_type)))
    except FileNotFoundError:
        print(f"文件未找到: {img_path}")


def main():
    if not files:
        print("没有可用的图片文件")
        return

    response = requests.post(url, headers=headers, data=payload, files=files, timeout=1000)
    print("status:", response.status_code)

    try:
        data = response.json()
    except ValueError:
        print("non-JSON response:", response.text)
        return

    if "data" not in data or not data["data"]:
        print("unexpected response:", json.dumps(data, ensure_ascii=False, indent=2))
        return

    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")

    for i, item in enumerate(data["data"], start=1):
        if item.get("b64_json"):
            image_bytes = base64.b64decode(item["b64_json"])
        elif item.get("url"):
            image_bytes = requests.get(item["url"], timeout=120).content
        else:
            print(f"第 {i} 张图片无有效数据")
            continue

        filename = f"edited_{ts}_{i}.png"
        output_path = os.path.join(output_dir, filename)
        with open(output_path, "wb") as f:
            f.write(image_bytes)
        print(f"saved {output_path}")


if __name__ == "__main__":
    main()
```

## 📦 返回示例

```text
status: 200
saved output\edited_20260422_194855_1.png
```

<p align="center">
  <small>© 2026 DMXAPI gpt-image-2 图片编辑</small>
</p>
