# Agnes Image 2.5 Flash 多图合成 API 文档

用多张参考图生成一张新图。例如，取第一张图的水果和第二张图的咖啡杯，组合成一张早餐海报。按提示词里提及的顺序传图，并写明每张图提供什么元素、这些元素在画面中如何摆放。

## 📌 接口地址

```text
POST https://www.dmxapi.cn/v1/images/generations
```

在 `Authorization` 请求头中传入 DMXAPI 密钥，请求体使用 `application/json`。

## 🎨 请求参数

| 参数 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `model` | string | 是 | `agnes-image-2.5-flash` |
| `prompt` | string | 是 | 按图号说明各参考图的用途，并描述最终画面的布局、光线和风格。 |
| `size` | string | 是 | 输出尺寸档位，支持 `1K`、`2K`、`3K`、`4K`。 |
| `ratio` | string | 否 | 输出宽高比，默认 `1:1`。各档位的可选比例见[输出尺寸表](/agnes-image-25-flash-t2i#output-sizes)。 |
| `extra_body.image` | string[] | 是 | 按顺序放入两张或更多参考图。每个元素可以是公开 HTTPS 图片链接，也可以是带 MIME 类型的 Base64 Data URI。 |
| `extra_body.response_format` | string | 否 | 填 `url` 返回图片链接，填 `b64_json` 返回 Base64 图像数据。 |

`extra_body` 里的字段不要写到请求体顶层。出图可能需要数秒到几十秒，客户端超时建议设在 60 至 360 秒之间，示例使用 180 秒。

## 💻 Python 示例代码

安装 `requests`（`python -m pip install requests`），并在运行脚本的终端设置环境变量 `DMXAPI_API_KEY`。第一个示例使用两张公开图片。第二个示例把图 2 换成当前目录的 `coffee.png`，图 1 仍使用公开链接。

::: code-group

```python [URL 输出]
import os

import requests

payload = {
    "model": "agnes-image-2.5-flash",
    "prompt": "制作一张竖版早餐海报。把图 1 的水果摆在浅木桌左前方，把图 2 的咖啡杯放在右后方，保留各自的形状和颜色。让两者都受到左侧窗光照射，画面顶部留白。",
    "size": "2K",
    "ratio": "3:4",
    "extra_body": {
        "image": [
            "https://cdn.jsdelivr.net/gh/opencv/opencv@4.10.0/samples/data/fruits.jpg",
            "https://cdn.jsdelivr.net/gh/scikit-image/scikit-image@v0.24.0/skimage/data/coffee.png",
        ],
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

# 图 2 使用本地 PNG 照片。Data URI 的 MIME 类型应与文件格式一致。
coffee = base64.b64encode(Path("coffee.png").read_bytes()).decode("ascii")
payload = {
    "model": "agnes-image-2.5-flash",
    "prompt": "制作一张竖版早餐海报。把图 1 的水果摆在浅木桌左前方，把图 2 的咖啡杯放在右后方，保留各自的形状和颜色。让两者都受到左侧窗光照射，画面顶部留白。",
    "size": "2K",
    "ratio": "3:4",
    "extra_body": {
        "image": [
            "https://cdn.jsdelivr.net/gh/opencv/opencv@4.10.0/samples/data/fruits.jpg",
            f"data:image/png;base64,{coffee}",
        ],
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
output = Path("agnes-breakfast.png")
output.write_bytes(base64.b64decode(encoded))
print(output.resolve())
```

:::

## 📤 返回示例

以下仅展示图片字段，链接和 Base64 字符串为示意值。URL 输出读取 `data[0].url`，Base64 输出读取 `data[0].b64_json`。

::: code-group

```json [URL 输出]
{
  "data": [{ "url": "https://example.com/generated/breakfast.png" }]
}
```

```json [Base64 输出]
{
  "data": [{ "b64_json": "iVBORw0KGgoAAAANSUhEUgAA..." }]
}
```

:::

另见 [文生图](/agnes-image-25-flash-t2i) · [图生图](/agnes-image-25-flash-i2i) · [Agnes 官方模型说明](https://agnes-ai.com/zh-Hans/docs/agnes-image-25-flash) · [DMXAPI 模型价格](https://www.dmxapi.cn/rmb)

<p align="center">
  <small>© 2026 DMXAPI Agnes Image 2.5 Flash 多图合成 API 文档</small>
</p>
