#!/usr/bin/env python3
"""สัมผัสในของสุนทรภู่ — ค่าเฉลี่ย การกระจายรายบท และรายเรื่อง

    python3 tools/inner_rhyme_stats.py > data/inner_rhyme_stats.txt

`calibrate.py` รายงานสัมผัสในเป็นเปอร์เซ็นต์รวมกับเปอร์เซ็นต์บทที่มีอย่างน้อยหนึ่งวรรค
ไฟล์นี้แตกออกมาดูว่า **บทหนึ่งท่านใส่สัมผัสในกี่วรรค** ซึ่งเป็นตัวเลขที่บอกที่มาของ
TH-KL-09 ได้ตรงกว่า: เกณฑ์ข้อนั้นมีสองชั้นเพราะเปอร์เซ็นต์รวมอย่างเดียวผ่านได้
ทั้งที่บางบทเหลือศูนย์วรรค

⚠️ ตัวเลขผูกกับตัวแบ่งพยางค์ใน `thai_prosody.py` เปลี่ยนตัวแบ่งต้องรันใหม่ทั้งชุด
"""
from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import klon_rules as R  # noqa: E402
from calibrate import MIN_ALIGN  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
CORPUS = ROOT / "data" / "corpus"


def main() -> int:
    registry = json.loads((CORPUS / "works.json").read_text(encoding="utf-8"))["works"]
    dist: Counter[int] = Counter()
    per_work: dict[str, tuple[float, int]] = {}
    total_verses = total_ok = 0

    for w in registry:
        if w["tier"] != "core":
            continue
        ok = verses = 0
        with (CORPUS / w["file"]).open(encoding="utf-8") as fh:
            for line in fh:
                b = json.loads(line)
                if len(b["v"]) != 4 or b.get("open") or b.get("ragged"):
                    continue
                if b.get("a", 1.0) < MIN_ALIGN:
                    continue
                n = sum(R.inner_rhyme_verses(b["v"]))
                dist[n] += 1
                ok += n
                verses += 4
        if verses:
            per_work[w["title"]] = (100 * ok / verses, verses // 4)
        total_ok += ok
        total_verses += verses

    print(f"รวม tier core: {total_verses // 4:,} บท / {total_verses:,} วรรค")
    print(f"สัมผัสใน {100 * total_ok / total_verses:.1f}% ของวรรค"
          f"  =  เฉลี่ย {4 * total_ok / total_verses:.2f} วรรคจาก 4 ต่อบท")

    n = sum(dist.values())
    print("\nกี่วรรคในบทที่มีสัมผัสใน:")
    for k in range(5):
        print(f"  {k} วรรค: {dist[k]:>7,} บท ({100 * dist[k] / n:>5.1f}%)")
    print(f"\nบทที่ไม่มีเลย {100 * dist[0] / n:.1f}% · บทที่มี 2-3 วรรค "
          f"{100 * (dist[2] + dist[3]) / n:.1f}% ← สิ่งที่ท่านทำจริง")

    print("\nรายเรื่อง:")
    for title, (pct, bots) in sorted(per_work.items(), key=lambda x: -x[1][0]):
        print(f"  {title:<28}{pct:>6.1f}%  ({bots:,} บท)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
