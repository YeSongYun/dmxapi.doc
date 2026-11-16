# Luna-TTS 1.5 语音合成 API 使用文档

基于 `luna-tts-1.5` 的文本转语音接口，支持中文、英文、日文和韩文，以及同步生成与流式生成两种调用方式。同步接口一次返回完整音频；流式接口在模型完成合成后，以 HTTP Chunked Transfer 分块传输音频，不保证首字节比同步接口更快。两种接口的请求参数相同，成功响应均为音频二进制，失败响应为 JSON。

## 接口地址

| 接口 | 请求方式 | URL |
|------|---------|-----|
| 同步语音合成 | POST | `https://www.dmxapi.cn/v1/text-to-speech` |
| 流式语音合成 | POST | `https://www.dmxapi.cn/v1/text-to-speech/stream` |
:::warning
请妥善保管您的 API Key！严禁将密钥泄露给他人、硬编码到代码中或提交到公开的代码仓库。如果怀疑密钥已泄露，请立即前往 DMXAPI 官网重新生成。
:::

## 模型名称

- `luna-tts-1.5`


## 语音合成示例代码

::: code-group

```python [非流式]
import requests
import json
import os

# ===============================================================
# 步骤1: 配置 API 连接信息
# ===============================================================

# DMXAPI 服务端点地址 (同步语音合成)
# 接口与 VuiLabs 官网一致，只需把域名换成 DMXAPI、密钥换成 DMXAPI 密钥
url = "https://www.dmxapi.cn/v1/text-to-speech"

# DMXAPI 密钥 (请替换为您自己的密钥)
# 获取方式: 登录 DMXAPI 官网 -> 个人中心 -> API 密钥管理
api_key = "sk-******************************************"

# 音频保存目录
output_dir = "output"

# ===============================================================
# 步骤2: 配置请求头
# ===============================================================

headers = {
    "Content-Type": "application/json",      # 指定请求体为 JSON 格式 (必填)
    "Authorization": f"{api_key}",           # token 认证方式
}

# ===============================================================
# 步骤3: 配置请求参数
# ===============================================================

payload = {
    # 【generate_text】(string, 必填) 需要转换的文本内容
    # 支持中文、英文、日文、韩文
    # 长度上限: 500 加权字符
    # 支持模型标签: 直接写在文本里，保留英文拼写和半角方括号，不需要单独的参数
    #   [laughs] 笑声 / [chuckles] 轻笑 / [gasps] 倒吸气 / [sighs] 叹气 / [inhales] 吸气
    #   [breath] 呼吸声 / [exhale] 呼气 / [coughs] 咳嗽 / [clears throat] 清嗓子
    #   [sniffles] 吸鼻子 / [snorts] 鼻哼声 / [hisses] 嘶声 / [tsks] 啧声 / [groans] 低吟声
    "generate_text": "你好，欢迎使用 DMXAPI。",

    # 【voice_id】(string, 必填) 音色 ID；可以参考下面的音色id查询
    # 例如: "jingcheng" / "bochuan" / "zhining" / "nianan"
    "voice_id": "jingcheng",

    # 【model_id】(string, 必填) 调用的模型名称
    # 必须显式指定 luna-tts-1.5
    "model_id": "luna-tts-1.5",

    # 【language】(string, 可选) 语言
    # 可选值: "zh" / "en" / "ja" / "ko"
    # 系统音色可省略，省略时以音色目录中的语言为准；个人音色默认 zh
    "language": "zh",

    # 【text_normalization】(boolean, 可选) 文本归一化
    # 默认值 true
    # 可选值:
    #   - True(对数字、日期等文本做归一化处理)
    #   - False(关闭文本归一化，按原文合成)
    # 注意: 请传 JSON 布尔值，不要传字符串 "true" / "false"；可与标签同时使用
    "text_normalization": True,

    # 【speed】(number, 可选) 语速倍率
    # 取值范围: [0.6, 1.2]；不传或为 0 时默认 1.0
    # 调整实际音频的速度并保持音高；超出范围返回参数错误
    "speed": 1.0,

    # 【volume】(number, 可选) 音量
    # 单位 dB，取值范围: [-5, 5]，步长 0.1，默认值 0
    "volume": 0,

    # 【audio_format】(string, 可选) 音频格式
    # 可选值:
    #   - 不传、空值或 "wav"(返回 WAV，响应 Content-Type 为 audio/wav)
    #   - "pcm" / "pcm_s16le"(返回原始 PCM S16LE，不含 WAV 文件头，响应 Content-Type 为 audio/pcm)
    #   - "opus"(返回 Ogg Opus，响应 Content-Type 为 audio/ogg，建议保存为 .opus)
    # WAV / PCM 为 24000 Hz、单声道、16-bit；Opus 参数以 Ogg 容器为准
    # 注意: 实际格式以响应的 Content-Type 为准，不要按请求参数或文件扩展名推断
    "audio_format": "wav"
}

# ===============================================================
# 步骤4: 发送请求并输出结果
# ===============================================================

# 发送 POST 请求到 API 服务器
response = requests.post(url, headers=headers, json=payload)

# 成功时响应体是音频 (不是 JSON)；失败时响应体是 JSON
# 注意: 厂商的业务错误 (如参数错误、超过 500 字符) HTTP 状态码也是 200，要以 Content-Type 判断
content_type = response.headers.get("Content-Type", "").split(";")[0].strip().lower()
print("状态码:", response.status_code)
print("Content-Type:", content_type)

if content_type.startswith("audio/"):
    # 本次请求的计费字符数，费用 = 计费字符数 × 单价
    print("计费字符数:", response.headers.get("X-Luna-Billable-Characters"))

    # 按返回的音频类型决定扩展名并保存
    if content_type == "audio/pcm":
        extension = "pcm"
    elif content_type == "audio/ogg":
        extension = "opus"
    else:
        extension = "wav"
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, f"luna_tts.{extension}")
    with open(output_path, "wb") as f:
        f.write(response.content)
    print("音频已保存:", output_path)
else:
    # 格式化输出 JSON 错误响应
    # - indent=2: 缩进 2 空格，便于阅读
    # - ensure_ascii=False: 正确显示中文字符
    print(json.dumps(response.json(), indent=2, ensure_ascii=False))
```

