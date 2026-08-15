#!/usr/bin/env python3
"""พยางค์ · คีย์สัมผัส · เสียงวรรณยุกต์ · คำเป็นคำตาย — สำหรับกลอนแปด

ไฟล์นี้เขียนตาม `references/klon-paet.md` §3 ทุกข้อ ซึ่งเป็นรายการบั๊กจริงที่เจอ
ตอนคาลิเบรตรอบก่อน ไม่ใช่ตำราไวยากรณ์ ที่สำคัญที่สุดสองข้อ:

1. **ตัวแบ่งพยางค์ต้องตัดทีละคำ ไม่ใช่ทั้งวรรครวด** — ssg ทั้งวรรคลาก ค จาก
   `อุปสรรค` ไปติด `รุม` แล้วตำแหน่งพยางค์เลื่อนทั้งวรรค
2. **รับว่าสัมผัสถ้าทางใดทางหนึ่งบอกว่าสัมผัส** — รูปเขียนกับ pronunciate ต่างก็ผิด
   คนละแบบ (`ไหล` = ไล แต่ `โหม` = โฮม เขียนเหมือนกันทุกประการ)

ตัวเลขที่ยืนยันว่าไฟล์นี้ใช้ได้อยู่ใน tools/calibrate.py — ห้ามแก้ไฟล์นี้แล้วไม่รันซ้ำ
"""
from __future__ import annotations

import functools
import re

CONS = "กขฃคฅฆงจฉชซฌญฎฏฐฑฒณดตถทธนบปผฝพฟภมยรลวศษสหฬอฮ"
CONS_SET = set(CONS)
TONE_MARKS = "่้๊๋"  # ่ ้ ๊ ๋
THANTHAKHAT = "์"  # ์ การันต์
PHINTHU = "ฺ"  # ฺ  pronunciate ใช้มาร์กอักษรนำ
MAI_TAI_KHU = "็"  # ็

# อักษรนำที่ ห / อ ไม่ออกเสียง — สองตัวนี้เป็นพยางค์เดียวเสมอ ห้ามให้ pronunciate
# มาแทน (มันอ่าน `หยิบ` เป็น หิ-บะ)
LEADING_H = set("งญณนมยรลวฬ")
_LEAD_RE = re.compile(rf"^ห[{''.join(LEADING_H)}]|^อย")

# ควบกล้ำแท้ + ไม่แท้ — ตัวที่ตามหลังพยัญชนะต้นแล้วยังเป็นพยัญชนะต้นอยู่
CLUSTER_SECOND = set("รลว")
CLUSTERS = {
    a + b
    for a in "กขคตปผพบฟดจซศสหมน"
    for b in "รลว"
}


def _strip_tones(s: str) -> str:
    return "".join(c for c in s if c not in TONE_MARKS)


# ---------------------------------------------------------------- มาตราตัวสะกด
# ตัวสะกดต่างรูปแต่เสียงเดียวกันต้องยุบเป็นมาตราเดียว ไม่งั้น `เข็ญ` ไม่รับ `เว้น`
CODA_CLASS = {
    **{c: "n" for c in "นณญรลฬ"},      # แม่กน
    **{c: "m" for c in "ม"},            # แม่กม
    **{c: "ng" for c in "ง"},           # แม่กง
    **{c: "k" for c in "กขคฆ"},         # แม่กก
    **{c: "t" for c in "ดตถทธฎฏฐฑฒจชซศษส"},  # แม่กด
    **{c: "p" for c in "บปพฟภ"},        # แม่กบ
    **{c: "j" for c in "ย"},            # แม่เกย
    **{c: "w" for c in "ว"},            # แม่เกอว
}
DEAD_CODA = {"k", "t", "p"}

