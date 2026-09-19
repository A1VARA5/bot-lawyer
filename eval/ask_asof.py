"""POST one question to /api/lawyer, optionally with asOf, and print the streamed answer plus timing.
Usage: python ask_asof.py --base http://localhost:3111 --q "question" [--asOf 2026-05-01] [--out file.json]"""
import json, sys, time, urllib.request, urllib.error
args = sys.argv[1:]
def opt(name, default=None):
    return args[args.index(name)+1] if name in args else default
base = opt("--base", "http://localhost:3111")
q = opt("--q")
asOf = opt("--asOf")
out = opt("--out")
body = {"messages": [{"id": "u1", "role": "user", "parts": [{"type": "text", "text": q}]}]}
if asOf: body["asOf"] = asOf
req = urllib.request.Request(base + "/api/lawyer", data=json.dumps(body).encode(), headers={"Content-Type": "application/json"})
t0 = time.time()
status = None
try:
    r = urllib.request.urlopen(req, timeout=240)
    status = r.status
    resp = r.read().decode("utf-8", "ignore")
except urllib.error.HTTPError as e:
    status = e.code
    resp = "data: " + json.dumps({"type": "error", "errorText": f"HTTP {e.code}: {e.read().decode('utf-8','ignore')[:300]}"})
except Exception as e:
    resp = "data: " + json.dumps({"type": "error", "errorText": str(e)})
dt = time.time() - t0
text, tools, err = [], [], None
for line in resp.splitlines():
    if not line.startswith("data:"): continue
    try: ev = json.loads(line[5:].strip())
    except Exception: continue
    t = ev.get("type", "")
    if t == "text-delta": text.append(ev.get("delta", ""))
    elif t == "tool-input-available": tools.append({"tool": ev.get("toolName"), "input": ev.get("input")})
    elif t == "error": err = ev.get("errorText")
answer = "".join(text)
res = {"base": base, "question": q, "asOf": asOf, "status": status, "seconds": round(dt, 1), "tools": tools, "error": err, "answer": answer}
if out:
    with open(out, "w", encoding="utf-8") as f: json.dump(res, f, indent=1, ensure_ascii=False)
print(f"status={status} seconds={dt:.1f} tools={[t['tool'] for t in tools]} error={err}")
print(answer)
