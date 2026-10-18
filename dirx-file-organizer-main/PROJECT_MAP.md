# PROJECT_MAP.md — DirX

المصدر: مشروع [DirX: File and folder handling tools](https://github.com/thePolitician/dirx-file-organizer) كما هو في هذه النسخة المحلية.

---

## Project Purpose

تطبيق tkinter لإدارة الملفات بالجملة: تنظيم، فك تجميع المجلدات، إعادة تسمية دفعة، تشفير ملف، ومسح مجلد Temp على Windows.

---

## Folder Structure

```text
dirx-file-organizer-main/
├── dirx.py                 # نقطة التشغيل والنافذة الرئيسية
├── windowsdpi.py           # DPI awareness على Windows
├── README.md               # توثيق المؤلف الأصلي
├── requirements.txt        # أُضيف: pycryptodome
├── RUN_GUIDE.md
├── TEACHING_GUIDE.md
├── FILE_TEACHING_ORDER.md
├── PROJECT_MAP.md
├── TEST_RUNNER.py          # اختبار آمن على ./TEST فقط
├── config/
│   └── config              # pickle: خريطة نوع الملف → قائمة امتدادات
├── icons/
│   └── dirx.ico
├── Frames/
│   ├── __init__.py
│   ├── organiser.py
│   ├── unpack.py
│   ├── rename.py
│   ├── encrypt.py
│   ├── cleartemp.py
│   ├── settings.py
│   └── status.py
└── TEST/                   # مجلد اختبار محلي (لا تستخدم Desktop)
```

لا يوجد في النسخة الأصلية: `LICENSE`، `setup.py`، `pyproject.toml`، `requirements.txt`، أو حزمة assets غير `icons/dirx.ico`.

---

## File Structure (دور كل ملف)

| ملف | الدور |
|---|---|
| `dirx.py` | `class DirX(tk.Tk)` + `ttk.Notebook` + `mainloop` |
| `windowsdpi.py` | `SetProcessDpiAwareness(1)` عبر `ctypes.windll` |
| `Frames/__init__.py` | يعيد تصدير الأصناف الخمسة للتبويبات |
| `Frames/organiser.py` | تنظيم الملفات + Undo + زر Settings |
| `Frames/settings.py` | نافذة تعديل مجموعات الامتدادات وكتابة pickle |
| `Frames/status.py` | عداد `Files Processed: n/total` ورسالة الخطأ |
| `Frames/unpack.py` | نقل ملفات المجلدات الفرعية المباشرة للأب |
| `Frames/rename.py` | Batch Rename |
| `Frames/encrypt.py` | AES-CBC لملف واحد |
| `Frames/cleartemp.py` | حجم ومسح `%USERPROFILE%\AppData\Local\Temp` |
| `config/config` | بيانات التصنيف (ليست شيفرة) |
| `icons/dirx.ico` | أيقونة النافذة |

---

## Architecture (مطابق للكود)

```text
User
  ↓
DirX (tk.Tk) + ttk.Notebook
  ↓
FileOrganizer | DirUnpack | BatchRename | Encrypt | ClearTemp
  ↓
Folder/File selection (filedialog) + path StringVar
  ↓
os.chdir / os.listdir / Path / splitext / pickle config
  ↓
Classify (FILE_FORMATS / ext folder / date folder)  OR  build new name  OR  AES
  ↓
shutil.move / Path.rename / os.rename / shutil.rmtree
  ↓
File System
  ↓
Status labels (Files Processed / Success / Error)
```

هذا المخطط يصف التدفق الفعلي. البرنامج ليس طبقات MVC منفصلة؛ كل تبويب Frame يخلط الواجهة والمنطق ونظام الملفات في نفس الملف.

---

## Execution Flow

1. `dirx.py` يستورد الحزم ويستدعي `set_dpi_awareness()`.
2. `root = DirX()` ثم `root.mainloop()`.
3. `DirX.__init__` يضبط العنوان والأيقونة ويمنع تغيير الحجم.
4. يُنشأ `ttk.Notebook` وخمسة إطارات.
5. إنشاء `FileOrganizer` يغيّر مجلد العمل إلى Desktop ويحمّل `config/config`.
6. إنشاء `DirUnpack` و `BatchRename` يفعل `os.chdir(Desktop)` أيضًا.
7. إنشاء `ClearTemp` يحسب حجم مجلد Temp الحقيقي (قراءة فقط عند الإقلاع).
8. المستخدم يختار تبويبًا ثم مسارًا ثم عملية.
9. Organizer / Unpack / Rename / Clear Temp تشغّل العمل في `threading.Thread`.
10. Encrypt/Decrypt يعملان على الخيط الرئيسي للواجهة.

---

## Data Flow

### تنظيم حسب النوع

```text
path → os.chdir(path) → os.listdir → isfile
     → os.path.splitext → lower()
     → FILE_FORMATS[ext] أو "OTHER"
     → Path.mkdir إن لزم
     → Path.rename إلى المجلد
     → undo_list['dirs'] تتذكر المجلدات الجديدة
```

`FILE_FORMATS` يُبنى في `init_file_formats()` من القاموس `DIRECTORIES` المحمّل بـ pickle.

### إعادة التسمية

```text
os.listdir files → لكل ملف:
  prefix من get_prefix
  fname من splitext أو get_fname
  postfix من get_postfix
  dest = f"{prefix}{fname}{postfix}{ext}"
  os.rename؛ إن FileExistsError جرب dest مع (i)
```

لا يوجد ملف سجل. العداد في `Status` فقط.

---

## File Dependencies

```text
dirx.py
  ├── windowsdpi.set_dpi_awareness
  └── Frames.__init__
        ├── organiser.FileOrganizer
        │     ├── status.Status
        │     └── settings.Settings  (عند زر Settings)
        ├── unpack.DirUnpack
        ├── rename.BatchRename
        │     └── status.Status
        ├── encrypt.Encrypt
        └── cleartemp.ClearTemp
```

`organiser.py` يستورد `pprint` ولا يستخدمه.

`rename.py` يعرّف `validate_fname` و`update_progress` ولا يستدعيهما من مسار Rename All العامل.

---

## Classes

| Class | ملف | أب |
|---|---|---|
| `DirX` | dirx.py | `tk.Tk` |
| `FileOrganizer` | organiser.py | `ttk.Frame` |
| `DirUnpack` | unpack.py | `ttk.Frame` |
| `BatchRename` | rename.py | `ttk.Frame` |
| `Encrypt` | encrypt.py | `ttk.Frame` |
| `ClearTemp` | cleartemp.py | `ttk.Frame` |
| `Settings` | settings.py | ليس Frame؛ ينشئ `tk.Toplevel` |
| `Status` | status.py | `ttk.Frame` |

دوال حرة: `disable` / `enable` في organiser و unpack و rename؛ `set_dpi_awareness` في windowsdpi.

---

## Functions (حسب المسؤولية)

### تنظيم

- `start_organize` / `organize` — اختيار الخوارزمية
- `organize_by_type` / `organize_by_ext` / `organize_by_doc` / `organize_by_dom`
- `undo_organize`
- `get_doc` / `get_dom`
- `open_dialog` / `cwd`
- `load_categories` / `init_file_formats`

### إعادة التسمية

- `start_rename` / `rename_all`
- `get_prefix` / `get_fname` / `get_postfix`
- `set_prefix` / `set_fname` / `set_postfix`
- `OnSelectPrefix` / `OnSelectName` / `OnSelectPostfix`
- `open_dialog` / `get_doc` / `get_dom`

### Unpack

- `start_unpack` / `unpack_files` / `open_dialog`

### تشفير

- `encrypt_file` / `decrypt_file` / `encrypt` / `decrypt`
- `check_encryption` / `check_hash` / `getKey` / `get_password`

### Temp

- `start_clear_temp` / `clear_temp` / `open_temp` / `get_size`

---

## Libraries (المستخدمة فعليًا)

| مكتبة | أين | لماذا |
|---|---|---|
| `tkinter` / `ttk` | كلها تقريبًا | GUI |
| `tkinter.filedialog` | organizer, unpack, rename, encrypt | اختيار مجلد/ملف |
| `tkinter.messagebox` | organizer, settings, encrypt | أخطاء |
| `tkinter.simpledialog` | settings, encrypt | إدخال نص/كلمة مرور |
| `os` | organizer, unpack, rename, encrypt, cleartemp | مسارات، listdir، chdir، rename، rmdir |
| `shutil` | organizer, unpack, cleartemp | move / rmtree |
| `pathlib.Path` | dirx, organizer, rename, settings, encrypt, cleartemp | مسارات وأيقونة وإحصاء الحجم |
| `datetime` | organizer, rename | تواريخ الملفات |
| `pickle` | organizer, settings | قراءة/كتابة config |
| `threading` | organizer, unpack, rename, cleartemp | تشغيل العملية في الخلفية |
| `subprocess` | cleartemp | `explorer` لفتح مجلد Temp |
| `ctypes.windll` | windowsdpi | DPI |
| `Crypto.Cipher.AES` / `SHA256` / `Random` | encrypt | AES-CBC ومفتاح من كلمة المرور |

غير مستخدم في الكود رغم شيوعه في دروس الملفات: `glob` كاستيراد مباشر (يوجد `Path.glob` داخل `get_size` فقط)، و`re`.

---

## User Interaction

1. تشغيل `python dirx.py`
2. اختيار تبويب من Notebook
3. Select Folder أو Select File أو المسار الافتراضي
4. ضبط خيارات (نوع التنظيم، بادئة الاسم، حذف المجلدات الفارغة، كلمة المرور)
5. زر التنفيذ
6. قراءة الحالة أسفل التبويب
7. Undo متاح فقط في File Organizer بعد عملية أنشأت مجلدات محفوظة في `undo_list`