# ---------------------------------------------------------------- รูปสระ
# เรียงจากยาวไปสั้น เพราะ matcher ลองตามลำดับ ตัวที่กินอักษรมากกว่าต้องมาก่อน
# แต่ละแถว: (regex ที่มี group 'f' เป็นตัวสะกด, คุณภาพสระ, สั้น/ยาว)
_V = [
    # สระประสม
    (r"^เ{C}ีย(?P<f>{K})?ะ$", "ia", "s"),
    (r"^เ{C}ีย(?P<f>{K})?$", "ia", "l"),
    (r"^เ{C}ือ(?P<f>{K})?ะ$", "uua", "s"),
    (r"^เ{C}ือ(?P<f>{K})?$", "uua", "l"),
    (r"^{C}ัวะ$", "ua", "s"),
    (r"^{C}ัว(?P<f>{K})?$", "ua", "l"),
    (r"^{C}ว(?P<f>{K})$", "ua", "l"),           # สระอัวลดรูป: ถ้วน ควร ผวน
    # สระเดี่ยวที่รูปพิเศษ
    (r"^เ{C}าะ$", "ɔ", "s"),
    (r"^{C}็อ(?P<f>{K})$", "ɔ", "s"),
    (r"^เ{C}็อ(?P<f>{K})$", "ɤ", "s"),
    (r"^เ{C}อะ$", "ɤ", "s"),
    (r"^เ{C}ิ(?P<f>{K})$", "ɤ", "l"),
    (r"^เ{C}อ(?P<f>{K})?$", "ɤ", "l"),
    (r"^เ{C}ะ$", "e", "s"),
    (r"^เ{C}็(?P<f>{K})$", "e", "s"),
    (r"^เ{C}(?P<f>{K})?$", "e", "l"),
    (r"^แ{C}ะ$", "ɛ", "s"),
    (r"^แ{C}็(?P<f>{K})$", "ɛ", "s"),
    (r"^แ{C}(?P<f>{K})?$", "ɛ", "l"),
    (r"^โ{C}ะ$", "o", "s"),
    (r"^โ{C}(?P<f>{K})?$", "o", "l"),
    # ไ ใ -ัย ไ-ย ทั้งหมดคือสระอาสั้น + ย จึงต้องชนกับ -าย ได้
    (r"^ไ{C}ย$", "a", "s", "j"),
    (r"^[ไใ]{C}$", "a", "s", "j"),
    (r"^{C}ัย$", "a", "s", "j"),
    (r"^เ{C}า$", "a", "s", "w"),          # เ-า = อาสั้น + ว จึงชนกับ -าว
    (r"^{C}ำ$", "a", "s", "m"),           # -ำ = อัม
    (r"^{C}รร(?P<f>{K})$", "a", "s"),     # -รรF = อั + F
    (r"^{C}รร$", "a", "s", "n"),          # -รร = อัน
    (r"^{C}ะ$", "a", "s"),
    (r"^{C}ั(?P<f>{K})$", "a", "s"),
    (r"^{C}า(?P<f>{K})?$", "a", "l"),
    (r"^{C}ิ(?P<f>{K})?$", "i", "s"),
    (r"^{C}ี(?P<f>{K})?$", "i", "l"),
    (r"^{C}ึ(?P<f>{K})?$", "ɯ", "s"),
    (r"^{C}ื(?P<f>{K})?อ?$", "ɯ", "l"),
    (r"^{C}ุ(?P<f>{K})?$", "u", "s"),
    (r"^{C}ู(?P<f>{K})?$", "u", "l"),
    (r"^{C}อ(?P<f>{K})?$", "ɔ", "l"),
    (r"^{C}ฤ$", "ɯ", "s"),
    # สะกดด้วย ร ไม่มีรูปสระ = สระออ (`พร` `จร` `เกสร` `อัมพร`) ไม่ใช่สระโอะลดรูป
    (r"^{C}ร$", "ɔ", "l", "n"),
    # ไม่มีรูปสระเลย = สระโอะลดรูป (ชล หน คง) — ต้องอยู่ท้ายสุด
    (r"^{C}(?P<f>{K})$", "o", "s"),
    (r"^{C}$", "a", "s"),                 # พยางค์เปล่า เช่น ก ณ
]

