# OpenAI Responses API 本地图片分析

本页演示将本地图片编码为 Base64 Data URL，再通过 DMXAPI 兼容代理交给 `gpt-5.6-sol` 分析。

## 🔗 请求地址

```text
https://www.dmxapi.cn/v1/responses
```

:::warning API 密钥安全
示例令牌为不可用占位符。请妥善保管真实 DMXAPI 令牌，不要写入公开仓库或日志。
:::

## 模型名称

- `gpt-5.6-sol`

## Python 请求示例

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
IMAGE_PATH = "img/cc_01.png"  # 仓库内可直接运行的示例图片

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
        "model": "gpt-5.6-sol",  # 使用 GPT-5.6 Sol 视觉模型
        "input": [{
            "role": "user",  # 消息角色：user（用户）、assistant（助手）、system（系统）
            "content": [
                # 文本输入：告诉模型我们想要什么
                {
                    "type": "input_text",
                    "text": "红色箭头指向哪个蓝色按钮？只回复按钮文字。",
                },
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

## 返回示例

```json
{
  "id": "resp_example_gpt56_base64_image_001",
  "object": "response",
  "status": "completed",
  "model": "gpt-5.6-sol",
  "output": [
    {
      "id": "msg_example_gpt56_base64_image_001",
      "type": "message",
      "status": "completed",
      "role": "assistant",
      "content": [
        {
          "type": "output_text",
          "text": "添加供应商",
          "annotations": []
        }
      ]
    }
  ]
}
```

## 注意事项

- Data URL 格式必须是 `data:<MIME>;base64,<内容>`。
- Base64 会增加请求体积；大文件应优先使用可访问的 URL 或文件上传方案。
- 不要读取不受信任的任意文件路径，生产环境应限制格式、大小和来源。
- 本页示例直接读取仓库内的 `img/cc_01.png`；红色箭头指向“添加供应商”按钮。

<p align="center">
  <small>© 2026 DMXAPI OpenAI Responses API 本地图片分析</small>
</p>
