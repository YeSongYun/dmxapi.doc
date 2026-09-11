# gpt-image-2.5 图片编辑 API 使用文档

通过 `/v1/images/edits` 接口上传一张或多张参考图，配合文字指令使用 `gpt-image-2.5-sunburst` 或 `gpt-image-2.5-flare` 编辑图片。参考图可使用本地文件路径或公网 URL，示例脚本会按文件名后缀判断格式并上传。
## 接口地址

| 接口 | 请求方式 | URL |
|------|---------|-----|
| 图片编辑 | POST | `https://www.dmxapi.cn/v1/images/edits` |
:::warning
请妥善保管 DMXAPI API Key，勿在前端代码、公开仓库或日志中暴露。运行前，将示例中 `api_key` 引号内的星号占位内容替换为你的完整 API 令牌。
:::
## 模型名称
| 模型 ID | 官方定位 | 使用选择 |
|------|------|------|
| `gpt-image-2.5-sunburst` | 以图像质量为重点的基础模型 | 更关注最终编辑效果与细节时选用 |
| `gpt-image-2.5-flare` | 以生成速度为重点的小模型 | 更关注编辑速度时选用 |

## 图片编辑示例代码
```python
import base64
import io
from contextlib import ExitStack
from datetime import datetime
from pathlib import Path
from urllib.parse import urlsplit

import requests

# 图片文件配置：可使用一张或多张图片作为参考图
# 支持 本地文件路径 / 公网 URL，自动识别；多图可继续添加列表项
# 本项是示例脚本的客户端配置，不是 API 参数
image_paths = [
    r"C:\path\to\reference-image.jpg",
    # "https://your-cdn.example.com/reference-image.png",
]

# API 配置
url = "https://www.dmxapi.cn/v1/images/edits"
api_key = "sk-*****************************************"  # 在引号内粘贴完整 API 令牌

# 请求头：只放 Bearer 鉴权
# multipart/form-data 的 Content-Type 与 boundary 由 requests 自动生成，不要手动指定 JSON 请求头
headers = {
    "Authorization": f"Bearer {api_key}",
}

# 请求参数（multipart 普通字段，通过 data=payload 发送）
payload = {
    # 【model】(string, 必填) 使用的图像编辑模型名称
    # 本文档对应 GPT Image 2.5 系列，两款模型均可用于图片编辑
    # 可选值:
    #   "gpt-image-2.5-sunburst"  (以图像质量为重点的基础模型，示例默认)
    #   "gpt-image-2.5-flare"     (以生成速度为重点的小模型)
    "model": "gpt-image-2.5-sunburst",

    # 【prompt】(string, 必填) 描述希望模型如何编辑输入图片
    # GPT image 系列模型最大长度 32000 字符
    # 可同时说明"要修改什么"和"要保留什么"，编辑结果越接近预期
    "prompt": "把图里的小猫换成小马",

    # 【n】(integer, 可选) 单次请求生成图像的张数（控制输出张数，与输入图数量无关）
    # 取值范围: [1, 10]，默认值为 1
    "n": 1,

    # 【size】(string, 可选) 生成图像的分辨率（针对输出，不要求输入图预先缩放）
    # GPT image 系列可选值:
    #   "auto"       (自动选择最佳尺寸，默认值)
    #   "1024x1024"  (正方形)
    #   "1536x1024"  (横版/landscape)
    #   "1024x1536"  (竖版/portrait)
    #   "2048x2048"  (2K/方形1:1)
    #   "2048x1152"  (2K/横版16:9)
    #   "3840x2160"  (4K/横版16:9)
    #   "2160x3840"  (4K/竖版9:16)
    # 约束: 最大边长 <= 3840px；宽高必须都是 16 的倍数；长宽比不能超过 3:1；总像素必须在 655,360 到 8,294,400 之间
    "size": "1024x1024",

    # 【output_format】(string, 可选) 指定输出文件格式
    # 可选值: "png"(默认) / "jpeg"(延迟更低) / "webp"(更高压缩率)
    # 若选择 jpeg 或 webp，可再配合 output_compression 调整压缩率；落盘扩展名随该值变化
    "output_format": "png",

    # 【quality】(string, 可选) 生成图像的质量等级
    # 可选值:
    #   "auto"      (自动选择最佳质量，默认值)
    #   "low"       (低质量，生成更快成本更低，适合草稿与快速迭代)
    #   "medium"    (中等质量)
    #   "high"      (高质量)
    #   "xhigh"     (2.5 新增：超高质量)
    #   "max"       (2.5 新增：最高质量，耗时与成本最高)
    "quality": "low",

    # 【output_compression】(integer, 可选) 输出压缩率
    # 仅在 output_format 为 jpeg 或 webp 时生效；数值越高，压缩越强、文件越小
    # 取值范围: 0 <= x <= 100，默认 100
    # PNG 输出不需要该参数，保持注释即可
    "output_compression": 100,

    # 【moderation】(string, 可选) 内容审核强度
    # 可选值: "auto"(默认) / "low"(更宽松，不表示关闭审核)
    # 上游 /v1/images/edits 官方参数表未列出该参数，确认渠道支持后取消注释
    # "moderation": "low",
}

def main():
    if not image_paths:
        raise ValueError("image_paths 至少需要一张参考图")

    # 按文件后缀设置上传的 MIME 类型；网络地址的文件名后缀应与真实格式一致
    mime_map = {
        ".png": "image/png",
        ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg",
        ".webp": "image/webp",
    }

    # 准备图片文件（支持 本地文件路径 / 公网 URL，自动识别）
    # 全部输入读取成功后才发起编辑；退出 with 块时自动关闭所有文件和内存流
    with ExitStack() as stack:
        files = []
        for source in image_paths:
            is_url = source.startswith(("http://", "https://"))
            # 去掉 URL 可能携带的查询参数（如 OSS 的 ?xxx），以便取到干净的文件名与后缀
            clean_path = urlsplit(source).path if is_url else source
            file_name = Path(clean_path).name
            suffix = Path(file_name).suffix.lower()
            if suffix not in mime_map:
                raise ValueError("参考图文件名必须以 png、jpg、jpeg 或 webp 结尾")

            if is_url:
                # 公网 URL：先下载到内存，再作为文件字节上传（open 无法打开 URL）
                download = requests.get(source, timeout=120)
                download.raise_for_status()
                file_obj = stack.enter_context(io.BytesIO(download.content))
            else:
                # 本地路径：直接打开文件
                file_obj = stack.enter_context(open(source, "rb"))

            # 【image】(file, 必填) 待编辑的输入图片文件
            # 可使用一张或多张图片作为参考图，每张图重复使用同一个 image 文件字段
            # 本文示例覆盖"参考图 + 提示词"编辑，未添加 mask 上传
            files.append(("image", (file_name, file_obj, mime_map[suffix])))

        # 普通参数（data）和文件（files）共同构成一次 multipart/form-data 请求
        # 图片编辑耗时较长，timeout 给足
        response = requests.post(
            url, headers=headers, data=payload, files=files, timeout=1000
        )

    print("status:", response.status_code)
    response.raise_for_status()

    # 解析响应 JSON；非 JSON 通常是渠道或网关报错
    try:
        result = response.json()
    except ValueError as exc:
        raise RuntimeError("接口未返回有效 JSON，请检查响应与渠道配置") from exc

    # 图片结果位于 data 数组，每个元素对应一张图
    items = result.get("data") if isinstance(result, dict) else None
    if not isinstance(items, list) or not items:
        raise RuntimeError("响应中没有非空 data 数组")

    # 结果统一保存到当前工作目录下的 output 文件夹
    output_dir = Path("output")
    output_dir.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    # 按 output_format 决定保存扩展名（jpeg 统一写成 .jpg）
    extension = payload.get("output_format", "png").lower()
    if extension == "jpeg":
        extension = "jpg"

    for index, item in enumerate(items, start=1):
        if not isinstance(item, dict):
            raise RuntimeError(f"第 {index} 个图片结果不是对象")
        if item.get("b64_json"):
            # 上游 GPT Image 默认返回 Base64 图片，优先解码
            image_bytes = base64.b64decode(item["b64_json"], validate=True)
        elif item.get("url"):
            # 沿用参考页的客户端兼容分支，不表示官方模型保证返回 URL
            download = requests.get(item["url"], timeout=120)
            download.raise_for_status()
            image_bytes = download.content
        else:
            raise RuntimeError(f"第 {index} 个图片结果缺少有效图片内容")

        # 以时间戳 + 序号命名，写入 output 目录
        output_path = output_dir / f"edited_{timestamp}_{index}.{extension}"
        output_path.write_bytes(image_bytes)
        print(f"saved {output_path}")


if __name__ == "__main__":
    main()
```
## 返回示例
```text
status: 200
saved output\edited_20260909_194855_1.png
```
<p align="center">
  <small>© 2026 DMXAPI gpt-image-2.5 图片编辑</small>
</p>
