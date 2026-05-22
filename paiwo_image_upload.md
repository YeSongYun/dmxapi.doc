# 拍我图片上传 API 文档
图生视频（含首尾帧生成）需要先将所用图片上传，上传成功后会返回对应的 img_id。后续发起视频生成任务时，通过这些 img_id 来指定首帧/尾帧等参考图


## 支持的参数
**支持格式**：`png`、`webp`、`jpeg`、`jpg`  
**支持类型**：`image/jpeg`、`image/jpg`、`image/png`、`image/webp`  
**尺寸限制**：最大支持 10000px 以内的图片
## 接口地址

```
https://www.dmxapi.cn/v1/responses
```


## 模型名称
`paiwo-picture`

## 本地传图 示例代码

```python
"""
╔═══════════════════════════════════════════════════════════════╗
║                  DMXAPI 自研接口                               ║
╚═══════════════════════════════════════════════════════════════╝

📝 功能说明:
   本脚本演示如何使用 requests 库调用 DMXAPI 的自研接口

═══════════════════════════════════════════════════════════════
"""
"""
╔═══════════════════════════════════════════════════════════════╗
║                  DMXAPI 自研接口                               ║
╚═══════════════════════════════════════════════════════════════╝
📝 功能说明:
   本脚本演示如何使用 requests 库调用 DMXAPI 的自研接口
═══════════════════════════════════════════════════════════════
"""
import requests
import json
import base64
# ═══════════════════════════════════════════════════════════════
# 🔑 步骤1: 配置 API 连接信息
# ═══════════════════════════════════════════════════════════════
# 🌐 DMXAPI 服务端点地址
url = "https://www.dmxapi.cn/v1/responses"
# 🔐 DMXAPI 密钥 (请替换为您自己的密钥)
# 获取方式: 登录 DMXAPI 官网 -> 个人中心 -> API 密钥管理
api_key = "sk-****************************************"
# ═══════════════════════════════════════════════════════════════
# 📋 步骤2: 配置请求头
# ═══════════════════════════════════════════════════════════════
headers = {
    "Content-Type": "application/json",      # 指定请求体为 JSON 格式
    "Authorization": f"{api_key}",    # token 认证方式
}
# ═══════════════════════════════════════════════════════════════
# 💬 步骤3: 配置请求参数
# ═══════════════════════════════════════════════════════════════
# 🖼️ 读取图片文件并转为 base64
image_path = "C:/Users/a1/Desktop/测试保存代码/a1.png"  # 替换为实际图片文件路径
with open(image_path, "rb") as f:
    image_base64 = base64.b64encode(f.read()).decode("utf-8")
payload = {
    "model": "paiwo-picture",
    "input": image_base64,
}
# ═══════════════════════════════════════════════════════════════
# 📤 步骤4: 发送请求并输出结果
# ═══════════════════════════════════════════════════════════════
# 发送 POST 请求到 API 服务器
response = requests.post(url, headers=headers, json=payload)
# 格式化输出 JSON 响应
# - indent=2: 缩进 2 空格，便于阅读
# - ensure_ascii=False: 正确显示中文字符
print(json.dumps(response.json(), indent=2, ensure_ascii=False))
```

## 返回示例

```json
{
  "ErrCode": 0,
  "ErrMsg": "Success",
  "Resp": {
    "img_id": 177602101,
    "img_url": "https://media.pixverseai.cn/openapi/d9135033-6998-45ee-bea7-3a8414b90d51_f3ccdd27d2000e3f9255a7e3e2c48800_auto.jpg"
  },
  "usage": {
    "total_tokens": 0,
    "input_tokens": 0,
    "input_tokens_details": {
      "cached_tokens": 0
    },
    "output_tokens": 0,
    "output_tokens_details": {
      "reasoning_tokens": 0
    }
  }
}


```



## url传图 示例代码
```python
"""
╔═══════════════════════════════════════════════════════════════╗
║                  DMXAPI 自研接口                               ║
╚═══════════════════════════════════════════════════════════════╝

📝 功能说明:
   本脚本演示如何使用 requests 库调用 DMXAPI 的自研接口

═══════════════════════════════════════════════════════════════
"""
import requests
import json

# ═══════════════════════════════════════════════════════════════
# 🔑 步骤1: 配置 API 连接信息
# ═══════════════════════════════════════════════════════════════

# 🌐 DMXAPI 服务端点地址
url = "https://www.dmxapi.cn/v1/responses"

# 🔐 DMXAPI 密钥 (请替换为您自己的密钥)
# 获取方式: 登录 DMXAPI 官网 -> 个人中心 -> API 密钥管理
api_key = "sk-**************************************"

# ═══════════════════════════════════════════════════════════════
# 📋 步骤2: 配置请求头
# ═══════════════════════════════════════════════════════════════

headers = {
    "Content-Type": "application/json",      # 指定请求体为 JSON 格式
    "Authorization": f"{api_key}",           # token 认证方式
}

# ═══════════════════════════════════════════════════════════════
# 💬 步骤3: 配置请求参数
# ═══════════════════════════════════════════════════════════════

payload ={
    "model": "paiwo-picture",
    "input": "url",    #不用修改，默认即可
    "image_url": "https://cdn.apifox.com/app/project-icon/custom/20260124/e0874802-fe3b-4740-9ac2-f0b0b47cffe7.png"

}

# ═══════════════════════════════════════════════════════════════
# 📤 步骤4: 发送请求并输出结果
# ═══════════════════════════════════════════════════════════════

# 发送 POST 请求到 API 服务器
response = requests.post(url, headers=headers, json=payload)

# 格式化输出 JSON 响应
# - indent=2: 缩进 2 空格，便于阅读
# - ensure_ascii=False: 正确显示中文字符
print(json.dumps(response.json(), indent=2, ensure_ascii=False))
```



## 返回示例

```json
{
  "ErrCode": 0,
  "ErrMsg": "Success",
  "Resp": {
    "img_id": 177602288,
    "img_url": "https://media.pixverseai.cn/openapi/4e97d22c-f6f2-4496-b449-4ee501ee55f7_1553d6566defe42bf0076e00798b1c94_auto.png"
  },
  "usage": {
    "total_tokens": 0,
    "input_tokens": 0,
    "input_tokens_details": {
      "cached_tokens": 0
    },
    "output_tokens": 0,
    "output_tokens_details": {
      "reasoning_tokens": 0
    }
  }
}
```


<p align="center">
  <small>© 2026 DMXAPI paiwo-picture</small>
</p>