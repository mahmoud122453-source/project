# دليل التشغيل — Stock Tracker

هذا الدليل يصف طريقة تشغيل المشروع **كما هو** على Windows بعد التحقق الفعلي، وليس تخميناً.

## البيئة المُتحقَّق منها

| العنصر | القيمة المُقاسة |
|---|---|
| نظام التشغيل | Windows 10 (`win32 10.0.19045`) |
| Python | **3.12.0** (`C:\Users\DELL\AppData\Local\Programs\Python\Python312\python.exe`) |
| pip (داخل البيئة الافتراضية) | 26.2.1 |
| نقطة الدخول | `app.py` |
| أمر التشغيل | `.\.venv\Scripts\python.exe -m streamlit run app.py` |
| عنوان المتصفح | http://localhost:8501 |

## التبعيات

### الملف الأصلي `requirements.txt`

```
pandas==1.5.3
streamlit==1.20.0
yfinance==0.2.14
numpy==1.24.4
```

هذه الإصدارات **لا تُثبَّت بنجاح على Python 3.12**: `pandas==1.5.3` يُنزَّل كملف مصدر (لا يوجد عجلة `cp312`) ويعلق أثناء البناء.

`numpy` مذكور في المتطلبات لكنه **غير مستورد** في `app.py`.

`pandas` مستورد في `app.py` لكنه **غير مستخدم مباشرة**؛ `yfinance` يعيد `DataFrame` وStreamlit يعرضه.

### الإصدارات التي شُغّل بها التطبيق فعلياً

داخل `.venv`:

- streamlit **1.64.0**
- yfinance **1.7.0**
- pandas **3.0.6**
- numpy **2.5.3**

## إنشاء البيئة الافتراضية والتثبيت (موثَّق)

من مجلد المشروع:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install --upgrade pip
```

**لا تستخدم** `pip install -r requirements.txt` على Python 3.12 (فشل التحقق).

استخدم بدلاً منه:

```powershell
.\.venv\Scripts\python.exe -m pip install --no-cache-dir pandas streamlit yfinance numpy
```

ملاحظة: التثبيت من PyPI كان بطيئاً على هذه الآلة؛ `--no-cache-dir` تجنّب خطأ تجزئة ظهر مع الكاش بعد محاولة التثبيت المثبتة النسخ.

للتحقق:

```powershell
.\.venv\Scripts\python.exe -c "import streamlit,yfinance,pandas; print(streamlit.__version__, yfinance.__version__, pandas.__version__)"
```

## أمر التشغيل المُتحقَّق

```powershell
.\.venv\Scripts\python.exe -m streamlit run app.py
```

أو نفس الأمر مع الخادم بدون فتح متصفح النظام تلقائياً:

```powershell
.\.venv\Scripts\python.exe -m streamlit run app.py --server.headless true --server.port 8501
```

الناتج المُلاحظ:

```
Local URL: http://localhost:8501
```

افتح المتصفح على: **http://localhost:8501**

عنوان تبويب الصفحة: `Stock Tracker`.

## إجراء الاختبار

1. انتظر اكتمال التحميل (الخلفية الداكنة + العنوان + الشريط الجانبي).
2. القيمة الافتراضية في الشريط الجانبي: `AAPL`.
3. تحقق من ظهور:
   - العنوان `Stock Tracker`
   - العنوان الفرعي `Visualization for AAPL`
   - مخطط خطي لعمود الإغلاق
   - جدول أسفل المخطط (Date + Close/High/Low/Open/Volume)
4. غيّر الرمز في الشريط الجانبي ثم اضغط Enter (أو انقر خارج الحقل). Streamlit يعيد تشغيل السكربت بالكامل.

حالات اختُبرت فعلياً:

| الإدخال | النتيجة |
|---|---|
| `AAPL` (افتراضي) | مخطط + جدول لـ Apple |
| `msft` (أحرف صغيرة) | يعمل؛ الجدول يعرض أعمدة `MSFT` |
| `INTC` | يعمل |
| ` AAPL ` (مسافات) | يعمل عبر yfinance؛ العنوان يحتفظ بالمسافات |
| `NOTAREALTICKERXYZ123` | لا استثناء؛ مخطط شبه فارغ (`0.000000`) وجدول بدون صفوف |
| حقل فارغ | **ValueError: No objects to concatenate** يظهر في واجهة Streamlit |

## أخطاء شائعة

1. **ModuleNotFoundError: streamlit**  
   لم تُفعَّل البيئة الافتراضية أو لم تُثبَّت الحزم. استخدم مسار `.venv\Scripts\python.exe`.

2. **فشل `pip install -r requirements.txt`**  
   الإصدارات المثبتة غير متوافقة مع Python 3.12.

3. **تعارض Streamlit العام على الجهاز**  
   نسخة Streamlit العامة على Python 3.12 كانت تتعطل بسبب `starlette`. الحل: شغّل دائماً من `.venv`.

4. **ValueError عند الرمز الفارغ**  
   المشروع لا يتحقق من الإدخال قبل `yf.download`.

5. **بيانات قليلة (~شهر واحد)**  
   في yfinance 1.7.0 الاستدعاء `yf.download(ticker)` بدون `start`/`end` يستخدم الفترة الافتراضية **1mo**، وليس التاريخ الكامل.

6. **شبكة / Yahoo Finance**  
   التطبيق يعتمد على الإنترنت. انقطاع الشبكة أو تغيير واجهة Yahoo يمنع الجلب.

## حدود البيانات الخارجية

- المصدر: Yahoo Finance عبر مكتبة `yfinance` (ليست بورصة رسمية مباشرة).
- لا توجد مفاتيح API في المشروع.
- التأخير، الرموز غير المدرجة، والعُطل المؤقتة ممكنة.
- `auto_adjust=True` افتراضياً في النسخة الحالية؛ لذلك عمود `Adj Close` قد لا يظهر للرموز الصالحة، بينما يظهر في الجدول الفارغ لرمز غير صالح.
- الأعمدة في النسخة المختبرة للرمز الصالح: `Close`, `High`, `Low`, `Open`, `Volume` بفهرس متعدد المستويات `(السعر, الرمز)`.
- هذا التطبيق **ليس** منصة تداول ولا يقدم توصيات استثمارية.

## استكشاف الأعطال

| العرض | السبب المحتمل | الإجراء |
|---|---|---|
| الصفحة سوداء لثوانٍ | Streamlit لا يزال يحمّل | انتظر ثم حدّث |
| مخطط فارغ وجدول بدون صفوف | رمز غير موجود | جرّب رمزاً معروفاً مثل `AAPL` |
| Traceback في الصفحة | إدخال فارغ أو خطأ شبكة | أدخل رمزاً صالحاً؛ تحقق من الإنترنت |
| المنفذ 8501 مستخدم | عملية Streamlit سابقة | أغلق العملية أو غيّر المنفذ `--server.port 8502` |
| بيانات لا تطابق التوقع التاريخي الطويل | الفترة الافتراضية 1 شهر | هذا سلوك المكتبة الحالية وليس واجهة المستخدم |
