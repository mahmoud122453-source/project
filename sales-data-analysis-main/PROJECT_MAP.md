# خريطة المشروع — Sales Data Analysis

التحقق من المستودع: https://github.com/ritheesh-chittimalla/sales-data-analysis  
الملفات الأصلية: `sales-analysis.py`، `sales.csv`، `requirements.txt`، `README.md`.

## المعمارية

مشروع سكربت واحد. ليست حزمة، ليست OOP، ليست API.

```
sales.csv  →  pandas.read_csv  →  DataFrame df
                                      ↓
                         فحص head / info
                                      ↓
                         إحصاءات عمود Sales
                                      ↓
              groupby Product | Region | شهر من Date
                                      ↓
                         Series.plot + matplotlib.pyplot.show
```

نقطة الدخول: `python sales-analysis.py`.

## بنية CSV بعد التصحيح المُتحقق

12 صف بيانات + صف ترويسة.

| عمود    | النوع بعد read_csv | ملاحظات |
|---------|---------------------|---------|
| Date    | object (نص)         | يُحوَّل لاحقاً إلى datetime |
| Product | object              | Laptop, Phone, Tablet |
| Region  | object              | North, South, East, West |
| Sales   | int64               | 300 … 2000 |

- قيم مفقودة: 0 في كل عمود
- صفوف مكررة بالكامل: 0
- تواريخ فريدة: 12، من 2025-01-01 إلى 2025-01-25
- قيم Sales بالترتيب: 1200, 800, 600, 1500, 950, 400, 2000, 700, 300, 1800, 1100, 500

قبل التصحيح: Pandas قرأ السطر `// This is just an sample data.` كعمود وحيد → لا `Sales`.

## تدفق DataFrame

```
pd.read_csv("sales.csv")
        ↓
df  (12 × 4)
        ↓
df.head()     → أول 5 صفوف للطباعة
df.info()     → الأنواع وNon-Null ثم قيمة الإرجاع None تُطبع
        ↓
df["Sales"]   → Series طولها 12
        ↓
sum 11850 | mean 987.5 | max 2000 | min 300
```

## تدفق التجميع (groupby)

لا يوجد `reset_index`. الناتج يبقى Series فهرسها اسم المجموعة.

### المنتج

```
df
 ↓
groupby("Product")
 ↓
["Sales"].sum()
 ↓
Laptop 6500 | Phone 3550 | Tablet 1800
```

صفوف المصدر:

- Laptop: 1200, 1500, 2000, 1800
- Phone: 800, 950, 700, 1100
- Tablet: 600, 400, 300, 500

### المنطقة

```
df
 ↓
groupby("Region")
 ↓
["Sales"].sum()
 ↓
East 3700 | North 2450 | South 3000 | West 2700
```

Pandas يطبع المناطق مرتبة أبجدياً حسب الفهرس (East, North, South, West) لا حسب ظهورها في الملف.

صفوف المصدر:

- North: 1200 + 950 + 300 = 2450
- South: 800 + 400 + 1800 = 3000
- East: 600 + 2000 + 1100 = 3700
- West: 1500 + 700 + 500 = 2700

### الشهر

```
df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
        ↓
df["Date"].dt.to_period("M")
        ↓
groupby(تلك الفترات)["Sales"].sum()
        ↓
Period 2025-01 → 11850
```

كل الصفوف في يناير 2025 → نقطة تجميع واحدة. لا `resample`.

## تدفق التصور

لا `plt.figure()` ولا `plt.savefig()` ولا `plt.legend()`. الشكل ينشأ من `Series.plot`.

```
sales_by_product.plot(kind="bar", figsize=(6,4), title="Sales by Product",
                      ylabel="Total Sales", xlabel="Product", color="skyblue")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

sales_by_region.plot(kind="pie", autopct='%1.1f%%', figsize=(6,6), title="Sales by Region")
plt.ylabel("")
plt.show()

monthly_sales.plot(kind="line", marker="o", figsize=(8,4), title="Monthly Sales Trend", ylabel="Sales")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
```

كل كتلة رسم محمية بنفس شرط وجود العمود المستخدم في التجميع.

مع شهر واحد: Matplotlib قد يحذّر من حدود محور س متطابقة، والرسم يظهر نقطة واحدة حول 11850 مع محور زمني موسَّع تلقائياً.

## كتل الكود للتدريس

| ملف | الأسطر | الغرض | مفاهيم سابقة | مفاهيم جديدة | صعوبة | طريقة |
|-----|--------|--------|---------------|---------------|--------|--------|
| sales.csv | كل الملف | البيانات | ملف نصي | صفوف/أعمدة CSV | مبتدئ | قراءة سطراً بسطر |
| sales-analysis.py | 1–2 | الاستيراد | تشغيل Python | import، اختصار pd/plt | مبتدئ | مفهوم أولاً ثم السطر |
| sales-analysis.py | 4–7 | التحميل | CSV | read_csv، DataFrame | مبتدئ | سطر بسطر |
| sales-analysis.py | 9–14 | الفحص | DataFrame | head، info | مبتدئ | تشغيل ومقارنة الطباعة |
| sales-analysis.py | 16–22 | الإحصاء | عمود Series | sum mean max min | مبتدئ | حساب يدوي ثم الكود |
| sales-analysis.py | 24–31 | groupby منتج/منطقة | اختيار عمود | groupby، in columns | متوسط | كتلة ثم تتبع الصفوف |
| sales-analysis.py | 33–36 | الشهر | groupby | to_datetime، dt، Period | متوسط | مفهوم أولاً |
| sales-analysis.py | 38–44 | شريط | Series المجمّعة | plot bar، xticks، show | متوسط | عرض ثم ربط بالأرقام |
| sales-analysis.py | 46–49 | دائرة | مجموع المناطق | pie، autopct | متوسط | نسبة من 11850 |
| sales-analysis.py | 51–55 | خط | تجميع شهري | line، marker، tight_layout | متوسط | إظهار محدودية نقطة واحدة |
| requirements.txt | 1–2 | الاعتماد | pip | أسماء الحزم | مبتدئ | عرض |
| README.md | كامل | التوثيق الأصلي | لا شيء | أمر التشغيل | مبتدئ | نقد مقابل التشغيل الفعلي |

## هيكل الملفات

```
sales-data-analysis-main/
├── sales-analysis.py      # السكربت الوحيد
├── sales.csv              # العينة (12 صف بعد التصحيح)
├── requirements.txt       # pandas, matplotlib
├── README.md              # توثيق المؤلف
├── RUN_GUIDE.md           # تشغيل مُتحقق (عربي)
├── TEACHING_GUIDE.md      # مسار التدريس
├── FILE_TEACHING_ORDER.md # ترتيب إعطاء الملفات
└── PROJECT_MAP.md         # هذه الخريطة
```
