# wan3.0-video-prime 参考文件生视频 API 使用文档

基于通义万相 3.0 视频生成模型（高速版）的参考文件生视频接口，通过 `/v1/responses` 端点以异步任务方式调用。直接上传 PPT、Word、Excel、PDF、Markdown 等 12 类文档（不超过 100MB、不超过 50 页）或一个网页链接作为创意来源，由模型读懂文件内容后生成带原生音频的视频；支持 480P / 720P / 1080P 三档分辨率、2~30 秒自定义时长与自适应宽高比，适合把产品方案、宣传文案、活动策划一键转成成片的场景。

## 接口地址

| 接口 | 请求方式 | URL |
|------|---------|-----|
| 提交任务 | POST | `https://www.dmxapi.cn/v1/responses` |
| 获取结果 | POST | `https://www.dmxapi.cn/v1/responses` |


:::warning
请妥善保管您的 API Key！严禁将密钥泄露给他人、硬编码到代码中或提交到公开的代码仓库。如果怀疑密钥已泄露，请立即前往 DMXAPI 官网重新生成。
:::

## 模型名称

- `wan3.0-video-prime`

## 参考文件生视频 示例代码

```python
import requests
import json

# ===============================================================
# 步骤1: 配置 API 连接信息
# ===============================================================

# DMXAPI 服务端点地址
url = "https://www.dmxapi.cn/v1/responses"

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
    # wan3.0-video-prime：高速版，能力对齐标准版，端到端速度显著提升
    "model": "wan3.0-video-prime",

    "input": {
        # wan3.0-video-prime：高速版，能力对齐标准版，端到端速度显著提升
        # 【input】(object, 必填) 输入的基本信息
        # prompt 和 media 必填其一
        "input": {
            # 【media】(array[object], 条件必选) 媒体素材数组
            # 支持图像、视频、音频、文件和网页作为输入，和 prompt 必填其一
            # 数组中每个元素为一个媒体对象，包含 type 与 url 字段
            # 在参考生视频模式下，按照数组顺序定义 prompt 中素材引用的顺序
            # 图和视频分别计数，即可同时存在图1、视频1:
            #   - 第 1 个 reference_image 对应 图1，第 2 个对应 图2，以此类推
            #   - 第 1 个 reference_video 对应 视频1，第 2 个对应 视频2，以此类推
            #   - 第 1 个 reference_audio 对应 音频1，第 2 个对应 音频2，以此类推
            # 注意: reference_xx / file / link 类型和 first_frame / last_frame 类型互斥，
            # 不能在同一请求中混用
            "media": [
                {
                    # 【type】(string, 必选) 媒体素材类型
                    # 本示例取值 "file"：文件。最多 1 个，不可与 link 同时输入
                    "type": "file",
                    # 【url】(string, 必选) 媒体素材 URL 或 Base64 编码数据
                    # 文件 URL。文件限制:
                    #   - 格式: docx、doc、xlsx、xls、pptx、ppt、pdf、txt、key、pages、numbers、md
                    #   - 文件大小: 不超过 100MB
                    #   - 页数限制: 不超过 50 页(对 pdf、docx、doc、pptx、ppt、key、pages 格式校验)
                    # 支持公网 URL(HTTP / HTTPS)、OSS 协议临时 URL
                    "url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260806/ebapmr/glass.pptx"
                },
            ],
            # 【prompt】(string, 条件必选) 文本提示词，用来描述期望生成的视频内容
            # 和 media 必填其一
            # 支持中英文，每个汉字/字母占一个字符，不超过 20000 个字符，超过部分会自动截断
            # 在全能参考模式下，prompt 中可以用"图1""视频1""音频1"等指代 media 数组中
            # 对应顺序的媒体素材
            "prompt": "一支高端智能眼镜产品广告，整体风格极简、未来感、时尚高级，光影克制，画面以黑色、银灰色、冰蓝色为主色调，局部点缀柔和白光与参数UI图形。开场在纯黑背景中，一副智能眼镜从黑暗中缓缓浮现，镜腿边缘掠过精致高光，镜框轮廓在冷冽边缘光下被勾勒出来，镜头超近距离掠过镜片、鼻托、转轴、镜腿与材质细节，展现金属与高性能复合材料的细腻质感，表面处理高级克制，线条轻薄流畅。随后产品在空中缓慢旋转，画面以极简动态图形同步展示核心参数信息。随后镜头快速收拢，所有零件精准回归组装成完整产品，切换到年轻模特佩戴展示，模特五官立体、气质自信，穿着简洁高级的都市时尚服装，在极简空间和城市光影环境中自然转头、抬手、行走、微笑，镜头从正面、侧面、斜后方展示眼镜佩戴状态，突出轻薄贴合、时尚轮廓与日常百搭属性。结尾在纯色背景中，产品悬浮定格，镜头缓慢推进到品牌logo和核心slogan，整体音乐极简电子氛围配合精准鼓点，节奏干净有力，画面质感高级、克制、纯粹，具有强烈品牌记忆点和国际化科技审美。"
        },
        # 【parameters】(object, 可选) 视频处理参数
        "parameters": {
            # 【duration】(integer, 可选) 生成视频的时长，单位为秒
            # 默认值为 5
            #   - 无视频输入时: 取值范围为 [2, 30] 的整数
            #   - 有视频输入时: 输入视频总时长 + 输出视频时长不超过 30 秒
            #   - 传 -1 时: 智能时长模式，模型根据输入的 prompt、内容和富媒体自动推荐合适时长生成
            "duration": 10,
            # 【prompt_extend】(boolean, 可选) 是否开启 prompt 智能改写
            # 开启后使用大模型对输入 prompt 进行智能改写
            # 对于较短的 prompt 生成效果提升明显，但会增加耗时
            # 可选值: True(默认值，开启智能改写) / False(不开启智能改写)
            "prompt_extend": True,
            # 【ratio】(string, 可选) 生成视频的宽高比
            # 可选值:
            #   - "adaptive"(默认值，自适应长宽比，根据输入媒体比例和意图自动推荐合适的长宽比)
            #   - "16:9" / "4:3" / "1:1" / "3:4" / "9:16"
            "ratio": "adaptive",
            # 【resolution】(string, 可选) 生成视频的分辨率档位
            # 默认值为 1080P
            # 可选值: "1080P" / "720P" / "480P"
            "resolution": "480P",
            # 【audio】(boolean, 可选) 输出视频是否包含音频
            # 可选值:
            #   - True(默认值，输出视频包含声音)
            #   - False(输出视频不包含音轨)
            # 开关声音价格相同
            "audio": True,
            # 【seed】(integer, 可选) 随机种子，用于复现生成结果
            # 取值范围: [0, 2147483647]
            "seed": 0,
            # 【watermark】(boolean, 可选) 是否添加水印标识
            # 可选值: False(默认值，不添加水印) / True(添加水印)
            "watermark": False
        },
    },
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
  "output": [
    {
      "type": "message",
      "content": [
        {
          "type": "output_text",
          "text": "cad7bc59-4d5e-46b7-a3c2-88e8f412d70b"
        }
      ]
    }
  ],
  "provider_metadata": {
    "task_id": "cad7bc59-4d5e-46b7-a3c2-88e8f412d70b",
    "task_status": "PENDING"
  },
  "request_id": "2c1a9355-e9be-935d-91bb-92dbf601b0fb",
  "usage": {
    "input_tokens": 0,
    "input_tokens_details": {
      "cached_tokens": 0
    },
    "output_tokens": 45000,
    "output_tokens_details": {
      "reasoning_tokens": 0
    },
    "total_tokens": 45000
  }
}
```

