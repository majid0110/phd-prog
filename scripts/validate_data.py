#!/usr/bin/env python3
"""Validate data.js before committing. Exit code 1 on any problem.

Usage: python3 scripts/validate_data.py [path/to/data.js]
"""
import json
import re
import sys

path = sys.argv[1] if len(sys.argv) > 1 else "data.js"
src = open(path, encoding="utf-8").read().strip()
if not src.startswith("window.DATA="):
    sys.exit("data.js must start with 'window.DATA='")
d = json.loads(src[len("window.DATA="):].rstrip(";"))

errors = []
DATE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
CATS = {"positive", "apply", "negative", "auto", "unclear"}
STAGES = {"waiting", "apply", "applied", "check", "later"}
HEAT = {"hot", "warm"}
ATYPES = {"followup", "apply", "portal", "form", "reply"}
DSTATUS = {"confirmed", "expected", "check", "reminder"}
# Privacy: the site is public. No email addresses or forbidden terms anywhere.
FORBIDDEN = [re.compile(r"[\w.+-]+@[\w-]+\.[\w.]+"), re.compile(r"misis", re.I)]

for k in ["replies", "leads", "actions", "deadlines", "sent", "bounced", "updated", "updatedISO", "sentLog", "log"]:
    if k not in d:
        errors.append(f"missing key: {k}")

for i, r in enumerate(d.get("replies", [])):
    if r.get("cat") not in CATS:
        errors.append(f"replies[{i}] bad cat {r.get('cat')}")
    if not DATE.match(r.get("date", "")):
        errors.append(f"replies[{i}] bad date")
    if not r.get("uni") or not r.get("country"):
        errors.append(f"replies[{i}] missing uni/country")
for i, l in enumerate(d.get("leads", [])):
    if l.get("stage") not in STAGES:
        errors.append(f"leads[{i}] bad stage {l.get('stage')}")
    if l.get("heat") not in HEAT:
        errors.append(f"leads[{i}] bad heat")
for i, a in enumerate(d.get("actions", [])):
    if a.get("type") not in ATYPES or not DATE.match(a.get("due", "")):
        errors.append(f"actions[{i}] bad type/due")
for i, x in enumerate(d.get("deadlines", [])):
    if x.get("status") not in DSTATUS or not DATE.match(x.get("date", "")):
        errors.append(f"deadlines[{i}] bad status/date")

blob = json.dumps(d, ensure_ascii=False)
for pat in FORBIDDEN:
    m = pat.search(blob)
    if m:
        errors.append(f"privacy: forbidden text found: {m.group(0)!r}")

if errors:
    print("\n".join(errors))
    sys.exit(1)
print(f"OK: {len(d['replies'])} replies, {len(d['leads'])} leads, {len(d['actions'])} actions, "
      f"{len(d['deadlines'])} deadlines, sent={d['sent']}, updated={d['updated']}")