```python [流式]
import requests
import json
import os

# ===============================================================
# 步骤1: 配置 API 连接信息
# ===============================================================

# DMXAPI 服务端点地址 (流式语音合成，音频开始返回后即按全文计费)
# 接口与 VuiLabs 官网一致，只需把域名换成 DMXAPI、密钥换成 DMXAPI 密钥
url = "https://www.dmxapi.cn/v1/text-to-speech/stream"

# DMXAPI 密钥 (请替换为您自己的密钥)
# 获取方式: 登录 DMXAPI 官网 -> 个人中心 -> API 密钥管理
api_key = "sk-******************************************"

# 音频保存目录
output_dir = "output"

# ===============================================================
# 步骤2: 配置请求头
# ===============================================================

headers = {
    "Content-Type": "application/json",      # 指定请求体为 JSON 格式 (必填)
    "Authorization": f"{api_key}",           # token 认证方式
}

# ===============================================================
# 步骤3: 配置请求参数
# ===============================================================

payload = {
    # 【generate_text】(string, 必填) 需要转换的文本内容
    # 支持中文、英文、日文、韩文
    # 长度上限: 500 加权字符
    # 支持模型标签: 直接写在文本里，保留英文拼写和半角方括号，不需要单独的参数
    #   [laughs] 笑声 / [chuckles] 轻笑 / [gasps] 倒吸气 / [sighs] 叹气 / [inhales] 吸气
    #   [breath] 呼吸声 / [exhale] 呼气 / [coughs] 咳嗽 / [clears throat] 清嗓子
    #   [sniffles] 吸鼻子 / [snorts] 鼻哼声 / [hisses] 嘶声 / [tsks] 啧声 / [groans] 低吟声
    "generate_text": "清晨的城市还没有完全醒来，街角的早餐店已经亮起了灯。蒸笼里冒出的热气混着豆浆的香味，慢慢飘到路口。赶早班车的人裹紧外套，一边看着手机，一边等着红灯变绿。公园里有人在打太极，动作不紧不慢，像是在和时间商量着什么。太阳从楼群的缝隙里升起来，把玻璃幕墙染成一片金色。送报的自行车从身边经过，车铃清脆地响了两声。卖花的阿姨把一桶一桶的鲜花摆到店门口，水珠顺着花瓣滑下来，落在青石板上。学校门口渐渐热闹起来，孩子们背着书包，三三两两地说着昨晚的动画片。新的一天就这样开始了，没有什么特别的事情发生，却让人觉得踏实而安稳。",

    # 【voice_id】(string, 必填) 音色 ID；可以参考下面的音色id查询
    # 例如: "jingcheng" / "bochuan" / "zhining" / "nianan"
    # 音色必须与模型兼容，不兼容时返回错误码 12913
    "voice_id": "jingcheng",

    # 【model_id】(string, 必填) 调用的模型名称
    # 必须显式指定 luna-tts-1.5
    "model_id": "luna-tts-1.5",

    # 【language】(string, 可选) 语言
    # 可选值: "zh" / "en" / "ja" / "ko"
    # 系统音色可省略，省略时以音色目录中的语言为准；个人音色默认 zh
    "language": "zh",

    # 【text_normalization】(boolean, 可选) 文本归一化
    # 默认值 true
    # 可选值:
    #   - True(对数字、日期等文本做归一化处理)
    #   - False(关闭文本归一化，按原文合成)
    # 注意: 请传 JSON 布尔值，不要传字符串 "true" / "false"；可与标签同时使用
    "text_normalization": True,

    # 【speed】(number, 可选) 语速倍率
    # 取值范围: [0.6, 1.2]；不传或为 0 时默认 1.0
    # 调整实际音频的速度并保持音高；超出范围返回参数错误
    "speed": 1.0,

    # 【volume】(number, 可选) 音量
    # 单位 dB，取值范围: [-5, 5]，步长 0.1，默认值 0
    "volume": 0,

    # 【audio_format】(string, 可选) 音频格式
    # 可选值:
    #   - 不传、空值或 "wav"(返回 WAV，响应 Content-Type 为 audio/wav)
    #   - "pcm" / "pcm_s16le"(返回原始 PCM S16LE，不含 WAV 文件头，响应 Content-Type 为 audio/pcm)
    #   - "opus"(返回 Ogg Opus，响应 Content-Type 为 audio/ogg，建议保存为 .opus)
    # WAV / PCM 为 24000 Hz、单声道、16-bit；Opus 参数以 Ogg 容器为准
    # 注意: 实际格式以响应的 Content-Type 为准，不要按请求参数或文件扩展名推断
    "audio_format": "wav"
}

# ===============================================================
# 步骤4: 发送请求并输出结果
# ===============================================================

# 发送 POST 请求到 API 服务器
# - stream=True: 边接收边写入文件
# 说明: 模型完成合成后才开始分块传输音频，首字节不保证比同步接口更快
#       音频开始传输后若发生错误，连接会中断，已接收的音频可能不完整
response = requests.post(url, headers=headers, json=payload, stream=True)

# 成功时响应体是音频 (不是 JSON)；失败时响应体是 JSON
# 注意: 厂商的业务错误 (如参数错误、超过 500 字符) HTTP 状态码也是 200，要以 Content-Type 判断
content_type = response.headers.get("Content-Type", "").split(";")[0].strip().lower()
print("状态码:", response.status_code)
print("Content-Type:", content_type)

if content_type.startswith("audio/"):
    # 本次请求的计费字符数，费用 = 计费字符数 × 单价
    print("计费字符数:", response.headers.get("X-Luna-Billable-Characters"))

    # 按返回的音频类型决定扩展名并保存
    if content_type == "audio/pcm":
        extension = "pcm"
    elif content_type == "audio/ogg":
        extension = "opus"
    else:
        extension = "wav"
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, f"luna_tts_stream.{extension}")
    with open(output_path, "wb") as f:
        for chunk in response.iter_content(chunk_size=4096):
            f.write(chunk)
    print("音频已保存:", output_path)
else:
    # 格式化输出 JSON 错误响应
    # - indent=2: 缩进 2 空格，便于阅读
    # - ensure_ascii=False: 正确显示中文字符
    print(json.dumps(response.json(), indent=2, ensure_ascii=False))
```
:::

