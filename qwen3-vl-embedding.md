# qwen3-vl-embedding 多模态向量化 API 使用文档

阿里云百炼的 `qwen3-vl-embedding` 可以把文本、图片和视频转换为同一语义空间中的向量。用文字搜图时，可分别为查询文本和每张候选图片生成独立向量，再按余弦相似度排序。需要同时表达一件商品的图片和描述时，可将图文融合为一个向量，用于商品检索。

## 接口地址

| 接口 | 请求方式 | URL |
| --- | --- | --- |
| 多模态向量化（同步返回） | POST | `https://www.dmxapi.cn/api/v1/services/embeddings/multimodal-embedding/multimodal-embedding` |

## 模型名称

`qwen3-vl-embedding`

## Python 调用示例

::: code-group

```python [独立向量]
import json
from datetime import datetime
from pathlib import Path

import requests  # 安装依赖可运行 python -m pip install requests

# API 配置
url = "https://www.dmxapi.cn/api/v1/services/embeddings/multimodal-embedding/multimodal-embedding"
api_key = "sk-xxxxxxxx"  # 填写您的 DMXAPI 令牌

# 请求头：JSON 请求体 + Bearer 鉴权
headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {api_key}",
}

# 请求参数
payload = {
    # 【model】(string, 必填) 使用的多模态向量模型名称
    "model": "qwen3-vl-embedding",

    # 【input】(object, 必填) 待生成向量的内容
    "input": {
        # 【contents】(array, 必填) 单次请求 1 到 20 个条目，每个对象填写 text、image、video 中的一项
        # 单次最多 10 张图片和 1 个视频
        # 每个条目生成一个向量，index 从 0 开始。做以文搜图时可逐项计算相似度
        "contents": [
            # 【text】(string, 可选) 待向量化的文本，也可以在 contents 中直接写字符串
            # 文本长度上限为 32,000 token
            {"text": "户外自然风景"},

            # 【image】(string, 可选) 公网图片 URL 或 Base64 Data URI
            # 支持 JPEG、PNG、WEBP、BMP、TIFF、ICO、DIB、ICNS、SGI，单张不超过 10 MB
            {"image": "https://img.alicdn.com/imgextra/i3/O1CN01rdstgY1uiZWt8gqSL_!!6000000006071-0-tps-1970-356.jpg"},

            # 【video】(string, 可选) 公开可访问的 MP4、AVI 或 MOV 视频 URL，最大 50 MB
            {"video": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250107/lbcemt/new+video.mp4"},
        ],
    },

    # 【parameters】(object, 可选) 向量生成选项
    "parameters": {
        # 【enable_fusion】(boolean, 可选) 指定向量生成方式
        # 可选值:
        #   False  (每个输入分别返回 1 个独立向量，默认值)
        #   True   (将所有输入合并为 1 个融合向量)
        "enable_fusion": False,

        # 【dimension】(integer, 可选) 输出向量的维度
        # 可选值: 256 / 512 / 768 / 1024 / 1536 / 2048 / 2560，默认 2560
        "dimension": 256,

        # 【output_type】(string, 可选) 输出向量格式
        # 支持 "dense" (稠密向量)，传入其他取值时仍返回稠密向量
        "output_type": "dense",

        # 【instruct】(string, 可选) 自定义任务说明，建议用英文描述检索意图
        "instruct": "Represent the input for cross-modal retrieval.",

        # 【fps】(float, 可选) 视频抽帧比例，取值范围 [0, 1]，默认 1.0
        # 取值越小，实际抽取的帧数越少
        "fps": 1.0,
    },
}


def main():
    body = dict(payload)

    # 发起同步请求，直接获取向量结果
    response = requests.post(url, headers=headers, json=body, timeout=1000)
    print("status:", response.status_code)
    if not response.ok:
        print("gateway_request_id:", response.headers.get("X-Oneapi-Request-Id") or "(未返回)")
        print("error:", response.text.strip() or "(响应正文为空)")
    response.raise_for_status()

    # 解析响应 JSON
    try:
        result = response.json()
    except ValueError as exc:
        raise RuntimeError("接口未返回有效 JSON，请检查响应与渠道配置") from exc

    # 向量结果位于 output.embeddings 数组，每个元素包含 index、type 和 embedding
    output = result.get("output") if isinstance(result, dict) else None
    items = output.get("embeddings") if isinstance(output, dict) else None
    if not isinstance(items, list) or not items:
        if isinstance(result, dict) and result.get("code"):
            raise RuntimeError(f"{result['code']}: {result.get('message', '')}")
        raise RuntimeError("响应中没有非空 output.embeddings 数组")

    print("request_id:", result.get("request_id"))
    print("usage:", json.dumps(result.get("usage", {}), ensure_ascii=False))

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    for index, item in enumerate(items, start=1):
        vector = item.get("embedding") if isinstance(item, dict) else None
        if not isinstance(vector, list) or not vector:
            raise RuntimeError(f"第 {index} 个结果缺少有效向量")

        # 以时间戳 + 序号命名，将这一条向量结果写入当前工作目录
        output_path = Path(f"output_{timestamp}_{index}.json")
        output_path.write_text(json.dumps(item, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"saved {output_path}")


if __name__ == "__main__":
    main()
```

