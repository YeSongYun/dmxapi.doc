#!/usr/bin/env python3
"""Render saved, redacted Gemini documentation test results; makes no API calls."""
from __future__ import annotations

import argparse
import hashlib
import html
import json
import re
from pathlib import Path
import shutil
import statistics

ROOT = Path(__file__).resolve().parents[1]
WORK = ROOT / "test" / "gemini-3.8-flash"
TITLES = {
    "gemini-chat": "文本 · 非流式", "gemini-chat-stream": "文本 · SSE 流式",
    "gemini-pdf": "PDF 分析", "gemini-video": "本地视频", "gemini-video1": "网络视频",
    "gemini-stt": "音频分析", "gemini-image": "本地图片", "gemini-image1": "网络图片",
    "gemini-json": "JSON 结构化输出", "duolunduihua": "多轮对话", "gemini-internet": "联网搜索",
    "gemini-3": "开发者指南", "gemini3-thinking-summary": "思考总结", "gemini-embedding-2-preview": "多模态向量",
}
GUIDE = ["SDK 基础", "REST 基础", "SDK 思考等级", "REST 思考等级", "SDK 图片分辨率", "REST 图片分辨率", "SDK 搜索 → JSON", "REST 搜索 → JSON"]
EMBED = ["文本", "图片", "音频", "视频", "PDF", "多模态组合", "批量"]
VARIANTS = {
    "gemini-image": ["REST 流式", "SDK"],
    "gemini-image1": ["REST", "SDK"],
    "duolunduihua": ["REST", "SDK"],
    "gemini3-thinking-summary": ["非流式", "流式"],
}