# พยัญชนะต้น: อักษรนำ ห/อ · ควบกล้ำ C+ร/ล/ว · หรือตัวเดียว
# ถ้าปล่อยให้เป็น [CONS][CONS]? เฉย ๆ `เว้น` จะถูกอ่านเป็น เ + (วน) แล้วกลายเป็น
# สระเอไม่มีตัวสะกด — ผลคือ `เข็ญ` ไม่รับ `เว้น` ซึ่งสุนทรภู่รับเป็นคู่สัมผัส
# ต้องเรียงอักษรนำไว้หน้าสุด ไม่งั้น `หมาย` จะ parse ไม่ผ่านแล้วโดนผ่าเป็น ห + มาย
# ⚠️ ตัวที่นำควบกล้ำได้ต้องไม่ใช่ ร ล ว เอง ไม่งั้น `แล้ว` จะถูกอ่านเป็น แ + (ลว)
# แล้วกลายเป็นสระแอไม่มีตัวสะกด — ผลคือไม่รับสัมผัสกับ `แคล้ว` ซึ่งเป็นคู่ของท่าน
_CLUSTER_HEAD = "".join(c for c in CONS if c not in "รลวฬญ")
# อักษรนำต้องมีอะไรตามหลัง ไม่งั้น `เอ๋ย` จะถูกอ่านเป็น เ + (อย) แล้วกลายเป็น
# สระเอไม่มีตัวสะกด — ผลคือไม่รับสัมผัสกับ `เคย` ซึ่งเป็นคู่ของท่าน
_C_PAT = (
    rf"(?P<c>ห[{''.join(LEADING_H)}](?=.)|อย(?=.)"
    rf"|[{_CLUSTER_HEAD}][รลว]|[{CONS}])"
)
# ตัวสะกดจับได้ถึงสองอักษร แล้วไปตรวจความถูกต้องใน _coda_class
_K_PAT = rf"[{CONS}][{CONS}]?"


@functools.lru_cache(maxsize=None)
def _compiled() -> list[tuple[re.Pattern, str, str, str | None]]:
    out = []
    for row in _V:
        pat, quality, length = row[0], row[1], row[2]
        forced = row[3] if len(row) > 3 else None
        out.append(
            (re.compile(pat.replace("{C}", _C_PAT).replace("{K}", _K_PAT)),
             quality, length, forced)
        )
    return out


@functools.lru_cache(maxsize=100_000)
def rhyme_key(syllable: str) -> tuple[str, ...]:
    """คืนคีย์สัมผัสของหนึ่งพยางค์ — อาจได้หลายคีย์เมื่อรูปเขียนกำกวม

    กำกวมจริงที่ต้องคืนสองคีย์: `ไหล` (=ไล อักษรนำ) กับ `โหม` (=โฮม ห เป็นพยัญชนะต้น)
    เขียนเหมือนกันทุกประการ แยกจากรูปไม่ได้ ถือว่าสัมผัสถ้าตรงคีย์ใดคีย์หนึ่ง
    """
    s = _normalise(syllable)
    if not s:
        return ()
    forms = [s]
    # สระลดรูปในคำบาลี: `ชาติ` `ญาติ` `นิบัติ` ลงท้าย /-ด/ รูปสระท้ายไม่ออกเสียง
    if s[-1] in "ิุ" and len(s) > 2:
        forms.append(s[:-1])
    # ไม้ไต่คู้ต้องคาไว้ตอน parse (มันบอกว่าตัวถัดไปเป็นตัวสะกด ไม่ใช่อักษรนำ)
    # **แต่ตอนเทียบสัมผัสต้องไม่นับ** — สุนทรภู่รับ `เข็ญ` กับ `เว้น` เป็นคู่สัมผัส
    if MAI_TAI_KHU in s:
        forms.append(s.replace(MAI_TAI_KHU, ""))
    # ถ้าขึ้นต้นด้วยอักษรนำ ห/อ ลองอ่านอีกแบบโดยตัดตัวนำทิ้ง
    if _LEAD_RE.match(s) and len(s) > 1:
        forms.append(s[0] + s[2:])   # อ่านแบบ ห เป็นพยัญชนะต้น (`โหม` = โฮม)
        forms.append(s[1:])          # อ่านแบบ ห ไม่ออกเสียง (`ไหล` = ไล)
    keys = {_parse(f) for f in forms}
    return tuple(sorted(k for k in keys if k))


