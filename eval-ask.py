import json, sys, urllib.request, time
q = sys.argv[1]
body = {"messages":[{"id":"u1","role":"user","parts":[{"type":"text","text":q}]}]}
req = urllib.request.Request("http://localhost:3111/api/lawyer", data=json.dumps(body).encode(), headers={"Content-Type":"application/json"})
t0=time.time(); raw = urllib.request.urlopen(req, timeout=180).read().decode("utf-8","ignore"); dt=time.time()-t0
text=[]; tools=[]
for line in raw.splitlines():
    if not line.startswith("data:"): continue
    try: ev=json.loads(line[5:].strip())
    except Exception: continue
    t=ev.get("type","")
    if t=="text-delta": text.append(ev.get("delta",""))
    elif t=="tool-input-available": tools.append((ev.get("toolName"), json.dumps(ev.get("input"))[:200]))
    elif t=="error": print("ERROR EVENT:", ev)
print(f"--- {dt:.1f}s, {len(tools)} tool calls ---")
for n,i in tools: print(" *",n,i)
print("--- answer ---"); print("".join(text))
