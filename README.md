# klao เกลาคำ

Claude Code skill สำหรับเกลาข้อความภาษาไทย: ตัด "สำนวน AI" และคำที่อธิบายซ้ำกับสิ่งที่จอ
หรือบริบทบอกอยู่แล้ว โดยไม่เปลี่ยนความหมายและไม่แตะ logic

จุดต่างจาก humanizer ทั่วไป: กฎทุกข้อกลั่นจากงานแก้จริงที่ merge แล้ว (copy-edit UI ไทย
ราว 50 จุด + คู่มือรีวิวเนื้อหายาวที่ AI ร่าง) ไม่ใช่ลิสต์แปลจากภาษาอังกฤษ และเน้นหนักที่
UI string (empty state, toast, placeholder, aria-label) ที่ skill สายบทความไม่ค่อยแตะ

## ติดตั้ง

```sh
git clone https://github.com/SeedGrit/klao ~/.claude/skills/klao
```

เปิด Claude Code ใหม่ แล้ว `/klao` จะอยู่ในลิสต์ skill ใช้ได้ทุกโปรเจกต์

## ใช้

พิมพ์ `/klao` พร้อมขอบเขต หรือพูดลอย ๆ ก็ทริกเอง เช่น "เกลาคำหน้านี้" "อ่านแล้วเหมือน AI เขียน"
"ยาวไป"

จบงานจะได้ตาราง before → after ทุกบรรทัดที่แก้ ให้ veto ได้ทีละอัน พร้อมรายการที่จงใจไม่แตะ
และเหตุผล

ที่ skill ไม่ทำ: แปลภาษา เขียนเนื้อหาใหม่ หลบ AI detector

## โครง

| ไฟล์ | มีอะไร |
|---|---|
| `SKILL.md` | workflow: ขอบเขต → สแกน → กฎไทย → ห้ามแตะ → gate → รายงาน |
| `references/tells-th.md` | ตาราง before/after 8 หมวด สำหรับสตริงไทยและ prose ยาว |
| `references/tells-en.md` | tells อังกฤษ เปิดด้วยรายการที่ห้ามแก้เพราะเป็นเสียงเจ้าของ |
| `references/repos.md` | โครงสำหรับเขียนกฎเฉพาะราย repo ของคุณเอง |
| `references/repos.local.md` | กฎจริงของ repo ส่วนตัว เขียนเองตามโครงข้างบน (gitignored) |

## กฎที่พลาดง่ายที่สุด

em-dash เป็น tell เฉพาะในข้อความไทย ส่วน prose อังกฤษ (commit body, PR, docs) ใช้ em-dash
ได้ และอาจเป็นลายเซ็นของคนเขียนอยู่แล้ว เช่นเดียวกับ "not X, but Y" ที่ใช้แยกแยะสาเหตุจริง
skill จึงแยกกฎไทย/อังกฤษคนละไฟล์ และเปิดหัวไฟล์อังกฤษด้วยรายการ "ห้ามแก้"

## งานอื่นที่ใกล้กัน

ของไทยและเพื่อนบ้านที่ควรรู้จัก คนละโฟกัสกับ klao แต่ใช้ร่วมกันได้:

- [chakrit/kien-thai](https://github.com/chakrit/kien-thai) · สอน AI เขียนภาษาไทยทั้งระบบ
  82 กฎพร้อม eval เน้น prose ยาว
- [vikimark/stop-slop-thai](https://github.com/vikimark/stop-slop-thai) · port ไทยของ
  stop-slop มีตารางคำ AI → คำแทน
- [citelogics-th/thai-humanizer](https://github.com/citelogics-th/thai-humanizer) ·
  humanizer ไทยสาย voice-matching
- [longhang2004/vietnamese-humanizer](https://github.com/longhang2004/vietnamese-humanizer) ·
  เวียดนาม โครง eval กับ false-positives ดีมาก
- [Wikipedia: Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing) ·
  แคตตาล็อก tell อังกฤษที่ครบที่สุด

## License

MIT
