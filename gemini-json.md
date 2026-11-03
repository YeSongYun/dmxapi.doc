# Gemini 原生格式 JSON 格式化输出 API 文档

本示例通过 DMXAPI 调用 `gemini-3.8-flash`，使用 `responseMimeType` 和 `responseSchema` 约束输出。结构化 JSON 位于响应的 `candidates[].content.parts[].text` 字符串中，需要再用 `json.loads` 解析。

运行前安装 `requests`（`pip install requests`），并填写 DMXAPI 密钥。

## 📌 请求地址

```
https://www.dmxapi.cn/v1beta/models/{model}:generateContent
```

## 💻 Python 示例代码
```python
"""
DMXAPI Gemini JSON模式测试脚本
功能：使用DMXAPI Gemini API生成结构化的JSON响应
示例：获取中国流行早餐及其配料信息
"""

import requests
import json

# ============================================================
# API配置部分
# ============================================================
api_key = "sk-*****************************************"  # 在这里填写你的DMX API Key
model = "gemini-3.8-flash"  # 使用的模型名称
url = f"https://www.dmxapi.cn/v1beta/models/{model}:generateContent?key={api_key}"

# ============================================================
# 请求数据配置
# ============================================================
payload = {
    # 对话内容
    "contents": [
        {
            "role": "user",  # 用户角色
            "parts": [{"text": "请列出几种流行的中国早餐,并包含配料的用量。"}]  # 提问内容
        }
    ],
    
    # 生成配置 - 指定返回JSON格式
    "generationConfig": {
        "responseMimeType": "application/json",  # 指定响应格式为JSON
        
        # 定义返回的JSON结构Schema
        "responseSchema": {
            "type": "ARRAY",  # 返回数组类型
            "items": {
                "type": "OBJECT",  # 数组中每个元素为对象
                "properties": {
                    # 早餐名称
                    "recipeName": {"type": "STRING"},
                    
                    # 配料列表
                    "ingredients": {
                        "type": "ARRAY",  # 配料为数组
                        "items": {"type": "STRING"}  # 每个配料为字符串
                    }
                },
                "required": ["recipeName", "ingredients"],
                # 属性顺序
                "propertyOrdering": ["recipeName", "ingredients"]
            }
        }
    }
}

# ============================================================
# 发送请求并输出结果
# ============================================================
headers = {"Content-Type": "application/json"}  # 设置请求头
response = requests.post(url, headers=headers, json=payload, timeout=(10, 120))
response.raise_for_status()
result = response.json()
text = "".join(
    part.get("text", "")
    for part in result["candidates"][0]["content"]["parts"]
    if not part.get("thought")
)
recipes = json.loads(text)
print(json.dumps(recipes, indent=2, ensure_ascii=False))

```

## 📤 返回示例

以下展示 API 原始响应结构，已省略部分字段；上方脚本实际打印解析后的早餐数组。示例文本与用量仅用于说明格式。
```json
{
  "candidates": [
    {
      "content": {
        "role": "model",
        "parts": [
          {
            "text": "[\n  {\n    \"recipeName\": \"豆浆油条 (Soy Milk and Fried Dough Stick)\",\n    \"ingredients\": [\n      \"豆浆 (Soy Milk): 200ml\",\n      \"油条 (Fried Dough Stick): 1根\",\n      \"白糖 (Sugar, optional): 适量\"\n    ]\n  },\n  {\n    \"recipeName\": \"皮蛋瘦肉粥 (Preserved Egg and Lean Pork Congee)\",\n    \"ingredients\": [\n      \"大米 (Rice): 1/2杯\",\n      \"清水 (Water): 6-8杯\",\n      \"猪瘦肉 (Lean Pork): 100克\",\n      \"皮蛋 (Preserved Egg): 1-2个\",\n      \"姜丝 (Shredded Ginger): 3-5片\",\n      \"葱花 (Chopped Green Onion): 1棵\",\n      \"盐 (Salt): 1/2茶匙\",\n      \"白胡椒粉 (White Pepper): 少许\",\n      \"香油 (Sesame Oil): 几滴\"\n    ]\n  },\n  {\n    \"recipeName\": \"煎饼果子 (Jianbing Guozi - Chinese Savory Crepe)\",\n    \"ingredients\": [\n      \"绿豆面粉 (Mung Bean Flour): 50克\",\n      \"小麦面粉 (Wheat Flour): 50克\",\n      \"清水 (Water): 200毫升\",\n      \"鸡蛋 (Egg): 1个\",\n      \"葱花 (Chopped Scallions): 1棵\",\n      \"香菜 (Cilantro): 少量\",\n      \"甜面酱 (Sweet Bean Paste): 1汤匙\",\n      \"辣椒酱 (Chili Sauce, optional): 1茶匙\",\n      \"薄脆 (Crispy Cracker) 或 油条 (Youtiao): 1片/根\",\n      \"食用油 (Cooking Oil): 少量\"\n    ]\n  },\n  {\n    \"recipeName\": \"小笼包 (Xiaolongbao - Soup Dumplings)\",\n    \"ingredients\": [\n      \"猪肉馅 (Pork Mince): 200 克\",\n      \"猪皮冻 (Gelatinous Broth/Aspic): 100克 (切丁)\",\n      \"姜末 (Grated Ginger): 1汤匙\",\n      \"葱花 (Chopped Green Onion): 2汤匙\",\n      \"生抽 (Light Soy Sauce): 1汤匙\",\n      \"料酒 (Shaoxing Wine): 1汤 匙\",\n      \"香油 (Sesame Oil): 1茶匙\",\n      \"盐 (Salt): 1/2茶匙\",\n      \"白胡椒粉 (White Pepper): 少许\",\n      \"小笼包皮 (Dumpling Wrappers): 20-25张\",\n      \"香醋 (Black Vinegar): 适量 (蘸食)\",\n      \"姜丝 (Shredded Ginger): 适量 (蘸食)\"\n    ]\n  }\n]"
          }
        ]
      },
      "finishReason": "STOP",
      "avgLogprobs": -0.71212544698201252
    }
  ],
  "usageMetadata": {
    "promptTokenCount": 28,
    "candidatesTokenCount": 668,
    "totalTokenCount": 2285,
    "trafficType": "ON_DEMAND",
    "promptTokensDetails": [
      {
        "modality": "TEXT",
        "tokenCount": 28
      }
    ],
    "candidatesTokensDetails": [
      {
        "modality": "TEXT",
        "tokenCount": 668
      }
    ],
    "thoughtsTokenCount": 1589
  },
  "modelVersion": "gemini-3.8-flash"
}
```
---

<p align="center">
  <small>© 2026 DMXAPI Gemini json</small>
</p>