# Qwen3.8-Omni-Flash 文本输入 API 使用文档

基于 Qwen3.8-Omni-Flash 全模态模型的文本对话接口，通过 `/v1/chat/completions` 端点以 SSE 流式方式调用。模型上下文长度达 1M Token，默认开启思考（`reasoning_effort` 默认为 `xhigh`，实际有效档位为 none / low / medium / xhigh 四档），支持 `enable_search` 联网搜索与自动生效的隐式缓存，流末尾可返回 Token 用量。适合知识问答、内容总结和普通对话等场景。

## 接口地址

| 接口 | 请求方式 | URL |
|------|---------|-----|
| 文本输入 | POST | `https://www.dmxapi.cn/v1/chat/completions` |

:::warning
请妥善保管您的 API Key！严禁将密钥泄露给他人、硬编码到代码中或提交到公开的代码仓库。如果怀疑密钥已泄露，请立即前往 DMXAPI 官网重新生成。
:::

## 模型名称

- `qwen3.8-omni-flash`

## 文本输入示例代码

```python
import requests
import json

# ===============================================================
# 步骤1: 配置 API 连接信息
# ===============================================================

# DMXAPI 服务端点地址
url = "https://www.dmxapi.cn/v1/chat/completions"

# DMXAPI 密钥 (请替换为您自己的密钥)
# 获取方式: 登录 DMXAPI 官网 -> 个人中心 -> API 密钥管理
api_key = "sk-******************************************"

# ===============================================================
# 步骤2: 配置请求头
# ===============================================================

headers = {
    "Content-Type": "application/json",      # 指定请求体为 JSON 格式
    "Authorization": f"Bearer {api_key}",    # Bearer token 认证方式
}

# ===============================================================
# 步骤3: 配置请求参数
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

            # 【content】(string | array, 必填) 消息内容
            # 纯文本对话时为字符串；多模态输入时为对象数组
            "content": "请介绍一下皂荚树。",
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
    # 实际有效档位为 none / low / medium / xhigh 四档
    "reasoning_effort": "none",

    # 【enable_search】(boolean, 可选) 是否开启联网搜索
    "enable_search": True,

    # 【search_options】(object, 可选) 联网搜索配置
    "search_options": {
        # 【search_strategy】(string, 可选) 搜索策略
        # 可选值: "agent"
        "search_strategy": "agent",
    },

    # 注意: reasoning_effort 和 thinking_budget 不能同时设置，否则请求报错
    # 当前使用 reasoning_effort，因此不要同时填写:
    # "thinking_budget": 20,
}

# ===============================================================
# 步骤4: 定义流式响应解析函数
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
# 步骤5: 发送请求并输出结果
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

    response.raise_for_status()

    print("\n模型回复：")
    read_stream(response)


if __name__ == "__main__":
    main()
```

## 返回示例

