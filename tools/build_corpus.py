#!/usr/bin/env python3
"""แปลงไฟล์ดิบใน data/raw เป็นคลังกลอนแปดที่หั่นเป็นบทละ 4 วรรคแล้ว

    python3 tools/build_corpus.py

ผลลงที่
  data/corpus/<work_id>.jsonl   หนึ่งบรรทัด = หนึ่งบท  {"c":ตอน,"i":ลำดับ,"v":[4 วรรค]}
  data/corpus/works.json        ทะเบียนงาน: ชื่อ · ชั้นการระบุผู้แต่ง · ที่มา · สถิติ

**ชั้นการระบุผู้แต่ง (tier)** เป็นของที่ต้องอ่านก่อนใช้คลังนี้ ไม่ใช่ metadata ประดับ
คลังคำที่เครื่องเอาไปบังคับ "ใช้คำจากสุนทรภู่เท่านั้น" สร้างจาก tier `core` เท่านั้น
เหตุผลของแต่ละชั้นอ้างคำอธิบายของกรรมการหอพระสมุดฯ ที่พิมพ์อยู่ในเล่มเดียวกัน
ดู data/SOURCES.md
"""
from __future__ import annotations

import json
import re
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / "data" / "raw"
OUT = ROOT / "data" / "corpus"

NIRAT_1 = "ประชุมกลอนนิราศต่างๆ-ภาคที่-๑-นิราศสุนทรภู่-๔-เรื่อง"
NIRAT_2 = "ประชุมกลอนนิราศต่างๆ-ภาคที่-๒-นิราศสุนทรภู่-๔-เรื่อง"


def th(n: int) -> str:
    return "".join("๐๑๒๓๔๕๖๗๘๙"[int(d)] for d in str(n))


def pam(first: int, last: int) -> list[str]:
    return [f"พระอภัยมณี__ตอนที่-{th(n)}" for n in range(first, last + 1)]


