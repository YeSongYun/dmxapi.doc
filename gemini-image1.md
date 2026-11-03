# Gemini 网络图片解析

## 📋 概述

本示例使用 `gemini-3.8-flash` 分析网络图片。代码先下载图片，再通过内联图片数据发送给模型；REST 和 SDK 示例均使用 JPEG 图片。

运行前安装依赖（`pip install requests google-genai`），填写 DMXAPI 密钥，并确保图片 URL 可访问。

## 🌐 请求地址

| 服务类型 | 接口地址 | 说明 |
|---------|---------|------|
|图片解析 | `https://www.dmxapi.cn` |SDK |
|图片解析 | `https://www.dmxapi.cn/v1beta` ||



## 💻 Python 示例代码

```python
"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                   Gemini 图片分析 - REST API 方式                             ║
╠══════════════════════════════════════════════════════════════════════════════╣
║  功能说明：调用 Gemini 模型分析网络图片                                         ║
║  API 提供商：DMXAPI                                                           ║
║  模型版本：Gemini 3.8 Flash                                                   ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""
import requests
import base64

# ═══════════════════════════════════════════════════════════════════════════════
# 📋 配置参数
# ═══════════════════════════════════════════════════════════════════════════════
GEMINI_API_KEY = "sk-**************************************************"  # DMXAPI 访问令牌
BASE_URL = "https://www.dmxapi.cn/v1beta"                               # API 基础地址
IMG_URL = "https://goo.gle/instrument-img"                            # 待分析 JPEG 图片 URL
MODEL = "gemini-3.8-flash"                                            # Gemini 模型版本

# ═══════════════════════════════════════════════════════════════════════════════
# 🔧 工具函数
# ═══════════════════════════════════════════════════════════════════════════════

HEADERS = {"User-Agent": "Mozilla/5.0"}


def get_image_mime_type(url):
    try:
        response = requests.head(url, headers=HEADERS, allow_redirects=True, timeout=10)
        mime_type = response.headers.get('Content-Type', '')
        if mime_type and mime_type.startswith('image/'):
            return mime_type.split(';')[0].strip()
    except Exception as e:
        print(f"⚠️  警告: 无法获取 MIME 类型 - {e}")
    return "image/jpeg"


def download_and_encode_image(url):
    response = requests.get(url, headers=HEADERS, timeout=10)
    response.raise_for_status()
    return base64.b64encode(response.content).decode('utf-8')


def analyze_image(image_b64, mime_type, prompt="Caption this image."):
    """
    调用 Gemini API 分析图片内容

    参数:
        image_b64 (str): base64 编码的图片数据
        mime_type (str): 图片的 MIME 类型
        prompt (str): 分析提示词，默认为 "Caption this image."

    返回:
        dict: API 返回的 JSON 响应，包含分析结果

    异常:
        requests.exceptions.RequestException: API 请求失败时抛出
    """
    # 构建完整的 API 端点 URL
    api_url = f"{BASE_URL}/models/{MODEL}:generateContent"

    # 设置请求头（使用 Token 认证）
    headers = {
        "Authorization": f"{GEMINI_API_KEY}",
        "Content-Type": "application/json"
    }

    # 构建请求负载（符合 Gemini API 规范）
    payload = {
        "contents": [{
            "parts": [
                {"inline_data": {"mime_type": mime_type, "data": image_b64}},
                {"text": prompt}
            ]
        }]
    }

    # 发送 POST 请求并返回结果
    response = requests.post(api_url, headers=headers, json=payload, timeout=30)
    response.raise_for_status()
    return response.json()


# ═══════════════════════════════════════════════════════════════════════════════
# 🚀 主程序入口
# ═══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    try:
        print(f"📸 正在分析图片: {IMG_URL}\n")

        # ────────────────────────────────────────────────────────────────────────
        # 步骤 1: 获取图片 MIME 类型
        # ────────────────────────────────────────────────────────────────────────
        mime_type = get_image_mime_type(IMG_URL)
        print(f"[1/3] ✓ MIME 类型: {mime_type}")

        # ────────────────────────────────────────────────────────────────────────
        # 步骤 2: 下载图片并进行 base64 编码
        # ────────────────────────────────────────────────────────────────────────
        image_b64 = download_and_encode_image(IMG_URL)
        print(f"[2/3] ✓ 图片编码完成 ({len(image_b64)} 字符)")

        # ────────────────────────────────────────────────────────────────────────
        # 步骤 3: 调用 Gemini API 进行图片分析
        # ────────────────────────────────────────────────────────────────────────
        print(f"[3/3] 🔄 正在分析...\n")
        result = analyze_image(image_b64, mime_type, prompt="解释这个图片的具体内容")

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
                    # 格式化输出文本
                    text_lines = part['text'].split('\n')
                    for line in text_lines:
                        print(f"║ {line}")
        else:
            print(f"║ ⚠️  未获取到结果: {result}")

        print("╚" + "═" * 68 + "╝")

    except requests.exceptions.RequestException as e:
        print(f"\n❌ 网络请求失败: {e}")
    except Exception as e:
        print(f"\n❌ 错误: {e}")

```
## 📤 返回示例

