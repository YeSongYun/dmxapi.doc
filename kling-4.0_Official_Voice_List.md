# 官方音色列表 API 使用文档

查询官方音色库，Kling 4.0 与 Kling 4.0 Flash 共用。路径和可灵官网一样，是 `/v1/general/presets-voices`，前面不要加 `/kling-4-0`。这是直接查询，马上返回，不用再查任务，也不扣费。`pageNum` 取值 1～1000，默认 1；`pageSize` 取值 1～1000，默认 30。
## 接口地址

| 接口 | 请求方式 | URL |
|------|---------|-----|
| 查询列表 | GET | `https://www.dmxapi.cn/v1/general/presets-voices` |


:::warning
请妥善保管您的 API Key！严禁将密钥泄露给他人、硬编码到代码中或提交到公开的代码仓库。如果怀疑密钥已泄露，请立即前往 DMXAPI 官网重新生成。
:::

## 模型名称

- Kling 4.0 与 Kling 4.0 Flash 共用

## 官方音色列表示例代码

```python
import requests
import json

# ===============================================================
# 步骤1: 配置 API 连接信息
# ===============================================================

# 官方音色列表接口。Kling 4.0 和 Kling 4.0 Flash 共用
url = "https://www.dmxapi.cn/v1/general/presets-voices"

# DMXAPI 密钥，请替换为您自己的密钥。令牌需要有 kling-4.0 的权限
# 获取方式: 登录 DMXAPI 官网 -> 个人中心 -> API 密钥管理
api_key = "sk-***********************************************"

# ===============================================================
# 步骤2: 配置请求头
# ===============================================================

headers = {
    "Content-Type": "application/json",  # 指定请求体为 JSON 格式
    "Authorization": f"Bearer {api_key}",  # Bearer 认证，填 DMXAPI 密钥
}

# ===============================================================
# 步骤3: 配置请求参数
# ===============================================================

params = {
    # 【pageNum】(int，可选) 页码，取值 1～1000，默认 1
    "pageNum": 1,
    # 【pageSize】(int，可选) 每页数量，取值 1～500，默认 30
    "pageSize": 30,
}

# ===============================================================
# 步骤4: 发送请求并输出结果
# ===============================================================

response = requests.get(url, headers=headers, params=params)
print("status:", response.status_code)
result = response.json()
print(json.dumps(result, indent=2, ensure_ascii=False))
response.raise_for_status()

# 这个接口是直接查询，马上返回结果，不用再查任务，也不扣费。
# 返回的 data 是一个列表，每一项的 task_result.voices[0] 里：
#   voice_id     官方音色编号。写进全能参考 contents 里的 voice_id，或创建主体时的 element_voice_id
#   voice_name   音色名称
#   trial_url    试听音频地址
#   owned_by     音色来源
# 这里查到的是网关上游这一份官方音色库，编号和可灵官网查到的不通用。
```

## 返回示例

```json
{
  "code": 0,
  "message": "SUCCEED",
  "request_id": "example-request-id",
  "data": [
    {
      "task_status": "succeed",
      "task_result": {
        "voices": [
          {
            "voice_id": "951071228826487641",
            "voice_name": "示例音色",
            "trial_url": "https://example.com/voice-trial.mp3",
            "owned_by": "kling"
          }
        ]
      }
    }
  ]
}
```

<p align="center">
  <small>© 2026 DMXAPI 官方音色列表</small>
</p>
