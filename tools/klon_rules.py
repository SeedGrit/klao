#!/usr/bin/env python3
"""กฎกลอนแปด TH-KL-01..11 ในรูปที่เครื่องตรวจได้ — ดู references/klon-paet.md

ทุกฟังก์ชันรับ `bot` = list ของ 4 วรรค คืนรายการข้อที่ละเมิด
**ห้ามเชื่อไฟล์นี้ก่อนรัน tools/calibrate.py** ตัวตรวจรุ่นแรกที่เขียนโดยไม่คาลิเบรต
ตัดสินว่าสุนทรภู่ผิด 43.7%
"""
from __future__ import annotations

from collections import Counter

from thai_prosody import (
    count_syllables,
    is_dead,
    rhyme_family,
    rhymes,
    syllables_of_verse,
    tone,
)

# ตำแหน่งที่วรรครับ/วรรคส่งรับสัมผัสยาว
#
# ของจริงคือ**คำที่ 3** — วัดกับนิราศภูเขาทอง 87 บทได้ 62/87 ตกที่ตำแหน่งนี้พอดี
# แต่ที่ยอมรับ 2-5 ไม่ใช่เพราะฉันทลักษณ์อนุญาต **เป็นการเผื่อความคลาดของตัวแบ่งพยางค์**
# อีก 10 บทตกที่คำที่ 2 และ 6 บทตกที่คำที่ 4 ซึ่งเปิดดูแล้วเป็นบทที่ตัวแบ่งพยางค์
# เลื่อนไปหนึ่งตำแหน่ง ไม่ใช่ที่ท่านวางสัมผัสผิดที่
#
# ⚠️ ถ้าวันหนึ่งเปลี่ยนตัวแบ่งพยางค์ให้แม่นขึ้น ให้บีบกลับมาเป็น [2] (และ [2,4]
# สำหรับวรรค 8 พยางค์ตามตาราง §0) แล้ววัดใหม่ — ค่านี้ผูกกับตัวแบ่ง ไม่ใช่กับภาษา
def _catch_positions(n_syllables: int) -> list[int]:
    return [1, 2, 3, 4] if n_syllables >= 8 else [1, 2, 3]


def outer_rhyme(bot: list[str]) -> list[str]:
    """TH-KL-01 สัมผัสนอกครบสามข้อ"""
    if len(bot) != 4:
        return []
    syl = [syllables_of_verse(v) for v in bot]
    if any(not s for s in syl):
        return ["วรรคว่าง"]
    bad = []
    # R1: ท้ายวรรค 1 ↔ คำที่ 3 (หรือ 5) ของวรรค 2
    if not any(
        i < len(syl[1]) and rhymes(syl[0][-1], syl[1][i])
        for i in _catch_positions(len(syl[1]))
    ):
        bad.append("R1")
    # R2: ท้ายวรรค 2 ↔ ท้ายวรรค 3
    if not rhymes(syl[1][-1], syl[2][-1]):
        bad.append("R2")
    # R3: ท้ายวรรค 3 ↔ คำที่ 3 (หรือ 5) ของวรรค 4
    if not any(
        i < len(syl[3]) and rhymes(syl[2][-1], syl[3][i])
        for i in _catch_positions(len(syl[3]))
    ):
        bad.append("R3")
    return bad


def repeated_rhyme_word(bot: list[str]) -> list[str]:
    """TH-KL-02 สัมผัสห้ามใช้คำเดิมซ้ำ — สุนทรภู่ 0/87 ข้อห้ามเด็ดขาด"""
    if len(bot) != 4:
        return []
    syl = [syllables_of_verse(v) for v in bot]
    if any(not s for s in syl):
        return []
    bad = []
    if syl[1] and syl[2] and syl[1][-1] == syl[2][-1]:
        bad.append("ท้าย 2 = ท้าย 3")
    for label, src, dst in (("R1", syl[0], syl[1]), ("R3", syl[2], syl[3])):
        if not src:
            continue
        for i in _catch_positions(len(dst)):
            if i < len(dst) and src[-1] == dst[i]:
                bad.append(f"{label}: {src[-1]} ซ้ำ")
                break
    return bad