# tier:
#   core     — หอพระสมุดฯ ชำระว่าเป็นสำนวนของท่าน ไม่มีข้อโต้แย้งในเล่ม → เข้าพจนานุกรม
#   attrib   — บัญชี 24 เรื่องของกรมพระยาดำรงฯ นับเป็นงานของท่าน แต่ฉบับพิมพ์มีส่วนที่
#              คนอื่นแต่งต่อปนอยู่ และแบ่งด้วยเลขตอนไม่ได้ → ไม่เข้าพจนานุกรมโดยปริยาย
#   other    — ในเล่มเดียวกันบอกเองว่าไม่ใช่สำนวนท่าน → ใช้เป็นชุดเทียบ ไม่เข้าพจนานุกรม
WORKS: list[dict] = [
    # ---- นิราศ 7 เรื่องที่เป็นกลอนแปด (เรื่องที่ 8 คือโคลงนิราศสุพรรณ เป็นโคลง ไม่อยู่ในคลัง)
    dict(id="nirat-mueang-klaeng", title="นิราศเมืองแกลง", year="๒๓๕๐", tier="core",
         files=[f"{NIRAT_1}__นิราศเมืองแกลง"]),
    dict(id="nirat-phra-bat", title="นิราศพระบาท", year="๒๓๕๐", tier="core",
         files=[f"{NIRAT_1}__นิราศพระบาท"]),
    dict(id="nirat-phu-khao-thong", title="นิราศภูเขาทอง", year="๒๓๗๑", tier="core",
         files=[f"{NIRAT_1}__นิราศภูเขาทอง"],
         note="หมุดคาลิเบรตเดิมของ references/klon-paet.md"),
    dict(id="nirat-wat-chao-fa", title="นิราศวัดเจ้าฟ้า", year="ราว ๒๓๗๙", tier="core",
         files=[f"{NIRAT_1}__นิราศวัดเจ้าฟ้า"],
         note="แต่งเป็นสำนวนเณรพัดผู้เป็นบุตร แต่กรมพระยาดำรงฯ ระบุว่าท่านแต่งเอง"),
    dict(id="nirat-i-nao", title="นิราศอิเหนา", year="", tier="core",
         files=[f"{NIRAT_2}__นิราศอิเหนา"]),
    dict(id="nirat-phra-pathom", title="นิราศพระประธม", year="๒๓๘๕", tier="core",
         files=[f"{NIRAT_2}__นิราศพระประธม"]),
    dict(id="nirat-mueang-phet", title="นิราศเมืองเพ็ชร", year="๒๓๘๘-๙๒", tier="core",
         files=[f"{NIRAT_2}__นิราศเมืองเพ็ชร"]),
    dict(id="ramphan-philap", title="รำพันพิลาป", year="๒๓๘๕", tier="core",
         files=["รำพันพิลาป-ฉบับชำระใหม่__รำพันพิลาป"]),
    # ---- นิทานคำกลอน
    dict(id="kho-but", title="โคบุตร", year="ก่อน ๒๓๕๐", tier="core",
         files=[f"โคบุตรและจันทโครบ__โคบุตร__ตอนที่-{th(n)}" for n in range(1, 15)],
         note="งานเก่าที่สุดที่ยังมีฉบับ ๘ เล่มสมุดไทย"),
    dict(id="phra-aphai-mani", title="พระอภัยมณี ตอนที่ ๑–๖๔", year="ร.๒–ร.๓", tier="core",
         files=pam(1, 64),
         note="ภาคต้นที่หอพระสมุดฯ ชำระเป็นสำนวนสุนทรภู่ จบที่พระอภัยมณีออกบวช "
              "(= ๔๙ เล่มสมุดไทยที่ท่านตั้งใจให้จบ) รวม ๒๕,๐๙๘ คำกลอนตามคำนำ ๒๕๔๔"),
    dict(id="sing-kraiphop", title="สิงหไกรภพ", year="ร.๒", tier="attrib",
         files=[f"สิงหไกรภพ__ตอนที่-{th(n)}" for n in range(1, 20)],
         note="คำอธิบายในเล่ม: ท่านแต่งไว้เพียง ๑๕ เล่มสมุดไทย ฉบับพิมพ์ ๑๙ ตอน "
              "แบ่งเส้นด้วยเลขตอนไม่ได้"),
    dict(id="laksanawong", title="ลักษณวงศ์", year="", tier="attrib",
         files=[f"ลักษณวงศ์__ตอนที่-{th(n)}" for n in range(1, 21)],
         note="ประวัติสุนทรภู่: ๙ เล่มสมุดไทย เป็นสำนวนแต่งต่ออีก ๓๐ เล่ม "
              "ฉบับพิมพ์รวมทั้งสองส่วน"),
    # ---- สุภาษิต
    dict(id="sawatdiraksa", title="สวัสดิรักษา", year="๒๓๖๕-๗", tier="core",
         files=["สวัสดิรักษาคำกลอน-เพลงยาวถวายโอวาท__สวัสดิรักษา"]),
    dict(id="phleng-yao-thawai-owat", title="เพลงยาวถวายโอวาท", year="ราว ๒๓๗๓", tier="core",
         files=["สวัสดิรักษาคำกลอน-เพลงยาวถวายโอวาท__เพลงยาวถวายโอวาท"]),
    dict(id="suphasit-son-satri", title="สุภาษิตสอนสตรี", year="๒๓๘๐-๓", tier="attrib",
         files=["สวัสดิรักษาคำกลอน-เพลงยาวถวายโอวาท__สุภาษิตสอนสตรี"],
         note="กรมพระยาดำรงฯ นับเป็นสุภาษิตเรื่องที่ ๓ ของท่าน "
              "นักวิชาการรุ่นหลังโต้ว่าเป็นของ 'ภู่' คนอื่น"),
    # ---- ชุดเทียบ ไม่ใช่สำนวนท่าน
    dict(id="phra-aphai-mani-later", title="พระอภัยมณี ตอนที่ ๖๕–๑๓๒", year="", tier="other",
         files=pam(65, 132) + ["พระอภัยมณี__นิทานเรื่องพระอภัยมณี-ต่อจากคำกลอนที่พิมพ์แล้ว"],
         note="คำนำเมื่อพิมพ์ครั้งแรก: 'มีสำนวนกลอนของผู้อื่นสลับซับซ้อนปะปนกัน' "
              "ท่านแต่งเองบ้าง วานศิษย์แต่งบ้าง"),
    dict(id="chantakhrop", title="จันทโครบ", year="", tier="other",
         files=[f"โคบุตรและจันทโครบ__จันทโครบ__ตอนที่-{th(n)}" for n in range(1, 5)],
         note="กรมพระยาดำรงฯ: 'ไม่พบกลอนตอนใดที่จะเชื่อได้ว่าเป็นสำนวนกลอนสุนทรภู่"
              "สักแห่งเดียว'"),
    dict(id="nirat-phra-thaen-dong-rang", title="นิราศพระแท่นดงรัง", year="", tier="other",
         files=[f"{NIRAT_2}__นิราศพระแท่นดงรัง"],
         note="บัญชี ๒๔ เรื่องนับเป็นนิราศเรื่องที่ ๗ ของท่าน แต่ฉบับวชิรญาณขึ้นชื่อ"
              "สามเณรกลั่น — กลอนแปดร่วมสมัยที่ใช้เป็นชุดควบคุมของตัวตรวจคำนอกคลัง"),
]

