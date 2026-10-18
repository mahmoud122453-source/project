# FILE_TEACHING_ORDER

السؤال: ما الملفات التي يجب أن أعطيها للذكاء الاصطناعي (أو أشرحها للطلاب) بالترتيب حتى يُفهم المشروع؟

المصدر الوحيد للكود التنفيذي هو `app.py`. باقي الملفات توثيق أو ترخيص أو أصل المشروع. الترتيب التالي حسب تبعية المفاهيم، لا حسب الاسم.

---

## 1. README.md

1. File: `README.md`
2. Teaching Order: 1
3. Why now? يعرّف المشروع الأصلي، الأمر `python app.py`، وأن Tkinter مدمج. يحفظ حقوق المؤلف والفكرة المصدرية.
4. Concepts: تشغيل سكربت، مكتبات مدمجة، إشارة إلى `demo.png`
5. Prerequisites: لا شيء
6. What to explain: هذا تطبيق آلة حاسبة Tkinter من BaseMax؛ التشغيل بملف واحد؛ لا requirements
7. What to postpone: قسم PyInstaller بالكامل
8. Importance: عالية كمقدمة، منخفضة ككود

---

## 2. RUN_GUIDE.md

1. File: `RUN_GUIDE.md`
2. Teaching Order: 2
3. Why now? قبل قراءة الكود يجب أن يرى الطالب النافذة تعمل على جهازه.
4. Concepts: Python على Windows، `import tkinter`، أمر التشغيل المختبر
5. Prerequisites: README
6. What to explain: `python app.py`، التحقق من Tkinter، الاستخدام اليدوي للأزرار الموجودة
7. What to postpone: بناء exe
8. Importance: إلزامي لجلسة المعمل

---

## 3. demo.png

1. File: `demo.png`
2. Teaching Order: 3
3. Why now? صورة الواجهة الأصلية تساعد على تسمية الأزرار قبل الغوص في الكلاس.
4. Concepts: تخطيط الآلة الحاسبة (شاشة + شبكة أزرار)
5. Prerequisites: تشغيل أو على الأقل رؤية الصورة
6. What to explain: الشاشتان، صف `C x² √x ÷`، شبكة الأرقام، `=` العريض
7. What to postpone: أي زر غير ظاهر في الصورة/الكود
8. Importance: مساعدة بصرية

---

## 4. app.py (الكتل B01–B07: نافذة وواجهة)

1. File: `app.py` (جزء الواجهة)
2. Teaching Order: 4
3. Why now? بعد أن تعمل النافذة، يطابق الطالب ما رآه مع `Tk`, `Frame`, `Label`, `Button`.
4. Concepts: import، ثوابت، `__init__`، pack/grid، قواميس `digits`/`operations`
5. Prerequisites: تشغيل المشروع، متغيرات ودوال Python
6. What to explain: إنشاء النافذة، الإطارات، الشاشتان، شبكة الأزرار
7. What to postpone: `eval`, `bind_keys`, تفاصيل lambda في الحلقات إن لزم تأجيلها سطرًا واحدًا («هذه الدالة تُستدعى عند الضغط»)
8. Importance: MUST TEACH

---

## 5. app.py (الكتل B08–B13: أحداث وحالة)

1. File: `app.py` (المنطق الأساسي)
2. Teaching Order: 5
3. Why now? الأزرار بلا معنى حتى تُربط بالحالة.
4. Concepts: `command`, `lambda`, `add_to_expression`, `append_operator`, `update_*`
5. Prerequisites: جزء الواجهة
6. What to explain: السلسلتان، لماذا العامل يُنقل إلى `total_expression` ويفرغ الحالي
7. What to postpone: لوحة المفاتيح، الأمان
8. Importance: MUST TEACH — قلب المنهج

---

## 6. app.py (الكتل B14–B15: حساب وأخطاء)

1. File: `app.py` (`evaluate`, `clear`, `square`, `sqrt`)
2. Teaching Order: 6
3. Why now? يعتمد على اكتمال التعبير في `total_expression`.
4. Concepts: `eval`, `try/except/finally`, `"Error"`
5. Prerequisites: الحالة والتسلسل `2+3`
6. What to explain: يساوي يجمع النص ثم يقيمه؛ القسمة على صفر؛ أولوية العوامل
7. What to postpone: بدائل `eval` (tokenize، AST) — خارج المشروع
8. Importance: MUST TEACH مع تحذير أمني موجز