def dead_word_at_catch(bot: list[str]) -> list[str]:
    """TH-KL-03 ท้ายวรรครับเลี่ยงคำตาย"""
    if len(bot) != 4:
        return []
    syl = syllables_of_verse(bot[1])
    return [f"ท้ายวรรครับเป็นคำตาย: {syl[-1]}"] if syl and is_dead(syl[-1]) else []


STOP = set("ที่ และ กับ ให้ ได้ จะ ไม่ ก็ ว่า มี เป็น ของ ใน อยู่ มา ไป".split())


def repeated_word(bot: list[str]) -> list[str]:
    """TH-KL-04 คำ ≥2 พยางค์ห้ามซ้ำข้ามวรรค + คำใดโผล่ ≥3 ครั้งในบทเดียว"""
    from pythainlp.tokenize import word_tokenize

    if len(bot) != 4:
        return []
    per_verse = [
        [w for w in word_tokenize(v, keep_whitespace=False) if w.strip()] for v in bot
    ]
    bad = []
    seen: dict[str, int] = {}
    for vi, words in enumerate(per_verse):
        for w in set(words):
            if len(syllables_of_verse(w)) >= 2 and w not in STOP:
                if w in seen and seen[w] != vi:
                    bad.append(f"{w} ซ้ำวรรค {seen[w] + 1} และ {vi + 1}")
                seen.setdefault(w, vi)
    counts = Counter(w for words in per_verse for w in words)
    for w, n in counts.items():
        if n >= 3 and w not in STOP and len(w) > 1:
            bad.append(f"{w} โผล่ {n} ครั้งในบทเดียว")
    return bad


# สุนทรภู่ทำจริง — ใช้เป็นเกณฑ์ ไม่ใช่ตำรา (klon-paet TH-KL-05)
TONE_RULE = {
    0: {"forbid": {"สามัญ"}},                       # สดับ ท่านลงสามัญแค่ 1.1%
    1: {"prefer": {"จัตวา", "เอก", "โท"}},          # รับ จัตวา 81.6%
    2: {"prefer": {"สามัญ", "ตรี"}},                # รอง 97.7%
    3: {"prefer": {"สามัญ", "ตรี"}},                # ส่ง 100%
}


def tone_at_end(bot: list[str]) -> list[str]:
    """TH-KL-05 เสียงวรรณยุกต์ท้ายวรรค"""
    if len(bot) != 4:
        return []
    bad = []
    for i, v in enumerate(bot):
        syl = syllables_of_verse(v)
        if not syl:
            continue
        t = tone(syl[-1])
        rule = TONE_RULE[i]
        if "forbid" in rule and t in rule["forbid"]:
            bad.append(f"วรรค {i + 1} ลงเสียง{t}")
        if "prefer" in rule and t not in rule["prefer"]:
            bad.append(f"วรรค {i + 1} ลงเสียง{t}")
    return bad


def syllable_count(bot: list[str], lo: int = 7, hi: int = 10) -> list[str]:
    """TH-KL-06 วรรคละ 7–10 พยางค์"""
    bad = []
    for i, v in enumerate(bot):
        n = count_syllables(v)
        if not lo <= n <= hi:
            bad.append(f"วรรค {i + 1} มี {n} พยางค์")
    return bad


def inner_rhyme_verses(bot: list[str]) -> list[bool]:
    """TH-KL-09 วรรคไหนมีสัมผัสใน — พยางค์ติดกันคล้องจอง แต่พยัญชนะต้นคนละตัว"""
    out = []
    for v in bot:
        syl = syllables_of_verse(v)
        found = False
        for a, b in zip(syl, syl[1:]):
            if a == b:
                continue  # คำซ้ำที่ตั้งใจ ไม่ใช่สัมผัสใน
            if _same_initial(a, b):
                continue  # `ถ้วน`/`ถวน` คือคำที่ถูกบิด ไม่ใช่สัมผัสใน (klon-paet §2)
            if rhymes(a, b):
                found = True
                break
        out.append(found)
    return out


