# qwen3-omni-flash 全模态模型 API 文档
Qwen-Omni 模型能够接收文本与单一其他模态（图片、音频、视频）的组合输入，并生成文本或语音形式的回复， 提供多种拟人音色，支持多语言和方言的语音输出，可应用于文本创作、视觉识别、语音助手等场景。


## 🔗 请求地址

```text
https://www.dmxapi.cn/v1/responses

```
:::tip 提示
Qwen-Omni 目前仅支持以流式输出的方式进行调用，stream参数必须设置为True，否则会报错。
:::

## 💻 文生【文+音频】示例代码

```python
import requests
import json
import base64
import os

# ============================================================================
# 配置部分 - API 连接信息
# ============================================================================

# DMXAPI 的 URL 地址
url = "https://www.dmxapi.cn/v1/responses"

# API 密钥 - 用于身份验证和访问控制
api_key = "sk-******************************************"  # ⚠️ 请替换为你的API密钥

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
    "model": "qwen3-omni-flash-all",
    "input": [
        {
            "role": "user",
            "content": "你是谁？"
        }
    ],
    "stream": True,
    "stream_options": {
        "include_usage": True
    },
    "modalities": ["text", "audio"],
    "audio": {"voice": "Serena", "format": "wav"}
}

# ============================================================================
# 发送请求并处理流式响应
# ============================================================================

# 确保 output 目录存在
os.makedirs("output", exist_ok=True)

# 发送 POST 请求到 API 服务器,启用流式响应模式
response = requests.post(url, headers=headers, json=data, stream=True)

# 检查响应状态码
if not response.ok:
    print(f"❌ HTTP 错误: {response.status_code}")
    print(f"响应内容: {response.text}")
    exit(1)

# ----------------------------------------------------------------------------
# 处理流式响应 - 解析文字并保存音频
# ----------------------------------------------------------------------------
try:
    current_event = None
    text_content = ""  # 累积文字内容

    # 逐行读取响应流
    for line in response.iter_lines():
        if line:
            line_text = line.decode('utf-8').strip()

            if line_text.startswith('event: '):
                current_event = line_text[7:]

            elif line_text.startswith('data: '):
                data_str = line_text[6:]

                try:
                    json_data = json.loads(data_str)

                    # 处理文字增量
                    if current_event == 'response.output_text.delta':
                        delta = json_data.get('delta', '')
                        if delta:
                            print(delta, end='', flush=True)
                            text_content += delta

                    # 处理音频数据
                    elif current_event == 'response.output_item.done':
                        item = json_data.get('item', {})
                        content_list = item.get('content', [])
                        for content in content_list:
                            if content.get('type') == 'output_audio':
                                audio_info = content.get('audio', {})
                                audio_data = audio_info.get('data', '')
                                audio_id = audio_info.get('id', 'output')
                                if audio_data:
                                    # 解码 base64 并保存音频文件
                                    audio_bytes = base64.b64decode(audio_data)
                                    audio_filename = os.path.join("output", f"{audio_id}.wav")
                                    with open(audio_filename, 'wb') as f:
                                        f.write(audio_bytes)
                                    print(f"\n\n音频已保存: {audio_filename}")

                except json.JSONDecodeError:
                    pass

    print(f"\n\n完整文字内容:\n{text_content}")

# ----------------------------------------------------------------------------
# 异常处理
# ----------------------------------------------------------------------------
except KeyboardInterrupt:
    # 处理用户中断 - 当用户按 Ctrl+C 时优雅退出
    print("\n\n⚠️ 用户中断了请求")

except Exception as e:
    # 处理其他异常 - 捕获并显示任何意外错误
    print(f"\n\n❌ 发生错误: {e}")

# 最后换行 - 确保输出格式整洁
print()

```






## ✈️ 文生【文+音频】（思考模式）调用示例

Qwen3-Omni-Flash在思考模式下，不支持输出音频。

Qwen3-Omni-Flash（非思考模式）：支持汉语（普通话，部分方言），英语，法语、德语、俄语、意语、西语、葡语、日语、韩语

