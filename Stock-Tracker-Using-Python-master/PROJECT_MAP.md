# خريطة المشروع — Stock Tracker

## البنية

```
Stock-Tracker-Using-Python-master/
├── app.py              نقطة الدخول الوحيدة للتطبيق
├── requirements.txt    تثبيت نُسخ قديمة (غير متوافقة مع Python 3.12 كما قيس)
├── README.md           وصف المستودع الأصلي
├── RUN_GUIDE.md        دليل تشغيل موثَّق
├── TEACHING_GUIDE.md
├── FILE_TEACHING_ORDER.md
└── PROJECT_MAP.md      هذا الملف
```

لا توجد وحدات بايثون إضافية، ولا مجلد `src/`, ولا إعداد YAML، ولا مفاتيح API.

**المعمارية:** سكربت Streamlit واحد. لا طبقة خدمات، لا قاعدة بيانات، لا مصادقة.

```
المتصفح  ↔  خادم Streamlit (منفذ 8501)  ↔  app.py
                                              ↕
                                         yfinance
                                              ↕
                                      Yahoo Finance (شبكة)
```

## تدفق Streamlit

1. عند فتح الصفحة يُنفَّذ `app.py` من السطر 1 إلى النهاية.
2. `st.set_page_config` ثم `st.title` ثم CSS عبر `st.markdown`.
3. تُعرَّف `get_stock_data` مع `@st.cache_data`.
4. `st.sidebar.text_input` يُرجع القيمة الحالية (`AAPL` أول مرة).
5. يُرسم عنوان HTML يستخدم `ticker_input`.
6. تُستدعى `get_stock_data(ticker_input)`.
7. يُرسم المخطط ثم الجدول.
8. عند تغيير النص في الشريط الجانبي (Enter أو فقدان التركيز) **يُعاد تشغيل الملف بالكامل**. لا يوجد `on_change` مخصص في الكود.
9. إذا تكرر نفس `ticker`، قد تُعاد النتيجة من الكاش بدل الشبكة.

## تدفق البيانات الخارجية

```
ticker_input : str
        ↓
get_stock_data(ticker)
        ↓
yf.download(ticker)
  — period الافتراضي في yfinance 1.7.0: 1mo (عند عدم تمرير start/end)
  — interval الافتراضي: 1d
  — auto_adjust=True
        ↓
طلب شبكة إلى مصدر Yahoo عبر المكتبة
        ↓
pandas.DataFrame أو استثناء
```

لم يُستخدم في المشروع: `Ticker()`, `history()`, قائمة رموز متعددة في الواجهة (رغم أن `download` يدعم قائمة).

## تدفق DataFrame

للرمز الصالح `AAPL` كما قيس:

- النوع: `pandas.DataFrame`
- الشكل التقريبي: نحو 22 صفاً × 5 أعمدة (فترة شهر تداول تقريباً)
- الفهرس: `Date`، النوع `datetime64[s]`
- الأعمدة (MultiIndex):

  `(Close, AAPL)`, `(High, AAPL)`, `(Low, AAPL)`, `(Open, AAPL)`, `(Volume, AAPL)`

- لا يظهر `Adj Close` في هذه الحالة بسبب الضبط التلقائي في المكتبة.

للرمز غير الصالح:

- `DataFrame` فارغ (`empty == True`)
- أعمدة تتضمن أيضاً `Adj Close`
- لا يرفع الكود استثناءً؛ الواجهة تعرض مخططاً شبه فارغاً وجدولاً بلا صفوف

للإدخال الفارغ:

- `yf.download('')` يرفع `ValueError: No objects to concatenate`
- Streamlit يعرض التتبع لأن لا `try/except` في `app.py`

## تدفق العرض

```
stock_data['Close']  →  st.line_chart
  المحور السيني: فهرس Date
  المحور الصادي: قيم الإغلاق
  السلسلة: اسم الرمز في المستوى الثاني من الأعمدة

stock_data          →  st.write
  جدول تفاعلي (سلوك Streamlit لعرض DataFrame)
  يعرض كل الأعمدة المُعادة وليس Close فقط
```

الفرق بين البيانات الخام والمعروضة:

- **الخام:** كل أعمدة OHLCV (ومع MultiIndex).
- **المخطط:** سلسلة الإغلاق فقط.
- **الجدول:** الإطار كاملاً كما أعادته المكتبة.

لا يوجد في الكود: تصفية، فرز، `head`/`tail`, حذف قيم ناقصة، إعادة تسمية أعمدة.

## الدوال

| الاسم | الموقع | الدور |
|---|---|---|
| `get_stock_data(ticker)` | `app.py` 21–24 | تغليف `yf.download` مع كاش Streamlit |

باقي الملف سكربت مستوى وحدة (module-level)، ليس دوالاً.

## مكونات غير موجودة (لا تُختلق)

- أزرار، قوائم اختيار، نطاق تواريخ في الواجهة
- Plotly / Matplotlib
- تنبؤ أو مؤشرات
- ملف إعدادات
- اختبارات pytest
