# SPEC v1.2 — จาก skill ส่วนตัว เป็น skill สาธารณะเต็มตัว

> สถานะ: **รอทำ** · เขียน 2026-07-28 จากผล research เทียบ skill เกลาคำไทย/เทศ 8 ตัว
> ผู้ทำ: session ใหม่อ่านไฟล์นี้แล้วลงมือได้เลย ไม่ต้องมี context อื่น
> ตำแหน่ง repo: `~/Sites/Seed/klao` (= `~/.claude/skills/klao` ผ่าน symlink) · push ขึ้น
> `SeedGrit/klao` (public) ได้ทุก commit — **ห้ามมีข้อมูลของ repo ส่วนตัวใด ๆ ในไฟล์ที่ commit**
> (กฎราย repo อยู่ `references/repos.local.md` ซึ่ง gitignored เท่านั้น)

## สถานะปัจจุบัน (v1.1.0)

| ไฟล์ | มีอะไร |
|---|---|
| `SKILL.md` | workflow 8 ขั้น: ขอบเขต → สแกน → กฎไทย 6 ข้อ → กฎอังกฤษ → ห้ามแตะ → gate → รายงาน → commit |
| `references/tells-th.md` | หมวด A–H: em-dash 4 ท่า (A), ขีดเปล่า (B), select placeholder (C), ข้อสรุปขึ้นก่อน (D), คำที่บริบทถือ (E), placeholder รูปร่างคำตอบ (F), คำหยอด (G), prose ยาว (H1–H8) |
| `references/tells-en.md` | เปิดด้วยรายการ "ไม่ใช่ tell ห้ามแก้" แล้วค่อย A–F + commit subject voice |
| `references/repos.md` | template สำหรับเขียนกฎราย repo ลง `repos.local.md` |

## หลักคุมทั้ง spec (อ่านก่อนลงมือ)

1. **SKILL.md ห้ามบวม** — กฎใหม่ทั้งหมดลง `references/` แล้วให้ SKILL.md ชี้ไป
   (progressive disclosure แบบ stop-slop-thai: ตัวหลัก 6KB, ลิสต์ 36KB โหลดเมื่อใช้)
2. **ทุกกฎใหม่ต้องระบุที่มา** หนึ่งในสาม: `corpus` (จากงานแก้จริงของเรา) ·
   `borrowed` (ยืมจาก repo MIT ระบุชื่อ) · `provisional` (ยังไม่มีหลักฐาน รอ corpus ยืนยัน)
   — ตามวินัยของ kien-thai และ honesty pattern ของ octomind-tap
3. **klao เป็น editor ไม่ใช่ detector** — ไม่ตัดสินว่าข้อความเป็น AI เขียน ไม่ช่วยหลบ detector
   ไม่เติมความผิดพลาดปลอมให้ดูเป็นคน (anti-goals ตาม vietnamese-humanizer)
4. กฎใหม่อันไหนทับกับหมวดเดิม ให้ **merge เข้าหมวดเดิม** ไม่ตั้งซ้ำ (ระบุ mapping ไว้ในงาน 2 แล้ว)

## แหล่งที่ยืมได้ (MIT ทั้งหมด — ต้อง credit ใน `references/upstream-notice.md`, งาน 6)

