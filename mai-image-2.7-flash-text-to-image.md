# MAI-Image-2.7-Flash 文生图 API 使用文档

通过 `/mai/v1/images/generations` 接口提交文本提示词，使用微软 Azure AI Foundry 的 `MAI-Image-2.7-Flash` 生成图片。接口为微软官方原生格式，同步返回 Base64 编码的 PNG 图片。

## 接口地址

| 接口 | 请求方式 | URL |
|------|---------|-----|
| 文生图 | POST | `https://www.dmxapi.cn/mai/v1/images/generations` |

:::warning
请妥善保管 DMXAPI API Key，勿在前端代码、公开仓库或日志中暴露。运行前，将示例中 `api_key` 引号内的星号占位内容替换为你的完整 API 令牌。
:::

## 模型名称

| 模型 ID | 官方定位 |
|------|------|
| `MAI-Image-2.7-Flash` | 微软 Foundry 轻量版图像模型，速度与成本优先， |


## 文生图示例代码

```python
import base64
from datetime import datetime
from pathlib import Path

import requests

# API 配置
url = "https://www.dmxapi.cn/mai/v1/images/generations"
api_key = "sk-*****************************************"  # 在引号内粘贴完整 API 令牌

# 输出目录：生成的图片保存位置
output_dir = Path("output")

# 请求头：JSON 请求体 + Bearer 鉴权
headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {api_key}",
}

# 请求参数
payload = {
    # 【model】(string, 必填) 使用的图像生成模型名称，固定为 "MAI-Image-2.7-Flash"
    "model": "MAI-Image-2.7-Flash",

    # 【prompt】(string, 必填) 期望生成图像的文本描述
    # 上下文上限 32,000 token；描述越具体、越场景化，生成效果越接近预期
    "prompt": "一只橘色小猫趴在窗台上晒太阳，窗外是樱花，柔和的午后光线，摄影风格",

    # 【width】(integer, 可选) 输出图片宽度，单位像素
    # 最小 768；与 height 的乘积不能超过 4,194,304 像素（宽、高均不超过 4096）
    # 单边可超过 2048，例如全景图 3072×1024；省略时由模型自动决定（本次实测为 1024×1024）
    "width": 1024,

    # 【height】(integer, 可选) 输出图片高度，单位像素
    # 限制同 width；width 与 height 可以只填其中一个，另一个由模型匹配
    "height": 1536,

    # 【background】(string, 可选) 背景模式
    # 可选值: "transparent" (透明背景，输出带透明通道的 PNG)
    # 不需要透明背景时删除此行，模型按默认输出不透明背景
    # "background": "transparent",
}


def main():
    output_dir.mkdir(parents=True, exist_ok=True)

    # 发起同步请求；图片生成耗时较长（实测约 15 秒），timeout 给足
    response = requests.post(url, headers=headers, json=payload, timeout=1000)
    print("status:", response.status_code)
    response.raise_for_status()

    # 解析响应 JSON；非 JSON 通常是渠道或网关报错
    try:
        result = response.json()
    except ValueError as exc:
        raise RuntimeError("接口未返回有效 JSON，请检查响应与渠道配置") from exc

    # 图片结果位于 data 数组，每个元素对应一张图；usage 为本次实际 token 用量
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
        output_path = output_dir / f"mai_generation_{timestamp}_{index}.png"
        output_path.write_bytes(image_bytes)
        print(f"saved {output_path}")


if __name__ == "__main__":
    main()
```

## 返回示例


```text
status: 200
usage: {'num_input_text_tokens': 43, 'num_input_image_tokens': 0, 'num_output_tokens': 1024}
saved output/mai_generation_20261127_193921_1.png
```

```json
{
  "created": 1795779560,
  "data": [
    {
      "b64_json": "iVBORw0KGgoAAAANSUhEUgAABAAAAAYACAIAAABn4K39AABM...<3384700 chars>"
    }
  ],
  "model": "MAI-Image-2.7-Flash",
  "size": "1024x1536",
  "usage": {
    "cost": "¥0.112678",
    "num_input_image_tokens": 0,
    "num_input_text_tokens": 43,
    "num_output_tokens": 1536,
    "num_web_calls": 0
  }
}
```


<p align="center">
  <small>© 2026 DMXAPI MAI-Image-2.7-Flash 文生图</small>
</p>
