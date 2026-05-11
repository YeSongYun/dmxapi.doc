# gemini-embedding-2-preview 多模态嵌入 API 使用文档

`gemini-embedding-2-preview` 是 Google 推出的新一代多模态嵌入模型，支持将文本、图片、音频、视频和 PDF 文档转化为高维浮点向量，最高支持 3072 维输出，输入 token 上限达 8192。单次请求可将多模态内容聚合为统一向量，也可通过 `batchEmbedContents` 端点批量处理多个独立请求。输出向量自动归一化，可直接用于语义检索、相似度比较、聚类分析等下游任务，无需手动处理截断后的向量。


## 模型名称

- `gemini-embedding-2-preview`

## 请求地址

| 接口 | 请求方式 | URL |
|------|---------|-----|
| 单内容嵌入 | POST | `https://www.dmxapi.cn/v1beta/models/gemini-embedding-2-preview:embedContent` |
| 批量嵌入 | POST | `https://www.dmxapi.cn/v1beta/models/gemini-embedding-2-preview:batchEmbedContents` |

:::warning
请妥善保管您的 API Key！严禁将密钥泄露给他人、硬编码到代码中或提交到公开的代码仓库。
:::

## 文本嵌入

```python
import requests

url = "https://www.dmxapi.cn/v1beta/models/gemini-embedding-2-preview:embedContent"

api_key = "sk-******************************************"  # 填写您的 api_key

headers = {
    "Content-Type": "application/json",
    # 【x-goog-api-key】(string, 必填) Gemini API 认证密钥
    "Authorization": f"{api_key}",
}

payload = {
    # 【content】(object, 必填) 输入内容对象，包含待嵌入的内容片段
    "content": {
        # 【parts】(array, 必填) 内容片段列表，支持文本与媒体混合输入
        "parts": [
            {
                # 【text】(string, 条件必填) 纯文本输入，与 inline_data 二选一
                "text": "你是谁？"
            }
        ]
    },
    # 【output_dimensionality】(integer, 可选) 输出向量维度
    # 指定返回嵌入向量的维度数量，默认值为 3072
    # 推荐值: 768、1536、3072，取值范围: [128, 3072]
    # 截断后向量自动归一化，无需手动处理
    "output_dimensionality": 768
}

response = requests.post(url, headers=headers, json=payload, timeout=60)
print(response.text)
```

### 返回示例

```json
{
  "embedding": {
    "values": [
      -0.02061161,
      0.0036372687,
      -0.036011722,
      0.0017922518,
      "...",
      -0.0039523887,
      -0.006603699
    ]
  },
  "usageMetadata": {
    "promptTokenCount": 5,
    "promptTokenDetails": [
      {
        "modality": "TEXT",
        "tokenCount": 5
      }
    ]
  }
}
```

## 图片嵌入

支持的图片格式：

| MIME 类型 | 格式说明 | 限制 |
|-----------|---------|------|
| `image/jpeg` | JPEG 图片 | 每请求最多 6 张 |
| `image/png` | PNG 图片 | 每请求最多 6 张 |

