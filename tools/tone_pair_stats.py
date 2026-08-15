#!/usr/bin/env python3
"""คู่เสียงวรรณยุกต์ของสัมผัส R2 และสัมผัสที่ดักก่อนคำท้ายวรรครอง

    python3 tools/tone_pair_stats.py > data/tone_pair_stats.txt

เขียนขึ้นหลังเจ้าของทักกลอนที่ AI ร่างสองข้อ (2026-08-15) ซึ่งทั้งคู่เป็นข้อที่
`calibrate.py` มองไม่เห็น เพราะรายงานเสียงท้ายวรรค**ทีละวรรค** ไม่ได้ดูเป็น**คู่**

1. "ไม่ใช้เสียงสูง (ตรี จัตวา) มาคล้องกันสองอัน"
2. "ท้ายวรรครับไปคล้องกับคำต้นวรรครอง ทั้งที่ต้องไปคล้องกับคำท้ายวรรครอง"

ไฟล์นี้วัดทั้งสองข้อกับคลัง แล้วผลออกมาว่าข้อ 1 ถูกสามในสี่ช่อง — ดู TH-KL-05
กับ TH-KL-12 ใน references/klon-paet.md
"""
from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from calibrate import MIN_ALIGN  # noqa: E402
from thai_prosody import rhymes, syllables_of_verse, tone  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
CORPUS = ROOT / "data" / "corpus"
HIGH = {"ตรี", "จัตวา"}


def main() -> int:
    registry = json.loads((CORPUS / "works.json").read_text(encoding="utf-8"))["works"]
    pair: Counter[tuple[str, str]] = Counter()
    rong_end: Counter[str] = Counter()
    early = n = 0

    for w in registry:
        if w["tier"] != "core":
            continue
        with (CORPUS / w["file"]).open(encoding="utf-8") as fh:
            for line in fh:
                b = json.loads(line)
                if len(b["v"]) != 4 or b.get("open") or b.get("ragged"):
                    continue
                if b.get("a", 1.0) < MIN_ALIGN:
                    continue
                syl = [syllables_of_verse(v) for v in b["v"]]
                if any(not s for s in syl):
                    continue
                n += 1
                pair[(tone(syl[1][-1]), tone(syl[2][-1]))] += 1
                rong_end[tone(syl[2][-1])] += 1
                rong = syl[2]
                if any(rhymes(rong[i], rong[-1]) for i in range(len(rong) - 1)):
                    early += 1

    print(f"บทที่วัดได้ {n:,} (tier core · ตัดตอนที่หั่นบทไม่ลงตัวออกแล้ว)")

    print("\n[1] เสียงท้ายวรรครับ → เสียงท้ายวรรครอง (คู่สัมผัส R2)")
    print(f"{'รับ':<8}{'รอง':<8}{'บท':>9}{'%':>8}")
    for (a, b_), c in pair.most_common(12):
        print(f"{a:<8}{b_:<8}{c:>9,}{100 * c / n:>7.2f}%")

    print("\nช่องที่เจ้าของบอกว่าห้าม — 'เสียงสูงคล้องกันสองอัน':")
    for combo in (("จัตวา", "จัตวา"), ("ตรี", "จัตวา"), ("ตรี", "ตรี"), ("จัตวา", "ตรี")):
        c = pair.get(combo, 0)
        verdict = ("ห้ามเด็ดขาด" if 100 * c / n < 0.3
                   else "เลี่ยงหนัก" if 100 * c / n < 1
                   else "**ท่านทำเป็นปกติ — ข้อนี้ไม่ใช่ข้อห้าม**")
        print(f"   {combo[0]:<6}+{combo[1]:<6}{c:>7,} = {100 * c / n:>5.2f}%   {verdict}")

    print("\nเสียงท้ายวรรครองล้วน ๆ (ตัวที่บังคับจริง):")
    for t, c in rong_end.most_common():
        print(f"   {t:<8}{c:>9,} = {100 * c / n:>5.2f}%")

    print(f"\n[2] วรรครองมีเสียงสัมผัสของตัวเองโผล่ก่อนคำท้าย: "
          f"{early:,} = {100 * early / n:.1f}%")
    print("    (นับพยางค์ใดก็ได้ในวรรครองที่สัมผัสกับคำท้ายวรรครอง — พยางค์แรกของ")
    print("     คำสองพยางค์อย่าง `ธา` ใน `ธารา` ก็ติดด้วย จึงเป็นเพดานบน ไม่ใช่ตัวเลขสุทธิ)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
