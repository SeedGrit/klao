#!/usr/bin/env python3
"""ดึงงานของสุนทรภู่จาก vajirayana.org (หอพระสมุดวชิรญาณ) มาเก็บเป็นไฟล์ดิบ

ตัวไซต์ v2 เป็น VitePress ที่ render ฝั่งเซิร์ฟเวอร์ไว้แล้ว เนื้อกลอนจึงอยู่ใน HTML
ตรง ๆ ใน <div class="vp-doc"> โดยหนึ่งวรรคเป็นหนึ่งบรรทัด ไม่ต้องรัน JS

    python3 tools/fetch_sunthorn.py            # ดึงเฉพาะที่ยังไม่มีในแคช
    python3 tools/fetch_sunthorn.py --force    # ดึงใหม่ทั้งหมด

ผลลงที่ data/raw/<slug>.txt  (บรรทัดแรกเป็น title, ที่เหลือเป็นเนื้อ)
"""
from __future__ import annotations

import argparse
import html
import json
import re
import sys
import time
import urllib.parse
from pathlib import Path

import requests

ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / "data" / "raw"
BASE = "https://vajirayana.org"
UA = "klao-corpus-bot/1.0 (+https://github.com/SeedGrit/klao) corpus build for Thai prosody research"

THAI_DIGITS = "๐๑๒๓๔๕๖๗๘๙"


def thnum(n: int) -> str:
    """URL ของวชิรญาณใช้เลขไทย `ตอนที่-๑๐` ไม่ใช่ `ตอนที่-10`"""
    return "".join(THAI_DIGITS[int(d)] for d in str(n))


def chapters(prefix: str, first: int, last: int) -> list[str]:
    return [f"{prefix}{thnum(n)}" for n in range(first, last + 1)]


# แผนที่หนังสือ → งานที่อยู่ข้างใน  ดู data/SOURCES.md ว่าทำไมถึงเลือกเท่านี้
# หน้า index / คำนำ / อธิบาย ไม่ได้อยู่ในนี้เพราะเป็นร้อยแก้วของกรรมการหอสมุด ไม่ใช่กลอน
#
# ⚠️ คลังนี้เก็บ **กลอนแปดอย่างเดียว** ฉันท์ กาพย์ โคลง กลอนบทละคร กลอนเสภา
# นับพยางค์คนละแบบและวางสัมผัสคนละที่ ถ้าปนเข้ามาจะพากฎใน references/klon-paet.md
# เพี้ยนทั้งไฟล์ รายการที่ตัดออกพร้อมเหตุผลอยู่ใน OTHER_METERS ข้างล่าง
BOOKS: dict[str, list[str]] = {
    "พระอภัยมณี": chapters("ตอนที่-", 1, 132)
    + ["นิทานเรื่องพระอภัยมณี-ต่อจากคำกลอนที่พิมพ์แล้ว"],
    "โคบุตรและจันทโครบ": chapters("โคบุตร/ตอนที่-", 1, 14)
    + chapters("จันทโครบ/ตอนที่-", 1, 4),
    "สิงหไกรภพ": chapters("ตอนที่-", 1, 19),
    "ลักษณวงศ์": chapters("ตอนที่-", 1, 20),
    "ประชุมกลอนนิราศต่างๆ-ภาคที่-๑-นิราศสุนทรภู่-๔-เรื่อง": [
        "นิราศเมืองแกลง",
        "นิราศพระบาท",
        "นิราศภูเขาทอง",
        "นิราศวัดเจ้าฟ้า",
    ],
    "ประชุมกลอนนิราศต่างๆ-ภาคที่-๒-นิราศสุนทรภู่-๔-เรื่อง": [
        "นิราศอิเหนา",
        "นิราศพระประธม",
        "นิราศเมืองเพ็ชร",
        # ไม่ใช่ของสุนทรภู่ (สามเณรกลั่น) แต่เป็นกลอนแปดร่วมสมัยที่พิมพ์รวมเล่มเดียวกัน
        # เก็บไว้เป็น **ชุดควบคุม** ของตัวตรวจคำนอกคลัง ไม่เข้าพจนานุกรม
        "นิราศพระแท่นดงรัง",
    ],
    "รำพันพิลาป-ฉบับชำระใหม่": ["รำพันพิลาป"],
    "สวัสดิรักษาคำกลอน-เพลงยาวถวายโอวาท": [
        "สวัสดิรักษา",
        "เพลงยาวถวายโอวาท",
        "สุภาษิตสอนสตรี",
    ],
}

# งานของสุนทรภู่ที่ **ไม่ได้** อยู่ในคลัง เพราะเป็นฉันทลักษณ์อื่น
# เขียนไว้ให้รอบหน้ารู้ว่าไม่ได้ลืม และรู้ว่าจะไปเอาที่ไหนถ้าจะขยาย
OTHER_METERS: dict[str, str] = {
    "โคลงนิราศสุพรรณ": "โคลงสี่สุภาพ — บทละ 4 บาท เอกโท ไม่ใช่สัมผัสนอกสามจุด",
    "กาพย์เรื่องพระไชยสุริยา": "กาพย์ยานี/ฉบัง/สุรางคนางค์ สลับกัน วรรคละ 5-6 คำ",
    "บทเห่กล่อมพระเจ้าลูกเธอ": "กาพย์ยานี ๑๑ + บทเห่ วรรคละ 5-6 คำ",
    "บทละครเรื่องอภัยนุราช": "กลอนบทละคร วรรคละ 6-7 คำ ขึ้นต้นด้วยคำบอกบท",
    "เสภา เรื่องพระราชพงศาวดาร": "กลอนเสภา จังหวะขับ ไม่ใช่ 3-2-3",
    "ขุนช้างขุนแผน ตอนกำเนิดพลายงาม": "กลอนเสภา (และเป็นตอนเดียวในเล่มที่เป็นของท่าน)",
}