def rhyme_family(syllable: str) -> tuple[tuple[str, str], ...]:
    """คีย์แบบยุบความสั้น-ยาวของสระตัวเดียวกัน ใช้กับ TH-KL-10 เท่านั้น

    ⚠️ ห้ามเอาไปใช้ตัดสินสัมผัสนอก — เกณฑ์นี้กว้างกว่าและตั้งใจให้กว้าง เพราะข้อ 10
    ถามว่า "ท้ายสองวรรคฟังแล้วซ้ำกันไหม" ไม่ได้ถามว่า "สัมผัสกันไหม"
    """
    return tuple(sorted({(q, coda) for q, _length, coda in rhyme_key(syllable)}))


def _normalise(s: str) -> str:
    s = s.strip()
    # ตัดพยัญชนะที่การันต์ฆ่า พร้อมรูปสระที่เกาะอยู่กับมัน
    # (`ศักดิ์` ต้องเหลือ `ศัก` ถ้าตัดแค่ `ด์` จะเหลือ `ศักิ` ซึ่ง parse ไม่ผ่าน)
    s = re.sub(rf"[{CONS}][ิุ]?[{THANTHAKHAT}]", "", s)
    s = s.replace(PHINTHU, "")
    s = _strip_tones(s)
    # ไม้ไต่คู้เป็นหลักฐานว่าตัวถัดไปเป็นตัวสะกด ต้องเก็บไว้ตอน parse
    # แต่ `เข็ญ` ต้องรับกับ `เว้น` ได้ จึงไม่ต้องเก็บเข้าไปในคีย์ (ดู _parse)
    return s


def _coda_class(raw: str) -> str | None:
    """มาตราตัวสะกดของตัวสะกด 1-2 อักษร คืน None ถ้าไม่ใช่ตัวสะกดที่เป็นไปได้"""
    if not raw:
        return ""
    if len(raw) == 1:
        return CODA_CLASS.get(raw)
    a, b = raw[0], raw[1]
    # ร นำหน้าแล้วไม่ออกเสียง: `สารท` = /สาด/ · `สามารถ` = /สามาด/
    if a == "ร":
        return CODA_CLASS.get(b)
    # ร ตามหลังแล้วไม่ออกเสียง: `มิตร` = /มิด/ · `จักร` = /จัก/
    if b == "ร":
        return CODA_CLASS.get(a)
    # ตัวสะกดคู่แบบบาลี ต้องอยู่มาตราเดียวกันเท่านั้น (`สุทธ` = /สุด/)
    # ถ้าปล่อยให้คู่ไหนก็ได้ `กุศล` จะกลายเป็นพยางค์เดียว ทั้งที่เป็น กุ-สน
    ca, cb = CODA_CLASS.get(a), CODA_CLASS.get(b)
    return ca if ca and ca == cb else None


def _parse(s: str) -> tuple[str, ...] | None:
    if not s:
        return None
    for pat, quality, length, forced in _compiled():
        m = pat.match(s)
        if not m:
            continue
        raw_f = m.groupdict().get("f") or ""
        coda = forced or _coda_class(raw_f)
        if coda is None:
            continue
        # ควบกล้ำท้ายพยางค์ไม่ใช่ตัวสะกด — `ไกล` ล เป็นควบกล้ำ ไม่งั้นไม่รับกับ `ไพ`
        return (quality, length, coda)
    return None


def rhymes(a: str, b: str) -> bool:
    """สองพยางค์สัมผัสกันไหม — ตรงคีย์ใดคีย์หนึ่งก็ถือว่าใช่"""
    ka, kb = rhyme_key(a), rhyme_key(b)
    return bool(ka) and bool(kb) and bool(set(ka) & set(kb))


