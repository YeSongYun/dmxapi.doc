# 阿里 text-embedding-v4 向量模型 API 文档

## 概念介绍

该模型是通义实验室基于Qwen3训练的多语言文本统一向量模型，相较V3版本在文本检索、聚类、分类性能大幅提升。

在MTEB多语言、中英、Code检索等评测任务上效果提升15%~40%；支持64~2048维用户自定义向量维度。

## 模型名称
`text-embedding-v4`

## 最大支持长度
128K 输入

## 基础信息
- **Base URL**: `https://www.dmxapi.cn/v1/embeddings`
- **认证方式**: Token

## 请求参数
| 参数名 | 类型 | 必填 | 说明 |
|-------|------|------|------|
| model | string | 是 | 使用的模型ID |
| input | string | 是 | 需要转换为向量的文本内容 |

## Python 调用示例
```python
import json
import requests

# API配置
url = "https://www.dmxapi.cn/v1/embeddings"
headers = {
    "Authorization": "sk-****************",  # 替换为你的 DMXAPI 令牌
    "Content-Type": "application/json",
}

# 请求数据
payload = json.dumps({
    "model": "text-embedding-v4-250515",  # 指定模型版本
    "input": "你好，把这句话变向量吧。"  # 需要转换的文本
})

# 发送请求
response = requests.post(url, headers=headers, data=payload)

# 输出结果
print(response.json())  # 返回的向量数据
```

## 响应示例
成功响应将返回包含向量数据的JSON对象：
```json
{
  "object": "list",
  "data": [
    {
      "object": "embedding",
      "embedding": [0.1, 0.2, ...],  # 文本向量
      "index": 0
    }
  ],
  "model": "text-embedding-v4-250515"
}
```

> 注意：请妥善保管API密钥，不要泄露给他人。

<p align="center">
  <small>© 2025 DMXAPI 向量嵌入</small>
</p>