```python
import requests
import json
import base64
import os

# ============================================================================
# 配置部分 - API 连接信息
# ============================================================================

# DMXAPI 的 URL 地址
url = "https://www.dmxapi.cn/v1/responses"

# API 密钥 - 用于身份验证和访问控制
api_key = "sk-********************************************"  # ⚠️ 请替换为你的API密钥

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
    "model": "qwen3-omni-flash-all",
    "input": [
        {
            "role": "user",
            "content": "你是谁？"
        }
    ],
    "stream": True,
    "stream_options": {
        "include_usage": True
    },
    "modalities": ["text"],
    "enable_thinking": True
}

# ============================================================================
# 发送请求并处理流式响应
# ============================================================================

# 确保 output 目录存在
os.makedirs("output", exist_ok=True)

# 发送 POST 请求到 API 服务器,启用流式响应模式
response = requests.post(url, headers=headers, json=data, stream=True)

# 检查响应状态码
if not response.ok:
    print(f"❌ HTTP 错误: {response.status_code}")
    print(f"响应内容: {response.text}")
    exit(1)

# ----------------------------------------------------------------------------
# 处理流式响应 - 解析文字并保存音频
# ----------------------------------------------------------------------------
try:
    current_event = None
    text_content = ""  # 累积文字内容

    # 逐行读取响应流
    for line in response.iter_lines():
        if line:
            line_text = line.decode('utf-8').strip()

            if line_text.startswith('event: '):
                current_event = line_text[7:]

            elif line_text.startswith('data: '):
                data_str = line_text[6:]

                try:
                    json_data = json.loads(data_str)

                    # 处理文字增量
                    if current_event == 'response.output_text.delta':
                        delta = json_data.get('delta', '')
                        if delta:
                            print(delta, end='', flush=True)
                            text_content += delta

                    # 处理音频数据
                    elif current_event == 'response.output_item.done':
                        item = json_data.get('item', {})
                        content_list = item.get('content', [])
                        for content in content_list:
                            if content.get('type') == 'output_audio':
                                audio_info = content.get('audio', {})
                                audio_data = audio_info.get('data', '')
                                audio_id = audio_info.get('id', 'output')
                                if audio_data:
                                    # 解码 base64 并保存音频文件
                                    audio_bytes = base64.b64decode(audio_data)
                                    audio_filename = os.path.join("output", f"{audio_id}.wav")
                                    with open(audio_filename, 'wb') as f:
                                        f.write(audio_bytes)
                                    print(f"\n\n音频已保存: {audio_filename}")

                except json.JSONDecodeError:
                    pass

    print(f"\n\n完整文字内容:\n{text_content}")

# ----------------------------------------------------------------------------
# 异常处理
# ----------------------------------------------------------------------------
except KeyboardInterrupt:
    # 处理用户中断 - 当用户按 Ctrl+C 时优雅退出
    print("\n\n⚠️ 用户中断了请求")

except Exception as e:
    # 处理其他异常 - 捕获并显示任何意外错误
    print(f"\n\n❌ 发生错误: {e}")

# 最后换行 - 确保输出格式整洁
print()

```





## 🚗 【文+音频】生【文+音频】调用示例
 仅支持输入一个音频文件；

文件大小：

- **Qwen3-Omni-Flash：不能超过  100MB，时长最长 20 分钟。**


以下示例代码以传入音频公网 URL 为例，传入本地音频请参见：输入 Base64 编码的本地文件。当前只支持以流式输出的方式进行调用。



```python
import requests
import json
import base64
import os

# ============================================================================
# 配置部分 - API 连接信息
# ============================================================================

# DMXAPI 的 URL 地址
url = "https://www.dmxapi.cn/v1/responses"

# API 密钥 - 用于身份验证和访问控制
api_key = "sk-*******************************************************"  # ⚠️ 请替换为你的API密钥

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
    "model": "qwen3-omni-flash-all",
    "input": [
        {
            "role": "user",
            "content": [
                {
                    "type": "input_audio",
                    "input_audio": {
                        "data": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250211/tixcef/cherry.wav",
                        "format": "wav",
                    },
                },
                {"type": "text", "text": "这段音频在说什么"},
            ],
        },
    ],
    "stream": True,
    "stream_options": {
        "include_usage": True
    },
    "modalities": ["text", "audio"],
    "audio": {"voice": "Serena", "format": "wav"}
}

# ============================================================================
# 发送请求并处理流式响应
# ============================================================================

# 确保 output 目录存在
os.makedirs("output", exist_ok=True)

# 发送 POST 请求到 API 服务器,启用流式响应模式
response = requests.post(url, headers=headers, json=data, stream=True)

# 检查响应状态码
if not response.ok:
    print(f"❌ HTTP 错误: {response.status_code}")
    print(f"响应内容: {response.text}")
    exit(1)

# ----------------------------------------------------------------------------
# 处理流式响应 - 解析文字并保存音频
# ----------------------------------------------------------------------------
try:
    current_event = None
    text_content = ""  # 累积文字内容

    # 逐行读取响应流
    for line in response.iter_lines():
        if line:
            line_text = line.decode('utf-8').strip()

            if line_text.startswith('event: '):
                current_event = line_text[7:]

            elif line_text.startswith('data: '):
                data_str = line_text[6:]

                try:
                    json_data = json.loads(data_str)

                    # 处理文字增量
                    if current_event == 'response.output_text.delta':
                        delta = json_data.get('delta', '')
                        if delta:
                            print(delta, end='', flush=True)
                            text_content += delta

                    # 处理音频数据
                    elif current_event == 'response.output_item.done':
                        item = json_data.get('item', {})
                        content_list = item.get('content', [])
                        for content in content_list:
                            if content.get('type') == 'output_audio':
                                audio_info = content.get('audio', {})
                                audio_data = audio_info.get('data', '')
                                audio_id = audio_info.get('id', 'output')
                                if audio_data:
                                    # 解码 base64 并保存音频文件
                                    audio_bytes = base64.b64decode(audio_data)
                                    audio_filename = os.path.join("output", f"{audio_id}.wav")
                                    with open(audio_filename, 'wb') as f:
                                        f.write(audio_bytes)
                                    print(f"\n\n音频已保存: {audio_filename}")

                except json.JSONDecodeError:
                    pass

    print(f"\n\n完整文字内容:\n{text_content}")

# ----------------------------------------------------------------------------
# 异常处理
# ----------------------------------------------------------------------------
except KeyboardInterrupt:
    # 处理用户中断 - 当用户按 Ctrl+C 时优雅退出
    print("\n\n⚠️ 用户中断了请求")

except Exception as e:
    # 处理其他异常 - 捕获并显示任何意外错误
    print(f"\n\n❌ 发生错误: {e}")

# 最后换行 - 确保输出格式整洁
print()

```