def is_dead(syllable: str) -> bool:
    """คำตาย = สะกดแม่ กก/กด/กบ หรือสระเสียงสั้นไม่มีตัวสะกด (TH-KL-03)"""
    for key in rhyme_key(syllable):
        _quality, length, coda = key
        if coda in DEAD_CODA:
            return True
        if not coda and length == "s":
            return True
        return False
    return False


# ---------------------------------------------------------------- วรรณยุกต์
HIGH = set("ขฃฉฐถผฝศษสห")
MID = set("กจฎฏดตบปอ")
# ที่เหลือเป็นอักษรต่ำ


def tone(syllable: str) -> str:
    """เสียงวรรณยุกต์: สามัญ เอก โท ตรี จัตวา  (TH-KL-05)"""
    raw = syllable.strip()
    s = _normalise(raw)
    if not s:
        return "?"
    m = re.match(rf"^[เแโใไ]?(?P<c>[{CONS}][{CONS}]?)", s)
    if not m:
        return "?"
    c = m.group("c")
    lead = c[0]
    # อักษรนำ ห/อ ทำให้ตัวตามกลายเป็นเสียงสูง/กลาง
    if _LEAD_RE.match(s):
        cls = "high" if lead == "ห" else "mid"
    elif lead in HIGH:
        cls = "high"
    elif lead in MID:
        cls = "mid"
    else:
        cls = "low"
        if len(c) == 2 and c[0] in HIGH:
            cls = "high"

    mark = next((ch for ch in raw if ch in TONE_MARKS), "")
    key = rhyme_key(raw)
    dead = is_dead(raw)
    long_v = bool(key) and key[0][1] == "l"

    if mark == "่":  # ่
        return {"low": "โท", "mid": "เอก", "high": "เอก"}[cls]
    if mark == "้":  # ้
        return {"low": "ตรี", "mid": "โท", "high": "โท"}[cls]
    if mark == "๊":  # ๊
        return "ตรี"
    if mark == "๋":  # ๋
        return "จัตวา"
    if not dead:
        return {"low": "สามัญ", "mid": "สามัญ", "high": "จัตวา"}[cls]
    if cls == "low":
        return "ตรี" if not long_v else "โท"
    return "เอก"


# ---------------------------------------------------------------- แบ่งพยางค์
_DICT_CACHE: set[str] | None = None


def _thai_dict() -> set[str]:
    global _DICT_CACHE
    if _DICT_CACHE is None:
        from pythainlp.corpus import thai_words

        _DICT_CACHE = set(thai_words())
    return _DICT_CACHE


@functools.lru_cache(maxsize=200_000)
def syllables_of_word(word: str) -> tuple[str, ...]:
    """แบ่งพยางค์ของ **หนึ่งคำ** ห้ามส่งทั้งวรรคเข้ามา (ดูหัวไฟล์)"""
    from pythainlp.tokenize import subword_tokenize

    w = word.strip()
    if not w or not re.search(r"[ก-๙]", w):
        return ()
    # อักษรนำเป็นพยางค์เดียวเสมอ ห้ามให้เสียงอ่านมาแทน (`หยิบ` → หิ-บะ ผิด)
    if _LEAD_RE.match(w) and len(w) <= 5:
        parts = tuple(x for x in subword_tokenize(w, engine="ssg") if x.strip())
        if len(parts) > 1 and w in _thai_dict():
            return (w,)
    if w in _thai_dict():
        # คำที่อยู่ในพจนานุกรม แปลว่า pronunciate มีรายการจริงให้อ่าน ไม่ได้เดา
        try:
            from pythainlp.transliterate import pronunciate

            said = pronunciate(w)
            if said and "-" in said:
                n = len([p for p in said.split("-") if p.strip()])
                parts = tuple(x for x in subword_tokenize(w, engine="ssg") if x.strip())
                if len(parts) == n:
                    return parts
                if n > len(parts):
                    return _resplit(w, n) or parts
                return parts
        except Exception:  # noqa: BLE001 — pronunciate ล้มได้ ใช้ ssg แทน
            pass
    return tuple(x for x in subword_tokenize(w, engine="ssg") if x.strip())


