# Gemini 本地图片解析

## 📋 概述

本示例使用 `gemini-3.8-flash` 分析本地图片，分别演示 REST 流式响应和 Google GenAI SDK 调用。示例使用 JPEG；更换图片格式时请同步修改 MIME 类型。
## 🌐 请求地址
| 服务类型 | 接口地址 | 说明 |
|---------|---------|------|
|图片解析 | `https://www.dmxapi.cn` |SDK |
|图片解析 | `https://www.dmxapi.cn/v1beta` ||


## 💻 Python 示例代码

```python
"""
================================================================================
                    DMXAPI Gemini 图像分析示例（流式版本）
================================================================================
功能说明：
    使用 Google Gemini API 对本地图片进行智能分析
    支持流式响应，实时获取分析结果

API 提供商：DMXAPI
使用模型：gemini-3.8-flash
================================================================================
"""

import base64
import requests
import json


# ==============================================================================
# 配置参数区域
# ==============================================================================
MODEL = "gemini-3.8-flash"                                      # AI 模型名称
API_KEY = "sk-******************************************"       # API 密钥
BASE_URL = "https://www.dmxapi.cn/v1beta"                       # DMXAPI 基础地址

# 默认参数配置
DEFAULT_IMAGE_PATH = "test/example.jpg"                         # 默认图片路径
DEFAULT_PROMPT = "形容一下图片内容"                                # 默认提示词


# ==============================================================================
# 工具函数：图片编码
# ==============================================================================
def encode_image_to_base64(image_path):
    """
    将图片文件转换为 base64 编码字符串

    参数:
        image_path (str): 图片文件的路径

    返回:
        str: base64 编码的图片字符串
    """
    with open(image_path, 'rb') as image_file:
        image_data = image_file.read()
        encoded_string = base64.b64encode(image_data).decode('utf-8')
    return encoded_string


# ==============================================================================
# 主功能函数：调用 Gemini API
# ==============================================================================
def call_gemini_api_stream(image_path=DEFAULT_IMAGE_PATH, prompt_text=DEFAULT_PROMPT):
    """
    调用 Gemini API 进行流式图片分析

    参数:
        image_path (str, optional): 图片文件路径，默认使用 DEFAULT_IMAGE_PATH
        prompt_text (str, optional): 提示文本，默认使用 DEFAULT_PROMPT

    返回:
        dict: 包含完整响应文本的字典 {'full_text': str}
        None: 当请求发生错误时返回 None
    """

    # --------------------------------------------------------------------------
    # 步骤 1: 构建 API 请求 URL
    # --------------------------------------------------------------------------
    url = f"{BASE_URL}/models/{MODEL}:streamGenerateContent?key={API_KEY}&alt=sse"

    # --------------------------------------------------------------------------
    # 步骤 2: 编码图片为 base64
    # --------------------------------------------------------------------------
    image_base64 = encode_image_to_base64(image_path)

    # --------------------------------------------------------------------------
    # 步骤 3: 构造请求头和请求体
    # --------------------------------------------------------------------------
    headers = {
        "Content-Type": "application/json"
    }

    payload = {
        "contents": [{
            "parts": [
                {
                    "inline_data": {
                        "mime_type": "image/jpeg",              # 图片 MIME 类型
                        "data": image_base64                    # base64 编码的图片数据
                    }
                },
                {"text": prompt_text}                           # 分析提示词
            ]
        }]
    }

    # --------------------------------------------------------------------------
    # 步骤 4: 发送请求并处理流式响应
    # --------------------------------------------------------------------------
    try:
        response = requests.post(url, headers=headers, json=payload, stream=True, timeout=(10, 120))
        response.raise_for_status()

        full_text = ""
        print("=== 流式响应开始 ===\n")

        # 逐行解析 SSE 格式的响应
        for line in response.iter_lines():
            if line:
                line_str = line.decode('utf-8')

                # SSE 冒号后的空格可省略
                if line_str.startswith('data:'):
                    json_str = line_str[5:].strip()

                    try:
                        data = json.loads(json_str)

                        # 提取响应中的文本内容
                        if 'candidates' in data:
                            for candidate in data['candidates']:
                                if 'content' in candidate and 'parts' in candidate['content']:
                                    for part in candidate['content']['parts']:
                                        if 'text' in part and not part.get('thought'):
                                            text_chunk = part['text']
                                            print(text_chunk, end='', flush=True)
                                            full_text += text_chunk

                    except json.JSONDecodeError:
                        continue                                # 跳过无法解析的行

        print("\n\n=== 流式响应结束 ===")
        return {"full_text": full_text}

    except requests.exceptions.RequestException as e:
        print(f"请求错误: {e}")
        return None

    except Exception as e:
        print(f"发生错误: {e}")
        return None


# ==============================================================================
# 主程序入口
# ==============================================================================
if __name__ == "__main__":
    # 调用 API 进行图片分析（使用默认配置）
    result = call_gemini_api_stream()

    # 输出最终结果统计
    if result:
        print(f"\n\n✓ 分析完成！完整响应文本长度: {len(result['full_text'])} 字符")
    else:
        print("\n✗ API 调用失败")

```
## 📤 返回示例

