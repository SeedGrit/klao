#!/usr/bin/env python3
"""รันกฎทุกข้อกับคลังสุนทรภู่ แล้วรายงานว่า "ท่านละเมิดกี่ครั้ง"

นี่คือ §2 ของ references/klon-paet.md ที่เขียนเป็นโปรแกรม — ข้อที่สำคัญที่สุดในไฟล์นั้น

    python3 tools/calibrate.py                     # ทุกงาน tier core
    python3 tools/calibrate.py nirat-phu-khao-thong   # หมุดเดิม 87 บท
    python3 tools/calibrate.py --all               # ทุกงานรวม tier อื่น

อ่านผลว่า  0 = ข้อห้ามเด็ดขาด · ~5-12% = พึงเลี่ยง · 40%+ = **กฎข้อนั้นผิด ไม่ใช่กลอนผิด**
"""
from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import klon_rules as R  # noqa: E402
from thai_prosody import count_syllables  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
CORPUS = ROOT / "data" / "corpus"


MIN_ALIGN = 0.5


def load(work_id: str, min_align: float = MIN_ALIGN) -> tuple[list[list[str]], int]:
    """คืนบทเต็มที่หั่นได้อย่างมั่นใจ พร้อมจำนวนบทที่ตัดออกเพราะหั่นไม่ลงตัว

    ⚠️ บทจากตอนที่คะแนนการหั่นต่ำ **ห้ามเอามานับสถิติฉันทลักษณ์** เพราะกฎทุกข้อ
    อ่านจากตำแหน่งวรรคในบท ถ้าหั่นเลื่อนไปหนึ่งวรรค เครื่องจะฟ้องสุนทรภู่ 100%
    """
    out, dropped = [], 0
    with (CORPUS / f"{work_id}.jsonl").open(encoding="utf-8") as fh:
        for line in fh:
            b = json.loads(line)
            if len(b["v"]) != 4 or b.get("open") or b.get("ragged"):
                continue
            if b.get("a", 1.0) < min_align:
                dropped += 1
                continue
            out.append(b["v"])
    return out, dropped


def run(bots: list[list[str]]) -> dict:
    n = len(bots)
    hits = Counter()
    syl_dist = Counter()
    inner_verses = 0
    inner_bots = 0
    total_verses = 0
    for bot in bots:
        for rid, fn in R.ALL.items():
            if fn(bot):
                hits[rid] += 1
        for v in bot:
            syl_dist[count_syllables(v)] += 1
        flags = R.inner_rhyme_verses(bot)
        inner_verses += sum(flags)
        inner_bots += 1 if any(flags) else 0
        total_verses += len(bot)
    return {
        "bots": n,
        "violations": dict(hits),
        "syllables": dict(sorted(syl_dist.items())),
        "inner_verse_pct": 100 * inner_verses / total_verses if total_verses else 0,
        "inner_bot_pct": 100 * inner_bots / n if n else 0,
        "verses": total_verses,
    }


def report(name: str, res: dict) -> None:
    n = res["bots"]
    print(f"\n=== {name} · {n:,} บท / {res['verses']:,} วรรค")
    if not n:
        print("  ไม่เหลือบทที่หั่นได้อย่างมั่นใจ — ข้ามการวัดฉันทลักษณ์ของงานนี้")
        return
    print(f"{'กฎ':<12}{'ละเมิด':>9}{'%':>8}   อ่านว่า")
    for rid in sorted(R.ALL):
        c = res["violations"].get(rid, 0)
        pct = 100 * c / n if n else 0
        verdict = (
            "ข้อห้ามเด็ดขาด" if pct == 0
            else "พึงเลี่ยง" if pct < 15
            else "ปกติในกลอนไทย — กฎผิด ไม่ใช่กลอนผิด" if pct >= 40
            else "ตรวจได้ แต่อย่าเรียกว่าผิด"
        )
        print(f"{rid:<12}{c:>9,}{pct:>7.1f}%   {verdict}")
    print(f"สัมผัสใน      {res['inner_verse_pct']:>7.1f}% ของวรรค · "
          f"{res['inner_bot_pct']:.1f}% ของบท")
    dist = res["syllables"]
    tot = sum(dist.values())
    inrange = sum(v for k, v in dist.items() if 7 <= k <= 10)
    print("พยางค์ต่อวรรค " + " · ".join(f"{k}:{v:,}" for k, v in dist.items() if v)
          + f"   (นอกช่วง 7-10 = {100 * (tot - inrange) / tot:.1f}%)")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("works", nargs="*")
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--json", type=Path)
    args = ap.parse_args()

    registry = json.loads((CORPUS / "works.json").read_text(encoding="utf-8"))["works"]
    if args.works:
        chosen = [w for w in registry if w["id"] in args.works]
    elif args.all:
        chosen = registry
    else:
        chosen = [w for w in registry if w["tier"] == "core"]

    results = {}
    pooled: list[list[str]] = []
    for w in chosen:
        bots, dropped = load(w["id"])
        res = run(bots)
        res["dropped_weak_align"] = dropped
        results[w["id"]] = res
        report(f"{w['title']} [{w['tier']}]", res)
        if dropped:
            print(f"  (ตัดออก {dropped:,} บท จากตอนที่หั่นบทไม่ลงตัว)")
        if w["tier"] == "core":
            pooled.extend(bots)

    if len(chosen) > 1 and pooled:
        res = run(pooled)
        results["_pooled_core"] = res
        report("รวมทุกงาน tier core", res)

    if args.json:
        args.json.write_text(
            json.dumps(results, ensure_ascii=False, indent=1), encoding="utf-8"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
