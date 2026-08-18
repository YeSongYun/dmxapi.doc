# Gemini API 视频分析接口文档

## 📌 接口地址

```
https://www.dmxapi.cn/v1beta/models/{model}:generateContent
```



## 💻 Python 示例代码

```python
"""
========================================
视频分析脚本 - DMXAPI Gemini API 视频内容分析工具
========================================

功能说明:
    使用 DMXAPI Gemini API 对视频文件进行智能内容分析
    支持将视频文件编码为 Base64 格式并发送给 AI 模型进行分析
    
作者: DMXAPI团队
"""

import base64
import json
import requests


# ========================================
# 配置参数
# ========================================

model = "gemini-2.5-flash"          # AI 模型名称，支持视频分析
API_URL = f"https://www.dmxapi.cn/v1beta/models/{model}:generateContent"
API_KEY = "sk-*****************************************"  # 请替换为您自己的 DMXAPI 密钥
VIDEO_PATH = "test/example.mp4"      # 视频文件路径


# ========================================
# 视频编码函数
# ========================================

def encode_video_to_base64(video_path):
    """
    将视频文件编码为 Base64 字符串
    
    参数:
        video_path (str): 视频文件的路径
        
    返回:
        str: Base64 编码的视频数据字符串，失败返回 None
        
    说明:
        Base64 编码是将二进制数据转换为 ASCII 字符串的编码方式，
        这样可以通过 HTTP 请求安全地传输视频数据。
    """
    try:
        # 以二进制模式打开视频文件
        with open(video_path, "rb") as video_file:
            # 读取文件内容
            video_bytes = video_file.read()
            # 将字节数据编码为 Base64 字符串
            base64_string = base64.b64encode(video_bytes).decode("utf-8")
            return base64_string
            
    except Exception as e:
        # 捕获所有可能的异常（文件不存在、权限问题等）
        print(f"❌ 视频编码错误: {e}")
        return None


# ========================================
# 视频分析主函数
# ========================================

def analyze_video():
    """
    发送视频分析请求到 Gemini API
    
    执行流程:
        1. 检查 API 密钥是否存在
        2. 将视频文件编码为 Base64 格式
        3. 构建 API 请求数据
        4. 发送 POST 请求到 Gemini API
        5. 解析并显示分析结果
    """
    
    # ----------------------------------------
    # 步骤 1: 检查 DMXAPI 密钥
    # ----------------------------------------
    if not API_KEY:
        print("❌ 错误: 请设置 API 密钥")
        return

    # ----------------------------------------
    # 步骤 2: 编码视频文件
    # ----------------------------------------
    print("📹 正在编码视频文件...")
    video_data = encode_video_to_base64(VIDEO_PATH)
    if not video_data:
        print("❌ 视频编码失败，程序终止")
        return

    # ----------------------------------------
    # 步骤 3: 构建 HTTP 请求
    # ----------------------------------------
    # 设置请求头
    headers = {"Content-Type": "application/json"}
    
    # 构建请求负载 (按照 DMXAPI Gemini API 格式要求)
    payload = {
        "contents": [{
            "role": "user",                    # 角色: 用户
            "parts": [
                {
                    "inlineData": {
                        "mimeType": "video/mp4",    # 文件类型
                        "data": video_data          # Base64 编码的视频数据
                    }
                },
                {
                    "text": "视频文件里都显示了哪些内容？"  # 分析提示词
                }
            ]
        }]
    }

    # ----------------------------------------
    # 步骤 4: 发送 API 请求
    # ----------------------------------------
    try:
        print("🚀 正在发送请求到 Gemini API...")
        
        # 发送 POST 请求
        response = requests.post(
            API_URL,
            headers=headers,
            params={"key": API_KEY},
            json=payload
        )
        
        # 检查 HTTP 状态码
        response.raise_for_status()
        
        # ----------------------------------------
        # 步骤 5: 解析响应结果
        # ----------------------------------------
        result = response.json()
        
        # 提取并显示分析结果
        if "candidates" in result and len(result["candidates"]) > 0:
            candidate = result["candidates"][0]
            
            if "content" in candidate and "parts" in candidate["content"]:
                # 提取 AI 生成的文本内容
                text_content = candidate["content"]["parts"][0].get("text", "")
                
                # 显示分析结果
                print("\n" + "=" * 50)
                print("📊 视频分析结果")
                print("=" * 50)
                print(text_content)
                
                # 显示 API 使用统计
                print("\n" + "=" * 50)
                print("📈 使用统计")
                print("=" * 50)
                if "usageMetadata" in result:
                    usage = result["usageMetadata"]
                    print(f"总 Token 数:  {usage.get('totalTokenCount', 0)}")
                    print(f"提示 Token 数: {usage.get('promptTokenCount', 0)}")
                    print(f"回复 Token 数: {usage.get('candidatesTokenCount', 0)}")
            else:
                print("⚠️  响应格式异常，无法提取文本内容")
        else:
            print("⚠️  未获得有效的分析结果")
            
        # 调试选项: 显示完整的 API 响应（可选）
        # print("\n" + "=" * 50)
        # print("🔍 完整响应")
        # print("=" * 50)
        # print(json.dumps(result, indent=2, ensure_ascii=False))
        
    except requests.exceptions.RequestException as e:
        # 捕获所有 requests 相关的异常
        print(f"\n❌ 请求失败: {e}")
        
        # 显示详细的错误信息
        if hasattr(e, 'response') and e.response:
            print(f"状态码: {e.response.status_code}")
            print(f"响应: {e.response.text}")



# ========================================
# 程序入口
# ========================================

if __name__ == "__main__":
    """
    主程序入口
    当脚本直接运行时执行视频分析
    (防止模块被导入时自动执行)
    """
    print("=" * 50)
    print("🎬 Gemini 视频分析工具启动")
    print("=" * 50 )
    
    analyze_video()
    
    print("=" * 50)
    print("✅ 分析完成")
    print("=" * 50  )
```

## ✅ 返回示例

```json
==================================================
🎬 Gemini 视频分析工具启动
==================================================
📹 正在编码视频文件...
🚀 正在发送请求到 Gemini API...

==================================================
📊 视频分析结果
==================================================
这段视频的开头显示了一只白色的鸟在黑暗的背景中飞翔。它很快变成了蓝色背景中的一只鸟，俯冲到蓝色背景中的水面上。这只鸟潜入水中，露出了水下正在迁徙的一大群鱼。随后，一群白色的鸟潜入水中，露出了另一大群鱼。在这之后，一群海豚在捕食 那些鱼。这又引发了一群鲨鱼吃鱼。最后，在视频的结尾，一条鲸鱼从水里跳出来。

==================================================
📈 使用统计
==================================================
总 Token 数:  13391
提示 Token 数: 13285
回复 Token 数: 106
==================================================
✅ 分析完成
==================================================
```

---

<p align="center">
  <small>© 2026 DMXAPI Gemini 视频</small>
</p>