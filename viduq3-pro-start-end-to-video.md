# viduq3-pro 首尾帧生视频 API 使用文档

viduq3-pro 首尾帧生视频 API 支持传入首帧和尾帧两张图像，并结合文本提示词异步生成首尾连贯的视频内容。该模型支持 1-16 秒视频生成，分辨率最高可选 1080p，并支持 q3 系列专属的音视频直出能力，可输出包含台词和音效的音画同步视频。

## 模型名称

- `viduq3-pro`

## 接口地址

| 接口 | 请求方式 | URL |
|------|---------|-----|
| 提交任务 | POST | `https://www.dmxapi.cn/v1/responses` |

:::warning
请妥善保管您的 API Key！严禁将密钥泄露给他人、硬编码到代码中或提交到公开的代码仓库。
:::

## 首尾帧生视频 示例代码

```python
import requests
import json

# 步骤1: 配置 API 连接信息

# DMXAPI 服务端点地址
url = "https://www.dmxapi.cn/v1/responses"

# DMXAPI 密钥，请替换为您自己的密钥
# 获取方式: 登录 DMXAPI 官网 -> 个人中心 -> API 密钥管理
api_key = "sk-******************************************"

# 步骤2: 配置请求头

headers = {
    "Content-Type": "application/json",
    "Authorization": f"{api_key}",
}

# 步骤3: 配置请求参数

payload = {
    # 【model】(string, 必填) 模型名称。
    # 当前文档使用 viduq3-pro：高效生成优质音视频内容，让视频内容更生动、更形象、更立体，效果更好。
    "model": "viduq3-pro",

    # 【input】(array[string], 必填) DMXAPI 图像输入参数，对应 Vidu 官方文档中的 images 参数。
    # 支持输入两张图：第一张图片视作首帧图，第二张图片视作尾帧图，模型将根据两张图生成视频。
    # 支持传入图片 Base64 编码或图片 URL；图片支持 png、jpeg、jpg、webp 格式，单张图片大小不超过 50MB。
    # 首尾帧两张输入图的分辨率需相近，首帧图分辨率 / 尾帧图分辨率需在 0.8-1.25 之间；图片比例需小于 1:4 或 4:1。
    # 请注意，HTTP 请求的 POST body 不超过 20MB；Base64 编码需包含适当的内容类型字符串，例如 data:image/png;base64,{base64_encode}。
    "input": [
        "https://prod-ss-images.s3.cn-northwest-1.amazonaws.com.cn/vidu-maas/template/startend2video-1.jpeg",
        "https://prod-ss-images.s3.cn-northwest-1.amazonaws.com.cn/vidu-maas/template/startend2video-2.jpeg",
    ],

    # 【prompt】(string, 可选) 文本提示词。
    # 用于填写生成视频的文本描述；官方限制字符长度不能超过 5000 个字符。
    # 若使用 is_rec 推荐提示词参数，模型将不考虑此参数所输入的提示词。
    "prompt": "图一的鸟在图二的人头上，两个主体互动，跳舞",

    # 【is_rec】(bool, 可选) 是否使用推荐提示词。
    # true 表示由系统自动推荐提示词，并使用推荐提示词内容生成视频，推荐提示词数量为 1。
    "is_rec": False,

    # 【duration】(int, 可选) 视频时长参数。
    # viduq3-pro 默认 5 秒，可选范围为 1-16 秒。
    "duration": 10,

    # 【seed】(int, 可选) 随机种子。
    # 默认不传或传 0 时，会使用随机数替代；手动设置时使用指定种子。
    "seed": 0,

    # 【resolution】(string, 可选) 视频分辨率。
    # viduq3-pro 在 1-16 秒时默认 720p，可选值: "540p" / "720p" / "1080p"。
    "resolution": "1080p",

    # 【audio】(bool, 可选) 是否使用音视频直出能力。
    # 默认值为 true；false 表示输出静音视频，true 表示需要音画同步并输出带声音的视频（包括台词和音效）。
    # 仅 q3 系列模型支持该参数。
    "audio": True,

    # 【watermark】(bool, 可选) 是否添加水印。
    # true 表示添加水印，false 表示不添加水印；官方说明目前水印内容固定，默认不添加。
    # 可通过 watermarked_url 参数查询获取带水印的视频内容，详情见查询任务接口。
    "watermark": False,

    # 【wm_position】(int, 可选) 水印位置。
    # 可选值: 1=左上角，2=右上角，3=右下角，4=左下角；默认值为 3。
    "wm_position": 3,

    # 【wm_url】(string, 可选) 水印内容图片 URL。
    # 不传或为空时，使用默认水印：内容由 AI 生成。
    "wm_url": "",

    # 【callback_url】(string, 可选) 任务状态变化回调地址。
    # 创建任务时主动设置 callback_url 后，当视频生成任务状态变化时，Vidu 将向该地址发送 POST 回调请求。
    # 回调请求内容结构与查询任务 API 的返回体一致。
    # 回调状态包括: processing=任务处理中，success=任务完成，failed=任务失败；发送失败时会回调三次。
    "callback_url": "https://www.dmxapi.cn",
}

# 步骤4: 发送请求并输出结果

response = requests.post(url, headers=headers, json=payload)

print(json.dumps(response.json(), indent=2, ensure_ascii=False))
```

