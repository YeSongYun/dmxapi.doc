# MiMo mimo-v2-tts 语音合成 API 使用文档

MiMo V2 TTS 是小米 MiMo 大模型推出的文字转语音功能，基于 `/v1/chat/completions` 端点，支持 `mimo_default`、`default_zh`、`default_en` 三种预置音色，并可通过 `<style>` 标签灵活控制情绪、语速、方言及场景风格（如唱歌、角色扮演等）。合成结果以 Base64 编码的 WAV 音频返回，待合成文本须置于 `assistant` 消息中。

## 🔗 请求地址

```
https://www.dmxapi.cn/v1/chat/completions
```

:::warning
请妥善保管您的 API Key！严禁将密钥泄露给他人、硬编码到代码中或提交到公开的代码仓库。如果怀疑密钥已泄露，请立即前往 DMXAPI 官网重新生成。
:::

## 🤖 模型名称

- `mimo-v2-tts`

## 🎵 语音合成 示例代码

```python
import base64
import time
import requests

# ============================================================

# ---------- 鉴权配置 ----------
API_KEY = "sk-****************************"

# ---------- 音色配置 ----------
# mimo_default : MiMo 默认音色
# default_zh   : MiMo 中文女声
# default_en   : MiMo 英文女声
# 注意: 当前不支持音色克隆，只能从以上预置音色中选择
VOICE = "mimo_default"

# ---------- 风格配置 ----------
# 合成时会自动在文本开头插入 <style>...</style> 标签
# 支持的风格示例（不限于列表，可自由填写）:
#   情绪类 → 开心 / 悲伤 / 生气
#   语速类 → 变快 / 变慢
#   方言类 → 东北话 / 粤语 / 四川话 / 河南话
#   风格类 → 悄悄话 / 夹子音 / 台湾腔
#   场景类 → 唱歌 / 角色扮演(孙悟空 / 林黛玉 等)
# 留空则不添加风格标签
#
# 多风格写法: 将多个风格名称写在同一个标签内，分隔符不限
#   示例: STYLE = "开心 变快"  →  <style>开心 变快</style>
#
# ⚠️ 唱歌场景特别注意: 必须单独使用 "唱歌" 风格，不可与其他风格混用
#   正确: STYLE = "唱歌"  TEXT = "原谅我这一生不羁放纵爱自由……"
STYLE = "唱歌"

# ---------- 待合成文本 ----------
# 支持在文本内嵌入自然语言音频标签，进行细粒度情绪/动作控制，例如:
#   "（紧张，深呼吸）呼……冷静，冷静。不就是一个面试吗……"
#   "（极其疲惫，有气无力）师傅……到地方了叫我一声……（长叹一口气）"
#   "（提高音量喊话）大姐！这鱼新鲜着呢！早上刚捞上来的！"
TEXT = "原谅我这一生不羁放纵爱自由……"

# ============================================================
#  构造请求
# ============================================================

# 拼接风格前缀与正文，最终格式: <style>风格</style>待合成内容
style_prefix = f"<style>{STYLE}</style>" if STYLE else ""
content = style_prefix + TEXT

url = "https://www.dmxapi.cn/v1/chat/completions"

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

payload = {
    "model": "mimo-v2-tts",
    "messages": [
        # user 消息为可选项，但建议携带，可在部分场景下影响合成的语气与风格
        {"role": "user", "content": "Hello, MiMo, have you had lunch?"},
        # 待合成的目标文本必须置于 assistant 消息中，不可放在 user 消息内
        {"role": "assistant", "content": content}
    ],
    # format: 非流式调用固定使用 wav
    #         流式调用需指定 pcm16（以便拼接成完整音频）
    # voice:  指定预置音色，见上方音色配置说明
    "audio": {"format": "wav", "voice": VOICE}
}

# ============================================================
#  发送请求并保存音频
# ============================================================

response = requests.post(url, headers=headers, json=payload)
response.raise_for_status()  # 请求失败时立即抛出异常，便于排查错误

# 响应结构: choices[0] → message → audio → data（Base64 编码的音频内容）
audio_b64 = response.json()["choices"][0]["message"]["audio"]["data"]
audio_bytes = base64.b64decode(audio_b64)

# 以当前时间戳命名输出文件，避免覆盖历史结果
filename = f"audio_{time.strftime('%Y%m%d_%H%M%S')}.wav"
with open(filename, "wb") as f:
    f.write(audio_bytes)

print(f"已保存: {filename}")

```

## 🐯 返回示例

```json
已保存: audio_20260323_130835.wav
```

<p align="center">
  <small>© 2026 DMXAPI MiMo mimo-v2-tts 语音合成</small>
</p>
