# Agnes Image 2.5 Flash 图生图 API 文档

用一张参考图和文字指令编辑画面。提示词可以分别说明要修改和要保留的内容。例如，将水果静物照片改为水彩画，同时保留水果的位置、轮廓和投影方向。

## 📌 接口地址

```text
POST https://www.dmxapi.cn/v1/images/generations
```

在 `Authorization` 请求头中传入 DMXAPI 密钥，请求体使用 `application/json`。

## 🎨 请求参数

| 参数 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `model` | string | 是 | `agnes-image-2.5-flash` |
| `prompt` | string | 是 | 描述编辑指令，例如更换背景、调整颜色或转换画风，并指出需要保留的细节。 |
| `size` | string | 是 | 输出尺寸档位，支持 `1K`、`2K`、`3K`、`4K`。 |
| `ratio` | string | 否 | 输出宽高比，默认 `1:1`。各档位的可选比例见[输出尺寸表](/agnes-image-25-flash-t2i#output-sizes)。 |
| `extra_body.image` | string[] | 是 | 单图编辑也使用数组，其中放一张图片的公开 HTTPS 链接或带 MIME 类型的 Base64 Data URI。 |
| `extra_body.response_format` | string | 否 | 填 `url` 返回图片链接，填 `b64_json` 返回 Base64 图像数据。 |

`extra_body` 里的字段不要写到请求体顶层。出图可能需要数秒到几十秒，客户端超时建议设在 60 至 360 秒之间，示例使用 180 秒。

## 💻 Python 示例代码

安装 `requests`（`python -m pip install requests`），并在运行脚本的终端设置环境变量 `DMXAPI_API_KEY`。第一个示例使用公开的水果照片，第二个示例读取当前目录的 `fruits.jpg`。两种输入方式均可搭配任一返回格式。

::: code-group

```python [URL 输出]
import os

import requests

payload = {
    "model": "agnes-image-2.5-flash",
    "prompt": "把这张水果静物照片画成水彩画，背景换成米白色画纸，保留每个水果的位置、轮廓和投影方向。",
    "size": "1K",
    "ratio": "1:1",
    "extra_body": {
        "image": ["https://cdn.jsdelivr.net/gh/opencv/opencv@4.10.0/samples/data/fruits.jpg"],
        "response_format": "url",
    },
}
response = requests.post(
    "https://www.dmxapi.cn/v1/images/generations",
    headers={"Authorization": os.environ["DMXAPI_API_KEY"]},
    json=payload,
    timeout=180,
)
response.raise_for_status()
print(response.json()["data"][0]["url"])
```

```python [Base64 输出]
import base64
import os
from pathlib import Path

import requests

# 读取 JPEG 原图并构造 Data URI。使用 PNG 原图时，将 MIME 类型改为 image/png。
source = Path("fruits.jpg")
encoded_image = base64.b64encode(source.read_bytes()).decode("ascii")
payload = {
    "model": "agnes-image-2.5-flash",
    "prompt": "把这张水果静物照片画成水彩画，背景换成米白色画纸，保留每个水果的位置、轮廓和投影方向。",
    "size": "1K",
    "ratio": "1:1",
    "extra_body": {
        "image": [f"data:image/jpeg;base64,{encoded_image}"],
        "response_format": "b64_json",
    },
}
response = requests.post(
    "https://www.dmxapi.cn/v1/images/generations",
    headers={"Authorization": os.environ["DMXAPI_API_KEY"]},
    json=payload,
    timeout=180,
)
response.raise_for_status()
encoded = response.json()["data"][0]["b64_json"]
output = Path("agnes-watercolor.png")
output.write_bytes(base64.b64decode(encoded))
print(output.resolve())
```

:::

## 📤 返回示例

以下仅展示图片字段，链接和 Base64 字符串为示意值。URL 输出读取 `data[0].url`，Base64 输出读取 `data[0].b64_json`。

::: code-group

```json [URL 输出]
{
  "data": [{ "url": "https://example.com/generated/watercolor.png" }]
}
```

```json [Base64 输出]
{
  "data": [{ "b64_json": "iVBORw0KGgoAAAANSUhEUgAA..." }]
}
```

:::

另见 [文生图](/agnes-image-25-flash-t2i) · [多图合成](/agnes-image-25-flash-images) · [Agnes 官方模型说明](https://agnes-ai.com/zh-Hans/docs/agnes-image-25-flash) · [DMXAPI 模型价格](https://www.dmxapi.cn/rmb)

<p align="center">
  <small>© 2026 DMXAPI Agnes Image 2.5 Flash 图生图 API 文档</small>
</p>