## 🚢 【文+图】生【文+音频】 调用示例
Qwen-Omni 模型支持传入多张图片。对输入图片的要求如下：

- **单个图片文件的大小不超过10 MB;**
- **图片数量受模型图文总 Token 上限（即最大输入）的限制，所有图片的总 Token 数必须小于模型的最大输入** ;
- **图片的宽度和高度均应大于10像素，宽高比不应超过200:1或1:200；**
- **支持的图片类型请参见视觉理解。**

以下示例代码以传入图片公网 URL 为例，传入本地图片请参见：输入 Base64 编码的本地文件。当前只支持以流式输出的方式进行调用。

```python
import requests
import json
import base64
import os

# ============================================================================
# 配置部分 - API 连接信息
# ============================================================================

# DMXAPI 的 URL 地址
url = "https://www.dmxapi.cn/v1/responses"

# API 密钥 - 用于身份验证和访问控制
api_key = "sk-*********************************************************"  # ⚠️ 请替换为你的API密钥

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
    "model": "qwen3-omni-flash-all",
    "input": [
        {
            "role": "user",
            "content": [
                {
                    "type": "image_url",
                    "image_url": {
                        "url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241022/emyrja/dog_and_girl.jpeg"
                    },
                },
                {"type": "text", "text": "图中描绘的是什么景象？"},
            ],
        },
    ],
    "stream": True,
    "stream_options": {
        "include_usage": True
    },
    "modalities": ["text", "audio"],
    "audio": {"voice": "Serena", "format": "wav"}
}

# ============================================================================
# 发送请求并处理流式响应
# ============================================================================

# 确保 output 目录存在
os.makedirs("output", exist_ok=True)

# 发送 POST 请求到 API 服务器,启用流式响应模式
response = requests.post(url, headers=headers, json=data, stream=True)

# 检查响应状态码
if not response.ok:
    print(f"❌ HTTP 错误: {response.status_code}")
    print(f"响应内容: {response.text}")
    exit(1)

# ----------------------------------------------------------------------------
# 处理流式响应 - 解析文字并保存音频
# ----------------------------------------------------------------------------
try:
    current_event = None
    text_content = ""  # 累积文字内容

    # 逐行读取响应流
    for line in response.iter_lines():
        if line:
            line_text = line.decode('utf-8').strip()

            if line_text.startswith('event: '):
                current_event = line_text[7:]

            elif line_text.startswith('data: '):
                data_str = line_text[6:]

                try:
                    json_data = json.loads(data_str)

                    # 处理文字增量
                    if current_event == 'response.output_text.delta':
                        delta = json_data.get('delta', '')
                        if delta:
                            print(delta, end='', flush=True)
                            text_content += delta

                    # 处理音频数据
                    elif current_event == 'response.output_item.done':
                        item = json_data.get('item', {})
                        content_list = item.get('content', [])
                        for content in content_list:
                            if content.get('type') == 'output_audio':
                                audio_info = content.get('audio', {})
                                audio_data = audio_info.get('data', '')
                                audio_id = audio_info.get('id', 'output')
                                if audio_data:
                                    # 解码 base64 并保存音频文件
                                    audio_bytes = base64.b64decode(audio_data)
                                    audio_filename = os.path.join("output", f"{audio_id}.wav")
                                    with open(audio_filename, 'wb') as f:
                                        f.write(audio_bytes)
                                    print(f"\n\n音频已保存: {audio_filename}")

                except json.JSONDecodeError:
                    pass

    print(f"\n\n完整文字内容:\n{text_content}")

# ----------------------------------------------------------------------------
# 异常处理
# ----------------------------------------------------------------------------
except KeyboardInterrupt:
    # 处理用户中断 - 当用户按 Ctrl+C 时优雅退出
    print("\n\n⚠️ 用户中断了请求")

except Exception as e:
    # 处理其他异常 - 捕获并显示任何意外错误
    print(f"\n\n❌ 发生错误: {e}")

# 最后换行 - 确保输出格式整洁
print()

```