```text
**皂荚树**（学名：*Gleditsia sinensis*），又称皂角树、猪牙皂，是豆科（Fabaceae）皂荚属的落叶乔木。它在中国有着悠久的栽培历史，不仅是一种重要的经济林木和园林绿化树种，还在传统医学和日常生活中扮演着独特角色。

以下是关于皂荚树的详细介绍：

### 1. 形态特征
*   **树干与枝条**：成年皂荚树可高达15-30米。最显著的特征是其枝干上通常长有粗壮、分枝状的**硬刺**（称为“皂荚刺”或“天丁”），这些刺可达数厘米至十几厘米长，非常坚硬，既是防御机制，也是中药材来源之一。
*   **叶片**：为二回羽状复叶，小叶呈卵形或椭圆形，边缘有细锯齿，夏季翠绿，秋季变黄脱落。
*   **果实**：结出扁平、长条形的**荚果**，成熟时由绿变黑褐色，表面常有一层白粉。荚果内含多粒种子，果肉富含胰皂质（Saponin）。
*   **花**：夏季开黄白色小花，总状花序，气味并不浓烈。

### 2. 主要用途

#### 🧼 天然清洁剂（洗涤用）
在化学合成洗涤剂普及之前，皂荚是中国民间最主要的清洁用品。
*   **原理**：皂荚果肉中含有丰富的**三萜皂苷**（Triterpenoid saponins），这是一种天然的表面活性剂。将其捣碎泡水后，会产生大量泡沫，具有良好的去污、乳化和发泡能力。
*   **应用**：古人常用其洗头、洗衣、洗碗，甚至用于制作化妆品（如胭脂粉的粘合剂）。因其温和、无残留且易生物降解，近年来又受到环保主义者和天然护肤品牌的青睐。

#### 💊 药用价值（中药）
皂荚全身皆可入药，在《本草纲目》等中医典籍中有详细记载：
*   **皂荚（果实）**：性温，味辛、咸；有小毒。功效包括祛痰开窍、散结消肿。常用于治疗中风痰迷、肺疾咳嗽、喉痹等症。
*   **猪牙皂**：指不育种子的畸形小荚果，药效更强，主要用于通窍。
*   **皂荚刺（天丁）**：具有托毒排脓、活血消痈的功效，常用于治疗疮疡肿毒。
*   **注意**：皂荚含有毒性成分，需经专业炮制并在医生指导下使用，不可自行随意服用。

#### 🌳 园林与生态价值
*   **绿化观赏**：树形高大优美，冠幅广阔，夏季遮阴效果好，秋季叶色金黄，是优良的行道树和庭荫树。
*   **抗逆性强**：耐干旱、耐瘠薄、耐寒，对土壤要求不严，能在石灰岩山地生长，因此也是中国北方及西南地区荒山造林的重要树种。
*   **固氮改良土壤**：作为豆科植物，其根部有根瘤菌，能固定空气中的氮气，提高土壤肥力。

#### 🪵 木材利用
皂荚木材质地坚硬，纹理美观，耐腐蚀，可用于制作家具、农具、雕刻工艺品等。但因树木生长较慢，大径级木材较少见。

### 3. 分布与生长环境
*   **地理分布**：原产于中国，广泛分布于华北、华东、华中、华南及西南各省区。此外，朝鲜半岛和日本也有分布。
*   **气候适应**：喜光，稍耐阴；适生于温暖湿润气候，但也能耐受一定程度的寒冷（部分品种可耐-20℃低温）。喜欢深厚、肥沃、排水良好的沙壤土，忌积水。

### 4. 文化寓意
*   **“皂白不分”**：成语“青红皂白”中的“皂”即指黑色，源于皂荚染色可得黑色染料。古代官员穿“皂衣”，故“皂隶”指衙门差役。
*   **吉祥象征**：在一些地区，皂荚树因寿命长、树冠庞大，被视为“风水树”或“神树”，种植于村头庙旁，象征庇佑子孙、家族兴旺。
*   **文学意象**：古诗文中常有提及，如唐代杜甫《戏作俳谐体遣闷》中“家家养乌鬼，顿顿食黄鱼……皂荚先秋晒，朱樱此日肥”，反映了当时人们利用皂荚的生活场景。

### 5. 现代研究与开发
随着绿色消费趋势兴起，皂荚提取物被广泛应用于：
*   **日化产品**：天然洗发水、沐浴露、婴儿洗护用品。
*   **农业助剂**：作为农药增效剂，帮助药液更好地附着在作物叶片上。
*   **食品工业**：少量用作天然乳化剂或起泡剂（需符合食品安全标准）。

---

✅ **温馨提示**：  
虽然皂荚是天然好物，但其水溶液对眼睛和黏膜有一定刺激性，使用时应避免接触眼部。若用于药用，请务必咨询专业中医师，切勿自行配方内服。

Token 用量：
{
  "completion_tokens": 1122,
  "completion_tokens_details": {
    "text_tokens": 1122
  },
  "prompt_tokens": 336,
  "prompt_tokens_details": {
    "cached_tokens": 0,
    "text_tokens": 336
  },
  "total_tokens": 1458
}
```

<p align="center">
  <small>© 2026 DMXAPI Qwen3.8-Omni-Flash 文本输入</small>
</p>
