# Openai 视频模型 Sora2-chat API使用文档
OpenAI 正式发布 Sora 2，称“视频生成进入 ChatGPT 时刻”。新模型可一次性生成 15 秒音视频同步短片，物理真实度与多镜头叙事大幅提升。

::: warning
该模型为 OpenAI 网页版本 sora-2-hd 的 api，固定时长15s/10s，仅供娱乐；无论生成失败还是成功都会被收费，按次收费；介意请勿使用
:::

## 模型名称
`sora-2-hd-15s-chat`    
`sora-2-hd-10s-chat`
## 接口地址
`https://www.dmxapi.cn/v1/chat/completions`

:::tip
可以在提示词中设置视频比例，系统会自动识别！  
例如：`中国街头吃西瓜,生成视频比例9:16`
:::

## Cherry studio 直接使用
选择模型，在聊天界面直接调用
![sora2-chat-insert-image](img\sora2_01.png)


## Python 代码示例

```python
# -*- coding: utf-8 -*-
"""
sora-2-hd-15s-chat 文生视频 / 对话模型流式调用示例

使用前准备
- 安装依赖：pip install requests
- 配置密钥：建议从环境变量或安全配置读取（如 DMX_API_KEY），避免硬编码

关键参数说明
- model：对话模型名称（如 sora-2-hd-15s-chat）
- messages：OpenAI 兼容消息结构 [{role, content}]
- stream：是否启用 SSE 流式输出
- headers：Token 认证，Accept: text/event-stream
"""
import requests
import json

# 端点：DMX API 的 chat completions（OpenAI 兼容）
url = "https://www.dmxapi.cn/v1/chat/completions"

# 请求体参数
payload = {
    "model": "sora-2-hd-15s-chat", #可选"sora-2-hd-10s-chat" 10s模型
    "messages": [
        # 可以在提示词中设置横屏、竖屏、9:16、16:9 等视频比例，系统会自动识别！
        {"role": "user", "content": "中国街头吃西瓜,生成视频比例9:16"} 
    ],
    "stream": True,
}

# 请求头（生产环境请勿硬编码密钥，改为环境变量）
headers = {
    "Authorization": "sk-********************************************",
    "Content-Type": "application/json",
    "Accept": "text/event-stream"
}

def stream_chat():
    """以 SSE 流式方式调用 DMX Chat Completions 并打印增量内容。"""
    try:
        response = requests.post(url, headers=headers, json=payload, stream=True)
    except Exception as e:
        print(f"请求失败: {e}")
        return

    if response.status_code != 200:
        try:
            err = response.json()
            print(json.dumps(err, ensure_ascii=False, indent=2))
        except Exception:
            text = response.text
            if isinstance(text, bytes):
                text = text.decode("utf-8", errors="ignore")
            print(text)
        return

    response.encoding = "utf-8"

    for raw_line in response.iter_lines(decode_unicode=True):
        if not raw_line:
            continue

        line = raw_line.decode("utf-8", errors="ignore").strip() if isinstance(raw_line, bytes) else raw_line.strip()

        data_str = line[len("data:"):].strip() if line.startswith("data:") else line

        if not data_str:
            continue
        if data_str == "[DONE]":
            break

        try:
            obj = json.loads(data_str)
            choices = obj.get("choices", [])
            if choices:
                delta = choices[0].get("delta") or choices[0].get("message") or {}
                text = delta.get("content") or ""
                if text:
                    print(text, end="", flush=True)
        except json.JSONDecodeError:
            print(data_str, end="", flush=True)

    print()

if __name__ == "__main__":
    stream_chat()
```

## 返回示例

```json
{
  "prompt": "中国街头吃西瓜",
  "orientation": "portrait",
  "duration": 15
}
```

> ID: `task_01k8sxz17gewz8kac074xz4crh`  
> [数据预览](https://asyncdata.net/web/task_01k8sxz17gewz8kac074xz4crh) | [原始数据](https://asyncdata.net/source/task_01k8sxz17gewz8kac074xz4crh)  
> 排队中... 生成中.

> 🏃‍ 进度 42..54..67..75..81..

> 生成完成 ✅  
> sid: `s_69030aec68108191a24f05b2089bcb59`

![https://filesystem.site/cdn/20251030/5aad43fd4008074d2074b13d8dd4c9.webp](https://filesystem.site/cdn/20251030/5aad43fd4008074d2074b13d8dd4c9.webp)
[在线播放▶️](https://filesystem.site/cdn/20251030/181a1916dcfe0bb84cafed2427204c.mp4)

<p align="center">
  <small>© 2025 DMXAPI Openai 视...</small>
</p>