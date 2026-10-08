# Qwen3.8-Omni-Flash 多模态输入 API 使用文档

基于 Qwen3.8-Omni-Flash 全模态模型的多模态理解接口，通过 `/v1/chat/completions` 端点在同一条 user 消息中组合文本、图片、音频和视频输入，并以文本形式流式返回分析结果。图片单张不超过 20MB（URL 方式最多 2048 张），音频最长 3 小时，视频单个文件不超过 2GB、时长不超过 2 小时、最多 64 个且可理解视频中的音频轨；支持 `use_multichannel` 解析双通道 / 四通道空间音频，`vl_high_resolution_images` 可将图片 Token 上限从 1280 提升至 16384。本示例演示一次性提交图片、音频、视频三种媒体与文本提示词的调用方式。

## 接口地址

| 接口 | 请求方式 | URL |
|------|---------|-----|
| 多模态输入 | POST | `https://www.dmxapi.cn/v1/chat/completions` |

:::warning
请妥善保管您的 API Key！严禁将密钥泄露给他人、硬编码到代码中或提交到公开的代码仓库。如果怀疑密钥已泄露，请立即前往 DMXAPI 官网重新生成。
:::

## 模型名称

- `qwen3.8-omni-flash`

## 支持的输入类型

- `text`：文本提示词。
- `image_url`：图片公网 URL 或 Base64 Data URL。
- `input_audio`：音频 URL 或 Base64 数据，并在 `format` 中指定格式。
- `video_url`：视频公网 URL 或 Base64 Data URL，可理解视频中的音频。
- `video`：视频帧图片列表（最少 2 张、最多 2048 张），帧图片可以是公网 URL，也可以是本地图片；只含帧画面，不能理解视频中的音频。

## 多模态输入示例代码

