# ترتيب ملفات التدريس

السؤال الذي يجيب عنه هذا الملف:

**ما الملفات التي يجب أن أعطيها للذكاء الاصطناعي بالترتيب حتى يشرح المشروع للطلاب؟**

الترتيب مبني على اعتماد المفاهيم داخل الكود الحقيقي، وليس على الترتيب الأبجدي.

أعطِ الملفات واحدًا واحدًا. لا تعطِ `save.py` قبل أن يفهم الطالب `scrape.py` و`parse.py`.

---

## 0. README.md

1. File: `README.md`
2. Teaching Order: 0 (سياق قبل الكود)
3. Why now?: يعرّف هدف المشروع وموقعه ومكتباته دون قفز إلى التنفيذ.
4. Concepts: Web Scraping، Requests، BeautifulSoup، Books to Scrape
5. Prerequisites: لا شيء
6. What to explain: أن المشروع مثال تدريجي من Oxylabs، وأن الملفات الثلاثة مراحل وليست برامج منفصلة الأهداف.
7. What to postpone: تفاصيل pandas وCSV وencoding
8. Importance: عالية للسياق والحقوق، منخفضة ككود تنفيذي

---

## 1. src/requirements.txt

1. File: `src/requirements.txt`
2. Teaching Order: 1
3. Why now?: الطالب يحتاج أن يعرف ماذا يثبّت قبل التشغيل.
4. Concepts: dependency، pip، beautifulsoup4 / pandas / requests
5. Prerequisites: معرفة أن Python يحتاج مكتبات خارجية
6. What to explain: أسماء المكتبات الثلاث ولماذا كل واحدة موجودة
7. What to postpone: إدارة الإصدارات، wheels، الفرق بين pandas 1.x و2.x
8. Importance: متوسطة (تشغيل)، منخفضة (مفهوم الـ scraping نفسه)

---

## 2. src/scrape.py

1. File: `src/scrape.py`
2. Teaching Order: 2
3. Why now?: أول كود حقيقي: طلب الصفحة بدون تحليل.
4. Concepts: import، requests.get، URL، response، status_code، if، print، exit
5. Prerequisites: تشغيل ملف Python، شرط if
6. What to explain:
   - ما هو HTTP request
   - ماذا تعني 200
   - ماذا يفعل البرنامج إذا فشل الجلب
7. What to postpone: HTML parsing، القوائم، CSV، BeautifulSoup
8. Importance: عالية جدًا — نقطة الدخول

---

## 3. HTML الحي للموقع (ليس ملفًا في المشروع)

1. File: صفحة `https://books.toscrape.com` (عرض المصدر في المتصفح)
2. Teaching Order: 3
3. Why now?: قبل BeautifulSoup يجب أن يرى الطالب العنصر الذي سيبحث عنه الكود.
4. Concepts: HTML، tag، attribute، `article.product_pod`، `h3`، `a title`
5. Prerequisites: نجاح `scrape.py`
6. What to explain: أين يقع عنوان الكتاب ولماذا النص الظاهر داخل الرابط مقصوص
7. What to postpone: السعر، التقييم، الصور، الصفحات التالية
8. Importance: عالية — تربط الويب بالكود

---

## 4. src/parse.py

1. File: `src/parse.py`
2. Teaching Order: 4
3. Why now?: يضيف التحليل والاستخراج فوق نفس طلب HTTP.
4. Concepts: BeautifulSoup، html.parser، find_all، تنقل الوسوم، attrs، list، for، append
5. Prerequisites: scrape.py + رؤية HTML
6. What to explain:
   - `soup = BeautifulSoup(response.content, 'html.parser')`
   - `articles = soup.find_all('article')`
   - `title = article.h3.a.attrs['title']`
7. What to postpone: `find` / `select` / `get_text` لأنها غير مستخدمة في المشروع
8. Importance: الأعلى تعليميًا

---

## 5. src/save.py

1. File: `src/save.py`
2. Teaching Order: 5
3. Why now?: يكمل الدورة بحفظ الملف بعد أن صارت القائمة مفهومة.
4. Concepts: pandas.DataFrame، قاموس العمود `Title`، to_csv، index=False، encoding
5. Prerequisites: parse.py وقائمة `titles`
6. What to explain: لماذا نحفظ بدل الطباعة، أين يُكتب الملف، كيف نفتحه
7. What to postpone: تحليل بيانات، تنظيف نصوص، دوال pandas الأخرى
8. Importance: عالية للناتج النهائي

---

## 6. src/books.csv

1. File: `src/books.csv`
2. Teaching Order: 6
3. Why now?: دليل أن الاستخراج نجح. ليس ملفًا تُشرح منه الخوارزمية.
4. Concepts: CSV، صف رأس `Title`، صفوف البيانات
5. Prerequisites: تشغيل save.py
6. What to explain: عدد الصفوف، الاقتباس حول العناوين التي تحتوي فاصلة
7. What to postpone: معالجة CSV يدويًا أو مكتبات csv المعيارية (غير مستخدمة)
8. Importance: متوسطة — تحقق ومخرجات

---

## 7. ملفات المدرس (لا تُعطى للطالب في الحصة الأولى)

| File | متى |
|---|---|
| `TEACHING_GUIDE.md` | تحضير المدرس فقط |
| `FILE_TEACHING_ORDER.md` | هذا الملف — للمدرس / للذكاء الاصطناعي الشارح |
| `PROJECT_MAP.md` | مرجع سريع للمدرس |
| `RUN_GUIDE.md` | يُعطى عند التشغيل على أجهزة الطلاب |

---

## جملة جاهزة لنموذج الذكاء الاصطناعي الشارح

استخدم هذا الترتيب عند طلب الشرح للطلاب:

1. `README.md` — السياق فقط
2. `src/scrape.py` — HTTP
3. مصدر صفحة Books to Scrape — HTML
4. `src/parse.py` — BeautifulSoup والاستخراج
5. `src/save.py` — CSV
6. `src/books.csv` — التحقق من الناتج

لا تبدأ بـ `save.py` كاملًا في أول شرح.
