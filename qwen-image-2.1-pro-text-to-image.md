# qwen-image-2.1-pro 文生图 API 使用文档

基于 `qwen-image-2.1-pro` 的文生图（T2I）接口，通过 `/v1/images/generations` 端点同步调用。支持单次输出 1~6 张图，输出分辨率总像素在 512×512 至 2048×2048 之间、宽高比 1:8 至 8:1 自由设置（不指定 `size` 时由模型根据提示词自动推荐分辨率），并提供提示词智能改写（DPE / APE）、思考模式、水印与随机种子等配置；该模型价格为 0.25 元/张。

## 接口地址

| 接口 | 请求方式 | URL |
|------|---------|-----|
| 文生图 | POST | `https://www.dmxapi.cn/v1/images/generations` |

:::warning
请妥善保管您的 API Key！严禁将密钥泄露给他人、硬编码到代码中或提交到公开的代码仓库。如果怀疑密钥已泄露，请立即前往 DMXAPI 官网重新生成。
:::

## 模型名称

- `qwen-image-2.1-pro`

## 文生图 示例代码

```python
import requests
import json

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
    "Content-Type": "application/json",      # 指定请求体为 JSON 格式
    "Authorization": f"{api_key}",           # token 认证方式
}

# ===============================================================
# 步骤3: 配置请求参数
# ===============================================================

payload = {
    # 【model】(string, 必填) 调用的模型名称
    "model": "qwen-image-2.1-pro",

    # 【prompt】(string, 必填) 正向提示词
    # 用于描述您期望生成的图像内容、风格和构图，支持中英文
    # 推荐不超过 4500 Token
    "prompt": "一只橘猫坐在窗边，阳光穿过树叶洒在地面上，电影感，高细节",

    # 【n】(integer, 可选) 输出图像的数量，支持输出 1~6 张图片，默认值 1
    "n": 1,

    # 【prompt_extend】(bool, 可选) 是否开启提示词智能改写，默认值 True (建议开启)
    # 开启后模型会按照 prompt_extend_mode 指定的方式优化正向提示词
    # 对描述较简单的提示词效果提升明显
    "prompt_extend": True,

    # 【prompt_extend_mode】(string, 可选) 提示词改写方式，默认值 "direct"
    # 可选值:
    #   - "direct" 直接提示词增强(DPE)，适用于大多数场景，T2I 和 I2I 均支持
    #   - "agent"  智能体提示词增强(APE)，提供更精细的改写效果，仅支持文生图(T2I)
    "prompt_extend_mode": "direct",

    # 【enable_thinking】(bool, 可选) 是否开启思考模式，默认值 True
    # 开启时模型将增强推理能力以提升出图质量，但会增加生成耗时
    # 仅在 prompt_extend=True 时生效
    "enable_thinking": True,

    # 【watermark】(bool, 可选) 是否添加水印，默认值 False
    "watermark": False,

    # ---------------------------------------------------------------
    # 以下为可选参数，按需取消注释后使用
    # ---------------------------------------------------------------

    # 【size】(string, 可选) 设置输出图像的分辨率，格式为 宽x高，例如 "1024x1024"
    # 未指定或填写 "auto" 时，由模型根据提示词自动推荐分辨率
    # 文生图(T2I): 像素面积范围 512x512 至 2048x2048，宽高比限制 1:8 至 8:1
    # "size": "1024x1024",

    # 【seed】(integer, 可选) 随机数种子，取值范围 [0, 2147483647]
    # 未传入时服务会随机选择种子，固定种子可使生成结果相对稳定
    # "seed": 42,
}


# ===============================================================
# 步骤4: 发送请求并输出结果
# ===============================================================

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
  "created": 1792396854,
  "data": [
    {
      "url": "https://dashscope-a717.oss-accelerate.aliyuncs.com/1d/50/20261019/0f854a6a/f1a6d996-0cba-905b-a6c4-03ff01292764_qwen_image3_serving_output_0.png?..."
    }
  ],
  "usage": {
    "height": 1680,
    "image_count": 1,
    "width": 2512
  }
}
```

<p align="center">
  <small>© 2026 DMXAPI qwen-image-2.1-pro 文生图</small>
</p>