```python
import requests
import json
import base64
import mimetypes
import os

# ===============================================================
# 步骤1: 配置 API 连接信息
# ===============================================================

# DMXAPI 服务端点地址
url = "https://www.dmxapi.cn/v1/chat/completions"

# DMXAPI 密钥 (请替换为您自己的密钥)
# 获取方式: 登录 DMXAPI 官网 -> 个人中心 -> API 密钥管理
api_key = "sk-******************************************"

# ===============================================================
# 步骤2: 配置媒体地址
# ===============================================================

# 官方输入限制:
# 图片: 宽和高均大于 10 像素，宽高比不超过 200:1；单张不超过 20MB
#       URL 方式最多 2048 张，Base64 方式最多 250 张
# 音频: 时长不超过 3 小时，URL 方式单个不超过 2GB、最多 2048 个
# 视频: 单个文件不超过 2GB，时长不超过 2 小时，最多 64 个
# 本地文件转 Base64 后的字符串必须小于 10MB，更大的文件请使用公网 URL

# 必须替换成模型可以访问的公网地址
# 也可以改成本地文件路径，程序会自动转换为 Base64 Data URL
image_url = "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241022/emyrja/dog_and_girl.jpeg"
# 例如本地图片路径:
# image_url = r"C:\Users\a1\Pictures\homelander.webp"

audio_url = "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250211/tixcef/cherry.wav"
# 例如本地音频路径:
# audio_url = r"C:\Users\a1\Desktop\test\cherry.wav"

video_url = "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241115/cqqkru/1.mp4"
# 例如本地视频路径:
# video_url = r"C:\Users\a1\Desktop\test\video.mp4"

# ===============================================================
# 步骤3: 配置请求头
# ===============================================================

headers = {
    "Content-Type": "application/json",      # 指定请求体为 JSON 格式
    "Authorization": f"Bearer {api_key}",    # Bearer token 认证方式
}

# ===============================================================
# 步骤4: 配置请求参数
# ===============================================================

payload = {
    # 【model】(string, 必填) 调用的模型名称
    "model": "qwen3.8-omni-flash",

    # 【messages】(array, 必填) 对话消息列表，按时间顺序排列
    # 音频 / 视频输入仅允许出现在 user 消息中
    "messages": [
        {
            # 【role】(string, 必填) 消息角色
            # 可选值: "system"(系统提示，设定助手行为) / "user"(用户输入) / "assistant"(助手回复，用于多轮对话)
            "role": "user",

            # 【content】(array, 必填) 多模态消息内容，由不同类型的输入对象组成
            "content": [
                {
                    # 【type】(string, 必填) 输入类型
                    # 可选值: "text"(文本) / "image_url"(图片) / "input_audio"(音频) / "video_url"(视频文件) / "video"(视频帧图片列表)
                    "type": "text",

                    # 【text】(string, 必填) 文本提示词内容
                    "text": (
                        "请严格分别分析以下三个输入："
                        "第一项是图片，第二项是音频，第三项是视频。"
                        "只根据实际收到的媒体内容回答。"
                        "不要引用不存在的文字描述，也不要臆造未提供的输入。"
                        "请分别输出：图片内容、音频内容、视频内容。"
                    ),
                },
                {
                    # 【type】"image_url": 图片输入
                    "type": "image_url",

                    # 【image_url】(object, 必填) 图片地址信息
                    "image_url": {
                        # 【url】(string, 必填) 图片公网 URL 或 Base64 Data URL
                        # 图片限制: 宽和高均大于 10 像素，宽高比不超过 200:1
                        # 单张不超过 20MB，URL 方式最多 2048 张，Base64 编码后须小于 10MB
                        "url": image_url,
                    },
                },
                {
                    # 【type】"input_audio": 音频输入
                    "type": "input_audio",

                    # 【input_audio】(object, 必填) 音频数据信息
                    "input_audio": {
                        # 【data】(string, 必填) 音频公网 URL 或 Base64 数据 (data:;base64,...)
                        # 音频限制: 时长不超过 3 小时，URL 方式单个不超过 2GB、最多 2048 个
                        "data": audio_url,

                        # 【format】(string, 必填) 音频格式
                        # 支持: AMR、WAV、3GP、3GPP、AAC、MP3 等
                        "format": "wav",
                    },
                },
                {
                    # 【type】"video_url": 视频文件输入，可理解视频中的音频
                    "type": "video_url",

                    # 【video_url】(object, 必填) 视频地址信息
                    "video_url": {
                        # 【url】(string, 必填) 视频公网 URL 或 Base64 Data URL
                        # 视频限制: 单个文件不超过 2GB、时长不超过 2 小时、最多 64 个
                        # 支持格式: MP4、AVI、MKV、MOV、FLV、WMV 等
                        "url": video_url,
                    },
                },
                # 视频也可以改用图片列表形式传入 (与 video_url 二选一):
                # 图片列表只包含帧画面，不能理解视频中的音频轨
                # 最少 2 张、最多 2048 张，每张图片的限制与 image_url 相同
                # 帧图片可以是公网 URL，也可以是本地图片
                # {
                #     "type": "video",
                #     "video": [
                #         "https://example.com/frame1.jpg",
                #         "https://example.com/frame2.jpg",
                #         "https://example.com/frame3.jpg",
                #         "https://example.com/frame4.jpg",
                #     ],
                # },
            ],
        }
    ],

    # 【modalities】(array, 可选) 输出模态
    # qwen3.8-omni-flash 仅支持文本输出，固定为 ["text"]
    "modalities": ["text"],

    # 【stream】(boolean, 可选) 是否使用流式输出
    "stream": True,

    # 【stream_options】(object, 可选) 流式输出选项，仅在 stream=True 时生效
    "stream_options": {
        # 【include_usage】(boolean, 可选) 在流末尾的最后一个数据块返回 Token 用量
        "include_usage": True,
    },

    # 【reasoning_effort】(string, 可选) 思考强度，不传时默认开启思考，默认值为 "xhigh"
    # 可选值: "none"(关闭思考) / "minimal" / "low" / "medium" / "high" / "xhigh" / "max"
    # 取值映射: "minimal" 按 "low" 处理，"high" 和 "max" 按 "xhigh" 处理
    "reasoning_effort": "none",

    # 注意: reasoning_effort 和 thinking_budget 不能同时设置，否则请求报错
    # "thinking_budget": 8192,

    # 【enable_search】(boolean, 可选) 是否开启联网搜索
    "enable_search": True,

    # 【search_options】(object, 可选) 联网搜索配置
    "search_options": {
        # 【search_strategy】(string, 可选) 搜索策略
        # 可选值: "agent"
        "search_strategy": "agent",
    },

    # 【use_multichannel】(boolean, 可选) 是否解析双通道或四通道空间音频，默认 False
    # 设为 True 时解析双通道 (左右) 或四通道 (FOA，WYZX 顺序) 空间音频
    # 普通单声道音频使用 False
    "use_multichannel": False,

    # 【vl_high_resolution_images】(boolean, 可选) 是否启用高分辨率图片处理，默认 False
    # 图片 Token 上限默认为 1280，设置为 True 时上限提升至 16384
    "vl_high_resolution_images": False,
}

# ===============================================================
# Token 计算规则 (官方)
# ===============================================================

# 音频输入: 总 Tokens = 音频时长(秒) × 7，不足 1 秒按 1 秒计
# 图片输入: 每 32×32 像素对应 1 个 Token，每张最少 24 个 Token
# 视频输入: 视觉与音频分开计费
#          视觉部分按 FPS=2 抽帧，帧像素下限 64×32×32、上限 640×32×32
#          最少 2 帧、最多 2048 帧，视频总像素上限 180224×32×32

# ===============================================================
# 步骤5: 定义本地文件转换函数
# ===============================================================

def convert_local_file_to_data_url(source, media_type):
    """
    支持以下输入方式：

    1. 公网 URL
    2. 已经是 Base64 Data URL
    3. 本地文件路径

    本地文件会自动转换成 Base64 Data URL。
    """

    if not isinstance(source, str) or not source.strip():
        raise ValueError("媒体地址或本地文件路径不能为空")

    source = source.strip()

    # 已经是公网 URL，直接使用
    if source.startswith(("http://", "https://")):
        return source

    # 已经是 Base64 Data URL，直接使用
    if source.startswith("data:"):
        return source

    # 本地文件不存在时直接报错
    if not os.path.isfile(source):
        raise FileNotFoundError(f"找不到本地文件：{source}")

    # 根据文件扩展名识别 MIME 类型
    mime_type, _ = mimetypes.guess_type(source)

    if not mime_type:
        extension = os.path.splitext(source)[1].lower()

        fallback_mime_types = {
            ".jpg": "image/jpeg",
            ".jpeg": "image/jpeg",
            ".png": "image/png",
            ".webp": "image/webp",
            ".gif": "image/gif",
            ".bmp": "image/bmp",
            ".wav": "audio/wav",
            ".mp3": "audio/mpeg",
            ".aac": "audio/aac",
            ".mp4": "video/mp4",
            ".mov": "video/quicktime",
            ".avi": "video/x-msvideo",
            ".mkv": "video/x-matroska",
        }

        mime_type = fallback_mime_types.get(extension)

    if not mime_type:
        raise ValueError(f"无法识别文件类型：{source}")

    # 读取本地文件并转换为 Base64
    with open(source, "rb") as file:
        encoded_data = base64.b64encode(file.read()).decode("utf-8")

    # 图片使用具体 MIME 类型
    if media_type == "image":
        return f"data:{mime_type};base64,{encoded_data}"

    # 音频和视频使用 data:;base64 格式
    return f"data:;base64,{encoded_data}"


# 将本地路径转换为 Base64 Data URL
# 如果传入的是公网 URL，则保持原 URL 不变
payload["messages"][0]["content"][1]["image_url"]["url"] = (
    convert_local_file_to_data_url(
        payload["messages"][0]["content"][1]["image_url"]["url"],
        "image",
    )
)

payload["messages"][0]["content"][2]["input_audio"]["data"] = (
    convert_local_file_to_data_url(
        payload["messages"][0]["content"][2]["input_audio"]["data"],
        "audio",
    )
)

payload["messages"][0]["content"][3]["video_url"]["url"] = (
    convert_local_file_to_data_url(
        payload["messages"][0]["content"][3]["video_url"]["url"],
        "video",
    )
)

# 如果启用了上面图片列表形式的 video，其中的本地图片也要逐帧转换，例如:
# video_item["video"] = [
#     convert_local_file_to_data_url(frame, "image")
#     for frame in video_item["video"]
# ]

# ===============================================================
# 步骤6: 定义流式响应解析函数
# ===============================================================

def read_stream(response):
    usage = None
    pending = ""

    for raw_line in response.iter_lines(decode_unicode=False):
        if not raw_line:
            continue

        # 强制使用 UTF-8，避免中文乱码
        line = raw_line.decode("utf-8", errors="replace").strip()

        if not line.startswith("data:"):
            continue

        data = line[5:].lstrip()

        if not data:
            continue

        if data == "[DONE]":
            break

        # 防止网关把一个 JSON 响应拆成多个片段
        pending += data

        try:
            chunk = json.loads(pending)
        except json.JSONDecodeError:
            continue

        pending = ""

        if chunk.get("usage"):
            usage = chunk["usage"]

        choices = chunk.get("choices") or []
        if not choices:
            continue

        delta = choices[0].get("delta") or {}

        # 思考开启时，思考内容通过 delta.reasoning_content 输出
        if delta.get("reasoning_content"):
            print(delta["reasoning_content"], end="", flush=True)

        # 正式回答通过 delta.content 输出
        if delta.get("content"):
            print(delta["content"], end="", flush=True)

    print()

    if pending:
        print("\n警告：流式响应结束时仍有未完成数据：")
        print(repr(pending[:500]))

    if usage:
        print("\nToken 用量：")
        print(json.dumps(usage, ensure_ascii=False, indent=2))

# ===============================================================
# 步骤7: 发送请求并输出结果
# ===============================================================

def main():
    response = requests.post(
        url,
        headers=headers,
        json=payload,
        stream=True,
        timeout=(30, 1000),
    )

    print("HTTP 状态码：", response.status_code)

    if response.status_code >= 400:
        print("错误响应：")
        print(response.text)

    response.raise_for_status()

    print("\n模型回复：")
    read_stream(response)


if __name__ == "__main__":
    main()
```