def _resplit(word: str, n: int) -> tuple[str, ...] | None:
    """ssg แบ่งได้น้อยกว่าเสียงอ่าน — ผ่าก้อนที่ยาวจนกว่าจะครบ n พยางค์

    ของจริง: `อุปสรรค` ssg คืน ['อุป','สรรค'] แต่อ่าน อุ-ปะ-สัก คือ 3
    ถ้าไม่ผ่า ตำแหน่งพยางค์ที่ 3 (จุดสัมผัสนอก) จะเลื่อนไปทั้งวรรค
    """
    from pythainlp.tokenize import subword_tokenize

    parts = [x for x in subword_tokenize(word, engine="ssg") if x.strip()]
    guard = 0
    while len(parts) < n and guard < 8:
        guard += 1
        # ผ่าก้อนที่ยาวที่สุดที่ยังผ่าได้ ตรงหลังพยัญชนะ+สระอะลดรูป (2 อักษร)
        idx = max(
            (i for i, p in enumerate(parts) if len(p) >= 3 and p[1] not in "รลว"),
            key=lambda i: len(parts[i]),
            default=None,
        )
        if idx is None:
            return None
        p = parts[idx]
        parts[idx: idx + 1] = [p[:2], p[2:]]
    return tuple(parts) if len(parts) == n else None


VOWEL_CHARS = set("ะัาำิีึืุูเแโใไ็ๅฤฦ")


def _has_vowel(piece: str) -> bool:
    return any(c in VOWEL_CHARS for c in piece)


def _readable(piece: str) -> bool:
    """อ่านเป็นพยางค์เดียวออกไหม — ใช้ rhyme_key เพราะมีชั้น fallback ครบ
    (`ธาตุ` `ญาติ` `ศักดิ์` parse ตรง ๆ ไม่ผ่าน แต่เป็นพยางค์เดียวทั้งคู่)"""
    return bool(rhyme_key(piece))


def _merge_orphans(pieces: list[str]) -> list[str]:
    """รวมเศษที่ไม่มีรูปสระของตัวเองกลับเข้าพยางค์ก่อนหน้า

    ตัวแบ่งพยางค์ทุกตัวที่ลองมาเรียนจากภาษาไทยปัจจุบัน แต่คลังนี้เป็นอักขรวิธี
    ฉบับพิมพ์ ๒๔๖๖-๒๔๘๑ — `อาไศรย` ถูกตัดเป็น `อา`+`ไศ`+`รย` · `อาไลย` เป็น
    `อาไล`+`ย` เศษท้ายไม่มีสระเป็นของตัวเองและต่อกลับแล้วอ่านออกเป็นพยางค์เดียว
    ซึ่งเป็นลายเซ็นของการตัดผิด ไม่ใช่พยางค์จริง

    เกณฑ์ "ไม่มีรูปสระ" ทำให้ `กุ`+`ศล` ไม่ถูกรวม เพราะ `ศล` เป็นพยางค์จริง
    (สระโอะลดรูป) และ `กุศล` ต่อกันแล้ว parse ไม่ผ่าน
    """
    out: list[str] = []
    for p in pieces:
        # อักษรนำที่ถูกตัดหลุดมาข้างหน้า: `ห`+`มาย` · `อ`+`ย่าง` ต้องต่อกลับเสมอ
        # (ห + งญณนมยรลวฬ และ อ + ย เป็นพยางค์เดียวตายตัว — klon-paet §3)
        if out and out[-1] in ("ห", "อ") and p:
            head = next((c for c in p if c in CONS_SET), "")
            if (out[-1] == "ห" and head in LEADING_H) or (out[-1] == "อ" and head == "ย"):
                out[-1] += p
                continue
        if out and len(p) <= 2 and not _has_vowel(p) and _readable(out[-1] + p):
            # เศษท้ายที่ไม่มีรูปสระของตัวเอง (`อาไศ`+`รย`) ต่อกลับแล้วอ่านออก
            # เลือกทางที่ได้พยางค์น้อยกว่า เพราะกลอนแปดวรรคละ 7-10 พยางค์
            out[-1] += p
        else:
            out.append(p)
    return out


