# MAI-Image-2.7 图片编辑 API 使用文档

通过 `/mai/v1/images/edits` 接口上传 1 至 5 张 JPEG/PNG 参考图，配合文字指令使用微软 Azure AI Foundry 的 `MAI-Image-2.7` 编辑图片。接口为微软官方原生 multipart 格式，同步返回 Base64 编码的 PNG 图片。

## 接口地址

| 接口 | 请求方式 | URL |
|------|---------|-----|
| 图片编辑 | POST | `https://www.dmxapi.cn/mai/v1/images/edits` |

:::warning
请妥善保管 DMXAPI API Key，勿在前端代码、公开仓库或日志中暴露。运行前，将示例中 `api_key` 引号内的星号占位内容替换为你的完整 API 令牌。
:::

## 模型名称

| 模型 ID | 官方定位 |
|------|------|
| `MAI-Image-2.7` | 微软 Foundry 标准版图像模型，画质与细节优先 |


## 图片编辑示例代码

```python
import base64
from contextlib import ExitStack
from datetime import datetime
from pathlib import Path

import requests

# 图片文件配置：填 1 至 5 张本地参考图的文件路径（JPEG 或 PNG），多图可继续添加列表项
# 按列表顺序作为重复的 image 字段上传，不支持 GIF、SVG 或 Base64 字符串
image_paths = [
    r"C:\Users\Y\Desktop\图片\小猫.png",
    r"C:\Users\Y\Desktop\图片\窗台樱花.png",
]

# 输出目录：编辑后的图片保存位置
output_dir = Path("output")

# API 配置
url = "https://www.dmxapi.cn/mai/v1/images/edits"
api_key = "sk-*****************************************"  # 在引号内粘贴完整 API 令牌

# 请求头：只放 Bearer 鉴权
# multipart/form-data 的 Content-Type 与 boundary 由 requests 自动生成，不要手动指定 JSON 请求头
headers = {
    "Authorization": f"Bearer {api_key}",
}

# 请求参数（multipart 普通字段，通过 data=payload 发送）
payload = {
    # 【model】(string, 必填) 使用的图像编辑模型名称，固定为 "MAI-Image-2.7"
    "model": "MAI-Image-2.7",

    # 【prompt】(string, 必填) 描述希望模型如何使用输入图片
    # 上下文上限 32,000 token；可同时说明"要修改什么"和"要保留什么"
    # 多张参考图按上传顺序称为第一张、第二张……
    "prompt": "把第一张图中的小猫放进第二张图的窗台场景里，保留第二张图的樱花背景和光线风格，画面自然。",
}


def main():
    if not image_paths:
        raise ValueError("image_paths 至少需要一张参考图")
    if len(image_paths) > 5:
        raise ValueError("image_paths 最多 5 张参考图")
    output_dir.mkdir(parents=True, exist_ok=True)

    mime_map = {
        ".png": "image/png",
        ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg",
    }

    with ExitStack() as stack:
        files = []
        for file_path in image_paths:
            file_name = Path(file_path).name
            suffix = Path(file_name).suffix.lower()
            if suffix not in mime_map:
                raise ValueError("参考图文件名必须以 png、jpg 或 jpeg 结尾")

            # 本地路径：直接打开文件
            file_obj = stack.enter_context(open(file_path, "rb"))

            # 【image】(file, 必填) 参考图片文件，每张图重复使用同一个 image 字段
            # 顺序与 image_paths 一致，最多 5 张
            files.append(("image", (file_name, file_obj, mime_map[suffix])))

        # 普通参数（data）和文件（files）共同构成一次 multipart/form-data 请求
        # 编辑接口不支持 width/height，输出尺寸由模型决定（本次实测为 1024×1024）
        # 图片编辑耗时较长（实测约 95 秒），timeout 给足
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
    # 只打印 token 用量；cost 含人民币符号，Windows 的 GBK 控制台直接 print 会报编码错误
    usage = result.get("usage") or {}
    print("usage:", {name: usage.get(name) for name in (
        "num_input_text_tokens", "num_input_image_tokens", "num_output_tokens")})

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    for index, item in enumerate(items, start=1):
        if not isinstance(item, dict):
            raise RuntimeError(f"第 {index} 个图片结果不是对象")
        # 微软原生接口固定返回 Base64 编码的 PNG
        if not item.get("b64_json"):
            raise RuntimeError(f"第 {index} 个图片结果缺少 b64_json")
        image_bytes = base64.b64decode(item["b64_json"], validate=True)

        # 以时间戳 + 序号命名，写入输出目录
        output_path = output_dir / f"mai_edit_{timestamp}_{index}.png"
        output_path.write_bytes(image_bytes)
        print(f"saved {output_path}")


if __name__ == "__main__":
    main()
```

## 返回示例

```text
status: 200
usage: {'num_input_text_tokens': 107, 'num_input_image_tokens': 2560, 'num_output_tokens': 1024}
saved output/mai_edit_20261127_194109_1.png
```

```json
{
  "created": 1795779668,
  "data": [
    {
      "b64_json": "iVBORw0KGgoAAAANSUhEUgAABAAAAAQACAIAAADwf7zUAABM...<2671504 chars>"
    }
  ],
  "model": "MAI-Image-2.7",
  "size": "1024x1024",
  "usage": {
    "cost": "¥0.407566",
    "num_input_image_tokens": 2560,
    "num_input_image_tokens": 107,
    "num_output_tokens": 1024,
    "num_web_calls": 0
  }
}
```

<p align="center">
  <small>© 2026 DMXAPI MAI-Image-2.7 图片编辑</small>
</p>
