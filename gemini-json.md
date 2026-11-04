# Gemini 原生格式 JSON 格式化输出 API 文档

本示例通过 DMXAPI 调用 `gemini-3.8-flash`，使用 `responseMimeType` 和 `responseSchema` 约束输出。结构化 JSON 位于响应的 `candidates[].content.parts[].text` 字符串中，需要再用 `json.loads` 解析。

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

```json
[
  {
    "recipeName": "皮蛋瘦肉粥",
    "ingredients": [
      "大米 100克",
      "猪瘦肉 80克",
      "皮蛋 2个",
      "姜丝 5克",
      "葱花 5克",
      "食盐 3克",
      "清水 1000毫升"
    ]
  },
  {
    "recipeName": "煎饼果子",
    "ingredients": [
      "绿豆面 50克",
      "面粉 30克",
      "水 150毫升",
      "鸡蛋 1个",
      "薄脆 1张",
      "甜面酱 10克",
      "葱花 5克",
      "熟黑芝麻 2克"
    ]
  },
  {
    "recipeName": "鲜肉小馄饨",
    "ingredients": [
      "馄饨皮 30张",
      "猪肉馅 150克",
      "生抽 10毫升",
      "香油 5毫升",
      "食盐 2克",
      "紫菜 2克",
      "虾皮 5克",
      "葱花 5克",
      "高汤 500毫升"
    ]
  },
  {
    "recipeName": "自制油条",
    "ingredients": [
      "中筋面粉 250克",
      "鸡蛋 1个",
      "无铝泡打粉 4克",
      "小苏打 2克",
      "食盐 3克",
      "温水 130毫升",
      "植物油 500毫升（炸制耗约30毫升）"
    ]
  }
]
```
---

<p align="center">
  <small>© 2026 DMXAPI Gemini json</small>
</p>