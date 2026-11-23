# Agnes Image 2.5 Flash 文生图 API 文档

用文字生成一张图片。适合需要安排多个视觉元素的场景，例如在一张早市插画中分别指定前景的水果摊、中景的商贩和远处的渔船。

## 📌 接口地址

```text
POST https://www.dmxapi.cn/v1/images/generations
```

在 `Authorization` 请求头中传入 DMXAPI 密钥，请求体使用 `application/json`。

## 🎨 请求参数

| 参数 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `model` | string | 是 | `agnes-image-2.5-flash` |
| `prompt` | string | 是 | 描述要生成的画面，可指定主体、背景、光线和构图。 |
| `size` | string | 是 | 输出尺寸档位，支持 `1K`、`2K`、`3K`、`4K`。 |
| `ratio` | string | 否 | 与尺寸档位搭配使用，默认 `1:1`。所有可选比例见下方的[输出尺寸表](#output-sizes)。 |
| `extra_body.response_format` | string | 否 | 填 `url` 返回图片链接，填 `b64_json` 返回 Base64 图像数据。 |

`extra_body` 里的字段不要写到请求体顶层。出图可能需要数秒到几十秒，客户端超时建议设在 60 至 360 秒之间，示例使用 180 秒。

## 💻 Python 示例代码

安装 `requests`（`python -m pip install requests`），并在运行脚本的终端设置环境变量 `DMXAPI_API_KEY`。以下两个示例都生成 `2K` 横版插画。

::: code-group

```python [URL 输出]
import os

import requests

payload = {
    "model": "agnes-image-2.5-flash",
    "prompt": "画一张海边早市的横版插画。前景是摆满柑橘的木摊，中景有撑条纹伞的商贩，远景是晨雾中的渔船。晨光从左侧照入，让果皮纹理清晰可见。",
    "size": "2K",
    "ratio": "16:9",
    "extra_body": {"response_format": "url"},
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

payload = {
    "model": "agnes-image-2.5-flash",
    "prompt": "画一张海边早市的横版插画。前景是摆满柑橘的木摊，中景有撑条纹伞的商贩，远景是晨雾中的渔船。晨光从左侧照入，让果皮纹理清晰可见。",
    "size": "2K",
    "ratio": "16:9",
    "extra_body": {"response_format": "b64_json"},
}
response = requests.post(
    "https://www.dmxapi.cn/v1/images/generations",
    headers={"Authorization": os.environ["DMXAPI_API_KEY"]},
    json=payload,
    timeout=180,
)
response.raise_for_status()
encoded = response.json()["data"][0]["b64_json"]
output = Path("agnes-market.png")
output.write_bytes(base64.b64decode(encoded))
print(output.resolve())
```

:::

## 📤 返回示例

以下仅展示图片字段，链接和 Base64 字符串为示意值。URL 输出读取 `data[0].url`，Base64 输出读取 `data[0].b64_json`。

::: code-group

```json [URL 输出]
{
  "data": [{ "url": "https://example.com/generated/market.png" }]
}
```

```json [Base64 输出]
{
  "data": [{ "b64_json": "iVBORw0KGgoAAAANSUhEUgAA..." }]
}
```

:::

## 输出尺寸 {#output-sizes}

下表列出三种工作流共用的输出尺寸，单位为像素。`size` 也兼容 `1024x768` 等历史写法，服务可能将指定的宽高映射到原生尺寸。例如，要做 `1920x1080` 的壁纸，可以先用 `2K` 和 `16:9` 生成 `2624x1472` 的图片，再裁剪或缩放到目标画布。

| `ratio` | `1K` | `2K` | `3K` | `4K` |
| --- | --- | --- | --- | --- |
| `1:1` | 1024x1024 | 2048x2048 | 3072x3072 | 4096x4096 |
| `3:4` | 864x1152 | 1728x2304 | 2592x3456 | 3456x4608 |
| `4:3` | 1152x864 | 2304x1728 | 3456x2592 | 4608x3456 |
| `16:9` | 1312x736 | 2624x1472 | 3936x2208 | 5248x2944 |
| `9:16` | 736x1312 | 1472x2624 | 2208x3936 | 2944x5248 |
| `2:3` | 832x1248 | 1664x2496 | 2496x3744 | 3328x4992 |
| `3:2` | 1248x832 | 2496x1664 | 3744x2496 | 4992x3328 |
| `21:9` | 1568x672 | 3136x1344 | 4704x2016 | 6272x2688 |

另见 [图生图](/agnes-image-25-flash-i2i) · [多图合成](/agnes-image-25-flash-images) · [Agnes 官方模型说明](https://agnes-ai.com/zh-Hans/docs/agnes-image-25-flash) · [DMXAPI 模型价格](https://www.dmxapi.cn/rmb)

<p align="center">
  <small>© 2026 DMXAPI Agnes Image 2.5 Flash 文生图 API 文档</small>
</p>
