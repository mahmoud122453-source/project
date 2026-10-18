# دليل تدريس مشروع استخراج البيانات من الويب

مشروع تدريسي مبني على المستودع الأصلي:

https://github.com/oxylabs/web-scraping-data-parsing-beautiful-soup

حقوق المحتوى الأصلي تعود إلى Oxylabs. هذا الملف دليل تعليمي إضافي ولا يستبدل README الأصلي.

---

## هدف المشروع

أن يفهم الطالب دورة كاملة لاستخراج بيانات من صفحة ويب:

طلب HTTP ← استجابة HTML ← تحليل الصفحة ← استخراج قيم ← حفظ CSV

الموقع المستخدم: `https://books.toscrape.com`

البيانات المستخرجة فعليًا في الكود: **عنوان الكتاب فقط** (`Title`).

---

## مستوى الطلاب

مناسب لمستوى **مبتدئ إلى متوسط** بعد أساسيات Python.

لا يحتاج الطالب إلى معرفة شبكات عميقة أو DOM احترافي. يحتاج أن يقرأ HTML بسيطًا ويتبع مسار عنصر.

---

## Prerequisites

قبل المشروع يجب أن يعرف الطالب:

- تشغيل ملف `.py`
- `import`
- المتغيرات والنصوص
- القوائم `list`
- حلقة `for`
- شرط `if`
- القاموس بشكل مبسط (يُستخدم عند إنشاء DataFrame)
- فتح ملف CSV بعد إنشائه

مفيد لكن ليس شرطًا صارمًا:

- فكرة HTML tags
- فكرة الموقع والرابط URL

---

## Learning outcomes

بعد إنهاء المشروع يستطيع الطالب أن:

1. يشرح لماذا نستخدم `requests.get`.
2. يفسر معنى `status_code == 200`.
3. يفرّق بين HTML الخام والكائن `soup`.
4. يستخدم `find_all('article')` لإيجاد عناصر متكررة.
5. يصل إلى خاصية HTML عبر التنقل بين الوسوم: `article.h3.a.attrs['title']`.
6. يجمع النتائج في قائمة.
7. يحفظ القائمة في CSV عبر pandas.
8. يفرّق بين السكربتات الثلاثة كخطوات تعليمية متدرجة.

---

## Architecture

المشروع ليس تطبيقًا متعدد الطبقات. هو ثلاثة سكربتات مستقلة، كل واحد يكرر الخطوات السابقة ثم يضيف خطوة:

```text
scrape.py   HTTP فقط
    ↓
parse.py    HTTP + BeautifulSoup + طباعة
    ↓
save.py     HTTP + BeautifulSoup + DataFrame + CSV
```

لا توجد دوال معرّفة من المؤلف، ولا Classes، ولا ملفات إعداد، ولا قاعدة بيانات.

---

## Execution flow

في `src/save.py` (النسخة النهائية):

```text
1. import pandas, requests, BeautifulSoup
2. response = requests.get('https://books.toscrape.com')
3. if response.status_code != 200 → طباعة خطأ و exit(1)
4. print نجاح الجلب
5. soup = BeautifulSoup(response.content, 'html.parser')
6. articles = soup.find_all('article')
7. titles = []
8. for article in articles:
       title = article.h3.a.attrs['title']
       titles.append(title)
9. data_frame = pandas.DataFrame({'Title': titles})
10. data_frame.to_csv('books.csv', index=False, encoding='utf-8')
```

---

## Teaching order

1. نظرة على المشروع وREADME
2. الموقع وHTML الحقيقي
3. `scrape.py`: requests وstatus_code
4. مفهوم response.content
5. `parse.py`: إنشاء soup
6. `find_all('article')`
7. التنقل `h3.a.attrs['title']`
8. القائمة والحلقة
9. `save.py`: DataFrame وCSV
10. فتح النتيجة وعدّ الصفوف
11. معالجة الأخطاء الموجودة فقط (`status_code`)
12. ما الذي لم يُعالج بعد (مؤجّل)

---

## Files

