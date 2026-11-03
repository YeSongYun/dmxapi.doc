# Gemini 网络视频分析

## 📋 概述

本示例通过 DMXAPI 调用 `gemini-3.8-flash`，使用 `fileData.fileUri` 传入网络视频地址。客户端无需下载视频，服务端需要能够访问该直链；实际支持情况取决于当前模型通道和媒体来源。

运行前安装 `requests`（`pip install requests`），填写 DMXAPI 密钥，并确认 `VIDEO_URL` 可公开访问。

## 🌐 请求地址

| 服务类型 | 接口地址 | 说明 |
|---------|---------|------|
| 视频分析 | `https://www.dmxapi.cn/v1beta` | REST API |

```
https://www.dmxapi.cn/v1beta/models/{model}:generateContent
```

## 💻 Python 示例代码

```python
"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                   Gemini 视频分析 - REST API 方式（网络视频）                    ║
╠══════════════════════════════════════════════════════════════════════════════╣
║  功能说明：调用 Gemini 模型分析网络视频（通过 fileUri 传入视频地址）              ║
║  API 提供商：DMXAPI                                                           ║
║  模型版本：gemini-3.8-flash                                                   ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""
import requests
import json

# ═══════════════════════════════════════════════════════════════════════════════
# 📋 配置参数
# ═══════════════════════════════════════════════════════════════════════════════
API_KEY = "sk-**************************************************"          # DMXAPI 访问令牌
BASE_URL = "https://www.dmxapi.cn/v1beta"                               # API 基础地址
MODEL = "gemini-3.8-flash"                                             # Gemini 模型版本
VIDEO_URL = "https://doc.dmxapi.cn/0_fenxiang/aa.mp4"                   # 待分析视频 URL（网络地址）
PROMPT = "分析视频内容"                                            # 分析提示词


# ═══════════════════════════════════════════════════════════════════════════════
# 🔧 工具函数
# ═══════════════════════════════════════════════════════════════════════════════
def analyze_video(video_url, prompt=PROMPT):
    """
    调用 Gemini API 分析网络视频内容

    参数:
        video_url (str): 视频的网络地址（fileUri）
        prompt (str): 分析提示词，默认为 PROMPT

    返回:
        dict: API 返回的 JSON 响应，包含分析结果

    异常:
        requests.exceptions.RequestException: API 请求失败时抛出
    """
    # 构建完整的 API 端点 URL
    api_url = f"{BASE_URL}/models/{MODEL}:generateContent"

    # 设置请求头（使用 Token 认证）
    headers = {
        "Authorization": f"{API_KEY}",
        "Content-Type": "application/json"
    }

    # 构建请求负载（符合 Gemini API 规范，使用 fileData 引用网络视频，无需下载到本地）
    payload = {
        "contents": [
            {
                "role": "user",
                "parts": [
                    {
                        "fileData": {
                            "mimeType": "video/mp4",
                            "fileUri": video_url
                        }
                    },
                    {"text": prompt}
                ]
            }
        ]
    }

    # 发送 POST 请求并返回结果
    response = requests.post(api_url, headers=headers, data=json.dumps(payload), timeout=60)
    response.raise_for_status()
    return response.json()


# ═══════════════════════════════════════════════════════════════════════════════
# 🚀 主程序入口
# ═══════════════════════════════════════════════════════════════════════════════
if __name__ == "__main__":
    try:
        print(f"🎬 正在分析视频: {VIDEO_URL}\n")

        # ────────────────────────────────────────────────────────────────────────
        # 步骤 1: 调用 Gemini API 进行视频分析
        # ────────────────────────────────────────────────────────────────────────
        print("[1/1] 🔄 正在分析...\n")
        result = analyze_video(VIDEO_URL, prompt=PROMPT)

        # ────────────────────────────────────────────────────────────────────────
        # 输出分析结果
        # ────────────────────────────────────────────────────────────────────────
        print("╔" + "═" * 68 + "╗")
        print("║" + " " * 24 + "📊 分析结果" + " " * 32 + "║")
        print("╠" + "═" * 68 + "╣")

        if 'candidates' in result and result['candidates']:
            # 提取并输出 AI 生成的文本内容
            for part in result['candidates'][0].get('content', {}).get('parts', []):
                if 'text' in part:
                    # 格式化输出文本（按行拆分，避免破坏边框排版）
                    text_lines = part['text'].split('\n')
                    for line in text_lines:
                        print(f"║ {line}")
        else:
            print(f"║ ⚠️  未获取到结果: {result}")

        print("╚" + "═" * 68 + "╝")

    except requests.exceptions.RequestException as e:
        print(f"\n❌ 网络请求失败: {e}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"   状态码  : {e.response.status_code}")
            print(f"   响应内容: {e.response.text}")
    except Exception as e:
        print(f"\n❌ 错误: {e}")
```

