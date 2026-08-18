# qwen3-omni-30b-a3b-captioner 音频理解 API 文档

Qwen3-Omni-Captioner是以通义千问3-Omni为基座的开源模型，无需任何提示，自动为复杂语音、环境声、音乐、影视声效等生成精准、全面的描述，能识别说话人的情绪、音乐元素（如风格、乐器）、敏感信息等，适用于音频内容分析、安全审核、意图识别、音频剪辑等多个领域。

## 📍 请求地址

```
https://www.dmxapi.cn/v1/chat/completions
```

## 🎯 模型名称

`qwen3-omni-30b-a3b-captioner` 

## 💻 音频理解URL 调用示例

```python
# ============================================================================
#                    Qwen3-Omni 音频理解示例 (URL方式)
# ============================================================================
# 功能说明：通过URL方式上传音频文件，使用Qwen3-Omni模型进行音频内容理解
# 模型名称：qwen3-omni-30b-a3b-captioner
# ============================================================================

import requests

# ----------------------------------------------------------------------------
#                              API 配置信息
# ----------------------------------------------------------------------------
# 接口地址：DMXAPI Chat Completions 端点
url = "https://www.dmxapi.cn/v1/chat/completions"

# 请求头配置
headers = {
    "Authorization": "sk-*****************************************",  # API密钥
    "Content-Type": "application/json"                                              # 内容类型
}

# ----------------------------------------------------------------------------
#                              请求体构建
# ----------------------------------------------------------------------------
data = {
    # 指定使用的模型
    "model": "qwen3-omni-30b-a3b-captioner",

    # 消息列表
    "messages": [
        {
            "role": "user",
            "content": [
                {
                    # 音频输入类型
                    "type": "input_audio",
                    "input_audio": {
                        # 音频文件URL地址（支持公网可访问的音频链接）
                        "data": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20240916/xvappi/装修噪音.wav"
                    }
                }
            ]
        }
    ]
}

# ----------------------------------------------------------------------------
#                              发送请求并输出结果
# ----------------------------------------------------------------------------
response = requests.post(url, headers=headers, json=data)
print(response.json())
```

## 🚗 音频理解URL（流式输出）调用示例
```python
# ============================================================================
#              Qwen3-Omni 音频理解示例 (URL方式 - 流式输出)
# ============================================================================
# 功能说明：通过URL方式上传音频，使用流式输出实时获取模型响应
# 模型名称：qwen3-omni-30b-a3b-captioner
# ============================================================================

import requests
import json
import time

# ----------------------------------------------------------------------------
#                              API 配置信息
# ----------------------------------------------------------------------------
API_KEY = "sk-******************************************"  # API密钥
BASE_URL = "https://www.dmxapi.cn/v1/chat/completions"            # 接口地址

# ----------------------------------------------------------------------------
#                              请求头配置
# ----------------------------------------------------------------------------
headers = {
    "Authorization": f"{API_KEY}",  # 认证信息
    "Content-Type": "application/json"     # 内容类型
}

# ----------------------------------------------------------------------------
#                              请求体构建
# ----------------------------------------------------------------------------
data = {
    # 指定使用的模型
    "model": "qwen3-omni-30b-a3b-captioner",

    # 消息列表
    "messages": [
        {
            "role": "user",
            "content": [
                {
                    "type": "input_audio",      # 音频输入类型
                    "input_audio": {
                        # 音频文件URL地址
                        "data": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20240916/xvappi/%E8%A3%85%E4%BF%AE%E5%99%AA%E9%9F%B3.wav"
                    }
                }
            ]
        }
    ],

    # ------------------------------------------------------------------------
    #                           流式输出配置
    # ------------------------------------------------------------------------
    "stream": True,                 # 启用流式输出
    "stream_options": {
        "include_usage": True       # 在流式响应中包含Token用量统计
    }
}


# ============================================================================
#                              主函数
# ============================================================================
def main():
    """
    主函数：发送流式请求并处理响应
    功能包括：实时输出、首Token延迟计算、Token用量统计
    """
    print("开始请求...")

    # ------------------------------------------------------------------------
    #                           初始化计时与变量
    # ------------------------------------------------------------------------
    start_time = time.time()      # 记录请求开始时间
    first_token_time = None       # 首个Token到达时间
    full_response = ""            # 完整响应内容
    usage_info = None             # Token用量信息

    # ------------------------------------------------------------------------
    #                           发送流式请求
    # ------------------------------------------------------------------------
    try:
        response = requests.post(
            BASE_URL,
            headers=headers,
            json=data,
            stream=True               # 启用流式接收
        )
        response.raise_for_status()   # 检查HTTP状态码

        # --------------------------------------------------------------------
        #                       逐行处理流式响应
        # --------------------------------------------------------------------
        for line in response.iter_lines():
            if line:
                line = line.decode('utf-8')

                # 处理SSE格式数据（以"data: "开头）
                if line.startswith("data: "):
                    json_str = line[6:]           # 去掉 "data: " 前缀

                    # 检测流结束标志
                    if json_str == "[DONE]":
                        break

                    try:
                        chunk = json.loads(json_str)

                        # 提取并输出内容片段
                        if "choices" in chunk and len(chunk["choices"]) > 0:
                            delta = chunk["choices"][0].get("delta", {})
                            content = delta.get("content", "")

                            if content:
                                # 记录首Token时间
                                if first_token_time is None:
                                    first_token_time = time.time()
                                # 实时输出内容（不换行）
                                print(content, end="", flush=True)
                                full_response += content

                        # 提取Token用量信息
                        if "usage" in chunk:
                            usage_info = chunk["usage"]

                    except json.JSONDecodeError:
                        continue

        print("\n")

    # ------------------------------------------------------------------------
    #                           异常处理
    # ------------------------------------------------------------------------
    except requests.exceptions.RequestException as e:
        print(f"\n请求错误: {e}")
        return

    # ========================================================================
    #                           统计信息输出
    # ========================================================================
    end_time = time.time()
    total_time = end_time - start_time

    print("=" * 50)
    print("统计信息:")
    print(f"  总耗时: {total_time:.2f}秒")

    # 首Token延迟 (TTFT: Time To First Token)
    if first_token_time:
        ttft = first_token_time - start_time
        print(f"  首Token延迟: {ttft:.2f}秒")

    # Token用量详情
    if usage_info:
        prompt_tokens = usage_info.get("prompt_tokens", 0)
        completion_tokens = usage_info.get("completion_tokens", 0)
        total_tokens = usage_info.get("total_tokens", 0)

        print(f"  输入Tokens: {prompt_tokens}")
        print(f"  输出Tokens: {completion_tokens}")
        print(f"  总Tokens: {total_tokens}")

        # 计算输出速度
        if total_time > 0 and completion_tokens > 0:
            tokens_per_sec = completion_tokens / total_time
            print(f"  输出速度: {tokens_per_sec:.2f} tokens/秒")


# ============================================================================
#                              程序入口
# ============================================================================
if __name__ == "__main__":
    main()
```



