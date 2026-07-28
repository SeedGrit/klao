# กฎเฉพาะราย repo — เขียนเองใน `repos.local.md`

กฎกลางของ skill ใช้ได้ทุก repo แต่แต่ละ repo มีของเฉพาะตัว: ไฟล์ไหนมีคำให้เกลา คำไหนห้ามแตะ
gate อะไรต้องเขียว ของพวกนี้**ไม่ควรอยู่ใน repo สาธารณะ** เพราะมักพันกับ business rule และ
โครงระบบภายใน

วิธีใช้: สร้าง `references/repos.local.md` (ไฟล์นี้ถูก gitignore ไว้แล้ว) แล้วเขียนหัวข้อละ repo
ตามโครงนี้ — skill จะอ่านไฟล์นั้นก่อนลงมือทุกครั้งถ้ามี

## โครงต่อ repo (3 ส่วน)

```markdown
## <ชื่อ repo> — `<path>` (<โดเมน/คำอธิบายสั้น>)

**ที่มีคำให้เกลา**

| ที่ | คืออะไร |
|---|---|
| `src/components/**/*.tsx` | UI copy ไทย |
| `src/lib/notify.ts` | ข้อความ notification |
| `*.md` | prose อังกฤษ ใช้ tells-en.md |

**gate**

​```sh
pnpm typecheck && pnpm lint && pnpm test
grep -rn "—\|–" src | grep -vE ':[0-9]+: *(//|\*|/\*)' | grep '[ก-๙]'
​```

**ระวังเฉพาะ repo นี้**

- คำที่อ้างถึงปุ่มจริง (`<ชื่อปุ่ม>`) ห้ามเปลี่ยน ไม่งั้นข้อความกับปุ่มเรียกของเดียวกันคนละชื่อ
- นโยบายที่เป็นกฎจริง (เช่น หน้าต่างแก้ไข N วัน) ย่อได้ แต่ห้ามย่อจนตัวเลขหรือเงื่อนไขหาย
- ข้อความใน `aria-label` เกลาได้ แต่ต้องยังบอก screen reader ครบว่าแถวนั้นคืออะไร
```

## เก็บ baseline กัน regression

หลังเกลาครบรอบใหญ่ ให้จดผล grep ล่าสุดไว้ในหัวข้อของ repo นั้น เช่น "กรองแล้วเหลือ N จุด
ล้วนเป็น en-dash ในช่วง" — รอบหน้าถ้าเลขโตกว่า baseline = มีคำใหม่หลุดเข้ามา

## เนื้อหาชุดใหม่ที่ AI ร่าง → ล็อกด้วย test

```ts
it('ไม่มี em-dash/en-dash ใน field เนื้อหา', () => {
  for (const key of AUTHORED_KEYS) {
    const c = contentFor(key)
    for (const s of proseFieldsOf(c)) expect(/[—–]/.test(s), `em-dash ที่ ${key}`).toBe(false)
  }
})
```