def _split_unparsable(pieces: list[str]) -> list[str]:
    """ผ่าก้อนที่อ่านเป็นพยางค์เดียวไม่ออก ให้เป็นสองพยางค์ที่อ่านออกทั้งคู่

    ssg กลืน `ผกา` `วสา` `ถนา` `สกล` `เกสร` ไว้เป็นก้อนเดียว ทั้งที่เป็นสองพยางค์
    (สระอะลดรูปที่ตัวหน้า) ทุกตัวคือคู่สัมผัสที่ท่านใช้จริง ถ้าไม่ผ่า สัมผัสนอกจะหลุด
    """
    out: list[str] = []
    for p in pieces:
        if _readable(p) or len(p) < 3:
            out.append(p)
            continue
        best = None
        for cut in range(1, len(p)):
            a, b = p[:cut], p[cut:]
            if _readable(a) and _readable(b):
                # สระอะลดรูปกินอักษรเดียว ตัวเลือกที่หัวสั้นที่สุดจึงถูกเกือบเสมอ
                best = (a, b)
                break
        if best is None and len(p) > 2 and p[0] in "เแโใไ" and p[1] in CONS_SET:
            # `เสด็จ` = สะ-เด็จ — พยางค์แรกเป็นพยัญชนะเปล่า ส่วนสระหน้าเป็นของ
            # พยางค์หลัง ผ่าตรง ๆ ไม่ได้เพราะรูปสระเขียนนำหน้าพยัญชนะทั้งสองตัว
            a, b = p[1], p[0] + p[2:]
            if _readable(b):
                best = (a, b)
        out.extend(best if best else [p])
    return out


def syllables_of_verse(verse: str) -> list[str]:
    """แบ่งพยางค์ทั้งวรรค

    ⚠️ อ่านหมายเหตุใน klon-paet.md §3 ว่าทำไมห้ามส่ง ssg ทั้งวรรคแบบดิบ ๆ
    ที่ทำได้คือส่งทั้งวรรคแล้วซ่อมสองด่าน — **รวมเศษที่ไม่มีสระกลับ** แล้ว
    **ผ่าก้อนที่อ่านไม่ออก** ซึ่งวัดแล้วดีกว่าตัดคำก่อน เพราะตัวตัดคำแตกคำ
    อักขรวิธีเก่าเป็นเศษมากกว่าตัวแบ่งพยางค์เสียอีก
    """
    from pythainlp.tokenize import subword_tokenize, word_tokenize

    raw: list[str] = []
    for w in word_tokenize(verse.replace("​", " "), keep_whitespace=False):
        if not w.strip():
            continue
        raw.extend(x for x in subword_tokenize(w, engine="ssg") if x.strip())
    out = _split_unparsable(_merge_orphans(raw))
    return [s for s in out if re.search(r"[ก-๙]", s)]


def count_syllables(verse: str) -> int:
    return len(syllables_of_verse(verse))


# ---------------------------------------------------------------- ก้อนจังหวะ
def rhythm_groups(n: int) -> tuple[int, ...]:
    """จังหวะของวรรคตามจำนวนพยางค์ — 9 พยางค์อ่าน 3-3-3 (วัดจากสุนทรภู่ 59 วรรค)"""
    if n <= 7:
        return (3, 2, max(0, n - 5))
    if n == 8:
        return (3, 2, 3)
    if n == 9:
        return (3, 3, 3)
    if n == 10:
        return (3, 3, 4)
    return (3, 3, n - 6)


if __name__ == "__main__":
    import sys

    for arg in sys.argv[1:]:
        syls = syllables_of_verse(arg)
        print(f"{arg}\n  พยางค์ {len(syls)}: {' | '.join(syls)}")
        print(f"  คีย์ท้าย {rhyme_key(syls[-1]) if syls else ()}"
              f"  เสียง {tone(syls[-1]) if syls else '?'}"
              f"  {'คำตาย' if syls and is_dead(syls[-1]) else 'คำเป็น'}")