## 🚀音频理解本地（base64）

```python
# ============================================================================
#              Qwen3-Omni 音频理解示例 (本地文件 - Base64方式)
# ============================================================================
# 功能说明：读取本地音频文件，转换为Base64编码后发送给模型进行理解
# 模型名称：qwen3-omni-30b-a3b-captioner
# 适用场景：本地音频文件处理、无公网URL的音频分析
# ============================================================================

import base64
import requests

# ----------------------------------------------------------------------------
#                              API 配置信息
# ----------------------------------------------------------------------------
api_key = "sk-************************************************"  # API密钥
url = "https://www.dmxapi.cn/v1/chat/completions"                 # 接口地址

# ----------------------------------------------------------------------------
#                              音频文件配置
# ----------------------------------------------------------------------------
# 填写本地音频文件路径，支持 wav、mp3 等格式
# 留空则使用默认示例数据
file_path = "qwen/装修噪音.wav"  # 例如: "C:/audio/test.mp3"


# ============================================================================
#                              工具函数
# ============================================================================
def file_to_base64(path):
    """
    读取本地文件并转换为Base64编码字符串

    参数:
        path: 文件路径
    返回:
        Base64编码的字符串
    """
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")


# ----------------------------------------------------------------------------
#                           音频数据准备
# ----------------------------------------------------------------------------
# 根据是否填写文件路径，自动转换本地文件或使用示例数据
if file_path:
    audio_data = f"data:;base64,{file_to_base64(file_path)}"
else:
    # 默认示例数据（Base64编码的音频片段）
    audio_data = "data:;base64,SUQzBAAAAAAAI1RTU0UAAAAPAAADTGF2ZjU4LjI5...."

# ----------------------------------------------------------------------------
#                              请求头配置
# ----------------------------------------------------------------------------
headers = {
    "Authorization": f"{api_key}",  # 认证信息
    "Content-Type": "application/json"     # 内容类型
}

# ----------------------------------------------------------------------------
#                              请求体构建
# ----------------------------------------------------------------------------
data = {
    # 指定使用的模型
    "model": "qwen3-omni-30b-a3b-captioner",

    # 消息列表
    "messages": [
        {
            "role": "user",
            "content": [
                {
                    "type": "input_audio",      # 音频输入类型
                    "input_audio": {
                        "data": audio_data      # Base64编码的音频数据
                    }
                }
            ]
        }
    ]
}

# ----------------------------------------------------------------------------
#                           发送请求并输出结果
# ----------------------------------------------------------------------------
response = requests.post(url, headers=headers, json=data)
print(response.json())
```

## 📚 阿里官方网站

```
https://help.aliyun.com/zh/model-studio/qwen3-omni-captioner

```

---

<p align="center">

  <small>© 2026 DMXAPI qwen3-omni-30b-a3b-captioner音频理解 </small>

</p>