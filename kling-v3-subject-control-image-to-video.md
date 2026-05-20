# kling-v3 主体控制 图生视频 API 使用文档

kling-v3 主体控制能力基于 DMXAPI `/v1/responses` 端点，通过 `element_list` 引用预先创建的主体（视频角色主体或多图主体，最多 3 个），结合参考图与文本提示词进行主体一致性视频生成。支持单镜头/多镜头（最多 6 个分镜）、3~15 秒可选时长、std/pro/4k 三种生成模式，并提供 cfg_scale 控制提示词相关性、sound 开关音效、watermark_info 控制水印输出，可在提示词中通过 `<<<element_N>>>` 语法绑定具体主体。采用异步任务模式，提交后返回 `taskId`，需通过查询接口获取最终视频地址。

## 模型名称

- `kling-v3`

## 接口地址

| 接口 | 请求方式 | URL |
|------|---------|-----|
| 提交任务 | POST | `https://www.dmxapi.cn/v1/responses` |
| 获取结果 | POST | `https://www.dmxapi.cn/v1/responses` |

:::warning
请妥善保管您的 API Key！严禁将密钥泄露给他人、硬编码到代码中或提交到公开的代码仓库。
:::

## 主体控制 图生视频 示例代码

```python
import requests
import json

# ═══════════════════════════════════════════════════════════════
# 步骤1: 配置 API 连接信息
# ═══════════════════════════════════════════════════════════════

# DMXAPI 服务端点地址
url = "https://www.dmxapi.cn/v1/responses"

# DMXAPI 密钥 (请替换为您自己的密钥)
# 获取方式: 登录 DMXAPI 官网 -> 个人中心 -> API 密钥管理
api_key = "sk-******************************************"

# ═══════════════════════════════════════════════════════════════
# 步骤2: 配置请求头
# ═══════════════════════════════════════════════════════════════

headers = {
    "Content-Type": "application/json",      # 指定请求体为 JSON 格式
    "Authorization": f"{api_key}",           # token 认证方式
}
# ═══════════════════════════════════════════════════════════════
# 步骤3: 配置请求参数
# ═══════════════════════════════════════════════════════════════
payload = {
    # 【model】(string, 必填) 模型名称
    # 可选值: "kling-v3"(可灵 V3 模型)
    "model": "kling-v3",

    # 【image】(string, 可选) 参考图像
    # 支持传入图片 Base64 编码或图片 URL（确保可访问）
    # 若使用 base64，请直接传 Base64 编码字符串，不要附加 data:image/png;base64, 前缀
    # 图片格式支持 .jpg / .jpeg / .png
    # 图片文件大小不能超过 10MB，宽高尺寸不小于 300px，宽高比介于 1:2.5 ~ 2.5:1 之间
    # image 参数与 image_tail 参数至少二选一，不能同时为空
    "image": "https://prod-ss-images.s3.cn-northwest-1.amazonaws.com.cn/vidu-maas/template/image2video.png",

    # 【input】(string, 必填) 文本提示词，可包含正向描述和负向描述
    # 可将提示词模板化以满足不同视频生成需求
    # 可通过 <<<>>> 格式指定主体/图片/视频，如：<<<element_1>>>、<<<image_1>>>、<<<video_1>>>
    # 不能超过 2500 个字符
    # 可用 <<<voice_1>>> 指定音色，序号同 voice_list 参数所引用音色的排列顺序
    # 一次视频生成任务至多引用 2 个音色；指定音色时，sound 参数值必须为 on
    # 语法结构越简单越好，如：男人<<<voice_1>>>说："你好"
    # 当 voice_list 不为空且 input 中引用音色 ID 时，按"有指定音色"计量计费
    # 当 multi_shot 为 false 或 shot_type 为 intelligence 时，当前参数必填
    "input": "<<<element_1>>> 和宇航员手牵手，一起遥望星空，然后乘坐飞船，返回地球",

    # 【element_list】(array, 可选) 参考主体列表
    # 基于主体库中主体的 ID 配置，最多支持 3 个参考主体
    # 主体分为视频定制主体（视频角色主体）和图片定制主体（多图主体），适用范围不同
    # element_list 参数与 voice_list 参数互斥，不能共存
    # 格式：[{"element_id": long}, {"element_id": long}]
    "element_list": [
        # 【element_id】(long, 必填) 主体 ID
        # 通过创建主体接口预先生成；input 中的 <<<element_N>>> 序号与本数组顺序对应
        # 可在文档末尾「部分主体参考列表」查看可用的 element_id 与对应元素名称
        {"element_id": 149},
    ],

    # 【negative_prompt】(string, 可选) 负向文本提示词
    # 不能超过 2500 个字符
    # 用于声明不希望出现的画面内容，提升画面纯净度
    "negative_prompt": "模糊, 抖动",

    # 【sound】(string, 可选) 生成视频时是否同时生成声音
    # 可选值: "on"(开启声音) / "off"(关闭声音)
    # 默认值: "off"
    "sound": "on",

    # 【cfg_scale】(float, 可选) 生成视频的自由度
    # 值越大，模型自由度越小，与用户输入的提示词相关性越强
    # 取值范围: [0, 1]，默认值为 0.5
    "cfg_scale": 0.5,

    # 【mode】(string, 可选) 生成视频的模式
    # 可选值:
    #   - "std": 标准模式，基础模式，性价比高
    #   - "pro": 专家模式（高品质），高表现模式，生成视频质量更佳
    #   - "4k":  4K 模式，高表现（同 pro），输出视频分辨率为 4K
    # 默认值: "std"
    "mode": "pro",

    # 【duration】(string, 可选) 生成视频时长，单位 s
    # 可选值: "3" / "4" / "5" / "6" / "7" / "8" / "9" / "10" / "11" / "12" / "13" / "14" / "15"
    # 默认值: "5"
    "duration": "8",

    # 【watermark_info】(object, 可选) 是否同时生成含水印的结果
    # 暂不支持自定义水印
    "watermark_info": {
        # 【enabled】(boolean, 必填) 是否生成含水印的结果
        # true 为生成，false 为不生成
        "enabled": False
    },
}

# ═══════════════════════════════════════════════════════════════
# 步骤4: 发送请求并输出结果
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
  "request_id": "tsk-geuaywbthrhr9ux3",
  "output": [
    {
      "type": "message",
      "content": [
        {
          "type": "output_text",
          "text": "{\"taskId\":\"tsk-geuaywbthrhr9ux3\"}"
        }
      ]
    }
  ],
  "usage": {
    "total_tokens": 96000,
    "input_tokens": 0,
    "input_tokens_details": {
      "cached_tokens": 0
    },
    "output_tokens": 96000,
    "output_tokens_details": {
      "reasoning_tokens": 0
    }
  }
}
```