返回中的 `task_id`（即 `output` 数组内的任务 ID 文本）用于第二步查询生成结果，`task_status` 为 `PENDING` 表示任务已排队等待处理。

## 获取生成视频 示例代码

```python
"""
╔═══════════════════════════════════════════════════════════════╗
║                  DMXAPI 自研接口                               ║
╚═══════════════════════════════════════════════════════════════╝

📝 功能说明:
   本脚本演示如何使用 requests 库调用 DMXAPI 的自研接口

═══════════════════════════════════════════════════════════════
"""

import requests
import json

# ═══════════════════════════════════════════════════════════════
# 🔑 步骤1: 配置 API 连接信息
# ═══════════════════════════════════════════════════════════════

# 🌐 DMXAPI 服务端点地址
url = "https://www.dmxapi.cn/v1/responses"

# 🔐 DMXAPI 密钥 (请替换为您自己的密钥)
# 获取方式: 登录 DMXAPI 官网 -> 个人中心 -> API 密钥管理
api_key = "sk-***********************************************"

# ═══════════════════════════════════════════════════════════════
# 📋 步骤2: 配置请求头
# ═══════════════════════════════════════════════════════════════

headers = {
    "Content-Type": "application/json",      # 指定请求体为 JSON 格式
    "Authorization": f"{api_key}",    # token 认证方式
}

# ═══════════════════════════════════════════════════════════════
# 💬 步骤3: 配置请求参数
# ═══════════════════════════════════════════════════════════════

payload = {

    "model": "wan3.0-get",
    "input": "cad7bc59-4d5e-46b7-a3c2-88e8f412d70b"

}


# ═══════════════════════════════════════════════════════════════
# 📤 步骤4: 发送请求并输出结果
# ═══════════════════════════════════════════════════════════════

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
  "output": [
    {
      "type": "message",
      "content": [
        {
          "type": "output_text",
          "text": "https://dashscope-a717.oss-accelerate.aliyuncs.com/1d/06/20260828/e4b11e52/cad7bc59-4d5e-46b7-a3c2-88e8f412d70b.mp4?Expires=1787977555&OSSAccessKeyId=LTAI5tPxpiCM2hjmWrFXrym1&Signature=cvVf1sQtf5IeQtf0y7%2F%2FL5RnPAw%3D"
        }
      ]
    }
  ],
  "request_id": "31b13d48-3223-989e-9aa2-6af54b5edeb7",
  "usage": {
    "SR": 480,
    "duration": 10.0,
    "fps": 30,
    "input_tokens": 0,
    "input_tokens_details": {
      "cached_tokens": 0
    },
    "input_video_duration": 0,
    "output_tokens": 0,
    "output_tokens_details": {
      "reasoning_tokens": 0
    },
    "output_video_duration": 10.0,
    "ratio": "16:9",
    "total_tokens": 0,
    "video_count": 1
  }
}
```

任务成功后 `output` 中返回视频的临时下载链接（有效期由 `Expires` 参数决定，请及时转存）；`usage` 中的 `SR` 为输出分辨率短边、`duration` / `output_video_duration` 为视频时长（秒）、`fps` 为帧率、`ratio` 为实际输出的宽高比、`video_count` 为生成视频数量。

<p align="center">
  <small>© 2026 DMXAPI wan3.0-video-prime 参考文件生视频</small>
</p>
