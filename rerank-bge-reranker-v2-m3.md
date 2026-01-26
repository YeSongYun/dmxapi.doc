# bge-reranker-v2-m3-free 重排序模型 API 文档
由北京智源人工智能研究院（BAAI）开发的轻量级、高性能重排序模型，具备多语言能力，可计算查询与文档间的相关性得分。
## 接口地址

```
https://www.dmxapi.cn/v1/rerank
```
## 模型名称
`bge-reranker-v2-m3-free`

## Python 调用示例
```python
import requests
import json

# API配置
api_key ="sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
api_url = "https://www.dmxapi.cn/v1/rerank"
headers = {
        "Authorization": f"{api_key}",
        "Content-Type": "application/json"
    }
query = "如何预防感冒"
documents = [
    "预防感冒应勤洗手、戴口罩，保持室内通风（来源：协和医院研究）",
    "流感疫苗每年10月接种最佳，可降低70%感染风险（来源：卫健委2024指南）",
    "维生素C对感冒的预防效果存在争议（来源：JAMA医学期刊）"
    ]

payload = {
    "model": "bge-reranker-v2-m3-free",  # 模型名称，必填
    "query": query,                       # 查询文本，必填
    "documents": documents,               # 待排序文档列表，至少1个字符串，目前仅支持字符串列表。未来将支持文档对象，必填
    "top_n": 3,                       # 要返回的最相关文档或索引的数量，选填
    "return_documents": True, # 是否返回原文，true包含文本，false不包含，选填
    "max_chunks_per_doc": 5,  # 文档中生成的最大数据块数。长文档会被分割成多个数据块进行计算，取其中得分最高的数据块作为文档的最终得分，选填
    "overlap_tokens": 20      # 文档分块后相邻块之间的词元重叠数，最大80，选填
}


# 发送API请求
try:
    response = requests.post(api_url, headers=headers, data=json.dumps(payload), timeout=30)
    response.raise_for_status()
    result = response.json()
    print("重排序结果:")
    print(json.dumps(result, ensure_ascii=False, indent=2))
except Exception as e:
    print(f"请求失败: {e}")

```

## 响应格式
```json
{
  "results": [
    {
      "document": {
        "text": "预防感冒应勤洗手、戴口罩，保持室内通风（来源：协和医院研究）"
      },
      "index": 0,
      "relevance_score": 0.9700092673301697
    },
    {
      "document": {
        "text": "流感疫苗每年10月接种最佳，可降低70%感染风险（来源：卫健委2024指南）"
      },
      "index": 1,
      "relevance_score": 0.14572574198246002
    },
    {
      "document": {
        "text": "维生素C对感冒的预防效果存在争议（来源：JAMA医学期刊）"
      },
      "index": 2,
      "relevance_score": 0.02796747349202633
    }
  ],
  "usage": {
    "prompt_tokens": 0,
    "completion_tokens": 0,
    "total_tokens": 0,
    "prompt_tokens_details": {
      "cached_tokens_details": {}
    },
    "completion_tokens_details": {},
    "claude_cache_creation_5_m_tokens": 0,
    "claude_cache_creation_1_h_tokens": 0
  }
}
```


<p align="center">
  <small>© 2025 DMXAPI 重排序</small>
</p>