def title(row):
    stem = Path(row["doc"]).stem
    index = row["block"] - 1
    suffix = GUIDE[index] if stem == "gemini-3" else EMBED[index] if stem == "gemini-embedding-2-preview" else VARIANTS[stem][index] if stem in VARIANTS else str(row["block"])
    return TITLES.get(stem, stem) + (f" / {suffix}" if stem in {"gemini-3", "gemini-embedding-2-preview", "gemini-image", "gemini-image1", "duolunduihua", "gemini3-thinking-summary"} else "")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--date", default="2026-11-03")
    args = parser.parse_args()
    date = args.date
    destination = ROOT / "public" / "reports" / f"gemini-3.8-flash-{date}"
    destination.mkdir(parents=True, exist_ok=True)
    data = json.loads((WORK / "results.json").read_text(encoding="utf-8"))
    fixture_info = json.loads((WORK / "fixtures.json").read_text(encoding="utf-8"))
    for name, info in fixture_info.items():
        asset = WORK / name
        if hashlib.sha256(asset.read_bytes()).hexdigest() != info["sha256"]:
            raise ValueError(f"Fixture file differs from manifest: {name}")
    for row in data["results"]:
        source = (ROOT / row["doc"]).read_text(encoding="utf-8")
        blocks = list(re.finditer(r"^```python[^\n]*\n(.*?)^```\s*$", source, re.M | re.S))
        block = blocks[row["block"] - 1]
        if hashlib.sha256(block.group(1).encode()).hexdigest() != row["sha256"]:
            raise ValueError(f"Result is stale for current source: {row['id']}")
        if any(fixture_info.get(name) != info for name, info in row.get("fixtures", {}).items()):
            raise ValueError(f"Result is stale for current fixtures: {row['id']}")
        row["line"] = source[:block.start()].count("\n") + 1
    # Publish portable paths, with no user-profile or machine-specific directory names.
    def portable(value):
        if isinstance(value, str):
            return value.replace(str(WORK), "test/gemini-3.8-flash").replace(str(ROOT), "[workspace]")
        if isinstance(value, list):
            return [portable(item) for item in value]
        if isinstance(value, dict):
            return {key: portable(item) for key, item in value.items()}
        return value
    data = portable(data)
    for row in data["results"] + data.get("history", []):
        row["title"] = title(row)
        row["group"] = "embedding" if row["doc"] == "gemini-embedding-2-preview.md" else "generation"
        row["blocked"] = row["status"] == "FAIL" and "model_not_found" in (row.get("error") or "")
    data["fixtures"] = fixture_info
    data["method"] = {
        "execution": "提取 Markdown 中实际 Python 代码块，AST 仅替换密钥与本地素材路径；保留提示词、模型和请求参数。使用真实 requests / Google GenAI SDK 调用。",
        "validation": "检查 HTTP、响应 modelVersion、代码实际打印的答案、流式结束、已知素材内容、最终一轮日期、JSON 结构、搜索来源及 thought 摘要。",
        "limits": "单次功能抽检，不是压力测试或可用性 SLA；耗时含代码执行及远程素材下载。未验证的思考等级、文件上限及配额不作保证。",
    }
    build_path = WORK / "build-check.json"
    data["build"] = json.loads(build_path.read_text(encoding="utf-8")) if build_path.exists() else {"status": "PENDING"}
    for filename in ("fixture.jpg", "fixture.pdf", "fixture.mp3", "fixture.mp4"):
        shutil.copyfile(WORK / filename, destination / filename)
    (destination / "results.json").write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    safe_json = json.dumps(data, ensure_ascii=False).replace("<", "\\u003c")
    page = TEMPLATE.replace("__DATE__", html.escape(date)).replace("__DATA__", safe_json)
    (destination / "index.html").write_text(page, encoding="utf-8")

    generative = [row for row in data["results"] if row["group"] == "generation"]
    embedded = [row for row in data["results"] if row["group"] == "embedding"]
    passed = sum(row["status"] == "PASS" for row in generative)
    embedding_pass = sum(row["status"] == "PASS" for row in embedded)
    median = statistics.median(row["duration_s"] for row in generative if row.get("duration_s") is not None)
    link = f"/reports/gemini-3.8-flash-{date}"
    rows = []
    for row in data["results"]:
        status = "通过" if row["status"] == "PASS" else "阻塞：503 无可用渠道" if row["blocked"] else row["status"]
        duration = f'{row["duration_s"]:.3f}' if row.get("duration_s") is not None else "—"
        rows.append(f'| {row["title"]} | [{row["doc"][:-3]}](/' + row["doc"][:-3] + f') · 代码块 {row["block"]} | {status} | {duration} |')
    markdown = f'''# Gemini 3.8 Flash 文档实测报告

测试日期：**{date}**。本次使用提供的测试密钥，对“Gemini 请求格式”下的真实 Python 代码进行远程 API 调用。报告和提交文件不包含密钥。

[打开交互式报告：结果筛选、实际回答、耗时与素材]({link}/index.html) · [下载脱敏 JSON 证据]({link}/results.json)

## 结果

| 范围 | 结果 |
| --- | --- |
| Gemini 3.8 Flash 生成与分析 | **{passed}/{len(generative)} 通过** |
| 专用嵌入模型 | **{embedding_pass}/{len(embedded)} 通过**；当前密钥分组返回 503 / model_not_found |
| Python 语法 | **{data['syntax_blocks']} 个代码块通过** |
| 生成类示例耗时中位数 | {median:.3f} 秒，含代码执行与远程素材下载 |
| 文档构建 | {data['build']['status']} |

13 篇生成与分析文档统一使用 `gemini-3.8-flash`。向量化文档继续使用 `gemini-embedding-2-preview`，因为 `embedContent` / `batchEmbedContents` 返回数值向量，不能直接替换为生成模型。

## 实际观察与修正

- **搜索 + JSON**：原单次组合请求返回 JSON，但 SDK / REST 都没有返回搜索来源。改为先搜索并确认来源、再整理 JSON；报告记录原失败尝试和最终复测结果。
- **音频**：3 秒 440 Hz 纯音收到 HTTP 200，却被回答为“没有提供音频”，判定失败。最终使用已知内容的合成语音，校验订单号 **427** 和金额 **180**，不把 HTTP 200 当成内容正确。
- **超时**：测试期间 SDK 基础调用、思考等级、图片、多轮和思考总结等出现过超时。报告保留这些历史失败；最终状态取最近一次实际执行结果，不能据此保证长期稳定性。
- **流式思考总结未通过**：首轮曾返回 `thought=True` 摘要，后续一次只返回最终答案、一次读取超时。最终状态为失败，报告保留成功及失败证据；非流式思考总结已通过本次实测。
- **嵌入服务阻塞**：7 个示例均返回 `503 model_not_found`，错误提示 `default` 分组没有 `gemini-embedding-2-preview` 可用渠道。需开通该模型通道后再次验证。
- **输出校验修正**：网络图片和网络视频的装饰边框曾导致校验器误报。对同一次真实调用的完整输出去除行首边框后重新比对，不重新发送请求；修正记录保存在 JSON 的 `output_recheck` 与历史中。
- **输出处理**：修正 SSE 对冒号后空格的假设，并合并视频回复中所有非思考文本，避免签名部分导致答案丢失。

## 测试素材与校验

使用自行生成的素材：红圆 / 蓝方 / 绿三角图片、同画面的 3 秒 MP4、含 Q1=120 / Q2=180 的 PDF，以及已知订单号与金额的语音。网络图片与视频使用更新后示例中的公开地址，分别校验管风琴与 DMXAPI 内容。交互报告提供素材预览、每项断言、响应来源、正文和脱敏输出。

测试直接提取 Markdown 的 Python 代码块，只替换测试密钥和本地媒体路径；保留提示词、模型和请求参数。每条结果记录代码 SHA-256，复测器会使代码、校验器或素材已变更的旧通过结果失效。

环境：Python `{data['python']}`；requests `{data['packages']['requests']}`；google-genai `{data['packages']['google-genai']}`；pydantic `{data['packages']['pydantic']}`。

## 逐项结果

| 示例 | 文档 | 最终结果 | 耗时 / 秒 |
| --- | --- | --- | --- |
''' + "\n".join(rows) + '''

## 本地复测

安装 `requests google-genai pydantic pillow`，并确保 `ffmpeg` 在 PATH 中。Windows 使用系统语音合成制作已知内容的语音；其他系统默认使用纯音素材，应另行验证非语音识别结果。

```powershell
pip install -U requests google-genai pydantic pillow
python scripts/verify-gemini-docs.py --prepare
$env:DMXAPI_API_KEY = "填写你自己的密钥"
python scripts/verify-gemini-docs.py
```

只复测部分示例可添加 `--only gemini-stt-1 gemini-3-7`。所有检查通过才返回退出码 0；当前嵌入通道阻塞时，完整测试返回 1。历史结果保存在 `test/gemini-3.8-flash/results.json`，该目录不提交。

生成报告：`python scripts/render-gemini-report.py --date 2026-11-03`。本报告是当前密钥、当前通道的一次功能测试，不是性能基准或稳定性保证。
'''
    (ROOT / "gemini-3.8-flash-test-report.md").write_text(markdown, encoding="utf-8")
    print(f"Generated {destination / 'index.html'} and gemini-3.8-flash-test-report.md")


