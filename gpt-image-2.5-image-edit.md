# gpt-image-2.5 图片编辑 API 使用文档

通过 DMXAPI 代理的 `/v1/images/edits` 接口上传一张或多张参考图，配合文字指令使用 `gpt-image-2.5-sunburst` 或 `gpt-image-2.5-flare` 编辑图片。本文沿用 GPT Image 2 参考文档的 multipart 文件上传方式，提供本地图片、网络图片读取以及结果保存的完整 Python 示例。

**适用说明：** 接口写法依据 DMXAPI 现有参考文档，2.5 型号与新增参数依据 OpenAI 官方资料。截至 2026-09-09，本文尚未通过 DMXAPI 实际调用验证两款模型及新增参数；模型可用性、渠道别名和参数限制以 DMXAPI 实际配置为准。下文标注的“上游规格”不代表代理渠道已经实测通过。

## 接口地址

| 接口 | 请求方式 | URL |
|------|---------|-----|
| 图片编辑 | POST | `https://www.dmxapi.cn/v1/images/edits` |

:::warning
请妥善保管 DMXAPI API Key，勿在前端代码、公开仓库或日志中暴露。运行前，将示例中 `api_key` 引号内的星号占位内容替换为你的完整 API 令牌。
:::

请求头 `Authorization` 的值由 `f"Bearer {api_key}"` 生成。普通参数用 `data=payload` 传入，图片用 `files=files` 上传；`requests` 自动生成 `multipart/form-data` 的 Content-Type 和 boundary，请勿手动指定 JSON 请求头。[DMXAPI 图片编辑参考文档](https://doc.dmxapi.cn/gpt-image-2-image-edit.html)

## 模型名称

| 模型 ID | 官方定位 | 使用选择 |
|------|------|------|
| `gpt-image-2.5-sunburst` | 以图像质量为重点的基础模型 | 更关注最终编辑效果与细节时选用 |
| `gpt-image-2.5-flare` | 以生成速度为重点的小模型 | 更关注编辑速度时选用 |

示例默认使用 Sunburst，切换 Flare 时修改 `payload["model"]`。两款模型均支持图片编辑；本文不推测额外渠道后缀，也不提供未经实测的速度倍数或固定耗时。[Sunburst 模型说明](https://developers.openai.com/api/docs/models/gpt-image-2.5-sunburst)、[Flare 模型说明](https://developers.openai.com/api/docs/models/gpt-image-2.5-flare)

## 图片编辑参数说明

以下是本文示例涉及的参数。默认值、枚举与范围按上游资料说明；multipart 普通字段由 `requests` 编码，图片保留为文件字段。

| 参数 | 位置 | 类型 | 必填 | 说明 |
|------|------|------|------|------|
| `model` | multipart 普通字段 | string | 本文显式指定 | 使用上表两个模型 ID 之一；示例为 Sunburst |
| `prompt` | multipart 普通字段 | string | 是 | 编辑要求；上游最长 32,000 字符；可说明要修改和要保留的内容 |
| `image` | multipart 文件字段 | file，可重复 | 是 | 按参考页使用重复的 `image` 字段上传一张或多张图片 |
| `size` | multipart 普通字段 | string | 否 | 输出尺寸，默认 `auto`；示例 `1024x1024`；不表示输入图片需要预先改成该尺寸 |
| `background` | multipart 普通字段 | string | 否 | `auto`（默认）、`opaque`、`transparent`；示例 `auto`；透明输出需 `png` 或 `webp` |
| `output_compression` | multipart 普通字段 | integer | 否 | 0～100；仅 `jpeg` 或 `webp` 输出时使用；PNG 示例不发送 |
| `output_format` | multipart 普通字段 | string | 否 | `png`、`jpeg`、`webp`；默认 `png`；保存扩展名随配置变化 |
| `quality` | multipart 普通字段 | string | 否 | `auto`、`low`、`medium`、`high`、`xhigh`、`max`；默认 `auto`；示例沿用参考页的 `low` |
| `n` | multipart 普通字段 | integer | 否 | 生成结果的张数，默认 1；示例 1；上游当前范围 1～10，DMXAPI 的 2.5 批量上限尚未实测 |

两款 2.5 模型都在已有质量档位之外支持 `xhigh` 和 `max`，并支持透明背景。这些是上游规格，新增参数在 DMXAPI 的可用性需要结合实际渠道确认。[官方编辑接口参数](https://developers.openai.com/api/reference/resources/images/methods/edit)

### 输入图片与输出尺寸

`image_paths` 是示例脚本的本地配置，**不是 API 参数**。本地文件使用路径读取；HTTP(S) 地址先下载到内存，再以文件字节上传。参考页证明的是这种客户端处理方式，不能据此把 URL 字符串直接作为 `image` 发送，也不能直接改用 JSON `images` 请求体。[DMXAPI 图片读取与上传示例](https://doc.dmxapi.cn/gpt-image-2-image-edit.html)

示例按 `.png`、`.jpg`、`.jpeg`、`.webp` 后缀设置上传 MIME 类型。网络地址需要能直接返回图片，文件名后缀应与真实格式一致；带查询参数的 URL 会用路径部分识别后缀。多图输入可向列表继续添加路径，`n` 控制的是输出张数。本文示例覆盖“参考图 + 提示词”编辑，没有添加 `mask` 上传。

上游输出可使用 `1024x1024`、`1536x1024`、`1024x1536` 或合规自定义尺寸：宽高均为 16 的倍数，单边不超过 3840 像素，长宽比介于 1:3 与 3:1，总像素为 655,360～8,294,400。总像素超过 3,686,400 的输出属于实验性能力，例如 `2048x2048` 和 `3840x2160`。这些约束针对输出 `size`。[官方图像生成指南](https://developers.openai.com/api/docs/guides/image-generation)

## 图片编辑示例代码

运行环境：Python 3，依赖 `requests`，可通过 `python -m pip install requests` 安装。把你的完整 API 令牌直接粘贴到下方 `api_key` 的引号内，将 `image_paths` 替换为实际参考图路径，再运行代码。模型、提示词、尺寸等参数直接在 `payload` 中修改。示例中的 `example.com` 域名地址仅为占位，不能直接使用。

```python
import base64
import io
from contextlib import ExitStack
from datetime import datetime
from pathlib import Path
from urllib.parse import urlsplit

import requests

# 客户端图片配置：替换为实际路径；多图可继续添加列表项
image_paths = [
    r"C:\path\to\reference-image.jpg",
    # "https://your-cdn.example.com/reference-image.png",
]

url = "https://www.dmxapi.cn/v1/images/edits"
api_key = "sk-*****************************************"  # 在引号内粘贴完整 API 令牌

headers = {
    "Authorization": f"Bearer {api_key}",
}

payload = {
    # 【model】(string, 本文必填) 可改为 gpt-image-2.5-flare
    # 渠道可用性以 DMXAPI 为准
    "model": "gpt-image-2.5-sunburst",

    # 【prompt】(string, 必填) 编辑要求；上游最多 32000 字符
    "prompt": "把图里的小猫换成小马",

    # 【size】(string, 可选) 输出尺寸，默认 auto
    # 自定义宽高须满足正文中的尺寸、长宽比和像素限制
    "size": "1024x1024",

    # 【background】(string, 可选) auto（默认）/ opaque / transparent
    # transparent 需 png 或 webp，使用前确认渠道支持
    "background": "auto",

    # 【output_compression】(integer, 可选) 0～100
    # 仅在 output_format 为 jpeg 或 webp 时取消注释
    # "output_compression": 100,

    # 【output_format】(string, 可选) png / jpeg / webp；默认 png
    "output_format": "png",

    # 【quality】(string, 可选) auto / low / medium / high / xhigh / max
    # 默认 auto；示例沿用 low，可按需求调整
    "quality": "low",

    # 【n】(integer, 可选) 结果张数，默认 1
    # 上游当前为 1～10；代理 2.5 上限尚未实测
    "n": 1,
}


def main():
    if not image_paths:
        raise ValueError("image_paths 至少需要一张参考图")

    mime_map = {
        ".png": "image/png",
        ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg",
        ".webp": "image/webp",
    }

    # 全部输入读取成功后才发起编辑；退出时关闭所有文件和内存流
    with ExitStack() as stack:
        files = []
        for source in image_paths:
            is_url = source.startswith(("http://", "https://"))
            clean_path = urlsplit(source).path if is_url else source
            file_name = Path(clean_path).name
            suffix = Path(file_name).suffix.lower()
            if suffix not in mime_map:
                raise ValueError("参考图文件名必须以 png、jpg、jpeg 或 webp 结尾")

            if is_url:
                download = requests.get(source, timeout=120)
                download.raise_for_status()
                file_obj = stack.enter_context(io.BytesIO(download.content))
            else:
                file_obj = stack.enter_context(open(source, "rb"))

            # 【image】(file, 必填) 每张图重复使用同一个 image 文件字段
            files.append(("image", (file_name, file_obj, mime_map[suffix])))

        # 普通参数和文件共同构成一次 multipart 请求
        response = requests.post(
            url, headers=headers, data=payload, files=files, timeout=1000
        )

    print("status:", response.status_code)
    response.raise_for_status()
    try:
        result = response.json()
    except ValueError as exc:
        raise RuntimeError("接口未返回有效 JSON，请检查响应与渠道配置") from exc

    items = result.get("data") if isinstance(result, dict) else None
    if not isinstance(items, list) or not items:
        raise RuntimeError("响应中没有非空 data 数组")

    output_dir = Path("output")
    output_dir.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    extension = payload.get("output_format", "png").lower()
    if extension == "jpeg":
        extension = "jpg"

    for index, item in enumerate(items, start=1):
        if not isinstance(item, dict):
            raise RuntimeError(f"第 {index} 个图片结果不是对象")
        if item.get("b64_json"):
            image_bytes = base64.b64decode(item["b64_json"], validate=True)
        elif item.get("url"):
            # 沿用参考页的客户端兼容分支，不表示官方模型保证返回 URL
            download = requests.get(item["url"], timeout=120)
            download.raise_for_status()
            image_bytes = download.content
        else:
            raise RuntimeError(f"第 {index} 个图片结果缺少有效图片内容")

        output_path = output_dir / f"edited_{timestamp}_{index}.{extension}"
        output_path.write_bytes(image_bytes)
        print(f"saved {output_path}")


if __name__ == "__main__":
    main()
```

## 返回示例

以下为 Windows 上 `n=1`、输出 PNG 时的**脚本运行输出示意**，不是原始 API 响应，也不是本次对 GPT Image 2.5 的实测记录。文件名时间戳会随运行时间变化。

```text
status: 200
saved output\edited_20260909_194855_1.png
```

HTTP 响应按 JSON 解析。示例优先读取 `data[].b64_json` 并解码；`data[].url` 是沿用 DMXAPI 参考页的客户端兼容分支，不代表上游保证返回图片 URL。结果保存在当前工作目录下的 `output` 文件夹；切换到 JPEG 或 WebP 后，文件扩展名会相应变为 `.jpg` 或 `.webp`。[DMXAPI 返回处理参考](https://doc.dmxapi.cn/gpt-image-2-image-edit.html)

## 从 gpt-image-2 迁移

沿用 multipart 普通字段与重复 `image` 文件字段，先替换成 DMXAPI 实际开放的 2.5 型号进行基础验证。确认之后再逐项调整质量、背景和分辨率。对于希望保留主体的编辑，可以在提示词中同时说明“修改什么”和“保留什么”，例如修改背景但保持主体位置、比例和可见文字；这是提示词写法建议，不构成像素级保持保证。[官方图像提示词指南](https://developers.openai.com/api/docs/guides/image-prompting)

<p align="center">
  <small>© 2026 DMXAPI gpt-image-2.5 图片编辑</small>
</p>