- [vikimark/stop-slop-thai](https://github.com/vikimark/stop-slop-thai) — ตารางวลี/โครงสร้างไทย
- [chakrit/kien-thai](https://github.com/chakrit/kien-thai) — สำนวนแปล, budget คำเชื่อม, use-vs-mention
- [citelogics-th/thai-humanizer](https://github.com/citelogics-th/thai-humanizer) — opener/connector patterns
- [longhang2004/vietnamese-humanizer](https://github.com/longhang2004/vietnamese-humanizer) — โครง false-positives, output modes, preservation contract
- [beefiker/superloopy humanize-korean](https://github.com/beefiker/superloopy/tree/main/skills/humanize-korean) — โครง audit script, change-rate budget, S1/S2 tiers

---

## งาน 1 — rule ID + ระดับความเข้ม (ทำก่อน งานอื่นอ้าง ID)

**Scheme:** `TH-UI-xx` (สตริง UI ไทย = หมวด A–G เดิม) · `TH-PR-xx` (prose ไทย = H + หมวดใหม่) ·
`EN-xx` (อังกฤษ) — เลขรันตามลำดับในไฟล์ ห้าม reuse เลขที่เลิกใช้

**ระดับ:** `hard` = เจอแล้วแก้เสมอ · `soft` = เป็น tell เมื่อ**ซ้ำ**หรือผิด register เท่านั้น
(เช่น tricolon อันเดียวไม่ผิด ผิดตอนทุกย่อหน้าเป็น; อย่างไรก็ตาม ตัดราวครึ่งหนึ่งของที่เจอ ไม่ใช่หมด)

**วิธีใส่:** เติมบรรทัดใต้หัวข้อแต่ละหมวดใน tells-th/tells-en เช่น
`> TH-UI-01 · hard · corpus` — **ไม่ต้อง** แปลงไฟล์เป็น YAML/JSON (เกินจำเป็นสำหรับ skill ขนาดนี้;
ค่อยทำเมื่อมี tooling อ่านจริง)

**Acceptance:** ทุกหมวดใน tells-th.md / tells-en.md มี ID + ระดับ + ที่มา · SKILL.md §7 สั่งให้
ตาราง before→after อ้าง ID ทุกแถว

---

## งาน 2 — เพิ่ม tells ไทยชุดใหม่ (วัตถุดิบกลั่นจาก research แล้ว ใช้ได้เลย)

### 2a. merge เข้าหมวด H เดิม

| เข้าที่ | เพิ่มอะไร | ที่มา |
|---|---|---|
| H1 (ไม่ใช่ X แต่ Y) | variants: `ไม่เพียงแต่…แต่ยัง…`, `ไม่ใช่แค่ X แต่ยังเป็น Y`, `ปัญหาไม่ได้อยู่ที่ X แต่อยู่ที่ Y`, `คำตอบไม่ใช่ X แต่คือ Y`, negative listing (`ไม่ใช่ X… ไม่ใช่ Y… แต่คือ Z` → พูด Z เลย) | borrowed: stop-slop-thai |
| H3 (closer สำเร็จรูป) | `โดยสรุป` `กล่าวโดยสรุป` `จะเห็นได้ว่า` `ดังที่กล่าวมาข้างต้น` `ท้ายที่สุดแล้ว` `หวังว่าจะเป็นประโยชน์` `อนาคตสดใสรออยู่` `ขอให้โชคดี` | borrowed: stop-slop-thai, thai-humanizer |
| H5 (อย่าง+adj) | `อย่างมีนัยสำคัญ` `อย่างยิ่งยวด` `อย่างลงตัว` `ครบครัน` + หมายเหตุ: `อย่างมาก`/`อย่างมีประสิทธิภาพ` เป็น native บาง register → ลง false-positives (งาน 3) | borrowed: thai-humanizer, kien-thai |
| H7 (คำเชื่อมฟุ่มเฟือย) | **budget แบบ kien-thai**: ซึ่ง ≤1/ประโยค (antecedent รูปธรรมใช้ ที่), โดย ≤1/ย่อหน้า, ในขณะที่ = เวลาเท่านั้นไม่ใช่ contrast (contrast ใช้ แต่/ส่วน/กลับ) | borrowed: kien-thai |
| H8 (hedging) | hedge stack `อาจจะมีความเป็นไปได้ที่จะ` → เหลือ อาจ เดียวเมื่อไม่แน่จริง | borrowed: kien-thai |

### 2b. หมวดใหม่ I — opener สำเร็จรูป (`hard`)

เปิดเรื่องด้วยของจริง (อาการ ตัวเลข คำถามจริง) ไม่ใช่ท่าเปิดสำเร็จรูป:

- ยุคสมัย: `ในยุคที่…` `ในยุคดิจิทัล` `ในโลกปัจจุบัน(ที่)…` `ในบริบทของ…`
- ประกาศสัจธรรม: `เป็นที่ทราบกันดีว่า` `ปฏิเสธไม่ได้ว่า` `แน่นอนว่า` `เป็นที่น่าสังเกตว่า`
- clickbait: `คุณเคยสงสัยไหมว่า…` `เคยไหมที่…` `ลองจินตนาการว่า…` `จะเป็นอย่างไรถ้า…`
- ขอเกริ่นก่อน: `ก่อนอื่นเรามาทำความเข้าใจกันก่อนว่า…` `เรามาดูกันว่า…` `มาเริ่มกันที่…`
- meta: `ในบทความนี้…` `ในส่วนนี้เราจะ…` `ดังที่จะกล่าวต่อไป…`
- ประโยค generality ว่างเปล่า (`โลกกำลังเปลี่ยนแปลงอย่างรวดเร็ว`) — **ตัดทั้งประโยค** ไม่ใช่รีไรต์

ที่มา: borrowed (stop-slop-thai, thai-humanizer, MarketThink article) + corpus บางส่วน

### 2c. หมวดใหม่ J — กาวย่อหน้าไทย (`soft` — เป็น tell เมื่อซ้ำ)

คู่ขนานกับ `Additionally,` ฝั่งอังกฤษที่มีอยู่แล้ว: ขึ้นประโยคด้วย `นอกจากนี้` (ตัวการอันดับหนึ่ง)
`อีกทั้ง` `ยิ่งไปกว่านั้น` `ทั้งนี้` `อย่างไรก็ตาม` `ในขณะเดียวกัน` `กล่าวคือ` `โดยเฉพาะอย่างยิ่ง`
— ส่วนใหญ่ตัดทิ้งแล้วประโยคต่อกันเอง เหลือได้เมื่อ encode ความสัมพันธ์เชิงตรรกะที่จำเป็นจริง
(อย่างไรก็ตาม: ตัดราวครึ่ง ใช้ แต่ หรือขึ้นประโยคใหม่แทน — kien-thai)

ที่มา: borrowed (stop-slop-thai, thai-humanizer, kien-thai)

### 2d. หมวดใหม่ K — สำนวนแปล (translationese) (`hard` เกือบทั้งหมด)

| ก่อน | หลัง |
|---|---|
| `ทำการ` + กริยา (`ทำการบันทึก`) | กริยาเปล่า (`บันทึก`) |
| `มีความ` + คุณศัพท์ (`มีความสุขใจ`) | คุณศัพท์เปล่า (เว้นเน้นจริง) |
| `มีความสามารถในการ…` | `…ได้` / `ทำได้` |
| การ-chain (`การพัฒนาของระบบเศรษฐกิจของประเทศไทย`) | นามประกอบ (`การพัฒนาเศรษฐกิจไทย`) |
| `ถูก`/`โดน` passive กับเหตุการณ์ไม่ร้าย (`ถูกออกแบบมาเพื่อ`) | active หรือ `ออกแบบมาให้` |
| `ทำให้มั่นใจว่า…` (ensures that) | บอกผลตรง ๆ |
| `ในการที่จะ…` | `เพื่อ…` หรือตัด |
| `ในเรื่องของ` / `ในส่วนของ` (regarding) | ตัดได้เกือบเสมอ |
| `ไม่ว่าจะเป็น A, B หรือ C` (catalog แปล) | ราย A B C เปล่า ๆ หรือ `ทั้ง…และ` |
| `ถือเป็น` / `นับได้ว่าเป็น` / `ทำหน้าที่เป็น` / `ได้รับการยกย่องว่าเป็น` | `เป็น` / `คือ` |
| `มันคือ…ที่…` / dummy subject (`มันเป็นที่ชัดเจนว่า`) | `เห็นได้ชัดว่า` หรือเอาประธานจริงขึ้น |

ที่มา: borrowed (kien-thai เป็นหลัก, thai-humanizer) — สอดคล้องคำแนะนำราชบัณฑิตเรื่องบทแปล

### 2e. หมวดใหม่ L — ตารางคำ AI → คำแทน (`hard` เมื่อ abstract)

| คำ AI | ใช้แทน |
|---|---|
| ขับเคลื่อน | ผลักดัน / ทำให้เกิด / ช่วยให้ |
| ยกระดับ | ปรับปรุง / ทำให้ดีขึ้น |
| ปลดล็อก(ศักยภาพ) | เปิดทาง / ทำให้เข้าถึงได้ |
| พลิกโฉม / ปฏิวัติ | เปลี่ยน |
| เจาะลึก | ดู / ศึกษา / ตรวจสอบ |
| โอบรับ | ใช้ / ยอมรับ |
| ไร้รอยต่อ | ราบรื่น / ต่อเนื่อง |
| ภูมิทัศน์ (abstract) | วงการ / สถานการณ์ |
| หลากหลายมิติ | หลายด้าน |
| เป็นเครื่องพิสูจน์ | แสดงให้เห็น |
| นำทาง (navigate abstract) | รับมือ / จัดการ |
| เก็บเกี่ยว (harness) | ใช้ / นำมาใช้ |

ที่มา: borrowed (stop-slop-thai `references/phrases.md` — MIT) · เก็บเป็นตาราง 2 คอลัมน์แบบเขา

### 2f. หมวดใหม่ M — โครงสร้าง prose (`soft` ส่วนใหญ่)

- **false agency**: สิ่งไม่มีชีวิตทำกริยาคน (`ข้อมูลบอกเราว่า` `ตลาดตอบแทน` `ปัญหาต้องการทางออก`)
  → บอกว่าใครทำ
- **lazy extremes**: `ทุกคน` `ไม่มีใคร` `เสมอ` `หลาย ๆ คน` → ตัวเลขจริงหรือระบุกลุ่ม
- **แม้…แต่… bridge**: ยก downside มาเป็นสะพานข้ามไป upside — ถ้ายกมาต้องจริงจังกับมัน
- **ถาม-ตอบเอง**: `แล้วทำไมถึงเป็นแบบนั้น? คำตอบคือ…` → พูดเนื้อเลย
- **อธิบายซ้ำ**: `พูดง่าย ๆ ก็คือ…` — ถ้าต้องพูดง่ายอีกรอบ แปลว่ารอบแรกไม่ควรอยู่
- **emoji ทุก bullet / **bold** ทุก bullet** → เอาออก ให้เนื้อหานำ
- **ประโยค quotable**: อ่านแล้วเหมือนคำคม → รีไรต์เป็นประโยคธรรมดา

ที่มา: borrowed (stop-slop-thai, MarketThink) + corpus (กฎ bullet ตรงกับ tells-en D1 เดิม)

### 2g. ขยายหมวด B — empty state ระดับ section: การบ้านที่ไม่ต้องสั่ง (`corpus`, hard)

หมวด B เดิมจัดการ "ขีดเปล่าแทนค่าว่าง" ระดับบรรทัด — กฎนี้ยกขึ้นระดับ section:
**section ของฟีเจอร์รองที่ empty state ทั้งก้อนมีเนื้อหาแค่ "คุณยังไม่ได้ทำ X ไปทำ X สิ"
→ ไม่ต้อง render ทั้ง section** การบอกให้ผู้ใช้ไปทำการบ้านไม่ใช่ข้อมูล

| ก่อน | หลัง |
|---|---|
| heading `ที่ติดตาม` + badge `0` + การ์ด `ยังไม่ได้ติดตามใคร กดติดตามคนที่ชอบ แล้วโพสต์ของเขาจะขึ้นก่อนในฟีด` | ไม่แสดง section นี้เลยจนกว่าจะมีของ |

สังเกตว่าตัวอย่างนี้บอกความว่าง**สองรอบ**: badge `0` แล้วการ์ดอธิบายอีกที — ต่อให้เก็บ section
ไว้ badge ศูนย์กับการ์ดอธิบายว่างก็ต้องเหลืออันเดียว

ขอบเขตของกฎ:

- **ตัดทั้ง section** เมื่อเป็นฟีเจอร์รอง/ของประดับหน้า — ว่างแล้วหน้าไม่เสียความหมาย
- **เก็บ empty state** (แบบหมวด B เดิม) เมื่อ section คือเนื้อหาหลักของหน้า — ตารางที่คน
  ตั้งใจเปิดมาดู ว่างแล้วต้องบอกว่าว่างเพราะอะไร ไม่งั้นดูเหมือนโหลดพัง
- **mode `ask`** (งาน 4) เมื่อ empty state เป็น onboarding CTA ของฟีเจอร์หลักที่ product
  ตั้งใจดัน — อันนั้นเป็น product call ไม่ใช่ copy call ห้ามตัดเงียบ ๆ

### 2h. เสียงเจ้าของใน docs ไทย (`corpus` — เจ้าของเกลา README ของ repo นี้เอง)

corpus ชุดที่สาม และแม่นสุดเพราะเป็น diff ที่เจ้าของแก้มือกับข้อความที่ AI เกลามาแล้วรอบหนึ่ง
(commit `80c602f`) — ทุกกฎมีตัวอย่างจริงใน diff นั้น · register: `prose`/docs

| กฎ | ตัวอย่างจาก diff | ระดับ |
|---|---|---|
| **ไม่ไทยคำอังกฤษคำ** — มีคำไทยที่คนใช้จริง ให้ใช้ | `ไม่แตะ logic`→`ไม่กระทบกระบวนการทำงาน` · `copy-edit`→`ปรับคำ` · `veto`→`โต้แย้ง` · `ลิสต์แปล`→`รายการแปล` · `ทริกเอง`→`เปิดใช้ได้เอง` | soft — term of art คงอังกฤษ (UI string, em-dash, commit body) และเจ้าของเองยังใช้ `ลิสต์ skill` ในบริบท UI |
| **อังกฤษที่เก็บไว้ นิยมขึ้นต้น capital** | `klao`→`Klao` · `humanizer`→`Humanizer` · `Skill นี้` · `Before → After` | soft ("นิยม" — เจ้าของปล่อยตัวเล็กกลางประโยคบางจุด) · สอดคล้อง loanword-title-case ที่เจอใน corpus formal (งาน 7) = ยืนยันเป็นเสียงเจ้าของข้าม register |
| **สัญลักษณ์เป็นคำใน prose** | `+`→`และ` · `:` กลางประโยค→`คือ` | ขยายกฎ symbol-to-word ของ 7a จาก formal มาถึง docs |
| **ประโยคเต็มแทน fragment + colon** | `ที่ skill ไม่ทำ: แปลภาษา…`→`Skill นี้ไม่ครอบคลุมการแปลภาษา…` | docs ไทยเอียงทางการกว่า UI string |
| **soften เมื่อพูดถึงงานคนอื่น** | `ไม่ค่อยแตะ`→`ยังไม่ค่อยมี…ทำเท่าไหร่นัก` · `ควรรู้จัก`→`น่าสนใจ` · `คนละโฟกัส`→`โฟกัสอาจต่าง` | มารยาท ไม่ใช่ hedge ที่ต้องตัด (โยงช่อง ± ของ H8 ในตาราง 7c) |

→ เข้า **งาน 3** เพิ่มอีกหนึ่ง false-positive: **คอมมาคั่นตัวอย่างใน quote** (`"…", "…", "…"`)
เจ้าของ restore กลับเองหลัง AI ตัด — กฎ comma-apposition (kien-thai) ไม่ครอบลิสต์ตัวอย่างใน quote

**Acceptance งาน 2:** ทุกกฎมี ID/ระดับ/ที่มา · ไม่มีกฎซ้ำความกับหมวดเดิม (merge แล้ว) ·
SKILL.md ยาวขึ้นได้ไม่เกิน ~10 บรรทัด (สรุป + ชี้ references) · grep ใน §2 ของ SKILL.md
อัปเดตให้ครอบ tells ใหม่ตัวที่ grep ได้ (ทำการ, มีความ, นอกจากนี้ ฯลฯ)

---

## งาน 3 — `references/false-positives.md` (ของที่ดูเหมือน tell แต่ห้ามแก้)

โครงตาม vietnamese-humanizer + kien-thai: แต่ละรายการ = pattern · ทำไมถึงชอบโดน flag ผิด ·
เมื่อไหร่เป็น tell จริง · ตัวอย่าง

เนื้อหาตั้งต้น (ยกจากกฎ "ห้ามแตะ" เดิม + research):

1. **use-vs-mention** — ข้อความใน backtick/quote ที่กำลัง*พูดถึง* pattern ห้ามไป "แก้"
   (สำคัญมากตอนเกลาไฟล์ style guide หรือ SKILL.md เอง — kien-thai มีกฎนี้ตรง ๆ)
2. `ยิ่ง…ยิ่ง…` ที่เป็นสำนวนแท้ (`ยิ่งเร็วยิ่งดี`) — เป็น tell เมื่อใช้เป็นท่า closer ซ้ำ ๆ
3. en-dash ในช่วง (`08:00–20:00`, `จ–ศ`) + `·` separator — ถูกแล้ว
4. em-dash ใน prose อังกฤษ — ลายเซ็นคนเขียนได้ (กฎเดิม tells-en)
5. `ไม่ใช่ X แต่ Y` เมื่อ contrast คือประเด็นจริง ไม่ใช่ท่าเปิด
6. `อย่างมาก` / `อย่างมีประสิทธิภาพ` ใน register ทางการ — native (kien-thai corpus-traced)
7. ครับ/ค่ะ ใน chat/บทสนทนา — ไม่ใช่ tell (kien-thai เคย flag ผิดแล้วบันทึก postmortem —
   ใช้เป็นตัวอย่างแรกของ log ด้านล่าง)
8. ศัพท์เทคนิค/ชื่อแบรนด์/ทับศัพท์ที่ทีมใช้ — ห้าม "แปลกลับ" เป็นไทย
9. tricolon เดี่ยว — เป็น tell เมื่อทุก list เป็นสามชิ้น
10. `ซึ่ง` ใน technical/legal clause ที่ต้องการ antecedent ชัด

ท้ายไฟล์: **postmortem log** — ทุกครั้งที่ flag ผิดจริงในการใช้งาน ให้เพิ่ม entry ลงวันที่
(pattern · ทำไมถึง flag ผิด · กติกาใหม่) — แบบ kien-thai `docs/decisions/`

กติกาใช้: pattern ที่ FP สูง → **เสนอทางเลือก + เหตุผล** แทนแก้เงียบ ๆ (โยงกับ mode `ask` งาน 4)

**Acceptance:** ไฟล์มี ≥10 รายการตั้งต้น · SKILL.md §5 "ห้ามแตะ" ชี้มาไฟล์นี้ · กฎ FP-สูง
ระบุ mode ที่ต้องใช้

---

## งาน 4 — output modes + preservation contract

### 4a. สี่โหมด (ตาม vietnamese-humanizer — เลือกผิดโหมด = ผิดในตัว)

| mode | ใช้เมื่อ | ผลลัพธ์ |
|---|---|---|
| `rewrite` | tell ชัด แก้ได้โดยความหมายไม่ขยับ (default) | ข้อความใหม่ |
| `flag` | เนื้อหามีปัญหาที่แก้เองไม่ได้ เช่น คำชมไม่มีหลักฐาน, `ผู้เชี่ยวชาญระบุว่า…` ลอย ๆ — **ห้ามแต่งแหล่ง/ตัวเลขแทน** | คอมเมนต์บอกว่าขาดอะไร |
| `ask` | อ่านแล้วตีความได้หลายทาง แก้ทางไหนความหมายก็ขยับ | เสนอ 2-3 ทางพร้อม trade-off |
| `no-change` | ของสะอาดอยู่แล้ว | คืนทั้งดุ้น + บอกตรง ๆ ว่าไม่แก้ **ห้ามฝืนแก้เพื่อให้ดูมีผลงาน** |

### 4b. preservation contract (เข้มขึ้นจาก "ไม่เปลี่ยนความหมาย" บรรทัดเดียว)

hard blockers — ผิดข้อใดข้อหนึ่ง = แก้นั้น fail แม้อ่านลื่นขึ้น:

- modality คงเดิม: `อาจ` ≠ `จะ`, `ต้อง` ≠ `ควร`
- ห้าม upgrade correlation → causation (`สัมพันธ์กับ` ≠ `ทำให้`)
- ตัวเลข วันที่ ชื่อ URL เงื่อนไข negation คงเดิมทุกตัว
- ห้ามเติม fact ตัวอย่าง metric คำอ้างอิง ที่ไม่มีในต้นฉบับ
- placeholder/interpolation (`{name}`, `%s`, `${x}`) รอดครบ byte-for-byte
- register คงเดิม: ทางการอยู่ทางการ แชตอยู่แชต (ห้าม "ทำให้เป็นกันเอง" เอง)

### 4c. อัปเดต SKILL.md §7 รายงานกลับ

ตารางเพิ่ม 2 คอลัมน์: **rule ID** + **mode** · ท้ายรายงานแจ้ง **change rate** (% อักขระที่เปลี่ยน
โดยประมาณ) — เกิน ~50% = หยุด ถามก่อน (เพดานตาม humanize-korean; ของเราเน้น UI string
สั้น จึงใช้เป็นสัญญาณเตือน ไม่ใช่ hard gate)

**Acceptance:** SKILL.md อธิบาย 4 โหมด ≤15 บรรทัด (รายละเอียดลง references ถ้ายาว) ·
contract อยู่ใน §5 · ตารางรายงานมีคอลัมน์ใหม่

---

## งาน 5 — eval fixtures + audit script

### 5a. `evals/cases/*.md` — 20-30 เคส

format ต่อเคส (markdown ไฟล์ละเคส, ชื่อไฟล์ = slug):

```markdown
# <slug>
mode: rewrite | flag | ask | no-change
rules: TH-UI-01, TH-PR-07        # tells ที่ต้องเจอ (ว่างได้เมื่อ no-change)
preserve: "8 ชม.", "{name}"      # token ที่ต้องรอดครบ

## input
<ข้อความก่อน>

## expected
<ข้อความหลัง หรือคำอธิบาย flag/ask หรือ "เหมือน input" เมื่อ no-change>
```

ที่มาเคส: แปลงจากตาราง before/after ใน tells-th.md (สะอาดแล้ว ใช้ได้เลย) + เขียน
**no-change ≥5 เคส** (ประโยคไทยดี ๆ ที่มี ยิ่ง…ยิ่ง แท้, มี en-dash ช่วง, มี tricolon เดี่ยว —
วัดว่า skill ไม่ over-edit) + flag/ask อย่างละ ≥2

### 5b. `scripts/check.sh` — dependency-free (bash + grep เท่านั้น)

ทำ 3 อย่าง:
1. **tell counter**: นับ occurrence ของ pattern ต่อ rule ID (grep -c) ใน input vs output —
   กฎ hard ต้องเหลือ 0, กฎ soft ต้องไม่เพิ่ม
2. **preserve check**: ทุก token ใน `preserve:` ต้องอยู่ใน output ครบ (byte-for-byte)
3. **สรุป**: exit 1 พร้อมรายการที่ fail

ใช้สองทาง: รันกับ eval cases (CI ของ repo นี้เอง) และรันกับงานจริง (SKILL.md §6 เรียกใช้เป็น
gate เสริมได้เมื่อสะดวก)

### 5c. ไม่ใช้ LLM judge

ตาม ADR ของ kien-thai: judge ที่แชร์ prior กับคนเขียนมองไม่เห็น error class ที่ทดสอบอยู่ —
mechanical check เป็น advisory, คำตัดสินสุดท้ายคือหูเจ้าของภาษา ระบุไว้ใน `evals/README.md`

**Acceptance:** `bash scripts/check.sh` เขียวกับทุก expected ใน evals/cases ·
มี no-change ≥5 · script ไม่มี dependency นอก POSIX

---

## งาน 6 — ปิดท้าย

- `references/upstream-notice.md` — credit 5 แหล่ง (ตารางบนสุด) ระบุว่ายืมส่วนไหน ปรับอะไร
  (pattern ตาม humanize-korean)
- `CHANGELOG.md` — เริ่มที่ 1.1.0 (public release) แล้วบันทึก 1.2.0
- README: อัปเดตตารางโครง (ไฟล์ใหม่: false-positives, evals, scripts, upstream-notice) +
  ย่อหน้าสั้น ๆ เรื่อง output modes
- `SKILL.md` frontmatter: version 1.2.0
- แถม (ทำได้ถ้ามีแรง ไม่บล็อก): เปิด PR ไป
  [Muvon/octomind-tap](https://github.com/Muvon/octomind-tap) เสนอ klao เป็น Thai calibration
  anchor — ไฟล์ `content-locale-humanize-th` ของเขาเขียนไว้เองว่ายังไม่มี Thai tell list
  ให้เกาะ (ยืนยันกับ maintainer ก่อนว่ารับ external anchor ไหม)

## งาน 7 — `references/registers.md`: register ทางการ + บทพูด (กฎบางข้อกลับทิศ)

> ที่มา: **corpus จริงชุดที่สอง** — ขุด before/after 82 คู่จากร่าง proposal ยื่นประมูลลูกค้า
> องค์กรใหญ่ (draft ราย section → เล่มจริง) + สคริปต์ pitch/Q&A ของโปรเจกต์เดียวกัน
> ข้อมูลดิบ (มีชื่อลูกค้า **ห้าม commit**): `docs/corpus-formal-proposal.local.json` (gitignored)
> — session ที่ implement อ่านไฟล์นี้ได้เต็ม ๆ แต่ตัวอย่างที่ลง registers.md ต้อง genericize แล้ว

การค้นพบหลัก: **กฎ klao เป็น register-sensitive** — corpus พิสูจน์ว่าใน "เอกสารทางการยื่น
ลูกค้า/ประมูล" ทิศทางการเกลา*กลับด้าน*กับ UI/prose ทั่วไปหลายข้อ ไฟล์ registers.md จึงต้อง
ระบุ ต่อ register ว่ากฎไหน ใช้ / กลับทิศ / ปิด (แบบ genre-gating ของ humanize-korean)

### 7a. register `formal-proposal` — ตารางกฎกลับทิศ (จาก corpus)

| กฎ casual | ใน formal-proposal |
|---|---|
| สั้นกว่า = คนกว่า | **กลับทิศ**: ร่าง AI แบบ telegraphic ถูกขยายเป็นประโยคทางการเต็ม สัญลักษณ์กลายเป็นคำ (`10+ ปี`→`ทศวรรษหน้า`, `+`→`มากกว่า`, `MD`→`Managing Director`, `จุฬาฯ`→ชื่อเต็ม) |
| H8 ตัด hedge | **กลับทิศ**: คำเคลมเด็ดขาดถูก soften (`ไม่ผูกขาด`→`ลดความเสี่ยง…`, `ต้อง`→`ควร`, scare tactic ถูกลบ, เพิ่ม `อาจ`) |
| E ตัดคำที่บริบทถือ | `บริษัทฯ` ต้องเป็นประธานซ้ำแทบทุกประโยคสำคัญ ห้ามตัด · แต่ qualifier แบบ `ในมุมมองของบริษัทฯ` ยังตัดได้ (E ใช้ได้เป็นจุด ๆ) |
| ทำการ/มีการ = tell (งาน 2d) | **กลับทิศ**: คนเขียนเอง*เพิ่ม* `ทำการ+กริยา` `มีการ+นาม` `ดังนี้` `ดังกล่าว` เข้าไป — เป็น convention ของ register |
| H3 ตัด closer | ตัดเฉพาะ closer **อวยตัวเอง** · closer ที่เป็น fact ตรวจสอบได้ กับย่อหน้าสรุปท้าย section เป็น convention เก็บไว้ |
| H1 ไม่ใช่ X แต่ Y | ดู **function** ไม่ใช่ pattern: หางซ้ำหัว/เหน็บคู่แข่ง = ตัด · differentiation claim กับ ceremonial elevation (`ไม่ใช่เพียงการเลือกผู้ให้บริการ แต่คือการเลือกพันธมิตร…`) = วาทศิลป์ทางการแท้ เก็บ |
| em-dash = tell อันดับ 1 | em-dash แทบไม่ปรากฏ — ตัวเชื่อมประจำ register คือ **`·`** ใช้เชื่อมประโยคเต็มด้วย: เก็บใน label/bullet/ตาราง ตัดเฉพาะ `·` ที่เชื่อมประโยคใน prose (กฎ "· = label separator เท่านั้น" ของเดิมแคบไป) |
| jargon คงอังกฤษ | **เลือกทาง**: ศัพท์ที่มีคำไทยตรง → ไทย (`Locked`→`ห้ามเปลี่ยน`) หรือรูป "ไทยทางการ (English gloss)" · term of art คงอังกฤษ (Lump Sum, Go-live, Payroll) |

กฎที่**ยืนยันว่าใช้ได้ข้าม register** (โดนแก้แม้ในเอกสารทางการ): A4 ตัดหางที่ซ้ำ label/หัวข้อ ·
emoji ในเนื้อความ (`❌` ซ้ำคำว่าไม่ผ่าน) · ศัพท์ dev หลุด register (`Antipattern`) · overclaim
(`หายากในตลาด`, `ตลอดกาล`, intensifier `จริง`) · diplomatic reframe (ห้ามบอกว่าลูกค้า "มีปัญหา"
→ "ประเด็นที่องค์กรให้ความสำคัญ")

**tell ใหม่จาก corpus นี้** (เข้า tells-th ได้เลย, ที่มา corpus):
- **nominalization ลูกผสมไทย-อังกฤษ**: `ความ Stable นี้คือ Proof ว่า…`, `มี Combination ที่หายาก`,
  `จะ Propose replacement` — โดน rewrite ทุกจุดใน corpus
- **สัญลักษณ์แทนคำในเอกสารทางการ**: `20+`, `✓`, `❌`, `>30%` ใน prose (ไม่ใช่ตาราง) → เขียนเป็นคำ
- **คำประดิษฐ์เอง vs ศัพท์มาตรฐาน**: `ตัววัดผล`→`ตัวชี้วัด` — AI ชอบ coin คำเลียนศัพท์จริง

### 7b. register `spoken-pitch` — บทพูด/สคริปต์นำเสนอ

- `ครับ/ค่ะ` ท้ายประโยค + กริยาถ่อมตัว `ขอ…` (ขอเล่า/ขอเน้น/ขอ commit) = โครงบังคับ ไม่ใช่ filler
- คำขอบคุณเปิด-ปิด = ข้อบังคับ (กฎ G ปิดใน register นี้)
- tricolon = message discipline ที่ตั้งใจ (H4 ปิด) · การซ้ำ frame ข้ามสไลด์ = ตั้งใจ ถ้าหางแบก
  ข้อความขาย / = filler ถ้าหางแค่ปฏิเสธซ้ำหัว
- ที่ยังใช้ได้: D ข้อสรุปขึ้นก่อน (Q&A ที่ดีเปิดด้วย verdict) · H8 ห้ามตอบ `เกือบครบ` ·
  สูตรคืนอำนาจตัดสินใจให้ลูกค้าท้ายคำตอบเชิงเปรียบเทียบ = มารยาทบังคับ ไม่ใช่ hedge
- em-dash บนสไลด์ (`**คีย์เวิร์ด** — คำขยาย`) เป็น layout device — ตัวแก้ที่ถูกคือ typography
  (colon/ขึ้นบรรทัด) ไม่ใช่กฎ prose

### 7c. ตารางรวม กฎ × register (โครงตั้งต้นของ registers.md — เติมให้ครบจาก corpus)

register มี 4 ค่า: `ui` (สตริงในจอ) · `prose` (บทความ/docs/commit) · `formal` (เอกสารยื่น
ลูกค้า/ประมูล) · `spoken` (บทพูด/สคริปต์นำเสนอ) — ค่าในตาราง: ✓ ใช้ · ± ดูเงื่อนไข ·
⇄ กลับทิศ · ✗ ปิด

| กลุ่มกฎ | ui | prose | formal | spoken |
|---|---|---|---|---|
| A em-dash 4 ท่า | ✓ hard | ✓ | ✗ แทบไม่เจอ — ดูกฎ `·` แทน (เก็บใน label ตัดที่เชื่อมประโยคใน prose) | ✗ บนสไลด์เป็น layout device แก้ด้วย typography |
| B/C empty state, placeholder | ✓ | – | – | – |
| D ข้อสรุปขึ้นก่อน | ✓ | ✓ | ✓ | ✓ Q&A เปิดด้วย verdict |
| E คำที่บริบทถือ | ✓ | ✓ | ± qualifier ตัดได้ แต่ `บริษัทฯ` ประธานซ้ำ = ห้ามตัด | ± |
| G คำหยอด/ขอบคุณ | ✓ | ✓ | ± สูตรขอบคุณพิธีการ = เก็บ | ✗ ขอบคุณเปิด-ปิดเป็นข้อบังคับ |
| H1 ไม่ใช่ X แต่ Y | ✓ | ✓ | ± ดู function: หางซ้ำหัว=ตัด, ceremonial=เก็บ | ± ดู function |
| H3 closer | ✓ | ✓ | ± เฉพาะ closer อวยตัวเอง; สรุปท้าย section=เก็บ | ✗ peroration ต้องมี |
| H4 tricolon | ✓ soft | ✓ soft | ± | ✗ เป็น message discipline |
| H8 hedging | ✓ | ✓ | ⇄ ต้อง**เพิ่ม** hedge ลดคำเคลม | ✓ ห้ามตอบ "เกือบครบ" |
| K สำนวนแปล (ทำการ/มีการ/ดังนี้) | ✓ | ✓ | ⇄ เป็น convention คนเขียนเติมเอง | ± |
| L ตารางคำ AI | ✓ | ✓ | ✓ | ✓ |
| heuristic "สั้นกว่า = คนกว่า" | ✓ | ✓ | ⇄ ขยาย telegraphic เป็นประโยคทางการเต็ม | ⇄ bullet → ประโยคพูดเต็ม+ครับ |
| A4 หางซ้ำหัว/label · emoji ในเนื้อความ · overclaim · diplomatic reframe | ✓ | ✓ | ✓ (ยืนยันจาก corpus) | ✓ |

**การเดา register (default — user บอกมาเมื่อไหร่ให้ชนะเสมอ):** string ใน component/i18n
→ `ui` · md/docs/commit/บทความ → `prose` · เอกสารยื่นลูกค้า/ประมูล/สัญญา → `formal` ·
สคริปต์พูด/demo/Q&A → `spoken` · ก้ำกึ่ง → ถาม (mode `ask`)

### 7d. ผลกระทบต่องานอื่น

- **งาน 3 (false-positives):** เพิ่ม entry แบบ register-conditional จากตาราง 7a (ดังนี้/บริษัทฯ/
  ทำการ ใน formal · ครับ+ขอ ใน spoken · `·` เชื่อมประโยคใน formal-proposal)
- **งาน 5 (evals):** เพิ่มเคส register ละ ≥2 (เคส formal ที่คำตอบถูกคือ "ขยาย ไม่ใช่ตัด")
- **template `repos.md`:** เพิ่มช่อง **คำต้องห้าม/คำบังคับรายโปรเจกต์** — corpus มีตัวอย่างจริง:
  spec ของโปรเจกต์กำหนดคำเรียกงานอ้างอิงที่ห้ามใช้ด้วยเหตุผล NDA พร้อม checklist บังคับ —
  กลไกเดียวกับที่ klao ควรมีให้ทุก repo
- SKILL.md §1 (ขอบเขต): เพิ่มคำถามที่สาม — **register ไหน** (ui / prose / formal-proposal /
  spoken-pitch) แล้วอ่าน registers.md เมื่อไม่ใช่สองอันแรก

**Acceptance งาน 7:** registers.md มีตาราง กฎ×register (ใช้/กลับทิศ/ปิด) ครบทุกกฎหลัก ·
ตัวอย่างทุกอันใน registers.md เป็นแบบ genericize (ไม่มีชื่อลูกค้า/โปรเจกต์/ตัวเลขสัญญา —
เช็คด้วยสายตาก่อน commit เพราะ corpus ดิบมีข้อมูลลูกค้า) · เคส eval ฝั่ง formal ผ่าน check.sh

## ลำดับ commit แนะนำ

1. `feat: rule IDs and severity on every tell` (งาน 1)
2. `feat: the Thai tells the corpus was missing` (งาน 2 — commit เดียว หรือแยก 2a/2b-f ก็ได้)
3. `feat: false positives get their own file, with a postmortem log` (งาน 3)
4. `feat: four output modes and a preservation contract` (งาน 4)
5. `feat: eval cases and a grep-only audit script` (งาน 5)
6. `feat: registers — the rules that flip in formal and spoken Thai` (งาน 7 — ทำหลังงาน 3/5
   เพราะเติม false-positives กับ eval cases)
7. `chore: changelog, upstream credits, readme` (งาน 6)

ทุก commit: subject บอกว่าของมันทำอะไรตอนนี้ (voice ตาม tells-en ท้ายไฟล์) · push ได้เลย
repo public อยู่แล้ว

## Definition of done รวม

- [ ] ทุกกฎ (เก่า+ใหม่) มี ID · ระดับ · ที่มา **· ระบุ register ที่ใช้/กลับทิศ/ปิด**
- [ ] `bash scripts/check.sh` เขียว
- [ ] SKILL.md ยัง ≤ ~130 บรรทัด (ตอนนี้ ~110)
- [ ] `grep -rn "team\|mu4\|seedgrit/team" --include='*.md' .` (นอก repos.local.md) = ว่าง
- [ ] เปิดอ่านด้วยสายตาคนนอก: ไม่มีบรรทัดไหนตอบไม่ได้ว่า "มาจากไหน ทำไมถึงเชื่อ"