TEMPLATE = r'''<!doctype html>
<html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Gemini 3.8 Flash · 实测报告</title>
<style>
:root{color-scheme:light;--ink:#162437;--muted:#536579;--line:#dce5ed;--green:#167449;--red:#b33742;--amber:#8b610d;--blue:#1b58bf}*{box-sizing:border-box}body{margin:0;background:#f3f6fa;color:var(--ink);font-family:system-ui,"Microsoft YaHei",sans-serif;line-height:1.6}main{max-width:1200px;margin:auto;padding:36px 24px 70px}header{padding:30px 34px;border-radius:20px;background:linear-gradient(120deg,#142e51,#1d5378);color:#fff}header p{max-width:920px;color:#dae9f5}h1{font-size:32px;line-height:1.25;margin:8px 0 12px}h2{font-size:22px;margin:30px 0 14px}h3{margin:0 0 10px;font-size:17px}.eyebrow{letter-spacing:.08em;font-size:12px;text-transform:uppercase}.cards{display:grid;grid-template-columns:repeat(4,1fr);gap:16px;margin:22px 0}.card,.panel{border:1px solid var(--line);border-radius:14px;padding:21px;background:white}.card strong{font-size:31px;display:block}.card span,.muted{color:var(--muted);font-size:13px}.pass{color:var(--green)}.fail{color:var(--red)}.blocked{color:var(--amber)}a{color:var(--blue);overflow-wrap:anywhere}.notice{border-left:4px solid #d29b21;margin:14px 0;padding:13px 17px;background:#fff9e8;border-radius:5px}.notes{display:grid;grid-template-columns:1fr 1fr;gap:14px}.notes p{margin:0;font-size:14px}.toolbar{display:flex;flex-wrap:wrap;gap:9px;align-items:center;margin:18px 0}button,input{font:inherit;border:1px solid #c5d3e0;background:#fff;border-radius:8px;padding:7px 12px;color:var(--ink)}button{cursor:pointer}button[aria-pressed=true]{background:#1b58bf;color:white;border-color:#1b58bf}input{flex:1;min-width:190px}table{width:100%;border-collapse:collapse;background:#fff;font-size:14px}th{text-align:left;color:var(--muted);background:#edf3f9;padding:11px}td{padding:12px 11px;border-top:1px solid var(--line);vertical-align:top}th:nth-child(1){width:12%}th:nth-child(2){width:31%}th:nth-child(3){width:18%}.table-wrap{overflow:auto;border:1px solid var(--line);border-radius:12px}.badge{display:inline-block;padding:2px 8px;border-radius:5px;font-size:12px;font-weight:700;background:#eaf4ef}.badge.fail{background:#fcecef}.badge.blocked{background:#fcf2d9}.bar{height:5px;background:#d7e7fa;border-radius:3px;margin-top:7px;max-width:130px}.bar i{display:block;height:100%;background:#3979bc;border-radius:3px}details summary{cursor:pointer;color:var(--blue)}.detail-body{padding:8px 5px 16px}pre{white-space:pre-wrap;overflow-wrap:anywhere;background:#f2f5f8;border:1px solid var(--line);border-radius:8px;padding:15px;font:13px/1.65 ui-monospace,Consolas,monospace;max-height:430px;overflow:auto}.checks{padding-left:22px;font-size:13px}.assets{display:grid;grid-template-columns:1fr 1fr;gap:20px}.assets img,.assets video{width:100%;display:block;max-height:300px;object-fit:contain;border-radius:8px;background:#fff}.assets audio{width:100%;margin:12px 0}footer{color:var(--muted);font-size:13px;margin-top:30px}.history-item{padding:12px 0;border-top:1px solid var(--line)}.history-item:first-child{border-top:0}.history-item p{font-size:13px;margin:5px 0}.legend{font-size:13px;color:var(--muted)}@media(max-width:750px){main{padding:18px 14px}header{padding:22px}h1{font-size:25px}.cards{grid-template-columns:1fr 1fr}.notes,.assets{grid-template-columns:1fr}.card{padding:16px}table{min-width:660px}}
</style></head><body><main>
<header><div class="eyebrow">DMXAPI / Documentation verification / __DATE__</div><h1>Gemini 3.8 Flash 文档实测报告</h1><p id="headline"></p><div>真实 API 调用 · 原文代码执行 · 失败历史保留 · 密钥已脱敏</div></header>
<section class="cards" id="cards"></section>
<div class="notice" id="generation-limit"></div>
<div class="notice"><strong>向量接口仍有阻塞：</strong>gemini-embedding-2-preview 返回 503 / model_not_found，当前密钥分组没有可用渠道。该接口需要专用嵌入模型，无法通过替换成 Flash 修复。</div>
<section><h2>本次验证发现了什么</h2><div class="notes">
<div class="panel"><h3>搜索先验证来源，再整理 JSON</h3><p>单次组合请求虽返回 JSON，但 SDK / REST 都没有搜索来源。最终代码改为两次请求，先检查 groundingChunks，再将已搜索到的内容整理成 JSON。</p></div>
<div class="panel"><h3>音频内容正确才算通过</h3><p>3 秒纯音返回 HTTP 200，却被回答为“未提供音频”，因此记为失败。语音样例包含订单号 427 和金额 180，用于核对实际识别结果。</p></div>
<div class="panel"><h3>超时记录保留</h3><p>测试中多项 SDK 调用曾超时，包括基础调用、思考等级、图片、多轮和思考总结。下方展示最近一次执行结果，历史失败可展开查看；一次复测通过不代表长期稳定性。</p></div>
<div class="panel"><h3>检验用户实际看到的输出</h3><p>校验器同时检查 HTTP、模型版本、正确内容和代码打印出的最终答案。SSE 兼容可省略的空格，视频提取会跳过签名部分并合并完整文本。</p></div>
</div></section>
<section><h2>逐项结果与实际回答</h2><p class="legend">点击“查看真实结果”可展开完整答案、来源、断言、HTTP 状态与代码摘要。耗时包含代码执行和远程媒体下载，不是纯模型延迟。</p>
<div class="toolbar" role="group" aria-label="筛选测试结果"><button data-filter="all" aria-pressed="true">全部</button><button data-filter="PASS" aria-pressed="false">通过</button><button data-filter="failed" aria-pressed="false">失败 / 阻塞</button><button data-filter="generation" aria-pressed="false">生成与分析</button><button data-filter="embedding" aria-pressed="false">向量</button><input id="search" type="search" aria-label="搜索示例" placeholder="搜索：音频、SDK、PDF…"></div>
<p class="legend" id="count" aria-live="polite"></p><div class="table-wrap"><table><thead><tr><th>状态</th><th>示例</th><th>执行耗时</th><th>结果摘要</th></tr></thead><tbody id="rows"></tbody></table></div></section>
<section><h2>测试素材</h2><div class="assets"><div class="panel"><h3>已知内容的图片与文档</h3><img src="fixture.jpg" alt="测试图片：红色圆形、蓝色方形、绿色三角形，标题 DMXAPI TEST"><p>图片：核对红圆与蓝方。<br>PDF：Q1=120，Q2=180，合计 300，增长 50%。</p><a href="fixture.pdf" target="_blank" rel="noopener">打开测试 PDF</a></div><div class="panel"><h3>3 秒视频与合成语音</h3><video controls preload="metadata" poster="fixture.jpg" src="fixture.mp4"></video><audio controls preload="metadata" src="fixture.mp3"></audio><p class="legend">语音原文：This is the Gemini audio test. The order number is four two seven. The total is one hundred eighty dollars.</p></div></div></section>
<section><h2>历史失败尝试</h2><details class="panel"><summary id="history-title"></summary><div id="history"></div></details></section>
<section><h2>方法与可复查证据</h2><div class="panel"><p id="method"></p><p id="environment" class="muted"></p><p><a href="results.json" download>下载脱敏 JSON 结果</a> · 原始代码 SHA-256、素材 SHA-256、校验器摘要和失败记录均保存在结果中。</p><p class="muted">每个测试只替换密钥与本地媒体路径，不替换提示词、请求参数或响应。报告依据接口返回的 modelVersion 记录模型；未把旧文档的格式示例当成本次实测输出。</p></div></section>
<footer>本报告为当前密钥与通道的功能抽检，不是压力测试、性能基准或稳定性保证。向量通道恢复后需重新验证。报告可离线打开，无外部字体或脚本依赖。</footer>
</main><script>
const data=__DATA__;
const esc=v=>String(v??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const gen=data.results.filter(r=>r.group==='generation'), emb=data.results.filter(r=>r.group==='embedding');
const failedGen=gen.filter(r=>r.status!=='PASS');
const limitation=document.querySelector('#generation-limit');
limitation.hidden=failedGen.length===0;
limitation.textContent='生成类未通过项：'+failedGen.map(r=>r.title).join('、')+'。流式思考总结首轮曾成功，后续出现无摘要和超时，最终仍按失败记录。';
const good=rows=>rows.filter(r=>r.status==='PASS').length;
const durations=gen.map(r=>r.duration_s).filter(v=>typeof v==='number').sort((a,b)=>a-b);
const median=durations.length?(durations[Math.floor((durations.length-1)/2)]+durations[Math.floor(durations.length/2)])/2:0;
document.querySelector('#headline').textContent=`生成与分析 ${good(gen)}/${gen.length} 通过；向量 ${good(emb)}/${emb.length} 通过。最终结果与历史失败分开展示，下面可直接查看每个示例的实际返回内容。`;
document.querySelector('#cards').innerHTML=[['生成与分析',`${good(gen)} / ${gen.length}`,'通过实测','pass'],['嵌入模型',`${good(emb)} / ${emb.length}`,'当前通道阻塞','blocked'],['Python 语法',`${data.syntax_blocks} / ${data.syntax_blocks}`,'代码块可解析','pass'],['耗时中位数',`${median.toFixed(2)} s`,'生成类示例最终执行','']].map(([label,value,note,cls])=>`<div class="card"><span>${label}</span><strong class="${cls}">${value}</strong><span>${note}</span></div>`).join('');
let filter='all',query='';
function render(){const rows=data.results.filter(r=>(filter==='all'||filter==='failed'&&r.status!=='PASS'||r.status===filter||r.group===filter)&&`${r.title} ${r.id}`.toLowerCase().includes(query));
document.querySelector('#count').textContent=`显示 ${rows.length} / ${data.results.length} 项。`;
document.querySelector('#rows').innerHTML=rows.map(r=>{const cls=r.status==='PASS'?'pass':r.blocked?'blocked':'fail';const label=r.status==='PASS'?'通过':r.blocked?'阻塞':r.status;const answer=r.final_answer||r.answer||r.error||'无结果';const evidence={checked_at:r.checked_at,model_versions:r.model_versions,http:r.http,first_text_s:r.first_text_s,response_chunks:r.response_chunks,thought_chars:r.thought_chars,usage:r.usage,code_sha256:r.sha256,verifier_sha256:r.verifier_sha256,fixtures:r.fixtures};return `<tr><td><span class="badge ${cls}">${label}</span></td><td><strong>${esc(r.title)}</strong><div class="muted">${esc(r.doc)} · 代码块 ${r.block}</div></td><td>${r.duration_s==null?'—':r.duration_s.toFixed(3)+' 秒'}<div class="bar"><i style="width:${Math.min(100,(r.duration_s||0)/120*100)}%"></i></div><span class="muted">HTTP ${esc((r.http||[]).map(h=>h.status).join(' / ')||'无响应')}</span></td><td>${esc(answer.slice(0,110))}${answer.length>110?'…':''}<details><summary>查看真实结果</summary><div class="detail-body"><h3>${r.error?'错误 / 回答':'实际最终回答'}</h3><pre>${esc(answer)}</pre>${r.sources?.length?'<h3>返回的搜索来源</h3><ul>'+r.sources.map(s=>'<li>'+esc(s.title)+'<br>'+esc(s.uri)+'</li>').join('')+'</ul>':''}<h3>校验断言</h3><ul class="checks">${(r.checks||[]).map(c=>`<li class="${c.passed?'pass':'fail'}">${c.passed?'✓':'✗'} ${esc(c.name)}</li>`).join('')}</ul><details><summary>请求证据与代码摘要</summary><pre>${esc(JSON.stringify(evidence,null,2))}</pre></details><details><summary>代码实际打印的内容</summary><pre>${esc(r.stdout||'未取得输出')}</pre></details></div></details></td></tr>`}).join('');}
document.querySelectorAll('[data-filter]').forEach(b=>b.addEventListener('click',()=>{filter=b.dataset.filter;document.querySelectorAll('[data-filter]').forEach(x=>x.setAttribute('aria-pressed',String(x===b)));render()}));document.querySelector('#search').addEventListener('input',e=>{query=e.target.value.trim().toLowerCase();render()});render();
const failures=(data.history||[]).filter(r=>r.status==='FAIL');document.querySelector('#history-title').textContent=`展开 ${failures.length} 条历史失败记录（不覆盖最终结果）`;
document.querySelector('#history').innerHTML=failures.map(r=>`<div class="history-item"><strong>${esc(r.title)}</strong><p>${esc(r.checked_at||'首轮超时')} · ${r.duration_s??'超时'} 秒</p><p class="fail">${esc(r.validation_issue||r.error||(r.checks||[]).filter(c=>!c.passed).map(c=>c.name).join('；'))}</p><details><summary>当时返回的内容</summary><pre>${esc(r.answer||r.stdout||'请求未完成')}</pre></details></div>`).join('');
document.querySelector('#method').textContent=data.method.execution+' '+data.method.validation;
document.querySelector('#environment').textContent=`测试环境：Python ${data.python} / requests ${data.packages.requests} / google-genai ${data.packages['google-genai']} / pydantic ${data.packages.pydantic}。文档构建：${data.build.status}。生成时间：${data.generated_at}。`;
</script></body></html>'''

if __name__ == "__main__":
    main()
