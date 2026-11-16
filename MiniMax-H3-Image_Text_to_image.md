# MiniMax-H3-Image 文生图 API 使用文档

基于 MiniMax-H3-Image 的文生图接口，调用 `POST /v1/images/generations` 同步返回图片。标准版 `MiniMax-H3-Image` 与极速版 `MiniMax-H3-Image-Highspeed` 参数相同。

## 接口地址

| 接口 | 请求方式 | URL |
|------|---------|-----|
| 文生图（非流式 / 流式） | POST | `https://www.dmxapi.cn/v1/images/generations` |

流式与非流式是同一条地址。流式在请求体中设置 `stream: true`，且 `response_format` 只能是 `url`。

:::warning
请妥善保管您的 API Key！严禁将密钥泄露给他人、硬编码到代码中或提交到公开的代码仓库。如果怀疑密钥已泄露，请立即前往 DMXAPI 官网重新生成。
:::

## 模型名称

- `MiniMax-H3-Image`
- `MiniMax-H3-Image-Highspeed`

## 完整代码示例

用上方标签切换非流式和流式。两者是同一条地址，流式在请求体里加 `stream: true`，`response_format` 只能是 `url`。

::: code-group

```python [非流式]
import requests
import json
import os
import base64
from urllib.parse import urlparse

# ===============================================================
# 步骤1: 配置 API 连接信息
# ===============================================================

# DMXAPI 服务端点地址
url = "https://www.dmxapi.cn/v1/images/generations"

# DMXAPI 密钥 (请替换为您自己的密钥)
# 获取方式: 登录 DMXAPI 官网 -> 个人中心 -> API 密钥管理
api_key = "sk-******************************************"

# 图片保存目录
output_dir = "output"

# 客户端超时（秒）。官方服务端最长等待 600 秒，客户端必须不小于 600。
# 这个接口不幂等：超时或断开后服务端仍会继续生成，成功的图照样计费；重试会再生成并再次计费。
timeout = 620

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
    # 可选值:
    #   - "MiniMax-H3-Image"(标准版)
    #   - "MiniMax-H3-Image-Highspeed"(极速版，参数与标准版相同)
    "model": "MiniMax-H3-Image",

    # 【prompt】(string, 必填) 文本描述
    # 按 Unicode 字符计，不含首尾空白，最长 32000。空白 prompt 返回 400。
    "prompt": "哈苏镜头效果下的花海",

    # 【disable_prompt_enhanced】(boolean, 可选) 是否关闭提示词增强
    # 默认 false，开启增强。增强后的文本见响应 data[].revised_prompt。
    # 设为 true 时直接使用原始 prompt，模型大约只读取前 4096 个 token，超出部分不生效。
    # 此时输出比例必须由请求给出，否则返回 400，二选一：
    #   - size 写成「宽x高」
    #   - size 不传或为 auto，并且 aspect_ratio 写成「X:Y」（area 可不传，默认 4K）
    # size 不是「宽x高」、同时 aspect_ratio 不传或为 auto，会返回 400。
    "disable_prompt_enhanced": False,

    # 【n】(integer, 可选) 生成数量
    # 取值范围 [1, 10]，默认 1。
    # data 的长度始终等于 n，和请求顺序对齐。只对成功的图片计费，失败项不算。
    "n": 1,

    # 【aspect_ratio】(string, 可选) 宽高比
    # 只在 size 不传或为 auto 时使用，默认 auto（由提示词决定）。
    # 可选值: "auto" 或 "X:Y"。X、Y 是 1 到 300 的整数，宽高比含边界 1:3 到 3:1。
    # 与下面的 size「宽x高」二选一。改用「宽x高」时，本字段和 area 都不能再传，传了返回 400，即使值是 auto。
    "aspect_ratio": "16:9",

    # 【area】(string, 可选) 面积档位
    # 只在 size 不传或为 auto 时使用，默认 4K。
    # 可选值: "1K" / "2K" / "4K"，分别按 1024²、2048²、4096² 的面积生成。
    # 这是面积，不是固定成 1024x1024。实际宽高还要看 aspect_ratio。
    "area": "1K",

    # 【size】(string, 可选) 精确输出尺寸
    # 默认 auto。写成「宽x高」时，宽和高必须是正整数，面积含边界 655360 到 20000000，
    # 宽高比含边界 1:3 到 3:1。不合规不缩放、不取整，直接返回 400。
    # 使用「宽x高」时不能再传 aspect_ratio 和 area，即使它们的值是 auto。
    # 下面这行是 2K 的 16:9 预设，不是上面 area=1K 的结果。启用时请删掉 aspect_ratio 和 area。
    # 常用预设：
    #   2K 1:1 2048x2048，4:3 2368x1760，16:9 2720x1536，3:1 3552x1184，竖图把宽高对调
    #   4K 1:1 4096x4096，4:3 4736x3552，16:9 5472x3072，3:1 7104x2368
    # 16:9 的 4K 不是 2720 乘 2。2720 乘 2 是 5440，官方预设和实测都是 5472x3072。
    # "size": "2720x1536",

    # 【output_format】(string, 可选) 图片格式
    # 默认 jpeg。可选值: "png" / "jpeg" / "jpg" / "webp"。
    # jpg 与 jpeg 等价，响应里的 output_format 写成 jpeg。
    "output_format": "png",

    # 【output_compression】(integer, 可选) 压缩质量
    # 取值范围 [0, 100]，默认 95。只对 jpeg / webp 生效，png 忽略。
    # 请求里的 jpg 按 jpeg 处理，所以也会压缩。
    "output_compression": 95,

    # 【response_format】(string, 可选) 返回方式
    # 可选值:
    #   - "url"(默认，图片地址 24 小时内有效)
    #   - "b64_json"(图片放在 data[].b64_json，不能和 stream: true 同时使用)
    # b64_json 按 n×宽×高 限制总面积，含边界：png 最大 20000000（约一张 4K），
    # jpeg / webp 最大 80000000（约四张 4K 或十张 2K）。size 为 auto 时，每张按 area 那一档的面积计算。
    "response_format": "url",

    # 【aigc_watermark】(boolean, 可选) 画面可见水印
    # 默认 false。true 时在画面上添加可见的 AIGC 标识。
    # 文件元数据里的隐式 AIGC 标识始终会写，不受这个参数控制。
    "aigc_watermark": False,
}

# ===============================================================
# 步骤4: 发送请求并输出结果
# ===============================================================

# 发送 POST 请求到 API 服务器
response = requests.post(url, headers=headers, json=payload, timeout=timeout)

# 格式化输出 JSON 响应
# - indent=2: 缩进 2 空格，便于阅读
# - ensure_ascii=False: 正确显示中文字符
# 至少一张成功才是 200。部分失败时 data 里对应项只有 error。
# 全部失败时上游是 402、422 或 500，网关会改成自己的 error。
result = response.json()
print(json.dumps(result, indent=2, ensure_ascii=False))

if response.status_code == 200:
    os.makedirs(output_dir, exist_ok=True)
    output_format = result.get("output_format") or "jpeg"
    if output_format == "jpg":
        output_format = "jpeg"
    for index, item in enumerate(result.get("data") or []):
        if "error" in item:
            print(f"第 {index} 张失败:", item["error"].get("message"))
            continue
        output_path = os.path.join(output_dir, f"minimax-h3-{index}.{output_format}")
        if payload["response_format"] == "b64_json":
            with open(output_path, "wb") as image_file:
                image_file.write(base64.b64decode(item["b64_json"]))
        else:
            image_url = item["url"]
            parsed = urlparse(image_url)
            if parsed.scheme not in ("http", "https") or not parsed.netloc:
                raise SystemExit(f"拒绝下载非法地址: {image_url}")
            download_headers = {}
            if parsed.netloc.endswith("dmxapi.cn"):
                download_headers["Authorization"] = api_key
            image_response = requests.get(image_url, headers=download_headers, timeout=timeout)
            content_type = image_response.headers.get("Content-Type", "")
            if image_response.status_code != 200 or not content_type.startswith("image/"):
                raise SystemExit(f"下载失败 {image_response.status_code}: {image_response.text[:300]}")
            with open(output_path, "wb") as image_file:
                image_file.write(image_response.content)
        print("已保存:", output_path)
```

