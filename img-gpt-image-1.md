# OpenAI GPT Image 文生图 API 文档

## 📍 请求地址

```
https://www.dmxapi.cn/v1/images/generations
```

## 🎯 支持的模型

| 模型名称 | 状态 |
|---------|------|
| `gpt-image-1.5` | ✅ 可用 |
| `gpt-image-1` | ✅ 可用 |
| `gpt-image-1-mini` | ✅ 可用 |
| `dall-e-3` | ✅ 可用 |

## 💻 图像生成 Python 调用示例

```python
"""
===========================================
    DMXAPI 图片生成工具
===========================================
功能说明：
    使用 DMXAPI 的图片生成接口，根据文字描述生成 AI 图片
    支持多种模型：gpt-image、dall-e-3
    生成的图片自动保存到 output 文件夹
===========================================
"""

import requests
import base64
from datetime import datetime
import os

# ============ API 配置 ============
API_KEY = "sk-****************************************"  # 替换为你的 DMXAPI API密钥
API_URL = "https://www.dmxapi.cn/v1/images/generations"  # DMXAPI图片生成接口地址

# ============ 构建请求参数 ============
payload = {
    # 【必填】图像描述
    "prompt": "哪吒竖着大拇指，背景广告牌写着 DMXAPI",
    # 提示词最大长度：gpt-image(32000字符) | dall-e-3(4000字符)
    
    # 【必填】生成数量
    "n": 1,
    # 范围：1-10（注意：dall-e-3 仅支持 n=1）
    
    # 【必填】使用模型
    "model": "gpt-image-1.5",
    
    # 【必填】图像尺寸
    "size": "1024x1536",
    # gpt-image：1024x1024(正方形) | 1536x1024(横版) | 1024x1536(竖版) | auto(自动)
    # dall-e-3：1024x1024 | 1792x1024 | 1024x1792
    
    # 【可选】背景透明度（仅 gpt-image 支持）
    "background": "auto",
    # 可选值：transparent(透明) | opaque(不透明) | auto(自动，默认)
    
    # 【可选】内容审核级别（仅 gpt-image 支持）
    "moderation": "auto",
    # 可选值：low(宽松过滤) | auto(自动，默认)
    
    # 【可选】压缩级别（仅 gpt-image 支持，且输出格式为 webp 或 jpeg）
    # "output_compression": 100,
    # 范围：0-100（默认：100，表示无压缩）
    
    # 【可选】输出格式（仅 gpt-image 支持）
    "output_format": "png",
    # 可选值：png | jpeg | webp
    
    # 【可选】图像质量
    "quality": "auto",
    # gpt-image：auto(自动，默认) | high(高) | medium(中) | low(低)
    # dall-e-3：hd(高清) | standard(标准)
    
    # 【可选】响应格式（仅dall-e-3 支持）
    # "response_format": "url",
    # 可选值：url(图片链接，有效期60分钟) | b64_json(base64编码)
    # 注意：gpt-image 始终返回 base64 编码的图像
    
    # 【可选】图像风格（仅 dall-e-3 支持）
    # "style": "vivid"
    # 可选值：vivid(鲜艳) | natural(自然)
}

# ============ 设置 HTTP 请求头 ============
headers = {
    "Authorization": f"{API_KEY}",  # 身份验证：使用 Token 格式
    "Content-Type": "application/json"     # 内容类型：JSON 格式
}

# ============ 主程序执行 ============
try:
    print("=" * 50)
    print("🎨 开始生成图片...")
    print("=" * 50)
    
    # ---------- 步骤1：创建输出文件夹 ----------
    output_dir = "output"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"✓ 已创建输出文件夹: {output_dir}")
    else:
        print(f"✓ 输出文件夹已存在: {output_dir}")
    
    # ---------- 步骤2：发送 API 请求 ----------
    print(f"📡 正在向 API 发送请求...")
    print(f"   模型: {payload['model']}")
    print(f"   尺寸: {payload['size']}")
    print(f"   数量: {payload['n']}")
    print(f"   提示词: {payload['prompt']}")
    
    response = requests.post(API_URL, json=payload, headers=headers)
    response.raise_for_status()  # 检查 HTTP 状态码，如有错误则抛出异常
    
    # ---------- 步骤3：解析 API 响应 ----------
    result = response.json()
    print(f"✓ API 响应成功！")
    
    # ---------- 步骤4：处理并保存图片 ----------
    if 'data' in result and len(result['data']) > 0:
        print(f"💾 开始保存图片...")
        
        # 遍历返回的每张图片
        for i, image_data in enumerate(result['data']):
            # 处理 base64 编码的图片（gpt-image 返回格式）
            if 'b64_json' in image_data:
                # 解码 base64 数据
                base64_data = image_data['b64_json']
                image_bytes = base64.b64decode(base64_data)
                
                # 生成唯一文件名（时间戳 + 序号）
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"generated_image_{timestamp}_{i+1}.png"
                filepath = os.path.join(output_dir, filename)
                
                # 保存图片到本地
                with open(filepath, 'wb') as f:
                    f.write(image_bytes)
                
                # 获取文件大小
                file_size = os.path.getsize(filepath) / 1024  # 转换为 KB
                print(f"   ✓ 图片 {i+1}: {filepath} ({file_size:.2f} KB)")
            
            # 处理 URL 格式的图片（dall-e-3返回格式）
            elif 'url' in image_data:
                print(f"   ✓ 图片 {i+1} URL: {image_data['url']}")
                print(f"   ⚠️  注意：URL 有效期仅 60 分钟，请及时下载")
        
        print(f"{'=' * 50}")
        print(f"✅ 所有图片处理完成！")
        print(f"{'=' * 50}")
    else:
        print("❌ 未找到图片数据，请检查 API 响应")
    
except requests.exceptions.RequestException as e:
    # 网络请求异常处理
    print(f"{'=' * 50}")
    print(f"❌ 请求失败！")
    print(f"{'=' * 50}")
    print(f"错误信息: {e}")
    
    # 打印详细的错误响应
    if e.response:
        print(f"HTTP 状态码: {e.response.status_code}")
        print(f"响应内容: {e.response.text}")
        
except Exception as e:
    # 其他异常处理
    print(f"{'=' * 50}")
    print(f"❌ 发生未知错误！")
    print(f"{'=' * 50}")
    print(f"错误信息: {e}")
```

## 📤 返回示例

```json
==================================================
🎨 开始生成图片...
==================================================
✓ 已创建输出文件夹: output
📡 正在向 API 发送请求...
   模型: gpt-image-1.5
   尺寸: 1024x1536
   数量: 1
   提示词: 哪吒竖着大拇指，背景广告牌写着 DMXAPI
✓ API 响应成功！
💾 开始保存图片...
   ✓ 图片 1: output\generated_image_20251107_120453_1.png (3024.86 KB)
==================================================
✅ 所有图片处理完成！
==================================================
```

---

<p align="center">
  <small>© 2025 DMXAPI GPT图片</small>
</p>