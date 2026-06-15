# lyric_generation 歌词生成 API 使用文档

基于 MiniMax lyric_generation 模型的歌词生成接口，通过 `/v1/responses` 端点同步调用，输入主题描述即可一键产出带完整曲式结构的原创歌词。支持 `write_full_song`（写完整歌曲）与 `edit`（编辑/续写歌词）两种模式，输出自动附带歌名（song_title）、风格标签（style_tags）以及包含 14 种结构标签（[Intro]、[Verse]、[Pre-Chorus]、[Chorus]、[Bridge]、[Outro] 等）的规范歌词，生成的歌词可直接用于音乐生成接口的 `lyrics` 参数完成"歌词 → 歌曲"的创作闭环，适合音乐创作、短视频文案、AI 作曲等场景。

## 接口地址

| 接口 | 请求方式 | URL |
|------|---------|-----|
| 歌词生成 | POST | `https://www.dmxapi.cn/v1/responses` |



:::warning
请妥善保管您的 API Key！严禁将密钥泄露给他人、硬编码到代码中或提交到公开的代码仓库。如果怀疑密钥已泄露，请立即前往 DMXAPI 官网重新生成。
:::

## 模型名称

- `lyric_generation`

## 歌词生成 示例代码

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
    "model": "lyric_generation",

    # 【mode】(string, 必填) 生成模式
    # 可选值:
    #   - "write_full_song"(写完整歌曲)
    #   - "edit"(编辑/续写歌词)
    "mode": "write_full_song",

    # 【input】(string, 可选) 提示词/指令，用于描述歌曲主题、风格或编辑方向
    # 为空时随机生成，长度上限 2000 个字符
    "input": "一首关于夏日海边的轻快情歌",

    # 【lyrics】(string, 可选) 现有歌词内容，仅在 edit 模式下有效
    # 可用于续写或修改已有歌词，长度上限 3500 个字符
    "lyrics" : "[verse]\n街灯微亮晚风轻抚\n影子拉长独自漫步\n旧外套裹着深深忧郁\n不知去向渴望何处\n[chorus]\n推开木门香气弥漫\n熟悉的角落陌生人看",

    # 【title】(string, 可选) 歌曲标题，传入后输出将保持该标题不变
    "title": "test"
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
  "song_title": "test",
  "style_tags": "summer, beach, love song, upbeat, pop",
  "lyrics": "[Intro]\n\n[Verse]\n阳光洒满了沙滩\n脚印一深一浅\n海浪亲吻着脚边\n心跳也变得热烈\n你的笑像夏天\n融化我所有不安\n\n[Pre-Chorus]\n微风吹过发梢\n吹来了你的味道\n世界突然变小\n只有我和你的依靠\n\n[Chorus]\n就让海风来见证\n我们小小的约定\n手牵着手不分离\n海边的身影多甜蜜\n听海浪唱着情歌\n你就是我的快乐\n这一刻永不褪色\n\n[Post-Chorus]\n啦啦啦 啦啦啦\n夏日的海边\n啦啦啦 啦啦啦\n爱意在蔓延\n\n[Verse]\n冰淇淋融化得快\n像我们热恋的节拍\n看海鸥自由自在\n想和你一起去未来\n你的眼睛闪亮\n像星辰坠入海洋\n\n[Pre-Chorus]\n微风吹过发梢\n吹来了你的味道\n世界突然变小\n只有我和你的依靠\n\n[Chorus]\n就让海风来见证\n我们小小的约定\n手牵着手不分离\n海边的身影多甜蜜\n听海浪唱着情歌\n你就是我的快乐\n这一刻永不褪色\n\n[Bridge]\n夕阳染红了天空\n晚霞像你的脸红\n我们并肩坐着\n听海浪轻轻诉说\n\n[Verse]\n时间好像暂停\n只留下你的身影\n海风吹乱了发型\n也吹乱我的心\n只想和你一起\n看海潮起又潮落\n\n[Chorus]\n就让海风来见证\n我们小小的约定\n手牵着手不分离\n海边的身影多甜蜜\n听海浪唱着情歌\n你就是我的快乐\n这一刻永不褪色\n\n[Post-Chorus]\n啦啦啦 啦啦啦\n夏日的海边\n啦啦啦 啦啦啦\n爱意在蔓延\n\n[Outro]",
  "base_resp": {
    "status_code": 0,
    "status_msg": "success"
  },
  "usage": {
    "total_tokens": 500,
    "input_tokens": 0,
    "input_tokens_details": {
      "cached_tokens": 0
    },
    "output_tokens": 500,
    "output_tokens_details": {
      "reasoning_tokens": 0
    }
  }
}
```

<p align="center">
  <small>© 2026 DMXAPI lyric_generation 歌词生成</small>
</p>