## 🚄 【文+图片集】生【文+音频】 调用示例
以下示例代码以传入视频公网 URL 为例，传入本地视频请参见：输入 Base64 编码的本地文件。当前只支持以流式输出的方式进行调用。

图片数量：
- **Qwen3-Omni-Flash：最少传入 2 张图片，最多可传入 128 张图片。**
```python
import requests
import json
import base64
import os

# ============================================================================
# 配置部分 - API 连接信息
# ============================================================================

# DMXAPI 的 URL 地址
url = "https://www.dmxapi.cn/v1/responses"

# API 密钥 - 用于身份验证和访问控制
api_key = "sk-*********************************************************"  # ⚠️ 请替换为你的API密钥

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
    "model": "qwen3-omni-flash-all",
    "input": [
        {
            "role": "user",
            "content": [
                {
                    "type": "video",
                    "video": [
                        "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241108/xzsgiz/football1.jpg",
                        "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241108/tdescd/football2.jpg",
                        "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241108/zefdja/football3.jpg",
                        "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241108/aedbqh/football4.jpg",
                    ],
                },
                {"type": "text", "text": "描述这个视频的具体过程"},
            ],
        }
    ],
    "stream": True,
    "stream_options": {
        "include_usage": True
    },
    "modalities": ["text", "audio"],
    "audio": {"voice": "Serena", "format": "wav"}
}

# ============================================================================
# 发送请求并处理流式响应
# ============================================================================

# 确保 output 目录存在
os.makedirs("output", exist_ok=True)

# 发送 POST 请求到 API 服务器,启用流式响应模式
response = requests.post(url, headers=headers, json=data, stream=True)

# 检查响应状态码
if not response.ok:
    print(f"❌ HTTP 错误: {response.status_code}")
    print(f"响应内容: {response.text}")
    exit(1)

# ----------------------------------------------------------------------------
# 处理流式响应 - 解析文字并保存音频
# ----------------------------------------------------------------------------
try:
    current_event = None
    text_content = ""  # 累积文字内容

    # 逐行读取响应流
    for line in response.iter_lines():
        if line:
            line_text = line.decode('utf-8').strip()

            if line_text.startswith('event: '):
                current_event = line_text[7:]

            elif line_text.startswith('data: '):
                data_str = line_text[6:]

                try:
                    json_data = json.loads(data_str)

                    # 处理文字增量
                    if current_event == 'response.output_text.delta':
                        delta = json_data.get('delta', '')
                        if delta:
                            print(delta, end='', flush=True)
                            text_content += delta

                    # 处理音频数据
                    elif current_event == 'response.output_item.done':
                        item = json_data.get('item', {})
                        content_list = item.get('content', [])
                        for content in content_list:
                            if content.get('type') == 'output_audio':
                                audio_info = content.get('audio', {})
                                audio_data = audio_info.get('data', '')
                                audio_id = audio_info.get('id', 'output')
                                if audio_data:
                                    # 解码 base64 并保存音频文件
                                    audio_bytes = base64.b64decode(audio_data)
                                    audio_filename = os.path.join("output", f"{audio_id}.wav")
                                    with open(audio_filename, 'wb') as f:
                                        f.write(audio_bytes)
                                    print(f"\n\n音频已保存: {audio_filename}")

                except json.JSONDecodeError:
                    pass

    print(f"\n\n完整文字内容:\n{text_content}")

# ----------------------------------------------------------------------------
# 异常处理
# ----------------------------------------------------------------------------
except KeyboardInterrupt:
    # 处理用户中断 - 当用户按 Ctrl+C 时优雅退出
    print("\n\n⚠️ 用户中断了请求")

except Exception as e:
    # 处理其他异常 - 捕获并显示任何意外错误
    print(f"\n\n❌ 发生错误: {e}")

# 最后换行 - 确保输出格式整洁
print()
```




## 🚀 【文+视频】生【文+音频】 调用示例
仅支持输入一个视频文件；

文件大小：

- **Qwen3-Omni-Flash：限制为 256 MB，时长限制为 150s；**

:::tip
    视频文件中的视觉信息与音频信息会分开计费。
:::

