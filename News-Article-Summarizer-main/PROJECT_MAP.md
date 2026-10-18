# خريطة المشروع

الخوارزمية استخراجية. كل جملة في الملخص مأخوذة من النص المستخرج، ثم تُعاد إلى موضعها الأصلي.

## من الرابط إلى الملخص

```text
URL
 ↓
newspaper3k
 Article(url)
 download()
 parse()
 ↓
title / authors / publish_date / text
 ↓
spaCy: nlp(text)  →  doc
 ↓
تصفية الرموز
 الإبقاء إذا لم تكن الكلمة في STOP_WORDS
 وإذا لم يكن نص الرمز ضمن string.punctuation
 ↓
word_frequencies[word] += 1
 ↓
القسمة على أكبر تكرار
 ↓
لكل جملة: مجموع التكرارات المطبّعة لكلماتها
 ↓
sorted حسب الدرجة تنازليًا ثم أول N
 ↓
sorted حسب sentence.start
 ↓
" ".join(...)  →  summary
```

`N` في الواجهة هو شريط Streamlit من 2 إلى 10، والقيمة الابتدائية 5.

## من النص إلى الكيانات

```text
text
 ↓
doc = nlp(text)
 ↓
doc.ents
 ↓
الإبقاء على PERSON و ORG و GPE و EVENT و PRODUCT
 ↓
set  →  قص إلى 10 عناصر
 ↓
Key Entities في الواجهة
```

هذا المسار لا يؤثر في درجة الجملة.

## من القاموس إلى الشاشة

```text
المستخدم يلصق الرابط ويختار N ويضغط Summarize
 ↓
app.py يفحص الفراغ وبداية http
 ↓
summarize_news(url, num_sentences)
 ↓
قاموس فيه title, authors, publish_date, summary, keywords,
         word_count, sentence_count
 أو قاموس فيه error
 ↓
metrics + العنوان + الملخص + الكيانات
 أو st.error
```

## أين تُكتب الأحداث

```text
app.py        →  log_files/app_streamlit.log
news_summarizer.py  →  log_files/news_summarizer.log
```

يُسجل الرابط وعنوان المقال والأخطاء عمدًا. مستوى السجل DEBUG، لذلك تظهر أيضًا خطوات التكرار والتسجيل.

## ما لا يوجد في المسار

- لا استدعاء لـ `article.nlp()` ولا لملخص newspaper الجاهز.
- لا `Counter`.
- لا `heapq`.
- لا `token.is_stop`.
- لا توليد جمل جديدة.
- لا نموذج لغوي توليدي ولا مفتاح API.
