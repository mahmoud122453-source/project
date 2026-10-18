# دليل التشغيل — Professional Language Translator

هذا الدليل يصف التشغيل الذي تم التحقق منه على هذا الجهاز في 28 سبتمبر 2026.

## البيئة التي تم التحقق منها

| البند | القيمة |
| --- | --- |
| نظام التشغيل | Windows 10 (10.0.19045) |
| Python | 3.12.0 |
| pip داخل البيئة الافتراضية | 26.2.1 |
| Tkinter | 8.6 (مكتبة قياسية) |
| googletrans | `4.0.0-rc1` (يظهر في `pip show` كـ `4.0.0rc1`) |
| httpx | `0.13.3` (تبعية يثبّتها هذا الإصدار من googletrans) |

لا يوجد ملف `requirements.txt` في المستودع. التبعية الوحيدة التي يذكرها README هي:

```text
googletrans==4.0.0-rc1
```

لا تثبّت إصدارًا آخر. هذا الإصدار يثبت `httpx==0.13.3` معه. لا ترفع إصدار `httpx` بشكل منفصل.

## البيئة الافتراضية

من مجلد المشروع:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install "googletrans==4.0.0-rc1"
```

هذان الأمران نُفّذا بنجاح على هذا الجهاز.

المجلد `.venv` بيئة محلية للتشغيل. ليس جزءًا من الكود الأصلي للمشروع.

للتحقق من الإصدار:

```powershell
.\.venv\Scripts\python.exe -m pip show googletrans
```

النتيجة المتوقعة: `Version: 4.0.0rc1`.

## متطلب الإنترنت

الترجمة لا تعمل دون اتصال.

`translator.py` ينشئ `Translator()` من `googletrans`. الإعداد الافتراضي لهذه المكتبة يستخدم المضيف `translate.google.com`. هذه واجهة غير رسمية لموقع الترجمة، وليست Google Cloud Translation API.

تم التحقق:

- طلب إلى `https://translate.google.com` أعاد الحالة `200`.
- استدعاء `translate()` أعاد نصًا مترجمًا فعلًا.
- عند توجيه عنوان الخدمة إلى مضيف غير موجود، ظهرت الرسالة `Translation failed` مع الخطأ `[Errno 11001] getaddrinfo failed`.

## أمر التشغيل الذي تم التحقق منه

من مجلد المشروع:

```powershell
.\.venv\Scripts\python.exe translator.py
```

النتيجة التي تم التحقق منها:

- تظهر نافذة بعنوان `Professional Translator - Jaweid Moraadi`.
- القياس `650x550`.
- النافذة غير قابلة لتغيير الحجم.
- إغلاق العملية يغلق النافذة.

نقطة الدخول هي نهاية `translator.py`:

```python
if __name__ == "__main__":
    root = tk.Tk()
    app = ProfessionalTranslatorApp(root)
    root.mainloop()
```

## ماذا تظهر الواجهة

- مربع `Enter Text`
- قائمة واحدة للغة الهدف فقط: `Select Target Language`
- زر `Translate`
- زر `Clear`
- مربع `Translated Text`

لا يوجد اختيار للغة المصدر في الواجهة. `translate()` يُستدعى بمعامل `dest` فقط، لذلك تستخدم المكتبة القيمة الافتراضية `src='auto'`.

## اللغات في القائمة

| ما يظهر في القائمة | الرمز المرسل إلى المكتبة |
| --- | --- |
| `en - English` | `en` |
| `fa - Persian` | `fa` |
| `ar - Arabic` | `ar` |
| `fr - French` | `fr` |
| `de - German` | `de` |
| `tr - Turkish` | `tr` |
| `ur - Urdu` | `ur` |

القيمة الابتدائية هي `en - English`.

## اختبارات لغات تم تنفيذها عبر الواجهة

| الاختبار | النتيجة |
| --- | --- |
| `Hello, how are you?` → Arabic | `مرحبا، كيف حالك؟` |
| `مرحبا كيف حالك؟` → English | `Hello, how are you?` |
| `Good morning` → French | `Bonjour` |
| `Bonjour le monde` → English | `Hello world` |
| `Guten Tag` → English | `Good day` |
| `Merhaba` → English | `Hello` |
| `Peace` → Persian | `صلح` |
| `Peace` → Urdu | `امن` |

لغة المصدر في هذه الاختبارات لم تُختَر من قائمة. المكتبة تعرّفها تلقائيًا. الواجهة لا تعرض لغة المصدر المكتشفة.

## اختبارات عربية

1. English → Arabic: النص الناتج المخزن في المربع هو `مرحبا، كيف حالك؟`.
2. Arabic → English: الإدخال `مرحبا كيف حالك؟` والناتج `Hello, how are you?`.
3. اليونيكود يُحفظ ويُقرأ من `tk.Text` بشكل صحيح.
4. المربع محاذى لليسار. المشروع لا يضبط اتجاهًا من اليمين إلى اليسار. لا تعتبر الواجهة واجهة RTL مكتملة.

## أعطال شوهدت أثناء التحقق

| الحالة | سلوك البرنامج |
| --- | --- |
| مربع الإدخال فارغ أو مسافات فقط | نافذة تحذير: `Please enter text to translate.` ولا يُستدعى المترجم |
| رمز لغة هدف غير صالح مثل `xx` | `Translation failed` ثم `invalid destination language` |
| تعذر الوصول إلى مضيف الترجمة | `Translation failed` ثم `[Errno 11001] getaddrinfo failed` |
| المكتبة غير مثبتة | `ModuleNotFoundError: No module named 'googletrans'` قبل فتح المنطق الداخلي للترجمة |

القائمة `readonly`، لذلك المستخدم لا يستطيع اختيار لغة خارج اللغات السبع من الواجهة نفسها.

## استكشاف الأخطاء

1. `No module named 'googletrans'`  
   ثبّت الإصدار المحدد داخل البيئة نفسها التي تشغّل بها `translator.py`.

2. `Translation failed` مع خطأ شبكة أو `getaddrinfo`  
   تحقق من الاتصال. لا يوجد وضع ترجمة محلي في هذا المشروع.

3. `invalid destination language`  
   الرمز يجب أن يكون الجزء الذي قبل ` - ` في نص القائمة، مثل `ar` وليس `Arabic`.

4. نتيجة فارغة مع نص عربي ظاهر بشكل غريب  
   اقرأ النص من المربع أولًا. إذا كانت السلسلة اليونيكود صحيحة والمظهر معكوس أو ملتصق باليسار، فالسبب عرض `tk.Text` وليس فشل الترجمة.

5. لا تغيّر محرك الترجمة إلى مكتبة أخرى إذا فشلت الخدمة. العطل هنا من الاتصال أو من واجهة `googletrans` غير الرسمية.
