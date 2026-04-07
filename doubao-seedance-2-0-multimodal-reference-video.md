# doubao-seedance-2-0-260128 多模态参考生视频 API 使用文档

基于豆包 Seedance 2.0 模型的多模态参考生视频接口，支持同时输入参考图片（1~9 张）、参考视频（1~3 个）、参考音频（1~3 段）及文本提示词，生成高度贴合参考素材的目标视频。支持生成全新视频、编辑视频和延长视频三种创作模式，可生成时长 4~15 秒、最高 720p 分辨率的有声视频。采用异步任务模式，提交后通过独立查询接口获取结果。

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


## 🎥 多模态参考生视频 示例代码

```python
import requests
import json

# 步骤1: 配置 API 连接信息
url = "https://www.dmxapi.cn/v1/responses"
api_key = "sk-******************************************"

# 步骤2: 配置请求头
headers = {
    "Content-Type": "application/json",
    # token 认证方式，注意此处不加 Bearer 前缀
    "Authorization": f"{api_key}",
}

# 步骤3: 配置请求参数
payload = {
    # 【model】(string, 必填) 模型 ID
    "model": "doubao-seedance-2-0-260128",

    # 【input】(array, 必填) 多模态输入内容数组
    # 支持文本、图片（1~9 张）、视频（1~3 个）、音频（1~3 段）
    # 注意：不可单独传入音频，必须至少包含 1 个参考图片或视频
    "input": [
        {
            # 【type】(string, 必填) 输入类型，此处为文本提示词
            "type": "text",
            # 【text】(string, 可选) 文本提示词，建议中文不超过 500 字
            # 可用 "[图1]xxx，[图2]xxx" 格式指定多张图片的组合
            "text": "全程使用视频1的第一视角构图，全程使用音频1作为背景音乐。第一人称视角果茶宣传广告，seedance牌「苹苹安安」苹果果茶限定款；首帧为图片1，你的手摘下一颗带晨露的阿克苏红苹果，轻脆的苹果碰撞声；2-4 秒：快速切镜，你的手将苹果块投入雪克杯，加入冰块与茶底，用力摇晃，冰块碰撞声与摇晃声卡点轻快鼓点，背景音：「鲜切现摇」；4-6 秒：第一人称成品特写，分层果茶倒入透明杯，你的手轻挤奶盖在顶部铺展，在杯身贴上粉红包标，镜头拉近看奶盖与果茶的分层纹理；6-8 秒：第一人称手持举杯，你将图片2中的果茶举到镜头前（模拟递到观众面前的视角），杯身标签清晰可见，背景音「来一口鲜爽」，尾帧定格为图片2。背景声音统一为女生音色。"
        },
        {
            # 【type】(string, 必填) 输入类型，此处为图片
            "type": "image_url",
            "image_url": {
                # 【url】(string) 图片公网 URL、Base64 编码或素材 ID
                # 支持格式：jpeg/png/webp/bmp/tiff/gif
                # 宽高比范围 (0.4, 2.5)，宽高像素范围 (300, 6000)，单张小于 30 MB
                "url": "https://ark-project.tos-cn-beijing.volces.com/doc_image/r2v_tea_pic1.jpg"
            },
            # 【role】(string, 条件必填) 图片角色，多模态参考场景固定为 reference_image
            "role": "reference_image"
        },
        {
            "type": "image_url",
            "image_url": {
                "url": "https://ark-project.tos-cn-beijing.volces.com/doc_image/r2v_tea_pic2.jpg"
            },
            "role": "reference_image"
        },
        {
            # 【type】(string, 必填) 输入类型，此处为视频
            "type": "video_url",
            "video_url": {
                # 【url】(string) 视频公网 URL 或素材 ID
                # 支持格式：mp4/mov，分辨率 480p/720p，帧率 [24, 60] FPS
                # 单个视频时长 [2, 15]s，最多传入 3 个，总时长不超过 15s，大小不超过 50 MB
                "url": "https://ark-project.tos-cn-beijing.volces.com/doc_video/r2v_tea_video1.mp4"
            },
            # 【role】(string, 条件必填) 视频角色，当前仅支持 reference_video（参考视频）
            "role": "reference_video"
        },
        {
            # 【type】(string, 必填) 输入类型，此处为音频
            "type": "audio_url",
            "audio_url": {
                # 【url】(string) 音频公网 URL、Base64 编码或素材 ID
                # 支持格式：wav/mp3，单段时长 [2, 15]s，最多传入 3 段，总时长不超过 15s，大小不超过 15 MB
                "url": "https://ark-project.tos-cn-beijing.volces.com/doc_audio/r2v_tea_audio1.mp3"
            },
            # 【role】(string, 条件必填) 音频角色，当前仅支持 reference_audio（参考音频）
            "role": "reference_audio"
        },
    ],

    # 【generate_audio】(boolean, 可选) 是否生成同步音频
    # true：模型自动生成匹配的人声、音效及背景音乐（默认）
    # false：输出无声视频
    # 注意：DMXAPI 当前版本此参数不生效，视频始终包含音频轨道
    "generate_audio": True,

    # 【resolution】(string, 可选) 视频分辨率
    # 可选值: "480p" / "720p"（默认）
    # 注意：Seedance 2.0 & 2.0 fast 不支持 1080p
    "resolution": "480p",

    # 【ratio】(string, 可选) 视频宽高比
    # 可选值: "16:9"(1280x720px) / "4:3"(1112x834px) / "1:1"(960x960px)
    #         "3:4"(834x1112px) / "9:16"(720x1280px) / "21:9"(1470x630px)
    #         "adaptive"（模型自动选择最合适的宽高比，Seedance 2.0 默认值）
    "ratio": "16:9",

    # 【duration】(integer, 可选) 视频时长（秒）
    # 取值范围: [4, 15]；默认值: 5
    # 注意：DMXAPI 不支持 -1（官方 API 支持），请使用具体整数值
    "duration": 4,

    # 【seed】(integer, 可选) 随机种子，控制生成内容随机性
    # 取值范围: [-1, 4294967295]；-1 表示使用随机数（默认）
    # 相同请求下，相同 seed 会生成类似结果，但不保证完全一致
    "seed": -1,

    # 【watermark】(boolean, 可选) 是否添加水印
    # false：无水印（默认）；true：有水印
    "watermark": False,

    # 【callback_url】(string, 可选) 任务状态变更回调地址
    # 任务状态变化时，平台向此地址推送 POST 请求
    # 回调状态枚举: "queued"（排队中）/ "running"（运行中）/ "succeeded"（成功）
    #               "failed"（失败）/ "expired"（超时）
    "callback_url": "https://www.dmxapi.cn",

    # 【return_last_frame】(boolean, 可选) 是否返回视频尾帧图片
    # true：返回 PNG 格式尾帧，可用于生成多个连续视频（以上一视频尾帧作为下一视频首帧）
    # false：不返回尾帧图片（默认）
    "return_last_frame": False,

    # 【execution_expires_after】(integer, 可选) 任务超时阈值（秒）
    # 取值范围: [3600, 259200]；默认值: 172800（48 小时）
    # 超过该时间后任务自动终止并标记为 expired 状态
    "execution_expires_after": 172800,

    # 【tools】(array, 可选) 工具配置
    # "web_search"：联网搜索工具，模型自主判断是否搜索互联网内容，可提升视频时效性
    "tools": [{"type": "web_search"}]
}

# 步骤4: 发送请求并输出结果
response = requests.post(url, headers=headers, json=payload)
print(json.dumps(response.json(), indent=2, ensure_ascii=False))
```

### 返回示例

```json
{
  "id": "cgt-20260402203437-bfb5r",
  "usage": {
    "total_tokens": 60850,
    "input_tokens": 0,
    "input_tokens_details": {
      "cached_tokens": 0
    },
    "output_tokens": 60850,
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
    # 【model】(string, 必填) 获取结果专用模型标识，固定为 seedance-2-0-get
    "model": "seedance-2-0-get",
    # 【input】(string, 必填) 提交任务时返回的任务 ID（id 字段的值）
    # 任务 ID 仅保存 7 天，超时后自动清除
    "input": "cgt-20260403171827-s64n7"
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

### 返回示例

```json
{
  "request_id": "cgt-20260403171827-s64n7",
  "output": [
    {
      "type": "message",
      "content": [
        {
          "type": "output_text",
          "text": "{\"content\":{\"video_url\":\"https://...视频链接...\"},\"id\":\"cgt-20260403171827-s64n7\",\"model\":\"doubao-seedance-2-0-260128\",\"status\":\"succeeded\"}"
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

视频链接: https://...（有效期 24 小时的临时下载链接）
```

<p align="center">
  <small>© 2026 DMXAPI doubao-seedance-2-0-260128 多模态参考生视频</small>
</p>