def _same_initial(a: str, b: str) -> bool:
    from thai_prosody import CONS_SET

    fa = next((c for c in a if c in CONS_SET), "")
    fb = next((c for c in b if c in CONS_SET), "")
    return bool(fa) and fa == fb


def end_collision(bot: list[str]) -> list[str]:
    """TH-KL-10 ท้ายวรรคห้ามชนกัน ทั้งคู่ 1↔2 และคู่ 3↔4"""
    if len(bot) != 4:
        return []
    ends = []
    for v in bot:
        syl = syllables_of_verse(v)
        ends.append(syl[-1] if syl else "")
    bad = []
    for a, b, label in ((0, 1, "1↔2"), (2, 3, "3↔4")):
        if not ends[a] or not ends[b]:
            continue
        if set(rhyme_family(ends[a])) & set(rhyme_family(ends[b])):
            bad.append(f"{label}: {ends[a]} / {ends[b]}")
    return bad


def rong_ends_high(bot: list[str]) -> list[str]:
    """TH-KL-12 ท้ายวรรครองห้ามลงจัตวา — สุนทรภู่ทำ 0.87%

    แยกออกมาจาก TH-KL-05 เป็นข้อของตัวเองระดับ hard เพราะของจริงที่พลาด
    (`มีมากหลาย` จัตวา / `ไม่ทิ้งสาย` จัตวา) เครื่องฟ้องไว้แล้วในฐานะ soft
    **แล้วคนอ่านรายงานปล่อยผ่าน** — ระดับของกฎคือสิ่งที่ตัดสินว่าคนจะแก้หรือไม่แก้
    """
    if len(bot) != 4:
        return []
    syl = syllables_of_verse(bot[2])
    if syl and tone(syl[-1]) == "จัตวา":
        return [f"ท้ายวรรครองลงจัตวา: {syl[-1]}"]
    return []


def early_rhyme_in_rong(bot: list[str]) -> list[str]:
    """TH-KL-13 วรรครองห้ามดักสัมผัสก่อนคำท้าย — สุนทรภู่ทำ 10.3% (เพดานบน)

    ⚠️ ตัวนับจับพยางค์แรกของคำสองพยางค์ด้วย (`ธา` ใน `ธารา`) ซึ่งไม่ใช่การดัก
    จริง จึงข้ามคู่ที่อยู่ติดกัน แล้วยังเหลือ false positive อยู่ **ต้องเปิดดู**
    """
    if len(bot) != 4:
        return []
    syl = syllables_of_verse(bot[2])
    if len(syl) < 3:
        return []
    hits = [
        syl[i]
        for i in range(len(syl) - 2)  # ข้ามพยางค์ที่ติดกับคำท้าย
        if rhymes(syl[i], syl[-1])
    ]
    return [f"{h} ดักสัมผัสก่อน {syl[-1]}" for h in hits]


ALL = {
    "TH-KL-01": outer_rhyme,
    "TH-KL-02": repeated_rhyme_word,
    "TH-KL-03": dead_word_at_catch,
    "TH-KL-04": repeated_word,
    "TH-KL-05": tone_at_end,
    "TH-KL-06": syllable_count,
    "TH-KL-10": end_collision,
    "TH-KL-12": rong_ends_high,
    "TH-KL-13": early_rhyme_in_rong,
}
HARD = {"TH-KL-01", "TH-KL-02", "TH-KL-07", "TH-KL-08", "TH-KL-09", "TH-KL-10",
        "TH-KL-12"}


def check_bot(bot: list[str]) -> dict[str, list[str]]:
    out = {}
    for rid, fn in ALL.items():
        hits = fn(bot)
        if hits:
            out[rid] = hits
    return out