以下为 2026-11-03 REST 实测结果（已移除进度信息和边框），测试 ID：`gemini-image1-1`，HTTP 200。输入图片：`https://goo.gle/instrument-img`。测试记录：[results.json](/reports/gemini-3.8-flash-2026-11-03/results.json)。

### 实测回答正文
```text
这张图片展示的是一台极其庞大且精密的**大型管风琴（或高级电子/数字管风琴）的演奏台（Console）**。

其各个核心组成部分的具体功能如下：

---

### 1. 手键盘（Manuals）
* 中央由下至上叠放了 **4层手键盘**（四排手键）。
* 不同的键盘通常控制管风琴中不同特性的音管群（如主琴音栓组 Great、独奏音栓组 Solo、强弱音栓组 Swell、伴奏音栓组 Choir 等），让演奏者能双手在不同声部和音色之间快速切换。

---

### 2. 音栓片（Stop Tabs / Tilting Tablets）
* 键盘上方及左右两侧像机翼般展开的弧形面板上，密密麻麻排列着数百个可上下拨动的**音栓翻牌（Stop Tabs）**。
* **功能**：每个音栓代表一种特定的乐器音色（如笛管、簧管、弦乐声部、全合奏混合音栓等）或特定的脚度（音高，如 16'、8'、4'、2' 等）。黑色的翻牌通常是“音栓耦合器（Couplers）”，用于将不同键盘的音色连接联动。

---

### 3. 手栓预设按钮（Thumb Pistons）
* 位于每层手键盘正下方的木框上，排列着一排排白色圆形小按钮。
* **功能**：演奏者可以在不中断弹奏的情况下，用拇指迅速触按这些按钮，一键切换提前编排好的音色组合（预设）。

---

### 4. 脚键盘（Pedalboard）
* 位于演奏台底部，是由木板条排列制成的放射状凹面踏板系统。
* **功能**：供演奏者用双脚（鞋底和鞋跟）弹奏管风琴的低音声部（Bass）。

---

### 5. 表情踏板与渐强踏板（Expression & Crescendo Pedals）
* 位于脚键盘上方中央的凹槽内，排列着 **4个踏板**。
* **功能**：通常用于脚踩控制不同百叶窗式声箱的开合，从而改变特定声部的音量大小（如 Swell / Choir / Solo 表情踏板）；最右侧通常为渐强踏板（Crescendo Pedal），随着踩下角度逐渐增加启用的音栓数量，产生由弱到强的宏大效果。

---

### 6. 脚栓按键（Toe Studs）
* 分布在表情踏板两侧及下方的球形黄铜金属凸起按钮。
* **功能**：与键盘下方的拇指按钮类似，供演奏者在弹奏过程中用脚尖快速触发音栓预设组合，无需腾出手来。

---

### 总结
这种采用弧形机翼排列（Horseshoe/Curved layout）并配备音栓翻牌的设计，在美式交响管风琴、大型定制管风琴或现代化高级数字管风琴（如 Allen、Rodgers、Walker 等品牌）中非常典型，旨在让一位演奏者能在人体工程学合理的范围内操控数以千计的管风琴音管声响。
```

## 💻 Python 示例代码（SDK）