```python
import requests
import json
import base64
import os

# ============================================================================
# 配置部分 - API 连接信息
# ============================================================================

# DMXAPI 的 URL 地址
url = "https://www.dmxapi.cn/v1/responses"

# API 密钥 - 用于身份验证和访问控制
api_key = "sk-*********************************************************"  # ⚠️ 请替换为你的API密钥

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
    "model": "qwen3-omni-flash-all",
    "input": [
        {
            "role": "user",
            "content": [
                {
                    "type": "video_url",
                    "video_url": {
                        "url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241115/cqqkru/1.mp4"
                    },
                },
                {"type": "text", "text": "详细介绍一下视频内容和视频的背景音乐内容?"},
            ],
        },
    ],
    "stream": True,
    "stream_options": {
        "include_usage": True
    },
    "modalities": ["text", "audio"],
    "audio": {"voice": "Serena", "format": "wav"}
}

# ============================================================================
# 发送请求并处理流式响应
# ============================================================================

# 确保 output 目录存在
os.makedirs("output", exist_ok=True)

# 发送 POST 请求到 API 服务器,启用流式响应模式
response = requests.post(url, headers=headers, json=data, stream=True)

# 检查响应状态码
if not response.ok:
    print(f"❌ HTTP 错误: {response.status_code}")
    print(f"响应内容: {response.text}")
    exit(1)

# ----------------------------------------------------------------------------
# 处理流式响应 - 解析文字并保存音频
# ----------------------------------------------------------------------------
try:
    current_event = None
    text_content = ""  # 累积文字内容

    # 逐行读取响应流
    for line in response.iter_lines():
        if line:
            line_text = line.decode('utf-8').strip()

            if line_text.startswith('event: '):
                current_event = line_text[7:]

            elif line_text.startswith('data: '):
                data_str = line_text[6:]

                try:
                    json_data = json.loads(data_str)

                    # 处理文字增量
                    if current_event == 'response.output_text.delta':
                        delta = json_data.get('delta', '')
                        if delta:
                            print(delta, end='', flush=True)
                            text_content += delta

                    # 处理音频数据
                    elif current_event == 'response.output_item.done':
                        item = json_data.get('item', {})
                        content_list = item.get('content', [])
                        for content in content_list:
                            if content.get('type') == 'output_audio':
                                audio_info = content.get('audio', {})
                                audio_data = audio_info.get('data', '')
                                audio_id = audio_info.get('id', 'output')
                                if audio_data:
                                    # 解码 base64 并保存音频文件
                                    audio_bytes = base64.b64decode(audio_data)
                                    audio_filename = os.path.join("output", f"{audio_id}.wav")
                                    with open(audio_filename, 'wb') as f:
                                        f.write(audio_bytes)
                                    print(f"\n\n音频已保存: {audio_filename}")

                except json.JSONDecodeError:
                    pass

    print(f"\n\n完整文字内容:\n{text_content}")

# ----------------------------------------------------------------------------
# 异常处理
# ----------------------------------------------------------------------------
except KeyboardInterrupt:
    # 处理用户中断 - 当用户按 Ctrl+C 时优雅退出
    print("\n\n⚠️ 用户中断了请求")

except Exception as e:
    # 处理其他异常 - 捕获并显示任何意外错误
    print(f"\n\n❌ 发生错误: {e}")

# 最后换行 - 确保输出格式整洁
print()

```
## 🧙‍♀️ 多轮对话 调用示例
您在使用 Qwen-Omni 模型的多轮对话功能时，需要注意：

- **Assistant Message:**

添加到 messages 数组中的 Assistant Message 只可以包含文本数据。

- **User Message:**

一条 User Message 只可以包含文本和一种模态的数据，在多轮对话中您可以在不同的 User Message 中输入不同模态的数据。

