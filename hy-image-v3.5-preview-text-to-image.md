# hy-image-v3.5-preview 文生图 API 使用文档

基于腾讯混元 Hy-Image-3.5-preview 模型的文生图接口，通过 `/v1/images/generations` 端点调用，一次请求同步返回生成结果，无需提交任务与轮询。支持最高 4096×4096（4K）分辨率输出，宽高可在 [256, 8192] 范围内自由指定；未指定尺寸时模型按 1K / 1.5K / 2K 三个面积档位自主决策出图尺寸，同时支持生成种子复现、外部搜索增强与最长 16 字符的自定义水印脚注，返回有效期 12 小时的临时图片地址。

## 🌐 请求地址

```text
https://www.dmxapi.cn/v1/images/generations
```

:::warning
请妥善保管您的 API Key！严禁将密钥泄露给他人、硬编码到代码中或提交到公开的代码仓库。如果怀疑密钥已泄露，请立即前往 DMXAPI 官网重新生成。
:::

## 模型名称

- `hy-image-v3.5-preview`

## 文生图 示例代码

```python
import json
import requests

# ===============================================================
# 步骤1: 配置 API 连接信息
# ===============================================================

# DMXAPI 服务端点地址
url = "https://www.dmxapi.cn/v1/images/generations"

# DMXAPI 密钥 (请替换为您自己的密钥)
# 获取方式: 登录 DMXAPI 官网 -> 个人中心 -> API 密钥管理
api_key = "sk-***********************************************"

# ===============================================================
# 步骤2: 配置请求头
# ===============================================================

headers = {
    "Authorization": f"Bearer {api_key}",    # Bearer token 认证方式
    "Content-Type": "application/json",      # 指定请求体为 JSON 格式
}

# ===============================================================
# 步骤3: 配置请求参数
# ===============================================================

payload = {
    # 【model】(string, 必填) 调用的模型名称
    # 取值: hy-image-v3.5-preview
    "model": "hy-image-v3.5-preview",

    # 【prompt】(string, 必填) 文生图提示词
    "prompt": "一辆在落日余晖里极速行驶的拉力赛车",

    # 【size】(string, 可选) 生成尺寸，格式 ${宽}x${高}
    # 宽、高均为正整数，取值范围 [256, 8192]
    # 宽 × 高（面积）不超过 16777216，即最高支持 4096x4096（4K）
    # 不传或传空串时，由模型基于 prompt 语义与 generate_max_pixels 自主决定尺寸
    # 传入具体值时强制按指定尺寸出图；需要 4K 输出时传 "4096x4096" 即可
    "size": "1024x1024",

    # 【seed】(integer, 可选) 生成种子
    # int64 类型，取值范围 [0, 2^63-1]；为 0 或不传时服务端随机分配，负值将被拒绝
    # 需要复现同一结果时，请固定 seed + prompt + size
    "seed": 0,

    # 【generate_max_pixels】(integer, 可选) 生成图片的目标面积（像素数）
    # 仅在未传 size 时生效，支持 3 个枚举档位:
    #   - 1048576: 1K（1024x1024）
    #   - 2359296: 1.5K（默认档位）
    #   - 4194304: 2K
    # 传入非枚举中间值时按最近面积归档
    # 该参数最高档位为 2K，需要更高分辨率请改用 size 指定
    "generate_max_pixels": 4194304,

    # 【resize_max_pixels】(integer, 可选) 输入参考图面积上限（像素数）
    # 原图面积不超过阈值时原样透传；超过阈值时按比例等比缩放到接近阈值后再送入模型
    # 用于控制大图（4K/6K）带来的上下文 token 消耗
    # 不传时默认 1048576（1024x1024）
    "resize_max_pixels": 1048576,

    # 【footnote】(string, 可选) 业务自定义水印内容
    # 最长 16 个字符（按 utf8.RuneCount 计算，不区分中英文），生成在图片右下角
    "footnote": "DMXAPI",

    # 【use_search_tool】(object, 可选) 外部搜索增强开关
    # 结构固定为 {"value": true} 或 {"value": false}，当前默认关闭
    "use_search_tool": {
        "value": False
    }
}

# ===============================================================
# 步骤4: 发送请求并输出结果
# ===============================================================

# 发送 POST 请求到 API 服务器
response = requests.post(
    url,
    headers=headers,
    json=payload,
    timeout=300
)

response.raise_for_status()

result = response.json()

# 格式化输出 JSON 响应
# - indent=2: 缩进 2 空格，便于阅读
# - ensure_ascii=False: 正确显示中文字符
print(json.dumps(result, indent=2, ensure_ascii=False))

# 打印生成的图片地址（临时签名 URL，有效期 12 小时，请及时下载转存）
if result.get("data"):
    print("\n图片地址：")
    print(result["data"][0].get("url"))
```

## 返回示例

```json
{
  "created": 1789720599,
  "data": [
    {
      "url": "https://aigc-output-image-file-1326893053.cos.ap-guangzhou.myqcloud.com/xxx/main.png?..."
    }
  ],
  "request_id": "a1c00d07-041b-4daa-bae0-b7eabf2bc33a",
  "usage": {
    "total_tokens": 20000
  }
}
```

<p align="center">
  <small>© 2026 DMXAPI hy-image-v3.5-preview 文生图</small>
</p>
