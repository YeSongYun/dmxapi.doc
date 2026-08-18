# Openai Responses 本地图片分析 API 文档

## 📋 概述

该 API 允许用户上传本地图片并获取 AI 生成的详细描述,支持多种图片格式（JPG、PNG、GIF、WebP 等）。



## 🔗 请求地址

```
https://www.dmxapi.cn/v1/responses
```

---

## 💻 Python 示例代码

### 📝 代码说明

本示例展示了如何使用 Python 调用 DMXAPI 进行本地图片分析：

1. **图片编码**：将本地图片转换为 Base64 格式
2. **构造请求**：组装 API 请求参数
3. **发送请求**：调用 API 并获取响应
4. **解析结果**：提取并显示 AI 生成的图片描述

### 完整可运行示例

```python
"""
DMXAPI 图片识别示例脚本
================================
本脚本演示如何使用 DMXAPI 的视觉模型来分析和描述图片内容
功能：将本地图片编码为 Base64 格式，然后发送到 API 进行内容识别

作者：DMXAPI 团队
"""

import base64
import json
import os
import requests

# ========================================
# 配置参数
# ========================================
API_KEY = "sk-****************************"  # 替换为你的 DMXAPI 令牌
IMAGE_PATH = "test/example.jpg"  # 本地图片路径

# ========================================
# 图片编码函数
# ========================================
def encode_image_to_base64(filepath):
    """
    将图片编码为 Base64 数据 URI 格式
    
    该函数读取本地图片文件，将其转换为 Base64 编码的数据 URI，
    这是一种可以直接嵌入到 JSON 或 HTML 中的图片表示格式。
    
    参数说明：
        filepath (str): 图片文件的本地路径
        
    返回值：
        str: 格式为 "data:image/jpeg;base64,..." 的完整数据 URI 字符串
        
    示例：
        >>> encode_image_to_base64("example.jpg")
        'data:image/jpeg;base64,/9j/4AAQSkZJRgABAQEA...'
    """
    # 获取文件扩展名并转换为小写（如 ".jpg", ".png"）
    ext = os.path.splitext(filepath)[1].lower()
    
    # 定义文件扩展名到 MIME 类型的映射表
    # MIME 类型用于标识数据的格式，浏览器和 API 依赖此信息正确处理图片
    mime_map = {
        '.jpg': 'image/jpeg',
        '.jpeg': 'image/jpeg',
        '.png': 'image/png',
        '.gif': 'image/gif',
        '.webp': 'image/webp'
    }
    
    # 根据扩展名获取对应的 MIME 类型，未知格式使用通用二进制类型
    mime_type = mime_map.get(ext, 'application/octet-stream')
    
    # 以二进制模式读取图片文件
    with open(filepath, "rb") as f:
        # 执行编码流程：
        # 1. f.read() - 读取文件的所有二进制数据
        # 2. base64.b64encode() - 将二进制数据编码为 Base64
        # 3. .decode('utf-8') - 将 Base64 字节串转换为 UTF-8 字符串
        # 4. f"data:{mime_type};base64,..." - 构造符合标准的数据 URI
        return f"data:{mime_type};base64,{base64.b64encode(f.read()).decode('utf-8')}"


# ========================================
# 主程序入口
# ========================================
if __name__ == "__main__":
    print("=" * 60)
    print("DMXAPI 图片识别示例程序")
    print("=" * 60)
    
    # ----------------------------------------
    # 步骤 1: 图片编码
    # ----------------------------------------
    print("[步骤 1/3] 正在编码图片...")
    print(f"图片路径: {IMAGE_PATH}")
    image_data = encode_image_to_base64(IMAGE_PATH)
    print(f"✓ 编码成功，数据长度: {len(image_data)} 字符")
    
    # ----------------------------------------
    # 步骤 2: 构造 API 请求
    # ----------------------------------------
    print("[步骤 2/3] 正在构造 API 请求...")
    
    # 设置 HTTP 请求头
    # Content-Type: 告诉服务器我们发送的是 JSON 格式数据
    # Authorization: 包含 API 密钥，用于身份验证和授权
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"{API_KEY}"
    }
    
    # 构造请求载荷（Payload）
    # 这是发送给 API 的核心数据，包含模型选择和输入内容
    payload = {
        "model": "gpt-5-mini",  # 使用 GPT-5-Mini 视觉模型
        "input": [{
            "role": "user",  # 消息角色：user（用户）、assistant（助手）、system（系统）
            "content": [
                # 文本输入：告诉模型我们想要什么
                {"type": "input_text", "text": "描述这张图片"},
                # 图片输入：Base64 编码的图片数据
                {"type": "input_image", "image_url": image_data}
            ]
        }]
    }
    print("✓ 请求构造完成")
    
    # ----------------------------------------
    # 步骤 3: 发送请求并处理响应
    # ----------------------------------------
    print("\n[步骤 3/3] 正在发送请求到 DMXAPI...")
    
    try:
        # 发送 POST 请求到 DMXAPI 端点
        # requests.post() 会自动处理 JSON 序列化和 HTTP 连接
        response = requests.post(
            "https://www.dmxapi.cn/v1/responses",  # DMXAPI 的响应式端点
            headers=headers,                        # 包含授权信息的请求头
            json=payload                           # 自动序列化为 JSON 的请求体
        )
        
        # 检查 HTTP 状态码
        # 如果状态码不是 2xx（成功），raise_for_status() 会抛出异常
        response.raise_for_status()
        print("✓ 请求发送成功")
        
        # ----------------------------------------
        # 解析 API 响应
        # ----------------------------------------
        print("\n正在解析 API 响应...")
        result = response.json()  # 将响应体解析为 Python 字典
        
        # 打印完整响应用于调试
        # indent=2 使输出格式化，ensure_ascii=False 保留中文字符
        print("\n" + "=" * 60)
        print("完整 API 响应:")
        print("=" * 60)
        print(json.dumps(result, indent=2, ensure_ascii=False))
        print("=" * 60)
        
        # ----------------------------------------
        # 检查处理状态
        # ----------------------------------------
        if result.get("status") == "completed":
            print("\n✓ 请求处理完成，正在提取结果...")
            
            # ----------------------------------------
            # 提取输出内容
            # ----------------------------------------
            # API 响应的 output 字段包含模型的输出结果
            output = result.get("output", [])
            
            if output and len(output) > 0:
                # 在 output 数组中查找 type 为 "message" 的项
                # 这是标准的消息输出格式
                message = None
                for item in output:
                    if item.get("type") == "message":
                        message = item
                        break
                
                # 如果没找到 message 类型，退而求其次使用第一个输出项
                if not message:
                    message = output[0]
                
                # 获取消息内容
                content = message.get("content")
                
                # ----------------------------------------
                # 解析不同格式的内容
                # ----------------------------------------
                # API 可能返回多种格式的内容，需要灵活处理
                description = ""
                
                if isinstance(content, list) and len(content) > 0:
                    # 情况 1: content 是数组格式
                    # 例如: [{"type": "output_text", "text": "这是一张..."}]
                    text_content = content[0]
                    
                    if isinstance(text_content, dict):
                        # 内容项是字典，尝试提取 text 字段
                        if text_content.get("type") == "output_text":
                            description = text_content.get("text", "")
                        elif "text" in text_content:
                            description = text_content.get("text", "")
                    elif isinstance(text_content, str):
                        # 内容项直接是字符串
                        description = text_content
                        
                elif isinstance(content, str):
                    # 情况 2: content 直接是字符串
                    # 例如: "这是一张图片的描述"
                    description = content
                
                # ----------------------------------------
                # 显示结果
                # ----------------------------------------
                if description:
                    print("\n" + "=" * 60)
                    print("📷 图片识别结果")
                    print("=" * 60)
                    print(description)
                    print("=" * 60)
                else:
                    # 内容解析失败，显示调试信息
                    print("\n❌ 错误：无法提取文本内容")
                    print(f"消息类型: {message.get('type')}")
                    print(f"内容结构: {content}")
            else:
                # 响应中没有 output 数据
                print("\n❌ 错误：响应中没有输出数据")
                print(f"完整结果: {result}")
        else:
            # ----------------------------------------
            # 处理非完成状态
            # ----------------------------------------
            # 请求可能处于 pending（处理中）、failed（失败）等状态
            print(f"\n⚠️  请求状态: {result.get('status')}")
            if result.get("error"):
                print(f"API 错误信息: {result.get('error')}")
            
    # ----------------------------------------
    # 异常处理
    # ----------------------------------------
    except requests.exceptions.RequestException as e:
        # 捕获所有 requests 库相关的异常
        # 包括：网络连接失败、超时、DNS解析失败、HTTP错误等
        print(f"❌ 网络请求失败: {str(e)}")
        print("请检查：")
        print("  1. 网络连接是否正常")
        print("  2. API 密钥是否有效")
        print("  3. API 端点 URL 是否正确")
        
    except json.JSONDecodeError as e:
        # 捕获 JSON 解析失败的异常
        # 通常发生在服务器返回的不是有效的 JSON 格式时
        print(f"❌ JSON 解析失败: {str(e)}")
        print("服务器返回的内容可能不是有效的 JSON 格式")
        print(f"响应内容: {response.text[:200]}")  # 显示前200个字符
        
    except Exception as e:
        # 捕获所有其他未预期的异常
        # 这是最后的安全网，防止程序崩溃
        print(f"❌ 未知错误: {str(e)}")
        print(f"错误类型: {type(e).__name__}")
    
    finally:
        # 无论成功还是失败，都会执行的清理代码
        print("=" * 60)
        print("程序执行完毕")
        print("=" * 60)
```

