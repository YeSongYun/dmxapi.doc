# Agnes Image 2.5 Flash 图生图 API 文档

Sapiens AI 出品的图像生成模型，传入一张或多张参考图，按文字指令进行编辑或多图合成。参考图支持公网图片 URL 和本地图片（Data URI Base64）两种输入方式。接口同步返回，结果为图片 URL。

## 📌 接口地址

```text
https://www.dmxapi.cn/v1/images/generations
```

## 🎨 模型列表

- `agnes-image-2.5-flash`

## 💻 Python 示例代码

::: code-group

```python [图片 URL 输入]
import requests
import json

# Agnes Image 2.5 Flash 图生图示例(图片 URL 作为参考图，URL 输出)
# 官方文档: https://agnes-ai.com/zh-Hans/docs/agnes-image-25-flash

# ===============================================================
# 步骤1: 配置 API 连接信息
# ===============================================================

# DMXAPI 服务端点地址
url = "https://www.dmxapi.cn/v1/images/generations"

# DMXAPI 密钥 (请替换为您自己的密钥)
# 获取方式: 登录 DMXAPI 官网 -> 个人中心 -> API 密钥管理
api_key = "sk-******************************************"

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
    # 【prompt】(string, 必填) 图像编辑指令
    # 描述需要对参考图做的修改，不能为空，长度不超过 32000 个字符
    # 推荐结构: [改变要求] + [新风格 / 场景] + [需要添加或移除的元素] + [需要保留的元素]
    # 多图合成推荐结构: [参考图角色] + [目标场景] + [图像之间的关系] + [风格 / 光照 / 构图]
    "prompt": "让第一张图中的女生换上第二张图中的黑色连衣裙，保留她的面部、发型、姿态和背景，全身照",

    # 【extra_body】(object, 图生图必填) 高级工作流的附加参数
    # 图生图的参考图放在这里
    "extra_body": {
        # 【image】(string[], 图生图必填) 输入参考图列表
        # 支持公共 http(s) 图片 URL 或 Data URI Base64(data:image/png;base64,...)
        # 最多 16 张；使用 Data URI 时每张图片不超过 20 MiB
        # 多图合成时传入多张图片，数组顺序即参考图顺序，请在 prompt 中说明每张图的作用
        # 注意: URL 必须可公开直接访问，不能需要登录或 Cookie，且需从国内网络可访问(如 GitHub raw 地址会下载失败)；无法公开访问时请改用 Data URI
        # 计费: 参考图数量会计入用量，具体价格以 DMXAPI 模型价格页为准
        "image": [
            "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250925/thtclx/input1.png",   # 第一张: 人物
            "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250925/iclsnx/input2.png"    # 第二张: 服装
        ],
    },

    # 【model】(string, 必填) 调用的模型名称
    # 固定为 agnes-image-2.5-flash，每次请求生成 1 张图片
    "model": "agnes-image-2.5-flash",

    # 【ratio】(string, 可选) 图片宽高比
    # 与档位式 size 配合使用，默认值 "1:1"；size 填写精确像素尺寸时请删除本字段
    # 可选值: "1:1" / "3:4" / "4:3" / "16:9" / "9:16" / "2:3" / "3:2" / "21:9"
    # 各档位对应的宽高像素值:
    #   - 1K: 1:1 1024×1024、3:4 864×1152、4:3 1152×864、16:9 1312×736、
    #         9:16 736×1312、2:3 832×1248、3:2 1248×832、21:9 1568×672
    #   - 2K: 1:1 2048×2048、3:4 1728×2304、4:3 2304×1728、16:9 2624×1472、
    #         9:16 1472×2624、2:3 1664×2496、3:2 2496×1664、21:9 3136×1344
    #   - 3K: 1:1 3072×3072、3:4 2592×3456、4:3 3456×2592、16:9 3936×2208、
    #         9:16 2208×3936、2:3 2496×3744、3:2 3744×2496、21:9 4704×2016
    #   - 4K: 1:1 4096×4096、3:4 3456×4608、4:3 4608×3456、16:9 5248×2944、
    #         9:16 2944×5248、2:3 3328×4992、3:2 4992×3328、21:9 6272×2688
    "ratio": "3:4",

    # 【size】(string, 必填) 输出尺寸档位
    # 可选值: "1K" / "2K" / "3K" / "4K"(推荐，配合 ratio 使用)
    # 也兼容 "1024x768" 这类精确像素写法(宽、高各 16 ~ 8192 像素)，但不支持的尺寸可能会被自动标准化
    # 例如 "1920x1080" 可能被映射为 16:9 的 1K 输出 1312×736；
    # 需要 16:9 显示素材时建议使用 size "2K" + ratio "16:9"，再在下游裁剪或缩放
    "size": "4K",
}

# ===============================================================
# 步骤4: 发送请求并输出结果
# ===============================================================

# 发送 POST 请求到 API 服务器
# 接口为同步返回，生成通常需要数秒到几十秒，这里把超时设置为 300 秒
response = requests.post(url, headers=headers, json=payload, timeout=300)

# 格式化输出 JSON 响应
# 成功时结构为 {"created": ..., "data": [{"url": ..., "revised_prompt": ...}]}
# 图片 URL 位于 data[0].url；失败时返回 {"error": {"message": ...}}
# - indent=2: 缩进 2 空格，便于阅读
# - ensure_ascii=False: 正确显示中文字符
print(json.dumps(response.json(), indent=2, ensure_ascii=False))
```

