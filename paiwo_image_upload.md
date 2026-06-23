# 图片上传 API 文档

图生视频（含首尾帧）需先把所用图片上传，成功后返回 `img_id`；后续发起生成任务时，用该 `img_id` 指定参考图 / 首帧 / 尾帧。





## 接口地址

```
https://www.dmxapi.cn/v1/responses
```

## 模型名称

| 模型 | 适用范围 |
|------|----------|
| `paiwo-picture` | paiwo-v5.6 图生视频 / 首尾帧 |
| `pixverse-picture` | PixVerse-V6、PixVerse-C1 图生视频 / 首尾帧 / 参考 |

::: warning 选对上传模型（用错会报 701009）
两个上传模型的 `img_id` **互不通用**，请按下表选用与生成模型配套的上传模型；用错会报 `701009 (You can only query your own generated or uploaded content)`。

| 你要用的生成模型 | 用这个上传模型 |
|---|---|
| `paiwo-v5.6-itv`、`paiwo-v5.6-itv2`（v5.6 图生视频 / 首尾帧） | `paiwo-picture` |
| `PixVerse-V6`、`PixVerse-C1`（图生视频 / 首尾帧 / 参考） | `pixverse-picture` |
:::

## 支持的参数
**支持格式**：`png`、`webp`、`jpeg`、`jpg`  
**支持类型**：`image/jpeg`、`image/jpg`、`image/png`、`image/webp`  
**尺寸限制**：最大支持 10000px 以内的图片

## 本地传图（base64）

::: code-group

```python [paiwo-picture（v5.6）]
import requests
import json
import base64

url = "https://www.dmxapi.cn/v1/responses"
api_key = "sk-****************************************"  # 替换为你的 DMXAPI 密钥

headers = {
    "Content-Type": "application/json",
    "Authorization": f"{api_key}",
}

# 读取本地图片并转 base64
image_path = "C:/Users/a1/Desktop/测试保存代码/a1.png"  # 替换为实际图片路径
with open(image_path, "rb") as f:
    image_base64 = base64.b64encode(f.read()).decode("utf-8")

payload = {
    "model": "paiwo-picture",   # 用于 paiwo-v5.6
    "input": image_base64,
}

response = requests.post(url, headers=headers, json=payload)
print(json.dumps(response.json(), indent=2, ensure_ascii=False))
```

```python [pixverse-picture（V6 / C1）]
import requests
import json
import base64

url = "https://www.dmxapi.cn/v1/responses"
api_key = "sk-****************************************"  # 替换为你的 DMXAPI 密钥

headers = {
    "Content-Type": "application/json",
    "Authorization": f"{api_key}",
}

# 读取本地图片并转 base64
image_path = "C:/Users/a1/Desktop/测试保存代码/a1.png"  # 替换为实际图片路径
with open(image_path, "rb") as f:
    image_base64 = base64.b64encode(f.read()).decode("utf-8")

payload = {
    "model": "pixverse-picture",   # 用于 PixVerse-V6 / PixVerse-C1
    "input": image_base64,
}

response = requests.post(url, headers=headers, json=payload)
print(json.dumps(response.json(), indent=2, ensure_ascii=False))
```

:::

## URL 传图

::: code-group

```python [paiwo-picture（v5.6）]
import requests
import json

url = "https://www.dmxapi.cn/v1/responses"
api_key = "sk-****************************************"  # 替换为你的 DMXAPI 密钥

headers = {
    "Content-Type": "application/json",
    "Authorization": f"{api_key}",
}

payload = {
    "model": "paiwo-picture",   # 用于 paiwo-v5.6
    "input": "url",             # 固定填 "url"，不用修改
    "image_url": "https://cdn.apifox.com/app/project-icon/custom/20260124/e0874802-fe3b-4740-9ac2-f0b0b47cffe7.png",
}

response = requests.post(url, headers=headers, json=payload)
print(json.dumps(response.json(), indent=2, ensure_ascii=False))
```

```python [pixverse-picture（V6 / C1）]
import requests
import json

url = "https://www.dmxapi.cn/v1/responses"
api_key = "sk-****************************************"  # 替换为你的 DMXAPI 密钥

headers = {
    "Content-Type": "application/json",
    "Authorization": f"{api_key}",
}

payload = {
    "model": "pixverse-picture",   # 用于 PixVerse-V6 / PixVerse-C1
    "input": "url",                # 固定填 "url"，不用修改
    "image_url": "https://cdn.apifox.com/app/project-icon/custom/20260124/e0874802-fe3b-4740-9ac2-f0b0b47cffe7.png",
}

response = requests.post(url, headers=headers, json=payload)
print(json.dumps(response.json(), indent=2, ensure_ascii=False))
```

:::

## 返回示例

两个模型返回格式一致：

```json
{
  "ErrCode": 0,
  "ErrMsg": "Success",
  "Resp": {
    "img_id": 177602101,
    "img_url": "https://media.pixverseai.cn/openapi/d9135033-6998-45ee-bea7-3a8414b90d51_f3ccdd27d2000e3f9255a7e3e2c48800_auto.jpg"
  },
  "usage": {
    "total_tokens": 0,
    "input_tokens": 0,
    "input_tokens_details": {
      "cached_tokens": 0
    },
    "output_tokens": 0,
    "output_tokens_details": {
      "reasoning_tokens": 0
    }
  }
}
```

<p align="center">
  <small>© 2026 DMXAPI 图片上传</small>
</p>