```python [流式]
import requests
import json
import os
from urllib.parse import urlparse

# ===============================================================
# 步骤1: 配置 API 连接信息
# ===============================================================

# DMXAPI 服务端点地址
# 流式不是单独的路径，仍是文生图地址，加上 stream: true。
# 编辑也一样，把地址换成 /v1/images/edits 并带上 images，事件名里的 image_generation 换成 image_edit。
url = "https://www.dmxapi.cn/v1/images/generations"

# DMXAPI 密钥 (请替换为您自己的密钥)
# 获取方式: 登录 DMXAPI 官网 -> 个人中心 -> API 密钥管理
api_key = "sk-******************************************"

# 图片保存目录
output_dir = "output"

# 客户端超时（秒）。官方服务端最长等待 600 秒，客户端必须不小于 600。
# 响应头大约在第一个保活注释前返回，之后每 15 秒一条 `: keepalive`。
# 这个接口不幂等：超时或断开后服务端仍会继续生成，成功的图照样计费；重试会再生成并再次计费。
# 响应头返回之前的失败是普通 HTTP 错误，网关使用自己的 error 格式。响应头返回之后才是 SSE。
timeout = 620

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
    # 可选值:
    #   - "MiniMax-H3-Image"(标准版)
    #   - "MiniMax-H3-Image-Highspeed"(极速版，参数与标准版相同)
    "model": "MiniMax-H3-Image-Highspeed",

    # 【prompt】(string, 必填) 文本描述
    # 按 Unicode 字符计，不含首尾空白，最长 32000。空白 prompt 返回 400。
    "prompt": "哈苏镜头效果，模拟第三人称的单机游戏，主角在森林里穿着牛仔经典服饰骑着马举着左轮手枪，在追捕一个通缉犯，场景真实，逼真，有单机游戏的风格",

    # 【disable_prompt_enhanced】(boolean, 可选) 是否关闭提示词增强
    # 默认 false，开启增强。增强后的文本见 partial_succeeded 事件里的 revised_prompt。
    # 设为 true 时直接使用原始 prompt，模型大约只读取前 4096 个 token，超出部分不生效。
    # 此时输出比例必须由请求给出，否则返回 400，二选一：
    #   - size 写成「宽x高」
    #   - size 不传或为 auto，并且 aspect_ratio 写成「X:Y」（area 可不传，默认 4K）
    # size 不是「宽x高」、同时 aspect_ratio 不传或为 auto，会返回 400。
    "disable_prompt_enhanced": False,

    # 【stream】(boolean, 可选) 是否流式返回
    # 默认 false。true 时返回 text/event-stream，并且 response_format 必须是 url，b64_json 会返回 400。
    "stream": True,

    # 【n】(integer, 可选) 生成数量
    # 取值范围 [1, 10]，默认 1。
    # 事件按完成先后到达，不一定按 image_index 排序。image_index 从 0 开始，范围 [0, n-1]。只对成功的图片计费。
    "n": 1,

    # 【aspect_ratio】(string, 可选) 宽高比
    # 只在 size 不传或为 auto 时使用，默认 auto（由提示词决定）。
    # 可选值: "auto" 或 "X:Y"。X、Y 是 1 到 300 的整数，宽高比含边界 1:3 到 3:1。
    # 与下面的 size「宽x高」二选一。改用「宽x高」时，本字段和 area 都不能再传，传了返回 400，即使值是 auto。
    "aspect_ratio": "16:9",

    # 【area】(string, 可选) 面积档位
    # 只在 size 不传或为 auto 时使用，默认 4K。
    # 可选值: "1K" / "2K" / "4K"，分别按 1024²、2048²、4096² 的面积生成。
    # 这是面积，不是固定成 1024x1024。实际宽高还要看 aspect_ratio。
    "area": "1K",

    # 【size】(string, 可选) 精确输出尺寸
    # 默认 auto。写成「宽x高」时，宽和高必须是正整数，面积含边界 655360 到 20000000，
    # 宽高比含边界 1:3 到 3:1。不合规不缩放、不取整，直接返回 400。
    # 使用「宽x高」时不能再传 aspect_ratio 和 area，即使它们的值是 auto。
    # 下面这行是 2K 的 16:9 预设，不是上面 area=1K 的结果。启用时请删掉 aspect_ratio 和 area。
    # "size": "2720x1536",

    # 【output_format】(string, 可选) 图片格式
    # 默认 jpeg。可选值: "png" / "jpeg" / "jpg" / "webp"。
    # jpg 与 jpeg 等价，事件里的 output_format 写成 jpeg。
    "output_format": "png",

    # 【output_compression】(integer, 可选) 压缩质量
    # 取值范围 [0, 100]，默认 95。只对 jpeg / webp 生效，png 忽略。
    # 请求里的 jpg 按 jpeg 处理，所以也会压缩。
    "output_compression": 95,

    # 【response_format】(string, 可选) 返回方式
    # 默认 url。流式时只能是 "url"。图片地址 24 小时内有效，在 partial_succeeded 的 url 字段。
    "response_format": "url",

    # 【aigc_watermark】(boolean, 可选) 画面可见水印
    # 默认 false。true 时在画面上添加可见的 AIGC 标识。
    # 文件元数据里的隐式 AIGC 标识始终会写，不受这个参数控制。
    "aigc_watermark": False,
}

# ===============================================================
# 步骤4: 发送请求并输出结果
# ===============================================================

# 发送 POST 请求到 API 服务器
response = requests.post(url, headers=headers, json=payload, timeout=timeout, stream=True)

# 先看 HTTP 状态。响应头之前的错误不是 SSE，按 JSON 文本打印。
print("状态码:", response.status_code)
if response.status_code != 200:
    print(response.text)
    raise SystemExit("生成失败")

# 事件类型:
#   image_generation.partial_succeeded  一张成功。url、image_index、size、revised_prompt 在 JSON 顶层
#   image_generation.partial_failed     一张失败。message、code、image_index 在 JSON 顶层
#   image_generation.completed          至少一张成功后的结束事件，带 usage 和 request_id
#   error                               一张都没成功，或响应头已发出但还没开始生成就失败。不计费，usage 全是 0
# 每行 `event:` 只重复 type，这里只解析 `data:`。`: keepalive` 是保活注释，跳过。
os.makedirs(output_dir, exist_ok=True)
for raw_line in response.iter_lines(decode_unicode=True):
    if not raw_line:
        continue
    line = raw_line.strip()
    if not line.startswith("data:"):
        continue
    data_text = line[len("data:"):].strip()
    if data_text == "[DONE]":
        continue
    event = json.loads(data_text)
    print(json.dumps(event, indent=2, ensure_ascii=False))
    event_type = event.get("type", "")
    if event_type == "image_generation.partial_succeeded":
        image_index = event["image_index"]
        output_format = event.get("output_format") or "jpeg"
        if output_format == "jpg":
            output_format = "jpeg"
        output_path = os.path.join(output_dir, f"minimax-h3-stream-{image_index}.{output_format}")
        image_url = event["url"]
        parsed = urlparse(image_url)
        if parsed.scheme not in ("http", "https") or not parsed.netloc:
            raise SystemExit(f"拒绝下载非法地址: {image_url}")
        download_headers = {}
        if parsed.netloc.endswith("dmxapi.cn"):
            download_headers["Authorization"] = api_key
        image_response = requests.get(image_url, headers=download_headers, timeout=timeout)
        content_type = image_response.headers.get("Content-Type", "")
        if image_response.status_code != 200 or not content_type.startswith("image/"):
            raise SystemExit(f"下载失败 {image_response.status_code}: {image_response.text[:300]}")
        with open(output_path, "wb") as image_file:
            image_file.write(image_response.content)
        print("已保存:", output_path)
    elif event_type == "error":
        raise SystemExit("生成失败")
```

