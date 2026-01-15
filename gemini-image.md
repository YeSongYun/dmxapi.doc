# Gemini 本地图片解析

## 📋 概述

该 API 允许用户上传本地图片并获取 AI 生成的详细描述,支持多种图片格式（JPEG、PNG、WEBP、HEIC、HEIF 等）。

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
使用模型：gemini-2.5-flash
================================================================================
"""

import base64
import requests
import json


# ==============================================================================
# 配置参数区域
# ==============================================================================
MODEL = "gemini-2.5-flash"                                      # AI 模型名称
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
        response = requests.post(url, headers=headers, json=payload, stream=False)
        response.raise_for_status()

        full_text = ""
        print("=== 流式响应开始 ===\n")

        # 逐行解析 SSE 格式的响应
        for line in response.iter_lines():
            if line:
                line_str = line.decode('utf-8')

                # SSE 数据行以 "data: " 开头
                if line_str.startswith('data: '):
                    json_str = line_str[6:]                     # 去掉 "data: " 前缀

                    try:
                        data = json.loads(json_str)

                        # 提取响应中的文本内容
                        if 'candidates' in data:
                            for candidate in data['candidates']:
                                if 'content' in candidate and 'parts' in candidate['content']:
                                    for part in candidate['content']['parts']:
                                        if 'text' in part:
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

### 成功响应
```json
=== 流式响应开始 ===

这张照片展示了一个白色的佳能（Canon）计算器，型号是WS-1212H，它放在一个带有蓝色和白色抽象图案的桌垫上。

计算器是白色的，按键是深灰色和红色的。屏幕上方有“Canon”品牌标识和型号“WS-1212H”。屏幕下方有一排功能按钮，包括“MU”、“GT”、“CM”、“RM”、“M±”和“M=”。再往下是数字键（0-9）、小数点键、算术运算符（+、-、×、÷）、百分比键（%±√）、等号键（=）以及清除/开启（ON/CA）和清除/关闭（CI/C）键。其中，“ON/CA”和“CI/C”键是红色的。

计算器右上角有一个小的“12”字样，这可能表示其显示位数。屏幕顶部附近还有一些小开关或指示符，上面写着“5/4”和“+43210F”，这可能是关于小数位数或舍入规则的设置。

背景中可以看到一个米色的物体和一小块浅绿色毛巾状的物品，以及一些线缆。光线似乎从左上方照射过来，在计算器屏幕上造成了一些反光。

=== 流式响应结束 ===

```


## 💻 Python 示例代码（SDK）

```python
"""
=================================================
DMXAPI Gemini 图像分析示例（SDK）
=================================================
模型: gemini-2.5-flash
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
    model='gemini-2.5-flash',
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

### 成功响应
```json
这张图片显示了一台 **Canon (佳能) 品牌的计算器**，型号为 **WS-1212H**。

以下是详细分析：

1.  **主要物体：** 一台桌面计算器。
2.  **品牌与型号：**
    *   品牌：Canon (佳能)
    *   型号：WS-1212H
3.  **颜色与设计：**
    *   计算器主体为浅灰色或白色。
    *   按键颜色主要为深灰色，其中 "ON/CA" 和 "CI/C" 两个按键是红色的，用于强调开关机和清除功能。
    *   按键布局规整，符合标准计算器的设计。
    *   机身边缘圆润。
4.  **显示屏区域：**
    *   上方有一个矩形的大尺寸液晶显示屏，目前是空白的，有反光。
    *   显示屏上方有两个拨动开关和一些小字标识：
        *   左侧的开关旁标有 "5/4 ↓" 和一个箭头，这通常用于设置四舍五入或截取模式。
        *   右侧的开关旁标有 "+43210F" 和一个箭头，这通常用于设置小数点位数。
        *   最右侧有一个数字 "12" 和一个类似电池或显示位数的小图标，表明它可能是一个12位显示的计算器。
5.  **按键功能：**
    *   **基本运算键：** 0-9 数字键、00 键、小数点键 ( . )、加 ( + )、减 ( - )、乘 ( X )、除 ( ÷ )、等于 ( = )。
    *   **内存键：**
        *   MU (Mark-Up)：加价/利润计算。
        *   GT (Grand Total)：总计。
        *   CM (Clear Memory)：清除内存。
        *   RM (Recall Memory)：读取内存。
        *   M± (Memory Plus/Minus)：内存加/减。
        *   M= (Memory Equal)：内存显示或可能是另一个内存减键。
    *   **特殊功能键：**
        *   ON/CA (On / Clear All)：开机/全部清除 (红色)。
        *   CI/C (Clear Entry / Clear)：清除当前输入/清除 (红色)。
        *   %± (Percent / Change Sign)：百分比/正负号转换。
        *   √ (Square Root)：平方根。
        *   一个带有双向箭头的按键 (左侧ON/CA上方)：通常表示货币兑换或汇率功能，对于商用计算器很常见。
6.  **背景环境：**
    *   计算器放置在一个带有蓝色、白色和黄色抽象图案的表面上，这看起来像是一个鼠标垫或桌面垫。
    *   背景右侧有一个浅蓝色的毛巾或布料物体。
    *   背景上方（计算器后面）有一些模糊的物体，包括一根深色数据线和一个金属USB接头。

**总结：**
这是一台功能齐全的佳能WS-1212H型号桌面计算器，具有标准的算术功能、内存功能、利润计算、百分比、平方根以及小数点和舍入设置等高级功能，甚至可能包含货币兑换功能，适合办公或商务使用。它放置在一个色彩鲜明的桌面垫上。
```


## ⚠️ 注意事项

- 请妥善保管您的 API 密钥,不要将其暴露在公开代码中
- API 请求需要稳定的网络连接
- 建议在生产环境中添加重试机制和错误处理
- 注意监控 token 使用量以控制成本

---

<p align="center">
  <small>© 2025 DMXAPI Gemini图片分析</small>
</p>