```python [图文融合向量]
import base64
import json
from datetime import datetime
from pathlib import Path

import requests  # 安装依赖可运行 python -m pip install requests

# API 配置
url = "https://www.dmxapi.cn/api/v1/services/embeddings/multimodal-embedding/multimodal-embedding"
api_key = "sk-xxxxxxxx"  # 填写您的 DMXAPI 令牌

# 请求头：JSON 请求体 + Bearer 鉴权
headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {api_key}",
}

# 请求参数
payload = {
    # 【model】(string, 必填) 使用的多模态向量模型名称
    "model": "qwen3-vl-embedding",

    # 【input】(object, 必填) 待生成向量的内容
    "input": {
        # 【contents】(array, 必填) 单次请求 1 到 20 个条目，每个对象填写 text、image、video 中的一项
        # 单次最多 10 张图片和 1 个视频
        # 将商品描述和图片作为一条记录建索引时，把它们各写成一个条目并开启融合
        "contents": [
            # 【text】(string, 可选) 待向量化的文本，也可以在 contents 中直接写字符串
            # 文本长度上限为 32,000 token
            {"text": "检索与这张图片主题相似的内容。"},

            # 【image】(string, 可选) 公网图片 URL 或 Base64 Data URI
            # 支持 JPEG、PNG、WEBP、BMP、TIFF、ICO、DIB、ICNS、SGI，单张不超过 10 MB
            {"image": "https://img.alicdn.com/imgextra/i3/O1CN01rdstgY1uiZWt8gqSL_!!6000000006071-0-tps-1970-356.jpg"},
            # 本地 PNG 图片可用下一行替换上面的 image 条目，其他格式请同步修改 MIME 类型
            # {"image": "data:image/png;base64," + base64.b64encode(Path("示例.png").read_bytes()).decode("ascii")},
            # 多图融合时，可再添加一个 image 条目
            # {"image": "https://dashscope.oss-cn-beijing.aliyuncs.com/images/256_1.png"},

            # 【video】(string, 可选) 公开可访问的 MP4、AVI 或 MOV 视频 URL，最大 50 MB
            # 需要把视频也融入向量时，取消下一行的注释
            # {"video": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250107/lbcemt/new+video.mp4"},
        ],
    },

    # 【parameters】(object, 可选) 向量生成选项
    "parameters": {
        # 【enable_fusion】(boolean, 可选) 指定向量生成方式
        # 可选值:
        #   False  (每个输入分别返回 1 个独立向量，默认值)
        #   True   (将所有输入合并为 1 个融合向量)
        "enable_fusion": True,

        # 【dimension】(integer, 可选) 输出向量的维度
        # 可选值: 256 / 512 / 768 / 1024 / 1536 / 2048 / 2560，默认 2560
        "dimension": 256,

        # 【output_type】(string, 可选) 输出向量格式
        # 支持 "dense" (稠密向量)，传入其他取值时仍返回稠密向量
        "output_type": "dense",

        # 【instruct】(string, 可选) 自定义任务说明，建议用英文描述检索意图
        "instruct": "Represent the image and its description for retrieval.",

        # 【fps】(float, 可选) 视频抽帧比例，取值范围 [0, 1]，默认 1.0
        # 需要调整视频抽帧比例时再取消注释
        # "fps": 1.0,
    },
}


def main():
    body = dict(payload)

    # 发起同步请求，直接获取向量结果
    response = requests.post(url, headers=headers, json=body, timeout=1000)
    print("status:", response.status_code)
    if not response.ok:
        print("gateway_request_id:", response.headers.get("X-Oneapi-Request-Id") or "(未返回)")
        print("error:", response.text.strip() or "(响应正文为空)")
    response.raise_for_status()

    # 解析响应 JSON
    try:
        result = response.json()
    except ValueError as exc:
        raise RuntimeError("接口未返回有效 JSON，请检查响应与渠道配置") from exc

    # 向量结果位于 output.embeddings 数组，每个元素包含 index、type 和 embedding
    output = result.get("output") if isinstance(result, dict) else None
    items = output.get("embeddings") if isinstance(output, dict) else None
    if not isinstance(items, list) or not items:
        if isinstance(result, dict) and result.get("code"):
            raise RuntimeError(f"{result['code']}: {result.get('message', '')}")
        raise RuntimeError("响应中没有非空 output.embeddings 数组")

    print("request_id:", result.get("request_id"))
    print("usage:", json.dumps(result.get("usage", {}), ensure_ascii=False))

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    for index, item in enumerate(items, start=1):
        vector = item.get("embedding") if isinstance(item, dict) else None
        if not isinstance(vector, list) or not vector:
            raise RuntimeError(f"第 {index} 个结果缺少有效向量")

        # 以时间戳 + 序号命名，将这一条向量结果写入当前工作目录
        output_path = Path(f"output_{timestamp}_{index}.json")
        output_path.write_text(json.dumps(item, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"saved {output_path}")


if __name__ == "__main__":
    main()
```

