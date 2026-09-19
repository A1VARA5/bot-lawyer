# Validates seed/seed.ndjson against the schema shape and research/raw.
# Run: python seed/validate_seed.py  (from bot-lawyer/)
import json
import os
import re
import sys
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
RAW = os.path.join(ROOT, "research", "raw")
SEED = os.path.join(HERE, "seed.ndjson")

docs = [json.loads(line) for line in open(SEED, encoding="utf-8") if line.strip()]
by_id = {}
errors = []

# 1. unique ids
for d in docs:
    if d["_id"] in by_id:
        errors.append(f"duplicate _id {d['_id']}")
    by_id[d["_id"]] = d

# 2. every _ref resolves; every object array item has _key
def walk(node, path, doc_id):
    if isinstance(node, dict):
        if node.get("_type") == "reference":
            if node.get("_ref") not in by_id:
                errors.append(f"{doc_id}: dangling _ref {node.get('_ref')} at {path}")
        for k, v in node.items():
            walk(v, f"{path}.{k}", doc_id)
    elif isinstance(node, list):
        keys = []
        for i, item in enumerate(node):
            if isinstance(item, dict):
                if "_key" not in item:
                    errors.append(f"{doc_id}: array item without _key at {path}[{i}]")
                else:
                    keys.append(item["_key"])
            walk(item, f"{path}[{i}]", doc_id)
        if len(keys) != len(set(keys)):
            errors.append(f"{doc_id}: duplicate _key in {path}")

for d in docs:
    walk(d, d["_id"], d["_id"])

# 3. schema list values
SOURCE_KINDS = {"developerDocs", "developerPolicy", "developerTerms", "terms", "privacy", "guidelines", "monetizationTerms",
                "developerSupport", "userSupport", "changelog", "announcement", "github"}
INTENTS = {"MESSAGE_CONTENT", "GUILD_MEMBERS", "GUILD_PRESENCES"}
DATE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
for d in docs:
    t = d["_type"]
    if t == "source":
        if d["kind"] not in SOURCE_KINDS:
            errors.append(f"{d['_id']}: bad kind {d['kind']}")
        for f in ("publishedAt", "lastEditedAt", "snapshotAt"):
            if f in d and not DATE.match(d[f]):
                errors.append(f"{d['_id']}: bad date {f}={d[f]}")
    if t == "rule":
        for f in ("title", "area", "plainAnswer", "quote", "effectiveFrom", "source", "confidence"):
            if f not in d:
                errors.append(f"{d['_id']}: missing {f}")
        if d.get("confidence") not in ("confirmed", "inferred"):
            errors.append(f"{d['_id']}: bad confidence")
        for f in ("effectiveFrom", "effectiveTo"):
            if f in d and not DATE.match(d[f]):
                errors.append(f"{d['_id']}: bad date {f}")
        if "effectiveTo" in d and d["effectiveTo"] < d["effectiveFrom"]:
            errors.append(f"{d['_id']}: effectiveTo before effectiveFrom")
        aw = d.get("appliesWhen", {})
        for i in aw.get("intents", []):
            if i not in INTENTS:
                errors.append(f"{d['_id']}: bad intent {i}")
        if aw.get("verificationState") not in (None, "any", "unverified", "verified"):
            errors.append(f"{d['_id']}: bad verificationState")
        if aw.get("ownerAge") not in (None, "any", "16plus", "18plus"):
            errors.append(f"{d['_id']}: bad ownerAge")
        if d["area"]["_ref"] not in by_id or by_id[d["area"]["_ref"]]["_type"] != "policyArea":
            errors.append(f"{d['_id']}: area ref is not a policyArea")
        if by_id.get(d["source"]["_ref"], {}).get("_type") != "source":
            errors.append(f"{d['_id']}: source ref is not a source")
        if d.get("contradictionId") and not d.get("conflictsWith"):
            errors.append(f"{d['_id']}: contradictionId without conflictsWith")
        if d.get("contradictionId") and not d.get("resolution"):
            errors.append(f"{d['_id']}: contradictionId without resolution")
    if t == "question":
        if d.get("kind") not in ("standard", "trap", "unknown"):
            errors.append(f"{d['_id']}: bad kind")
        for r in d.get("expectedRules", []):
            if by_id.get(r["_ref"], {}).get("_type") != "rule":
                errors.append(f"{d['_id']}: expectedRules ref is not a rule")

# 4. conflicts are symmetric (both directions)
for d in docs:
    if d["_type"] != "rule":
        continue
    for c in d.get("conflictsWith", []):
        other = by_id[c["_ref"]]
        back = [x["_ref"] for x in other.get("conflictsWith", [])]
        if d["_id"] not in back:
            errors.append(f"conflict not symmetric: {d['_id']} -> {c['_ref']} but not back")

# 5. no em or en dashes in prose fields
DASHES = re.compile("[—–]")
for d in docs:
    for f in ("plainAnswer", "resolution", "notes", "title", "expectedAnswer", "description", "text", "note"):
        if f in d and isinstance(d[f], str) and DASHES.search(d[f]):
            errors.append(f"{d['_id']}: dash in {f}")

# 6. quotes verbatim in research/raw
LINK = re.compile(r"\[([^\]]+)\]\([^)]*\)")
ANGLE = re.compile(r"<(https?://[^>]+)>")
WS = re.compile(r"\s+")


def normalize(s):
    s = s.replace("\\_", "_").replace("\\*", "*").replace("\\$", "$")
    s = LINK.sub(r"\1", s)
    s = ANGLE.sub(r"\1", s)
    return WS.sub(" ", s).strip()


raw_cache = {}


def raw_text(fname):
    if fname not in raw_cache:
        raw_cache[fname] = open(os.path.join(RAW, fname), encoding="utf-8").read()
    return raw_cache[fname]


quote_report = []
exact = normalized = missing = 0
for d in docs:
    if d["_type"] != "rule":
        continue
    src = by_id[d["source"]["_ref"]]
    fname = src["snapshotFile"]
    text = raw_text(fname)
    q = d["quote"]
    if q in text:
        exact += 1
        quote_report.append((d["_id"], fname, "exact"))
    elif normalize(q) in normalize(text):
        normalized += 1
        quote_report.append((d["_id"], fname, "exact after markdown normalisation"))
    else:
        missing += 1
        quote_report.append((d["_id"], fname, "NOT FOUND"))
        errors.append(f"{d['_id']}: quote not found in {fname}")

counts = Counter(d["_type"] for d in docs)
print("counts:", dict(counts))
print(f"quotes: {exact} exact, {normalized} exact after markdown normalisation, {missing} missing")
print("contradictions:", sorted(Counter(d.get("contradictionId") for d in docs if d.get("contradictionId")).items()))
print("question kinds:", dict(Counter(d.get("kind") for d in docs if d["_type"] == "question")))
if errors:
    print("ERRORS:")
    for e in errors:
        print(" ", e)
    sys.exit(1)
print("OK: no errors")

if "--report" in sys.argv:
    for r in quote_report:
        print("|".join(r))