```python
import requests
import json
import base64
import os

# ============================================================================
# 配置部分 - API 连接信息
# ============================================================================

# DMXAPI 的 URL 地址
url = "https://www.dmxapi.cn/v1/responses"

# API 密钥 - 用于身份验证和访问控制
api_key = "sk-**************************************************"  # ⚠️ 请替换为你的API密钥

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
    "model": "qwen3-omni-flash-all",
    "input": [
        {
            "role": "user",
            "content": [
                {
                    "type": "input_audio",
                    "input_audio": {
                        "data": "https://dashscope.oss-cn-beijing.aliyuncs.com/audios/welcome.mp3"
                    }
                },
                {
                    "type": "text",
                    "text": "这段音频在说什么"
                }
            ]
        },
        {
            "role": "assistant",
            "content": [
                {
                    "type": "text",
                    "text": "这段音频在说：欢迎使用阿里云"
                }
            ]
        },
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": "介绍一下这家公司？"
                }
            ]
        }
    ],
    "stream": True,
    "stream_options": {
        "include_usage": True
    },
    "modalities": ["text"]
}

# ============================================================================
# 发送请求并处理流式响应
# ============================================================================

# 确保 output 目录存在
os.makedirs("output", exist_ok=True)

# 发送 POST 请求到 API 服务器,启用流式响应模式
response = requests.post(url, headers=headers, json=data, stream=True)

# 检查响应状态码
if not response.ok:
    print(f"❌ HTTP 错误: {response.status_code}")
    print(f"响应内容: {response.text}")
    exit(1)

# ----------------------------------------------------------------------------
# 处理流式响应 - 解析文字并保存音频
# ----------------------------------------------------------------------------
try:
    current_event = None
    text_content = ""  # 累积文字内容

    # 逐行读取响应流
    for line in response.iter_lines():
        if line:
            line_text = line.decode('utf-8').strip()

            if line_text.startswith('event: '):
                current_event = line_text[7:]

            elif line_text.startswith('data: '):
                data_str = line_text[6:]

                try:
                    json_data = json.loads(data_str)

                    # 处理文字增量
                    if current_event == 'response.output_text.delta':
                        delta = json_data.get('delta', '')
                        if delta:
                            print(delta, end='', flush=True)
                            text_content += delta

                    # 处理音频数据
                    elif current_event == 'response.output_item.done':
                        item = json_data.get('item', {})
                        content_list = item.get('content', [])
                        for content in content_list:
                            if content.get('type') == 'output_audio':
                                audio_info = content.get('audio', {})
                                audio_data = audio_info.get('data', '')
                                audio_id = audio_info.get('id', 'output')
                                if audio_data:
                                    # 解码 base64 并保存音频文件
                                    audio_bytes = base64.b64decode(audio_data)
                                    audio_filename = os.path.join("output", f"{audio_id}.wav")
                                    with open(audio_filename, 'wb') as f:
                                        f.write(audio_bytes)
                                    print(f"\n\n音频已保存: {audio_filename}")

                except json.JSONDecodeError:
                    pass

    print(f"\n\n完整文字内容:\n{text_content}")

# ----------------------------------------------------------------------------
# 异常处理
# ----------------------------------------------------------------------------
except KeyboardInterrupt:
    # 处理用户中断 - 当用户按 Ctrl+C 时优雅退出
    print("\n\n⚠️ 用户中断了请求")

except Exception as e:
    # 处理其他异常 - 捕获并显示任何意外错误
    print(f"\n\n❌ 发生错误: {e}")

# 最后换行 - 确保输出格式整洁
print()

```

## ☀️支持的音色

**支持的音色：**输出音频的音色与文件格式通过`audio`参数来配置，如：`audio={"voice": "Cherry", "format": "wav"}`：


- 文件格式（`format`）：只支持设定为`"wav"`；

- 音频音色（`voice）`：

-  音色表

