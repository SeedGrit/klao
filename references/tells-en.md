# Tells ภาษาอังกฤษ (docs / commit body / PR body / README)

> **ที่มาของไฟล์นี้ต่างจาก `tells-th.md`** corpus ทั้งสี่ชุดของ klao เป็นภาษาไทยล้วน
> กฎอังกฤษที่เป็น**รายการคำ** จึงเป็น `borrowed` (Wikipedia: Signs of AI writing เป็นหลัก)
> ส่วนกฎที่กลั่นจาก commit/PR ของเจ้าของเองเป็น `corpus` — ระบุไว้รายหมวด

## สิ่งที่ **ไม่ใช่** tell ใน repo พวกนี้ — อย่าไปแก้

> EN-FP · corpus · เทียบจาก commit body เก่าของเจ้าของ — รายการนี้ชนะกฎทุกข้อข้างล่าง

เสียงอังกฤษของเจ้าของอาจมีของที่ *ดูเหมือน* AI แต่เป็นลายเซ็นจริง เทียบจาก commit body
เก่า ๆ ของเจ้าของเองก่อนตัดสินใจแก้อะไร ตัวอย่างที่พบบ่อย:

- **em-dash** — ถูกต้องและใช้เยอะ. กฎ "ห้าม em-dash" ใช้กับ **สตริงไทยที่ผู้ใช้เห็นเท่านั้น**
- **"not X, but Y"** เมื่อใช้แยกแยะสาเหตุจริง ๆ
  ("not a calendar that is hard to use, but one that is hard to reach") — เก็บไว้
- **ตัวเลขวัดจริง** ("17px inside a 122px field in Chrome 148") — นี่คือของดี ไม่ใช่ความยาวเกิน
- **ย่อหน้าอธิบายว่าทำไมถึงไม่ทำอีกทางหนึ่ง** — เป็นแก่นของ commit body ทุกอัน
- **prose ยาว ๆ ใน commit body** — เจ้าของเขียนแบบนี้ตั้งใจ อย่าย่อเป็น bullet

---

## A. คำที่เป็น tell ตรง ๆ

> EN-01 · soft · borrowed · เป็น tell เมื่อ**ซ้ำ** หรือแทนคำธรรมดาได้ทันที ไม่ใช่เจอแล้วตัดทุกตัว

`delve` · `leverage` (เป็นกริยา) · `robust` · `seamless` · `comprehensive` · `utilize` ·
`facilitate` · `myriad` · `plethora` · `a testament to` · `the landscape of` · `the realm of` ·
`tapestry` · `game-changer` · `unlock` · `empower` · `elevate` · `crucial` · `vital` ·
`in today's fast-paced …` · `at the end of the day`

แทนด้วยคำธรรมดาหรือตัดทิ้ง: `utilize` → `use`, `facilitate` → `let`, `robust` → บอกว่ามันทน
อะไรได้จริง ๆ

## B. หางประโยคที่พูดซ้ำสิ่งที่เพิ่งพูด

> EN-02 · hard · borrowed · คู่ขนานกับ TH-UI-02 ฝั่งไทย

- `This ensures that …`
- `This allows you to …`
- `, making it easier to …`
- `, which means that …`

ถ้าประโยคก่อนหน้าบอกไปแล้ว ตัดทั้งหาง

## C. กาวย่อหน้า

> EN-03 · soft · borrowed · คู่ขนานกับหมวด J ฝั่งไทย (ตัดราวครึ่ง ไม่ใช่ทั้งหมด)

`Additionally,` · `Furthermore,` · `Moreover,` · `That said,` (เมื่อไม่ได้ค้านอะไรจริง) ·
`It's worth noting that` · `It's important to note that`

ส่วนใหญ่ตัดทิ้งได้ทั้งคำ ประโยคยังอ่านต่อกันได้เอง

## D. รูปร่างเอกสารที่เป็น tell

> EN-04 · soft · corpus · ข้อ 5–6 (PR body) มาจากวิธีเขียน PR ของเจ้าของเอง

1. **Bullet list ที่มี `**bold label** —` ทุกข้อ** เป็นค่า default
   ใช้ bullet เมื่อของมันเป็นรายการจริง ๆ (สาม shape, สี่ไฟล์) ถ้าเป็นเหตุผลต่อเนื่อง ให้เขียน prose
2. **ย่อหน้าสรุปปิดท้าย** ที่พูดซ้ำทั้งเอกสาร (`In summary` / `Overall` / `To sum up`) — ตัด
3. **หัวข้อ Title Case ทุกอัน** + emoji นำหัวข้อ — ใช้ sentence case
4. **Tricolon ทุกประโยค** ("faster, cleaner, and more maintainable")
5. **PR body ที่เล่า diff เป็น bullet** ("Added X. Updated Y. Refactored Z.")
   diff บอกเองได้ว่าแก้อะไร body ต้องบอกว่า**ทำไม** และ**ทำไมถึงไม่เลือกอีกทาง**
6. **เปิดด้วย "This PR …" / "In this change, we …"** — เริ่มที่ปัญหาหรือที่พฤติกรรมใหม่เลย

## E. Hedging

> EN-05 · soft · borrowed · **กลับทิศใน `formal`/`forecast`** เหมือน TH-PR-08

`generally` · `typically` · `may potentially` · `might possibly` · `in most cases` ·
`can sometimes`

ถ้าไม่แน่ใจจริง ๆ ให้บอกว่าไม่แน่ใจตรง ๆ และบอกว่าจะรู้ได้ยังไง อย่าโรย hedge ไปทั่ว

## F. เปิดแบบประจบ

> EN-06 · hard · borrowed

`Great question!` · `Absolutely!` · `You're right to be concerned about …` — ตัดทั้งประโยค

---

## Commit subject — เสียงของ repo

> EN-07 · soft · corpus · ยกมาจาก commit จริงของเจ้าของใน repo งานจริง (ไม่ได้อยู่ใน log ของ repo นี้)

subject เป็น**ประโยคที่บอกว่าตอนนี้ของมันทำอะไร** ไม่ใช่ชื่องานที่ไปทำมา ตัวอย่างเสียงที่ใช้จริง:

```
fix(ui): the copy drops its em-dashes and its AI voice
fix(ui): a phone stops zooming when you type, and stops scrolling sideways
fix(form): the whole date field opens the calendar, not its 17px glyph
copy(settings): shorter subtitle on หน้าตั้งค่า
```

สังเกต: lowercase หลัง `type(scope):`, ประธานเป็นตัวของที่ถูกแก้ (the copy / the running clock /
a phone), ไม่มีคำว่า "add" หรือ "update" นำ, ปนไทยได้เมื่ออ้างชื่อหน้าจริง