PAGE_RE = re.compile(r"^\[[๐-๙0-9]+\]$")
THAI_RE = re.compile(r"[ก-๙]")


def read_verses(path: Path) -> tuple[list[str], dict]:
    """คืนรายชื่อวรรคตามลำดับ พร้อมตัวเลขว่าตัดอะไรทิ้งไปบ้าง"""
    lines = path.read_text(encoding="utf-8").split("\n")
    title, _url, body = lines[0], lines[1], lines[2:]
    body = [x.strip() for x in body]
    body = [x for x in body if x]

    # หัวเรื่องซ้ำบรรทัดแรกของเนื้อ
    if body and body[0] == title:
        body = body[1:]
    if body and re.fullmatch(r"ตอนที่ [๐-๙]+", body[0]):
        body = body[1:]

    footnotes = 0
    # เชิงอรรถอยู่ท้ายไฟล์เสมอ ปิดท้ายด้วย ↩︎ — ตัดตั้งแต่วรรคสุดท้ายที่ลงท้ายด้วย ฯ
    if "↩︎" in body:
        last_verse = max((i for i, x in enumerate(body) if x.endswith("ฯ")), default=-1)
        if last_verse >= 0:
            tail = body[last_verse + 1:]
            footnotes = tail.count("↩︎")
            body = body[: last_verse + 1]

    stats = Counter()
    verses = []
    for x in body:
        if x == "↩︎" or PAGE_RE.match(x):
            stats["marker"] += 1
            continue
        if not THAI_RE.search(x):
            stats["no_thai"] += 1
            continue
        verses.append(x)
    stats["footnotes"] = footnotes
    return verses, dict(stats)


LEAD_RE = re.compile(r"^[๏\s]+")
TAIL_RE = re.compile(r"[\s฿ฯะๆ​]*$")


def clean(verse: str) -> str:
    """เอาเครื่องหมายเปิด-ปิดคำกลอนออก เหลือแต่ตัวกลอน"""
    v = LEAD_RE.sub("", verse)
    v = re.sub(r"\s*ฯ\s*ะ?\s*$", "", v)
    return v.strip()


def _last_syllable(verse: str) -> str:
    from thai_prosody import syllables_of_verse

    syl = syllables_of_verse(verse)
    return syl[-1] if syl else ""


def find_offset(verses: list[str]) -> tuple[int, float]:
    """หาว่าวรรคแรกของไฟล์คือวรรคที่เท่าไรของบท โดยวัดจากสัมผัสนอกข้อ R2

    ⚠️ **ข้อนี้คือกับดักที่ทำให้รอบแรกอ่านว่าสุนทรภู่ผิด 100%** — นิราศขึ้นต้นด้วย
    บท 3 วรรค (ไม่มีวรรคสดับ) เกณฑ์เดิมที่ใช้คือ "ถ้าจำนวนวรรคหาร 4 เหลือ 3 ให้ตัด
    สามวรรคแรก" ซึ่งพังทันทีที่ท้ายเรื่องมีวรรคขาดมาหักล้างพอดี: นิราศเมืองแกลง
    ได้ 992 วรรค หาร 4 ลงตัว เกณฑ์จึงไม่ทำงาน แล้วทั้งเรื่องเลื่อนไป 3 วรรค

    R2 (ท้ายวรรครับสัมผัสกับท้ายวรรครอง) เป็นหมุดที่ดีที่สุดเพราะไม่ขึ้นกับตำแหน่ง
    พยางค์ในวรรค ใช้แค่คำท้าย — ออฟเซ็ตที่ถูกให้ ~93% ส่วนที่ผิดให้ 0%
    """
    ends = [_last_syllable(v) for v in verses]
    from thai_prosody import rhymes

    best, best_score = 0, -1.0
    for off in range(4):
        seq = ends[off:]
        n = len(seq) // 4
        if n < 3:
            continue
        ok = sum(1 for i in range(n) if rhymes(seq[i * 4 + 1], seq[i * 4 + 2]))
        score = ok / n
        if score > best_score:
            best, best_score = off, score
    return best, best_score