---

## 7. app.py (الكتلة B16: لوحة المفاتيح)

1. File: `app.py` (`bind_keys`)
2. Teaching Order: 7
3. Why now? نفس المنطق السابق مربوط بحدث مختلف. يثبّت فكرة Event-Driven.
4. Concepts: `bind`, `<Return>`, `lambda event`
5. Prerequisites: أزرار `command` تعمل
6. What to explain: الأرقام والعوامل وEnter فقط؛ لا Backspace ولا Escape
7. What to postpone: أحداث إضافية غير موجودة
8. Importance: SHOULD TEACH في درس ثانٍ

---

## 8. PROJECT_MAP.md ثم TEACHING_GUIDE.md

1. File: `PROJECT_MAP.md`, `TEACHING_GUIDE.md`
2. Teaching Order: 8
3. Why now? للمدرس أو للذكاء الاصطناعي كسياق شامل بعد الكود.
4. Concepts: خرائط التدفق، نواتج التعلم، تمارين
5. Prerequisites: قراءة `app.py`
6. What to explain: كيف تُقسَّم الحصص
7. What to postpone: إن كان الطالب مبتدئًا جدًا، يكتفي المدرس بهذه الملفات
8. Importance: SHOULD TEACH للمدرس / CATEGORY B للطالب المتقدم

---

## 9. LICENSE

1. File: `LICENSE`
2. Teaching Order: 9 (متأخر)
3. Why now? بعد استقرار الفهم التقني. المشروع GPL-3.0؛ يجب عدم حذف الحقوق.
4. Concepts: برمجيات حرة، ذكر المؤلف
5. Prerequisites: لا شيء تقني
6. What to explain: يمكن نسخ المشروع وتعليمه مع الإبقاء على الترخيص والتنويه
7. What to postpone: قراءة 17 قسمًا قانونيًا
8. Importance: CATEGORY D في البداية، ثم إشارة قصيرة

---

## 10. .gitignore

1. File: `.gitignore`
2. Teaching Order: لا يُدرَّس في البداية
3. Why now? لا علاقة له بسلوك الآلة الحاسبة
4. Concepts: Git
5. Prerequisites: Git
6. What to explain: لاحقًا إن دُرِّس Git
7. What to postpone: الحصة الأولى وكل حصص Tkinter
8. Importance: DO NOT TEACH INITIALLY

---

## CATEGORY SUMMARY

| File | Category | Reason | Concepts | Teaching Priority |
|------|----------|--------|----------|-------------------|
| app.py | A MUST TEACH | كل السلوك هنا | GUI, OOP, events, eval | 1 |
| README.md | B SHOULD TEACH | أصل التشغيل وحقوق المشروع | run command | 2 |
| RUN_GUIDE.md | A MUST TEACH (معمل) | تشغيل Windows/Tkinter | environment | 2 |
| demo.png | B SHOULD TEACH | مرجع بصري | layout | 3 |
| TEACHING_GUIDE.md | B SHOULD TEACH (مدرس) | خطة الحصص | pedagogy | 4 |
| PROJECT_MAP.md | B SHOULD TEACH (مدرس) | خريطة بنية | architecture | 4 |
| FILE_TEACHING_ORDER.md | C ADVANCED للمدرس | ميتا-ترتيب | curriculum | 5 |
| LICENSE | D initially | قانوني لا تشغيلي | GPL | 6 |
| .gitignore | D | أداة Git | git | 7 |

## الترتيب النهائي المختصر للذكاء الاصطناعي

أعطِ الملفات بهذا الترتيب في جلسة الشرح:

1. `README.md`
2. `RUN_GUIDE.md`
3. `demo.png`
4. `app.py` (واجهة)
5. `app.py` (حالة وأزرار)
6. `app.py` (evaluate / square / sqrt)
7. `app.py` (`bind_keys`)
8. `PROJECT_MAP.md` + `TEACHING_GUIDE.md` للمدرس

لا تبدأ بـ `LICENSE` أو `.gitignore`.
