# doubao-seedance-2-0-260128 首帧生视频 API 使用文档

基于字节跳动 Seedance 2.0 模型的首帧生视频接口，支持将一张图片作为首帧，结合文本提示词生成 4～15 秒的 AI 视频。视频支持 480p/720p 分辨率、多种宽高比（包括自适应），可选联网搜索增强、同步音频生成及尾帧图像返回功能。采用异步任务模式，通过 DMXAPI 封装的"提交任务 → 直接获取"两步流程完成视频生成。

## 🎬 模型名称

- `doubao-seedance-2-0-260128`

## 🔗 接口地址

| 接口 | 请求方式 | URL |
|------|---------|-----|
| 提交任务 | POST | `https://www.dmxapi.cn/v1/responses` |
| 获取结果 | POST | `https://www.dmxapi.cn/v1/responses` |

:::warning
请妥善保管您的 API Key！严禁将密钥泄露给他人、硬编码到代码中或提交到公开的代码仓库。如果怀疑密钥已泄露，请立即前往 DMXAPI 官网重新生成。
:::


## 🎥 首帧生视频 示例代码

```python
import requests
import json

# 步骤1: 配置 API 连接信息

# DMXAPI 服务端点地址
url = "https://www.dmxapi.cn/v1/responses"

# DMXAPI 密钥 (请替换为您自己的密钥)
# 获取方式: 登录 DMXAPI 官网 -> 个人中心 -> API 密钥管理
api_key = "sk-******************************************"

# 步骤2: 配置请求头

headers = {
    "Content-Type": "application/json",
    "Authorization": f"{api_key}",
}

# 步骤3: 配置请求参数

payload = {
    # 【model】(string, 必填) 调用的模型 ID
    "model": "doubao-seedance-2-0-260128",

    # 【input】(array, 必填) 输入内容数组，支持文本 + 图片组合
    # 首帧生视频：传入 1 个文本对象 + 1 个图片对象，图片 role 设为 first_frame
    "input": [
        {
            # 【type】(string, 必填) 内容类型，文本固定为 "text"
            "type": "text",
            # 【text】(string, 必填) 文本提示词，建议中文不超过 500 字
            "text": "图中小狗对着镜头说\"茄子\"，360度环绕运镜"
        },
        {
            # 【type】(string, 必填) 内容类型，图片固定为 "image_url"
            "type": "image_url",
            "image_url": {
                # 【url】(string, 必填) 首帧图片地址，支持公网 URL、Base64 编码或素材 ID
                # 图片格式：jpeg、png、webp、bmp、tiff、gif
                # 宽高比要求：(0.4, 2.5)，宽高长度：(300, 6000) px，大小不超过 30 MB
                "url": "https://img.shetu66.com/2023/07/14/1689320796087949.png"
            },
            # 【role】(string, 条件必填) 图片用途：首帧生视频固定填 "first_frame"
            "role": "first_frame"
        },
    ],

    # 【generate_audio】(boolean, 可选) 是否生成同步音频（人声、音效、背景音乐）
    # true：生成有声视频（建议将对话内容置于双引号内以优化效果）
    # false：生成无声视频
    # 默认值：true，仅 Seedance 2.0 支持
    "generate_audio": True,

    # 【resolution】(string, 可选) 视频分辨率
    # 可选值："480p" / "720p"（Seedance 2.0 不支持 "1080p"）
    # 默认值："720p"
    "resolution": "720p",

    # 【ratio】(string, 可选) 宽高比
    # 可选值："16:9" / "4:3" / "1:1" / "3:4" / "9:16" / "21:9" / "adaptive"
    # "adaptive"：首帧生视频时根据首帧图片比例自动选择最接近的宽高比
    # 默认值："adaptive"
    "ratio": "adaptive",

    # 【duration】(integer, 可选) 视频时长（秒）
    # 取值范围：[4, 15]
    # 默认值：5
    "duration": 4,

    # 【seed】(integer, 可选) 随机种子，控制生成结果的随机性
    # 取值范围：[-1, 2^32-1]，-1 表示使用随机数
    # 相同 seed 值生成结果相近但不保证完全一致
    # 默认值：-1
    "seed": -1,

    # 【watermark】(boolean, 可选) 是否在生成视频中添加水印
    # false：不含水印（推荐）
    # true：含水印
    # 默认值：false
    "watermark": False,

    # 【callback_url】(string, 可选) 任务状态变更回调地址
    # 状态变更时方舟将向此地址推送 POST 请求
    # 回调状态：queued（排队中）/ running（运行中）/ succeeded（成功）/ failed（失败）/ expired（超时）
    "callback_url": "https://www.dmxapi.cn",

    # 【return_last_frame】(boolean, 可选) 是否返回生成视频的尾帧图像
    # true：返回尾帧图像（PNG 格式，无水印，可用于生成连续视频）
    # false：不返回尾帧图像
    # 默认值：false
    "return_last_frame": False,

    # 【execution_expires_after】(integer, 可选) 任务超时阈值（秒）
    # 取值范围：[3600, 259200]，超时后任务自动终止并标记为 expired
    # 默认值：172800（48 小时）
    "execution_expires_after": 172800,

    # 【tools】(array, 可选) 工具配置，仅 Seedance 2.0 支持
    # {"type": "web_search"}：开启联网搜索，模型根据提示词自主判断是否搜索互联网内容
    "tools": [{"type": "web_search"}]
}

# 步骤4: 发送请求并输出结果

response = requests.post(url, headers=headers, json=payload)

print(json.dumps(response.json(), indent=2, ensure_ascii=False))
```

