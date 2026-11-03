#!/usr/bin/env python3
"""Run the actual Python fences in the Gemini docs against DMXAPI.

Install: pip install -U requests google-genai pydantic pillow
Prepare: python scripts/verify-gemini-docs.py --prepare (requires ffmpeg)
Run: DMXAPI_API_KEY=... python scripts/verify-gemini-docs.py
The key is injected in memory only. Generated fixtures/results stay under test/.
"""
from __future__ import annotations

import argparse
import ast
import concurrent.futures
import contextlib
import hashlib
import importlib.metadata
import io
import json
import math
import os
from pathlib import Path
import re
import subprocess
import sys
import time
from datetime import datetime
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]
WORK = ROOT / "test" / "gemini-3.8-flash"
MODEL = "gemini-3.8-flash"
VERIFIER_SHA256 = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
DOCS = [
    "gemini-chat", "gemini-chat-stream", "gemini-pdf", "gemini-video",
    "gemini-video1", "gemini-stt", "gemini-image", "gemini-image1",
    "gemini-json", "duolunduihua", "gemini-internet", "gemini-3",
    "gemini3-thinking-summary", "gemini-embedding-2-preview",
]
FENCES = re.compile(r"^```python[^\n]*\n(.*?)^```\s*$", re.M | re.S)


def cases():
    result = []
    for name in DOCS:
        source = (ROOT / f"{name}.md").read_text(encoding="utf-8")
        for index, match in enumerate(FENCES.finditer(source), 1):
            code = match.group(1)
            ast.parse(code)
            result.append({"id": f"{name}-{index}", "doc": f"{name}.md",
                           "block": index, "line": source[:match.start()].count("\n") + 1,
                           "sha256": hashlib.sha256(code.encode()).hexdigest(), "code": code})
    return result