# ร้อยแก้วของกรรมการหอพระสมุด เก็บไว้ต่างหากเพื่ออ้างเรื่องผู้แต่ง ไม่เข้าคลังกลอน
NOTES: dict[str, list[str]] = {
    "พระอภัยมณี": [
        "อธิบาย-ว่าด้วยเรื่องพระอภัยมณีของสุนทรภู่",
        "ประวัติสุนทรภู่",  # มีบัญชีงานทั้งหมดของท่านพร้อมจำนวนเล่มสมุดไทย
        "คำนำ-พศ-๒๕๔๔",
        "คำนำ-พศ-๒๕๒๙",
        "คำนำเมื่อพิมพ์ครั้งแรก",
    ],
    "สวัสดิรักษาคำกลอน-เพลงยาวถวายโอวาท": ["อธิบายเรื่องสุภาษิตของสุนทรภู่"],
    "โคบุตรและจันทโครบ": [
        "โคบุตร/อธิบายเรื่องโคบุตร",
        "จันทโครบ/อธิบายเรื่องจันทโครบ",
    ],
    "สิงหไกรภพ": ["คำอธิบาย"],
    "ลักษณวงศ์": ["คำอธิบาย"],
    "ประชุมกลอนนิราศต่างๆ-ภาคที่-๑-นิราศสุนทรภู่-๔-เรื่อง": ["อธิบายนิราศ"],
    "ประชุมกลอนนิราศต่างๆ-ภาคที่-๒-นิราศสุนทรภู่-๔-เรื่อง": ["คำนำ"],
}


def slugify(book: str, chapter: str) -> str:
    return f"{book}__{chapter}".replace("/", "__")


def page_url(book: str, chapter: str) -> str:
    path = "/".join(urllib.parse.quote(p) for p in [book] + chapter.split("/"))
    return f"{BASE}/v2/books/{path}"


TAG_RE = re.compile(r"<[^>]+>")
DOC_RE = re.compile(r'<div class="vp-doc[^"]*"[^>]*>(.*?)<footer', re.S)
MAIN_RE = re.compile(r"<main[^>]*>(.*?)</main>", re.S)
TITLE_RE = re.compile(r"<title>(.*?)</title>", re.S)


def extract(page: str) -> tuple[str, list[str]]:
    m = DOC_RE.search(page) or MAIN_RE.search(page)
    if not m:
        raise ValueError("ไม่พบ vp-doc")
    body = TAG_RE.sub("\n", m.group(1))
    lines = [html.unescape(x).strip() for x in body.split("\n")]
    lines = [x for x in lines if x and x != "​"]
    t = TITLE_RE.search(page)
    title = html.unescape(t.group(1)).split("|")[0].strip() if t else ""
    return title, lines


def fetch(session: requests.Session, url: str, retries: int = 4) -> str:
    delay = 2.0
    for attempt in range(retries):
        try:
            r = session.get(url, timeout=90)
            r.raise_for_status()
            # วชิรญาณไม่ส่ง charset มาใน Content-Type ถ้าปล่อยให้ requests เดา
            # มันเลือก latin-1 แล้วได้ไฟล์เป็นขยะทั้งคลังโดยไม่มีอะไรร้อง
            return r.content.decode("utf-8")
        except Exception as exc:  # noqa: BLE001 — ขอแค่ retry แล้วรายงาน
            if attempt == retries - 1:
                raise
            print(f"    retry {attempt + 1}/{retries - 1} ({exc})", file=sys.stderr)
            time.sleep(delay)
            delay *= 2
    raise AssertionError("unreachable")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--force", action="store_true", help="ดึงใหม่แม้มีในแคชแล้ว")
    ap.add_argument("--delay", type=float, default=0.4, help="วินาทีระหว่างคำขอ")
    args = ap.parse_args()

    RAW.mkdir(parents=True, exist_ok=True)
    session = requests.Session()
    session.headers["User-Agent"] = UA

    jobs = [(b, c, "poem") for b, cs in BOOKS.items() for c in cs]
    jobs += [(b, c, "note") for b, cs in NOTES.items() for c in cs]

    manifest, failed = [], []
    for i, (book, chapter, kind) in enumerate(jobs, 1):
        slug = slugify(book, chapter)
        out = RAW / f"{slug}.txt"
        if out.exists() and not args.force:
            manifest.append({"book": book, "chapter": chapter, "kind": kind, "file": out.name})
            continue
        url = page_url(book, chapter)
        print(f"[{i}/{len(jobs)}] {book}/{chapter}")
        try:
            title, lines = extract(fetch(session, url))
        except Exception as exc:  # noqa: BLE001
            print(f"    FAILED {exc}", file=sys.stderr)
            failed.append({"book": book, "chapter": chapter, "url": url, "error": str(exc)})
            continue
        out.write_text("\n".join([title, url] + lines) + "\n", encoding="utf-8")
        manifest.append(
            {"book": book, "chapter": chapter, "kind": kind, "file": out.name,
             "title": title, "url": url, "lines": len(lines)}
        )
        time.sleep(args.delay)

    (RAW / "manifest.json").write_text(
        json.dumps({"manifest": manifest, "failed": failed}, ensure_ascii=False, indent=1),
        encoding="utf-8",
    )
    print(f"\nได้ {len(manifest)} หน้า · พลาด {len(failed)}")
    for f in failed:
        print("  พลาด:", f["book"], f["chapter"], f["error"])
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