---

## 📤 返回示例

### 💡 输出说明

当成功运行上述代码后，您将看到以下内容：

- ✅ **执行进度**：显示三个步骤的执行状态
- 📋 **完整响应**：API 返回的完整 JSON 数据
- 🎯 **识别结果**：AI 对图片的详细文字描述

### 控制台输出示例
```json
============================================================
DMXAPI 图片识别示例程序
============================================================
[步骤 1/3] 正在编码图片...
图片路径: test/example.jpg
✓ 编码成功，数据长度: 289823 字符
[步骤 2/3] 正在构造 API 请求...
✓ 请求构造完成

[步骤 3/3] 正在发送请求到 DMXAPI...
✓ 请求发送成功

正在解析 API 响应...

============================================================
完整 API 响应:
============================================================
{
  "id": "resp_059d6fda1ca05d6e00690de77578048193b8506f6dfdba715f",
  "object": "response",
  "model": "gpt-5-mini-2025-08-07",
  "usage": {
    "total_tokens": 1324,
    "input_tokens": 933,
    "input_tokens_details": {
      "cached_tokens": 0
    },
    "output_tokens": 391,
    "output_tokens_details": {
      "reasoning_tokens": 192
    }
  },
  "created_at": 1762518901,
  "status": "completed",
  "background": false,
  "content_filters": null,
  "error": null,
  "incomplete_details": null,
  "instructions": null,
  "max_output_tokens": null,
  "max_tool_calls": null,
  "output": [
    {
      "id": "rs_059d6fda1ca05d6e00690de779303c8193943a992c91a3904c",
      "type": "reasoning",
      "summary": []
    },
    {
      "id": "msg_059d6fda1ca05d6e00690de77be738819384ec98eafa486417",
      "type": "message",
      "status": "completed",
      "content": [
        {
          "type": "output_text",
          "annotations": [],
          "logprobs": [],
          "text": "这是一张桌面拍摄的照片，画面正中是一台 Canon 品牌的台式计算器（机身上可见型号 WS-1212H 和 “12” 位数标识）。计算器有大尺寸液晶显示屏，上方有两个滑动开关（用于小数位/四舍五入等设置），按键区由深灰、浅灰和红色按键组成，左下角有红色的 ON/CA 和 C/CE 键，右侧有明显的加减乘除和等号键。计算器放在带有大理石纹或水彩纹图案的桌垫上，右上角还能看到一块浅绿色毛巾和一段黑色 USB 线/数据线的线头。整体光线充足，物品清晰、干净且处于可正常使用的状态。"
        }
      ],
      "role": "assistant"
    }
  ],
  "parallel_tool_calls": true,
  "previous_response_id": null,
  "prompt_cache_key": null,
  "reasoning": {
    "effort": "medium",
    "summary": null
  },
  "safety_identifier": null,
  "service_tier": "default",
  "store": true,
  "temperature": 1.0,
  "text": {
    "format": {
      "type": "text"
    },
    "verbosity": "medium"
  },
  "tool_choice": "auto",
  "tools": [],
  "top_logprobs": 0,
  "top_p": 1.0,
  "truncation": "disabled",
  "user": null,
  "metadata": {}
}
============================================================

✓ 请求处理完成，正在提取结果...

============================================================
📷 图片识别结果
============================================================
这是一张桌面拍摄的照片，画面正中是一台 Canon 品牌的台式计算器（机身上可见型号 WS-1212H 和 “12” 位数标识）。计算器有大尺寸液晶显示屏，上方有两个滑动开关（用于小数位/四舍五入等设置），按键区由深灰、浅灰和红色按键组成，左下角有红 色的 ON/CA 和 C/CE 键，右侧有明显的加减乘除和等号键。计算器放在带有大理石纹或水彩纹图案的桌垫上，右上角还能看到一块浅绿色毛巾和一段黑色 USB 线/数据线的线头。整体光线充足，物品清晰、干净且处于可正常使用的状态。
============================================================
============================================================
程序执行完毕
============================================================
```

---

## 📚 重要说明

### 🔑 API 密钥配置

在使用前，请确保：

1. 将代码中的 `API_KEY` 替换为您的真实 DMXAPI 令牌
2. API 密钥格式：`sk-****************************`
3. 保护好您的 API 密钥，不要泄露给他人

### 📁 图片路径设置

- 修改 `IMAGE_PATH` 变量指向您要分析的本地图片
- 支持相对路径和绝对路径
- 确保图片文件存在且可读

### ⚠️ 常见问题

**Q: 支持哪些图片格式？**  
A: 支持 JPG、JPEG、PNG、GIF、WebP 等常见格式。

**Q: 图片大小有限制吗？**  
A: 建议图片大小不超过 20MB，过大的图片会导致编码后数据过长。

**Q: 如何处理请求失败？**  
A: 代码中已包含完善的异常处理机制，会显示详细的错误信息。

### 💾 依赖安装

运行此代码前，请确保已安装所需的 Python 库：

```bash
pip install requests
```

Python 内置库（无需额外安装）：
- `base64` - Base64 编码
- `json` - JSON 处理
- `os` - 文件系统操作

---

<p align="center">
  <small>© 2026 DMXAPI Openai 本地图片分析</small>
</p>