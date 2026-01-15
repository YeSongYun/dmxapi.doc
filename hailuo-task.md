# 海螺视频 API 首尾帧生成文档

本文档介绍如何使用 DMXAPI 的海螺视频首尾帧生成接口（MiniMax-Hailuo-02 模型），支持通过指定首帧和尾帧图片生成高质量视频内容。

## 快速开始

使用海螺视频 API 需要三个步骤：
1. **提交任务** - 上传首尾帧图片和视频描述
2. **查询状态** - 监控生成进度
3. **下载视频** - 获取最终的视频文件

## API 接口地址

| 功能 | 接口端点 | 请求方式 |
|------|---------|---------|
| 提交任务 | `https://www.dmxapi.cn/v1/video_generation` | POST |
| 查询任务 | `https://www.dmxapi.cn/v1/query/video_generation` | GET |
| 下载视频 | `https://www.dmxapi.cn/v1/files/retrieve` | GET |

## 模型名称

`MiniMax-Hailuo-02`

## 1. 提交视频生成任务

向服务器提交视频生成请求，需要提供视频描述、首尾帧图片（可选）等信息。

### 示例代码
```python
import requests
import json

# ============ DMXAPI配置 ============
url = "https://www.dmxapi.cn/v1/video_generation"

headers = {
    "Content-Type": "application/json",
    "Authorization": "sk-*******************************************" # 替换为你的实际DMXAPI密钥
}

# ============ 请求参数配置 ============
payload = {
    # 模型名称（必填）
    # 可用值：MiniMax-Hailuo-02
    # 注意：首尾帧生成功能不支持 512P 分辨率
    "model": "MiniMax-Hailuo-02",

    # 视频文本描述（必填）
    # 最大 2000 字符，支持使用 [指令] 语法进行运镜控制
    #
    # 支持的15种运镜指令：
    # - 左右移：[左移], [右移]
    # - 左右摇：[左摇], [右摇]
    # - 推拉：[推进], [拉远]
    # - 升降：[上升], [下降]
    # - 上下摇：[上摇], [下摇]
    # - 变焦：[变焦推近], [变焦拉远]
    # - 其他：[晃动], [跟随], [固定]
    #
    # 使用规则：
    # 1. 组合运镜：同一组 [] 内的多个指令会同时生效，如 [左摇,上升]（建议不超过3个）
    # 2. 顺序运镜：prompt中前后出现的指令会依次生效，如 "...[推进], 然后...[拉远]"
    # 3. 自然语言：也支持通过自然语言描述运镜，但使用标准指令能获得更准确的响应
    "prompt": "A little girl grow up.",

    # 首帧图片（可选）
    # 将指定图片作为视频的起始帧
    # 支持公网URL或Base64编码的Data URL (data:image/jpeg;base64,...)
    #
    # 图片要求：
    # - 格式：JPG, JPEG, PNG, WebP
    # - 体积：小于 20MB
    # - 尺寸：短边像素大于 300px，长宽比在 2:5 和 5:2 之间
    # ⚠️ 生成视频尺寸遵循首帧图片
    "first_frame_image": "https://filecdn.minimax.chat/public/fe9d04da-f60e-444d-a2e0-18ae743add33.jpeg",

    # 尾帧图片（可选）
    # 将指定图片作为视频的结束帧
    # 支持公网URL或Base64编码的Data URL (data:image/jpeg;base64,...)
    #
    # 图片要求：
    # - 格式：JPG, JPEG, PNG, WebP
    # - 体积：小于 20MB
    # - 尺寸：短边像素大于 300px，长宽比在 2:5 和 5:2 之间
    # ⚠️ 生成视频尺寸遵循首帧图片，当首帧和尾帧的图片尺寸不一致时，模型将参考首帧对尾帧图片进行裁剪
    "last_frame_image": "https://filecdn.minimax.chat/public/97b7cd08-764e-4b8b-a7bf-87a0bd898575.jpeg",

    # 视频时长（可选）
    # 单位：秒，默认值为 6
    # 首尾帧生成可用值与分辨率相关：
    # - 768P：6 或 10 秒
    # - 1080P：6 秒
    "duration": 6,

    # 视频分辨率（可选）
    # 首尾帧生成支持 768P 和 1080P
    # - MiniMax-Hailuo-02 默认值：768P
    # 可用选项：768P, 1080P
    "resolution": "768P",

    # Prompt优化（可选）
    # 是否自动优化 prompt，默认为 true
    # 设为 false 可进行更精确的控制
    # "prompt_optimizer": True,

    # AIGC水印（可选）
    # 是否在生成的视频中添加水印，默认为 false
    # "aigc_watermark": False
}

# ============ 发送请求 ============
print("正在发送视频生成请求...")
response = requests.post(url, json=payload, headers=headers)

# ============ 输出结果 ============
print("\n响应结果：")
print(json.dumps(response.json(), indent=2, ensure_ascii=False))
```

### 返回示例

响应成功时返回任务 ID，用于后续查询：

```json
{
  "task_id": "335812458701204",
  "base_resp": {
    "status_code": 0,
    "status_msg": "success"
  }
}
```

### 参数说明

#### 必填参数
- **model** - 模型名称，固定值：`MiniMax-Hailuo-02`
- **prompt** - 视频描述文本（最多 2000 字符），支持 [指令] 语法控制运镜效果

#### 图片参数（可选）
- **first_frame_image** - 首帧图片 URL 或 Base64，指定视频起始帧
- **last_frame_image** - 尾帧图片 URL 或 Base64，指定视频结束帧