## 📤 返回示例

以下为 **2026-11-03** 使用 `gemini-3.8-flash` 分析代码中视频地址的实测回答正文（HTTP 200），对应[测试记录](/reports/gemini-3.8-flash-2026-11-03/results.json)中的 `gemini-video1-1`。已去除控制台进度提示和装饰边框。

### 成功响应

```text
这段视频是一个结合了**漫威《复仇者联盟》元素**与**AI数字人/图像生成技术**的创意宣传短片。具体内容分析如下：

1. **核心内容与流程**：
   - **00:00 - 00:01**：展示电影《复仇者联盟4：终局之战》的官方中文海报，奠定主题背景。
   - **00:01 - 00:03**：展示AI生成的**美国队长与黑寡妇**全身形象，配音：“我们准备好了，为了正义。”
   - **00:03 - 00:04**：展示AI生成的**雷神索尔**特写（周身有闪电特效，手持雷神之锤），配音：“风暴即将降临。”
   - **00:04 - 00:06**：展示AI生成的**黑寡妇**面部特写，耳侧带有发光高科技装置，配合唇形同步说话，台词：“没有退路。”
   - **00:06 - 00:09**：展示一张以复联角色为原型的重绘宣传海报，上方带有大号文字标识 **“DMXAPI”**，配音提示：“启动协议，DMXAPI”。

2. **制作与表现手法**：
   - **AI绘画/生图**：视频中的人物角色（美队、雷神、黑寡妇）采用了逼真的AI重绘风格，还原了漫威电影角色的经典特征。
   - **动态与唇形同步**：对静态人像进行了面部微动态与开口说话处理（AI动态人像技术）。
   - **配音与音效**：配有英雄集结氛围的中文配音，增强了紧张激昂的氛围感。

3. **目的与主题**：
   视频整体属于一次**科技/平台（DMXAPI）的宣传推广**，借助高知名度的超级英雄IP与AI生成视觉效果来吸引观众注意。
```

## ⚙️ 参数说明

| 参数 | 类型 | 说明 |
|------|------|------|
| `MODEL` | string | Gemini 模型版本，本示例为 `gemini-3.8-flash` |
| `VIDEO_URL` | string | 视频的网络地址，通过 `fileData.fileUri` 传入 |
| `mimeType` | string | 视频的 MIME 类型，如 `video/mp4` |
| `PROMPT` | string | 分析提示词，用于指定分析任务 |

## ⚠️ 注意事项

- 网络视频方式通过 `fileData.fileUri` 直接引用视频地址，无需将视频下载并 base64 编码，适合体积较大的视频
- 请确保 `VIDEO_URL` 为可公开访问的直链地址，且与 `mimeType` 一致
- 请妥善保管您的 API 密钥，不要将其暴露在公开代码中
- API 请求需要稳定的网络连接，视频较大时建议适当调大 `timeout`
- 建议在生产环境中添加重试机制和错误处理

---

<p align="center">
  <small>© 2026 DMXAPI Gemini 网络视频分析</small>
</p>