```python
"""
Gemini 图片分析示例
=====================
使用DMXAPI 代理服务分析网络图片内容
功能说明:
- 从网络 URL 下载图片
- 使用 Gemini 3.8 Flash 模型分析图片内容
- 通过 DMXAPI 代理访问 Gemini API
"""
from google import genai
from google.genai import types
import requests

# ============================================================================
# 配置部分
# ============================================================================

# DMXAPI 配置信息
api_key = "sk-*****************************"  # 使用在DMXAPI官网获取的令牌
BASE_URL = "https://www.dmxapi.cn"  # DMXAPI 基础地址

# ============================================================================
# 图片准备
# ============================================================================

# 图片来源 URL
image_path = "https://goo.gle/instrument-img"  #(可换成自己图片的url图片地址)

# 下载图片并获取字节数据
image_response = requests.get(image_path, timeout=30)
image_response.raise_for_status()
image_bytes = image_response.content

# 将图片字节转换为 Gemini API 所需的 Part 对象
image = types.Part.from_bytes(
    data=image_bytes,
    mime_type="image/jpeg"
)

# ============================================================================
# 初始化 Gemini 客户端
# ============================================================================

# 创建 Gemini 客户端，配置使用 DMXAPI 代理
client = genai.Client(
    api_key=api_key,
    http_options={'base_url': BASE_URL}
)

# ============================================================================
# 图片分析
# ============================================================================

# 调用 Gemini 3.8 Flash 模型分析图片
# contents 参数包含提示词和图片对象
response = client.models.generate_content(
    model="gemini-3.8-flash",
    contents=["解释这个图片的具体内容", image],
)

# ============================================================================
# 输出结果
# ============================================================================

# 打印 AI 生成的图片分析结果
print(response.text)

```

## 📤 返回示例

以下为 2026-11-03 SDK 实测结果，测试 ID：`gemini-image1-2`，HTTP 200。输入图片：`https://goo.gle/instrument-img`。测试记录：[results.json](/reports/gemini-3.8-flash-2026-11-03/results.json)。

### 实测回答正文
```text
这张图片展示的是一台极其庞大且复杂的**大型管风琴演奏台（Pipe Organ Console）**。管风琴被称为“乐器之王”，而演奏台是演奏家控制整座庞大管风琴发声的核心控制中心。

以下是该演奏台各主要部件的具体解析：

### 1. 手键盘（Manuals）
* **层数**：中央叠放着 **4层手键盘**（从下往上通常对应主音栓键盘 Great、合唱键盘 Choir/Positive、膨胀键盘 Swell、独奏键盘 Solo 等不同分部）。
* **作用**：演奏家双手弹奏这些键盘，每一层键盘控制不同音色区域的管风琴发声管。

### 2. 舌片式音栓区（Stop Tabs / Tilting Tablets）
* **分布**：位于键盘左右两侧呈弧形展开的翼板（Stop Jambs）以及最上方的控制条上。
* **外观**：采用了密密麻麻的白色与少量黑色“翻转式小拨片”（舌片音栓），数量有数百个。
* **作用**：每个小片代表一组特定音色的风管（Rank）或音栓联动（Coupler）。按下它们即可开启或关闭对应的音色（如笛音、弦音、簧片音、小号音等）。

### 3. 脚键盘 / 踏板（Pedalboard）
* **结构**：底部是一个扇形分布、略带弧度下凹的木质大型脚键盘（标准辐射凹面脚踏板，Radiating Concave Pedalboard）。
* **作用**：由演奏家双脚（鞋底和鞋跟）踩踏，主要负责演奏极低沉雄厚的低音部（Pedal Division）。

### 4. 表情踏板与渐强踏板（Expression & Crescendo Pedals）
* **位置**：位于脚键盘正上方、内嵌在木质琴体内的 **4个深灰色倾斜踏板**。
* **作用**：
  * 前几个通常是**表情踏板**（Swell Pedals），通过控制百叶窗开合来调节特定分部音量的大小。
  * 最右侧通常是**渐强踏板**（Crescendo Pedal），踩下时会按预设顺序自动增加音栓，使声音从极弱逐渐达到雷鸣般的极强。

### 5. 音色预设按钮（Pistons & Toe Studs）
* **拇指活塞（Thumb Pistons）**：在每层键盘下方排列的白色小圆形按钮，供双手弹奏时快速切换预设的音色组合。
* **脚活塞（Toe Studs）**：在脚踏板上方两侧排布的金黄色金属球形按钮，供脚部在弹奏时踢动，用于切换低音或全局预设。

---

**总结**：
这是一座采用精致橡木（或类似硬木）打造的高规格管风琴控制台，其左右展开的环抱式设计是为了符合人体工程学，方便演奏家在演奏中触及数以百计的音栓控制器。这类规模的管风琴通常安装于大型天主教堂、基督重大教堂或国家级音乐厅中。
```

## ⚠️ 注意事项

- 请妥善保管您的 API 密钥,不要将其暴露在公开代码中
- API 请求需要稳定的网络连接
- 建议在生产环境中添加重试机制和错误处理
- 注意监控 token 使用量以控制成本

---

<p align="center">
  <small>© 2026 DMXAPI Gemini网络图片分析</small>
</p>