def build_work(work: dict) -> tuple[list[dict], dict]:
    bots: list[dict] = []
    agg = Counter()
    missing = []
    offsets = Counter()
    for chapter_no, stem in enumerate(work["files"], 1):
        path = RAW / f"{stem}.txt"
        if not path.exists():
            missing.append(stem)
            continue
        verses, st = read_verses(path)
        for k, v in st.items():
            agg[k] += v
        agg["verses"] += len(verses)

        cleaned = [v for v in (clean(x) for x in verses) if v]
        offset, score = find_offset(cleaned)
        offsets[offset] += 1
        agg["align_score_sum"] += score
        agg["align_chapters"] += 1
        if score < 0.5:
            agg["align_weak"] += 1

        # คะแนนความมั่นใจของการหั่นบท ติดไว้กับทุกบทของตอนนั้น
        # ตอนที่คะแนนต่ำแปลว่าหั่นบทไม่ลงตัว **สถิติฉันทลักษณ์ของตอนนั้นเชื่อไม่ได้**
        # (แต่คลังคำยังใช้ได้ เพราะคลังคำไม่สนใจว่าวรรคไหนอยู่บทไหน)
        a = round(score, 2)
        if offset:
            # วรรคหัวที่เหลือคือบทเปิดที่ไม่ครบ 4 วรรค เก็บไว้ให้คลังคำ
            # แต่มาร์ก open ไว้ ตัวคาลิเบรตจะได้ไม่เอาไปนับเป็นบทที่ผิดกฎ
            bots.append({"c": chapter_no, "i": 0, "v": cleaned[:offset], "open": True, "a": a})
            agg["opening_partial"] += 1

        rest = cleaned[offset:]
        full = len(rest) // 4
        for i in range(full):
            bots.append({"c": chapter_no, "i": len(bots), "v": rest[i * 4:i * 4 + 4], "a": a})
        leftover = len(rest) - full * 4
        if leftover:
            agg["leftover_verses"] += leftover
            bots.append({"c": chapter_no, "i": len(bots), "v": rest[full * 4:],
                         "ragged": True, "a": a})
    agg["missing_files"] = len(missing)
    agg["offsets"] = dict(offsets)
    return bots, dict(agg)


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    registry = []
    grand = Counter()
    for work in WORKS:
        bots, stats = build_work(work)
        path = OUT / f"{work['id']}.jsonl"
        with path.open("w", encoding="utf-8") as fh:
            for b in bots:
                fh.write(json.dumps(b, ensure_ascii=False, separators=(",", ":")) + "\n")
        full = [b for b in bots if len(b["v"]) == 4 and not b.get("open")]
        entry = {k: v for k, v in work.items() if k != "files"}
        entry.update(
            chapters=len(work["files"]),
            bot=len(bots),
            bot_full=len(full),
            verses=stats.get("verses", 0),
            ragged_verses=stats.get("leftover_verses", 0),
            align_offsets=stats.get("offsets", {}),
            align_score=round(
                stats.get("align_score_sum", 0) / max(stats.get("align_chapters", 1), 1), 3
            ),
            align_weak_chapters=stats.get("align_weak", 0),
            footnotes=stats.get("footnotes", 0),
            file=path.name,
        )
        registry.append(entry)
        grand["bot"] += len(bots)
        grand["bot_full"] += len(full)
        grand["verses"] += stats.get("verses", 0)
        grand["ragged"] += stats.get("leftover_verses", 0)
        if stats.get("missing_files"):
            print(f"  ⚠ {work['id']}: ขาดไฟล์ {stats['missing_files']}", file=sys.stderr)

    (OUT / "works.json").write_text(
        json.dumps(
            {"works": registry, "total": dict(grand)}, ensure_ascii=False, indent=1
        ),
        encoding="utf-8",
    )

    by_tier = Counter()
    print(f"{'งาน':<34}{'ชั้น':<8}{'บท':>8}{'บทเต็ม':>9}{'วรรค':>9}{'วรรคเศษ':>9}")
    for e in registry:
        by_tier[e["tier"]] += e["bot_full"]
        print(f"{e['title']:<34}{e['tier']:<8}{e['bot']:>8,}{e['bot_full']:>9,}"
              f"{e['verses']:>9,}{e['ragged_verses']:>9,}")
    print("-" * 78)
    print(f"{'รวม':<42}{grand['bot']:>8,}{grand['bot_full']:>9,}"
          f"{grand['verses']:>9,}{grand['ragged']:>9,}")
    for t, n in by_tier.most_common():
        print(f"  tier {t:<8} {n:>8,} บทเต็ม")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
