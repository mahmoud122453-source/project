# دليل التشغيل — ملخّص المقالات الإخبارية

هذا دليل تشغيل للمشروع الحالي كما هو على الجهاز. الأوامر التالية نُفّذت وتحققنا من نتيجتها.

المشروع تلخيص **استخراجي**: يختار جملاً موجودة داخل المقال. لا يولّد جملاً جديدة ولا يستخدم نموذجًا توليديًا.

## إصدار بايثون

- Python **3.12.0**
- pip داخل البيئة الافتراضية: **26.2.1**

الأمر الذي أظهر الإصدار:

```bash
python --version
```

## الاعتماديات الفعلية

من `Requirements.txt`، وبعد التثبيت داخل `.venv`:

| الحزمة | الإصدار المثبت |
| --- | --- |
| nltk | 3.8.1 |
| newspaper3k | 0.2.8 |
| spacy | 3.7.4 |
| lxml | 4.9.3 |
| lxml_html_clean | 0.4.4 |
| Pillow | 10.2.0 |
| requests | 2.31.0 |
| streamlit | 1.64.0 |
| click | 8.1.7 |

`newspaper3k` يجلب معه أيضًا `beautifulsoup4` و`feedparser` و`tldextract` وغيرها. خوارزمية التلخيص لا تستدعيها مباشرة.

`NLTK` يُستورد عند تشغيل الملف، ويُنزّل بيانات `punkt` و`punkt_tab`. تقسيم الجمل في التلخيص يتم عبر spaCy، لا عبر NLTK.

## البيئة الافتراضية

من مجلد المشروع:

```bash
python -m venv .venv
.venv\Scripts\activate
python -m pip install -r Requirements.txt
```

على PowerShell، إذا لم يُسمح بتفعيل السكربت، يمكن استدعاء المفسر مباشرة:

```bash
.venv\Scripts\python.exe -m pip install -r Requirements.txt
```

لا تستخدم بايثون النظام العامة لهذا المشروع. عليها نسخة Streamlit تتعطل بسبب تعارض `starlette`، بينما البيئة `.venv` تعمل.

## نموذج spaCy

الكود يحمّل النموذج عند الاستيراد:

```python
nlp = spacy.load("en_core_web_sm")
```

النموذج **مطلوب**. بدونه يتوقف `app.py` و`news_summarizer.py` قبل أي تلخيص، برسالة:

```text
OSError: [E050] Can't find model '...'
```

الإصدار المتوافق مع spaCy 3.7.4 هو **en_core_web_sm 3.7.1**.

الأمر الرسمي، بعد تثبيت `click==8.1.7`:

```bash
.venv\Scripts\python.exe -m spacy download en_core_web_sm
```

تحققنا من نجاحه. الرسالة الأخيرة:

```text
Download and installation successful
You can now load the package via spacy.load('en_core_web_sm')
```

مكونات النموذج المحمّلة: `tok2vec`, `tagger`, `parser`, `attribute_ruler`, `lemmatizer`, `ner`.

التلخيص يستخدم التقطيع إلى رموز، وحدود الجمل، والكيانات المسماة. لا يستخدم المتجهات ولا الجذع اللغوي.

### إذا فشل أمر التنزيل بخطأ 404

مع Click **8.5.0** وTyper **0.9.4** يمرّر سطر أوامر spaCy القيم المنطقية كنص `"False"`. النص غير الفارغ يُعد صحيحًا في بايثون، فيطلب pip عنوانًا غير موجود:

```text
https://github.com/explosion/spacy-models/releases/download/-en_core_web_sm/-en_core_web_sm.tar.gz
```

العلاج المتحقق منه:

```bash
.venv\Scripts\python.exe -m pip install click==8.1.7
.venv\Scripts\python.exe -m spacy download en_core_web_sm
```

`Requirements.txt` يثبت `click==8.1.7` حتى لا تتكرر المشكلة في تثبيت جديد.

تثبيت بديل تحققنا منه مباشرة:

```bash
.venv\Scripts\python.exe -m pip install https://github.com/explosion/spacy-models/releases/download/en_core_web_sm-3.7.1/en_core_web_sm-3.7.1-py3-none-any.whl
```

## تشغيل Streamlit

```bash
.venv\Scripts\python.exe -m streamlit run app.py
```

العنوان المحلي الذي ظهر:

```text
Local URL: http://localhost:8501
```

الواجهة عند الإقلاع:

- العنوان: News Article Summarizer
- حقل رابط المقال
- شريط عدد الجمل من **2** إلى **10**، والقيمة الابتدائية **5**
- زر Summarize
- تذييل باسم Hema Malini

## تشغيل وضع الطرفية

```bash
.venv\Scripts\python.exe news_summarizer.py
```

هذا الوضع يسأل عن عدد الجمل ثم عن الرابط. الرقم غير الصحيح يعود إلى 5. لا يقيّد الإدخال بين 2 و10؛ هذا القيد موجود في شريط Streamlit فقط. اكتب `quit` للخروج.

## مقال للتجربة

رابط عام نجح معه الاستخراج والتلخيص:

```text
https://techcrunch.com/2026/09/27/anthropics-ceo-is-about-to-have-dinner-with-president-trump/
```

النتيجة المقاسة مع 3 جمل:

- العنوان: Anthropic’s CEO is about to have dinner with President Trump
- الكلمات: 215
- الجمل: 7
- تاريخ النشر المعروض: 2026-09-27
- نسبة التخفيض: 57%

مقال أطول نجح أيضًا:

```text
https://techcrunch.com/2025/12/22/tech-layoffs-2025-list/
```

حوالي 7075 كلمة و306 جملة.

## حدود الروابط

لا تفترض أن كل رابط يعمل.

| نوع الرابط | ما حدث فعليًا |
| --- | --- |
| مقال TechCrunch | استخراج النص، التلخيص، الكيانات، والتاريخ |
| صفحة BBC News الرئيسية | نص قصير من الصفحة، وليس مقالًا كاملًا |
| مقالات BBC المختبرة | نحو 40–64 كلمة و1–3 جمل فقط |
| `https://example.com` | يلخّص نص الصفحة رغم أنها ليست خبرًا |
| دومين غير موجود | خطأ في `download()` بسبب فشل DNS |
| `https://httpbin.org/status/204` | `You must download() an article first!` |
| `https://httpbin.org/robots.txt` | `Could not extract text from this URL.` |
| Reuters | `401 Client Error: HTTP Forbidden` |

لا تحاول تجاوز تسجيل الدخول أو جدار الدفع أو CAPTCHA. رفض الموقع قرار من الموقع نفسه.

حقل المؤلفين في مقالات TechCrunch الحالية يخلط اسم الكاتب مع أجزاء من CSS. هذا سلوك `newspaper3k` على HTML الصفحة، وليس خطوة إضافية في خوارزمية التلخيص.

## أخطاء شائعة

1. **`ModuleNotFoundError: No module named 'log_code'`**  
   الملف كان غائبًا عن المستودع رغم أن `app.py` و`news_summarizer.py` يستوردانه. الملف موجود الآن في المشروع.

2. **نموذج spaCy غير مثبت**  
   الفشل يحدث عند `spacy.load`، خارج `try` داخل `summarize_news`. التطبيق لا يفتح.

3. **رابط فارغ**  
   تحذير: `Please enter a news article URL.`

4. **رابط لا يبدأ بـ `http://` أو `https://`**  
   تحذير: `URL must start with http:// or https://`

5. **الموقع يرفض الطلب الآلي**  
   تظهر رسالة `st.error` تبدأ بـ `Something went wrong:` ثم نص استثناء newspaper.

6. **Click 8.2 أو أحدث**  
   أمر تنزيل نموذج spaCy يطلب ملفًا غير موجود. ثبّت `click==8.1.7`.

7. **شريط الجمل أكبر من عدد جمل المقال**  
   المقياس `Reduced By` قد يصبح سالبًا. مثال متحقق: 10 جمل مختارة على مقال من 7 جمل تعطي **-43%**.

## استكشاف الأعطال

- تأكد أن الطرفية داخل مجلد المشروع، لأن السجلات تُكتب إلى `log_files/` نسبةً لمجلد التشغيل.
- إذا تغيرت الواجهة ولم تظهر النتيجة، أعد تشغيل Streamlit. تحميل النموذج يتم مرة عند استيراد `news_summarizer`.
- راجع `log_files/app_streamlit.log` و`log_files/news_summarizer.log`. السجلات تسجل الرابط عمدًا. لا تلصق روابط خاصة في تقارير عامة.
- أول تشغيل يحتاج شبكة لتنزيل بيانات NLTK إذا لم تكن موجودة. على هذا الجهاز نجح `punkt` و`punkt_tab`.