```python
import os
import json
import base64
import mimetypes
import requests

# 步骤1: 配置 API 连接信息

# DMXAPI Gemini Embedding 接口地址
url = "https://www.dmxapi.cn/v1beta/models/gemini-embedding-2-preview:embedContent"

# DMXAPI API Key
api_key = "sk-******************************************"  # 填写您的 api_key

# 本地图片路径
image_path = r"C:/Users/a1/Desktop/测试保存代码/c13.png"

# 步骤2: 工具函数

def get_mime_type(file_path: str) -> str:
    """
    根据本地文件路径自动识别 MIME 类型。

    常见结果:
      .jpg / .jpeg -> image/jpeg
      .png         -> image/png
      .webp        -> image/webp
    """
    mime_type, _ = mimetypes.guess_type(file_path)

    if mime_type is None:
        # 如果无法识别，默认按 png 处理
        mime_type = "image/png"
    return mime_type


def image_file_to_base64(file_path: str) -> str:
    """
    将本地图片文件转换为纯 base64 字符串。

    这里返回的是纯 base64，不包含:
       data:image/jpeg;base64,
       data:image/png;base64,
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"图片文件不存在: {file_path}")

    with open(file_path, "rb") as f:
        image_bytes = f.read()

    img_base64 = base64.b64encode(image_bytes).decode("utf-8")

    return img_base64


def remove_data_url_prefix(base64_data: str) -> str:
    """
    如果传入的 base64 字符串不小心带了 Data URL 前缀，则自动去掉前缀。

    例如:
      data:image/jpeg;base64,/9j/4AAQ...
    会变成:
      /9j/4AAQ...
    """
    if base64_data.startswith("data:") and ";base64," in base64_data:
        return base64_data.split(",", 1)[1]

    return base64_data


# 步骤3: 配置请求头
headers = {
    "Content-Type": "application/json",
    # 【x-goog-api-key】(string, 必填) Gemini API 认证密钥
    "x-goog-api-key": api_key
}

# 步骤4: 读取本地图片并转为纯 base64

# 自动识别图片 MIME 类型
mime_type = get_mime_type(image_path)
# 将图片转为纯 base64
img_base64 = image_file_to_base64(image_path)
# 保险处理，确保没有 data:image/...;base64, 前缀
img_base64 = remove_data_url_prefix(img_base64)

# 步骤5: 配置请求参数

payload = {
    # 【content】(object, 必填) 输入内容对象，包含待嵌入的内容片段
    "content": {
        # 【parts】(array, 必填) 内容片段列表，支持文本与媒体混合输入
        "parts": [
            {
                # 【inline_data】(object, 条件必填) 二进制媒体数据容器，与 text 二选一
                "inline_data": {
                    # 【mime_type】(string, 必填) 媒体 MIME 类型
                    # 图片支持: image/jpeg、image/png、image/webp
                    # 由 get_mime_type() 自动从文件扩展名识别
                    "mime_type": mime_type,
                    # 【data】(string, 必填) 媒体文件的纯 Base64 编码字符串
                    # 注意: 不得包含 data:image/...;base64, 前缀
                    "data": img_base64
                }
            }
        ]
    }
}


# 步骤6: 发送请求并输出结果

try:
    response = requests.post(
        url,
        headers=headers,
        json=payload,
        timeout=120
    )
    # 如果 HTTP 状态码不是 2xx，这里会抛出异常
    response.raise_for_status()
    result = response.json()
    # 格式化输出 JSON 响应
    # - indent=2: 缩进 2 空格，便于阅读
    # - ensure_ascii=False: 正确显示中文字符
    print(json.dumps(result, indent=2, ensure_ascii=False))

except requests.exceptions.HTTPError as e:
    print("请求失败，HTTP 状态码异常")
    print("状态码:", response.status_code)
    print("响应内容:")
    print(response.text)

except requests.exceptions.RequestException as e:
    print("请求失败，网络或连接异常")
    print(str(e))

except Exception as e:
    print("程序执行异常")
    print(str(e))
```

### 返回示例

```json
{
  "embedding": {
    "values": [
      -0.02061161,
      0.0036372687,
      -0.036011722,
      0.0017922518,
      "...",
      -0.0039523887,
      -0.006603699
    ]
  },
  "usageMetadata": {
    "promptTokenCount": 258,
    "promptTokenDetails": [
      {
        "modality": "IMAGE",
        "tokenCount": 258
      }
    ]
  }
}
```

## 音频嵌入

支持的音频格式：

| MIME 类型 | 格式说明 | 限制 |
|-----------|---------|------|
| `audio/mpeg` | MP3 音频 | 最长 180 秒 |
| `audio/wav` | WAV 音频 | 最长 180 秒 |