### 返回示例

```json
{
  "id": "cgt-20260402221030-dmf5x",
  "usage": {
    "total_tokens": 40000,
    "input_tokens": 0,
    "input_tokens_details": {
      "cached_tokens": 0
    },
    "output_tokens": 40000,
    "output_tokens_details": {
      "reasoning_tokens": 0
    }
  }
}
```


## 📥 获取结果 示例代码

```python
import requests
import json

url = "https://www.dmxapi.cn/v1/responses"
api_key = "sk-******************************************"

headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {api_key}",
}

payload = {
    "model": "seedance-2-0-get",
    "input": "cgt-20260403150532-lvbsj"
}

response = requests.post(url, headers=headers, json=payload)
result = response.json()
print(json.dumps(result, indent=2, ensure_ascii=False))

# 提取 video_url
try:
    text = result["output"][0]["content"][0]["text"]
    inner = json.loads(text)
    video_url = inner["content"]["video_url"]
    print(f"\n视频链接: {video_url}")
except Exception as e:
    print(f"提取 URL 失败: {e}")
```

### 返回示例（成功时的原始 JSON）

```json
{
  "request_id": "cgt-20260403150532-lvbsj",
  "output": [
    {
      "type": "message",
      "content": [
        {
          "type": "output_text",
          "text": "{\"content\":{\"video_url\":\"https://ark-acg-cn-beijing.tos-cn-beijing.volces.com/doubao-seedance-2-0/02177520001006000000000000000000000ffffac181cba4c76c3.mp4?X-Tos-Algorithm=TOS4-HMAC-SHA256\\u0026X-Tos-Credential=AKLTYWJkZTExNjA1ZDUyNDc3YzhjNTM5OGIyNjBhNDcyOTQ%2F20260403%2Fcn-beijing%2Ftos%2Frequest\\u0026X-Tos-Date=20260403T070939Z\\u0026X-Tos-Expires=86400\\u0026X-Tos-Signature=b5e95645d33723917482057752dcf8343674e26644f4073e499d25d64d888425\\u0026X-Tos-SignedHeaders=host\"},\"id\":\"cgt-20260403150532-lvbsj\",\"model\":\"doubao-seedance-2-0-260128\",\"status\":\"succeeded\"}"
        }
      ]
    }
  ],
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

视频链接: https://ark-acg-cn-beijing.tos-cn-beijing.volces.com/doubao-seedance-2-0/02177520001006000000000000000000000ffffac181cba4c76c3.mp4?X-Tos-Algorithm=TOS4-HMAC-SHA256&X-Tos-Credential=AKLTYWJkZTExNjA1ZDUyNDc3YzhjNTM5OGIyNjBhNDcyOTQ%2F20260403%2Fcn-beijing%2Ftos%2Frequest&X-Tos-Date=20260403T070939Z&X-Tos-Expires=86400&X-Tos-Signature=b5e95645d33723917482057752dcf8343674e26644f4073e499d25d64d888425&X-Tos-SignedHeaders=host
```

<p align="center">
  <small>© 2026 DMXAPI doubao-seedance-2-0-260128 首帧生视频</small>
</p>
