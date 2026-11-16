# MiniMax-H3-Image 提示词增强 API 使用文档

单独调用 MiniMax-H3-Image 的提示词增强，地址是 `POST /v1/h3_image_context_ir`。只改写提示词，不生成图片。不传 `images` 时按文生图增强；传入 1 到 16 张参考图时按图片编辑增强，空数组会返回 400。

## 接口地址

| 接口 | 请求方式 | URL |
|------|---------|-----|
| 提示词增强 | POST | `https://www.dmxapi.cn/v1/h3_image_context_ir` |

:::warning
请妥善保管您的 API Key！严禁将密钥泄露给他人、硬编码到代码中或提交到公开的代码仓库。如果怀疑密钥已泄露，请立即前往 DMXAPI 官网重新生成。
:::

## 模型名称

- `MiniMax-H3-Image`

`MiniMax-H3-Image-Highspeed` 不能用于本接口。

## 提示词增强示例代码

```python
import requests
import json

# ===============================================================
# 步骤1: 配置 API 连接信息
# ===============================================================

# DMXAPI 服务端点地址
# 只改写提示词，不生成图片。报错时网关使用自己的 error 格式。
url = "https://www.dmxapi.cn/v1/h3_image_context_ir"

# DMXAPI 密钥 (请替换为您自己的密钥)
# 获取方式: 登录 DMXAPI 官网 -> 个人中心 -> API 密钥管理
api_key = "sk-******************************************"

# 客户端超时（秒）。官方服务端最长等待 600 秒，实际通常只要几秒。
timeout = 600

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
    # 【model】(string, 必填) 模型名称
    # 只能是 "MiniMax-H3-Image"。MiniMax-H3-Image-Highspeed 返回 400。
    "model": "MiniMax-H3-Image",

    # 【prompt】(string, 必填) 待增强的文本
    # 按 Unicode 字符计，不含首尾空白，最长 32000。空白 prompt 返回 400。
    # 不传 images 时按文生图增强；传了 images 就按图片编辑增强。
    "prompt": "哈苏镜头下的花海",

    # 【images】(object[], 可选) 参考图
    # 不传 images 是文生图增强。传了就必须是 1 到 16 张，空数组会返回 400。顺序对应「图1」「图2」。
    # image_url 三选一：公网 URL、"mm_file://{file_id}"（文件上传 purpose=image_generation_input），
    # 或 "data:image/<格式>;base64,<Base64>"，格式名小写。
    # 格式只支持 JPG、JPEG、PNG、WEBP、HEIC、HEIF。单文件不超过 64MiB，
    # 宽和高都在 128 到 8192，长边/短边不超过 4:1。整个请求体不超过 64MiB。
    # Base64 大约是原文件的 4/3，放不下时改用 URL。
    # 文生图增强不看 size、aspect_ratio、area。这三个参数只影响带参考图的增强。
    # "images": [
    #     {"image_url": "https://example.com/original-cat.png"},
    # ],

    # 【aspect_ratio】(string, 可选) 宽高比
    # 只在 size 不传或为 auto 时使用，默认 auto。文生图增强会忽略它。
    # 编辑增强里，"X:Y" 会让改写描述这个比例；"auto" 或不传则由增强自己决定。
    # X、Y 是 1 到 300 的整数，宽高比含边界 1:3 到 3:1。
    # 只有 size 和 aspect_ratio 都是省略或 auto 时，响应才返回 aspect_ratio。
    # 请求里已经写了 "X:Y"，响应就不再带这个字段。
    "aspect_ratio": "auto",

    # 【area】(string, 可选) 面积档位
    # 只在 size 不传或为 auto 时使用，默认 4K。不影响增强后的文本。
    # 可选值: "1K" / "2K" / "4K"，分别对应 1024²、2048²、4096²。
    "area": "4K",

    # 【size】(string, 可选) 输出尺寸
    # 默认 auto。文生图增强会忽略。编辑增强里写成「宽x高」时，改写会按这个宽高比描述画面。
    # 宽和高必须是正整数，面积含边界 655360 到 20000000，宽高比含边界 1:3 到 3:1。
    # 使用「宽x高」时不能再传 aspect_ratio 和 area，即使它们的值是 auto。
    # "size": "2048x2048",
}

# ===============================================================
# 步骤4: 发送请求并输出结果
# ===============================================================

# 发送 POST 请求到 API 服务器
response = requests.post(url, headers=headers, json=payload, timeout=timeout)

# 格式化输出 JSON 响应
# 两步用法只省文生图的增强费：把 revised_prompt 交给 /v1/images/generations，
# 同时设 disable_prompt_enhanced: true。响应里有 aspect_ratio 就原样带上；
# 没有的话，生成请求改用明确的「宽x高」，不要再传 auto。
# 编辑接口每次都会重新增强，这一步省不掉。
print(json.dumps(response.json(), indent=2, ensure_ascii=False))
```

## 返回示例


```json
{
  "created": 1794023743,
  "revised_prompt": "哈苏中画幅镜头拍摄的大片花海，前景花朵清晰可辨，花田向地平线铺开，自然柔光，色彩饱满，浅景深，胶片质感",
  "aspect_ratio": "3:2",
  "usage": {
    "total_tokens": 3489,
    "input_tokens": 3489
  },
  "request_id": "021792308678142a2c883cf675b9804d"
}
```

<p align="center">
  <small>© 2026 DMXAPI MiniMax-H3-Image 提示词增强</small>
</p>