```python
import os
import json
import base64
import mimetypes
import requests
# 步骤1: 配置 API 连接信息
url = "https://www.dmxapi.cn/v1beta/models/gemini-embedding-2-preview:embedContent"
api_key = "sk-******************************************"  # 填写你的 API Key
# 音频本地路径
# Windows 示例:
# audio_path = r"C:\Users\a1\Desktop\test.mp3"
audio_path = r"C:/Users/a1/Desktop/测试保存代码/output.mp3"

# 步骤2: 工具函数
def get_mime_type(file_path: str) -> str:
    mime_type, _ = mimetypes.guess_type(file_path)
    if mime_type is None:
        # 如果无法识别，默认按 mp3 处理
        mime_type = "audio/mpeg"
    return mime_type

def file_to_base64(file_path: str) -> str:
    """
    将本地音频文件转换为纯 base64 字符串。
    注意:
    返回值不会包含 data:audio/mpeg;base64, 这种前缀。
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"音频文件不存在: {file_path}")
    with open(file_path, "rb") as f:
        file_bytes = f.read()
    return base64.b64encode(file_bytes).decode("utf-8")

def remove_data_url_prefix(base64_data: str) -> str:
    if base64_data.startswith("data:") and ";base64," in base64_data:
        return base64_data.split(",", 1)[1]
    return base64_data


# 步骤3: 准备请求数据
mime_type = get_mime_type(audio_path)
audio_base64 = file_to_base64(audio_path)
# 保险处理，确保 data 里没有 data:audio/...;base64, 前缀
audio_base64 = remove_data_url_prefix(audio_base64)
headers = {
    "Content-Type": "application/json",
    # 【x-goog-api-key】(string, 必填) Gemini API 认证密钥
    "x-goog-api-key": api_key
}

payload = {
    # 【content】(object, 必填) 输入内容对象，包含待嵌入的内容片段
    "content": {
        # 【parts】(array, 必填) 内容片段列表，支持文本与媒体混合输入
        "parts": [
            {
                # 【inline_data】(object, 条件必填) 二进制媒体数据容器，与 text 二选一
                "inline_data": {
                    # 【mime_type】(string, 必填) 媒体 MIME 类型
                    # 音频支持: audio/mpeg、audio/wav、audio/mp4、audio/ogg、audio/flac
                    # 由 get_mime_type() 自动从文件扩展名识别
                    "mime_type": mime_type,
                    # 【data】(string, 必填) 媒体文件的纯 Base64 编码字符串
                    # 注意: 不得包含 data:audio/...;base64, 前缀
                    "data": audio_base64
                }
            }
        ]
    }
}
# 步骤4: 发送请求，只输出 embedding
try:
    response = requests.post(
        url,
        headers=headers,
        json=payload,
        timeout=120
    )
    response.raise_for_status()
    result = response.json()
    embedding_values = result["embedding"]["values"]
    print(json.dumps(embedding_values, ensure_ascii=False))
except requests.exceptions.HTTPError:
    print(response.text)
except requests.exceptions.RequestException as e:
    print(str(e))
except Exception as e:
    print(str(e))
```

### 返回示例
```json
[0.020162337, 0.008672163, -0.0054970523, -0.021474715, 0.024371188, "...", -0.11284455, -0.0032555202, -0.05529588, -0.031505797, -0.0021848765]
```

## 视频嵌入

支持的视频格式：

| MIME 类型 | 格式说明 | 限制 |
|-----------|---------|------|
| `video/mp4` | MP4 视频（支持 H264/H265/AV1/VP9 编解码器） | 最长 120 秒 |
| `video/quicktime` | MOV 视频 | 最长 120 秒 |

> 系统最多处理每个视频 32 帧：短视频（≤32 秒）以 1 fps 的速率抽样，较长视频则均匀抽样为 32 帧。视频文件中不处理音轨。

