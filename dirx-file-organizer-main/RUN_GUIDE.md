# تشغيل مشروع إعادة تسمية وتنظيم الملفات

هذا الدليل مبني على المشروع الحقيقي **DirX** كما هو موجود في المجلد، وعلى أوامر تم تشغيلها فعليًا على Windows.

المصدر الأصلي: [thePolitician/dirx-file-organizer](https://github.com/thePolitician/dirx-file-organizer)

---

## 1. فكرة المشروع

DirX أداة مكتبية مكتوبة بـ **Python 3 + tkinter**. النافذة تحتوي على خمس تبويبات:

| التبويب | الملف | ماذا يفعل |
|---|---|---|
| File Organizer | `Frames/organiser.py` | ينظّم ملفات مجلد واحد حسب النوع أو الامتداد أو تاريخ الإنشاء أو تاريخ التعديل |
| Unpack | `Frames/unpack.py` | ينقل ملفات المجلدات الفرعية المباشرة إلى المجلد الأب |
| Batch Rename | `Frames/rename.py` | يعيد تسمية كل الملفات في المجلد حسب قالب (Prefix / Filename / Postfix) |
| Encrypt/Decrypt | `Frames/encrypt.py` | يشفر/يفك تشفير **ملف واحد** بـ AES وكلمة مرور |
| Clear Temp | `Frames/cleartemp.py` | يحذف محتويات مجلد Temp الخاص بالمستخدم على Windows |

نقطة التشغيل هي `dirx.py`. لا يوجد `if __name__ == "__main__"`: الملف ينشئ النافذة ويستدعي `mainloop()` مباشرة.

---

## 2. المتطلبات

- Windows (المسار الافتراضي يستخدم `\\Desktop` و `AppData\\Local\\Temp`)
- Python 3 مع tkinter (اختُبر على **Python 3.12.0**)
- مكتبة واحدة خارج المكتبة القياسية: **pycryptodome** (يستوردها `Frames/encrypt.py` كـ `Crypto`)
- أيقونة: `icons/dirx.ico`
- إعدادات التصنيف: `config/config` (ملف pickle)

لا يوجد في المشروع الأصلي ملف `requirements.txt`. أُضيف لاحقًا ليطابق الاعتماد الحقيقي.

---

## 3. Python version

تم الاختبار على:

```text
Python 3.12.0
tkinter 8.6
```

الأمر المستخدم:

```powershell
python --version
```

الكود الأصلي في README يقول `python3 dirx.py`. على Windows في هذه البيئة الأمر `python3` غير متوفر؛ استخدم `python`.

---

## 4. إنشاء virtual environment

من مجلد المشروع الذي يحتوي `dirx.py`:

```powershell
cd D:\project_lv3\dirx-file-organizer-main\dirx-file-organizer-main
python -m venv .venv
```

---

## 5. تفعيل البيئة في Windows

PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

أو بدون تفعيل، استخدم المفسر مباشرة:

```powershell
.\.venv\Scripts\python.exe
```

---

## 6. تثبيت dependencies

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

الاعتماد الوحيد غير القياسي الذي ثبتناه واختبرناه:

```text
pycryptodome==3.23.0
```

بدون هذه المكتبة يفشل التشغيل عند الاستيراد:

```text
File "Frames\__init__.py", line 5, in <module>
    from Frames.encrypt import Encrypt
File "Frames\encrypt.py", line 5, in <module>
    from Crypto.Cipher import AES
ModuleNotFoundError: No module named 'Crypto'
```

tkinter يأتي مع تثبيت Python الرسمي لـ Windows؛ لا يُثبَّت عبر pip.

---

## 7. تشغيل المشروع

من مجلد `dirx.py`:

```powershell
.\.venv\Scripts\python.exe dirx.py
```

هذا الأمر شُغّل فعليًا. ظهرت نافذة عنوانها **DirX** وفيها التبويبات الخمسة.

لإغلاق البرنامج: أغلق النافذة من زر الإغلاق في Windows.

---

## 8. كيفية اختيار المجلد

في تبويبات Organizer / Unpack / Rename:

1. اضغط **Select Folder**.
2. اختر مجلدًا من مربع الحوار (`tkinter.filedialog.askdirectory`).
3. يُكتب المسار في حقل Path.

يمكنك أيضًا لصق المسار يدويًا في الحقل.

تحذير: القيمة الافتراضية عند فتح البرنامج هي مجلد **سطح المكتب** (`os.path.expanduser('~') + '\\Desktop'`). لا تستخدم سطح المكتب الحقيقي للتدريب.

---

## 9. كيفية تنظيم الملفات

في تبويب **File Organizer**:

1. اختر مجلد الاختبار فقط.
2. من **Organize By** اختر أحد الخيارات:
   - `Type of File` → مجلدات مثل `IMAGES` و `PDF` حسب `config/config`
   - `Extension of File` → مجلد باسم الامتداد بدون النقطة (`jpg`, `pdf`)
   - `Date Created` → مجلد بتاريخ `st_ctime` بالصيغة `%d %b %Y`
   - `Date Modified` → مجلد بتاريخ `st_mtime` بنفس الصيغة
3. اضغط **Organize**.
4. الزر يعمل في خيط (`threading.Thread`) حتى لا تتجمد الواجهة.
5. الامتداد غير المعروف يذهب إلى مجلد `OTHER`.
6. **Undo** يعيد الملفات من المجلدات التي أنشأها آخر تنظيم ثم يحذف تلك المجلدات إن صارت فارغة. Undo يعمل فقط أثناء تشغيل الجلسة الحالية (القائمة في الذاكرة وليست ملف سجل).

---

## 10. كيفية إعادة التسمية

في تبويب **Batch Rename**:

1. اختر المجلد.
2. فعّل واحدًا أو أكثر من:
   - **Add Prefix**
   - **Change File Name**
   - **Add Postfix**
3. لكل جزء اختر: `Custom` أو `Numeric` أو `Date Created` أو `Date Modified`.
4. إذا اخترت Custom اكتب النص في حقل Text المقابل.
5. اضغط **Rename All**.

الاسم النهائي في الكود:

```text
{prefix}{fname}{postfix}{ext}
```

حيث الامتداد الأصلي يُحفظ عبر `os.path.splitext`. الرقم في الوضع Numeric يبدأ من **0** (هذا سلوك الكود الفعلي، وهو مذكور في مثال README الأصلي).

إذا وُجد اسم مكرر يُلحق `(1)` ثم `(2)` ... قبل الامتداد.

لا يوجد Undo لإعادة التسمية.

---

## 11. أمثلة عملية

استخدم فقط مجلد `TEST` داخل المشروع.

**تنظيم حسب النوع**

ضع في `TEST\06_organize` ملفات مثل `sample.jpg` و `document.pdf`. بعد Organize يجب أن تظهر مجلدات `IMAGES` و `PDF`.

**Batch Rename كما في README**

- Prefix = Numeric
- Filename = Custom `SalesReport`
- النتيجة الفعلية المختبرة: `0 SalesReport.txt`, `1 SalesReport.txt`, `2 SalesReport.txt`

**Unpack**

بعد التنظيم، Unpack ينقل الملفات من المجلدات الفرعية المباشرة إلى الأب. خيار **Delete emptied folders** يحذف المجلد الفرعي إذا أصبح فارغًا.

---

## 12. المشاكل الشائعة

| المشكلة | السبب |
|---|---|
| `No module named 'Crypto'` | لم يُثبَّت pycryptodome |
| `python3` غير موجود | على Windows استخدم `python` |
| النافذة لا تفتح وخطأ `iconbitmap` | ملف `icons/dirx.ico` مفقود |
| `Config file not found!` | ملف `config/config` مفقود |
| Organize لا يفعل شيئًا ظاهرًا | مسار غير موجود، أو الملفات مجلدات وليست ملفات، أو فشل النقل وصُمت بـ `except: pass` |
| Unpack لا ينقل شيئًا رغم وجود مجلدات | سابقًا كان يفحص `os.path.isdir(name)` نسبةً لمجلد العمل الحالي وليس للمسار المكتوب |

---

## 13. حلول المشاكل

1. ثبّت الاعتماد: `pip install -r requirements.txt`
2. شغّل من مجلد المشروع حتى تعمل حزمة `Frames`
3. تأكد من وجود `icons/dirx.ico` و `config/config`
4. استخدم مجلد TEST وليس Desktop
5. إذا ظهر `Invalid Path!` فالمسار في الحقل غير موجود (`FileOrganizer.cwd`)

---

## 14. تحذيرات مهمة

- البرنامج يغيّر الملفات على القرص فور الضغط على Organize / Rename / Unpack / Encrypt / Clear Temp.
- القيمة الافتراضية هي **Desktop**. غيّرها قبل أي عملية.
- **Clear Temp** يستهدف `%USERPROFILE%\AppData\Local\Temp` ويستدعي `shutil.rmtree`. لا تشغّله في درس المبتدئين وعلى جهاز حقيقي إلا بوعي.
- Organize لا يستبدل ملفًا موجودًا بنفس الاسم في الوجهة: العملية تفشل بصمت ويبقى الملف في المصدر (اختُبر).
- Rename يمنع الكتابة فوق اسم موجود بإضافة `(i)`.
- Encrypt يكتب ملفًا جديدًا `filename.enc` وDecrypt يكتب `(decrypted)filename`؛ الملف الأصلي للتشفير يبقى.
- Undo للتنظيم فقط، وفي الذاكرة فقط.
- المؤلف الأصلي نبّه أن استخدام threading قد لا يكون آمنًا مع tkinter.

---

## 15. كيفية الاختبار الآمن

1. لا تختبر على Desktop أو Downloads أو Documents الحقيقي.
2. استخدم مجلد المشروع `TEST`.
3. ضع ملفات تجريبية غير مهمة فقط.
4. يمكن تشغيل سكربت الاختبار الآمن الذي يستدعي نفس الأصناف بدون `mainloop`:

```powershell
.\.venv\Scripts\python.exe TEST_RUNNER.py
```

هذا السكربت يعمل فقط تحت `./TEST` ولا يستدعي `ClearTemp.clear_temp`.
