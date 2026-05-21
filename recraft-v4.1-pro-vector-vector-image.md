# Recraft recraft-v4.1-pro-vector 矢量图生成 API 使用文档

基于 Recraft V4.1 Pro Vector 模型的矢量图生成接口，通过 OpenAI 兼容的 `/v1/chat/completions` 端点调用。专注高质量 SVG 矢量图输出，适合品牌设计、图标制作、插画生成等需要无损缩放的场景

## 🌐 请求地址

```
https://www.dmxapi.cn/v1/chat/completions
```

:::warning
请妥善保管您的 API Key！严禁将密钥泄露给他人、硬编码到代码中或提交到公开的代码仓库。如果怀疑密钥已泄露，请立即前往 DMXAPI 官网重新生成。
:::

## 🎨 模型名称

- `recraft-v4.1-pro-vector`

## 🖼️ 矢量图生成示例代码

```python
import base64
import re

import requests

url = "https://www.dmxapi.cn/v1/chat/completions"
api_key = "sk-**********************************************"

headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json",
}

payload = {
    # 【model】(string, 必填) 调用的模型名称，固定为矢量图生成模型
    "model": "recraft-v4.1-pro-vector",
    # 【messages】(array, 必填) 对话消息列表，按时间顺序排列
    "messages": [
        {
            # 【role】(string, 必填) 消息角色
            # 可选值: "system"(系统提示) / "user"(用户输入) / "assistant"(助手回复)
            "role": "user",
            # 【content】(string | array, 必填) 消息内容；纯文本时为字符串，多模态时为对象数组
            # 此处作为生成提示词，直接描述想要生成的矢量图画面
            "content": "生成一个非常帅气的,站在赛车前的男人"
        }
    ],
    # 【modalities】(array, 可选) 期望返回的模态类型列表
    # 矢量图生成场景须包含 "image" 以触发图像输出
    "modalities": ["image"],
}

response = requests.post(url, headers=headers, json=payload)
print("status:", response.status_code)
data = response.json()

message = data["choices"][0]["message"]
images = message.get("images") or []
if not images:
    print("body:", response.text)
    raise SystemExit("响应中未包含 images 字段")

mime_to_ext = {
    "image/svg+xml": "svg",
    "image/png": "png",
    "image/jpeg": "jpg",
    "image/webp": "webp",
    "image/gif": "gif",
}

for idx, image in enumerate(images):
    image_url = image["image_url"]["url"]
    match = re.match(r"data:([^;]+);base64,(.*)", image_url, re.DOTALL)
    if not match:
        print(f"image[{idx}] 不是 base64 data URL: {image_url[:80]}")
        continue
    mime, b64_payload = match.group(1), match.group(2)
    ext = mime_to_ext.get(mime, "bin")
    out_path = f"output_{idx}.{ext}"
    with open(out_path, "wb") as f:
        f.write(base64.b64decode(b64_payload))
    print(f"已保存: {out_path}  (mime={mime}, size={len(b64_payload)} chars base64)")
```

## 📦 返回示例

```text
status: 200
已保存: output_0.svg  (mime=image/svg+xml, size=114260 chars base64)
```

<p align="center">
  <small>© 2026 DMXAPI recraft-v4.1-pro-vector 矢量图生成</small>
</p>


