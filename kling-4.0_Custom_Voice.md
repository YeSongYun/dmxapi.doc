# kling-4.0 音色创建 API 使用文档

基于可灵 Kling 4.0 的自定义音色接口，通过 DMXAPI 网关创建音色。可灵官网只有 Kling 4.0 有音色功能，Kling 4.0 Flash 没有。官网路径是 `/v1/general/custom-voices`，网关上要在前面多加一段 `/kling-4-0`。音色名称不超过 20 个字符。素材支持 mp3、wav、mp4、mov，人声要干净、没有杂音，并且只能有一种人声，时长 5～30 秒。提交后返回音色任务号 `data.task_id`。这个任务号只能用来查询，不能写进全能参考或主体；查询成功后要取的是 `voice_id`。

## 接口地址

| 接口 | 请求方式 | URL |
|------|---------|-----|
| 提交任务 | POST | `https://www.dmxapi.cn/kling-4-0/v1/general/custom-voices` |
| 获取结果 | GET | `https://www.dmxapi.cn/kling-4-0/v1/general/custom-voices/{task_id}` |


:::warning
请妥善保管您的 API Key！严禁将密钥泄露给他人、硬编码到代码中或提交到公开的代码仓库。如果怀疑密钥已泄露，请立即前往 DMXAPI 官网重新生成。
:::

## 模型名称

- `kling-4.0`

## 音色创建示例代码

```python
import requests
import json

# ===============================================================
# 步骤1: 配置 API 连接信息
# ===============================================================

# DMXAPI Kling 4.0 创建自定义音色接口
# 官网只有 Kling 4.0 有音色功能，Kling 4.0 Flash 没有
url = "https://www.dmxapi.cn/kling-4-0/v1/general/custom-voices"

# DMXAPI 密钥，请替换为您自己的密钥
# 获取方式: 登录 DMXAPI 官网 -> 个人中心 -> API 密钥管理
api_key = "sk-***********************************************"

# ===============================================================
# 步骤2: 配置请求头
# ===============================================================

headers = {
    "Content-Type": "application/json",  # 指定请求体为 JSON 格式
    "Authorization": f"Bearer {api_key}",  # Bearer 认证，填 DMXAPI 密钥
}

# ===============================================================
# 步骤3: 配置请求参数
# ===============================================================

payload = {
    # 【voice_name】(string，必填) 音色名称，不超过 20 个字符
    "voice_name": "旁白",

    # 【voice_url】(string，必填) 音色素材的网址
    #   格式 mp3 / wav / mp4 / mov
    #   人声要干净、没有杂音，并且只能有一种人声；时长 5～30 秒
    #   示例是阿里云文档的公开样例视频，约 7 秒，真人说话
    "voice_url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250717/pvegot/input_video_01.mp4",
}

# ===============================================================
# 步骤4: 发送请求并输出结果
# ===============================================================

response = requests.post(url, headers=headers, json=payload)
print("status:", response.status_code)
result = response.json()
print(json.dumps(result, indent=2, ensure_ascii=False))
response.raise_for_status()

# 返回里的 data.task_id 是音色任务号，填到音色查询脚本的 task_id，查询音色编号 voice_id。
# 音色任务号只能用来查音色；全能参考和主体里要填的是查询得到的 voice_id。
```

## 返回示例

```json
status: 200
{
  "code": "0",
  "data": {
    "task_id": "task_tvLN2tN8PRLOmyzWy2ZClwNETUnpFFEE",
    "task_status": "submitted"
  },
  "message": "SUCCEED"
}
```

## 获取音色 示例代码

```python
import requests
import json
import time

# ===============================================================
# 步骤1: 配置 API 连接信息
# ===============================================================

# DMXAPI Kling 4.0 查询单个自定义音色接口
# 官网地址是 /v1/general/custom-voices/{id}，网关上要在前面多加一段 /kling-4-0
# 音色任务号不写在这里，填在下面的 task_id
url = "https://www.dmxapi.cn/kling-4-0/v1/general/custom-voices"

# DMXAPI 密钥，请替换为您自己的密钥。只能查到本账号创建的音色任务
# 获取方式: 登录 DMXAPI 官网 -> 个人中心 -> API 密钥管理
api_key = "sk-***********************************************"

# ===============================================================
# 步骤2: 配置请求头
# ===============================================================

headers = {
    "Content-Type": "application/json",  # 指定请求体为 JSON 格式
    "Authorization": f"Bearer {api_key}",  # Bearer 认证，填 DMXAPI 密钥
}

# ===============================================================
# 步骤3: 配置请求参数
# ===============================================================

# 【task_id】(string，必填) 音色任务号。填音色创建后返回的 data.task_id
# 官网把这个号放在地址最后，这里单独写出来，发送时再拼到地址后面
task_id = "task_tvLN2tN8PRLOmyzWy2ZClwNETUnpFFEE"

# ===============================================================
# 步骤4: 发送请求并输出结果
# ===============================================================

# 网关会立刻返回任务当前的状态。脚本每 25 秒查一次，期间不打印，任务结束后只输出一次，最多等 600 秒。
end_time = time.time() + 600
while time.time() < end_time:
    response = requests.get(f"{url}/{task_id}", headers=headers)
    response.raise_for_status()
    result = response.json()
    data = result.get("data") if isinstance(result, dict) else None
    data = data if isinstance(data, dict) else {}
    status = str(data.get("task_status") or "").lower()
    if status in {"succeed", "failed"}:
        break
    time.sleep(25)
else:
    raise TimeoutError("音色任务在 600 秒内没有结束")

print("status:", response.status_code)
print(json.dumps(result, indent=2, ensure_ascii=False))

# 返回的 data 里：
#   task_id           音色任务号
#   task_status       任务状态：submitted 已提交、processing 处理中、succeed 成功、failed 失败
#   task_status_msg   任务失败时的原因
#   task_result.voices[0].voice_id     音色编号。写进全能参考 contents 里的 voice_id，或创建主体时的 element_voice_id
#   task_result.voices[0].voice_name   音色名称
#   task_result.voices[0].trial_url    试听音频地址
#   task_result.voices[0].owned_by     音色来源
```

## 返回示例

```json
status: 200
{
  "code": "0",
  "data": {
    "task_id": "task_tvLN2tN8PRLOmyzWy2ZClwNETUnpFFEE",
    "task_result": {
      "voices": [
        {
          "owned_by": "self",
          "trial_url": "https://v2-kling.kechuangai.com/bs2/upload-ylab-stunt/muse/855977437636227152/VIDEO/20261120/158912308ec77db9e07ecef27925a0e8-331b298e-585d-410e-8845-29e4553b551a.quality.wav?x-kcdn-pid=113274",
          "voice_id": "951968946058953756",
          "voice_name": "旁白"
        }
      ]
    },
    "task_status": "succeed",
    "task_status_msg": ""
  },
  "message": "SUCCEED"
}
```

<p align="center">
  <small>© 2026 DMXAPI kling-4.0 音色创建</small>
</p>
