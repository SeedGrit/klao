# klao — เกลาคำ

Claude Code skill สำหรับเกลาข้อความภาษาไทย: ตัด "สำนวน AI" และตัดคำที่อธิบายซ้ำกับสิ่งที่จอ
หรือบริบทบอกอยู่แล้ว โดยไม่เปลี่ยนความหมายและไม่แตะ logic

จุดต่างจาก humanizer ทั่วไป: กฎทุกข้อกลั่นจาก**งานแก้จริงที่ merge แล้ว** — งาน copy-edit
UI ไทยราว 50 จุด กับคู่มือรีวิวเนื้อหายาวที่ AI ร่าง ไม่ใช่ลิสต์คำต้องห้ามที่แปลมาจากภาษาอังกฤษ
และโฟกัสหนักที่ **UI string** (empty state, toast, placeholder, aria-label) ซึ่ง skill
สายบทความไม่ค่อยครอบคลุม

## ติดตั้ง

```sh
git clone https://github.com/SeedGrit/klao ~/.claude/skills/klao
```

เปิด Claude Code ใหม่ แล้ว `/klao` จะอยู่ในลิสต์ skill (ใช้กับทุกโปรเจกต์)

## ใช้

พิมพ์ `/klao` พร้อมขอบเขต หรือพูดลอย ๆ ก็ทริกเอง — "เกลาคำหน้านี้", "อ่านแล้วเหมือน AI เขียน",
"ตัดสำนวน AI", "ยาวไป"

จบงานจะได้ตาราง before → after ทุกบรรทัดที่แก้ ให้ veto ได้ทีละอัน พร้อมรายการที่จงใจไม่แตะ
และเหตุผล

ขอบเขตที่ skill ไม่ทำ: แปลภาษา, เขียนเนื้อหาใหม่, หลบ AI detector

## โครง

| ไฟล์ | มีอะไร |
|---|---|
| `SKILL.md` | workflow: ขอบเขต → สแกน → กฎไทย → ห้ามแตะ → gate → รายงาน |
| `references/tells-th.md` | ตาราง before/after 8 หมวด สำหรับสตริงไทยและ prose ยาว |
| `references/tells-en.md` | tells อังกฤษ **+ รายการที่ห้ามแก้เพราะเป็นเสียงเจ้าของ** |
| `references/repos.md` | โครงสำหรับเขียนกฎเฉพาะราย repo ของคุณเอง |
| `references/repos.local.md` | (gitignored) กฎจริงของ repo ส่วนตัว — เขียนเองตามโครงข้างบน |

## กฎที่พลาดง่ายที่สุด

**em-dash ถูกแบนเฉพาะสตริงไทยที่ผู้ใช้เห็น** — prose อังกฤษ (commit body, PR, docs) ใช้
em-dash ได้และอาจเป็นลายเซ็นของคนเขียนอยู่แล้ว เช่นเดียวกับ "not X, but Y" ในอังกฤษที่ใช้
แยกแยะสาเหตุจริง ๆ skill นี้จึงแยกกฎไทย/อังกฤษเป็นคนละไฟล์ และเปิดหัวไฟล์อังกฤษด้วยรายการ
"ห้ามแก้"

## งานอื่นที่ใกล้กัน

ของไทยและเพื่อนบ้านที่ควรรู้จัก (คนละโฟกัสกับ klao แต่เอามาใช้ร่วมกันได้):

- [chakrit/kien-thai](https://github.com/chakrit/kien-thai) — สอน AI เขียนภาษาไทยทั้งระบบ
  (โครง 82 กฎ + eval) เน้น prose ยาว
- [vikimark/stop-slop-thai](https://github.com/vikimark/stop-slop-thai) — port ของ stop-slop
  เป็นไทย มีตารางคำ AI → คำแทน
- [citelogics-th/thai-humanizer](https://github.com/citelogics-th/thai-humanizer) — humanizer
  ไทยสาย voice-matching
- [longhang2004/vietnamese-humanizer](https://github.com/longhang2004/vietnamese-humanizer) —
  เวียดนาม แต่โครง eval + false-positives ดีมาก
- [Wikipedia: Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing) —
  แคตตาล็อก tell อังกฤษที่ครบที่สุด

## License

MIT
