# دليل التدريس — Stock Tracker Using Python

## هدف المشروع

تطبيق ويب بسيط يعرض **أسعار إغلاق تاريخية** لرمز سهم يدخله المستخدم، عبر:

1. واجهة Streamlit
2. جلب بيانات من Yahoo Finance باستخدام `yfinance`
3. عرض مخطط خطي وجدول Pandas

المشروع **لا** يتضمن تنبؤاً، ولا تعلّم آلة، ولا توصيات تداول.

المؤلف الأصلي للمستودع: [deepankarvarma/Stock-Tracker-Using-Python](https://github.com/deepankarvarma/Stock-Tracker-Using-Python). الملف التنفيذي الوحيد للتطبيق: `app.py`.

## المتطلبات السابقة للطالب

يجب أن يعرف الطالب قبل الدرس:

- تشغيل Python من الطرفية
- مفهوم المكتبة (`import`)
- السلسلة النصية والمتغير
- استدعاء دالة بمعامل

مفيد لكن غير إلزامي في البداية:

- DataFrame بشكل سطحي
- فكرة أن الواجهة الرسومية يمكن أن تكون سكربت Python يعاد تشغيله

## أهداف التعلم

بعد إكمال التسلسل يستطيع الطالب أن:

1. يشرح ما هو رمز التداول (ticker) كمفتاح نصي لجلب بيانات بعيدة.
2. يفرّق بين إدخال المستخدم في Streamlit واستدعاء المكتبة الخارجية.
3. يقرأ `yf.download(ticker)` ويربطه بـ DataFrame.
4. يشرح لماذا `st.line_chart(stock_data['Close'])` يرسم سلسلة زمنية.
5. يشرح لماذا `st.write(stock_data)` يعرض جدولاً دون `st.table`.
6. يصف نموذج إعادة التشغيل في Streamlit (لا توجد callbacks في هذا المشروع).
7. يحدّد غياب معالجة الأخطاء ويصوغ تمريناً لإضافتها **بدون** توسيع المشروع إلى منصة تداول.

## مفاهيم Streamlit المستخدمة فعلياً

| الاستدعاء | الدور في هذا المشروع |
|---|---|
| `st.set_page_config` | عنوان التبويب وأيقونة الصفحة |
| `st.title` | عنوان الصفحة `Stock Tracker` |
| `st.markdown` | CSS لخلفية بعيدة + عنوان HTML للمستوى 3 |
| `@st.cache_data` | تخزين نتيجة `get_stock_data` حسب قيمة `ticker` |
| `st.sidebar.text_input` | إدخال الرمز مع قيمة افتراضية `AAPL` |
| `st.line_chart` | مخطط خطي من عمود `Close` |
| `st.write` | عرض DataFrame كجدول تفاعلي |

**غير مستخدم** في الكود: `st.header`, `st.button`, `st.selectbox`, `st.error`, `st.warning`, `st.dataframe`, `st.table`. لا تُدرَّس كجزء من هذا المشروع إلا كمقارنة اختيارية لاحقاً.

## مفاهيم yfinance المستخدمة فعلياً

المستخدم **فقط**:

```python
yf.download(ticker)
```

غير مستخدم: `yf.Ticker()`, `.history()`, معاملات `start`/`end`/`interval` في الكود.

في النسخة المختبرة (yfinance 1.7.0):

- `period` الافتراضي عند غياب start/end: **1mo**
- `interval` الافتراضي: **1d**
- `auto_adjust=True`
- `multi_level_index=True` → أعمدة من مستويين `(Price, Ticker)`

## مفاهيم Pandas المستخدمة فعلياً

لا يوجد في `app.py` استدعاء مباشر مثل `head()`, `filter`, `sort`. العمليات الفعلية:

- استلام كائن `DataFrame` من `yf.download`
- اختيار عمود: `stock_data['Close']` (ينتج DataFrame بسبب الفهرس المتعدد)
- الفهرس الزمني `Date` يأتي من المصدر
- العرض عبر Streamlit وليس عبر طباعة Pandas

`import pandas as pd` موجود وغير مستخدم — نقطة تدريس عن الاستيراد غير الضروري.

## تدفق البيانات (كما في الكود)

```
المستخدم
  → st.sidebar.text_input  (ticker_input)
  → إعادة تشغيل سكربت Streamlit
  → get_stock_data(ticker_input)
  → yf.download(ticker)
  → شبكة / Yahoo Finance
  → pandas.DataFrame
  → stock_data['Close'] → st.line_chart
  → stock_data → st.write
```

## تسلسل التدريس (حسب الاعتماد المفاهيمي)

1. ما متتبع الأسهم؟ عرض أسعار تاريخية في صفحة ويب، وليس تداولاً.
2. ما رمز التداول؟ مثال تدريسي فقط: `AAPL`, `INTC` — بدون توصية.
3. ما البيانات الخارجية؟ المكتبة تتصل بالشبكة وتعيد جدولاً.
4. Streamlit كسكربت يُنفَّذ من الأعلى للأسفل عند كل تفاعل.
5. `st.sidebar.text_input` والقيمة الافتراضية.
6. الدالة `get_stock_data(ticker)` و`return`.
7. `yf.download` وما الذي تعيده (شكل الأعمدة كما قيس).
8. DataFrame: صفوف = تواريخ تداول، أعمدة = أسعار وحجم.
9. الفهرس `Date` مقابل عمود عادي.
10. اختيار `Close` للمخطط.
11. `st.line_chart`.
12. `st.write` للجدول الكامل.
13. `@st.cache_data` بعد فهم إعادة التشغيل.
14. غياب `try/except` وسلوك الرمز الفارغ/غير الصالح.
15. المسار الكامل من الإدخال إلى الشاشة.

تأجيل: MultiIndex بعمق، `auto_adjust`، Vega-Lite الداخلي في Streamlit، خيوط `threads` داخل yfinance.

## تمارين عملية (على الكود الموجود)

1. غيّر القيمة الافتراضية في `text_input` إلى رمز آخر معروف ولاحظ إعادة التشغيل.
2. اطبع `stock_data.columns` مؤقتاً بـ `st.write` لرؤية MultiIndex.
3. قارن `st.write(stock_data)` مع عرض `stock_data['Close']` فقط.
4. أدخل رمزاً غير صالح وسجّل ما يظهر (بدون إضافة منطق جديد أولاً).
5. أدخل حقلاً فارغاً وسجّل الاستثناء — ثم اقترح مكان فحص `if not ticker_input.strip()`.

## التحدي الختامي (محدود)

أضف **حدّاً أدنى** من التحقق:

- إذا كان الإدخال فارغاً بعد `strip`: أظهر رسالة عبر `st.warning` ولا تستدعِ `yf.download`.
- إذا كان `DataFrame` فارغاً: أظهر `st.error` ولا ترسم المخطط.

لا تُضف تنبؤاً ولا مؤشرات فنية ولا توصيات شراء/بيع.
