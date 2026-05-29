# Vidu视频模型 viduq2-ctv（viduq2） 参考生视频 API使用文档

作为国内首款实现商业落地的视频模型，viduq2一经推出，即获众多淘宝商家青睐。其卓越的视频生成能力，在真实感与流畅度上均表现出色，成为可靠的商用视频解决方案。

## 模型名称
`viduq2-ctv`

## 接口地址
调用 `viduq2-ctv` 官方接口需分两步：  

1. 提交视频生成任务  
2. 根据返回的 `ID` 查询结果  

| 功能 | 端点 |
|------|------|
| 提交视频任务 | `https://www.dmxapi.cn/v1/responses` |
| 查询视频结果 | `https://www.dmxapi.cn/v1/responses` |


## 可选参数
- `resolution`：视频分辨率，默认 `720p`，可选值：`540p` / `720p` / `1080p`
- `duration`：视频时长（单位：秒）
  - 默认值：`5`
  - 可选值：`1` - `10`

## 创建多图参考生视频任务示例
```python
import requests
import json
# ============================================================================
# 配置部分 - API 连接信息
# ============================================================================
# DMXAPI 的 URL 地址
url = "https://www.dmxapi.cn/v1/responses"
# API 密钥 - 用于身份验证和访问控制
# ⚠️ 请替换为您自己实际的API密钥
api_key = "sk-******************************"  
# ============================================================================
# 请求头配置 - 设置内容类型和授权信息
# ============================================================================
headers = {
    "Content-Type": "application/json",      # 指定请求体为 JSON 格式
    "Authorization": f"{api_key}",    # token 认证方式
}
# ============================================================================
# 请求参数配置 - AI 模型与输入内容
# ============================================================================
data = {
    # ---------- 基础配置 ----------
    "model": "viduq2-ctv",
    "subjects": [
        {
            "id": "1",
            "images": ["https://prod-ss-images.s3.cn-northwest-1.amazonaws.com.cn/vidu-maas/template/reference2video-2.png", "https://prod-ss-images.s3.cn-northwest-1.amazonaws.com.cn/vidu-maas/template/reference2video-3.png"],
            "voice_id": ""
        },
        {
            "id": "2",
            "images": ["https://prod-ss-images.s3.cn-northwest-1.amazonaws.com.cn/vidu-maas/template/reference2video-1.png"],
            "voice_id": ""
        },
    ],
    # ---------- prompt 文本提示词 ----------
    # 生成视频的文本描述
    # 注：字符长度不能超过 2000 个字符
    "input": "@1 中的两个小人在 @2 的场景中拥抱",

    # ---------- 视频时长配置 ----------
    # 默认值：5 秒，可选范围：1-10 秒
    "duration": 8,

    "audio": True,

    # ---------- 随机种子配置 ----------
    # 当默认不传或者传 0 时，会使用随机数替代
    # 手动设置则使用设置的种子
    "seed": 0,

    "aspect_ratio": "16:9",

    # ---------- 视频分辨率配置 ----------
    # 默认值：720p，可选值：540p、720p、1080p
    "resolution": "720p",

    "movement_amplitude": "auto",

    # ---------- 水印配置 ----------
    # 是否添加水印
    # - true：添加水印
    # - false：不添加水印
    # 注：目前水印内容为固定，内容由 AI 生成，默认不加
    "watermark": False,

    # ---------- 水印位置配置 ----------
    # 表示水印出现在图片的位置，可选项为：
    # 1：左上角
    # 2：右上角
    # 3：右下角
    # 4：左下角
    "wm_position": 3,

    # ---------- 水印内容配置 ----------
    # 水印内容，此处为图片 URL
    # 不传时，使用默认水印：内容由 AI 生成
    "wm_url": "https://prod-ss-images.s3.cn-northwest-1.amazonaws.com.cn/vidu-maas/template/reference2video-3.png",

    # ---------- 回调地址配置 ----------
    # Callback 协议：请求方法为 POST
    # 当视频生成任务有状态变化时，Vidu 将向此地址发送包含任务最新状态的回调请求
    # 回调请求内容结构与查询任务 API 的返回体一致
    # 回调返回的 status 包括以下状态：
    # - processing：任务处理中
    # - success：任务完成（如发送失败，回调三次）
    # - failed：任务失败（如发送失败，回调三次）
    "callback_url": "https://prod-ss-images.s3.cn-northwest-1.amazonaws.com.cn"
}
# ============================================================================
# 发送请求并处理非流式响应
# ============================================================================
# 发送 POST 请求到 API 服务器
response = requests.post(url, headers=headers, json=data)
# ----------------------------------------------------------------------------
# 处理非流式响应 - 格式化打印原始 JSON 数据
# ----------------------------------------------------------------------------
try:
    # 获取响应的 JSON 数据
    response_data = response.json()
    # 格式化打印原始 JSON 响应
    # indent=2: 使用2个空格缩进
    # ensure_ascii=False: 保留中文字符不转义
    print(json.dumps(response_data, indent=2, ensure_ascii=False))
# ----------------------------------------------------------------------------
# 异常处理
# ----------------------------------------------------------------------------
except KeyboardInterrupt:
    # 处理用户中断 - 当用户按 Ctrl+C 时优雅退出
    print("\n\n⚠️ 用户中断了请求")
except json.JSONDecodeError as e:
    # 处理 JSON 解析错误
    print(f"❌ JSON 解析错误: {e}")
    print(f"原始响应内容: {response.text}")
except Exception as e:
    # 处理其他异常 - 捕获并显示任何意外错误
    print(f"❌ 发生错误: {e}")
```

