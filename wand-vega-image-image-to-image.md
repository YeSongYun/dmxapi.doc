# WAND-Vega-Image 图生图 API 使用文档

基于腾讯云 WAND-Vega-Image 系列多模态图像生成模型的图生图（参考生图）接口，该系列提供 Lite、Flash、Pro 三档能力，共 4 个模型。本文通过 DMXAPI 代理的 `/v1/images/generations` 端点以 POST 方式调用，在请求体的 `input[].content[]` 中以 `input_image` 片段逐张传入参考图片 URL，模型按 `prompt` 的描述处理参考图；示例代码从单次响应中读取生成图片的 `data[].url` 与本次消耗的 `usage.total_tokens`，并将图片下载保存到本地。参考图片最多 10 张，格式为 png / jpeg，单张不超过 20MB；提示词上限 8192 字符，输出分辨率支持 1K / 2K / 4K 三档，宽高比支持 1:1、2:3、3:2、3:4、4:3、9:16、16:9、21:9。本示例传入 4 张参考图片，演示将多张图片融合生成一张新的艺术风格图片。

## 🌐 请求地址

```text
https://www.dmxapi.cn/v1/images/generations
```

:::warning
请妥善保管您的 DMXAPI API Key！严禁将密钥泄露给他人或提交到公开的代码仓库；如怀疑密钥已泄露，请立即停用并更换新的密钥。
:::

## 模型名称

- WAND-Vega-Image-1.0-Lite：`wand-vega-image-lite`
- WAND-Vega-Image-1.0-Flash：`wand-vega-image-flash`
- WAND-Vega-Image-1.0-Pro：`wand-vega-image-pro`
- WAND-Vega-Image-1.5-Pro：`wand-vega-image-1.5-pro`

## 图生图示例代码

```python
from datetime import datetime
from pathlib import Path

import requests


url = "https://www.dmxapi.cn/v1/images/generations"
api_key = "sk-***********************************************"  # 在引号内粘贴完整 API 令牌

# 参考图片地址列表:可公网访问的 URL
# 文档限制:最多 10 张,格式 png/jpeg,单张不超过 20MB
image_urls = [
    "https://cdn.jsdelivr.net/gh/opencv/opencv/samples/data/fruits.jpg",
    "https://img.shetu66.com/2023/07/14/1689320796087949.png",
    "https://cdn.jsdelivr.net/gh/opencv/opencv/samples/data/fruits.jpg",
    "https://cdn.jsdelivr.net/gh/opencv/opencv/samples/data/fruits.jpg"
]

# 请求头:JSON 请求体 + Bearer 鉴权
headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {api_key}",
}

# 请求参数(严格按官方文档字段)
payload = {
    # 【model】(string, 必填) 
    #   "wand-vega-image-lite"     (参考图不额外收费)
    #   "wand-vega-image-flash"    (参考图不额外收费)
    #   "wand-vega-image-pro"      (前 3 张参考图免费,第 4 张起每张 +¥0.1)
    #   "wand-vega-image-1.5-pro"  (每张参考图 +¥0.1)
    "model": "wand-vega-image-1.5-pro",

    # 【prompt】(string, 必填) 对参考图做什么处理的文字描述,上限 8192 字符
    "prompt": "把这些图片融合在一起，生成一张新的艺术风格图片",

    # 【size】(string, 可选) 输出分辨率 "宽x高",如 1024x1024
    # 档位 1K/2K/4K,宽高比 1:1、2:3、3:2、3:4、4:3、9:16、16:9、21:9
    "size": "1024x1024",

    # 【input】(array[object], 可选) 多模态输入数组,传了它就是图生图/参考图
    # 结构:
    #   input[].content          内容片段数组,按顺序拼接成多模态提示
    #   input[].content[].type   string,文档只给出 "input_image" 一种取值
    #   input[].content[].image_url  参考图地址(最多 10 张,png/jpeg,≤20MB)
    "input": [
        {
            "content": [
                {"type": "input_image", "image_url": image_url}
                for image_url in image_urls
            ]
        }
    ],
}


def main():
    response = requests.post(url, headers=headers, json=payload, timeout=1000)
    print("status:", response.status_code)
    response.raise_for_status()

    try:
        result = response.json()
    except ValueError as exc:
        raise RuntimeError("接口未返回有效 JSON,请检查响应与渠道配置") from exc

    items = result.get("data") if isinstance(result, dict) else None
    if not isinstance(items, list) or not items:
        raise RuntimeError("响应中没有非空 data 数组")

    usage = result.get("usage") or {}
    print("消耗 token:", usage.get("total_tokens"))

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    for index, item in enumerate(items, start=1):
        if not isinstance(item, dict) or not item.get("url"):
            raise RuntimeError(f"第 {index} 个图片结果缺少 url")
        download = requests.get(item["url"], timeout=120)
        download.raise_for_status()
        output_path = Path(f"wand_{timestamp}_{index}.png")
        output_path.write_bytes(download.content)
        print(f"saved {output_path}")


if __name__ == "__main__":
    main()
```

## 返回示例

```json
{
  "created": 1791625560,
  "data": [
    {
      "url": "http://data-shanghai-1378942524.cos.ap-shanghai.myqcloud.com/output/wand-vega/40b67483-38b7-474e-b35f-1c9b36de3804.png?..."
    }
  ],
  "usage": {
    "total_tokens": 90000
  }
}
```

<p align="center">
  <small>© 2026 DMXAPI WAND-Vega-Image 图生图</small>
</p>