```python
import os
import json
import base64
import mimetypes
import requests

# 步骤1: 配置 API 连接信息

url = "https://www.dmxapi.cn/v1beta/models/gemini-embedding-2-preview:embedContent"
api_key = "sk-******************************************"  # 填写你的 API Key
# 视频本地路径
# Windows 示例:
# video_path = r"C:\Users\a1\Desktop\test.mp4"
video_path = r"C:/Users/a1/Desktop/测试保存代码/output.mp4"

# 步骤2: 工具函数
def get_mime_type(file_path: str) -> str:
    """
    根据本地视频路径自动识别 MIME 类型。
    常见结果:
      .mp4  -> video/mp4
      .mov  -> video/quicktime
    """
    mime_type, _ = mimetypes.guess_type(file_path)
    if mime_type is None:
        # 如果无法识别，默认按 mp4 处理
        mime_type = "video/mp4"
    return mime_type

def file_to_base64(file_path: str) -> str:
    """
    将本地视频文件转换为纯 base64 字符串。
    注意:
    返回值不会包含 data:video/mp4;base64, 这种前缀。
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"视频文件不存在: {file_path}")
    with open(file_path, "rb") as f:
        file_bytes = f.read()
    return base64.b64encode(file_bytes).decode("utf-8")

def remove_data_url_prefix(base64_data: str) -> str:
    """
    如果 base64 字符串不小心带了 Data URL 前缀，则自动去掉。
    错误格式:
      data:video/mp4;base64,AAAAIGZ0eXBtcDQy...
    正确格式:
      AAAAIGZ0eXBtcDQy...
    """
    if base64_data.startswith("data:") and ";base64," in base64_data:
        return base64_data.split(",", 1)[1]
    return base64_data


# 步骤3: 准备请求数据
mime_type = get_mime_type(video_path)
video_base64 = file_to_base64(video_path)
# 保险处理，确保 data 里没有 data:video/...;base64, 前缀
video_base64 = remove_data_url_prefix(video_base64)
headers = {
    "Content-Type": "application/json",
    # 【x-goog-api-key】(string, 必填) Gemini API 认证密钥
    "x-goog-api-key": api_key
}
payload = {
    # 【content】(object, 必填) 输入内容对象，包含待嵌入的内容片段
    "content": {
        # 【parts】(array, 必填) 内容片段列表，支持文本与媒体混合输入
        "parts": [
            {
                # 【inline_data】(object, 条件必填) 二进制媒体数据容器，与 text 二选一
                "inline_data": {
                    # 【mime_type】(string, 必填) 媒体 MIME 类型
                    # 视频支持: video/mp4、video/quicktime
                    # 由 get_mime_type() 自动从文件扩展名识别
                    "mime_type": mime_type,
                    # 【data】(string, 必填) 媒体文件的纯 Base64 编码字符串
                    # 注意: 不得包含 data:video/...;base64, 前缀
                    "data": video_base64
                }
            }
        ]
    }
}
# 步骤4: 发送请求，只输出 embedding
try:
    response = requests.post(
        url,
        headers=headers,
        json=payload,
        timeout=300
    )
    response.raise_for_status()
    result = response.json()
    embedding_values = result["embedding"]["values"]
    print(json.dumps(embedding_values, ensure_ascii=False))
except requests.exceptions.HTTPError:
    print(response.text)
except requests.exceptions.RequestException as e:
    print(str(e))
except Exception as e:
    print(str(e))
```

### 返回示例

```json
[-0.00907308, -0.0031938262, -0.012869417, 0.017437436, 0.0018481556, "...", 0.0033451857, 0.0148743065, 0.001180565, -0.01527782, 0.011965878]
```

