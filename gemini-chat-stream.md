# Gemini 原生格式流式输出 API 文档

使用 `gemini-3.8-flash` 的 `streamGenerateContent` 接口，以 SSE 格式逐步接收文本。

## 📌 接口地址

```
https://www.dmxapi.cn/v1beta/models/{model}:streamGenerateContent?alt=sse
```

## 💻 请求示例 (Python)

```python
"""
==============================================================================
DMXAPI Gemini AI 流式对话 API 调用示例
==============================================================================
功能说明：
    本脚本演示如何使用 DMXAPI 调用 Gemini 模型进行流式对话生成
    支持实时接收和显示 AI 生成的文本内容
    
作者：DMXAPI
==============================================================================
"""

import json
import requests

# ==============================================================================
# 配置参数区域
# ==============================================================================
model = "gemini-3.8-flash"  # 使用的 AI 模型名称
API_KEY = "sk-*****************************************"  # 你的 API 密钥

# 构建完整的 API 请求 URL
# 格式：基础URL + 模型名称 + 流式生成端点 + API密钥 + SSE格式参数
url = f"https://www.dmxapi.cn/v1beta/models/{model}:streamGenerateContent?key={API_KEY}&alt=sse"

# ==============================================================================
# 请求数据准备
# ==============================================================================
payload = json.dumps({
    "system_instruction": {  # 系统指令：定义 AI 助手的角色和行为特征
        "parts": [{"text": "你是我的助手，你叫 小巴。"}]
    },
    "contents": [  # 用户输入：包含用户的对话内容
        {"role": "user", "parts": [{"text": "随机生成300个字"}]}
    ]
})

# 设置 HTTP 请求头
headers = {"Content-Type": "application/json"}

# ==============================================================================
# 发送 API 请求
# ==============================================================================
# 发送 POST 请求到 API 端点
# stream=True：启用流式响应，可以实时接收数据块，而不是等待全部完成
response = requests.post(url, headers=headers, data=payload, stream=True, timeout=(10, 120))

# 检查响应状态码
if response.status_code != 200:
    print(f"API 请求失败，状态码: {response.status_code}")
    print(f"错误信息: {response.text}")
    exit(1)

response.encoding = 'utf-8'  # 设置编码为 UTF-8，确保中文字符正确显示

# ==============================================================================
# SSE 流式响应解析函数
# ==============================================================================
def parse_sse_response(response):
    """
    解析 Server-Sent Events (SSE) 格式的流式响应
    
    SSE 是一种服务器向客户端推送实时数据的技术，常用于流式 AI 对话场景
    本函数会实时解析并输出 AI 生成的文本内容
    
    参数说明：
        response (requests.Response): requests 库返回的响应对象，包含流式数据
        
    返回值：
        str: 完整拼接后的 AI 生成文本
        
    工作流程：
        1. 逐行读取 SSE 数据流
        2. 识别并提取 JSON 格式的数据
        3. 解析 JSON 并提取文本内容
        4. 实时输出文本片段
        5. 累积并返回完整文本
    """
    full_text = ""  # 用于累积存储完整的 AI 响应文本
    
    # 逐行迭代读取流式响应数据
    for line in response.iter_lines(decode_unicode=True):
        # 跳过空行
        if not line or line.strip() == "":
            continue
            
        # SSE 数据行以 'data:' 开头，冒号后的空格可省略
        if line.startswith('data:'):
            json_str = line[5:].strip()
            
            # 跳过空数据或 [DONE] 标记
            if not json_str or json_str == '[DONE]':
                continue
            
            try:
                # 将 JSON 字符串解析为 Python 字典对象
                data = json.loads(json_str)
                
                # 验证响应数据结构的完整性
                # 检查是否包含 'candidates' 字段且不为空
                if 'candidates' in data and len(data['candidates']) > 0:
                    candidate = data['candidates'][0]  # 获取第一个候选响应结果
                    
                    # 检查候选结果是否包含内容数据
                    if 'content' in candidate and 'parts' in candidate['content']:
                        # 遍历内容的各个部分（parts）
                        for part in candidate['content']['parts']:
                            # 如果当前部分包含文本内容
                            if 'text' in part and not part.get('thought'):
                                text = part['text']
                                full_text += text  # 累积到完整文本中
                                # 实时输出文本片段
                                # end='': 不自动换行
                                # flush=True: 立即刷新输出缓冲区，确保实时显示
                                print(text, end='', flush=True)
                                
            except json.JSONDecodeError:
                # 如果遇到非法 JSON 格式，跳过当前行继续处理下一行
                continue
            except Exception:
                # 捕获其他异常，确保程序继续运行
                continue
    
    return full_text  # 返回完整拼接的生成文本


# ==============================================================================
# 主程序执行
# ==============================================================================
# 调用解析函数处理 API 响应并获取完整结果
result_text = parse_sse_response(response)
```

## 📤 返回示例

```text
好的，小巴为您生成了下面这段约300字的内容：

微风穿过静谧的森林，树叶沙沙作响，像是在低声诉说着古老的秘密。阳光透过稀疏的云层，斑驳地洒在青石板铺成的小径上。一只蓝色的飞鸟掠过清澈见底的溪流，惊起了停在水草尖上的蜻蜓。远处的山峦在晨雾中若隐若现，轮廓柔和得宛如一幅未干的水墨画。街角的旧书店悄悄推开了木门，风铃发出清脆的声响，混合着咖啡与旧纸张的香气。时间在这里放慢了脚步，让人忘却了喧嚣。生活总在不经意间展现温柔，或许是一朵破土而出的野花，或许是一抹黄昏时的晚霞。只要静下心倾听，平凡的瞬间都藏着独特的诗意，默默治愈着疲惫的灵魂，给平淡的日子镀上一层温暖的光晕。
```
---

<p align="center">
  <small>© 2026 DMXAPI Gemini 流式输出</small>
</p>