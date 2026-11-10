# gpt-image-2.6 图片编辑 API 使用文档

通过 `/v1/images/edits` 接口上传一张或多张参考图，配合文字指令使用 `gpt-image-2.6-sunburst` 或 `gpt-image-2.6-flare` 编辑图片。参考图可使用本地文件路径或公网 URL，示例脚本会按文件名后缀判断格式并上传。
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
| `gpt-image-2.6-sunburst-ssvip` | 原价模型稳定性高 | 更关注最终编辑效果与细节时选用 |
| `gpt-image-2.6-flare-ssvip` | 原价模型稳定性高 | 更关注编辑速度时选用 |
| `gpt-image-2.6-sunburst` | 以图像质量为重点的基础模型 | 更关注最终编辑效果与细节时选用 |
| `gpt-image-2.6-flare` | 以生成速度为重点的小模型 | 更关注编辑速度时选用 |

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
# 官方输入为 png、webp 或 jpg，单张小于 50MB，最多 16 张；不要上传 GIF 或 SVG
# 编辑可以输出 GIF，但参考图必须是静图
image_paths = [
    r"C:\Users\Y\Desktop\马尾辫\小狗.png",
    # "https://your-cdn.example.com/reference-image.png",
]

markup_path = None
# markup_path = r"C:\path\to\markup.png"

# API 配置
url = "https://www.dmxapi.cn/v1/images/edits"
api_key = "sk-=========================================="  # 在引号内粘贴完整 API 令牌

# 请求头：只放 Bearer 鉴权
# multipart/form-data 的 Content-Type 与 boundary 由 requests 自动生成，不要手动指定 JSON 请求头
headers = {
    "Authorization": f"Bearer {api_key}",
}