```text
这是一张背景为白色的简洁图形测试图片，主要包含以下内容：

1. **文字部分**：
   * 左上角有一行黑色无衬线的大写英文字母：**“DMXAPI TEST”**。

2. **图形部分**：
   * 画面中央从左到右水平并列排布着三个色彩鲜明的基础几何图形：
     * **左侧**：一个纯**红色**的圆形。
     * **中间**：一个纯**蓝色**的正方形。
     * **右侧**：一个纯**绿色**、顶点朝上的三角形。

整体画面风格极简，三个图形分别对应了红、绿、蓝（RGB）三种经典基色，看起来像是一个用于程序、显示或API接口的色彩与图形渲染测试用例。
```
## 💻 Python 示例代码（SDK）

```python
"""
=================================================
DMXAPI Gemini 图像分析示例（SDK）
=================================================
模型: gemini-3.8-flash
=================================================
"""

from google import genai
from google.genai import types

# ============================================
# 1. 加载图片文件
# ============================================
with open('test/example.jpg', 'rb') as f:
    image_bytes = f.read()

# ============================================
# 2. 配置DMXAPI连接
# ============================================
api_key = "sk-******************************************"  # 使用在DMXAPI官网获取的令牌
BASE_URL = "https://www.dmxapi.cn"  # DMXAPI 基础地址

# 初始化 Gemini 客户端
client = genai.Client(
    api_key=api_key,
    http_options={'base_url': BASE_URL}
)

# ============================================
# 3. 调用 Gemini API 分析图片
# ============================================
response = client.models.generate_content(
    model='gemini-3.8-flash',
    contents=[
        # 将图片转换为 API 可接受的格式
        types.Part.from_bytes(
            data=image_bytes,
            mime_type='image/jpeg',
        ),
        # 分析指令
        '帮我分析一下这个图片'
    ]
)

# ============================================
# 4. 输出分析结果
# ============================================
print(response.text)

```



## 📤 返回示例

```text
这张图片是一个非常简洁的标准测试图（Test Pattern），整体包含以下几个维度的信息：

---

### 1. 元素组成与视觉特征
* **文字标识（左上角）：**
  * 内容为黑色的英文 **`DMXAPI TEST`**。
  * 表明该图主要用于某种名为“DMXAPI”的接口、程序或系统的功能测试。
* **主体图形（从左至右）：**
  1. **红色圆形**（Red Circle）：纯红色，代表色彩通道中的 **R（红）**。
  2. **蓝色正方形**（Blue Square）：纯蓝色，代表色彩通道中的 **B（蓝）**。
  3. **绿色三角形**（Green Triangle）：纯绿色，代表色彩通道中的 **G（绿）**。
* **背景：** 纯白色平底，高对比度。

---

### 2. 深层含义与专业用途推测

根据图片中的信息，这极可能是一张用于**开发测试**的基准图，常见应用场景包括：

1. **RGB 三原色与显示测试：**
   * 三个图形分别对应数字图像处理和显示系统中最基础的 **RGB（红、绿、蓝）** 三通道。通常用于检测显示设备、视频流或渲染引擎是否存在偏色、通道错位或黑白电平异常。
2. **DMX 协议 / 灯光与显示控制系统测试：**
   * 文字中的 **DMX** 通常指 **DMX512** 协议（广泛用于舞台灯光、LED大屏控制的工业通信标准）。
   * 该图可能是某个控制 LED 矩阵屏、舞台渲染引擎或视频控制台的 API（DMXAPI）在进行功能联调时生成的测试帧（例如分别测试红色、蓝色、绿色通道的映射是否正常）。
3. **图像识别与计算机视觉（CV）算法基准测试：**
   * 包含三种最基础的几何形状（圆、矩形/正方形、三角形）和三种高饱和度原色。常用于机器视觉入门教学或自动化测试中，用以验证轮廓检测、几何形状分类及颜色阈值分割算法。
4. **抗锯齿与渲染保真度测试：**
   * 圆形（曲率测试）、正方形（横平竖直像素对齐）、三角形（斜线抗锯齿/边缘虚化测试）。

---

### 总结
这是一张用于验证图形渲染、色彩映射或 **DMX 相关控制接口**正确性的**合成测试图片**。其特点是结构简单、颜色饱和、特征明确，便于程序做断言验证或肉眼快速排查显示/控制故障。
```


## ⚠️ 注意事项

- 请妥善保管您的 API 密钥,不要将其暴露在公开代码中
- API 请求需要稳定的网络连接
- 建议在生产环境中添加重试机制和错误处理
- 注意监控 token 使用量以控制成本

---

<p align="center">
  <small>© 2026 DMXAPI Gemini图片分析</small>
</p>