:::

## 返回示例

独立向量示例返回 3 条 `vl` 结果，`index` 为 `0`、`1`、`2`，依次对应文本、图片和视频。图文融合示例返回 1 条 `fusion` 结果，同时表示输入的文字和图片。以下实测响应均取每个 256 维向量的前 3 个分量展示。

::: code-group

```json [独立向量]
{
  "request_id": "<request_id>",
  "output": {
    "embeddings": [
      {
        "index": 0,
        "type": "vl",
        "embedding": [-0.0029579694382846355, 0.14832717180252075, 0.057230278849601746]
      },
      {
        "index": 1,
        "type": "vl",
        "embedding": [-0.0010725368047133088, 0.03496095910668373, 0.2336234152317047]
      },
      {
        "index": 2,
        "type": "vl",
        "embedding": [-0.0018370978068560362, -0.10288833826780319, 0.008662736974656582]
      }
    ]
  },
  "usage": {
    "input_tokens": 87,
    "image_tokens": 2122,
    "total_tokens": 2209,
    "cost": "¥0.00388"
  }
}
```

```json [图文融合向量]
{
  "request_id": "<request_id>",
  "output": {
    "embeddings": [
      {
        "index": 0,
        "type": "fusion",
        "embedding": [-0.001053795451298356, 0.0027962583117187023, 0.21231012046337128]
      }
    ]
  },
  "usage": {
    "input_tokens": 33,
    "image_tokens": 682,
    "total_tokens": 715,
    "cost": "¥0.00125"
  }
}
```

:::



<p align="center">
  <small>© 2026 DMXAPI qwen3-vl-embedding</small>
</p>