# 请求参数（multipart 普通字段，通过 data=payload 发送）
payload = {
    # 【model】(string, 必填) 使用的图像编辑模型名称
    # 可选值:
    #   "gpt-image-2.6-sunburst"  (以图像质量为重点的基础模型，示例默认)
    #   "gpt-image-2.6-flare"     (以生成速度为重点的小模型)
    "model": "gpt-image-2.6-sunburst",

    # 【prompt】(string, 必填) 描述希望模型如何编辑输入图片
    # GPT image 系列模型最大长度 32000 字符
    # 可同时说明"要修改什么"和"要保留什么"，编辑结果越接近预期
    "prompt": "在原图的基础上，将小狗的毛发颜色改为金黄色，保持背景不变，确保小狗的表情自然。",

    # 【n】(integer, 可选) 单次请求生成图像的张数（控制输出张数，与输入图数量无关）
    # 取值范围: [1, 10]，默认值为 1
    "n": 1,

    # 【size】(string, 可选) 生成图像的分辨率（针对输出，不要求输入图预先缩放）
    # GPT image 系列常用尺寸:
    #   "auto"       (自动选择最佳尺寸，默认值)
    #   "1024x1024"  (正方形)
    #   "1536x1024"  (横版/landscape)
    #   "1024x1536"  (竖版/portrait)
    #   "2048x2048"  (2K/方形1:1)
    #   "2048x1152"  (2K/横版16:9)
    #   "3840x2160"  (4K/横版16:9)
    #   "2160x3840"  (4K/竖版9:16)
    # 自定义约束: 宽高必须都是 16 的倍数；长短边比不能超过 3:1
    # 2K/4K 及尺寸上限沿用 2.5 文档作为参考，实际以 2.6 渠道支持为准:
    #   最大边长 <= 3840px；总像素在 655,360 到 8,294,400 之间
    # 输出 GIF 时，size 是每一帧的尺寸；帧数、帧尺寸和 n 必须同时落在模型限制与总像素预算内
    "size": "auto",

    # 【output_format】(string, 可选) 指定输出文件格式
    # 可选值: "png"(默认) / "jpeg"(延迟更低) / "webp"(更高压缩率) / "gif"(动画输出)
    # 若选择 jpeg 或 webp，可再配合 output_compression 调整压缩率；落盘扩展名随该值变化
    # 编辑不支持 SVG 输出，也不接受 SVG 或 GIF 作为输入；GIF 输出要用静图做参考
    # GIF 不支持 streaming、partial images、mask、output_compression，且需要账号有 GIF preview 权限
    "output_format": "gif",

    # 【frame_count】(integer, 可选) 仅 output_format 为 gif 时使用
    # 取值范围: 2 <= x <= 16，省略时默认 9
     "frame_count": 9,

    # 【frame_duration_ms】(integer, 可选) 仅 output_format 为 gif 时使用
    # 指南范围: 20 <= x <= 2000，按 10ms 取整，默认 200
    # API reference 另将编码延迟上限记为 655350ms
    # "frame_duration_ms": 200,

    # 【quality】(string, 可选) 生成图像的质量等级
    # 可选值:
    #   "auto"      (自动选择最佳质量，默认值)
    #   "low"       (低质量，生成更快成本更低，适合草稿与快速迭代)
    #   "medium"    (中等质量)
    #   "high"      (高质量)
    #   "xhigh"     (超高质量)
    #   "max"       (最高质量，耗时与成本最高)
    "quality": "low",

    # 【complexity】(string, 可选) 2.6 新增：控制渲染前的规划投入
    # 可选值（以下三档均已在两款模型的编辑接口实测）:
    #   "low"       (较少规划，适合局部修改与简单编辑)
    #   "medium"    (中等规划投入)
    #   "high"      (更多规划，适合复杂布局与多条件编辑，默认值)
    # 与 quality 独立：complexity 控制规划投入，quality 控制渲染细节
    # 编辑接口实测三档均成功，非法值返回 400 invalid_value；已确认参数接收与取值校验
    "complexity": "high",

    # 【output_compression】(integer, 可选) 输出压缩率
    # 仅在 output_format 为 jpeg 或 webp 时使用
    # 取值范围: 0 <= x <= 100，默认 100
    # PNG 输出不需要该参数，保持注释即可
    # "output_compression": 100,

    # 【moderation】(string, 可选) 内容审核强度
    # 可选值: "auto"(默认) / "low"(更宽松，不表示关闭审核)
    "moderation": "low",

    # 【background】(string, 可选) 输出图像的背景模式
    # 可选值:
    #   "auto"         (自动选择背景，默认值)
    #   "opaque"       (不透明背景)
    #   "transparent"  (透明背景；请选择 png 或 webp)
    "background": "auto",
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
            # 本文示例覆盖"参考图 + 提示词"编辑；markup 当前保持关闭，未添加 mask 上传
            files.append(("image", (file_name, file_obj, mime_map[suffix])))

        # 【markup】(file, 可选) 上游定义的透明 PNG 标注层，作为文件字段上传
        # 当前渠道未确认生效：两款模型均接受损坏标注文件，也都在圈选测试中出现过改错对象
        # 以下为上游要求，不能据此认定当前渠道已支持；确认支持前保持 markup_path = None
        # 宽高须与第一张输入图应用方向信息后的尺寸一致，不是与输出 size 一致
        # 必须包含透明像素；标注图不超过 50MB，且标注图和第一张输入图均不超过 16,777,216 像素
        # 不可与 mask 同时使用；2.5 与 2.6 均支持该参数
        if markup_path:
            markup_file = Path(markup_path)
            if markup_file.suffix.lower() != ".png":
                raise ValueError("markup 必须是透明 PNG 标注图")
            markup_obj = stack.enter_context(open(markup_file, "rb"))
            files.append(("markup", (markup_file.name, markup_obj, "image/png")))

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
saved output\edited_20261105_194855_1.png
```
<p align="center">
  <small>© 2026 DMXAPI gpt-image-2.6 图片编辑</small>
</p>
