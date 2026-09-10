# gpt-image-2.5 文生图 API 使用文档

通过 DMXAPI 代理的 `/v1/images/generations` 接口提交文本提示词，使用 `gpt-image-2.5-sunburst` 或 `gpt-image-2.5-flare` 生成图片。本文沿用 GPT Image 2 参考文档中的 JSON 请求、Bearer 鉴权和图片保存方式，补充 GPT Image 2.5 的模型选择、质量档位与透明背景配置。

**适用说明：** 接口写法依据 DMXAPI 现有参考文档，2.5 型号与新增参数依据 OpenAI 官方资料。截至 2026-09-09，本文尚未通过 DMXAPI 实际调用验证两款模型及新增参数；模型可用性、渠道别名和参数限制以 DMXAPI 实际配置为准。下文标注的“上游规格”不代表代理渠道已经实测通过。

## 接口地址

| 接口 | 请求方式 | URL |
|------|---------|-----|
| 文生图 | POST | `https://www.dmxapi.cn/v1/images/generations` |

:::warning
请妥善保管 DMXAPI API Key，勿在前端代码、公开仓库或日志中暴露。运行前，将示例中 `api_key` 引号内的星号占位内容替换为你的完整 API 令牌。
:::

请求体使用 `application/json`，请求头 `Authorization` 的值由 `f"Bearer {api_key}"` 生成。接口同步返回结果，客户端从响应 JSON 中读取图片并保存。[DMXAPI 文生图参考文档](https://doc.dmxapi.cn/gpt-image-2-text-to-image.html)

## 模型名称

| 模型 ID | 官方定位 | 使用选择 |
|------|------|------|
| `gpt-image-2.5-sunburst` | 以图像质量为重点的基础模型 | 更关注最终画面质量时选用 |
| `gpt-image-2.5-flare` | 以生成速度为重点的小模型 | 更关注生成速度时选用 |

示例默认使用 Sunburst；使用 Flare 时，仅修改 `payload["model"]` 的值。两者是独立型号，`flare` 并非 Sunburst 的质量参数；本文不推测额外的 `-ssvip` 等渠道后缀。[Sunburst 模型说明](https://developers.openai.com/api/docs/models/gpt-image-2.5-sunburst)、[Flare 模型说明](https://developers.openai.com/api/docs/models/gpt-image-2.5-flare)

## 文生图参数说明

以下是本文示例涉及的参数。默认值、枚举与范围按上游资料说明；示例值是本次请求主动设置的值。

| 参数 | 位置 | 类型 | 必填 | 说明 |
|------|------|------|------|------|
| `model` | JSON | string | 本文显式指定 | 使用上表两个模型 ID 之一；示例为 Sunburst |
| `prompt` | JSON | string | 是 | 期望生成的画面；上游最多 32,000 字符 |
| `n` | JSON | integer | 否 | 生成张数，默认 1；示例为 1；上游当前范围 1～10，DMXAPI 的 2.5 批量上限尚未实测 |
| `size` | JSON | string | 否 | 输出尺寸，默认 `auto`；示例 `1024x1024`；自定义尺寸见下文 |
| `output_format` | JSON | string | 否 | `png`、`jpeg`、`webp`；默认 `png` |
| `quality` | JSON | string | 否 | `auto`、`low`、`medium`、`high`、`xhigh`、`max`；默认 `auto`；示例 `high` |
| `output_compression` | JSON | integer | 否 | 0～100；上游默认 100；仅输出 `jpeg` 或 `webp` 时使用；PNG 示例不发送 |
| `moderation` | JSON | string | 否 | 内容审核级别：`auto`（默认）、`low`；示例沿用参考页的 `low`，不表示关闭审核 |
| `background` | JSON | string | 否 | `auto`（默认）、`opaque`、`transparent`；透明背景须搭配 `png` 或 `webp`；示例保留为可选注释 |

2.5 在 `low`、`medium`、`high` 之外新增 `xhigh` 和 `max`。需要测试这两档时修改 `quality`，无需更换接口；它们在 DMXAPI 的可用性仍需按实际渠道确认。[官方生成接口参数](https://developers.openai.com/api/reference/resources/images/methods/generate)

### 尺寸与透明背景

常用尺寸包括 `1024x1024`（方形）、`1536x1024`（横向）、`1024x1536`（竖向）。还可以使用符合模型限制的自定义 `宽x高` 字符串，例如 `2048x1152`。

上游尺寸约束：宽高均为 16 的倍数，单边不超过 3840 像素，长宽比介于 1:3 与 3:1，总像素在 655,360～8,294,400 之间。总像素超过 3,686,400 的输出属于实验性能力，例如 `2048x2048`、`3840x2160` 和 `2160x3840`。这些限制需要同时满足。[官方图像生成指南](https://developers.openai.com/api/docs/guides/image-generation)

需要透明素材时，设置 `background="transparent"`，并保持 `output_format="png"` 或改用 `webp`。JPEG 不支持透明输出；提示词中也可以直接描述“透明背景”。[官方背景参数说明](https://developers.openai.com/api/reference/resources/images/methods/generate)

## 文生图示例代码

运行环境：Python 3，依赖 `requests`，可通过 `python -m pip install requests` 安装。把你的完整 API 令牌直接粘贴到下方 `api_key` 的引号内，将代码保存为 Python 文件运行。模型、提示词、尺寸等参数直接在 `payload` 中修改。图片写入运行命令时所在的目录。

```python
import base64
from datetime import datetime
from pathlib import Path

import requests

url = "https://www.dmxapi.cn/v1/images/generations"
api_key = "sk-*****************************************"  # 在引号内粘贴完整 API 令牌

headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {api_key}",
}

payload = {
    # 【model】(string, 本文必填) 使用完整模型 ID
    # 可改为 "gpt-image-2.5-flare"；渠道可用性以 DMXAPI 为准
    "model": "gpt-image-2.5-sunburst",

    # 【prompt】(string, 必填) 描述生成内容；上游最多 32000 字符
    "prompt": "赛博朋克城市雨夜，霓虹招牌特写，电影画幅",

    # 【n】(integer, 可选) 默认 1；上游当前为 1～10，代理限制未实测
    "n": 1,

    # 【size】(string, 可选) 默认 auto；自定义尺寸须满足正文中的全部限制
    "size": "1024x1024",

    # 【output_format】(string, 可选) png / jpeg / webp；默认 png
    "output_format": "png",

    # 【quality】(string, 可选) auto / low / medium / high / xhigh / max
    # 上游默认 auto；xhigh 和 max 为 2.5 新增档位
    "quality": "high",

    # 【output_compression】(integer, 可选) 0～100，上游默认 100
    # 仅切换到 jpeg 或 webp 时启用；PNG 不发送此参数
    # "output_compression": 85,

    # 【moderation】(string, 可选) auto（默认）/ low
    "moderation": "low",

    # 【background】(string, 可选) auto（默认）/ opaque / transparent
    # 透明背景需 png 或 webp；确认渠道支持后取消注释
    # "background": "transparent",
}


def main():
    response = requests.post(url, headers=headers, json=payload, timeout=1000)
    print("status:", response.status_code)
    response.raise_for_status()

    try:
        result = response.json()
    except ValueError as exc:
        raise RuntimeError("接口未返回有效 JSON，请检查响应与渠道配置") from exc

    items = result.get("data") if isinstance(result, dict) else None
    if not isinstance(items, list) or not items:
        raise RuntimeError("响应中没有非空 data 数组")

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
            # 沿用 DMXAPI 参考页的兼容分支，不表示官方模型保证返回 URL
            download = requests.get(item["url"], timeout=120)
            download.raise_for_status()
            image_bytes = download.content
        else:
            raise RuntimeError(f"第 {index} 个图片结果缺少有效图片内容")

        output_path = Path(f"output_{timestamp}_{index}.{extension}")
        output_path.write_bytes(image_bytes)
        print(f"saved {output_path}")


if __name__ == "__main__":
    main()
```

## 返回示例

以下为 `n=1` 时的**脚本运行输出示意**，不是原始 API 响应，也不是本次对 GPT Image 2.5 的实测记录。文件名中的时间戳会随运行时间变化。

```text
status: 200
saved output_20260909_153823_1.png
```

HTTP 响应按 JSON 解析。示例优先读取 `data[].b64_json` 并解码；`data[].url` 仅为沿用 DMXAPI 参考页的客户端兼容逻辑。上游 GPT Image 返回 Base64 图片，本文不发送 `response_format`，也不把示例日志包装成虚构 JSON。[DMXAPI 返回处理参考](https://doc.dmxapi.cn/gpt-image-2-text-to-image.html)、[官方响应格式说明](https://developers.openai.com/api/reference/resources/images/methods/generate)

## 从 gpt-image-2 迁移

先将 `model` 改为平台实际开放的 2.5 型号，保留 `n=1`、常用尺寸和已有质量档位完成基础验证，再逐项测试 `xhigh`、`max`、透明背景或自定义尺寸。旧参考页的 `-ssvip`、`-03` 后缀及 `n≤16` 说明不能直接套用到 2.5；本文也不将高分辨率能力描述为 2.5 首次新增。[官方模型与参数范围](https://developers.openai.com/api/reference/resources/images/methods/generate)

<p align="center">
  <small>© 2026 DMXAPI gpt-image-2.5 文生图</small>
</p>
