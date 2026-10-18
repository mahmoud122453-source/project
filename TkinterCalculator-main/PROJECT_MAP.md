# PROJECT_MAP

خريطة المشروع كما هو في الملفات الحقيقية، وليس كما يُفترض أن تكون آلة حاسبة عامة.

**المصدر:** [BaseMax/TkinterCalculator](https://github.com/BaseMax/TkinterCalculator)  
**الرخصة:** GNU GPL v3 (`LICENSE`)  
**كود التشغيل:** `app.py`

## Project Purpose

آلة حاسبة GUI بلغة Python/Tkinter: إدخال أرقام وعوامل، تقييم التعبير بـ `eval`، دوال تربيع وجذر، مسح، ودعم جزئي للوحة المفاتيح.

## Folder Structure

المشروع مسطّح (لا حزم Python فرعية):

```text
TkinterCalculator-main/
├── app.py                 # التطبيق بالكامل
├── README.md              # توثيق المؤلف الأصلي
├── LICENSE                # GPL-3.0
├── .gitignore
├── demo.png               # لقطة واجهة مرفقة مع المشروع
├── RUN_GUIDE.md           # دليل التشغيل (تعليمي)
├── TEACHING_GUIDE.md      # دليل التدريس
├── FILE_TEACHING_ORDER.md
└── PROJECT_MAP.md         # هذا الملف
```

لا يوجد: `requirements.txt`, `setup.py`, مجلد `src/`, اختبارات pytest أصلية, ملفات تكوين tk.

## File Structure

| File | Role |
|------|------|
| app.py | كلاس `TkinterCalculator` + نقطة الدخول |
| README.md | تشغيل، ملاحظة Tkinter المدمج، PyInstaller اختياري |
| LICENSE | نص GPL-3.0 |
| demo.png | صورة الواجهة |
| .gitignore | قالب Python عام (venv, __pycache__, …) |

## GUI Architecture

```text
tk.Tk  (self.window)
  title = "Calculator"
  geometry = 375x667
  resizable = False, False
  │
  ├── Frame  self.display_frame   height=221, bg LIGHT_GRAY, pack(expand, fill both)
  │     ├── Label self.total_label     نص total_expression، خط صغير، anchor E
  │     └── Label self.label           نص current_expression، خط كبير، يُقص إلى 11 حرفًا عند العرض
  │
  └── Frame  self.buttons_frame   pack(expand, fill both)
        grid: صفوف 0–4، أعمدة 1–4 (العمود 0 غير مستخدم)
```

تخطيط الأزرار كما يبنيه الكود:

```text
row 0:  [C]   [x²]  [√x]  [÷]
row 1:  [7]   [8]   [9]   [×]
row 2:  [4]   [5]   [6]   [-]
row 3:  [1]   [2]   [3]   [+]
row 4:  [.]   [0]   [    =    ]   ← يساوي column 3–4 (columnspan=2)
```

ملاحظة: لا يوجد زر في `(4,4)` منفصل لأن `=` يمتد على عمودين.

## Widgets (كلها من الكود)

| Name | Widget | Purpose | Where created | How configured | How connected |
|------|--------|---------|---------------|----------------|---------------|
| self.window | Tk | النافذة الجذر | `__init__` | geometry, resizable, title | bind_keys, mainloop |
| self.display_frame | Frame | حاوية الشاشة | `create_display_frame` | height 221, bg, pack | يحوي Labels |
| self.total_label | Label | التعبير الكامل | `create_display_labels` | SMALL_FONT, LIGHT_GRAY, pack | `update_total_label` |
| self.label | Label | المدخل/النتيجة | `create_display_labels` | LARGE_FONT, pack | `update_label` |
| self.buttons_frame | Frame | شبكة الأزرار | `create_buttons_frame` | pack | parent لكل Button |
| (محلية) button | Button | أرقام ونقطة | `create_digit_buttons` | WHITE, DIGITS_FONT, grid | lambda → add_to_expression |
| (محلية) button | Button | عوامل | `create_operator_buttons` | OFF_WHITE, grid col 4 | lambda → append_operator |
| (محلية) button | Button | C | `create_clear_button` | grid (0,1) | command=self.clear |
| (محلية) button | Button | x² | `create_square_button` | grid (0,2) | command=self.square |
| (محلية) button | Button | √x | `create_sqrt_button` | grid (0,3) | command=self.sqrt |
| (محلية) button | Button | = | `create_equals_button` | LIGHT_BLUE, colspan 2 | command=self.evaluate |

لا توجد أسماء attributes للأزرار؛ تُنشأ وتُربط ثم تُترك للمتصفح الهندسي.

## Execution Flow

```text
python app.py
  → if __name__ == "__main__"
  → TkinterCalculator()
  → __init__ يبني الواجهة ويربط المفاتيح
  → run()
  → window.mainloop()
  → انتظار أحداث حتى إغلاق النافذة
```

## Event Flow

```text
ضغط زر رقم
  command=lambda x=digit: self.add_to_expression(x)
  current_expression += str(value)
  update_label()

ضغط عامل
  command=lambda x=operator: self.append_operator(x)
  current_expression += operator
  total_expression += current_expression
  current_expression = ""
  update_total_label(); update_label()

ضغط =
  evaluate()
  total_expression += current_expression
  try: current_expression = str(eval(total_expression)); total_expression = ""
  except: current_expression = "Error"
  finally: update_label()

مفتاح رقم / نقطة / عامل
  bind(str(key), lambda event, ...: نفس الدوال أعلاه)

Enter / Return
  bind("<Return>", lambda event: self.evaluate())
```

Backspace وEscape: غير مربوطين.

## Data Flow

```text
مدخل المستخدم (زر أو مفتاح)
  → تعديل str: current_expression و/أو total_expression
  → (عند = أو x² أو √x) eval(...) → str نتيجة أو "Error"
  → Label.config(text=...)
```

العرض العلوي يستبدل `*` و`/` برموز `×` و`÷` عند التحديث فقط؛ التخزين الداخلي يبقى ASCII للعمليات.

## Classes

### TkinterCalculator

- `__init__(self)`: بناء كل شيء
- لا وراثة مخصصة (ضمنيًا `object`)

## Methods

| Method | Role |
|--------|------|
| run | mainloop |
| create_display_frame | إطار الشاشة |
| create_display_labels | الـ Labels وإرجاعهما |
| create_buttons_frame | إطار الأزرار |
| create_digit_buttons | أزرار digits |
| create_operator_buttons | أزرار operations |
| create_special_buttons | يستدعي clear/equals/square/sqrt constructors |
| create_clear_button | زر C |
| create_equals_button | زر = |
| create_square_button | زر x² |
| create_sqrt_button | زر √x |
| add_to_expression | إلحاق رقم/نقطة |
| append_operator | إلحاق عامل ونقل للتعبير الكلي |
| bind_keys | لوحة المفاتيح |
| clear | تفريغ الحالة والشاشات |
| square | تربيع القيمة الحالية عبر eval |
| sqrt | جذر عبر eval |
| update_total_label | عرض التعبير الكلي بالرموز |
| update_label | عرض الحالي مقصوصًا إلى 11 |

لا توجد دوال على مستوى الوحدة غير مسار `__main__`.

## Functions

لا functions حرة خارج الكلاس. نقطة الدخول كائن ثم `run()`.

## Important Variables / State

| Name | Type | Initial | Purpose | Changed in | Read in |
|------|------|---------|---------|------------|---------|
| WHITE, OFF_WHITE, LABEL_COLOR, LIGHT_BLUE, LIGHT_GRAY | str | hex constants | ألوان | لا | إنشاء Widgets |
| DEFAULT_FONT_STYLE, DIGITS_FONT_STYLE, LARGE_FONT_STYLE, SMALL_FONT_STYLE | tuple | (Arial, size, …) | خطوط | لا | Widgets |
| self.window | Tk | Tk() | النافذة | __init__ | run, bind, frames |
| self.total_expression | str | `""` | التعبير المتراكم للتقييم | append_operator, evaluate, clear | evaluate, update_total_label, labels init |
| self.current_expression | str | `""` | الرقم/القطعة الحالية أو النتيجة أو `"Error"` | add_to_expression, append_operator, evaluate, clear, square, sqrt | معظم المنطق وupdate_label |
| self.display_frame | Frame | create_display_frame() | الشاشة | __init__ | labels parent |
| self.total_label | Label | create_display_labels() | العرض العلوي | update_total_label | — |
| self.label | Label | create_display_labels() | العرض السفلي | update_label | — |
| self.digits | dict | int/str → (row,col) | تخطيط الأرقام والنقطة | __init__ فقط | create_digit_buttons, bind_keys |
| self.operations | dict | op str → رمز عرض | عوامل | __init__ فقط | create_operator_buttons, bind_keys, update_total_label |
| self.buttons_frame | Frame | create_buttons_frame() | الأزرار | __init__ | grid parents |

لا توجد متغيرات باسم `result` أو `operation` منفصلة؛ العامل جزء من السلاسل.

## Calculation Logic

- الجمع/الطرح/الضرب/القسمة: تُسلسل في `total_expression` ثم `eval`
- الترتيب: أولوية Python (`*` `/` قبل `+` `-`)
- العشري: حرف `'.'` في `digits`
- السالب: عامل `-`؛ لا زر تغيير إشارة؛ `0-5` أو `-` ثم `5` ثم `=` يعملان عبر eval
- الجذر/التربيع: `eval(f"{current}**2")` و`eval(f"{current}**0.5")`
- مخاطر eval: ينفّذ تعبير Python؛ مدخل غير مراقب يمكن أن يستدعي دوال إن وُسّع الربط لاحقًا؛ هنا الأزرار والربط يقيّدان المفاتيح نسبيًا لكن النموذج غير آمن كمبدأ

## Error Handling

| Case | Behavior in code |
|------|------------------|
| Division by zero in evaluate | except → `"Error"` |
| Invalid expression in evaluate | except → `"Error"` |
| Empty evaluate (`eval("")`) | except → `"Error"` |
| Empty/malformed square or sqrt | بعد الإصلاح الضروري: `"Error"` (سابقًا SyntaxError يُسقط التطبيق) |
| Unexpected keys | غير مربوطة؛ تُتجاهل |
| After `"Error"` + digit | يُلحق النص (مثل `Error7`) — تحسين محتمل غير مُنفَّذ |

## Keyboard Events

موجود في `bind_keys`:

- `<Return>` → `evaluate`
- كل مفتاح في `digits` (0–9 و`.`) → `add_to_expression`
- كل مفتاح في `operations` (`/ * - +`) → `append_operator`

غير موجود: Backspace، Escape، مفتاح `=`.

## Dependencies

```text
Python 3
  └── tkinter (stdlib / Tcl-Tk bundle)
```

لا pip packages للتشغيل.

## Code Dependency Map

```text
app.py
  └── class TkinterCalculator
        ├── __init__
        │     ├── create_display_frame → Frame
        │     ├── create_display_labels → Label, Label
        │     ├── create_buttons_frame → Frame
        │     ├── create_digit_buttons → Button → add_to_expression
        │     ├── create_operator_buttons → Button → append_operator
        │     ├── create_special_buttons
        │     │     ├── clear / evaluate / square / sqrt
        │     └── bind_keys → same methods
        ├── add_to_expression / append_operator / clear / square / sqrt / evaluate
        │     └── update_label / update_total_label → Label.config
        └── run → mainloop
```

## POTENTIAL IMPROVEMENT (غير منفَّذ عمدًا)

- مسح حالة `"Error"` قبل إدخال جديد
- حماية أوسع بدل `eval` (AST)
- Backspace
- زر إشارة سالبة مخصص
- اختبارات آلية داخل المستودع
- تفريغ `total_expression` عند فشل `evaluate` (حاليًا يبقى النص عند الخطأ قبل finally)
