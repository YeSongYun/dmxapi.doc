# kling-4.0 视频主体创建 API 使用文档

基于可灵 Kling 4.0 主体管理接口，通过 DMXAPI 网关创建视频角色主体。视频主体使用 `reference_type = video_refer`，外观由 `element_video_list` 定义。当前只支持用视频定制写实风格的人物，并且只提交 1 段参考视频。创建接口立即返回 `data.task_id`，这时还没有 `element_id`。用主体任务查询等到 `task_status` 为 `succeed` 后，取 `data.task_result.elements[0].element_id`。

这个 `element_id` 用于全能参考生视频，引用方式和图片主体相同。<br/>
这个 `element_id` 只用于全能参考生视频：在 contents 里加一条 type 为 element 的素材，并在提示词中用对应的 @id 引用。图片主体和视频主体拿到的都是这种 ID，引用方式相同。
## 接口地址

| 接口 | 请求方式 | URL |
|------|---------|-----|
| 提交任务 | POST | `https://www.dmxapi.cn/v1/general/advanced-custom-elements` |
| 查询主体 | GET | `https://www.dmxapi.cn/v1/general/advanced-custom-elements/{task_id}` |

:::warning
请妥善保管您的 API Key！严禁将密钥泄露给他人、硬编码到代码中或提交到公开的代码仓库。如果怀疑密钥已泄露，请立即前往 DMXAPI 官网重新生成。
:::

## 模型名称

- `kling-4.0`

## 视频主体创建示例代码

```python
import requests
import json

# ===============================================================
# 步骤1: 配置 API 连接信息
# ===============================================================

# DMXAPI Kling 4.0 视频主体创建接口
# 与图片主体创建是同一个地址，用 reference_type 区分
url = "https://www.dmxapi.cn/v1/general/advanced-custom-elements"

# DMXAPI 密钥 (请替换为您自己的密钥)
# 获取方式: 登录 DMXAPI 官网 -> 个人中心 -> API 密钥管理
api_key = "sk-***********************************************"

# ===============================================================
# 步骤2: 配置请求头
# ===============================================================

headers = {
    "Content-Type": "application/json",       # 指定请求体为 JSON 格式
    "Authorization": f"Bearer {api_key}",     # Bearer 认证
}

# ===============================================================
# 步骤3: 配置请求参数
# ===============================================================

payload = {
    # 【model】(string, 必填) 模型名称，固定为 kling-4.0
    "model": "kling-4.0",

    # 【element_name】(string, 必填) 主体名称，最多 20 个字符
    "element_name": "video_v1",

    # 【element_description】(string, 必填) 主体描述，最多 100 个字符
    "element_description": "使用视频创建的主体参考",

    # 【reference_type】(string, 必填) 视频主体必须填写 video_refer
    # video_refer 的外观由 element_video_list 定义；此时不要传 element_image_list
    "reference_type": "video_refer",

    # 【element_video_list】(object, 必填) 视频主体参考视频
    "element_video_list": {
        # 【refer_videos】(array, 必填) 只能包含 1 个视频，video_url 不能为空
        "refer_videos": [
            {
                # 【video_url】(string, 必填) HTTP(S) 地址
                # 格式 mp4 或 mov，时长 3～8 秒，分辨率 1080p
                # 画面比例只能是 16:9 或 9:16，文件不超过 200MB
                # 仅支持写实风格人物；示例为 1080x1920、9:16、约 7 秒的人物正面出镜视频
                "video_url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250717/pvegot/input_video_01.mp4",
            }
        ],
    },

    # 【tag_list】(array, 可选) 标签对象。一个主体可以有多个标签
    # tag_id 取值：
    #   o_101 最热 / o_102 人物 / o_103 动物 / o_104 道具
    #   o_105 服饰 / o_106 场景 / o_107 特效 / o_108 其他
    "tag_list": [{"tag_id": "o_102"}],
}

# ===============================================================
# 步骤4: 发送请求并输出结果
# ===============================================================

response = requests.post(url, headers=headers, json=payload)
print("status:", response.status_code)
result = response.json()
print(json.dumps(result, indent=2, ensure_ascii=False))

# 主体创建返回的是 data.task_id，不是 element_id
data = result.get("data") if isinstance(result, dict) else None
if isinstance(data, dict):
    print("task_id:", data.get("task_id"))

response.raise_for_status()
```

## 返回示例

```json
status: 200
{
  "code": 0,
  "data": {
    "task_id": "task_WpPanSj0AAsyfRvxPNdzwc9lbHtErqeR",
    "task_status": "submitted"
  },
  "message": "",
  "request_id": "394c7fd8-fda5-497c-96b6-5a0aecd80c38"
}
task_id: task_WpPanSj0AAsyfRvxPNdzwc9lbHtErqeR
```
## 查询主体任务 示例代码

```python
import requests
import json
import time

# ===============================================================
# 步骤1: 配置 API 连接信息
# ===============================================================

# 创建接口返回的 data.task_id。路径参数使用 task_id 或 external_task_id，二者只能填一个
task_id = "task_LdsX7XEpIpOiu6rBHEDFEDOgXwsuXq5G"

# DMXAPI Kling 4.0 主体任务查询接口
# 图片主体和视频主体共用此接口，task_id 写在路径最后
url = f"https://www.dmxapi.cn/v1/general/advanced-custom-elements/{task_id}"

# DMXAPI 密钥 (请替换为您自己的密钥)
api_key = "sk-***********************************************"

# ===============================================================
# 步骤2: 配置请求头
# ===============================================================

headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {api_key}",
}

# ===============================================================
# 步骤3: 轮询直到任务结束
# ===============================================================

# 查询接口会立刻返回当前状态。每 25 秒查询一次，最多等待 600 秒。
# 主体任务成功状态是 succeed。失败时看 data.task_status_msg。
end_time = time.time() + 600
while time.time() < end_time:
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    result = response.json()
    data = result.get("data") if isinstance(result, dict) else None
    status = str(data.get("task_status") or data.get("status") or "").lower() if isinstance(data, dict) else ""
    if status in {"succeeded", "succeed", "failed", "cancelled", "timed_out"}:
        break
    time.sleep(25)
else:
    raise TimeoutError("主体任务在 600 秒内没有结束")

print("status:", response.status_code)
print(json.dumps(result, indent=2, ensure_ascii=False))

# 成功后，把 element_id 填入全能参考生视频 contents 里 type=element 的 element_id
if status in {"succeeded", "succeed"} and isinstance(data, dict):
    task_result = data.get("task_result", {})
    elements = task_result.get("elements", []) if isinstance(task_result, dict) else []
    if elements:
        print("element_id:", elements[0].get("element_id"))
```

## 返回示例

```json
status: 200
{
  "code": 0,
  "data": {
    "task_id": "task_WpPanSj0AAsyfRvxPNdzwc9lbHtErqeR",
    "task_result": {
      "elements": [
        {
          "element_id": "ke_d034ad7775362e3f",
          "reference_type": "video_refer",
          "status": "succeed"
        }
      ]
    },
    "task_status": "succeed",
    "task_status_msg": ""
  },
  "message": "",
  "request_id": "e3fc85b0-35c0-47bb-8dde-af3c7b399a61"
}
element_id: ke_d034ad7775362e3f
```


<p align="center">
  <small>© 2026 DMXAPI Kling-4.0 视频主体创建</small>
</p>