> `output[0].content[0].text` 字段为字符串化的 JSON，其中 `taskId` 即为后续查询所需的任务 ID。

## 获取结果 示例代码

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
import io
import sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
# ═══════════════════════════════════════════════════════════════
# 🔑 步骤1: 配置 API 连接信息
# ═══════════════════════════════════════════════════════════════

# 🌐 DMXAPI 服务端点地址
url = "https://www.dmxapi.cn/v1/responses"

# 🔐 DMXAPI 密钥 (请替换为您自己的密钥)
# 获取方式: 登录 DMXAPI 官网 -> 个人中心 -> API 密钥管理
api_key = "sk-************************************************"

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
    "model": "kling-v3-get-all",

    "input": "tsk-geuw5gb6s8ryza95",      
}
# ═══════════════════════════════════════════════════════════════
# 📤 步骤4: 发送请求并输出结果
# ═══════════════════════════════════════════════════════════════

# 发送 POST 请求到 API 服务器
response = requests.post(url, headers=headers, json=payload)
data = response.json()

# ═══════════════════════════════════════════════════════════════
# 📊 步骤5: 输出完整响应 + 视频清单
# ═══════════════════════════════════════════════════════════════

print("=" * 60)
print("完整响应")
print("=" * 60)
print(json.dumps(data, indent=2, ensure_ascii=False))

# Responses API 把上游真实 JSON 字符串化塞进 output[0].content[0].text，需要再解一层
try:
    inner = json.loads(data["output"][0]["content"][0]["text"])
    videos = (inner.get("data", {}).get("task_result") or {}).get("videos", [])
except (KeyError, IndexError, json.JSONDecodeError, TypeError):
    videos = []

if videos:
    print(f"\n视频输出（共 {len(videos)} 个）")
    for v in videos:
        print(f"  ┌─ id            {v.get('id')}")
        print(f"  │  时长          {v.get('duration')} 秒")
        print(f"  │  无水印 URL    {v.get('url')}")
        if v.get("watermark_url"):
            print(f"  │  水印版 URL    {v.get('watermark_url')}")
        print(f"  └─")


