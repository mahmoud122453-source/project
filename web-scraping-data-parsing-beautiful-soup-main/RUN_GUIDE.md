# تشغيل مشروع استخراج البيانات من الويب

دليل تشغيل مبني على المشروع الحقيقي: **Web Scraping and Data Parsing Using Beautiful Soup** (Oxylabs).

---

## 1. فكرة المشروع

المشروع يزور موقع التدريب `https://books.toscrape.com`، يجلب صفحة HTML، يستخرج عناوين الكتب الظاهرة في الصفحة الأولى، ثم يحفظها في ملف CSV.

هناك ثلاثة سكربتات متدرجة داخل `src/`:

| الملف | ماذا يفعل |
|---|---|
| `scrape.py` | طلب HTTP والتحقق من نجاحه |
| `parse.py` | تحليل HTML واستخراج العناوين وطباعتها |
| `save.py` | استخراج العناوين وحفظها في `books.csv` |

النسخة النهائية الكاملة هي `src/save.py`.

---

## 2. المتطلبات

- Python 3 (اختُبر على **Python 3.12.0**)
- اتصال بالإنترنت للوصول إلى `books.toscrape.com`
- المكتبات: `requests` و `beautifulsoup4` و `pandas`

---

## 3. Python version

على هذا الجهاز تم التحقق من:

```text
python --version
Python 3.12.0
```

المفسر المستخدم:

```text
C:\Users\DELL\AppData\Local\Programs\Python\Python312\python.exe
```

على Windows استخدم `python` وليس `python3`. الأمر `python3` غير متوفر هنا وقد يفتح متجر Microsoft بدل المفسر الحقيقي.

---

## 4. إنشاء virtual environment

من مجلد المشروع:

```powershell
python -m venv .venv
```

---

## 5. تفعيل البيئة على Windows

PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

إذا ظهرت رسالة تمنع تشغيل السكربتات، نفّذ مرة واحدة لحساب المستخدم الحالي ثم أعد التفعيل:

```powershell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
.\.venv\Scripts\Activate.ps1
```

بعد التفعيل يظهر اسم البيئة في بداية سطر الأوامر.

CMD:

```cmd
.venv\Scripts\activate.bat
```

---

## 6. تثبيت dependencies

من مجلد المشروع:

```powershell
python -m pip install -r src/requirements.txt
```

الملف الأصلي كان يثبّت إصدارات قديمة (`pandas==1.5.1`) لا تعمل على Python 3.12. تم تحديث الملف لإصدارات تم التحقق منها مع تشغيل المشروع.

---

## 7. طريقة التشغيل

### المرحلة 1 — جلب الصفحة فقط

من مجلد المشروع:

```powershell
python src/scrape.py
```

الناتج المتوقع:

```text
Successfully fetched the page
```

### المرحلة 2 — استخراج العناوين وطباعتها

```powershell
python src/parse.py
```

المتوقع: رسالة النجاح ثم قائمة عناوين الكتب.

### المرحلة 3 — حفظ النتائج (النسخة النهائية)

يجب تشغيل هذا السكربت من داخل `src` لأن الملف يُحفظ بالاسم النسبي `books.csv`:

```powershell
cd src
python save.py
```

الناتج المتوقع:

```text
Successfully fetched the page
```

الأمر الذي اختُبر فعليًا بنجاح على هذا الجهاز:

```powershell
cd src
python save.py
```

---

## 8. الموقع المستخدم للاختبار

```text
https://books.toscrape.com
```

موقع تجريبي مخصص لتعلم Web Scraping. لا تستخدم مواقع تتطلب تسجيل دخول أو CAPTCHA.

---

## 9. ماذا يحدث أثناء التشغيل؟

عند تشغيل `save.py`:

