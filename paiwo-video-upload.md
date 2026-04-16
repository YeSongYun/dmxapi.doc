# paiwo-video 视频上传 API 使用文档

paiwo-video 是拍我 AI 开放平台提供的媒体资源上传接口，支持将本地视频文件（Base64 编码）或远程 URL 上传至平台，返回唯一的 media_id 供后续 API 调用时引用。视频支持 mp4、mov、webm 格式，最大分辨率 1920、文件大小 50MB、时长 30 秒；音频支持 mp3、wav、aac、m4a 等格式，最大 50MB 与 30 秒时长。

## 模型名称

- `paiwo-video`

## 接口地址

| 接口 | 请求方式 | URL |
|------|---------|-----|
| 上传资源（视频） | POST | `https://www.dmxapi.cn/v1/responses` |

:::warning
请妥善保管您的 API Key！严禁将密钥泄露给他人、硬编码到代码中或提交到公开的代码仓库。
:::

## 示例代码

::: code-group

```python [本地文件上传]
import requests
import json
import base64

# 步骤1: 配置 API 连接信息

# DMXAPI 服务端点地址
url = "https://www.dmxapi.cn/v1/responses"

# DMXAPI 密钥 (请替换为您自己的密钥)
# 获取方式: 登录 DMXAPI 官网 -> 个人中心 -> API 密钥管理
api_key = "sk-******************************************"

# 步骤2: 配置请求头

headers = {
    # 【Content-Type】(string, 必需) 请求体格式，固定为 application/json
    "Content-Type": "application/json",
    # 【Authorization】(string, 必需) API 鉴权密钥，直接传入 DMXAPI Key，无需加 Bearer 前缀
    "Authorization": f"{api_key}",
}

# 步骤3: 读取文件并配置请求参数

# 读取本地视频或音频文件，转换为 Base64 编码字符串
# 支持视频格式: mp4 / mov / webm，最大分辨率 1920，文件大小上限 50MB，时长上限 30 秒
# 支持音频格式: mp3 / wav / aac / m4a，文件大小上限 50MB，时长上限 30 秒
video_path = "your_video.mp4"  # 替换为实际文件路径
with open(video_path, "rb") as f:
    video_base64 = base64.b64encode(f.read()).decode("utf-8")

payload = {
    # 【model】(string, 必需) 模型名称，固定值为 paiwo-video
    # 用于调用拍我AI媒体资源上传功能
    "model": "paiwo-video",

    # 【input】(string, 必需) 文件的 Base64 编码字符串
    # 将本地视频或音频文件读取后以标准 Base64 编码传入
    # 上传成功后返回的 media_id 可在图像生成视频、特效模板、对口型等后续接口中引用
    "input": video_base64,
}

# 步骤4: 发送请求并输出结果

response = requests.post(url, headers=headers, json=payload)

print(json.dumps(response.json(), indent=2, ensure_ascii=False))
```

```python [远程 URL 上传]
import requests
import json

# 步骤1: 配置 API 连接信息

# DMXAPI 服务端点地址
url = "https://www.dmxapi.cn/v1/responses"

# DMXAPI 密钥 (请替换为您自己的密钥)
# 获取方式: 登录 DMXAPI 官网 -> 个人中心 -> API 密钥管理
api_key = "sk-******************************************"

# 步骤2: 配置请求头

headers = {
    "Content-Type": "application/json",      # 指定请求体为 JSON 格式
    "Authorization": f"{api_key}",           # token 认证方式
}

# 步骤3: 配置请求参数

payload = {
    # 【model】(string, 必填) 指定上传资源所用模型
    # 使用 "paiwo-video" 调用拍我 AI 的视频/音频上传接口
    "model": "paiwo-video",

    # 【input】(string, 必填) 待上传资源的 URL 地址
    # 与本地文件上传（Base64）二选一，此处使用 URL 方式上传
    # 支持视频格式: mp4 / mov / webm / quicktime
    # 支持音频格式: mp3 / wav / m4a / aac
    # 视频限制: 最大分辨率 1920，最大文件大小 50MB，最大时长 30 秒
    # 音频限制: 最大文件大小 50MB，最大时长 30 秒
    "input": "https://www.runoob.com/try/demo_source/mov_bbb.mp4",  # 替换为实际视频/音频 URL
}

# 步骤4: 发送请求并输出结果

# 发送 POST 请求到 API 服务器
response = requests.post(url, headers=headers, json=payload)

# 格式化输出 JSON 响应
# - indent=2: 缩进 2 空格，便于阅读
# - ensure_ascii=False: 正确显示中文字符
print(json.dumps(response.json(), indent=2, ensure_ascii=False))
```

:::

### 返回示例

```json
{
  "ErrCode": 0,
  "ErrMsg": "success",
  "Resp": {
    "media_id": 397173518038512,
    "media_type": "video",
    "url": "https://media.pixverseai.cn/openapi/9a1d9e0c-41f2-4179-b253-c03d088eef5b.mp4"
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
  <small>© 2026 DMXAPI paiwo-video 视频上传</small>
</p>