### 返回示例

```json
{
  "task_id": "947408590711308288",
  "type": "headtailimg2video",
  "state": "created",
  "model": "viduq3-pro",
  "style": "general",
  "prompt": "图一的鸟在图二的人头上，两个主体互动，跳舞",
  "images": [
    "https://prod-ss-images.s3.cn-northwest-1.amazonaws.com.cn/vidu-maas/template/startend2video-1.jpeg",
    "https://prod-ss-images.s3.cn-northwest-1.amazonaws.com.cn/vidu-maas/template/startend2video-2.jpeg"
  ],
  "duration": 10,
  "seed": 2042719333,
  "aspect_ratio": "",
  "resolution": "1080p",
  "movement_amplitude": "auto",
  "created_at": 1777551325,
  "credits": 300,
  "payload": "",
  "cus_priority": 0,
  "off_peak": false,
  "watermark": false,
  "is_rec": false,
  "wm_position": "bottom_right",
  "wm_url": "",
  "meta_data": "",
  "client_request_id": "",
  "audio_type": "all",
  "usage": {
    "total_tokens": 93750,
    "input_tokens": 0,
    "input_tokens_details": {
      "cached_tokens": 0
    },
    "output_tokens": 93750,
    "output_tokens_details": {
      "reasoning_tokens": 0
    }
  }
}
```
## 获取生成视频 示例代码
```python
"""
================================================================================
DMXAPI 视频生成任务查询脚本
================================================================================

功能说明:
    本脚本用于查询 DMXAPI 平台上视频生成任务的状态和结果。
    通过提供任务 ID，可以实时获取视频生成进度，并在完成后获取下载链接。
依赖库:
    - requests: HTTP 请求库，用于发送 API 请求
    - json: JSON 解析库，用于处理响应数据

================================================================================
"""

import requests  # HTTP 请求库 - 用于发送网络请求
import json      # JSON 处理库 - 用于解析 API 响应数据

# ╔════════════════════════════════════════════════════════════════════════════╗
# ║                           第一部分: API 连接配置                              ║
# ╚════════════════════════════════════════════════════════════════════════════╝
#
# 说明: 此部分配置 API 服务器地址和身份验证信息
#       请确保 API 密钥的安全性，不要泄露给他人
#

# API 服务端点地址
# - 生产环境: https://www.dmxapi.cn/v1/responses
# - 该接口用于查询视频生成任务的状态和结果
url = "https://www.dmxapi.cn/v1/responses"

# API 密钥 (API Key)
# - 用途: 身份验证，确保只有授权用户可以访问 API
# - 格式: 以 "sk-" 开头的字符串
# - 注意: 请妥善保管，不要将密钥提交到公开代码仓库
api_key = "sk-***********************************************"

# ╔════════════════════════════════════════════════════════════════════════════╗
# ║                          第二部分: HTTP 请求头配置                            ║
# ╚════════════════════════════════════════════════════════════════════════════╝
#
# 说明: HTTP 请求头用于告知服务器请求的格式和认证信息
#       这是 RESTful API 调用的标准配置
#

headers = {
    # Content-Type: 指定请求体的媒体类型
    # - application/json 表示请求体为 JSON 格式
    # - 服务器会根据此字段正确解析请求数据
    "Content-Type": "application/json",

    # Authorization: 身份验证头
    # - 认证方案: OAuth 2.0 标准的令牌认证方式
    # - 格式: "<token>"
    # - 服务器通过此字段验证请求者身份
    "Authorization": f"{api_key}",
}

# ╔════════════════════════════════════════════════════════════════════════════╗
# ║                          第三部分: 请求参数配置                               ║
# ╚════════════════════════════════════════════════════════════════════════════╝
#
# 说明: 此部分定义发送给 API 的核心参数
#       包括模型选择、任务 ID 和响应模式
#

data = {
    # model: 指定查询所使用的模型/接口
    # - viduq2-pro-get: Vidu Q2 Pro 版本的任务查询接口（这个模型不要更改，就用viduq2-pro-get）
    # - 不同模型对应不同的视频生成能力
    "model": "vidu-get",

    # input: 要查询的任务 ID
    # - 此 ID 由创建任务时返回
    # - 每个任务有唯一的 ID 标识
    # - 请替换为您实际的任务 ID
    "input": "949909892414607360",

    # stream: 是否启用流式响应
    # - True: 启用 SSE 流式传输，实时接收生成进度
    # - False: 等待任务完成后一次性返回结果
    # - 推荐使用 True 以获得更好的用户体验
    "stream": True
}

# ╔════════════════════════════════════════════════════════════════════════════╗
# ║                       第四部分: 发送请求并处理响应                             ║
# ╚════════════════════════════════════════════════════════════════════════════╝
#
# 说明: 此部分负责发送 HTTP 请求并处理服务器返回的流式响应
#       使用 SSE 技术实时接收任务进度更新
#

# ----------------------------- 4.1 输出启动信息 -----------------------------
# 向用户显示程序已开始执行，提供清晰的视觉分隔
print("=" * 60)
print("🚀 发送流式请求...")
print("=" * 60)

# ----------------------------- 4.2 发送 API 请求 -----------------------------
# requests.post() 参数说明:
# - url: API 服务端点地址
# - headers: HTTP 请求头，包含认证信息
# - json: 请求体数据，会自动序列化为 JSON
# - stream=True: 启用流式响应，允许逐行读取返回数据
response = requests.post(url, headers=headers, json=data, stream=True)

# 输出 HTTP 状态码，便于调试和确认请求是否成功
# - 200: 请求成功
# - 401: 认证失败（检查 API 密钥）
# - 404: 任务不存在（检查任务 ID）
# - 500: 服务器内部错误
print(f"状态码: {response.status_code}")
print("-" * 60)
print()

# ----------------------------- 4.3 处理流式响应 -----------------------------
# SSE (Server-Sent Events) 响应格式说明:
# - 每条消息以 "data: " 开头
# - 后跟 JSON 格式的数据
# - 消息之间用空行分隔
#
# 响应数据结构示例:
# {
#     "delta": "当前进度: 50%",        // 增量更新内容
#     "type": "response.completed"    // 响应类型标识
# }
#
try:
    # iter_lines(): 迭代器方法，逐行读取响应内容
    # - 避免一次性加载全部数据到内存
    # - 适合处理大量或持续的流式数据
    for line in response.iter_lines():
        # 跳过空行（SSE 协议中用于分隔消息）
        if line:
            # 将字节数据解码为 UTF-8 字符串
            decoded_line = line.decode('utf-8')

            # --------------- 4.3.1 解析 SSE 数据格式 ---------------
            # 检查是否为标准 SSE 数据行
            if decoded_line.startswith('data: '):
                # 提取 JSON 部分（去掉 "data: " 前缀，共 6 个字符）
                json_str = decoded_line[6:]

                try:
                    # 将 JSON 字符串解析为 Python 字典
                    data_obj = json.loads(json_str)

                    # --------------- 4.3.2 处理增量更新 ---------------
                    # delta 字段包含实时进度信息
                    if 'delta' in data_obj:
                        delta_text = data_obj['delta']

                        # 检测任务完成信号
                        # 当收到完成消息时，显示 100% 进度条
                        if '✅ 视频生成完成' in delta_text:
                            print('\r[████████████████████] 100.00% 生成完成!', flush=True)

                        # 输出增量内容
                        # - end='': 不换行，保持进度条在同一行更新
                        # - flush=True: 立即刷新输出缓冲区
                        print(delta_text, end='', flush=True)

                    # --------------- 4.3.3 处理完成信号 ---------------
                    # type='response.completed' 表示响应流结束
                    elif data_obj.get('type') == 'response.completed':
                        # 响应完成，无需额外处理
                        # 此时所有数据已通过 delta 输出
                        pass

                except json.JSONDecodeError:
                    # JSON 解析失败时，直接输出原始内容
                    # 可能是服务器返回了非标准格式的数据
                    print(decoded_line)

# ----------------------------- 4.4 异常处理 -----------------------------
except KeyboardInterrupt:
    # 捕获 Ctrl+C 中断信号
    # 允许用户优雅地终止长时间运行的查询
    print("\n\n⚠️ 用户中断了请求")

except Exception as e:
    # 捕获所有其他异常
    # 包括网络错误、连接超时等
    print(f"\n\n❌ 发生错误: {e}")

# ----------------------------- 4.5 输出结束信息 -----------------------------
# 程序执行完毕，输出结束标识
print()
print("=" * 60)
print("🏁 流式输出结束")
print("=" * 60)
```