## 文档嵌入（PDF）
支持的文档格式：
| MIME 类型 | 格式说明 | 限制 |
|-----------|---------|------|
| `application/pdf` | PDF 文档 | 最多 6 页 |
```python
import os
import json
import base64
import mimetypes
import requests
# 步骤1: 配置 API 连接信息
url = "https://www.dmxapi.cn/v1beta/models/gemini-embedding-2-preview:embedContent"
api_key = "sk-******************************************"  # 填写你的 API Key
# PDF 本地路径
# Windows 示例:
# pdf_path = r"C:\Users\a1\Desktop\test.pdf"
pdf_path = r"C:\Users\a1\Desktop\测试保存代码\文字文稿1.pdf"

# 步骤2: 工具函数
def get_mime_type(file_path: str) -> str:
    """
    根据本地文件路径自动识别 MIME 类型。
    PDF 通常是:
      .pdf -> application/pdf
    """
    mime_type, _ = mimetypes.guess_type(file_path)
    if mime_type is None:
        mime_type = "application/pdf"
    return mime_type

def file_to_base64(file_path: str) -> str:
    """
    将本地 PDF 文件转换为纯 base64 字符串。
    注意:
    返回值不会包含 data:application/pdf;base64, 这种前缀。
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"PDF 文件不存在: {file_path}")
    with open(file_path, "rb") as f:
        file_bytes = f.read()
    return base64.b64encode(file_bytes).decode("utf-8")

def remove_data_url_prefix(base64_data: str) -> str:
    """
    如果 base64 字符串不小心带了 Data URL 前缀，则自动去掉。
    错误格式:
      data:application/pdf;base64,JVBERi0xLjQK...
    正确格式:
      JVBERi0xLjQK...
    """
    if base64_data.startswith("data:") and ";base64," in base64_data:
        return base64_data.split(",", 1)[1]
    return base64_data

# 步骤3: 准备请求数据
mime_type = get_mime_type(pdf_path)
pdf_base64 = file_to_base64(pdf_path)
# 保险处理，确保 data 里没有 data:application/pdf;base64, 前缀
pdf_base64 = remove_data_url_prefix(pdf_base64)
headers = {
    "Content-Type": "application/json",
    # 【x-goog-api-key】(string, 必填) Gemini API 认证密钥
    "x-goog-api-key": api_key
}
payload = {
    # 【content】(object, 必填) 输入内容对象，包含待嵌入的内容片段
    "content": {
        # 【parts】(array, 必填) 内容片段列表，支持文本与媒体混合输入
        "parts": [
            {
                # 【inline_data】(object, 条件必填) 二进制媒体数据容器，与 text 二选一
                "inline_data": {
                    # 【mime_type】(string, 必填) 媒体 MIME 类型
                    # 文档支持: application/pdf，最多 6 页
                    # 由 get_mime_type() 自动从文件扩展名识别
                    "mime_type": mime_type,
                    # 【data】(string, 必填) 媒体文件的纯 Base64 编码字符串
                    # 注意: 不得包含 data:application/pdf;base64, 前缀
                    "data": pdf_base64
                }
            }
        ]
    }
}
# 步骤4: 发送请求，只输出 embedding
try:
    response = requests.post(
        url,
        headers=headers,
        json=payload,
        timeout=300
    )
    response.raise_for_status()
    result = response.json()
    embedding_values = result["embedding"]["values"]
    print(json.dumps(embedding_values, ensure_ascii=False))
except requests.exceptions.HTTPError:
    print(response.text)
except requests.exceptions.RequestException as e:
    print(str(e))
except Exception as e:
    print(str(e))
```
### 返回示例

```json
[-0.015046478, -0.012107705, 0.019650083, 0.019790899, -0.009216446, "...", 0.014029637, -0.026796512, 0.0048678913, -0.14775057, -0.017756993]
```

## 多模态聚合嵌入

将文本和图片组合到单个 `content` 对象的多个 `parts` 中，模型将它们作为整体生成**一个**聚合嵌入向量，适用于需要同时捕获文本和视觉语义的场景（如以文搜图、跨模态检索）。

