# Jina 重排序模型 API 文档

## 概念说明

### 什么是重排序(Rerank)
重排序是信息检索中的关键技术，在初步检索结果基础上，通过更精细的相关性计算对结果进行重新排序，提升最相关结果的排名。


## 模型名称
`jina-reranker-m0`
Jina 多模态多语言文档重排序模型，10K Tokens 上下文，2.4B 参数，用于包含图文的文档排序。

### 上下文长度
10K Tokens

## API 基础信息
- **Base URL**: `https://www.dmxapi.cn/v1/rerank`
- **认证方式**: Token

## 请求参数
| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| model | string | 是 | 使用的模型名称 |
| query | string | 是 | 查询文本 |
| top_n | integer | 否 | 返回最相关的n个结果(默认全部) |
| documents | array | 是 | 待排序的文档列表 |

## Python 调用示例
```python
import requests
import json

# API配置
API_URL = "https://www.dmxapi.cn/v1/rerank"
API_KEY = "sk-****************************"  # 替换为你的实际API密钥

def rerank_documents(query, docs, top_n=3):
    """
    文档重排序函数
    
    :param query: 查询文本
    :param docs: 待排序文档列表 
    :param top_n: 返回结果数量
    :return: 排序后的文档索引和分数
    """
    payload = {
        "model": "jina-reranker-m0",
        "query": query,
        "top_n": top_n,
        "documents": docs
    }
    
    headers = {
        "Authorization": f"{API_KEY}",
        "Content-Type": "application/json"
    }
    
    # 发送API请求
    response = requests.post(API_URL, headers=headers, data=json.dumps(payload))
    response.raise_for_status()  # 检查请求是否成功
    
    return response.json()

# 使用示例
if __name__ == "__main__":
    query = "如何预防感冒"
    documents = [
        "预防感冒应勤洗手、戴口罩...",
        "流感疫苗每年10月接种最佳...",
        # 其他文档...
    ]
    
    result = rerank_documents(query, documents)
    print("重排序结果:", result)
```

## 响应格式

成功响应示例：
```json
{
  "results": [
    {
      "index": 0,
      "relevance_score": 0.97
    },
    {
      "index": 1,
      "relevance_score": 0.93
    }
  ],
  "usage": {
    "prompt_tokens": 144,
    "total_tokens": 144
  }
}
```

### 响应字段说明

- `results`: 排序结果数组
  - `index`: 原始文档索引
  - `relevance_score`: 相关性分数(0-1)
- `usage`: token使用统计

## 最佳实践

1. 建议`top_n`不超过20，大列表可分批次处理
2. 相关性分数>0.8通常表示高度相关
3. 对长文档建议先做分块处理

<p align="center">
  <small>© 2025 DMXAPI 重排序</small>
</p>