# Gemini PDF 内容总结 API 文档

## 📖 功能介绍

通过调用 Gemini API 对 PDF 文档进行智能内容总结,支持多页文档的完整解析和提取。



## 💻 Python 调用示例

```python
"""
PDF 智能总结工具
=================
功能说明：通过调用 DMXAPI Gemini API 对 PDF 文档进行智能内容总结
作者：DMX API Team
"""

import base64
import requests
import json

# ==================== API 配置 ====================
API_URL = "https://www.dmxapi.cn/v1beta/models/gemini-2.5-flash:generateContent"  #DMXAPI Gemini API 端点
API_KEY = "sk-*****************************************"  # 你的 DMXAPI 密钥（请妥善保管）
PDF_PATH = "test/example.pdf"  # 待处理的 PDF 文件路径

def encode_file_to_base64(file_path):
    """
    将文件编码为 Base64 字符串
    
    参数:
        file_path (str): 文件的完整路径
    
    返回:
        str: Base64 编码后的字符串，失败则返回 None
    """
    try:
        # 以二进制模式读取文件内容
        with open(file_path, "rb") as file:
            # 将二进制数据编码为 Base64 并转换为 UTF-8 字符串
            return base64.b64encode(file.read()).decode("utf-8")
    except Exception as e:
        print(f"❌ 文件处理错误: {e}")
        return None

def summarize_pdf():
    """
    调用 DMXAPI Gemini API 总结 PDF 文档内容
    
    流程:
        1. 读取并编码 PDF 文件为 Base64 格式
        2. 构造符合 API 规范的请求数据
        3. 发送 POST 请求并输出结果
    """
    # ==================== 第一步：读取并编码 PDF 文件 ====================
    print("📄 正在读取 PDF 文件...")
    base64_data = encode_file_to_base64(PDF_PATH)
    if not base64_data:
        print("❌ PDF 文件读取失败，程序终止")
        return

    # ==================== 第二步：准备请求数据 ====================
    print("🔧 正在构造 API 请求数据...")
    headers = {
        "Content-Type": "application/json"  # 设置请求头为 JSON 格式
    }
    
    # 构造符合 Gemini API 规范的请求体
    payload = {
        "contents": [{
            "parts": [
                # PDF 文件数据部分（Base64 格式）
                {
                    "inlineData": {
                        "mimeType": "application/pdf",  # 指定文件类型为 PDF
                        "data": base64_data  # Base64 编码的 PDF 数据
                    }
                },
                # 用户提示词部分
                {
                    "text": "请总结这份PDF的核心内容，清晰简洁表达，不要啰嗦。"
                }
            ]
        }]
    }

    # ==================== 第三步：发送请求并处理响应 ====================
    print("🚀 正在调用 Gemini API...")
    try:
        # 发送 POST 请求到 API 端点
        response = requests.post(
            API_URL,
            headers=headers,
            params={"key": API_KEY},  # 通过 URL 参数传递 API 密钥
            json=payload  # 将 payload 序列化为 JSON 并发送
        )
        
        # 检查响应状态，如果不是 2xx 则抛出异常
        response.raise_for_status()
        
        # 格式化输出 API 返回的 JSON 结果
        print("✅ API 调用成功！以下是总结结果：")
        print("=" * 60)
        print(json.dumps(response.json(), indent=2, ensure_ascii=False))
        print("=" * 60)
        
    except requests.exceptions.RequestException as e:
        # 捕获所有请求相关的异常
        print(f"❌ API 请求失败: {e}")
        if e.response:
            # 如果有响应对象，输出详细错误信息
            print(f"📋 错误详情: {e.response.text}")

# ==================== 程序入口 ====================
if __name__ == "__main__":
    print("=" * 60)
    print("📚 PDF 智能总结工具 - 基于 Gemini API")
    print("=" * 60 + "")
    summarize_pdf()
```



## ✅ 返回示例

```json
============================================================
📚 PDF 智能总结工具 - 基于 Gemini API
============================================================
📄 正在读取 PDF 文件...
🔧 正在构造 API 请求数据...
🚀 正在调用 Gemini API...
✅ API 调用成功！以下是总结结果：
============================================================
{
  "candidates": [
    {
      "content": {
        "role": "model",
        "parts": [
          {
            "text": "这份PDF的核心内容是**来自《圣经》箴言书23:4-5节的经文翻译**。该经文警示人们不要过度追求财富，因为财富是短暂的，会像鹰一样飞走。PDF提供了包括英语、俄语、亚美尼亚语、西班牙语、加泰罗尼亚语、法语、德语、简体中文、印地语、葡萄牙语、日语、韩语、意大利语、土耳其语和越南语在内的多种语言版本。"
          }
        ]
      },
      "finishReason": "STOP",
      "index": 0,
      "safetyRatings": []
    }
  ],
  "usageMetadata": {
    "promptTokenCount": 789,
    "candidatesTokenCount": 110,
    "totalTokenCount": 899,
    "thoughtsTokenCount": 0,
    "promptTokensDetails": null
  }
}
============================================================
```



## 🔑 关键参数说明

### API 配置
- **API_URL**: DMXAPI Gemini API 端点地址
- **API_KEY**: 你的 API 密钥（请妥善保管）
- **PDF_PATH**: 待处理的 PDF 文件路径

### 请求参数
- **mimeType**: 文件类型，PDF 文件使用 `application/pdf`
- **data**: Base64 编码的文件数据
- **text**: 用户提示词，指导模型如何处理文档

## ⚠️ 注意事项

1. **文件大小限制**: PDF 文件建议不超过 5 MB，过大的文件会消耗很多很多很多tokens
2. **支持格式**: 仅支持标准 PDF 格式文档
3. **API 密钥安全**: 不要在公开代码中暴露 API 密钥
4. **错误处理**: 建议添加完善的异常处理机制
5. **编码格式**: 确保使用 Base64 编码传输文件数据

## 💡 使用建议

- 对于大型 PDF 文档，建议分页处理
- 可以自定义提示词以获得更精准的总结
- 支持多语言 PDF 文档的内容提取
- 建议在生产环境中添加重试机制

---

<p align="center">
  <small>© 2025 DMXAPI Gemini PDF</small>
</p>