## 返回示例

```text
好的，我将严格根据您提供的三个媒体输入（一张图片、一段音频、一个视频）进行分析。

---

### 1. 图片内容 (Image Content)

这是一张在海滩上拍摄的温馨照片，捕捉了人与宠物之间亲密互动的瞬间。

- **主体**:
    - **人物**: 一位年轻女性坐在沙滩上，侧对着镜头。她留着深色长发，面带灿烂的笑容，眼睛微闭，表情非常愉悦和放松。她身穿一件蓝白格子的长袖衬衫和深色裤子。
    - **动物**: 一只黄色的拉布拉多犬或类似的寻回犬，正用后腿坐着，前爪搭在女子的手中，仿佛在和她“击掌”或玩耍。狗狗身上穿着一件带有彩色花纹的胸背带。

- **环境与背景**:
    - **地点**: 场景位于一片宽阔的沙滩上，沙子看起来很细腻。
    - **时间**: 从光线判断，这应该是日出或日落时分的“黄金时刻”。太阳的位置很低，光线温暖而柔和，在女子的头发和肩膀上形成了漂亮的轮廓光（逆光效果）。
    - **远景**: 背景是平静的海洋，可以看到一层层的海浪正在涌向岸边。天空和海面被夕阳/朝阳染上了一片温暖的金色调。

- **构图与氛围**:
    - 采用中景拍摄，将人物和狗作为画面的绝对焦点。
    - 整体氛围宁静、幸福、充满爱意，展现了人与动物和谐共处的美好关系。

---

### 2. 音频内容 (Audio Content)

这段音频包含两个部分：一段中文口语和一首歌曲。

- **第一部分 (00:00 - 00:09)**:
    - **语言**: 普通话（Mandarin Chinese）。
    - **内容**: 一位女性在描述一幅画面。她说：“嗯，这幅图啊，是在海滩上有个女人和一只狗在玩呢，背景是海浪拍打着沙滩，天空有点发白，应该是日出或者日落的时候吧。你要是还有啥想知道的尽管问哈。”
    - **分析**: 这段话语的内容与我上面分析的**图片内容**完全吻合。这表明该音频很可能是对那张图片的描述或解说。

- **第二部分 (00:10 - 00:23)**:
    - **类型**: 音乐。
    - **风格**: 这是一首节奏明快的华语流行歌曲（C-Pop），女声演唱。
    - **歌词片段**: “春色恼人那不得眠，春雨涨满池塘唤睡莲，春花开遍呢喃的燕，春风得意正少年。”
    - **氛围**: 歌曲充满了春天的气息，旋律欢快、积极，给人一种青春洋溢、心情舒畅的感觉。

---

### 3. 视频内容 (Video Content)

这是一个由AI生成的短视频，展示了一位女性的面部特写。

- **主体**:
    - 一位看起来很年轻的东亚女性，有着棕色的波波头短发和刘海。
    - 她穿着一件粉色的V领针织开衫，内搭白色T恤，脖子上戴着一条细细的项链。
    - 她的妆容自然，面带微笑，眼神温柔地看着镜头。

- **动作与变化**:
    - 视频的核心内容是这位女性的表情变化。她从开始的抿嘴微笑，逐渐变为张嘴大笑，露出了洁白的牙齿。整个过程中，她的头部有轻微的晃动，显得非常生动自然。
    - 这种连续且平滑的表情过渡是AI生成视频的常见特征。

- **技术与标识**:
    - **画质**: 视频画质清晰，色彩饱和度高，但人物的皮肤质感和光影效果略带一种“完美”的非真实感。
    - **水印**: 在视频的右上角，有一个清晰的标志和文字：“通义·AI合成”。这明确指出该视频是由阿里巴巴旗下的通义大模型技术生成的，并非真人实拍。

- **总结**: 这是一个展示AI数字人技术的演示视频，特点是能够生成逼真的人物形象和流畅的面部表情动画。

Token 用量：
{
  "completion_tokens": 848,
  "completion_tokens_details": {
    "text_tokens": 848
  },
  "prompt_tokens": 5437,
  "prompt_tokens_details": {
    "audio_tokens": 207,
    "cached_tokens": 0,
    "image_tokens": 1249,
    "text_tokens": 395,
    "video_tokens": 3586
  },
  "total_tokens": 6285
}
```

<p align="center">
  <small>© 2026 DMXAPI Qwen3.8-Omni-Flash 多模态输入</small>
</p>