1. `requests.get` يرسل طلب HTTP GET إلى الموقع.
2. البرنامج يفحص `response.status_code`.
3. إذا لم تكن القيمة `200` يطبع `Could not fetch the page` ويتوقف بـ `exit(1)`.
4. إذا نجح الطلب يطبع `Successfully fetched the page`.
5. `BeautifulSoup` يحوّل HTML إلى شجرة يمكن البحث فيها.
6. `find_all('article')` يجد بطاقات الكتب.
7. الحلقة تستخرج `article.h3.a.attrs['title']` لكل كتاب.
8. `pandas.DataFrame` يضع العناوين في عمود اسمه `Title`.
9. `to_csv` يحفظ الملف `books.csv`.

---

## 10. مكان ملف النتائج

عند التشغيل من داخل `src`:

```text
src/books.csv
```

المسار الكامل على هذا الجهاز بعد الاختبار:

```text
D:\project_lv3\web-scraping-data-parsing-beautiful-soup-main\src\books.csv
```

إذا شغّلت `python src/save.py` من جذر المشروع، سيُنشأ `books.csv` في مجلد التشغيل الحالي وليس داخل `src`. التزم بـ `cd src` ثم `python save.py`.

---

## 11. كيفية فتح النتائج

- Excel أو LibreOffice
- VS Code / Cursor
- PowerShell:

```powershell
Get-Content books.csv
```

أو من Python:

```python
import pandas
print(pandas.read_csv('books.csv'))
```

---

## 12. المشاكل الشائعة

- استخدام `python3` على Windows
- نسيان تفعيل البيئة الافتراضية
- تثبيت `requirements.txt` القديم على Python 3.12
- تشغيل `save.py` من مجلد خاطئ ثم البحث عن CSV في المكان الخطأ
- انقطاع الإنترنت أو فشل DNS
- الموقع غير متاح مؤقتًا

---

## 13. حلول المشاكل

| المشكلة | الحل |
|---|---|
| `python3` غير موجود | استخدم `python` |
| المكتبات غير مثبتة | `python -m pip install -r src/requirements.txt` |
| CSV غير موجود في `src` | شغّل من داخل `src` كما في README الأصلي |
| `Successfully fetched the page` لكن لا يوجد CSV | أنت شغّلت `scrape.py` أو `parse.py` وليس `save.py` |
| PowerShell يمنع تفعيل `.venv` | `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` |

---

## 14. مشاكل الاتصال

إذا فشل حل اسم النطاق يظهر `ConnectionError` من مكتبة `requests`. المشروع **لا يلتقط هذا الاستثناء**؛ ستظهر traceback في الطرفية.

إذا رد الموقع برمز غير `200` (مثل `404`) يطبع البرنامج:

```text
Could not fetch the page
```

ثم يتوقف.

---

## 15. مشاكل HTML

الاستخراج يعتمد على مسار ثابت:

```text
article → h3 → a → attribute title
```

إذا تغيّر HTML قد يحدث `AttributeError` أو `KeyError`. المشروع لا يعالج هذا الحالة. الموقع التدريبي مستقر لهذا المثال.

---

## 16. مشاكل المكتبات

- `ModuleNotFoundError: requests` / `bs4` / `pandas`: المكتبة غير مثبتة في المفسر الحالي.
- فشل تثبيت `pandas==1.5.1` على Python 3.12: استخدم `src/requirements.txt` المحدّث.
- تأكد أن Cursor يستخدم نفس المفسر الذي ثبّت عليه المكتبات:

```text
C:\Users\DELL\AppData\Local\Programs\Python\Python312\python.exe
```

---

## 17. ملاحظات Web Scraping المسؤولة

- استخدم مواقع تدريبية مثل Books to Scrape.
- لا تحاول تجاوز تسجيل الدخول أو CAPTCHA.
- لا ترسل طلبات متكررة بسرعة عالية.
- احترم شروط الموقع و`robots.txt` عند تجربة مواقع أخرى.
- هذا المشروع يطلب **صفحة واحدة فقط** في كل تشغيل.
- لا تجمع بيانات شخصية.
