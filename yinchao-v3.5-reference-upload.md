# yinchao-v3.5 上传参考音频 API 使用文档

要用本地音频仿写，先把文件上传到 DMXAPI。上传接口同步返回一个 `task_` 开头的 `id`，可以直接用它提交仿写。已有公网音频直链或已完成的音潮作品时，可以直接进入下一步。[参考音频仿写](/yinchao-v3.5-reference-to-song)

## 接口地址

| 接口 | 请求方式 | URL |
| --- | --- | --- |
| 上传参考音频 | POST（`multipart/form-data`） | `https://www.dmxapi.cn/yinchao/api/v1/file/upload` |

## 模型名称

`yinchao-v3.5`

## 上传参考音频示例代码


```python
import requests
import json
from pathlib import Path

# ===============================================================
# 步骤1: 配置 API 连接信息
# ===============================================================

url = "https://www.dmxapi.cn/yinchao/api/v1/file/upload"
api_key = "sk-******************************************"  # 填写自己的 DMXAPI 密钥
file_path = Path("reference.mp3")  # 替换为本地 MP3 或 WAV 文件路径

# ===============================================================
# 步骤2: 配置请求头
# ===============================================================

# requests 会根据 files 自动设置 multipart/form-data 和 boundary。
headers = {"Authorization": f"{api_key}"}

# ===============================================================
# 步骤3: 配置请求参数
# ===============================================================

form_data = {
    # 【upload_type】(string, 可选) 上传用途，默认值为 reference。
    "upload_type": "reference",

    # 【model】(string, 可选) 上传参考音频使用 yinchao-v3.5。
    "model": "yinchao-v3.5",
}

# ===============================================================
# 步骤4: 发送请求并输出结果
# ===============================================================

def main():
    mime_types = {".mp3": "audio/mpeg", ".wav": "audio/wav"}
    mime_type = mime_types.get(file_path.suffix.lower())
    if not file_path.is_file() or not mime_type:
        raise ValueError("请在步骤1填写一个存在的 MP3 或 WAV 文件路径。")
    if not 0 < file_path.stat().st_size <= 10 * 1024 * 1024:
        raise ValueError("参考音频不能为空，大小上限为 10 MB。")

    with file_path.open("rb") as audio:
        # 【file】(file, 必填) 参考音频的二进制文件内容。
        files = {"file": (file_path.name, audio, mime_type)}
        response = requests.post(url, headers=headers, data=form_data, files=files)

    if not response.ok:
        print(response.text)
        response.raise_for_status()
    print(json.dumps(response.json(), indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
```

## 返回示例

下面是一次真实请求的原始返回。`id` 是这次上传的网关任务 ID，可在仿写时作为 `task_id` 使用。

```json
{
  "id": "task_2HNosKEnIO07asPrGWzcJHA9YbbmjsdK",
  "usage": {
    "cost": "¥0"
  }
}
```

<p align="center">
  <small>© 2026 DMXAPI yinchao-v3.5 上传参考音频</small>
</p>
