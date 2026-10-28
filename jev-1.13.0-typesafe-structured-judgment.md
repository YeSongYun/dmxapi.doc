# jev-1.13.0 TypeSafe 结构化判研 API 使用文档

jev-1.13.0 是通过 DMXAPI TypeSafe 接口调用的结构化判研模型：把一段文本（如客服工单对话）作为共享上下文 `state`，一次请求同时提出多个问题，每个问题指定 3 种类型之一——choice（从给定选项中单选）、score（按档位评分）、noul（是 / 否判断），模型直接返回选中项、概率分布与置信度等机器可读的结构化结果，无需再解析自由文本。适合工单分级、满意度评估、意图识别等需要把自然语言对话转成可编程判定结果的场景。

## 📍 请求地址

```
https://www.dmxapi.cn/typesafe/v1/systemone
```

:::warning
请妥善保管您的 API Key！严禁将密钥泄露给他人、硬编码到代码中或提交到公开的代码仓库。如果怀疑密钥已泄露，请立即前往 DMXAPI 官网重新生成。
:::

## 🎯 模型名称

- `jev-latest`
- `jev-1.14.0`
- `jev-1.13.0`

## 🧩 问题类型说明

`questions` 中的每个问题通过 `type` 指定类型，不同类型对 `criteria` 的要求不同：

| type | 用途 | criteria 写法 | 示例问题 |
|------|------|---------------|----------|
| `choice` | 从给定选项中单选 | 对象，key 为选项名，value 为该选项的判定标准 | 紧急程度：低 / 中 / 高 |
| `score` | 按档位评分 | 数组，档位由低到高排列，示例为 5 档 | 客户满意度 |
| `noul` | 是 / 否判断（true / false） | 不需要 | 是否明确要求退款 |

## 💻 结构化判研 示例代码

对一段客服工单对话做结构化判研，一次请求同时问三类问题：紧急程度（choice）、客户满意度（score）、是否明确要求退款（noul）。

```python
import json
import urllib.error
import urllib.request

BASE_URL = "https://www.dmxapi.cn"
API_KEY = "sk-************************************************"  # 请改为你自己的 API Key，避免泄露
MODEL = "jev-1.14.0"

# 客服对话记录，作为共享上下文（state）传给所有问题
STATE = """
【客服工单 #20260921-017】
客户：我这个快递已经显示"运输中"整整六天了，一直没有更新，太离谱了！
客服：非常抱歉给您带来不便，我这边帮您查一下物流轨迹。
客户：查了也没用吧，上次也是这样一直拖，最后东西都过期了。这次要是再这样，
      我直接申请退款，不想要了。
客服：理解您的心情，我们会加急联系物流方核实。
客户：行吧，那你尽快，我明天就要用，再拖真的要退钱了。
"""

# 【questions】(object) 问题集合，key 为自定义的问题 ID，value 为问题定义
# 所有问题共享同一段 state 上下文，一次请求同时得到全部答案
QUESTIONS = {
    "urgency": {
        # 【type】(string) 问题类型
        # 可选值: "choice"(从 criteria 给定的选项中单选) / "score"(按 criteria 档位评分) / "noul"(true/false 判断)
        "type": "choice",
        # 【instructions】(string) 判断指令，告诉模型依据什么来回答这个问题
        "instructions": "根据客户的语气和诉求，判断这张工单需要被处理的紧急程度。",
        # 【criteria】(object) choice 类型的候选选项，key 为选项名，value 为该选项的判定标准
        "criteria": {
            "低": "客户语气平和，没有明确的时间压力或强烈不满",
            "中": "客户表达了不满，但尚未提出明确的最后期限或强硬诉求",
            "高": "客户情绪明显不满，并提出了明确的时间要求或退款威胁",
        },
    },
    "satisfaction": {
        "type": "score",
        "instructions": "根据对话中客户的措辞和情绪，评估客户当前对本次服务的满意度。",
        # 【criteria】(array) score 类型的评分档位，按从低到高排列，本例共 5 档
        "criteria": [
            "非常不满",
            "比较不满",
            "一般",
            "比较满意",
            "非常满意",
        ],
    },
    "refund_requested": {
        # noul 类型只需 type 与 instructions，不需要 criteria
        "type": "noul",
        "instructions": "判断客户是否已经明确提出，如果问题得不到解决就要退款。",
    },
}


def call_typesafe(state, questions, model=MODEL):
    url = BASE_URL.rstrip("/") + "/typesafe/v1/systemone"
    payload = json.dumps(
        {
            # 【model】(string) 模型名称，固定为 "jev-1.13.0"
            "model": model,
            # 【state】(string) 共享上下文，本例为客服工单对话记录，所有问题都基于这段文本判断
            "state": state,
            # 【questions】(object) 问题集合，见上方 QUESTIONS 定义
            "questions": questions,
        },
        ensure_ascii=False,
    ).encode("utf-8")

    request = urllib.request.Request(
        url,
        data=payload,
        method="POST",
        headers={
            "Authorization": "Bearer " + API_KEY,
            "Content-Type": "application/json",
            "Accept": "application/json",
        },
    )

    try:
        with urllib.request.urlopen(request, timeout=60) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as error:
        detail = error.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"TypeSafe 接口返回 HTTP {error.code}: {detail}") from error


def main():
    result = call_typesafe(STATE, QUESTIONS)

    print(f"模型: {result.get('model')}")
    print("判研结果:")
    for question_id, answer in result.get("answers", {}).items():
        print(f"  - {question_id}: {answer}")

    usage = result.get("usage")
    if usage:
        print(f"用量: {usage}")


if __name__ == "__main__":
    main()
```

## 📤 返回示例

```json
{
  "answers": {
    "refund_requested": {
      "noul": 0.96,
      "type": "noul"
    },
    "satisfaction": {
      "confidence": 0.64,
      "legend": {
        "0": "非常不满",
        "1": "比较不满",
        "2": "一般",
        "3": "比较满意",
        "4": "非常满意"
      },
      "probabilities": {
        "0": 0.57,
        "1": 0.43,
        "2": 0,
        "3": 0,
        "4": 0
      },
      "score": 0.43,
      "type": "score"
    },
    "urgency": {
      "choice": "高",
      "confidence": 1,
      "probabilities": {
        "中": 0,
        "低": 0,
        "高": 1
      },
      "type": "choice"
    }
  },
  "model": "jev-1.13.0",
  "usage": {
    "input_tokens": 715,
    "output_tokens": 72
  }
}
```

---
<p align="center">
  <small>© 2026 DMXAPI jev-1.13.0 TypeSafe 结构化判研</small>
</p>