```
## 返回示例
```json
============================================================
完整响应
============================================================
{
  "request_id": "d64f6d06-1502-4c4d-afb3-d0df2a518826",
  "output": [
    {
      "type": "message",
      "content": [
        {
          "type": "output_text",
          "text": "{\"code\":0,\"message\":\"SUCCEED\",\"data\":{\"task_id\":\"tsk-geuw5gb6s8ryza95\",\"task_status\":\"succeed\",\"task_info\":{},\"task_result\":{\"videos\":[{\"id\":\"mda-geuw8fck3u66fy1j\",\"url\":\"https://gcdy5vxfrcse3j396atj.exp.bcevod.com/mda-geuw8fck3u66fy1j/_src/mda-geuw8fck3u66fy1j/geuwp24ng6n6wjqntz0f.mp4\",\"duration\":\"3.041\"}]},\"task_status_msg\":\"\",\"created_at\":1779192467289,\"updated_at\":1779192587534,\"final_unit_deduction\":\"9\"},\"request_id\":\"d64f6d06-1502-4c4d-afb3-d0df2a518826\"}"
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
视频输出（共 1 个）
  ┌─ id            mda-geuw8fck3u66fy1j
  │  时长          3.041 秒
  │  无水印 URL    https://gcdy5vxfrcse3j396atj.exp.bcevod.com/mda-geuw8fck3u66fy1j/_src/mda-geuw8fck3u66fy1j/geuwp24ng6n6wjqntz0f.mp4
  └─
```

## 部分主体参考列表

下表列举了一部分可在 `element_list.element_id` 中引用的预置主体，供快速试用与参考。

| 序号 | task_id | element_id | 元素名称 | 分类标签 |
|------|---------|------------|----------|----------|
| 1 | 171 | 171 | 天台 | 场景 |
| 2 | 170 | 170 | 雪地 | 场景 |
| 3 | 169 | 169 | 宋代园林 | 场景 |
| 4 | 168 | 168 | 咖啡店 | 场景 |
| 5 | 167 | 167 | 雪山 | 场景 |
| 6 | 166 | 166 | 东方明珠 | 场景 |
| 7 | 165 | 165 | 旧游戏厅 | 场景 |
| 8 | 164 | 164 | 外星地表 | 场景 |
| 9 | 163 | 163 | 城市雨夜街道 | 场景 |
| 10 | 162 | 162 | 童年卧室 | 场景 |
| 11 | 161 | 161 | 香港都市街道 | 场景 |
| 12 | 160 | 160 | 美国公路加油站 | 场景 |
| 13 | 159 | 159 | 寒穹堡垒 | 场景 |
| 14 | 158 | 158 | 办公室 | 场景 |
| 15 | 157 | 157 | 核列车 | 场景 |
| 16 | 156 | 156 | 戈壁 | 场景 |
| 17 | 155 | 155 | 沙漠落地窗 | 场景 |
| 18 | 153 | 153 | 花园 | 场景 |
| 19 | 152 | 152 | 天坛 | 场景 |
| 20 | 151 | 151 | 西施 | 人物 |
| 21 | 150 | 150 | 林黛玉 | 人物 |
| 22 | 149 | 149 | 曹操 | 人物 |
| 23 | 148 | 148 | 鲁迅 | 人物 |
| 24 | 147 | 147 | 女子高中生 | 人物 |
| 25 | 146 | 146 | 嘻哈老太 | 人物、热梗 |
| 26 | 145 | 145 | 非洲甜心 | 人物、热梗 |
| 27 | 144 | 144 | 冷酷青年 | 人物 |
| 28 | 143 | 143 | 暴躁小孩 | 人物、热梗 |
| 29 | 142 | 142 | 刺客 | 人物 |
| 30 | 140 | 140 | 恶魔之翼 | 道具 |
| 31 | 139 | 139 | 手机 | 道具 |
| 32 | 138 | 138 | 马桶搋子 | 道具 |
| 33 | 137 | 137 | 北极熊 | 道具、热梗 |
| 34 | 136 | 136 | 手捧花 | 道具 |
| 35 | 135 | 135 | 宝剑 | 道具 |
| 36 | 134 | 134 | 摩托车 | 道具 |
| 37 | 133 | 133 | 天使之翼 | 道具 |
| 38 | 131 | 131 | 飞剑 | 道具 |
| 39 | 130 | 130 | 飞龙 | 道具 |
| 40 | 129 | 129 | 扳手 | 道具 |
| 41 | 128 | 128 | 仙女豚鼠 | 动物、热梗 |
| 42 | 127 | 127 | 小猫 | 动物 |
| 43 | 126 | 126 | 松鼠 | 动物 |
| 44 | 125 | 125 | 水豚 | 动物 |
| 45 | 124 | 124 | 香蕉猫 | 动物、热梗 |
| 46 | 122 | 122 | 安卓猫 | 动物、热梗 |
| 47 | 121 | 121 | 蜘蛛蟹 | 动物、热梗 |
| 48 | 120 | 120 | 白色婚纱 | 服饰 |
| 49 | 119 | 119 | 小生古装 | 服饰、热梗 |
| 50 | 118 | 118 | 留洋白月光 | 服饰 |
| 51 | 117 | 117 | 小丑玩偶服 | 服饰、热梗 |
| 52 | 116 | 116 | 魔法袍 | 服饰 |
| 53 | 115 | 115 | 民国绅士西装 | 服饰 |
| 54 | 114 | 114 | 红西装礼服 | 服饰 |
| 55 | 113 | 113 | 马面裙 | 服饰 |
| 56 | 112 | 112 | 未来感眼镜 | 服饰 |
| 57 | 111 | 111 | 怀旧婚纱 | 服饰 |
| 58 | 109 | 109 | 虫洞 | 特效 |
| 59 | 108 | 108 | 雪花 | 特效 |
| 60 | 107 | 107 | 花瓣 | 特效 |

<p align="center">
  <small>© 2026 DMXAPI kling-v3 主体控制 图生视频</small>
</p>


