# gpt-image-2 图片编辑 API 使用文档

基于 gpt-image-2 的图片编辑接口，可通过一张或多张参考图配合文本提示词生成新图，

## 🌐 请求地址

```text
https://www.dmxapi.cn/v1/images/edits
```


## 🤖 模型名称

- `gpt-image-2`

## 🧪 图片编辑 示例代码

```python
import base64
import requests
from pathlib import Path

url = "https://www.dmxapi.cn/v1/images/edits"

api_key = "sk-rOQH5ITfGkp9pbvnIIbcQyPRCQclFUl8bSjD3dFRPeuDUQHl"
image_path = input("C:/Users/a1/Desktop/测试保存代码/a2.png").strip()
prompt = input("背景换成星空").strip()

# 读取图片并转成 base64
with open(image_path, "rb") as f:
    image_base64 = base64.b64encode(f.read()).decode("utf-8")

# 如果接口要求 data URL 格式，可以改成下面这一行
# image_base64 = f"data:image/{Path(image_path).suffix.lstrip('.')};base64,{image_base64}"

body = {
    "image": image_base64,
    "prompt": prompt
}

response = requests.post(
    url,
    data=body,
    headers={
        "Authorization": f"Bearer {api_key}"
    }
)

print(response.status_code)
print(response.text)
```

## 📦 返回示例

```text
status: 200
saved output\edited_20260422_194855_1.png
```

<p align="center">
  <small>© 2026 DMXAPI gpt-image-2 图片编辑</small>
</p>