```python
import os
import json
import base64
import mimetypes
import requests

# 步骤1: 配置 API 连接信息
url = "https://www.dmxapi.cn/v1beta/models/gemini-embedding-2-preview:embedContent"
api_key = "sk-******************************************"  # 填写你的 api_key
image_path = r"C:/Users/a1/Desktop/测试保存代码/c13.png"
text_prompt = "An image of a dog"

# 步骤2: 工具函数
def get_mime_type(file_path: str) -> str:
    """
    根据本地图片路径自动识别 MIME 类型。
    """
    mime_type, _ = mimetypes.guess_type(file_path)
    if mime_type is None:
        mime_type = "image/png"
    return mime_type

def image_file_to_base64(file_path: str) -> str:
    """
    将本地图片文件转换为纯 base64 字符串。
    注意:
    返回值不会包含 data:image/png;base64, 这种前缀。
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"图片文件不存在: {file_path}")
    with open(file_path, "rb") as f:
        image_bytes = f.read()
    return base64.b64encode(image_bytes).decode("utf-8")


def remove_data_url_prefix(base64_data: str) -> str:
    """
    如果 base64 字符串不小心带了 Data URL 前缀，则自动去掉。
    例如:
      data:image/jpeg;base64,/9j/4AAQ...
    会变成:
      /9j/4AAQ...
    """
    if base64_data.startswith("data:") and ";base64," in base64_data:
        return base64_data.split(",", 1)[1]
    return base64_data

# 步骤3: 准备请求数据
headers = {
    "Content-Type": "application/json",
    # 【x-goog-api-key】(string, 必填) Gemini API 认证密钥
    "x-goog-api-key": api_key
}
mime_type = get_mime_type(image_path)
img_base64 = image_file_to_base64(image_path)
img_base64 = remove_data_url_prefix(img_base64)

payload = {
    # 【content】(object, 必填) 输入内容对象，包含多个混合模态的内容片段
    # 单个 content 包含多个 parts，模型将其聚合为一个统一嵌入向量
    "content": {
        # 【parts】(array, 必填) 内容片段列表，此处包含文本和图片两个 part
        "parts": [
            {
                # 【text】(string, 条件必填) 文本 part，与图片 part 共同组成多模态输入
                "text": text_prompt
            },
            {
                # 【inline_data】(object, 条件必填) 图片 part，与文本 part 共同组成多模态输入
                "inline_data": {
                    # 【mime_type】(string, 必填) 图片 MIME 类型，如 image/png、image/jpeg
                    "mime_type": mime_type,
                    # 【data】(string, 必填) 图片的纯 Base64 编码字符串，不含 data URL 前缀
                    "data": img_base64
                }
            }
        ]
    }
}

# 步骤4: 发送请求，只输出 embedding
try:
    response = requests.post(
        url,
        headers=headers,
        json=payload,
        timeout=120
    )
    response.raise_for_status()
    result = response.json()
    embedding_values = result["embedding"]["values"]
    print(json.dumps(embedding_values, indent=2, ensure_ascii=False))
except requests.exceptions.HTTPError:
    print(response.text)
except requests.exceptions.RequestException as e:
    print(str(e))
except Exception as e:
    print(str(e))
```

### 返回示例

```json
[
  0.0013523658,
  0.021081012,
  -0.029354148,
  -0.014817241,
  "...",
  -0.0031636902,
  -0.014405388,
  -0.016576933,
  0.017439118,
  -0.0037106818
]
```

## 批量嵌入（batchEmbedContents）

`batchEmbedContents` 端点支持在单次请求中批量处理多个独立的嵌入请求，每个请求可包含不同的内容和模态，并分别返回各自的嵌入向量，适合需要同时处理多条内容的场景。

