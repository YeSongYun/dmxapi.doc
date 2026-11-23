# 视频主体创建 API 使用文档

Kling 4.0 与 Kling 4.0 Flash 共用的视频主体创建接口，和图片主体是同一个地址，用 `reference_type` 区分，请求体不要填写 `model`。这里填 `video_refer`。目前只支持用视频定制写实风格的人形形象。参考视频只能传 1 段，格式 mp4 / mov，时长 3～8 秒，必须是 1080P，宽高比 16:9 或 9:16，不超过 200MB，只能填网址，不支持 Base64。视频里有人声时，会同时定制音色：音色进入音色库，并和这个主体绑定。也可以另外传入音色库里已有的 `element_voice_id`。提交后返回主体任务号 `data.task_id`。查询得到的 `element_id` 才能写进全能参考；用在全能参考里时，这段参考视频的时长也会计入视频费用。

## 接口地址

| 接口 | 请求方式 | URL |
|------|---------|-----|
| 提交任务 | POST | `https://www.dmxapi.cn/kling-4-0/v1/general/advanced-custom-elements` |
| 获取结果 | GET | `https://www.dmxapi.cn/kling-4-0/v1/general/advanced-custom-elements/{task_id}` |


:::warning
请妥善保管您的 API Key！严禁将密钥泄露给他人、硬编码到代码中或提交到公开的代码仓库。如果怀疑密钥已泄露，请立即前往 DMXAPI 官网重新生成。
:::

## 模型名称

- 请求体不要填写 `model`。Kling 4.0 与 Kling 4.0 Flash 共用

## 视频主体创建示例代码

```python
import requests
import json

# ===============================================================
# 步骤1: 配置 API 连接信息
# ===============================================================

# DMXAPI 创建主体接口（视频主体）。Kling 4.0 和 Kling 4.0 Flash 共用，请求体不要填 model
# 官网地址是 /v1/general/advanced-custom-elements，网关上要在前面多加一段 /kling-4-0
url = "https://www.dmxapi.cn/kling-4-0/v1/general/advanced-custom-elements"

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
    # 【element_name】(string，必填) 主体名称，不超过 20 个字符
    "element_name": "video_v1",

    # 【element_description】(string，必填) 主体描述，不超过 100 个字符
    "element_description": "使用视频创建的主体参考",

    # 【reference_type】(string，必填) 主体参考方式。image_refer 图片主体，video_refer 视频主体
    #   这里是视频主体，填 video_refer，用下面的 element_video_list 设定主体外表
    "reference_type": "video_refer",

    # 【element_video_list】(object，视频主体必填) 主体参考视频
    #   目前只支持用视频定制写实风格的人形形象
    #   视频里有人声时，会同时定制音色：音色进入音色库，并和这个主体绑定
    "element_video_list": {
        # 【refer_videos】(array，必填) 参考视频列表，只能传 1 段
        "refer_videos": [
            {
                # 【video_url】(string，必填) 参考视频网址，只能填网址，不支持 Base64
                #   格式 mp4 / mov；时长 3～8 秒；必须是 1080P；宽高比 16:9 或 9:16；不超过 200MB
                #   示例是阿里云文档的公开样例：1080x1920、9:16、约 7 秒、约 1.1MB，真人出镜
                "video_url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250717/pvegot/input_video_01.mp4",
            }
        ],
    },

    # 【element_voice_id】(string，可选) 给主体绑定音色库里已有的音色。不传则不额外绑定
    #   填音色查询返回的 voice_id，或官方音色列表里的 voice_id
    # "element_voice_id": "950590922579253989",

    # 【tag_list】(array，可选) 主体标签，一个主体可以配多个，例如 [{"tag_id": "o_101"}, {"tag_id": "o_102"}]
    #   o_101 热梗、o_102 人物、o_103 动物、o_104 道具、o_105 服饰、o_106 场景、o_107 特效、o_108 其他
    "tag_list": [{"tag_id": "o_102"}],
}

# ===============================================================
# 步骤4: 发送请求并输出结果
# ===============================================================

response = requests.post(url, headers=headers, json=payload)
print("status:", response.status_code)
result = response.json()
print(json.dumps(result, indent=2, ensure_ascii=False))
response.raise_for_status()

# 返回里的 data.task_id 是主体任务号，填到主体任务查询脚本的 task_id，查询主体编号 element_id。
# 主体任务号只能用来查主体，不能写进全能参考；全能参考里要填的是查询得到的 element_id。
# 视频主体用在全能参考里时，这段参考视频的时长也会计入视频费用。
```

## 返回示例

```json
status: 200
{
  "code": "0",
  "data": {
    "task_id": "task_7K8IlDi3IUn0HwKMDNq8tVQ3JBLulX2t",
    "task_status": "submitted"
  },
  "message": "SUCCEED"
}
```

## 获取主体 示例代码

```python
import requests
import json
import time

# ===============================================================
# 步骤1: 配置 API 连接信息
# ===============================================================

# DMXAPI 查询单个主体接口。Kling 4.0 和 Kling 4.0 Flash 共用
# 官网地址是 /v1/general/advanced-custom-elements/{id}，网关上要在前面多加一段 /kling-4-0
# 主体任务号不写在这里，填在下面的 task_id
url = "https://www.dmxapi.cn/kling-4-0/v1/general/advanced-custom-elements"

# DMXAPI 密钥，请替换为您自己的密钥。只能查到本账号创建的主体任务
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

# 【task_id】(string，必填) 主体任务号。填图片主体创建或视频主体创建后返回的 data.task_id
# 官网把这个号放在地址最后，这里单独写出来，发送时再拼到地址后面
task_id = "task_7K8IlDi3IUn0HwKMDNq8tVQ3JBLulX2t"

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
    raise TimeoutError("主体任务在 600 秒内没有结束")

print("status:", response.status_code)
print(json.dumps(result, indent=2, ensure_ascii=False))

# 返回的 data 里：
#   task_id           主体任务号
#   task_status       任务状态：submitted 已提交、processing 处理中、succeed 成功、failed 失败
#   task_status_msg   任务失败时的原因
#   task_result.elements[0].element_id       主体编号。写进全能参考 contents 里的 element_id
#   task_result.elements[0].reference_type   主体参考方式：image_refer 图片主体、video_refer 视频主体
```

## 返回示例

```json
{
  "code": "0",
  "data": {
    "task_id": "task_7K8IlDi3IUn0HwKMDNq8tVQ3JBLulX2t",
    "task_result": {
      "elements": [
        {
          "element_id": 327119791264146,
          "status": "succeed"
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
  <small>© 2026 DMXAPI 视频主体创建</small>
</p>
