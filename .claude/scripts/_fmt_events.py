#!/usr/bin/env python3
"""Render progress.jsonl lines as a compact event log. Reads stdin."""
import json
import sys

for line in sys.stdin:
    line = line.strip()
    if not line:
        continue
    try:
        e = json.loads(line)
    except ValueError:
        continue
    ts = e.get("ts", "")[11:19]
    detail = str(e.get("detail", ""))[:90]
    print("  %s  %-22s %s" % (ts, e.get("event", ""), detail))