- | **音色名**  | `**voice**`**参数** | **描述**                                                     | **支持的语种**                                               |
  | ----------- | ------------------- | ------------------------------------------------------------ | ------------------------------------------------------------ |
  | 芊悦        | Cherry              | 阳光积极、亲切自然小姐姐                                     | 中文、英语、法语、德语、俄语、意大利语、西班牙语、葡萄牙语、日语、韩语 |
  | 苏瑶        | Serena              | 温柔小姐姐                                                   | 中文、英语、法语、德语、俄语、意大利语、西班牙语、葡萄牙语、日语、韩语 |
  | 晨煦        | Ethan               | 标准普通话，带部分北方口音。阳光、温暖、活力、朝气           | 中文、英语、法语、德语、俄语、意大利语、西班牙语、葡萄牙语、日语、韩语 |
  | 千雪        | Chelsie             | 二次元虚拟女友                                               | 中文、英语、法语、德语、俄语、意大利语、西班牙语、葡萄牙语、日语、韩语 |
  | 茉兔        | Momo                | 撒娇搞怪，逗你开心                                           | 中文、英语、法语、德语、俄语、意大利语、西班牙语、葡萄牙语、日语、韩语 |
  | 十三        | Vivian              | 拽拽的、可爱的小暴躁                                         | 中文、英语、法语、德语、俄语、意大利语、西班牙语、葡萄牙语、日语、韩语 |
  | 月白        | Moon                | 率性帅气的月白                                               | 中文、英语、法语、德语、俄语、意大利语、西班牙语、葡萄牙语、日语、韩语 |
  | 四月        | Maia                | 知性与温柔的碰撞                                             | 中文、英语、法语、德语、俄语、意大利语、西班牙语、葡萄牙语、日语、韩语 |
  | 凯          | Kai                 | 耳朵的一场SPA                                                | 中文、英语、法语、德语、俄语、意大利语、西班牙语、葡萄牙语、日语、韩语 |
  | 不吃鱼      | Nofish              | 不会翘舌音的设计师                                           | 中文、英语、法语、德语、俄语、意大利语、西班牙语、葡萄牙语、日语、韩语 |
  | 萌宝        | Bella               | 喝酒不打醉拳的小萝莉                                         | 中文、英语、法语、德语、俄语、意大利语、西班牙语、葡萄牙语、日语、韩语 |
  | 詹妮弗      | Jennifer            | 品牌级、电影质感般美语女声                                   | 中文、英语、法语、德语、俄语、意大利语、西班牙语、葡萄牙语、日语、韩语 |
  | 甜茶        | Ryan                | 节奏拉满，戏感炸裂，真实与张力共舞                           | 中文、英语、法语、德语、俄语、意大利语、西班牙语、葡萄牙语、日语、韩语 |
  | 卡捷琳娜    | Katerina            | 御姐音色，韵律回味十足                                       | 中文、英语、法语、德语、俄语、意大利语、西班牙语、葡萄牙语、日语、韩语 |
  | 艾登        | Aiden               | 精通厨艺的美语大男孩                                         | 中文、英语、法语、德语、俄语、意大利语、西班牙语、葡萄牙语、日语、韩语 |
  | 沧明子      | Eldric Sage         | 沉稳睿智的老者，沧桑如松却心明如镜                           | 中文、英语、法语、德语、俄语、意大利语、西班牙语、葡萄牙语、日语、韩语 |
  | 乖小妹      | Mia                 | 温顺如春水，乖巧如初雪                                       | 中文、英语、法语、德语、俄语、意大利语、西班牙语、葡萄牙语、日语、韩语 |
  | 沙小弥      | Mochi               | 聪明伶俐的小大人，童真未泯却早慧如禅                         | 中文、英语、法语、德语、俄语、意大利语、西班牙语、葡萄牙语、日语、韩语 |
  | 燕铮莺      | Bellona             | 声音洪亮，吐字清晰，人物鲜活，听得人热血沸腾；金戈铁马入梦来，字正腔圆间尽显千面人声的江湖 | 中文、英语、法语、德语、俄语、意大利语、西班牙语、葡萄牙语、日语、韩语 |
  | 田叔        | Vincent             | 一口独特的沙哑烟嗓，一开口便道尽了千军万马与江湖豪情         | 中文、英语、法语、德语、俄语、意大利语、西班牙语、葡萄牙语、日语、韩语 |
  | 萌小姬      | Bunny               | “萌属性”爆棚的小萝莉                                         | 中文、英语、法语、德语、俄语、意大利语、西班牙语、葡萄牙语、日语、韩语 |
  | 阿闻        | Neil                | 平直的基线语调，字正腔圆的咬字发音，这就是最专业的新闻主持人 | 中文、英语、法语、德语、俄语、意大利语、西班牙语、葡萄牙语、日语、韩语 |
  | 墨讲师      | Elias               | 既保持学科严谨性，又通过叙事技巧将复杂知识转化为可消化的认知模块 | 中文、英语、法语、德语、俄语、意大利语、西班牙语、葡萄牙语、日语、韩语 |
  | 徐大爷      | Arthur              | 被岁月和旱烟浸泡过的质朴嗓音，不疾不徐地摇开了满村的奇闻异事 | 中文、英语、法语、德语、俄语、意大利语、西班牙语、葡萄牙语、日语、韩语 |
  | 邻家妹妹    | Nini                | 糯米糍一样又软又黏的嗓音，那一声声拉长了的“哥哥”，甜得能把人的骨头都叫酥了 | 中文、英语、法语、德语、俄语、意大利语、西班牙语、葡萄牙语、日语、韩语 |
  | 诡婆婆      | Ebona               | 她的低语像一把生锈的钥匙，缓慢转动你内心最深处的幽暗角落——那里藏着所有你不敢承认的童年阴影与未知恐惧 | 中文、英语、法语、德语、俄语、意大利语、西班牙语、葡萄牙语、日语、韩语 |
  | 小婉        | Seren               | 温和舒缓的声线，助你更快地进入睡眠，晚安，好梦               | 中文、英语、法语、德语、俄语、意大利语、西班牙语、葡萄牙语、日语、韩语 |
  | 顽屁小孩    | Pip                 | 调皮捣蛋却充满童真的他来了，这是你记忆中的小新吗             | 中文、英语、法语、德语、俄语、意大利语、西班牙语、葡萄牙语、日语、韩语 |
  | 少女阿月    | Stella              | 平时是甜到发腻的迷糊少女音，但在喊出“代表月亮消灭你”时，瞬间充满不容置疑的爱与正义 | 中文、英语、法语、德语、俄语、意大利语、西班牙语、葡萄牙语、日语、韩语 |
  | 博德加      | Bodega              | 热情的西班牙大叔                                             | 中文、英语、法语、德语、俄语、意大利语、西班牙语、葡萄牙语、日语、韩语 |
  | 索尼莎      | Sonrisa             | 热情开朗的拉美大姐                                           | 中文、英语、法语、德语、俄语、意大利语、西班牙语、葡萄牙语、日语、韩语 |
  | 阿列克      | Alek                | 一开口，是战斗民族的冷，也是毛呢大衣下的暖                   | 中文、英语、法语、德语、俄语、意大利语、西班牙语、葡萄牙语、日语、韩语 |
  | 多尔切      | Dolce               | 慵懒的意大利大叔                                             | 中文、英语、法语、德语、俄语、意大利语、西班牙语、葡萄牙语、日语、韩语 |
  | 素熙        | Sohee               | 温柔开朗，情绪丰富的韩国欧尼                                 | 中文、英语、法语、德语、俄语、意大利语、西班牙语、葡萄牙语、日语、韩语 |
  | 小野杏      | Ono Anna            | 鬼灵精怪的青梅竹马                                           | 中文、英语、法语、德语、俄语、意大利语、西班牙语、葡萄牙语、日语、韩语 |
  | 莱恩        | Lenn                | 理性是底色，叛逆藏在细节里——穿西装也听后朋克的德国青年       | 中文、英语、法语、德语、俄语、意大利语、西班牙语、葡萄牙语、日语、韩语 |
  | 埃米尔安    | Emilien             | 浪漫的法国大哥哥                                             | 中文、英语、法语、德语、俄语、意大利语、西班牙语、葡萄牙语、日语、韩语 |
  | 安德雷      | Andre               | 声音磁性，自然舒服、沉稳男生                                 | 中文、英语、法语、德语、俄语、意大利语、西班牙语、葡萄牙语、日语、韩语 |
  | 拉迪奥·戈尔 | Radio Gol           | 足球诗人Rádio Gol！今天我要用名字为你们解说足球。            | 中文、英语、法语、德语、俄语、意大利语、西班牙语、葡萄牙语、日语、韩语 |
  | 上海-阿珍   | Jada                | 风风火火的沪上阿姐                                           | 中文（上海话）、英语、法语、德语、俄语、意大利语、西班牙语、葡萄牙语、日语、韩语 |
  | 北京-晓东   | Dylan               | 北京胡同里长大的少年                                         | 中文（北京话）、英语、法语、德语、俄语、意大利语、西班牙语、葡萄牙语、日语、韩语 |
  | 南京-老李   | Li                  | 耐心的瑜伽老师                                               | 中文（南京话）、英语、法语、德语、俄语、意大利语、西班牙语、葡萄牙语、日语、韩语 |
  | 陕西-秦川   | Marcus              | 面宽话短，心实声沉——老陕的味道                               | 中文（陕西话）、英语、法语、德语、俄语、意大利语、西班牙语、葡萄牙语、日语、韩语 |
  | 闽南-阿杰   | Roy                 | 诙谐直爽、市井活泼的台湾哥仔形象                             | 中文（闽南语）、英语、法语、德语、俄语、意大利语、西班牙语、葡萄牙语、日语、韩语 |
  | 天津-李彼得 | Peter               | 天津相声，专业捧哏                                           | 中文（天津话）、英语、法语、德语、俄语、意大利语、西班牙语、葡萄牙语、日语、韩语 |
  | 四川-晴儿   | Sunny               | 甜到你心里的川妹子                                           | 中文（四川话）、英语、法语、德语、俄语、意大利语、西班牙语、葡萄牙语、日语、韩语 |
  | 四川-程川   | Eric                | 一个跳脱市井的四川成都男子                                   | 中文（四川话）、英语、法语、德语、俄语、意大利语、西班牙语、葡萄牙语、日语、韩语 |
  | 粤语-阿强   | Rocky               | 幽默风趣的阿强，在线陪聊                                     | 中文（粤语）、英语、法语、德语、俄语、意大利语、西班牙语、葡萄牙语、日语、韩语 |
  | 粤语-阿清   | Kiki                | 甜美的港妹闺蜜                                               | 中文（粤语）、英语、法语、德语、俄语、意大利语、西班牙语、葡萄牙语、日语、韩语 |

**必须使用流式输出**：所有对 Qwen-Omni 模型的请求都必须设置 `stream=True`。


## 💐base64文件传入

本地图片：
```python
{

                    "type": "image_url",
                    "image_url": {"url": f"data:image/png;base64,{base64_image}"},
 }
```

本地音频：
```python
 {

                    "type": "input_audio",
                    "input_audio": {
                        "data": f"data:;base64,{base64_audio}",
                        "format": "mp3",
},
```

本地视频：
```python
 {

                    "type": "input_audio",

                    "input_audio": {

                        "data": f"data:;base64,{base64_audio}",

                        "format": "mp3",

},
```

## 🎩qwen官方网站

网站地址：
```
https://help.aliyun.com/zh/model-studio/qwen-omni
```

<p align="center">
  <small>© 2025 DMXAPI qwen3-omni-flash 全模态模型</small>
</p>