| File | الدور التعليمي |
|---|---|
| `README.md` | السياق الأصلي وحقوق المشروع وشرح المؤلف |
| `src/scrape.py` | أول كود يشغّله الطالب |
| `src/parse.py` | جوهر BeautifulSoup |
| `src/save.py` | خط الأنابيب الكامل |
| `src/books.csv` | ناتج التشغيل وليس مصدر الشرح الأول |
| `src/requirements.txt` | المكتبات |
| `RUN_GUIDE.md` | التشغيل على Windows |
| هذا الملف | خطة المدرس |

---

## Code blocks

انظر التفصيل الكامل في `FILE_TEACHING_ORDER.md`. الملخص:

| Block | File | الغرض |
|---|---|---|
| B01 | scrape.py | import وGET |
| B02 | scrape.py | فحص status_code |
| B03 | parse.py | BeautifulSoup وfind_all |
| B04 | parse.py | الحلقة واستخراج title |
| B05 | save.py | DataFrame وto_csv |

لا تشرح ملفًا كاملًا في فيديو واحد إذا كان الطالب مبتدئًا. `parse.py` أهم ملف ويستحق أكثر من مقطع.

---

## Concepts

الموجودة فعليًا في الكود:

- import
- HTTP GET
- status_code
- exit
- print
- BeautifulSoup / html.parser
- find_all
- تنقل الوسوم (`.h3` `.a`)
- attrs
- list / append / for
- pandas.DataFrame
- to_csv مع index=False وencoding='utf-8'

غير موجودة في الكود (لا تُدرّس وكأنها جزء من المشروع):

- `find()`
- `select()`
- `get_text()`
- Classes
- دوال يعرّفها الطالب داخل المشروع
- Pagination
- استخراج السعر أو التقييم (موجودة في HTML لكن الكود لا يستخرجها)

---

## Exercises

1. شغّل `scrape.py` واقرأ الرسالة.
2. غيّر الرابط مؤقتًا إلى صفحة غير موجودة داخل نفس الموقع ولاحظ `Could not fetch the page`. أعد الرابط الأصلي بعد التجربة.
3. في `parse.py` اطبع `len(articles)` بعد `find_all`.
4. اطبع `article.h3.a.attrs` كاملًا لكتاب واحد.
5. قارن نص الرابط الظاهر داخل `<a>` مع قيمة `title`.
6. شغّل `save.py` وافتح CSV وعدّ العناوين.
7. اشرح لماذا نستخدم `index=False`.

---

## Common mistakes

- تشغيل `python3` على Windows
- البحث عن CSV في المجلد الخطأ
- الخلط بين `response.text` و`response.content` دون حاجة (المشروع يستخدم `content`)
- استخراج `.text` من `<a>` بدل `attrs['title']` فيحصل على عنوان مقصوص مثل `A Light in the ...`
- انتظار أسعار أو تقييمات بينما الكود يحفظ العنوان فقط
- تثبيت requirements القديمة على Python 3.12

---

## Challenges

- لماذا `find_all('article')` وليس `find_all('a')`؟
- ماذا يحدث لو حُذف فحص `status_code`؟
- لماذا `encoding='utf-8'` رغم أن العناوين هنا إنجليزية؟

---

## Homework

1. ارسم مسار HTML من `article` حتى `title`.
2. اكتب بجملتين الفرق بين `scrape.py` و`parse.py` و`save.py`.
3. افتح `books.csv` وأحضر أول عنوان وآخر عنوان.

---

## Final challenge

بدون تغيير هدف المشروع الأصلي: اطلب من الطالب أن يطبع عدد العناوين قبل الحفظ (`len(titles)`) ثم يتحقق أن عدد صفوف CSV يساوي هذا العدد.

تحدٍ اختياري متقدم (بعد المستوى الأساسي): استخراج حقل إضافي موجود في HTML مثل السعر `p.price_color` — هذا **ليس في الكود الأصلي**، لذلك يُقدَّم كإضافة لاحقة لا كجزء من المشروع الحالي.
