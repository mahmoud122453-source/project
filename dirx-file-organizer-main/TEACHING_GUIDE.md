# TEACHING_GUIDE.md — DirX

مشروع التدريس: **DirX — File and Folder Handling Tools**  
المؤلف الأصلي للبرنامج: المستودع [thePolitician/dirx-file-organizer](https://github.com/thePolitician/dirx-file-organizer)

الهدف التعليمي ليس إعادة بناء المشروع، بل فهمه وتشغيله وتعليم مسارات الملفات وواجهة tkinter كما هي في الكود.

---

## هدف المشروع

أن يستطيع الطالب:

- تشغيل تطبيق tkinter متعدد التبويبات
- اختيار مجلد وقراءة قائمة الملفات
- تصنيف الملفات حسب الامتداد
- إنشاء مجلدات ونقل الملفات
- إعادة تسمية دفعة مع الحفاظ على الامتداد
- فهم حدود البرنامج (Undo في الذاكرة، أخطاء صامتة، Desktop الافتراضي)

---

## مستوى الطلاب

الأنسب: **متوسط مبتدئ إلى متوسط** (يعرف الدوال والقوائم والقواميس، ورأى tkinter مرة).

غير مناسب كأول برنامج بايثون على الإطلاق إذا لم يُقسَّم إلى Blocks.

---

## Prerequisites

يجب أن يعرفه الطالب قبل المشروع:

- تشغيل ملف `.py`
- متغيرات، نصوص، قوائم، قواميس
- `if` / `for`
- تعريف دالة و`return`
- `import`
- فكرة المسار (مجلد وملف)

موصى به وغير ظاهر بقوة في كل الملفات: أساسيات الكائنات (`self`، `__init__`). سيُتعلَّم أثناء `ttk.Frame`.

---

## Learning Outcomes

بعد المسار الكامل يستطيع الطالب أن يشرح من الكود:

1. كيف تبدأ النافذة من `dirx.py`
2. كيف تُحمَّل التبويبات من حزمة `Frames`
3. كيف يُقرأ مجلد بـ `os.listdir`
4. كيف يُؤخذ الامتداد بـ `os.path.splitext`
5. كيف تُنشأ مجلدات التصنيف وكيف يُنقل الملف
6. كيف يُركَّب الاسم الجديد في Batch Rename
7. كيف يُمنعoverwrite في Rename عبر `(i)`
8. لماذا Undo التنظيم يختفي بعد إغلاق البرنامج

---

## Architecture

انظر `PROJECT_MAP.md`. باختصار: كل تبويب Frame يضم الواجهة والمنطق معًا. لا توجد طبقة خدمات منفصلة.

---

## Execution Flow

```text
python dirx.py
  → set_dpi_awareness()
  → DirX() يبني Notebook
  → FileOrganizer يحمّل pickle ويضبط المسار على Desktop
  → mainloop() ينتظر الأحداث
  → زر Organize / Rename / Unpack يفتح Thread غالبًا
  → تغييرات على القرص ثم تحديث Status
```

---

## Teaching Order (حسب الاعتماد الحقيقي)

1. نظرة على README: الوحدات الخمس
2. مسارات Windows ومجلد TEST الآمن
3. `dirx.py` نقطة الدخول
4. حزمة `Frames`
5. `status.py`
6. `os` / `pathlib` عبر قراءة مجلد
7. الامتدادات و`splitext`
8. `organize_by_ext` ثم `organize_by_type`
9. إنشاء المجلدات والنقل (`os.makedirs` / `Path.mkdir` / `shutil.move` / `Path.rename`)
10. Undo
11. Unpack كعملية عكسية تقريبية
12. Batch Rename: القالب والأرقام والتاريخ
13. أحداث tkinter: Checkbutton وCombobox
14. معالجة الأخطاء الموجودة فعليًا (`cwd`، `FileExistsError`، `except: pass`)
15. لاحقًا: Settings + pickle
16. متقدم: Encrypt، Clear Temp، threading وآمانه

لا تستخدم الترتيب الأبجدي للملفات.

---

## Files — التصنيف التدريسي

### CATEGORY A — MUST TEACH

| ملف | السبب |
|---|---|
| `dirx.py` | نقطة التشغيل |
| `Frames/__init__.py` | ربط الحزمة |
| `Frames/status.py` | تغذية راجعة للمستخدم |
| `Frames/organiser.py` | التنظيم وهو قلب المنهج |
| `Frames/rename.py` | إعادة التسمية بالجملة |
| `Frames/unpack.py` | نقل عكسي مبسّط |

### CATEGORY B — SHOULD TEACH

| ملف | السبب |
|---|---|
| `Frames/settings.py` | تحرير مجموعات الامتدادات |
| `config/config` | مصدر `DIRECTORIES` |
| `windowsdpi.py` | سطر الغرض فقط |

### CATEGORY C — ADVANCED

| ملف | السبب |
|---|---|
| `Frames/encrypt.py` | AES ومكتبة خارجية وملفات ثنائية |
| `Frames/cleartemp.py` | حذف حقيقي لمجلد النظام |

### CATEGORY D — DO NOT TEACH INITIALLY

| عنصر | السبب |
|---|---|
| `Frames/__pycache__` | نواتج تشغيل |
| `.venv` | بيئة محلية |
| الكود المعلّق الطويل في `organiser.py` | نسخة قديمة مربكة |
| `update_progress` / `validate_fname` غير المستدعاة | تشتيت |
| Clear Temp عمليًا على جهاز الطالب | خطر فقدان بيانات |

---

## Code Blocks

وحدات صغيرة لفيديو واحد لكل Block.

| Block ID | File | Function/Class | Purpose | Concepts | Prerequisites | Difficulty | Teaching Priority |
|---|---|---|---|---|---|---|---|
| B01 | dirx.py | `DirX.__init__` | بناء النافذة والتبويبات | Tk, Notebook | Python basics | 1 | P1 |
| B02 | dirx.py | أسفل الملف `root.mainloop` | حلقة الأحداث | event loop | B01 | 1 | P1 |
| B03 | windowsdpi.py | `set_dpi_awareness` | تحسين العرض على Windows | try/except, ctypes | B01 | 2 | P4 |
| B04 | Frames/__init__.py | الاستيرادات | تصدير الأصناف | packages | B01 | 1 | P1 |
| B05 | status.py | `Status` | عداد الملفات | StringVar, Style | B01 | 2 | P1 |
| B06 | organiser.py | `FileOrganizer.__init__` | واجهة التنظيم والمسار الافتراضي Desktop | Frame, StringVar, Combobox | B05 | 2 | P1 |
| B07 | organiser.py | `open_dialog`, `cwd` | اختيار المجلد والتحقق | filedialog, chdir, FileNotFoundError | B06 | 2 | P1 |
| B08 | organiser.py | `organize` | توجيه حسب Combobox | if/elif, current() | B07 | 1 | P1 |
| B09 | organiser.py | `organize_by_ext` | مجلد لكل امتداد | listdir, splitext, makedirs, shutil.move | B08 | 2 | P1 |
| B10 | organiser.py | `init_file_formats`, `organize_by_type` | تصنيف نوع + OTHER | dict comprehension, Path.rename | B09 | 3 | P1 |
| B11 | organiser.py | `get_doc`, `get_dom`, organize by date | مجلدات التاريخ | pathlib.stat, strftime | B09 | 3 | P2 |
| B12 | organiser.py | `undo_organize` | عكس آخر تنظيم | shutil.move, rmdir, undo_list | B10 | 3 | P1 |
| B13 | organiser.py | `start_organize` | Thread | threading | B08 | 3 | P3 |
| B14 | settings.py | `Settings` + pickle | تعديل المجموعات | Toplevel, Listbox, pickle | B10 | 3 | P2 |
| B15 | unpack.py | `unpack_files` | تفريغ مستوى واحد | isdir, join, rmdir | B09 | 2 | P1 |
| B16 | rename.py | `__init__` UI | قالب Prefix/Name/Postfix | Checkbutton, Combobox bind | B07 | 2 | P1 |
| B17 | rename.py | `rename_all` | تركيب الاسم + ext | f-string, os.rename | B16, B09 | 3 | P1 |
| B18 | rename.py | `get_prefix` / `get_fname` / `get_postfix` | مصادر الاسم | Numeric من 0، التواريخ | B17 | 2 | P1 |
| B19 | rename.py | فرع `FileExistsError` | منع overwrite | while True, (i) | B17 | 2 | P1 |
| B20 | encrypt.py | `encrypt` / `decrypt` | AES ملف واحد | binary files, Crypto | B07 | 4 | P4 |
| B21 | cleartemp.py | `clear_temp`, `get_size` | مسح Temp | rmtree, Path.glob | B15 | 3 | P4 |

---

## Concept Inventory

### موجود فعليًا في الكود — Python Basics

- Variables, Strings, Numbers, Boolean (`BooleanVar`)
- Lists, Dictionaries
- Conditions, Loops (`for`, `while True` في Rename)
- Functions, Parameters, Return
- Imports
- Exceptions (`try/except`, `FileNotFoundError`, `FileExistsError`, `OSError`, `ValueError`)

Tuples: ليست نمطًا مركزيًا في المشروع.

### موجود فعليًا — Intermediate

- Modules / Packages (`Frames`)
- Classes / Objects / `super().__init__`
- Callbacks (`command=`, `bind("<<ComboboxSelected>>")`)
- Context managers (`with open`)
- File handling (نصي/ثنائي في Encrypt)
- pathlib, os, shutil
- datetime
- GUI tkinter / ttk
- Event-driven programming
- threading
- pickle
- subprocess (Clear Temp)
- ctypes (DPI)

### غير موجود في الكود — لا تدرّسه كأنه جزء من DirX

- Decorators
- Type hints (عدا تعليق rtype في Status)
- `re` كاستيراد
- `glob` كوحدة (يوجد `Path.glob` في Clear Temp فقط)

### RECOMMENDED PREREQUISITE

- فكرة الوراثة قبل `class FileOrganizer(ttk.Frame)`
- فرق الملف عن المجلد قبل `os.path.isfile`

---

## LEVEL 1 — Beginner

شغّل البرنامج، اشرح التبويبات، غيّر المسار إلى TEST، اقرأ `dirx.py` و`status.py` وواجهة Organizer، نفّذ `organize_by_ext` على ملفات تجريبية.

## LEVEL 2 — Intermediate

`organize_by_type`، pickle عبر Settings، Undo، Unpack، Batch Rename كاملًا بما فيه الأسماء المكررة.

## LEVEL 3 — Advanced

Encrypt AES، Clear Temp، threading مع tkinter، أخطاء `except: pass`، لماذا `os.path.isdir(name)` بدون join كان يكسر Unpack.

---

## ما الذي لا نشرحه في البداية؟

| الجزء | لماذا متقدم؟ | نؤجله؟ | متى؟ | متطلبات سابقة |
|---|---|---|---|---|
| AES في encrypt.py | تشفير ومفاتيح وIV | نعم | بعد الملفات الثنائية | open rb/wb |
| كتابة المفتاح داخل الملف المشفّر | موضوع أمني حساس | نعم | درس أمن لاحق | فهم encrypt() |
| Clear Temp | حذف نظامي | نعم | آخر المنهج وبتحذير | shutil |
| pickle الثنائي | ليس JSON | نعم جزئيًا | مع Settings | القواميس |
| threading | سباق مع tkinter | نعم | بعد أن تعمل الأزرار | دوال Organize |
| ctypes DPI | WinAPI | نعم | اختياري | — |
| `except: pass` كأسلوب | جودة برمجية | ناقش بعد نجاح العملية | بعد Organize | try/except |

لا تحذف هذه الأجزاء من المستودع.

---

## Exercises

1. عدّ ملفات مجلد TEST بنفس تعبير `listdir` + `isfile` بعد `chdir`.
2. اطبع الامتداد لكل ملف بـ `splitext`.
3. توقّع مجلد الوجهة لـ `sample.jpg` من `FILE_FORMATS` ثم نفّذ Organize وتحقق.
4. نظّم حسب الامتداد ثم Unpack مع حذف المجلدات الفارغة.
5. أعد التسمية بـ Custom prefix فقط، ثم Numeric + Custom name.
6. أنشئ ملفين واجعل اسم الوجهة واحدًا؛ راقب `(1)`.
6. مسار فيه مسافات واسم عربي.
7. اكتب مسارًا خاطئًا وتأكد من `Invalid Path!`.
8. Organize ثم Undo ثم أغلق البرنامج واشرح لماذا لا يعود Undo.

---

## Common Mistakes

- الاختبار على Desktop الحقيقي لأن الحقل الافتراضي يشير إليه
- نسيان تثبيت `pycryptodome` ثم الاعتقاد أن tkinter معطوب
- تشغيل `python dirx.py` من مجلد آخر فلا تُوجد حزمة `Frames`
- الخلط بين Unpack وUndo
- انتظار أن Numeric يبدأ من 1 بينما الكود يبدأ من 0
- تعديل `config/config` كملف نصي فيدمر pickle

---

## Challenges

- أضف امتدادًا جديدًا من Settings ثم نظّم ملفًا بهذا الامتداد
- اشرح لماذا `organize_by_type` يستخدم `Path.rename` بينما `organize_by_ext` يستخدم `shutil.move`
- تتبّع `undo_list` على الورق أثناء عملية واحدة

---

## Homework

- ارسم تدفق `rename_all` لثلاثة ملفات
- قارن سلوك الاسم المكرر في Rename مقابل Organize (Rename يضيف `(i)`، Organize يفشل بصمت ويُبقي المصدر)

---

## Final Challenge

على مجلد TEST فقط: نظّم حسب النوع، تأكد من المجلدات، Undo، نظّم حسب الامتداد، Unpack، ثم Batch Rename بقالب README (`Numeric` + `SalesReport`). لا تستخدم Desktop ولا Clear Temp.

---

## Exercises للمدرس (سلامة)

- امنع الطلاب من Encrypt لملفات شخصية
- لا تشغّل Clear Temp في القاعة على أجهزة الطلاب