def prepare():
    from PIL import Image, ImageDraw, ImageFont
    WORK.mkdir(parents=True, exist_ok=True)
    image = Image.new("RGB", (640, 360), "white")
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype("arial.ttf", 28) if os.name == "nt" else ImageFont.load_default(size=28)
    draw.text((30, 25), "DMXAPI TEST", fill="black", font=font)
    draw.ellipse((40, 110, 180, 250), fill="red")
    draw.rectangle((245, 110, 385, 250), fill="blue")
    draw.polygon([(500, 110), (430, 250), (570, 250)], fill="green")
    image.save(WORK / "fixture.jpg", quality=95)

    # A one-page, known-answer PDF; no third-party or personal document is uploaded.
    lines = ["DMXAPI TEST REPORT", "Project: Gemini 3.8 Flash", "Q1 revenue: 120",
             "Q2 revenue: 180", "Total revenue: 300", "Growth: 50 percent"]
    stream = ("BT /F1 20 Tf 50 760 Td " + " 0 -40 Td ".join(f"({line}) Tj" for line in lines) + " ET").encode()
    objects = [b"<< /Type /Catalog /Pages 2 0 R >>",
               b"<< /Type /Pages /Kids [3 0 R] /Count 1 >>",
               b"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 595 842] /Resources << /Font << /F1 4 0 R >> >> /Contents 5 0 R >>",
               b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>",
               b"<< /Length " + str(len(stream)).encode() + b" >>\nstream\n" + stream + b"\nendstream"]
    pdf = bytearray(b"%PDF-1.4\n")
    offsets = [0]
    for i, obj in enumerate(objects, 1):
        offsets.append(len(pdf))
        pdf.extend(f"{i} 0 obj\n".encode() + obj + b"\nendobj\n")
    start = len(pdf)
    pdf.extend(f"xref\n0 {len(offsets)}\n0000000000 65535 f \n".encode())
    for offset in offsets[1:]:
        pdf.extend(f"{offset:010} 00000 n \n".encode())
    pdf.extend(f"trailer\n<< /Size {len(offsets)} /Root 1 0 R >>\nstartxref\n{start}\n%%EOF\n".encode())
    (WORK / "fixture.pdf").write_bytes(pdf)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-loop", "1", "-i", str(WORK / "fixture.jpg"),
                    "-t", "3", "-r", "10", "-c:v", "libx264", "-pix_fmt", "yuv420p", str(WORK / "fixture.mp4")], check=True)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "lavfi", "-i", "sine=frequency=440:duration=3",
                    "-c:a", "libmp3lame", str(WORK / "tone.mp3")], check=True)
    audio_kind = "tone"
    if os.name == "nt":
        # Local Windows TTS; known text permits checking actual transcription.
        wave = str(WORK / "speech.wav").replace("'", "''")
        speech = ("Add-Type -AssemblyName System.Speech\n"
                  "$speaker = New-Object System.Speech.Synthesis.SpeechSynthesizer\n"
                  f"$speaker.SetOutputToWaveFile('{wave}')\n"
                  "$speaker.Speak('This is the Gemini audio test. The order number is four two seven. The total is one hundred eighty dollars.')\n"
                  "$speaker.Dispose()")
        subprocess.run(["powershell.exe", "-NoProfile", "-NonInteractive", "-Command", speech], check=True, timeout=30)
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(WORK / "speech.wav"), str(WORK / "fixture.mp3")], check=True)
        audio_kind = "speech"
    else:
        (WORK / "fixture.mp3").write_bytes((WORK / "tone.mp3").read_bytes())
    manifest = {path.name: {"bytes": path.stat().st_size, "sha256": hashlib.sha256(path.read_bytes()).hexdigest()}
                for path in WORK.glob("fixture.*")}
    manifest["fixture.mp3"]["kind"] = audio_kind
    (WORK / "fixtures.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    print(f"Prepared synthetic JPEG / PDF / 3-second MP4 / MP3 ({audio_kind}) fixtures.")


def redact(text):
    key = os.environ.get("DMXAPI_API_KEY", "")
    if key:
        text = text.replace(key, "[REDACTED]")
    text = re.sub(r"(?i)([?&](?:key|api_key)=)[^&\s\"']+", r"\1[REDACTED]", text)
    return re.sub(r'("thought(?:Signature|_signature)"\s*:\s*")[^"]*', r'\1[OMITTED]', text)


def output_matches(answer, stdout):
    """Ignore the examples' decorative line prefixes; still require the full answer."""
    stdout = re.sub(r"(?m)^\s*║ ?", "", stdout)
    try:
        expected = json.loads(answer)
    except ValueError:
        expected = None
    if expected is not None:
        decoder = json.JSONDecoder()
        for match in re.finditer(r"[\[{]", stdout):
            try:
                if decoder.raw_decode(stdout[match.start():])[0] == expected:
                    return True
            except ValueError:
                pass
        return False
    normalize = lambda value: re.sub(r"\s+", "", value.replace('\\"', '"').replace('\\n', '\n'))
    return bool(answer.strip()) and normalize(answer) in normalize(stdout)


def recheck_output(discovered):
    """Replay the one changed assertion against saved real output, with no API call."""
    target = WORK / "results.json"
    payload = json.loads(target.read_text(encoding="utf-8"))
    current = {case["id"]: case for case in discovered}
    # This predecessor differs only in decorative-border normalization. Never
    # bless arbitrary older validation logic as equivalent to the current checks.
    compatible = {VERIFIER_SHA256,
                  "30ce19cd917cca411bfa25ebd33855e5a03959f16270d5c8ee13d9ed951492ba",
                  "60c55dc416d97ef2bfcb64013b5b307fb092799dbde88da9ade7d87d401a3e9f"}
    fixture_info = json.loads((WORK / "fixtures.json").read_text(encoding="utf-8"))
    for row in payload["results"]:
        checks = [check for check in row.get("checks", []) if check["name"] == "文档代码实际打印完整最终答案"]
        if not checks or row.get("verifier_sha256") not in compatible:
            continue
        if row["sha256"] != current[row["id"]]["sha256"]:
            raise ValueError(f"Source changed: {row['id']}; run the example again.")
        if any(fixture_info.get(name) != info for name, info in row.get("fixtures", {}).items()):
            raise ValueError(f"Fixtures changed: {row['id']}; run the example again.")
        if not row.get("evidence_complete") and (len(row.get("final_answer", "")) >= 16000 or len(row.get("stdout", "")) >= 24000):
            raise ValueError(f"Possibly truncated evidence: {row['id']}; cannot promote a prefix to PASS.")
        before = json.loads(json.dumps(row))
        checks[0]["passed"] = output_matches(row.get("final_answer", ""), row.get("stdout", ""))
        row["status"] = "PASS" if all(check["passed"] for check in row["checks"]) else "FAIL"
        row["output_recheck"] = {"method": "saved stdout; remove decorative line borders only; no new API request",
                                 "previous_verifier_sha256": row["verifier_sha256"],
                                 "previous_recheck": row.get("output_recheck")}
        row["verifier_sha256"] = VERIFIER_SHA256
        row["line"] = current[row["id"]]["line"]
        if row["status"] != before["status"]:
            before["validation_issue"] = "装饰边框导致输出校验误报，已用同一次真实调用的完整输出复核。"
            payload.setdefault("history", []).append(before)
            print(f"Output recheck: {row['id']}: {before['status']} -> {row['status']}")
    target.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def execute(case):
    """Observe real transports and SDK returns without replacing their behavior."""
    import requests
    import httpx
    from google.genai import models

    key = os.environ["DMXAPI_API_KEY"]
    http = []
    responses = []
    first_text = None
    started = time.perf_counter()
    replacements = []

    def record(data):
        nonlocal first_text
        if not isinstance(data, dict):
            return
        responses.append(data)
        for candidate in data.get("candidates") or []:
            for part in (candidate.get("content") or {}).get("parts") or []:
                if part.get("text") and not part.get("thought") and first_text is None:
                    first_text = round(time.perf_counter() - started, 3)

    original_send = requests.Session.send
    def send(session, request, **kwargs):
        response = original_send(session, request, **kwargs)
        if urlsplit(request.url).hostname == "www.dmxapi.cn":
            http.append({"status": response.status_code, "path": urlsplit(request.url).path})
            if kwargs.get("stream"):
                original_lines = response.iter_lines
                def iter_lines(*args, **kw):
                    for line in original_lines(*args, **kw):
                        text = line.decode("utf-8") if isinstance(line, bytes) else line
                        if text and text.startswith("data:"):
                            try:
                                record(json.loads(text[5:].strip()))
                            except json.JSONDecodeError:
                                pass
                        yield line
                response.iter_lines = iter_lines
            else:
                try:
                    record(response.json())
                except ValueError:
                    pass
        return response
    requests.Session.send = send

    original_httpx_send = httpx.Client.send
    def httpx_send(client, request, **kwargs):
        response = original_httpx_send(client, request, **kwargs)
        if request.url.host == "www.dmxapi.cn":
            http.append({"status": response.status_code, "path": request.url.path})
        return response
    httpx.Client.send = httpx_send

    original_generate = models.Models.generate_content
    def generate(self, *args, **kwargs):
        response = original_generate(self, *args, **kwargs)
        record(response.model_dump(by_alias=True, exclude_none=True, mode="json"))
        return response
    models.Models.generate_content = generate
    original_stream = models.Models.generate_content_stream
    def generate_stream(self, *args, **kwargs):
        for response in original_stream(self, *args, **kwargs):
            record(response.model_dump(by_alias=True, exclude_none=True, mode="json"))
            yield response
    models.Models.generate_content_stream = generate_stream

    class Inputs(ast.NodeTransformer):
        def visit_Constant(self, node):
            if not isinstance(node.value, str):
                return node
            value = node.value
            if re.fullmatch(r"sk-\*+", value):
                return ast.copy_location(ast.Constant(key), node)
            # Only replace local media paths, never prompts, URLs, or request configuration.
            suffix = Path(value.replace("\\", "/")).suffix.lower()
            suffix = {".jpg": ".jpg", ".jpeg": ".jpg", ".png": ".jpg", ".mp3": ".mp3",
                      ".mp4": ".mp4", ".pdf": ".pdf"}.get(suffix)
            if suffix and not value.startswith(("http:", "https:")) and ("/" in value or "\\" in value):
                replacement = str(WORK / f"fixture{suffix}")
                replacements.append({"from": value, "to": f"synthetic fixture{suffix}"})
                return ast.copy_location(ast.Constant(replacement), node)
            return node

    output = io.StringIO()
    error = None
    namespace = {"__name__": "__main__", "__file__": str(ROOT / case["doc"])}
    try:
        tree = ast.fix_missing_locations(Inputs().visit(ast.parse(case["code"])))
        with contextlib.redirect_stdout(output), contextlib.redirect_stderr(output):
            exec(compile(tree, case["doc"], "exec"), namespace)
    except BaseException as exc:
        error = f"{type(exc).__name__}: {exc}"
    elapsed = round(time.perf_counter() - started, 3)
    answers, thoughts, versions, finishes, sources, usages, vectors = [], [], set(), set(), [], [], []
    for data in responses:
        if data.get("error"):
            error = error or json.dumps(data["error"], ensure_ascii=False)
        if data.get("modelVersion"):
            versions.add(data["modelVersion"])
        if data.get("usageMetadata"):
            usages.append(data["usageMetadata"])
        if data.get("embedding"):
            vectors.append(data["embedding"].get("values", []))
        vectors.extend(item.get("values", []) for item in data.get("embeddings", []))
        for candidate in data.get("candidates") or []:
            if candidate.get("finishReason"):
                finishes.add(candidate["finishReason"])
            for part in (candidate.get("content") or {}).get("parts") or []:
                if part.get("text"):
                    (thoughts if part.get("thought") else answers).append(part["text"])
            for chunk in (candidate.get("groundingMetadata") or {}).get("groundingChunks") or []:
                if chunk.get("web"):
                    web = chunk["web"]
                    source = {"title": web.get("title", ""), "uri": web.get("uri", "")}
                    if source not in sources:
                        sources.append(source)
    text = "".join(answers)
    response_texts = ["".join(part.get("text", "") for candidate in data.get("candidates", [])
                              for part in (candidate.get("content") or {}).get("parts", []) if not part.get("thought"))
                      for data in responses]
    streaming = "streamGenerateContent" in case["code"] or "generate_content_stream" in case["code"]
    final_text = text if streaming else (response_texts[-1] if response_texts else "")
    stdout = output.getvalue()
    fixture_info = json.loads((WORK / "fixtures.json").read_text(encoding="utf-8"))
    used_fixtures = {Path(item["to"].removeprefix("synthetic ")).name for item in replacements}
    checks = []
    def check(name, passed):
        checks.append({"name": name, "passed": bool(passed)})
    check("Python 示例执行无未处理异常", error is None)
    check("已观察到真实 API 请求且全部 HTTP 2xx", http and all(200 <= row["status"] < 300 for row in http))
    embedding = case["doc"] == "gemini-embedding-2-preview.md"
    if embedding:
        check("返回非空有限数值向量", vectors and all(v and all(isinstance(x, (float, int)) and math.isfinite(x) for x in v) for v in vectors))
        payload = namespace.get("payload", {})
        requests_to_embed = payload.get("requests", [payload])
        expected_dimensions = [item.get("output_dimensionality", item.get("outputDimensionality", 3072)) for item in requests_to_embed]
        check("向量数量与请求一致", len(vectors) == len(requests_to_embed))
        check("向量维度符合请求（默认 3072）", [len(v) for v in vectors] == expected_dimensions)
    else:
        check("返回非空最终文本", bool(final_text.strip()))
        check("服务返回 modelVersion 为 gemini-3.8-flash", versions == {MODEL})
        check("文档代码实际打印完整最终答案", output_matches(final_text, stdout))
    if streaming:
        check("收到多个流式数据块", len(responses) > 1)
        check("流式正常结束（STOP）", "STOP" in finishes)
    if case["doc"] in {"gemini-image.md", "gemini-video.md"} or (case["doc"] == "gemini-3.md" and case["block"] in {5, 6}):
        check("识别固定素材中的红色圆形和蓝色方形", bool(re.search(r"红|red", text, re.I)) and bool(re.search(r"蓝|blue", text, re.I)) and bool(re.search(r"圆|circle", text, re.I)) and bool(re.search(r"方|矩形|square|rectangle", text, re.I)))
    if case["doc"] == "gemini-image1.md":
        check("识别网络图片中的管风琴 / 多层键盘", bool(re.search(r"管风琴|organ|多层.*键盘", final_text, re.I)))
    if case["doc"] == "gemini-video1.md":
        check("识别网络视频中的 DMXAPI 品牌", "dmxapi" in final_text.lower())
    if case["doc"] in {"gemini-image1.md", "gemini-video1.md"}:
        check("未返回媒体访问失败答复", not re.search(r"无法(?:直接)?(?:访问|读取|观看|打开)|cannot access|unable to access", final_text, re.I))
    if case["doc"] == "gemini-pdf.md":
        check("提取 PDF 关键数字 120 / 180", "120" in text and "180" in text)
    if case["doc"] == "gemini-stt.md":
        fixture_info = json.loads((WORK / "fixtures.json").read_text(encoding="utf-8"))
        if fixture_info.get("fixture.mp3", {}).get("kind") == "speech":
            check("识别语音中的订单号 427 与金额 180", "427" in text and "180" in text)
        else:
            check("识别纯音 / 音调 / 无人声特征", bool(re.search(r"纯音|正弦|音调|蜂鸣|嗡|哔|嘟|单一|持续|tone|sine|beep", text, re.I)))
    if case["doc"] == "duolunduihua.md":
        check("根据历史回答 12 月 27 日（最后一轮）", bool(re.search(r"12\s*月\s*27|12[-/]27|December 27", final_text, re.I)))
        if case["block"] == 2:
            check("SDK 实际完成两轮有效回复", len(response_texts) == 2 and all(response_texts))
    if case["doc"] == "gemini3-thinking-summary.md":
        check("实际返回 thought=True 摘要文本", bool(thoughts))
        check("回答明确判断 9.8 更大", bool(re.search(r"9\.8\D{0,15}(?:大|>|＞)|9\.8\s*>\s*9\.11", text)))
    structured = case["doc"] == "gemini-json.md" or (case["doc"] == "gemini-3.md" and case["block"] in {7, 8})
    if structured:
        try:
            final_text = "".join(part.get("text", "") for candidate in responses[-1].get("candidates", [])
                                 for part in (candidate.get("content") or {}).get("parts", []) if not part.get("thought"))
            parsed = json.loads(final_text)
            if case["doc"] == "gemini-json.md":
                valid = isinstance(parsed, list) and len(parsed) > 0 and all(isinstance(item.get("recipeName"), str) and isinstance(item.get("ingredients"), list) and all(isinstance(x, str) for x in item["ingredients"]) for item in parsed)
            else:
                valid = isinstance(parsed, dict) and all(isinstance(parsed.get(k), str) for k in ["city", "temperature", "weather_condition"])
            check("JSON 可解析且必需字段符合类型", valid)
        except (ValueError, TypeError, AttributeError, IndexError):
            check("JSON 可解析且必需字段符合类型", False)
    if case["doc"] == "gemini-internet.md" or (case["doc"] == "gemini-3.md" and case["block"] in {7, 8}):
        check("实际返回搜索来源 groundingChunks", any(source["uri"] for source in sources))
        if case["doc"] == "gemini-3.md":
            check("搜索与 JSON 整理分别完成请求", len(responses) >= 2)
    result = {k: v for k, v in case.items() if k != "code"}
    result.update(status="PASS" if all(c["passed"] for c in checks) else "FAIL",
                  checked_at=datetime.now().astimezone().isoformat(timespec="seconds"),
                  duration_s=elapsed, first_text_s=first_text, http=http, model_versions=sorted(versions),
                  response_chunks=len(responses), finish_reasons=sorted(finishes), checks=checks,
                  answer=redact(text), final_answer=redact(final_text),
                  response_texts=[redact(value) for value in response_texts],
                  thought_chars=sum(map(len, thoughts)),
                  sources=sources, usage=usages[-1] if usages else None,
                  vector_dimensions=[len(v) for v in vectors], replacements=replacements,
                  verifier_sha256=VERIFIER_SHA256,
                  fixtures={name: fixture_info[name] for name in used_fixtures},
                  error=redact(error) if error else None, stdout=redact(stdout), evidence_complete=True)
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--prepare", action="store_true")
    parser.add_argument("--recheck-output", action="store_true", help="Offline replay of the decorative-border assertion fix")
    parser.add_argument("--child")
    parser.add_argument("--only", nargs="*")
    parser.add_argument("--workers", type=int, default=3)
    args = parser.parse_args()
    os.chdir(ROOT)
    sys.stdout.reconfigure(encoding="utf-8")
    WORK.mkdir(parents=True, exist_ok=True)
    if args.prepare:
        prepare()
        return
    discovered = cases()
    if args.recheck_output:
        recheck_output(discovered)
        return
    if args.child:
        result = execute(next(c for c in discovered if c["id"] == args.child))
        (WORK / f"{args.child}.json").write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
        return
    if not os.environ.get("DMXAPI_API_KEY"):
        parser.error("Set DMXAPI_API_KEY before making live requests.")
    # SDK examples using an environment fallback receive the same test key.
    os.environ["GEMINI_API_KEY"] = os.environ["DMXAPI_API_KEY"]
    selected = [c for c in discovered if not args.only or c["id"] in args.only]
    if not selected:
        parser.error("No matching cases.")
    target = WORK / "results.json"
    previous = json.loads(target.read_text(encoding="utf-8")) if target.exists() else {}
    rows = {row["id"]: row for row in previous.get("results", [])}
    history = previous.get("history", [])
    fixture_info = json.loads((WORK / "fixtures.json").read_text(encoding="utf-8"))
    for case in discovered:
        row = rows.get(case["id"])
        if not row:
            continue
        stale_source = row.get("sha256") != case["sha256"]
        stale_validation = row.get("verifier_sha256") != VERIFIER_SHA256
        stale_fixture = any(fixture_info.get(name) != info for name, info in row.get("fixtures", {}).items())
        if stale_source or (row.get("status") == "PASS" and (stale_validation or stale_fixture)):
            history.append(row)
            rows[case["id"]] = {k: v for k, v in case.items() if k != "code"} | {
                "status": "STALE", "error": "示例、校验器或素材已变更，需要复测。", "checks": [], "duration_s": None}
        else:
            row["line"] = case["line"]
    def run(case):
        child_path = WORK / f"{case['id']}.json"
        child_path.unlink(missing_ok=True)
        try:
            run = subprocess.run([sys.executable, str(Path(__file__).resolve()), "--child", case["id"]],
                                 capture_output=True, text=True, encoding="utf-8", timeout=210,
                                 env={**os.environ, "PYTHONIOENCODING": "utf-8"})
            if run.returncode or not child_path.exists():
                raise RuntimeError(redact(run.stderr[-2500:] or f"child exit {run.returncode}"))
            return json.loads(child_path.read_text(encoding="utf-8"))
        except Exception as exc:
            return {k: v for k, v in case.items() if k != "code"} | {"status": "FAIL", "error": redact(str(exc)), "checks": [], "duration_s": None}
    print(f"Syntax PASS: {len(discovered)} Python blocks. Running {len(selected)} live cases.", flush=True)
    with concurrent.futures.ThreadPoolExecutor(max_workers=args.workers) as pool:
        futures = {pool.submit(run, c): c for c in selected}
        for future in concurrent.futures.as_completed(futures):
            row = future.result()
            if row["id"] in rows and rows[row["id"]].get("status") != "STALE":
                history.append(rows[row["id"]])
            rows[row["id"]] = row
            print(f"{row['status']:4} {row['id']:38} {row.get('duration_s')}s " + "; ".join(c["name"] for c in row["checks"] if not c["passed"]), flush=True)
            payload = {"model": MODEL, "generated_at": datetime.now().astimezone().isoformat(timespec="seconds"),
                       "python": sys.version.split()[0], "packages": {name: importlib.metadata.version(name) for name in ["requests", "google-genai", "pydantic", "pillow"]},
                       "syntax_blocks": len(discovered), "results": [rows[c["id"]] for c in discovered if c["id"] in rows], "history": history}
            target.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Finished: {sum(r['status'] == 'PASS' for r in rows.values())}/{len(rows)} PASS. {target}", flush=True)
    sys.exit(0 if all(row["status"] == "PASS" for row in rows.values()) else 1)


if __name__ == "__main__":
    main()