:::

## 返回示例

::: code-group

```json [非流式]
{
  "created": 1794563550,
  "data": [
    {
      "url": "https://hailuo-image-algeng-data.oss-cn-wulanchabu.aliyuncs.com/h3_image%2F1782658868262748430%2F20261113%2F462891946582596_0.png?Expires=1794649950&OSSAccessKeyId=LTAI5tB2SwrRwAtD23etQUbC&Signature=VMfLXCJ8J7gTISGMsSJf5GOil%2Bw%3D",
      "size": "1360x768",
      "revised_prompt": "The image is a professional studio portrait photograph of a cute little Golden Retriever puppy sitting squarely on a soft beige blanket. The puppy is centered in the frame, facing the camera directly with a relaxed, endearing expression. It has a thick, golden-brown coat, floppy ears with silky fur, and large, dark, glossy eyes that reflect the studio lights. Its small black nose and slightly open mouth with a tiny pink tongue out convey a playful mood. The front paws are planted firmly on the blanket, while the hind legs rest naturally in a seated pose. The lighting is soft and bright, with a key light coming from the upper left to illuminate the puppy's face and cast a gentle shadow toward the lower right. The background is a softly blurred neutral warm gray backdrop with a subtle vignette, keeping all visual focus on the puppy. A small light-colored wooden toy bone is placed on the lower left side of the blanket as a prop. The image uses a sharp focal depth on the puppy's face and body, with the background and prop softly out of focus."
    }
  ],
  "output_format": "png",
  "usage": {
    "generated_images": 1,
    "total_tokens": 7503,
    "input_tokens": 3423,
    "output_tokens": 4080,
    "input_tokens_details": {
      "text_tokens": 3423,
      "image_tokens": 0
    },
    "output_tokens_details": {
      "image_tokens": 4080
    }
  },
  "request_id": "074610d7a6160178344b4f5ea6317dcf"
}
已保存: output\minimax-h3-0.png
```

```text [流式]
event: image_generation.partial_succeeded
data: {"type":"image_generation.partial_succeeded","created":1792308690,"model":"MiniMax-H3-Image-Highspeed","image_index":0,"url":"https://example.com/h3-image/output-0.png","size":"2720x1536","output_format":"png","revised_prompt":"哈苏镜头下的第三人称单机游戏画面：主角穿着牛仔服饰，骑在马上举着左轮手枪，在写实的森林里追捕通缉犯，电影级光影"}

event: image_generation.completed
data: {"type":"image_generation.completed","created":1792308695,"model":"MiniMax-H3-Image-Highspeed","usage":{"generated_images":1,"total_tokens":7254,"input_tokens":3174,"output_tokens":4080,"input_tokens_details":{"text_tokens":3174,"image_tokens":0},"output_tokens_details":{"image_tokens":4080}},"request_id":"021792308678142a2c883cf675b9804d"}
```

:::

<p align="center">
  <small>© 2026 DMXAPI MiniMax-H3-Image 文生图</small>
</p>