```python [本地图片输入]
import requests
import json
import base64

# Agnes Image 2.5 Flash 图生图示例(本地图片转 Data URI 作为参考图，URL 输出)
# 官方文档: https://agnes-ai.com/zh-Hans/docs/agnes-image-25-flash

# ===============================================================
# 步骤1: 配置 API 连接信息
# ===============================================================

# DMXAPI 服务端点地址
url = "https://www.dmxapi.cn/v1/images/generations"

# DMXAPI 密钥 (请替换为您自己的密钥)
# 获取方式: 登录 DMXAPI 官网 -> 个人中心 -> API 密钥管理
api_key = "sk-******************************************"

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
    # 【prompt】(string, 必填) 图像编辑指令
    # 描述需要对参考图做的修改，不能为空，长度不超过 32000 个字符
    # 推荐结构: [改变要求] + [新风格 / 场景] + [需要添加或移除的元素] + [需要保留的元素]
    # 多图合成推荐结构: [参考图角色] + [目标场景] + [图像之间的关系] + [风格 / 光照 / 构图]
    "prompt": "把图一和图二完美融合起来",

    # 【extra_body】(object, 图生图必填) 高级工作流的附加参数
    # 图生图的参考图放在这里
    "extra_body": {
        # 【image】(string[], 图生图必填) 输入参考图列表
        # 本地图片直接填文件路径(支持 PNG / JPEG / WebP / GIF / BMP)，发送前会自动转成 Data URI
        # 也可以填公共 http(s) 图片 URL，两种写法可以混用
        # 最多 16 张；本地图片每张不超过 20 MiB
        # 多图合成时传入多张图片，数组顺序即参考图顺序，请在 prompt 中说明每张图的作用
        # 注意: URL 必须可公开直接访问，不能需要登录或 Cookie；无法公开访问时请改用本地图片路径
        # 计费: 参考图数量会计入用量，具体价格以 DMXAPI 模型价格页为准
        "image": [
            r"./input/image1.jpg",
            r"./input/image2.png",
        ],
    },

    # 【model】(string, 必填) 调用的模型名称
    # 固定为 agnes-image-2.5-flash，每次请求生成 1 张图片
    "model": "agnes-image-2.5-flash",

    # 【ratio】(string, 可选) 图片宽高比
    # 与档位式 size 配合使用，默认值 "1:1"；size 填写精确像素尺寸时请删除本字段
    # 可选值: "1:1" / "3:4" / "4:3" / "16:9" / "9:16" / "2:3" / "3:2" / "21:9"
    # 各档位对应的宽高像素值:
    #   - 1K: 1:1 1024×1024、3:4 864×1152、4:3 1152×864、16:9 1312×736、
    #         9:16 736×1312、2:3 832×1248、3:2 1248×832、21:9 1568×672
    #   - 2K: 1:1 2048×2048、3:4 1728×2304、4:3 2304×1728、16:9 2624×1472、
    #         9:16 1472×2624、2:3 1664×2496、3:2 2496×1664、21:9 3136×1344
    #   - 3K: 1:1 3072×3072、3:4 2592×3456、4:3 3456×2592、16:9 3936×2208、
    #         9:16 2208×3936、2:3 2496×3744、3:2 3744×2496、21:9 4704×2016
    #   - 4K: 1:1 4096×4096、3:4 3456×4608、4:3 4608×3456、16:9 5248×2944、
    #         9:16 2944×5248、2:3 3328×4992、3:2 4992×3328、21:9 6272×2688
    "ratio": "3:4",

    # 【size】(string, 必填) 输出尺寸档位
    # 可选值: "1K" / "2K" / "3K" / "4K"(推荐，配合 ratio 使用)
    # 也兼容 "1024x768" 这类精确像素写法(宽、高各 16 ~ 8192 像素)，但不支持的尺寸可能会被自动标准化
    # 例如 "1920x1080" 可能被映射为 16:9 的 1K 输出 1312×736；
    # 需要 16:9 显示素材时建议使用 size "2K" + ratio "16:9"，再在下游裁剪或缩放
    "size": "4K",
}

# ===============================================================
# 步骤4: 发送请求并输出结果
# ===============================================================

# 把 image 中的本地图片路径转成 Data URI(图片格式根据文件内容自动识别)，此段无需修改
image_data_uris = []
for image_path in payload["extra_body"]["image"]:
    if image_path.startswith(("http://", "https://", "data:")):
        image_data_uris.append(image_path)
        continue
    with open(image_path, "rb") as f:
        image_bytes = f.read()
    if image_bytes.startswith(b"\x89PNG"):
        mime_type = "image/png"
    elif image_bytes.startswith(b"\xff\xd8"):
        mime_type = "image/jpeg"
    elif image_bytes.startswith(b"RIFF") and image_bytes[8:12] == b"WEBP":
        mime_type = "image/webp"
    elif image_bytes.startswith(b"GIF8"):
        mime_type = "image/gif"
    elif image_bytes.startswith(b"BM"):
        mime_type = "image/bmp"
    else:
        raise ValueError(f"无法识别的图片格式: {image_path}")
    image_data_uris.append(f"data:{mime_type};base64," + base64.b64encode(image_bytes).decode("utf-8"))
payload["extra_body"]["image"] = image_data_uris

# 发送 POST 请求到 API 服务器
# 接口为同步返回，生成通常需要数秒到几十秒，这里把超时设置为 300 秒
response = requests.post(url, headers=headers, json=payload, timeout=300)

# 格式化输出 JSON 响应
# 成功时结构为 {"created": ..., "data": [{"url": ..., "revised_prompt": ...}]}
# 图片 URL 位于 data[0].url；失败时返回 {"error": {"message": ...}}
# - indent=2: 缩进 2 空格，便于阅读
# - ensure_ascii=False: 正确显示中文字符
print(json.dumps(response.json(), indent=2, ensure_ascii=False))
```

:::

## 📤 返回示例

```json
{
  "created": 1795443363,
  "data": [
    {
      "revised_prompt": "",
      "url": "https://cos-platform-outputs.agnes-ai.cn/images/i2i/task_XPI2uaf9a2JSR0U8D5jwAVYxgGW4E12F/output.png"
    }
  ]
}
```



<p align="center">
  <small>© 2026 DMXAPI Agnes Image 2.5 Flash 图生图 API 文档</small>
</p>
