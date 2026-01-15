# Openai 请求格式 - 网络图片分析 API 文档

## 📖 接口说明

通过多模态 AI 模型分析图片内容,理解图片、提取图片信息

:::tip 提示
OpenAI 出了新的 responses 接口,兼容性更好  
老接口在部分照片格式兼容上有一定的问题  
新接口文档:[http://doc.dmxapi.cn/res-url-image.html](http://doc.dmxapi.cn/res-url-image.html)
:::

## 🔗 接口地址

```
https://www.dmxapi.cn/v1/chat/completions
```


## 💻 Python 调用示例
```python
"""
图片分析工具 - 使用 Gemini 2.5 Flash 模型进行图片内容分析
============================================================
本脚本演示如何通过 DMX API 调用 Gemini 模型来分析图片内容
适用于图片描述、物体识别、场景理解等应用场景
"""

import requests

# ============================================================
# API 配置区域
# ============================================================
BASE_URL = "https://www.dmxapi.cn/"                                      # API 基础地址
API_ENDPOINT = BASE_URL + "v1/chat/completions"                          # 对话完成接口
API_KEY = "sk-*************************************************"         # API 密钥(请替换为你的密钥)
IMAGE_URL = "https://dmxapi.com/111.jpg"                                 # 待分析图片的 URL 地址

# ============================================================
# 核心功能函数
# ============================================================
def analyze_image(image_url, prompt):
    """
    调用 Gemini 模型分析图片内容
    
    功能说明:
        通过 DMX API 调用 Gemini-2.5-Flash 模型,对指定 URL 的图片进行智能分析
        支持图片描述、物体识别、场景理解等多种分析任务
    
    参数:
        image_url (str): 图片的 URL 地址,需要是公网可访问的链接
        prompt (str): 分析提示词,描述你希望模型如何分析这张图片
    """
    # 构建请求载荷
    payload = {
        "model": "gemini-2.5-flash",                                     # 使用的模型名称
        "messages": [
            {
                "role": "system",                                        # 系统角色:定义助手行为
                "content": [{"type": "text", "text": "你是一个图片分析助手。"}]
            },
            {
                "role": "user",                                          # 用户角色:发送分析请求
                "content": [
                    {"type": "image_url", "image_url": {"url": image_url}},  # 图片 URL
                    {"type": "text", "text": prompt}                     # 分析提示词
                ]
            }
        ],
        "temperature": 0.1                                               # 温度参数:0.1 使输出更确定性和专业
    }
    
    # 构建请求头
    headers = {
        "Content-Type": "application/json",                              # 内容类型:JSON 格式
        "Authorization": f"{API_KEY}"                             # 授权令牌
    }

    # 发送 API 请求并处理响应
    try:
        response = requests.post(API_ENDPOINT, headers=headers, json=payload)
        response.raise_for_status()                                      # 检查 HTTP 状态码
        return response.json()["choices"][0]["message"]["content"]       # 提取分析结果文本
    except Exception as e:
        print(f"❌ 请求失败: {e}")                                        # 错误提示
        return None

# ============================================================
# 程序入口
# ============================================================
if __name__ == "__main__":
    print("=" * 60)
    print("开始分析图片...")
    print("=" * 60)
    
    # 调用图片分析函数
    result = analyze_image(IMAGE_URL, "请描述这张图片的内容")
    
    # 输出分析结果
    if result:
        print("✅ 分析结果:")
        print("-" * 60)
        print(result)
        print("-" * 60)
    else:
        print("❌ 图片分析失败,请检查配置和网络连接")
```

## 📤 返回示例
```json
============================================================
开始分析图片...
============================================================
✅ 分析结果:
------------------------------------------------------------
这张图片展示了一张手写的清单或笔记,内容如下:

*   **第一项:** 680,1560 x 2个木饰面
*   **第二项:** 680,1560 x 1个利流政 (这部分文字可能识别有误,"利流政"看起来不太像常见的词语)
*   **第三项:** 710,(800 x 1个利院的) (同样,"利院的"可能识别有误)
*   **第四项:** 1240 木饰面
*   **第五项:** 700,1900个平面、底面不要,这是落地方
*   **第六项:** 795,2030 午市图像地门 (这部分文字也可能识别有误,"午市图像地门"看起来不太像常见的词语)

每项前面都有一个手绘的方框,方框旁边通常是数字,然后是具体的描述。图片底部有"Memo No."和"Date"的字样,以及一些日历相关的标记。
------------------------------------------------------------
```

---

<p align="center">
  <small>© 2025 DMXAPI Openai 网络图片分析</small>
</p>