### 返回示例

```json
{
  "task_id": "903875784081420288",
  "type": "character2video",
  "state": "created",
  "model": "viduq2",
  "style": "general",
  "prompt": "@2 中的两个小人在 @1 的场景中拥抱",
  "images": [
    "https://prod-ss-images.s3.cn-northwest-1.amazonaws.com.cn/vidu-maas/template/reference2video-2.png",
    "https://prod-ss-images.s3.cn-northwest-1.amazonaws.com.cn/vidu-maas/template/reference2video-3.png",
    "https://prod-ss-images.s3.cn-northwest-1.amazonaws.com.cn/vidu-maas/template/reference2video-1.png"
  ],
  "duration": 8,
  "seed": 1070246527,
  "aspect_ratio": "16:9",
  "resolution": "720p",
  "movement_amplitude": "auto",
  "created_at": 1767172295,
  "credits": 75,
  "payload": "",
  "cus_priority": 0,
  "off_peak": false,
  "watermark": false,
  "is_rec": false,
  "wm_position": "bottom_right",
  "wm_url": "https://prod-ss-images.s3.cn-northwest-1.amazonaws.com.cn/vidu-maas/template/reference2video-3.png",
  "meta_data": "",
  "client_request_id": "",
  "usage": {
    "total_tokens": 234375,
    "input_tokens": 0,
    "input_tokens_details": {
      "cached_tokens": 0
    },
    "output_tokens": 234375,
    "output_tokens_details": {
      "reasoning_tokens": 0
    }
  }
}

```

## 任务结果查询示例

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

url = "https://www.dmxapi.cn/v1/responses"

# API 密钥 - 用于身份验证和访问控制
# ⚠️ 请替换为您自己实际的API密钥
api_key = "sk-******************************"
headers = {
    "Content-Type": "application/json",
    "Authorization": f"{api_key}",

}

data = {
    # model: 指定查询所使用的模型/接口
    # - 不同模型对应不同的视频生成能力
    "model": "vidu-get",
    # input: 要查询的任务 ID
    # ⚠️请替换为您在"创建多图参考生视频任务示例"的返回结果中获取的实际的任务ID
    "input": "**************************",
    # stream: 是否启用流式响应
    # - True: 启用 SSE 流式传输，实时接收生成进度
    # - False: 等待任务完成后一次性返回结果
    # - 推荐用 True 以获得更好的用户体验
    "stream": True
}

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

### 返回示例
```json
============================================================
🚀 发送流式请求...
============================================================
状态码: 200
------------------------------------------------------------
[████████████████████] 100.00% 生成完成!

✅ 视频生成完成！
任务ID: 903875784081420288
--- 创作 1 ---
视频URL: https://prod-ss-vidu.s3.cn-northwest-1.amazonaws.com.cn/infer/tasks/25/1231/09/903875784081420288/creation-01/video.mp4?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIARRHG6JR7EMNHVUWT%2F20251231%2Fcn-northwest-1%2Fs3%2Faws4_request&X-Amz-Date=20251231T091307Z&X-Amz-Expires=86400&X-Amz-SignedHeaders=host&response-cache-control=max-age%3D86400&response-content-disposition=attachment%3Bfilename%3Dgeneral-9-2025-12-31T09%253A13%253A04Z.mp4&x-id=GetObject&X-Amz-Signature=1625f8aa540c0ce09cf043f353b443352365e0d2baa3c6b0b0a7df2427843ac9
封面URL: https://prod-ss-vidu.s3.cn-northwest-1.amazonaws.com.cn/infer/tasks/25/1231/09/903875784081420288/creation-01/cover.jpeg?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIARRHG6JR7EMNHVUWT%2F20251231%2Fcn-northwest-1%2Fs3%2Faws4_request&X-Amz-Date=20251231T091307Z&X-Amz-Expires=3600&X-Amz-SignedHeaders=host&response-cache-control=max-age%3D86400&x-id=GetObject&X-Amz-Signature=6746c50de6b7062409950751b3d9dcc43a6f0b33e6933246dfa0d03768782e83

============================================================
🏁 流式输出结束
============================================================
```

---

<p align="center">
  <small>© 2025 DMXAPI viduq2-ctv</small>
</p>