**图片要求：**
- 格式：JPG, JPEG, PNG, WebP
- 大小：小于 20MB
- 尺寸：短边 > 300px，长宽比在 2:5 ~ 5:2 之间
- 重要：生成视频的尺寸会遵循首帧图片；首尾帧尺寸不一致时，模型会参考首帧对尾帧进行裁剪

#### 生成参数（可选）
- **duration** - 视频时长（秒），默认 6 秒
  - 768P 分辨率：6 或 10 秒
  - 1080P 分辨率：6 秒
- **resolution** - 分辨率，可选值：`768P`（默认）、`1080P`
- **prompt_optimizer** - 是否自动优化描述文本，默认 true
- **aigc_watermark** - 是否添加 AIGC 水印，默认 false


## 2. 查询任务状态

查询已提交任务的生成进度和状态。

### 示例代码
```python
# ================================
# 视频生成任务查询脚本
# ================================

import requests
import json

# ================================
# 1. 配置 DMXAPI 信息
# ================================

# DMXAPI 基础地址
base_url = "https://www.dmxapi.cn"

# DMXAPI 端点：查询视频生成状态
endpoint = "/v1/query/video_generation"

# 视频生成任务 ID
task_id = "335812458701204"

# ================================
# 2. 认证信息
# ================================

# DMMXAPI 授权令牌（Token）
token = "sk-*******************************************"

# ================================
# 3. 构建 HTTP 请求
# ================================

# 完整的请求 URL
url = f"{base_url}{endpoint}?task_id={task_id}"

# 请求头，包含认证信息
headers = {
    "Authorization": f"{token}"
}

# ================================
# 4. 发送 API 请求
# ================================

response = requests.get(url, headers=headers)

# ================================
# 5. 处理和显示响应
# ================================

# 显示 HTTP 状态码
print(f"Status Code: {response.status_code}")

# 显示完整的 JSON 响应（格式化输出）
print("Response:")
print(json.dumps(response.json(), indent=2, ensure_ascii=False))
```

### 返回示例

```json
{
  "status": "Success",
  "file_id": "335811572470048",
  "task_id": "335812458701204",
  "base_resp": {
    "status_msg": "success",
    "status_code": 0
  },
  "video_width": 1364,
  "video_height": 768
}
```

### 状态说明

- **status: Success** - 视频生成完成，可使用 `file_id` 下载
- **status: Processing** - 视频正在生成中。
- **status: Failed** - 视频生成失败，检查错误信息


## 3. 下载视频文件

使用 `file_id` 和 `task_id` 获取生成的视频下载链接。

### 示例代码
```python
import requests
import json

# ======================== API 配置 ========================
# DMXAPI 基础 URL
BASE_URL = "https://www.dmxapi.cn"  # 替换为实际的 API 域名

# 文件 ID - 用于标识要检索的文件
FILE_ID = "335811572470048"

# 任务 ID - 用于标识相关的任务
TASK_ID = "335812458701204"

# 认证令牌 - 用于 DMXAPI 请求的身份验证
TOKEN = "sk-*******************************************"

# ======================== 构建 API 请求 ========================
# 文件检索端点 URL
url = f"{BASE_URL}/v1/files/retrieve"

# 请求参数：包含文件 ID 和任务 ID
params = {
    "file_id": FILE_ID,      # 指定要检索的文件
    "task_id": TASK_ID       # 指定相关的任务
}

# 请求头：包含认证信息
headers = {
    "Authorization": f"{TOKEN}"  # 令牌认证
}

# ======================== 发送 API 请求 ========================
# 发送 GET 请求到 API 端点
response = requests.get(url, params=params, headers=headers)

# ======================== 输出响应结果 ========================
# 输出 HTTP 状态码
print(f"Status Code: {response.status_code}")

# 输出格式化的 JSON 响应内容
print(f"Response:\n{json.dumps(response.json(), indent=2, ensure_ascii=False)}")
```

### 返回示例

```json
{
  "file": {
    "file_id": 335811572470048,
    "bytes": 0,
    "created_at": 1763538787,
    "filename": "output_aigc.mp4",
    "purpose": "video_generation",
    "download_url": "https://public-cdn-video-data-algeng.oss-cn-wulanchabu.aliyuncs.com/inference_output%2Fvideo%2F2025-11-19%2F51e89e4d-5fbd-4469-999d-f831e3c8618d%2Foutput_aigc.mp4?Expires=1763571243&OSSAccessKeyId=LTAI5tAmwsjSaaZVA6cEFAUu&Signature=9lng5ac8OJHCfpgVnPCQLzgl0%2B0%3D"
  },
  "base_resp": {
    "status_code": 0,
    "status_msg": "success"
  }
}
```

### 下载说明

- **download_url** - 视频的临时下载链接，建议在获取后立即下载
- **expires** - 下载链接有时间限制，请在过期前完成下载
- 下载后的视频格式为 MP4，可直接使用


## 常见问题

### 认证与安全
- 使用有效的 Token 进行身份验证
- **不要在公开代码中暴露密钥**，建议使用环境变量存储
- 定期轮换密钥以确保安全性

### 首尾帧图片
- 如果仅上传首帧，视频会从该帧开始生成
- 如果仅上传尾帧，视频会以该帧结束
- 首帧和尾帧都提供时，效果最佳
- 首尾帧尺寸需接近，否则模型会自动裁剪尾帧

### 运镜指令
- 使用 `[指令]` 格式准确控制镜头运动
- 组合指令需用逗号分隔，如 `[左摇,上升]`
- 顺序指令依次执行，如 `[推进] 后 [拉远]`
- 过多指令可能影响视频质量，建议不超过 3 个

### 生成时间
- 视频生成通常需要 1-5 分钟
- 高分辨率或长时长的视频可能需要更长时间


---

<p align="center">
  <small>© 2025 DMXAPI 海螺视频</small>
</p>
