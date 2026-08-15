#!/usr/bin/env python3
"""สร้างพจนานุกรมปิดจากคลังสุนทรภู่ — คำ · พยางค์ · ดัชนีสัมผัส

    python3 tools/build_lexicon.py

ผลลงที่
  data/lexicon/words.json      คำ → จำนวนครั้ง (ตัดด้วย newmm ตัวเดียวกับที่ตัวตรวจใช้)
  data/lexicon/syllables.json  พยางค์ → จำนวนครั้ง
  data/lexicon/rhymes.json     คีย์สัมผัส → พยางค์ที่ท่านใช้ เรียงตามความถี่
  data/lexicon/meta.json       ว่าสร้างจากงานไหน ตัด tier ไหนออก

**ทำไมต้องเป็นตัวตัดคำตัวเดียวกันทั้งสองฝั่ง** — `references/klon-paet.md` TH-KL-07
บันทึกไว้แล้วว่าตัวตัดคำแตกคำจริงเป็นเศษเยอะมาก (สุนทรภู่โดน 9/87 ทั้งที่ท่านไม่ได้
แต่งคำมั่ว) ถ้าฝั่งคลังใช้ตัวหนึ่งแล้วฝั่งร่างใช้อีกตัว เศษจะไม่หักล้างกัน แล้วรายงาน
จะเต็มไปด้วยคำที่ "ไม่มีในสุนทรภู่" ทั้งที่มี

⚠️ **พจนานุกรมนี้เป็นรายชื่อผู้ต้องสงสัย ไม่ใช่คำพิพากษา** คำที่ไม่อยู่ในนี้แปลว่า
"ไม่พบในคลัง" ไม่ได้แปลว่า "สุนทรภู่ไม่เคยใช้" — คลังคือสิ่งที่เหลือรอดมาถึงเรา
"""
from __future__ import annotations

import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from thai_prosody import rhyme_key, syllables_of_verse  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
CORPUS = ROOT / "data" / "corpus"
OUT = ROOT / "data" / "lexicon"

# tier ที่เข้าพจนานุกรม — ดู tools/build_corpus.py ว่าแต่ละชั้นแปลว่าอะไร
LEXICON_TIERS = {"core"}


def tokenize(text: str) -> list[str]:
    from pythainlp.tokenize import word_tokenize

    return [w for w in word_tokenize(text, keep_whitespace=False) if w.strip()]


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    registry = json.loads((CORPUS / "works.json").read_text(encoding="utf-8"))["works"]

    words: Counter[str] = Counter()
    syls: Counter[str] = Counter()
    verse_starts: Counter[str] = Counter()
    per_work: dict[str, int] = {}
    used, skipped = [], []

    for w in registry:
        if w["tier"] not in LEXICON_TIERS:
            skipped.append({"id": w["id"], "title": w["title"], "tier": w["tier"]})
            continue
        used.append({"id": w["id"], "title": w["title"], "bot": w["bot_full"]})
        n_before = len(words)
        with (CORPUS / w["file"]).open(encoding="utf-8") as fh:
            for line in fh:
                for verse in json.loads(line)["v"]:
                    words.update(tokenize(verse))
                    s = syllables_of_verse(verse)
                    syls.update(s)
                    if s:
                        verse_starts[s[0]] += 1
        per_work[w["id"]] = len(words) - n_before

    # ดัชนีสัมผัส: คีย์ → พยางค์ที่ท่านใช้จริง เรียงตามความถี่
    # นี่คือสิ่งที่ทำให้แต่งในคลังปิดเป็นไปได้ ไม่ใช่แค่ตรวจได้
    rhyme_index: dict[str, list[str]] = defaultdict(list)
    for s, _n in syls.most_common():
        for key in rhyme_key(s):
            rhyme_index["|".join(key)].append(s)

    (OUT / "words.json").write_text(
        json.dumps(dict(words.most_common()), ensure_ascii=False), encoding="utf-8"
    )
    (OUT / "syllables.json").write_text(
        json.dumps(dict(syls.most_common()), ensure_ascii=False), encoding="utf-8"
    )
    (OUT / "rhymes.json").write_text(
        json.dumps({k: v for k, v in sorted(rhyme_index.items())}, ensure_ascii=False),
        encoding="utf-8",
    )
    (OUT / "meta.json").write_text(
        json.dumps(
            {
                "tiers_included": sorted(LEXICON_TIERS),
                "works_used": used,
                "works_skipped": skipped,
                "word_types": len(words),
                "word_tokens": sum(words.values()),
                "syllable_types": len(syls),
                "syllable_tokens": sum(syls.values()),
                "rhyme_keys": len(rhyme_index),
                "tokenizer": "pythainlp.word_tokenize (newmm, default dict)",
            },
            ensure_ascii=False,
            indent=1,
        ),
        encoding="utf-8",
    )

    print(f"คำ  {len(words):,} รูป / {sum(words.values()):,} ครั้ง")
    print(f"พยางค์ {len(syls):,} รูป / {sum(syls.values()):,} ครั้ง")
    print(f"คีย์สัมผัส {len(rhyme_index):,} คีย์")
    print(f"งานที่เข้าพจนานุกรม {len(used)} เรื่อง · ไม่เข้า {len(skipped)} เรื่อง")
    print("\nคำที่ท่านใช้บ่อยที่สุด 20 คำ:")
    print("  " + " · ".join(f"{w}({n:,})" for w, n in words.most_common(20)))
    print("\nคีย์สัมผัสที่มีคำให้เลือกมากที่สุด:")
    for k, v in sorted(rhyme_index.items(), key=lambda x: -len(x[1]))[:5]:
        print(f"  {k:<14} {len(v):>4} พยางค์  {' '.join(v[:12])}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
