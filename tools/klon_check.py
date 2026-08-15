#!/usr/bin/env python3
"""ตรวจกลอนแปดที่ร่างขึ้น: ฉันทลักษณ์ + **คำที่ไม่มีในคลังสุนทรภู่**

    python3 tools/klon_check.py ร่าง.txt          # หนึ่งวรรคต่อบรรทัด บทละ 4 บรรทัด
    python3 tools/klon_check.py -                 # อ่านจาก stdin
    python3 tools/klon_check.py --rhyme ใจ        # คำที่ท่านใช้แล้วสัมผัสกับ `ใจ`
    python3 tools/klon_check.py --word ปรารถนา    # ท่านใช้คำนี้กี่ครั้ง
    python3 tools/klon_check.py ร่าง.txt --strict # คำนอกคลังนับเป็น fail

⚠️ **"ไม่พบในคลัง" ไม่เท่ากับ "สุนทรภู่ไม่เคยใช้"** คลังคือกลอนแปดที่เหลือรอดมาถึงเรา
และตัวตัดคำก็แตกคำจริงเป็นเศษด้วย รายงานนี้จึงเป็นรายชื่อผู้ต้องสงสัย ให้คนตัดสิน

⚠️ **ตัวตรวจนี้บอกไม่ได้ว่ากลอนอ่านรู้เรื่องไหม** ชั้นนั้นอยู่ใน klon-paet.md §5
ต้องมีคนอ่านออกเสียงเทียบต้นฉบับเสมอ
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import klon_rules as R  # noqa: E402
from thai_prosody import count_syllables, rhyme_key, syllables_of_verse  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
LEX = ROOT / "data" / "lexicon"

# เกณฑ์จากคลังสุนทรภู่ — ตัวเลขจริงอยู่ใน data/calibration.txt
INNER_RHYME_MIN = 0.60


def load_lexicon() -> tuple[dict, dict, dict, dict]:
    words = json.loads((LEX / "words.json").read_text(encoding="utf-8"))
    syls = json.loads((LEX / "syllables.json").read_text(encoding="utf-8"))
    rhymes = json.loads((LEX / "rhymes.json").read_text(encoding="utf-8"))
    meta = json.loads((LEX / "meta.json").read_text(encoding="utf-8"))
    return words, syls, rhymes, meta


def read_bots(lines: list[str]) -> list[list[str]]:
    verses = [x.strip() for x in lines if x.strip()]
    return [verses[i:i + 4] for i in range(0, len(verses), 4)]


def out_of_corpus(verse: str, words: dict, syls: dict) -> list[tuple[str, str]]:
    """คืน (คำ, ระดับ) — `คำ` คือไม่พบรูปคำ · `พยางค์` คือแม้พยางค์ก็ไม่พบ"""
    from pythainlp.tokenize import word_tokenize

    bad = []
    for w in word_tokenize(verse, keep_whitespace=False):
        if not w.strip() or w in words:
            continue
        missing_syls = [s for s in syllables_of_verse(w) if s not in syls]
        bad.append((w, "พยางค์" if missing_syls else "คำ"))
    return bad


def suggest(target: str, rhymes: dict, syls: dict, words: dict,
            limit: int = 12) -> list[str]:
    """พยางค์ในคลังที่สัมผัสกับ target เรียงตามความถี่

    ⚠️ **ต้องกรองเศษพยางค์ออก** ดัชนีสัมผัสสร้างจากผลของตัวแบ่งพยางค์ ซึ่งมีเศษ
    อย่าง `ลี่ย` `ดีย` ปนอยู่ เอาไปวางในกลอนไม่ได้ เกณฑ์ที่ใช้คือ **พยางค์นั้นเคยยืน
    เป็นคำเดี่ยวในคลังไหม** ถ้าไม่เคยก็เป็นชิ้นส่วนของคำอื่น ไม่ใช่คำ
    """
    out: list[str] = []
    for key in rhyme_key(target):
        for s in rhymes.get("|".join(key), []):
            if s != target and s not in out and s in words:
                out.append(s)
    return sorted(out, key=lambda s: -syls.get(s, 0))[:limit]


def check(bots: list[list[str]], words: dict, syls: dict, rhymes: dict,
          strict: bool) -> int:
    problems = 0
    total_verses = inner_ok = 0
    for n, bot in enumerate(bots, 1):
        print(f"\n{'─' * 74}\nบทที่ {n}")
        flags = R.inner_rhyme_verses(bot)
        for i, v in enumerate(bot):
            mark = "✓" if i < len(flags) and flags[i] else " "
            print(f"  {i + 1}. {v}   [{count_syllables(v)} พยางค์] สัมผัสใน {mark}")
        total_verses += len(bot)
        inner_ok += sum(flags)

        oov = [(i, w, lv) for i, v in enumerate(bot)
               for w, lv in out_of_corpus(v, words, syls)]
        if oov:
            problems += 1 if strict else 0
            print("\n  ⚠ คำที่ไม่พบในคลังสุนทรภู่")
            for i, w, level in oov:
                where = f"วรรค {i + 1}"
                hint = "" if level == "คำ" else "  ← แม้พยางค์ก็ไม่มีในคลัง"
                print(f"      {where}: {w}  (ไม่พบระดับ{level}){hint}")

        if len(bot) == 4:
            hits = R.check_bot(bot)
            if hits:
                for rid, msgs in sorted(hits.items()):
                    tag = "hard" if rid in R.HARD else "soft"
                    if tag == "hard":
                        problems += 1
                    print(f"  ✗ {rid} [{tag}] " + " · ".join(msgs))
                    if rid == "TH-KL-01":
                        syl = [syllables_of_verse(v) for v in bot]
                        for label, src in (("R1", syl[0]), ("R3", syl[2])):
                            if label in msgs and src:
                                s = suggest(src[-1], rhymes, syls, words)
                                if s:
                                    print(f"        คำที่ท่านใช้แล้วสัมผัสกับ "
                                          f"{src[-1]}: {' '.join(s)}")
            else:
                print("  ✓ ฉันทลักษณ์ผ่านทุกข้อที่เครื่องตรวจได้")
        else:
            print(f"  ⚠ บทนี้มี {len(bot)} วรรค ไม่ใช่ 4")
            problems += 1

    pct = 100 * inner_ok / total_verses if total_verses else 0
    bots_with = sum(1 for b in bots if any(R.inner_rhyme_verses(b)))
    print(f"\n{'─' * 74}")
    print(f"สัมผัสใน {pct:.1f}% ของวรรค ({inner_ok}/{total_verses}) · "
          f"{bots_with}/{len(bots)} บทมีอย่างน้อยหนึ่งวรรค")
    if pct < INNER_RHYME_MIN * 100:
        print(f"  ✗ TH-KL-09 [hard] ต่ำกว่าเกณฑ์ {INNER_RHYME_MIN:.0%} — "
              f"ถูกกฎแข็งครบแล้วอ่านแล้วแห้งได้ ต้องเติมสัมผัสใน")
        problems += 1
    if bots_with < len(bots):
        print("  ✗ TH-KL-09 [hard] มีบทที่ไม่เหลือสัมผัสในเลย")
        problems += 1
    return problems


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("file", nargs="?", help="ไฟล์กลอน หนึ่งวรรคต่อบรรทัด (`-` = stdin)")
    ap.add_argument("--rhyme", help="แสดงพยางค์ในคลังที่สัมผัสกับคำนี้")
    ap.add_argument("--word", help="ค้นว่าท่านใช้คำนี้กี่ครั้ง")
    ap.add_argument("--strict", action="store_true", help="คำนอกคลังนับเป็นข้อผิด")
    args = ap.parse_args()

    words, syls, rhymes, meta = load_lexicon()

    if args.rhyme:
        found = suggest(args.rhyme, rhymes, syls, words, limit=60)
        print(f"คีย์สัมผัสของ {args.rhyme}: {rhyme_key(args.rhyme)}")
        print(f"พยางค์ในคลัง {len(found)} ตัว (เรียงตามที่ท่านใช้บ่อย):")
        print("  " + " · ".join(f"{s}({syls.get(s, 0)})" for s in found))
        return 0

    if args.word:
        n = words.get(args.word, 0)
        print(f"{args.word}: {'พบ ' + format(n, ',') + ' ครั้ง' if n else 'ไม่พบในคลัง'}")
        if not n:
            missing = [s for s in syllables_of_verse(args.word) if s not in syls]
            print("  พยางค์ที่ไม่มีในคลัง: " + (" ".join(missing) if missing
                                                 else "ไม่มี — ทุกพยางค์ท่านใช้หมด"))
        return 0

    if not args.file:
        ap.error("ต้องระบุไฟล์ หรือใช้ --rhyme / --word")
    text = sys.stdin.read() if args.file == "-" else Path(args.file).read_text(
        encoding="utf-8"
    )
    bots = read_bots(text.split("\n"))
    if not bots:
        print("ไม่มีวรรคให้ตรวจ")
        return 1
    print(f"คลัง: {meta['word_types']:,} รูปคำ · {meta['syllable_types']:,} พยางค์ "
          f"จาก {len(meta['works_used'])} เรื่อง (tier {'+'.join(meta['tiers_included'])})")
    problems = check(bots, words, syls, rhymes, args.strict)
    print(f"\nสรุป: {'ผ่าน' if not problems else f'ติด {problems} จุด'}")
    return 1 if problems else 0


if __name__ == "__main__":
    raise SystemExit(main())
