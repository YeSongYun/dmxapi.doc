# 阿里 qwen3-reranker-8b 重排序模型 API 文档

## 模型名称
`qwen3-reranker-8b`

Qwen3-Reranker-8B 是阿里专为文本嵌入和重排序打造的模型，属于 Qwen3 家族。

上下文长度 32k，支持 100 多种语言。在 MTEB 多语言排行榜上，其嵌入模型表现优异。

该模型在文本检索场景表现出色，为相关任务提供强大助力 。

### 上下文长度
支持最长 32k token

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
        "model": "qwen3-reranker-8b",
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

```json
{
  "results":[
    {
      "document":{
        "text":"预防感冒应勤洗手、戴口罩，保持室内通风（来源：协和医院研究）"
      },
      "index":0,
      "relevance_score":0.99853515625
    },
    {
      "document":{
        "text":"维生素C对感冒的预防效果存在争议（来源：JAMA医学期刊）"
      },
      "index":4,
      "relevance_score":0.392333984375
    },
    {
      "document":{
        "text":"流感疫苗每年10月接种最佳，可降低70%感染风险（来源：卫健委2024指南）"
      },
      "index":1,
      "relevance_score":0.2069091796875
    }],
  "usage":{
    "prompt_tokens":0,
    "completion_tokens":0,
    "total_tokens":0,
    "prompt_tokens_details":{
      "cached_tokens_details":{
      }
    },
    "completion_tokens_details":{
    }
  }
}
```

<p align="center">
  <small>© 2025 DMXAPI 重排序</small>
</p>