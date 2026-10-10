# WAND-Vega-Image 文生图 API 使用文档

基于腾讯云 WAND-Vega-Image 系列多模态图像生成模型的文生图接口，该系列提供 Lite、Flash、Pro 三档能力，共 4 个模型。本文通过 DMXAPI 代理的 `/v1/images/generations` 端点以 POST 方式调用，示例代码从单次响应中读取生成图片的 `data[].url` 与本次消耗的 `usage.total_tokens`，并将图片下载保存到本地。提示词上限 8192 字符，输出分辨率支持 1K / 2K / 4K 三档，宽高比支持 1:1、2:3、3:2、3:4、4:3、9:16、16:9、21:9；本示例不传参考图片，仅凭文本提示词生成图片，`size` 设为 `4096x4096`。

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

## 文生图示例代码

```python
from datetime import datetime
from pathlib import Path

import requests

# ===============================================================
# 步骤1: 配置 API 连接信息
# ===============================================================

# DMXAPI 服务端点地址
url = "https://www.dmxapi.cn/v1/images/generations"

# DMXAPI 密钥（请替换为您自己的密钥）
api_key = "sk-***********************************************"

# ===============================================================
# 步骤2: 配置请求头
# ===============================================================

headers = {
    "Content-Type": "application/json",      # 指定请求体为 JSON 格式
    "Authorization": f"Bearer {api_key}",    # Bearer Token 认证方式
}

# ===============================================================
# 步骤3: 配置请求参数
# ===============================================================

payload = {
    # 【model】(string, 必填) 图像生成模型，可选值：
    #   - "wand-vega-image-lite"
    #   - "wand-vega-image-flash"
    #   - "wand-vega-image-pro"
    #   - "wand-vega-image-1.5-pro"
    "model": "wand-vega-image-lite",

    # 【prompt】(string, 必填) 期望生成图像的文本描述
    # 长度上限 8192 字符；不传参考图片时按此文本执行文生图
    "prompt": "电影画幅，生化危机",

    # 【size】(string, 可选) 生成图像的分辨率，格式 "宽x高"，如 "1024x1024"
    # 分辨率档位：1K / 2K / 4K
    # 宽高比可选：1:1、2:3、3:2、3:4、4:3、9:16、16:9、21:9
    # 不传时由上游决定尺寸
    "size": "4096x4096",
}


# ===============================================================
# 步骤4: 发送请求并保存生成的图片
# ===============================================================

def main():
    # 发送 POST 请求到 API 服务器（timeout 单位为秒）
    response = requests.post(url, headers=headers, json=payload, timeout=1000)
    print("status:", response.status_code)
    response.raise_for_status()

    # 解析 JSON 响应
    try:
        result = response.json()
    except ValueError as exc:
        raise RuntimeError("接口未返回有效 JSON,请检查响应与渠道配置") from exc

    # data：生成结果数组，每个元素的 url 为一张生成图片的地址
    items = result.get("data") if isinstance(result, dict) else None
    if not isinstance(items, list) or not items:
        raise RuntimeError("响应中没有非空 data 数组")

    # usage.total_tokens：本次调用消耗的 token 数（腾讯云官方《WAND 生图调用指南》说明：用于计费/对账）
    usage = result.get("usage") or {}
    print("消耗 token:", usage.get("total_tokens"))

    # 逐张下载图片并保存到当前目录，文件名形如 wand_20261010_153000_1.png
    # 腾讯云官方《WAND 生图调用指南》说明：生成图片的下载地址为临时地址（含签名），请及时下载转存
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
  "created": 1791625558,
  "data": [
    {
      "url": "http://data-shanghai-1378942524.cos.ap-shanghai.myqcloud.com/output/wand-vega/eaddd205-3f14-4db2-9f4e-85d89304e561.png?..."
    }
  ],
  "usage": {
    "total_tokens": 18000
  }
}
```

<p align="center">
  <small>© 2026 DMXAPI WAND-Vega-Image 文生图</small>
</p>
