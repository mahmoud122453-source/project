# TEACHING_GUIDE

دليل تدريس مبني على الملف الحقيقي `app.py` فقط. المؤلف الأصلي: [BaseMax/TkinterCalculator](https://github.com/BaseMax/TkinterCalculator) — رخصة GPL-3.0.

## Project Goal

تعليم الطلاب بناء تطبيق GUI بسيط بلغة Python: نافذة، أزرار، حالة داخل كائن، أحداث فأرة ولوحة مفاتيح، ومنطق آلة حاسبة يعتمد على سلسلتين نصيتين و`eval`.

## Student Level

مبتدئ إلى متوسط في Python. يُفضَّل أن يكون الطالب قد كتب دوالًا وشروطًا قبل هذه الوحدة. الـ Class يُدرَّس من هذا الملف، وليس كشرط مسبق ثقيل.

## Prerequisites

قبل فتح الكود:

1. تشغيل ملف `.py` من الطرفية
2. متغيرات وأنواع: `str`, `int`, `dict`, `tuple`
3. الدوال و`return`
4. الحلقات `for`
5. `if __name__ == "__main__"` بشكل سطحي
6. فكرة أن البرنامج ينتظر أحداث المستخدم (يُشرح هنا عمليًا)

غير مطلوب مسبقًا: Tkinter، `lambda`، `bind`، `eval`، تصميم OOP كامل.

## Learning Outcomes

بعد الوحدة يستطيع الطالب أن:

- ينشئ نافذة `tk.Tk` ويضبط العنوان والحجم
- يستخدم `Frame` و`Label` و`Button`
- يفرّق بين `pack` و`grid` كما هما مستخدمان في هذا الملف
- يربط زرًا بدالة عبر `command`
- يشرح لماذا الآلة الحاسبة تحتاج حالة (`total_expression`, `current_expression`)
- يتتبع مسار: زر → callback → تغيير الحالة → `config` على Label
- يفهم أن الحساب هنا يتم بـ `eval` على نص
- يفرّق بين حدث الزر وحدث لوحة المفاتيح (`bind`)

## Architecture

ملف واحد، كلاس واحد:

```text
app.py
  ثوابت ألوان وخطوط
  class TkinterCalculator
    __init__: نافذة + حالة + بناء الواجهة + bind_keys
    run: mainloop
    create_*: بناء Widgets
    add_to_expression / append_operator / clear / square / sqrt / evaluate
    update_label / update_total_label
  if __name__: إنشاء كائن ثم run()
```

لا يوجد MVC منفصل، لا قاعدة بيانات، لا ملفات إعداد، لا `Entry`، لا `StringVar`.

## Execution Flow

1. Python يحمّل `app.py`
2. `import tkinter as tk`
3. تعريف الثوابت ثم الكلاس
4. عند التشغيل المباشر: `tkinter_calculator = TkinterCalculator()`
5. `__init__` ينشئ `tk.Tk()`، يضبط `geometry("375x667")`، `resizable(0, 0)`، `title("Calculator")`
6. تهيئة `total_expression = ""` و`current_expression = ""`
7. إنشاء إطار العرض والـ Labels
8. تعبئة قواميس `digits` و`operations`
9. إنشاء إطار الأزرار وضبط `rowconfigure` / `columnconfigure`
10. إنشاء أزرار الأرقام والعوامل والأزرار الخاصة
11. `bind_keys()`
12. `run()` → `self.window.mainloop()`
13. البرنامج يتوقف في الحلقة حتى يغلق المستخدم النافذة

## Teaching Order

ترتيب يعتمد على تبعية المفاهيم داخل `app.py` (ليس ترتيب الأسطر الأبجدي):

1. فكرة المشروع وتشغيل `python app.py`
2. الاستيراد والثوابت (ألوان، خطوط)
3. نقطة الدخول `if __name__` والكائن
4. النافذة الجذرية في `__init__`
5. الحالة: السلسلتان
6. `Frame` + `pack` للشاشة والأزرار
7. `Label` وتحديث النص بـ `config`
8. `Button` + `grid`
9. `command` والدوال `add_to_expression` / `append_operator`
10. `lambda x=digit` (لماذا القيمة الافتراضية؟)
11. `evaluate` و`eval` و`try/except`
12. `clear` / `square` / `sqrt`
13. `bind_keys` و`Return`
14. مخاطر `eval` وتحسينات محتملة (بدون إعادة بناء)

## Files

| File | Role in teaching |
|------|------------------|
| `README.md` | مصدر المشروع الأصلي وكيفية التشغيل |
| `RUN_GUIDE.md` | تشغيل الصف |
| `app.py` | كل الكود القابل للتدريس |
| `PROJECT_MAP.md` | خريطة للمدرس |
| `FILE_TEACHING_ORDER.md` | ترتيب الملفات للشرح |
| `LICENSE` | GPL-3.0 — يُذكر ولا يُدرَّس سطرًا سطرًا |
| `demo.png` | صورة واجهة |
| `.gitignore` | لا يُدرَّس في البداية |

## Code Blocks

انظر الجدول التفصيلي في هذا الدليل (القسم التالي) و`PROJECT_MAP.md`.

### Block teaching map

| Block ID | File | Class / Function | Code Section | Purpose | Concepts | Prerequisites | Difficulty | Teaching Priority |
|----------|------|------------------|--------------|---------|----------|---------------|------------|-------------------|
| B01 | app.py | module | السطور 1–6 | هوية الملف واستيراد Tkinter | import, comments | تشغيل Python | 1 | 1 |
| B02 | app.py | module constants | WHITE … SMALL_FONT_STYLE | ثوابت مظهر | tuples, strings, naming | variables | 1 | 2 |
| B03 | app.py | TkinterCalculator.__init__ | window setup | إنشاء النافذة | Tk, geometry, title, resizable | B01 | 1 | 3 |
| B04 | app.py | __init__ | total/current_expression | حالة الآلة الحاسبة | attributes, str | B03 | 1 | 4 |
| B05 | app.py | create_display_frame / create_display_labels | Labels | الشاشتان | Frame, Label, pack, anchor | B03 | 2 | 5 |
| B06 | app.py | digits, operations | قواميس التخطيط والرموز | ربط القيمة الداخلية بالعرض | dict, unicode | loops intro | 2 | 6 |
| B07 | app.py | create_buttons_frame + row/columnconfigure | شبكة الأزرار | grid weights | Frame, pack, grid config | B05 | 2 | 7 |
| B08 | app.py | create_digit_buttons | أزرار 0–9 و`.` | command + lambda | Button, grid, lambda default arg | B06 B07 | 2 | 8 |
| B09 | app.py | create_operator_buttons | + − × ÷ | نفس النمط مع رموز العرض | for, unicode | B08 | 2 | 9 |
| B10 | app.py | create_special_buttons وcreate_* | C, =, x², √x | أزرار تستدعي methods بدون lambda | command=self.method | B08 | 2 | 10 |
| B11 | app.py | add_to_expression | إدخال | تحديث الحالة ثم الشاشة | concatenation | B04 | 1 | 11 |
| B12 | app.py | append_operator | نقل الرقم الحالي إلى التعبير الكلي | تدفق الحالة | string state machine | B11 | 2 | 12 |
| B13 | app.py | update_label / update_total_label | عرض | استبدال * و/ برموز، قص 11 حرفًا | replace, slice, config | B05 B12 | 2 | 13 |
| B14 | app.py | evaluate | الحساب | eval, try/except/finally | errors | B12 | 3 | 14 |
| B15 | app.py | clear, square, sqrt | مسح ودوال علمية صغيرة | eval على تعبير مبني | try/except | B14 | 2 | 15 |
| B16 | app.py | bind_keys | لوحة المفاتيح | bind, Return, lambda event | events | B08 B14 | 3 | 16 |
| B17 | app.py | run + __main__ | تشغيل الحلقة | mainloop, object | B03 | 1 | 17 |

## Concepts

انظر قسم Concept Inventory أدناه.

## PYTHON BASICS (موجود فعليًا)

- Variables / attributes
- Strings (تعبيرات، رموز Unicode)
- Numbers (مفاتيح dict للأرقام؛ الحساب عبر eval)
- Dictionaries (`digits`, `operations`)
- Tuples (خطوط، إحداثيات الشبكة)
- Conditions (`try/except` وليس `if` للحساب؛ يوجد `if __name__`)
- Loops (`for` على digits, operations, range)
- Functions / methods
- Parameters (`value`, `operator`, `event`, default `x=digit`)
- Return (من دوال `create_*`)
- Imports (`tkinter as tk`)
- f-strings في `square` و`sqrt` و`update_total_label`
- Slicing `[:11]`

غير موجود بشكل جوهري: lists كبنية حالة، Boolean كحقول حالة، `while` ظاهر (mainloop مخفي داخل Tk).

## OOP (موجود)

- Class `TkinterCalculator`
- `__init__`
- `self`
- Attributes: window, expressions, frames, labels, digits, operations
- Methods لكل البناء والمنطق
- Object: `tkinter_calculator = TkinterCalculator()`

لماذا Class؟ لتجميع حالة الآلة الحاسبة والواجهة معًا في كائن واحد بدل متغيرات عامة. الكائن يخزّن النصوص الحالية والمراجع إلى Widgets.

## TKINTER (المستخدم فعليًا فقط)

- `tk.Tk`
- `tk.Frame`
- `tk.Label`
- `tk.Button`
- `pack` (إطارات العرض والأزرار، والـ Labels)
- `grid` (الأزرار)
- `bind`
- `mainloop`
- `geometry`, `title`, `resizable`
- `rowconfigure`, `columnconfigure`
- `config` لتحديث النص
- `sticky=tk.NSEW`, `anchor=tk.E`

غير موجود: `Entry`, `StringVar`, `place`, `Canvas`, `Menu`.

## EVENT-DRIVEN (الموجود فعليًا)

- `command=` على Button
- callbacks: methods الكائن
- `lambda x=digit: ...` و`lambda x=operator: ...`
- `bind` مع `lambda event: ...` و`lambda event, digit=key: ...`
- لا يوجد `functools.partial`

مسار حدث الزر:

```text
Button
  → command
  → method (مثل add_to_expression)
  → تغيير self.current_expression / self.total_expression
  → update_label / update_total_label
  → Label.config(text=...)
```

## CALCULATOR

- تعبيران نصيان وليس رموزًا منفصلة
- عوامل تُخزَّن كـ `+ - * /` وتُعرض كرموز
- التقييم بـ `eval` (أولوية بايثون وليست بالضرورة يسار→يمين الآلة الحاسبة المدرسية)
- خطأ الحساب في `evaluate` يصبح النص `"Error"`

## Exercises

1. غيّر `title` و`geometry` ولاحظ الفرق.
2. غيّر لون `LIGHT_BLUE` لزر `=`.
3. أضف `print` داخل `add_to_expression` وتتبع الضغطات.
4. اشرح لماذا `1+2×3` يعطي `7`.
5. ارسم على الورق قيم `current_expression` و`total_expression` بعد كل خطوة في `2 + 3 =`.

## Common Mistakes

- الخلط بين الرمز الظاهر `×` والقيمة `*` التي تُمرَّر إلى `eval`
- نسيان أن `lambda x=digit` بدون قيمة افتراضية يلتقط آخر رقم في الحلقة
- انتظار `Entry` بينما العرض `Label`
- اعتبار `eval` آلة حاسبة «آمنة»
- البحث عن Backspace وهو غير موجود

## Challenges

- لماذا العمود `0` في الشبكة غير مستخدم؟ (`columnconfigure` يبدأ من 1، والأزرار على أعمدة 1–4)
- ماذا يحدث بعد ظهور `Error` إذا ضغط الطالب رقمًا؟ (التسلسل النصي يضيف فوق كلمة Error)
- لماذا الشاشة السفلى تعرض 11 حرفًا فقط؟

## Homework

1. اكتب تسلسل الحالة لـ `12 + 8 =`.
2. عدّد كل Widget في `app.py` مع السطر التقريبي.
3. قارن حدث الزر `=` مع حدث `<Return>`.

## Final Challenge

بدون إعادة بناء المشروع: اقترح على الورق (لا تنفّذ إلزاميًا) كيف تضيف Backspace باستخدام `bind("<BackSpace>", ...)` وما الذي ستعدّله في `current_expression`. الهدف فهم الحدث وليس تسليم ميزة جديدة.

## LEVEL 1 — Beginner

نافذة، Frame، Label، Button، pack/grid، متغيرات الحالة، `add_to_expression`، `clear`، `run`/`mainloop`.

ما يجب فهمه الآن: الواجهة تستدعي دوالًا تغيّر نصًا ثم تعيد رسم Label.

## LEVEL 2 — Intermediate

قواميس التخطيط، `lambda` داخل حلقة، `append_operator`، تحديث الرموز، `evaluate` + `try/except`.

## LEVEL 3 — Advanced / postpone

- مخاطر `eval` والأمان
- `bind` وتوقيع `event`
- `finally` في `evaluate`
- قص العرض `[:11]`
- أولوية عوامل Python مقابل آلة حاسبة يسار-إلى-يمين
- PyInstaller المذكور في README الأصلي (خارج منهج GUI الأساسي)
- LICENSE / GPL بالكامل

Black box مقبول في الأسبوع الأول: التنفيذ الداخلي لـ `mainloop`، ومحرّك Tk.

## WHAT TO POSTPONE

| What is it? | Why advanced? | Prerequisite? | When to teach? |
|-------------|---------------|---------------|----------------|
| `eval` security | أمان وإدخال خبيث | فهم eval كآلة حاسبة | بعد عمل = بنجاح |
| lambda default arguments | إغلاق الحلقات | loops + callbacks | عند شرح أزرار الأرقام |
| Unicode escapes `\u00F7` | تمثيل الرموز | strings | عند رموز ÷ × √ |
| `bind` keyboard | نموذج أحداث ثانٍ | command أولاً | درس لاحق |
| PyInstaller | توزيع تطبيقات | المشروع يعمل | اختياري |
| `.gitignore` | Git وليس Tkinter | git | إن وُجد مسار Git |
| `resizable(0,0)` تفاصيل إدارة النوافذ | سلوك مدير النوافذ | نافذة تعمل | سريعًا مع geometry |
