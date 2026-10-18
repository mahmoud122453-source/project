# PROJECT_MAP

خريطة المشروع الحقيقي بعد الفحص والتشغيل. لا تفترض ملفات غير موجودة.

---

## Project Purpose

جلب الصفحة الأولى من `https://books.toscrape.com` واستخراج عناوين الكتب الظاهرة فيها وحفظها في `books.csv`.

المستودع الأصلي: https://github.com/oxylabs/web-scraping-data-parsing-beautiful-soup

---

## Folder Structure

```text
web-scraping-data-parsing-beautiful-soup-main
│
├── README.md
├── RUN_GUIDE.md
├── TEACHING_GUIDE.md
├── FILE_TEACHING_ORDER.md
├── PROJECT_MAP.md
│
└── src
    ├── scrape.py
    ├── parse.py
    ├── save.py
    ├── books.csv
    └── requirements.txt
```

لا يوجد مجلد tests، ولا config، ولا package Python باسم قابل للاستيراد، ولا `.vscode` داخل المشروع.

---

## File Structure

| المسار | النوع | الدور |
|---|---|---|
| `README.md` | توثيق أصلي | شرح المؤلف، إعداد، أمثلة |
| `src/scrape.py` | Python | جلب الصفحة |
| `src/parse.py` | Python | جلب + تحليل + طباعة العناوين |
| `src/save.py` | Python | جلب + تحليل + حفظ CSV |
| `src/books.csv` | بيانات ناتجة | عمود Title |
| `src/requirements.txt` | تبعيات | beautifulsoup4، pandas، requests |
| `RUN_GUIDE.md` | توثيق تعليمي | تشغيل بالعربية |
| `TEACHING_GUIDE.md` | توثيق تعليمي | خطة التدريس |
| `FILE_TEACHING_ORDER.md` | توثيق تعليمي | ترتيب الملفات |
| `PROJECT_MAP.md` | توثيق تعليمي | هذه الخريطة |

---

## Architecture

سكربتات مستقلة متدرجة. كل ملف يعيد خطوات الملف السابق ثم يضيف طبقة.

```text
[Website]
    │  HTTP GET
    ▼
[requests.Response]
    │  status_code / content
    ▼
[BeautifulSoup soup]
    │  find_all('article')
    ▼
[list titles]
    │  DataFrame
    ▼
[books.csv]
```

---

## Execution Flow

Entry points (لا يوجد `if __name__ == '__main__'`):

```text
python src/scrape.py
python src/parse.py
cd src && python save.py
```

الملف النهائي للتشغيل الكامل: `src/save.py`.

---

## Data Flow

```text
Website HTML
    ↓  requests.get
response.content  (bytes / HTML)
    ↓  BeautifulSoup(..., 'html.parser')
soup
    ↓  find_all('article')
articles  (ResultSet من وسوم article)
    ↓  article.h3.a.attrs['title'] داخل for
titles: list[str]
    ↓  pandas.DataFrame({'Title': titles})
data_frame
    ↓  to_csv('books.csv', index=False, encoding='utf-8')
books.csv
```

---

## Dependencies

من `src/requirements.txt` بعد التحديث المتوافق مع Python 3.12:

- `beautifulsoup4==4.14.3`
- `pandas==2.1.3`
- `requests==2.32.3`

الإصدارات الأصلية في المستودع كانت:

- `beautifulsoup4==4.8.2`
- `pandas==1.5.1`
- `requests==2.28.1`

---

## Libraries

| المكتبة | الاستيراد في الكود | الاستخدام الفعلي |
|---|---|---|
| requests | `import requests` | `requests.get`، `response.status_code`، `response.content` |
| BeautifulSoup | `from bs4 import BeautifulSoup` | إنشاء soup، `find_all`، تنقل الوسوم، `attrs` |
| pandas | `import pandas` | `DataFrame`، `to_csv` |

---

## Important Functions

لا يعرّف المشروع دوالًا خاصة. الدوال المستخدمة من المكتبات:

| الدالة | الملف | السطر التقريبي |
|---|---|---|
| `requests.get` | scrape.py / parse.py / save.py | 3 |
| `BeautifulSoup` | parse.py / save.py | 11 |
| `soup.find_all` | parse.py / save.py | 12 |
| `list.append` | parse.py / save.py | داخل الحلقة |
| `pandas.DataFrame` | save.py | 20 |
| `DataFrame.to_csv` | save.py | 21 |
| `print` | scrape.py / parse.py / save.py | رسائل وحالة |
| `exit` | الثلاثة | عند فشل status_code |

---

## Important Variables

| المتغير | أين | المعنى |
|---|---|---|
| `response` | الثلاثة | كائن استجابة HTTP |
| `soup` | parse.py / save.py | شجرة HTML المحللة |
| `articles` | parse.py / save.py | كل عناصر article |
| `titles` | parse.py / save.py | قائمة العناوين |
| `article` | الحلقة | بطاقة كتاب واحدة |
| `title` | الحلقة | نص عنوان الكتاب |
| `data_frame` | save.py | جدول عمود واحد |

---

## Output Files

| الملف | الأعمدة | عدد صفوف البيانات بعد الاختبار | encoding في الكود |
|---|---|---|---|
| `src/books.csv` | `Title` | 20 | utf-8 |

عدد أسطر الملف بما فيها الرأس: 21.

الحقل الوحيد المستخرج: عنوان الكتاب من HTML attribute `title` داخل `article > h3 > a`.