## 返回示例
```json
============================================================
🚀 发送流式请求...
============================================================
状态码: 200
------------------------------------------------------------

[████████████████████] 100.00% 生成完成!


✅ 视频生成完成！

任务ID: 949913121705701376

--- 创作 1 ---
视频URL: https://prod-ss-vidu.s3.cn-northwest-1.amazonaws.com.cn/infer_76/tasks/26/0507/10/949913121705701376/creation-01/video.mp4?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Checksum-Mode=ENABLED&X-Amz-Credential=AKIARRHG6JR7EMNHVUWT%2F20260507%2Fcn-northwest-1%2Fs3%2Faws4_request&X-Amz-Date=20260507T100937Z&X-Amz-Expires=86400&X-Amz-SignedHeaders=host&response-cache-control=max-age%3D86400&response-content-disposition=attachment%3Bfilename%3Dgeneral-6-2026-05-07T10%253A09%253A34Z.mp4&x-id=GetObject&X-Amz-Signature=5bf63b6edd60b2fec21b7526afdaae3b421836e876802b5107e1ca43d76147ce
封面URL: https://prod-ss-vidu.s3.cn-northwest-1.amazonaws.com.cn/infer_76/tasks/26/0507/10/949913121705701376/creation-01/cover.jpeg?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Checksum-Mode=ENABLED&X-Amz-Credential=AKIARRHG6JR7EMNHVUWT%2F20260507%2Fcn-northwest-1%2Fs3%2Faws4_request&X-Amz-Date=20260507T100937Z&X-Amz-Expires=3600&X-Amz-SignedHeaders=host&response-cache-control=max-age%3D86400&x-id=GetObject&X-Amz-Signature=7ea042e10ee38dba95a5976df33758185115655bc4d9182d868018e65be9c329

============================================================
🏁 流式输出结束
============================================================

```


<p align="center">
  <small>© 2026 DMXAPI viduq3-pro 首尾帧生视频</small>
</p>
