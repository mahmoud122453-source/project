# دليل التشغيل — تحليل بيانات المبيعات

هذا الدليل مبني على تشغيل المشروع الفعلي في بيئة Windows، وليس على افتراضات README فقط.

## الحالة بعد التحقق

- نقطة الدخول: `sales-analysis.py`
- الأمر الموثَّق في README: `python sales-analysis.py` — صالح بعد تصحيح ملف CSV
- التشغيل الأصلي **قبل** تصحيح CSV: فشل بـ `KeyError: 'Sales'`
- التشغيل **بعد** إزالة السطر غير الصالح من `sales.csv`: نجح التحليل وطُلب عرض ثلاثة رسوم

## نسخة Python

- المُتحقق منها هنا: **Python 3.12.0**
- README يطلب Python 3.8 أو أحدث
- pip المُتحقق منه: **pip 26.1** (مع Python 3.12)

تحقق بنفسك:

```powershell
python --version
python -m pip --version
```

## الاعتماديات

ملف `requirements.txt` يحتوي فقط على:

```
pandas
matplotlib
```

بدون أرقام إصدارات.

المكتبات الموجودة مسبقاً في بيئة التحقق (لم يُنفَّذ تثبيت أعمى):

| الحزمة     | الإصدار المُتحقق |
|------------|------------------|
| pandas     | 2.1.3            |
| matplotlib | 3.8.2            |

تحقق:

```powershell
python -c "import pandas; print(pandas.__version__)"
python -c "import matplotlib; print(matplotlib.__version__)"
```

إذا فشل الاستيراد فقط، ثبّت من الملف:

```powershell
python -m pip install -r requirements.txt
```

## أمر التشغيل

من مجلد المشروع الذي يحتوي `sales-analysis.py` و`sales.csv`:

```powershell
python sales-analysis.py
```

يجب أن يكون المجلد الحالي هو مجلد المشروع لأن المسار في الكود هو `"sales.csv"` (مسار نسبي).

## ما يُتوقع في الطرفية (بعد تصحيح CSV)

نص مطابق لما طُبع فعلياً في التشغيل الناجح:

```
✅ Data loaded successfully

📌 First 5 rows of data:
         Date Product Region  Sales
0  2025-01-01  Laptop  North   1200
1  2025-01-03   Phone  South    800
2  2025-01-05  Tablet   East    600
3  2025-01-07  Laptop   West   1500
4  2025-01-09   Phone  North   950

📌 Data Info:
RangeIndex: 12 entries, 0 to 11
أعمدة: Date, Product, Region, Sales
Date/Product/Region = object ، Sales = int64

📊 --- Basic Summary ---
Total Sales: 11850
Average Sales: 987.5
Maximum Sale: 2000
Minimum Sale: 300

Sales by Product:
Laptop    6500
Phone     3550
Tablet    1800

Sales by Region:
East     3700
North    2450
South    3000
West     2700

Monthly Sales:
2025-01    11850
```

`df.info()` يطبع الجدول ثم يعيد `None`، لذلك يظهر `None` بعد معلومات الإطار في الطرفية. هذا سلوك Pandas وليس خطأ في الحساب.

## الرسوم المتوقعة

الكود يستدعي `plt.show()` ثلاث مرات. في بيئة رسومية تظهر نوافذ منفصلة بالترتيب:

1. **شريطي** — العنوان `Sales by Product` — المحور س: Product — المحور ص: Total Sales — ألوان `skyblue`
   - Laptop = 6500 ، Phone = 3550 ، Tablet = 1800
2. **دائري** — العنوان `Sales by Region` — نسب مئوية `autopct='%1.1f%%'`
   - East 31.2% (3700) ، South 25.3% (3000) ، West 22.8% (2700) ، North 20.7% (2450)
3. **خطي** — العنوان `Monthly Sales Trend` — نقطة واحدة لأن كل التواريخ في يناير 2025
   - القيمة 11850 لفترة `2025-01`

أغلق كل نافذة للمتابعة إلى الرسم التالي. لا يوجد `plt.savefig()` في المشروع الأصلي؛ الرسوم لا تُحفظ كملفات.

## عيب CSV الأصلي (مُتحقق)

السطر الأول في المستودع الأصلي كان:

```
// This is just an sample data.
```

`pd.read_csv("sales.csv")` تعامل معه كاسم عمود وحيد. النتيجة:

- شكل الإطار: 13 صف × عمود واحد
- لا يوجد عمود اسمه `Sales`
- التوقف عند السطر 18: `KeyError: 'Sales'`

التصحيح الذي طُبّق هنا: حذف ذلك السطر والإبقاء على الترويسة `Date,Product,Region,Sales` ثم 12 صف بيانات كما في مثال README.

## أخطاء شائعة وحلولها

| العرض | السبب المُتحقق / المحتمل | ماذا تفعل |
|--------|---------------------------|-----------|
| `KeyError: 'Sales'` | سطر تعليق/`//` قبل الترويسة، أو أسماء أعمدة مختلفة | اجعل الصف الأول هو `Date,Product,Region,Sales` |
| `FileNotFoundError: sales.csv` | تشغيل السكربت من مجلد آخر | `cd` إلى مجلد المشروع ثم أعد الأمر |
| نوافذ الرسوم لا تظهر | خلفية Matplotlib غير تفاعلية (مثل `Agg`) | شغّل من بيئة سطح مكتب عادية؛ تحذير `FigureCanvasAgg is non-interactive` يعني أن الحساب اكتمل دون عرض نافذة |
| تحذير `identical low and high xlims` على الخط | مجموعة شهرية واحدة فقط (`2025-01`) | متوقع مع هذه العينة؛ ليس استثناءً يوقف البرنامج |
| تحذير `Tight layout not applied` على الخط | نفس سبب النقطة الواحدة مع `tight_layout()` | متوقع مع هذه العينة |
| `ModuleNotFoundError: pandas` أو `matplotlib` | المكتبة غير مثبتة | `python -m pip install -r requirements.txt` |
| قيم المجاميع تختلف | ملف CSV مختلف عن العينة المُتحقق منها | لا تفترض أرقام README؛ أعد `df["Sales"].sum()` على الملف الحالي |

## استكشاف أعطال سريع

1. تأكد أنك داخل المجلد الصحيح وأن الملفين موجودان جنباً إلى جنب.
2. اطبع الأعمدة: بعد التحميل يجب أن تكون `['Date', 'Product', 'Region', 'Sales']`.
3. إذا ظهر عمود اسمه يبدأ بـ `//` فملف CSV ما زال يحتوي سطر تعليق.
4. إذا اكتمل الطباعة دون نوافذ: تحقق من خلفية Matplotlib ومن أنك لم تغلق النوافذ فوراً عبر سكربت غير تفاعلي.
