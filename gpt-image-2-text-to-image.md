# OpenAI gpt-image-2 文生图 API 使用文档

基于 OpenAI GPT Image 2 模型的图像生成接口，通过 `/v1/images/generations` 端点调用，兼容 OpenAI 官方 Images API 协议。支持最大 32000 字符的超长提示词，可配置 auto / 1024×1024 / 1536×1024（横版）/ 1024×1536（竖版）等多种分辨率，、批量生成数量（n=1~10）等精细化控制

## 🖼️ 请求地址

```
https://www.dmxapi.cn/v1/images/generations
```

:::warning
请妥善保管您的 API Key！严禁将密钥泄露给他人、硬编码到代码中或提交到公开的代码仓库。如果怀疑密钥已泄露，请立即前往 DMXAPI 官网重新生成。
:::

## 🤖 支持的模型

- `gpt-image-2`

## 🎨 文生图 示例代码

```python
import base64
from datetime import datetime

import requests

url = "https://www.dmxapi.cn/v1/images/generations"
api_key = "sk-**************************************************"

headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {api_key}",
}

payload = {
    # 【model】(string, 必填) 使用的图像生成模型名称
    # 本文档仅对应 gpt-image-2，保持该值不变
    "model": "gpt-image-2",

    # 【prompt】(string, 必填) 期望生成图像的文本描述
    # GPT image 系列模型最大长度 32000 字符
    # 描述越具体、越场景化，生成效果越接近预期
    "prompt": "墨菲特在召唤师峡谷高举欢迎DMXAPI的旗帜",

    # 【n】(number, 可选) 单次请求生成图像的张数
    # 取值范围: [1, 10]，默认值为 1
    # 注意：dall-e-3 仅支持 n=1；GPT image 系列支持多张批量生成
    "n": 2,

    # 【size】(string, 可选) 生成图像的分辨率
    # GPT image 系列可选值:
    #   "auto"       (自动选择最佳尺寸，默认值)
    #   "1024x1024"  (正方形)
    #   "1536x1024"  (横版/landscape)
    #   "1024x1536"  (竖版/portrait)
    "size": "auto",

    # 【quality】(string, 可选) 生成图像的质量等级
    # 可选值:
    #   "auto"      (自动选择最佳质量，默认值)
    #   "high"      (GPT image 系列：高质量)
    #   "medium"    (GPT image 系列：中等质量)
    #   "low"       (GPT image 系列：低质量，生成更快成本更低)
    "quality": "auto",
}


def main():
    response = requests.post(url, headers=headers, json=payload, timeout=1000)
    print("status:", response.status_code)

    try:
        data = response.json()
    except ValueError:
        print("non-JSON response:", response.text)
        return

    if "data" not in data or not data["data"]:
        print("unexpected response:", data)
        return

    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    for i, item in enumerate(data["data"], start=1):
        if item.get("b64_json"):
            image_bytes = base64.b64decode(item["b64_json"])
        elif item.get("url"):
            image_bytes = requests.get(item["url"], timeout=120).content
        else:
            print("no image payload in response item:", item)
            continue

        filename = f"output_{ts}_{i}.png"
        with open(filename, "wb") as f:
            f.write(image_bytes)
        print(f"saved {filename}")


if __name__ == "__main__":
    main()
```

## 📦 返回示例

```
status: 200
saved output_20260422_153823_1.png
saved output_20260422_153823_2.png
```

<p align="center">
  <small>© 2026 DMXAPI gpt-image-2 文生图</small>
</p>