```python
import os
import json
import base64
import mimetypes
import requests
# 步骤1: 配置 API 连接信息
url = "https://www.dmxapi.cn/v1beta/models/gemini-embedding-2-preview:batchEmbedContents"
api_key = "sk-******************************************"  # 填写你的 api_key
image_path = r"C:/Users/a1/Desktop/测试保存代码/c13.png"
text_prompt = "An image of a dog"

# 步骤2: 工具函数
def get_mime_type(file_path: str) -> str:
    """
    根据本地图片路径自动识别 MIME 类型。
    """
    mime_type, _ = mimetypes.guess_type(file_path)
    if mime_type is None:
        mime_type = "image/png"
    return mime_type
def image_file_to_base64(file_path: str) -> str:
    """
    将本地图片文件转换为纯 base64 字符串。
    注意:
    返回值不会包含 data:image/png;base64, 这种前缀。
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"图片文件不存在: {file_path}")
    with open(file_path, "rb") as f:
        image_bytes = f.read()
    return base64.b64encode(image_bytes).decode("utf-8")

def remove_data_url_prefix(base64_data: str) -> str:
    """
    如果 base64 字符串不小心带了 Data URL 前缀，则自动去掉。
    错误格式:
      data:image/jpeg;base64,/9j/4AAQ...
    正确格式:
      /9j/4AAQ...
    """
    if base64_data.startswith("data:") and ";base64," in base64_data:
        return base64_data.split(",", 1)[1]
    return base64_data

# 步骤3: 准备图片 base64 和请求参数
mime_type = get_mime_type(image_path)
img_base64 = image_file_to_base64(image_path)
# 保险处理，确保 data 里没有 data:image/...;base64, 前缀
img_base64 = remove_data_url_prefix(img_base64)
headers = {
    "Content-Type": "application/json",
    # 【x-goog-api-key】(string, 必填) Gemini API 认证密钥
    "x-goog-api-key": api_key
}
payload = {
    # 【requests】(array, 必填) 批量嵌入请求列表，每个元素为一个独立的嵌入请求
    # 每个请求会分别返回一个嵌入向量，返回顺序与请求顺序一致
    "requests": [
        {
            # 【model】(string, 必填) 每条批量请求需单独指定模型路径
            # 格式: "models/{model_name}"，与端点中的模型名一致
            "model": "models/gemini-embedding-2-preview",
            # 【content】(object, 必填) 第一条请求: 文本内容
            "content": {
                "parts": [
                    {
                        # 【text】(string, 条件必填) 纯文本输入
                        "text": text_prompt
                    }
                ]
            }
        },
        {
            # 【model】(string, 必填) 每条批量请求需单独指定模型路径
            "model": "models/gemini-embedding-2-preview",
            # 【content】(object, 必填) 第二条请求: 图片内容
            "content": {
                "parts": [
                    {
                        # 【inline_data】(object, 条件必填) 图片内容容器
                        "inline_data": {
                            # 【mime_type】(string, 必填) 图片 MIME 类型
                            "mime_type": mime_type,
                            # 【data】(string, 必填) 图片的纯 Base64 编码字符串
                            "data": img_base64
                        }
                    }
                ]
            }
        }
    ]
}
# 步骤4: 发送请求并直接输出 embeddings
try:
    response = requests.post(
        url,
        headers=headers,
        json=payload,
        timeout=120
    )
    response.raise_for_status()
    result = response.json()
    # batchEmbedContents 返回:
    # {
    #   "embeddings": [
    #     {"values": [...]},
    #     {"values": [...]}
    #   ]
    # }
    embeddings = result["embeddings"]
    print(json.dumps(embeddings, ensure_ascii=False))
except requests.exceptions.HTTPError:
    print(response.text)
except requests.exceptions.RequestException as e:
    print(str(e))
except Exception as e:
    print(str(e))
```

### 返回示例

```json
[
  {
    "values": [-0.0031602306, 0.0048682704, -0.0020779748, -0.026615573, "...", -0.025207799, 0.00014415888, -0.028636824, -0.011688847]
  },
  {
    "values": [0.0013523658, 0.021081012, -0.029354148, -0.014817241, "...", -0.014405388, -0.016576933, 0.017439118, -0.0037106818]
  }
]
```

<p align="center">
  <small>© 2026 DMXAPI gemini-embedding-2-preview 多模态嵌入</small>
</p>