## 返回示例

::: code-group

```json [非流式]
状态码: 200
Content-Type: audio/wav
计费字符数: 21
音频已保存: output\luna_tts.wav
```

```json [流式]
状态码: 200
Content-Type: audio/wav
计费字符数: 487
音频已保存: output\luna_tts_stream.wav
```

:::

## 原有中英文音色参考

以下仅收录官方系统音色列表中“原有中英文音色参考”分组的 39 个音色，可直接复制音色 ID 使用。

### 中文音色

| 序号 | 音色 ID | 音色名称 | 性别 | 描述 | 试听 |
|------|---------|---------|------|------|------|
| 1 | `jingcheng` | 播客景澄 | 男 | 温和、稳重且富有亲和力的男青年 | [试听](https://lunalab-res.oss-cn-hangzhou.aliyuncs.com/ttsPreV1/luna15-cn-production/20261104/jingcheng/jingcheng-01-demo-lunatts-1013-r5.wav) |
| 2 | `bochuan` | 柏川FM | 男 | 成熟、开朗的男青年 | [试听](https://lunalab-res.oss-cn-hangzhou.aliyuncs.com/ttsPreV1/luna15-cn-production/20261104/bochuan/bochuan-demo-lunatts-1013-r5.wav) |
| 3 | `zhining` | 播客芷宁 | 女 | 知性、温柔且富有亲和力的女青年 | [试听](https://lunalab-res.oss-cn-hangzhou.aliyuncs.com/ttsPreV1/luna15-cn-production/20261104/zhining/zhining-demo-lunatts-1013-r5.wav) |
| 4 | `nianan` | 念安FM | 女 | 清新、活泼的女青年 | [试听](https://lunalab-res.oss-cn-hangzhou.aliyuncs.com/ttsPreV1/luna15-cn-production/20261104/nianan/nianan-demo-lunatts-1013-r5.wav) |
| 5 | `jingyuan` | 靖哥说书 | 男 | 慵懒、个性且有磁性的霸总 | [试听](https://lunalab-res.oss-cn-hangzhou.aliyuncs.com/ttsPreV1/luna15-cn-production/20261104/jingyuan/jingyuan-demo-lunatts-1013-r5.wav) |
| 6 | `lixing` | 有声的砺行 | 男 | 清晰、温润的中年男性 | [试听](https://lunalab-res.oss-cn-hangzhou.aliyuncs.com/ttsPreV1/luna15-cn-production/20261104/lixing/lixing-01-demo-lunatts-1013-r5.wav) |
| 7 | `jinyu` | 有声的瑾瑜 | 女 | 温柔成熟的女声，富有层次感和表现力的女青年 | [试听](https://lunalab-res.oss-cn-hangzhou.aliyuncs.com/ttsPreV1/luna15-cn-production/20261104/jinyu/jinyu-demo-lunatts-1013-r5.wav) |
| 8 | `qiyan` | 绮言说书 | 女 | 女青年 | [试听](https://lunalab-res.oss-cn-hangzhou.aliyuncs.com/ttsPreV1/luna15-cn-production/20261104/qiyan/qiyan-demo-lunatts-1013-r5.wav) |
| 9 | `xiuyuan` | 客服小远 | 男 | 友好、耐心的男青年 | [试听](https://lunalab-res.oss-cn-hangzhou.aliyuncs.com/ttsPreV1/luna15-cn-production/20261104/xiuyuan/xiuyuan-demo-lunatts-1013-r5.wav) |
| 10 | `zhixia` | 客服小夏 | 女 | 友好、耐心的女青年 | [试听](https://lunalab-res.oss-cn-hangzhou.aliyuncs.com/ttsPreV1/luna15-cn-production/20261104/zhixia/zhixia-demo-lunatts-1013-r5.wav) |
| 11 | `xinxin` | 新新同学 | 男 | 稚气俏皮，充满孩子气的童声 | [试听](https://lunalab-res.oss-cn-hangzhou.aliyuncs.com/ttsPreV1/luna15-cn-production/20261104/xinxin/xinxin-demo-lunatts-1013-r5.wav) |
| 12 | `wukong` | 孙悟空 | 男 | 桀骜不驯、古灵精怪的猴子 | [试听](https://lunalab-res.oss-cn-hangzhou.aliyuncs.com/ttsPreV1/luna15-cn-production/20261104/wukong/wukong-demo-lunatts-1013-r5.wav) |
| 13 | `bajie` | 猪八戒 | 男 | 憨厚喜感的老猪 | [试听](https://lunalab-res.oss-cn-hangzhou.aliyuncs.com/ttsPreV1/luna15-cn-production/20261104/bajie/bajie-demo-lunatts-1013-r5.wav) |
| 14 | `linzi` | 东北琳子 | 女 | 搞笑直爽的东北老妹儿 | [试听](https://lunalab-res.oss-cn-hangzhou.aliyuncs.com/ttsPreV1/luna15-cn-production/20261104/linzi/linzi-demo-lunatts-1013-r5.wav) |
| 15 | `liuge` | 广西柳哥 | 男 | 搞笑广西表哥 | [试听](https://lunalab-res.oss-cn-hangzhou.aliyuncs.com/ttsPreV1/luna15-cn-production/20261104/liuge/liuge-demo-lunatts-1013-r5.wav) |
| 16 | `qinyao` | 沁瑶 | 女 | 知心姐姐 | [试听](https://lunalab-res.oss-cn-hangzhou.aliyuncs.com/ttsPreV1/luna15-cn-production/20261104/qinyao/qinyao-demo-lunatts-1103-r1.wav) |
| 17 | `xiyue` | 曦月 | 女 | 傲娇女友 | [试听](https://lunalab-res.oss-cn-hangzhou.aliyuncs.com/ttsPreV1/luna15-cn-production/20261104/xiyue/xiyue-demo-lunatts-1013-r5.wav) |
| 18 | `ruoxi` | 若兮 | 女 | 粘人小妹妹 | [试听](https://lunalab-res.oss-cn-hangzhou.aliyuncs.com/ttsPreV1/luna15-cn-production/20261104/ruoxi/ruoxi-demo-lunatts-1013-r5.wav) |
| 19 | `bochen` | 柏辰 | 男 | 温柔男友 | [试听](https://lunalab-res.oss-cn-hangzhou.aliyuncs.com/ttsPreV1/luna15-cn-production/20261104/bochen/bochen-demo-lunatts-1013-r5.wav) |
| 20 | `qingyan` | 清妍 | 女 | 明亮清晰、富有感染力的女生 | [试听](https://lunalab-res.oss-cn-hangzhou.aliyuncs.com/ttsPreV1/luna15-cn-production/20261104/qingyan/qingyan-demo-lunatts-1013-r5.wav) |
| 21 | `shuyan` | 书颜 | 女 | 甜美自然的女青年 | [试听](https://lunalab-res.oss-cn-hangzhou.aliyuncs.com/ttsPreV1/luna15-cn-production/20261104/shuyan/shuyan-demo-lunatts-1013-r5.wav) |
| 22 | `linhao` | 霖浩 | 男 | 专业且充满激情的解说员 | [试听](https://lunalab-res.oss-cn-hangzhou.aliyuncs.com/ttsPreV1/luna15-cn-production/20261104/linhao/linhao-01-demo-lunatts-1013-r5.wav) |
| 23 | `linning` | 霖宁 | 女 | 专业且充满激情的解说员 | [试听](https://lunalab-res.oss-cn-hangzhou.aliyuncs.com/ttsPreV1/luna15-cn-production/20261104/linning/linning-01-demo-lunatts-1013-r5.wav) |
| 24 | `luqiao` | 陆乔 | 男 | 热情开朗的男生 | [试听](https://lunalab-res.oss-cn-hangzhou.aliyuncs.com/ttsPreV1/luna15-cn-production/20261104/luqiao/luqiao-demo-lunatts-1013-r5.wav) |
| 25 | `yuheng` | 予衡 | 男 | 成熟、老钱风、有质感的中年男性 | [试听](https://lunalab-res.oss-cn-hangzhou.aliyuncs.com/ttsPreV1/luna15-cn-production/20261104/yuheng/yuheng-demo-lunatts-1013-r5.wav) |
| 26 | `duoyou` | 朵悠 | 女 | 青春洋溢的女生 | [试听](https://lunalab-res.oss-cn-hangzhou.aliyuncs.com/ttsPreV1/luna15-cn-production/20261104/duoyou/duoyou-demo-lunatts-1013-r5.wav) |
| 27 | `boxue` | 柏雪 | 女 | 温柔女友 | [试听](https://lunalab-res.oss-cn-hangzhou.aliyuncs.com/ttsPreV1/luna15-cn-production/20261104/boxue/boxue-demo-lunatts-1013-r5.wav) |
| 28 | `xiaowu` | 小武 | 男 | 文艺男友 | [试听](https://lunalab-res.oss-cn-hangzhou.aliyuncs.com/ttsPreV1/luna15-cn-production/20261104/xiaowu/xiaowu-demo-lunatts-1013-r5.wav) |

### 英文音色

| 序号 | 音色 ID | 音色名称 | 性别 | 描述 | 试听 |
|------|---------|---------|------|------|------|
| 29 | `michael` | Michael | 男 | 声音清晰、有亲和力的美国男青年 | [试听](https://lunalab-res.oss-cn-hangzhou.aliyuncs.com/ttsPreV1/luna15-cn-production/20261104/michael/michael-demo-lunatts-1013-r5.wav) |
| 30 | `james` | James | 男 | 优雅的英国男性 | [试听](https://lunalab-res.oss-cn-hangzhou.aliyuncs.com/ttsPreV1/luna15-cn-production/20261104/james/james-demo-lunatts-1013-r5.wav) |
| 31 | `grace` | Grace | 女 | 优雅的英国女性，口音标准圆润，叙事感强 | [试听](https://lunalab-res.oss-cn-hangzhou.aliyuncs.com/ttsPreV1/luna15-cn-production/20261104/grace/grace-demo-lunatts-1013-r5.wav) |
| 32 | `avery` | Avery | 女 | 友好、温和的美国女青年 | [试听](https://lunalab-res.oss-cn-hangzhou.aliyuncs.com/ttsPreV1/luna15-cn-production/20261104/avery/avery-demo-lunatts-1013-r5.wav) |
| 33 | `oscar` | Oscar | 男 | 友好、亲切的美国男青年 | [试听](https://lunalab-res.oss-cn-hangzhou.aliyuncs.com/ttsPreV1/luna15-cn-production/20261104/oscar/oscar-demo-lunatts-1013-r5.wav) |
| 34 | `olivia` | Olivia | 女 | 友好、亲切的美国女青年 | [试听](https://lunalab-res.oss-cn-hangzhou.aliyuncs.com/ttsPreV1/luna15-cn-production/20261104/olivia/olivia-demo-lunatts-1013-r5.wav) |
| 35 | `daniel` | Daniel | 男 | 声音明亮，充满活力的美国男青年 | [试听](https://lunalab-res.oss-cn-hangzhou.aliyuncs.com/ttsPreV1/luna15-cn-production/20261104/daniel/daniel-demo-lunatts-1013-r5.wav) |
| 36 | `ella` | Ella | 女 | 声音明亮，充满活力的美国女青年 | [试听](https://lunalab-res.oss-cn-hangzhou.aliyuncs.com/ttsPreV1/luna15-cn-production/20261104/ella/ella-demo-lunatts-1013-r5.wav) |
| 37 | `daisy` | Daisy | 女 | 甜美温柔的女友 | [试听](https://lunalab-res.oss-cn-hangzhou.aliyuncs.com/ttsPreV1/luna15-cn-production/20261104/daisy/daisy-demo-lunatts-1013-r5.wav) |
| 38 | `fiona` | Fiona | 女 | 细腻温柔的女友 | [试听](https://lunalab-res.oss-cn-hangzhou.aliyuncs.com/ttsPreV1/luna15-cn-production/20261104/fiona/fiona-demo-lunatts-1013-r5.wav) |
| 39 | `capriana` | Capriana | 女 | 冷静理性、语气克制的女青年 | [试听](https://lunalab-res.oss-cn-hangzhou.aliyuncs.com/ttsPreV1/luna15-cn-production/20261104/capriana/capriana-demo-lunatts-1013-r7-20261021-seed44.wav) |

<p align="center">
  <small>© 2026 DMXAPI Luna-TTS 1.5 语音合成</small>
</p>
